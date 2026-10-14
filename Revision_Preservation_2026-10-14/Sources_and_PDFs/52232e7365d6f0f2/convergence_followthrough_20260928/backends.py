"""Exact matched endpoints; MSB coordinate names, declared free axes retained."""
from pathlib import Path
import struct, sys

ROOT=Path(__file__).resolve().parent
BASE=ROOT/'inputs/baseline/CM_COMPUTATION_BASELINE_HANDOFF/reproducibility/code'
sys.path.insert(0,str(BASE))
from artifacts import Artifact, matrix_rows, rank_factor, selected_indices
from codec import dumps_binary, loads_binary

def validate(rho,scope):
    if not set(rho)<=set(scope) or any(type(x) is not int or x not in (0,1) for x in rho.values()):
        raise ValueError('restriction outside active scope')

class Packed:
    kind='packed_binary'
    def __init__(self,truth,scope):
        self.truth=truth;self.scope=tuple(scope);self.masks=None
        if type(truth) is not int or truth<0 or truth.bit_length()>1<<len(scope):raise ValueError('truth outside scope')
    def index(self):
        n=len(self.scope)
        self.masks={v:sum(1<<a for a in range(1<<n) if (a>>(n-1-j))&1) for j,v in enumerate(self.scope)}
    def query(self,rho):
        validate(rho,self.scope)
        if self.masks is None:raise RuntimeError('index must be constructed and charged')
        full=(1<<(1<<len(self.scope)))-1;mask=full
        for v,b in rho.items():mask &= self.masks[v] if b else full^self.masks[v]
        return (self.truth&mask).bit_count()
    def condition(self,rho):
        validate(rho,self.scope)
        indices=selected_indices(self.scope,rho)
        return Packed(sum(((self.truth>>a)&1)<<j for j,a in enumerate(indices)),[v for v in self.scope if v not in rho])
    def dumps(self):
        return b'QPB1'+struct.pack('<H',len(self.scope))+struct.pack('<'+'H'*len(self.scope),*self.scope)+self.truth.to_bytes(((1<<len(self.scope))+7)//8,'little')
    @classmethod
    def loads(cls,blob):
        if blob[:4]!=b'QPB1' or len(blob)<6:raise ValueError('packed header')
        n=struct.unpack_from('<H',blob,4)[0]
        if n>16 or len(blob)!=6+2*n+((1<<n)+7)//8:raise ValueError('packed size')
        scope=struct.unpack_from('<'+'H'*n,blob,6)
        if len(set(scope))!=n:raise ValueError('duplicate coordinate')
        return cls(int.from_bytes(blob[6+2*n:],'little'),scope)
    def point(self,assignment):
        a=sum(assignment[v]<<(len(self.scope)-1-j) for j,v in enumerate(self.scope))
        return (self.truth>>a)&1

class Rank:
    kind='coordinate_rank_baseline'
    def __init__(self,truth,scope,left):
        rows,right=matrix_rows(truth,tuple(scope),tuple(left));coef,basis=rank_factor(rows)
        self.art=Artifact('rank',tuple(scope),(tuple(left),right,coef,basis))
    @property
    def scope(self):return self.art.scope
    def index(self):pass # query_fused builds coordinate-sensitive selectors per query; charged there
    def query(self,rho):return self.art.query_fused(rho)
    def condition(self,rho):
        out=object.__new__(Rank);out.art=self.art.condition(rho);return out
    def dumps(self):return dumps_binary(self.art)
    @classmethod
    def loads(cls,blob):
        out=object.__new__(cls);out.art=loads_binary(blob)
        if out.art.kind!='rank':raise ValueError('expected rank artifact')
        return out
    def point(self,assignment):return self.art.query_fused(assignment)

def exact_count(manager,root):
    """Integer traversal adapted from repository exact_cudd_count.py; no float count."""
    width=len(manager.vars);zero,one=manager.false,manager.true;counts={zero:0,one:1};pending=[(root,False)]
    def level(node):return width if node==zero or node==one else node.level
    while pending:
        node,ready=pending.pop()
        if node in counts:continue
        if node.negated:
            pos=~node
            if ready:counts[node]=(1<<(width-level(node)))-counts[pos]
            else:pending.extend(((node,True),(pos,False)))
        elif ready:counts[node]=(counts[node.low]<<(level(node.low)-level(node)-1))+(counts[node.high]<<(level(node.high)-level(node)-1))
        else:pending.extend(((node,True),(node.low,False),(node.high,False)))
    return counts[root]<<level(root)

class Cudd:
    kind='cudd_fixed_order_binary'
    def __init__(self,truth,scope):
        from dd.cudd import BDD
        self.scope=tuple(scope);self.universe=tuple(scope);self.manager=BDD()
        self.manager.configure(reordering=False)
        if scope:self.manager.declare(*(f'x{v}' for v in scope))
        def build(bits,depth):
            rem=len(scope)-depth
            if bits==0:return self.manager.false
            if bits==(1<<(1<<rem))-1:return self.manager.true
            half=1<<(rem-1);mask=(1<<half)-1
            lo=build(bits&mask,depth+1);hi=build(bits>>half,depth+1)
            return self.manager.ite(self.manager.var(f'x{scope[depth]}'),hi,lo)
        self.root=build(truth,0)
        build=None # break recursive closure cycle before manager lifetime ends
    def __del__(self):
        # CUDD requires Function references to die before their manager.
        if hasattr(self,'root'):del self.root
        if hasattr(self,'manager'):del self.manager
    def index(self):pass
    def query(self,rho):
        validate(rho,self.scope)
        node=self.manager.let({f'x{k}':bool(v) for k,v in rho.items()},self.root) if rho else self.root
        return exact_count(self.manager,node)>>(len(self.universe)-len(self.scope)+len(rho))
    def condition(self,rho):
        validate(rho,self.scope);out=object.__new__(Cudd)
        out.manager=self.manager;out.universe=self.universe;out.scope=tuple(v for v in self.scope if v not in rho)
        out.root=self.manager.let({f'x{k}':bool(v) for k,v in rho.items()},self.root) if rho else self.root;return out
    def point(self,assignment):return self.query(assignment)
    def dumps(self):
        nodes=[];seen={self.manager.true:1}
        def visit(node):
            if node.negated:return -visit(~node)
            if node in seen:return seen[node]
            low,high=visit(node.low),visit(node.high)
            idx=len(nodes)+2;seen[node]=idx;nodes.append((node.level,low,high));return idx
        root=visit(self.root)
        visit=None # release recursive closure and its temporary node references
        head=b'QCB1'+struct.pack('<HHIq',len(self.universe),len(self.scope),len(nodes),root)
        return head+struct.pack('<'+'H'*(len(self.universe)+len(self.scope)),*(self.universe+self.scope))+b''.join(struct.pack('<Hqq',*x) for x in nodes)
    @classmethod
    def loads(cls,blob):
        from dd.cudd import BDD
        if len(blob)<20 or blob[:4]!=b'QCB1':raise ValueError('CUDD binary header')
        n,s,total,root=struct.unpack_from('<HHIq',blob,4)
        if n>16 or s>n or len(blob)!=20+2*(n+s)+18*total:raise ValueError('CUDD binary size')
        out=object.__new__(cls);names=struct.unpack_from('<'+'H'*(n+s),blob,20)
        out.universe=tuple(names[:n]);out.scope=tuple(names[n:]);out.manager=BDD();out.manager.configure(reordering=False)
        if len(set(out.universe))!=n or len(set(out.scope))!=s or not set(out.scope)<=set(out.universe):raise ValueError('scope')
        if n:out.manager.declare(*(f'x{v}' for v in out.universe))
        nodes={1:out.manager.true}
        def get(i):
            if abs(i) not in nodes:raise ValueError('non-topological edge')
            return nodes[i] if i>0 else ~nodes[-i]
        for j in range(total):
            level,lo,hi=struct.unpack_from('<Hqq',blob,20+2*(n+s)+18*j)
            if level>=n:raise ValueError('level')
            nodes[j+2]=out.manager.ite(out.manager.var(f'x{out.universe[level]}'),get(hi),get(lo))
        out.root=get(root);return out

METHODS={'packed_binary':Packed,'coordinate_rank_baseline':Rank,'cudd_fixed_order_binary':Cudd}

def make(method,bits,n,left):
    cls=METHODS[method]
    return cls(bits,tuple(range(n)),left) if cls is Rank else cls(bits,tuple(range(n)))
