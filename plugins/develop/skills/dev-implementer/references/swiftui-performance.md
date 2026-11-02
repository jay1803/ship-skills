# SwiftUI Performance

Read when a change touches a scrolling list or grid, a tab root, a screen that
stays mounted, or anything that updates often (streams, timers, scroll position,
geometry, image loading). Follow the repository's own patterns first; these
rules fill the gaps.

Most SwiftUI slowness measured in our apps was extra work, not slow drawing:
bodies re-evaluated for inputs that did not change, rows laid out that were not
on screen, and text measured more than once. An update should touch only the
views whose input changed.

## Containers and identity

- Unbounded or long collections use `List` or a `Lazy*Stack`, never a plain
  `VStack`/`HStack` inside a `ScrollView`. For a long feed prefer `List`: it
  reuses cells. A non-lazy stack lays out every loaded row on every change
  (the uikit-vs-swiftui benchmark: 2-3x memory and hundreds of hitches).
- `ForEach` uses a stable model id. Do not use indices, `id: \.self` on mutable
  values, ids created during `body`, or `.id(...)` to force a refresh.
- Bound what is mounted: page or window the data, and trim far rows when the
  list grows without limit.
- In a native `List`, avoid nested `NavigationLink` inside rows (it becomes row
  disclosure chrome); use a value route or a coordinator button.

## Invalidation

- Inputs passed to child views must compare equal when nothing changed. Do not
  create closures, `Binding(get:set:)`, namespaces, arrays or dictionaries
  fresh in `body` and pass them down: they never compare equal and redraw the
  whole subtree. Wrap actions in an `Equatable` struct, store bindings, and
  cache derived collections.
- Rows that do real work conform to `Equatable` on exactly what they draw and
  use `.equatable()`. Include the identity and version of the model a tap
  opens, or the row keeps a stale copy.
- Read fast-changing or global state (selected tab, scroll offset, focus,
  `openURL` and other environment values) in the smallest view or modifier
  that needs it, not in a screen's `body`. Read an environment value once in
  the container and pass the result down.
- Do not publish unchanged values: guard `@Published` / `@Observable` writes
  with an equality check. Watch for models whose `Equatable` compares only
  `id`; they hide content changes from that guard, so compare what is drawn.
- Keep `body` pure and cheap. Formatters, regexes, attributed-string parsing,
  sorting and grouping are built once (static, cached, or in the model), not
  per evaluation.

## Geometry and scroll position

- Do not have every row report its frame (`onGeometryChange`, preference keys,
  `GeometryReader`) into state that triggers a scroll correction. That loop was
  the largest SwiftUI cost in the benchmark. Track position by item id
  (`scrollPosition(id:)`, `ScrollViewReader`), observe only what is needed, and
  write state only when a threshold crossing changes the result.
- Keep a list's position across inserts by anchoring to an item id, not by
  measuring offsets after the fact.

## Layout and text

- A custom `Layout` caches measurements (`makeCache`/`updateCache`) and does not
  measure the same subview twice per pass.
- Avoid a `TextRenderer` or other per-text measurement hook on text that appears
  in every row; it re-measures every line on each layout pass. Prefer offsets
  and plain modifiers.
- Text size changes and data reloads re-measure only the rows that changed.

## Updates and input

- Coalesce bursts: collect incoming changes and apply them once per frame or
  run loop turn, and apply list changes incrementally rather than rebuilding
  the whole section model.
- Respond to input first. Do not wrap large state changes (tab switches,
  reloads) in an animation; show the control's new state in the first frame and
  switch heavy content in the next transaction. Select tabs on touch down.

## Images and memory

- Decode and downsample to display size off the main actor; keep image caches
  bounded. Retain an image the user will return to (a hero) outside lazy-row
  recycling, render memory-cache hits synchronously, and defer off-screen image
  work. Prefetch just ahead of the scroll direction.
- Database reads, decoding and diffing run off the main actor.

## Proving it

- A performance claim needs numbers: before and after on the same simulator or
  device, same build configuration, at least three runs, median reported.
  Debug-simulator numbers compare only with themselves; the final judgment is a
  Release build on a device with Instruments (SwiftUI, Hitches, Time Profiler).
- Use the repository's own benchmark harness or scroll-baseline UI test when
  one exists.
- Profile before tuning. Several small row fixes without a trace measured flat;
  find the dominant cost first, then fix that.
- `Self._printChanges()` shows why a body ran; use it while investigating and
  remove it before commit.
- Move a surface to UIKit (`UICollectionView` hosting SwiftUI cells) only when a
  trace shows container virtualization or diffing is still the bottleneck after
  the rules above. Scope it to that one list.
