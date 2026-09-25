# Finite Checks

## `lm_modal_bridge_checks.py`

This is the expanded independent checker used for the final bridge report. It implements `A = F2[u]/(u^4)` directly as 4-bit coefficient vectors and checks the finite claims without importing the supplied research implementation.

It verifies:

1. the ring's 16 elements, 8 units, and exactly two idempotents;
2. `|GL_2(A)| = 24,576`;
3. 192 unordered reversible projective two-outcome bases modulo independent unit row scaling and outcome swap;
4. the branch projectors `J_i^B = B^{-1} P_i B` are idempotent, mutually orthogonal, and resolve the identity;
5. for every projective basis, both outcomes, and all 256 one-system states, `J_i^B psi != 0` iff `(B psi)_i != 0`;
6. same-basis repeatability/support concentration;
7. invariance of the branch projectors under independent unit scaling of measurement rows;
8. the symbolic-support theorem for every `q` in `B tensor A` when `B` is the four-element valuation space of two Boolean variables: 65,536 symbolic scalars times four valuations = 262,144 checks;
9. lack of closure of the 16 Paper-B LM family under ordinary Boolean-ring matrix multiplication: 144 of 256 products leave the family;
10. failure of the nonzero support map to preserve XOR-addition and multiplication;
11. a nonzero tensor product that vanishes because of zero divisors;
12. a unimodular bipartite preparation whose conditional state is nonzero but nonunimodular.

Run:

```bash
python tests/lm_modal_bridge_checks.py
```

The exact recorded output is `lm_modal_bridge_checks_output.json` and the rerun output is `expanded_rerun.log`.

## Original first-pass checker

`cm_bridge_checks_original.py` and its output are preserved unchanged from the first research pass. `original_rerun.log` confirms that it also runs successfully in the packaging environment.
