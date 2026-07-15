---
name: design-system
description: >-
  Extract, create, refine, and document reusable design-system foundations and components. Use when Codex needs to derive tokens from code, screenshots, UI kits, or brand sources; define color, typography, spacing, radius, elevation, motion, and responsive foundations; inventory component variants and states; identify inconsistencies; or update canonical design-system artifacts from an approved direction.
---

# Design: System

Turn visual evidence and approved decisions into a coherent, reusable source of truth.

## Authority and Boundary

- Own canonical design-family writes to token files, component inventories, and design-system documentation.
- Use source evidence in extraction mode. Do not silently replace inconsistent values with invented ones.
- Use an approved `$design-direction` in creation mode. Label proposals separately from observed values.
- Do not decide product behavior or implement production components. Route those decisions to PM and Dev.
- Treat audit requests as report-first. Change canonical files only when the user asks to create, update, normalize, or fix them.

## Modes

- **Extract:** derive the current system from code, brand files, UI kits, screenshots, or existing artifacts.
- **Create/refine:** formalize an approved direction into named foundations and usage rules.
- **Component inventory:** identify reusable components, composition, variants, states, content rules, and accessibility requirements.
- **Consistency audit:** find near-duplicates, off-scale values, missing states, and undocumented patterns.

## Workflow

1. Identify the authoritative sources and target format. Prefer the repository's existing naming, platform, and file type.
2. Record provenance for every extracted or proposed foundation.
3. Capture relevant foundations:
   - Color roles, surfaces, semantic colors, modes, and contrast pairs.
   - Typography families or platform styles, scale, weights, line heights, and tracking.
   - Spacing, sizing, grid, breakpoints, and density.
   - Radius, border, elevation, material, and opacity.
   - Motion durations, easing or spring vocabulary, and reduced-motion behavior.
   - Iconography, imagery, z-index, and other system-level primitives when present.
4. Inventory components by name, purpose, anatomy, composition, variants, sizes, states, tokens, content rules, accessibility, and platform differences.
5. Separate findings into observed system, inconsistencies, gaps, and recommended proposals.
6. Emit artifacts in the native format when possible: CSS variables, typed constants, JSON, platform assets, or Markdown documentation.
7. Verify that names are consistent, referenced values exist, semantic aliases point to primitives, and examples do not introduce new one-off values.
8. Route the completed system through `$design-review` for conformance and accessibility checks when delivery requires a quality gate.

## System Rules

- Prefer semantic aliases over component-specific raw values.
- Keep primitive and semantic layers distinct when the target platform supports them.
- Document light/dark or platform modes explicitly; do not assume automatic parity.
- Require complete interactive states for interactive components.
- Record deprecated values and migration notes instead of silently deleting them.
- Keep one canonical definition per concept and make exceptions explicit.

## Output

```markdown
## Design System Record

### Scope and Sources
- Mode:
- Sources inspected:
- Canonical artifacts:
- Target platform and format:

### Foundations
- Color:
- Typography:
- Spacing and layout:
- Shape and elevation:
- Motion:
- Other:

### Components
| Component | Purpose | Variants | States | Tokens | Accessibility | Gaps |
| --- | --- | --- | --- | --- | --- | --- |

### Findings
- Inconsistencies:
- Missing definitions:
- Proposed decisions:
- Deprecated values and migration:

### Writes and Verification
- Files created or changed:
- Checks performed:
- Open decisions:
- Next route:
```
