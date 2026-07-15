---
name: dev-implementer
description: >-
  Implement planned code changes after Dev planning across iOS, macOS, SwiftUI, web, backend, and Supabase surfaces. Use when $dev-planner has selected implementation work and the coding phase needs a single controlled implementer that loads the relevant platform reference, follows the approved spec and technical plan, keeps scope tight, updates tests when practical, records validation evidence, and stops for product or architecture decisions outside the plan.
---

# Dev: Implementer

Implement the approved Dev plan. Keep product scope fixed, follow existing repo conventions, and load only the platform reference files needed for the selected surface.

## Reference Selection

Read the shared workflow first, then load one or more references from `references/`:

- iOS app, iOS simulator workflow, Xcode iOS target, UIKit, iOS SwiftUI screen, App Intent, or iOS runtime behavior: [implement-ios.md](references/implement-ios.md)
- macOS app, AppKit, macOS SwiftUI scene/window/menu, signing, entitlement, packaging, or macOS runtime behavior: [implement-macos.md](references/implement-macos.md)
- SwiftUI view, state, layout, navigation, sheet, animation, accessibility, preview, performance, or Liquid Glass work: [implement-swiftui.md](references/implement-swiftui.md)
- Frontend web, React, Next.js, Vite, dashboard UI, browser behavior, responsive layout, accessibility, client state, or web tests: [implement-web.md](references/implement-web.md)
- Backend/API/service work that is not primarily Supabase: [implement-backend.md](references/implement-backend.md)
- Supabase schema, migration, RLS, Auth, Edge Functions, Storage, Realtime, generated types, or Supabase client/server integration: [implement-supabase.md](references/implement-supabase.md)

Multiple references are allowed when the plan crosses surfaces. Sequence backend/API contracts before clients by default, and pair `implement-swiftui.md` with `implement-ios.md` or `implement-macos.md` when app-level build/run/debug behavior matters.

## Workflow

1. Read the product spec, repo context, technical approach, Dev plan, acceptance criteria, and any spike/API research output.
2. Confirm the selected platform surface and load the matching reference file(s). If the plan selected the wrong surface, stop and report the routing correction needed.
3. Inspect target files before editing. Reuse local module boundaries, naming, dependency injection, state, API, persistence, styling, and test patterns.
4. Make the smallest coherent code change needed by the plan. Do not broaden product behavior, redesign unrelated UI, rewrite architecture, or touch unrelated files.
5. Add or update focused tests, fixtures, previews, migrations, generated types, or docs when the repo has a practical surface and the plan calls for it.
6. Run the narrowest useful validation while implementing when it catches local mistakes cheaply. `$dev-test` still owns the formal post-implementation validation pass.
7. Stop if implementation uncovers missing product scope, architecture, provider/API contract, entitlement, security, migration, or data-retention decisions not covered by the plan.

## Output

```markdown
## Implementation Result

### Platform References Used
- <implement-ios | implement-macos | implement-swiftui | implement-web | implement-backend | implement-supabase>

### Changed Files
- <path>: <what changed and why>

### Platform Notes
- <platform/framework/build/signing/state/API/schema/accessibility/security note, or "None">

### Tests / Fixtures / Migrations / Previews
- <test, fixture, migration, generated type, preview, or "None">

### Validation Evidence
- `<command/tool>`: <result or blocker>

### Follow-Up Needed
- <technical follow-up, blocker, or "None">

### Recommended Next Step
Usually `$dev-test`.
```
