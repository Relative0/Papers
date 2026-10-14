from pathlib import Path
import hashlib, json, re, subprocess
from pypdf import PdfReader
from PIL import Image, ImageChops, ImageDraw

OUT=Path(__file__).resolve().parent
POPPLER=Path(r'C:\Users\brian\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe')
release=OUT/'prepared_website/public/manuscripts'
qa=OUT/'pdf_qa'
qa.mkdir(exist_ok=True)
records=[]
for new in sorted(release.glob('*.pdf')):
    old=OUT/'original_site_pdfs'/new.name.replace('-r2-','-r1-')
    before,after=PdfReader(old),PdfReader(new)
    assert len(before.pages)==len(after.pages)
    text_diffs=[]
    for i,(a,b) in enumerate(zip(before.pages,after.pages)):
        old_text=a.extract_text()
        if i==0:
            old_text=old_text.replace('Brian Droncheff','Brian Theory')
        if re.sub(r'\s+','',old_text)!=re.sub(r'\s+','',b.extract_text()):
            text_diffs.append(i+1)
    assert not text_diffs, (new.name,text_diffs)
    assert after.metadata.author=='Brian Theory'
    assert 'Brian Theory' in after.pages[0].extract_text()
    renderdirs=[]
    for label,path in [('before',old),('after',new)]:
        folder=qa/new.stem/label
        folder.mkdir(parents=True,exist_ok=True)
        subprocess.run([str(POPPLER),'-r','72','-png',str(path),str(folder/'page')],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=90)
        renderdirs.append(folder)
    diffs=[]
    for a,b in zip(sorted(renderdirs[0].glob('page-*.png')),sorted(renderdirs[1].glob('page-*.png'))):
        ia,ib=Image.open(a).convert('RGB'),Image.open(b).convert('RGB')
        assert ia.size==ib.size
        bbox=ImageChops.difference(ia,ib).getbbox()
        if bbox:
            diffs.append(dict(page=int(a.stem.split('-')[-1]),bbox=bbox))
    # At 72 dpi all changes must fit the title-page author band.
    assert all(d['page']==1 and d['bbox'][0]>200 and d['bbox'][2]<410 and d['bbox'][1]>125 and d['bbox'][3]<210 for d in diffs), (new.name,diffs)
    records.append(dict(file=new.name,sha256=hashlib.sha256(new.read_bytes()).hexdigest(),pages=len(after.pages),author=after.metadata.author,text_identical_except_title_author=True,render_differences=diffs,remaining_droncheff_references=[i+1 for i,p in enumerate(after.pages) if 'Droncheff' in (p.extract_text() or '')]))
    subprocess.run([str(POPPLER),'-r','125','-f','1','-singlefile','-png',str(new),str(qa/(new.stem+'-title'))],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
(OUT/'author_correction_verification.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
print(json.dumps(records,indent=2))
