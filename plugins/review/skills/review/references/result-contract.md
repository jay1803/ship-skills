# Review Result Contract

```markdown
## Technical Review

Contract Version: 2
Review Run ID: <id>
Generation: <integer>
Attempt Count: <accepted repaired heads>
Repair Limit / Authority: <default 5 | verified numeric user override and exact source/scope>
Repair Budget Remaining: <Repair Limit minus Attempt Count>
Generation Status: <collecting | judged | stale | resolved>
Invocation: <dev-managed | standalone>
Review Mode: <fast | standard | strict | explicit standalone>
Started At: <timestamp copied from the frozen envelope>
Target Type: <pull-request | immutable-diff>
Repository: <repository>
PR: <url or none>
Base Revision: <full SHA>
Head Revision: <full SHA>
Review Lens: <thermo-nuclear>
Decision: <approved | comments | stale | blocked>
Common Action: <repair-required | advisory | coverage-blocked | none>
Independence: <not required | satisfied | blocked>
GitHub Posting: <verified URL/evidence | not applicable | not posted>

### Source Verification
- <artifact ID, source/provenance, native decision, verified/quarantined>

### Findings and Dispositions
- <combined and separate findings with source IDs, native labels, dispositions,
  and immutable raw-source references in the assembled artifact>

### Coverage
- Specification: <assessed | not assessed | blocked>
- Core/conditional: <verified, skipped, missing, or quarantined>

### Quarantine
- <Artifact ID field with received value or `none - missing`,
  exact validation reason, provenance when available, and verbatim raw
  Markdown; complete judge artifact when invalid; or "None">

### Repair State
- Previous Head: <SHA or none>
- Change Evidence: <evidence or none>
- Prior Artifact: <reference or none>
- Issue/PR History: <prior runs, cumulative repair heads/root causes, base drift>
- Convergence Checkpoint: <not reached | passed with evidence | blocked>

### Blocker
- <blocker or "None">

### Recommended Next Step
<`$dev-implementer`, `$dev-ci-repair`, `$dev-merge-handoff`, caller/user, or blocked reason>
```
