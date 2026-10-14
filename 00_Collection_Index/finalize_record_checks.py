"""Check completed record links and hash the generated record set after reconciliation."""
from snapshot import ROOT,OUT,sha,dump
from reconcile_collection import local_links
import json,pathlib,re,urllib.parse,datetime,subprocess,collections,os
def main():
    old=json.loads((OUT/'readme_link_checks.json').read_text(encoding='utf-8'))
    rows=[]
    for r in old:
        if r['status']=='EXCLUDED_MIND_CONTENT':rows.append(r);continue
        r['status']='PASS' if (ROOT/r['target']).exists() else 'MISSING';rows.append(r)
    dump('readme_link_checks.json',rows)
    final=json.loads((OUT/'final_verification.json').read_text(encoding='utf-8'))
    final['new_navigation_broken_links']=[r for r in rows if r['new'] and r['status']=='MISSING']
    final['new_navigation_local_links_checked']=sum(r['new'] and r['status']!='EXCLUDED_MIND_CONTENT' for r in rows)
    final['final_record_check_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    before=(OUT/'git_status_before.txt').read_text(encoding='utf-8').split('\nSTDERR:')[0].splitlines()
    r=subprocess.run(['git','-c','core.quotepath=false','status','--short'],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
    (OUT/'git_status_after.txt').write_text(r.stdout+'\nSTDERR:\n'+r.stderr,encoding='utf-8')
    after=r.stdout.splitlines()
    head=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,text=True).stdout.strip()
    oldhead=(OUT/'git_head_before.txt').read_text().splitlines()[0].strip()
    staged=subprocess.run(['git','diff','--cached','--stat'],cwd=ROOT,capture_output=True,text=True).stdout
    final['git_head_unchanged']=head==oldhead;final['staged_diff_empty']=not staged.strip()
    dump('git_status_delta.json',{'added_status_entries':sorted(set(after)-set(before)),'removed_status_entries':sorted(set(before)-set(after)),'head_before':oldhead,'head_after':head,'staged_diff_stat':staged,'baseline_note':'Initial bookkeeping folder was created before the saved Git baseline; original working-tree state was read before that creation.'})
    dump('final_verification.json',final)
    assert final['source_preservation_pass']
    assert not final['new_navigation_broken_links']
    assert not final['introduced_broken_original_links']
    assert final['git_head_unchanged'] and final['staged_diff_empty']
    lines=['Papers for Publication/']
    for base,ds,fs in os.walk(ROOT):
        p=pathlib.Path(base);depth=len(p.relative_to(ROOT).parts)
        if p==ROOT:ds[:]=sorted(d for d in ds if d not in ('.git','The MIND'))
        else:ds.sort()
        if p!=ROOT:lines.append('  '*depth+p.name+'/')
        for n in sorted(fs):lines.append('  '*(depth+1)+n)
    lines+=['  The MIND/ [contents excluded; unchanged by this task]','  .git/ [contents excluded]']
    (OUT/'FOLDER_TREE.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    files=[]
    for p in OUT.rglob('*'):
        if p.is_file() and p.name!='collection_records_manifest.json':files.append({'path':p.relative_to(OUT).as_posix(),'size':p.stat().st_size,'sha256':sha(p)})
    dump('collection_records_manifest.json',{'scope':'All generated collection record, staging and verification files except this integrity manifest itself','files':files})
    print(json.dumps({'preservation':final['source_preservation_pass'],'new_navigation_links_checked':final['new_navigation_local_links_checked'],'new_broken_links':len(final['new_navigation_broken_links']),'introduced_broken_original_links':len(final['introduced_broken_original_links']),'concurrent_changes_with_verified_baselines':len(final['concurrent_original_path_changes_with_baseline_recovered']),'head_unchanged':final['git_head_unchanged'],'staged_diff_empty':final['staged_diff_empty'],'record_files_hashed':len(files)},indent=2))
if __name__=='__main__':main()
