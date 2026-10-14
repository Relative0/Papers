from pathlib import Path
import difflib, hashlib, json, shutil
from pypdf import PdfReader, PdfWriter

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
SITE = Path(r'C:\Users\brian\Documents\B-Theory\Website')
records = json.loads((OUT/'provenance_before.json').read_text(encoding='utf-8'))
for rec in records:
    p = Path(rec['site_file'])
    assert hashlib.sha256(p.read_bytes()).hexdigest() == rec['sha256']
    dest = OUT/'original_site_pdfs'/p.name
    dest.parent.mkdir(exist_ok=True)
    shutil.copy2(p, dest)

sources = {
    'observation-refinement-r2-v0.5': ROOT/'The MIND/01_Papers/01 Observation Refinement Descent (Research Manuscript)/Current_Manuscript/Observation_Refinement_Descent_and_Cone_Draft_v0.5.tex',
    'hierarchical-concepts-r2-v0.3': ROOT/'The MIND/01_Papers/02 Hierarchical Concepts (Research Note)/Current_Manuscript/v0.3_Original_Fresh_Referee/Paper_U_Resolution_Limited_Ultrametric_Concepts_v0.3.tex',
}
manifest = []
for stem, source in sources.items():
    destdir = OUT/'author_corrected_sources'/stem
    destdir.mkdir(parents=True, exist_ok=True)
    old = source.read_text(encoding='utf-8')
    assert old.count(r'\author{Brian Droncheff}') == 1
    new = old.replace(r'\author{Brian Droncheff}', r'\author{Brian Theory}')
    if 'observation-' in stem:
        assert new.count('pdfauthor={Brian Droncheff}') == 1
        new = new.replace('pdfauthor={Brian Droncheff}', 'pdfauthor={Brian Theory}')
    else:
        new = new.replace(r'\usepackage[hidelinks]{hyperref}', r'\usepackage[hidelinks]{hyperref}'+'\n'+r'\hypersetup{pdfauthor={Brian Theory}}')
        shutil.copy2(source.parent/'paper_u_refs_v0.3.bib', destdir/'paper_u_refs_v0.3.bib')
    dest = destdir/(stem+'.tex')
    dest.write_text(new, encoding='utf-8', newline='\n')
    (destdir/'author_only.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile=str(source),tofile=str(dest))),encoding='utf-8')
    manifest.append(dict(original_source=str(source),original_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),corrected_source=str(dest),corrected_sha256=hashlib.sha256(dest.read_bytes()).hexdigest()))

release = OUT/'prepared_website/public/manuscripts'
release.mkdir(parents=True,exist_ok=True)
source = OUT/'original_site_pdfs/binary-order-thinning-r1-v3.pdf'
reader = PdfReader(source)
writer = PdfWriter(clone_from=reader)
writer.add_metadata({'/Author':'Brian Theory'})
writer.write(release/'binary-order-thinning-r2-v3.pdf')
assert all(a.get_contents().get_data()==b.get_contents().get_data() for a,b in zip(reader.pages,writer.pages))
(OUT/'source_corrections.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(manifest,indent=2))
