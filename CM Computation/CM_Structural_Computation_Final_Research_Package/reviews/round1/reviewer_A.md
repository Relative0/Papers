# Round 1 Reviewer A: Boolean decomposition and logic synthesis

**Status:** internal AI role-based adversarial review of frozen Draft 1. Not an external referee, separate model, or independently recruited reviewer.

The report's actual contribution is not a new Boolean decomposition algorithm. It assembles exact factors into a conditioned-query interface and audits one implementation. The best publication argument is the distinction between discoverability, representational validity, and downstream utility. The strongest argument against a research-paper submission is that standard DSD/ACD methods already address far richer structural decomposition, while the new portfolio is deliberately restricted.

Major request R1-A1: connect the actual recovered four tags to the new representation through executable conversion, including the row/column factor ordering of Kronecker products. An explanation that both are products is mathematically adequate but not sufficient for reproducibility. R1-A2: report candidate-universe coverage and avoid 'best decomposition' without the frozen qualification. R1-A3: characterize ordinary cofactor multiplicity versus complement prototypes. A prototype index plus a complement bit can be redundant compared with optimized ACD functional encodings.

The EPFL controller is a reasonable smoke test, not a cut benchmark across independent circuits. All 26 outputs include small and constant functions, so container overhead is unsurprising. Do not call all-flat selection evidence that natural functions lack decomposition. An appendix giving ideal-size incidence versus encoded size would answer this directly.

Minor requests: preserve the source variable order; document off-set cube handling; give one decoded legacy Kronecker example. The fatal flaw test is whether the new paper would falsely inherit the compiler's P14 evidence. It does not currently do so. My recommendation is a useful technical report after adapter and size-sensitivity revisions; I do not require the entire ABC infrastructure for that modest form.
