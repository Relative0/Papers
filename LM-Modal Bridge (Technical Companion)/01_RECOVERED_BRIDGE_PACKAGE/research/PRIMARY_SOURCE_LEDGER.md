# Primary Source Ledger

This ledger records the primary CM/LM sources actually inspected for the bridge investigation.

## 1. Paper B

**Title:** Operator-Level Boolean Computation with Correspondence Matrices  
**Library filename:** `operator-level-boolean-computation-with-correspondence-matrices.pdf`  
**ChatGPT Library file id used during review:** `file_0000000070d882099cdc77a26444ee9c`

### Key passages inspected

- Parsed lines 560-611: Section 8.1, formula-valued LMs and positive/general valuation.
  - Defines `F` as the Boolean algebra of formulas modulo logical equivalence.
  - Defines polarity orbit `X_1=X`, `X_2=not X`, `Y_1=Y`, `Y_2=not Y`.
  - Defines the formula-valued LM as an XOR sum of polarity outer products.
  - Expands the LM to the four formula entries `X Theta Y`, `X Theta not Y`, etc.
  - States positive valuation recovers the numeric CM.
  - States general valuation gives row/column frame permutations.

- Parsed lines 613-669: Section 8.2, logical pairing and valuation theorem.
  - Defines formula states `(A, not A)`.
  - Shows their XOR-AND contraction gives logical equivalence.
  - Defines logical pairing `P = <L1| LM |L2>`.
  - Proposition 2: pairing identity `P = (L1 <-> X) Theta (Y <-> L2)`.
  - Theorem 3: valuation commutes with LM pairing.
  - Explicitly says the word "measurement" is nonphysical and does not assert Born probabilities, collapse, entanglement, or quantum speedup.

- Parsed lines 780-874: proof appendix and finite verification scope.
  - Gives the proof of the pairing identity and valuation commutation.
  - Distinguishes ANF conversion from LM valuation.
  - Lists finite checker coverage.

### Imported background rather than new bridge novelty

- formula-valued LM definition
- positive/general valuation
- logical pairing
- valuation commutes with pairing

## 2. Pure Boolean Modal CM Addendum

**Library filename:** `PURE_BOOLEAN_MODAL_CM_ADDENDUM.tex`  
**ChatGPT Library file id used during review:** `file_00000000a4b882119ec1daed8b247daf`

### Key passages inspected

- Lines 45-58:
  - Explicitly separates the original CM formalism from the later cyclic multiplication.
  - States: the modal readout is an **additional contract**.
  - Defines a joint outcome to be possible iff its coefficient is nonzero in `A`.
  - States this is a support rule, not a probability rule or collapse law.

- Lines 59-92:
  - Defines the cyclic CM phase ring.
  - Gives `A ~= F2[C4] ~= F2[u]/(u^4)`.
  - Gives the ideal chain and unit characterization.

- Lines 93-118:
  - Defines one-bit and two-party ring-valued states.
  - Defines CM-separability.
  - Defines local two-outcome measurement bases as effect rows of invertible matrices in `GL_2(A)`.
  - Defines projectivization by unit row scaling.
  - Counts 192 unordered reversible projective bases.

- Lines 440-539:
  - Uses the complete 192-basis family.
  - Defines support contextuality hierarchy.
  - States and proves the Smith/contextuality trichotomy.

- Lines 620-643:
  - Explicitly says a formal multi-round measurement/update theory remains an open enlargement of the present calculus.

## 3. Supplied adversarial-review archive

**Filename:** `CM_Adversarial_Review_2026-09-18(1).zip`

This archive is included unchanged under `inputs/` and unpacked under `prior_adversarial_review/`. It contains:

- annotated bibliography
- complete research dossier
- formal theorems
- novelty matrices
- paper blueprint
- search log and search scope
- source-hash audit
- reproduction scripts and logs
- audited Bell/GHZ/contextuality data
- 192-basis measurement audit
- full 65,536-resource inventory
- teleportation and dense-coding computational outputs
- independent extension checks

## Raw-byte availability note

The current runtime could read Paper B and the modal addendum through the File Library's parsed-text interface, but the Project files did not expose an authorized raw-byte materialization path. For that reason, the original Paper B PDF is not duplicated in this ZIP. The line-level ledger above is included so a future agent can request the exact passages or match them against a separately supplied copy of Paper B.
