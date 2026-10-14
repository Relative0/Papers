import cProfile,pstats,io,sys
sys.path.insert(0,'.')
import n2_p12_harness as h

def run(cls, rounds=10):
    for _ in range(rounds):
        for cid,d,i,build in h.p8.gatep_eval_recipes():
            build(cls)

def prof(cls):
    p=cProfile.Profile();p.enable();run(cls);p.disable();s=io.StringIO();pstats.Stats(p,stream=s).sort_stats('cumulative').print_stats(40);return s.getvalue()
for name,cls in [('DIRECT',h.base.Factory),('P11',h.p11.TreeSpecializedTelemetryFactory),('P12',h.LazyReuseTelemetryFactory)]:
    print('\n===== '+name+' =====')
    print(prof(cls))
