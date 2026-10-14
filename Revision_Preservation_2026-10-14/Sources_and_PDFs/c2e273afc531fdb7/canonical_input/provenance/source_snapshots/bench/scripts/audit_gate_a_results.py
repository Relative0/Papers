#!/usr/bin/env python3
from __future__ import annotations
import csv, json, hashlib, statistics, datetime
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'results' / 'raw' / 'gate_a_s1_s2.csv'
SUMMARY = ROOT / 'results' / 'gate_a_s1_s2_summary.json'
OUT = ROOT / 'results' / 'gate_a_s1_s2_audit.json'

rows = list(csv.DictReader(RAW.open(newline='', encoding='utf-8')))
admitted = [r for r in rows if r['all_arms_ok'] == '1' and r['correctness_status'] == 'OK']
s1 = [r for r in admitted if r['family'] == 'S1']
s2 = [r for r in admitted if r['family'] == 'S2']
assert len(rows) == 10500
assert len(s1) == 3750
assert len(s2) == 6639
assert len(admitted) == 10389
assert not [r for r in rows if r.get('correctness_status') not in ('OK','NO_SUCCESSFUL_ARM')]
assert all(r.get('successful_arms_agree') == '1' for r in admitted)
assert all(r.get('independent_eval_ok') == '1' for r in admitted)
assert all(r.get('live_k_exact_match') == '1' for r in s2)

metrics = ['multiplications','pair_terms','peak_monomials','output_unique_nodes','final_monomials','final_degree','serialized_bytes']
diffs = {}
for metric in metrics:
    n = sum(r[f'cm_frontend_sparse_{metric}'] != r[f'generic_2support_sparse_{metric}'] for r in admitted)
    diffs[metric] = n
    assert n == 0
assert sum(r['cm_frontend_sparse_digest'] != r['generic_2support_sparse_digest'] for r in admitted) == 0

generic_more_folds = sum(float(r['generic_2support_sparse_successful_folds']) > float(r['cm_frontend_sparse_successful_folds']) for r in admitted)
cm_more_folds = sum(float(r['cm_frontend_sparse_successful_folds']) > float(r['generic_2support_sparse_successful_folds']) for r in admitted)
assert generic_more_folds == 6010
assert cm_more_folds == 0

# Budget patterns over corrected S2.
s2_all = [r for r in rows if r['family'] == 'S2']
patterns = Counter()
for r in s2_all:
    if r['all_arms_ok'] != '1':
        patterns[tuple(r.get(a + '_status','') for a in (
            'direct_sparse_anf','cse_flat_sparse','generic_2support_sparse','cm_frontend_sparse'
        ))] += 1
assert sum(patterns.values()) == 111
assert patterns[('BUDGET','BUDGET','BUDGET','BUDGET')] == 108
assert patterns[('BUDGET','BUDGET','OK','OK')] == 2
assert patterns[('BUDGET','OK','BUDGET','BUDGET')] == 1

summary = json.load(SUMMARY.open(encoding='utf-8'))
assert summary['SC_A_pass_strict_all_predeclared_strata'] is True
assert summary['S2_live_k_exact_match_fraction'] == 1.0

# Recheck S2 sharing medians quoted in RESULTS.md.
share = {}
for level in (0.0,0.25,0.5):
    sub = [r for r in s2 if float(r['shared_fraction_requested']) == level]
    share[str(level)] = {
        'n': len(sub),
        'direct_multiplications_median': statistics.median(float(r['direct_sparse_anf_multiplications']) for r in sub),
        'cm_multiplications_median': statistics.median(float(r['cm_frontend_sparse_multiplications']) for r in sub),
        'generic_multiplications_median': statistics.median(float(r['generic_2support_sparse_multiplications']) for r in sub),
        'cm_folds_median': statistics.median(float(r['cm_frontend_sparse_successful_folds']) for r in sub),
        'generic_folds_median': statistics.median(float(r['generic_2support_sparse_successful_folds']) for r in sub),
    }

out = {
    'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'raw_sha256': hashlib.sha256(RAW.read_bytes()).hexdigest(),
    'summary_sha256': hashlib.sha256(SUMMARY.read_bytes()).hexdigest(),
    'row_count': len(rows),
    'admitted_count': len(admitted),
    's1_admitted': len(s1),
    's2_admitted': len(s2),
    'correctness_mismatches': 0,
    'cm_vs_generic_metric_differences': diffs,
    'generic_more_fold_rows': generic_more_folds,
    'cm_more_fold_rows': cm_more_folds,
    'budget_status_patterns': {'|'.join(k): v for k,v in patterns.items()},
    's2_sharing_medians': share,
    'sc_a_pass': True,
    'audit_pass': True,
}
OUT.write_text(json.dumps(out, indent=2, sort_keys=True), encoding='utf-8')
print(json.dumps(out, indent=2, sort_keys=True))
