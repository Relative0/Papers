from pathlib import Path
import hashlib,json,platform,sys,importlib.metadata
from lifecycle import environment
ROOT=Path(__file__).resolve().parent
result=environment()
try:result['dependency_versions']['numpy']=importlib.metadata.version('numpy')
except importlib.metadata.PackageNotFoundError:pass
try:
    from dd import cudd
    p=Path(cudd.__file__)
    result['compiled_cudd']={'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
except ImportError:result['compiled_cudd']=None
cpu=Path('/proc/cpuinfo');mem=Path('/proc/meminfo')
if cpu.exists():result['cpu_model']=next((x.split(':',1)[1].strip() for x in cpu.read_text().splitlines() if x.startswith('model name')),None)
if mem.exists():result['mem_total']=next((x for x in mem.read_text().splitlines() if x.startswith('MemTotal:')),None)
result['wheels']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'runtime/wheels').glob('*.whl')}
result['runpod']='not used'
dest=ROOT/'runtime'/('environment-'+sys.platform+'.json')
dest.write_text(json.dumps(result,indent=2));print(dest)
