import cProfile, pstats, io, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import n2_p9_harness as h
recipes=h.p8.gatep_eval_recipes()
pr=cProfile.Profile(); pr.enable()
for _ in range(10):
    for cid,d,i,build in recipes:
        build(h.MinimalTelemetryFactory)
pr.disable()
s=io.StringIO(); pstats.Stats(pr,stream=s).sort_stats('cumulative').print_stats(40)
(HERE/'P9_POSTHOC_TELEMETRY_PROFILE.txt').write_text(s.getvalue())
print(s.getvalue())
