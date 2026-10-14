"""Verify historical manifests and independently produced audit artifacts."""
from pathlib import Path
import csv, json, hashlib, platform, importlib.metadata
ROOT=Path(__file__).resolve().parents[1]
def main():
    manifests=[]
    for mf in sorted((ROOT/'source_snapshots').glob('*/MANIFEST_SHA256.txt')):
        missing=[];mismatch=[];checked=0
        for line in mf.read_text().splitlines():
            if not line.strip():continue
            digest, rel=line.split(None,1);p=mf.parent/rel.strip()
            if not p.exists():missing.append(rel);continue
            got=hashlib.sha256(p.read_bytes()).hexdigest();checked+=1
            if got!=digest:mismatch.append(rel)
        manifests.append({'package':mf.parent.name,'checked':checked,'missing':missing,'mismatched':mismatch})
    cardinalities={}
    expected={'resource_inventory_audited_65536.csv':65536,'class_inventory_audited.csv':15,'contextuality_audited_15_classes.csv':15,'measurement_bases_audited_192.csv':192,'teleportation_direct_256x64.csv':16384,'all_resource_branch_rank_audit.csv':64,'dense_coding_64_messages.csv':64,'ghz_tables_audited.csv':27,'bell_tables_audited.csv':9,'shared_restricted_and_quotient_exhaustive.csv':15}
    for name,n in expected.items():
        with (ROOT/'data'/name).open() as f:rows=list(csv.DictReader(f))
        assert len(rows)==n,(name,len(rows),n)
        cardinalities[name]=n
    result={'historical_manifests':manifests,'fresh_csv_cardinalities':cardinalities,'python':platform.python_version(),'platform':platform.platform(),'packages':{p:importlib.metadata.version(p) for p in ('numpy','scipy','sympy','pytest')}}
    (ROOT/'data/artifact_validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
