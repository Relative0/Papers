# Revision changelog after specialist and hostile review

## Mathematical/specification repairs

- Corrected the STP row/column convention by using the transpose of the column vectorization where a row truth vector is required.
- Added the explicit symbolic signed-frame transport identity, including exact placement of permutation and polarity masks.
- Added an explicit warning and arity-one counterexample showing the double-mask failure mode.
- Expanded the higher-arity logical-pairing proof to identify the unique selected polarity tuple under a valuation and the resulting agreement bits.
- Added the zero-rank convention: the empty XOR decomposition represents the zero function/matrix.
- Added empty-block and empty-Kronecker-product conventions for degenerate flattenings.
- Added a noncontiguous ordered-flattening example to make the row/column type contract concrete.

## Contribution and exposition repairs

- Sharpened the title to **Correspondence and Logical Matrices: A Typed Boolean Operator Calculus**.
- Rewrote the opening contribution statement so the paper claims a typed synthesis/integration, not a new underlying Boolean algebra.
- Added a complete end-to-end frame-alignment example using two implication occurrences. The example exhibits an actual wrong result before transport and the correct XOR result after transport, at both numeric and formula-valued levels, followed by logical pairing.
- Clarified throughout that pointwise Boolean superposition and XOR-AND matrix multiplication are different operations.
- Reduced phase/quantum-adjacent material to a boundary discussion rather than allowing it to compete with the foundations contribution.
- Renamed the spectral appendix so it no longer promises a complete atlas.
- Cleaned project-history/review-response language from the submission manuscript.

## Literature/priority repairs

- Explicitly credited Cheng, Zhao, and Xu (2011), Proposition 3.3, for the same-frame entrywise truth-table composition law.
- Added a direct comparison with the two-dimensional Boolean-frame mechanism implicit in Gudder and Latremoliere's stochastic-vector/cyclic-basis construction.
- Updated Eigenlogic positioning to the published 2020 Toffano version of record rather than relying on a fragile version-specific historical statement.
- Replaced the Zhao/Gao/Cheng placeholder with an identifiable undated author-hosted preprint record.
- Normalized the Mizraji bibliographic metadata.
- Added the 2025 Binary Matrix Product representation as a contemporary comparison and distinguished its compression-oriented objective from the exact uncompressed CM/LM truth tensor.
- Preserved explicit language that targeted literature searches do not certify historical firstness.

## Reproducibility and submission hygiene

- Removed reliance on the unrecovered historical 20,873-check provenance.
- Included a self-contained independent checker and machine-readable run record.
- Fresh verification passes **2,022,648 explicitly counted assertions**, including boundary counterexamples and signed symbolic transport tests.
- Final LaTeX build produces a 32-page PDF with no unresolved references/citations and no overfull/underfull box warnings.
- Rendered and visually inspected the final PDF, with targeted checks of the new worked example, signed transport law, related-work table, and finite-verification appendix.
- PDF metadata now matches the sharpened title.
