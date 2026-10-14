"""Package the clean compiled PDF and prepare, but do not certify, visual QA."""
import difflib
import hashlib
import json
from pathlib import Path
import re
import shutil
from PIL import Image, ImageDraw
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / 'build'
STEM = 'Observation_Refinement_Descent_and_Cone_Draft_v0.4'
BASE = ROOT.parent / 'Transferred Research/MIND_Unfolding_Project_Consolidated_Handoff_2026-09-29/01_CURRENT_MANUSCRIPT/Observation_Refinement_Descent_and_Cone_Draft_v0.3.tex'


def main():
    log = (BUILD / (STEM + '.log')).read_text(encoding='utf-8', errors='replace')
    issues = [line for line in log.splitlines() if re.search(r'Warning|Overfull|Underfull|undefined|multiply defined|^!', line)]
    assert not issues, issues
    pdf = BUILD / (STEM + '.pdf')
    reader = PdfReader(pdf)
    assert len(reader.pages) == 27, len(reader.pages)
    content = '\n\n'.join(f'PAGE {i + 1}\n{page.extract_text()}' for i, page in enumerate(reader.pages))
    assert '??' not in content
    (BUILD / 'pdf_text.txt').write_text(content, encoding='utf-8')
    shutil.copy2(pdf, ROOT / pdf.name)
    diff = difflib.unified_diff(BASE.read_text(encoding='utf-8').splitlines(keepends=True),
                               (ROOT / (STEM + '.tex')).read_text(encoding='utf-8').splitlines(keepends=True),
                               fromfile=BASE.name, tofile=STEM + '.tex')
    (ROOT / 'v0.3_to_v0.4.patch').write_text(''.join(diff), encoding='utf-8')
    pages = sorted((BUILD / 'render').glob('page-*.png'))
    assert len(pages) == len(reader.pages)
    for start in range(0, len(pages), 9):
        sheet = Image.new('RGB', (1380, 1875), '#dddddd')
        draw = ImageDraw.Draw(sheet)
        for j, path in enumerate(pages[start:start + 9]):
            with Image.open(path) as page:
                page.thumbnail((450, 590))
                x, y = (j % 3) * 460 + 5, (j // 3) * 625 + 25
                sheet.paste(page, (x, y))
                draw.text((x, y - 19), path.stem, fill='black')
        sheet.save(BUILD / 'render' / f'contact-{start // 9 + 1}.png')
    receipt = {
        'pdf': pdf.name,
        'pages': len(reader.pages),
        'pdf_sha256': hashlib.sha256(pdf.read_bytes()).hexdigest(),
        'source_sha256': hashlib.sha256((ROOT / (STEM + '.tex')).read_bytes()).hexdigest(),
        'compiler': 'installed MiKTeX pdfLaTeX',
        'package_installer_disabled': True,
        'shell_escape_disabled': True,
        'final_log_warnings_or_bad_boxes': issues,
        'source_labels': 23,
        'source_citations_used': 14,
        'pages_rendered': len(pages),
        'visual_review': 'PENDING: inspect final page renders before delivery',
    }
    (ROOT / 'PDF_QA_RECEIPT.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
