# Substantive changes: v2 -> v3

- Added a section on persistent information: exact two-variable histogram counterexample, an all-query state injectivity bound, a deterministic black-box source-verification bound, and a finest-ANF-factor counterexample.
- Strengthened access-model qualifications: field arithmetic, factor-sized versus table-sized work, raw oracle versus formula/certificate access, and unused declared variables.
- Fixed a real direct-constructor aliasing issue by recursively freezing nested caller sequences; added structure/policy tests.
- Implemented actual fresh PackedTruth and ROBDD deserialization; v3 queries newly loaded objects rather than preexisting live objects.
- Recorded a v3 protocol and measured 570 complete 128-query trials. Preserved the earlier timing arms, now explicitly labeled setup/warm-query proxies.
- Added a eight-command clean-directory correctness replay, 278 three-backend reload round trips, 7,070 query comparisons, 510 single-spike rank checks, and 76 exported selected witnesses.
- Added source/claim/novelty/overlap ledgers, deferred directions, actual issue responses and a conservative final audit.
- Broadened related work with tensor-network weighted counting and recent don't-care ACD without importing their different input semantics.

The revised manuscript is 15 pages. Neither a competitive speed result nor historically cleared new general theory is claimed.
