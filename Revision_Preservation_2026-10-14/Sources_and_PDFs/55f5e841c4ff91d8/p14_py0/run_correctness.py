"""P14-PY0 correctness gates.  Must pass before timing interpretation."""
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import random
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from p14_common import *


def sha(path):
    digest=hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda:handle.read(1024*1024),b""):digest.update(chunk)
    return digest.hexdigest()


def check_freeze():
    freeze=json.loads((HERE/"P14_FREEZE.json").read_text())
    for name,digest in freeze["source_hashes"].items():
        if sha(HERE/name)!=digest:raise RuntimeError(f"post-freeze source change: {name}")
    for name,digest in freeze["manifests"].items():
        if sha(HERE/name)!=digest:raise RuntimeError(f"post-freeze manifest change: {name}")
    return freeze


def natural_recipes():
    manifest=json.loads((HERE/"natural_holdout.json").read_text())
    out=[]
    for design in manifest["designs"]:
        path=HERE/design["path"]
        if sha(path)!=design["sha256"]:raise RuntimeError(f"BLIF drift {path}")
        blif=base.parse_blif(path)
        for item in design["cases"]:
            names=tuple(item["support_names"]);root=item["root"]
            def build(cls,blif=blif,root=root,names=names):
                return h.p8.build_cone_with_factory(blif,root,names,cls)
            oracle=h.p8.p1.eval_blif_cone(blif,root,names)
            out.append((f"{design['design']}:{root}",design["design"],build,oracle,len(names),item))
    return out


def synthetic_recipes():
    manifest=json.loads((HERE/"synthetic_holdout.json").read_text())
    return [(x["case_id"],x["family"],trace_builder(x["trace"]),x) for x in manifest["cases"]]


def check_token_algebra():
    checked=0
    for parent_index in range(3):
        for left in range(16):
            for right in range(16):
                got=p6.TOKEN_APPLY[parent_index][left][right]
                expected=0
                for x in (0,1):
                    for y in (0,1):
                        a=(left>>(2*x+y))&1;b=(right>>(2*x+y))&1
                        value=(a&b,a|b,a^b)[parent_index]
                        expected|=value<<(2*x+y)
                assert got==expected
                assert p6.SWAP_TOKEN[left] == sum(((left>>(2*y+x))&1)<<(2*x+y) for x in (0,1) for y in (0,1))
                checked+=1
    return checked


def compare_case(case_id,kind,build,oracle=None):
    t0=time.perf_counter()
    polys={};choices={};arm_seconds={}
    for arm in ARMS+CANONICAL_ARMS:
        arm_t0=time.perf_counter()
        poly,choice=compile_recipe(build,arm)
        arm_seconds[arm]=time.perf_counter()-arm_t0
        if arm_seconds[arm]>60:raise RuntimeError(f"per-compile cap {case_id} {arm} {arm_seconds[arm]}")
        if len(poly)>1_000_000:raise RuntimeError(f"monomial cap {case_id} {arm}")
        polys[arm]=poly;choices[arm]=choice
    expected=polys["D"]
    mismatched=[a for a,p in polys.items() if p!=expected]
    fac,root,nvars=build(base.Factory)
    if oracle is None:
        oracle=base.eval_node_bitset(root,nvars)
    truth_ok=base.anf_to_bitset(expected,nvars)==oracle
    pf,pr,_=build(MinimalP13Factory);ef,er,_=build(TupleBoundFactory)
    decision_ok=pf.dispatch_bool()==ef.dispatch_bool()==ref_decision(exact_stats(pf))
    if mismatched or not truth_ok or not decision_ok:
        raise AssertionError((case_id,mismatched,truth_ok,decision_ok))
    elapsed=time.perf_counter()-t0
    return {"case_id":case_id,"kind":kind,"seconds":elapsed,"nodes":len(fac.nodes),
            "nvars":nvars,"monomials":len(expected),"decision":choices["E"],
            "arm_seconds":arm_seconds,"max_arm_seconds":max(arm_seconds.values()),
            "digest":base.poly_digest(expected),"all_arms_equal":True,"truth_ok":truth_ok}


def fresh_targeted():
    rng=random.Random(2026091903);rows=[]
    for i in range(512):
        fi=rng.randrange(len(SYNTHETIC_FAMILIES));index=rng.randrange(32)
        factors=synthetic_factors(index);factors["multiplicity"]=(4,5,8,16)[i%4]
        trace=make_trace(fi,index,rng.getrandbits(63),factors)
        row=compare_case(f"fresh:{i}","fresh_targeted",trace_builder(trace))
        rows.append(row)
    return rows


def main():
    freeze=check_freeze()
    subprocess.run([sys.executable,str(AUDIT/"runtime/cm_n2_p13_run/n2_p13_harness.py"),
                    "--mode","invariant","--out",str(HERE/"regression_invariance.json")],check=True)
    subprocess.run([sys.executable,str(AUDIT/"runtime/cm_n2_p13_run/n2_p13_harness.py"),
                    "--mode","fuzz","--out",str(HERE/"regression_fuzz.json")],check=True)
    old_inv=json.loads((HERE/"regression_invariance.json").read_text())
    old_fuzz=json.loads((HERE/"regression_fuzz.json").read_text())
    diag=json.loads((AUDIT/"python_diagnostics/dispatch_diagnostics.json").read_text())
    targeted=json.loads((AUDIT/"python_diagnostics/targeted_dispatch_checks.json").read_text())
    if diag.get("code_sha256") != sha(AUDIT/"python_diagnostics/dispatch_diagnostics.py"):
        raise RuntimeError("archived dispatch diagnostic/code hash mismatch")
    if targeted.get("code_sha256") != sha(AUDIT/"python_diagnostics/targeted_dispatch_checks.py"):
        raise RuntimeError("archived targeted diagnostic/code hash mismatch")
    if not(old_inv["passed"] and old_fuzz["passed"] and not diag["failures"] and targeted["passed"]):
        raise RuntimeError("known regression gate failed")
    token_checks=check_token_algebra()
    rows=[]
    for cid,family,build,meta in synthetic_recipes():
        rows.append(compare_case(cid,"synthetic",build))
        print(f"S {len(rows)}/384 {cid}",flush=True)
    natural=natural_recipes()
    for i,(cid,design,build,oracle,nvars,meta) in enumerate(natural,1):
        rows.append(compare_case(cid,"natural",build,oracle))
        print(f"N {i}/{len(natural)} {cid}",flush=True)
    fresh=fresh_targeted()
    result={"schema":"p14-py0-correctness/v1","freeze_sha256":sha(HERE/"P14_FREEZE.json"),
            "status":"PASS","known":{"invariance":old_inv["total"],"fuzz":old_fuzz["cases"],
              "extra_dags":diag["checks"]["adversarial_cases"],"integer_boundaries":diag["checks"]["boundaries"],
              "targeted":targeted["cases"],"targeted_positive":targeted["annotated"]},
            "token_compositions":token_checks,"fresh_targeted":len(fresh),
            "holdout_cases":len(rows),"synthetic_cases":sum(r["kind"]=="synthetic" for r in rows),
            "natural_cases":sum(r["kind"]=="natural" for r in rows),
            "selected_synthetic":sum(r["kind"]=="synthetic" and r["decision"] for r in rows),
            "selected_natural":sum(r["kind"]=="natural" and r["decision"] for r in rows),
            "rows":rows,"fresh_rows":fresh}
    (HERE/"correctness_results.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k not in ("rows","fresh_rows")},indent=2))


if __name__=="__main__":main()
