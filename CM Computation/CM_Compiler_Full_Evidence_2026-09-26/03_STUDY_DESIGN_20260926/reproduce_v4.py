"""Run the frozen v4 method into a new, never-overwritten output directory."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import shutil

import study_v4

HERE = Path(__file__).resolve().parent
ORIGINAL = HERE/'run_v4_001'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True,
                        help='New direct child of this study directory')
    args = parser.parse_args()
    output = args.output.resolve()
    project = HERE.parent.resolve()
    if output.parent != HERE.resolve() or output.exists():
        raise SystemExit('Output must be a new direct child of this study directory')
    freeze = json.loads((ORIGINAL/'FREEZE.json').read_text(encoding='utf-8'))
    for relative, identity in freeze['files'].items():
        path = project/relative
        if relative.endswith(('TIMING.jsonl','MEMORY.jsonl','FAILURES.jsonl')):
            continue
        if sha256(path.read_bytes()).hexdigest()!=identity['sha256']:
            raise SystemExit(f'Frozen input changed: {relative}')
    output.mkdir(parents=True)
    for name in ('FREEZE.json','CORPUS.jsonl','RUN_CONFIG.json','ENVIRONMENT.json'):
        shutil.copyfile(ORIGINAL/name, output/name)
    for name in ('TIMING.jsonl','MEMORY.jsonl','FAILURES.jsonl'):
        (output/name).write_bytes(b'')
        expected = freeze['files'][(ORIGINAL/name).relative_to(project).as_posix()]['sha256']
        assert sha256((output/name).read_bytes()).hexdigest()==expected
    study_v4.RUN = output
    study_v4.run()
    study_v4.analyze()
    print(f'Replication output: {output}')

if __name__=='__main__':
    main()
