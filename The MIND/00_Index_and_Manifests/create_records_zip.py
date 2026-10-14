from pathlib import Path
import hashlib,json,zipfile
A=Path(__file__).resolve().parent
names=[
 'collection_manifest.json',
 'FOLDER_TREE.txt',
 'THEME_CROSSWALK.md',
 'README.md',
 'source_manifest.json',
 'source_manifest.csv',
 'folder_manifest.json',
 'archive_occurrence_manifest.json',
 'archive_members_final.json',
 'linked_related_archive_members.json',
 'duplicate_groups.json',
 'manuscript_version_catalog.json',
 'final_verification.json',
 'FINAL_VERIFICATION.md',
 'unresolved_source_manifest.json',
 'UNRESOLVED_AND_ACCESS.md',
 'reference_register_final.json',
 'paper_theme_crosswalk.json',
 'NEXT_AGENT_ORIGINAL_THEMES_ANALYSIS_PROMPT.md',
]
def sha(b):return hashlib.sha256(b).hexdigest()
payload={n:(A/n).read_bytes() for n in names}
payload['PACKAGE_CONTENTS_SHA256.json']=json.dumps({'purpose':'Four requested entry files plus the records they reference and the next-agent prompt','files':{n:{'bytes':len(b),'sha256':sha(b)} for n,b in payload.items()}},indent=2).encode('utf-8')
name='MIND_Collection_Records_2026-09-30.zip';dest=A/name;temp=A/(name+'.building')
with temp.open('xb') as stream:
 with zipfile.ZipFile(stream,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for n,b in payload.items():
   info=zipfile.ZipInfo(n,date_time=(2026,9,30,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
   z.writestr(info,b)
with zipfile.ZipFile(temp) as z:
 assert z.testzip() is None
 assert set(z.namelist())==set(payload)
 for n,b in payload.items():assert z.read(n)==b,n
temp.replace(dest)
receipt={'archive':str(dest),'bytes':dest.stat().st_size,'sha256':sha(dest.read_bytes()),'file_count':len(payload),'crc':'PASS','member_sha256':'ALL PASS','four_requested_files':['collection_manifest.json','FOLDER_TREE.txt','THEME_CROSSWALK.md','README.md']}
(A/(name+'.receipt.json')).write_text(json.dumps(receipt,indent=2),encoding='utf-8')
print(json.dumps(receipt,indent=2))
