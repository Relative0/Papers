# LM-centered revision notes

This revision updates the Astra-revised CM/LM foundations manuscript in response to the latest author feedback.

## Main changes

- Re-centered the abstract, introduction, discussion, conclusion, and subtitle on **formula-valued Logical Matrices (LMs)** rather than treating CM-level pointwise fusion as the principal focus.
- Recast the numeric CM superposition law as a **valued corollary** of the symbolic LM operator-superposition theorem. The manuscript now states explicitly that the raw numeric entrywise law has direct truth-vector prior art (Cheng, Zhao, Xu 2011).
- Added a cautious literature statement that, in the inspected Cheng source, the relevant construction is truth-vector/Boolean-matrix based; no formula-valued LM polarity lift, current logical-pairing identity, or bra-matrix-ket semantic layer was located there.
- Promoted a new main theorem titled **Aligned LM operator superposition and CM valuation**, with the LM identity first and valuation/CM selection as consequences.
- Added an LM-first worked example showing
  \[
  [M_{X\lor Y}]\widehat{\Updownarrow}[M_{X\land Y}]
  = [M_{X\Updownarrow Y}],
  \]
  and connected it explicitly to valuation and logical pairing.
- Retained the frame-alignment implication example to show why "same ordered operands" is a semantic type condition rather than merely an array convention.
- Added a notation/type convention: uppercase `X,Y,A,B,...` denote formulas/logical operands; lowercase `x,y,a,b,c,d,...` denote Boolean values, assignments, or scalar coefficients.
- Clarified that uppercase operands may be arbitrary formulas, not just atomic variables, but that **matrix/operator-valued LM entries are not assumed** in the current theory. Added operator-valued enrichment as an open direction.
- Improved all four TikZ diagrams with larger boxes, more horizontal/vertical breathing room, and label backgrounds/spacing so arrow text no longer collides with diagram content.
- Removed the duplicated OR/AND/XOR superposition example after the coherence theorem, replacing it with a shorter remark showing that logical pairing preserves the earlier LM operator calculation.

## Verification

- The revised manuscript compiles cleanly with no LaTeX overfull/underfull-box or undefined-reference warnings.
- The PDF was rendered and visually checked, including the revised diagrams.
- The existing independent finite checker still passes all **20,873** checks, covering frame normal form/valuation, all 4096 binary outer-superposition triples, the typed alignment example, matched-frame products, the corrected valuation-axis convention through arity three, and all 2x4 rank-one/separability cases.
