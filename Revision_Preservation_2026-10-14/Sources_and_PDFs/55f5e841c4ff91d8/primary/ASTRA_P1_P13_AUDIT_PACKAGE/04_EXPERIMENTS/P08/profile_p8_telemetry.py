import cProfile,pstats,io,sys,pathlib
HERE=pathlib.Path(__file__).resolve().parent; sys.path.insert(0,str(HERE)); import n2_p8_harness as h
rec=[x for x in h.gatep_eval_recipes() if x[1]==10][2][3]
pr=cProfile.Profile(); pr.enable()
for _ in range(400): rec(h.TelemetryFactory)
pr.disable(); s=io.StringIO(); pstats.Stats(pr,stream=s).sort_stats('cumulative').print_stats(35)
(HERE/'P8_POSTHOC_TELEMETRY_PROFILE.txt').write_text(s.getvalue())
print(s.getvalue()[:5000])
