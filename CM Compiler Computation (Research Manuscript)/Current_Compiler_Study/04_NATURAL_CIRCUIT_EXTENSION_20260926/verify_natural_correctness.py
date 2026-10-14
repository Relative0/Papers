"""Read-only recount of the frozen natural correctness run."""
from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json

from natural_correctness import CASES, HERE, RUN, verify_freeze


def main():
    verify_freeze()
    raw = (RUN / 'CORRECTNESS.jsonl').read_bytes()
    summary = json.loads((RUN / 'SUMMARY.json').read_text(encoding='utf-8'))
    rows = [json.loads(line) for line in raw.splitlines()]
    if len(rows) != len(CASES) or len(rows) != 71:
        raise ValueError('case count mismatch')
    if summary['result_sha256'] != sha256(raw).hexdigest():
        raise ValueError('raw result digest mismatch')
    outcomes = {strategy: Counter() for strategy in ('pure_structural', 'hybrid', 'retabulate')}
    supports = Counter()
    for index, (row, case) in enumerate(zip(rows, CASES)):
        if (row['case_index'] != index or row['design'] != case['design']
                or row['output'] != case['output'] or row['status'] != 'PASS'):
            raise ValueError(f'case/status mismatch at {index}')
        source = case['source_truth_sha256']
        if row['source_truth_sha256'] != source or any(
                value != source for value in row['truth_sha256'].values()):
            raise ValueError(f'backend truth mismatch at {index}')
        if set(row['truth_sha256']) != {'direct_packed', 'ordinary_cm_ir', 'abc_aig'}:
            raise ValueError(f'backend inventory mismatch at {index}')
        for strategy in outcomes:
            arm = row['strategies'][strategy]
            outcomes[strategy][arm['root_outcome']] += 1
            if arm['token_returned'] and arm['truth_sha256'] != source:
                raise ValueError(f'pair token mismatch at {index}: {strategy}')
        supports[row['support_count']] += 1
    if summary['status'] != 'PASS' or summary['passed'] != 71 or summary['failed'] != 0:
        raise ValueError('summary mismatch')
    result = {'status': 'PASS_READ_ONLY_RECOUNT', 'case_count': len(rows),
              'raw_sha256': sha256(raw).hexdigest(),
              'hybrid_outcomes': dict(outcomes['hybrid']),
              'pure_structural_outcomes': dict(outcomes['pure_structural']),
              'retabulate_outcomes': dict(outcomes['retabulate']),
              'support_distribution': dict(sorted(supports.items())),
              'performance_measured': False}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
