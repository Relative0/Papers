"""Export admitted primary-output cones as deterministic one-output BLIFs."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

from prepare_natural_admission import HERE, SOURCE, parse, relevant, truth_digest


def main():
    manifest = json.loads((HERE / 'NATURAL_ADMISSION.json').read_text(encoding='utf-8'))
    designs = {item['design']: item for item in manifest['designs']}
    cases = [json.loads(line) for line in (HERE / 'NATURAL_CASES.jsonl').read_text(encoding='utf-8').splitlines()]
    out_dir = HERE / 'cones'
    output_manifest = HERE / 'CONES_MANIFEST.json'
    if out_dir.exists() or output_manifest.exists():
        raise RuntimeError('Cone export already exists; use a copy to regenerate')
    out_dir.mkdir()
    records = []
    for index, case in enumerate(cases):
        if case['status'] != 'ADMITTED_PREMEASUREMENT':
            continue
        _, _, nodes = parse(SOURCE / designs[case['design']]['relative_path'])
        order, seen, active = [], set(), set()

        def visit(signal):
            if signal in case['support']:
                return
            if signal in seen:
                return
            if signal in active:
                raise ValueError('cyclic cone')
            active.add(signal)
            for child in relevant(nodes[signal]):
                visit(child)
            active.remove(signal)
            seen.add(signal)
            order.append(signal)

        visit(case['output'])
        lines = [f'.model epfl_case_{index:04d}',
                 '.inputs ' + ' '.join(case['support']),
                 '.outputs ' + case['output']]
        for signal in order:
            node = nodes[signal]
            active_indices = [j for j in range(len(node.fanins))
                              if any(cube[j] in '01' for cube in node.cubes)]
            fanins = [node.fanins[j] for j in active_indices]
            lines.append('.names ' + ' '.join(fanins + [signal]))
            for pattern in node.cubes:
                projected = ''.join(pattern[j] for j in active_indices)
                lines.append((projected + ' ' if projected else '') + str(node.polarity))
        lines.append('.end')
        name = f'{index:04d}_{case["design"]}.blif'
        blob = ('\n'.join(lines) + '\n').encode('utf-8')
        path = out_dir / name
        path.write_bytes(blob)
        inputs, outputs, extracted = parse(path)
        assert inputs == tuple(case['support']) and outputs == (case['output'],)
        assert truth_digest(case['output'], case['support'], extracted) == case['source_truth_sha256']
        records.append({'case_index': index, 'design': case['design'],
                        'source_output': case['output'], 'path': 'cones/' + name,
                        'sha256': sha256(blob).hexdigest(), 'bytes': len(blob),
                        'source_nodes': len(order),
                        'truth_sha256': case['source_truth_sha256']})
    result = {'status': 'PASS_SOURCE_EQUIVALENT_NO_CM_COMPILATION_OR_TIMING',
              'case_count': len(records), 'export_script_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
              'records': records}
    output_manifest.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': result['status'], 'case_count': len(records)}))


if __name__ == '__main__':
    main()
