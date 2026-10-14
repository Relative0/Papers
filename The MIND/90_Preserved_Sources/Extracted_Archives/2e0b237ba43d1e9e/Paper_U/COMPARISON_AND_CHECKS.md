# Comparison and fresh recovery checks
The previous review first recorded independent findings, then read 02_INDEPENDENT_REVIEW/ and the archived original transfer. Its conclusions agreed with the prior topology/tree/source reviews, but did not inherit their scores or claims of source access. Earlier v0.2 problems were already repaired in v0.3. The three new minor changes are definition completeness, cylinder-to-vertex explanation and a closer Dovgoshey completion citation.

The original thesis was inspected only for the correction target: printed p.4/PDF p.5 asserts the ultrametric-to-indiscrete inference, and p.11/PDF p.12 links ultrametric points to indistinguishability. No unrelated thesis theory is certified.

Both supplied scripts are preserved unchanged. The main verifier recursively constructs finite tree automorphisms and selects stabilizers by their actual action; normality tests all subgroup elements against generating adjacent swaps. Its expected formula does not manufacture subgroup orders. The second constructs the ternary group by breadth-first generator closure and independently selects pointwise/setwise stabilizers. Its mixed global group is inferred factorwise, not enumerated as a whole. Testing generator conjugates suffices in the finite groups; infinity is handled by the separate proof.

Both programs are rerun during recovery. checks/RECOVERY_VALIDATION.json records fresh results and output comparisons. The historical XOR and total-variation assertions inside the unchanged main program are executed only as part of the requested existing suite; they do not expand the manuscript.

Reproduction from the extracted Paper_U directory:
```text
python scripts/verify_paper_u.py --out checks/main
python scripts/check_mixed_ternary.py --out checks/ternary
powershell -File scripts/build.ps1
```

The build uses installed pdfLaTeX and Biber, with automatic package installation disabled. Local logreq support is copied from the supplied package. Normal MiKTeX cache access was required outside the sandbox, as in the earlier build. Final PDF pages are rendered and checked; final compiler logs and tests are included.

This recovered ZIP is a new archive with its own manifest/checksum, not a byte-identical recovery of the lost ZIP. The complete original input ZIP is preserved verbatim inside it. The extraction test and recursive ZIP CRC checks concern archive integrity; they are not a second research referee pass.

