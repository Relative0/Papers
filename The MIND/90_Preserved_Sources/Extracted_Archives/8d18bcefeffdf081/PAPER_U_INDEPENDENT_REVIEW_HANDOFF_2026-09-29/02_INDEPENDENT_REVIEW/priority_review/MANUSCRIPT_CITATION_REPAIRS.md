# Proposed citation repairs

Only the parent review edits the manuscript. These are supported by source_audit.json and PRIORITY_REVIEW.md.

## New bibliography entry

```bibtex
@article{MemoliSmithWan2023,
 author={Facundo M{\'e}moli and Zane Smith and Zhengchao Wan},
 title={The {Gromov--Hausdorff} distance between ultrametric spaces: its structure and computation},
 journaltitle={Journal of Computational Geometry},
 volume={14}, number={1}, pages={78--143}, date={2023},
 doi={10.20382/jocg.v14i1a4},
 eprint={2110.03136}, eprinttype={arxiv}}
```

## Tower setup insertion

```tex
The quotient metrics are the $t$-closed quotients of
M\'emoli, Smith and Wan \cite[Section 2.1, equation (5), Definition 10]{MemoliSmithWan2023},
with $t=r_k$.
```

This refers to the published numbering. Printed page 87 contains the equation and definition. The arXiv preprint uses Definition 9.

## Ishiki replacement

```tex
The collapse is a special case of Ishiki's pseudo-ultrametric amalgamation
\cite[Proposition 2.31]{Ishiki2023}, taking every within-cell pseudo-ultrametric
to be zero and the index metric to be $\delta_{\PP}$.
```

Definition 2.2 allows zero continuous pseudo-ultrametrics; its extra pleasantness condition is unnecessary for this conclusion. The finite index metric is discrete automatically. Paper U's own lemma still establishes that original distances give a well-defined index metric.

## Kleiner locator

Change `\cite[Section 3.4]{Kleiner2020}` to `\cite[Sections 3.3--3.4]{Kleiner2020}`.

