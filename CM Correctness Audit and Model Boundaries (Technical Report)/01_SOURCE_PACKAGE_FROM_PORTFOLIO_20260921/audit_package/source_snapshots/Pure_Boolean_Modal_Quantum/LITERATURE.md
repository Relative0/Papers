# Literature Comparison and Novelty Boundary

**Search date:** 2026-09-17.  
This is a bounded literature review, not a proof of novelty. The safest novelty language is “we did not locate prior work combining these exact ingredients” rather than “this has never been done.”

## 1. Modal quantum theory and finite-field quantum models

### Schumacher & Westmoreland — Modal Quantum Theory

- Benjamin Schumacher and Michael D. Westmoreland, **“Modal Quantum Theory,”** *Foundations of Physics* 42, 918–925 (2012).
- DOI: <https://doi.org/10.1007/s10701-012-9650-z>
- arXiv: <https://arxiv.org/abs/1010.2929>

MQT replaces complex amplitudes by a finite field and interprets measurement only through possibility/necessity, not probabilities. It already contains entangled states and versions of Bell's theorem and no-cloning.

**Implication for CM claims:** possible/impossible measurement, finite algebra, nonseparability, Bell-like contradictions, and no-cloning are not novel merely because they are Boolean/finite.

### Schumacher & Westmoreland — Non-contextuality and free will in MQT

- **“Non-contextuality and free will in modal quantum theory,”** arXiv:1010.5452.
- <https://arxiv.org/abs/1010.5452>

The paper gives modal analogues of Kochen–Specker/noncontextuality results and emphasizes that possibility structures can have behavior not representable by ordinary no-signaling probabilities.

**Implication:** a CM contextuality claim needs an explicit possibility structure and global-assignment obstruction, not an analogy to ordinary probability inequalities.

### James, Ortiz & Sabry — Quantum Computing over Finite Fields

- Roshan P. James, Gerardo Ortiz, and Amr Sabry, **“Quantum Computing over Finite Fields,”** arXiv:1101.3764.
- <https://arxiv.org/abs/1101.3764>

This work develops a finite-field/discrete quantum-computing model and explicitly discusses no-cloning, nonlocality, superdense coding, and teleportation.

**Implication:** the universal teleportation and dense-coding-like constructions in this package should be presented as CM-ring realizations/extensions, not first instances of these ideas outside complex quantum mechanics.

### Schumacher & Westmoreland — Almost Quantum Theory

- **“Almost quantum theory,”** arXiv:1204.0701.
- <https://arxiv.org/abs/1204.0701>

This extends modal theory to mixed states, generalized measurements, and open systems without ordinary positivity.

**Implication:** future CM work on generalized modal measurements should compare to these established modal constructions rather than inventing terminology independently.

## 2. Possibilistic Bell/contextuality frameworks

### Abramsky & Brandenburger

- Samson Abramsky and Adam Brandenburger, **“The Sheaf-Theoretic Structure of Non-Locality and Contextuality,”** *New Journal of Physics* 13 (2011) 113036.
- arXiv: <https://arxiv.org/abs/1102.0264>
- DOI: <https://doi.org/10.1088/1367-2630/13/11/113036>

This framework treats nonlocality/contextuality as obstruction to global sections and distinguishes strengths of contextuality using support information as well as probabilities.

**Use here:** “no deterministic global assignment” is identified with a strong/global-section obstruction. The established hierarchy is crucial: a Hardy-type model may have at least one compatible global assignment while still be **logically/possibilistically contextual** because some possible local event has no global extension. Exact relational locality is therefore stronger than merely finding one global section; every possible local section must be covered.

This distinction materially changed the CM result: the `B_star` state `diag(1,delta)` has global sections, so it is not strong, but an exact extension test finds 36,864 unextendable possible sections across the complete 192-basis family. Its correct category is Hardy/logical contextuality, not locality.

### Abramsky & Hardy — Logical Bell inequalities

- Samson Abramsky and Lucien Hardy, **“Logical Bell inequalities,”** *Physical Review A* 85, 062114 (2012).
- DOI: <https://doi.org/10.1103/PhysRevA.85.062114>

The paper makes explicit the logical-consistency core of Bell arguments, including probability-free/all-versus-nothing structures.

**Use here:** the CM Bell and GHZ results are stated directly as Boolean consistency contradictions rather than CHSH expectation-value calculations.

## 3. Phase groups and GHZ-style nonlocality

### Coecke, Edwards & Spekkens

- Bob Coecke, Bill Edwards, and Robert W. Spekkens, **“Phase Groups and the Origin of Non-locality for Qubits,”** arXiv:1003.5005.
- <https://arxiv.org/abs/1003.5005>
- DOI: <https://doi.org/10.1016/j.entcs.2011.01.021>

They compare theories with four-element phase groups, emphasizing the distinction between `Z4` and `Z2 x Z2` and its relation to GHZ correlations.

**Implication:** the mere existence of a four-phase subgroup `C4` in the CM ring is not by itself a novelty claim. The interesting question is how that phase subgroup interacts with the ring's nilpotent ideal structure, LM readout, and the specific CM gate set.

## 4. Quantum mechanics over sets / Booleanized models

### Ellerman — Quantum Mechanics over Sets

- David Ellerman, **“Quantum mechanics over sets: a pedagogical model with non-commutative finite probability theory as its quantum probability calculus,”** *Synthese* 194, 4863–4896 (2017).
- DOI: <https://doi.org/10.1007/s11229-016-1175-0>

QM/Sets works over `Z2`-related set structures but deliberately adds an external natural-number-valued overlap/probability calculus.

**Difference from this core branch:** the present CM work does **not** import that probability calculus. Integer Hamming/support counts remain external diagnostics only.

## 5. Matrix/vector logic and square roots of NOT

### Mizraji — Vector Logic

- Eduardo Mizraji, **“Vector Logic: A Natural Algebraic Representation of the Fundamental Logical Gates,”** *Journal of Logic and Computation* 18(1), 97–121 (2008).
- DOI: <https://doi.org/10.1093/logcom/exm057>

### Mizraji — square root of NOT

- Eduardo Mizraji, **“Vector logic allows counterfactual virtualization by the square root of NOT,”** *Logic Journal of the IGPL* 29(5), 859–870 (2021; online 2020).
- DOI: <https://doi.org/10.1093/jigpal/jzaa026>

Mizraji's vector logic represents truth values and gates using matrices and uses a **complex** square root of NOT in the latter work.

**Difference:** the CM phase square roots discussed in the intrinsic branch are elements of a 16-element characteristic-two ring with zero divisors. They are not complex matrix square roots and do not introduce signed/complex amplitudes.

## 6. Generalized categorical/ring/semiring quantum-like theories

### Coecke et al. — semiring-valued process theories

- Bob Coecke, Fabrizio Genovese, Stefano Gogioso, Dan Marsden, and Robin Piedeleu, **“Uniqueness of Composition in Quantum Theory and Linguistics,”** arXiv:1803.00708.
- <https://arxiv.org/abs/1803.00708>

The work studies wavefunctions/modules over commutative involutive semirings and explicitly includes modal quantum theory among examples.

### Tull — categorical reconstruction over a ring

- Sean Tull, **“A Categorical Reconstruction of Quantum Theory,”** *Logical Methods in Computer Science* 16(1):4 (2020).
- DOI: <https://doi.org/10.23638/LMCS-16(1:4)2020>
- arXiv: <https://arxiv.org/abs/1804.02265>

Tull reconstructs generalized finite-dimensional quantum theories over a suitable ring `S` under categorical axioms.

**Implication:** “quantum-like theory over a ring/semiring” is established territory. Any CM distinction must come from the specific ring, gate/readout machinery, and derived phenomena—not from ring-valued linear algebra alone.

## 7. The exact finite-chain-ring family already appears in quantum-code literature

### Sari & Siap

- Mustafa Sari and Irfan Siap, **“Quantum Codes over a Class of Finite Chain Rings,”** *Quantum Information and Computation* 16(1–2), 39–49 (2016).
- DOI: <https://doi.org/10.26421/QIC16.1-2-3>

This paper studies the chain ring `F2[u]/(u^s)` and uses Gray maps/orthogonality to construct binary quantum error-correcting codes. Setting `s=4` gives the same abstract truncated-polynomial ring as the CM phase ring presentation `F2[u]/(u^4)`.

### Liu & Liu

- Xiusheng Liu and Hualu Liu, **“Quantum Codes from Linear Codes over Finite Chain Rings,”** *Quantum Information Processing* 16, 240 (2017).
- DOI: <https://doi.org/10.1007/s11128-017-1695-7>
- arXiv: <https://arxiv.org/abs/1704.06375>

**Important boundary:** these works use finite chain rings as **coding-algebra inputs** to quantum-code constructions. They are not, from the material located in this search, the same as treating `F2[u]/(u^4)` itself as the modal state coefficient ring with CM-derived phase semantics and LM measurement.

Therefore neither the ring nor its nilpotent chain structure can be claimed as new to quantum-information-adjacent mathematics.

## 8. Finite-ring geometry and contextuality/entanglement adjacency

### Saniga, Planat & Minarovjech — projective lines over finite quotient rings

- Metod Saniga, Michel Planat, and Milan Minarovjech, **“Projective line over the finite quotient ring GF(2)[x]/<x^3-x> and quantum entanglement: The Mermin ‘magic’ square/pentagram,”** *Theoretical and Mathematical Physics* 151(2), 625–631 (2007).
- arXiv: `quant-ph/0603206`; DOI: `10.1007/s11232-007-0049-5`.

This is important adjacent prior art: finite quotient rings, including units and zero divisors, have already been used geometrically to model incidence/commutation structures associated with Mermin contextuality configurations.

**Difference from the present result:** that work studies projective ring-line geometry corresponding to operator configurations. The present CM calculation instead uses `F2[u]/(u^4)` directly as the coefficient ring of modal state vectors and proves a Smith-valuation classification of support extendability across a complete reversible effect-basis family. Therefore broad claims such as “first use of a finite ring/zero divisors in contextuality” would be indefensible.

## 9. Stabilizer/Clifford finite algebra comparisons

### Hostens, Dehaene & De Moor

- Erik Hostens, Jeroen Dehaene, and Bart De Moor, **“Stabilizer states and Clifford operations for systems of arbitrary dimensions and modular arithmetic,”** *Physical Review A* 71, 042315 (2005).
- DOI: <https://doi.org/10.1103/PhysRevA.71.042315>

This establishes extensive stabilizer/Clifford structure using modular arithmetic for arbitrary qudit dimension.

**Implication:** a future “CM stabilizer” paper needs to identify the exact generating group/module and compare its normalizer/action to existing finite modular stabilizer mathematics.

## 10. Smith normal form over finite chain rings

The local-equivalence classification used here is an application of standard Smith theory over principal ideal/finite chain rings, not a new algebra theorem.

Useful background example:

- **“Decoding Linear Codes over Chain Rings Given by Parity Check Matrices,”** *Mathematics* 9(16), 1878 (2021), section on Smith normal form over finite chain rings.
- <https://www.mdpi.com/2227-7390/9/16/1878>

That literature explicitly states that matrices over a commutative principal ideal ring have Smith normal form and specializes an algorithm to chain rings.

What is specific here is using the resulting 15 `2x2` Smith classes as a **CM-nonseparability/resource hierarchy** and connecting class `(0,2)` to the nilpotent teleportation obstruction.

## 11. Defensible current novelty statement

A bounded search did **not** locate a prior paper that simultaneously uses:

1. the original Droncheff CM basis/LM logic machinery;
2. the new cyclic CM convolution producing `F2[C4] ~= F2[u]/(u^4)`;
3. this ring itself as the coefficient system for multipartite modal states;
4. CM transpose as the involution and the specific `H_star`, `B_star`, shear, and CNOT gate set;
5. support-only LM-compatible measurement bases;
6. the complete theorem tying possibilistic contextuality strength to Smith valuations—equal valuations strong, unequal nonzero valuations logical-not-strong, separable classes relationally local; and
7. the resulting distinction between nondegenerate and nilpotent CM-nonseparable teleportation resources.

That combination is the appropriate target for a future novelty claim, after a broader scholarly search and expert review.

## 12. Most important literature-conditioned conclusions

- The **positive Bell and GHZ contradictions** are best classified as embedded finite-field modal results, not new nilpotent effects.
- **Universal teleportation** over all 256 ring-valued one-bit states is a genuine result of this model, but the protocol concept itself has clear finite-field prior art.
- The **Smith/contextuality trichotomy** is now the strongest distinctive result of this pass: the ten nonseparable classes split into four strong equal-valuation classes and six Hardy/logical off-diagonal classes, while all nonzero separable classes are exactly relationally local under the complete reversible-basis family.
- The **singular-but-nonseparable** contrast between support-Bell `(0,0)` and `B_star` `(0,2)` remains operationally important because the latter is logically contextual yet fails the natural universal teleportation construction.
- The exact ring `F2[u]/(u^4)` has quantum-code precedent, so novelty must lie in the CM-derived modal semantics and resource structure, not in naming the ring.

### Werner — tight teleportation classification

- Reinhard F. Werner, **“All teleportation and dense coding schemes,”** *Journal of Physics A: Mathematical and General* 34 (2001) 7081–7094. DOI: 10.1088/0305-4470/34/35/332.
- Establishes, in ordinary finite-dimensional quantum theory, a correspondence among tight teleportation schemes, maximally entangled bases, and unitary error bases.
- Relevance here: the CM theorem should be framed as a chain-ring/tight-linear analogue, not as the first resource characterization for teleportation.

### Abramsky & Coecke — categorical teleportation over generalized scalar systems

- Samson Abramsky and Bob Coecke, **“A Categorical Semantics of Quantum Protocols,”** LICS 2004, pp. 415–425. DOI: 10.1109/LICS.2004.1319636; arXiv:quant-ph/0402130.
- Abstracts teleportation away from complex Hilbert spaces and explicitly discusses algebraic requirements on the scalar (semi)ring.
- Relevance here: generalized-scalar teleportation has established categorical precedents; the CM-specific contribution is the unit-determinant/Smith `(0,0)` classification over `F2[u]/(u^4)` under the present modal linear architecture.

## 13. Conclusive/probabilistic teleportation with nonmaximally entangled resources

### Son et al. — conclusive teleportation

- W. Son, Jinhyoung Lee, M. S. Kim, and Y.-J. Park, **“Conclusive teleportation of a d-dimensional unknown state,”** *Physical Review A* 64, 064304 (2001).
- DOI: <https://doi.org/10.1103/PhysRevA.64.064304>

This paper studies heralded perfect teleportation events using a partially entangled quantum channel, with reduced overall success probability.

### Roa, Delgado & Fuentes-Guridi — optimal conclusive teleportation

- L. Roa, A. Delgado, and I. Fuentes-Guridi, **“Optimal conclusive teleportation of quantum states,”** *Physical Review A* 68, 022310 (2003).
- DOI: <https://doi.org/10.1103/PhysRevA.68.022310>

The work analyzes perfect/conclusive teleportation using nonmaximally entangled resources and relates success to state discrimination.

### Relevance to the CM singular-resource theorem

These ordinary quantum results make an important contrast with the CM chain-ring result. A partially entangled complex pure state can have unequal but still nonzero, invertible field-valued Schmidt coefficients. A conclusive measurement can therefore isolate a branch that remains invertible on the unknown state.

For a singular CM resource, the obstruction is different: the determinant is a **nonunit of the local ring**. Every branch determinant contains that nonunit factor, so no branch can become invertible by postselection within the `A`-linear calculus. The CM statement is therefore not “nonmaximal entanglement never permits conclusive teleportation”; it is the narrower chain-ring statement that **nonunit Smith factors cannot be removed by an `A`-linear analyzer/correction branch**.

The residue-field argument further shows that product local ancillas and any finite tensor power of a singular resource cannot activate universal exact one-bit teleportation: the resource has residue rank at most one, and tensor powers preserve that rank bound.
