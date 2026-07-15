---
name: design-explore
description: >-
  Explore visual solutions for an approved screen, component, or flow. Use when Codex needs low-fidelity wireframes, high-fidelity visual alternatives, layout comparisons, component options, or multiple substantive design variations before selecting a direction. Produce comparable artifacts and a recommendation without changing product scope or behavior.
---

# Design: Explore

Make design choices visible and comparable before committing to a final artifact. Vary the dimensions that matter, not cosmetic details.

## Boundary

- Require a clear product goal and approved workflow or screen requirements.
- Explore layout, hierarchy, density, visual treatment, and presentation within those requirements.
- Route changes to user flow, state behavior, feature scope, or acceptance criteria back to PM.
- Create design artifacts only. Do not mutate production application code unless the user explicitly changes the task to implementation.

## Modes

- **Wireframe:** low-fidelity structure, information hierarchy, and interaction model.
- **Visual directions:** high-fidelity alternatives that compare typography, color, density, composition, or tone.
- **Component exploration:** variants and states for one reusable element.
- **Flow storyboard:** a small sequence of screens that compares presentation while preserving approved behavior.

## Workflow

1. Read the approved brief, `$pm-ux-state` / `$pm-ui-design` output, current interface, selected `$design-direction`, and existing design-system sources.
2. Define the exploration question in one sentence.
3. Select two to four meaningful axes. Examples: information hierarchy, density, layout model, navigation presentation, typography, visual tone, or component treatment.
4. Confirm the requested option count. When the user asks for options without a count, default to three: conservative, refined, and more exploratory.
5. Choose the smallest useful artifact medium:
   - Use simple diagrams or grayscale frames for structural questions.
   - Use raster mockups for visual-only concepts when image generation is available.
   - Use a single HTML or code canvas when live comparison, responsive behavior, or toggles materially help.
6. Build the alternatives with the same real content and constraints so the comparison is fair.
7. Annotate each option with its thesis, changed axes, strengths, risks, and what it deliberately preserves.
8. Recommend one option or a specific hybrid. Capture the user's selection and rejected directions for the next phase.

## Artifact Rules

- Keep wireframes visibly low fidelity; avoid brand polish that distracts from structure.
- Make high-fidelity options substantively different. A color swap alone is not a variation.
- Prefer one comparison artifact with labeled variants over scattered version files when practical.
- Add tweak controls only when the options share structure and live comparison is useful. Keep the control set small and use ordinary application state; do not assume a proprietary host protocol.
- Use real or plausible domain content. Mark unknown imagery and data honestly.
- Preserve accessibility and platform conventions even in exploratory work.

## Output

```markdown
## Design Exploration

### Question
- Surface:
- Approved behavior:
- Axes explored:
- Artifact:

### Options
#### Option A — <thesis>
- Changes:
- Preserves:
- Strengths:
- Risks:

#### Option B — <thesis>
- Changes:
- Preserves:
- Strengths:
- Risks:

### Recommendation
- Pick:
- Why:
- Useful hybrid, if any:

### Decision Record
- Selected:
- Rejected:
- New constraint discovered:
- Next route: refine / `$design-prototype` / `$design-system` / `$design-review`
```
