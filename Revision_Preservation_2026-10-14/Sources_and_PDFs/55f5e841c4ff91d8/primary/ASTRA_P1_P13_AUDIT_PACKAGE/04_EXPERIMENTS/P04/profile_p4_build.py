import cProfile,pstats,io,random,sys
sys.path.insert(0,'.')
import n2_p4_harness as h
cases=h.generate_gate_cases(); target=[x for x in cases if x[0]==10 and x[1]==2][0]
_,_,root,n,oracle=target
pr=cProfile.Profile();pr.enable()
for _ in range(100): h.run_pipeline_once(root,h.P4_BUILD,oracle,n,False)
pr.disable();s=io.StringIO();pstats.Stats(pr,stream=s).sort_stats('cumtime').print_stats(25);print(s.getvalue())
