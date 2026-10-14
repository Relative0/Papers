"""Read public artifacts and compare with the reviewed local release."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import urllib.parse
import urllib.request

site = Path(__file__).resolve().parent.parent / 'sf-site-release/deliverables_n22_24/master_explainer_2026_08_03'
prefix = 'results/2026-09-30/research-register/'
base = 'https://relative0.github.io/Correspondence_Matrices/'
manifest = json.loads((site / prefix / 'artifact-manifest.json').read_text(encoding='utf-8'))
entries = {prefix+k:v for k,v in manifest['files'].items()}
for name in [prefix+'artifact-manifest.json','p-series-study-guide.html']:
    data=(site/name).read_bytes()
    entries[name]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}

def check(item):
    name,expected=item
    url=base+urllib.parse.quote(name,safe='/')+'?release=27b2f365'
    size=0; h=hashlib.sha256()
    with urllib.request.urlopen(url,timeout=90) as response:
        while block:=response.read(1024*1024):
            size+=len(block);h.update(block)
    assert size==expected['bytes'] and h.hexdigest()==expected['sha256'],name
    return name

with ThreadPoolExecutor(max_workers=6) as pool:
    verified=list(pool.map(check,entries.items()))
receipt={'status':'PASS','release_commit':'27b2f365','public_artifacts_verified':len(verified),
         'bytes_verified':sum(x['bytes'] for x in entries.values()),'paths':verified}
(Path(__file__).resolve().parent/'LIVE_VERIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in receipt.items() if k!='paths'}))
