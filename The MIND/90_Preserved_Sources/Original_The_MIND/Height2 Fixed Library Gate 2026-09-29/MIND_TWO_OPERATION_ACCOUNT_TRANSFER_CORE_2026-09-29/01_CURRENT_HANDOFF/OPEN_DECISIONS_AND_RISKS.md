# Open decisions and risks

## Mathematical risks

1. Query repair-safety may turn out to be hereditary under all relevant support restrictions, killing the activation/deactivation idea. This must be tested, not assumed.
2. The fixed-library model may reduce to an ordinary restricted decision tree with a state-dependent legal-action predicate. If so, the contribution must come from a new structural theorem about that predicate, not from the recursion itself.
3. Simultaneous block safety must not be conflated with sequential one-bit safety. ProLT v0.5 has explicit interaction phenomena.
4. Repair-forest equivalence is currently a one-bit height-two theorem. Do not silently transfer it to multi-bit blocks.
5. Relative boundary/mapping-cone conventions must preserve degree/sign conventions from the audited source.

## Novelty risks

Search against:

- restricted Twenty Questions;
- optimal decision trees;
- active learning with constrained queries;
- adaptive test cover / separating systems;
- graph-constrained queries;
- matroid-constrained adaptive selection;
- finite-space/discrete-Morse repair literature;
- graphic/cellular matroids.

## Project-management risk

Do not lose track of which documents are exploratory versus corrected. `THEOREM_STATUS.csv` and `MASTER_HANDOFF_FOR_NEW_ACCOUNT.md` are the current truth source for this branch.
