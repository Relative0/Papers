"""Read-only portable verification of the 2026-09-25 publication partition.
Run: python verify_partition.py [repository-root]
Uses only Python's standard library; no credentials, network or file writes.
"""
import pathlib,sys,json,hashlib,csv,subprocess
REG='CM-LM Publication Program - Reviews and Registers'
root=pathlib.Path(sys.argv[1]).resolve() if len(sys.argv)>1 else pathlib.Path(__file__).resolve().parents[3]
evidence=root/REG/'10_UNIQUE_PROJECT_PARTITION_20260925'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
mapping=read(evidence/'complete_preservation_map.json');projects=read(evidence/'projects.json');receipt=read(root/'PARTITION_VERIFICATION_RECEIPT.json')
cache={}
for x in mapping:
 p=(root/x['retained']).resolve();assert p.is_relative_to(root),x
 if p not in cache:cache[p]=sha(p)
 assert cache[p]==x['sha256'],x
assert len(mapping)==1086 and len({x['sha256'] for x in mapping})==597
checks=0
for m in receipt['manifests']:
 p=root/m['path'];assert sha(p)==m['sha256'],str(p)
 with p.open(encoding='utf-8',newline='') as stream:
  for row in csv.DictReader(stream):
   f=p.parent/row['RelativePath'];assert sha(f)==row['SHA256'] and f.stat().st_size==int(row['Bytes']),str(f);checks+=1
for p in projects:
 for rel in ['README_FIRST.md','CLAIMS_AND_UNIQUENESS.md','SOURCE_MANIFEST_SHA256.csv',p['source']]:assert (root/p['folder']/rel).is_file()
report=root/'CM_LM_UNIQUE_PROJECT_PARTITION_AND_OVERLAP_REPORT.md';assert sha(report)==receipt['report_sha256'];assert report.read_bytes()==(root/REG/report.name).read_bytes()
assert not (root/'CM_LM_PUBLICATION_PORTFOLIO_20260921').exists()
for x in read(evidence/'content_inventory_after.json')['files']:assert sha(root/x['path'])==x['sha256'],x['path']
git={}
try:
 git['commit']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True,stderr=subprocess.STDOUT).strip()
 git['status']=subprocess.check_output(['git','status','--short'],cwd=root,text=True,stderr=subprocess.STDOUT).strip()
except subprocess.CalledProcessError as e:git['read_error']=e.output.strip()
print(json.dumps(dict(result='PASS',original_instances_preserved=len(mapping),original_byte_streams_preserved=597,projects=len(projects),manifest_file_checks=checks,git=git),indent=2))
