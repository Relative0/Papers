# Final executive summary

## 1. What emerged

A complete 15-page third-draft technical report: **Exact Boolean Decomposition Artifacts under Conditioning: Algebraic Contracts and a Reproducibility Audit**. It is self-contained as a report about Boolean functions and exact data structures; it does not require a new CM formalism.

The direction is viable as a focused standalone **technical report**. The evidence does not yet justify presenting it as a mature new decomposition theory or competitive general-purpose Boolean engine. That is a narrower judgment than the original assistant's optimistic high-potential methods-paper assessment.

## 2. What is new in this work, versus historically novel

This pass contributes a concrete source-contract audit, a new tested reference implementation with explicit persistence semantics, an adapter for all four old artifact types, actual binary-format and fused-query sensitivities, and a corrected fresh-instance replay experiment. These are new work performed here.

The mathematical content is proved and useful, but no historical-first claim is made for restriction closure, XOR sign-sum counting, linear rank recompression, quotient-space bounds, or elementary information/query lower bounds. The report's possible contribution is their disciplined integration with an auditable implementation and evidence trail. Whether that integration clears a particular research venue's novelty bar remains unestablished.

## 3. Proposed novelty rejected or narrowed

'Compile once, query repeatedly', Boolean conditioning/counting, tensorized Boolean representations and certified knowledge compilation are established ideas. GF(2) rank factorization, prototype grouping, Kronecker products and disjoint-support decomposition are not new because they are used within CM work. The small containment/orbit atlases are not a sufficient paper spine. The fixed-cut inner-product separation is not a separation between optimally reordered whole portfolios.

## 4. New mathematical and software work

The report formalizes exact artifact scopes, including constants and unused declared variables; direct restriction and counting; a rank-profile character identity; a row-streaming alternative; factor-only minimal recompression; complement-quotient rank bounds; and a fixed-cut example separating GF(2), real and dictionary sizes.

The final revision adds two concrete warnings. First, `f(x,y)=xy` and `g(x,y)=(1-x)y` have identical unconditional rank-profile histograms and count one, but their counts after x=0 are zero and one. Assignment associations must persist. Second, `xyz XOR x XOR y` has one connected ANF component, but fixing z=0 reveals two. A retained factor list and a newly optimized decomposition have different monotonicity properties.

A deterministic exact source-verification lower bound is proved only for individual black-box value queries. It does not apply indiscriminately to formula proofs, trusted aggregate metadata or all possible representations.

## 5. Which results survived the internal attacks

All stated conditional mathematical results survived the role-separated checks. The strongest executable coverage includes 105,292 small-domain conditioning checks, all 65,536 binary 4x4 matrices for the rank/prototype/profile identities, 2,000 factor-only recompressions, 675 converted legacy artifacts with 6,750 query comparisons, and 7,070 final three-backend persisted-query comparisons. A clean-directory replay reran eight correctness commands successfully.

These are finite verification domains and same-assistant checks, not formal proof certification or independent external review.

## 6. What the experiments actually establish

The external corpus is all 26 outputs of one pinned EPFL control design; the other 12 cases are intentionally synthetic at n=4,8,12. All methods agree on the tested model counts.

JSON selection picks flat storage on every external output. Compact binary selection instead picks fourteen products and two rank artifacts, leaving ten flat. Thus the earlier result did not establish absence of useful structure. One external output uses 13 binary bytes versus 16 raw truth bytes. At n=12, the parity, inner-product and product-of-XOR controls use 29, 23 and 29 binary bytes versus 512 raw truth bytes.

Earlier timing arms summed setup and warm query costs, with Q=1000 modeled rather than directly executed. The second audit found that baseline loads parsed data but reused existing live objects. The final experiment repaired that issue: 570 actual build--check--save--reload--recheck--query trials execute 128 queries each on fresh loaded states. **No artifact pipeline has a lower per-case median than packed counting on any of the 38 cases.** This is a narrow reference-implementation result, not an impossibility theorem about structural computation.

## 7. How the drafts differ

| Draft | Main content | Substantive evolution |
|---|---|---|
| v1, 9 pages | Exact scopes/closure/counting, six old-source contract observations, first reference experiment | Establishes a coherent report rather than a catalogue of ideas |
| v2, 12 pages | Rank profiles, recompression, quotient/field gaps, legacy adapter, binary/fused sensitivities | Challenges the initial representation and cost assumptions with actual new work |
| v3, 15 pages | Persistent-state limits, source-access bound, constructor repair and true fresh-instance replay | Repairs a real measurement gap and sharpens the report's claims and limitations |

## 8. Strongest remaining objections

The principal objections are uncertain novelty, missing optimized CUDD/DSD/ACD/KC/tensor comparisons, one external design, no RSS or cold-disk study, and absence of formal or external independent proof review. No favorable internal reviewer assessment removes them.

## 9. Difference from neighboring papers

`CM-LMs and lifting` retains the CM/LM calculus, valuation, logical pairing, arbitrary-arity lifts, signed frames and foundational rank/separability discussion. The pair compiler retains compilation rules, S/T/H and P14 evidence. This report owns the persistent-data-structure contract, reproducible boundary audit and the new exact-count experiment. It does not recast the other papers' theorems or speedups as new contributions.

## 10. Standalone viability and audience

A standalone methods/reproducibility technical report is supported. It is useful to readers working on exact symbolic representations, Boolean decomposition and experimental correctness. A competitive novel theory/systems submission needs an additional differentiated contribution and stronger evaluation. No acceptance prediction is made.

## 11. Deliberately excluded future work

Structural retrieval, learned routing, sixteen-operator atlases, weighted/care-set counting, large formula compilation, general tensor-network dichotomies and phase/modal results remain separate. The deferred-directions register preserves the ideas and why they were excluded.

## 12. Recommended next gate

Do not expand the paper's scope simply to create novelty. First identify one stronger, testable advantage: a proved query/space regime not already supplied by standard representations, or a repeatable gain on broader external functions with optimized comparators and full setup costs. Until then, retain the present result as a transparent technical report.
