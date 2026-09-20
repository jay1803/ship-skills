# Release Notes

Use this reference when drafting or revising the notes for a release candidate,
release PR, or GitHub Release. It owns writing guidance within `$release`;
it does not expand the request into publication or change merge authority.

## Repository Guidance First

Follow the user's explicit writing instructions and the repository's designated
release notes guideline or template, including its language, audience, required
sections, and ordering. Look for pointers in repository instructions, README,
and release documentation. Respect applicable `.github/release.yml` category
and exclusion settings; those settings alone may not define a complete writing
format. Use the default below for unspecified aspects without adding sections
that conflict with the repository's format.

When no guideline exists, use the English default: headings and prose are in
English, even when the surrounding conversation is in another language. A
repository guideline or explicit user language request can override this
fallback. Do not invent or require a repository guideline file.

Writing guidelines do not grant promotion, merge, tag, deploy, or publish
permission. The repository release policy contract remains authoritative for
promotion branches and merge capability; the current request still limits
actions. A notes-only request ends with the draft.

## Evidence And Section Selection

- Resolve the previous release for the same package and release line, and the
  exact candidate revision. Use their actual difference, merged PRs, and
  supporting changes to draft the notes. A promotion branch comparison alone
  can miss unreleased changes already on the target. For a first release, use
  its initial scope; do not invent a previous tag or comparison link.
- In a monorepo, include only the selected package/plugin and shared changes
  that affect it. Exclude unrelated packages and work outside the candidate.
- Describe the capability, changed behavior, or concrete symptom fixed. Combine
  duplicate PR/commit entries. Automated GitHub notes are source material to
  curate, not proof of user impact. Do not invent performance claims from an
  internal refactor or turn planned work into shipped features.
- The main sections are **Added**, **Changed and Improved**, and **Bug Fixes**.
  All are optional: omit empty sections rather than writing `None` or padding
  the release. A fix-only release can contain just **Bug Fixes**.
- Include **Upgrade Notes** for breaking changes, required migration/configuration
  steps, or compatibility changes. Put it before the main sections when action
  is required. Optional sections do not make material upgrade impacts optional
  to disclose; use the repository's equivalent section when it has a template.
- Include **Deprecated and Removed** for affected capabilities, alternatives,
  and any confirmed removal schedule; **Security** for relevant fixes and
  public advisory links; **Known Issues** for evidenced limitations and available
  workarounds. Avoid inventing dates, advisories, or workarounds.
- A short opening summary and **Full Changelog** comparison link are optional.
  Keep technical detail only when the intended reader needs it to use or
  upgrade the release. Internal-only releases can say what maintenance changed
  without claiming a new user capability.

## Default Template

Adapt [the English template](../assets/release-notes.md) and remove unused
sections, the optional summary, and unavailable links. Before handoff or
publication, check every item against the final candidate and verify that
material upgrade impacts are visible. Recheck scope if the candidate changes.

## Sources

- [Keep a Changelog](https://keepachangelog.com/en/1.1.0/): curated changes for
  people, grouped by type, including deprecations, removals, and security fixes.
- [GitHub release notes configuration](https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes):
  category and exclusion settings for generated notes.
