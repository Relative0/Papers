from __future__ import annotations
import argparse, hashlib, json, math, random, statistics, sys, time, tracemalloc
from collections import defaultdict
from pathlib import Path
from _collections import _count_elements

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
P12_DIR = ROOT / 'cm_n2_p12_run'
if str(P12_DIR) not in sys.path:
    sys.path.insert(0, str(P12_DIR))
import n2_p12_harness as p12

p11 = p12.p11
p10 = p12.p10
p9 = p12.p9
p8 = p12.p8
base = p12.base
SEED = p12.SEED
FUZZ_SEED = SEED ^ 0xB13F
PREREG_SHA256 = '28cd2f282764cd34d2c9c3bc2c9beca283fb34bf5d8f3900789f58a87eaf922a'
FUZZ_CASES = 1000
GATEP_REPS = p12.GATEP_REPS
NAT_REPS = p12.NAT_REPS

DIRECT = p12.DIRECT
P6ARM = p12.P6ARM
P12ARM = p12.P12
P13 = 'p13_deferred_pair_dispatch'
COMP_DIRECT = p12.COMP_DIRECT
COMP_P6 = p12.COMP_P6

REUSE_NODE = p12.REUSE_NODE
REPEAT_NODE = p12.REPEAT_NODE
ANNOTATE_LEAF = p12.ANNOTATE_LEAF
REPEAT_BYPASS_LEAF = p12.REPEAT_BYPASS_LEAF
REUSE_BYPASS_LEAF = p12.REUSE_BYPASS_LEAF


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def geomean(xs):
    return p12.geomean(xs)


def bootstrap_geomean(ratios, n=5000, seed=SEED):
    return p12.bootstrap_geomean(ratios, n, seed)


def _ratio_le_int(num: int, den: int, threshold: float) -> bool:
    return p12._ratio_le_int(num, den, threshold)


class DeferredPairTelemetryFactory(base.Factory):
    """Frozen P12 decision with pair statistics deferred to C-backed dispatch work."""
    def __init__(self):
        self.cache = {}
        self.nodes = []
        self.edge_count = 0
        self.binary_nodes = 0
        self._pair_keys = []
        # Last-dispatch diagnostics only. No pair-count dictionary is maintained while building.
        self._distinct_pairs = None
        self._repeat_excess = None
        self._pair_exactified = False
        self._shell_exact = None
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
            self._pair_keys.append((a << 32) | b)
        return n

    def _verification_pair_stats(self):
        """Untimed verification helper; exact values, independent of dispatch shortcuts."""
        keys = self._pair_keys
        distinct = len(set(keys))
        repeat = self.binary_nodes - distinct
        if self.binary_nodes < 5 or repeat < 4:
            shell = False
        else:
            counts = {}
            _count_elements(counts, keys)
            shell = any(v >= 5 for v in counts.values())
        return repeat, shell, distinct

    def counters(self):
        return {
            'edge_count': self.edge_count,
            'binary_nodes': self.binary_nodes,
            'pair_repeat_excess': self._repeat_excess,
            'distinct_pairs': self._distinct_pairs,
            'pair_exactified': bool(self._pair_exactified),
            'shell_ge5': self._shell_exact,
            'reuse_scanned': bool(self._reuse_scanned),
            'reuse_scan_edges': int(self._reuse_scan_edges),
            'reuse_edge_events': self._reuse_events,
            'reuse_early_abort': bool(self._reuse_early_abort),
        }

    def dispatch(self, gate):
        tree = gate['tree']
        self._distinct_pairs = None
        self._repeat_excess = None
        self._pair_exactified = False
        self._shell_exact = None
        self._reuse_scanned = False
        self._reuse_scan_edges = 0
        self._reuse_events = None
        self._reuse_early_abort = False

        # Cardinality alone proves a five-shell impossible.
        if self.binary_nodes < 5:
            self._shell_exact = False
            return False, 'binary_lt5_bypass', None, self.counters()

        # Exact distinct/repeat statistic; set construction executes its inner loop in C.
        distinct = len(set(self._pair_keys))
        repeat_excess = self.binary_nodes - distinct
        self._distinct_pairs = distinct
        self._repeat_excess = repeat_excess

        repeat_t = float(tree['threshold'][REPEAT_NODE])
        if not _ratio_le_int(repeat_excess, self.binary_nodes, repeat_t):
            # The annotate leaf is conjunctive, so shell multiplicity need not be known.
            return False, 'pair_repeat_density_bypass', math.exp(tree['value'][REPEAT_BYPASS_LEAF]), self.counters()

        # A fivefold occurrence contributes at least four repeat-excess events.
        if repeat_excess < 4:
            self._shell_exact = False
            return False, 'repeat_lt4_shell_bypass', None, self.counters()

        # Only repeat-density-eligible cases pay for exact multiplicity counting.
        counts = {}
        _count_elements(counts, self._pair_keys)
        self._pair_exactified = True
        shell = any(v >= 5 for v in counts.values())
        self._shell_exact = bool(shell)
        if not shell:
            return False, 'shell_lt5_exact_bypass', None, self.counters()

        # Frozen P12 lazy reuse exactification.
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
    return p12.load_gate()


def _compare_p12_p13(f12, f13, cid, gate):
    # Exact P12 reference decision and counters.
    d12, code12, leaf12, diag12 = f12.dispatch(gate)
    c12_repeat = f12.pair_repeat_excess()
    exact_repeat13, exact_shell13, exact_distinct13 = f13._verification_pair_stats()
    if f12.edge_count != f13.edge_count or f12.binary_nodes != f13.binary_nodes:
        raise AssertionError(('P12/P13 basic counter mismatch', cid, f12.edge_count, f13.edge_count, f12.binary_nodes, f13.binary_nodes))
    if c12_repeat != exact_repeat13:
        raise AssertionError(('P12/P13 repeat mismatch', cid, c12_repeat, exact_repeat13))
    if bool(f12.shell_ge5) != exact_shell13:
        raise AssertionError(('P12/P13 exact shell mismatch', cid, f12.shell_ge5, exact_shell13))

    d13, code13, leaf13, diag13 = f13.dispatch(gate)
    if d12 != d13:
        raise AssertionError(('P12/P13 decision mismatch', cid, d12, d13, code12, code13, diag12, diag13))

    # Whenever P13 materializes repeat statistics, they must be exact.
    if diag13['pair_repeat_excess'] is not None and diag13['pair_repeat_excess'] != exact_repeat13:
        raise AssertionError(('P13 dispatch repeat mismatch', cid, diag13, exact_repeat13))
    if diag13['distinct_pairs'] is not None and diag13['distinct_pairs'] != exact_distinct13:
        raise AssertionError(('P13 distinct mismatch', cid, diag13, exact_distinct13))
    if diag13['pair_exactified'] and diag13['shell_ge5'] != exact_shell13:
        raise AssertionError(('P13 exactified shell mismatch', cid, diag13, exact_shell13))
    if code13 == 'binary_lt5_bypass' and exact_shell13:
        raise AssertionError(('P13 binary shortcut invalid', cid))
    if code13 == 'repeat_lt4_shell_bypass' and exact_shell13:
        raise AssertionError(('P13 repeat shortcut invalid', cid, exact_repeat13))
    if code13 == 'pair_repeat_density_bypass':
        threshold = float(gate['tree']['threshold'][REPEAT_NODE])
        if _ratio_le_int(exact_repeat13, f13.binary_nodes, threshold):
            raise AssertionError(('P13 premature repeat-density bypass', cid, exact_repeat13, f13.binary_nodes))

    # Eligible reuse behavior should be the same frozen P12 scan.
    if diag13['reuse_scanned'] != diag12['reuse_scanned']:
        raise AssertionError(('P12/P13 reuse eligibility mismatch', cid, diag12, diag13))
    if diag13['reuse_scanned']:
        if diag13['reuse_early_abort'] != diag12['reuse_early_abort']:
            raise AssertionError(('P12/P13 reuse abort mismatch', cid, diag12, diag13))
        if diag13['reuse_scan_edges'] != diag12['reuse_scan_edges'] or diag13['reuse_edge_events'] != diag12['reuse_edge_events']:
            raise AssertionError(('P12/P13 reuse scan mismatch', cid, diag12, diag13))
    return diag12, diag13, d12, code12, code13, leaf12, leaf13


def invariant_check():
    gate = load_gate()
    cal = json.loads((p9.P8_DIR / 'calibration.json').read_text())
    gp = json.loads((p9.P8_DIR / 'gatep.json').read_text())
    combined = json.loads((p9.P8_DIR / 'n2_p8_results.json').read_text())
    issues = []
    checked = {'training': 0, 'validation': 0, 'gatep': 0, 'natural': 0}
    pair_exact = reuse_scans = reuse_early = 0

    def check(cid, build, ref):
        nonlocal pair_exact, reuse_scans, reuse_early
        try:
            f12, r12, n12 = build(p12.LazyReuseTelemetryFactory)
            f13, r13, n13 = build(DeferredPairTelemetryFactory)
            d12diag, d13diag, dec12, code12, code13, leaf12, leaf13 = _compare_p12_p13(f12, f13, cid, gate)
            pair_exact += int(d13diag['pair_exactified'])
            reuse_scans += int(d13diag['reuse_scanned'])
            reuse_early += int(d13diag['reuse_early_abort'])
            refpred = p8.eval_tree(gate['tree'], ref['features'])
            if (refpred <= gate['cutoff']) != dec12:
                raise AssertionError(('reference decision mismatch', cid, refpred, dec12))
            if n12 != n13:
                raise AssertionError(('nvars mismatch', cid, n12, n13))
            oracle12 = base.eval_node_bitset(r12, n12)
            oracle13 = base.eval_node_bitset(r13, n13)
            c12 = p12.compile_once(r12, COMP_DIRECT, oracle12, n12, False)
            c13 = p12.compile_once(r13, COMP_DIRECT, oracle13, n13, False)
            if c12['digest'] != c13['digest']:
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
        'schema': 'cm-n2-p13-invariance/v1', 'checked': checked, 'total': sum(checked.values()),
        'pair_exactification_cases': pair_exact, 'reuse_scans': reuse_scans, 'reuse_early_aborts': reuse_early,
        'issues': issues, 'passed': not issues,
        'gate_sha256': sha256_file(p9.P8_DIR / 'P8_FROZEN_GATE.json')
    }


def compile_once(root, backend, oracle, nvars, memory=False):
    return p12.compile_once(root, backend, oracle, nvars, memory)


def p6_stats(root, oracle, nvars):
    return p12.p6_stats(root, oracle, nvars)


def source_arm_once(build, oracle, gate, arm, memory=False):
    if memory:
        tracemalloc.start()
    t0 = time.perf_counter_ns()
    decision_code = None
    dispatch_diag = None
    if arm == P13:
        f, root, n = build(DeferredPairTelemetryFactory)
        annotate, decision_code, leaf_ratio, dispatch_diag = f.dispatch(gate)
        feat = f.counters(); pred = leaf_ratio
        backend = COMP_P6 if annotate else COMP_DIRECT
    elif arm == P12ARM:
        f, root, n = build(p12.LazyReuseTelemetryFactory)
        annotate, decision_code, leaf_ratio, dispatch_diag = f.dispatch(gate)
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
    gate = load_gate(); rng = random.Random(FUZZ_SEED); failures = []; annotated = 0; pair_exact = reuse_scans = reuse_early = 0
    for i in range(FUZZ_CASES):
        seed = rng.getrandbits(63); nvars = rng.randint(2, 8); depth = rng.randint(2, 9)
        def build(Cls, seed=seed, nvars=nvars, depth=depth):
            rr = random.Random(seed); f = Cls(); root = base.random_expr(rr, nvars, depth, f); return f, root, nvars
        try:
            pf, pr, n = build(base.Factory)
            f12, r12, n12 = build(p12.LazyReuseTelemetryFactory)
            f13, r13, n13 = build(DeferredPairTelemetryFactory)
            d12diag, d13diag, choose, code12, code13, leaf12, leaf13 = _compare_p12_p13(f12, f13, f'fuzz:{i}', gate)
            annotated += int(choose); pair_exact += int(d13diag['pair_exactified']); reuse_scans += int(d13diag['reuse_scanned']); reuse_early += int(d13diag['reuse_early_abort'])
            oracle = base.eval_node_bitset(pr, n)
            dd = compile_once(pr, COMP_DIRECT, oracle, n, False)
            qq = compile_once(pr, COMP_P6, oracle, n, False)
            d12c = compile_once(r12, COMP_DIRECT, oracle, n12, False)
            d13c = compile_once(r13, COMP_DIRECT, oracle, n13, False)
            if not (dd['ok'] and qq['ok'] and d12c['ok'] and d13c['ok'] and dd['digest'] == qq['digest'] == d12c['digest'] == d13c['digest']):
                raise AssertionError('digest/oracle')
            qs = p6_stats(pr, oracle, n)
            if qs.get('selector_accepted', 0) != qs.get('fold_lowerings', 0):
                raise AssertionError('P6 utilization')
        except Exception as e:
            failures.append({'case': i, 'error': repr(e)})
            if len(failures) >= 20:
                break
    return {
        'schema': 'cm-n2-p13-fuzz/v1', 'cases': FUZZ_CASES, 'annotated': annotated,
        'pair_exactification_cases': pair_exact, 'reuse_scans': reuse_scans, 'reuse_early_aborts': reuse_early,
        'failures': failures, 'passed': not failures
    }


def eval_case(cid, build, oracle, meta, reps, seed, gate):
    f12, r12, n12 = build(p12.LazyReuseTelemetryFactory)
    f13, r13, n13 = build(DeferredPairTelemetryFactory)
    d12diag, d13diag, annotate, code12, code13, leaf12, leaf13 = _compare_p12_p13(f12, f13, cid, gate)

    pf, proot, n = build(base.Factory)
    if n != n12 or n != n13:
        raise AssertionError(('nvars drift', cid, n, n12, n13))
    direct = compile_once(proot, COMP_DIRECT, oracle, n, True)
    p6r = compile_once(proot, COMP_P6, oracle, n, True)
    selected = p6r if annotate else direct
    if not (direct['ok'] and p6r['ok'] and direct['digest'] == p6r['digest']):
        raise AssertionError(('symbolic', cid))
    qs = p6_stats(proot, oracle, n)
    if qs.get('selector_accepted', 0) != qs.get('fold_lowerings', 0):
        raise AssertionError(('P6 utilization', cid))
    symbolic = {
        'case_id': cid, **meta, 'p12_dispatch': d12diag, 'p13_dispatch': d13diag,
        'p12_decision_code': code12, 'p13_decision_code': code13,
        'annotate': annotate, 'backend': COMP_P6 if annotate else COMP_DIRECT,
        'direct': {k: direct.get(k) for k in ('digest', 'multiplications', 'pair_terms', 'peak_monomials', 'anf_nodes_evaluated', 'python_peak_bytes')},
        'p6': {k: p6r.get(k) for k in ('digest', 'multiplications', 'pair_terms', 'peak_monomials', 'anf_nodes_evaluated', 'python_peak_bytes')},
        'p13': {k: selected.get(k) for k in ('digest', 'multiplications', 'pair_terms', 'peak_monomials', 'anf_nodes_evaluated', 'python_peak_bytes')},
        'p6_folds': qs.get('fold_lowerings', 0), 'p6_accepted': qs.get('selector_accepted', 0),
        'p6_accepted_shared': qs.get('selector_accepted_shared', 0),
    }
    rr = random.Random(seed)
    schedule = [a for _ in range(reps) for a in (DIRECT, P6ARM, P12ARM, P13)]
    rr.shuffle(schedule)
    rows = []
    for rep, arm in enumerate(schedule):
        r = source_arm_once(build, oracle, gate, arm, False)
        if not r['ok']:
            raise AssertionError(('timed source', cid, arm))
        if arm in (P12ARM, P13) and bool(r['annotate']) != annotate:
            raise AssertionError(('timed decision drift', cid, arm))
        rows.append({'case_id': cid, **meta, 'rep': rep, **{k: r[k] for k in (
            'arm', 'source_pipeline_ns', 'source_build_ns', 'compiler_ns', 'backend', 'annotate',
            'predicted_ratio', 'decision_code', 'dispatch_diag', 'ok')}})
    mem = []
    for arm in (DIRECT, P6ARM, P12ARM, P13):
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
                            GATEP_REPS, SEED + d * 1000 + i + 0xB130, gate)
        sym.append(s); timing.extend(t); mem.extend(m)
    return {'schema': 'cm-n2-p13-gatep/v1', 'gate_sha256': sha256_file(p9.P8_DIR / 'P8_FROZEN_GATE.json'),
            'symbolic': sym, 'source_timing_rows': timing, 'memory_rows': mem}


def run_natural_case(case_id):
    gate = load_gate(); recipes, selection, selsha = p8.natural_eval_recipes(); by = {x[0]: x for x in recipes}
    cid, circuit, depth, build, oracle, c = by[case_id]
    meta = {'corpus': 'natural', 'circuit': circuit, 'root': c['root'], 'support': c['support'],
            'source_nodes': c['source_nodes'], 'depth': depth}
    s, t, m = eval_case(cid, build, oracle, meta, NAT_REPS,
                        SEED ^ int(hashlib.sha256(cid.encode()).hexdigest()[:8], 16) ^ 0xB130, gate)
    return {'schema': 'cm-n2-p13-natural-case/v1', 'case_id': cid, 'selection_sha256': selsha,
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
        d = r['direct'].get(field); z = r['p13'].get(field)
        if d not in (None, 0):
            vals.append(z / d)
    return {'geomean_ratio': geomean(vals), 'median_ratio': statistics.median(vals) if vals else None}


def summarize(gatep, natural, fuzz, invariant):
    gs = gatep['source_timing_rows']; gsym = gatep['symbolic']; ns = []; nsy = []; nmem = []
    for x in natural:
        ns.extend(x['source_timing_rows']); nsy.append(x['symbolic']); nmem.extend(x['memory_rows'])

    def cmps(rows, metric, prefix):
        pairs = (
            ('p13_direct', P13, DIRECT), ('p13_p12', P13, P12ARM), ('p13_p6', P13, P6ARM),
            ('p12_direct', P12ARM, DIRECT), ('p6_direct', P6ARM, DIRECT)
        )
        return {k: compare(rows, metric, a, b,
                           SEED ^ int(hashlib.sha256((prefix + k + metric).encode()).hexdigest()[:8], 16))
                for k, a, b in pairs}

    source = cmps(gs, 'source_pipeline_ns', 'g'); build = cmps(gs, 'source_build_ns', 'gb'); compiler = cmps(gs, 'compiler_ns', 'gc')
    nsource = cmps(ns, 'source_pipeline_ns', 'n'); nbuild = cmps(ns, 'source_build_ns', 'nb'); ncompiler = cmps(ns, 'compiler_ns', 'nc')
    work = {f: work_ratio(gsym, f) for f in ('multiplications', 'pair_terms', 'peak_monomials', 'anf_nodes_evaluated')}
    primary = source['p13_direct']; pair = work['pair_terms']['geomean_ratio']; peak = work['peak_monomials']['geomean_ratio']
    passflag = (fuzz['passed'] and invariant['passed'] and any(r['annotate'] and r['p6_folds'] > 0 for r in gsym)
                and primary['geomean_ratio'] <= .95 and primary['ci95'][1] < 1.0
                and (pair is None or pair <= 1.05) and (peak is None or peak <= 1.05))
    eng = (invariant['passed'] and build['p13_p12']['geomean_ratio'] <= .95
           and source['p13_p12']['geomean_ratio'] <= .99 and source['p13_p12']['ci95'][1] < 1.0)

    def memory_compare(memrows, num, den):
        by = {(r['case_id'], r['arm']): r['python_peak_bytes'] for r in memrows}; cases = sorted({r['case_id'] for r in memrows})
        ratios = [by[(c, num)] / by[(c, den)] for c in cases if by[(c, den)]]
        return {'cases': len(ratios), 'geomean_ratio': geomean(ratios),
                'median_ratio': statistics.median(ratios) if ratios else None}

    def p13_stats(symbolic):
        exact = [r['p13_dispatch'] for r in symbolic if r['p13_dispatch']['pair_exactified']]
        scans = [r['p13_dispatch'] for r in symbolic if r['p13_dispatch']['reuse_scanned']]
        total_edges = sum(r['p12_dispatch']['edge_count'] for r in symbolic)
        scanned_edges = sum(x['reuse_scan_edges'] for x in scans)
        return {
            'cases': len(symbolic), 'pair_exactification_cases': len(exact),
            'reuse_scan_cases': len(scans), 'reuse_early_abort_cases': sum(x['reuse_early_abort'] for x in scans),
            'reuse_scan_edges': scanned_edges,
            'reuse_scan_fraction_all_source_edges': scanned_edges / total_edges if total_edges else 0.0,
        }

    # Depth strata on source-inclusive endpoint.
    depth = {}
    for d in sorted({r['depth'] for r in gs}):
        sub = [r for r in gs if r['depth'] == d]
        depth[str(d)] = {
            'p13_direct': compare(sub, 'source_pipeline_ns', P13, DIRECT, SEED ^ d ^ 0x13),
            'p13_p12': compare(sub, 'source_pipeline_ns', P13, P12ARM, SEED ^ d ^ 0x1313),
            'p13_direct_build': compare(sub, 'source_build_ns', P13, DIRECT, SEED ^ d ^ 0x23),
        }

    return {
        'schema': 'cm-n2-p13-summary/v1', 'fuzz': fuzz, 'invariance': invariant,
        'gatep_source': source, 'gatep_source_build': build, 'gatep_compiler': compiler,
        'gatep_depth': depth,
        'gatep_annotated': sum(r['annotate'] for r in gsym),
        'gatep_fold_cases': sum(r['annotate'] and r['p6_folds'] > 0 for r in gsym),
        'gatep_folds': sum(r['p6_folds'] if r['annotate'] else 0 for r in gsym),
        'gatep_pair_lazy': p13_stats(gsym), 'gatep_work': work,
        'gatep_memory': {
            'p13_direct': memory_compare(gatep['memory_rows'], P13, DIRECT),
            'p13_p12': memory_compare(gatep['memory_rows'], P13, P12ARM),
            'p13_p6': memory_compare(gatep['memory_rows'], P13, P6ARM),
        },
        'natural_source': nsource, 'natural_source_build': nbuild, 'natural_compiler': ncompiler,
        'natural_annotated': sum(r['annotate'] for r in nsy),
        'natural_fold_cases': sum(r['annotate'] and r['p6_folds'] > 0 for r in nsy),
        'natural_pair_lazy': p13_stats(nsy),
        'natural_memory': {
            'p13_direct': memory_compare(nmem, P13, DIRECT),
            'p13_p12': memory_compare(nmem, P13, P12ARM),
        },
        'predeclared_gatep_direct_crossover_pass': passflag,
        'predeclared_deferred_pair_engineering_success': eng,
    }


def main():
    if sha256_file(HERE / 'N2_P13_PREREGISTRATION.md') != PREREG_SHA256:
        raise SystemExit('P13 preregistration hash mismatch')
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
