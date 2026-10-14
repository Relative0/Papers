# Computational interaction audit — 29 September 2026

## Scope and principal finding

The new gate extends the previous exhaustive four-state calculations to **all 90,201 naturally labelled poset/profile cases through five states**, of which 86,751 have five states. The filtered mixed chain complex was computed over `F2` for every case. All these small cases collapse by `E2`; this is finite evidence, not a general theorem.

A targeted larger search found a **seven-state `K_{1,3}` example with a nonzero integral `d2`**. Its exclusive graph is simultaneously a forest, Ferrers, and chordal bipartite. Thus none of these three unrestricted graph classes forces `E2` collapse. The witness has torsion-free first page and torsion-free total homology; higher differentials do not require torsion.

A separate structural search then found an **eight-state `K2,2` example with integral `d2=±1`**. Thus maximum degree two also fails to force `E2` collapse without excluding or controlling four-cycle cores. Both witnesses were independently certified with exact signed chains and integral Smith calculations.

The integral interaction-torsion construction is audited separately by `verify_torsion_star.py` and its accompanying output, owned by the main gate. That construction produces `Z/2` interaction torsion despite torsion-free local link groups. The small-case absence of torsion below must not be interpreted as a torsion-freeness theorem.

## Reproducible computation

Runtime used: `C:\Users\brian\AppData\Local\Programs\Python\Python310\python.exe`, Python 3.10, SymPy 1.14.0. No packages were installed. Commands, from this gate directory:

```powershell
python verify_interaction.py --exhaustive-n 5 --random-n 6 --random-trials 5000
python verify_local_interactions.py
python verify_d2_certificate.py --case all
python canonicalize_interaction_results.py
```

`verify_interaction.py` imports the frozen matching verifier's poset, product, chain, and integral Smith routines. It does not invoke that verifier's `main()` and does not rewrite its saved results. Bytecode creation is disabled before importing the frozen source.

The three relevant complexes are kept separate:

- `C(K,L)` computes reduced topological-cone homology (equivalently algebraic mapping-cone homology).
- `C(K,U)` is the mixed two-colour complex, with `H_m(K,U)=H_{m-1}(K,L)`.
- Its filtration is missing-core cardinality, with page coordinates reported in the JSON files as **`filtration,total_degree`**. Standard bidegree is `(p,q)=(filtration,total_degree-filtration)`.

For example, the witness differential written `4,4 -> 2,3` is `d2:E2_{4,0}->E2_{2,1}`. The mixed total degree is one larger than cone degree.

## Method and independent checks

Every mixed simplex is an actual strict chain in `Q x {0<1}` containing both missing colours. Its oriented boundary deletes one vertex with the ordinary alternating sign and discards faces outside the relative complex. Filtration is the number of missing vertices.

For the field calculation, simplices are ordered by `(filtration,dimension,vertex_tuple)` and the full boundary matrix is reduced by bit-packed exact `F2` column operations. A finite persistence interval with birth filtration `a` and death filtration `b` records a rank-one differential on page `r=b-a`. Length-zero intervals describe the internal `d0` reductions; positive-length endpoints survive through `Er` and disappear on `E(r+1)`. Infinite intervals describe `E∞`. This computes page dimensions and differential ranks, rather than a preferred matrix for each differential.

Each processed case was checked independently in two ways:

1. `E1` dimensions from the interval reduction equal the homology dimensions computed directly from boundary entries that preserve filtration.
2. Final surviving dimensions equal ordinary homology dimensions computed from separate ranks of the unfiltered boundary matrices.

Integral checks use the baseline's **full Smith decomposition**: a primitive integral basis of the kernel of `d_n`, followed by Smith reduction of `im d_(n+1)` in that basis. They do not subtract integer matrix ranks and call the result integral homology. The signed boundary-square identity is asserted for each integral mixed complex.

The selected integral results are also compared against the separately built pair `C(K,L)` using the exact two-colour degree shift. No disagreement was found.

## Exhaustive and random scope

| Coarse states | Distinct naturally labelled transitive closures | Profiles checked |
|---:|---:|---:|
| 1 | 1 | 3 |
| 2 | 2 | 18 |
| 3 | 7 | 189 |
| 4 | 40 | 3,240 |
| 5 | 357 | 86,751 |
| Total | 407 | 90,201 |

Transitive closures are deduplicated as labelled relations; posets are **not** deduplicated up to isomorphism. Every finite poset with at most five states has a linear extension among these labelled representatives. All three-valued availability profiles are included.

An additional 5,000 deterministic six-state trials sampled forward relations at several densities, took their transitive closures, and chose availability profiles. These are neither an exhaustive six-state calculation nor uniformly sampled isomorphism classes. Seed: `20260929`.

The main run completed in 24.75 seconds and had at most 287 mixed simplices in a processed case. It checked 95,201 cases total. Across this run, only `d1` was nonzero (aggregate rank 6,745); there were no `d2` or later differentials. Every `E1` and total-homology consistency check passed.

| Exhaustive class through five states | Cases | Cases with nonzero `d1` | Cases with nonzero `d2` or later |
|---|---:|---:|---:|
| All | 90,201 | 4,485 | 0 |
| Matching | 79,537 | 0 | 0 |
| Maximum degree at most two | 88,697 | 3,321 | 0 |
| Forest | 89,758 | 4,168 | 0 |
| Ferrers | 89,863 | 4,441 | 0 |
| Chordal bipartite | 90,201 | 4,485 | 0 |

These classes overlap; row counts must not be added. A bipartite graph on at most five vertices cannot have an induced cycle of length at least six, so the last row is automatically the whole exhaustive sample. This is not evidence that the chordal condition itself improves the result.

The main run performed **435 selected exact integral comparisons**, including every profile through three states and a deterministic sparse larger sample. There was no torsion in this selected sample. It did **not** compute integral Smith normal form for all 90,201 exhaustive cases. Full case-level field summaries are in `interaction_case_summary.csv`; integral cases and their selection reasons are in `interaction_integral_checks.json`.

## Isomorphism deduplication and exclusive graph types

`canonicalize_interaction_results.py` postprocesses the saved exhaustive CSV without rerunning homology. Each naturally labelled coarse poset is canonicalized under **every vertex permutation**, giving respectively `1,2,5,16,63` unlabelled coarse posets on one through five states: **87 coarse isomorphism types** total. The JSON catalog records the canonical order code, all corresponding natural-poset IDs, and the selected representative.

Keeping one representative of each unlabelled coarse poset and every availability assignment on that representative gives **16,761 cases**: `3,18,135,1,296,15,309` by size. This removes redundant coarse labels; it does not additionally quotient availability assignments by poset automorphisms. Both this view and the original 90,201-case view are retained in the graph-type aggregation.

Exclusive graphs are canonicalized by independent permutations within `P` and within `Z`. The two colours are preserved, including isolated `P` and isolated `Z` vertices; split states are excluded from the exclusive graph. Under this convention there are **70 exclusive graph isomorphism types** in the exhaustive cases. Both coarse-label views contain exactly the same 70 types. Counts, nonzero differential/homology case counts, and summed ranks are stored per type in `interaction_graph_isomorphism_types.csv` and `interaction_isomorphism_summary.json`.

The 5,000 random six-state rows are explicitly excluded from this postprocessing: their saved random trial IDs alone do not reconstruct the coarse posets. They retain their original separate computational status. The canonicalization run took 3.141 seconds and performed no new homology computation. Its count assertions and graph-type coverage assertions passed.

## Exact local models

All nine following models were independently computed over `Z` in both the mixed and the direct pair complexes. The results and signed boundary columns are stored in `local_interaction_models.json`.

| Model | Largest mixed core | Positive-page differential ranks over `F2` | Nonzero reduced cone homology over `Z` |
|---|---:|---|---|
| Ordered two-edge star, chain profile `(1,0,0)` | 3 | `rank d1=1` | `H1=Z` |
| Same star with incomparable leaves | 2 | none | `H1=Z²` |
| Four-vertex path, height-two coarse poset | 2 | none | `H1=Z³` |
| Four-vertex path with both endpoint triples supported | 3 | `rank d1=2` | `H1=Z` |
| `K2,2`, height-two coarse poset | 2 | none | `H1=Z⁴` |
| `K2,2`, one colour ordered | 3 | `rank d1=2` | `H1=Z²` |
| `K2,2`, four-state coarse chain | 4 | `rank d1=4` | `H1=Z` |
| Six-cycle, height-two coarse poset | 2 | none | `H1=Z⁶` |
| Three-edge star with ordered leaves | 4 | `rank d1=3` | `H1=Z` |

The same abstract graph can have different mixed-core support and different homology. Both same-colour comparabilities and available links matter. The old ordered-star counterexample is retained and verified.

## Larger star search and integral `d2` witness

The targeted search samples `Q={0}+R`, with bottom `0` 1-only and each point of `R` either 0-only or split. It therefore stays inside exclusive stars, hence inside Ferrers and chordal-bipartite graphs. Seed: `2026092902`.

The search was capped at 10,000 trials and **stopped on its first higher-page witness after 414 trials**, using 7–10 coarse states. This took 1.61 seconds; the largest sampled mixed complex had 4,988 simplices. The first witness had ten states. Exhaustive induced-subset testing of that particular witness, retaining its bottom, produced the following seven-state witness. It is not asserted to be globally minimal.

Its coarse Hasse covers are

```text
0<1, 0<2, 1<3, 2<3, 2<5, 3<4, 3<6, 5<6.
```

Its availability profile is `(1,2,0,0,2,2,0)`, where `2` means split. Thus `P={0}`, `Z={2,3,6}`, and the exclusive graph is `K1,3`. The mixed chain complex has 79 simplices and maximal core size four.

Integral Smith calculations give exactly:

```text
E1 = E2:
  (filtration,total degree)=(2,3): Z²
  (filtration,total degree)=(4,4): Z
  all other groups zero.

H3(K,U;Z)=Z, all other mixed homology zero.
Reduced H2(Cone;Z)=Z, all other reduced cone homology zero.
```

Only one differential can change these groups: `d2:Z->Z²`, from `(4,4)` to `(2,3)`. It is injective with primitive image, so its only nonzero Smith invariant factor is `1`. In suitable integral bases it is the column `(1,0)`. The sequence collapses at `E3`, not `E2`.

The proof certificate goes beyond matching ranks. `verify_d2_certificate.py` carries out **unit-pivot integral** filtered reduction, asserting that every pivot used is `±1`. It constructs actual signed chains `x` of core size four and `y` of core size three, and verifies

```text
d0 x = 0,
d1 x + d0 y = 0,
d0(d1 y) = 0.
```

The chain `d1 y` represents the nonzero `d2` image. All oriented simplex coefficients, the first-page integral groups, the total integral groups, and the interval pair are stored in `star_d2_integral_certificate.json`. A readable geometric/link proof is supplied separately in the gate's theory notes.

## Maximum-degree-two four-cycle obstruction

The independent structural search is documented in `verify_c4_search.py` and `c4_search.json`. It ran 20,000 seeded trials with 6–10 coarse states and an exclusive `K2,2`, obtaining five `d2` witnesses. There were 15,655 distinct labelled poset/profile pairs; no isomorphism deduplication is claimed. Runtime was 127.828 seconds, seed `2026092917`. These totals are separate from the main exhaustive table and the star-targeted sample above.

The resulting eight-state witness has availability `(1,2,2,1,2,0,0,2)` and strict relations given by the upward lists

```text
0 < 2,3,4,5,6,7
1 < 2,3,4,5,6,7
2 < 5,6,7
3 < 4,5,6,7
4 < 6,7
5 < 6,7.
```

Its exclusive sets are `P={0,3}` and `Z={5,6}`, with all four comparisons present. Its integral first page equals its second page and has exactly `Z` at `(filtration,total_degree)=(2,3)` and `Z` at `(4,4)`. Both the mixed complex and the direct cone pair are integrally acyclic. Therefore `d2:Z->Z` is an isomorphism with Smith invariant `1`.

`c4_d2_integral_certificate.json` independently records full signed chains `x,y`, the checked zigzag identities, unit-pivot integral persistence, and integral first-page and total homology. This is separate from the structural agent's link-by-link proof and explicit target-cycle certificate. The small four-state `K2,2` chain in the local table does not reveal this obstruction; the extra available vertices change the link interactions.

## Limits and retained boundaries

- Absence of `d2` through five states does not prove a collapse theorem; the seven-state star explicitly defeats that extrapolation.
- The existence of a four-vertex core alone does not force `d2`: the four-state chain `K2,2` example has only `d1`.
- The main exhaustive run is over `F2`; all integral claims here name the selected or explicit cases actually checked.
- No general conclusion about torsion, integral extension problems, total unimodularity, or homotopy type follows merely from the field page dimensions.
- Matching permits inherited link torsion, as established before this gate. The main gate's separate torsion construction addresses torsion produced by interaction.
- The field persistence calculation detects ranks. General signed formulas and theorem-level collapse statements require the independent chain-theoretic arguments in the gate.

## Frozen handoff audit

Before new research, all 83 entries of the consolidated archive's SHA256 manifest and all 23 entries of the latest-gate nested manifest matched. The current v0.3 manuscript source matches the latest gate's `BASELINE_DRAFT_v0.3.tex`; both copies of `MANUSCRIPT_REVISION_SECTION.tex` also match. The latter is a separate candidate insertion and remains unmerged.

The saved older computations agree with their stated principal scope: 3,242 matching integral cases through four coarse states, 1,707 product-link checks over `F2`, 639 nonempty matching five-state samples over `F2`, direct integral `B2` and `B3` examples, and a theorem/link prediction for `B4` only. One minor reporting distinction is that the old Horn script directly checks minima/maxima of the relation and its projection; it does not separately assert projection meet/join closure, although that closure is an elementary algebraic consequence.

Notation must continue to distinguish reduced topological cone homology from ordinary topological `H0`, and the distributive endpoint construction requires distinct bottom and top (nonempty generating poset). No frozen manuscript or handoff source was edited.
