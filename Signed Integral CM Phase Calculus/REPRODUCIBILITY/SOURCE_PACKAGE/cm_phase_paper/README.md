# Correspondence Matrices, Cyclic Phase, and Exact Quantum Encodings

**Research draft prepared for Brian Droncheff, 17 September 2026.**

This package contains a mathematical consolidation, corrections, targeted literature review, and reproducible computational audit of the CM/phase investigation. It is not peer reviewed, a claim of a new physical theory, or evidence of a simulation speedup.

## Start here

- `paper.pdf`: compiled paper (33 pages in this release).
- `paper.tex` and `sections/`: editable modular LaTeX source.
- `standalone.tex`: the same manuscript as one LaTeX file, with its bibliography embedded using `filecontents*`.
- `references.bib`: 20 primary/historical references, with explicit source and version limitations.
- `code/`: the exact arithmetic and reproducible checks.
- `data/`: results freshly computed for this draft, not copied from earlier conversational CSV summaries.

The most important sections are 5 (finite audit and failed constructions), 6–7 (the explicit QP = JQ bridge), 8 (CM predicates compiled into actual reversible and phase operators), 12 (related work), and Appendix A (correction ledger).

## What is proved and what is assumed

The original Boolean CMs have a genuine C4 rotation action. A new circular-convolution multiplication makes them F2[C4]. The integer lift and the quotient identifying opposite phases as negatives are ADDITIONAL constructions, not an embedding that preserves every Boolean operation. The quotient is the established Gaussian-integer representation of complex phase.

Normalized Hamming weight follows from specified equal-weight/additivity assumptions. The lifted squared-modulus probability rule is the ordinary quantum measurement interpretation pulled back through an exact representation; it is not derived from Boolean logic alone.

The supplied Python scripts check finite classifications and circuit arithmetic. Proofs are mathematical arguments in the paper, not proof-assistant certificates. The literature review identifies substantial predecessors and does not establish novelty or priority.

## Run verification

Python 3.10 or newer is recommended; this release was tested using Python 3.13.5 and NumPy 2.3.5. The amplitude backend itself uses only the Python standard library. NumPy is required by the exhaustive classification and numerical cross-check scripts.

```sh
python -m pip install -r requirements.txt
python code/verify_finite.py
python code/verify_quantum.py
python code/verify_bridges.py
python code/make_tables.py
```

Run from the package root. Each script writes results into `data/` and prints a summary. The random circuit seed is 20260917. Runtime fields are diagnostic and will differ across machines; they are not claimed performance benchmarks.

### Expected headline checks

- 65,536 operators, each tested on all 256 strict-ring states.
- 24,576 invertible operators, independently checked by binary rank as well as the determinant criterion.
- 32 global Hamming isometries; 512 weight-four shell preservers; 128 distinct shell actions.
- 32 full integer-correlation isometries.
- No exact four-phase (0, 1/2, 1, 1/2) Hamming fringe in the specified normalized-shell experiment.
- 24 and 11,520 projective Clifford elements in the exact one- and two-qubit Pauli-action checks.
- 5,760 exact intermediate norm checks on 240 random circuits.
- 120 independent exact path-sum/state-vector comparisons.
- Deutsch–Jozsa: 8/8 two-input and 72/72 three-input promised functions.
- Grover: 1 for every two-bit marked item; 25/32 for every three-bit marked item after one iteration.
- CHSH: 2 sqrt(2) from exact C8 measurement circuits; local marginals remain 1/2.

### Quick amplitude example

```python
import sys
sys.path.insert(0, "code")
from phase_calculus import basis

psi = basis(1).h(0).p(0, 1).h(0)  # H, then T, then H
print(psi.probabilities())
# ((1/2, 1/4), (1/2, -1/4)), with exact Fraction objects.
# Each pair (r,s) denotes the real number r + s*sqrt(2).
assert psi.norm() == (1, 0)
```

The `p(q,k)` gate is T^k on qubit q. Thus S is `p(q,2)`, Z is `p(q,4)`, and T inverse is `p(q,7)`. Qubit zero is the leftmost bit; quantum arrays use ascending bitstrings. This storage convention differs from the original CM truth-vector ordering but is explicitly translated in the paper.

## Build the paper

A TeX installation with pdfLaTeX, latexmk, BibLaTeX/Biber, newtx fonts, TikZ-cd, and the usual AMS/table packages is needed.

```sh
latexmk -pdf -interaction=nonstopmode paper.tex
```

To compile only the self-contained source, copy `standalone.tex` into an empty directory and run:

```sh
latexmk -pdf -interaction=nonstopmode standalone.tex
```

The embedded bibliography is written to `references.bib` on first compilation. This draft was built with pdfTeX 1.40.26 and Biber 2.20. No font files or copies of third-party papers are distributed.

## Data format

`finite_classification.npz` contains the 65,536 encoded operators and Boolean membership masks for each class. Bit k of a ring element is the coefficient of g^k; the displayed CM is [[a0,a1],[a3,a2]]. The finite model orders its two branches as (|1>,|0>). The exact quantum code uses ascending bitstrings.

`finite_summary.json`, `quantum_summary.json`, and `bridge_summary.json` are human-readable summaries. `interference_tables.json` contains all 1,024 Boolean interference outputs. The four complete tables are printed in Appendix C.

## Reuse and scientific limitations

The code is research/reference code, not a validated production quantum compiler. No license is imposed here on the user's original manuscript, and no claim of ownership of the user's ideas is made. Third-party sources retain their own rights. Before public submission, choose authorship, licensing, acknowledgments, and a venue; have an independent mathematician review the proofs and a quantum-computing specialist review the novelty and interpretation.
