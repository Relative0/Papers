# Binary Order Thinning of Finite Posets - post-audit v2

Primary manuscript:

- `binary_order_thinning_finite_posets_post_audit_v2.tex`
- `binary_order_thinning_finite_posets_post_audit_v2.pdf`

Audit/freeze companions:

- `MANUSCRIPT_CHANGELOG.md`
- `THEOREM_DEPENDENCY_MAP.md`
- `SUBMISSION_READINESS_CHECK.md`

Reproducibility:

- `reproducibility/README.md`
- exact seven-state verifier and certificate
- exhaustive two-bit checker and n=1,...,6 rerun outputs
- retained one-bit verifiers and rerun outputs
- run scripts and SHA-256 manifest

The manuscript deliberately separates the explicit mathematical seven-state theorem
from the computer-assisted n<=6 minimality result. It also replaces dependency on the
missing/empty historical v0.3 TeX source with a self-contained chain theorem/proof in
the new manuscript; the archived v0.3 PDF was used as the historical source.

Panel revision v2 adds the dedicated two-layer matching--collapse lemma, UCT coefficient argument, tightened quotient-factorization hypothesis, updated Ferrers prior art, all-r>=2 bit-count padding, and two explanatory figures.
