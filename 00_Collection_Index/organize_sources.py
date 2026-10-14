"""Scoped reversible organization. Originals move only after a verified copy exists."""
from snapshot import ROOT,OUT,sha,dump
from audit_archives import safe_member
import pathlib,json,shutil,zipfile,hashlib,os,stat
B=json.loads((OUT/'baseline_sources.json').read_text(encoding='utf-8'))
operations=[]
def checked_copy(src,dst,expected=None):
    expected=expected or sha(src)
    if dst.exists():
        assert sha(dst)==expected, f'Refusing overwrite: {dst}'
        return
    dst.parent.mkdir(parents=True,exist_ok=True)
    with open(src,'rb') as a,open(dst,'xb') as b:shutil.copyfileobj(a,b)
    shutil.copystat(src,dst)
    assert sha(dst)==expected,f'Copy mismatch: {dst}'
def stage_archive(src,key,select=None):
    stage=OUT/'Extraction_Staging'/key;stage.mkdir(parents=True,exist_ok=True)
    members=[]; seen=set()
    with zipfile.ZipFile(src) as z:
        for info in z.infolist():
            if select is not None and not select(info.filename):continue
            assert safe_member(info.filename) and not stat.S_ISLNK(info.external_attr>>16)
            q=stage/info.filename.replace('\\','/')
            assert q.resolve().is_relative_to(stage.resolve())
            folded=str(q.resolve()).casefold();assert folded not in seen,f'Duplicate case-insensitive archive destination: {q}';seen.add(folded)
            if info.is_dir():q.mkdir(parents=True,exist_ok=True);continue
            data=z.read(info);h=hashlib.sha256(data).hexdigest()
            if q.exists():assert sha(q)==h
            else:
                q.parent.mkdir(parents=True,exist_ok=True)
                with open(q,'xb') as f:f.write(data)
            assert sha(q)==h
            members.append({'member':info.filename,'sha256':h,'size':len(data),'staging_path':q.relative_to(ROOT).as_posix()})
    return stage,members
def expose(src,key,destination,select=None):
    stage,ms=stage_archive(src,key,select)
    for m in ms:
        dst=destination/m['member'];checked_copy(ROOT/m['staging_path'],dst,m['sha256'])
        operations.append({'action':'verified_archive_extraction','archive_source':str(src.relative_to(ROOT)) if src.is_relative_to(ROOT) else str(src),'archive_sha256':sha(src),'member':m['member'],'destination':dst.relative_to(ROOT).as_posix(),'sha256':m['sha256'],'size':m['size'],'staging_path':m['staging_path']})
def main():
    specs=[('Finite Jet Rigitity (Paper A)','Finite_Jet_FINAL_SUBMISSION_PACKAGE_2026-09-27.zip','FINAL_REVIEWED_PACKAGE_2026-09-27','finite_jet'),('Guarded Boolean Operator (Paper B)','Guarded_Boolean_Paper_B_Reviewed_2026-09-28.zip','REVIEWED_PACKAGE_2026-09-28','guarded'),('Intrinsic Boolean CM Phase Algebra','CM_Phase_Research_Revision_2026-09-28.zip','REVIEWED_PACKAGE_2026-09-28','intrinsic')]
    for folder,archive,dest,key in specs:expose(ROOT/folder/archive,key,ROOT/folder/dest)
    # Restore an archive-supplied expected filename; keep the user's renamed copy.
    folder='Signed Integral CM Phase Calculus'
    expose(ROOT/folder/'CM_Phase_Calculus_Submission_Revision_2026-09-27.zip','signed_source_filename',ROOT/folder,lambda n:n=='CM_Phase_Calculus_Submission_Revision/paper.tex')
    # Keep external current convergence evidence locally as intact packages and expose only reading entry points.
    folder=ROOT/'CM Structural Computation and Decomposition (Research Direction)'/'CONVERGENCE_EVIDENCE_2026-09-28'
    for name in ['CM_Structural_Computation_C1-C4_T3_Phase2_2026-09-28.zip','CM_Convergence_Audit_and_Computation_Preparation_2026-09-28.zip']:
        src=pathlib.Path('C:/Users/brian/Documents/CM_Computation')/name;dst=folder/'Original_Packages'/name
        checked_copy(src,dst)
        operations.append({'action':'copy_external_package','source':str(src),'destination':dst.relative_to(ROOT).as_posix(),'sha256':sha(src),'size':src.stat().st_size})
        def selected(n):
            parts=n.split('/')
            return len(parts)==2 and pathlib.PurePosixPath(n).suffix in ('.md','.csv') and any(x in parts[-1].upper() for x in ('HANDOFF','README','LEDGER','MANIFEST','REPORT','SUMMARY','REPRODUC'))
        expose(dst,'external_'+('t3' if 'T3_Phase2' in name else 'convergence'),folder/'Reading_Entry_Points',selected)
    # Move only the unambiguous root ZIP snapshots. Both safety copy and original are retained.
    for f in B:
        rel=f['original_path']
        if '/' in rel or not rel.lower().endswith('.zip'):continue
        src=ROOT/rel;copy=ROOT/'90_Preserved_Sources'/'Verified_PreMove_Copies'/rel;dst=ROOT/'90_Preserved_Sources'/'Former_Root_ZIPs'/rel
        assert src.resolve().parent==ROOT.resolve()
        assert copy.resolve().is_relative_to(ROOT.resolve()) and dst.resolve().is_relative_to(ROOT.resolve())
        checked_copy(src,copy,f['sha256'])
        assert sha(src)==f['sha256'] and not dst.exists()
        dst.parent.mkdir(parents=True,exist_ok=True);src.rename(dst)
        assert sha(dst)==f['sha256'] and sha(copy)==f['sha256']
        operations.append({'action':'relocate_after_verified_copy','source':rel,'destination':dst.relative_to(ROOT).as_posix(),'verified_copy':copy.relative_to(ROOT).as_posix(),'sha256':f['sha256'],'size':f['size']})
    dump('organization_operations.json',operations)
    print(json.dumps({'operations':len(operations),'root_zips_moved':sum(x['action']=='relocate_after_verified_copy' for x in operations),'archive_files_exposed':sum(x['action']=='verified_archive_extraction' for x in operations)}))
if __name__=='__main__':main()
