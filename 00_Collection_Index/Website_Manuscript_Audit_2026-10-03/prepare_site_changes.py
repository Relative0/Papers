from pathlib import Path
import difflib, hashlib, json

OUT=Path(__file__).resolve().parent
SITE=Path(r'C:\Users\brian\Documents\B-Theory\Website')
STAGE=OUT/'prepared_website'
before=json.loads((OUT/'provenance_before.json').read_text(encoding='utf-8'))
after={r['file']:r for r in json.loads((OUT/'author_correction_verification.json').read_text(encoding='utf-8'))}
changes=[]

def write_change(rel,transform):
    source=SITE/rel
    data=source.read_bytes()
    old=data.decode('utf-8')
    new=transform(old)
    assert new!=old, rel
    backup=OUT/'website_files_before'/rel
    backup.parent.mkdir(parents=True,exist_ok=True)
    backup.write_bytes(data)
    dest=STAGE/rel
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(new,encoding='utf-8',newline='')
    changes.append(dict(path=rel,before_sha256=hashlib.sha256(data).hexdigest(),after_sha256=hashlib.sha256(dest.read_bytes()).hexdigest()))
    return ''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile=rel,tofile=rel))

def replace_once(text,old,new):
    assert text.count(old)==1,old
    return text.replace(old,new)

diffs=[]
for slug,filename in [('binary-order-thinning','binary-order-thinning-r1-v3.pdf'),('hierarchical-concepts','hierarchical-concepts-r1-v0.3.pdf'),('observation-refinement','observation-refinement-r1-v0.5.pdf')]:
    def update(t,slug=slug,filename=filename):
        newline='\r\n' if '\r\n' in t else '\n'
        t=replace_once(t,'paperPdf: /manuscripts/'+filename,'paperPdf: /manuscripts/'+filename.replace('-r1-','-r2-')+newline+'paperReadingCopy: 2')
        t=t.replace('paperByline: Brian Droncheff','paperByline: Brian Theory')
        if slug=='hierarchical-concepts':
            t=replace_once(t,'paperSourceVersion: Original fresh-referee v0.3 PDF, dated September 29, 2026; v0.1 and v0.2 retained in revision archives.','paperSourceVersion: Fresh-referee v0.3, September 29, 2026; author corrected October 3, 2026. Original PDF retained in the local history.')
        elif slug=='observation-refinement':
            t=replace_once(t,'paperSourceVersion: Referee-repair draft v0.5, dated September 29, 2026; v0.1–v0.4 retained in revision archives.','paperSourceVersion: Referee-repair draft v0.5, September 29, 2026; author corrected October 3, 2026. Earlier revisions retained in the collection.')
        else:
            t=replace_once(t,'paperSourceVersion: Reviewed local v3, dated September 27, 2026; v2 retained in the collection.','paperSourceVersion: Reviewed local v3, September 27, 2026; PDF Author metadata completed October 3, 2026. Mathematical content unchanged.')
        return t
    diffs.append(write_change(f'src/content/projects/{slug}.md',update))

diffs.append(write_change('src/content.config.ts',lambda t:replace_once(t,'    paperByline: z.string().optional(),','    paperByline: z.string().optional(),'+ ('\r\n' if '\r\n' in t else '\n')+'    paperReadingCopy: z.number().int().positive().default(1),')))
diffs.append(write_change('src/pages/[slug].astro',lambda t:replace_once(t,'Site reading copy 1 from {project.data.paperSourceVersion}','Site reading copy {project.data.paperReadingCopy} from {project.data.paperSourceVersion}')))
def papers(t):
    t=replace_once(t,'“Site reading copy 1” means the first PDF made available here. Each entry also names the manuscript revision from which that copy came.','Reading-copy numbers identify the PDF version selected for this site. Copy 2 corrects author attribution or metadata without changing the mathematics. Each entry also names its source manuscript revision.')
    t=replace_once(t,'Reading copy 1 · <strong>PDF byline:</strong>','Reading copy {project.data.paperReadingCopy} · <strong>PDF byline:</strong>')
    return replace_once(t,'The reading copies preserve the author name printed in each source PDF. Brian Theory and Brian Droncheff refer to the same person. The version labels distinguish the first copy posted on this site from the earlier internal revisions of each manuscript; they do not imply journal acceptance.','All current reading copies name Brian Theory as author. Historical references retain the names under which the cited works appeared. The version labels distinguish site reading copies from the internal revisions of each manuscript; they do not imply journal acceptance.')
diffs.append(write_change('src/pages/papers.astro',papers))
diffs.append(write_change('README.md',lambda t:replace_once(t,'Five byte-identical manuscript reading copies are bundled in `public/manuscripts/`; Structured Boolean Factorization remains index-only pending an integrated manuscript with a named author. The website uses “site reading copy 1” while preserving each paper\'s internal version.','Five manuscript reading copies are bundled in `public/manuscripts/`, all credited to Brian Theory. Three use reading copy 2 for author or metadata corrections; the two unchanged PDFs remain copy 1. Superseded files are preserved in `manuscript-history/reading-copy-1/`. Structured Boolean Factorization remains index-only pending an integrated manuscript with a named author. Site release numbers remain separate from internal manuscript versions.')))

lines=['# Manuscript reading-copy provenance and author correction','', 'Updated 3 October 2026. Local preparation only; no external publication or repository upload.','', '## Version convention','', 'Reading-copy numbers identify fixed PDF bytes selected for this website. They are separate from manuscript revision numbers and do not imply journal acceptance or human peer review. Copy 2 records only author/metadata corrections. Superseded copy-1 PDFs have been moved out of the active public manuscript directory to `manuscript-history/reading-copy-1/`; their old public filenames are retired. Original scientific sources and review packages remain preserved in the publication collection.','', '## Current PDFs','', '| Site file | Manuscript revision | Byline / PDF Author | Pages | SHA-256 |','| --- | --- | --- | ---: | --- |']
versions={'binary-order-thinning':'Reviewed v3, 27 September 2026','correspondence-matrices':'Final adversarial revision, 27 September 2026','hierarchical-concepts':'Original fresh-referee v0.3, 29 September 2026, with author correction','observation-refinement':'Referee-repair v0.5, 29 September 2026, with author correction','prolt':'v0.9 submission package'}
for r in before:
    old=Path(r['site_file']).name
    name=old.replace('-r1-','-r2-') if old.replace('-r1-','-r2-') in after else old
    a=after.get(name,r)
    prefix=next(p for p in versions if name.startswith(p))
    lines.append(f"| `{name}` | {versions[prefix]} | Brian Theory | {a['pages']} | `{a['sha256']}` |")
lines+=['','## Exact source provenance','', 'All five original copy-1 PDFs were SHA-256 identical to the selected source PDFs under `C:\\Users\\brian\\Documents\\Math Latex etc\\Papers for Publication`. The full audit, exact source paths, review scores, before/after hashes, source-author patches and verification receipts are in `00_Collection_Index/Website_Manuscript_Audit_2026-10-03/MANUSCRIPT_AUDIT.md` under that collection.','', 'Binary Order Thinning had a correct printed byline but a blank PDF Author field; only that field was completed. Observation Refinement was rebuilt from a copy of the exact reviewed source with only its author line and PDF Author value changed. Hierarchical Concepts received a surgical title-page author/font replacement and PDF Author metadata; its other page content was preserved. A matching author-corrected TeX/bibliography copy is retained in the audit folder; a full local rebuild was blocked by the missing `logreq.sty` package. No package was installed.','', 'All three corrected PDFs retain their page counts. Full page-text comparison found only the intended title-page author changes. Rendering every before/after page at 72 dpi found changes confined to the two title-page byline rectangles; Binary Order Thinning rendered identically throughout. Updated title pages were also visually inspected at 125 dpi.','', 'Historical bibliography attributions remain unchanged, including the Droncheff thesis/reference entries. These are citations, not current manuscript bylines.','', '## Superseded reading-copy-1 hashes','', '| Retired site file | SHA-256 |','| --- | --- |']
for r in before:
    old=Path(r['site_file']).name
    if old.replace('-r1-','-r2-') in after:
        lines.append(f"| `{old}` | `{r['sha256']}` |")
lines+=['','## Deferred copy','', 'Structured Boolean Factorization remains index-only. The Phase 5 theorem note has a “Research draft” byline and later unintegrated Phase 5B work. It was not one of the five PDFs audited or changed in this task.','']
diffs.append(write_change('MANUSCRIPT_READING_COPIES.md',lambda _: '\n'.join(lines)))
(OUT/'website_changes.diff').write_text(''.join(diffs),encoding='utf-8')
(OUT/'website_changes.json').write_text(json.dumps(changes,indent=2),encoding='utf-8')
print(json.dumps(changes,indent=2))
