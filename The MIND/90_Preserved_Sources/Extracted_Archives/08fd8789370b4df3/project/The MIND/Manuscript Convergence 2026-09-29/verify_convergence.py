"""Recheck preserved inputs and selected integrated certificates without editing them."""
import contextlib
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / 'Transferred Research/MIND_Unfolding_Project_Consolidated_Handoff_2026-09-29'
GATE = ROOT.parent / 'Interaction Core Gate 2026-09-29'
BUILD = ROOT / 'build'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(directory):
    return {str(p.relative_to(directory)): sha(p) for p in directory.rglob('*')
            if p.is_file() and '__pycache__' not in p.parts}


def main():
    checked = 0
    for line in (BASE / 'SHA256SUMS.txt').read_text().splitlines():
        if not line.strip():
            continue
        expected, relative = line.split(maxsplit=1)
        assert sha(BASE / relative) == expected, relative
        checked += 1
    assert checked == 83, checked
    archive = Path('C:/Users/brian/Downloads/MIND_Unfolding_Project_Consolidated_Handoff_2026-09-29.zip')
    assert sha(archive) == '3c21634d3ded87d33770f72cb94da86550bd3256f71470fd9c1c3b0fe2cdfd66'
    before = snapshot(GATE)
    certificate_dir = BUILD / 'certificates'
    certificate_dir.mkdir(exist_ok=True)
    sys.path.insert(0, str(GATE))
    import verify_d2_certificate as d2
    import verify_torsion_star as torsion
    d2.ROOT = certificate_dir
    torsion.ROOT = certificate_dir
    with (BUILD / 'certificate_rerun.txt').open('w', encoding='utf-8') as log:
        with contextlib.redirect_stdout(log):
            star = json.loads((GATE / 'minimal_star_d2.json').read_text())
            d2.run(star)
            d2.c4_case()
            torsion.main()
    certificates = []
    metadata_differences = {}
    for name in ['star_d2_integral_certificate.json', 'c4_d2_integral_certificate.json', 'interaction_torsion_star.json']:
        fresh = json.loads((certificate_dir / name).read_text())
        prior = json.loads((GATE / name).read_text())
        changed = {k: {'fresh': fresh.get(k), 'prior': prior.get(k)}
                   for k in fresh.keys() | prior.keys() if fresh.get(k) != prior.get(k)}
        # Earlier certificates predate the gate's revised minimality annotations.
        # Exclude only these two descriptive fields, preserving the differences.
        assert set(changed) <= {'minimality_scope', 'induced_subsets_checked_by_size'}, (name, changed)
        if changed:
            metadata_differences[name] = changed
        certificates.append(name)
    assert before == snapshot(GATE), 'prior gate was modified'
    integration = json.loads((ROOT / 'INTEGRATION_RECEIPT.json').read_text())
    assert sha(ROOT / integration['output']) == integration['output_sha256']
    for name, expected in integration['input_sha256'].items():
        assert sha(ROOT.parent / name) == expected, name
    report = {
        'original_manifest_files_verified': checked,
        'source_zip_verified': True,
        'frozen_v0_3_and_transferred_inputs_unchanged': True,
        'prior_interaction_gate_unchanged': True,
        'fresh_integral_certificates_equal_prior_results': certificates,
        'comparison_scope': 'Every mathematical field agrees. Historical minimality annotations differ as recorded below.',
        'historical_annotation_differences': metadata_differences,
        'scope': 'Two signed integer d2 certificates and the reduced torsion-star/link model; no new exhaustive enumeration.',
        'source_receipt_verified': True,
    }
    (ROOT / 'VERIFICATION_RECEIPT.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
