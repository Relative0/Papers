# Round 2 reviewer E: Returning reproducibility and research-software specialist

**Disclosure:** same-assistant adversarial specialist-role assessment of frozen Draft 2; no independent external review.

The frozen source versions, source-hash check and standard-library-only tests are valuable. The new codec and legacy adapter substantially improve reproducibility. Nevertheless the frozen dataclass claim is broader than runtime enforcement: a direct caller can still supply a mutable list.

Normalize nested containers on construction or reject them, test post-construction mutation of the caller-owned list, and ensure malformed structure is rejected before a query is trusted. Avoid sharing the semantic checker with the producer's critical evaluation routine. Codec roundtrip means semantic equality after canonicalizing variable order, not byte identity for every arbitrary input object.

A clean-directory replay should include all test suites and validate manuscript freeze hashes. Store actual command outputs rather than writing 'tests pass' based on memory. The Python ROBDD should deserialize its stored nodes, not rebuild from truth, when claiming persisted-state replay.

The strongest case for release is a transparent, reproducible audit. The strongest case against an assurance claim is lack of formal verification and true independent implementation. Keep these distinctions visible. No evidence justifies a security-hardening or external-certification label.

## Requested disposition
Revise against the concrete requests above. Unexecuted optimized comparisons and unsettled priority remain open; they are not waived by this role assessment.
