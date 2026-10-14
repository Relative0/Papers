from __future__ import annotations
import csv, json, os, sys, time, platform, hashlib
sys.path.insert(0, os.path.join(os.path.dirname(__file__),"..","src"))
from cmbench.core import fold_cm,fold_generic_2support,vars_of,eval_expr
from cmbench.anf import ANFStats,propagate,propagate_mask
from cmbench.workloads import same_operand_tree,mixed_tree

OUT=os.path.join(os.path.dirname(__file__),"..","results","exploratory")
os.makedirs(OUT,exist_ok=True)
rows=[]
for family in ("same_operand","mixed"):
  for depth in range(1,7):
    for seed in range(10):
      e=same_operand_tree(depth,seed) if family=="same_operand" else mixed_tree(max(4,depth+2),depth,seed)
      variants={"direct":e,"cm":fold_cm(e,[]),"generic2":fold_generic_2support(e,[])}
      polys={}
      for name,v in variants.items():
        st=ANFStats(); t0=time.perf_counter_ns(); p=propagate(v,st); dt=time.perf_counter_ns()-t0
        order=tuple(sorted(vars_of(v))); pm=propagate_mask(v,order)
        decoded=frozenset(frozenset(order[i] for i in range(len(order)) if (m>>i)&1) for m in pm)
        assert decoded==p
        polys[name]=p
        rows.append({"family":family,"depth":depth,"seed":seed,"variant":name,
                     "anf_ns":dt,"monomials":len(p),"peak_monomials":st.peak_monomials,
                     "peak_degree":st.peak_degree,"poly_multiplications":st.multiplications,
                     "multiplication_pair_terms":st.multiplication_pair_terms})
      assert polys["direct"]==polys["cm"]==polys["generic2"]

path=os.path.join(OUT,"mechanism_smoke.csv")
with open(path,"w",newline="") as f:
  w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
meta={"status":"EXPLORATORY_NOT_PREREGISTERED_TIMING_EVIDENCE","python":sys.version,"platform":platform.platform(),"rows":len(rows)}
with open(os.path.join(OUT,"mechanism_smoke_meta.json"),"w") as f: json.dump(meta,f,indent=2)
print(path)
