import cProfile,pstats,io,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import n2_p5_harness as h
case=[x for x in h.generate_gate_cases() if x[0]==10 and x[1]==2][0]
depth,i,root,n,oracle=case
pr=cProfile.Profile(); pr.enable()
for _ in range(100): h.run_pipeline_once(root,h.P5_BUILD,oracle,n,False)
pr.disable(); s=io.StringIO(); pstats.Stats(pr,stream=s).sort_stats('cumulative').print_stats(30)
print(s.getvalue())
