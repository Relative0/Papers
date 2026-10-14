"""Auditable Boolean artifacts, v1 reference implementation.

Assignments use the stated variable order, first variable most significant.
The integer truth vector has bit a equal to f(a). No third-party dependencies.
Costs are reference-Python costs, not optimized synthesis-tool claims.
"""
from __future__ import annotations
from dataclasses import dataclass
from collections import Counter
from itertools import combinations
import json
from math import prod


def assignments(n: int):
    return range(1 << n)


def bits_of(a: int, n: int) -> tuple[int, ...]:
    return tuple((a >> (n - 1 - j)) & 1 for j in range(n))


def index_of(values) -> int:
    a = 0
    for value in values:
        a = (a << 1) | int(value)
    return a


def selected_indices(scope: tuple[int, ...], rho: dict[int, int]) -> tuple[int, ...]:
    tests = [(len(scope)-1-i, rho[v]) for i, v in enumerate(scope) if v in rho]
    return tuple(a for a in assignments(len(scope)) if all(((a >> i) & 1) == b for i, b in tests))


def restrict_table(bits: int, scope: tuple[int, ...], rho: dict[int, int]):
    indices = selected_indices(scope, rho)
    result = sum(((bits >> a) & 1) << j for j, a in enumerate(indices))
    return result, tuple(v for v in scope if v not in rho)


def matrix_rows(bits: int, scope: tuple[int, ...], left: tuple[int, ...]):
    right = tuple(v for v in scope if v not in left)
    out = []
    for a in assignments(len(left)):
        env = dict(zip(left, bits_of(a, len(left))))
        row = 0
        for b in assignments(len(right)):
            env.update(zip(right, bits_of(b, len(right))))
            index = index_of(env[v] for v in scope)
            row |= ((bits >> index) & 1) << b
        out.append(row)
    return tuple(out), right


def rank_factor(rows: tuple[int, ...]):
    """Return coefficients and independent original basis rows over F2."""
    pivots: dict[int, tuple[int, int]] = {}
    basis = []
    coefficients = []
    for row in rows:
        value, coef = row, 0
        while value:
            p = value.bit_length() - 1
            if p not in pivots:
                bit = 1 << len(basis)
                basis.append(row)
                pivots[p] = (value, coef ^ bit)
                coef = bit  # This source row is the newly introduced basis row.
                break
            val, rep = pivots[p]
            value ^= val
            coef ^= rep
        coefficients.append(coef)
    return tuple(coefficients), tuple(basis)


def cofactor_payload(rows: tuple[int, ...], width: int):
    mask = (1 << width) - 1
    prototypes, lookup, references = [], {}, []
    for row in rows:
        representative = min(row, row ^ mask)
        if representative not in lookup:
            lookup[representative] = len(prototypes)
            prototypes.append(representative)
        references.append((lookup[representative], int(row != representative)))
    return tuple(prototypes), tuple(references)


def _tupleize(value):
    return tuple(_tupleize(x) for x in value) if isinstance(value, list) else value


@dataclass(frozen=True)
class Artifact:
    kind: str
    scope: tuple[int, ...]
    payload: tuple

    def dumps(self) -> bytes:
        # No claimed rank/minimum/cost/hash is trusted; costs come from payload.
        return json.dumps({'schema': 'sc-reference/v1', 'kind': self.kind,
                           'scope': self.scope, 'payload': self.payload},
                          separators=(',', ':'), sort_keys=True).encode('ascii')

    @staticmethod
    def loads(blob: bytes) -> 'Artifact':
        def strict_pairs(pairs):
            d = {}
            for k, v in pairs:
                if k in d:
                    raise ValueError('duplicate JSON key')
                d[k] = v
            return d
        doc = json.loads(blob, object_pairs_hook=strict_pairs)
        if set(doc) != {'schema', 'kind', 'scope', 'payload'} or doc['schema'] != 'sc-reference/v1':
            raise ValueError('wrong schema')
        return Artifact(doc['kind'], tuple(doc['scope']), _tupleize(doc['payload']))

    def ideal_bits(self) -> int:
        """Logical payload only: scopes, tags, lengths and allocation excluded."""
        if self.kind == 'flat':
            return 1 << len(self.scope)
        if self.kind in ('xor', 'product'):
            factors = self.payload[1] if self.kind == 'xor' else self.payload[0]
            return int(self.kind == 'xor') + sum(1 << len(s) for s, _ in factors)
        left, right = self.payload[:2]
        R, C = 1 << len(left), 1 << len(right)
        if self.kind == 'rank':
            return len(self.payload[3]) * (R + C)
        if self.kind == 'cofactor':
            k = len(self.payload[2])
            return k*C + R*((max(k, 1)-1).bit_length()+1)
        raise ValueError('unknown kind')

    def condition(self, rho: dict[int, int]) -> 'Artifact':
        if not set(rho) <= set(self.scope) or any(type(v) is not int or v not in (0, 1) for v in rho.values()):
            raise ValueError('assignment outside declared universe or non-Boolean value')
        remaining = tuple(v for v in self.scope if v not in rho)
        if self.kind == 'flat':
            bits, _ = restrict_table(self.payload[0], self.scope, rho)
            return Artifact('flat', remaining, (bits,))
        if self.kind in ('xor', 'product'):
            factors = self.payload[1] if self.kind == 'xor' else self.payload[0]
            new = []
            for scope, bits in factors:
                table, rem = restrict_table(bits, scope, rho)
                new.append((rem, table))
            return Artifact(self.kind, remaining,
                            (self.payload[0], tuple(new)) if self.kind == 'xor' else (tuple(new),))
        left, right = self.payload[:2]
        li, ri = selected_indices(left, rho), selected_indices(right, rho)
        nl, nr = tuple(v for v in left if v not in rho), tuple(v for v in right if v not in rho)
        if self.kind == 'rank':
            coef, basis = self.payload[2:]
            newbasis = tuple(sum(((b >> col) & 1) << j for j, col in enumerate(ri)) for b in basis)
            return Artifact('rank', remaining, (nl, nr, tuple(coef[i] for i in li), newbasis))
        if self.kind == 'cofactor':
            prototypes, refs = self.payload[2:]
            sliced = tuple(sum(((b >> col) & 1) << j for j, col in enumerate(ri)) for b in prototypes)
            # Recanonicalize without constructing the R by C matrix.
            mask = (1 << len(ri)) - 1
            lookup, newp, newrefs = {}, [], []
            for i in li:
                j, flip = refs[i]
                value = sliced[j]
                canonical = min(value, value ^ mask)
                if canonical not in lookup:
                    lookup[canonical] = len(newp)
                    newp.append(canonical)
                newrefs.append((lookup[canonical], flip ^ int(value != canonical)))
            return Artifact('cofactor', remaining, (nl, nr, tuple(newp), tuple(newrefs)))
        raise ValueError('unknown kind')

    def count(self) -> int:
        if self.kind == 'flat':
            return self.payload[0].bit_count()
        if self.kind in ('xor', 'product'):
            factors = self.payload[1] if self.kind == 'xor' else self.payload[0]
            ones = [b.bit_count() for _, b in factors]
            if self.kind == 'product':
                return prod(ones)
            sizes = [1 << len(s) for s, _ in factors]
            return (prod(sizes) - (-1)**self.payload[0] * prod(t-2*o for t, o in zip(sizes, ones))) // 2
        left, right, a, b = self.payload
        if self.kind == 'rank':
            total = 0
            for coef, multiplicity in Counter(a).items():
                row = 0
                for j, base in enumerate(b):
                    if (coef >> j) & 1:
                        row ^= base
                total += multiplicity * row.bit_count()
            return total
        if self.kind == 'cofactor':
            weights = [p.bit_count() for p in a]
            C = 1 << len(right)
            return sum(C-weights[j] if flip else weights[j] for j, flip in b)
        raise ValueError('unknown kind')

    def query(self, rho: dict[int, int]) -> int:
        return self.condition(rho).count()


def xor_artifact(bits: int, scope: tuple[int, ...]) -> Artifact:
    n = len(scope)
    anf = [(bits >> a) & 1 for a in assignments(n)]
    for b in range(n):
        for a in assignments(n):
            if (a >> b) & 1:
                anf[a] ^= anf[a ^ (1 << b)]
    parent = list(range(n))
    def root(i):
        while parent[i] != i:
            i = parent[i]
        return i
    terms = []
    for a in range(1, 1 << n):
        if anf[a]:
            ids = [j for j in range(n) if (a >> (n-1-j)) & 1]
            for j in ids[1:]:
                parent[root(j)] = root(ids[0])
            terms.append(ids)
    groups = {}
    for j in range(n):
        groups.setdefault(root(j), []).append(j)
    factors = []
    for group in groups.values():
        local = [tuple(group.index(j) for j in term) for term in terms if term[0] in group]
        table = 0
        for a in assignments(len(group)):
            values = bits_of(a, len(group))
            value = sum(all(values[j] for j in term) for term in local) & 1
            table |= value << a
        factors.append((tuple(scope[j] for j in group), table))
    return Artifact('xor', scope, (anf[0], tuple(factors)))


def factor_candidates(bits: int, scope: tuple[int, ...], left: tuple[int, ...]):
    rows, right = matrix_rows(bits, scope, left)
    coef, basis = rank_factor(rows)
    yield Artifact('rank', scope, (left, right, coef, basis))
    prototypes, refs = cofactor_payload(rows, 1 << len(right))
    yield Artifact('cofactor', scope, (left, right, prototypes, refs))
    nonzero = set(rows) - {0}
    if len(nonzero) <= 1:
        pattern = next(iter(nonzero), 0)
        table = sum(int(bool(row)) << i for i, row in enumerate(rows))
        yield Artifact('product', scope, (((left, table), (right, pattern)),))


def partitions(scope: tuple[int, ...], budget: int = 16):
    if len(scope) < 2:
        return ()
    out = []
    for left in [(v,) for v in scope] + [s for size in sorted(range(1, len(scope)), key=lambda k: (abs(2*k-len(scope)), k))
                                          for s in combinations(scope, size) if scope[0] in s]:
        if left not in out:
            out.append(left)
        if len(out) >= budget:
            break
    return tuple(out)


def discover(bits: int, n: int, budget: int = 16):
    if not 0 <= n <= 16 or bits < 0 or bits.bit_length() > (1 << n):
        raise ValueError('invalid truth vector or reference size limit')
    scope = tuple(range(n))
    candidates = [Artifact('flat', scope, (bits,)), xor_artifact(bits, scope)]
    for left in partitions(scope, budget):
        candidates.extend(factor_candidates(bits, scope, left))
    # Frozen deterministic selection, actual JSON bytes, then ideal bits, kind, bytes.
    candidates.sort(key=lambda a: (len(a.dumps()), a.ideal_bits(), a.kind, a.dumps()))
    return candidates[0], tuple(candidates)


def walsh_count(artifact: Artifact) -> int:
    """Dense-rank profile identity; exponential in stored inner dimension."""
    if artifact.kind != 'rank':
        raise ValueError('rank artifact required')
    left, right, coef, basis = artifact.payload
    r, C = len(basis), 1 << len(right)
    if r > 20:
        raise ValueError('reference Walsh workspace limit exceeded')
    hist = [0] * (1 << r)
    for c in range(C):
        profile = sum(((row >> c) & 1) << j for j, row in enumerate(basis))
        hist[profile] += 1
    step = 1
    while step < len(hist):
        for i in range(0, len(hist), 2*step):
            for j in range(step):
                a, b = hist[i+j], hist[i+j+step]
                hist[i+j], hist[i+j+step] = a+b, a-b
        step *= 2
    signsum = sum(m * hist[u] for u, m in Counter(coef).items())
    return (len(coef)*C - signsum) // 2
