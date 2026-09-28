# Draft 2 claim crosswalk

Draft 1 crosswalk remains valid for historical v1 results. The additions are:

| ID | Claim | Location / code / data | Evidence status |
|---|---|---|---|
| C10 | Rank-profile count identity; explicit-size row streaming | Section 7; `walsh_count`; extensions_v2.json | Proof plus all 65,536 binary 4x4 matrices |
| C11 | Factor-only minimal recompression | Section 7; `recompress_rank`; checker.minimal_rank_witness | Standard linear algebra proof; 2,000 checks |
| C12 | r <= k+delta and k <= 2^(r-delta) | Section 8; extensions_v2.json | Quotient-space proof plus exhaustive 4x4 matrices |
| C13 | Fixed-cut dictionary gap and field-rank gap | Section 8; field_ranks_v2.json | Proof; exact rational elimination r=1..5 |
| C14 | Binary versus JSON changes selections | Section 10.4; benchmark_v2_binary.json | Same-data exploratory sensitivity |
| C15 | Legacy semantic interoperability | Section 11; legacy_adapter_v2.json | 675 artifacts, 6,750 queries; not identical search |
| C16 | Sequential/fused/binary updates agree | Section 11; extensions_v2.json | Finite tested domain, not proof of all Python behavior |

Counts, exact source pins and verification limits are not claims of independently replicated peer review. Q=1000 values are modeled rather than directly executed thousand-query pipelines.
