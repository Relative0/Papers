from __future__ import annotations
import argparse, hashlib, json, math, random, statistics, sys, time, tracemalloc
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
P10_DIR = ROOT / 'cm_n2_p10_run'
if str(P10_DIR) not in sys.path:
    sys.path.insert(0, str(P10_DIR))
import n2_p10_harness as p10

p9 = p10.p9
p8 = p10.p8
base = p10.base
SEED = p10.SEED
FUZZ_SEED = SEED ^ 0xB11F
PREREG_SHA256 = '2a6f61652058ec6b1d8db4ab77f1cb9e34032f385406d783f821a23db701f304'
FUZZ_CASES = 1000
GATEP_REPS = p10.GATEP_REPS
NAT_REPS = p10.NAT_REPS

DIRECT = p10.DIRECT
P6ARM = p10.P6ARM
P10ARM = p10.P10
P11 = 'p11_tree_specialized_dispatch'
COMP_DIRECT = p10.COMP_DIRECT
COMP_P6 = p10.COMP_P6

# Frozen P8 tree node indices used by the only annotate path.
ROOT_NODE = 0          # max_pair_shells <= 4.5 -> all bypass leaves
REUSE_NODE = 8         # reuse_density <= threshold
REPEAT_NODE = 9        # pair_repeat_density <= threshold -> annotate leaf 10
ANNOTATE_LEAF = 10
REPEAT_BYPASS_LEAF = 11
REUSE_BYPASS_LEAF = 12


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def geomean(xs):
    xs = [float(x) for x in xs if x is not None and x > 0]
    return math.exp(sum(math.log(x) for x in xs) / len(xs)) if xs else None


def quantile(xs, p):
    s = sorted(xs)
    if not s:
        return None
    z = (len(s) - 1) * p
    lo = int(z); hi = min(lo + 1, len(s) - 1); f = z - lo
    return s[lo] * (1 - f) + s[hi] * f


def bootstrap_geomean(ratios, n=5000, seed=SEED):
    ratios = [x for x in ratios if x and x > 0]
    if not ratios:
        return {'estimate': None, 'ci95': [None, None]}
    rng = random.Random(seed)
    vals = [geomean([rng.choice(ratios) for _ in ratios]) for __ in range(n)]
    return {'estimate': geomean(ratios), 'ci95': [quantile(vals,.025), quantile(vals,.975)], 'bootstrap_n': n}


def _ratio_le_int(num: int, den: int, threshold: float) -> bool:
    """Exact rational comparison against the frozen binary-float threshold."""
    if den <= 0:
        return 0 <= threshold
    tnum, tden = float(threshold).as_integer_ratio()
    return num * tden <= den * tnum


class TreeSpecializedTelemetryFactory(base.Factory):
    """Ordinary Factory semantics plus only telemetry needed by the frozen annotate path."""
    def __init__(self):
        self.cache = {}
        self.nodes = []
        self.used = bytearray()
        self.edge_count = 0
        self.binary_nodes = 0
        self.reuse_edge_events = 0
        self.pair_repeat_excess = 0
        self.shell_ge5 = False
        self._pair_counts = {}

    def _make(self, op, args=(), value=None):
        args = tuple(args)
        ids = tuple(a.nid for a in args)
        key = (op, ids, value)
        cache = self.cache
        n = cache.get(key)
        if n is not None:
            return n

        nodes = self.nodes
        n = base.Node(len(nodes), op, args, value)
        cache[key] = n
        nodes.append(n)
        self.used.append(0)

        arity = len(args)
        self.edge_count += arity
        used = self.used
        reuse = self.reuse_edge_events
        for i in ids:
            if used[i]:
                reuse += 1
            else:
                used[i] = 1
        self.reuse_edge_events = reuse

        if arity == 2 and op in ('and','or','xor','tf'):
            self.binary_nodes += 1
            a, b = ids
            if a > b:
                a, b = b, a
            pkey = (a << 32) | b
            counts = self._pair_counts
            if self.shell_ge5:
                # Once a five-shell exists, exact shell counts are irrelevant to the frozen
                # decision. Membership alone is enough to maintain pair_repeat_excess.
                if pkey in counts:
                    self.pair_repeat_excess += 1
                else:
                    counts[pkey] = 1
            else:
                old = counts.get(pkey, 0)
                if old:
                    self.pair_repeat_excess += 1
                    new = old + 1
                    counts[pkey] = new
                    if new >= 5:
                        self.shell_ge5 = True
                else:
                    counts[pkey] = 1
        return n

    def counters(self):
        return {
            'edge_count': self.edge_count,
            'binary_nodes': self.binary_nodes,
            'reuse_edge_events': self.reuse_edge_events,
            'pair_repeat_excess': self.pair_repeat_excess,
            'shell_ge5': bool(self.shell_ge5),
        }

    def dispatch(self, gate):
        tree = gate['tree']
        # Root threshold is frozen at 4.5. shell_ge5 exactly encodes the right branch.
        if not self.shell_ge5:
            return False, 'shell_lt5_bypass', None

        reuse_t = float(tree['threshold'][REUSE_NODE])
        if not _ratio_le_int(self.reuse_edge_events, self.edge_count, reuse_t):
            return False, 'reuse_density_bypass', math.exp(tree['value'][REUSE_BYPASS_LEAF])

        repeat_t = float(tree['threshold'][REPEAT_NODE])
        if _ratio_le_int(self.pair_repeat_excess, self.binary_nodes, repeat_t):
            return True, 'annotate_leaf10', math.exp(tree['value'][ANNOTATE_LEAF])
        return False, 'pair_repeat_density_bypass', math.exp(tree['value'][REPEAT_BYPASS_LEAF])


def load_gate():
    gate = p9.load_gate()
    tree = gate['tree']
    # Freeze the structural proof that only leaf 10 is below the 0.80 cutoff.
    if gate['cutoff'] != 0.8:
        raise ValueError('P8 cutoff drift')
    if tree['feature'][ROOT_NODE] != 10 or tree['threshold'][ROOT_NODE] != 4.5:
        raise ValueError('P8 root drift')
    if tree['feature'][REUSE_NODE] != 14 or tree['feature'][REPEAT_NODE] != 15:
        raise ValueError('P8 annotate path feature drift')
    leaves = [i for i,l in enumerate(tree['children_left']) if l < 0]
    below = [i for i in leaves if math.exp(tree['value'][i]) <= gate['cutoff']]
    if below != [ANNOTATE_LEAF]:
        raise ValueError(('P8 annotate leaf drift', below))
    return gate


def _compare_p10_p11(f10, f11, cid, gate):
    a = f10.features(); c = f11.counters()
    for k in ('edge_count','binary_nodes','reuse_edge_events','pair_repeat_excess'):
        if a[k] != c[k]:
            raise AssertionError(('P10/P11 counter mismatch',cid,k,a[k],c[k]))
    if bool(a['max_pair_shells'] >= 5) != c['shell_ge5']:
        raise AssertionError(('P10/P11 shell mismatch',cid,a['max_pair_shells'],c['shell_ge5']))
    pred10 = p9.eval_tree_min(gate['tree'], a)
    d10 = pred10 <= gate['cutoff']
    d11, code, leaf_ratio = f11.dispatch(gate)
    if d10 != d11:
        raise AssertionError(('P10/P11 decision mismatch',cid,d10,d11,pred10,code,leaf_ratio,a,c))
    return a, c, pred10, d11, code, leaf_ratio


def invariant_check():
    gate = load_gate()
    cal = json.loads((p9.P8_DIR / 'calibration.json').read_text())
    gp = json.loads((p9.P8_DIR / 'gatep.json').read_text())
    combined = json.loads((p9.P8_DIR / 'n2_p8_results.json').read_text())
    issues = []
    checked = {'training':0,'validation':0,'gatep':0,'natural':0}

    def check(cid, build, ref):
        try:
            f10, r10, n10 = build(p10.FusedMinimalTelemetryFactory)
            f11, r11, n11 = build(TreeSpecializedTelemetryFactory)
            a,c,pred,d11,code,leaf = _compare_p10_p11(f10,f11,cid,gate)
            refpred = p8.eval_tree(gate['tree'], ref['features'])
            if (refpred <= gate['cutoff']) != d11:
                raise AssertionError(('reference decision mismatch',cid,refpred,d11))
            if n10 != n11:
                raise AssertionError(('nvars mismatch',cid,n10,n11))
            # Semantic identity is checked cheaply through the structural direct compiler digest.
            d10 = p10.compile_once(r10, COMP_DIRECT, base.eval_node_bitset(r10,n10), n10, False)
            d11c = p10.compile_once(r11, COMP_DIRECT, base.eval_node_bitset(r11,n11), n11, False)
            if d10['digest'] != d11c['digest']:
                raise AssertionError(('source semantic digest mismatch',cid))
        except Exception as e:
            issues.append({'case_id':cid,'error':repr(e)})

    train_refs = {r['case_id']:r for r in cal['training_records']}
    for cid, kind, d, build in p8.training_synthetic_recipes():
        check(cid, build, train_refs[cid]); checked['training'] += 1
    for cid, kind, d, build, oracle, extra in p8.epfl_recipes('train', cal['selection']):
        check(cid, build, train_refs[cid]); checked['training'] += 1

    val_refs = {r['case_id']:r for r in cal['validation_records']}
    for cid, kind, d, build in p8.validation_synthetic_recipes():
        check(cid, build, val_refs[cid]); checked['validation'] += 1
    for cid, kind, d, build, oracle, extra in p8.epfl_recipes('validation', cal['selection']):
        check(cid, build, val_refs[cid]); checked['validation'] += 1

    gp_refs = {r['case_id']:r for r in gp['symbolic']}
    for cid, d, i, build in p8.gatep_eval_recipes():
        check(cid, build, gp_refs[cid]); checked['gatep'] += 1

    nat_refs = {x['case_id']:x['symbolic'] for x in combined['natural_cases']}
    for cid, circuit, d, build, oracle, c in p8.natural_eval_recipes()[0]:
        check(cid, build, nat_refs[cid]); checked['natural'] += 1

    return {'schema':'cm-n2-p11-invariance/v1','checked':checked,'total':sum(checked.values()),
            'issues':issues,'passed':not issues,'gate_sha256':sha256_file(p9.P8_DIR/'P8_FROZEN_GATE.json')}


def compile_once(root, backend, oracle, nvars, memory=False):
    return p10.compile_once(root, backend, oracle, nvars, memory)


def p6_stats(root, oracle, nvars):
    return p10.p6_stats(root, oracle, nvars)


def source_arm_once(build, oracle, gate, arm, memory=False):
    if memory:
        tracemalloc.start()
    t0 = time.perf_counter_ns()
    decision_code = None
    if arm == P11:
        f, root, n = build(TreeSpecializedTelemetryFactory)
        annotate, decision_code, leaf_ratio = f.dispatch(gate)
        feat = f.counters(); pred = leaf_ratio
        backend = COMP_P6 if annotate else COMP_DIRECT
    elif arm == P10ARM:
        f, root, n = build(p10.FusedMinimalTelemetryFactory)
        feat = f.features(); pred = p9.eval_tree_min(gate['tree'], feat)
        annotate = pred <= gate['cutoff']; backend = COMP_P6 if annotate else COMP_DIRECT
    else:
        f, root, n = build(base.Factory)
        feat = None; pred = None; annotate = arm == P6ARM
        backend = COMP_P6 if annotate else COMP_DIRECT
    s1 = time.perf_counter_ns()
    cr = compile_once(root, backend, oracle, n, False)
    t1 = time.perf_counter_ns()
    peak = None
    if memory:
        _, peak = tracemalloc.get_traced_memory(); tracemalloc.stop()
    return {
        'arm':arm,'ok':cr['ok'],'source_pipeline_ns':t1-t0,'source_build_ns':s1-t0,
        'compiler_ns':cr['pipeline_ns'],'backend':backend,'annotate':bool(annotate),
        'predicted_ratio':pred,'decision_code':decision_code,'python_peak_bytes':peak,'digest':cr['digest'],
        'multiplications':cr.get('multiplications'),'pair_terms':cr.get('pair_terms'),
        'peak_monomials':cr.get('peak_monomials'),'anf_nodes_evaluated':cr.get('anf_nodes_evaluated'),
        'final_monomials':cr.get('final_monomials'),'final_degree':cr.get('final_degree'),'features':feat,
    }


def fuzz():
    gate = load_gate(); rng = random.Random(FUZZ_SEED); failures=[]; annotated=0
    for i in range(FUZZ_CASES):
        seed=rng.getrandbits(63); nvars=rng.randint(2,8); depth=rng.randint(2,9)
        def build(Cls, seed=seed, nvars=nvars, depth=depth):
            rr=random.Random(seed); f=Cls(); root=base.random_expr(rr,nvars,depth,f); return f,root,nvars
        try:
            pf, pr, n = build(base.Factory)
            f10, r10, n10 = build(p10.FusedMinimalTelemetryFactory)
            f11, r11, n11 = build(TreeSpecializedTelemetryFactory)
            a,c,pred10,choose,code,leaf = _compare_p10_p11(f10,f11,f'fuzz:{i}',gate)
            annotated += int(choose)
            oracle=base.eval_node_bitset(pr,n)
            dd=compile_once(pr,COMP_DIRECT,oracle,n,False)
            qq=compile_once(pr,COMP_P6,oracle,n,False)
            d10=compile_once(r10,COMP_DIRECT,oracle,n10,False)
            d11=compile_once(r11,COMP_DIRECT,oracle,n11,False)
            if not (dd['ok'] and qq['ok'] and d10['ok'] and d11['ok'] and dd['digest']==qq['digest']==d10['digest']==d11['digest']):
                raise AssertionError('digest/oracle')
            selected=qq if choose else dd
            for k in ('multiplications','pair_terms','peak_monomials','anf_nodes_evaluated'):
                if selected.get(k) != (qq if choose else dd).get(k):
                    raise AssertionError(('selected work',k))
            qs=p6_stats(pr,oracle,n)
            if qs.get('selector_accepted',0) != qs.get('fold_lowerings',0):
                raise AssertionError('P6 utilization')
        except Exception as e:
            failures.append({'case':i,'error':repr(e)})
            if len(failures)>=20: break
    return {'schema':'cm-n2-p11-fuzz/v1','cases':FUZZ_CASES,'annotated':annotated,'failures':failures,'passed':not failures}


def eval_case(cid, build, oracle, meta, reps, seed, gate):
    f10, r10, n10 = build(p10.FusedMinimalTelemetryFactory)
    f11, r11, n11 = build(TreeSpecializedTelemetryFactory)
    feat10,c11,pred10,annotate,code,leaf = _compare_p10_p11(f10,f11,cid,gate)

    pf, proot, n = build(base.Factory)
    if n != n10 or n != n11: raise AssertionError(('nvars drift',cid,n,n10,n11))
    direct=compile_once(proot,COMP_DIRECT,oracle,n,True)
    p6r=compile_once(proot,COMP_P6,oracle,n,True)
    selected=p6r if annotate else direct
    if not (direct['ok'] and p6r['ok'] and direct['digest']==p6r['digest']): raise AssertionError(('symbolic',cid))
    qs=p6_stats(proot,oracle,n)
    if qs.get('selector_accepted',0)!=qs.get('fold_lowerings',0): raise AssertionError(('P6 utilization',cid))
    symbolic={
        'case_id':cid,**meta,'p10_features':feat10,'p10_predicted_ratio':pred10,'p11_counters':c11,
        'p11_decision_code':code,'p11_leaf_ratio':leaf,'annotate':annotate,'backend':COMP_P6 if annotate else COMP_DIRECT,
        'direct':{k:direct.get(k) for k in ('digest','multiplications','pair_terms','peak_monomials','anf_nodes_evaluated','python_peak_bytes')},
        'p6':{k:p6r.get(k) for k in ('digest','multiplications','pair_terms','peak_monomials','anf_nodes_evaluated','python_peak_bytes')},
        'p11':{k:selected.get(k) for k in ('digest','multiplications','pair_terms','peak_monomials','anf_nodes_evaluated','python_peak_bytes')},
        'p6_folds':qs.get('fold_lowerings',0),'p6_accepted':qs.get('selector_accepted',0),'p6_accepted_shared':qs.get('selector_accepted_shared',0),
    }
    rr=random.Random(seed); schedule=[a for _ in range(reps) for a in (DIRECT,P6ARM,P10ARM,P11)]; rr.shuffle(schedule)
    rows=[]
    for rep,arm in enumerate(schedule):
        r=source_arm_once(build,oracle,gate,arm,False)
        if not r['ok']: raise AssertionError(('timed source',cid,arm))
        if arm in (P10ARM,P11) and bool(r['annotate']) != annotate: raise AssertionError(('timed decision drift',cid,arm))
        rows.append({'case_id':cid,**meta,'rep':rep,**{k:r[k] for k in ('arm','source_pipeline_ns','source_build_ns','compiler_ns','backend','annotate','predicted_ratio','decision_code','ok')}})
    mem=[]
    for arm in (DIRECT,P6ARM,P10ARM,P11):
        r=source_arm_once(build,oracle,gate,arm,True)
        if not r['ok']: raise AssertionError(('memory',cid,arm))
        mem.append({'case_id':cid,**meta,**r})
    return symbolic,rows,mem


def run_gatep():
    gate=load_gate(); sym=[]; timing=[]; mem=[]
    frozen={(d,i):(r,n,o) for d,i,r,n,o in p8.p6.generate_gate_cases()}
    for cid,d,i,build in p8.gatep_eval_recipes():
        pf,pr,n=build(base.Factory); oracle=base.eval_node_bitset(pr,n)
        fr,fn,fo=frozen[(d,i)]; fd=compile_once(fr,COMP_DIRECT,fo,fn,False); rd=compile_once(pr,COMP_DIRECT,oracle,n,False)
        if fd['digest']!=rd['digest']: raise AssertionError(('Gate-P frozen identity drift',cid))
        s,t,m=eval_case(cid,build,oracle,{'corpus':'gatep','depth':d,'case':i},GATEP_REPS,SEED+d*1000+i+0xB110,gate)
        sym.append(s); timing.extend(t); mem.extend(m)
    return {'schema':'cm-n2-p11-gatep/v1','gate_sha256':sha256_file(p9.P8_DIR/'P8_FROZEN_GATE.json'),
            'symbolic':sym,'source_timing_rows':timing,'memory_rows':mem}


def run_natural_case(case_id):
    gate=load_gate(); recipes,selection,selsha=p8.natural_eval_recipes(); by={x[0]:x for x in recipes}
    cid,circuit,depth,build,oracle,c=by[case_id]
    meta={'corpus':'natural','circuit':circuit,'root':c['root'],'support':c['support'],'source_nodes':c['source_nodes'],'depth':depth}
    s,t,m=eval_case(cid,build,oracle,meta,NAT_REPS,SEED^int(hashlib.sha256(cid.encode()).hexdigest()[:8],16)^0xB110,gate)
    return {'schema':'cm-n2-p11-natural-case/v1','case_id':cid,'selection_sha256':selsha,'symbolic':s,'source_timing_rows':t,'memory_rows':m}


def medians(rows, metric):
    g=defaultdict(list)
    for r in rows:g[(r['case_id'],r['arm'])].append(r[metric])
    return {k:statistics.median(v) for k,v in g.items()}


def compare(rows,metric,num,den,seed=SEED):
    m=medians(rows,metric); cases=sorted({r['case_id'] for r in rows}); ratios=[]; wins=0; an=ad=0.0; per={}
    for c in cases:
        a=m[(c,num)]; b=m[(c,den)]; ratios.append(a/b); wins+=a<b; an+=a; ad+=b; per[c]=a/b
    bs=bootstrap_geomean(ratios,5000,seed)
    return {'cases':len(cases),'geomean_ratio':bs['estimate'],'ci95':bs['ci95'],'weighted_ratio':an/ad,'wins':wins,'case_ratios':per}


def work_ratio(symbolic,field):
    vals=[]
    for r in symbolic:
        d=r['direct'].get(field); z=r['p11'].get(field)
        if d not in (None,0): vals.append(z/d)
    return {'geomean_ratio':geomean(vals),'median_ratio':statistics.median(vals) if vals else None}


def summarize(gatep,natural,fuzz,invariant):
    gs=gatep['source_timing_rows']; gsym=gatep['symbolic']; ns=[]; nsy=[]; nmem=[]
    for x in natural: ns.extend(x['source_timing_rows']); nsy.append(x['symbolic']); nmem.extend(x['memory_rows'])
    def cmps(rows,metric,prefix):
        pairs=(('p11_direct',P11,DIRECT),('p11_p10',P11,P10ARM),('p11_p6',P11,P6ARM),('p10_direct',P10ARM,DIRECT),('p6_direct',P6ARM,DIRECT))
        return {k:compare(rows,metric,a,b,SEED^int(hashlib.sha256((prefix+k+metric).encode()).hexdigest()[:8],16)) for k,a,b in pairs}
    source=cmps(gs,'source_pipeline_ns','g'); build=cmps(gs,'source_build_ns','gb'); compiler=cmps(gs,'compiler_ns','gc')
    nsource=cmps(ns,'source_pipeline_ns','n'); nbuild=cmps(ns,'source_build_ns','nb'); ncompiler=cmps(ns,'compiler_ns','nc')
    work={f:work_ratio(gsym,f) for f in ('multiplications','pair_terms','peak_monomials','anf_nodes_evaluated')}
    primary=source['p11_direct']; pair=work['pair_terms']['geomean_ratio']; peak=work['peak_monomials']['geomean_ratio']
    passflag=(fuzz['passed'] and invariant['passed'] and any(r['annotate'] and r['p6_folds']>0 for r in gsym)
              and primary['geomean_ratio']<=.95 and primary['ci95'][1]<1.0
              and (pair is None or pair<=1.05) and (peak is None or peak<=1.05))
    eng=(invariant['passed'] and build['p11_p10']['geomean_ratio']<=.90 and source['p11_p10']['geomean_ratio']<=.98 and source['p11_p10']['ci95'][1]<1.0)
    def memory_compare(memrows,num,den):
        by={(r['case_id'],r['arm']):r['python_peak_bytes'] for r in memrows}; cases=sorted({r['case_id'] for r in memrows})
        ratios=[by[(c,num)]/by[(c,den)] for c in cases if by[(c,den)]]
        return {'cases':len(ratios),'geomean_ratio':geomean(ratios),'median_ratio':statistics.median(ratios) if ratios else None}
    gm=medians(gs,'source_pipeline_ns'); good=bad=miss=p6wins=0
    for r in gsym:
        c=r['case_id']; win=gm[(c,P6ARM)]<gm[(c,DIRECT)]; p6wins+=int(win)
        if r['annotate']: good+=int(win); bad+=int(not win)
        elif win: miss+=1
    return {
        'schema':'cm-n2-p11-summary/v1','fuzz':fuzz,'invariance':invariant,
        'gatep_source':source,'gatep_source_build':build,'gatep_compiler':compiler,
        'gatep_annotated':sum(r['annotate'] for r in gsym),'gatep_fold_cases':sum(r['annotate'] and r['p6_folds']>0 for r in gsym),
        'gatep_folds':sum(r['p6_folds'] if r['annotate'] else 0 for r in gsym),
        'gatep_confusion':{'p6_wins':p6wins,'annotated_p6_wins':good,'annotated_p6_losses':bad,'p6_wins_bypassed':miss},
        'gatep_work':work,
        'gatep_memory':{'p11_direct':memory_compare(gatep['memory_rows'],P11,DIRECT),'p11_p10':memory_compare(gatep['memory_rows'],P11,P10ARM),'p11_p6':memory_compare(gatep['memory_rows'],P11,P6ARM)},
        'natural_source':nsource,'natural_source_build':nbuild,'natural_compiler':ncompiler,
        'natural_annotated':sum(r['annotate'] for r in nsy),'natural_fold_cases':sum(r['annotate'] and r['p6_folds']>0 for r in nsy),
        'natural_memory':{'p11_direct':memory_compare(nmem,P11,DIRECT),'p11_p10':memory_compare(nmem,P11,P10ARM)},
        'predeclared_gatep_direct_crossover_pass':passflag,'predeclared_specialized_telemetry_engineering_success':eng,
    }


def main():
    if sha256_file(HERE/'N2_P11_PREREGISTRATION.md') != PREREG_SHA256:
        raise SystemExit('P11 preregistration hash mismatch')
    ap=argparse.ArgumentParser(); ap.add_argument('--mode',required=True,choices=('invariant','fuzz','gatep','natural-case')); ap.add_argument('--case-id'); ap.add_argument('--out',required=True)
    a=ap.parse_args(); out=Path(a.out)
    if a.mode=='invariant':obj=invariant_check()
    elif a.mode=='fuzz':obj=fuzz()
    elif a.mode=='gatep':obj=run_gatep()
    else:
        if not a.case_id:raise SystemExit('--case-id required')
        obj=run_natural_case(a.case_id)
    out.write_text(json.dumps(obj,indent=2),encoding='utf-8')
    print(json.dumps({'mode':a.mode,'out':str(out),'ok':True,'keys':list(obj)[:8]},indent=2))

if __name__=='__main__':main()
