# Reproducibility

Run from an environment with Python 3:

```bash
python code/vtree_exhaustive.py
python code/defect_localization.py
python code/benchmark_vtrees.py
```

The scripts import the Phase 4 `sdd_direct_extraction.py` from the unpacked input baseline path used during this run. For standalone reuse, copy that Phase 4 module next to these scripts or adjust `sys.path`.

Seed for the n=5 benchmark: `20260929`.

Expected headline values:

- n=4 nonfalse functions: 65,535;
- decomposable: 2,601;
- fixed balanced fully aligned among decomposable: 225;
- random-vtree mean alignment probability among decomposable: ~0.21937716;
- n=4 global exposure optimum reaches full prime partition: 65,535;
- all-equal-support counterexample has empty pairwise rank-2 edge set for n=3..6 and minimum balanced-cut witness support n.
