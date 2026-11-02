#!/usr/bin/env python3
"""
Classify whether GitHub rules allow deleting one remote branch head.

Reads the paginated response of `repos/{owner}/{repo}/rules/branches/{branch}`
and, when present, the classic `repos/{owner}/{repo}/branches/{branch}/protection`
response. Prints one tab-separated line: decision, reason, evidence.

Only `allowed` permits deletion. Anything restrictive, missing or unparseable
is `retained`, so an unknown state never becomes a deletion.

Usage:
  classify_branch_deletion.py RULES_JSON [PROTECTION_JSON]
"""

import json
import sys


def json_documents(text):
    # `gh api --paginate` may emit one JSON array per page back to back.
    decoder = json.JSONDecoder()
    index = 0
    while True:
        while index < len(text) and text[index].isspace():
            index += 1
        if index == len(text):
            return
        value, index = decoder.raw_decode(text, index)
        yield value


def classify(rules_text, protection_text):
    try:
        rules = []
        pages = list(json_documents(rules_text))
        if not pages:
            return 'retained', 'deletion rules response was empty', 'rules=unknown'
        for page in pages:
            if not isinstance(page, list):
                return 'retained', 'deletion rules response was not a list', 'rules=unknown'
            rules.extend(page)

        types = sorted({str(rule.get('type')) for rule in rules if isinstance(rule, dict)})
        evidence = 'rules=' + (','.join(types) or 'none')

        deletion = [rule for rule in rules if isinstance(rule, dict) and rule.get('type') == 'deletion']
        if deletion:
            ruleset_ids = sorted({str(rule.get('ruleset_id')) for rule in deletion})
            return ('retained', 'a deletion rule applies to this branch',
                    evidence + '; deletion ruleset_id=' + ','.join(ruleset_ids))

        if not protection_text.strip():
            return 'allowed', 'no deletion rule and no classic branch protection', evidence + '; classic=not protected'

        protection = json.loads(protection_text)
        allow = protection.get('allow_deletions') if isinstance(protection, dict) else None
        enabled = allow.get('enabled') if isinstance(allow, dict) else None
        if enabled is True:
            return 'allowed', 'no deletion rule and classic protection allows deletion', evidence + '; classic allow_deletions=true'
        if enabled is False:
            return 'retained', 'classic branch protection disallows deletion', evidence + '; classic allow_deletions=false'
        return 'retained', 'classic branch protection did not report allow_deletions', evidence + '; classic=unknown'
    except (ValueError, AttributeError) as error:
        return 'retained', 'deletion rules could not be parsed: %s' % error, 'rules=unparsed'


def main(argv):
    if len(argv) not in (2, 3):
        print(__doc__.strip(), file=sys.stderr)
        return 2
    with open(argv[1], encoding='utf-8') as rules_file:
        rules_text = rules_file.read()
    protection_text = ''
    if len(argv) == 3:
        with open(argv[2], encoding='utf-8') as protection_file:
            protection_text = protection_file.read()
    fields = [' '.join(field.split()) for field in classify(rules_text, protection_text)]
    print('\t'.join(fields))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
