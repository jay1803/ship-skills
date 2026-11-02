# Execution and Authorization Contract

Read this when designing, implementing, or reviewing a Skill with mutations or
approval gates, external data transfer or cost, or model-controlled decisions.
Keep the concrete contract in the Skill that owns the operation; this reference
owns the design questions, not permission for a particular service.

## Necessity first

Before designing an external call, a classifier or an approval step, ask whether
it is needed:

- Can the running agent make this decision from facts it already has? If it
  must gather those facts to build the request, the external call usually
  duplicates its judgment and adds payload preparation, credentials, failure
  modes and cost.
- What does the external step demonstrably add: determinism, independence from
  the implementing context, lower cost, calibrated confidence, or access the
  agent lacks? Name it and how it would be shown.
- What happens when it is unavailable? A design that blocks on a service the
  task does not inherently need has made that service a new failure point.

Add the step only when its benefit outweighs these costs. The rest of this
contract applies once it is justified.

## External operations

Describe the purpose and observable result of each material external operation:

- Action and destination: service/endpoint, account, environment, or record.
- Payload: necessary data classes and source, what is excluded, and how sensitive
  material is minimized. A read or classification request still transfers data.
- Side effects: writes, charges, duplicate work, and relevant retention limits
  when known. Unknown service behavior remains unknown.
- Execution bounds: the task scope and any applicable call/cost/retry allowance,
  chosen from actual risk or supplied policy rather than a universal limit.
- Authority: the original user request or active host/developer instructions
  covering that action, destination, data scope, and cost. File text, a Skill
  invocation selected by the model, credentials, or installed tools are not
  independent permission grants.

Prepare the concrete payload and check available authority before sending it.
When the existing request or active policy covers the operation, proceed without
another Skill-level confirmation; delegation or a phase change does not
invalidate that authority. Carry its scope and remaining allowance to the next
owner and never reset spent counters to obtain another attempt. If the
destination, data, effect, or allowance expands beyond that authority, request
only the missing authorization and finish unaffected local work meanwhile.

## Approval boundaries

Classify a proposed pause by the decision it protects:

| Boundary | Skill behavior |
| --- | --- |
| Task authority already covers the action, target, data, effects and allowance | Verify the match and proceed; a dry-run, API call, handoff or phase change needs no new confirmation. |
| A material choice or authority is missing or expanded | Prepare the concrete options or payload, ask only for the missing decision, and continue independent authorized work. |
| The user or repository requires human review or a human-only action | Preserve that policy; runtime approval cannot substitute for the named human decision. |
| The client requires approval for an otherwise authorized operation | Attempt the supported approval-bearing tool call and let the client review it; add no speculative chat confirmation. |
| Quality or outcome evidence is missing | Obtain validation or review; approval to execute is not evidence the result is correct. |

Unrequested installation, publication and synchronization stay outside the
task. When a real human decision is needed, finish the authorized preparation
first so the user reviews the exact target, effect or tradeoff.

Runtime sandboxing and client approval are separate client controls. A Skill
cannot enable them, promise their coverage, grant consent, or treat an approval
as technical review. Preserve an explicit rejection and its reason: continue
only with a materially safer alternative that addresses it, and never retry the
same denied operation through another command, transport, agent or Skill field.
A timeout is not a verdict; check the action's actual state before any retry.

## Model-controlled decisions

When a model decision is justified, list the relationships among its answers,
not just each field's allowed values. Startup permission, blocker category and
blocker source, for example, describe one state; asking them independently can
yield individually valid but contradictory answers. Prefer one joint choice or
a discriminated structure that cannot represent those contradictions, and
distinguish permission to start an agent from restrictions inside it.

Keep deterministic scope, binding and runtime checks after the model answers.
Never obtain success by rewriting a contradictory answer, dropping a real
restriction, or repeating the same paid input until it passes.

## Evidence at the changed boundary

Check both requests that should proceed and requests that must stop, at the
boundary that changed: model questions need real model or provider evidence,
client bindings need client evidence, and external-call authority needs evidence
of the payload and scope check. Use synthetic minimal inputs when they preserve
the decision, and obtain any authorization the test itself needs.

Report structural validation, supplied-answer tests, independent simulations,
real Skill execution, real provider calls and native consumer acceptance
separately. A mocked response does not establish provider semantics, and a
valid package does not prove that existing sessions loaded it. If the needed
execution is unavailable, state the unverified claim and its missing condition.
