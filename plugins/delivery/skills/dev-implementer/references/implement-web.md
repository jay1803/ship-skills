# Implement Web

Use for frontend web apps, React, Next.js, Vite, dashboards, responsive browser UI, browser behavior, accessibility, client state, web tests, and visually driven product UI.

## Workflow

1. Load `$build-web-apps:frontend-app-builder` when creating or substantially changing frontend UI, dashboards, websites, games, or visually driven flows. For small fixes inside an existing design system, use the repo's local conventions first.
2. Discover framework, package manager, scripts, routing, styling system, component library, state pattern, test stack, and browser verification path before editing.
3. Inspect target files before editing. Follow existing component, data-fetching, state, accessibility, and styling conventions.
4. Make the smallest coherent web code change needed by the plan. Do not add landing-page wrappers or visual redesigns unless the spec asks for them.
5. Add or update focused tests when the repo has a practical surface.
6. Run relevant typecheck, lint, unit test, build, and browser/screenshot checks when cheap enough during implementation, and record exact evidence.
7. Stop if implementation requires product scope, visual design, provider/API contract, or architecture decisions not covered by the plan.

## Notes To Report

- Framework, routing, state, styling, accessibility, responsive, or browser behavior constraints.
- Tests added or skipped, with rationale.
- Validation command/tool and exact result or blocker.
