"""Create a clean, non-overwriting sibling run with the frozen inputs/protocol."""
from pathlib import Path
import shutil,sys

source=Path(__file__).resolve().parents[1]
dest=Path(sys.argv[1]).resolve()
if dest.exists():raise SystemExit('Refusing to overwrite an existing run directory')
if not (dest.parent/'continuity_archive').is_dir():raise SystemExit('Destination needs continuity_archive as a sibling')
dest.mkdir()
for sub in ['code','data','logs','reproduction','reviews']:(dest/sub).mkdir()
for p in (source/'code').glob('*.py'):shutil.copy2(p,dest/'code'/p.name)
for name in ['BENCHMARK_PROTOCOL.md','PROTOCOL_CLARIFICATIONS.md','requirements-lock.txt']:
    shutil.copy2(source/name,dest/name)
shutil.copy2(source/'data'/'benchmark_manifest.json',dest/'data'/'benchmark_manifest.json')
print(dest)
