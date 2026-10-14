# RF-IDENT: exact bounded-height-two subclass

Date: 2026-09-29. New phase following the completed fixed-library gate.

**Result:** RF-IDENT is polynomial on every finite poset of height at most two
having a global least and greatest element, for arbitrary explicit oriented
Boolean libraries. General height-two feasibility remains open.

For P={a}+M+{z}, let Q_safe={q:q(a)<=q(z)}. Identification is possible exactly
when Q separates all middle pairs and Q_safe separates each endpoint from every
other state. A canonical peeling-then-star construction provides a successful
tree in O(n^2+m n^2) time including validation of the explicit poset input.

Read:

1. THEOREM.md — precise statement, full proof, construction, and boundary cases.
2. AUDIT.md — objections, computational evidence, limitations, primary-source check.
3. VERIFICATION.json — machine-readable coverage and results.
4. PROTOCOL_EXAMPLES.json — supplied queries and verified example protocols.
5. verify_bounded_height2.py — reproducible standard-library verification.

The prior gate remains unchanged at
`../Height2 Fixed Library Gate 2026-09-29/`. Its general complexity statement
is not superseded. This new result supplies the natural actual-height-two
subclass theorem requested as an acceptable outcome in the handoff.

## Reproduction

From this directory, run:

```powershell
python verify_bounded_height2.py
```

This regenerates only this phase's VERIFICATION.json and PROTOCOL_EXAMPLES.json.
It checks 87,376 matrix safety cases, 16,452 exhaustive small libraries,
9,000 seeded larger libraries, and 83,143 pooled protocol nodes. Every check
passed. The initial execution's corrected syntax error is recorded in AUDIT.md.
Timing is host-dependent and is not a performance guarantee. SHA256SUMS.txt
records hashes of the final phase artifacts except itself; rerunning changes
the timing field and hence the verification JSON hash.

## Phase decision and next step

This research phase is complete: the requested exact natural-subclass theorem
has been proved and checked. No further computation is required for this
deliverable. Continue in this task for closely related corrections, which reuse
the definitions, proof, and evidence. Before publication integration, obtain a
fresh proof review; a new task is appropriate for that independent reading.
GPT-6-astra at high reasoning is a conservative available choice for the
mathematical audit; no cheaper model's reliability for this proof is established
here, and no price or cache saving is asserted. A new general-classification
search is optional and should be deferred until that review.

Suggested review prompt:

> Independently audit THEOREM.md and verify_bounded_height2.py under
> C:\Users\brian\Documents\Math Latex etc\Papers for Publication\The MIND\RF-IDENT Bounded Height2 2026-09-29.
> Reconstruct necessity and sufficiency for arbitrary explicit oriented query
> libraries on P={a}+M+{z}, with M an antichain. Check that initially unsafe
> tests cannot usefully separate an endpoint, that equal-endpoint peeling
> reaches the claimed core, and that both residual stars are identifiable.
> Use the preceding Height2 Fixed Library Gate 2026-09-29/research boundary
> theorem as the inherited topological input. Keep height as strict inequality
> count and test safety before conditioning. Preserve U2/U4/U6/A1 and the
> V5-06/07/09 corrections. Local reversible edits, bounded computations and
> read-only primary-source searches are authorized; no commits, pushes,
> external publication or paid spending. Do not treat this as a solution of
> general height-two RF-IDENT or optimal depth. Report actionable gaps or a
> carefully scoped validation; do not expand to unrelated research branches.
