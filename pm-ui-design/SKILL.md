---
name: pm-ui-design
description: >-
  Define product-level UI design for PM workflow handoff. Use when Codex needs to turn a Linear issue, UX flow, product requirement, or existing feature improvement into concrete screen specs for new or changed visible screens, layout hierarchy, controls, states, UI copy placement, platform conventions, or design-review-ready PM comments before engineering.
---

# PM: UI Design

Turn approved or clearly stated product behavior into concrete screen-level UI specifications that engineering can implement.

## Boundary

- Own visible screen shape: screen inventory, layout hierarchy, sections, controls, default and important states, copy placement, and platform-specific UI decisions.
- Use `$pm-ux-state` first when the journey, involved screens, permissions, recovery behavior, or state model is unclear.
- Stay at the product UI layer. Do not implement code, choose architecture, or rewrite unrelated product scope.
- Generate image mockups only when explicitly requested or after the user approves the UI proposal. Do not attach generated images to a tracker without user approval.
- After approval, route to `$design` only when the user needs visual alternatives, a rendered artifact, an interactive prototype, design-system work, or a craft review. The textual proposal remains sufficient for ordinary engineering handoff.

## Input Routing

- Linear issue: read the issue, comments, acceptance criteria, linked docs, and current status before designing.
- UX flow or PM artifact: use it as the behavioral source of truth and do not silently rescope it.
- Raw requirement: route through `$pm` when the user problem, scope, or acceptance criteria are not clear.
- Existing feature improvement: inspect the current UI through repo files, screenshots, docs, running app behavior, or recent context when available.

If current UI cannot be inspected, state what was not inspected and proceed only with labeled assumptions or ask for screenshots/app context when the answer changes layout or copy.

## Platform Rules

- Prefer native platform patterns over custom novelty.
- For iOS, use familiar navigation stacks, tabs, lists, forms, sheets, confirmation dialogs, system controls, SF Symbols, safe-area-aware layouts, and Dynamic Type support.
- For macOS, use appropriate windows, sidebars, split views, toolbars, inspectors, menus, keyboard shortcuts, focus states, pointer behavior, table/list density, and settings surfaces.
- For cross-platform work, call out differences instead of forcing identical UI.
- For Apple-platform proposals or HIG-sensitive changes, read `references/apple-ui-checklist.md` before finalizing the proposal.

## Workflow

1. Confirm the product source of truth: issue, PM spec, UX flow, or approved requirement.
2. Identify every involved screen, including unchanged entry points.
3. Inspect current UI when modifying an existing surface.
4. Decide whether `$pm-ux-state` is needed before screen design.
5. Design each screen in two layers: user feel first, then concrete screen spec.
6. Specify layout, sections, controls, state variants, copy, accessibility notes, and platform differences.
7. Present the UI proposal for user approval.
8. When a visual artifact is needed, hand the approved proposal to `$design` and keep its artifact links and decisions with the PM record.
9. After approval, post the approved UI proposal as a tracker comment when tools allow, or provide exact comment text.

## Proposal Quality Bar

- Name every involved screen.
- Describe what the screen should feel like to the user before listing UI details.
- Specify section order, primary and secondary actions, controls, empty/loading/error/disabled states, and important copy.
- State what existing UI was inspected, or explicitly state that inspection was not possible.
- Keep open questions limited to decisions that would change layout, hierarchy, controls, or user trust.
- Include accessibility, localization, privacy, and platform differences where they affect the visible UI.

## Tracker Write Authority

Only post tracker comments after the user approves the UI proposal, unless the user explicitly asks for a draft only. Do not edit issue descriptions; `$pm-spec` owns canonical description updates.

When live tracker tools are unavailable, produce exact comment text and metadata suggestions instead of claiming updates were applied.

## Sub-Agent Contract

This skill is safe to run inline or as a bounded sub-agent. When delegated:

- Use only the request, provided sources, and directly referenced tracker or product context.
- Produce the UI proposal plus any allowed tracker comment or draft.
- Follow this skill's tracker-write rules; do not edit issue descriptions.
- Return sources read, writes applied or drafts, blockers, and open questions.

## Output

```markdown
## UI Proposal

### Source
- Input: <Linear issue ID, PM artifact, UX flow, or requirement>
- Platform: <iOS / macOS / web / cross-platform / unknown>
- Requirement status: Clear / Needs clarification
- UX dependency: None / Based on `$pm-ux-state` / Needs `$pm-ux-state` first

### Current UI
<What was inspected and what the current UI looks like. If not inspected, state the gap and assumptions.>

### Design Direction
<Native UI direction, hierarchy, and rationale.>

### Screens
#### <Screen name>
- User feel: <How the screen should feel for the target task.>
- Screen spec:
  - Overall appearance: <What the full screen looks like at first glance.>
  - Layout: <Navigation, major regions, hierarchy, spacing/density notes.>
  - Sections: <Top-to-bottom or leading-to-trailing order.>
  - Controls: <Primary actions, secondary actions, inputs, menus, toggles, destructive actions.>
  - States: <Default, empty, loading, error, disabled, permission, or other relevant states.>
  - Copy: <Titles, button labels, empty/error/help text, or copy direction.>
  - Accessibility: <Labels, Dynamic Type/scaling, keyboard/focus, contrast, motion notes.>

### Open Questions
- <Only decisions that change UI, scope, or user trust.>
```
