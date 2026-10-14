"""Final source/archive reconciliation, exact duplicate mapping and navigational checks."""
from snapshot import ROOT,OUT,sha,dump
from build_navigation import write_new,link
import json,pathlib,os,collections,csv,re,urllib.parse,posixpath,subprocess,datetime
def load(n):return json.loads((OUT/n).read_text(encoding='utf-8'))
def local_links(text):
    # Balanced parentheses allow ordinary Windows filenames with spaces/parentheses.
    out=[]
    for match in re.finditer(r'\]\(',text):
        i=match.end()
        if i<len(text) and text[i]=='<':
            end=text.find('>',i+1)
            if end>=0:out.append(text[i+1:end])
            continue
        start=i;level=1
        while i<len(text) and level:
            if text[i]=='(':level+=1
            elif text[i]==')':level-=1
            i+=1
        if level==0:out.append(text[start:i-1])
    return out
def main():
    B=load('baseline_sources.json');D=load('baseline_directories.json');E=load('external_sources.json');A=load('archive_catalog.json');OP=load('organization_operations.json');P=load('paper_catalog.json')
    moves={x['source']:x for x in OP if x['action']=='relocate_after_verified_copy'}
    original_ops={x['source']:x for x in OP if x['action'] in ('relocate_after_verified_copy','retained_original_after_workflow_check')}
    recoveries={x['original_path']:x for x in load('concurrent_baseline_recovery.json')} if (OUT/'concurrent_baseline_recovery.json').exists() else {}
    roots={p['home']:p for p in P};originals={x['original_path'] for x in B};source_rows=[];fail=[];concurrent=[]
    groups=collections.defaultdict(lambda:{'file_locations':[],'archive_members':[]});actuals={};generated=[]
    def role(path):
        s=path.lower()
        if s.endswith('.zip'):return 'original_delivery_package'
        if any(v in s for v in ['review','audit','referee','scorecard']):return 'review_or_audit'
        if any(v in s for v in ['manifest','receipt','checksum','sha256']):return 'provenance_or_integrity_record'
        if any(v in s for v in ['history/','historical','original_snapshot','prior_version','legacy']):return 'historical_source'
        if any(v in s for v in ['reproduc','verification','code/','data/','test','benchmark','runtime','supplement']):return 'reproducibility_or_support'
        if s.endswith(('.tex','.pdf','.bib')):return 'manuscript_or_scientific_support'
        return 'research_or_navigation'
    for f in B:
        rel=f['original_path'];dest=moves.get(rel,{}).get('destination',rel);p=ROOT/dest
        h=sha(p) if p.exists() and f['sha256'] else None
        unchanged=h==f['sha256'] if f['sha256'] else None
        recovery=recoveries.get(rel)
        if unchanged is False:
            if recovery and sha(ROOT/recovery['baseline_preserved_location'])==f['sha256']:
                concurrent.append({'original_path':rel,'before':f['sha256'],'current_sha256':h,'baseline_preserved_location':recovery['baseline_preserved_location'],'evidence':'concurrent_workflow_evidence.json'})
                dest=recovery['baseline_preserved_location']
            else:fail.append({'original_path':rel,'destination':dest,'before':f['sha256'],'after':h})
        owner=roots.get(rel.split('/')[0],{}).get('id')
        if '/CM_Structural_Computation_Final_Research_Package/' in rel:owner='SC'
        if rel.startswith(('Paper_U_','Structured Factorization/')):owner='MIND-linked preserved workflow'
        if rel.startswith('B-Theory Website/'):owner='website delivery copies'
        source_rows.append({**f,'scope':'workspace_original','organized_location':dest,'additional_verified_copy':original_ops.get(rel,{}).get('verified_copy'),'owner':owner,'role':role(rel),'unchanged':unchanged,'disposition':'baseline preserved after independently confirmed concurrent workflow edit; live path untouched' if recovery and unchanged is False else 'relocated original after verified copy' if rel in moves else 'retained at original path','duplicate_group_sha256':f['sha256']})
    for f in E:
        copies=[x['destination'] for x in OP if x.get('source')==f['original_path'] and x['action']=='copy_external_package']
        source_rows.append({**f,'scope':'specifically_referenced_external_package','organized_location':copies[0] if copies else f['original_path'],'original_retained':True,'unchanged':sha(pathlib.Path(f['original_path']))==f['sha256'],'role':'external_delivery_package','disposition':'verified local package copy; external original retained' if copies else 'original external location retained; archived members catalogued without duplicate extraction','duplicate_group_sha256':f['sha256']})
        groups[f['sha256']]['file_locations'].append(f['original_path'])
    # Final inventory excludes The MIND/.git and our own record directory; staging/test copies are tracked separately by operations.
    for base,ds,fs in os.walk(ROOT):
        if pathlib.Path(base)==ROOT:ds[:]=[d for d in ds if d not in ('.git','The MIND','00_Collection_Index')]
        for n in fs:
            p=pathlib.Path(base)/n;rel=p.relative_to(ROOT).as_posix()
            if n.startswith('.env'):continue
            h=sha(p);actuals[rel]={'sha256':h,'size':p.stat().st_size};groups[h]['file_locations'].append(rel)
            if rel not in originals and rel not in {m['destination'] for m in moves.values()}:generated.append({'path':rel,**actuals[rel]})
    for h,a in A.items():
        for m in a['members']:
            if m.get('sha256'):groups[m['sha256']]['archive_members'].append({'archive_sha256':h,'index':m['index'],'member':m['path'],'size':m['size']})
    dump('source_manifest.json',source_rows)
    fields=['scope','original_path','size','sha256','organized_location','additional_verified_copy','owner','role','unchanged','disposition','duplicate_group_sha256']
    with open(OUT/'source_manifest.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fields,extrasaction='ignore');w.writeheader();w.writerows(source_rows)
    dump('folder_manifest.json',[{**d,'organized_location':d['original_path'],'exists':(ROOT/d['original_path']).is_dir(),'disposition':'original directory retained'} for d in D])
    dump('duplicate_groups.json',{h:g for h,g in groups.items() if len(g['file_locations'])+len(g['archive_members'])>1})
    # Every occurrence is represented, including duplicate archives and arbitrarily repeated nested packages.
    count=0;archive_only=0;dirs=0
    with open(OUT/'archive_occurrence_manifest.jsonl','w',encoding='utf-8') as out,open(OUT/'archive_occurrence_manifest.csv','w',newline='',encoding='utf-8') as cf:
        fields=['source_archive_path','organized_archive_path','archive_chain','member_index','member','directory','size','sha256','organized_location','disposition'];w=csv.DictWriter(cf,fields);w.writeheader()
        def expand(h,original,dest,chain='',depth=0):
            nonlocal count,archive_only,dirs
            assert depth<=12
            for m in A[h]['members']:
                locs=groups.get(m.get('sha256'),{}).get('file_locations',[])
                # Prefer a workspace file over a Downloads source; no inferred MIND file locations.
                loc=next((s for s in locs if not pathlib.Path(s).is_absolute()),locs[0] if locs else None)
                disposition='exact bytes mapped to retained file' if loc else 'retained in intact archive; extraction unnecessary for selected reading heads'
                if m['directory']:disposition='directory entry retained in intact archive';dirs+=1
                elif not loc:archive_only+=1
                row={'source_archive_path':original,'organized_archive_path':dest,'archive_chain':chain,'member_index':m['index'],'member':m['path'],'directory':m['directory'],'size':m['size'],'sha256':m.get('sha256'),'organized_location':loc or (dest+'!/'+chain+m['path']),'disposition':disposition}
                out.write(json.dumps(row,ensure_ascii=False)+'\n');w.writerow(row);count+=1
                if m.get('nested_archive_sha256'):expand(m['nested_archive_sha256'],original,dest,chain+m['path']+'!/',depth+1)
        for f in B+E:
            if f['original_path'].lower().endswith('.zip'):
                dest=next(s['organized_location'] for s in source_rows if s['original_path']==f['original_path'])
                expand(f['sha256'],f['original_path'],dest)
    # All archive extraction and copy operations checked against the intended bytes, including staging.
    opfail=[]
    for op in OP:
        if sha(ROOT/op['destination'])!=op['sha256']:opfail.append(op['destination'])
        for key in ['verified_copy','staging_path']:
            if op.get(key) and sha(ROOT/op[key])!=op['sha256']:opfail.append(op[key])
    # Readme/link checks distinguish inherited broken links from generated navigation.
    links=[];newbroken=[];oldbroken=[];introduced=[]
    baseline_paths=originals|{d['original_path'] for d in D}|{'.','The MIND','.git'}
    mdpaths=[ROOT/f['original_path'] for f in B if f['original_path'].endswith('.md')]
    mdpaths += [ROOT/'README.md',*ROOT.glob('*/COLLECTION_README.md'),ROOT/'90_Preserved_Sources/README.md',*OUT.glob('*.md')]
    for p in dict.fromkeys(mdpaths):
        if not p.exists():continue
        rel=p.relative_to(ROOT).as_posix();isnew=rel not in originals
        text=p.read_text(encoding='utf-8-sig',errors='replace')
        for raw in local_links(text):
            raw=urllib.parse.unquote(raw.split('#')[0])
            if not raw or re.match(r'^(https?|mailto|app|codex|sandbox|data):',raw):continue
            raw=raw.replace('\\','/')
            target=(p.parent/raw).resolve()
            if not target.is_relative_to(ROOT.resolve()):continue
            rtarget=target.relative_to(ROOT).as_posix()
            if rtarget.startswith('The MIND/') and rtarget!='The MIND/README.md':
                links.append({'file':rel,'target':rtarget,'status':'EXCLUDED_MIND_CONTENT','new':isnew});continue
            ok=target.exists();row={'file':rel,'target':rtarget,'status':'PASS' if ok else 'MISSING','new':isnew};links.append(row)
            if not ok:(newbroken if isnew else oldbroken).append(row)
            if not ok and not isnew and rtarget in baseline_paths:introduced.append(row)
    dump('readme_link_checks.json',links);dump('inherited_broken_links.json',oldbroken)
    # Website delivery copies.
    web=[]
    for f in B:
        if f['original_path'].startswith('B-Theory Website/'):
            web.append({'source':f['original_path'],'sha256':f['sha256'],'exact_other_file_locations':[x for x in groups[f['sha256']]['file_locations'] if not x.startswith('B-Theory Website/')],'current_paper_matches':[p['id'] for p in P if p['start_sha256']==f['sha256']]})
    dump('website_delivery_map.json',web)
    # MIND-side identity comes from an inspected prior chat, not forbidden filesystem reads.
    mind=[]
    for name,h in [('Paper_U_Resolution_Limited_Ultrametric_Concepts_v0.3.tex','7c50938b401468d412f3df3d7d5b0765bf3aec8af4bc17c8d32983bc55e69c30'),('paper_u_refs_v0.3.bib','401a939eb529b727e3918cbd1e3563899ac32b2dc31dbf16aaa19cc471c22646')]:
        mind.append({'relationship':'exact_duplicate_previously_verified','sha256':h,'currently_verified_sibling_locations':[s for s in groups[h]['file_locations'] if s.startswith('Paper_U_')],'mind_location_reported':'The MIND/01_Papers/02_Hierarchical_Concepts_Paper_U/Current_Manuscript/v0.3_Rebuilt_Referee_Clarifications/'+name,'mind_side_evidence':'Organize The MIND research / prior command output in mind_prior_verification_evidence.json','mind_side_rehashed_this_task':False})
    mind.extend([{'relationship':'reported_shared_precursor_or_preserved_workflow','source':s,'canonical_collection':'The MIND/README.md','basis':'MIND root README and inspected project chats; no new MIND byte comparison'} for s in ['General ProLT Observation Refinement (Research Direction)','Paper_U_Independent_Review_2026-09-29','Paper_U_Fresh_Referee_2026-09-29','Structured Factorization']])
    dump('mind_overlap_map.json',mind)
    # Historical hash versions not located are explicit unresolved entries, not data loss caused by this task.
    claims=load('checksum_claims.json');unlocated={}
    for c in claims:
        if not c['recorded_bytes_retained']:unlocated.setdefault((c['recorded_path'],c['expected_sha256']),c)
    dump('unlocated_historical_hash_versions.json',list(unlocated.values()))
    # Scope exact chat artifact availability without opening MIND or secret stores.
    referenced=[]
    for cp in OUT.glob('chat_evidence*.json'):
        for chat in json.loads(cp.read_text(encoding='utf-8')):
            for turn in chat.get('turns',[]):
                for item in turn['items']:
                    texts=[item['text']] if 'text' in item else [x.get('text','') for x in item.get('content',[]) if x.get('type')=='text']
                    for text in texts:
                        matches=re.findall(r'(?:[Cc]:[\\/])[^\r\n<>"`]+?\.(?:zip|tex|pdf|md|json|csv|txt|bib)(?=[>"`\s\)]|$)',text)
                        matches+=re.findall(r'(?:sandbox:)?/mnt/data/[^\s<>"`\)]+',text)
                        for raw in matches:
                            raw=raw.rstrip('.;,');p=pathlib.Path(raw)
                            if 'The MIND' in raw:status='EXCLUDED_MIND_CONTENT; old chat paths may have moved; use MIND README'
                            elif raw.startswith(('sandbox:','/mnt/')):status='REMOTE_SESSION_ARTIFACT_NOT_LOCALLY_ACCESSIBLE'
                            elif '.env' in raw:status='SENSITIVE_STORE_NOT_READ'
                            elif p.is_file():status='ACCESSIBLE_FILE'
                            elif p.is_relative_to(ROOT) and p.relative_to(ROOT).as_posix() in moves:status='RELOCATED_WITH_VERIFIED_COPY: '+moves[p.relative_to(ROOT).as_posix()]['destination']
                            elif p.exists():status='ACCESSIBLE_DIRECTORY'
                            else:status='NOT_FOUND_AT_REFERENCED_PATH'
                            referenced.append({'thread_id':chat['thread']['id'],'thread_title':chat['thread']['title'],'path':raw,'status':status})
    referenced=list({(x['thread_id'],x['path']):x for x in referenced}.values());dump('chat_artifact_access.json',referenced)
    # Collect archive receipt integrity/count claims that have a directly named archive.
    receipts=[]
    for f in B:
        if 'receipt' not in f['original_path'].lower() or not f['original_path'].endswith('.json'):continue
        try:o=json.loads((ROOT/f['original_path']).read_text(encoding='utf-8-sig'))
        except ValueError:continue
        if not isinstance(o,dict):continue
        h=o.get('sha256');arc=o.get('archive',o.get('zip'))
        if h in A and arc:
            n=len(A[h]['members']);row={'receipt':f['original_path'],'archive':arc,'sha256':h,'archive_hash_located':True,'crc_status':A[h]['crc_status'],'actual_entries':n}
            for k in ['archive_entries','entries']:
                if isinstance(o.get(k),int):row[k+'_claim_matches']=o[k]==n
            receipts.append(row)
    receipt=load_json_path(ROOT/'PARTITION_VERIFICATION_RECEIPT.json')
    receipts.append({'receipt':'PARTITION_VERIFICATION_RECEIPT.json','claim':'report_sha256','expected':receipt['report_sha256'],'actual':sha(ROOT/'CM_LM_UNIQUE_PROJECT_PARTITION_AND_OVERLAP_REPORT.md'),'matches':receipt['report_sha256']==sha(ROOT/'CM_LM_UNIQUE_PROJECT_PARTITION_AND_OVERLAP_REPORT.md')})
    dump('receipt_verification.json',receipts)
    # Preserve Git state snapshots; no index mutation.
    for name,args in [('git_status_after.txt',['status','--short']),('git_diff_stat_after.txt',['diff','--stat']),('git_diff_check_after.txt',['diff','--check'])]:
        r=subprocess.run(['git','-c','core.quotepath=false',*args],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
        (OUT/name).write_text(r.stdout+'\nSTDERR:\n'+r.stderr,encoding='utf-8')
    summary={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'workspace_original_files':len(B),'workspace_original_directories':len(D),'external_packages':len(E),'original_source_changes_or_missing':fail,'operation_verification_failures':opfail,'source_rows':len(source_rows),'archive_occurrences':count,'archive_directory_occurrences':dirs,'archive_only_file_occurrences':archive_only,'unique_zip_streams':len(A),'archive_crc_failures':[h for h,a in A.items() if a['crc_status']!='PASS'],'root_zips_moved':len(moves),'new_navigation_broken_links':newbroken,'inherited_missing_local_links':len(oldbroken),'introduced_broken_original_links':introduced,'unlocated_historical_path_hash_pairs':len(unlocated),'missing_chat_artifact_paths':len({x['path'] for x in referenced if x['status'].startswith(('NOT_FOUND','REMOTE_SESSION'))}),'source_preservation_pass':not fail and not opfail,'notes':['The MIND excluded from traversal; no assertion of a fresh MIND-side duplicate audit.','Original README files and old manifests remain unchanged.','Active sibling workspaces can change after this snapshot; no live-workflow files were written.']}
    summary['concurrent_original_path_changes_with_baseline_recovered']=concurrent
    dump('final_verification.json',summary)
    dump('final_workspace_file_inventory.json',actuals)
    dump('new_collection_files.json',[g for g in generated if not g['path'].startswith('Structured Factorization/')])
    dump('observed_new_live_workflow_files.json',[g for g in generated if g['path'].startswith('Structured Factorization/')])
    lines=['Papers for Publication/']
    for base,ds,fs in os.walk(ROOT):
        p=pathlib.Path(base);rel=p.relative_to(ROOT);depth=len(rel.parts)
        if p==ROOT:ds[:]=sorted(d for d in ds if d not in ('.git','The MIND'))
        else:ds.sort()
        if p!=ROOT:lines.append('  '*depth+p.name+'/')
        for n in sorted(fs):lines.append('  '*(depth+1)+n)
    lines+=['  The MIND/ [contents excluded; unchanged by this task]','  .git/ [contents excluded]']
    (OUT/'FOLDER_TREE.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))
def load_json_path(p):return json.loads(p.read_text(encoding='utf-8'))
if __name__=='__main__':main()
