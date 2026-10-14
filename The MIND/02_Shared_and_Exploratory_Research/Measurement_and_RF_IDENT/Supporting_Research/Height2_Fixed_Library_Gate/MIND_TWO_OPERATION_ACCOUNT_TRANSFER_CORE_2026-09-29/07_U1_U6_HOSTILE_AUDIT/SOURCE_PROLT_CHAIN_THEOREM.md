# Source theorem used for adaptive audit

From *Controlled Refinement Regimes for Propositional Logical Topologies* v0.3:

For a coarse signature poset that is a chain, adding a one-bit observation with profile b_1...b_n is topology-defective exactly when the profile is a strict antitone threshold 11...100...0. Every other profile has contractible refined order complex. The reported exact counts are n+1 redundant profiles, n-1 defective profiles, and 2^n-2n nonredundant but homotopy-neutral profiles.

The audit uses the more specific redundancy statement from the same ProLT program: on a T0 carrier, a one-bit observation is topologically redundant exactly when its induced bit is isotone, hence on a chain exactly when the profile is nondecreasing 0*1*.
