"""Packed truth mask/popcount and an explicit, fixed-order Python ROBDD.

ROBDD is a deliberately labeled reference implementation, not CUDD.
"""
from functools import lru_cache
import json

class PackedTruth:
    def __init__(self, truth: int, n: int):
        if type(n) is not int or not 0 <= n <= 16 or type(truth) is not int or truth < 0 or truth.bit_length() > (1 << n):
            raise ValueError('invalid packed truth dimension or payload')
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

    @staticmethod
    def loads(blob):
        doc = json.loads(blob)
        if set(doc) != {'kind','n','truth'} or doc['kind'] != 'packed-mask-source':
            raise ValueError('wrong packed schema')
        return PackedTruth(doc['truth'],doc['n'])

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

    @staticmethod
    def loads(blob):
        """Load listed nodes into a fresh object, without reconstructing from truth."""
        doc=json.loads(blob)
        if set(doc)!={'kind','n','root','nodes'} or doc['kind']!='reference-robdd':
            raise ValueError('wrong BDD schema')
        n,root,nodes=doc['n'],doc['root'],doc['nodes']
        if type(n) is not int or not 0<=n<=16 or type(nodes) is not list or len(nodes)<2 or nodes[:2]!=[None,None]:
            raise ValueError('invalid BDD dimension/terminals')
        seen=set()
        for i,node in enumerate(nodes[2:],2):
            if type(node) is not list or len(node)!=3 or any(type(v) is not int for v in node):
                raise ValueError('invalid BDD node')
            level,lo,hi=node
            if not 0<=level<n or not 0<=lo<i or not 0<=hi<i or lo==hi:
                raise ValueError('invalid BDD edge/reduction')
            for child in (lo,hi):
                if child>1 and nodes[child][0]<=level: raise ValueError('variable ordering')
            if tuple(node) in seen: raise ValueError('nonunique BDD node')
            seen.add(tuple(node))
        if type(root) is not int or not 0<=root<len(nodes): raise ValueError('root')
        loaded=ReferenceBDD.__new__(ReferenceBDD)
        loaded.n=n; loaded.root=root
        loaded.nodes=[None,None]+[tuple(v) for v in nodes[2:]]
        return loaded
