"""Read only supplied PDFs; save page-labelled text inside this dossier."""
from pathlib import Path
import hashlib
import json
from pypdf import PdfReader

OUT = Path(__file__).resolve().parent
ORIENTATION = OUT.parents[2] / 'pdf' / 'palo_cm_relationships_2026-10-13'

def main():
    inventory = json.loads((ORIENTATION / 'source_inventory.json').read_text(encoding='utf-8-sig'))
    records = []
    for item in inventory['sources']:
        if item['key'] not in {'FJ', 'GU', 'LM', 'PALO'}:
            continue
        source = Path(item['path'])
        data = source.read_bytes()
        reader = PdfReader(source)
        text = '\n\n'.join(f'=== PDF PAGE {i+1} ===\n{p.extract_text()}' for i, p in enumerate(reader.pages))
        destination = OUT / f"source_{item['key']}.txt"
        destination.write_text(text, encoding='utf-8')
        records.append({**item, 'observed_sha256': hashlib.sha256(data).hexdigest(),
                        'observed_pages': len(reader.pages), 'extracted_to': str(destination)})
    (OUT / 'local_source_versions.json').write_text(json.dumps(records, indent=2), encoding='utf-8')
    print(json.dumps([{k: r[k] for k in ('key','observed_pages','observed_sha256')} for r in records], indent=2))

if __name__ == '__main__':
    main()
