# Research plugin

Research turns an open question into decision-ready evidence. It frames the
decision, chooses only evidence that can change it, runs appropriate specialist
work, synthesizes uncertainty, and independently reviews the result.

## Main entrypoints

- [`research`](skills/research/SKILL.md) owns question classification, planning,
  evidence waves, synthesis, and completion.
- Framing skills cover the question, decision model, hypothesis map, and
  evidence plan.
- Specialist skills cover desk, competitive, market, user, data, causal,
  forecasting, and experiment-design work.
- [`research-synthesis`](skills/research-synthesis/SKILL.md) integrates the
  evidence and [`research-review`](skills/research-review/SKILL.md) checks
  decision readiness.

## Workflow

```mermaid
flowchart TD
    Question[Open question] --> Classify[Classify question, mode, intent, and sources]
    Classify --> Resume{Reusable current evidence?}
    Resume -->|yes| Plan[Evidence plan]
    Resume -->|no| Frame[Question framing]
    Frame --> Model[Decision model and hypothesis map]
    Model --> Plan
    Plan --> Value{Would more evidence change the decision?}
    Value -->|no| Synthesis[research-synthesis]
    Value -->|yes| Wave[Specialist evidence wave]
    Wave --> Desk[Desk, market, and competitive]
    Wave --> Empirical[User, data, and causal]
    Wave --> Future[Forecasting and experiments]
    Desk --> Synthesis
    Empirical --> Synthesis
    Future --> Synthesis
    Synthesis --> Review[research-review]
    Review -->|gaps worth resolving| Plan
    Review --> Terminal[Decision ready, experiment ready, monitor, inconclusive, or blocked]
```

Research may inform Product, Project, or engineering work, but it does not make
their canonical writes or delivery decisions. Install with
`codex plugin add research@jay1803-ship-skills`. Source policy and terminal criteria
remain defined by the Skills.
