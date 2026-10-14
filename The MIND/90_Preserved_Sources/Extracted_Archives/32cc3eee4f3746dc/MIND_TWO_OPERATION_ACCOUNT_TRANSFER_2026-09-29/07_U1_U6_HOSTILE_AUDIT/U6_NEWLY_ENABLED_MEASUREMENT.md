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
