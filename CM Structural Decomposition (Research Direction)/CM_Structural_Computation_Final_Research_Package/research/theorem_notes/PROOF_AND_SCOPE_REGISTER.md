# Proof and scope register

Full proofs are in the final TeX/PDF; this register records status and assumptions.

| Result | Necessary hypotheses | Status |
|---|---|---|
| Conditioning closure | Declared finite scopes; disjoint factors; fixed-cut Cartesian selection; n=0 allowed | Proved by entrywise substitution; finite exhaustive tests |
| Structural monotonicity | Retained factor list, rank of a restricted matrix, occurring prototypes modulo complement | Proved; not a statement about fresh factor discovery or serialized bytes |
| XOR exact count | Disjoint scopes including irrelevant declared variables; integer counts | Sign-product proof; tested |
| Product/prototype counts | Independent product scopes or correct prototype references/polarities | Proved; tested |
| Rank profile identity | GF(2) dot-product semantics, integer profile multiplicities, specified query | Character identity; all 4x4 matrices tested |
| Transform/stream cost | Dense transform after histogram construction, explicit listed factor input | Explicit operation/workspace bounds; no rank-hardness assertion |
| Factor-only recompression | Exact field arithmetic and rank factorizations | Standard linear-algebra proof; 2,000 updates checked |
| Complement quotient | Nonempty row/column domains; occurring whole-row classes | Elementary quotient proof; exhaustive 4x4 tests |
| Inner-product field/dictionary gap | Fixed x|y cut; explicit prototype dictionary | Proved, exact ranks r=1..5 checked; not an all-order portfolio separation |
| Histogram insufficiency | Named coordinate restrictions | Explicit f=xy, g=(1-x)y counterexample |
| All-query state bound | Deterministic exact answers including complete assignments; fixed-width state | Elementary injectivity/counting proof |
| Black-box source verification | Deterministic zero-error individual value queries; zero candidate | All-zero transcript argument; rank<=1 promise preserved |
| Finest XOR factor increase | Fresh ANF decomposition rather than retained list | xyz XOR x XOR y under z=0; explicit test |

No mathematical result in this register is designated a historically first theorem. Proof correctness and priority are separate questions. The tests do not replace universal proofs, nor do the proofs certify all Python parsing and allocation behavior.
