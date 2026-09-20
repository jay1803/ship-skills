# Project Deploy Contract

Contract version: `release-deploy/v1`

This contract connects the global `$release` orchestrator to one repository's
project-level deploy skill. The project skill may use any platform-specific
mechanism, but it must accept and return these semantics.

## Required Request

```yaml
contract: release-deploy/v1
project: <stable project name>
repo: <absolute repository path>
action: deploy | verify
environment: test | production
requested_ref: <full commit SHA>
release_tag: <immutable tag or null>
release_pr: <URL or null>
authorization: <what the user requested and any relevant limit>
```

`requested_ref` is always required. A production request should also provide
`release_tag`. Branch names may be recorded for context, but are not immutable
deployment identities.

## Required Receipt

```yaml
contract: release-deploy/v1
project: <stable project name>
action: deploy | verify
environment: test | production
status: deployed | verified | blocked | failed | rolled-back
requested_ref: <full commit SHA>
observed_ref: <full running commit SHA or documented immutable equivalent>
release_tag: <tag or null>
deployment_id: <provider/run/deployment id or null>
started_at: <timestamp or null>
finished_at: <timestamp or null>
checks:
  build: passed | failed | not-applicable
  migration: passed | failed | not-applicable
  rollout: passed | failed | not-applicable
  health: passed | failed | not-applicable
  smoke: passed | failed | not-applicable
rollback:
  supported: true | false
  target: <immutable ref or null>
  performed: true | false
evidence:
  - <redacted command result, provider URL, health response, or runtime proof>
notes:
  - <remaining risk or none>
```

## Invariants

- Never expose credentials, tokens, signing material, or private configuration
  in the request, receipt, logs, tracker comments, or final response.
- Resolve the exact target account, project, environment, host, region, and
  runtime before mutation. Do not infer production from the current shell host.
- `deploy` performs a state change; `verify` is read-only. Do not convert one
  into the other without authorization.
- A successful command or uploaded artifact is not enough. Success requires
  runtime evidence and revision integrity.
- `observed_ref` must match `requested_ref`, or the project skill must document
  a deterministic immutable mapping that the caller can verify.
- Do not automatically retry a non-idempotent deployment, migration, store
  submission, or rollback. Define bounded retry and stop conditions locally.
- Rollback is a separate mutation. Perform it only when explicitly authorized
  or when an already-authorized repository policy clearly owns that decision.
- Source-control promotion branches and merge authority come only from
  `release-policy/v1` as resolved by `$release`. A project deploy skill must not
  infer, decide, override, or grant PR merge authority.
- If any required evidence cannot be collected, return `blocked` or `failed`;
  never synthesize a successful receipt.

## Project Skill Capability Declaration

The project deploy skill must state:

- its supported environments and whether each is automatic or manual;
- required tools, accounts, roles, and non-secret configuration;
- how it builds or locates the exact artifact for `requested_ref`;
- migration and compatibility ordering;
- rollout and readiness behavior;
- health, smoke, and revision-integrity checks;
- retry, stop, and rollback boundaries;
- whether GitHub Release publication triggers deployment;
- the canonical evidence sources used to populate the receipt.
