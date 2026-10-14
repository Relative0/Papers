"""Cache public primary PDFs for private research, without executing their content."""
from pathlib import Path
import hashlib, json, urllib.request
from pypdf import PdfReader

OUT = Path(__file__).resolve().parent
sources = {
 'xu2018': 'https://proceedings.mlr.press/v80/xu18h/xu18h.pdf',
 'amc2017': 'https://starai.cs.ucla.edu/papers/KimmigJAL16.pdf',
 'semirings2024': 'https://arxiv.org/pdf/2402.13782v1',
 'scallop2023': 'https://www.cis.upenn.edu/~jianih/res/papers/pldi23_scallop.pdf',
 'spl2022': 'https://arxiv.org/pdf/2206.00426',
 'qll2026': 'https://arxiv.org/pdf/2605.13845v2',
 'foundation2026': 'https://arxiv.org/pdf/2602.23878v1',
 'adequate2026': 'https://arxiv.org/pdf/2605.13348v3',
 'gradient2025': 'https://arxiv.org/pdf/2502.18406v1',
 'atlas2024': 'https://arxiv.org/pdf/2412.05481',
}
(OUT/'sources').mkdir(exist_ok=True)
rows = []
for key, url in sources.items():
    path = OUT/'sources'/f'{key}.pdf'
    try:
        if not path.exists():
            request = urllib.request.Request(url, headers={'User-Agent':'Research source verification'})
            with urllib.request.urlopen(request, timeout=20) as r:
                data = r.read(20_000_000)
            if not data.startswith(b'%PDF'):
                raise ValueError('Not a PDF response')
            path.write_bytes(data)
        reader = PdfReader(path)
        pages = [p.extract_text() or '' for p in reader.pages]
        (OUT/'sources'/f'{key}_pages.json').write_text(json.dumps(pages, ensure_ascii=False),encoding='utf-8')
        (OUT/'sources'/f'{key}.txt').write_text('\n\n'.join(f'=== PDF PAGE {i+1} ===\n{p}' for i,p in enumerate(pages)),encoding='utf-8')
        row = {'key':key,'url':url,'pages':len(pages),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'status':'cached'}
    except Exception as e:
        row = {'key':key,'url':url,'status':'unavailable','reason':str(e)}
    rows.append(row)
    print(json.dumps(row),flush=True)
    (OUT/'external_source_inventory.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
