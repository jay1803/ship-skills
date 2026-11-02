# Codex Adapter

Use after the helper selects `codex`. Model IDs live in
[`models.json`](../scripts/models.json); this table maps the binding onto the
actual tool. Read the tool schema and its usage rules first; a rule restricting
a field is not a missing field or an unavailable model.

| Surface | Model | Effort | Profile |
| --- | --- | --- | --- |
| Bounded spawn | `model` | `reasoning_effort` | Named role profile; some surfaces accept a model override only without full parent history, otherwise record the inherited binding |
| Visible task (`create_thread`) | Only when the tool rule permits, often only a model the user named; otherwise omit it and set `model_selection: application-default` in the runtime inventory | `thinking` | Usually none: carry the role instructions in the prompt and record that no profile loaded |
| Existing chat follow-up | A next-turn `model`/`thinking` override where the tool exposes one | Same | Unchanged |

The generated profiles omit model and effort, so pinned values cannot override
the binding. A recommendation or permission to delegate is not a user-named
model; do not change client defaults or switch surfaces to bypass a tool rule.
Application-default selection is not an availability fallback.

A successful call confirms only the arguments Codex accepted. A queued creation
is not a running task: at the first ready or active observation, read its
binding once and record what is exposed; otherwise keep `unknown`. Never infer
the effective model from a title, prompt or settings, and steering an active
turn does not change its model.

Spark is an explicit, text-only option for a bounded fast worker; it cannot take
screenshot-dependent work, diagnosis, control or review. Astra is never selected
or substituted automatically.
