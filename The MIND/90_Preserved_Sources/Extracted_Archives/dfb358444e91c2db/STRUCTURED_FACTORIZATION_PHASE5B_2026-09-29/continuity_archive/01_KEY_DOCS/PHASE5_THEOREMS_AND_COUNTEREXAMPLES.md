# Theorems and Counterexamples

| ID | Statement | Status |
|---|---|---|
| T1 | `max_T |E_T(f)| = |Pi_f|` | proved |
| T2 | Two partitions are simultaneously representable as vtree clades iff their block families are laminar | proved |
| T3 | A defect witness with varying supports `U,W` implies some prime block intersects both | proved |
| C1 | Singleton/singleton defect support is a sound must-link edge | proved |
| T4 | Positive irredundant CNF interaction components equal semantic prime blocks | proved; baseline/priority weak |
| N1 | Every failed cut admits a singleton/singleton rank-two witness | false |
| N2 | Pairwise rank-two interaction graph always recovers semantic prime blocks | false |

## Counterexample family for N1/N2

`f_n=1` iff all variables are 0 or all variables are 1.

For `n>=3`, the semantic prime partition is one block, but every fixed-context two-variable slice has rank at most one. The bundled computation verifies n=3..6 and minimum balanced-cut witness support n.
