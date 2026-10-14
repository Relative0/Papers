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
