from __future__ import annotations
import argparse, hashlib, json, math, random, statistics, sys, time, tracemalloc
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
P8_DIR = ROOT / 'cm_n2_p8_run'
if str(P8_DIR) not in sys.path:
    sys.path.insert(0, str(P8_DIR))
import n2_p8_harness as p8

base = p8.base
SEED = 20260918
FUZZ_SEED = SEED ^ 0x9F22
PREREG_SHA256 = '76ab67e4918d625552313acdd8611d8ff0a86523b9114b1d6ed721b3052645d3'
FUZZ_CASES = 1000
GATEP_REPS = 20
NAT_REPS = 15

DIRECT = 'direct_source_pipeline'
P6ARM = 'p6_source_pipeline'
P8FULL = 'p8_full_source_dispatch'
P9 = 'p9_min_source_dispatch'
COMP_DIRECT = p8.COMP_DIRECT
COMP_P6 = p8.COMP_P6
USED_FEATURES = ('max_depth', 'max_pair_shells', 'binary_density', 'reuse_density', 'pair_repeat_density')


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
    lo = int(z)
    hi = min(lo + 1, len(s) - 1)
    f = z - lo
    return s[lo] * (1 - f) + s[hi] * f


def bootstrap_geomean(ratios, n=5000, seed=SEED):
    ratios = [x for x in ratios if x and x > 0]
    if not ratios:
        return {'estimate': None, 'ci95': [None, None]}
    rng = random.Random(seed)
    vals = [geomean([rng.choice(ratios) for _ in ratios]) for __ in range(n)]
    return {'estimate': geomean(ratios), 'ci95': [quantile(vals, .025), quantile(vals, .975)], 'bootstrap_n': n}


class MinimalTelemetryFactory(base.Factory):
    """Ordinary source Factory plus only telemetry required by the frozen P8 tree."""
    def __init__(self):
        super().__init__()
        self.depths = bytearray()
        self.used = bytearray()
        self.edge_count = 0
        self.binary_nodes = 0
        self.max_depth = 0
        self.reuse_edge_events = 0
        self.pair_repeat_excess = 0
        self.max_pair_shells = 0
        self._pair_counts = {}

    def _make(self, op, args=(), value=None):
        before = len(self.nodes)
        n = super()._make(op, args, value)
        if len(self.nodes) == before:
            return n

        ar = n.args
        if not ar:
            depth = 0
        elif len(ar) == 1:
            depth = self.depths[ar[0].nid] + 1
        elif len(ar) == 2:
            d0 = self.depths[ar[0].nid]
            d1 = self.depths[ar[1].nid]
            depth = (d0 if d0 >= d1 else d1) + 1
        else:
            depth = 1 + max(self.depths[c.nid] for c in ar)
        if depth > 255:
            raise OverflowError('P9 source depth exceeds byte telemetry bound')
        self.depths.append(depth)
        self.used.append(0)
        if depth > self.max_depth:
            self.max_depth = depth

        self.edge_count += len(ar)
        used = self.used
        for c in ar:
            i = c.nid
            if used[i]:
                self.reuse_edge_events += 1
            else:
                used[i] = 1

        if len(ar) == 2 and op in ('and', 'or', 'xor', 'tf'):
            self.binary_nodes += 1
            a = ar[0].nid
            b = ar[1].nid
            if a > b:
                a, b = b, a
            key = (a << 32) | b
            old = self._pair_counts.get(key, 0)
            new = old + 1
            self._pair_counts[key] = new
            if old:
                self.pair_repeat_excess += 1
            if new > self.max_pair_shells:
                self.max_pair_shells = new
        return n

    def features(self):
        n = len(self.nodes)
        e = self.edge_count
        b = self.binary_nodes
        return {
            'node_count': n,
            'edge_count': e,
            'binary_nodes': b,
            'max_depth': self.max_depth,
            'reuse_edge_events': self.reuse_edge_events,
            'pair_repeat_excess': self.pair_repeat_excess,
            'max_pair_shells': self.max_pair_shells,
            'binary_density': b / max(1, n),
            'reuse_density': self.reuse_edge_events / max(1, e),
            'pair_repeat_density': self.pair_repeat_excess / max(1, b),
        }


def eval_tree_min(tree, features):
    # Use the original P8 feature indices/names, but P9 computes only names the tree can reach.
    i = 0
    names = p8.FEATURE_NAMES
    while True:
        l = tree['children_left'][i]
        r = tree['children_right'][i]
        if l == r or l < 0:
            return math.exp(tree['value'][i])
        name = names[tree['feature'][i]]
        if name not in features:
            raise KeyError(f'frozen P8 tree unexpectedly requested omitted feature {name}')
        i = l if float(features[name]) <= tree['threshold'][i] else r


def load_gate():
    gate = json.loads((P8_DIR / 'P8_FROZEN_GATE.json').read_text())
    if gate['cutoff'] != 0.8:
        raise ValueError('P8 cutoff drift')
    if tuple(gate['tree_features_used']) != tuple(sorted(USED_FEATURES)):
        raise ValueError(('P8 used-feature set drift', gate['tree_features_used']))
    return gate


def compare_used_features(p9f, p8f, cid):
    for k in USED_FEATURES:
        a = p9f[k]
        b = p8f[k]
        if a != b:
            raise AssertionError(('P8/P9 feature mismatch', cid, k, a, b))


def _build_p9(build):
    f, root, n = build(MinimalTelemetryFactory)
    return f, root, n, f.features()


def invariant_check():
    gate = load_gate()
    cal = json.loads((P8_DIR / 'calibration.json').read_text())
    gatep = json.loads((P8_DIR / 'gatep.json').read_text())
    combined = json.loads((P8_DIR / 'n2_p8_results.json').read_text())
    issues = []
    checked = {'training': 0, 'validation': 0, 'gatep': 0, 'natural': 0}

    def check(cid, build, ref):
        try:
            f, root, n, feat = _build_p9(build)
            compare_used_features(feat, ref['features'], cid)
            pred = eval_tree_min(gate['tree'], feat)
            refpred = p8.eval_tree(gate['tree'], ref['features'])
            if pred != refpred:
                raise AssertionError(('prediction mismatch', pred, refpred))
            choose = pred <= gate['cutoff']
            refchoose = refpred <= gate['cutoff']
            if choose != refchoose:
                raise AssertionError(('decision mismatch', choose, refchoose))
            if 'annotate' in ref and bool(ref['annotate']) != choose:
                raise AssertionError(('recorded decision mismatch', choose, ref['annotate']))
        except Exception as e:
            issues.append({'case_id': cid, 'error': repr(e)})

    train_refs = {r['case_id']: r for r in cal['training_records']}
    for cid, kind, d, build in p8.training_synthetic_recipes():
        check(cid, build, train_refs[cid]); checked['training'] += 1
    for cid, kind, d, build, oracle, extra in p8.epfl_recipes('train', cal['selection']):
        check(cid, build, train_refs[cid]); checked['training'] += 1

    val_refs = {r['case_id']: r for r in cal['validation_records']}
    for cid, kind, d, build in p8.validation_synthetic_recipes():
        check(cid, build, val_refs[cid]); checked['validation'] += 1
    for cid, kind, d, build, oracle, extra in p8.epfl_recipes('validation', cal['selection']):
        check(cid, build, val_refs[cid]); checked['validation'] += 1

    gp_refs = {r['case_id']: r for r in gatep['symbolic']}
    for cid, d, i, build in p8.gatep_eval_recipes():
        check(cid, build, gp_refs[cid]); checked['gatep'] += 1

    nat_refs = {x['case_id']: x['symbolic'] for x in combined['natural_cases']}
    for cid, circuit, d, build, oracle, c in p8.natural_eval_recipes()[0]:
        check(cid, build, nat_refs[cid]); checked['natural'] += 1

    return {'schema': 'cm-n2-p9-invariance/v1', 'checked': checked, 'total': sum(checked.values()),
            'issues': issues, 'passed': not issues, 'gate_sha256': sha256_file(P8_DIR / 'P8_FROZEN_GATE.json')}


def compile_once(root, backend, oracle, nvars, memory=False):
    return p8.compile_once(root, backend, oracle, nvars, memory)


def p6_stats(root, oracle, nvars):
    return p8.p6_stats(root, oracle, nvars)


def source_arm_once(build, oracle, gate, arm, memory=False):
    if memory:
        tracemalloc.start()
    t0 = time.perf_counter_ns()
    if arm == P9:
        f, root, n = build(MinimalTelemetryFactory)
        feat = f.features()
        pred = eval_tree_min(gate['tree'], feat)
        annotate = pred <= gate['cutoff']
        backend = COMP_P6 if annotate else COMP_DIRECT
    elif arm == P8FULL:
        f, root, n = build(p8.TelemetryFactory)
        feat = f.features()
        pred = p8.eval_tree(gate['tree'], feat)
        annotate = pred <= gate['cutoff']
        backend = COMP_P6 if annotate else COMP_DIRECT
    else:
        f, root, n = build(base.Factory)
        feat = None
        pred = None
        annotate = arm == P6ARM
        backend = COMP_P6 if annotate else COMP_DIRECT
    s1 = time.perf_counter_ns()
    cr = compile_once(root, backend, oracle, n, False)
    t1 = time.perf_counter_ns()
    peak = None
    if memory:
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
    return {
        'arm': arm, 'ok': cr['ok'], 'source_pipeline_ns': t1 - t0, 'source_build_ns': s1 - t0,
        'compiler_ns': cr['pipeline_ns'], 'backend': backend, 'annotate': bool(annotate),
        'predicted_ratio': pred, 'python_peak_bytes': peak, 'digest': cr['digest'],
        'multiplications': cr.get('multiplications'), 'pair_terms': cr.get('pair_terms'),
        'peak_monomials': cr.get('peak_monomials'), 'anf_nodes_evaluated': cr.get('anf_nodes_evaluated'),
        'final_monomials': cr.get('final_monomials'), 'final_degree': cr.get('final_degree'),
        'features': feat,
    }


def fuzz():
    gate = load_gate()
    rng = random.Random(FUZZ_SEED)
    failures = []
    annotated = 0
    for i in range(FUZZ_CASES):
        seed = rng.getrandbits(63)
        nvars = rng.randint(2, 8)
        depth = rng.randint(2, 9)
        def build(Cls, seed=seed, nvars=nvars, depth=depth):
            rr = random.Random(seed)
            f = Cls()
            root = base.random_expr(rr, nvars, depth, f)
            return f, root, nvars
        try:
            pf, pr, n = build(base.Factory)
            ff, fr, _ = build(p8.TelemetryFactory)
            mf, mr, _ = build(MinimalTelemetryFactory)
            p8feat = ff.features(); p9feat = mf.features()
            compare_used_features(p9feat, p8feat, f'fuzz:{i}')
            pred8 = p8.eval_tree(gate['tree'], p8feat); pred9 = eval_tree_min(gate['tree'], p9feat)
            choose8 = pred8 <= gate['cutoff']; choose9 = pred9 <= gate['cutoff']
            if pred8 != pred9 or choose8 != choose9:
                raise AssertionError(('dispatch drift', pred8, pred9, choose8, choose9))
            annotated += int(choose9)
            oracle = base.eval_node_bitset(pr, n)
            dd = compile_once(pr, COMP_DIRECT, oracle, n, False)
            qq = compile_once(pr, COMP_P6, oracle, n, False)
            md = compile_once(mr, COMP_DIRECT, oracle, n, False)
            if not (dd['ok'] and qq['ok'] and md['ok'] and dd['digest'] == qq['digest'] == md['digest']):
                raise AssertionError('digest/oracle')
            selected = qq if choose9 else dd
            for k in ('multiplications', 'pair_terms', 'peak_monomials', 'anf_nodes_evaluated'):
                if selected.get(k) != (qq if choose8 else dd).get(k):
                    raise AssertionError(('selected work', k))
            qs = p6_stats(pr, oracle, n)
            if qs.get('selector_accepted', 0) != qs.get('fold_lowerings', 0):
                raise AssertionError('P6 utilization')
        except Exception as e:
            failures.append({'case': i, 'error': repr(e)})
            if len(failures) >= 20:
                break
    return {'schema': 'cm-n2-p9-fuzz/v1', 'cases': FUZZ_CASES, 'annotated': annotated,
            'failures': failures, 'passed': not failures}


def eval_case(cid, build, oracle, meta, reps, seed, gate):
    mf, mroot, n = build(MinimalTelemetryFactory)
    mfeat = mf.features()
    ff, froot, fn = build(p8.TelemetryFactory)
    ffeat = ff.features()
    compare_used_features(mfeat, ffeat, cid)
    pred9 = eval_tree_min(gate['tree'], mfeat)
    pred8 = p8.eval_tree(gate['tree'], ffeat)
    if pred9 != pred8:
        raise AssertionError(('P8/P9 prediction drift', cid, pred8, pred9))
    annotate = pred9 <= gate['cutoff']

    pf, proot, pn = build(base.Factory)
    if pn != n or fn != n:
        raise AssertionError(('nvars drift', cid))
    direct = compile_once(proot, COMP_DIRECT, oracle, n, True)
    p6r = compile_once(proot, COMP_P6, oracle, n, True)
    selected = p6r if annotate else direct
    if not (direct['ok'] and p6r['ok'] and direct['digest'] == p6r['digest']):
        raise AssertionError(('symbolic', cid))
    qs = p6_stats(proot, oracle, n)
    if qs.get('selector_accepted', 0) != qs.get('fold_lowerings', 0):
        raise AssertionError(('P6 utilization', cid))

    symbolic = {
        'case_id': cid, **meta, 'p9_features': mfeat, 'predicted_ratio': pred9, 'annotate': annotate,
        'backend': COMP_P6 if annotate else COMP_DIRECT,
        'direct': {k: direct.get(k) for k in ('digest','multiplications','pair_terms','peak_monomials','anf_nodes_evaluated','python_peak_bytes')},
        'p6': {k: p6r.get(k) for k in ('digest','multiplications','pair_terms','peak_monomials','anf_nodes_evaluated','python_peak_bytes')},
        'p9': {k: selected.get(k) for k in ('digest','multiplications','pair_terms','peak_monomials','anf_nodes_evaluated','python_peak_bytes')},
        'p6_folds': qs.get('fold_lowerings', 0), 'p6_accepted': qs.get('selector_accepted', 0),
        'p6_accepted_shared': qs.get('selector_accepted_shared', 0),
    }

    rr = random.Random(seed)
    schedule = [a for _ in range(reps) for a in (DIRECT, P6ARM, P8FULL, P9)]
    rr.shuffle(schedule)
    rows = []
    for rep, arm in enumerate(schedule):
        r = source_arm_once(build, oracle, gate, arm, False)
        if not r['ok']:
            raise AssertionError(('timed source', cid, arm))
        if arm in (P8FULL, P9) and bool(r['annotate']) != annotate:
            raise AssertionError(('timed decision drift', cid, arm))
        rows.append({'case_id': cid, **meta, 'rep': rep, **{k: r[k] for k in (
            'arm','source_pipeline_ns','source_build_ns','compiler_ns','backend','annotate','predicted_ratio','ok')}})

    mem = []
    for arm in (DIRECT, P6ARM, P8FULL, P9):
        r = source_arm_once(build, oracle, gate, arm, True)
        if not r['ok']:
            raise AssertionError(('memory', cid, arm))
        mem.append({'case_id': cid, **meta, **r})
    return symbolic, rows, mem


def run_gatep():
    gate = load_gate()
    sym = []; timing = []; mem = []
    frozen = {(d, i): (r, n, o) for d, i, r, n, o in p8.p6.generate_gate_cases()}
    for cid, d, i, build in p8.gatep_eval_recipes():
        pf, pr, n = build(base.Factory)
        oracle = base.eval_node_bitset(pr, n)
        fr, fn, fo = frozen[(d, i)]
        fd = compile_once(fr, COMP_DIRECT, fo, fn, False)
        rd = compile_once(pr, COMP_DIRECT, oracle, n, False)
        if fd['digest'] != rd['digest']:
            raise AssertionError(('Gate-P frozen identity drift', cid))
        s, t, m = eval_case(cid, build, oracle, {'corpus':'gatep','depth':d,'case':i},
                            GATEP_REPS, SEED + d*1000 + i + 0x9900, gate)
        sym.append(s); timing.extend(t); mem.extend(m)
    return {'schema':'cm-n2-p9-gatep/v1','gate_sha256':sha256_file(P8_DIR/'P8_FROZEN_GATE.json'),
            'symbolic':sym,'source_timing_rows':timing,'memory_rows':mem}


def run_natural_case(case_id):
    gate = load_gate()
    recipes, selection, selsha = p8.natural_eval_recipes()
    by = {x[0]: x for x in recipes}
    cid, circuit, depth, build, oracle, c = by[case_id]
    meta = {'corpus':'natural','circuit':circuit,'root':c['root'],'support':c['support'],
            'source_nodes':c['source_nodes'],'depth':depth}
    s, t, m = eval_case(cid, build, oracle, meta, NAT_REPS,
                        SEED ^ int(hashlib.sha256(cid.encode()).hexdigest()[:8], 16) ^ 0x9900, gate)
    return {'schema':'cm-n2-p9-natural-case/v1','case_id':cid,'selection_sha256':selsha,
            'symbolic':s,'source_timing_rows':t,'memory_rows':m}


def medians(rows, metric):
    g = defaultdict(list)
    for r in rows:
        g[(r['case_id'], r['arm'])].append(r[metric])
    return {k: statistics.median(v) for k, v in g.items()}


def compare(rows, metric, num, den, seed=SEED):
    m = medians(rows, metric)
    cases = sorted({r['case_id'] for r in rows})
    ratios = []; wins = 0; an = 0.0; ad = 0.0; per = {}
    for c in cases:
        a = m[(c, num)]; b = m[(c, den)]
        ratios.append(a/b); wins += a < b; an += a; ad += b; per[c] = a/b
    bs = bootstrap_geomean(ratios, 5000, seed)
    return {'cases':len(cases),'geomean_ratio':bs['estimate'],'ci95':bs['ci95'],
            'weighted_ratio':an/ad,'wins':wins,'case_ratios':per}


def work_ratio(symbolic, field):
    vals = []
    for r in symbolic:
        d = r['direct'].get(field); z = r['p9'].get(field)
        if d not in (None, 0):
            vals.append(z/d)
    return {'geomean_ratio':geomean(vals), 'median_ratio':statistics.median(vals) if vals else None}


def summarize(gatep, natural, fuzz, invariant):
    gs = gatep['source_timing_rows']
    gsym = gatep['symbolic']
    ns = []; nsy = []; nmem = []
    for x in natural:
        ns.extend(x['source_timing_rows']); nsy.append(x['symbolic']); nmem.extend(x['memory_rows'])

    def cmps(rows, metric, prefix):
        pairs = (
            ('p9_direct', P9, DIRECT), ('p9_p8', P9, P8FULL), ('p9_p6', P9, P6ARM),
            ('p8_direct', P8FULL, DIRECT), ('p6_direct', P6ARM, DIRECT),
        )
        return {k: compare(rows, metric, a, b, SEED ^ int(hashlib.sha256((prefix+k+metric).encode()).hexdigest()[:8],16))
                for k,a,b in pairs}

    source_cmp = cmps(gs, 'source_pipeline_ns', 'g')
    build_cmp = cmps(gs, 'source_build_ns', 'gb')
    compiler_cmp = cmps(gs, 'compiler_ns', 'gc')
    nat_source = cmps(ns, 'source_pipeline_ns', 'n')
    nat_build = cmps(ns, 'source_build_ns', 'nb')
    nat_compiler = cmps(ns, 'compiler_ns', 'nc')

    gm = medians(gs, 'source_pipeline_ns')
    goodann = badann = p6wins = bypassed = 0
    for r in gsym:
        c = r['case_id']; win = gm[(c,P6ARM)] < gm[(c,DIRECT)]
        p6wins += int(win)
        if r['annotate']:
            goodann += int(win); badann += int(not win)
        elif win:
            bypassed += 1

    work = {f: work_ratio(gsym, f) for f in ('multiplications','pair_terms','peak_monomials','anf_nodes_evaluated')}
    pair = work['pair_terms']['geomean_ratio']; peak = work['peak_monomials']['geomean_ratio']
    primary = source_cmp['p9_direct']
    passflag = (fuzz['passed'] and invariant['passed'] and any(r['annotate'] and r['p6_folds'] > 0 for r in gsym)
                and primary['geomean_ratio'] <= .95 and primary['ci95'][1] < 1.0
                and (pair is None or pair <= 1.05) and (peak is None or peak <= 1.05))
    eng = (invariant['passed'] and build_cmp['p9_p8']['geomean_ratio'] <= .75
           and source_cmp['p9_p8']['geomean_ratio'] <= .98)

    # Memory comparisons use one untimed row per case/arm.
    def memory_compare(memrows, num, den):
        by = {(r['case_id'], r['arm']): r['python_peak_bytes'] for r in memrows}
        cases = sorted({r['case_id'] for r in memrows})
        ratios = [by[(c,num)] / by[(c,den)] for c in cases if by[(c,den)]]
        return {'cases':len(ratios),'geomean_ratio':geomean(ratios),'median_ratio':statistics.median(ratios) if ratios else None}

    return {
        'schema':'cm-n2-p9-summary/v1','fuzz':fuzz,'invariance':invariant,
        'gatep_source':source_cmp,'gatep_source_build':build_cmp,'gatep_compiler':compiler_cmp,
        'gatep_annotated':sum(r['annotate'] for r in gsym),
        'gatep_fold_cases':sum(r['annotate'] and r['p6_folds']>0 for r in gsym),
        'gatep_folds':sum(r['p6_folds'] if r['annotate'] else 0 for r in gsym),
        'gatep_confusion':{'p6_wins':p6wins,'annotated_p6_wins':goodann,'annotated_p6_losses':badann,'p6_wins_bypassed':bypassed},
        'gatep_work':work,
        'gatep_memory':{
            'p9_direct':memory_compare(gatep['memory_rows'],P9,DIRECT),
            'p9_p8':memory_compare(gatep['memory_rows'],P9,P8FULL),
            'p9_p6':memory_compare(gatep['memory_rows'],P9,P6ARM),
        },
        'natural_source':nat_source,'natural_source_build':nat_build,'natural_compiler':nat_compiler,
        'natural_annotated':sum(r['annotate'] for r in nsy),
        'natural_fold_cases':sum(r['annotate'] and r['p6_folds']>0 for r in nsy),
        'natural_memory':{
            'p9_direct':memory_compare(nmem,P9,DIRECT),'p9_p8':memory_compare(nmem,P9,P8FULL)
        },
        'predeclared_gatep_p9_source_inclusive_pass':passflag,
        'predeclared_telemetry_engineering_success':eng,
    }


def main():
    if sha256_file(HERE/'N2_P9_PREREGISTRATION.md') != PREREG_SHA256:
        raise SystemExit('P9 preregistration hash mismatch')
    ap = argparse.ArgumentParser()
    ap.add_argument('--mode', required=True, choices=('invariant','fuzz','gatep','natural-case'))
    ap.add_argument('--case-id')
    ap.add_argument('--out', required=True)
    a = ap.parse_args(); out = Path(a.out)
    if a.mode == 'invariant': obj = invariant_check()
    elif a.mode == 'fuzz': obj = fuzz()
    elif a.mode == 'gatep': obj = run_gatep()
    else:
        if not a.case_id: raise SystemExit('--case-id required')
        obj = run_natural_case(a.case_id)
    out.write_text(json.dumps(obj, indent=2), encoding='utf-8')
    print(json.dumps({'mode':a.mode,'out':str(out),'ok':True,'keys':list(obj)[:8]}, indent=2))

if __name__ == '__main__':
    main()
