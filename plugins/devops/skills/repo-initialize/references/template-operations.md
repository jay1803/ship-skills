# Template Operations

The source repository is `jay1803/agent-repo-template`, currently private.
Default audited revision: `603812c5aee1742f5504d5d1a97ef02840f87fe3` (template
version `1.1.0`). Access requires an authenticated account with repository access.
Use a local verified checkout if remote access is unavailable; do not substitute
an unrelated public template or expose credentials.

## Fetch and Inspect

Clone into a separate temporary checkout, not over the target repository. For
example, after checking the installed `gh repo clone` help:

```bash
template_checkout=$(mktemp -d)
gh repo clone jay1803/agent-repo-template "$template_checkout"
git -C "$template_checkout" fetch origin 603812c5aee1742f5504d5d1a97ef02840f87fe3
git -C "$template_checkout" checkout --detach 603812c5aee1742f5504d5d1a97ef02840f87fe3
git -C "$template_checkout" rev-parse HEAD
```

For an explicit update to a newer template, fetch its remote default branch or
the requested revision, resolve a full commit SHA, and check out that immutable
revision. Inspect the diff from the prior ledger revisions, especially the
updater, manifest, and policy modules, before execution. Do not run downloaded
code merely because a tag or branch name looks familiar. Verify the source
identity and check the selected files against their committed content.

Read the source `README.md`, `.template/manifest.json`, `.template/manage.py`,
and selected module files. The updater itself verifies all input files against
its HEAD before planning. This integrity check does not replace inspecting an
updated executable before running it.

## Preview and Apply

The target is an existing physical directory; resolve symlinked checkout paths
first. The default selects core only, plus modules already recorded by an earlier
adoption. Optional module names are `development`, `coding`, `validation`,
`skills`, `release`, and `release-runbook`.

```bash
python3 "$template_checkout/.template/manage.py" --target /path/to/project
python3 "$template_checkout/.template/manage.py" --target /path/to/project --apply
```

To include coding and validation guidance, add `--modules coding validation` to
both commands. Do not enable every module for convenience. The development and
release samples select a split-branch workflow and need the policy decisions in
[policy mapping](policy-mapping.md).

For a repository generated through GitHub's template button, run the same
procedure from the source checkout. Identical existing files are adopted into
the ledger; custom files are preserved. No direct branch relationship or ongoing
synchronization is established by GitHub template generation.

The helper only writes root `AGENTS.md`, selected policy/runbook files, and
`.agents/template-state.json`. It creates no secondary index. It does not copy the
source README, tooling, Git metadata, or inactive examples into an existing repo.
The root instructions are appended as a marked block; existing surrounding
instructions remain byte-for-byte intact. Reconcile any existing discovery
section directly in root `AGENTS.md`. Link adopted rules and SOPs there.

## Interpret the Receipt

- `create`, `append`, `update`: proposed writes; performed only with `--apply`.
- `unchanged`: content matches the selected source; the ledger may still advance.
- `preserve-existing`: unowned content at the destination; compare and adapt.
- `preserve-local`: managed content was customized; compare three versions.
- `preserve-deleted`: a managed file/block was removed; do not resurrect it.
- `index-migration-required`: an old root block would change while its recorded
  legacy index still exists. Preserve the root until the index content and
  consumers have been migrated, so unique rules remain reachable.
- `policy-review-required`: upstream policy changed; inspect the permission and
  workflow difference, preserving project decisions unless a change is authorized.
- `preserve-retired`: source dropped the file; read its contents and migrate
  its consumers before authorized removal.
- `retired-removed`: the legacy index was already removed and its old path is
  absent from the resulting root; apply removes only its obsolete ledger entry.

Exit `0` means a clean plan/apply; `2` means attention remains and safe independent
writes may have applied; `1` means an error. Invalid source/state/path errors
occur before application. An I/O failure can leave partial writes; inspect the
actual diff and receipt before retrying. There is no force-update/delete mode.

Each ledger entry retains the hash of template-owned content and its source
commit, not a hash of arbitrary local decisions. Leave a customized file's
baseline unchanged. Do not set its hash to the local contents to make the next
upgrade overwrite it. A deliberate customization may remain `preserve-local`
on future runs without being a migration failure. Explain that outcome.

## Layout Migration

The standard destinations are in [policy mapping](policy-mapping.md). When a
setup/update request includes adopting this layout, it covers meaning-preserving
moves of in-scope agent documentation. Preserve explicit requests to keep paths
and documented repository exceptions. Do not introduce a new approval step for
an already-authorized move; ask only about an unresolved conflicting decision.

For an existing `.agents/release.md`, move it to `.agents/runbooks/release.md`
when its scope is the release SOP. Read both source and any existing destination
first. If both exist, compare their meaning and consumers; reconcile deliberately
or report the unresolved conflict, never overwrite the destination blindly.
Update live inbound links in AGENTS, READMEs, scripts, CI, and other rules, plus
relative links inside the moved file. Preserve its requirements and permissions.
Validate referenced files and anchors from their new locations. Do not perform a
release or deployment merely to validate a documentation move.

For an old `.agents/README.md` index:

1. Read it completely. Preserve unique rules in root AGENTS or the appropriate
   canonical policy/SOP. Transfer useful links directly to root AGENTS with their
   reading triggers, rebasing relative paths. Keep existing inline rules intact.
2. Use the updater preview/apply for the new core where safe. Handle
   `index-migration-required` by migrating the index content into the root before
   removing the legacy file; do not force past it. Then adapt the root
   to the repository. A customized old root block may need a semantic merge;
   the helper preserves it rather than overwriting it.
3. After content preservation and live-consumer checks, remove the redundant
   index within the authorized migration. Do not rewrite immutable historical
   evidence for cosmetic path changes. Distinguish historical mentions from
   executable paths or active links; document external consumers that cannot
   migrate yet as explicit exceptions instead of breaking them.
4. Preview/apply again. The updater accepts the legacy ledger, keeps retained
   indexes as `preserve-retired`, and drops only the already-removed index entry
   as `retired-removed` when the resulting root no longer mentions the old path.
   This bookkeeping check is not proof that all other consumers were migrated.
   Do not erase the whole ledger or replace local-content hashes to force a match.
5. Repeat the preview: no unexpected writes or index resurrection. A deliberately
   customized root may remain `preserve-local`; report that expected preservation.

A moved, template-managed document needs provenance checked separately: retain
its original source baseline at the new canonical destination if it represents
the same template artifact. Do not mark local policy text as an upstream baseline.
Unmanaged project SOPs stay unmanaged; moving one does not justify replacing it
with a generic release-runbook module or adding a synthetic ledger entry.

## Checks

```bash
python3 -m unittest discover -s "$template_checkout/.template/tests" -v
python3 "$template_checkout/.template/check.py"
git -C /path/to/project diff --check
```

Also inspect the target diff, selected policy meaning, required links, untracked
files, and repeat preview. The source test suite validates deterministic update
behavior; it does not validate the project's build, deployment, branch existence,
or the semantic correctness of customized policies.
