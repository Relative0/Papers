# Audit-derived exact-identification rank characterization

27 September 2026. Optional research note; not a revision of the manuscript.

## A constructive exact-identification rank characterization

**Status: independently derived in this audit; not part of the submitted manuscript; priority unresolved.** The prior assessment correctly warned that an arbitrary rank bound is not automatically an achievable algorithm. For the paper's unrestricted QXOR and complete-readout model, a particular rank condition can in fact be made sufficient by an explicit construction.

Let $X$ be a finite nonempty address set and $P$ a finite nonempty family of distinct Boolean functions on $X$. Form $E_q(P)$ with columns indexed by $f\in P$ and rows indexed by subsets $S\subseteq X$ of size at most $q$:

$$
(E_q(P))_{S,f}=\prod_{x\in S}f(x).
$$

The empty product is one. In the manuscript's characteristic-two field model, with unrestricted finite-dimensional secret-independent linear operations and complete readout,

$$
Q_{\rm exact}^{\rm QXOR}(\operatorname{Identify}P)
=\min\{q\ge0:\operatorname{rank}_F E_q(P)=|P|\}.
$$

This is a statement about **identifying the entire promised function**, not arbitrary many-to-one classification, and not polynomial gate complexity.

### Necessity

Write the truth-table bits as $t_x=f(x)$. Each pointwise query is affine in those bits. The recorded-path induction therefore expresses every output coordinate as a polynomial of total degree at most $q$ in the $t_x$, reduced to squarefree form on Boolean inputs. The matrix of records has a factorization through $E_q(P)$, so its rank is at most $\operatorname{rank}E_q(P)$. Exact identification requires $|P|$ independent nonzero records. This necessity also holds for the broader fixed-action lower-bound class.

### Sufficiency

A single QXOR call on the fixed nonzero preparation $\sum_{x\in X}|x,0\rangle$ produces

$$
|\Gamma_f\rangle=\sum_{x\in X}|x,f(x)\rangle.
$$

Preparing $q$ independent registers and querying each once produces $|\Gamma_f\rangle^{\otimes q}$. Preparation is permitted: any desired nonzero vector can be the image of a fixed basis vector under an invertible linear map. The tensor state is nonzero over a field.

Let $B_q$ have these tensor states as columns. Every coordinate of a column is a product of $q$ factors, each either $f(x)$ or $1+f(x)$; hence the row space of $B_q$ is contained in the row space of $E_q(P)$.

Conversely, fix a row monomial $\prod_{x\in S}f(x)$ with $|S|=k\le q$. Assign $k$ query slots to those addresses and take target label 1 in each. In the remaining slots use any fixed address and sum the two target-label coordinate rows. Each unused slot contributes $(1+f(x))+f(x)=1$. Thus the desired monomial is a linear combination of rows of $B_q$. For $q=0$, both matrices reduce to the constant feature. Therefore their row spaces, and ranks, agree.

If $E_q(P)$ has full column rank, the tensor graph states are independent. Extend them to a basis and apply the complete dual-basis readout, assigning one label to each promised function. This instrument is fixed from the known promise family and does not depend on the unknown function. It identifies every promised input exactly. The linear combinations in the row-space argument are a proof of rank equality, not a permission to inspect unknown coefficients for free.

### Consequences and cautions

The result supplies a nonadaptive optimal-query realization for identification in this permissive model. Arbitrary adaptive protocols cannot beat the rank threshold. For a promised subset of BV secrets, the address family contains the unit queries, so the degree-$q$ truth-query features span exactly the restricted degree-$q$ secret monomials. The same criterion therefore gives an exact promised-BV identification characterization, not only a necessary bound.

For the full BV cube, the threshold is $n$, recovering Theorem 4.2. The fresh program checks row-rank equality on all 255 nonempty promises on three Boolean addresses at four query budgets. Those computations are corroboration; the argument above is the proof.

This does **not** give matching upper bounds for arbitrary pairs $G_0,G_1$, efficient gate synthesis, a uniform algorithm from a succinct promise description, or a general decision/classification characterization. The necessary measurement may be very large. Nor does it close the DJ gap, because DJ identifies a class rather than the entire truth table.

This is the highest-value optional strengthening found in this audit: it directly generalizes the paper's main theorem instead of adding a new topic. Before insertion, audit its novelty against oracle identification, modal multiple-copy discrimination, and algebraic feature-rank literature. It has not received an external review. Keep it as an optional proposition until that comparison is done.


---

**Revision-package status (27 September 2026):** This result is retained as a **candidate extension only**. It has not undergone the same theorem-level prior-art audit as the revised P02 manuscript and is intentionally not incorporated into the paper. Do not present it as novel or publication-ready without a separate audit.
