from __future__ import annotations
import argparse, cProfile, pstats, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import n2_p10_harness as h

def run(kind, rounds=10):
    cls={'direct':h.base.Factory,'p9':h.p9.MinimalTelemetryFactory,'p10':h.FusedMinimalTelemetryFactory}[kind]
    recipes=h.p8.gatep_eval_recipes()
    for _ in range(rounds):
        for cid,d,i,build in recipes:
            f,r,n=build(cls)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--kind',choices=('direct','p9','p10'),required=True);ap.add_argument('--out',required=True);a=ap.parse_args()
    prof=cProfile.Profile(); prof.enable(); run(a.kind); prof.disable()
    with open(a.out,'w') as fp:
        ps=pstats.Stats(prof,stream=fp).sort_stats('cumulative');ps.print_stats(35)
if __name__=='__main__':main()
