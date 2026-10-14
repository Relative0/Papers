# Substantive changes: v1 -> v2

- Manuscript grows from 9 to 12 pages, adding explicit proofs rather than only editorial changes.
- New sections: rank profile count formula; Walsh alternative versus row streaming; factor-only minimal-rank repair; complement-quotient bounds; fixed-cut dictionary and field-rank gaps.
- New code: compact bitstream codec, fused exact queries, legacy adapter, factor-only recompression, separate rank-minimality checker.
- New executed evidence: 65,536 matrices, 3,020 sequential/fused checks, 2,000 recompressions, 675 legacy adapters with 6,750 queries, exact field ranks r=1..5, and two new timing arms.
- Minimum-binary selection finds nonflat artifacts on 16 of 26 external outputs. The previous minimum-JSON result is therefore not treated as evidence of structural absence.
- No measured sensitivity arm establishes a timing advantage over the packed baseline in its Q=1000 extrapolation. Lack of optimized competitors is unchanged.
- Publication posture remains a technical report. Elementary identities and fixed-cut bounds are proved but not asserted historically novel.
