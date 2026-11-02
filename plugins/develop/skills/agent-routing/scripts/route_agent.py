#!/usr/bin/env python3
"""Validate caller-supplied routing decisions and assemble an executor binding.

Offline and deterministic: no network call, credential or dispatch. The caller
decides role, tier, effort, decision_state, risk and judgment_review. This
command applies the floors, chooses the executor and model from models.json,
resolves the profile and returns a proposal that the runtime still has to accept.
"""
import argparse
import json
from pathlib import Path
import sys
import tomllib

SKILL = Path(__file__).resolve().parents[1]
MODELS = json.loads((Path(__file__).resolve().parent / "models.json").read_text())
TIERS = ["fast", "standard", "deep", "critical"]
EFFORTS = ["low", "medium", "high", "xhigh", "max"]  # low only appears in older previous routes
ROLES = ["explorer", "worker", "reviewer", "architect", "operator"]
DECISIONS = {"role": ROLES, "tier": TIERS, "effort": EFFORTS[1:],
             "decision_state": ["settled", "unresolved"],
             "risk": ["ordinary", "excluded", "unknown"], "judgment_review": ["no", "yes"]}
EXECUTORS = ("codex", "claude-code")


class RoutingError(Exception):
    """A fixed reason code; the route is blocked and nothing is dispatched."""


def validate_input(facts):
    if not isinstance(facts, dict) or not isinstance(facts.get("request"), str) or not facts["request"].strip():
        raise RoutingError("request_required")
    if facts.get("lifecycle") not in ("controller", "bounded"):
        raise RoutingError("lifecycle_required")
    decisions = facts.get("decisions")
    if not isinstance(decisions, dict):
        raise RoutingError("decisions_required")
    for name, options in DECISIONS.items():
        if decisions.get(name) not in options:
            raise RoutingError("invalid_decision_" + name)
    facts.setdefault("permissions", "inherit")
    facts.setdefault("write_scope", "task")
    facts.setdefault("profile_fallback", "allowed")
    facts.setdefault("executor_policy", {"mode": "auto", "executor": "any", "fallback": "allowed"})
    if facts["permissions"] not in ("inherit", "read-only", "workspace-write", "external-write"):
        raise RoutingError("permissions_required")
    if not isinstance(facts["write_scope"], str) or not facts["write_scope"]:
        raise RoutingError("write_scope_required")
    if facts["permissions"] in ("workspace-write", "external-write") and facts["write_scope"] == "none":
        raise RoutingError("exact_write_scope_required")
    if not isinstance(facts.get("requirements"), list) or not all(isinstance(r, str) for r in facts["requirements"]):
        raise RoutingError("requirements_required")
    if facts.get("profile_fallback") not in ("allowed", "forbidden"):
        raise RoutingError("profile_fallback_required")
    policy = facts["executor_policy"]
    if (not isinstance(policy, dict) or policy.get("mode") not in ("auto", "prefer", "required")
            or policy.get("executor") not in ("any", *EXECUTORS) or policy.get("fallback") not in ("allowed", "forbidden")):
        raise RoutingError("executor_policy_required")
    independent = policy.setdefault("independent_from", "none")
    if independent != "none" and (not isinstance(independent, dict) or not independent.get("id")
                                  or independent.get("executor") not in EXECUTORS):
        raise RoutingError("independence_evidence_required")
    allowlist = facts.setdefault("availability_fallback", {}).setdefault("allowed_models", [])
    if not isinstance(allowlist, list) or not all(isinstance(m, str) for m in allowlist):
        raise RoutingError("invalid_model_fallback_allowlist")
    runtime = facts.get("runtime")
    if not isinstance(runtime, dict) or not runtime or set(runtime) - set(EXECUTORS):
        raise RoutingError("runtime_inventory_required")
    for item in runtime.values():
        if (not isinstance(item, dict) or not isinstance(item.get("models"), list)
                or not isinstance(item.get("profiles"), dict) or not isinstance(item.get("requirements"), list)
                or not isinstance(item.get("reasoning_levels"), list)):
            raise RoutingError("invalid_runtime_inventory")
        if item.get("model_selection") not in ("explicit", "application-default", "inherited"):
            raise RoutingError("runtime_model_selection_required")
        if set(item["profiles"].values()) - {"available", "unavailable", "not_attempted"}:
            raise RoutingError("invalid_profile_inventory")


def apply_floors(facts, decisions):
    """Raise tier and effort to the deterministic floors; never lower them."""
    tier, effort, applied = decisions["tier"], decisions["effort"], []

    def raise_tier(floor, why):
        nonlocal tier
        if TIERS.index(tier) < TIERS.index(floor):
            tier = floor
            applied.append(why + " -> " + floor)

    if decisions["risk"] == "excluded":
        raise_tier("deep", "protected-domain risk")
    elif decisions["risk"] == "unknown":
        raise_tier("standard", "unknown risk")
    if facts["lifecycle"] == "controller":
        raise_tier("standard", "controller lifecycle")
    if decisions["judgment_review"] == "yes":
        producing = facts.get("producing_capability_tier")
        if producing not in TIERS:
            raise RoutingError("producing_decision_tier_required")
        raise_tier(producing, "judgment review")
    if decisions["decision_state"] == "unresolved":
        raise_tier("deep", "unresolved decisions")
    if decisions["decision_state"] == "unresolved" or tier == "critical":
        minimum = "max"
    elif facts["lifecycle"] == "controller" or decisions["role"] in ("reviewer", "architect") or tier == "deep":
        minimum = "high"
    else:
        minimum = "medium"
    if EFFORTS.index(effort) < EFFORTS.index(minimum):
        effort = minimum
        applied.append("effort floor -> " + minimum)
    if tier == "fast" and EFFORTS.index(effort) > EFFORTS.index("high"):
        raise_tier("standard", effort + " effort")
    return tier, effort, minimum, applied


def eligible(executor, model, tier, facts, decisions):
    table = MODELS[executor]
    ceiling = table["ceilings"].get(model)
    if ceiling is None or TIERS.index(ceiling) < TIERS.index(tier):
        return False
    if decisions["decision_state"] == "unresolved" and model in table["settled_only"]:
        return False
    if model in table["explicit_bounded_worker_only"] and (
            facts["lifecycle"] != "bounded" or decisions["role"] != "worker"):
        return False
    return True


def bind_model(facts, decisions, executor, tier, effort):
    """Check one executor's capability; profile state never decides this."""
    runtime = facts["runtime"].get(executor)
    if runtime is None:
        raise RoutingError("executor_unavailable")
    independent = facts["executor_policy"]["independent_from"]
    if independent != "none" and independent["executor"] == executor:
        raise RoutingError("executor_independence_conflict")
    if not set(facts["requirements"]) <= set(runtime["requirements"]):
        raise RoutingError("runtime_requirements_unavailable")
    table = MODELS[executor]
    proposed = table["unresolved"] if decisions["decision_state"] == "unresolved" else table["tiers"][tier]
    required = facts.get("required_model")
    if required:
        if not eligible(executor, required, tier, facts, decisions):
            raise RoutingError("required_model_below_floor_or_incompatible")
        proposed = required
    reasoning = table["effort"].get(effort, effort)
    if reasoning not in runtime["reasoning_levels"]:
        raise RoutingError("reasoning_unavailable")
    model, fallback, selection = proposed, "none", runtime["model_selection"]
    if selection == "explicit" and model not in runtime["models"]:
        if required:
            raise RoutingError("required_model_unavailable")
        order = table["fallback_order"]
        stronger = order[order.index(model) + 1:] if model in order else []
        allowed = facts["availability_fallback"]["allowed_models"]
        replacements = [m for m in stronger if m in allowed and m in runtime["models"]
                        and eligible(executor, m, tier, facts, decisions)]
        if not replacements:
            raise RoutingError("model_unavailable")
        model, fallback = replacements[0], proposed + " -> " + replacements[0]
    if selection != "explicit":
        if required or facts.get("exact_binding_required"):
            raise RoutingError("model_override_not_permitted")
        observed = runtime.get("observed_model")
        if observed and not eligible(executor, observed, tier, facts, decisions):
            raise RoutingError("observed_default_below_floor")
    return {"executor": executor, "proposed_model": proposed,
            "requested_model": model if selection == "explicit" else selection,
            "model_selection": selection, "model_fallback": fallback, "reasoning": reasoning,
            "reasoning_fallback": "none" if reasoning == effort else executor + " maps " + effort + " -> " + reasoning}


def choose_executor(facts, decisions, tier, effort):
    policy = facts["executor_policy"]
    requested = policy["executor"]
    if requested == "any":
        candidates = list(facts["runtime"])
    else:
        candidates = [requested]
        if policy["mode"] != "required" and policy["fallback"] == "allowed":
            candidates += [e for e in facts["runtime"] if e != requested]
    first_error = None
    for executor in candidates:
        try:
            binding = bind_model(facts, decisions, executor, tier, effort)
        except RoutingError as error:
            first_error = first_error or error
            continue
        binding["executor_fallback"] = "none" if requested in ("any", executor) else requested + " -> " + executor
        binding["independence"] = "not-required" if policy["independent_from"] == "none" else "satisfied"
        return binding
    raise first_error


def resolve_profile(facts, role, binding):
    runtime = facts["runtime"][binding["executor"]]
    profile = facts.get("required_profile", role)
    state = runtime["profiles"].get(profile, "not_attempted")
    proposed, fallback = profile, "none"
    if state == "unavailable" or runtime.get("profile_selection") is False:
        if facts["profile_fallback"] != "allowed":
            raise RoutingError("profile_unavailable")
        proposed = "default"
        fallback = profile + " unavailable" if state == "unavailable" else "runtime has no profile selector"
    return {"requested_profile": profile, "proposed_profile": proposed, "profile_state": state,
            "profile_fallback": fallback}


def compare_previous(facts, role, tier, effort, minimum):
    """An escalation keeps scope and never silently downgrades; the owner counts it."""
    previous = facts.get("previous_route")
    if not previous:
        return None
    if not isinstance(previous, dict) or any(previous.get(key) != facts[key]
                                             for key in ("lifecycle", "permissions", "write_scope")):
        raise RoutingError("escalation_scope_conflict")
    if previous.get("role") != role and facts.get("role_change_authorized") is not True:
        raise RoutingError("role_change_authority_required")
    if previous.get("capability_tier") not in TIERS or previous.get("reasoning_depth") not in EFFORTS:
        raise RoutingError("invalid_previous_route")
    tier_step = TIERS.index(tier) - TIERS.index(previous["capability_tier"])
    effort_step = EFFORTS.index(effort) - EFFORTS.index(previous["reasoning_depth"])
    if tier_step < 0 or effort_step < 0:
        raise RoutingError("automatic_downgrade_forbidden")
    return {"capability_escalation": tier_step > 0,
            "effort_adjustment": effort_step > 0 and (tier_step == 0 or EFFORTS.index(effort) > EFFORTS.index(minimum))}


def route(facts):
    validate_input(facts)
    decisions = facts["decisions"]
    role = decisions["role"]
    if facts.get("required_role") and role != facts["required_role"]:
        raise RoutingError("required_role_conflict")
    tier, effort, minimum, applied = apply_floors(facts, decisions)
    adjustment = compare_previous(facts, role, tier, effort, minimum)
    binding = choose_executor(facts, decisions, tier, effort)
    binding.update(resolve_profile(facts, role, binding))
    binding.update(accepted_model="unknown", accepted_reasoning="unknown", accepted_profile="unknown")
    envelope = {"semantic_route": ("controller" if facts["lifecycle"] == "controller" else role) + "/" + tier,
                "lifecycle": facts["lifecycle"], "role": role, "capability_tier": tier, "reasoning_depth": effort,
                "decision_state": decisions["decision_state"], "risk": decisions["risk"],
                "judgment_review": decisions["judgment_review"], "selection_reason": decisions.get("reason", ""),
                "floors_applied": applied, "permissions": facts["permissions"], "write_scope": facts["write_scope"],
                "requirements": facts["requirements"], "executor_policy": facts["executor_policy"],
                "profile_fallback": facts["profile_fallback"], "availability_fallback": facts["availability_fallback"]}
    if adjustment is not None:
        envelope["adjustment"] = adjustment
    role_path = SKILL / "assets/roles" / (role + ".toml")
    return {"status": "routed", "routing_envelope": envelope, "runtime_binding": binding,
            "role_instructions": tomllib.loads(role_path.read_text())["instructions"].strip(),
            "task": {k: facts[k] for k in ("request", "evidence", "validation", "stop_conditions",
                                           "allowed_writes", "forbidden_writes") if k in facts}}


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", default="-", help="facts JSON file, or - for stdin")
    args = parser.parse_args()
    try:
        text = sys.stdin.read() if args.input == "-" else Path(args.input).read_text()
        result = route(json.loads(text))
    except RoutingError as error:
        result = {"status": "blocked", "reason": str(error)}
    except (OSError, ValueError):
        result = {"status": "blocked", "reason": "invalid_input_json"}
    except (KeyError, TypeError):
        result = {"status": "blocked", "reason": "invalid_input"}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "routed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
