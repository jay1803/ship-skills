# Interaction and Screen Specification

Use for a user journey, state/recovery model, UI proposal or text handoff. The
primary artifact is a coherent flow/screen specification, not separate PM UX
and UI workflow stages. Honor a request limited to behavior, one screen or a
small layout change without expanding into the entire product.

## Source and policy boundary

Read the confirmed goal, user/role, affected surface and material policies.
Inspect existing flow and UI from available sources; say what could not be
inspected and ask only when that gap changes the result. Existing screenshots
can establish presentation, not hidden authentication or persistence behavior.

Keep product policy distinct from its presentation. For example, an approved
“explicit cancellation after fresh same-account login” can be designed into
screens, controls, states and recovery. It does not authorize cancel-on-login,
a new retention window, clearing local data or changing account identity rules.
Recommend an unresolved policy to PM with its exact impact; do not quietly
choose it inside empty/error states or confirmation copy.

## Build only the needed specification

- Map entry, main path, completion, exit/back/cancel and relevant recovery.
  Name screens to explain the flow, reusing current surfaces where appropriate.
- Include states that can occur and affect completion, trust or acceptance:
  loading, empty, error, denied, stale/offline, interrupted and success as
  applicable. For each material transition, explain its trigger, visible result,
  permitted action and recovery. Avoid speculative state inventories.
- Connect controls and copy to those transitions. Successful reauthentication
  is not automatically successful completion of the later requested operation.
  Do not treat a success mockup as evidence that an integration works.
- When screen detail is needed, specify hierarchy, primary/secondary controls,
  copy placement, important variants and changes to the existing UI. A flow-only
  request need not choose typography or detailed layout.
- Follow existing system and native platform patterns. Account for iOS touch,
  safe areas and Dynamic Type, or macOS keyboard/focus, windows and density when
  applicable. Include relevant accessibility and localization constraints;
  do not force identical platform layouts.

## Result

Use prose, a compact flow diagram, screen descriptions or a transition table
according to what clarifies the request. Include only relevant parts:

- source and confirmed product promise;
- inspected existing behavior/interface, with any material evidence gap;
- flow and affected screens;
- states: trigger -> visible behavior/action -> recovery;
- screen hierarchy, controls, copy and platform/accessibility differences;
- observable behavior for PM to incorporate into critical acceptance;
- unresolved material decisions and next owner.

A text result is sufficient for ordinary engineering handoff. Produce mockups,
alternatives or a prototype when requested or needed to settle a concrete design
question. Do not add an image-generation or attachment approval sequence to a
text-only request. Publication requires its own authorized destination.
