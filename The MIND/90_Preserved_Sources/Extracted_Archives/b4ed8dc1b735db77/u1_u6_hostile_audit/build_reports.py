from pathlib import Path
import csv, json, hashlib, textwrap, os

out=Path('/mnt/data/u1_u6_hostile_audit')
out.mkdir(exist_ok=True)

def write(name, s):
    (out/name).write_text(textwrap.dedent(s).lstrip(), encoding='utf-8')

status_rows = [
    ['U1','Preorder refinement is intersection; support conditioning is induced restriction','VALID AS STATED','standard / definition-level specialization','High'],
    ['U2','Fine quotient maps canonically to coarse quotient; splitting may create internal fiber order while cross-fiber comparabilities can only be lost','VALID WITH REPAIR','useful synthesis of standard quotient-order facts','High'],
    ['U3','Every finite refinement factors through the lexicographic sum of its new-coordinate fiber profiles','VALID AS STATED','standard lexicographic sum used as a ProLT-specific canonical intermediate','High'],
    ['U4','Cone(j)->Cone(r)->Cone(pi)->Cone(j)[1] yields the defect LES; no direct-sum decomposition in general','VALID WITH TERMINOLOGY REPAIR','standard octahedral mapping-cone theorem specialized to U3','High'],
    ['U5','The expansion/support square is a pullback iff every surviving coarse point retains its full refined label profile','VALID AS STATED','standard pullback/fiber-saturation calculation specialized to ProLT','High'],
    ['U6','For a fine-measurable event, coarse measurability iff the expansion square is cartesian iff fiber defect is zero','VALID AS STATED; HYPOTHESIS ESSENTIAL','useful synthesis of saturation with measurement availability','High'],
    ['D1','Every finite target preorder R1 subseteq R0 is realizable by Boolean tests; minimize tests under constraints','VALID','unrestricted part standard bit-vector/2-dimension territory; constrained relative problem remains interesting','High'],
    ['A1','Chain-safe adaptive identification has depth ceil(log2 n), exactly one redundant query is necessary/sufficient on a worst-case path, and nonredundant-safe-only identification is impossible','PROVED','plausible new ProLT-specific corollary; general restricted-query search is established literature','High mathematically / Moderate novelty'],
]
with (out/'THEOREM_STATUS.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['Theorem','Final statement','Status','Novelty classification','Confidence']); w.writerows(status_rows)

write('U1_PREORDER_REFINEMENT.md', r'''
# U1 — Preorder refinement by intersection

## Verdict

**VALID AS STATED.** The result is exact, but it is essentially definitional once the observation preorder is defined coordinatewise. It should be retained as the foundational bookkeeping lemma, not advertised as a new theorem.

Let `S` be a finite support and let every observation `phi` take values in a preorder `A_phi`. Define

\[
x\preceq_{\Phi,S}y
\iff
x,y\in S\ \text{and}\ \phi(x)\le_{A_\phi}\phi(y)\quad\forall\phi\in\Phi.
\]

Boolean values are not essential. Any preordered codomains work.

For observation families `Phi,Theta`,

\[
\preceq_{\Phi\cup\Theta,S}
=
\preceq_{\Phi,S}\cap\preceq_{\Theta,S}.
\]

For `T subseteq S`,

\[
\preceq_{\Phi,T}
=
\preceq_{\Phi,S}\cap(T\times T).
\]

The second identity is simultaneously the restriction of a relation, the induced subpreorder, and—under the finite Alexandrov correspondence—the specialization preorder of the induced subspace.

## Hidden hypotheses

1. Each observation must be a total map on the carrier under consideration. Partial observations require either restricting their domains or adding an explicit undefined value/order.
2. The observation codomain must carry a preorder if the coordinatewise order definition is to make sense.
3. Duplicated/indexed observations do not change the induced relation unless later weights/costs use multiplicity.

## Novelty classification

Finite topological spaces are classically equivalent to finite preorders, and `T0` is exactly antisymmetry. The intersection identity adds no independent novelty. Its value is architectural: it puts refinement and support restriction in one relation calculus.
''')

write('U2_T0_PHASE_TRANSITION.md', r'''
# U2 — The T0 phase transition: hostile audit and repair

## Verdict

**VALID WITH REPAIR.** The source correctly identifies world-level refinement as relation deletion, but its quotient-level summary is too strong if read as saying that quotient refinement only splits vertices and deletes old strict comparabilities. Splitting one coarse quotient point can itself expose **new strict order inside the split fiber**.

## Minimal counterexample

Let `S={a,b}` and let the coarse observation family be empty. The coarse world preorder is indiscrete: both `a<=b` and `b<=a`, so the Kolmogorov quotient has one point.

Add one Boolean observation with

\[
\theta(a)=0,\qquad \theta(b)=1.
\]

The refined world preorder deletes `b<=a` but retains `a<=b`. The fine quotient is therefore a two-point chain.

Thus the statement

> no new strict quotient comparabilities can appear under refinement

is false. The new strict comparability appears **inside the descendants of one old coarse quotient point**.

## Repaired theorem

Let `Psi superset Phi`. Write

\[
Q=S/{\sim_\Psi},\qquad P=S/{\sim_\Phi}.
\]

Then:

1. every fine equivalence class lies inside a unique coarse equivalence class;
2. hence there is a canonical surjective map
   \[
   r:Q\to P;
   \]
3. `r` is monotone;
4. if `q1<=q2` in `Q`, then either `r(q1)=r(q2)` or `r(q1)<=r(q2)` in `P`;
5. therefore refinement cannot create comparability between descendants of two **distinct coarse-incomparable** points;
6. a split coarse point may acquire a nontrivial internal fiber order;
7. between distinct coarse points, existing coarse comparabilities may disappear when new coordinates descend.

The clean quotient picture is therefore:

\[
\boxed{\text{fiber expansion within coarse points}\ +\ \text{cross-fiber order thinning}.}
\]

Relative `T0` means every coarse fiber is a singleton. At that stage the expansion mechanism disappears, leaving only same-vertex order thinning.

## Computational attack

The four-world exhaustive audit found 5,680 one-bit observation refinements over all 355 observation-generated preorders:

- pre-T0 redundant: 660;
- pre-T0 splitting only: 578;
- pre-T0 thinning only: 338;
- pre-T0 **both splitting and thinning**: 600;
- T0 redundant: 1,678;
- T0 thinning only: 1,826.

There were zero violations of the repaired carrier-level monotonicity theorem.
''')

write('U3_LEXICOGRAPHIC_FACTORIZATION.md', r'''
# U3 — Lexicographic fiber-expansion / thinning factorization

## Verdict

**VALID AS STATED**, with two qualifications about positioning:

1. the intermediate object really is the standard **lexicographic sum of posets**;
2. the lexicographic construction itself is standard. The project-specific content is its use as the canonical intermediate object attached to a ProLT observation refinement.

## Setup

For `Psi=(Phi,Theta)` and support `S`, let

\[
P=P_{\Phi,S}.
\]

For each coarse signature `p`, let `C_p` be its coarse class and

\[
B_p=\{\alpha_\Theta(x):x\in C_p\}\subseteq\{0,1\}^{\Theta}
\]

with coordinatewise order. The fine signature poset is

\[
Q=\{(p,a):p\in P,\ a\in B_p\},
\]

with product condition

\[
(p,a)\le_Q(q,b)
\iff
p\le_Pq\ \text{and}\ a\le b.
\]

Define the lexicographic sum

\[
F=\sum_{p\in P}B_p
\]

by

\[
(p,a)\le_F(q,b)
\iff
\begin{cases}
a\le b,&p=q,\\
\text{true},&p<q,\\
\text{false},&p\parallel q.
\end{cases}
\]

This matches the standard definition: substitute the fiber poset `B_p` for each point `p`, and make every element of the `p`-fiber precede every element of the `q`-fiber whenever `p<q`.

## The factorization

There is a canonical factorization

\[
Q\xhookrightarrow{j}F\xrightarrow{\pi}P,
\qquad
\pi(p,a)=p.
\]

`Q` and `F` have the same vertices. The inclusion `j` removes exactly those cross-fiber relations for which the new labels violate `a<=b`. Projection `pi` is surjective and monotone, and the usual fine-to-coarse map is `pi o j`.

Literal canonicality holds once the realized signature sets are fixed. Under abstract relabeling, the construction is canonical up to the obvious isomorphism.

## T0 specialization

If `Phi` is relatively `T0` on `S`, each coarse class contains one world. Therefore each `B_p` contains one realized new label, so

\[
F\cong P.
\]

U3 then reduces exactly to same-vertex order thinning.

## Additional structural observation

The projection `pi:F->P` is an open surjection in the Alexandrov/up-set topology: if an upset in `F` meets a fiber over `p`, it contains every whole fiber over each `q>p`. Hence it is also a topological quotient map. This is useful but still standard lexicographic-sum behavior.

## Independent finite verification

- 5,680 observation-generated four-world transitions: zero U3 failures.
- independent abstract-poset/fiber verifier through four base points: 3,450 cases, zero failures.

## Priority assessment

Do **not** claim invention of the lexicographic sum, substitution, or fibered-poset idea. A defensible contribution claim, if desired, is narrower: the ProLT fiber-profile refinement has a canonical lexicographic-expansion intermediate that isolates splitting from cross-fiber descent thinning.
''')

write('U4_CONE_DECOMPOSITION.md', r'''
# U4 — Mapping-cone / octahedral defect sequence

## Verdict

**VALID WITH TERMINOLOGY REPAIR.** The orientation of the proposed triangle is correct under the standard cone convention, but the word **decomposition** must not be read as a direct-sum decomposition. What is obtained canonically is a distinguished triangle and a long exact sequence.

Let

\[
A=C_*(\Delta Q),\quad B=C_*(\Delta F),\quad C=C_*(\Delta P),
\]

and let

\[
f=j_*:A\to B,\qquad g=\pi_*:B\to C,\qquad h=gf=r_*.
\]

Use the homological cone convention

\[
\operatorname{Cone}(f)_n=B_n\oplus A_{n-1},
\]

\[
d(b,a)=(d_Bb+f(a),-d_Aa).
\]

Then the standard octahedral cone triangle is

\[
\operatorname{Cone}(f)
\longrightarrow
\operatorname{Cone}(gf)
\longrightarrow
\operatorname{Cone}(g)
\longrightarrow
\operatorname{Cone}(f)[1].
\]

One convenient pair of the first chain maps is

\[
\alpha(b,a)=(g(b),a),
\qquad
\beta(c,a)=(c,f(a)).
\]

The third morphism is the connecting map determined by the cone triangle; sign conventions vary with the chosen definition of shift/cone. The finite verifier uses one fixed convention and checks exactness on homology directly.

Define

\[
D_k^{\rm thin}=H_k\operatorname{Cone}(f),\qquad
D_k^{\rm total}=H_k\operatorname{Cone}(gf),\qquad
D_k^{\rm exp}=H_k\operatorname{Cone}(g).
\]

Then

\[
\cdots\to
D_k^{\rm thin}\to
D_k^{\rm total}\to
D_k^{\rm exp}\to
D_{k-1}^{\rm thin}\to\cdots.
\]

## Relative homology

Because `j:Delta Q -> Delta F` is a simplicial inclusion, with the convention above

\[
H_k\operatorname{Cone}(j_*)\cong H_k(\Delta F,\Delta Q)
\]

with **no degree shift**.

At relative `T0`, `F congruent P`; therefore `pi` is an isomorphism and `Cone(pi_*)` is acyclic. Consequently

\[
D_k^{\rm total}\cong D_k^{\rm thin}
\cong H_k(\Delta P,\Delta Q).
\]

This recovers the existing post-T0 relative-homology formulation.

## No automatic direct sum

The long exact sequence does not imply

\[
D^{\rm total}\cong D^{\rm thin}\oplus D^{\rm exp}.
\]

A splitting requires additional hypotheses (for example, vanishing connecting maps plus algebraic splitting conditions); even over a field, a resulting vector-space splitting need not be natural.

## Verification

- exhaustive over F2 for all 5,680 four-world transitions: 62,934 exactness checks, zero failures;
- 18,982 relative-homology dimension checks, zero failures;
- all 3,504 post-T0 transition cases passed the acyclic-expansion/relative reduction check;
- independent exact-rational representative census: 1,420 cases, 15,387 exactness checks, zero failures.

The construction is coefficient-independent at the chain level; the integral statement follows formally from the same chain maps and the standard octahedral theorem, rather than from an exhaustive Smith-normal-form census.

## Priority assessment

The mapping-cone triangle for a composite is standard homological algebra. The possible project contribution is the **choice of U3 factorization to which it is applied**, not the octahedral sequence itself.
''')

write('U5_CARTESIAN_SATURATION.md', r'''
# U5 — Cartesian fiber-saturation theorem

## Verdict

**VALID AS STATED.** The theorem is a clean ProLT specialization of an elementary pullback/fiber-saturation fact.

For `T subseteq S`, form

\[
\begin{array}{ccc}
F_T&\longrightarrow&P_T\\
\downarrow&&\downarrow\\
F_S&\longrightarrow&P_S.
\end{array}
\]

The vertical arrows are inclusions induced by support restriction. The pullback of `F_S -> P_S` along `P_T -> P_S` is exactly

\[
\pi^{-1}(P_T)=\{(p,a):p\in P_T,\ a\in B_p^S\}.
\]

Meanwhile

\[
F_T=\{(p,a):p\in P_T,\ a\in B_p^T\}.
\]

Therefore the square is cartesian iff

\[
B_p^T=B_p^S
\qquad\forall p\in P_T.
\]

This is stronger than merely saying `T` meets the same coarse fibers. It says every surviving coarse fiber retains every **fine signature type** previously present over it.

The left `Q/F` thinning square is always a pullback because both posets are restricted to exactly the same surviving fine-signature vertices and `Q` is the same-vertex suborder of `F`.

## Saturation terminology

Ordinary saturation for a quotient `q:S->P` is

\[
T=q^{-1}(q(T)),
\]

i.e. `T` is a union of whole coarse fibers. U5 is naturally viewed as a **profile saturation** statement at the intermediate expansion level. Ordinary coarse saturation implies the U5 profile condition, but the two notions should not be silently conflated when `T` is not known to be a union of fine cells.

## Exhaustive verification

All 90,880 support/refinement cases generated from the 355 four-world observation preorders passed. An independent partition-only implementation checked 3,840 partition/bit/event cases with zero failures.
''')

# compatibility names required by user's prompt (numbering mismatch)
write('U4_CARTESIAN_SATURATION.md', r'''
# Numbering note — requested U4 cartesian/saturation file

The hostile prompt anticipated U4 = cartesian/saturation, but the authoritative unification source actually numbers the **mapping-cone theorem as U4** and the **cartesian fiber-saturation theorem as U5**.

To avoid silently renumbering the source theory, the substantive cartesian audit is in:

- `U5_CARTESIAN_SATURATION.md`

The source-numbered U4 audit is:

- `U4_CONE_DECOMPOSITION.md`
''')
write('U5_MAPPING_CONE_DECOMPOSITION.md', r'''
# Numbering note — requested U5 mapping-cone file

The hostile prompt anticipated U5 = mapping-cone decomposition, but the authoritative unification source numbers the **mapping-cone theorem as U4** and the **cartesian theorem as U5**.

The substantive cone audit is in:

- `U4_CONE_DECOMPOSITION.md`

The source-numbered U5 audit is:

- `U5_CARTESIAN_SATURATION.md`
''')

write('U6_NEWLY_ENABLED_MEASUREMENT.md', r'''
# U6 — Newly enabled measurement / non-cartesianity

## Verdict

**VALID AS STATED, WITH AN ESSENTIAL HYPOTHESIS.** The event must already be measurable at the **fine** observation level.

Let `A_{Phi,S}` be the Boolean algebra of unions of `Phi`-signature cells, and let `Psi` refine `Phi`. Let `E subseteq S`, and assume

\[
E\in\mathcal A_{\Psi,S}.
\]

Then the following are equivalent:

1. `E in A_{Phi,S}`;
2. the U5 expansion/conditioning square is cartesian;
3. the fiber-completion defect has cardinality zero.

Reason: fine measurability says `E` takes whole fine-signature classes. Cartesianity says that whenever `E` touches a coarse class, every fine class over that coarse class remains. Together these are exactly the statement that `E` is a union of whole coarse classes.

Thus

\[
E\in\mathcal A_{\Psi,S}\setminus\mathcal A_{\Phi,S}
\]

iff the square is non-cartesian.

## Why the fine-measurability hypothesis cannot be removed

Take a coarse class `{a,b,c}`, refine it into fine classes `{a,b}` and `{c}`, and choose event `E={a,c}`. At the label-profile level, every fine label can remain represented, so the profile square can be cartesian. But `E` cuts the fine class `{a,b}` and is neither fine-measurable nor coarse-measurable.

Therefore “cartesian implies coarse measurable” is false without the fine-measurability assumption.

## Interpretation

U6 is not a quantum noncommutativity theorem. It is a saturation/availability theorem: refinement can make an event expressible as a union of newly available cells, and non-cartesianity records precisely the fact that its selection cuts some old coarse information fiber.

After relative `T0`, every coarse cell is a singleton, so `A_{Phi,S}=2^S` and the obstruction vanishes.

## Verification

The main four-world audit checked 80,652 fine-measurable event cases with zero U6 failures. The independent partition implementation also found zero failures.
''')

write('U6_CONSTRAINED_OBSERVATION_DESIGN.md', r'''
# Constrained observation design — audit of Section 9 (not source U6)

## Numbering correction

The hostile prompt treated constrained observation design as a possible U6. In the authoritative source, U6 is the newly-enabled measurement theorem. Observation design is the subsequent Section 9 program. This file audits that program without renumbering the source.

## Unrestricted realization

Let `R1 subseteq R0` be finite preorders on the same carrier `S`. For each `z in S`, define

\[
\theta_z(x)=1[z\,R_1\,x].
\]

Then

\[
x\,R_1\,y
\iff
\theta_z(x)\le\theta_z(y)\quad\forall z\in S.
\]

The forward direction is transitivity. For the reverse direction, if `x not R1 y`, choose `z=x`: `theta_x(x)=1` and `theta_x(y)=0`.

Hence the observation preorder generated by all `theta_z` is exactly `R1`, and therefore

\[
R_0\cap R_\Theta=R_1.
\]

Boolean observations always suffice, with at most the number of `R1` quotient points needed after removing duplicate principal-upset coordinates.

## Priority assessment

This unrestricted construction is standard bit-vector/order embedding territory. Embedding a poset into a Boolean lattice by subset inclusion is the classical 2-dimension problem; minimum encodings are computationally difficult. When `R0` is maximally coarse, the relative problem collapses toward that established theory.

For pure separation from a restricted test pool, the problem contains classical Test Cover, which is NP-hard.

## Where the research opportunity remains

The interesting quantity is therefore not an unrestricted `odim`, but a **constrained relative observation dimension**

\[
\operatorname{odim}_{\mathcal C}(R_0,R_1),
\]

where admissible tests must satisfy ProLT-specific restrictions, e.g.:

- homotopy-neutrality at the current branch;
- bounded relative defect rank;
- repair-forest conditions;
- fixed formula fragments (Horn, monotone, bounded size);
- a fixed observation library;
- costs or physical/cognitive availability constraints.

Those restrictions can create a problem not exhausted by ordinary 2-dimension or Test Cover.
''')

write('COUNTEREXAMPLES.md', r'''
# Counterexamples and repaired overstatements

## C1 — quotient refinement can expose a new strict order inside a split coarse point

**False stronger statement:** “No new strict quotient comparabilities ever appear under refinement.”

Carrier `S={a,b}`; no coarse observations; add `theta(a)=0, theta(b)=1`.

- coarse quotient: one point;
- fine quotient: two-point chain `0<1`.

**Repair:** no fine comparability can connect descendants of two distinct coarse-incomparable points. New strict relations may appear **inside the fiber of one split coarse point**.

## C2 — cartesianity does not imply coarse measurability without fine measurability

Coarse cell `{a,b,c}`; fine cells `{a,b}` and `{c}`; event `E={a,c}`.

`E` cuts a fine cell. Thus it is not fine-measurable and not coarse-measurable, even though the coarser label-profile condition can be cartesian.

**Repair:** U6 must assume `E` is a union of fine signature classes.

## C3 — U4 is not a direct-sum decomposition theorem

The octahedral axiom yields a distinguished triangle and long exact sequence. Without vanishing connecting morphisms and further splitting data, one cannot conclude

\[
D^{\rm total}\cong D^{\rm thin}\oplus D^{\rm exp}.
\]

**Repair:** call U4 an “octahedral defect sequence” or “cone factorization sequence,” not an unconditional direct decomposition.

## C4 — homotopy-neutral query restrictions alone do not make adaptive identification hard

If arbitrary Boolean queries are available on a finite T0 poset, choose a linear extension. Any suffix of a linear extension is an upset and therefore defines an isotone/topologically redundant query. A suffix can be chosen to split the current support as evenly as possible. Repeating yields depth `ceil(log2 n)`.

**Repair of research target:** to obtain nontrivial adaptive complexity, impose a fixed query library, syntactic/cost restriction, or require nonredundant safe queries.
''')

write('ADAPTIVE_THEOREM_SEARCH.md', r'''
# Constrained-adaptive theorem search

## Gate result

The U1–U6 framework survives after two repairs: U2 needs a more accurate quotient statement, and U4 must be described as an exact triangle/LES rather than a direct-sum decomposition. The strongest adaptive search therefore focused on the exact ProLT chain classification.

## Hostile negative result N1 — homotopy-neutrality alone is too weak

Let `P` be any finite T0 poset with `n` candidate worlds, and suppose arbitrary Boolean queries are available. There is an adaptive identification protocol of worst-case depth

\[
\lceil\log_2 n\rceil
\]

using **only topologically redundant (isotone) queries**.

### Proof

Choose a linear extension of the current induced poset. A suffix of a linear extension is an upset: if `x` is in the suffix and `x<=y`, then `y` appears no earlier than `x`, so `y` is also in the suffix. Therefore its indicator is isotone and adding it is topologically redundant.

Choose a suffix whose size is as close to half of the current support as possible and measure that query. Each branch has at most `ceil(m/2)` candidates. Conditioning preserves the induced finite poset, so repeat. The ordinary binary-information lower bound proves optimality.

### Consequence

A constraint of the form “each query must be homotopy-neutral” cannot, by itself, create a worst-case query-complexity gap if the Boolean query pool is unrestricted.

This negative theorem sharply narrows the meaningful adaptive program.

---

## Preferred chain regime

The existing ProLT chain theorem classifies a one-bit profile `b1...bm` on an `m`-chain:

- redundant exactly when the profile is nondecreasing `0*1*`;
- topology-defective exactly for a strict antitone threshold `1^k0^{m-k}`, `1<=k<m`;
- every other profile is nonredundant but homotopy-neutral.

At an adaptive branch, all earlier query bits are constant on the surviving support, so the current induced poset remains a chain. Hence this classification can be applied recursively.

## Computation

Dynamic programming was performed for chain sizes 2 through 10 over the exact legal query language. Independent closed-form verification was run through size 30.

Results for every `2<=n<=10`:

\[
d_{HN}(n)=\lceil\log_2 n\rceil,
\]

minimum worst-path redundant-query count among depth-optimal protocols is `1`, and identification using **only nonredundant homotopy-neutral queries** is impossible.

The constructive policy uses an alternating profile `0101...` whenever the current chain has at least three elements. It is nonconstant, non-isotone, and not a strict antitone threshold, hence is nonredundant homotopy-neutral. It splits the chain into `ceil(m/2)` and `floor(m/2)` survivors. On a final two-element chain, the informative safe profile is `01`, which is redundant.

These computations suggested A1, proved in `ADAPTIVE_THEOREM_FINAL.md`.
''')

write('ADAPTIVE_THEOREM_FINAL.md', r'''
# A1 — Chain safe-query dichotomy and optimal adaptive depth

## Theorem A1

Let the branch-relative current ProLT signature poset be an `n`-element chain, `n>=2`. Suppose an adaptive protocol may choose arbitrary Boolean query profiles, but every query must be **homotopy-neutral before its outcome is conditioned upon**. Then:

1. complete identification is possible in optimal worst-case depth
   \[
   d_{HN}(n)=\lceil\log_2 n\rceil;
   \]
2. among depth-optimal safe protocols, the minimum possible value of the **maximum number of topologically redundant queries on a root-to-leaf path** is exactly `1`;
3. if topologically redundant queries are forbidden entirely—so every query must be both nonredundant and homotopy-neutral—complete identification is impossible for every `n>=2`.

## Proof

### Lower bound

Any yes/no decision tree with `n` leaves has height at least `ceil(log2 n)`.

### Optimal construction

For any current branch with `m>=3` surviving chain elements, ask the alternating query

\[
0101\cdots
\]

in chain order (either parity choice works with the appropriate base convention).

This profile is:

- not constant;
- not nondecreasing, hence not topologically redundant;
- not of the strict antitone-threshold form `1^k0^{m-k}`.

By the exact ProLT chain classification it is therefore **nonredundant homotopy-neutral**. Its two outcomes retain `ceil(m/2)` and `floor(m/2)` chain elements.

Earlier query coordinates are constant on a branch because their outcomes have been fixed, so each child’s branch-relative signature poset remains the induced subchain. Recurse.

When `m=2`, ask profile `01`. It separates the two candidates and is nondecreasing, hence topologically redundant and homotopy-neutral.

The recurrence

\[
D(m)=1+\max(D(\lceil m/2\rceil),D(\lfloor m/2\rfloor))
\]

with `D(1)=0` gives

\[
D(m)=\lceil\log_2 m\rceil.
\]

Every root-to-leaf path uses nonredundant neutral queries until it reaches a two-point branch, followed by exactly one redundant separator. Thus one redundant query per worst path suffices.

### Necessity of a redundant query

Every finite full binary identification tree with at least two leaves contains a **cherry**: an internal node whose two children are leaves. At that node exactly two candidate worlds remain. Since the branch-relative poset is an induced subchain, it is a two-element chain.

The only informative Boolean profiles on a two-chain are `01` and `10` (up to answer complementation). By the ProLT chain theorem:

- `01` is isotone and topologically redundant;
- `10` is the unique strict antitone threshold and is topology-defective.

Therefore a homotopy-neutral separator at the cherry must be the redundant profile `01`. Every safe identification tree has at least one redundant query on some root-to-leaf path. Combining with the construction proves the exact value `1`.

If redundant queries are forbidden, no two-element branch can ever be resolved, so complete identification is impossible. `square`

## Computational verification

- exact DP for `n=2,...,10` agrees with all three conclusions;
- independent constructive/lower-bound verifier agrees through `n=30`;
- `LEGAL_QUERY_PROFILES.csv` contains all 2,044 profiles examined for `n=2,...,10`.

## Novelty discipline

Restricted-question “20 questions,” constrained binary identification, generalized binary search, and poset search are established areas. Therefore the `ceil(log2 n)` information-theoretic depth should **not** be claimed as novel.

What may be a new ProLT-specific corollary is the exact safe-query statement:

> on chains, ProLT homotopy-neutrality permits information-theoretically optimal adaptive identification, but every safe identification tree is forced to spend a redundant query at a two-state cherry; exactly one such redundant query on a worst branch is sufficient and necessary.

The priority search did not find this particular topological admissibility language/result, but the proof is elementary once the ProLT chain theorem is known. Novelty confidence is therefore **moderate, not high**.
''')

write('LITERATURE_PRIORITY_AUDIT.md', r'''
# Literature and priority audit through September 2026

This audit is conservative: absence of an exact phrase is not evidence of novelty.

## U1/U2 — finite topologies and preorders

Finite topology/preorder equivalence and the fact that `T0` corresponds to antisymmetry are classical. A recent accessible statement is:

- Mrozek et al., *Conley Index for Multivalued Maps on Finite Topological Spaces*, Foundations of Computational Mathematics (2024/2025 online context), https://link.springer.com/article/10.1007/s10208-024-09685-4
- Jonathan Barmak, *Algebraic Topology of Finite Topological Spaces and Applications*, Springer, 2011, DOI 10.1007/978-3-642-22003-6.

**Priority effect:** U1 is standard. U2's repaired fiber/cross-fiber interpretation is a synthesis, not a claim to the quotient-order foundations.

## U3 — lexicographic sums

The intermediate `F=sum_p B_p` matches the standard lexicographic sum/substitution of posets: within a fiber use its order; when index `p<q`, every point of the `p`-fiber is below every point of the `q`-fiber.

- Sage/Stanford finite-poset documentation: https://sporadic.stanford.edu/reference/combinat/sage/combinat/posets/posets.html

**Priority effect:** lexicographic sum is standard. The potentially useful project-specific step is identifying it canonically from ProLT fiber profiles and then separating its expansion map from descent thinning.

## U4 — mapping cones and the octahedral axiom

The cone of a map gives the standard distinguished triangle, and composable maps fit the octahedral pattern connecting `Cone(f)`, `Cone(gf)`, and `Cone(g)`.

- Stacks Project, *Cones and distinguished triangles*: https://stacks.math.columbia.edu/tag/09P1
- Stacks Project, *Distinguished triangles in the homotopy category*: https://stacks.math.columbia.edu/tag/014P

**Priority effect:** the octahedral LES is standard homological algebra. Do not claim it. The application to the U3 refinement factorization is the only project-specific content.

## U5/U6 — pullbacks, saturation, and measurement availability

Pullbacks are fiber products; in sets and concrete ordered settings the relevant square selects exactly the elements lying over the surviving base. Saturated subsets of a quotient are unions of whole quotient fibers. U5/U6 are therefore close to standard fiber/saturation mathematics.

- nLab pullback overview: https://ncatlab.org/nlab/show/pullback

The epistemic-update interpretation also has established neighbors. Public Announcement Logic updates a model by deleting worlds at which the announced formula is false:

- Stanford Encyclopedia of Philosophy, *Dynamic Epistemic Logic*: https://plato.stanford.edu/entries/dynamic-epistemic/
- SEP, *Logic and Information*: https://plato.stanford.edu/entries/logic-information/

**Priority effect:** U5 is a standard pullback criterion in project notation. U6 is a useful synthesis identifying non-cartesianity with “newly enabled measurement” under a fine-measurability hypothesis.

## Observation design — 2-dimension and Test Cover

Bit-vector encodings of a poset into a Boolean lattice, minimizing the number of coordinates, are the classical 2-dimension problem:

- Habib et al., *Computational aspects of the 2-dimension of partially ordered sets*, Theoretical Computer Science 312 (2004) 401–431, DOI 10.1016/j.tcs.2003.10.029, https://www.sciencedirect.com/science/article/pii/S0304397503005747

Pair separation from a prescribed test pool is classical Test Cover:

- Gutin, Muciaccia, Yeo, *(Non-)existence of polynomial kernels for the Test Cover problem*, Information Processing Letters 113 (2013) 123–126, DOI 10.1016/j.ipl.2012.12.008, https://www.sciencedirect.com/science/article/abs/pii/S0020019012003183

**Priority effect:** unrestricted U-design is standard territory. Novelty, if any, must come from ProLT-specific admissibility/cost/topological constraints.

## Adaptive identification and restricted query languages

Decision-tree optimization and constrained query families are deeply established:

- Hyafil & Rivest, *Constructing optimal binary decision trees is NP-complete*, Information Processing Letters 5 (1976) 15–17, DOI 10.1016/0020-0190(76)90095-8.
- Karbasi & Zadimoghaddam, *Constrained Binary Identification Problem*, STACS 2013, https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.STACS.2013.550
- Dagan, Filmus, Gabizon, Moran, *Twenty (Simple) Questions*, STOC 2017, DOI 10.1145/3055399.3055422, arXiv:1611.01655. This explicitly studies restricted sets of yes/no questions while trying to retain optimal information performance.
- Nowak, *The Geometry of Generalized Binary Search*, IEEE Transactions on Information Theory 57 (2011); arXiv:0910.4397. It studies adaptively chosen near-balanced queries and logarithmic query complexity under geometric conditions.
- Cicalese et al./related poset-search literature: *On the complexity of searching in trees and partially ordered structures*, Theoretical Computer Science 412 (2011) 6879–6896, DOI 10.1016/j.tcs.2011.08.042.
- Eisel, McMullen, Muth, *An efficient search strategy for hidden ideals in pointed partially ordered sets* (2025/2026 publication cycle), DOI 10.61091/jcmcc128-11, arXiv:2505.07604.

**Priority effect on A1:** the general topic “adaptive identification under restricted queries” is emphatically not new. The potentially new item is only the exact query language induced by the ProLT chain homotopy classification and the resulting “exactly one redundant query is necessary/sufficient” corollary. This should be presented as a narrow ProLT theorem unless a deeper priority audit finds a direct equivalent.

## Bottom line

- U1: standard.
- U2: repaired useful synthesis.
- U3: standard lexicographic construction + useful ProLT factorization.
- U4: standard octahedral machinery + useful application.
- U5: standard pullback/fiber criterion in ProLT form.
- U6: useful saturation/measurement-availability synthesis.
- A1: correct and nontrivial as a ProLT consequence; novelty plausible but modest and should remain explicitly provisional.
''')

write('OPEN_PROBLEMS.md', r'''
# Open problems after the hostile gate

## 1. Fixed-library safe adaptive identification

The strongest negative result is that arbitrary Boolean isotone queries trivialize the homotopy-neutral adaptive-depth problem to `ceil(log2 n)`. The next serious regime should therefore fix a finite query library `Q` and ask for

\[
d_{HN}(S,\Phi;\mathcal Q).
\]

Determine complexity, approximation, and exact subclasses.

## 2. Nonredundancy budget

A1 suggests a mixed resource measure. Minimize worst-case depth subject to at most `r` topologically redundant queries per branch, or conversely minimize redundancy subject to an optimal/near-optimal depth bound.

## 3. Height-two adaptive protocols

Use the exact deleted-edge/deleted-triangle boundary criterion and repair-forest theorem to characterize legal safe queries at each branch. This is the next regime where the ProLT topology is genuinely richer than a chain.

## 4. Adaptive protocols with bounded defect

Permit a query if

\[
\dim H_*(K,L)\le k
\]

or if a chosen defect norm is below budget. Determine depth/defect tradeoffs.

## 5. Joint refinement-conditioning defect

Develop the total cofiber/double-complex object associated with a refinement-conditioning square. Determine whether it yields an informative mixed invariant beyond separate horizontal and vertical defects.

## 6. Iterated U3 factorization

For a sequence of refinements, study whether successive expansion/thinning factors give a useful filtration of the total mapping cone and a spectral sequence with an interpretable `E1` page.

## 7. Relative observation dimension under logical restrictions

Determine `odim_C(R0,R1)` for monotone, Horn, dual-Horn, bounded-formula-size, CM-realizable, or compiler-realizable tests.

## 8. Priority search for A1

Search decision-tree theory for the exact forbidden-pattern language generated by “all Boolean chain profiles except strict antitone thresholds, with nondecreasing profiles marked redundant.” A direct equivalent would lower the novelty status of A1 further.
''')

write('HANDOFF_TO_MASTER.md', r'''
# Handoff to Master — U1–U6 hostile gate

**Date:** 29 September 2026

## Gate verdict

The unified framework **survives**, but it must be presented conservatively.

### Repairs

- **U2:** repair the quotient-language claim. Refinement can create strict order *inside a split old quotient point*. What cannot happen is creation of comparability between descendants of two distinct coarse-incomparable points.
- **U4:** call it an octahedral/long-exact defect sequence, not a direct-sum decomposition.
- **U6:** retain the explicit hypothesis that the event is fine-measurable.

## Status

- U1: valid, standard.
- U2: valid after repair, useful synthesis.
- U3: valid; the intermediate object genuinely is a lexicographic sum; construction standard, ProLT factorization useful.
- U4: valid LES, standard homological algebra applied to U3.
- U5: valid cartesian/fiber-profile theorem, mostly standard pullback mathematics.
- U6: valid measurement-availability/saturation equivalence under fine measurability.
- unrestricted observation-design realization: valid but standard bit-vector/2-dimension territory.

## Strongest negative result

With an unrestricted Boolean query pool, **homotopy-neutrality alone imposes no adaptive worst-case depth penalty** on a finite T0 poset. Balanced isotone (therefore topologically redundant) queries along linear extensions give depth `ceil(log2 n)`.

Therefore future adaptive work must constrain the query library, syntax/cost, defect budget, or nonredundancy.

## New theorem A1

For an n-chain under the exact ProLT one-bit homotopy-neutral query language:

1. optimal safe adaptive depth is `ceil(log2 n)`;
2. every safe identification tree must use a redundant query on at least one root-to-leaf path;
3. there is an optimal protocol whose maximum redundant-query count per path is exactly one;
4. if redundant queries are forbidden, identification is impossible.

The theorem was DP-verified for n=2..10 and independently checked constructively through n=30.

## Novelty stance

A1 is best described as a **plausibly new, narrow ProLT corollary**, not a new general decision-tree theorem. Restricted-query twenty-questions and constrained binary identification are established literatures.

## Recommended next step

Do **not** broaden the framework. Move to one of two focused problems:

1. fixed-library homotopy-neutral adaptive identification; or
2. height-two adaptive identification under the exact repair-forest/boundary-matrix admissibility criterion.

The second is more tightly tied to the existing strongest ProLT mathematics.
''')

write('U1_U6_HOSTILE_AUDIT.md', r'''
# Focused Hostile Theorem Audit of U1–U6 and Constrained-Adaptive Extension

**Project:** Unified Differentiation Calculus
**Date:** 29 September 2026
**Method:** source reconstruction, adversarial proof audit, exhaustive bounded computation, independent verifiers, and theorem-level priority search.

## 1. Numbering correction before the audit

The audit prompt anticipated U4=cartesian/saturation, U5=mapping-cone, and U6=constrained observation design. The authoritative unification manuscript numbers them differently:

- U1 — unified preorder thinning;
- U2 — quotient interpretation / T0 transition;
- U3 — canonical lexicographic refinement factorization;
- U4 — mapping-cone / octahedral defect sequence;
- U5 — cartesian fiber-saturation theorem;
- U6 — newly-enabled measurement / non-cartesianity theorem.

Constrained observation design is the following Section 9 program. This audit follows the source numbering and supplies compatibility filenames for the prompt's anticipated numbering.

## 2. Theorem status table

| Result | Correctness | Repair needed? | Prior-art status | Research value |
|---|---|---|---|---|
| U1 | Valid | No | Standard / definitional | Foundational notation only |
| U2 | Valid after repair | **Yes** | Standard quotient-order ingredients | Useful synthesis |
| U3 | Valid | No substantive repair | Lexicographic sum is standard | Strong organizing lemma |
| U4 | Valid | Terminology: LES, not direct sum | Standard octahedral mapping-cone theorem | Useful application to U3 |
| U5 | Valid | No | Pullback/fiber saturation is standard | Clean interface theorem |
| U6 | Valid under stated fine-measurability hypothesis | Hypothesis must remain explicit | Saturation/measurability ingredients standard | Useful measurement-availability interpretation |
| Observation design | Valid | Separate unrestricted vs constrained | 2-dimension/Test Cover nearby | Constrained version promising |
| A1 | Proved | No | Restricted-query search is established; exact ProLT corollary not located | Plausible narrow contribution |

## 3. Strongest hostile findings

### U2 overstatement

At world level, refinement only deletes preorder relations. But quotienting can turn deletion of one direction in a formerly symmetric pair into a **new strict relation between two newly split quotient points**. Thus “splitting + deletion of old quotient comparisons” is incomplete. U3 supplies the correct repair: a split coarse point expands to a fiber poset, while cross-fiber descents are deleted.

### U4 terminology

The standard octahedral triangle is oriented correctly:

\[
\operatorname{Cone}(j)\to\operatorname{Cone}(r)\to\operatorname{Cone}(\pi)\to\operatorname{Cone}(j)[1].
\]

It yields a long exact sequence, not an unconditional direct-sum decomposition.

### U6 hypothesis

The equivalence “cartesian iff coarse measurable” needs `E` to be fine-measurable. Without that hypothesis, an event may cut a fine signature cell while leaving all fine *labels* represented.

## 4. Exhaustive computational gate

### Four-world relation/refinement census

All 65,536 Boolean observation families were reduced to 355 distinct observation-generated preorders. Each was refined by all 16 one-bit observations: 5,680 transitions.

- U1 failures: **0**
- U3 failures: **0**
- pre-T0 simultaneous splitting+thinning cases: **600**
- T0 cases with splitting: **0**, as required

### Cartesian / measurement census

- support/refinement cases: **90,880**
- U5 failures: **0**
- fine-measurable U6 cases: **80,652**
- U6 failures: **0**

Independent partition-only implementation:

- 15 partitions;
- 3,840 partition/label/event cases;
- failures: **0**.

### U4 cone sequence

Over F2, all 5,680 transitions were rebuilt at chain level:

- exactness checks: **62,934**;
- failures: **0**;
- relative-homology dimension checks: **18,982**;
- post-T0 cases checked: **3,504**.

An exact-rational representative census covered 1,420 cases and 15,387 exactness checks with zero failures. The integral result is supported formally by the coefficient-independent cone construction rather than by a full Smith-normal-form census.

## 5. Priority verdict

The hostile literature search removes broad novelty claims from U1, the lexicographic machinery of U3, the cone machinery of U4, and the raw pullback/saturation content of U5. It also places unrestricted observation design next to established Boolean-lattice 2-dimension and Test Cover theory.

The coherent potential contribution is therefore the **ProLT-specific assembly**:

\[
\text{fiber-profile refinement}
\to
\text{lexicographic expansion + descent thinning}
\to
\text{cartesian availability obstruction}
\to
\text{defect sequence},
\]

plus constrained regimes in which ProLT topology genuinely limits allowable observations.

## 6. Adaptive gate: an important negative result

With arbitrary Boolean queries, homotopy-neutrality does **not** make identification harder. At every finite T0 branch, take a linear extension and choose a near-half suffix. Its indicator is isotone, hence topologically redundant and homotopy-neutral. This gives optimal worst-case depth `ceil(log2 n)` on every finite poset.

So a publication-worthy adaptive problem needs a stricter resource: fixed query library, syntax/cost restriction, defect budget, or a nonredundancy constraint.

## 7. New theorem A1

The chain regime nonetheless yields a sharp ProLT-specific result. Using the exact chain classification, safe adaptive identification has optimal depth

\[
\lceil\log_2 n\rceil,
\]

but every safe identification tree must use a **topologically redundant separator** at some two-state cherry. Exactly one redundant query on each worst branch is sufficient. If redundant safe queries are forbidden, identification is impossible.

The key construction uses alternating query profiles on all branches of size at least three and the redundant profile `01` only at the final two-state split.

This was exhaustively optimized through `n=10` and independently verified through `n=30`.

## 8. Final answers to the audit questions

1. **Does U3 survive exactly?** Yes.
2. **Is F genuinely a lexicographic sum?** Yes, under the standard substitution definition.
3. **Is it canonical?** Canonical on realized signature data; canonically isomorphic under relabeling.
4. **Is U5 a real pullback theorem or a saturation restatement?** Both: it is a genuine pullback statement whose proof reduces to exact fiber/profile saturation.
5. **Strongest saturation criterion?** `B_p^T=B_p^S` for every surviving coarse `p`; for fine-measurable events this is equivalent to coarse measurability.
6. **Is U4's cone orientation correct?** Yes under the stated cone convention.
7. **Does U4 give a direct decomposition?** No; it gives an exact triangle and LES. Direct splitting needs extra hypotheses.
8. **Does T0 recover relative homology?** Yes: `F congruent P`, expansion cone acyclic, and the thinning cone is the relative complex of `(Delta P,Delta Q)`.
9. **Is observation design merely Test Cover/poset dimension?** Unrestricted forms substantially overlap established theory; ProLT-constrained variants remain nontrivial.
10. **What belongs in a paper?** U3 as organizer, repaired U2, U5/U6 as interaction lemmas, and U4 as standard machinery clearly labeled as such; U1 should be background.
11. **Did the adaptive search produce a correct nontrivial theorem?** Yes: A1. It is genuinely tied to the exact ProLT chain admissibility theorem, but novelty should be described conservatively.
12. **Next restricted regime?** Height-two adaptive protocols under the repair-forest/boundary-matrix criterion, preferably with a fixed query library.
''')

write('README.md', r'''
# U1–U6 Hostile Audit Package

This folder contains the focused hostile theorem audit requested for the Unified Differentiation Calculus.

## Start here

1. `U1_U6_HOSTILE_AUDIT.md` — master verdict.
2. `HANDOFF_TO_MASTER.md` — concise integration handoff.
3. `ADAPTIVE_THEOREM_FINAL.md` — theorem A1 and proof.
4. `LITERATURE_PRIORITY_AUDIT.md` — priority positioning.

## Source-numbered theorem files

- `U1_PREORDER_REFINEMENT.md`
- `U2_T0_PHASE_TRANSITION.md`
- `U3_LEXICOGRAPHIC_FACTORIZATION.md`
- `U4_CONE_DECOMPOSITION.md`
- `U5_CARTESIAN_SATURATION.md`
- `U6_NEWLY_ENABLED_MEASUREMENT.md`

The prompt anticipated a different U4/U5/U6 numbering, so compatibility note files are also included.

## Computation

- `verify_u1_u6.py`
- `verify_u3_abstract_independent.py`
- `verify_cartesian_independent.py`
- `verify_u4_octahedral_f2.py`
- `verify_u4_octahedral_Q.py`
- `verify_chain_adaptive.py`
- `verify_chain_adaptive_independent.py`

Main outputs include the transition census, cartesian audit, cone exactness summaries, chain-depth tables, legal-query profiles, optimal protocol JSON, and counterexamples.

All CSVs were validated for constant row width; the package checksum manifest is `SHA256SUMS.txt`.
''')

# Verification log
write('VERIFICATION_LOG.md', r'''
# Verification log

## Carrier/refinement audit

`verify_u1_u6.py`

- distinct observation-generated four-world preorders: 355
- one-bit transition cases: 5,680
- U1 failures: 0
- U3 failures: 0
- cartesian support cases: 90,880
- U5 failures: 0
- fine-measurable U6 cases: 80,652
- U6 failures: 0

## Independent U3 abstract audit

`verify_u3_abstract_independent.py`

- abstract base-poset/fiber cases through four points: 3,450
- failures: 0

## Independent cartesian/measurability audit

`verify_cartesian_independent.py`

- set partitions of four points: 15
- partition/label/event cases: 3,840
- fine-measurable cases: 2,348
- U6 equivalence failures: 0

## U4 over F2

`verify_u4_octahedral_f2.py`

- transitions: 5,680
- LES exactness checks: 62,934
- failures: 0
- relative-homology dimension checks: 18,982
- post-T0 cases: 3,504

## U4 over Q

`verify_u4_octahedral_Q.py`

- representative exact-rational cases: 1,420
- exactness checks: 15,387
- failures: 0

## Adaptive chain theorem

`verify_chain_adaptive.py`

- exact optimization n=2..10
- legal profiles recorded: 2,044
- all theorem checks: pass

`verify_chain_adaptive_independent.py`

- independent constructive/lower-bound checks n=2..30
- all checks: pass
''')

# Save a machine-readable handoff/status
with (out/'AUDIT_SUMMARY.json').open('w',encoding='utf-8') as f:
    json.dump({
        'date':'2026-09-29',
        'gate':'SURVIVES_WITH_REPAIRS',
        'repairs':{
            'U2':'Allow new strict order inside a split coarse fiber; only cross-fiber comparabilities are monotone-downward.',
            'U4':'Exact triangle/LES, not direct-sum decomposition.',
            'U6':'Fine-measurability hypothesis is essential.'
        },
        'new_result':'A1 chain safe-query dichotomy and optimal-depth theorem',
        'recommended_next':'height-two adaptive identification under repair-forest/boundary-matrix admissibility with a fixed query library'
    }, f, indent=2)

