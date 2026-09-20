"""TypeSafe transport shared by the packaged routing commands (stdlib only)."""
from __future__ import annotations

import hashlib
import http.client
import json
import math
import os
from pathlib import Path
import re
import shlex
import time

MODEL = "jev-1.13.0"


class RoutingError(Exception):
    """Safe, fixed error codes only; never retain request headers or secrets."""


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def credential():
    for name in ("TYPESAFE_API_KEY", "JEV_API_KEY"):
        if os.environ.get(name):
            return os.environ[name]
    path = Path(os.environ.get("JEV_ENV_FILE", "~/.config/jev/.env.local")).expanduser()
    try:
        lines = path.read_text().splitlines()
    except OSError:
        raise RoutingError("credential_unavailable") from None
    values = {}
    for line in lines:
        match = re.match(r"^\s*(?:export\s+)?(TYPESAFE_API_KEY|JEV_API_KEY)\s*=\s*(.*)$", line)
        if match:
            try:
                parts = shlex.split(match[2], comments=True)
            except ValueError:
                raise RoutingError("credential_format") from None
            if len(parts) != 1 or not parts[0]:
                raise RoutingError("credential_format")
            values[match[1]] = parts[0]
    if not values:
        raise RoutingError("credential_unavailable")
    return values.get("TYPESAFE_API_KEY") or values["JEV_API_KEY"]


def choice(instructions, options):
    return {"type": "choice", "instructions": instructions,
            "criteria": options if isinstance(options, dict) else {item: item for item in options}}


def validate_answers(data, questions):
    if not isinstance(data, dict) or data.get("model") != MODEL:
        raise RoutingError("model_mismatch")
    answers = data.get("answers")
    if not isinstance(answers, dict) or set(answers) != set(questions):
        raise RoutingError("invalid_answers")
    for name, question in questions.items():
        answer = answers[name]
        if not isinstance(answer, dict) or answer.get("type") != "choice":
            raise RoutingError("invalid_answer_type")
        probs = answer.get("probabilities")
        options = question["criteria"]
        if not isinstance(probs, dict) or set(probs) != set(options):
            raise RoutingError("invalid_probabilities")
        if any(type(p) not in (int, float) or not math.isfinite(p) or not 0 <= p <= 1 for p in probs.values()):
            raise RoutingError("invalid_probabilities")
        selected = answer.get("choice")
        if (selected not in options or abs(sum(probs.values()) - 1) > .02
                or probs[selected] < max(probs.values())):
            raise RoutingError("invalid_choice")
        confidence = answer.get("confidence")
        if type(confidence) not in (int, float) or not math.isfinite(confidence) or not 0 <= confidence <= 1:
            raise RoutingError("invalid_confidence")
    return {name: answer["choice"] for name, answer in answers.items()}


def evaluate(state, questions, policy):
    # Fixed HTTPS host and no redirects prevent credentials reaching another host.
    # No retries: a timed-out POST may already have been charged.
    key = credential()
    payload = {"model": MODEL, "state": {"routing_policy": policy, "facts": state},
               "questions": questions}
    body = json.dumps(payload, ensure_ascii=False).encode()
    if len(body) > 110_000:
        raise RoutingError("input_too_large")
    connection = http.client.HTTPSConnection("api.typesafe.ai", timeout=20)
    started = time.perf_counter()
    try:
        connection.request("POST", "/v1/systemone", body=body,
                           headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
        response = connection.getresponse()
        raw = response.read(2_000_001)
        if response.status != 200:
            raise RoutingError("typesafe_http_" + str(response.status))
        if len(raw) > 2_000_000:
            raise RoutingError("response_too_large")
        data = json.loads(raw)
    except RoutingError:
        raise
    except (OSError, http.client.HTTPException, ValueError):
        raise RoutingError("typesafe_transport_or_json_error") from None
    finally:
        connection.close()
    selected = validate_answers(data, questions)
    evidence = {"provider": "typesafe", "model": data["model"],
                "latency_ms": round((time.perf_counter() - started) * 1000, 1),
                "usage": data.get("usage"), "input_sha256": digest(state),
                "policy_sha256": digest(policy), "answers": data["answers"]}
    return selected, evidence


def read_input(path):
    import sys
    try:
        text = sys.stdin.read() if path == "-" else Path(path).read_text()
        data = json.loads(text)
    except (OSError, ValueError):
        raise RoutingError("invalid_input_json") from None
    if not isinstance(data, dict) or not isinstance(data.get("request"), str) or not data["request"].strip():
        raise RoutingError("request_required")
    sources = data.get("evidence", [])
    if not isinstance(sources, list) or not all(isinstance(s, dict) and isinstance(s.get("source"), str)
            and isinstance(s.get("content"), str) for s in sources):
        raise RoutingError("invalid_evidence")
    return data


def run(route, description):
    import argparse
    import sys
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--input", default="-", help="JSON file or stdin; never put credentials in the input")
    args = parser.parse_args()
    try:
        result = route(read_input(args.input))
    except RoutingError as error:
        result = {"status": "blocked", "reason": str(error), "next_action": "Resolve the named input/service boundary and rerun; do not reroute in the main model."}
    except (KeyError, TypeError, ValueError, OSError):
        result = {"status": "blocked", "reason": "invalid_input_or_policy", "next_action": "Correct input or package resources; do not reroute in the main model."}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("status") == "routed" else 2
