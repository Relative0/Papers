import cProfile,pstats,io,sys
sys.path.insert(0,'cm_n2_p11_run')
import n2_p11_harness as h

def run(cls, rounds=10):
    for _ in range(rounds):
        for cid,d,i,build in h.p8.gatep_eval_recipes():
            build(cls)

def prof(cls):
    p=cProfile.Profile();p.enable();run(cls);p.disable();s=io.StringIO();pstats.Stats(p,stream=s).sort_stats('cumulative').print_stats(35);return s.getvalue()
for name,cls in [('DIRECT',h.base.Factory),('P10',h.p10.FusedMinimalTelemetryFactory),('P11',h.TreeSpecializedTelemetryFactory)]:
    print('\n===== '+name+' =====')
    print(prof(cls))
