---
name: proj-context
description: Build or refresh a project onboarding context pack from existing documents and relevant sources. Reuse known project materials; use proj-sources when discovery is needed.
metadata:
  owner: jay1803
  family: project
  maturity: stable
  distribution: project
---

# Project Context

Produce an evidence-backed account of a project's purpose, people, decisions,
timeline, current state and open questions. Read the
[document contract](../project/references/document-contract.md).

Start with supplied context, proposal or Entry Page and read its authoritative
records first. Reuse a current source inventory. When sources are missing, use
[proj-sources](../proj-sources/SKILL.md) with the relevant question and scope;
a complete discovery sweep is needed only when requested. Distinguish already
reviewed material from new or unchecked sources rather than re-reading every
historical link on each invocation.

Read sources needed to support the requested account, follow material decisions
and conflicts to their underlying records, and state the coverage. A source list
alone is not a factual summary. Report inaccessible or unchecked material and
avoid claiming exhaustive context from a partial read.

Return a context pack with overview, timeline, roles, decided/open questions,
source links and gaps, matching the user's language. Write to a requested file
when authorized; for a requested local pack without a filename use
`<project>-context.md`, with a separate sources file only when it is useful or
requested. Context collection does not change the Entry Page, approval state,
Linear objects or send messages. Return the pack to the requesting Project
stage; do not start a proposal or engineering workflow merely to onboard.
