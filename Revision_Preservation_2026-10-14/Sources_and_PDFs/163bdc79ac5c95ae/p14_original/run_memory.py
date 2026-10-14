"""Frozen P14-PY0 separate peak-memory pass using tracemalloc."""
from __future__ import annotations

from pathlib import Path
import json
import sys
import tracemalloc

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from p14_common import ARMS,compile_recipe
from run_correctness import check_freeze,natural_recipes,synthetic_recipes,sha


def main():
    check_freeze()
    if json.loads((HERE/"correctness_results.json").read_text()).get("status")!="PASS":
        raise RuntimeError("correctness gate absent")
    recipes=[]
    for cid,family,build,meta in synthetic_recipes():recipes.append(("synthetic",family,cid,build))
    for cid,design,build,oracle,nvars,meta in natural_recipes():recipes.append(("natural",design,cid,build))
    rows=[]
    for i,(corpus,family,cid,build) in enumerate(recipes,1):
        expected=compile_recipe(build,"D")[0]
        for arm in ARMS:
            tracemalloc.start()
            tracemalloc.reset_peak()
            poly,selected=compile_recipe(build,arm)
            current,peak=tracemalloc.get_traced_memory()
            tracemalloc.stop()
            if poly!=expected:raise AssertionError((cid,arm))
            rows.append({"case_id":cid,"corpus":corpus,"family":family,"arm":arm,
                         "current_bytes":current,"peak_bytes":peak,"selected":selected,
                         "monomials":len(poly)})
        if i%25==0:print(f"memory {i}/{len(recipes)}",flush=True)
    out={"schema":"p14-py0-memory/v1","freeze_sha256":sha(HERE/"P14_FREEZE.json"),"rows":rows}
    (HERE/"memory_results.json").write_text(json.dumps(out,separators=(",",":"))+"\n")
    print(f"PASS memory: {len(rows)} observations",flush=True)


if __name__=="__main__":main()
