---
name: proj-review
description: Review a proposal, kickoff, project update or closeout document for decision quality, evidence and consistency. Return findings and readiness; does not approve the project or edit the document unless separately authorized.
metadata:
  owner: jay1803
  family: project
  maturity: stable
  distribution: project
---

# Project Document Review

Review the requested document against its purpose and current evidence. Read the
[document contract](../project/references/document-contract.md), then inspect
the named artifact and supporting decision/source records. This is document
review, not Product readiness or technical PR review.

## Stage-specific questions

| Document | What changes readiness? |
| --- | --- |
| Proposal | Is the decision/ask clear? Does evidence support the problem, recommendation and expected value? Are alternatives, costs, assumptions and material unknowns visible? |
| Kickoff / Entry Page | Is the approved revision identifiable? Do scope and commitments match it? Are responsibilities, dependencies, milestones and unresolved agreements actionable? |
| Update | Are changes sourced and current? Are baseline, accepted plan and suggestions distinct? Were blockers and coverage gaps preserved, and overview/history reconciled? |
| Closeout | Are delivery, acceptance, handover and measured impact distinguished? Are comparisons to the original baseline honest, and outstanding responsibilities visible? |

For every material finding, name the location/claim, supporting evidence or
missing evidence, its consequence for the document's purpose and a bounded
correction. Missing source access is a verification gap, never a pass. Avoid
style preferences as blockers unless they prevent the intended audience from
understanding or acting. Do not require inapplicable template sections.

Return one document-readiness result: `ready`, `needs-revision`, or
`unable-to-verify`, with the reviewed artifact/revision, material findings and
remaining evidence gaps. Readiness is relative to the requested use: an honest
kickoff draft can be useful while execution agreements remain pending. Explain
that distinction rather than treating a draft as an approved execution record.

A standalone review stops at findings without edits. In an authorized authoring
workflow, return findings to that stage's author for correction and inspect the
affected claims afterward. Do not confer leadership approval, resource authority,
project closure or permission to publish. Review delegation is optional and
must preserve access/write boundaries; the workflow does not require an agent
per document or stage.
