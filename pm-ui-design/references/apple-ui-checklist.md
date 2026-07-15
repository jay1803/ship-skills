# Apple UI Checklist

Use this checklist while drafting Apple-platform UI proposals. Treat it as a working aid, not a substitute for current Apple Human Interface Guidelines.

## Native-First Checks

- Use platform-native navigation before custom navigation.
- Use system controls before custom controls.
- Match platform density: iOS touch-first and macOS pointer/keyboard-first.
- Keep iOS and macOS layouts related but not forced to be identical.
- Use SF Symbols only where the symbol meaning is obvious or labeled.
- Avoid decorative color as the only status indicator.
- Prefer system sheets, popovers, alerts, confirmation dialogs, menus, and settings patterns.
- Use progressive disclosure for advanced or rare controls.

## iOS Screen Checks

- Navigation title matches the current task or object.
- Primary action is visible but not overbearing.
- Destructive action uses clear confirmation.
- Empty states explain what happened and provide the next useful action.
- Loading states preserve layout when possible.
- Form rows, toggles, pickers, segmented controls, and lists use familiar placement.
- Toolbars use concise labels or obvious icons with accessibility labels.
- Layout works with safe areas, one-handed use where relevant, and Dynamic Type.

## macOS Screen Checks

- Window, sidebar, toolbar, inspector, and settings placement match the task.
- Toolbar items are stable and not overloaded.
- Menus and keyboard shortcuts exist for repeated commands when relevant.
- Selection, focus, hover, disabled, and drag states are described.
- Lists and tables use appropriate density and column behavior.
- Sheets are used for modal tasks tied to a window; separate windows are used for independent tasks.
- Empty and error states do not block the user from other available work.

## State Inventory

Consider whether each involved screen needs these states:

- Default
- Empty
- Loading
- Refreshing
- Error
- Offline or stale data
- Permission required
- Disabled or unavailable
- Editing
- Saving
- Saved or success
- Validation error
- Destructive confirmation
- Conflict or duplicate

Only include states that can actually occur.

## UI Copy Checks

- Titles are nouns or short task phrases.
- Primary buttons start with clear verbs.
- Error copy names the issue and the recovery action.
- Empty copy explains the absence without blaming the user.
- Confirmation copy names the destructive result.
- Labels are localizable and avoid overloaded metaphors.
- Help text is short and placed near the decision it supports.

## Proposal Quality Bar

- Every involved screen is named.
- Every screen has two layers: user feel first, then detailed screen spec.
- The screen spec describes overall appearance, layout, section count, and section order.
- Existing pages explain what is already present and exactly where new elements are added.
- Every section has appearance, state count, state details, and UI copy.
- Existing UI inspection is summarized, or the absence of inspection is explicit.
- Platform differences are called out.
- Accessibility and privacy moments are visible in the proposal.
- Open questions are only questions that would change the UI.

## Visual Mockup Checks

- Generate images only after the UI proposal is approved and the issue is updated or ready to update.
- Use the approved screen description as the prompt source.
- Keep every image atomic: one platform, one screen, one version or state.
- Never place iOS and macOS mockups in the same image.
- Never place multiple screens, variants, or before/after states in the same image.
- Label each generated image by platform, screen, and version or state.
- Preserve existing screen structure when the design modifies an existing page.
- Make the result look like a native iOS or macOS app screenshot.
- Ask the user to review generated images before attaching them to Linear.
- Attach only user-approved images to the ticket.
