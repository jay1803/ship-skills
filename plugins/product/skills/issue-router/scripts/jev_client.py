"""Jev-first decisions, independent Luna checks and bound main-model resolution."""
from __future__ import annotations

import hashlib
import copy
import http.client
import json
import math
import os
from pathlib import Path
import re
import shlex
import time

MODEL = "jev-1.13.0"
LUNA_MODEL = "openai/gpt-6-luna-decisions"
LUNA_IDENTITIES = {LUNA_MODEL, LUNA_MODEL + "-20261006"}
THRESHOLDS = {"jev": 0.80, "luna": 0.85}


class RoutingError(Exception):
    """Safe, fixed error codes only; never retain request headers or secrets."""

    def __init__(self, code, evidence=None):
        super().__init__(code)
        self.evidence = evidence


class MainModelRequired(RoutingError):
    def __init__(self, state, questions, policy, evidence):
        super().__init__("low_confidence_disagreement", evidence)
        self.task = {"facts": state, "policy": policy,
                     "questions": {k: questions[k] for k in evidence["cascade"]["unresolved"]}}


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


def luna_credential():
    path = Path(os.environ.get("OPENROUTER_ENV_FILE", "~/.config/openrouter/.env.local")).expanduser()
    try:
        lines = path.read_text().splitlines()
    except FileNotFoundError:
        lines = []
    except OSError:
        raise RoutingError("openrouter_credential_unreadable") from None
    values = {}
    for line in lines:
        match = re.match(r"^\s*(?:export\s+)?(OPENROUTER_API_KEY|API_KEY)\s*=\s*(.*)$", line)
        if match:
            try:
                parts = shlex.split(match[2], comments=True)
            except ValueError:
                raise RoutingError("openrouter_credential_format") from None
            if len(parts) != 1 or not parts[0]:
                raise RoutingError("openrouter_credential_format")
            values[match[1]] = parts[0]
    # A configured file wins over an inherited stale account key.
    key = values.get("OPENROUTER_API_KEY") or values.get("API_KEY") or os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise RoutingError("openrouter_credential_unavailable")
    return key


def choice(instructions, options):
    return {"type": "choice", "instructions": instructions,
            "criteria": options if isinstance(options, dict) else {item: item for item in options}}


def validate_answers(data, questions, *, luna=False):
    identities = LUNA_IDENTITIES if luna else {MODEL}
    if not isinstance(data, dict) or not isinstance(data.get("model"), str) or data["model"] not in identities:
        raise RoutingError("model_mismatch")
    if luna and data.get("provider") not in (None, "OpenAI"):
        raise RoutingError("luna_provider_mismatch")
    answers = data.get("answers")
    if not isinstance(answers, dict) or set(answers) != set(questions):
        raise RoutingError("invalid_answers")
    for name, question in questions.items():
        answer = answers[name]
        if not isinstance(answer, dict) or answer.get("type") != "choice":
            raise RoutingError("invalid_answer_type")
        probs = answer.get("probabilities")
        options = question["criteria"]
        selected = answer.get("choice")
        if not isinstance(selected, str) or selected not in options:
            raise RoutingError("invalid_choice")
        if probs is not None or not luna:
            if not isinstance(probs, dict) or set(probs) != set(options):
                raise RoutingError("invalid_probabilities")
            if any(type(p) not in (int, float) or not math.isfinite(p) or not 0 <= p <= 1 for p in probs.values()):
                raise RoutingError("invalid_probabilities")
            if abs(sum(probs.values()) - 1) > .02 or probs[selected] < max(probs.values()):
                raise RoutingError("invalid_choice")
        confidence = answer.get("confidence")
        if confidence is None and luna:
            continue  # Agreement can use a valid choice without a confidence field.
        if type(confidence) not in (int, float) or not math.isfinite(confidence) or not 0 <= confidence <= 1:
            raise RoutingError("invalid_confidence")
    return {name: answer["choice"] for name, answer in answers.items()}


def request_decisions(state, questions, policy, *, luna=False):
    # Fixed HTTPS host and no redirects prevent credentials reaching another host.
    # No retries: a timed-out POST may already have been charged.
    key = luna_credential() if luna else credential()
    provider = "openrouter" if luna else "typesafe"
    host, path = ("openrouter.ai", "/api/alpha/decisions") if luna else ("api.typesafe.ai", "/v1/systemone")
    payload = {"model": LUNA_MODEL if luna else MODEL, "state": {"routing_policy": policy, "facts": state},
               "questions": questions}
    body = json.dumps(payload, ensure_ascii=False).encode()
    if len(body) > 110_000:
        raise RoutingError("input_too_large")
    connection = http.client.HTTPSConnection(host, timeout=20)
    started = time.perf_counter()
    try:
        connection.request("POST", path, body=body,
                           headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
        response = connection.getresponse()
        raw = response.read(2_000_001)
        if response.status != 200:
            raise RoutingError(provider + "_http_" + str(response.status))
        if len(raw) > 2_000_000:
            raise RoutingError("response_too_large")
        data = json.loads(raw)
        if isinstance(data, dict) and data.get("error"):
            raise RoutingError(provider + "_api_error")
    except RoutingError:
        raise
    except (OSError, http.client.HTTPException, ValueError):
        raise RoutingError(provider + "_transport_or_json_error") from None
    finally:
        connection.close()
    selected = validate_answers(data, questions, luna=luna)
    evidence = {"provider": provider, "model": data["model"],
                "latency_ms": round((time.perf_counter() - started) * 1000, 1),
                "usage": data.get("usage"), "input_sha256": digest(state),
                "policy_sha256": digest(policy), "questions_sha256": digest(questions),
                "response_sha256": hashlib.sha256(raw).hexdigest(), "response": data,
                "answers": data["answers"]}
    return selected, evidence


def low_questions(evidence, questions):
    return {k: q for k, q in questions.items()
            if evidence["answers"][k]["confidence"] < THRESHOLDS["jev"]}


def select_cascade(evidence, questions):
    """Choose per question; preserve both providers' original answers."""
    decisions, sources, unresolved = {}, {}, []
    luna = evidence["cascade"].get("luna")
    for name in questions:
        primary = evidence["answers"][name]
        if primary["confidence"] >= THRESHOLDS["jev"]:
            decisions[name], sources[name] = primary["choice"], "jev"
            continue
        if luna is None:
            raise RoutingError("luna_receipt_required")
        secondary = luna["answers"][name]
        if secondary["choice"] == primary["choice"]:
            decisions[name], sources[name] = primary["choice"], "agreement"
        elif secondary.get("confidence") is not None and secondary["confidence"] >= THRESHOLDS["luna"]:
            decisions[name], sources[name] = secondary["choice"], "luna"
        else:
            unresolved.append(name)
    return decisions, sources, unresolved


def resume_resolution(state, questions, policy, resolution):
    """Reconsume the actual frozen receipt; no provider request on this path."""
    if not isinstance(resolution, dict) or set(resolution) != {"version", "receipt", "receipt_sha256", "answers"} \
            or type(resolution["version"]) is not int or resolution["version"] != 1:
        raise RoutingError("invalid_decision_resolution")
    evidence = resolution["receipt"]
    if not isinstance(evidence, dict) or digest(evidence) != resolution["receipt_sha256"]:
        raise RoutingError("decision_receipt_changed")
    evidence = copy.deepcopy(evidence)
    for key, expected in (("input_sha256", digest(state)), ("policy_sha256", digest(policy)),
                          ("questions_sha256", digest(questions))):
        if evidence.get(key) != expected:
            raise RoutingError("stale_decision_resolution")
    if evidence.get("provider") != "typesafe":
        raise RoutingError("invalid_primary_receipt")
    validate_answers(evidence.get("response"), questions)
    if evidence.get("model") != MODEL or evidence.get("answers") != evidence["response"]["answers"]:
        raise RoutingError("invalid_primary_receipt")
    cascade = evidence.get("cascade", {})
    if not isinstance(cascade, dict) or type(cascade.get("version")) is not int \
            or cascade["version"] != 1 or cascade.get("thresholds") != THRESHOLDS:
        raise RoutingError("invalid_cascade_receipt")
    low = low_questions(evidence, questions)
    secondary = cascade.get("luna")
    if not low or not isinstance(secondary, dict) or secondary.get("provider") != "openrouter":
        raise RoutingError("invalid_luna_receipt")
    for key, expected in (("input_sha256", digest(state)), ("policy_sha256", digest(policy)),
                          ("questions_sha256", digest(low))):
        if secondary.get(key) != expected:
            raise RoutingError("stale_decision_resolution")
    validate_answers(secondary.get("response"), low, luna=True)
    if secondary.get("model") != secondary["response"]["model"] or secondary.get("answers") != secondary["response"]["answers"]:
        raise RoutingError("invalid_luna_receipt")
    decisions, sources, unresolved = select_cascade(evidence, questions)
    if not unresolved or cascade.get("unresolved") != unresolved \
            or cascade.get("decisions") != decisions or cascade.get("sources") != sources:
        raise RoutingError("invalid_pending_decisions")
    answers = resolution["answers"]
    if not isinstance(answers, dict) or set(answers) != set(unresolved):
        raise RoutingError("incomplete_decision_resolution")
    for name, answer in answers.items():
        if not isinstance(answer, dict) or set(answer) != {"choice", "basis"} \
                or not isinstance(answer["choice"], str) or answer["choice"] not in questions[name]["criteria"] \
                or not isinstance(answer["basis"], str) or not answer["basis"].strip():
            raise RoutingError("invalid_main_model_answer")
        decisions[name], sources[name] = answer["choice"], "main-model"
    cascade.update(decisions=decisions, sources=sources, unresolved=[],
                   main_model_answers=copy.deepcopy(answers), prior_receipt_sha256=resolution["receipt_sha256"])
    return decisions, evidence


def evaluate(state, questions, policy, *, resolution=None):
    if resolution is not None:
        return resume_resolution(state, questions, policy, resolution)
    _, evidence = request_decisions(state, questions, policy)
    evidence["cascade"] = {"version": 1, "thresholds": dict(THRESHOLDS), "luna": None}
    low = low_questions(evidence, questions)
    if low:
        try:
            _, secondary = request_decisions(state, low, policy, luna=True)
        except RoutingError as error:
            evidence["cascade"]["failure"] = str(error)
            raise RoutingError(str(error), evidence) from None
        evidence["cascade"]["luna"] = secondary
    decisions, sources, unresolved = select_cascade(evidence, questions)
    evidence["cascade"].update(decisions=decisions, sources=sources, unresolved=unresolved)
    if unresolved:
        raise MainModelRequired(state, questions, policy, evidence)
    return decisions, evidence


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


def receipt_summary(result, path, serialized):
    """A bounded view; the file remains the lossless source for consumers."""
    omitted = {"routing_evidence", "decision_task", "resolution_template", "instructions",
               "task", "role_instructions", "dispatch_instructions"}
    summary = {k: v for k, v in result.items() if k not in omitted}
    if "issue_route" in summary:
        route = summary["issue_route"]
        summary["issue_route"] = {k: route[k] for k in
                                  ("version", "target", "selected", "pm_action", "completion_contract")
                                  if k in route}
    if result.get("status") == "needs-main-model":
        summary["pending_questions"] = result["decision_task"]["questions"]
        summary["resolution_template"] = result["resolution_template"]
    summary["receipt_file"] = str(path)
    summary["receipt_file_sha256"] = hashlib.sha256(serialized).hexdigest()
    return summary


def run(route, description):
    import argparse
    import sys
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--input", default="-", help="JSON file or stdin; never put credentials in the input")
    parser.add_argument("--decision-resolution", help="Main-model answers bound to the saved low-confidence disagreement receipt; no new API calls")
    parser.add_argument("--output", type=Path, help="Save the complete receipt to a new private JSON file; never overwrite")
    parser.add_argument("--summary", action="store_true", help="With --output, print status and pending questions instead of the full receipt")
    args = parser.parse_args()
    if args.summary and args.output is None:
        parser.error("--summary requires --output to preserve the complete receipt")
    output = None
    if args.output is not None:
        args.output = args.output.expanduser().absolute()
        try:
            # Reserve the destination before a paid request. O_EXCL also rejects
            # existing symlinks and preserves prior/partially written receipts.
            descriptor = os.open(args.output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            output = os.fdopen(descriptor, "wb")
        except OSError:
            print(json.dumps({"status": "blocked", "reason": "receipt_output_unavailable",
                              "next_action": "Choose a new writable output path. No provider request was made."}))
            return 2
    try:
        facts = read_input(args.input)
        if args.decision_resolution:
            resolution = json.loads(Path(args.decision_resolution).read_text())
            if not isinstance(resolution, dict):
                raise RoutingError("invalid_decision_resolution")
            result = route(facts, decision_resolution=resolution)
        else:
            result = route(facts)
    except MainModelRequired as error:
        result = {"status": "needs-main-model", "reason": str(error),
                  "routing_evidence": error.evidence, "decision_task": error.task,
                  "resolution_template": {"version": 1, "receipt_sha256": digest(error.evidence),
                                          "answers": {k: {"choice": None, "basis": None}
                                                      for k in error.task["questions"]}},
                  "next_action": "Save this original receipt. Use the main model only for the unresolved questions on the supplied facts/policy; add the unchanged routing_evidence as receipt to the completed resolution_template and rerun the same input with --decision-resolution. Do not dispatch, waive gates, invent evidence or repeat paid calls."}
    except RoutingError as error:
        result = {"status": "blocked", "reason": str(error), "next_action": "Resolve the named input/service boundary and rerun; do not reroute in the main model."}
        if error.evidence is not None:
            result["routing_evidence"] = error.evidence
    except (KeyError, TypeError, ValueError, OSError):
        result = {"status": "blocked", "reason": "invalid_input_or_policy", "next_action": "Correct input or package resources; do not reroute in the main model."}
    serialized = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if output is not None:
        try:
            with output:
                output.write(serialized)
                output.flush()
                os.fsync(output.fileno())
        except OSError:
            # Retain the original result in stdout if persistence failed. Never
            # repeat a provider request merely to recover this transport.
            print(json.dumps({"status": "blocked", "reason": "receipt_output_write_failed",
                              "receipt_file": str(args.output), "unpersisted_result": result,
                              "next_action": "Preserve stdout and inspect the partial file; do not automatically repeat the request."},
                             ensure_ascii=False, indent=2))
            return 2
    rendered = receipt_summary(result, args.output, serialized) if args.summary else result
    print(json.dumps(rendered, ensure_ascii=False, indent=2))
    return 0 if result.get("status") == "routed" else 2
