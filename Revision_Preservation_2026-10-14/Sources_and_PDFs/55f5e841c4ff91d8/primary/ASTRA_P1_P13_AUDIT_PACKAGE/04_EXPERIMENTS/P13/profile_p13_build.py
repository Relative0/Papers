import cProfile,pstats,io,sys
sys.path.insert(0,'.')
import n2_p13_harness as h

def run_direct(rounds=10):
    for _ in range(rounds):
        for cid,d,i,build in h.p8.gatep_eval_recipes():
            build(h.base.Factory)

def run_p12(rounds=10):
    gate=h.load_gate()
    for _ in range(rounds):
        for cid,d,i,build in h.p8.gatep_eval_recipes():
            f,root,n=build(h.p12.LazyReuseTelemetryFactory); f.dispatch(gate)

def run_p13(rounds=10):
    gate=h.load_gate()
    for _ in range(rounds):
        for cid,d,i,build in h.p8.gatep_eval_recipes():
            f,root,n=build(h.DeferredPairTelemetryFactory); f.dispatch(gate)

def prof(fn):
    p=cProfile.Profile();p.enable();fn();p.disable();s=io.StringIO();pstats.Stats(p,stream=s).sort_stats('cumulative').print_stats(50);return s.getvalue()
for name,fn in [('DIRECT_BUILD',run_direct),('P12_BUILD_DISPATCH',run_p12),('P13_BUILD_DISPATCH',run_p13)]:
    print('\n===== '+name+' =====')
    print(prof(fn))
