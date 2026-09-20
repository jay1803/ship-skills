#!/usr/bin/env python3
"""Validate immutable Review inputs and assemble lossless JSON; never query/post."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path
import re
import sys

CORE = {'review-spec', 'review-correctness', 'review-code-quality'}
CONDITIONAL = {'architecture', 'test', 'security', 'integration'}
LEVELS = {'P0', 'P1', 'P2', 'P3'}
DISPOSITIONS = {'confirmed', 'corroborates', 'needs-evidence', 'not-actionable'}


class Invalid(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise Invalid(message)


def text(value):
    return isinstance(value, str) and bool(value.strip())


def digest(data):
    return hashlib.sha256(data).hexdigest()


def validate_target(target):
    require(isinstance(target, dict), 'target must be an object')
    require(target.get('contract_version') == 2, 'unsupported target version')
    require(type(target.get('generation')) is int and target['generation'] > 0,
            'invalid generation')
    for key in ('run_id', 'repository', 'started_at'):
        require(text(target.get(key)), f'missing target {key}')
    for key in ('base', 'head'):
        require(isinstance(target.get(key), str) and
                re.fullmatch(r'[0-9a-f]{40}', target[key]), f'invalid {key} SHA')
    require(target.get('invocation') in {'standalone', 'dev-managed'}, 'invalid invocation')
    require(target.get('target_type') in {'pull-request', 'immutable-diff'}, 'invalid target type')
    require(target.get('mode') in {'fast', 'standard', 'strict'}, 'invalid mode')
    require(target.get('lens') == 'thermo-nuclear', 'invalid lens')
    if target['target_type'] == 'pull-request':
        require(text(target.get('pr')), 'missing PR')
    else:
        require(target['invocation'] == 'standalone' and target.get('pr') is None,
                'immutable diff must be standalone without PR')


def validate_inputs(manifest, directory):
    require(isinstance(manifest, dict), 'manifest must be an object')
    require(manifest.get('assembly_version') == 1, 'unsupported assembly version')
    target = manifest.get('target')
    validate_target(target)
    signals = manifest.get('conditional_signals')
    require(isinstance(signals, dict) and set(signals) <= CONDITIONAL and
            all(text(v) for v in signals.values()), 'invalid conditional signals')
    defaults = {'P0', 'P1', 'P2'} if target['mode'] == 'strict' else {'P0', 'P1'}
    threshold = manifest.get('blocking_levels', sorted(defaults))
    require(isinstance(threshold, list) and len(threshold) == len(set(threshold)) and
            set(threshold) <= LEVELS, 'invalid threshold')
    if set(threshold) != defaults:
        require(text(manifest.get('policy_authority')), 'override needs explicit policy authority')
    spec_missing = manifest.get('specification_not_assessed', False)
    require(type(spec_missing) is bool, 'invalid specification state')
    if spec_missing:
        require(target['invocation'] == 'standalone' and text(manifest.get('specification_reason')),
                'specification exception requires standalone reason')
    expected = CORE | set(signals)
    sources = manifest.get('sources')
    require(isinstance(sources, list), 'sources must be a list')
    ids = [s.get('id') if isinstance(s, dict) else None for s in sources]
    require(all(text(i) for i in ids) and len(ids) == len(set(ids)), 'missing/duplicate source ID')
    names = [s.get('name') for s in sources]
    require(len(names) == len(set(names)) and set(names) <= expected, 'duplicate/unexpected source')
    stored, verified, candidates, errors = [], {}, {}, []
    for source in sources:
        raw = b''
        replies = []
        try:
            require(text(source.get('raw_path')), 'missing raw_path')
            path = Path(source['raw_path'])
            raw = (directory / path).read_bytes()
            markdown = raw.decode('utf-8')
            require(source.get('contract_version') == 2, 'unsupported source version')
            require(source.get('target') == target, 'source target mismatch')
            require(text(source.get('provenance')), 'missing provenance')
            require(source.get('kind') == ('core' if source['name'] in CORE else 'conditional'),
                    'source kind mismatch')
            require(type(source.get('raw_length')) is int and source['raw_length'] == len(raw),
                    'raw length mismatch')
            require(source.get('raw_sha256') == digest(raw), 'raw hash mismatch')
            require(text(source.get('native_decision')), 'missing native decision')
            cs = source.get('candidates')
            require(isinstance(cs, list), 'missing candidate index')
            local = {}
            for c in cs:
                require(isinstance(c, dict) and text(c.get('id')), 'invalid candidate')
                key = (source['id'], c['id'])
                require(key not in local, 'duplicate candidate')
                start, end = c.get('start'), c.get('end')
                require(type(start) is int and type(end) is int and 0 <= start < end <= len(raw),
                        'invalid candidate byte range')
                span = raw[start:end].decode('utf-8')
                require(c.get('category') in {'defect', 'optional', 'requirement'}, 'invalid category')
                level = c.get('priority')
                require(level is None or level in LEVELS, 'invalid priority')
                if level:
                    require(re.search(r'(?<!\w)' + level + r'(?!\w)', span),
                            'priority absent from native candidate')
                local[key] = dict(c, gate_priority=level)
            additions = source.get('clarifications', [])
            require(isinstance(additions, list), 'invalid source clarifications')
            clarified = set()
            for reply in additions:
                require(isinstance(reply, dict) and text(reply.get('raw_path')),
                        'invalid clarification artifact')
                received = (directory / Path(reply['raw_path'])).read_bytes()
                record = {'envelope': reply, 'received_bytes_base64':
                          base64.b64encode(received).decode('ascii')}
                replies.append(record)
                reply_text = received.decode('utf-8')
                key = (source['id'], reply.get('candidate_id'))
                require(key in local and key not in clarified,
                        'unknown/duplicate clarification candidate')
                require(reply.get('target') == target and text(reply.get('provenance')),
                        'clarification target/provenance mismatch')
                require(type(reply.get('raw_length')) is int and reply['raw_length'] == len(received)
                        and reply.get('raw_sha256') == digest(received), 'clarification bytes mismatch')
                priority = reply.get('priority')
                require(priority in LEVELS and
                        re.search(r'(?<!\w)' + priority + r'(?!\w)', reply_text),
                        'clarification priority absent')
                # Keep the original native label; only the additive source reply resolves the gate.
                local[key]['gate_priority'] = priority
                record.update(verification='verified', raw_markdown=reply_text)
                del record['received_bytes_base64']
                clarified.add(key)
            verified[source['name']] = source
            candidates.update(local)
            stored.append({'envelope': source, 'verification': 'verified', 'raw_markdown': markdown,
                           'clarification_artifacts': replies})
        except (Invalid, OSError, UnicodeError, TypeError, KeyError) as exc:
            reason = str(exc)
            errors.append({'source_id': source['id'], 'reason': reason})
            stored.append({'envelope': source, 'verification': 'quarantined', 'reason': reason,
                           'received_bytes_base64': base64.b64encode(raw).decode('ascii'),
                           'clarification_artifacts': replies})
    claims = manifest.get('required_claims')
    require(isinstance(claims, dict) and all(text(k) and text(v) for k, v in claims.items()),
            'invalid required claims')
    exceptions = manifest.get('claim_exceptions', {})
    require(isinstance(exceptions, dict) and set(exceptions) <= set(claims),
            'unknown claim exception')
    for claim_id, authority in exceptions.items():
        require(isinstance(authority, dict) and authority.get('target') == target and
                authority.get('requirement') == claims[claim_id] and
                all(text(authority.get(k)) for k in
                    ('instruction_ref', 'instruction_quote', 'authorized_by', 'scope')),
                'exception requires exact target, original requirement and instruction authority')
    kinds = manifest.get('claim_kinds', {})
    require(isinstance(kinds, dict) and set(kinds) <= set(claims) and
            all(v in {'acceptance', 'independent'} for v in kinds.values()),
            'invalid claim kinds')
    deferred = set()
    for claim_id, authority in exceptions.items():
        if authority.get('effect') == 'defer-acceptance':
            require(kinds.get(claim_id) == 'acceptance' and
                    authority.get('priority') in {'P2', 'P3'},
                    'acceptance deferral requires explicit acceptance kind and P2/P3')
            deferred.add(claim_id)
        else:
            require('effect' not in authority, 'unknown exception effect')
    for candidate in candidates.values():
        claim_id = candidate.get('claim_id')
        require(claim_id is None or claim_id in claims, 'unknown candidate claim')
        if claim_id in deferred:
            require(candidate['category'] == 'requirement' and
                    candidate.get('gate_priority') == exceptions[claim_id]['priority'],
                    'deferred candidate must match acceptance severity')
    coverage = {}
    for name in sorted(expected):
        s = verified.get(name)
        allowed = {'findings', 'compliant'} if name == 'review-spec' else {'findings', 'no findings'}
        coverage[name] = bool(s and s['native_decision'] in allowed)
        if name == 'review-spec' and spec_missing and s:
            coverage[name] = s['native_decision'] == 'Specification not assessed'
    return dict(target=target, signals=signals, threshold=threshold,
                spec_missing=spec_missing, stored=stored, verified=verified,
                candidates=candidates, errors=errors, claims=claims,
                exceptions=exceptions, kinds=kinds, deferred=deferred, coverage=coverage)


def preflight(manifest, directory):
    """Check declared source transport before Judge; never decide findings or write."""
    state = validate_inputs(manifest, directory)
    ready = not state['errors'] and all(state['coverage'].values())
    return {'assembly_version': 1, 'status': 'ready' if ready else 'blocked',
            'target': state['target'], 'coverage': state['coverage'],
            'sources': [{'source_id': s['envelope']['id'],
                         'name': s['envelope']['name'],
                         'verification': s['verification']} for s in state['stored']],
            'candidate_count': len(state['candidates']), 'quarantine': state['errors'],
            'remaining_checks': ['native identity and completion declarations',
                                 'candidate index completeness and semantic fidelity',
                                 'originating-source and instruction authority',
                                 'required evidence and finding judgment',
                                 'current PR base/head and posting authority']}


def assemble(manifest, judgment, directory):
    require(isinstance(judgment, dict), 'judgment must be an object')
    require(judgment.get('assembly_version') == 1, 'unsupported assembly version')
    state = validate_inputs(manifest, directory)
    target, signals, threshold = state['target'], state['signals'], state['threshold']
    spec_missing, stored = state['spec_missing'], state['stored']
    verified, candidates, errors = state['verified'], state['candidates'], state['errors']
    claims, exceptions = state['claims'], state['exceptions']
    kinds, deferred, coverage = state['kinds'], state['deferred'], state['coverage']
    require(judgment.get('target') == target, 'judge target mismatch')
    dispositions = judgment.get('dispositions')
    require(isinstance(dispositions, list), 'missing dispositions')
    seen, groups = set(), {}
    for row in dispositions:
        require(isinstance(row, dict), 'invalid disposition')
        key = (row.get('source_id'), row.get('candidate_id'))
        require(key in candidates and key not in seen, 'unknown/duplicate/quarantined candidate')
        require(row.get('disposition') in DISPOSITIONS and text(row.get('reason')), 'invalid disposition')
        if row['disposition'] == 'not-actionable':
            require(candidates[key]['category'] == 'optional',
                    'not-actionable requires source-native optional content')
        if row['disposition'] in {'confirmed', 'corroborates'}:
            require(text(row.get('group_id')), 'missing group ID')
            groups.setdefault(row['group_id'], []).append(row)
        seen.add(key)
    require(seen == set(candidates), 'candidate disposition coverage incomplete')
    by_id = {s['id']: s for s in verified.values()}
    for row in dispositions:
        if row['disposition'] in {'confirmed', 'corroborates'}:
            require(by_id[row['source_id']]['native_decision'] not in {'no findings', 'compliant'},
                    'clean decision cannot confirm a finding')
    for group in groups.values():
        require(sum(x['disposition'] == 'confirmed' for x in group) == 1,
                'group requires exactly one confirmed source')
        require(len({by_id[x['source_id']]['name'] == 'review-spec' for x in group}) == 1,
                'specification and engineering judgments must remain separate')
    outcomes = judgment.get('required_claims')
    require(isinstance(outcomes, dict) and set(outcomes) == set(claims), 'claim coverage incomplete')
    evaluated = {}
    for claim_id, outcome in outcomes.items():
        require(isinstance(outcome, dict) and text(outcome.get('evidence')),
                'invalid claim outcome')
        # Legacy v1 status remains readable; never reinterpret a historical pass.
        legacy = outcome.get('status')
        status = outcome.get('evidence_status', legacy)
        require(status in {'pass', 'fail', 'blocked', 'unverified'}, 'invalid evidence status')
        if legacy is not None:
            require(legacy in {'pass', 'fail', 'blocked'} and legacy == status,
                    'conflicting claim statuses')
        default_gate = 'non-blocking' if status == 'pass' else 'blocking'
        gate = outcome.get('gate_effect', default_gate)
        require(gate in {'blocking', 'non-blocking'}, 'invalid gate effect')
        authority = outcome.get('exception_authority')
        if claim_id in deferred and status in {'fail', 'blocked', 'unverified'} and gate == 'non-blocking':
            require(authority == exceptions[claim_id] and text(outcome.get('remaining_evidence')),
                    'deferred acceptance requires bound authority and remaining evidence')
        elif status == 'unverified' and gate == 'non-blocking':
            require(claim_id in exceptions and authority == exceptions[claim_id] and
                    text(outcome.get('remaining_evidence')),
                    'nonblocking unverified claim requires bound authority and remaining evidence')
        else:
            require(gate == default_gate and authority is None,
                    'exception cannot override failed, blocked or passing evidence')
        evaluated[claim_id] = dict(outcome, evidence_status=status, gate_effect=gate)

    questions = judgment.get('clarifications')
    require(isinstance(questions, list) and all(text(q) for q in questions), 'invalid clarifications')
    actionable = [candidates[(d['source_id'], d['candidate_id'])] for d in dispositions
                  if d['disposition'] in {'confirmed', 'corroborates'}]
    unlabeled = any(c['category'] == 'defect' and c.get('gate_priority') is None for c in actionable)
    if errors or not all(coverage.values()) or questions or unlabeled or any(
            o['evidence_status'] in {'blocked', 'unverified'} and o['gate_effect'] == 'blocking'
            for o in evaluated.values()):
        action = 'coverage-blocked'
    elif any(c.get('claim_id') not in deferred and (
            c.get('gate_priority') in threshold or
            (c['category'] == 'requirement' and (
                c.get('gate_priority') not in {'P2', 'P3'} or text(c.get('mandatory_authority')))))
             for c in actionable) or any(
            o['evidence_status'] == 'fail' and o['gate_effect'] == 'blocking'
            for o in evaluated.values()):
        action = 'repair-required'
    elif dispositions or spec_missing or any(
            o['evidence_status'] != 'pass' for o in evaluated.values()):
        action = 'advisory'
    else:
        action = 'none'
    require(judgment.get('common_action') == action, 'judge action disagrees with verified gate')
    return {'assembly_version': 1, 'target': target, 'blocking_levels': threshold,
            'policy_authority': manifest.get('policy_authority'),
            'conditional_signals': signals, 'required_claims': claims,
            'claim_outcomes': evaluated, 'claim_exceptions': exceptions, 'claim_kinds': kinds,
            'specification_not_assessed': spec_missing,
            'specification_reason': manifest.get('specification_reason'), 'sources': stored,
            'judgment': judgment, 'coverage': coverage, 'quarantine': errors,
            'common_action': action,
            'decision': {'coverage-blocked': 'blocked', 'repair-required': 'comments',
                         'advisory': 'comments', 'none': 'approved'}[action],
            'handoff': 'Review must verify current target and posting authority before acceptance.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('judgment', type=Path, nargs='?')
    parser.add_argument('output', type=Path, nargs='?')
    parser.add_argument('--preflight', action='store_true',
                        help='validate source inputs without Judge or output writes')
    args = parser.parse_args()
    try:
        if args.preflight:
            require(args.judgment is None and args.output is None,
                    'preflight accepts only a manifest and writes no artifact')
            manifest = json.loads(args.manifest.read_text())
            result = preflight(manifest, args.manifest.parent)
            print(json.dumps(result, ensure_ascii=False))
            return 0 if result['status'] == 'ready' else 1
        require(args.judgment is not None and args.output is not None,
                'assembly requires manifest, judgment and output')
        require(not args.output.exists(), 'refusing to overwrite an existing artifact')
        manifest = json.loads(args.manifest.read_text())
        judgment = json.loads(args.judgment.read_text())
        result = assemble(manifest, judgment, args.manifest.parent)
        repository = Path(result['target']['repository'])
        if repository.is_dir():
            require(not args.output.resolve().is_relative_to(repository.resolve()),
                    'output must be outside the reviewed repository')
        # Exclusive creation prevents replacing source evidence through an alias/race.
        data = (json.dumps(result, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
        with args.output.open('xb') as stream:
            stream.write(data)
        print(json.dumps({'path': str(args.output), 'bytes': len(data),
                          'sha256': digest(data), 'common_action': result['common_action']}))
    except (Invalid, ValueError, OSError, TypeError, KeyError) as exc:
        if args.preflight:
            print(json.dumps({'assembly_version': 1, 'status': 'blocked', 'error': str(exc)}))
        else:
            print(f'assembly rejected: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
