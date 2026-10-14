# Literature and Priority Audit Through 2026

## Executive verdict

The foundational two-operation idea is a **useful synthesis, not a new primitive mathematics**. Several prior literatures already contain near-exact versions of one or both axes.

## 1. Closest antecedent to observational equivalence: rough sets

Pawlak's rough-set information systems take a universe of objects and a set of attributes. A subset of attributes induces

\[
x\,IND_B\,y
\iff
\forall a\in B,\ a(x)=a(y),
\]

an equivalence relation whose classes partition the universe. This is essentially the same construction as

\[
x\sim_\Phi y\iff o_\Phi(x)=o_\Phi(y).
\]

Thus the partition-level observation calculus should explicitly cite rough sets / indiscernibility relations. Attribute reducts are also close antecedents to minimal observational bases.

Key sources:

- Z. Pawlak, **Rough sets**, *International Journal of Computer & Information Sciences* 11 (1982), 341--356. DOI `10.1007/BF01001956`.
- Rough-set surveys explicitly formulate attributes as functions, equality of all selected attribute values as an indiscernibility relation, and the induced partition.

**Priority class:** standard antecedent; very close.

## 2. Information partitions: Aumann and epistemic models

Aumann's 1976 framework represents an agent's information by a partition of the state space; the true state identifies the cell known by the agent. This is another direct antecedent for the partition reading of `Phi`.

- R. J. Aumann, **Agreeing to Disagree**, *Annals of Statistics* 4(6), 1236--1239 (1976), DOI `10.1214/aos/1176343654`.

**Priority class:** standard antecedent.

## 3. Refinement/informativeness of experiments: Blackwell

Blackwell's comparison of experiments formalizes when one experiment is more informative than another, equivalently when the less informative experiment can be obtained by garbling the more informative one under the classical setup.

- D. Blackwell, **Comparison of experiments** (1951).
- D. Blackwell, **Equivalent comparisons of experiments**, *Annals of Mathematical Statistics* 24 (1953), 265--272, DOI `10.1214/aoms/1177729032`.

The area remains active through 2026 (for example, work on prior-free Blackwell comparisons), so any claim about a new ordering of observation interfaces must be compared here.

**Priority class:** standard stochastic/information antecedent.

## 4. Conditioning as model restriction: Dynamic Epistemic Logic / PAL

Public Announcement Logic updates a Kripke model by eliminating worlds where the announced proposition is false and restricting the remaining relations/valuation. This is structurally close to

\[
S\mapsto S\cap E.
\]

Sequential announcements and more general epistemic actions provide a mature dynamic logic for information-changing operations.

Useful orientation sources:

- Stanford Encyclopedia of Philosophy, **Dynamic Epistemic Logic**;
- SEP, **Logic and Information**.

**Priority class:** direct antecedent for update/restriction dynamics.

## 5. Minimal separation: Test Cover / separating systems

The Test Cover problem is precisely: choose a minimum subcollection of tests so that every pair of objects is separated by at least one test. It is NP-hard for a restricted supplied test family.

- G. Gutin, G. Muciaccia, A. Yeo, **(Non-)existence of Polynomial Kernels for the Test Cover Problem**, arXiv:1204.4368.

If arbitrary Boolean tests are allowed, the lower bound is simply coding-theoretic: `ceil(log2 N)` tests suffice and are necessary for `N` objects. Thus complexity claims require a restricted candidate family or cost model.

**Priority class:** direct antecedent.

## 6. Formal Concept Analysis and information algebras

Formal Concept Analysis uses object--attribute incidence and Galois connections to build complete concept lattices. Attribute reduction is a developed topic. Kohlas's information algebras explicitly study algebraic **combination** and **focusing** of information. These do not duplicate the exact ProLT topology, but they are close enough that a broad "two operations on information" novelty claim would be unsafe.

**Priority class:** neighboring established frameworks.

## 7. Logical projectors: Eigenlogic

Eigenlogic represents binary propositions by commuting projector observables with truth values as eigenvalues. The first arXiv posting of Toffano's paper is 21 December 2015, after the thesis date of 3 December 2015, but it is direct prior art for any *current* claim that diagonal logical projectors are new.

- Z. Toffano, **Eigenlogic in the spirit of George Boole**, arXiv:1512.06632.
- F. Dubois, Z. Toffano, **Eigenlogic: a Quantum View for Multiple-Valued and Fuzzy Systems**, arXiv:1607.03509.

**Priority class:** direct projector-logic antecedent for modern publication.

## 8. Nonclassical boundary: modal quantum and contextuality

- B. Schumacher and M. Westmoreland, **Modal quantum theory**, arXiv:1010.2929 (2010), develops finite-field quantum-like state theory using possibility/necessity.
- S. Abramsky and A. Brandenburger, **The Sheaf-Theoretic Structure of Non-Locality and Contextuality**, *New Journal of Physics* 13 (2011), arXiv:1102.0264, identifies contextuality with obstructions to global sections.

These sources support a strict boundary: one global Boolean event algebra plus set intersection is classical; genuinely contextual structure requires incompatible contexts/no global assignment or another nonclassical state-effect contract.

## 9. Project-internal priority boundary

The strongest caution is internal: `ProLT_Controlled_Refinement_Regimes_v0.3` already states and proves that, after T0, observation refinement and premise accumulation commute as simplicial inclusions and form a bifiltration. Therefore the two-axis commutative square cannot be claimed as a newly discovered theorem in this audit.

The v0.5 simultaneous-refinement note already contains nontrivial interaction phenomena on the refinement axis, including destructive and compensating observation blocks.

## 10. Priority map

| Proposed item | Closest antecedent | Status |
|---|---|---|
| signature equivalence / partition | rough sets; information partitions | standard |
| adding tests refines partition | rough sets / partitions | standard |
| event outcome restricts worlds | conditioning; PAL/DEL | standard |
| refinements and fixed restrictions commute | elementary product action; already ProLT v0.3 | standard / already internal |
| minimum separating tests | Test Cover / separating systems | standard |
| probability experiment informativeness | Blackwell order | standard |
| diagonal logical projectors | Eigenlogic + ordinary characteristic projectors | standard |
| CM-to-event-to-diagonal bridge | project-specific typed synthesis | useful synthesis |
| pre/post-T0 split vs order-thinning | current ProLT program | project-specific established result/candidate package |
| refinement/update homological bifiltration | current ProLT v0.3 + multiparameter persistence language | project-specific synthesis; novelty requires dedicated audit |
| pair-ambiguity / invisible-symmetry identity | elementary combinatorics/group theory | useful derived lemma, no novelty claim |
| contextual extension without global section | sheaf-theoretic contextuality | established framework |

## 11. Publication positioning

A defensible paper should not be titled or sold as a discovery of "measurement as refinement plus conditioning." A stronger positioning is:

> a typed bridge connecting CM/LM Boolean observables, ProLT observation refinement, and premise/outcome restriction, with a precise pre-T0/post-T0 distinction, computable differentiation monotones, and a clean classical/nonclassical boundary.

The novelty burden then falls on the ProLT-specific topology/homology results and any genuinely new interaction theorem proved beyond the already-known commuting bifiltration.
