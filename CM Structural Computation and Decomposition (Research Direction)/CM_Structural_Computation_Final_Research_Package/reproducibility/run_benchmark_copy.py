"""Rerun final timing in a new output tree, preserving the published raw records."""
from pathlib import Path
import argparse,shutil,subprocess,sys

def main(out):
    base=Path(__file__).resolve().parent
    if out.exists():raise SystemExit(f'Output already exists: {out}; choose a new directory')
    out.mkdir(parents=True);r=out/'reproducibility';r.mkdir()
    for name in ('code','data'):shutil.copytree(base/name,r/name,ignore=shutil.ignore_patterns('__pycache__'))
    for name in ('raw_results','logs','environment'):(r/name).mkdir()
    p=out/'research/experiment_design';p.mkdir(parents=True)
    shutil.copy2(base.parent/'research/experiment_design/PROTOCOL_V3_REPLAY.json',p/'PROTOCOL_V3_REPLAY.json')
    script=(r/'code/benchmark_replay_v3.py').resolve()
    for start,end in ((0,34),(34,38)):
        subprocess.run([sys.executable,str(script),str(start),str(end)],cwd=out,check=True)
    print(f'Replay complete: {r / "raw_results/benchmark_v3_replay.json"}')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('benchmark_replay_new'))
    main(p.parse_args().output.resolve())
