PALO AND THE CORRESPONDENCE-MATRIX RESEARCH PORTFOLIO
Research synthesis prepared for Brian Theory, 13 October 2026 (Asia/Bangkok)

MAIN DELIVERABLES
palo_cm_relationships.pdf -- compiled, visually reviewed report.
palo_cm_relationships.tex -- standalone editable LaTeX source; bibliography is embedded.

The report compares the supplied PALO paper with six portfolio manuscripts.
It distinguishes source results, elementary derived connections, and proposed
extensions. It covers reciprocal benefits, semantic limits, a combined
architecture, and staged experiments with decision gates.

SUPPORTING FILES
source_inventory.json -- exact source paths, titles, page counts, and SHA-256 hashes.
build_source_inventory.py -- regenerates that inventory from the local PDFs (pypdf required).
verify_bridges.py -- exact rational checks of the report's elementary algebra and examples.
verification_results.json -- passing results for 40,668 bounded assertions.
quality_checks.json -- build, reference, and document boundary checks.
build_status.txt -- compilation route and visual review scope.
SHA256SUMS.txt -- hashes of the package's main files.

REBUILD
Run pdflatex twice on palo_cm_relationships.tex to resolve citations and the table
of contents. No external bibliography, source PDF, or image is needed to compile.
The file uses standard LaTeX packages listed in its preamble.

The built-in Codex LaTeX compiler was attempted but failed before processing the
source with: "Unable to find standard directories for platform". The requested
PDF was successfully produced with the already installed MiKTeX/pdfLaTeX runtime.
Automatic package installation was disabled. The LaTeX source was opened in the
built-in editor and the PDF was opened separately for viewing.

VERIFICATION
Run: python verify_bridges.py
This script uses the Python standard library and writes verification_results.json.
Its passing calculations are not a LIME integration, learning experiment,
compiler benchmark, or independent proof audit of the source manuscripts.

SCOPE
Original manuscripts were read only. The report and support files are new local
artifacts. No source paper is redistributed in the report package. No remote
publication, training, paid compute, commit, or push was performed.
