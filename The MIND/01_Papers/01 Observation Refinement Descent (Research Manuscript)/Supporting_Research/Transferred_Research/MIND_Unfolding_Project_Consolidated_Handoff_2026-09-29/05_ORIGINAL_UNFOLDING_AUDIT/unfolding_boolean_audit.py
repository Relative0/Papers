#!/usr/bin/env python3
"""Finite audit of the 2015 thesis's logical unfolding operator.

No third-party dependencies.  The script separates three constructions:
1. thesis one-step unfolding of a chosen factorization (Boolean OR semantics),
2. an exact-layer Boolean-lattice extension of repeated unfolding,
3. an unsigned linear incidence operator over Z and F_2.

Run: python3 unfolding_boolean_audit.py
"""
from itertools import product, combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def all_bits(n):
    return list(product([0, 1], repeat=n))


def thesis_unfold_factor_values(values):
    """OR_j( not factor_j AND all other factors ), i.e. exactly one factor false."""
    m = len(values)
    return int(sum(1 for v in values if not v) == 1)


def rep_dependence_example():
    # f = X & Y, represented as [X,Y] or [X,Y,X|Z].  Same conjunction.
    rows = []
    differs = []
    for X, Y, Z in all_bits(3):
        conj2 = X & Y
        conj3 = X & Y & (X | Z)
        u2 = thesis_unfold_factor_values([X, Y])
        u3 = thesis_unfold_factor_values([X, Y, X | Z])
        row = {"X": X, "Y": Y, "Z": Z,
               "conj_[X,Y]": conj2,
               "conj_[X,Y,XorZ]": conj3,
               "U_[X,Y]": u2,
               "U_[X,Y,XorZ]": u3}
        rows.append(row)
        if u2 != u3:
            differs.append(row)
    assert all(r["conj_[X,Y]"] == r["conj_[X,Y,XorZ]"] for r in rows)
    return rows, differs


def exact_layer(m, k):
    """Sets of negated coordinates at exact unfolding depth k."""
    return [tuple(c) for c in combinations(range(m), k)]


def thesis_printed_partial2_xyz(x, y, z):
    # As printed in Example 2.6:
    # X & not(Y&Z) OR Y & not(X&Z) OR Z & not(X&Y)
    return int((x and not (y and z)) or
               (y and not (x and z)) or
               (z and not (x and y)))


def exact_two_negations_xyz(x, y, z):
    return int((1-x)+(1-y)+(1-z) == 2)


def compare_printed_second_stage():
    rows = []
    for x, y, z in all_bits(3):
        rows.append({
            "X": x, "Y": y, "Z": z,
            "printed_partial2": thesis_printed_partial2_xyz(x,y,z),
            "exact_two_negations": exact_two_negations_xyz(x,y,z),
            "hamming_weight": x+y+z,
        })
    return rows


def incidence_matrix_rank_m(m, k):
    """Unsigned incidence D_k: rank-k subsets -> rank-(k+1) subsets."""
    src = exact_layer(m, k)
    tgt = exact_layer(m, k+1)
    idx = {s:i for i,s in enumerate(tgt)}
    M = [[0]*len(src) for _ in tgt]
    for j, S in enumerate(src):
        sset = set(S)
        for a in range(m):
            if a not in sset:
                T = tuple(sorted((*S, a)))
                M[idx[T]][j] += 1
    return src, tgt, M


def matmul(A, B):
    if not A or not B:
        return []
    assert len(A[0]) == len(B)
    return [[sum(A[i][k]*B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]


def mod2(M):
    return [[x % 2 for x in row] for row in M]


def is_zero(M):
    return all(x == 0 for row in M for x in row)


def unsigned_square_example(m=4):
    data=[]
    for k in range(m-1):
        _, _, Dk = incidence_matrix_rank_m(m,k)
        _, _, Dk1 = incidence_matrix_rank_m(m,k+1)
        sqZ = matmul(Dk1,Dk)
        sqF2 = mod2(sqZ)
        vals = sorted(set(x for row in sqZ for x in row))
        data.append({
            "m":m,"k":k,
            "integer_Dkp1_Dk_values":vals,
            "integer_square_zero":is_zero(sqZ),
            "F2_square_zero":is_zero(sqF2),
            "integer_square_matrix":sqZ,
        })
    return data


def boolean_derivative_monomial(bits, j):
    # f(x)=AND_i x_i; Boolean derivative is f(x_j=0) XOR f(x_j=1).
    b0=list(bits); b1=list(bits); b0[j]=0; b1[j]=1
    f0=int(all(b0)); f1=int(all(b1))
    return f0 ^ f1


def verify_gated_boolean_derivative(max_m=5):
    bad=[]
    for m in range(1,max_m+1):
        for bits in all_bits(m):
            for j in range(m):
                factors=list(bits)
                summand=int((not bits[j]) and all(bits[i] for i in range(m) if i!=j))
                gated=int((not bits[j]) and boolean_derivative_monomial(bits,j))
                if summand != gated:
                    bad.append((m,bits,j,summand,gated))
    return bad


def thesis_gluing_example_27():
    rows=[]
    for X,Y,Z in all_bits(3):
        lhs=int(((X and Y) or (Y and Z)) and
                ((X and Z) or (Y and Z)) and
                ((X and Y) or (Y and Z)))
        rhs=int(X and Y and Z)
        rows.append({"X":X,"Y":Y,"Z":Z,"lhs":lhs,"rhs_XYZ":rhs,"equal":lhs==rhs})
    return rows


def main():
    rows, differs = rep_dependence_example()
    printed = compare_printed_second_stage()
    layers = {str(m): {str(k): exact_layer(m,k) for k in range(m+1)} for m in range(1,6)}
    squares = unsigned_square_example(4)
    derivative_bad = verify_gated_boolean_derivative(5)
    gluing_rows = thesis_gluing_example_27()

    result = {
        "representation_dependence": {
            "description": "[X,Y] and [X,Y,X OR Z] have the same conjunction X AND Y but different unfoldings.",
            "truth_table": rows,
            "differing_rows": differs,
        },
        "exact_hamming_layers_up_to_5_factors": layers,
        "printed_Example_2_6_vs_exact_two_negations": printed,
        "unsigned_incidence_square": squares,
        "gated_boolean_derivative_verification": {"max_arity":5,"counterexamples": derivative_bad},
        "thesis_gluing_example_2_7": gluing_rows,
        "claims_checked": {
            "one_step_is_exactly_one_factor_false": True,
            "not_well_defined_mod_boolean_equivalence": len(differs) > 0,
            "unsigned_integer_linearization_square_zero": all(x["integer_square_zero"] for x in squares),
            "F2_linearization_square_zero": all(x["F2_square_zero"] for x in squares),
            "gated_boolean_derivative_identity_verified_through_arity_5": len(derivative_bad)==0,
            "thesis_gluing_example_2_7_identity": all(r["equal"] for r in gluing_rows),
        }
    }
    out = HERE / "boolean_audit_results.json"
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("Representation dependence counterexample rows:")
    for r in differs:
        print(r)
    print("\nPrinted Example 2.6 truth set (X,Y,Z):",
          [(r['X'],r['Y'],r['Z']) for r in printed if r['printed_partial2']])
    print("Exact two-negation layer truth set:",
          [(r['X'],r['Y'],r['Z']) for r in printed if r['exact_two_negations']])
    print("\nGated Boolean derivative counterexamples:", derivative_bad)
    print("Thesis Example 2.7 gluing counterexamples:", [r for r in gluing_rows if not r["equal"]])
    print("\nUnsigned incidence squares over Z / F2:")
    for x in squares:
        print(f"k={x['k']}: values={x['integer_Dkp1_Dk_values']}, "
              f"Z-zero={x['integer_square_zero']}, F2-zero={x['F2_square_zero']}")
    print(f"\nWrote {out}")

if __name__ == "__main__":
    main()
