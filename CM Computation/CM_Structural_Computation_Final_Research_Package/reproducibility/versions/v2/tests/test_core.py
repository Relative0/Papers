"""Exhaustive small-domain semantic tests, executable without pytest."""
from __future__ import annotations
import sys, json, time
from pathlib import Path
from itertools import product
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'code'))
from artifacts import Artifact, discover, factor_candidates, xor_artifact, bits_of
from checker import verify, evaluate


def reference_restrict(bits, n, rho):
    free = [j for j in range(n) if j not in rho]
    out = 0
    for a in range(2**len(free)):
        env = dict(rho)
        for j, v in enumerate(free):
            env[v] = (a // 2**(len(free)-j-1)) % 2
        index = sum(env[j] * 2**(n-j-1) for j in range(n))
        out += ((bits // 2**index) % 2) * 2**a
    return out


def run():
    started = time.perf_counter()
    stats = {'functions': 0, 'artifacts': 0, 'conditioning_checks': 0,
             'serialization_checks': 0, 'corruption_rejections': 0}
    for n in range(4):
        scope = tuple(range(n))
        for truth in range(2**(2**n)):
            stats['functions'] += 1
            artifacts = [Artifact('flat', scope, (truth,)), xor_artifact(truth, scope)]
            if n >= 2:
                for mask in range(1, 2**n-1):
                    left = tuple(j for j in range(n) if (mask >> j) & 1)
                    artifacts.extend(factor_candidates(truth, scope, left))
            for artifact in artifacts:
                stats['artifacts'] += 1
                assert verify(artifact, truth), (n, truth, artifact)
                assert artifact.count() == truth.bit_count()
                roundtrip = Artifact.loads(artifact.dumps())
                assert artifact == roundtrip and verify(roundtrip, truth)
                stats['serialization_checks'] += 1
                assert not verify(artifact, truth ^ 1)
                stats['corruption_rejections'] += 1
                for values in product((-1, 0, 1), repeat=n):
                    rho = {j: value for j, value in enumerate(values) if value != -1}
                    expected = reference_restrict(truth, n, rho)
                    reduced = artifact.condition(rho)
                    assert verify(reduced, expected), (n, truth, artifact.kind, rho)
                    assert reduced.count() == expected.bit_count(), (n, truth, artifact, rho)
                    stats['conditioning_checks'] += 1
    stats['elapsed_seconds'] = time.perf_counter() - started
    stats['status'] = 'PASS'
    return stats

if __name__ == '__main__':
    result = run()
    path = Path(__file__).resolve().parents[1] / 'raw_results' / 'core_exhaustive_v1.json'
    path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
