"""Frozen P14-PY0 implementations and deterministic benchmark recipes.

This module contains no timing or result-dependent tuning.  It is hashed into the
freeze record before holdout correctness, opportunity inspection, or timing.
"""
from __future__ import annotations

from _collections import _count_elements
from collections import Counter
from pathlib import Path
import json
import math
import random
import sys

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
sys.path.insert(0, str(AUDIT / "runtime" / "cm_n2_p13_run"))
sys.path.insert(0, str(AUDIT))
import n2_p13_harness as h
from stats_free_diagnostic import make_backend
from python_diagnostics.dispatch_diagnostics import (
    TupleBoundFactory, CanonicalFactory, exact_stats, ref_decision,
)

base = h.base
p6 = h.p8.p6
p5 = p6.p5
p3 = p6.p3
GATE = h.load_gate()
clean_base, clean_p3, clean_p6 = make_backend(base, p3, p6)

ARMS = ("D", "F", "E", "A", "G")
CANONICAL_ARMS = ("CD", "CA")
SYNTHETIC_FAMILIES = (
    "affine_deep", "nonlinear_deep", "dense_rare", "cheap_repeats",
    "unprofitable_sharing", "unshared_tree", "high_fanout",
    "shared_products", "wide_pairs", "nested_pairs",
    "encoding_variants", "dead_history",
)
DEPTHS = (2, 6, 12, 24)
WIDTHS = (1, 4, 16)
SUPPORTS = (4, 8, 12, 16)
FANOUTS = (1, 2, 8, 32)
MULTIPLICITIES = (1, 3, 4, 5, 8, 16)
S_MASTER_SEED = 2026091901
BOOTSTRAP_SEED = 2026091902


class MinimalP13Factory(h.DeferredPairTelemetryFactory):
    """Frozen P13 decision with a Boolean-only measured interface."""
    def dispatch_bool(self):
        if self.binary_nodes < 5:
            return False
        distinct = len(set(self._pair_keys))
        repeat = self.binary_nodes - distinct
        repeat_t = float(GATE["tree"]["threshold"][h.REPEAT_NODE])
        if not h._ratio_le_int(repeat, self.binary_nodes, repeat_t):
            return False
        if repeat < 4:
            return False
        counts = {}
        _count_elements(counts, self._pair_keys)
        if max(counts.values(), default=0) < 5:
            return False
        reuse_t = float(GATE["tree"]["threshold"][h.REUSE_NODE])
        tnum, tden = reuse_t.as_integer_ratio()
        allowed_num = self.edge_count * tnum
        used = bytearray(len(self.nodes))
        reuse = 0
        for node in self.nodes:
            for child in node.args:
                i = child.nid
                if used[i]:
                    reuse += 1
                    if reuse * tden > allowed_num:
                        return False
                else:
                    used[i] = 1
        return True


class GenericSigFactory(base.Factory):
    """Unpacked generic two-expression truth-function metadata.

    This independently represents propagated signatures and estimates.  It uses
    the same declared profitability policy so the comparison isolates the
    representation/formulation rather than silently changing selection.
    """
    def __init__(self):
        super().__init__()
        self.est = []
        self.uses = []
        self.sig = []  # None or (base_a, base_b, token, propagated)

    def align(self, child, a, b):
        if child.nid == a:
            return base.TOK_X, False, False
        if child.nid == b:
            return base.TOK_Y, False, False
        if child.op == "not":
            c = child.args[0].nid
            if c == a:
                return base.TOK_X ^ 15, False, False
            if c == b:
                return base.TOK_Y ^ 15, False, False
        s = self.sig[child.nid]
        if s is None:
            return None
        sa, sb, token, _ = s
        if (sa, sb) == (a, b):
            return token, True, False
        if (sa, sb) == (b, a):
            return p6.SWAP_TOKEN[token], True, True
        return None

    def estimate(self, op, args, value):
        cap = h.p8.p1.MONOMIAL_CAP
        if op == "const": return 1 if value else 0
        if op == "var": return 1
        if op == "not": return min(cap, self.est[args[0].nid] + 1)
        if op == "xor": return min(cap, self.est[args[0].nid] + self.est[args[1].nid])
        if op == "and": return min(cap, self.est[args[0].nid] * self.est[args[1].nid])
        if op == "or":
            a, b = self.est[args[0].nid], self.est[args[1].nid]
            return min(cap, a + b + a*b)
        if op == "tf":
            return p5.token_estimate_fast(int(value), self.est[args[0].nid], self.est[args[1].nid])
        if op == "andn":
            out = 1
            for child in args: out = min(cap, out*self.est[child.nid])
            return out
        if op == "orn":
            out = 0
            for child in args:
                q = self.est[child.nid]
                out = min(cap, out + q + out*q)
            return out
        raise ValueError(op)

    def _make(self, op, args=(), value=None):
        args = tuple(args)
        key = (op, tuple(x.nid for x in args), value)
        old = self.cache.get(key)
        if old is not None:
            return old
        node = base.Node(len(self.nodes), op, args, value)
        self.cache[key] = node
        self.nodes.append(node)
        self.est.append(self.estimate(op, args, value))
        self.uses.append(0)
        self.sig.append(None)
        for child in args:
            self.uses[child.nid] += 1
        if op in ("and", "or", "xor", "tf") and len(args) == 2:
            token = p6.PARENT_TOKENS[op] if op in p6.PARENT_TOKENS else int(value) & 15
            if op in p6.PARENT_TOKENS:
                for source in args:
                    s = self.sig[source.nid]
                    if s is None: continue
                    a, b = s[0], s[1]
                    left, right = self.align(args[0], a, b), self.align(args[1], a, b)
                    if left is not None and right is not None and (left[1] or right[1]):
                        token = p6.TOKEN_APPLY[p6.PARENT_INDEX[op]][left[0]][right[0]]
                        self.sig[node.nid] = (a, b, token, True)
                        break
            if self.sig[node.nid] is None:
                self.sig[node.nid] = (args[0].nid, args[1].nid, token, False)
        return node


def clone_generic(root):
    factory = GenericSigFactory()
    memo = {}
    def rec(node):
        if node.nid in memo: return memo[node.nid]
        args = tuple(rec(x) for x in node.args)
        if node.op == "var": out = factory.var(node.value)
        elif node.op == "const": out = factory.const(node.value)
        elif node.op == "not": out = factory.not_(args[0])
        elif node.op in ("and", "or", "xor"): out = factory.bin(node.op, args[0], args[1])
        elif node.op in ("andn", "orn"): out = factory.nary(node.op, args)
        elif node.op == "tf": out = factory.tf(node.value, args[0], args[1])
        else: raise ValueError(node.op)
        memo[node.nid] = out
        return out
    return factory, rec(root)


def lower_generic(root, factory):
    memo = {}
    def rec(node):
        if node.nid in memo: return memo[node.nid]
        accepted = False
        if node.op in p6.PARENT_TOKENS:
            s = factory.sig[node.nid]
            if s is not None and s[3]:
                a, b, composed, _ = s
                left, right = factory.align(node.args[0], a, b), factory.align(node.args[1], a, b)
                if left is None or right is None or not (left[1] or right[1]):
                    raise AssertionError("generic alignment")
                tl, tr = left[0], right[0]
                ma, mb = factory.est[a], factory.est[b]
                ml = p5.token_estimate_fast(tl, ma, mb)
                mr = p5.token_estimate_fast(tr, ma, mb)
                keep = p6.NONLINEAR[p6.PARENT_TOKENS[node.op]] * ml * mr
                if left[1] and factory.uses[node.args[0].nid] == 1:
                    keep += p6.NONLINEAR[tl] * ma * mb
                if right[1] and factory.uses[node.args[1].nid] == 1:
                    keep += p6.NONLINEAR[tr] * ma * mb
                fold = p6.NONLINEAR[composed] * ma * mb
                benefit = keep - fold
                shared = factory.uses[node.args[0].nid] > 1 or factory.uses[node.args[1].nid] > 1
                frac = h.p8.p1.SHARED_FRACTION_MIN if shared else h.p8.p1.UNSHARED_FRACTION_MIN
                accepted = benefit > 0 and benefit >= h.p8.p1.BENEFIT_MIN and benefit/max(1, keep) >= frac
        if accepted:
            poly = clean_p3.apply_tf_poly(composed, rec(factory.nodes[a]), rec(factory.nodes[b]), base.AnfStats())
        elif node.op == "const": poly = {0} if node.value else set()
        elif node.op == "var": poly = {1 << node.value}
        elif node.op == "not":
            poly = rec(node.args[0]).copy()
            poly.symmetric_difference_update({0})
        elif node.op == "xor": poly = rec(node.args[0]).symmetric_difference(rec(node.args[1]))
        elif node.op == "and": poly = clean_base.mul_poly(rec(node.args[0]), rec(node.args[1]), base.AnfStats())
        elif node.op == "or":
            x, y = rec(node.args[0]), rec(node.args[1])
            poly = x ^ y ^ clean_base.mul_poly(x, y, base.AnfStats())
        elif node.op == "tf": poly = clean_p3.apply_tf_poly(node.value, rec(node.args[0]), rec(node.args[1]), base.AnfStats())
        elif node.op in ("andn", "orn"):
            vals = [rec(x) for x in node.args]
            if node.op == "andn":
                poly = {0}
                for value in vals: poly = clean_base.mul_poly(poly, value, base.AnfStats())
            else:
                poly = set()
                for value in vals: poly = poly ^ value ^ clean_base.mul_poly(poly, value, base.AnfStats())
        else: raise ValueError(node.op)
        memo[node.nid] = poly
        return poly
    return rec(root)


def compile_recipe(build, arm):
    """Recipe-to-owned-ANF production endpoint; no validation/reporting."""
    if arm == "D":
        _, root, _ = build(base.Factory)
        return clean_base.lower_anf(root)[0], False
    if arm == "F":
        fac, root, _ = build(MinimalP13Factory)
        choice = fac.dispatch_bool()
        if not choice: return clean_base.lower_anf(root)[0], False
        annotated, meta = p6.build_innode(root)
        return clean_p6.lower_p6(annotated, meta, collect_stats=False)[0], True
    if arm == "E":
        fac, root, _ = build(TupleBoundFactory)
        choice = fac.dispatch_bool()
        if not choice: return clean_base.lower_anf(root)[0], False
        annotated, meta = p6.build_innode(root)
        return clean_p6.lower_p6(annotated, meta, collect_stats=False)[0], True
    if arm == "A":
        _, root, _ = build(base.Factory)
        annotated, meta = p6.build_innode(root)
        return clean_p6.lower_p6(annotated, meta, collect_stats=False)[0], True
    if arm == "G":
        _, root, _ = build(base.Factory)
        fac, generic = clone_generic(root)
        return lower_generic(generic, fac), True
    if arm in CANONICAL_ARMS:
        _, root, _ = build(CanonicalFactory)
        if arm == "CD": return clean_base.lower_anf(root)[0], False
        annotated, meta = p6.build_innode(root)
        return clean_p6.lower_p6(annotated, meta, collect_stats=False)[0], True
    raise ValueError(arm)


def build_ir(root, arm):
    """IR-to-ANF secondary endpoint, including any observer/metadata clone."""
    if arm == "D": return clean_base.lower_anf(root)[0], False
    if arm in ("F", "E"):
        cls = MinimalP13Factory if arm == "F" else TupleBoundFactory
        fac = cls()
        observed, _ = p6.clone_dag(root, fac)
        choice = fac.dispatch_bool()
        if not choice: return clean_base.lower_anf(observed)[0], False
        annotated, meta = p6.build_innode(observed)
        return clean_p6.lower_p6(annotated, meta, collect_stats=False)[0], True
    if arm == "A":
        annotated, meta = p6.build_innode(root)
        return clean_p6.lower_p6(annotated, meta, collect_stats=False)[0], True
    if arm == "G":
        fac, generic = clone_generic(root)
        return lower_generic(generic, fac), True
    raise ValueError(arm)


def synthetic_factors(index):
    return dict(depth=DEPTHS[index % len(DEPTHS)],
                width=WIDTHS[(index // 2) % len(WIDTHS)],
                support=SUPPORTS[(index // 3) % len(SUPPORTS)],
                fanout=FANOUTS[(index // 5) % len(FANOUTS)],
                multiplicity=MULTIPLICITIES[(index // 7) % len(MULTIPLICITIES)])


def make_trace(family_index, case_index, seed, factors):
    """Return a portable instruction trace: (op, child indexes, optional token)."""
    rng = random.Random(seed)
    nvars = factors["support"]
    ops = []
    def add(op, args, value=None):
        ops.append([op, list(args), value])
        return nvars + len(ops) - 1
    def chain(kind, ids):
        cur = ids[0]
        for item in ids[1:]: cur = add(kind, (cur, item))
        return cur
    vars_ = list(range(nvars))
    half = max(2, nvars // 2)
    affine_a = chain("xor", vars_[:half])
    affine_b = chain("xor", vars_[half:] or vars_[:2])
    nonlinear_a = add("or", (add("and", (vars_[0], vars_[1])), affine_a))
    nonlinear_b = add("xor", (add("and", (vars_[-1], vars_[-2])), affine_b))
    a, b = (affine_a, affine_b) if family_index in (0, 3, 5, 8, 10) else (nonlinear_a, nonlinear_b)
    shells = []
    count = factors["multiplicity"]
    shell_ops = ("and", "or", "xor")
    for i in range(count):
        left, right = (b, a) if (family_index == 10 and i % 2) else (a, b)
        shells.append(add(shell_ops[i % 3], (left, right)))
    if family_index == 11:
        for i in range(max(8, factors["width"] * 2)):
            add(shell_ops[i % 3], (vars_[i % nvars], vars_[(i+1) % nvars]))
    if family_index == 5:
        cur = vars_[0]
        for i in range(factors["depth"] + factors["width"]):
            rhs = vars_[(i+1) % nvars]
            cur = add(shell_ops[rng.randrange(3)], (cur, rhs))
        root = cur
    elif family_index == 8:
        groups = []
        for i in range(max(1, factors["width"])):
            x, y = vars_[i % nvars], vars_[(i*3+1) % nvars]
            groups.append(add(shell_ops[i % 3], (x, y)))
        root = chain("xor", groups)
    elif family_index == 2:
        dense = chain("or", vars_)
        root = add("xor", (dense, shells[-1] if shells else a))
    else:
        cur = shells[0] if shells else add("xor", (a, b))
        other = shells[-1] if shells else b
        for level in range(factors["depth"]):
            q = shells[level % len(shells)] if shells else add(shell_ops[level % 3], (a, b))
            left = add(shell_ops[(level+family_index) % 3], (cur, q))
            if family_index == 6:
                for j in range(min(factors["fanout"], 8)):
                    add("xor", (q, vars_[j % nvars]))
            if family_index == 7:
                shared = add("and", (a, b))
                right = add("or", (shared, other))
            elif family_index == 4:
                right = add("xor", (q, other))
                for j in range(min(factors["fanout"], 8)):
                    add("and", (q, vars_[j % nvars]))
            elif family_index == 9:
                right = add(shell_ops[(level+2) % 3], (a, b))
                a, b = q, right
            else:
                right = other
            cur = add(shell_ops[(level+2) % 3], (left, right))
            other = q
        root = cur
    return {"nvars": nvars, "ops": ops, "root": root}


def trace_builder(trace):
    def build(factory_cls):
        fac = factory_cls()
        nodes = [fac.var(i) for i in range(trace["nvars"])]
        for op, ids, value in trace["ops"]:
            args = [nodes[i] for i in ids]
            if op in ("and", "or", "xor"): node = fac.bin(op, args[0], args[1])
            elif op == "not": node = fac.not_(args[0])
            elif op == "tf": node = fac.tf(value, args[0], args[1])
            elif op in ("andn", "orn"): node = fac.nary(op, args)
            else: raise ValueError(op)
            nodes.append(node)
        return fac, nodes[trace["root"]], trace["nvars"]
    return build


def scalar_node(node, values, memo=None):
    memo = {} if memo is None else memo
    if node.nid in memo: return memo[node.nid]
    if node.op == "var": out = values[node.value]
    elif node.op == "const": out = bool(node.value)
    elif node.op == "not": out = not scalar_node(node.args[0], values, memo)
    elif node.op == "and": out = scalar_node(node.args[0], values, memo) and scalar_node(node.args[1], values, memo)
    elif node.op == "or": out = scalar_node(node.args[0], values, memo) or scalar_node(node.args[1], values, memo)
    elif node.op == "xor": out = scalar_node(node.args[0], values, memo) ^ scalar_node(node.args[1], values, memo)
    elif node.op == "tf":
        x, y = int(scalar_node(node.args[0], values, memo)), int(scalar_node(node.args[1], values, memo))
        out = bool((node.value >> (2*x+y)) & 1)
    elif node.op == "andn": out = all(scalar_node(x, values, memo) for x in node.args)
    elif node.op == "orn": out = any(scalar_node(x, values, memo) for x in node.args)
    else: raise ValueError(node.op)
    memo[node.nid] = out
    return out


def scalar_poly(poly, values):
    out = False
    for monomial in poly:
        term = True
        bits = monomial
        while bits:
            low = bits & -bits
            term = term and values[low.bit_length()-1]
            if not term: break
            bits ^= low
        out ^= term
    return out


def operation_counts(build):
    fac, root, nv = build(base.Factory)
    direct, ds = base.lower_anf(root)
    annotated, meta = p6.build_innode(root)
    folded, fs, selector = p6.lower_p6(annotated, meta, collect_stats=True)
    return {"nodes": len(fac.nodes), "support": nv, "direct_pair_terms": ds.pair_terms,
            "fold_pair_terms": fs.pair_terms, "direct_multiplications": ds.multiplications,
            "fold_multiplications": fs.multiplications, "folds": selector.fold_lowerings,
            "final_monomials": len(direct), "equal": direct == folded}
