from pathlib import Path
import json, sys
import pypdfium2 as pdfium
from PIL import Image, ImageOps, ImageDraw
from pypdf import PdfReader

pdf=Path(sys.argv[1]).resolve();out=pdf.parent/'visual_review';out.mkdir(exist_ok=True)
doc=pdfium.PdfDocument(pdf)
thumbs=[]
for i in range(len(doc)):
    page=doc[i];im=page.render(scale=1.4).to_pil().convert('RGB')
    im.save(out/f'page_{i+1:02d}.png')
    thumb=ImageOps.contain(im,(425,580));tile=Image.new('RGB',(445,610),'#dddddd')
    tile.paste(thumb,((445-thumb.width)//2,20));ImageDraw.Draw(tile).text((12,592),f'Page {i+1}',fill='black');thumbs.append(tile)
for start in range(0,len(thumbs),6):
    batch=thumbs[start:start+6];sheet=Image.new('RGB',(445*3,610*2),'white')
    for j,im in enumerate(batch):sheet.paste(im,((j%3)*445,(j//3)*610))
    sheet.save(out/f'contact_{start//6+1}.png')
reader=PdfReader(pdf);text='\n\n'.join(p.extract_text() or '' for p in reader.pages)
(out/'extracted_text.txt').write_text(text,encoding='utf-8')
(out/'RENDER_MANIFEST.json').write_text(json.dumps(dict(pdf=str(pdf),pages=len(doc),page_size=[float(reader.pages[0].mediabox.width),float(reader.pages[0].mediabox.height)],empty_pages=[i+1 for i,p in enumerate(reader.pages) if not (p.extract_text() or '').strip()],visual_inspection='Pending explicit image review'),indent=2)+'\n')
print(json.dumps(dict(pages=len(doc),sheets=(len(doc)+5)//6,out=str(out))))
