"""Frozen P14-PY0 analysis: paired case/process ratios and hierarchical bootstrap."""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import csv
import hashlib
import json
import math
import random
import statistics
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from p14_common import ARMS,operation_counts,trace_builder
from run_correctness import natural_recipes,synthetic_recipes,sha

BOOTSTRAP_SEED=2026091902
DRAWS=10000


def geo(values):return math.exp(statistics.mean(math.log(x) for x in values))


def quantile(values,p):
    values=sorted(values);x=(len(values)-1)*p;i=int(x);f=x-i
    return values[i]*(1-f)+values[min(i+1,len(values)-1)]*f


def summarize(rows,corpus,a,b,endpoint="recipe"):
    subset=[r for r in rows if r["corpus"]==corpus and r["endpoint"]==endpoint and r["arm"] in (a,b)]
    groups=defaultdict(list)
    for r in subset:groups[(r["case_id"],r["arm"])].append(r["per_compile_ns"])
    cases=sorted({r["case_id"] for r in subset});med={k:statistics.median(v) for k,v in groups.items()}
    ratios=[med[c,a]/med[c,b] for c in cases]
    families={c:next(r["family"] for r in subset if r["case_id"]==c) for c in cases}
    fam_groups=defaultdict(list)
    for c in cases:fam_groups[families[c]].append(c)
    worker_groups=defaultdict(list)
    workers_by_case=defaultdict(set)
    for r in subset:
        worker=(r["session"],r["worker"])
        worker_groups[(r["case_id"],r["arm"],worker)].append(r["per_compile_ns"])
        workers_by_case[r["case_id"]].add(worker)
    worker_medians={key:statistics.median(values) for key,values in worker_groups.items()}
    workers_by_case={case:sorted(values) for case,values in workers_by_case.items()}
    rng=random.Random(BOOTSTRAP_SEED ^ sum(map(ord,corpus+a+b)));draws=[]
    fams=sorted(fam_groups)
    for _ in range(DRAWS):
        sampled_fams=[rng.choice(fams) for _ in fams];logs=[]
        for family in sampled_fams:
            fc=fam_groups[family]
            for _ in fc:
                c=rng.choice(fc)
                # Resample matched worker medians; case/arm pairing stays together.
                w=rng.choice(workers_by_case[c])
                logs.append(math.log(worker_medians[c,a,w]/worker_medians[c,b,w]))
        draws.append(math.exp(statistics.mean(logs)))
    return {"corpus":corpus,"endpoint":endpoint,"comparison":f"{a}/{b}","cases":len(cases),"families":len(fams),
            "geomean":geo(ratios),"median":statistics.median(ratios),
            "aggregate":sum(med[c,a] for c in cases)/sum(med[c,b] for c in cases),
            "wins":sum(x<1 for x in ratios),"ci95":[quantile(draws,.025),quantile(draws,.975)],
            "ci98_75":[quantile(draws,.00625),quantile(draws,.99375)],
            "case_ratios":dict(zip(cases,ratios))}


def main():
    rows=[]
    for path in sorted(HERE.glob("timing_s*_w*.json")):
        rows.extend(json.loads(path.read_text())["rows"])
    expected=3*1
    workers={(r["session"],r["worker"]) for r in rows}
    if len(workers)!=expected:raise RuntimeError(f"expected {expected} workers got {len(workers)}")
    comparisons=[]
    for corpus in ("synthetic","natural"):
        for a,b in (("E","F"),("E","D"),("A","D"),("G","D")):
            comparisons.append(summarize(rows,corpus,a,b))
    comparisons.append(summarize(rows,"canonical","CA","CD"))
    secondary=[]
    for corpus in ("synthetic","natural"):
        for a,b in (("E","F"),("E","D"),("A","D"),("G","D")):
            secondary.append(summarize(rows,corpus,a,b,"ir"))
    for item in comparisons:
        item["ordinary_superiority"]=item["ci95"][1]<1
        item["simultaneous_superiority"]=item["ci98_75"][1]<1
        item["effect_threshold_pass"]=(item["geomean"]<=.95 if item["comparison"]=="E/D" else item["geomean"]<=.99 if item["comparison"]=="E/F" else None)
    op=[]
    for cid,family,build,meta in synthetic_recipes():op.append({"case_id":cid,"corpus":"synthetic","family":family,**operation_counts(build)})
    for cid,design,build,oracle,nvars,meta in natural_recipes():op.append({"case_id":cid,"corpus":"natural","family":design,**operation_counts(build)})
    correctness=json.loads((HERE/"correctness_results.json").read_text())
    result={"schema":"p14-py0-results/v1","workers":len(workers),"raw_rows":len(rows),
            "correctness_status":correctness["status"],"comparisons":comparisons,"secondary_ir":secondary,
            "confirmatory_note":"Four confirmatory comparisons use frozen Bonferroni 98.75% two-sided hierarchical-bootstrap intervals for familywise alpha 0.05.",
            "selected":{"synthetic":correctness["selected_synthetic"],"natural":correctness["selected_natural"]},
            "operation_rows":op}
    (HERE/"P14_RESULTS.json").write_text(json.dumps(result,indent=2)+"\n")
    with (HERE/"P14_CASE_RATIOS.csv").open("w",newline="") as handle:
        writer=csv.writer(handle);writer.writerow(["corpus","comparison","case_id","ratio"])
        for item in comparisons:
            for cid,ratio in item["case_ratios"].items():writer.writerow([item["corpus"],item["comparison"],cid,ratio])
    memory=json.loads((HERE/"memory_results.json").read_text())
    lines=["# P14-PY0 execution report","",f"Status: **{correctness['status']}**",'',
           f"Frozen synthetic cases: {correctness['synthetic_cases']}; natural cases: {correctness['natural_cases']} across {len(set(r['family'] for r in rows if r['corpus']=='natural'))} families.",
           f"Timing: {len(workers)} fresh sequential workers, {len(rows):,} measured rows. Memory: {len(memory['rows']):,} isolated tracemalloc observations.","",
           "## Primary recipe endpoint","","| Corpus | Comparison | Geomean | 95% CI | Simultaneous 98.75% CI | Wins |","|---|---:|---:|---:|---:|---:|"]
    for x in comparisons:
        lines.append(f"| {x['corpus']} | {x['comparison']} | {x['geomean']:.4f} | {x['ci95'][0]:.4f}–{x['ci95'][1]:.4f} | {x['ci98_75'][0]:.4f}–{x['ci98_75'][1]:.4f} | {x['wins']}/{x['cases']} |")
    lines += ["","## Secondary compiler-IR endpoint","","| Corpus | Comparison | Geomean | 95% CI |","|---|---:|---:|---:|"]
    for x in secondary:
        lines.append(f"| {x['corpus']} | {x['comparison']} | {x['geomean']:.4f} | {x['ci95'][0]:.4f}–{x['ci95'][1]:.4f} |")
    lines += ["","## Interpretation","",result["confirmatory_note"],
              "The reduced local budget is a declared departure from the draft. Close effects remain inconclusive; results do not support production rollout without the independent P14-PY1 confirmation.",""]
    (HERE/"P14_EXECUTION_REPORT.md").write_text("\n".join(lines))
    print(json.dumps({"workers":len(workers),"raw_rows":len(rows),"selected":result["selected"],
                      "comparisons":[{k:v for k,v in x.items() if k!="case_ratios"} for x in comparisons]},indent=2))


if __name__=="__main__":main()
