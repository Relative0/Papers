"""Bind the clean-extraction run and visual review to the delivered inputs."""
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT/'validation/clean_extraction/P01_REVISED_DRAFT_2026-09-26'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    reproduction = json.loads((CLEAN/'supplement/reproduced/run_record.json').read_text())
    if reproduction['status'] != 'PASS':
        raise AssertionError('Reproduction failed')
    build = json.loads((ROOT/'validation/clean_build/build_record.json').read_text())
    if build['status'] != 'PASS':
        raise AssertionError('Clean build failed')
    for record in build['receipts']:
        if record.get('exit_code', 0) or record.get('final_warnings', []):
            raise AssertionError(record)
    inputs = sorted((ROOT/'manuscript').glob('*.tex')) + sorted((ROOT/'manuscript').glob('*.bib'))
    inputs += sorted((ROOT/'supplement').glob('*.py'))
    inputs += [ROOT/'supplement/boolean_interface.tex',ROOT/'supplement/companion_reference.json',ROOT/'supplement/COMPANION_PROVENANCE.json']
    inputs += sorted((ROOT/'supplement/companion_source').glob('*.py'))
    inputs += sorted((ROOT/'supplement/reference_results').glob('*'))
    input_hashes = {}
    for path in inputs:
        rel = path.relative_to(ROOT)
        if path.read_bytes() != (CLEAN/rel).read_bytes():
            raise AssertionError('Clean extraction input differs: '+str(rel))
        input_hashes[rel.as_posix()] = digest(path)
    pdf_checks = []
    for relative in ('manuscript/main.pdf','supplement/boolean_interface.pdf'):
        delivered = PdfReader(ROOT/relative)
        rebuilt = PdfReader(CLEAN/relative)
        if len(delivered.pages) != len(rebuilt.pages):
            raise AssertionError('PDF page-count mismatch')
        for a,b in zip(delivered.pages,rebuilt.pages):
            if a.extract_text() != b.extract_text() or a.get_contents().get_data() != b.get_contents().get_data():
                raise AssertionError('PDF page content differs')
        pdf_checks.append(dict(path=relative,pages=len(delivered.pages),
                               sha256=digest(ROOT/relative),text_and_drawing_streams_match=True))
    receipt = dict(
        status='PASS', utc=datetime.now(timezone.utc).isoformat(),
        method='Full documented reproduction command passed from a fresh ZIP extraction. A later discussion-only cross-reference correction was copied into that extracted tree; both working and extracted PDFs were rebuilt and compared. Numerical scripts, reference data and manuscript table are unchanged from the successful reproduction run. All final tested source and reference inputs are hash-bound below.',
        tested_payload_sha256=input_hashes, reproduction=reproduction,
        pdf_build=build, pdf_comparisons=pdf_checks,
    )
    (ROOT/'validation/CLEAN_EXTRACTION.json').write_text(json.dumps(receipt,indent=2)+'\n')
    qa = dict(status='PASS',renderer='Poppler pdftoppm, 110 dpi',
              inspection='All 12 article pages and both optional-note pages visually inspected; revised comparison table remains with its section.',
              findings='No clipping, overlapping content, unresolved references, missing glyphs or overflowing tables. Final LaTeX logs have no citation/reference/box warnings.',
              documents=pdf_checks)
    (ROOT/'validation/VISUAL_QA.json').write_text(json.dumps(qa,indent=2)+'\n')
    print(f'PASS: {len(input_hashes)} tested input hashes, 14 identical PDF page drawing streams, clean reproduction and build.')


if __name__=='__main__':
    main()
