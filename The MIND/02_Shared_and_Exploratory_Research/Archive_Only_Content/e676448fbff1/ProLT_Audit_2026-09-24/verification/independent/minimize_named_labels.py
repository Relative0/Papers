"""Exact one-/two-bit compression certificates for three named examples.
Uses only the standard library; runs after audit_checks.py has produced inputs.
"""
from pathlib import Path
from collections import deque
import json

ROOT = Path(__file__).resolve().parent

def certificate(name):
    data = json.loads((ROOT / (name + '.json')).read_text())
    n = data['n']
    p = set(map(tuple, data['P_strict']))
    q = set(map(tuple, data['Q_strict'])) | {(i, i) for i in range(n)}
    demands = sorted(p - q)
    adj = [set() for _ in demands]
    for i, (x, y) in enumerate(demands):
        for j, (u, v) in enumerate(demands[:i]):
            if (x, v) in q or (u, y) in q:
                adj[i].add(j)
                adj[j].add(i)
    colors, parents = {}, {}
    odd = None
    for start in range(len(demands)):
        if start in colors:
            continue
        colors[start] = 0
        parents[start] = None
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in sorted(adj[u]):
                if v not in colors:
                    colors[v] = 1 - colors[u]
                    parents[v] = u
                    queue.append(v)
                elif colors[v] == colors[u] and odd is None:
                    path_u, path_v = [], []
                    x = u
                    while x is not None:
                        path_u.append(x)
                        x = parents[x]
                    x = v
                    while x is not None:
                        path_v.append(x)
                        x = parents[x]
                    meet = next(x for x in path_u if x in path_v)
                    odd = path_u[:path_u.index(meet)+1] + list(reversed(path_v[:path_v.index(meet)]))
                    assert len(odd) % 2 == 1
                    assert all(odd[(i+1) % len(odd)] in adj[odd[i]] for i in range(len(odd)))
    result = {'example': name, 'demands': demands,
              'conflict_edges': [(i, j) for i in range(len(adj)) for j in sorted(adj[i]) if i < j],
              'bipartite': odd is None}
    if odd is None:
        k = (2 if any(adj) else 1) if demands else 0
        labels = [0] * n
        for color in range(k):
            firsts = [demands[i][0] for i in range(len(demands)) if colors[i] == color]
            for v in range(n):
                if any((x, v) in q for x in firsts):
                    labels[v] |= 1 << color
        realized = {(x, y) for x, y in p if labels[x] & ~labels[y] == 0}
        assert realized == q - {(i, i) for i in range(n)}
        result.update({'minimum_bits': k, 'compressed_labels': labels,
                       'lower_bound': 'nonempty conflict edge' if k == 2 else 'P differs from Q' if k else 'P equals Q'})
    else:
        assert name == 'cyclic_8'
        labels = data['labels']
        assert max(labels) < 8
        assert {(x,y) for x,y in p if labels[x] & ~labels[y] == 0} == q - {(i,i) for i in range(n)}
        result.update({'minimum_bits': 3, 'original_three_bit_labels': labels,
                       'odd_cycle_demand_indices': odd,
                       'odd_cycle_demands': [demands[i] for i in odd]})
    (ROOT / (name + '_minimal_labels.json')).write_text(json.dumps(result, indent=2))
    print(json.dumps({k: v for k, v in result.items() if k not in ('demands','conflict_edges')}, indent=2))
    return result

if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Assertions must be enabled')
    for name in ('compensating_5','torsion2_RP2_13','cyclic_8'):
        certificate(name)
