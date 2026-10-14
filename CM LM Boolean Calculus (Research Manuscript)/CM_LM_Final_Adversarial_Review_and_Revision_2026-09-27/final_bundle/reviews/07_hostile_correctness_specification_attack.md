# Hostile Review B - Correctness, typing, and edge-case attack

**Mandate:** search for a concrete false statement, type error, counterexample, or degenerate case that breaks the advertised calculus.

## Attack targets
- dependent formula references rather than free Boolean variables;
- frame inversion and valuation order;
- unmatched input frames under pointwise superposition;
- symbolic signed permutations and polarity masks;
- output complement versus input-frame actions;
- zero-rank factorization;
- empty row/column blocks in flattenings;
- STP row/column orientation;
- matched-frame XOR-AND products;
- confusion between pointwise superposition and matrix multiplication.

## Defects actually found
1. **STP orientation defect.** The prose treated vec([f]) as a row vector although vec was defined as a column vector. This is a real dimensional inconsistency.
2. **Signed symbolic transport specification gap.** The pre-revision text did not state exactly whether the polarity mask lived in the reference tuple or in the slot index. An implementation could therefore apply the mask twice and silently cancel it.
3. **Degenerate conventions.** The zero-rank theorem and higher-arity flattening discussion needed explicit empty-XOR/empty-product conventions.

## Counterattacks that failed
I did not find a counterexample to the binary frame normal form, inverse frame identity, agreement-bit pairing, aligned Boolean superposition, higher-arity lift, partition-selector preservation law, matched-intermediate-frame product, rank/separability theorem, or the declared ANF/spectral boundary when read with their stated assumptions.

## Revision response
All three actual defects/gaps were repaired. The signed transport law is now written explicitly and includes a one-variable double-mask counterexample. The STP orientation is dimensionally consistent. Degenerate conventions are explicit. The new independent checker contains signed symbolic transport tests and boundary witnesses.

## Post-revision hostile verdict
No central correctness blocker remains from this attack. A future referee may dislike the level of novelty, but I do not currently have a concrete mathematical falsification of the paper as revised.
