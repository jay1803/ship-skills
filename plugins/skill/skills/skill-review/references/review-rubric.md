# Skill Behavior Review Rubric

Select surfaces from the mode, the changed decision and the governing contract.
These are review questions, not instructions to run every check or invent a new
threshold.

## Purpose and discovery

Does this Skill add repeatable, non-obvious help beyond ordinary agent capability?
Is there one primary job and one canonical owner, with realistic positive and
adjacent negative requests? Inspect discovery as the client presents it,
including the first sentence when descriptions are truncated. A catalog entry
does not prove selection, and selection does not prove the Skill was applied.
Check nearby Skills before recommending a new one or a split.

## Necessity and cost

- **Footprint against value:** is what a typical request reads before acting,
  plus its agents and external calls, proportional to the decisions the Skill
  changes? File length is not the measure; footprint against decision value is.
  A large footprint with a small difference from the minimal alternative is a
  finding.
- **External models and services:** does the running agent already hold the
  facts the call needs? What demonstrated benefit justifies payload
  preparation, credentials, cost and the new failure point? A service the task
  does not inherently need, made a blocking dependency, is a finding.
- **Bookkeeping and evidence mechanisms:** what fact does each hash, receipt,
  manifest, ledger or index establish? A mechanism whose own text concedes it
  cannot prove the claim, or one that checks the shape of evidence instead of
  the artifact itself, is ceremony.
- **Agents, phases and handoffs:** each must add information or a required
  independent check. Fan-out that a single pass with a checklist would match is
  a finding.
- **State and ownership:** does a called Skill carry policy its caller owns,
  such as budgets, rounds, retries or deferrals? Move it to the orchestrator.
- **Accretion:** the same prohibition repeated across files, exception layers
  on one rule, compatibility layers for ephemeral artifacts, defensive negation
  that restates a boundary already set, and rules justified only by one past
  incident.

Prefer corrections that delete, generalize, merge or move a rule to its owner
over ones that add text. Simplification cannot remove authority, necessary
ownership, required independence or required evidence.

## Instructions and execution

Can authorized normal work reach the intended outcome without invented
approvals, unnecessary phases or a completion dependency on itself? Inspect
conditional references, handoffs and the important constraints retained after
compaction. Verify the text separates requirements, defaults, examples and
proposals. Assess coupled decisions together: individually valid model answers
may be mutually inconsistent. Check both intended dispatch and legitimate
rejection; fail-closed handling alone does not prove useful execution.

For accumulated patches, follow the instruction path through canonical rules,
references and representative consumers, and demonstrate conflicting
requirements with a realistic request rather than judging each patch alone.

For model-controlled decisions, inspect real provider evidence for the changed
question before accepting a semantic-success claim; mocked answers prove only
deterministic handling.

## Authority and external operations

Use the sibling execution contract for action, destination, necessary data,
side effects, bounds, original authority and client limits. Verify that
same-scope authority continues without a new confirmation, missing authority
stops before external effects, and expanded destination, payload or allowance is
detected. Skills and credentials cannot grant consent. Look for unnecessary
friction as well as unauthorized execution, and classify each material approval
pause against the
[approval boundaries](../../skill-patterns/references/execution-contract.md#approval-boundaries):
it should protect a missing choice, added scope, explicit human policy or a real
runtime requirement, not a dry-run, phase, owner or file count. Denial recovery
must reduce the rejected risk; a timeout stays unresolved.

## Evidence and completion

Map claims to observations at the changed boundary. YAML parsing, package
closure, source-guided simulation, actual model behavior and consumer acceptance
answer different questions. Compare raw inputs and outputs with governing
expectations and preserve failed runs and unknowns. A packet, proposed binding
or release file does not prove accepted execution, installed content or session
reload. Prefer comparative evidence (no skill or previous version against the
candidate, with cost) for claims that the Skill helps.

## Test relevance and upkeep

Inspect affected cases against current requirements, dependencies and failure
modes, including their raw inputs. Distinguish obsolete assertions from useful
regression exclusions, and look for overlapping tests with no distinct failure
protection, implementation-mirroring checks, unreplayable inputs and historical
outputs treated as current proof. Recommend reuse, a specific repair,
consolidation or retirement with its behavioral reason; retire cases whose
mechanism no longer exists, after preserving reusable inputs under host policy.
Never refresh historical results or weaken a valid expectation to make a run
pass.

## Client and delivery compatibility

Confirm decision-relevant fields against the target client's current mechanisms
when they change; the portable text must preserve the boundary if a client
ignores another client's metadata. Check packaged references, one active Skill
identity, migration paths and representative consumers for shared changes. A
portable Skill must not embed a one-off issue ID, machine path, vendor secret or
new global gate.

## Finding priority

Lead with effects on user intent, authority, correctness and achievable outcome.
Then recurring cost: footprint, agents and external calls on every use. Then
discovery mistakes and maintainability. Use host severity policy when supplied.
A missing preferred heading, optional edge-case test or exact phrase is not a
defect. State concrete impact and evidence, and separate a demonstrable defect
from an untested counterfactual.
