# Round 1 Reviewer E: Research software and reproducibility

**Status:** internal AI role-based adversarial review of frozen Draft 1. Not an external referee, separate model, or independently recruited reviewer.

The source hash, original archive, executable H1--H6 examples, and separate scalar checker make the report unusually auditable. The checker does not call the artifact's query logic, which is a meaningful implementation separation. It is not an independent formal specification, and the same assistant wrote both modules.

R1-E1: freeze code snapshots with each draft, not just the TeX. Otherwise later fixes can silently change reproduction of v1 results. R1-E2: the legacy adapter should be tested with all four tags and malformed/cost-modified records. R1-E3: add sequential conditioning, retained unused variables, all-fixed constants, nonminimal rank, complement-merge, and wrong-source tests outside the n<=3 enumeration.

The phrase 'full lifecycle' needs an access-model qualification. The common truth-vector construction is excluded, and decoded baseline objects are parsed rather than restored into a fresh process. This is a construct/verify/serialize/parse benchmark, not a cold disk-cache experiment. Say so. Actual RSS was not measured. Literal-mask memory has a cost even when the source payload is small.

I checked the stored result counts against the test loops and the source contract examples. They are consistent. The fatal flaw test is accepting a malicious document because it supplies a matching new source hash: H3 demonstrates why the external truth is the authority. Do not call H3 a failure of SHA-256. Strong recommendation for a report once version snapshots, adapter coverage, and access-model wording are tightened.
