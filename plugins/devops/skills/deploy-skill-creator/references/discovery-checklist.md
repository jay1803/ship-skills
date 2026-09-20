# Deployment Discovery Checklist

Inspect only the surfaces relevant to the repository. Prefer authoritative
project configuration and live read-only provider state over historical notes.

## Repository Sources

- `AGENTS.md`, `CLAUDE.md`, README, operations and release documentation
- `.github/workflows/`, CI/CD configuration, Makefile, Taskfile, package scripts
- infrastructure manifests, deployment configuration, service definitions
- version, build-info, health, readiness, and smoke-test endpoints
- database migrations, generated artifacts, compatibility and ordering rules
- existing rollback, incident, canary, promotion, or store-submission procedures
- existing local skills under `.agents/skills` or `.codex/skills`

## Environment Facts

For both test and production, resolve:

- branch trigger and whether deployment is automatic or manual;
- provider account, project/app/service id, region, host, and runtime;
- build command and immutable artifact identity;
- required credentials by variable or login name, never value;
- migrations and their ordering relative to application rollout;
- readiness delay, bounded retry, health check, smoke test, and revision proof;
- rollback capability, rollback target selection, and authorization boundary;
- canonical deployment id, log, dashboard, or API used as evidence.

## Validation Questions

- Can `verify` prove which exact commit is running without changing state?
- Can `deploy` be given a full SHA/tag rather than relying on the current branch?
- Does the skill distinguish the current machine from the deployment target?
- Can a successful upload still fail readiness or integrity checks?
- Are non-idempotent migrations, submissions, or restarts protected from blind
  retry?
- Will a failure return an honest `blocked` or `failed` receipt?
- Does the skill avoid owning release-policy resolution, production-promotion
  merge, version, tag, or GitHub Release state?
