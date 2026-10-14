# Reproducibility report

Audit date: 24 September 2026. All results below were obtained in this session from the supplied archive or from new independent code. A successful finite computation supports, but does not prove, a general theorem.

## 1. Source availability and preservation

The ZIP opens normally. Its manifest entries were inspected in the requested order. The core PDF, both historical TeX notes, and v0.1-v0.5 primary manuscripts are readable, with one important exception: **the v0.3 TeX is an empty file**. Its 15-page PDF was used instead. The core was supplied as an 18-page PDF, not a TeX source. No missing source was silently replaced by a prior conversation artifact.

The bundle includes an unchanged source snapshot, original run logs, independent scripts, exact named-example JSON, and SHA-256 manifests. Reports and additional checks are separate from the original sources. The Files connector did not parse the ZIP, but the mounted archive was extracted successfully with normal archive tools; that connector result was not an archive-read failure.

## 2. Original verifier reruns

All five supplied verifier scripts exited successfully with assertions enabled. Recorded interpreter: Python 3.13.5. See `verification/original_runs/run_metadata.json`.

| Script | Exit | Recorded seconds | Audit interpretation |
|---|---:|---:|---|
| verify_refinement_classification.py | 0 | 0.724 | Reproduces the early finite profiles and named examples; not a universal homotopy oracle |
| verify_refinement_subclasses.py | 0 | 2.073 | Checks chain/subclass counts and relative boundary criteria |
| verify_homotopy_preserving_observations.py | 0 | 1.128 | Checks sufficient criteria and homology coverage on stated finite cases |
| verify_repair_forest_theorem.py | 0 | 14.157 | Reproduces exact-height-two one-bit table |
| verify_multibit_v05.py | 0 | 1.069 | Reproduces small two-bit counts and programmed examples |

These are one-run timings, not performance benchmarks. The repair-forest script uses an absolute import path. To run it without changing the supplied source, its unchanged dependency was copied to the expected `/mnt/data` location. That workaround is documented rather than presented as portable packaging.

### Code-quality and inference limits

The scripts contain useful checks, but several comparison labels are stronger than the calculation. Equality of Betti numbers is not proof that the induced map is a homology isomorphism; acyclicity of the actual relative or mapping-cone complex is the appropriate map test. Neither condition proves homotopy equivalence generally. Beat-point reduction proves finite-space contractibility when it succeeds, but is not a complete test for order-complex contractibility.

Some routines essentially compare the relative boundary rank criterion with another implementation of that same criterion. This is a consistency check, not an independent proof of the structural forest theorem. Some named-example matching helpers occur after the main invocation and are not exercised by the ordinary run. The independent audit explicitly enumerated those matchings.

No environment lock, portable input-path contract, test suite with isolated expected fixtures, or assertion-safe non-optimized execution guard was supplied. Do not run these scripts under `python -O`.

## 3. Enumeration conventions

A **naturally labelled poset** here has every strict relation (i,j) oriented i<j in one fixed vertex order. The generator enumerates transitive subsets of those forward pairs and applies the height filter. Every finite poset is isomorphic to one with a natural labelling, so no isomorphism type at the stated size is omitted. However, a type may occur multiple times through distinct compatible labellings. These are neither all arbitrary labelled orders nor one representative per isomorphism class.

All bit assignments are then enumerated on each generated order. No restriction to surjective labels is imposed: constant observations, duplicates, and unused bit patterns are deliberately included. Height counts strict inequalities, so height<=2 means the order complex has dimension<=2.

## 4. Independent implementation

`verification/independent/audit_checks.py` imports **none of the original verifiers**. It separately constructs transitive relations, thinned orders, simplices, signed boundary matrices, modular ranks, exact Smith forms, repair graphs, perfect matchings, acyclicity, and beat/collapse sequences. It uses SymPy only for exact integer normal forms, rather than floating-point determinants.

`higher_height_and_edges.py` builds the cone/whisker counterexamples and checks edge cases. `extend_two_bits.py` extends the two-bit range to five vertices. The first two import only the audit's own shared implementation when they need common routines; they are not three independent implementations of every operation. The principal structural independence is **graph DSU/leaf elimination versus boundary algebra**, and **set cover versus conflict-graph coloring**.

### 4A. Early 255 profiles

The original early search reproduces 255 nonempty small signature-profile cases. Its five recorded pattern frequencies are 24, 16, 20, 144, and 51 (total 255), corresponding to the program's tests. These are profiles in that particular search, **not** all posets on a universal vertex bound. The audit reran and inspected this script; it did not independently reproduce this exact early-profile generator. Later independent exhaustive poset checks test the substantive order-thinning claims more broadly.

### 4B. Chains through twelve vertices

All 2^n one-bit words for n=1,...,12 were checked, for a total of 8,190 words. This check uses actual beat-point reduction, and separately tests all principal prefixes and suffixes, not merely their Betti numbers.

At n=12 the counts are: 13 redundant, 11 defective, 4,072 nonredundant neutral, and 1,013 neutral profiles missed by both Quillen orientations. All lengths agree with the theorem. The original script's displayed run limit and supplied CSV extent are not identical; the independent n<=12 check removes that ambiguity for the claimed table range. File: `chain_checks.json`.

### 4C. One bit, height at most two, through six vertices

| Vertices | Natural posets, height<=2 | All profiles | Exact-height-two profiles | Exact-height-two nonredundant neutral |
|---:|---:|---:|---:|---:|
| 1 | 1 | 2 | 0 | 0 |
| 2 | 2 | 8 | 0 | 0 |
| 3 | 7 | 56 | 8 | 2 |
| 4 | 39 | 624 | 208 | 50 |
| 5 | 330 | 10,560 | 5,504 | 1,232 |
| 6 | 4,117 | 263,488 | 178,368 | 36,783 |
| **Total** | | **274,738** | **184,088** | **38,067** |

For every profile, relative boundary ranks over F2, F3, and F5 agree with the rooted-incidence characterization. The exact-height-two subsearch reproduces the supplied 184,088 figure. The supplied last CSV column excludes redundant profiles: the empty deleted complex is also a valid rooted forest and must not be accidentally excluded from the theorem.

The integral theorem is proved by signed incidence/TU, not inferred from three primes. File: `onebit_exhaustive.json`.

### 4D. Two-bit blocks through four vertices

| Vertices | Profiles | F2-neutral | Unique matching/direct collapse | Destructive interaction |
|---:|---:|---:|---:|---:|
| 1 | 4 | 4 | 4 | 0 |
| 2 | 32 | 25 | 25 | 0 |
| 3 | 448 | 256 | 256 | 2 |
| 4 | 9,984 | 4,174 | 4,174 | 98 |
| **Total** | **10,468** | **4,459** | **4,459** | **100** |

“Destructive” means both individual coordinates are neutral relative to the original P, but their joint refinement is not. It does not mean every sequential step is neutral. File: `block_exhaustive.json`.

### 4E. New five-vertex two-bit extension

All 330 natural posets of height<=2 on five vertices and all 4^5 labels were checked: **337,920 profiles**. Results:

- 103,562 homology-neutral blocks, with the same neutrality decision over F2, F3, and F5;
- 4,514 destructive-interaction profiles;
- zero F2-neutral examples failing direct collapse.

The “coefficient differences” field compares the **neutrality decision**, not every rank in every rectangular matrix. It must not be rephrased as a proof that all homology groups are coefficient-independent. File: `two_bit_n5_extension.json`.

**Incomplete run:** an attempted six-vertex two-bit extension was stopped by a 200-second execution timeout. It produced no completed result JSON. Its empty log is retained as provenance only. No six-vertex two-bit exhaustion is claimed. This does not affect the completed six-vertex **one-bit** run.

### 4F. Observation dimension

For all naturally labelled same-vertex pairs Q subset P with n<=4, an upset-cover solver was compared against conflict-graph coloring: 1, 3, 22, and 356 pairs at sizes 1-4, totaling **382**. Separately, the height-one graph-coloring reduction was checked on **1,099 graphs** through five vertices. Both two-vertex counterexamples to the original 2-dimension equality are explicit fixtures.

These checks support the corrected theorem A2. They do not validate the original total-order complexity claim. File: `dimension_checks.json`.

### 4G. Edge cases and higher height

691 edge-case labels were checked over F2, F3, and F5, including constant coordinates, repeated coordinates, and empty/no-change cases. The cone/whisker construction gives explicitly checked one-bit height-three examples on 14 and 80 states with Z/2 and Z/3 relative torsion. Files: `edge_case_checks.json`, `onebit_height3_torsion2_14.json`, `onebit_height3_torsion3_80.json`.

## 5. Named examples reconstructed from definitions

| Example | Independent result |
|---|---|
| Three-chain 010/101 | Each coordinate a tree; joint one edge plus isolated vertex; nonzero degree-one relative class |
| Five-state compensation | Signed 3x3 matrix determinant 1; unique perfect matching; actual collapse; each coordinate alone has a relative obstruction |
| Eight-state three-bit example | Signed 11x11 matrix determinant 1, Smith diagonal all ones; exactly three perfect matchings, all cyclic; both endpoint posets beat-contractible; no direct relative collapse |
| Thirteen-state RP2 block | Signed 24x24 relative matrix, Smith diagonal 23 ones and 2; relative H1=Z/2; F2 relative Betti (0,1,1), F3/F5 zero |
| Seventy-nine-state Moore block | Signed 162x162 matrix, Smith diagonal 161 ones and 3; relative H1=Z/3; F2/F5 zero, F3 relative Betti (0,1,1) |

The complete orders, labels, deleted cells, matrices, and certificates are in named JSON files. A final independent standard-library check in `minimize_named_labels.py` applies the proved conflict-coloring criterion: the final five-state pair needs one bit; the thirteen-state torsion pair needs two; the eight-state noncollapse pair needs three. Each compression is checked against every P-comparison. The three-bit lower bound is certified by an explicit conflict triangle, not merely a failed coloring heuristic. Files end in `_minimal_labels.json`. The 13- and 79-state examples are not claimed globally minimal. The eight-state example's minimality is also not proved by the supplied small search.

## 6. What was not done

No formal proof-assistant verification; no complete recognition algorithm for homotopy equivalence; no exhaustive coefficient search beyond the explicitly stated fields; no completed n=6 two-bit enumeration; no global minimality proof for torsion witnesses; no recovery or recompilation of the absent v0.3 source; no claim that a passing verifier establishes novelty.

## 7. Confirmatory work worth doing before submission

First make the existing package portable and attach exact expected outputs. Then obtain a second independently written certificate checker for the eight-state example and the signed integral matrices, preferably in SageMath or another exact algebra system. This is more valuable than another unbounded brute-force count.

For the next research question, target the **two-bit height-two boundary** using symmetry-reduced or constraint-based search with independently checkable witnesses. Use a predetermined finite range or certificate target. An uncompleted long run is not a theorem and should not determine the paper's headline.
