from __future__ import annotations
import argparse, hashlib, json, math, random, statistics, sys, time, tracemalloc
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
P11_DIR = ROOT / 'cm_n2_p11_run'
if str(P11_DIR) not in sys.path:
    sys.path.insert(0, str(P11_DIR))
import n2_p11_harness as p11

p10 = p11.p10
p9 = p11.p9
p8 = p11.p8
base = p11.base
SEED = p11.SEED
FUZZ_SEED = SEED ^ 0xB12F
PREREG_SHA256 = '90963ffa72693a066b2bc9441887f586204015c647684c68e7cb9afef7a3b3f7'
FUZZ_CASES = 1000
GATEP_REPS = p11.GATEP_REPS
NAT_REPS = p11.NAT_REPS

DIRECT = p11.DIRECT
P6ARM = p11.P6ARM
P11ARM = p11.P11
P12 = 'p12_lazy_reuse_dispatch'
COMP_DIRECT = p11.COMP_DIRECT
COMP_P6 = p11.COMP_P6

REUSE_NODE = p11.REUSE_NODE
REPEAT_NODE = p11.REPEAT_NODE
ANNOTATE_LEAF = p11.ANNOTATE_LEAF
REPEAT_BYPASS_LEAF = p11.REPEAT_BYPASS_LEAF
REUSE_BYPASS_LEAF = p11.REUSE_BYPASS_LEAF


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def geomean(xs):
    return p11.geomean(xs)


def quantile(xs, p):
    return p11.quantile(xs, p)


def bootstrap_geomean(ratios, n=5000, seed=SEED):
    return p11.bootstrap_geomean(ratios, n, seed)


def _ratio_le_int(num: int, den: int, threshold: float) -> bool:
    return p11._ratio_le_int(num, den, threshold)


class LazyReuseTelemetryFactory(base.Factory):
    """Frozen P11 decision with lazy reuse exactification and derived repeat excess."""
    def __init__(self):
        self.cache = {}
        self.nodes = []
        self.edge_count = 0
        self.binary_nodes = 0
        self.shell_ge5 = False
        self._pair_counts = {}
        # Last-dispatch diagnostics. They are not maintained during construction.
        self._reuse_scanned = False
        self._reuse_scan_edges = 0
        self._reuse_events = None
        self._reuse_early_abort = False

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

        arity = len(args)
        self.edge_count += arity
        if arity == 2 and op in ('and', 'or', 'xor', 'tf'):
            self.binary_nodes += 1
            a, b = ids
            if a > b:
                a, b = b, a
            pkey = (a << 32) | b
            counts = self._pair_counts
            old = counts.get(pkey)
            if old is None:
                counts[pkey] = 1
            elif old < 5:
                new = old + 1
                counts[pkey] = new
                if new == 5:
                    self.shell_ge5 = True
            # Values are deliberately saturated at 5. Membership remains exact.
        return n

    def pair_repeat_excess(self):
        return self.binary_nodes - len(self._pair_counts)

    def counters(self):
        return {
            'edge_count': self.edge_count,
            'binary_nodes': self.binary_nodes,
            'pair_repeat_excess': self.pair_repeat_excess(),
            'shell_ge5': bool(self.shell_ge5),
            'reuse_scanned': bool(self._reuse_scanned),
            'reuse_scan_edges': int(self._reuse_scan_edges),
            'reuse_edge_events': self._reuse_events,
            'reuse_early_abort': bool(self._reuse_early_abort),
        }

    def dispatch(self, gate):
        tree = gate['tree']
        self._reuse_scanned = False
        self._reuse_scan_edges = 0
        self._reuse_events = None
        self._reuse_early_abort = False

        if not self.shell_ge5:
            return False, 'shell_lt5_bypass', None, self.counters()

        repeat_excess = self.pair_repeat_excess()
        repeat_t = float(tree['threshold'][REPEAT_NODE])
        if not _ratio_le_int(repeat_excess, self.binary_nodes, repeat_t):
            return False, 'pair_repeat_density_bypass', math.exp(tree['value'][REPEAT_BYPASS_LEAF]), self.counters()

        # Only cases that survive both cheap predicates pay for exact reuse.
        self._reuse_scanned = True
        used = bytearray(len(self.nodes))
        reuse = 0
        scanned = 0
        reuse_t = float(tree['threshold'][REUSE_NODE])
        tnum, tden = reuse_t.as_integer_ratio()
        allowed_num = self.edge_count * tnum
        for node in self.nodes:
            for child in node.args:
                scanned += 1
                i = child.nid
                if used[i]:
                    reuse += 1
                    # Exact rational comparison, with monotone early failure.
                    if reuse * tden > allowed_num:
                        self._reuse_scan_edges = scanned
                        self._reuse_events = reuse
                        self._reuse_early_abort = True
                        return False, 'reuse_density_early_bypass', math.exp(tree['value'][REUSE_BYPASS_LEAF]), self.counters()
                else:
                    used[i] = 1
        self._reuse_scan_edges = scanned
        self._reuse_events = reuse
        return True, 'annotate_leaf10', math.exp(tree['value'][ANNOTATE_LEAF]), self.counters()


def load_gate():
    return p11.load_gate()


def _compare_p11_p12(f11, f12, cid, gate):
    c11 = f11.counters()
    for k in ('edge_count', 'binary_nodes', 'pair_repeat_excess'):
        v12 = f12.edge_count if k == 'edge_count' else f12.binary_nodes if k == 'binary_nodes' else f12.pair_repeat_excess()
        if c11[k] != v12:
            raise AssertionError(('P11/P12 counter mismatch', cid, k, c11[k], v12))
    if c11['shell_ge5'] != bool(f12.shell_ge5):
        raise AssertionError(('P11/P12 shell mismatch', cid, c11['shell_ge5'], f12.shell_ge5))

    d11, code11, leaf11 = f11.dispatch(gate)
    d12, code12, leaf12, diag12 = f12.dispatch(gate)
    if d11 != d12:
        raise AssertionError(('P11/P12 decision mismatch', cid, d11, d12, code11, code12, c11, diag12))

    # Validate lazy reuse exactification against P11's eager exact count whenever used.
    if diag12['reuse_scanned']:
        threshold = float(gate['tree']['threshold'][REUSE_NODE])
        if diag12['reuse_early_abort']:
            if _ratio_le_int(diag12['reuse_edge_events'], c11['edge_count'], threshold):
                raise AssertionError(('P12 premature reuse abort', cid, diag12, c11))
            if _ratio_le_int(c11['reuse_edge_events'], c11['edge_count'], threshold):
                raise AssertionError(('P11 exact reuse should also bypass', cid, diag12, c11))
        else:
            if diag12['reuse_edge_events'] != c11['reuse_edge_events']:
                raise AssertionError(('P12 reuse exactification mismatch', cid, diag12, c11))
            if not _ratio_le_int(diag12['reuse_edge_events'], c11['edge_count'], threshold):
                raise AssertionError(('completed reuse scan should annotate', cid, diag12, c11))
    return c11, diag12, d11, code11, code12, leaf11, leaf12


def invariant_check():
    gate = load_gate()
    cal = json.loads((p9.P8_DIR / 'calibration.json').read_text())
    gp = json.loads((p9.P8_DIR / 'gatep.json').read_text())
    combined = json.loads((p9.P8_DIR / 'n2_p8_results.json').read_text())
    issues = []
    checked = {'training': 0, 'validation': 0, 'gatep': 0, 'natural': 0}
    reuse_scans = reuse_early = 0

    def check(cid, build, ref):
        nonlocal reuse_scans, reuse_early
        try:
            f11, r11, n11 = build(p11.TreeSpecializedTelemetryFactory)
            f12, r12, n12 = build(LazyReuseTelemetryFactory)
            c11, d12, dec11, code11, code12, leaf11, leaf12 = _compare_p11_p12(f11, f12, cid, gate)
            reuse_scans += int(d12['reuse_scanned'])
            reuse_early += int(d12['reuse_early_abort'])
            refpred = p8.eval_tree(gate['tree'], ref['features'])
            if (refpred <= gate['cutoff']) != dec11:
                raise AssertionError(('reference decision mismatch', cid, refpred, dec11))
            if n11 != n12:
                raise AssertionError(('nvars mismatch', cid, n11, n12))
            oracle11 = base.eval_node_bitset(r11, n11)
            oracle12 = base.eval_node_bitset(r12, n12)
            d11c = p11.compile_once(r11, COMP_DIRECT, oracle11, n11, False)
            d12c = p11.compile_once(r12, COMP_DIRECT, oracle12, n12, False)
            if d11c['digest'] != d12c['digest']:
                raise AssertionError(('source semantic digest mismatch', cid))
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

    gp_refs = {r['case_id']: r for r in gp['symbolic']}
    for cid, d, i, build in p8.gatep_eval_recipes():
        check(cid, build, gp_refs[cid]); checked['gatep'] += 1

    nat_refs = {x['case_id']: x['symbolic'] for x in combined['natural_cases']}
    for cid, circuit, d, build, oracle, c in p8.natural_eval_recipes()[0]:
        check(cid, build, nat_refs[cid]); checked['natural'] += 1

    return {
        'schema': 'cm-n2-p12-invariance/v1', 'checked': checked, 'total': sum(checked.values()),
        'reuse_scans': reuse_scans, 'reuse_early_aborts': reuse_early,
        'issues': issues, 'passed': not issues,
        'gate_sha256': sha256_file(p9.P8_DIR / 'P8_FROZEN_GATE.json')
    }


def compile_once(root, backend, oracle, nvars, memory=False):
    return p11.compile_once(root, backend, oracle, nvars, memory)


def p6_stats(root, oracle, nvars):
    return p11.p6_stats(root, oracle, nvars)


def source_arm_once(build, oracle, gate, arm, memory=False):
    if memory:
        tracemalloc.start()
    t0 = time.perf_counter_ns()
    decision_code = None
    dispatch_diag = None
    if arm == P12:
        f, root, n = build(LazyReuseTelemetryFactory)
        annotate, decision_code, leaf_ratio, dispatch_diag = f.dispatch(gate)
        feat = f.counters(); pred = leaf_ratio
        backend = COMP_P6 if annotate else COMP_DIRECT
    elif arm == P11ARM:
        f, root, n = build(p11.TreeSpecializedTelemetryFactory)
        annotate, decision_code, leaf_ratio = f.dispatch(gate)
        feat = f.counters(); pred = leaf_ratio
        backend = COMP_P6 if annotate else COMP_DIRECT
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
        'arm': arm, 'ok': cr['ok'], 'source_pipeline_ns': t1 - t0, 'source_build_ns': s1 - t0,
        'compiler_ns': cr['pipeline_ns'], 'backend': backend, 'annotate': bool(annotate),
        'predicted_ratio': pred, 'decision_code': decision_code, 'dispatch_diag': dispatch_diag,
        'python_peak_bytes': peak, 'digest': cr['digest'],
        'multiplications': cr.get('multiplications'), 'pair_terms': cr.get('pair_terms'),
        'peak_monomials': cr.get('peak_monomials'), 'anf_nodes_evaluated': cr.get('anf_nodes_evaluated'),
        'final_monomials': cr.get('final_monomials'), 'final_degree': cr.get('final_degree'), 'features': feat,
    }


def fuzz():
    gate = load_gate(); rng = random.Random(FUZZ_SEED); failures = []; annotated = 0; reuse_scans = reuse_early = 0
    for i in range(FUZZ_CASES):
        seed = rng.getrandbits(63); nvars = rng.randint(2, 8); depth = rng.randint(2, 9)
        def build(Cls, seed=seed, nvars=nvars, depth=depth):
            rr = random.Random(seed); f = Cls(); root = base.random_expr(rr, nvars, depth, f); return f, root, nvars
        try:
            pf, pr, n = build(base.Factory)
            f11, r11, n11 = build(p11.TreeSpecializedTelemetryFactory)
            f12, r12, n12 = build(LazyReuseTelemetryFactory)
            c11, d12, choose, code11, code12, leaf11, leaf12 = _compare_p11_p12(f11, f12, f'fuzz:{i}', gate)
            annotated += int(choose); reuse_scans += int(d12['reuse_scanned']); reuse_early += int(d12['reuse_early_abort'])
            oracle = base.eval_node_bitset(pr, n)
            dd = compile_once(pr, COMP_DIRECT, oracle, n, False)
            qq = compile_once(pr, COMP_P6, oracle, n, False)
            d11c = compile_once(r11, COMP_DIRECT, oracle, n11, False)
            d12c = compile_once(r12, COMP_DIRECT, oracle, n12, False)
            if not (dd['ok'] and qq['ok'] and d11c['ok'] and d12c['ok'] and dd['digest'] == qq['digest'] == d11c['digest'] == d12c['digest']):
                raise AssertionError('digest/oracle')
            selected = qq if choose else dd
            for k in ('multiplications', 'pair_terms', 'peak_monomials', 'anf_nodes_evaluated'):
                if selected.get(k) != (qq if choose else dd).get(k):
                    raise AssertionError(('selected work', k))
            qs = p6_stats(pr, oracle, n)
            if qs.get('selector_accepted', 0) != qs.get('fold_lowerings', 0):
                raise AssertionError('P6 utilization')
        except Exception as e:
            failures.append({'case': i, 'error': repr(e)})
            if len(failures) >= 20:
                break
    return {
        'schema': 'cm-n2-p12-fuzz/v1', 'cases': FUZZ_CASES, 'annotated': annotated,
        'reuse_scans': reuse_scans, 'reuse_early_aborts': reuse_early,
        'failures': failures, 'passed': not failures
    }


def eval_case(cid, build, oracle, meta, reps, seed, gate):
    f11, r11, n11 = build(p11.TreeSpecializedTelemetryFactory)
    f12, r12, n12 = build(LazyReuseTelemetryFactory)
    c11, d12, annotate, code11, code12, leaf11, leaf12 = _compare_p11_p12(f11, f12, cid, gate)

    pf, proot, n = build(base.Factory)
    if n != n11 or n != n12:
        raise AssertionError(('nvars drift', cid, n, n11, n12))
    direct = compile_once(proot, COMP_DIRECT, oracle, n, True)
    p6r = compile_once(proot, COMP_P6, oracle, n, True)
    selected = p6r if annotate else direct
    if not (direct['ok'] and p6r['ok'] and direct['digest'] == p6r['digest']):
        raise AssertionError(('symbolic', cid))
    qs = p6_stats(proot, oracle, n)
    if qs.get('selector_accepted', 0) != qs.get('fold_lowerings', 0):
        raise AssertionError(('P6 utilization', cid))
    symbolic = {
        'case_id': cid, **meta, 'p11_counters': c11, 'p12_dispatch': d12,
        'p11_decision_code': code11, 'p12_decision_code': code12,
        'annotate': annotate, 'backend': COMP_P6 if annotate else COMP_DIRECT,
        'direct': {k: direct.get(k) for k in ('digest', 'multiplications', 'pair_terms', 'peak_monomials', 'anf_nodes_evaluated', 'python_peak_bytes')},
        'p6': {k: p6r.get(k) for k in ('digest', 'multiplications', 'pair_terms', 'peak_monomials', 'anf_nodes_evaluated', 'python_peak_bytes')},
        'p12': {k: selected.get(k) for k in ('digest', 'multiplications', 'pair_terms', 'peak_monomials', 'anf_nodes_evaluated', 'python_peak_bytes')},
        'p6_folds': qs.get('fold_lowerings', 0), 'p6_accepted': qs.get('selector_accepted', 0),
        'p6_accepted_shared': qs.get('selector_accepted_shared', 0),
    }
    rr = random.Random(seed)
    schedule = [a for _ in range(reps) for a in (DIRECT, P6ARM, P11ARM, P12)]
    rr.shuffle(schedule)
    rows = []
    for rep, arm in enumerate(schedule):
        r = source_arm_once(build, oracle, gate, arm, False)
        if not r['ok']:
            raise AssertionError(('timed source', cid, arm))
        if arm in (P11ARM, P12) and bool(r['annotate']) != annotate:
            raise AssertionError(('timed decision drift', cid, arm))
        rows.append({'case_id': cid, **meta, 'rep': rep, **{k: r[k] for k in (
            'arm', 'source_pipeline_ns', 'source_build_ns', 'compiler_ns', 'backend', 'annotate',
            'predicted_ratio', 'decision_code', 'dispatch_diag', 'ok')}})
    mem = []
    for arm in (DIRECT, P6ARM, P11ARM, P12):
        r = source_arm_once(build, oracle, gate, arm, True)
        if not r['ok']:
            raise AssertionError(('memory', cid, arm))
        mem.append({'case_id': cid, **meta, **r})
    return symbolic, rows, mem


def run_gatep():
    gate = load_gate(); sym = []; timing = []; mem = []
    frozen = {(d, i): (r, n, o) for d, i, r, n, o in p8.p6.generate_gate_cases()}
    for cid, d, i, build in p8.gatep_eval_recipes():
        pf, pr, n = build(base.Factory); oracle = base.eval_node_bitset(pr, n)
        fr, fn, fo = frozen[(d, i)]
        fd = compile_once(fr, COMP_DIRECT, fo, fn, False); rd = compile_once(pr, COMP_DIRECT, oracle, n, False)
        if fd['digest'] != rd['digest']:
            raise AssertionError(('Gate-P frozen identity drift', cid))
        s, t, m = eval_case(cid, build, oracle, {'corpus': 'gatep', 'depth': d, 'case': i},
                            GATEP_REPS, SEED + d * 1000 + i + 0xB120, gate)
        sym.append(s); timing.extend(t); mem.extend(m)
    return {'schema': 'cm-n2-p12-gatep/v1', 'gate_sha256': sha256_file(p9.P8_DIR / 'P8_FROZEN_GATE.json'),
            'symbolic': sym, 'source_timing_rows': timing, 'memory_rows': mem}


def run_natural_case(case_id):
    gate = load_gate(); recipes, selection, selsha = p8.natural_eval_recipes(); by = {x[0]: x for x in recipes}
    cid, circuit, depth, build, oracle, c = by[case_id]
    meta = {'corpus': 'natural', 'circuit': circuit, 'root': c['root'], 'support': c['support'],
            'source_nodes': c['source_nodes'], 'depth': depth}
    s, t, m = eval_case(cid, build, oracle, meta, NAT_REPS,
                        SEED ^ int(hashlib.sha256(cid.encode()).hexdigest()[:8], 16) ^ 0xB120, gate)
    return {'schema': 'cm-n2-p12-natural-case/v1', 'case_id': cid, 'selection_sha256': selsha,
            'symbolic': s, 'source_timing_rows': t, 'memory_rows': m}


def medians(rows, metric):
    g = defaultdict(list)
    for r in rows:
        g[(r['case_id'], r['arm'])].append(r[metric])
    return {k: statistics.median(v) for k, v in g.items()}


def compare(rows, metric, num, den, seed=SEED):
    m = medians(rows, metric); cases = sorted({r['case_id'] for r in rows}); ratios = []; wins = 0; an = ad = 0.0; per = {}
    for c in cases:
        a = m[(c, num)]; b = m[(c, den)]; ratios.append(a / b); wins += a < b; an += a; ad += b; per[c] = a / b
    bs = bootstrap_geomean(ratios, 5000, seed)
    return {'cases': len(cases), 'geomean_ratio': bs['estimate'], 'ci95': bs['ci95'],
            'weighted_ratio': an / ad, 'wins': wins, 'case_ratios': per}


def work_ratio(symbolic, field):
    vals = []
    for r in symbolic:
        d = r['direct'].get(field); z = r['p12'].get(field)
        if d not in (None, 0):
            vals.append(z / d)
    return {'geomean_ratio': geomean(vals), 'median_ratio': statistics.median(vals) if vals else None}


def summarize(gatep, natural, fuzz, invariant):
    gs = gatep['source_timing_rows']; gsym = gatep['symbolic']; ns = []; nsy = []; nmem = []
    for x in natural:
        ns.extend(x['source_timing_rows']); nsy.append(x['symbolic']); nmem.extend(x['memory_rows'])

    def cmps(rows, metric, prefix):
        pairs = (
            ('p12_direct', P12, DIRECT), ('p12_p11', P12, P11ARM), ('p12_p6', P12, P6ARM),
            ('p11_direct', P11ARM, DIRECT), ('p6_direct', P6ARM, DIRECT)
        )
        return {k: compare(rows, metric, a, b,
                           SEED ^ int(hashlib.sha256((prefix + k + metric).encode()).hexdigest()[:8], 16))
                for k, a, b in pairs}

    source = cmps(gs, 'source_pipeline_ns', 'g'); build = cmps(gs, 'source_build_ns', 'gb'); compiler = cmps(gs, 'compiler_ns', 'gc')
    nsource = cmps(ns, 'source_pipeline_ns', 'n'); nbuild = cmps(ns, 'source_build_ns', 'nb'); ncompiler = cmps(ns, 'compiler_ns', 'nc')
    work = {f: work_ratio(gsym, f) for f in ('multiplications', 'pair_terms', 'peak_monomials', 'anf_nodes_evaluated')}
    primary = source['p12_direct']; pair = work['pair_terms']['geomean_ratio']; peak = work['peak_monomials']['geomean_ratio']
    passflag = (fuzz['passed'] and invariant['passed'] and any(r['annotate'] and r['p6_folds'] > 0 for r in gsym)
                and primary['geomean_ratio'] <= .95 and primary['ci95'][1] < 1.0
                and (pair is None or pair <= 1.05) and (peak is None or peak <= 1.05))
    eng = (invariant['passed'] and build['p12_p11']['geomean_ratio'] <= .90
           and source['p12_p11']['geomean_ratio'] <= .98 and source['p12_p11']['ci95'][1] < 1.0)

    def memory_compare(memrows, num, den):
        by = {(r['case_id'], r['arm']): r['python_peak_bytes'] for r in memrows}; cases = sorted({r['case_id'] for r in memrows})
        ratios = [by[(c, num)] / by[(c, den)] for c in cases if by[(c, den)]]
        return {'cases': len(ratios), 'geomean_ratio': geomean(ratios),
                'median_ratio': statistics.median(ratios) if ratios else None}

    gm = medians(gs, 'source_pipeline_ns'); good = bad = miss = p6wins = 0
    for r in gsym:
        c = r['case_id']; win = gm[(c, P6ARM)] < gm[(c, DIRECT)]; p6wins += int(win)
        if r['annotate']:
            good += int(win); bad += int(not win)
        elif win:
            miss += 1

    def lazy_stats(symbolic):
        scans = [r['p12_dispatch'] for r in symbolic if r['p12_dispatch']['reuse_scanned']]
        total_edges = sum(r['p11_counters']['edge_count'] for r in symbolic)
        scanned_edges = sum(x['reuse_scan_edges'] for x in scans)
        eligible_edges = sum(r['p11_counters']['edge_count'] for r in symbolic if r['p12_dispatch']['reuse_scanned'])
        return {
            'cases': len(symbolic), 'reuse_scan_cases': len(scans),
            'reuse_early_abort_cases': sum(x['reuse_early_abort'] for x in scans),
            'reuse_scan_edges': scanned_edges,
            'reuse_scan_fraction_all_source_edges': scanned_edges / total_edges if total_edges else 0.0,
            'reuse_scan_fraction_eligible_edges': scanned_edges / eligible_edges if eligible_edges else 0.0,
        }

    return {
        'schema': 'cm-n2-p12-summary/v1', 'fuzz': fuzz, 'invariance': invariant,
        'gatep_source': source, 'gatep_source_build': build, 'gatep_compiler': compiler,
        'gatep_annotated': sum(r['annotate'] for r in gsym),
        'gatep_fold_cases': sum(r['annotate'] and r['p6_folds'] > 0 for r in gsym),
        'gatep_folds': sum(r['p6_folds'] if r['annotate'] else 0 for r in gsym),
        'gatep_confusion': {'p6_wins': p6wins, 'annotated_p6_wins': good, 'annotated_p6_losses': bad, 'p6_wins_bypassed': miss},
        'gatep_lazy': lazy_stats(gsym), 'gatep_work': work,
        'gatep_memory': {
            'p12_direct': memory_compare(gatep['memory_rows'], P12, DIRECT),
            'p12_p11': memory_compare(gatep['memory_rows'], P12, P11ARM),
            'p12_p6': memory_compare(gatep['memory_rows'], P12, P6ARM),
        },
        'natural_source': nsource, 'natural_source_build': nbuild, 'natural_compiler': ncompiler,
        'natural_annotated': sum(r['annotate'] for r in nsy),
        'natural_fold_cases': sum(r['annotate'] and r['p6_folds'] > 0 for r in nsy),
        'natural_lazy': lazy_stats(nsy),
        'natural_memory': {
            'p12_direct': memory_compare(nmem, P12, DIRECT),
            'p12_p11': memory_compare(nmem, P12, P11ARM),
        },
        'predeclared_gatep_direct_crossover_pass': passflag,
        'predeclared_lazy_statistics_engineering_success': eng,
    }


def main():
    if sha256_file(HERE / 'N2_P12_PREREGISTRATION.md') != PREREG_SHA256:
        raise SystemExit('P12 preregistration hash mismatch')
    ap = argparse.ArgumentParser()
    ap.add_argument('--mode', required=True, choices=('invariant', 'fuzz', 'gatep', 'natural-case'))
    ap.add_argument('--case-id'); ap.add_argument('--out', required=True)
    a = ap.parse_args(); out = Path(a.out)
    if a.mode == 'invariant':
        obj = invariant_check()
    elif a.mode == 'fuzz':
        obj = fuzz()
    elif a.mode == 'gatep':
        obj = run_gatep()
    else:
        if not a.case_id:
            raise SystemExit('--case-id required')
        obj = run_natural_case(a.case_id)
    out.write_text(json.dumps(obj, indent=2), encoding='utf-8')
    print(json.dumps({'mode': a.mode, 'out': str(out), 'ok': True, 'keys': list(obj)[:8]}, indent=2))


if __name__ == '__main__':
    main()
