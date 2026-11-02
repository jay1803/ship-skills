# Session sources and bounded retrieval

Use this reference when resolving IDs and retrieving evidence. The bundled reader
uses Python 3.10+ and the standard library. Run it from any directory by resolving
`scripts/read_sessions.py` relative to this Skill's installed location.

## Resolve the requested identity

```bash
python3 /path/to/skill-session-review/scripts/read_sessions.py codex:<id> claude:<id>
```

The default is a content-free, paginated event index. Discovery looks only for
matching filenames in `$CODEX_HOME/sessions`, `$CODEX_HOME/archived_sessions`
(default home `~/.codex`), and `$CLAUDE_CONFIG_DIR/projects` (default `~/.claude`).
It does not read all session contents to search for a topic. Override with
`--codex-home PATH` or `--claude-home PATH` for a known local/exported data root.
Exact duplicate file bytes collapse to one source with alias paths. Conflicting
snapshots or a bare ID present in both providers return `ambiguous`, with paths;
choose a source explicitly rather than silently preferring a newer copy.

When the requested Codex task spawned relevant local sub-agents, inspect the
`session_meta.parent_thread_id` of candidate child logs for the exact requested
parent ID. Resolve confirmed child IDs with the reader and cost profiler before
claiming their usage is unavailable. Limit this lookup to the parent's local
session tree; do not search other tasks by topic. Record which linked children
were included and which could not be accessed.

For exports or a specific disambiguated source:

```bash
python3 /path/to/skill-session-review/scripts/read_sessions.py --file /path/to/session.jsonl
```

`--file` may repeat. File input detects the provider from record structure and
reports embedded identity when available. Missing identity is marked unknown;
unsupported/mixed exports are reported rather than treated as successful reads.
Arbitrary exports need explicit file paths. Missing local IDs may live on another
host; use an available read-only task API or request the location/export. Task
summaries can locate context but cannot establish command-level compliance.

## Expand evidence

```bash
python3 /path/to/skill-session-review/scripts/read_sessions.py codex:<id> --offset 80 --limit 80
python3 /path/to/skill-session-review/scripts/read_sessions.py codex:<id> --mode excerpts --lines 15:45
python3 /path/to/skill-session-review/scripts/read_sessions.py claude:<id> --mode excerpts --match SKILL.md --context 3
```

Line ranges are inclusive original JSONL lines. `--match` is a case-insensitive
literal search of the original record; combine neither filter to page through
all events. `--offset`/`--limit` paginate selected events (default 0/80), and
`--max-chars` caps each excerpt (default 3000). These are adjustable retrieval
controls, not review scope limits. Output includes `selected_count`, `next_offset`,
line numbers, per-record digest, file digest, and explicit excerpt truncation.
Check file digests between reads; if a session resumed or changed, identify the
new snapshot and revisit affected conclusions rather than silently mixing versions.
Match/range context precedes pagination. Read beyond matches for goals, steering,
valid exceptions, and outcomes; no match is not evidence of absence of Skill use.

The reader preserves original records in excerpt form rather than flattening away
tool arguments/results or historical instruction messages. Common credential
patterns are masked; this is best-effort, not comprehensive de-identification.
Never paste raw output into a PR, issue, or shared report. Keep evidence in its
original store; if local scratch output is needed, use private storage outside Git.

## Cost profile before deep inspection

For requested Codex or Claude sources, the companion analyzer produces a
content-free inventory of observable usage and cost proxies:

```bash
python3 /path/to/skill-session-review/scripts/analyze_session_cost.py codex:<id>
python3 /path/to/skill-session-review/scripts/analyze_session_cost.py --file /path/to/session.jsonl
```

It uses the reader's source resolution and original line locators. Review its
coverage and warnings before totals. Codex's final observed cumulative usage
snapshot is reported once; it is not allocated to models or phases. Claude
message usage is deduplicated by message ID; usage without a stable message ID
is excluded from totals and reported as missing coverage. Input, cache-read,
cache-creation, output, and reasoning fields remain separate. Visible message
characters and tool-result characters are proxies, not billable tokens. The
profile reports observed model names, tool calls, identical-result candidates,
visible instruction/request characters, and compaction markers only where the
source exposes them. A call mentioning `SKILL.md` or `references/` with a result
is only an instruction-load candidate; inspect the result and historical source
before claiming a load or its benefit. The profile cannot recover hidden system
context, classify ticket/project/handoff text reliably, decide whether repeated
reads were necessary, infer retries from repeated calls, or establish verified
outcome. Use its line locators to inspect suspicious spans with the reader,
including contrary context and changed source state.

No raw message, tool argument, or tool result is included in the profile.
Hashes and sizes still describe potentially sensitive local records; keep
scratch profiles private. Do not treat the absence of a visible context source
as proof that the runtime did not inject it.

## Provider interpretation

- Codex JSONL: `session_meta` identifies the session; `turn_context` supplies turn
  context; `response_item` contains messages and call/result items; `event_msg`
  includes task lifecycle and usage events. User/assistant text may be mirrored
  in event and response streams. Prefer response items for content and link the
  event mirror; do not count both as independent work. `compacted` and summary
  records mean earlier detail may be missing.
- Claude JSONL: top-level `sessionId`, `uuid`, `parentUuid`, `type`, and nested
  `message` identify records. Content blocks include `text`, `tool_use` (including
  Skill calls), and `tool_result`. Pair calls/results by their tool-use ID, not
  proximity alone. Partial records may share a message ID; do not blindly add their
  usage. Linked subagent logs are separate evidence, not automatically loaded.
- Unknown records remain visible by type and locator. Parse warnings, recognized
  provider, and successful file access do not prove that the transcript is complete.
  Read errors are reported per input; other supplied inputs still proceed.

Usage is left in source records for interpretation. Codex cumulative usage
snapshots must not be summed as turn usage. Claude partial/streaming message usage
may repeat; deduplicate by message identity before aggregation. Keep input, output,
cache-read/write, and reasoning categories distinct and report their coverage.
Across providers compare only compatible measurements. Tool counts and repeated
output size are proxies, not tokens. The reader deliberately does not score
compliance, infer success, or claim token savings.
