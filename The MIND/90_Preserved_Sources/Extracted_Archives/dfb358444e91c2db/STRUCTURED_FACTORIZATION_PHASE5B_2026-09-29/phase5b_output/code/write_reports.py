"""Render measured campaign summaries without modifying experimental inputs."""
from pathlib import Path
import json,statistics

ROOT=Path(__file__).resolve().parents[1]
def write(name,text):(ROOT/name).write_text(text.strip()+'\n',encoding='utf-8')
def main():
    result=json.loads((ROOT/'data/statistical_summary.json').read_text());s=result['summary'];m=s['M5'];base=result['baseline']
    rows=[json.loads(l) for l in (ROOT/'data/heldout_results.jsonl').read_text().splitlines()]
    pairs=json.loads((ROOT/'data/paired_heldout_results.json').read_text())
    primary=result['primary_pilot_go'];rescue=result['primary_residual_rescue']
    decision='G. MORE RESEARCH REQUIRED' if primary or rescue else 'D. MATHEMATICAL NOTE SURVIVES; ALGORITHMIC NO-GO'
    table='| Method | Median total ms | Mean total ms | IQR ms | Paired geo ratio vs '+base+' | 95% descriptive interval | Wins / losses | Median SAT calls incl. probes | Failures |\n|---|---:|---:|---:|---:|---|---:|---:|---:|\n'
    for method,x in s.items():
        lo,hi=x['paired_ratio_bootstrap_95']
        table+=f"| {method} | {1000*x['median_seconds']:.3f} | {1000*x['mean_seconds']:.3f} | {1000*x['iqr_seconds']:.3f} | {x['paired_geometric_ratio']:.3f} | [{lo:.3f}, {hi:.3f}] | {x['wins']} / {x['losses']} | {x['median_sat_calls']:.1f} | {x['failures']} |\n"
    fam=[]
    for family in sorted({r['family'] for r in rows}):
        ids={r['id'] for r in rows if r['family']==family}
        pp=[p for p in pairs if p['method']=='M5' and p['id'] in ids]
        fam.append(f"| {family} | {len(pp)} | {statistics.median(p['ratio'] for p in pp):.3f} | {sum(p['ratio']<1 for p in pp)} |")
    write('BENCHMARK_RESULTS.md',f'''# Phase 5B benchmark results

The maintained-tool pilot completed **{result['total_trials']:,} principal trials**: 70 generated CNFs x ten methods x three repetitions. Train/validation/held-out counts are 600/600/900 trials, representing 20/20/30 instances. Successful semantic and simultaneous partitions agree with the independent model/projection baseline; total failures/timeouts: **{result['total_failures']}**. No inputs or objective weights were changed from held-out results.

Validation selected **{base}**, saved before held-out execution. Primary challenger M5 has paired geometric total-runtime ratio **{m['paired_geometric_ratio']:.3f}**, with descriptive paired-instance bootstrap interval **[{m['paired_ratio_bootstrap_95'][0]:.3f}, {m['paired_ratio_bootstrap_95'][1]:.3f}]**. A ratio above one is slower. Its runtime criterion is **{'PASS' if primary else 'FAIL'}** and separately preregistered practical residual-work rescue is **{'PASS' if rescue else 'FAIL'}**. O is an oracle control, never an algorithmic competitor.

{table}

The runtime summaries use per-instance medians over three trials before aggregation. SAT-call columns summarize completed raw trials and include probe calls, so they do not conceal defect preprocessing. The paired machine-readable CSV gives every per-instance comparison. Raw JSONL retains tree search, real SDD sizes, partitions, SAT counters, memory and move traces. No conflict/propagation number is an estimate from encoding size.

## Primary family strata

| Family | Held-out instances | Median M5/{base} ratio | M5 faster instances |
|---|---:|---:|---:|
{chr(10).join(fam)}

These are descriptive strata, not a second selection criterion. Each family has n=6,8,10 instances. Many are relabelled copies or size extensions of the same simple module structures present in train/validation; this is not a test of generalization to unseen industrial structures. The random family has independent planted clause draws. Read-once and repeated-module cases cover restricted explicit CNF constructions, not arbitrary operator DAGs.

## Scope and negative boundaries

Real PySDD/Glucose measurements close the tooling gap. They do not close the scale/baseline gap. M searches recompile every candidate, whereas B2 has native dynamic minimization; B3 is a component/min-fill-order balanced construction. The fixed first-six-neighbor policy may miss beneficial moves. These costs and limitations belong to the tested implementation. A negative result does not refute every possible exposure/defect objective or native implementation.

Public documentation CNFs are reported separately in `data/public_control_results.json`; they are public smoke controls, not an industrial benchmark corpus. Separate move diagnostics measure size/exposure/residual-cost tradeoffs after primary timing. The training-only SAT reuse experiment compares actual solver persistence and fresh encodings. Neither supplementary experiment changes the primary decision.
''')
    write('STATISTICAL_ANALYSIS.md',f'''# Statistical analysis

Primary decision for this fixed pilot: **{'criterion met; industrial result still unestablished' if primary or rescue else 'algorithmic NO-GO'}**. All {result['total_trials']:,} required trial cells exist and their source/protocol/manifest fingerprints agree across splits. All completed outputs are correct; {result['total_failures']} failed/censored rows are recorded. Analysis verifies that the validation file and analysis code match the pre-held-out selection receipt.

The sole primary comparison is M5/{base}. Median-of-three times are paired by instance; their geometric ratio is {m['paired_geometric_ratio']:.6f}. The 10,000-draw percentile bootstrap (seed 2026092907) is [{m['paired_ratio_bootstrap_95'][0]:.6f}, {m['paired_ratio_bootstrap_95'][1]:.6f}]. M5 wins on {m['wins']}, loses on {m['losses']}, ties on {m['ties']} of 30 held-out instances. Runtime GO required ratio <=0.90, upper interval <1, zero correctness disagreements and no excess failures. Other methods/family strata are exploratory; no multiple-comparison winner is substituted for M5.

Residual rescue required all three registered conditions: >=25% median paired SAT-call reduction, >=10% median paired SAT-wall reduction, and >=0.005 seconds median absolute SAT saving, with no excess failures. M5 values are respectively **{m['median_sat_call_reduction']}**, **{m['median_sat_wall_reduction']}**, and **{m['median_sat_wall_saving_seconds']} seconds** (fractions for reductions). Probe calls/time are included. These conditions **{'pass' if rescue else 'fail'}**. A call reduction alone is not a speedup, and the rescue never changes the named runtime primary.

For baseline-zero work, both-zero is no improvement and method-positive is negative infinity. Censored/error pairs count as negative infinity for rescue and are not dropped. Timeout/error primary penalty is PAR2=30 seconds per trial before the median. The 15-second watchdog measures full process lifetime; successful algorithm runtime excludes startup/parsing. Raw process time is also saved. Failure counts retain all repetitions even if a median could otherwise hide one timeout.

Intervals are conditional descriptive resampling of this fixed 30-instance mixture. Related generator structures and only three timing repetitions do not justify an independent industrial-population inference. Machine load and OS temporary-file costs are uncontrolled. Reported medians, means, IQRs, paired effects and complete raw data are more informative here than an isolated significance label. No extrapolation to larger n, production workload, energy use or wall-time savings is warranted.

No parameter was tuned from train, validation or held-out measurements; coefficients and search budget were fixed beforehand. Validation only selects B2 versus B3. The held-out outcome is not used to revise any objective. A changed method needs a new protocol and campaign, not reuse of this held-out set for confirmatory claims.
''')
    write('PHASE5B_MASTER_REPORT.md',f'''# Structured Factorization Phase 5B master report

Date: 2026-09-29. **Primary decision: {decision}.**

The frozen Phase 4/5 record reproduced, and a real PySDD + persistent Glucose4 exact pipeline now works. The new bounded pilot ran **{result['total_trials']:,} trials** with **{result['total_failures']} failures/timeouts** and no correctness disagreement. Against validation-selected {base}, the primary carrier+defect+exposure method M5 had a paired geometric total-runtime ratio **{m['paired_geometric_ratio']:.3f}** (95% descriptive interval **[{m['paired_ratio_bootstrap_95'][0]:.3f}, {m['paired_ratio_bootstrap_95'][1]:.3f}]**). Runtime and practical residual-work criteria are respectively **{'PASS' if primary else 'FAIL'}** and **{'PASS' if rescue else 'FAIL'}**. This is a maintained-tool small-instance campaign, not industrial-scale validation.

## What is mathematically proved

Under their explicit nonfalse, compression, support-disjointness and essentiality hypotheses, the frozen compressed-SDD cut/exposure theorem, exposure optimum, laminar carrier obstruction, defect-support crossing lemma, equality-family localization obstruction, positive irredundant-CNF baseline and CM read-once recursion survive independent proof review. A new application note proves sound inclusion-minimal support shrinking and a group-deletion oracle-query bound. These do not imply minimum-cardinality support, FPT SAT runtime, efficient global vtree search or novel priority.

One prose claim is corrected: an externally certified prime-aligned tree needs no residual search, but an ordinary solver cannot infer primeness from a failed vtree cut. Every nonsingleton exposed block is exact-refined in this implementation, including the oracle tree. This correction is in the new ledger; historical files are unchanged.

## What is computationally reproduced

All six frozen campaigns and eleven archived artifacts match, excluding only timing/newline differences. Independent checks cover 458,745 cuts, 983,025 n=4 function/vtree pairs, 121,500 n=5 score calls and all 540 seeded n=5 inputs. Key counts remain 2,601 decomposable n=4 functions, fixed-tree full exposure 225, and exhaustive exposure optimum correct on all 65,535 nonfalse functions. Real-backend tests add 903 SDD compilations, 113 minimizations, 881 direct/semantic/carrier comparisons each and 1,390 SAT cuts, all with zero discrepancies.

## What is newly observed

Actual SDD element/node sizes, Glucose conflicts/decisions/propagations, wall times and process memory are now measured. The primary 70-instance/ten-method/three-repetition experiment freezes inputs and code, excludes oracle truth from all heuristic payloads, and charges recompilation/probe/refinement overhead. The held-out results and separate move/SAT-reuse diagnostics are recorded with full machine-readable data. The actual runtime conclusion is specific to this implementation and synthetic generator mix.

## What is prior art

Dynamic vtree rotations/swaps, SDD size minimization, graph/treewidth/hypergraph compilation, component decomposition, SAT/QBF bi-decomposition, Cartesian relation factorization, and monotone-predicate minimization all have substantial antecedents. The current audit includes 2025–2026 circuit-aware, semantic-vtree and alternative-representation work. No firstness claim is supported by absence from a web search.

## What failed and what remains open

{'The registered primary improvement gate was not cleared, and there is no practically meaningful residual-work rescue. Do not develop an algorithm paper around a post-hoc metric switch.' if not(primary or rescue) else 'A pilot numerical criterion was met, but larger independently structured instances and stronger baselines remain necessary before any industrial claim.'} Universal pairwise defect localization remains refuted. No efficient exposure-optimal search theorem, general small-support guarantee, unrestricted structured-d-DNNF extraction theorem or industrial runtime improvement is established. Native integration of alternative objectives is untested; the current custom search pays full recompilation costs. Carrier-compatible early residual refinement could avoid work done by the current semantic-first/final-LCC variant.

## Review and publication posture

Six internal reviewer roles cover SDD, SAT/decomposition, graph/vtree, engineering/statistics, novelty and mathematics. They found and prompted provenance safeguards and the exposed-factor/prime-certificate correction, and imposed explicit limits on the relabeling-heavy tiny benchmark, modest graph baseline and biased candidate prefix. Full findings and dispositions are preserved. This is internal adversarial review, not external peer review.

The proofs survive as a mathematical working note and the implementation as a reproducibility artifact. **Publication-ready novelty is not established.** A new LaTeX paper is deliberately not produced: the requested condition that a surviving contribution warrant one is not met after the current priority review. Archived theorem drafts remain preserved verbatim. Keep theorem validity, computational evidence, prior art and conjectures separate.

The submitted 117-file archive remains unchanged. The complete deliverable includes it beside this new output, plus code, lockfile, inputs/seeds, all principal logs/results, theorem/priority updates, research/review ledgers, reproducibility commands, checksums and the next gate.
''')
    write('NEXT_RESEARCH_GATE.md',f'''# Next research gate

**{decision}.**

{'Stop this algorithmic extension in its tested form. The frozen exact results survive, but M5 does not clear the registered total-runtime or practical residual-work gate. Preserve this negative result; do not retune on the held-out set or market a factor-count improvement as a solver speedup.' if not(primary or rescue) else 'The pilot is insufficient for an industrial claim. A new independent campaign is required before advancing algorithmic publication.'}

Nothing remains required to reproduce or archive this Phase 5B result. The mathematical note remains a working note, not a novelty-cleared paper. Defer further computation unless there is a concrete mechanism to reduce search/recompilation overhead or a separately justified scientific need. No new thread/model run is recommended merely to seek a positive outcome.

If a later request reopens the algorithm branch, require a new preregistration: native local SDD transformations for all objectives, fair search-budget accounting, a stronger decomposition-to-vtree baseline, carrier-compatible residual refinement, structurally distinct held-out families, and licensed public instances at meaningful scale. Freeze ablations, hardware/resource budget and censoring policy before executing. Retain exact SAT and oracle isolation. The present negative pilot cannot settle that different implementation, but it gives no license to assume improvement.

A concrete publication attempt first needs a theorem-level comparison against relational factorization, Boolean bi-decomposition, MSMP and the 2026 semantic-vtree work, plus an external specialist review. Do not add a paper draft until that identifies a substantive contribution.

## Conditional handoff for a separately requested campaign

Use a **new task** for a genuinely new native-search implementation/campaign; the compact verified package is a better starting point than carrying this completed execution history. Recommended model/effort if that substantial research is authorized: **gpt-6-astra, high**, because correctness, experimental design and theorem/priority boundaries interact. This is a qualitative reliability recommendation, not a measured cost claim or permission to launch work.

Starter prompt:

> Continue Structured Factorization from the delivered `phase5b_output/PHASE5B_MASTER_REPORT.md`, `NEXT_RESEARCH_GATE.md`, `HOSTILE_REVIEW_LEDGER.md`, and `REPRODUCIBILITY.md`; keep sibling `continuity_archive` unchanged. Phase 5B reproduced all frozen claims and validated real PySDD/Glucose exactness, but the small recompilation-based pilot does not establish industrial improvement. Inspect code/hybrid_core.py and code/benchmark.py and the frozen raw results before designing a different native-vtree campaign. Preserve nonsingleton prime certification, U/W defect semantics, final carrier exactness, ground-truth isolation and negative findings. Create a new output directory, freeze independently structured inputs, fair baselines, budgets and success criteria before any new held-out run. Workspace implementation/read-only diagnostics are authorized only within the new user's requested scope; do not publish, commit, push or incur spending without applicable authorization.
''')
    print(json.dumps({'decision':decision,'M5_ratio':m['paired_geometric_ratio'],'runtime_gate':primary,'rescue':rescue}))

if __name__=='__main__':main()
