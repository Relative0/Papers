"""C1 adapter checks. External Astra oracle remains unmodified and attributed.

Oracle coordinate j is bit j (LSB). Project coordinate v is bit n-1-v.
Truth integers agree; translate coordinate labels, never reverse truth bytes.
"""
from pathlib import Path
import argparse, hashlib, importlib.util, itertools, json, platform, subprocess, sys, time

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent
AUDIT=ROOT/'inputs/external_audit/ASTRA_Convergence_Audit_2026-09-28'
BASE=ROOT/'inputs/baseline/CM_COMPUTATION_BASELINE_HANDOFF/reproducibility/code'
sys.path.insert(0,str(ROOT/'main_source_snapshot' if (ROOT/'main_source_snapshot').exists() else REPO));sys.path.insert(0,str(BASE))
from artifacts import Artifact, matrix_rows, rank_factor, restrict_table, walsh_count
from cmbench.recognition.gf2_decomposition import gf2_rank_factor, _unpartition
from cmbench.recognition.natural_decomposition import partitioned_bits

spec=importlib.util.spec_from_file_location('external_astra_oracle',AUDIT/'EVIDENCE/independent_math_audit.py')
oracle=importlib.util.module_from_spec(spec);spec.loader.exec_module(oracle)

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main(output):
    output.mkdir(parents=True,exist_ok=False)
    start=time.perf_counter()
    counts={'all_4x4_factorizations':0,'restricted_profile_comparisons':0,'permuted_cut_comparisons':0,
            'zero_constant_unequal_cut_comparisons':0,'cumulative_update_comparisons':0}
    query_hash=hashlib.sha256()
    masks=oracle.query_masks(4,4,False)
    for f in range(65536):
        rows=tuple(oracle.matrix_rows(f,2,2))
        rank,coef,basis=gf2_rank_factor(rows,4)
        assert rank==len(oracle.gf2_basis(rows))
        a,b=rank_factor(rows)
        assert len(b)==rank
        counts['all_4x4_factorizations']+=1
        if rank>2:continue
        art=Artifact('rank',(0,1,2,3),((0,1),(2,3),coef,basis))
        assert matrix_rows(f,(0,1,2,3),(0,1))[0]==rows
        for S,value,mask in masks:
            rho={3-j:(value>>j)&1 for j in S}
            want=(f&mask).bit_count()
            residual=art.condition(rho)
            assert art.query_fused(rho)==residual.count()==walsh_count(residual)==want
            rb,scope=restrict_table(f,(0,1,2,3),rho)
            assert rb.bit_count()==want and residual.scope==scope
            query_hash.update(f'{f}:{S}:{value}:{want}\n'.encode())
            counts['restricted_profile_comparisons']+=1
    # Reversed and noncontiguous cuts expose conversions hidden by symmetric parity.
    for n in range(2,6):
        fs={0,(1<<(1<<n))-1,oracle.parity(n),0x9 & ((1<<(1<<n))-1)}
        fs.update(1<<x for x in range(1<<n))
        cuts={(0,),tuple(range(n//2)),tuple(reversed(range(n//2))),tuple(range(0,n,2))}
        for left in sorted(cuts):
            right=tuple(v for v in range(n) if v not in left)
            for f in sorted(fs):
                rows,rr=matrix_rows(f,tuple(range(n)),left)
                arranged,lp,rp=partitioned_bits(f,n,left)
                assert (lp,rp)==(len(left),len(right))
                assert _unpartition(arranged,n,left)==f
                want_rows=tuple((arranged>>(i*(1<<len(right)))) & ((1<<(1<<len(right)))-1) for i in range(1<<len(left)))
                assert rows==want_rows and rr==right
                r,u,v=gf2_rank_factor(rows,1<<len(right))
                art=Artifact('rank',tuple(range(n)),(left,right,u,v))
                for S,value,mask in oracle.query_masks(n,n,False):
                    rho={n-1-j:(value>>j)&1 for j in S}
                    assert art.query_fused(rho)==(f&mask).bit_count()
                    counts['permuted_cut_comparisons']+=1
                    if f in (0,(1<<(1<<n))-1):counts['zero_constant_unequal_cut_comparisons']+=1
                    # Residual names stay original; no silent coordinate renumbering.
                    state=art
                    for key,val in sorted(rho.items()):state=state.condition({key:val})
                    assert state.count()==(f&mask).bit_count()
                    counts['cumulative_update_comparisons']+=1
                    query_hash.update(f'{n}:{left}:{f}:{rho}\n'.encode())
    for n in (0,1):
        for f in range(1<<(1<<n)):
            for S,value,mask in oracle.query_masks(n,n,False):
                rho={n-1-j:(value>>j)&1 for j in S}
                assert Artifact('flat',tuple(range(n)),(f,)).query(rho)==(f&mask).bit_count()
                counts['zero_constant_unequal_cut_comparisons']+=1
    # The histogram and horizon obstructions are contract tests, not performance claims.
    f,g=8,2  # xy and (1-x)y in MSB coordinate order (x,y).
    assert f.bit_count()==g.bit_count()==1
    assert Artifact('flat',(0,1),(f,)).query({0:0})==0
    assert Artifact('flat',(0,1),(g,)).query({0:0})==1
    source_hashes={str(Path(m.__file__).resolve().relative_to(REPO)):sha(Path(m.__file__))
                   for m in list(sys.modules.values()) if getattr(m,'__file__',None)
                   and Path(m.__file__).resolve().is_relative_to(REPO)
                   and not Path(m.__file__).resolve().is_relative_to(REPO/'.venv')}
    result={'status':'PASS','counts':counts,'query_sha256':query_hash.hexdigest(),
            'source_sha256':source_hashes,'python':sys.version,'platform':platform.platform(),
            'elapsed_seconds':time.perf_counter()-start,
            'attribution':'Imported external Astra 2026-09-28 oracle; local adapter and main implementation comparisons are new.',
            'coordinate_mapping':'MSB_project_coordinate = n - 1 - LSB_oracle_coordinate; integer truth bits unchanged'}
    (output/'integration_results.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({'status':'PASS','counts':counts,'query_sha256':query_hash.hexdigest()},indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True)
    main(ap.parse_args().output)
