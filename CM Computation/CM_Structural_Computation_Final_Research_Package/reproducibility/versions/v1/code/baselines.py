"""Packed truth mask/popcount and an explicit, fixed-order Python ROBDD.

ROBDD is a deliberately labeled reference implementation, not CUDD.
"""
from functools import lru_cache
import json

class PackedTruth:
    def __init__(self, truth: int, n: int):
        self.truth, self.n = truth, n
        self.full = (1 << (1 << n))-1
        self.masks = []
        for j in range(n):
            block = 1 << (n-j-1)
            one = (self.full // ((1 << block)+1)) << block
            self.masks.append((self.full ^ one, one))
    def query(self, rho: dict[int,int]) -> int:
        values = self.truth
        for v, b in rho.items():
            values &= self.masks[v][b]
        return values.bit_count()
    def dumps(self):
        return json.dumps({'kind':'packed-mask-source','n':self.n,'truth':self.truth},
                          separators=(',',':'), sort_keys=True).encode()

class ReferenceBDD:
    def __init__(self, truth: int, n: int):
        self.n, self.nodes, unique = n, [None, None], {}
        def build(t, level):
            size = 1 << (n-level)
            if t == 0: return 0
            if t == (1 << size)-1: return 1
            half = size // 2
            low = build(t & ((1 << half)-1), level+1)
            high = build(t >> half, level+1)
            if low == high: return low
            key = (level, low, high)
            if key not in unique:
                unique[key] = len(self.nodes)
                self.nodes.append(key)
            return unique[key]
        self.root = build(truth, 0)
    def evaluate(self, a):
        u = self.root
        while u > 1:
            level, lo, hi = self.nodes[u]
            u = hi if (a >> (self.n-level-1)) & 1 else lo
        return u
    def verify(self, truth):
        return all(self.evaluate(a) == ((truth >> a)&1) for a in range(1 << self.n))
    def query(self, rho):
        free_prefix = [0]
        for v in range(self.n):
            free_prefix.append(free_prefix[-1] + int(v not in rho))
        @lru_cache(None)
        def visit(u, start):
            if u == 0: return 0
            if u == 1: return 1 << (free_prefix[self.n]-free_prefix[start])
            level, lo, hi = self.nodes[u]
            scale = 1 << (free_prefix[level]-free_prefix[start])
            if level in rho:
                return scale * visit(hi if rho[level] else lo, level+1)
            return scale * (visit(lo, level+1) + visit(hi, level+1))
        return visit(self.root, 0)
    def dumps(self):
        return json.dumps({'kind':'reference-robdd','n':self.n,'root':self.root,'nodes':self.nodes},
                          separators=(',',':'),sort_keys=True).encode()
