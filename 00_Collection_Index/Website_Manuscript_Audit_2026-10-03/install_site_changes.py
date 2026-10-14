"""Apply the requested local author correction after validating all old/new hashes."""
from pathlib import Path
import hashlib, json, shutil

OUT=Path(__file__).resolve().parent
SITE=Path(r'C:\Users\brian\Documents\B-Theory\Website').resolve()
STAGE=OUT/'prepared_website'
changes=json.loads((OUT/'website_changes.json').read_text(encoding='utf-8'))
originals=json.loads((OUT/'provenance_before.json').read_text(encoding='utf-8'))
corrected=json.loads((OUT/'author_correction_verification.json').read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def within_site(p):
    assert p.resolve().is_relative_to(SITE),p
    return p

operations=[]
for item in changes:
    target=within_site(SITE/item['path'])
    assert sha(target)==item['before_sha256'],f'Changed since preparation: {target}'
    assert sha(STAGE/item['path'])==item['after_sha256']
for item in corrected:
    new=within_site(SITE/'public/manuscripts'/item['file'])
    old=within_site(new.with_name(new.name.replace('-r2-','-r1-')))
    history=within_site(SITE/'manuscript-history/reading-copy-1'/old.name)
    record=next(r for r in originals if Path(r['site_file']).name==old.name)
    assert sha(old)==record['sha256']
    assert sha(OUT/'original_site_pdfs'/old.name)==record['sha256']
    assert sha(STAGE/'public/manuscripts'/new.name)==item['sha256']
    assert not new.exists() and not history.exists()
    operations.append((old,new,history,item))

# Preserve each exact old PDF in local history before installing its new release.
for old,new,history,item in operations:
    history.parent.mkdir(parents=True,exist_ok=True)
    old.rename(history)
    shutil.copy2(STAGE/'public/manuscripts'/new.name,new)
    assert sha(new)==item['sha256']
for item in changes:
    target=within_site(SITE/item['path'])
    target.write_bytes((STAGE/item['path']).read_bytes())
    assert sha(target)==item['after_sha256']
receipt=dict(status='applied',website=str(SITE),text_files=changes,pdf_files=corrected,retired_files=[str(h) for _,_,h,_ in operations],external_publication=False)
(OUT/'website_installation_receipt.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
print(json.dumps(dict(status='applied',changed_text_files=len(changes),corrected_pdfs=len(corrected),preserved_original_pdfs=len(operations),external_publication=False)))
