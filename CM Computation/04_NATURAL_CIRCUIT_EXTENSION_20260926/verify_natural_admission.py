"""Verify frozen EPFL inputs and exhaustive BLIF-to-AST translation."""
from __future__ import annotations

from hashlib import sha1, sha256
import json
from pathlib import Path
import sys

from prepare_natural_admission import (HERE, SOURCE, CM_SOURCE, ast_stats,
                                       bounded_cone, parse, translated)

sys.path.insert(0, str(CM_SOURCE))
from bitset_backend import eval_expr_bitset  # noqa: E402


def rows(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line]


def main():
    manifest = json.loads((HERE / 'NATURAL_ADMISSION.json').read_text(encoding='utf-8'))
    assert manifest['status'] == 'ADMISSION_ONLY_NO_CM_COMPILATION_OR_TIMING'
    assert sha256((HERE / 'NATURAL_ADMISSION_RULES.md').read_bytes()).hexdigest() == manifest['rule_sha256']
    assert sha256((HERE / 'prepare_natural_admission.py').read_bytes()).hexdigest() == manifest['script_sha256']
    cases = rows(HERE / 'NATURAL_CASES.jsonl')
    screens = rows(HERE / 'NATURAL_SCREEN.jsonl')
    assert len(cases) == manifest['selected_cases']
    assert len(screens) == sum(d.get('primary_outputs', 0) for d in manifest['designs'])
    assert sum(c['status'] == 'ADMITTED_PREMEASUREMENT' for c in cases) == manifest['admitted_cases']
    for design in manifest['designs']:
        path = SOURCE / design['relative_path']
        raw = path.read_bytes()
        assert len(raw) == design['bytes'] and sha256(raw).hexdigest() == design['sha256']
        assert sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == design['git_blob_sha1']
        inputs, outputs, nodes = parse(path)
        recorded = [row for row in screens if row['design'] == design['design']]
        assert len(recorded) == len(outputs)
        assert [row['output'] for row in recorded] == list(outputs)
        eligible = []
        for output, row in zip(outputs, recorded):
            metadata, reason = bounded_cone(output, inputs, nodes)
            assert row['structural_status'] == ('eligible' if metadata is not None else reason)
            if metadata is not None:
                assert all(row[key] == (list(value) if key == 'support' else value)
                           for key, value in metadata.items())
                eligible.append(row)
        selected = {row['output'] for row in sorted(
            eligible, key=lambda item: (item['rank_sha256'], item['output']))[:8]}
        assert {row['output'] for row in recorded if row['selected']} == selected
        assert {case['output'] for case in cases if case['design'] == design['design']} == selected
    for case in cases:
        if case['status'] != 'ADMITTED_PREMEASUREMENT':
            continue
        design = next(d for d in manifest['designs'] if d['design'] == case['design'])
        _, _, nodes = parse(SOURCE / design['relative_path'])
        expr = translated(case['output'], case['support'], nodes)
        assert ast_stats(expr) == {key: case[key] for key in (
            'translated_ast_sha256', 'ast_unique_object_nodes', 'ast_occurrences',
            'identity_shared_nodes', 'equal_but_distinct_object_nodes')}
        width = 1 << len(case['support'])
        env = {f'x{j}': sum(((assignment >> j) & 1) << assignment for assignment in range(width))
               for j in range(len(case['support']))}
        bits = eval_expr_bitset(expr, env)
        digest = sha256(len(case['support']).to_bytes(1, 'little')
                        + bits.to_bytes((width + 7) // 8, 'little')).hexdigest()
        assert digest == case['source_truth_sha256'], (case['design'], case['output'])
    result = {'status': 'PASS', 'source_files': len(manifest['designs']),
              'screened_outputs': len(screens), 'cases': len(cases),
              'exhaustive_ast_blif_agreements': manifest['admitted_cases'],
              'scope': 'No CM pair compiler or timing invoked'}
    (HERE / 'NATURAL_VALIDATION.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
