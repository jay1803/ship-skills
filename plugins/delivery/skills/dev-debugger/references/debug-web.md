# Debug Web

Use for frontend web bugs, React, Next.js, Vite, browser behavior, hydration, routing, responsive layout, accessibility, client state, browser tests, and visually driven UI defects.

## Workflow

1. Load `$build-web-apps:frontend-app-builder` when the bug is in a substantial frontend flow or visual behavior. For small fixes inside an existing app, prioritize local conventions and repo scripts.
2. Discover framework, package manager, scripts, routes, rendering mode, styling system, component library, state/cache layer, API client, test stack, and browser verification path.
3. Reproduce with the affected browser, viewport, route, auth state, data fixture, locale, feature flag, network condition, and environment.
4. Search from evidence anchors: console error, stack trace, route, UI copy, component name, test name, API endpoint, query key, local storage key, and CSS class.
5. Use browser/dev-server evidence before proposing a fix when the issue is visual, hydration, routing, or client-state dependent.

## Symptom Map

- Console/runtime error: stack trace, component boundary, source map, failing route.
- Hydration mismatch: server/client data, non-deterministic render, time/random/browser-only API.
- Route/navigation bug: router params, redirects, auth guard, stale loader/action data.
- Wrong data: query key, cache invalidation, API response mapping, optimistic update.
- Form bug: validation schema, controlled/uncontrolled input, submit state, disabled/loading behavior.
- Responsive/layout bug: viewport-specific CSS, container sizing, overflow, text wrapping.
- Accessibility bug: keyboard path, focus trap, labels, roles, color contrast, dynamic content.
- Performance bug: bundle size, re-render loop, expensive effect, network waterfall.
- Test-only failure: fixture drift, async wait, selector fragility, mocked API contract.

## Evidence To Report

- Browser, viewport, route, auth/data state, environment, and reproduction reliability.
- Console/network/test evidence and screenshots when relevant.
- Candidate files and confidence level.
- Exact command, Playwright/browser check, or test that should verify the hypothesis.
