"""Scoped use of the separately supplied process-semantics implementation."""
import argparse
from collections import Counter
import csv
import hashlib
from itertools import product
import json
from pathlib import Path
import sys
import time
import unittest

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'companion_source'))
import verify_semantics as companion
from test_semantics import SemanticsChecks
from p01_independent_checks import Ring, smith2


def main():
    if not __debug__:
        raise RuntimeError('Assertions are required; do not use optimized Python')
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    start = time.monotonic()
    counts = Counter()
    ring = Ring(2, 4)
    for matrix in product(range(16), repeat=4):
        a, b = companion.smith(matrix)
        if (a, b) != smith2(ring, matrix):
            raise AssertionError(('Smith disagreement', matrix))
        if companion.rank(companion.rho(matrix)) != 8-a-b:
            raise AssertionError(('Binary rank disagreement', matrix))
        counts[a, b] += 1
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(SemanticsChecks)
    tests = unittest.TextTestRunner(verbosity=2).run(suite)
    if not tests.wasSuccessful():
        raise AssertionError('Companion regression failure')
    result = dict(
        status='PASS', matrices=65536, smith_mismatches=0,
        binary_rank_mismatches=0, regression_tests=tests.testsRun,
        inventory=[dict(a=a, b=b, count=n) for (a, b), n in sorted(counts.items())],
        source_sha256={p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in sorted((ROOT / 'companion_source').glob('*.py'))},
        scope='All length-four 2x2 Smith types and regular binary ranks; 10 supplied regression tests. No full support solve or full historical campaign.',
        seconds=time.monotonic()-start,
    )
    args.out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
