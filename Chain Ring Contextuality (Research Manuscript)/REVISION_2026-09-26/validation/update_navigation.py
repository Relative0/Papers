"""Update only P01 navigation; preserve all historical source/evidence bytes."""
import csv
import difflib
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
sys.path.insert(0, str(ROOT/'supplement'))
from run_reproduction import substantive

audit = ROOT/'P01_ASTRA_AUDIT/evidence/independent_full'
comparisons = []
for old in sorted(audit.iterdir()):
    fresh = ROOT/'supplement/reference_results'/old.name
    same = substantive(json.loads(old.read_text())) == substantive(json.loads(fresh.read_text())) if old.suffix == '.json' else old.read_text() == fresh.read_text()
    if not same:
        raise AssertionError('Audit comparison failed: '+old.name)
    comparisons.append(old.name)
(ROOT/'validation/audit_comparison.json').write_text(json.dumps(dict(status='PASS', files=comparisons, ignored_fields=['python','platform','seconds']),indent=2)+'\n')

documents = {
    'README_FIRST.md': """# Contextuality and Exact Information Resources over Finite Chain Rings

**Current draft:** revised 26 September 2026. **Author:** Brian Theory, B-Theory.

Read [the revised PDF](REVISION_2026-09-26/manuscript/main.pdf) or edit [the LaTeX source](REVISION_2026-09-26/manuscript/main.tex). The [revision entry point](REVISION_2026-09-26/README.md) links the self-contained computational supplement, audit response and optional Boolean note.

The article retains three linked contribution groups:

- P011: Residue-hyperplane criterion, uniform Hardy witness and complete-basis Smith trichotomy.
- P012: Exact orbit codebook dh under full invertible local encoders and complete joint readout.
- P013: Universal exact raw teleportation iff invertibility, with a nonprimitive separator and an explicit primitive-resource boundary.

The two major and seven localized audit issues are addressed in the [revision response](REVISION_2026-09-26/REVISION_RESPONSE.md). Full finite checks and a scoped check using the supplied process-semantics companion pass. Historical priority remains a bounded literature judgment; no publication or submission has been made.

- [Claims and boundaries](CLAIMS_AND_UNIQUENESS.md)
- [Reproduction](REPRODUCIBILITY/README.md)
- [Reviews](REVIEWS_AND_RECOMMENDATIONS/README.md)
- [History](HISTORY/README.md)
- [Current source manifest](SOURCE_MANIFEST_SHA256.csv)

The source package dated 19 September and prior reviews remain preserved. They are historical versions, not competing manuscript heads.
""",
    'CLAIMS_AND_UNIQUENESS.md': """# Claims and boundaries - P01

**Canonical owner:** Chain Ring Contextuality and Exact Resources (P01).

Current source: [revised main.tex](REVISION_2026-09-26/manuscript/main.tex).

- P011: Complete-basis support classification by r and h; hyperplane and Hardy lemmas. Outcome choices are indexed by settings, with no extra shared-ray KS identification.
- P012: Exactly dh messages for the specified full-GL orbit and complete joint decoder. This is not general channel capacity.
- P013: Universal exact raw-vector, reference-preserving teleportation iff invertibility, with a complete joint covector basis and unrestricted invertible corrections.
- Primitive-resource boundary: maximal d^2 coding iff invertibility iff raw teleportation. The maximal-coding/nonteleportation separator requires nonprimitive resources.
- Two-setting boundary: a global assignment exists in the stated binary-residue setting; this does not assert full locality.

Classical ingredients include Smith/module theory, matrix spanning by invertibles, modal protocols and the global-section hierarchy. The [source comparison](REVISION_2026-09-26/LITERATURE_COMPARISON.md) records established overlap, different task assumptions and access limitations. External firstness is not certified.

The support model admits nonzero static resources but is not an unchanged tensor-closed preparation/process theory. Literal binary expansion changes tensor and effect contracts. The optional Boolean construction is separate from the article.

The [standalone supplement](REVISION_2026-09-26/supplement/README.md) distinguishes direct support solving, invariant-derived aggregation and explicit lower-bound certificates. The received audit and all historical manuscript files remain preserved. No general physical realization, probability model, speedup or formal proof certification is claimed.
""",
    'REPRODUCIBILITY/README.md': """# Reproducibility

The current draft has a [standalone computational supplement](../REVISION_2026-09-26/supplement/README.md).

After extracting the revised package, run:

    python supplement/run_reproduction.py

Python 3.10+ and the standard library suffice. The wrapper reruns the unchanged audit checker, a scoped companion comparison and ten supplied tests; compares substantive outputs; regenerates the manuscript table; and writes commands, timings, exit codes and hashes. No original portfolio dependencies are needed. Do not disable assertions.

The [revision response](../REVISION_2026-09-26/REVISION_RESPONSE.md) states coverage and limits. The historical generator in the preserved 19 September source package depended on absent inputs and is not the current entry point. Old canonical-runner or LM-product assertions describe historical snapshots and are not evidence claims of the revised article.

Build PDFs with python supplement/build_documents.py using an installed TeX distribution. The [revision README](../REVISION_2026-09-26/README.md) gives details.
""",
    'REVIEWS_AND_RECOMMENDATIONS/README.md': """# Reviews and revision response

- [Supplied Astra publication-readiness audit](../REVISION_2026-09-26/P01_ASTRA_AUDIT/P01_ASTRA_PUBLICATION_READINESS_AUDIT.md), preserved unchanged; describes the 19 September draft.
- [Issue-by-issue response](../REVISION_2026-09-26/REVISION_RESPONSE.md) for the revised draft.
- [Source comparison](../REVISION_2026-09-26/LITERATURE_COMPARISON.md), with bounded priority claims.
- [Original internal review](../01_SOURCE_PACKAGE_FROM_PORTFOLIO_20260921/source_package/ADVERSARIAL_REVIEW.md), preserved as historical context.

Labels such as panel/referee in supplied reviews do not establish independent human review. The revision does not re-score itself or claim a new journal acceptance/readiness verdict. All identified draft and package repairs are documented; external release remains an author decision.
""",
    'HISTORY/README.md': """# Version history

Current head: [26 September revision](../REVISION_2026-09-26/manuscript/main.tex).

- The [19 September manuscript source](../01_SOURCE_PACKAGE_FROM_PORTFOLIO_20260921/source_package/main.tex), PDF, generator and accompanying evidence are preserved unchanged.
- The [partition baseline](PARTITION_BASELINE_20260925/00_PUBLICATION_CONTEXT_2026-09-25.md) and its manifest remain historical records.
- The received Astra audit is preserved unchanged in REVISION_2026-09-26/P01_ASTRA_AUDIT.
- The revised draft adds a self-contained replacement supplement, scoped companion evidence, an explicit primitive-resource consequence, corrected exposition and bibliography, and confirmed authorship.

Historical filenames and claims describe their own snapshots. They do not override the current manuscript or CLAIMS_AND_UNIQUENESS.md.
""",
}
for name, content in documents.items():
    path = PROJECT/name
    (ROOT/'validation/navigation_before').mkdir(exist_ok=True)
    backup = ROOT/'validation/navigation_before'/name.replace('/','__')
    if not backup.exists():
        backup.write_bytes(path.read_bytes())
    path.write_text(content, encoding='utf-8', newline='\n')

original = PROJECT/'01_SOURCE_PACKAGE_FROM_PORTFOLIO_20260921/source_package'
diff = ''
for name in ('main.tex', 'references.bib'):
    diff += ''.join(difflib.unified_diff((original/name).read_text().splitlines(True),
                    (ROOT/'manuscript'/name).read_text().splitlines(True),
                    fromfile='preserved_19_September/'+name, tofile='revised_26_September/'+name))
(ROOT/'validation/manuscript_changes.patch').write_text(diff,encoding='utf-8')

with (ROOT/'validation/pre_revision_manifest.csv').open(newline='',encoding='utf-8-sig') as f:
    baseline = list(csv.DictReader(f))
unchanged = []
for entry in baseline:
    rel = entry['RelativePath']
    if rel in documents:
        continue
    path = PROJECT/rel
    if hashlib.sha256(path.read_bytes()).hexdigest().lower() != entry['SHA256'].lower():
        raise AssertionError('Unexpected original-file change: '+rel)
    unchanged.append(rel)
(ROOT/'validation/source_integrity.json').write_text(json.dumps(dict(status='PASS',baseline_files_verified_unchanged=unchanged,modified_navigation=list(documents)),indent=2)+'\n')
print(f'Updated five navigation files; verified {len(unchanged)} baseline files unchanged; audit outputs agree.')
