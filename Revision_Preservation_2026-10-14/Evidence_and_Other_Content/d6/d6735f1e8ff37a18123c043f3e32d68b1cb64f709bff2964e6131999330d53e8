# CM/LM foundations manuscript - publication-readiness revision notes

## Revision target

**Correspondence and Logical Matrices: A Boolean Operator Calculus**  
*Formula-valued logical matrices, valuation, pairing, and coherent operator superposition*

This revision implements the publication-readiness program identified in the 26 September 2026 audit without changing the paper into the compiler paper or the cyclic-phase/modal paper. The sound frame, pairing, selector, arbitrary-arity, flattening, block-lift, and rank mathematics is retained. The main changes are claim calibration, exact frame typing, prior-art comparison, reproducibility, and a single end-to-end example that demonstrates usefulness.

## Substantive mathematical changes

1. **Exact symbolic signed-frame transport is now a theorem.** The manuscript now states explicitly
   \[
   \mathcal L_{\mathbf X}(f\circ\phi_{\sigma,\epsilon})[\alpha]
   \equiv
   \mathcal L_{P_\sigma\mathbf X}(f)[P_\sigma\alpha\oplus\epsilon]
   \equiv
   \mathcal L_{\phi_{\sigma,\epsilon}(\mathbf X)}(f)[P_\sigma\alpha].
   \]
   A companion remark explains that the polarity mask is applied once: either in the polarity index or in the transported reference formulas, not both.

2. **Dependent formulas are used to clarify what an LM preserves.** A new example takes `X=Y=P` and XOR. Although the all-positive reference formula collapses to false, the full LM remains the swap matrix and the inverse frame identity still reconstructs the represented connective. This makes the distinction between the ring identity and a jointly satisfiable all-true valuation explicit.

3. **The block-lift theorem is explicitly conditional.** A new limitation remark uses equality of two two-bit blocks to show that not every function across a bipartition factors through one Boolean summary bit from each block.

4. **The rank theorem handles the zero function exactly.** The minimum XOR-decomposition length now allows `k=0`, with the empty XOR representing the zero function. A bipartition-dependence example is included.

5. **Closure language is narrowed.** Boolean closure is stated as closure of the scalar/entrywise algebra and not as closure of every specially shaped state family under arbitrary vector operations.

## One running example now carries the usefulness argument

The former collection of short examples is centered on
\[
F(X,Y)=(X\Rightarrow Y)\oplus(Y\Rightarrow X).
\]
The example begins with the concrete failure mode: the two local implication occurrences have identical local truth arrays, so frame-blind entrywise XOR would incorrectly return zero. It then:

- transports the second occurrence from `(Y,X)` to `(X,Y)` by transposition;
- performs the aligned LM-level outer operation;
- obtains the XOR LM;
- pairs the result against formula states and verifies the agreement-bit semantics;
- distributes pairing through the aligned operator calculation;
- valuates to the numeric CM and obtains the same scalar result.

This turns frame typing from a bookkeeping convention into a demonstrated semantic safeguard.

## Prior-art and claim-boundary repairs

The introduction and related-work table now distinguish the manuscript's integration claim from known ingredients.

- **Cheng, Zhao, Xu (2011), Proposition 3.3** is identified as a direct antecedent for entrywise application of an outer logical operator to aligned truth vectors. The CM same-frame law is therefore not presented as a new numerical identity.
- **William Bricken (technical note internally dated March 1997)** is identified as a direct antecedent for 2x2 logical matrices and explicit bra-matrix-ket evaluation. The note's arithmetic conventions are distinguished from the manuscript's uniform XOR-AND coefficient algebra.
- **Gudder and Latremoliere (2009), Example 2.13** is now compared directly with the complementary frame matrix: the cyclic basis generated from the two-component Boolean partition `(X, not X)` has exactly the row/column pattern of `S_X`. Their vector addition is Boolean join, not unrestricted XOR, so the two calculi are not identified globally.
- **Toffano, Eigenlogic** is described with version-specific chronology: the work was first posted in 2015, while the cited statement about deliberately avoiding Dirac notation occurs in version 12 dated 6 February 2018.
- The unresolved `ZhaoSTP` bibliography placeholder is removed and replaced with the published Cheng-Qi-Li Springer book, including the chapter *Matrix Expression of Logic*.
- Bibliographic metadata was tightened for Edwards, Mizraji, Cheng/Qi, Mishchenko-Chatterjee-Brayton, Zhou-Wang-Mishchenko, Rutherford, Blyth, and Gudder-Latremoliere.

The revised contribution language makes no firstness claim for formula-valued matrices, bra-ket logical notation, pointwise truth-vector composition, or complementary Boolean frames individually. The paper instead emphasizes the integrated reference-polarity architecture, agreement-pairing semantics, and explicit symbolic/numeric transport contracts.

## Reproducibility repair

The manuscript no longer states that the unrecovered historical **20,873-check** checker accompanies the revision. That historical run could not be reconstructed from the supplied archive.

A new standard-library release checker is included as `independent_verify_release.py`. A clean rerun on 27 September 2026 reports:

- status: `PASS`
- explicitly counted checks: **2,022,648**
- checker SHA-256: `adb8d2c30eee7bfb30ba86948cd15ee5889dcaabf9542b1c29286b1f3439d336`

The output distinguishes these new checks from the unreproduced historical count. It also records expected counterexamples to stronger claims deliberately excluded by the manuscript.

Run with:

```bash
python independent_verify_release.py --output verification_release
```

## Build and visual QA

The revised source compiles with `pdflatex` in two passes to a 34-page PDF. The final log contains no unresolved references, unresolved citations, overfull boxes, underfull boxes, or LaTeX/package warnings detected by the release grep. The PDF was rendered page-by-page at 160 dpi and visually inspected, with focused checks on the end-to-end example, signed-frame theorem, notation table, verification note, and bibliography.

## Files in the release bundle

- revised LaTeX source
- compiled PDF
- this revision note
- unified source diff against the audited manuscript
- release verification script
- verification results
- compact 16-CM atlas emitted by the checker
- boundary-counterexample ledger emitted by the checker
- SHA-256 manifest
