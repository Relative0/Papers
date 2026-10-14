from __future__ import annotations
import argparse, dataclasses, hashlib, json, math, random, statistics, sys, time, tracemalloc
from collections import defaultdict
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
P6_DIR=ROOT/'cm_n2_p6_run'
P7B_DIR=ROOT/'cm_n2_p7b_run'
P1_DIR=ROOT/'cm_n2_p1_bundle'
for p in (P6_DIR,P7B_DIR,P1_DIR):
    if str(p) not in sys.path: sys.path.insert(0,str(p))
import n2_p6_harness as p6
import n2_p1_harness as p1
base=p6.base

SEED=20260918
TRAIN_SEED=SEED ^ 0x8008A
VAL_SEED=SEED ^ 0x8008B
TREE_SEED=SEED ^ 0x8D33
FUZZ_SEED=SEED ^ 0x8F22
PREREG_SHA256='7be7224825d29b81441864ec8c251a6c4e50624b350bcdd0db7f3a153b7c53f3'
TRAIN_REPS=9
VAL_REPS=9
GATEP_REPS=20
NAT_REPS=15
FUZZ_CASES=1000
CUTS=tuple(round(0.80+i*0.01,2) for i in range(21))

DIRECT='direct_source_pipeline'
P6ARM='p6_source_pipeline'
P8='p8_source_dispatch'
COMP_DIRECT='direct_build_sparse'
COMP_P6='cm_innode_sig_build_sparse'

FEATURE_NAMES=(
    'node_count','edge_count','max_depth','binary_nodes','nonlinear_binary_nodes','cse_hits',
    'reuse_edge_events','max_use','pair_repeat_excess','multi_token_pair_groups','max_pair_shells',
    'max_pair_token_diversity','binary_density','nonlinear_density','reuse_density','pair_repeat_density'
)
PARENT_TOKENS={'and':base.TOK_AND,'or':base.TOK_OR,'xor':base.TOK_XOR}


def sha256_file(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def geomean(xs):
    xs=[float(x) for x in xs if x is not None and x>0]
    return math.exp(sum(math.log(x) for x in xs)/len(xs)) if xs else None

def quantile(xs,p):
    s=sorted(xs)
    if not s:return None
    z=(len(s)-1)*p; lo=int(z); hi=min(lo+1,len(s)-1); f=z-lo
    return s[lo]*(1-f)+s[hi]*f

def bootstrap_geomean(ratios,n=5000,seed=SEED):
    ratios=[x for x in ratios if x and x>0]
    if not ratios:return {'estimate':None,'ci95':[None,None]}
    rng=random.Random(seed); vals=[]
    for _ in range(n): vals.append(geomean([rng.choice(ratios) for __ in ratios]))
    return {'estimate':geomean(ratios),'ci95':[quantile(vals,.025),quantile(vals,.975)],'bootstrap_n':n}

class TelemetryFactory(base.Factory):
    """Semantics-identical source Factory plus O(1)-incremental dispatch telemetry."""
    def __init__(self):
        super().__init__()
        self.depths=[]; self.uses=[]
        self.edge_count=0; self.max_depth=0; self.binary_nodes=0; self.nonlinear_binary_nodes=0
        self.cse_hits=0; self.reuse_edge_events=0; self.max_use=0
        self.pair_repeat_excess=0; self.multi_token_pair_groups=0; self.max_pair_shells=0; self.max_pair_token_diversity=0
        self._pair_counts={}; self._pair_masks={}

    def _make(self,op,args=(),value=None):
        args=tuple(args); key=(op,tuple(a.nid for a in args),value)
        n=self.cache.get(key)
        if n is not None:
            self.cse_hits+=1
            return n
        n=base.Node(len(self.nodes),op,args,value)
        self.cache[key]=n; self.nodes.append(n)
        d=0 if not args else 1+max(self.depths[a.nid] for a in args)
        self.depths.append(d); self.uses.append(0)
        if d>self.max_depth:self.max_depth=d
        self.edge_count+=len(args)
        for c in args:
            u=self.uses[c.nid]+1; self.uses[c.nid]=u
            if u>1:self.reuse_edge_events+=1
            if u>self.max_use:self.max_use=u
        if op in ('and','or','xor','tf') and len(args)==2:
            self.binary_nodes+=1
            tok=(PARENT_TOKENS[op] if op in PARENT_TOKENS else int(value)&15)
            a,b=args[0].nid,args[1].nid
            if a>b:
                a,b=b,a; tok=base.swap_token(tok)
            if p6.p5.NONLINEAR[tok]: self.nonlinear_binary_nodes+=1
            k=(a,b); oldc=self._pair_counts.get(k,0); newc=oldc+1; self._pair_counts[k]=newc
            if oldc>=1:self.pair_repeat_excess+=1
            if newc>self.max_pair_shells:self.max_pair_shells=newc
            oldm=self._pair_masks.get(k,0); newm=oldm|(1<<tok); self._pair_masks[k]=newm
            od=oldm.bit_count(); nd=newm.bit_count()
            if od<2 and nd>=2:self.multi_token_pair_groups+=1
            if nd>self.max_pair_token_diversity:self.max_pair_token_diversity=nd
        return n

    def features(self):
        n=len(self.nodes); e=self.edge_count; b=self.binary_nodes
        raw={
            'node_count':n,'edge_count':e,'max_depth':self.max_depth,'binary_nodes':b,
            'nonlinear_binary_nodes':self.nonlinear_binary_nodes,'cse_hits':self.cse_hits,
            'reuse_edge_events':self.reuse_edge_events,'max_use':self.max_use,
            'pair_repeat_excess':self.pair_repeat_excess,'multi_token_pair_groups':self.multi_token_pair_groups,
            'max_pair_shells':self.max_pair_shells,'max_pair_token_diversity':self.max_pair_token_diversity,
            'binary_density':b/max(1,n),
            'nonlinear_density':self.nonlinear_binary_nodes/max(1,b),
            'reuse_density':self.reuse_edge_events/max(1,e),
            'pair_repeat_density':self.pair_repeat_excess/max(1,b),
        }
        return raw


def feature_vector(f:TelemetryFactory):
    d=f.features(); return [float(d[k]) for k in FEATURE_NAMES],d

# ---------- deterministic source recipes ----------

def _random_expr(rng,nvars,depth,f): return base.random_expr(rng,nvars,depth,f)

def gatep_with_factory(rng,depth,idx,FactoryCls):
    f=FactoryCls(); nvars=8
    A=base.make_base_expr(rng,nvars,3,f); B=base.make_base_expr(rng,nvars,3,f)
    cur=f.bin(rng.choice(('and','or','xor')),A,B)
    other=f.bin(rng.choice(('and','or','xor')),A,B)
    for level in range(depth):
        q=f.bin(rng.choice(('and','or','xor')),A,B)
        left=f.bin(rng.choice(('and','or','xor')),cur,q)
        s=f.bin(rng.choice(('and','or','xor')),B,A) if level%3==1 else other
        cur=f.bin(rng.choice(('and','or','xor')),left,s)
        other=q
    return f,cur,nvars

def pair_noise_with_factory(seed,depth,idx,FactoryCls):
    rng=random.Random(seed); f=FactoryCls(); nvars=8
    bases=[base.make_base_expr(rng,nvars,3,f) for _ in range(6)]
    pairs=((0,1),(2,3),(4,5),(0,2),(1,4),(3,5),(0,4),(1,5))
    a,b=pairs[0]; cur=f.bin(rng.choice(('and','or','xor')),bases[a],bases[b])
    for level in range(depth):
        a,b=pairs[(level+1)%len(pairs)]
        q=f.bin(rng.choice(('and','or','xor')),bases[a],bases[b])
        s=f.bin(rng.choice(('and','or','xor')),bases[a],bases[b])
        left=f.bin(rng.choice(('and','or','xor')),cur,q)
        cur=f.bin(rng.choice(('and','or','xor')),left,s)
    return f,cur,nvars

def synthetic_recipe(kind,seed,depth,idx):
    def build(FactoryCls):
        if kind=='gatep': return gatep_with_factory(random.Random(seed),depth,idx,FactoryCls)
        if kind=='pair_noise': return pair_noise_with_factory(seed,depth,idx,FactoryCls)
        rng=random.Random(seed); f=FactoryCls(); n=8; root=base.random_expr(rng,n,depth,f); return f,root,n
    return build

def training_synthetic_recipes():
    out=[]; j=0
    for d in (4,6,8,10,12,14):
        for i in range(12):
            seed=TRAIN_SEED ^ (d<<12) ^ i ^ 0x111100; out.append((f'train-gatep:{d}:{i}','gatep',d,synthetic_recipe('gatep',seed,d,i))); j+=1
    for d in (6,8,10,12,14,16):
        for i in range(9):
            seed=TRAIN_SEED ^ (d<<12) ^ i ^ 0x222200; out.append((f'train-noise:{d}:{i}','pair_noise',d,synthetic_recipe('pair_noise',seed,d,i))); j+=1
    for i in range(54):
        rng=random.Random(TRAIN_SEED ^ i ^ 0x333300); d=rng.randint(6,12); seed=TRAIN_SEED ^ i ^ 0x333333
        out.append((f'train-random:{i}','random',d,synthetic_recipe('random',seed,d,i)))
    return out

def validation_synthetic_recipes():
    out=[]
    for d in (4,6,8,10,12,14):
        for i in range(6):
            seed=VAL_SEED ^ (d<<12) ^ i ^ 0x111100; out.append((f'val-gatep:{d}:{i}','gatep',d,synthetic_recipe('gatep',seed,d,i)))
    counts={6:4,8:4,10:4,12:5,14:5,16:5}
    for d,c in counts.items():
        for i in range(c):
            seed=VAL_SEED ^ (d<<12) ^ i ^ 0x222200; out.append((f'val-noise:{d}:{i}','pair_noise',d,synthetic_recipe('pair_noise',seed,d,i)))
    for i in range(27):
        rng=random.Random(VAL_SEED ^ i ^ 0x333300); d=rng.randint(6,12); seed=VAL_SEED ^ i ^ 0x333333
        out.append((f'val-random:{i}','random',d,synthetic_recipe('random',seed,d,i)))
    return out

# Exact frozen Gate-P shared-RNG recipe states.
def gatep_eval_recipes():
    rng=random.Random(base.SEED^0x6A7E); out=[]
    for d in p1.GATEP_DEPTHS:
        for i in range(p1.GATEP_CASES_PER_DEPTH):
            state=rng.getstate()
            _f,_r,_n=base.gatep_case(rng,d,i)  # advance exact frozen stream
            def build(FactoryCls,state=state,d=d,i=i):
                rr=random.Random(); rr.setstate(state); return gatep_with_factory(rr,d,i,FactoryCls)
            out.append((f'{d}:{i}',d,i,build))
    return out

# ---------- natural source construction ----------

def build_cone_with_factory(blif,root,support_names,FactoryCls):
    f=FactoryCls(); varmap={name:f.var(i) for i,name in enumerate(support_names)}; memo={}; active=set()
    def rec(s):
        if s in varmap:return varmap[s]
        if s in memo:return memo[s]
        if s in active:raise ValueError('cycle')
        if s in blif.inputs:raise ValueError(f'undeclared support input {s}')
        active.add(s); nd=blif.nodes[s]; cubes=[]
        for patt in nd.cubes:
            lits=[]
            for bit,ch in zip(patt,nd.inputs):
                if bit=='-':continue
                c=rec(ch); lits.append(c if bit=='1' else f.not_(c))
            cubes.append(base.balanced(f,'and',lits,1))
        val=base.balanced(f,'or',cubes,0)
        if nd.cube_output==0:val=f.not_(val)
        active.remove(s); memo[s]=val; return val
    return f,rec(root),len(support_names)

def eval_root_ids():
    cases,_,_=p6.load_cases(); return {c['circuit']:{c['root'] for c in cases if c['circuit']==circuit} for circuit in {c['circuit'] for c in cases}}

def _structural_candidates(blif,exclude):
    sm={}; dm={}; out=[]
    for root in sorted(blif.nodes):
        if root in exclude:continue
        sup=p1.capped_support(blif,root,13,sm)
        if not (6<=len(sup)<=12):continue
        n=p1.cone_node_count(blif,root)
        if n>128:continue
        d=p1.cone_depth(blif,root,dm)
        names=tuple(x for x in blif.inputs if x in sup)
        out.append({'root':root,'support_names':names,'support':len(names),'source_nodes':n,'depth':d})
    out.sort(key=lambda x:(x['source_nodes'],x['depth'],x['root']))
    return out

def _quantile3(items):
    if not items:return []
    ids=[0] if len(items)==1 else ([0,len(items)-1] if len(items)==2 else [0,(len(items)-1)//2,len(items)-1])
    return [items[i] for i in ids]

def epfl_trainval_selection():
    evalcases,_,_=p6.load_cases(); ex=defaultdict(set)
    for c in evalcases: ex[c['circuit']].add(c['root'])
    epfl=ROOT/'cm_n2_p7b_run'/'epfl'
    mapping={'adder':'adder_size_2022.blif','bar':'bar_size_2015.blif','cavlc':'cavlc_size_2024.blif',
             'int2float':'int2float_size_2025.blif','priority':'priority_size_2024.blif','router':'router_size_2024.blif'}
    traincir=('adder','cavlc','bar'); valcir=('int2float','priority','router')
    doc={'schema':'cm-n2-p8-epfl-trainval-selection/v1','train':[],'validation':[],'evaluation_roots':{k:sorted(v) for k,v in ex.items()}}
    for split,circs in [('train',traincir),('validation',valcir)]:
        for circuit in circs:
            path=epfl/mapping[circuit]; blif=base.parse_blif(path); cands=_structural_candidates(blif,ex[circuit]); sel=_quantile3(cands)
            doc[split].append({'circuit':circuit,'file':mapping[circuit],'file_sha256':sha256_file(path),'candidate_count':len(cands),
                               'selected':[{**x,'support_names':list(x['support_names'])} for x in sel]})
    return doc

def epfl_recipes(split,selection):
    epfl=ROOT/'cm_n2_p7b_run'/'epfl'; out=[]
    for cir in selection[split]:
        path=epfl/cir['file']; blif=base.parse_blif(path)
        for x in cir['selected']:
            names=tuple(x['support_names']); root=x['root']; cid=f"{split}-epfl:{cir['circuit']}:{root}"
            oracle=p1.eval_blif_cone(blif,root,names)
            def build(FactoryCls,blif=blif,root=root,names=names): return build_cone_with_factory(blif,root,names,FactoryCls)
            out.append((cid,'epfl',x['depth'],build,oracle,{**x,'circuit':cir['circuit']}))
    return out

def natural_eval_recipes():
    cases,selection,selsha=p6.load_cases(); epfl=ROOT/'cm_n2_p7b_run'/'epfl'; out=[]
    cache={}
    for c in cases:
        path=epfl/c['file']; blif=cache.setdefault(c['file'],base.parse_blif(path)); names=tuple(c['support_names']); root=c['root']
        def build(FactoryCls,blif=blif,root=root,names=names): return build_cone_with_factory(blif,root,names,FactoryCls)
        out.append((c['case_id'],c['circuit'],c['depth'],build,c['oracle'],c))
    return out,selection,selsha

# ---------- tree ----------
def eval_tree(tree,features):
    x=[float(features[k]) for k in FEATURE_NAMES]; i=0
    while True:
        l=tree['children_left'][i]; r=tree['children_right'][i]
        if l==r or l<0:return math.exp(tree['value'][i])
        fi=tree['feature'][i]
        i=l if x[fi] <= tree['threshold'][i] else r

def load_gate():
    obj=json.loads((HERE/'P8_FROZEN_GATE.json').read_text())
    if obj.get('schema')!='cm-n2-p8-frozen-gate/v1':raise ValueError('bad P8 gate schema')
    return obj

# ---------- timing helpers ----------
def compile_once(root,arm,oracle,nvars,memory=False):
    a=p6.DIRECT_BUILD if arm==COMP_DIRECT else p6.P6_BUILD
    return p6.run_pipeline_once(root,a,oracle,nvars,memory)

def paired_compile(root,oracle,nvars,reps,seed):
    rng=random.Random(seed); arms=[COMP_DIRECT,COMP_P6]*reps; rng.shuffle(arms); rows=[]
    for rep,a in enumerate(arms):
        r=compile_once(root,a,oracle,nvars,False)
        if not r['ok']:raise AssertionError(('compile oracle',a))
        rows.append({'rep':rep,'arm':a,'pipeline_ns':r['pipeline_ns'],'dag_build_ns':r['dag_build_ns'],'lower_ns':r['lower_ns']})
    return rows

def source_build_timing(build,reps,seed):
    rng=random.Random(seed); kinds=['plain','telemetry']*reps; rng.shuffle(kinds); rows=[]
    for rep,k in enumerate(kinds):
        Cls=base.Factory if k=='plain' else TelemetryFactory
        t0=time.perf_counter_ns(); f,root,n=build(Cls); ns=time.perf_counter_ns()-t0
        rows.append({'rep':rep,'kind':k,'source_build_ns':ns,'nodes':len(f.nodes)})
    return rows

def med_by(rows,keyfield,valfield):
    d=defaultdict(list)
    for r in rows:d[r[keyfield]].append(r[valfield])
    return {k:statistics.median(v) for k,v in d.items()}

def case_record(cid,kind,depth,build,oracle=None,extra=None,reps=TRAIN_REPS,seed=0):
    tf,troot,n=build(TelemetryFactory); vec,feat=feature_vector(tf)
    if oracle is None:oracle=base.eval_node_bitset(troot,n)
    # semantics-equivalent plain source
    pf,proot,pn=build(base.Factory)
    if pn!=n:raise AssertionError(('nvars drift',cid,pn,n))
    d0=compile_once(proot,COMP_DIRECT,oracle,n,False); dt=compile_once(troot,COMP_DIRECT,oracle,n,False)
    if not (d0['ok'] and dt['ok'] and d0['digest']==dt['digest']):raise AssertionError(('source semantics drift',cid))
    comp=paired_compile(troot,oracle,n,reps,seed^0xC011)
    cm=med_by(comp,'arm','pipeline_ns')
    sb=source_build_timing(build,reps,seed^0x50A7)
    sm=med_by(sb,'kind','source_build_ns')
    return {'case_id':cid,'kind':kind,'depth':depth,'features':feat,'feature_vector':vec,
            'direct_compile_median_ns':cm[COMP_DIRECT],'p6_compile_median_ns':cm[COMP_P6],
            'p6_over_direct':cm[COMP_P6]/cm[COMP_DIRECT],
            'plain_source_median_ns':sm['plain'],'telemetry_source_median_ns':sm['telemetry'],
            'telemetry_over_plain_source':sm['telemetry']/sm['plain'],**(extra or {})}

def collect_training(selection):
    recs=[]
    for j,(cid,kind,d,build) in enumerate(training_synthetic_recipes()):
        recs.append(case_record(cid,kind,d,build,reps=TRAIN_REPS,seed=TRAIN_SEED+j*31))
    for j,(cid,kind,d,build,oracle,extra) in enumerate(epfl_recipes('train',selection)):
        recs.append(case_record(cid,kind,d,build,oracle,extra,TRAIN_REPS,TRAIN_SEED^0xE000^j))
    return recs

def fit_tree(records):
    import numpy as np
    from sklearn.tree import DecisionTreeRegressor
    X=np.asarray([r['feature_vector'] for r in records],dtype=float)
    y=np.asarray([math.log(r['p6_over_direct']) for r in records],dtype=float)
    m=DecisionTreeRegressor(max_depth=3,min_samples_leaf=12,min_samples_split=24,random_state=TREE_SEED)
    m.fit(X,y); t=m.tree_
    return {'children_left':[int(x) for x in t.children_left], 'children_right':[int(x) for x in t.children_right],
            'feature':[int(x) for x in t.feature], 'threshold':[float(x) for x in t.threshold],
            'value':[float(x) for x in t.value[:,0,0]], 'n_node_samples':[int(x) for x in t.n_node_samples],
            'max_depth':int(t.max_depth),'node_count':int(t.node_count)}

def collect_validation(selection,tree):
    recs=[]
    syn=validation_synthetic_recipes()
    for j,(cid,kind,d,build) in enumerate(syn):
        r=case_record(cid,kind,d,build,reps=VAL_REPS,seed=VAL_SEED+j*37); r['predicted_ratio']=eval_tree(tree,r['features']); recs.append(r)
    for j,(cid,kind,d,build,oracle,extra) in enumerate(epfl_recipes('validation',selection)):
        r=case_record(cid,kind,d,build,oracle,extra,VAL_REPS,VAL_SEED^0xE100^j); r['predicted_ratio']=eval_tree(tree,r['features']); recs.append(r)
    return recs

def choose_cutoff(records):
    table=[]
    for c in CUTS:
        ratios=[]; annotated=0; wn=wd=0.0
        for r in records:
            choose=r['predicted_ratio']<=c; annotated+=int(choose)
            num=r['telemetry_source_median_ns']+(r['p6_compile_median_ns'] if choose else r['direct_compile_median_ns'])
            den=r['plain_source_median_ns']+r['direct_compile_median_ns']
            ratios.append(num/den); wn+=num; wd+=den
        table.append({'cutoff':c,'geomean_ratio':geomean(ratios),'weighted_ratio':wn/wd,'annotated_cases':annotated})
    best=min(x['geomean_ratio'] for x in table)
    eligible=[x for x in table if x['geomean_ratio']<=best+0.0025]
    selected=min(eligible,key=lambda x:x['cutoff'])
    return selected,table

def calibrate():
    selection=epfl_trainval_selection()
    train=collect_training(selection); tree=fit_tree(train)
    val=collect_validation(selection,tree); selected,table=choose_cutoff(val)
    used=sorted({FEATURE_NAMES[i] for i in tree['feature'] if i>=0})
    return {'schema':'cm-n2-p8-calibration/v1','prereg_sha256':PREREG_SHA256,'feature_names':list(FEATURE_NAMES),
            'selection':selection,'training_records':train,'tree':tree,'tree_features_used':used,
            'validation_records':val,'cutoff_objective':table,'selected_cutoff':selected['cutoff'],'selected_validation':selected,
            'train_summary':{'cases':len(train),'p6_over_direct_geomean':geomean([r['p6_over_direct'] for r in train])},
            'validation_summary':{'cases':len(val),'selected_source_inclusive_geomean':selected['geomean_ratio'],'annotated':selected['annotated_cases']}}

# ---------- evaluation ----------
def source_arm_once(build,oracle,gate,arm,memory=False):
    if memory:tracemalloc.start()
    t0=time.perf_counter_ns()
    if arm==P8:
        f,root,n=build(TelemetryFactory); feat=f.features(); pred=eval_tree(gate['tree'],feat); annotate=pred<=gate['cutoff']
        backend=COMP_P6 if annotate else COMP_DIRECT
    else:
        f,root,n=build(base.Factory); feat=None; pred=None; annotate=(arm==P6ARM); backend=COMP_P6 if arm==P6ARM else COMP_DIRECT
    s1=time.perf_counter_ns()
    cr=compile_once(root,backend,oracle,n,False)
    t1=time.perf_counter_ns(); peak=None
    if memory:
        _,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
    return {'arm':arm,'ok':cr['ok'],'source_pipeline_ns':t1-t0,'source_build_ns':s1-t0,'compiler_ns':cr['pipeline_ns'],
            'backend':backend,'annotate':bool(annotate),'predicted_ratio':pred,'python_peak_bytes':peak,'digest':cr['digest'],
            'multiplications':cr.get('multiplications'),'pair_terms':cr.get('pair_terms'),'peak_monomials':cr.get('peak_monomials'),
            'anf_nodes_evaluated':cr.get('anf_nodes_evaluated'),'final_monomials':cr.get('final_monomials'),'final_degree':cr.get('final_degree'),
            'features':feat}

def compiler_dispatch_once(root,oracle,nvars,gate,features,arm):
    t0=time.perf_counter_ns()
    if arm==P8:
        pred=eval_tree(gate['tree'],features); backend=COMP_P6 if pred<=gate['cutoff'] else COMP_DIRECT
    else:
        pred=None; backend=COMP_P6 if arm==P6ARM else COMP_DIRECT
    r=compile_once(root,backend,oracle,nvars,False); t1=time.perf_counter_ns()
    return {'arm':arm,'compiler_dispatch_ns':t1-t0,'compiler_ns':r['pipeline_ns'],'backend':backend,'predicted_ratio':pred,'ok':r['ok']}

def p6_stats(root,oracle,nvars):
    pr,inf=p6.build_innode(root); r=p6.run_p6(pr,inf,oracle,nvars,False,True); return r

def eval_case(cid,build,oracle,meta,reps,seed,gate):
    # Fixed source semantics and symbolic work.
    tf,troot,n=build(TelemetryFactory); feat=tf.features(); pf,proot,pn=build(base.Factory)
    d=compile_once(proot,COMP_DIRECT,oracle,n,True); q=compile_once(proot,COMP_P6,oracle,n,True)
    pred=eval_tree(gate['tree'],feat); annotate=pred<=gate['cutoff']; z=q if annotate else d
    if not (d['ok'] and q['ok'] and d['digest']==q['digest']):raise AssertionError(('symbolic',cid))
    qs=p6_stats(proot,oracle,n)
    if qs.get('selector_accepted',0)!=qs.get('fold_lowerings',0):raise AssertionError(('P6 utilization',cid))
    symbolic={'case_id':cid,**meta,'features':feat,'predicted_ratio':pred,'annotate':annotate,
              'backend':COMP_P6 if annotate else COMP_DIRECT,
              'direct':{k:d.get(k) for k in ('digest','multiplications','pair_terms','peak_monomials','anf_nodes_evaluated','python_peak_bytes')},
              'p6':{k:q.get(k) for k in ('digest','multiplications','pair_terms','peak_monomials','anf_nodes_evaluated','python_peak_bytes')},
              'p8':{k:z.get(k) for k in ('digest','multiplications','pair_terms','peak_monomials','anf_nodes_evaluated','python_peak_bytes')},
              'p6_folds':qs.get('fold_lowerings',0),'p6_accepted':qs.get('selector_accepted',0),'p6_accepted_shared':qs.get('selector_accepted_shared',0)}
    # source-inclusive randomized schedule
    rr=random.Random(seed); schedule=[a for _ in range(reps) for a in (DIRECT,P6ARM,P8)]; rr.shuffle(schedule); rows=[]
    for rep,a in enumerate(schedule):
        r=source_arm_once(build,oracle,gate,a,False)
        if not r['ok']:raise AssertionError(('timed source',cid,a))
        rows.append({'case_id':cid,**meta,'rep':rep,**{k:r[k] for k in ('arm','source_pipeline_ns','source_build_ns','compiler_ns','backend','annotate','predicted_ratio','ok')}})
    # compiler-only randomized on one telemetry source root
    rr=random.Random(seed^0xC0A1); sched=[a for _ in range(reps) for a in (DIRECT,P6ARM,P8)]; rr.shuffle(sched); comp=[]
    for rep,a in enumerate(sched):
        r=compiler_dispatch_once(troot,oracle,n,gate,feat,a)
        if not r['ok']:raise AssertionError(('timed compiler',cid,a))
        comp.append({'case_id':cid,**meta,'rep':rep,**r})
    mem=[{'case_id':cid,**meta,**source_arm_once(build,oracle,gate,a,True)} for a in (DIRECT,P6ARM,P8)]
    return symbolic,rows,comp,mem

def fuzz():
    gate=load_gate(); rng=random.Random(FUZZ_SEED); failures=[]; ann=0
    for i in range(FUZZ_CASES):
        seed=rng.getrandbits(63); n=rng.randint(2,8); d=rng.randint(2,9)
        def build(Cls,seed=seed,n=n,d=d):
            rr=random.Random(seed); f=Cls(); root=base.random_expr(rr,n,d,f); return f,root,n
        try:
            tf,tr,nv=build(TelemetryFactory); pf,pr,_=build(base.Factory); oracle=base.eval_node_bitset(pr,nv)
            dd=compile_once(pr,COMP_DIRECT,oracle,nv,False); qq=compile_once(pr,COMP_P6,oracle,nv,False)
            pred=eval_tree(gate['tree'],tf.features()); choose=pred<=gate['cutoff']; zz=qq if choose else dd; ann+=int(choose)
            if not (dd['ok'] and qq['ok'] and dd['digest']==qq['digest']==zz['digest']):raise AssertionError('digest/oracle')
            td=compile_once(tr,COMP_DIRECT,oracle,nv,False)
            if td['digest']!=dd['digest']:raise AssertionError('telemetry semantics')
            for k in ('multiplications','pair_terms','peak_monomials','anf_nodes_evaluated'):
                if zz.get(k)!=(qq if choose else dd).get(k):raise AssertionError(('work',k))
        except Exception as e:
            failures.append({'case':i,'error':repr(e)})
            if len(failures)>=20:break
    return {'schema':'cm-n2-p8-fuzz/v1','cases':FUZZ_CASES,'annotated':ann,'failures':failures,'passed':not failures}

def run_gatep():
    gate=load_gate(); sym=[]; timing=[]; comp=[]; mem=[]
    frozen={(d,i):(r,n,o) for d,i,r,n,o in p6.generate_gate_cases()}
    for j,(cid,d,i,build) in enumerate(gatep_eval_recipes()):
        pf,pr,n=build(base.Factory); oracle=base.eval_node_bitset(pr,n)
        fr,fn,fo=frozen[(d,i)]; fd=compile_once(fr,COMP_DIRECT,fo,fn,False); rd=compile_once(pr,COMP_DIRECT,oracle,n,False)
        if fd['digest']!=rd['digest']:raise AssertionError(('Gate-P frozen identity drift',cid))
        s,t,c,m=eval_case(cid,build,oracle,{'corpus':'gatep','depth':d,'case':i},GATEP_REPS,SEED+d*1000+i+0x8800,gate)
        sym.append(s); timing.extend(t); comp.extend(c); mem.extend(m)
    return {'schema':'cm-n2-p8-gatep/v1','gate_sha256':sha256_file(HERE/'P8_FROZEN_GATE.json'),'symbolic':sym,
            'source_timing_rows':timing,'compiler_timing_rows':comp,'memory_rows':mem}

def run_natural_case(case_id):
    gate=load_gate(); recipes,selection,selsha=natural_eval_recipes(); by={x[0]:x for x in recipes}; cid,circuit,d,build,oracle,c=by[case_id]
    meta={'corpus':'natural','circuit':circuit,'root':c['root'],'support':c['support'],'source_nodes':c['source_nodes'],'depth':d}
    s,t,cc,m=eval_case(cid,build,oracle,meta,NAT_REPS,SEED^int(hashlib.sha256(cid.encode()).hexdigest()[:8],16)^0x8800,gate)
    return {'schema':'cm-n2-p8-natural-case/v1','case_id':cid,'selection_sha256':selsha,'symbolic':s,
            'source_timing_rows':t,'compiler_timing_rows':cc,'memory_rows':m}

# ---------- summarization ----------
def medians(rows,metric):
    g=defaultdict(list)
    for r in rows:g[(r['case_id'],r['arm'])].append(r[metric])
    return {k:statistics.median(v) for k,v in g.items()}

def compare(rows,metric,num,den,seed=SEED):
    m=medians(rows,metric); cases=sorted({r['case_id'] for r in rows}); ratios=[]; wins=0; an=ad=0.0
    per={}
    for c in cases:
        a=m[(c,num)]; b=m[(c,den)]; ratios.append(a/b); wins+=a<b; an+=a; ad+=b; per[c]=a/b
    bs=bootstrap_geomean(ratios,5000,seed)
    return {'cases':len(cases),'geomean_ratio':bs['estimate'],'ci95':bs['ci95'],'weighted_ratio':an/ad,'wins':wins,'case_ratios':per}

def sym_work(symbolic,field):
    vals=[]
    for r in symbolic:
        d=r['direct'].get(field); z=r['p8'].get(field)
        if d not in (None,0):vals.append(z/d)
    return {'geomean_ratio':geomean(vals),'median_ratio':statistics.median(vals) if vals else None}

def summarize(gatep,natural,fuzz,cal):
    gs=gatep['source_timing_rows']; gc=gatep['compiler_timing_rows']; ns=[]; nc=[]; nsy=[]; nmem=[]
    for x in natural: ns.extend(x['source_timing_rows']); nc.extend(x['compiler_timing_rows']); nsy.append(x['symbolic']); nmem.extend(x['memory_rows'])
    source_cmp={k:compare(gs,'source_pipeline_ns',num,den,SEED^hash(k)) for k,num,den in (
        ('p8_direct',P8,DIRECT),('p8_p6',P8,P6ARM),('p6_direct',P6ARM,DIRECT))}
    comp_cmp={k:compare(gc,'compiler_dispatch_ns',num,den,SEED^hash(k)) for k,num,den in (
        ('p8_direct',P8,DIRECT),('p8_p6',P8,P6ARM),('p6_direct',P6ARM,DIRECT))}
    nat_source={k:compare(ns,'source_pipeline_ns',num,den,SEED^0x100^hash(k)) for k,num,den in (
        ('p8_direct',P8,DIRECT),('p8_p6',P8,P6ARM),('p6_direct',P6ARM,DIRECT))}
    nat_comp={k:compare(nc,'compiler_dispatch_ns',num,den,SEED^0x200^hash(k)) for k,num,den in (
        ('p8_direct',P8,DIRECT),('p8_p6',P8,P6ARM),('p6_direct',P6ARM,DIRECT))}
    gsym=gatep['symbolic']; annotated=[r for r in gsym if r['annotate']]; p6wins=[]; goodann=badann=0
    gm=medians(gs,'source_pipeline_ns')
    for r in gsym:
        c=r['case_id']; win=gm[(c,P6ARM)]<gm[(c,DIRECT)]; p6wins.append(win)
        if r['annotate']:
            if win:goodann+=1
            else:badann+=1
    work={f:sym_work(gsym,f) for f in ('multiplications','pair_terms','peak_monomials','anf_nodes_evaluated')}
    # telemetry source overhead from direct vs P8 source_build medians isolates source builder cost approximately.
    srcm=medians(gs,'source_build_ns'); src_rat=[srcm[(c,P8)]/srcm[(c,DIRECT)] for c in sorted({r['case_id'] for r in gs})]
    nsrcm=medians(ns,'source_build_ns'); nsrc_rat=[nsrcm[(c,P8)]/nsrcm[(c,DIRECT)] for c in sorted({r['case_id'] for r in ns})]
    primary=source_cmp['p8_direct']; pair=work['pair_terms']['geomean_ratio']; peak=work['peak_monomials']['geomean_ratio']
    passflag=(fuzz['passed'] and any(r['annotate'] and r['p6_folds']>0 for r in gsym) and primary['geomean_ratio']<=.95 and primary['ci95'][1]<1.0 and (pair is None or pair<=1.05) and (peak is None or peak<=1.05))
    return {'schema':'cm-n2-p8-summary/v1','fuzz':fuzz,'calibration':{'train_cases':len(cal['training_records']),'validation_cases':len(cal['validation_records']),
            'selected_cutoff':cal['selected_cutoff'],'tree_features_used':cal['tree_features_used'],'validation_selected':cal['selected_validation']},
            'gatep_source':source_cmp,'gatep_compiler':comp_cmp,'gatep_annotated':len(annotated),'gatep_fold_cases':sum(r['annotate'] and r['p6_folds']>0 for r in gsym),
            'gatep_folds':sum(r['p6_folds'] if r['annotate'] else 0 for r in gsym),'gatep_confusion':{'p6_wins':sum(p6wins),'annotated_p6_wins':goodann,'annotated_p6_losses':badann,
            'p6_wins_bypassed':sum(win and not r['annotate'] for win,r in zip(p6wins,gsym))},'gatep_work':work,
            'gatep_telemetry_source_overhead':{'geomean_ratio':geomean(src_rat),'median_ratio':statistics.median(src_rat)},
            'natural_source':nat_source,'natural_compiler':nat_comp,'natural_annotated':sum(r['annotate'] for r in nsy),
            'natural_fold_cases':sum(r['annotate'] and r['p6_folds']>0 for r in nsy),'natural_telemetry_source_overhead':{'geomean_ratio':geomean(nsrc_rat),'median_ratio':statistics.median(nsrc_rat)},
            'predeclared_gatep_source_inclusive_pass':passflag}


def main():
    if sha256_file(HERE/'N2_P8_PREREGISTRATION.md')!=PREREG_SHA256:raise SystemExit('P8 preregistration hash mismatch')
    ap=argparse.ArgumentParser(); ap.add_argument('--mode',required=True,choices=('selection','calibrate','fuzz','gatep','natural-case')); ap.add_argument('--case-id'); ap.add_argument('--out',required=True)
    a=ap.parse_args(); out=Path(a.out)
    if a.mode=='selection': obj=epfl_trainval_selection()
    elif a.mode=='calibrate': obj=calibrate()
    elif a.mode=='fuzz': obj=fuzz()
    elif a.mode=='gatep': obj=run_gatep()
    else:
        if not a.case_id:raise SystemExit('--case-id required')
        obj=run_natural_case(a.case_id)
    out.write_text(json.dumps(obj,indent=2),encoding='utf-8'); print(json.dumps({'mode':a.mode,'out':str(out),'ok':True,'keys':list(obj)[:8]},indent=2))

if __name__=='__main__': main()
