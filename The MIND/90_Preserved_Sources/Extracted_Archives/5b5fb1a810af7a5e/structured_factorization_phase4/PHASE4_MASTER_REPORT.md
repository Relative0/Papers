# Structured Factorization Phase 4 — Direct Extraction, CM/LM Rank Recursion, and Incremental Four-Corner SAT

**Date:** 29 September 2026  
**Status:** Research convergence gate completed; two exact direct-extraction subclasses survived, while the unrestricted structured-d-DNNF route did not.

## Executive conclusion

Phase 4 attacked three routes in parallel:

1. direct factor extraction from structured d-DNNF / SDD representations;
2. direct factor extraction from CM/LM operator DAGs;
3. a single-formula, selector-controlled incremental four-corner SAT comparator.

The outcome is not one universal direct algorithm. It is a sharper three-level architecture:

\[
\boxed{
\text{direct exact structure when certified}
\;\longrightarrow\;
\text{decompose into residual blocks}
\;\longrightarrow\;
\text{incremental four-corner SAT only on unresolved blocks.}
}
\]

The two positive theorem classes are:

- **compressed SDDs:** exact extraction of the finest factorization whose factor blocks are vtree subtrees; this becomes the full prime factorization when the vtree is prime-aligned;
- **support-disjoint/read-once CM/LM operator trees:** exact full semantic prime AND-factorization by a local two-state CM-rank recursion.

The unrestricted structured-d-DNNF claim was deliberately rejected. Current knowledge-compilation results show that structured d-DNNF lacks several polynomial-time closure transformations that would make the most obvious extraction proofs work, and a fixed vtree can hide genuine cross-vtree factors.

The incremental SAT branch was upgraded to one permanent four-copy semantic CNF with one selector per carrier block. Candidate cuts are now solver assumptions rather than rebuilt formulas. The present environment did not contain an industrial assumption-capable CDCL solver, so this phase validates **logical correctness and encoding reuse**, not learned-clause runtime speedup.

---

## 1. Baseline carried into Phase 4

The project already had two exact facts:

1. for a fixed cut \(A\mid B\), conjunctive separability is equivalent to CM flattening rank at most one,
   \[
   f(a,b)=g(a)\land h(b)
   \iff
   \operatorname{rank}_{\mathbb F_2}[f]_{A\mid B}\le 1;
   \]
2. if \(\Pi_K\) and \(\Pi_f\) are the finest carrier and semantic partitions, respectively, the finest simultaneous partition is
   \[
   \Pi_{K,f}=\operatorname{LCC}(\Pi_K,\Pi_f).
   \]

Phase 4 asks whether \(\Pi_f\) can be extracted without generic SAT/QBF on useful compiled/operator representations, while retaining SAT as an exact fallback.

---

## 2. Branch A — structured d-DNNF / SDD direct extraction

### 2.1 Negative boundary for arbitrary structured d-DNNF

No theorem was found or proved saying that the unrestricted semantic prime AND-partition can be read from an arbitrary structured d-DNNF in polynomial time.

This is not just a missing implementation detail. Structured d-DNNF is noncanonical and its deterministic OR nodes need not syntactically identify semantically equal cofactors. Moreover, Vinall-Smeeth (IJCAI 2024) proves that structured d-DNNF does not admit polynomial-time negation, disjunction, or existential-quantification transformations in general. Therefore the tempting route “compile, transform, compare/project, and read factors” cannot simply be assumed efficient.

### 2.2 Exact compressed-SDD cut theorem

At a vtree split \(X\mid Y\), a compressed SDD decision node has the form

\[
f(X,Y)=\bigvee_i p_i(X)\land s_i(Y),
\]

where the primes are mutually exclusive, exhaustive and nonfalse, and compression makes the subs pairwise distinct.

For a nonfalse function:

\[
\boxed{
f(X,Y)=g(X)\land h(Y)
\iff
\text{the compressed decision has at most one nonfalse sub.}
}
\]

Reason: fixing \(X=x\) selects exactly one prime, so the corresponding sub is exactly the right cofactor \(f_x(Y)\). A rank-one/AND factorization has only two possible cofactors, \(0\) and one common nonzero function \(h\). Compression merges all equal nonfalse subs.

This is simultaneously:

- an SDD cofactor statement;
- the CM statement that every nonzero row of the \(X\mid Y\) flattening is identical;
- the rank-one criterion already established in the CM calculus.

### 2.3 Finest vtree-laminar factorization

Call a partition **\(T\)-laminar** when each factor block is exactly the leaf set of a vtree subtree. Recursing on the cut theorem gives the unique finest \(T\)-laminar AND-factorization.

If the root cut fails, no nontrivial \(T\)-laminar refinement is possible: every such refinement would regroup into a valid root factorization. If the root cut succeeds, recurse independently on the two factor sides.

If every full semantic prime factor happens to be a vtree subtree, the same recursion returns the unrestricted full semantic prime partition. This is the **prime-aligned vtree corollary**.

### 2.4 Exhaustive four-variable validation and the alignment barrier

Using the fixed balanced vtree

\[
((x_0,x_1),(x_2,x_3)),
\]

`code/sdd_direct_extraction.py` exhaustively checked all 65,535 nonfalse four-variable Boolean functions.

- root cut criterion failures: **0**;
- recursive \(T\)-laminar extraction failures: **0**;
- functions with nontrivial unrestricted prime factorization: **2,601**;
- functions where unrestricted prime factorization was strictly finer than the fixed-vtree-laminar result: **2,376**.

Thus only 225 of the 2,601 decomposable functions had their complete prime partition exposed by this particular fixed balanced vtree. This is a vtree-alignment result, not a negative statement about SDDs in general.

The algorithmic consequence is important: SDD structure should be used to **peel certified factors**, but any unresolved cross-vtree factorization must remain eligible for an exact fallback.

---

## 3. Branch B — CM/LM operator-DAG attack

### 3.1 The attack naturally collapses to a read-once tree theorem

For a single-output operator DAG, genuine reuse of a nonconstant subexpression means repeated variable support. Once two dependent branches reconverge, XOR cancellation, absorption, and other Boolean identities can invalidate a purely local gate rule.

The clean exact class is therefore a **support-decomposable/read-once operator tree**: every leaf attribute appears once, and the two children of every binary gate have disjoint supports.

This is the correct boundary of the local theorem rather than an artificial restriction.

### 3.2 Rank dichotomy at an essential binary gate

There are ten binary Boolean connectives essential in both inputs. Under ordinary \(\mathbb F_2\) rank of the \(2\times2\) CM:

- four have rank one; exactly the four signed conjunction minterms;
- six have rank two.

Output complementation can move a connective between the two classes, so define

\[
\operatorname{PF}(u,\epsilon),\qquad \epsilon\in\{0,1\},
\]

for the prime partition of the node function or its complement.

### 3.3 Exact CM-rank recursion theorem

Let node \(u\) compute \(\Theta(g,h)\) on disjoint supports \(A,B\). Let \(M_u^{(\epsilon)}\) be the gate CM, complemented entrywise when \(\epsilon=1\).

If

\[
\operatorname{rank}_{\mathbb F_2}M_u^{(\epsilon)}=1,
\]

then the requested output is a signed conjunction

\[
g^{(\sigma)}\land h^{(\tau)},
\]

and

\[
\operatorname{PF}(u,\epsilon)
=
\operatorname{PF}(g,\sigma)\cup\operatorname{PF}(h,\tau).
\]

If

\[
\operatorname{rank}_{\mathbb F_2}M_u^{(\epsilon)}=2,
\]

then

\[
\boxed{\operatorname{PF}(u,\epsilon)=\{A\cup B\}.}
\]

The rank-two proof is stronger than a syntactic heuristic. Every descendant variable is essential. For any cross pair \(x\in A\), \(y\in B\), context-fix the other variables so that toggling \(x\) toggles \(g\) and toggling \(y\) toggles \(h\). The induced \(2\times2\) truth slice is the gate CM up to row/column permutation. Rank two therefore supplies a nonzero four-corner minor, so no AND factorization can separate that cross pair. Hence every left variable and every right variable lie in one semantic prime block.

The resulting semantic algorithm is linear in tree size, followed by an LCC merge with the carrier partition.

### 3.4 Computational validation

`code/cm_operator_tree_factor.py` checked the rank recursion against exhaustive semantic prime factorization on:

- all 10 two-variable essential gates;
- all 200 ordered three-variable trees in the tested family;
- all 5,000 ordered four-variable trees;
- 30,000 sampled five-variable trees out of 140,000 available ordered gate-labelled instances.

Total: **35,210** instances; **0 discrepancies**.

### 3.5 Priority boundary

This is not evidence that read-once Boolean factorization itself is new. Read-once recognition/factorization has a substantial literature. The potentially project-specific part is the exact **CM-rank recursion and four-corner fusion proof**, especially its signed output-polarity formulation and direct composition with the carrier LCC theorem. A dedicated priority search did not find this exact formulation, but absence from a search is not proof of firstness.

---

## 4. Branch C — selector-controlled incremental four-corner SAT

### 4.1 One persistent formula

Given carrier blocks

\[
\Pi_K=\{B_1,\ldots,B_k\},
\]

introduce one selector \(s_j\) per carrier block. For each original variable \(x_v\), create two assignment clones \(x_v^{(0)},x_v^{(1)}\). Pure corners use the clone directly. Mixed corners use multiplexers controlled by the selector of the variable's carrier block:

\[
z_v^{01}=\operatorname{ITE}(s_{B(v)},x_v^{(0)},x_v^{(1)}),
\]

\[
z_v^{10}=\operatorname{ITE}(s_{B(v)},x_v^{(1)},x_v^{(0)}).
\]

The four semantic copies and the final CM defect remain fixed:

\[
(F_{00}\land F_{11})
\mathbin{\Updownarrow}
(F_{01}\land F_{10})=1.
\]

A candidate cut is now only a vector of selector assumptions.

### 4.2 Assumption-equivalence theorem

Fix a nontrivial union of carrier blocks and assign the selectors accordingly. After simplification, the controlled mixed-corner multiplexers are exactly the input substitutions of the independent Phase-3 four-corner formula. Therefore:

\[
\boxed{
\text{controlled base CNF under the cut assumptions is SAT}
\iff
\text{fresh independent four-corner CNF for that cut is SAT}.}
\]

This validates use of one permanent SAT instance for all carrier-compatible cuts.

### 4.3 Correctness campaign

`code/validate_incremental.py` generated 120 random carrier/CNF instances and checked **516 carrier-compatible cut queries**.

For every query it compared:

1. the controlled base formula under assumptions;
2. a freshly rebuilt Phase-3 cut formula;
3. direct exhaustive CM rank-one computation.

It also compared complete recursive factor recovery between the controlled and independent engines.

Result: **0 discrepancies**.

### 4.4 Encoding amortization

A deterministic size experiment with two variables per carrier block produced:

| carrier blocks | unordered cuts | controlled base clauses | fresh clauses over all cuts | fresh/base |
|---:|---:|---:|---:|---:|
| 2 | 1 | 284 | 252 | 0.89 |
| 3 | 3 | 420 | 1,116 | 2.66 |
| 4 | 7 | 556 | 3,444 | 6.19 |
| 5 | 15 | 692 | 9,180 | 13.27 |
| 6 | 31 | 828 | 22,692 | 27.41 |
| 7 | 63 | 964 | 53,676 | 55.68 |
| 8 | 127 | 1,100 | 123,444 | 112.22 |

This measures **CNF emission/reuse only**. It is not a solver-time benchmark. With one cut, the controlled multiplexer overhead can make the permanent formula larger.

The code contains an optional PySAT assumption interface, but no industrial assumption-capable solver was installed in the execution environment. The reproducibility fallback restarts a small DPLL solver while reusing the same base encoding, so no learned-clause speedup is claimed here.

Incremental SAT for Boolean bi-decomposition is also prior art; the project-specific value is the carrier-block control plus the CM four-corner defect and simultaneous-factor workflow.

---

## 5. New hybrid exact architecture

The three branches combine cleanly.

### Certified-direct stage

- If the semantic object is a read-once CM/LM operator tree, compute the exact \(\Pi_f\) by the rank recursion and finish with \(\operatorname{LCC}(\Pi_K,\Pi_f)\).
- If the semantic object is a compressed SDD, compute its finest \(T\)-laminar semantic partition \(\Pi_T\).

Because \(\Pi_T\) is itself a valid semantic factorization, define

\[
\Pi_0=\operatorname{LCC}(\Pi_K,\Pi_T).
\]

Then \(\Pi_0\) is a valid simultaneous factorization. The true finest simultaneous partition \(\Pi_*\) refines \(\Pi_0\). Therefore every unresolved structured prime factor lies wholly inside one block of \(\Pi_0\).

### Residual exact stage

Run the incremental four-corner SAT oracle **independently inside each unresolved block of \(\Pi_0\)**. No candidate cut crossing already certified simultaneous blocks needs to be tested.

This yields an exact hybrid algorithm, not a heuristic:

\[
\boxed{
\text{direct SDD/CM certificates}
\;\to\;
\text{safe block decomposition}
\;\to\;
\text{incremental SAT only on residual blocks}.
}
\]

When the SDD vtree is prime-aligned, the residual SAT stage is empty.

---

## 6. Priority / novelty assessment

The current evidence supports a careful claim boundary.

### Established prior art

- compressed SDD partitions and their canonicity are standard SDD theory;
- structured d-DNNF has known transformation/closure limitations;
- read-once Boolean recognition and factorization are classical;
- SAT/incremental-SAT Boolean bi-decomposition is established logic-synthesis technology;
- 2026 work such as DivKC already studies decomposing formulas into pieces to improve d-DNNF compilation.

### What appears project-specific

1. the **compressed-SDD cut criterion interpreted exactly as the CM rank-one/cofactor condition**;
2. the distinction between full prime factors and **vtree-laminar** prime exposure, with exact residual-SAT fallback;
3. the signed two-state **CM rank recursion** for support-disjoint read-once operator trees, including the rank-two four-corner fusion proof;
4. the common carrier-aware architecture based on \(\operatorname{LCC}(\Pi_K,\Pi_f)\);
5. one selector per carrier prime block in the four-corner defect engine, allowing a single persistent semantic formula for all carrier-compatible cuts.

The phrase “appears project-specific” is deliberate. It is not a firstness claim.

---

## 7. Recommended convergence decision

### Keep

- **Theorem A:** compressed-SDD vtree-cut rank-one criterion and finest \(T\)-laminar extraction;
- **Theorem B:** exact CM-rank prime-factor recursion for essential read-once operator trees;
- **Algorithm C:** one-formula carrier-selector four-corner SAT comparator;
- **Hybrid corollary:** direct certified factors safely partition the remaining exact SAT problem.

### Do not claim

- polynomial direct extraction from arbitrary structured d-DNNF;
- novelty of SDD compression/canonicity;
- novelty of read-once factorization;
- novelty of incremental SAT bi-decomposition;
- runtime speedup from the current incremental prototype.

### Strongest next theorem problem

The most interesting next mathematical extension is no longer “does direct extraction work at all?” It is:

> **Controlled repeated-support CM/LM factorization.** Find the broadest operator-DAG class strictly beyond read-once trees for which local CM certificates plus a bounded amount of shared-module information still recover the exact prime factor partition without generic SAT.

Good candidate restrictions are bounded read number, deterministic shared modules, bounded overlap treewidth, or canonicalized DAGs in which equivalence/cancellation has been normalized.

In parallel, the compiled route should investigate **vtree adaptation**: can the carrier partition, operator-support graph, or SAT defect cores drive rotations/restructuring toward a vtree that exposes more semantic prime factors before SAT is invoked?

The computational follow-up should use an industrial incremental CDCL API and report wall-clock/propagation/conflict/learned-clause reuse against independent-cut rebuilding on the same cut order. Until that experiment is run, encoding reuse is the only supported performance result.
