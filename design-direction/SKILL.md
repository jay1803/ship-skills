---
name: design-direction
description: >-
  Define a concrete visual direction for an approved product brief or interface. Use when Codex needs to establish or refine typography, color, density, spacing rhythm, shape, elevation, imagery, iconography, motion character, and a distinctive visual signature before high-fidelity exploration or prototyping, especially when no usable brand or design system exists.
---

# Design: Direction

Create a visual language that is specific to the product, audience, task, and medium. Produce decisions that later design artifacts can follow without inventing new values ad hoc.

## Boundary

- Own visual language and craft principles, not product scope, user flow, screen inventory, or acceptance criteria.
- Use an approved PM brief or clearly stated user request as the behavioral source of truth.
- Inspect and follow an existing brand or design system before proposing change. Use `$design-system` to extract unclear foundations.
- Do not implement production UI. Route a selected direction to `$design-explore`, `$design-prototype`, or Dev.

## Workflow

1. Read the product brief, audience, primary task, platform, current UI, brand assets, references, and stated anti-references.
2. Decide whether the work is extension or greenfield.
   - Extension: preserve the established visual vocabulary and propose only intentional deltas.
   - Greenfield: define a new direction from the product's subject matter and audience.
3. Ask only for missing choices that would materially change the direction. Do not run a question quota.
4. Commit to concrete decisions on every relevant axis:
   - Intent: three useful adjectives plus one sentence describing the desired impression.
   - Typography: named families or platform styles, roles, weights, scale, and fallback plan.
   - Color: palette tone, primary and accent roles, semantic colors, surfaces, and contrast constraints.
   - Rhythm: spacing base, density, grid, alignment, and type rhythm.
   - Shape: radii, borders, elevation, materials, and component treatment.
   - Imagery and icons: source, style, cropping, and placeholder rules.
   - Motion: quiet, expressive, or physical; define purpose and reduced-motion behavior.
   - Signature: one memorable element grounded in the brief.
5. Test the direction against a representative small surface or concrete example when an artifact is in scope.
6. Run a specificity check and revise any choice that could have been pasted onto an unrelated product.

## Quality Bar

- Make every choice traceable to the product, audience, platform, or source material.
- Use real content or clearly marked placeholders; do not invent claims or filler to occupy space.
- Prefer a coherent system over isolated decoration.
- Treat gradients, emoji, fashionable fonts, card treatments, and expressive motion as choices requiring a reason, not universal bans or defaults.
- Establish legible hierarchy, accessible contrast, visible focus, scalable type, and reduced-motion behavior from the start.
- Spend boldness in one or two places; keep the rest disciplined.

## Output

```markdown
## Design Direction Brief

### Source
- Product brief:
- Audience and primary task:
- Platform and medium:
- Existing context inspected:
- Mode: extension / greenfield

### Direction
- Intent:
- Signature:
- Rationale:

### Foundations
- Typography:
- Color:
- Spacing and density:
- Grid and hierarchy:
- Shape and elevation:
- Imagery and iconography:
- Motion:
- Accessibility floor:

### Representative Application
<How the direction appears on one representative surface.>

### Guardrails
- Prefer:
- Avoid unless justified:

### Open Decisions
- <Only choices that materially affect later artifacts.>

### Next Route
<$design-explore, $design-system, $design-prototype, or Dev>
```
