# Specification Compliance Finding Contract

Use this contract for every `review-spec` finding. It is a requirement-evidence
record, not a code-quality score or a request to redesign the product.

## Classifications

- `missing`: a governing requirement has no implementation evidence.
- `incorrect`: implementation evidence contradicts a governing requirement.
- `extra`: implementation behavior exceeds an explicit scope boundary.
- `unverifiable`: the governing requirement is known, but the available
  implementation evidence cannot establish compliance.

Do not use `extra` when the authority is merely silent, and do not use any
classification when the governing authority is missing or ambiguous. Those are
bounded blockers.

## Required Finding Shape

```markdown
- [<missing | incorrect | extra | unverifiable>] <short requirement label>
  - Requirement: <identifier or exact requirement statement>
  - Requirement evidence: <authority source and precise location>
  - Implementation evidence: <file, revision, test, behavior, or unavailable evidence>
  - Compliance gap: <direct comparison without code-quality judgment>
  - Requested resolution: <smallest change or evidence needed>
```

Both evidence fields are required. Keep quoted source text short and identify
the source location precisely enough to be checked again.
