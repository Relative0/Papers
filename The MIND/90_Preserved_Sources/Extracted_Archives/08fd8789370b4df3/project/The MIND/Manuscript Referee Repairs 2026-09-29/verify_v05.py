"""Verify the bounded source repair, clean PDF, and preservation of prior inputs."""
from pathlib import Path
import difflib
import hashlib
import json
import re
import shutil
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
PREVIOUS = ROOT.parent / 'Manuscript Convergence 2026-09-29'
BASE = ROOT.parent / 'Transferred Research/MIND_Unfolding_Project_Consolidated_Handoff_2026-09-29'
STEM = 'Observation_Refinement_Descent_and_Cone_Draft_v0.5'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def unfold(values):
    return int(sum(not value for value in values) == 1)


def main():
    recipe = json.loads((ROOT / 'REPAIR_RECEIPT.json').read_text(encoding='utf-8'))
    source = Path(recipe['source'])
    output = ROOT / recipe['output']
    assert source.resolve() == (PREVIOUS / 'Observation_Refinement_Descent_and_Cone_Draft_v0.4.tex').resolve()
    assert sha(source) == recipe['source_sha256'] == 'e158e05f904209487b43e0e3b60dd9253287b2ad168ac1c70b9a77eaa02d29cc'
    assert sha(output) == recipe['output_sha256']
    checked = 0
    for line in (BASE / 'SHA256SUMS.txt').read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        expected, relative = line.split(maxsplit=1)
        assert sha(BASE / relative) == expected, relative
        checked += 1
    assert checked == 83

    for arity in range(2, 7):
        one_false = [0] + [1] * (arity - 1)
        two_false = [0, 0] + [1] * (arity - 2)
        assert not all(one_false) and not all(two_false)
        assert unfold(one_false) == 1 and unfold(two_false) == 0
    assert unfold([0]) == 1 and unfold([1]) == 0

    text = output.read_text(encoding='utf-8')
    assert '$m=|A|\\ge2$' in text
    assert r'\mathcal V$ be' in text and 'finite good subcomplex cover of $Y$' in text
    assert 'pullbacks are represented' in text
    assert 'Does the chosen map fail to be a homology equivalence?' in text
    assert '$B-A$ in the $02$ link' in text
    assert 'No unique extension from $Y$ to $X$ is asserted' in text
    assert 'direct specialization of the obstruction' in text
    assert len(re.findall(r'\\label\{([^}]+)\}', text)) == recipe['labels']

    build = ROOT / 'build'
    log = (build / (STEM + '.log')).read_text(encoding='utf-8', errors='replace')
    issues = [line for line in log.splitlines() if re.search(r'Warning|Overfull|Underfull|undefined|multiply defined|^!', line)]
    assert not issues, issues
    pdf = build / (STEM + '.pdf')
    reader = PdfReader(pdf)
    page_text = '\n\n'.join(f'PAGE {i+1}\n{page.extract_text()}' for i, page in enumerate(reader.pages))
    assert len(reader.pages) == 27
    assert '??' not in page_text
    assert 'fixed arity' in page_text.lower() or 'Fix the arity' in page_text
    assert 'subcomplex' in page_text
    (build / 'pdf_text.txt').write_text(page_text, encoding='utf-8')
    shutil.copy2(pdf, ROOT / pdf.name)
    diff = difflib.unified_diff(source.read_text(encoding='utf-8').splitlines(keepends=True),
                                text.splitlines(keepends=True),
                                fromfile=source.name, tofile=output.name)
    (ROOT / 'v0.4_to_v0.5.patch').write_text(''.join(diff), encoding='utf-8')
    record = {
        'input_v04_sha256': sha(source),
        'output_v05_source_sha256': sha(output),
        'output_v05_pdf_sha256': sha(pdf),
        'transferred_manifest_files_verified': checked,
        'fixed_arity_boolean_examples_checked': [2, 3, 4, 5, 6],
        'one_factor_exception_checked': True,
        'source_labels': recipe['labels'],
        'citations_used': recipe['citations_used'],
        'pdf_pages': len(reader.pages),
        'latex_warnings_or_bad_boxes': issues,
        'pdf_text_extraction': 'passed',
        'visual_review': 'PENDING',
        'scope': 'Targeted referee repairs; prior interaction enumerations and certificates not rerun.'
    }
    (ROOT / 'VERIFICATION_RECEIPT.json').write_text(json.dumps(record, indent=2), encoding='utf-8')
    print(json.dumps(record, indent=2))


if __name__ == '__main__':
    main()
