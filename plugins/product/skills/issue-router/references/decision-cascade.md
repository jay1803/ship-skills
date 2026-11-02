# Decision Cascade

This is the decision-selection and explicit adjudication contract for the
package-local issue-routing helper. It changes classifier selection, not task
authority, lifecycle ownership, independent technical Review or runtime bindings.

## Selection

The initial configured thresholds are **Jev 0.80** and **Luna 0.85**. They are
user-selected operating parameters, not calibrated correctness guarantees.
Apply them per finite-choice question on the same facts, policy and schema:

1. Accept Jev when its confidence is at least 0.80.
2. Batch only the remaining questions into one independent Luna Decisions
   request. Send the original facts, policy and questions, without Jev's answers
   or reasons. Questions do not consume sibling answers; dependent states must
   remain joint choices or separate evidence-bound requests.
3. Accept matching valid choices regardless of either confidence.
4. For a disagreement, accept Luna when its confidence is at least 0.85.
5. Otherwise return `needs-main-model` for the unresolved questions only. A
   missing optional Luna confidence can establish agreement, but cannot satisfy
   the high-confidence disagreement branch. Never fabricate probabilities.

Retain high-confidence Jev selections while resolving other questions. Equal
unknown/missing-evidence choices retain their existing evidence boundary; they
do not become successful delivery. Apply all original deterministic policy,
scope, capability, revision, history and budget checks after selection.

## Destinations and evidence

The primary request uses TypeSafe `jev-1.13.0` at
`https://api.typesafe.ai/v1/systemone`. Luna uses
`openai/gpt-6-luna-decisions` at
`https://openrouter.ai/api/alpha/decisions`; the client also recognizes the
verified resolved snapshot `openai/gpt-6-luna-decisions-20261006`. Other model
identities require an explicit adapter update, not silent substitution.

Jev credentials retain `TYPESAFE_API_KEY`, `JEV_API_KEY`, and `JEV_ENV_FILE`.
Luna reads `OPENROUTER_API_KEY` or `API_KEY` from `OPENROUTER_ENV_FILE` (default
`~/.config/openrouter/.env.local`) before an inherited `OPENROUTER_API_KEY`.
Files are parsed, never executed; credentials remain outside model input and
receipts. Check existing task authority for the selected destinations, bounded
evidence and paid calls; this contract and available credentials grant no new
permission. Keep raw private sessions and unrelated data out of requests.

`routing_evidence` preserves the original Jev receipt and answers. Its additive
`cascade` contains the original Luna receipt when called, configured thresholds,
final `decisions`, per-question `sources` and unresolved IDs. Use those final
decisions, not the original Jev `answers`, when inspecting a mixed result.
Provider receipts retain model identity, input/policy/question hashes, response
hash, complete parsed response, probabilities, usage and elapsed time. Do not
relabel an adjudicated answer as either provider's output.

Authentication, transport, invalid-response or policy failures remain `blocked`,
with the original primary evidence retained when Luna fails. They are not
low-confidence answers and do not silently select another provider or the main
model. Diagnose before an authorized new request; POSTs are not auto-retried.

## Main-model resolution

The packaged CLI can preserve its complete output in a new private JSON file
with `--output FILE --summary`. It refuses an existing/unwritable destination
before any provider call. The summary gives status and pending questions plus
the file's SHA-256; the file contains the unchanged full receipt and task.
Legacy stdout remains unchanged without these flags. A summary cannot replace
the original receipt. If saving fails after a request, retain the complete
result returned in stdout and inspect the partial file; do not repeat a paid
request to recover transport.

On `needs-main-model` (exit 2), save the unchanged output before dependent work.
Use the supplied `decision_task` to resolve only the listed questions. The
calling main model uses the original policy and observed facts, supplies an
allowed `choice` and a source-grounded `basis`, and preserves unknowns when
evidence is insufficient. It does not approve code or expand action authority. For a material agent-binding choice that still
cannot be resolved from policy/facts, the owning controller prepares supported
model/effort alternatives, tradeoffs and a recommendation for human adjudication,
then waits on only that dependent decision. Do not fill the template with a guess
or fabricate certainty to force dispatch. Clear policy choices need no new
confirmation; missing evidence/authority retains its original owner.

After the human decides, retain the instruction as the basis for the caller's
allowed resolution. Record its origin separately from Jev/Luna/model output.
Changed facts or explicit binding constraints require the appropriate fresh
route; unchanged bound questions can use the resolution path below. Human input
does not rewrite accepted provider choices or reset budgets.

Complete `resolution_template`, adding the exact saved `routing_evidence` as
its `receipt` field. Retain the template's `receipt_sha256`; never rewrite the
provider answers or accepted decisions. Run the same helper and input with:

```bash
python3 <installed-skill>/scripts/route_issue.py \
  --input facts.json --decision-resolution resolution.json
```

The helper verifies receipt
identity, all input/policy/schema bindings, both provider responses, accepted
decisions and the exact unresolved answer set, then reapplies its normal routing
checks **without another API request**. Partial answers, changed accepted
choices, unknown options or stale evidence stop. Material changes require a
fresh route, not editing old receipts. Hashes establish continuity, not the
truth of supplied facts or live authority; the owner still verifies actual
receipt provenance and current external state.

The main-model source and basis are recorded separately, with no invented
confidence. Do not independently reclassify an already accepted high-confidence
or agreed result. A current route remains a proposal until its owner verifies
the existing acceptance and runtime gates.

Interface sources: [TypeSafe confidence](https://docs.typesafe.ai/confidence),
[OpenRouter Decisions API](https://openrouter.ai/docs/api/api-reference/alphadecisions/submit-a-decisions-request)
and [Luna Decisions](https://openrouter.ai/openai/gpt-6-luna-decisions).
