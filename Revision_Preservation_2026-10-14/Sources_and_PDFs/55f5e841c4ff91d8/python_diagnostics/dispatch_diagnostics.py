"""Exploratory, untimed exact-dispatch and canonical-CSE diagnostics.

Original artifacts remain untouched. This script imports the relocated runtime copy.
No performance conclusion is inferred from these operation-count experiments.
"""
from __future__ import annotations

from _collections import _count_elements
from collections import Counter
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import random
import sys

HERE = Path(__file__).resolve().parent
RUNTIME = HERE.parent / 'runtime'
sys.path.insert(0, str(RUNTIME / 'cm_n2_p13_run'))
import n2_p13_harness as h

base = h.base
GATE = h.load_gate()
REPEAT_NUM, REPEAT_DEN = GATE['tree']['threshold'][h.REPEAT_NODE].as_integer_ratio()
REUSE_NUM, REUSE_DEN = GATE['tree']['threshold'][h.REUSE_NODE].as_integer_ratio()
MIN_BINARY = (4 * REPEAT_DEN + REPEAT_NUM - 1) // REPEAT_NUM


def exact_stats(f):
    counts = Counter()
    uses = Counter()
    edges = 0
    for n in f.nodes:
        ids = tuple(c.nid for c in n.args)
        uses.update(ids)
        edges += len(ids)
        if len(ids) == 2 and n.op in ('and', 'or', 'xor', 'tf'):
            counts[tuple(sorted(ids))] += 1
    binaries = sum(counts.values())
    repeat = binaries - len(counts)
    reuse = edges - len(uses)
    return dict(nodes=len(f.nodes), edges=edges, binaries=binaries,
                repeat=repeat, reuse=reuse, distinct_pairs=len(counts),
                shells=max(counts.values(), default=0),
                unreachable_use_roots=len(f.nodes) - len(uses),
                min_binary_bypass=binaries < MIN_BINARY,
                reuse_bound_bypass=max(0, edges-len(f.nodes)+1)*REUSE_DEN > edges*REUSE_NUM)


def ref_decision(s):
    return (s['shells'] >= 5 and s['repeat']*REPEAT_DEN <= s['binaries']*REPEAT_NUM
            and s['reuse']*REUSE_DEN <= s['edges']*REUSE_NUM)


class TupleBoundFactory(base.Factory):
    """Exact decision prototype: cached ID tuples, stronger bounds, one count pass.

    _make preserves all structural identities and ordering. This deliberately
    returns just the decision: P13 diagnostics/leaf reporting remain untimed.
    """
    def __init__(self):
        self.cache = {}
        self.nodes = []
        self.edge_count = 0
        self.pairs = []

    def _make(self, op, args=(), value=None):
        args = tuple(args)
        ids = tuple(a.nid for a in args)
        key = (op, ids, value)
        cache = self.cache
        node = cache.get(key)
        if node is not None:
            return node
        nodes = self.nodes
        node = base.Node(len(nodes), op, args, value)
        cache[key] = node
        nodes.append(node)
        arity = len(args)
        self.edge_count += arity
        if arity == 2 and op in ('and', 'or', 'xor', 'tf'):
            a, b = ids
            self.pairs.append(ids if a <= b else (b, a))
        return node

    def dispatch_bool(self):
        b = len(self.pairs)
        if b < MIN_BINARY:
            return False
        allowed_reuse = self.edge_count*REUSE_NUM // REUSE_DEN
        if self.edge_count - len(self.nodes) + 1 > allowed_reuse:
            return False
        counts = {}
        _count_elements(counts, self.pairs)
        repeat = b-len(counts)
        if repeat*REPEAT_DEN > b*REPEAT_NUM or repeat < 4:
            return False
        if max(counts.values()) < 5:
            return False
        used = bytearray(len(self.nodes))
        reuse = 0
        for node in self.nodes:
            for child in node.args:
                i = child.nid
                if used[i]:
                    reuse += 1
                    if reuse > allowed_reuse:
                        return False
                else:
                    used[i] = 1
        return True


class CanonicalFactory(base.Factory):
    def bin(self, op, a, b):
        if op in ('and', 'or', 'xor') and a.nid > b.nid:
            a, b = b, a
        return super().bin(op, a, b)


def recipes():
    cal = json.loads((RUNTIME/'cm_n2_p8_run/calibration.json').read_text())
    for split, getter in [('training', h.p8.training_synthetic_recipes),
                          ('validation', h.p8.validation_synthetic_recipes)]:
        for cid, kind, depth, build in getter():
            yield split, cid, build
        for cid, kind, depth, build, oracle, extra in h.p8.epfl_recipes(
                'train' if split == 'training' else split, cal['selection']):
            yield split, cid, build
    for cid, depth, idx, build in h.p8.gatep_eval_recipes():
        yield 'gatep', cid, build
    for cid, circuit, depth, build, oracle, extra in h.p8.natural_eval_recipes()[0]:
        yield 'natural', cid, build


def main():
    records = []
    failures = []
    for split, cid, build in recipes():
        f, root, nv = build(h.DeferredPairTelemetryFactory)
        g, gr, gn = build(TupleBoundFactory)
        s = exact_stats(f)
        d = f.dispatch(GATE)[0]
        new = g.dispatch_bool()
        structure_same = list(f.cache) == list(g.cache)
        if not (d == new == ref_decision(s) and structure_same):
            failures.append(dict(split=split, cid=cid, ref=d, new=new, structure_same=structure_same))
        records.append(dict(split=split, cid=cid, annotate=d, **s))

    canonical_rows = []
    for cid, depth, idx, build in h.p8.gatep_eval_recipes():
        f, r, nv = build(base.Factory)
        c, cr, cn = build(CanonicalFactory)
        p, st = base.lower_anf(r)
        cp, cst = base.lower_anf(cr)
        inf = h.p8.p6.InNodeFactory()
        ar, _ = h.p8.p6.clone_dag(cr, inf)
        ap, ast, dst = h.p8.p6.lower_p6(ar, inf, collect_stats=True)
        same = (p == cp == ap and base.eval_node_bitset(r, nv) == base.eval_node_bitset(cr, cn))
        if not same:
            failures.append(dict(cid=cid, problem='canonical semantic drift'))
        old = exact_stats(f)
        new = exact_stats(c)
        canonical_rows.append(dict(cid=cid, depth=depth, semantics_equal=same,
                                   original=old, canonical=new, original_annotate=ref_decision(old),
                                   canonical_annotate=ref_decision(new),
                                   direct=asdict(st), canonical_direct=asdict(cst),
                                   canonical_always_p6=asdict(ast), canonical_p6_selection=asdict(dst)))

    # Extra DAG generator targets tf shells, high sharing, CSE hits, orientation,
    # n-ary edges, and dead constructed nodes; no benchmark decisions are tuned.
    seed = 20260918 ^ 0xD14A
    rng = random.Random(seed)
    adversarial = []
    for i in range(2000):
        actions = []
        for _ in range(rng.randrange(4, 160)):
            actions.append((rng.randrange(7), rng.getrandbits(16), rng.getrandbits(16), rng.randrange(16)))
        def build(cls):
            fac = cls()
            nodes = [fac.var(j) for j in range(8)]
            for op, ia, ib, tok in actions:
                a, b = nodes[ia % len(nodes)], nodes[ib % len(nodes)]
                if op < 3:
                    n = fac.bin(('and', 'or', 'xor')[op], a, b)
                elif op == 3:
                    n = fac.tf(tok, a, b)
                elif op == 4:
                    n = fac.not_(a)
                else:
                    n = fac.nary('andn' if op == 5 else 'orn', (a, b, nodes[(ia+ib) % len(nodes)]))
                nodes.append(n)
            return fac, nodes[-1], 8
        f, r, nv = build(h.DeferredPairTelemetryFactory)
        g, gr, _ = build(TupleBoundFactory)
        s = exact_stats(f)
        d = f.dispatch(GATE)[0]
        if not(d == g.dispatch_bool() == ref_decision(s) and list(f.cache) == list(g.cache)):
            failures.append(dict(cid=i, problem='adversarial dispatch mismatch'))
        adversarial.append(s)

    # Decision boundaries using abstract legal multiset features. No claim that
    # each independently varied tuple has a realizable DAG.
    boundary_checks = 0
    for b in range(1, 1000):
        allowed = b*REPEAT_NUM // REPEAT_DEN
        for repeat in set([0, 3, 4, max(0, allowed-1), allowed, allowed+1]):
            for shell in (4, 5, 6):
                if shell > repeat+1 or shell > b:
                    continue
                if shell >= 5 and repeat*REPEAT_DEN <= b*REPEAT_NUM:
                    assert b >= MIN_BINARY
                boundary_checks += 1
    for e in range(0, 1000):
        allowed = e*REUSE_NUM // REUSE_DEN
        for reuse in (max(0, allowed-1), allowed, allowed+1):
            assert (reuse*REUSE_DEN <= e*REUSE_NUM) == (reuse <= allowed)
            boundary_checks += 1

    by_split = {}
    for split in ('training','validation','gatep','natural'):
        rows = [r for r in records if r['split'] == split]
        by_split[split] = dict(cases=len(rows), annotated=sum(r['annotate'] for r in rows),
                              min_binary_bypass=sum(r['min_binary_bypass'] for r in rows),
                              reuse_bound_bypass=sum(r['reuse_bound_bypass'] for r in rows),
                              either_bound=sum(r['min_binary_bypass'] or r['reuse_bound_bypass'] for r in rows))
    out = dict(exploratory=True, timed=False, code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               python=sys.version, minimum_binary=MIN_BINARY, seed=seed,
               checks=dict(recorded_cases=len(records), adversarial_cases=len(adversarial), boundaries=boundary_checks),
               by_split=by_split, failures=failures, records=records, canonical_gatep=canonical_rows,
               adversarial_summary=dict(annotated=sum(ref_decision(s) for s in adversarial),
                                         min_binary=sum(s['min_binary_bypass'] for s in adversarial),
                                         reuse_bound=sum(s['reuse_bound_bypass'] for s in adversarial)))
    (HERE/'dispatch_diagnostics.json').write_text(json.dumps(out, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:out[k] for k in ('checks','minimum_binary','by_split','failures','adversarial_summary')}, indent=2))


if __name__ == '__main__':
    main()
