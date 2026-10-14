"""Render all final pages with Poppler and make legible inspection sheets."""
import json
from pathlib import Path
import shutil
import subprocess
from PIL import Image, ImageDraw
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / 'validation/rendered'
out.mkdir(exist_ok=True)
poppler = shutil.which('pdftoppm')
if not poppler:
    raise RuntimeError('pdftoppm unavailable')
records = []
for stem, pdf in [('main', ROOT/'manuscript/main.pdf'),
                  ('boolean', ROOT/'supplement/boolean_interface.pdf')]:
    subprocess.run([poppler, '-r', '110', '-png', str(pdf), str(out/stem)], check=True, capture_output=True)
    reader = PdfReader(pdf)
    text = '\n\n'.join(page.extract_text() for page in reader.pages)
    (out/(stem+'.txt')).write_text(text, encoding='utf-8')
    pages = sorted(out.glob(stem+'-*.png'))
    for offset in range(0, len(pages), 4):
        group = pages[offset:offset+4]
        canvas = Image.new('RGB', (1300, 1740), 'white')
        draw = ImageDraw.Draw(canvas)
        for j, path in enumerate(group):
            im = Image.open(path).convert('RGB')
            im.thumbnail((630, 830))
            x, y = (j%2)*650+10, (j//2)*870+30
            canvas.paste(im, (x,y))
            draw.text((x,y-20), path.stem, fill='black')
        canvas.save(out/f'{stem}_sheet_{offset//4+1}.png')
    records.append(dict(document=stem, pages=len(reader.pages), characters=len(text),
                        replacement_characters=text.count('\ufffd')))
(out/'render_record.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps(records,indent=2))
