# Paper B - next revision plan after fresh adversarial review

## Mandatory repairs

1. Walsh adjacency: state ordinary facet-adjacency result for `n>=2` or define regular adjacency explicitly; handle `n=1` separately.
2. Add Cover 1965 and a Schlaefli/Zaslavsky hyperplane-arrangement reference.
3. Add an explicit tope-graph reference and say the hypercube-minus-constants graph is classical under the simplex-arrangement equivalence.
4. Add Basu-Pollack-Roy / Jeronimo-Perrucci-Sabia sign-condition references in the polynomial section.
5. Reframe the centered Walsh theorem as a classical calibration/coordinate realization, not the independent novelty spine.
6. Consider restating the Walsh proof using the linear isomorphism to the zero-sum score subspace or the centered Fourier identity `h-E[h]`; retain the explicit coefficient witness as a corollary/example.
7. Prove the two short LM properties used in Paper B directly from the displayed definition, or make the companion paper an accessible stable citation.
8. Change trajectory wording to "relatively open interval components."

## Editorial choice

### Route 1: methods/interface paper

Keep the current architecture and be explicit that the paper's contribution is a rigorous integration/specification layer. Move the Walsh section to "calibration examples" and substantially reduce theorem-novelty language.

### Route 2: stronger research paper

Before another referee round, add one nonclassical payload:

- certified nonlinear implementation/case study;
- restricted guard-language minimum-complexity theorem;
- operator-quotient compression bounds for a structured score class;
- CM/LM-compatible symmetry/orbit theorem with a nontrivial consequence.

## Best next mathematical target

The strongest theoretical target is probably **restricted guard-language exactness**. The unrestricted coarsest fiber is tautological; minimal exact representation in a declared guard language is not. A precise problem statement could be:

> Given a polynomial score family and a finite predicate/inequality library L, determine whether there exists an exact guarded operator atlas using at most k L-definable guards; if so, construct one.

Then investigate hardness, tractable subclasses, or approximation bounds. This would distinguish Paper B from classical sign-condition decomposition because the target is the compressed Boolean-operator quotient subject to a representation language, not enumeration of all sign cells.
