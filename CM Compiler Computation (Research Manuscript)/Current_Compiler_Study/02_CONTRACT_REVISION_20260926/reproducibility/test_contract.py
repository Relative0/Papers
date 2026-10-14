"""Regression tests for the manuscript contract against the unmodified snapshot."""
import sys
from itertools import product
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent / 'source'))
import numpy as np
import pytest
import cm_build_pair as pair
from cm_exprlib import And, Not, Or, Var, Xor
from cm_token import TOK, cm_align_signed_operands, cm_compose, cm_token_value
from cmbench.output_budget import OutputBudget, OutputBudgetExceeded

X, Y, Z = Var(0), Var(1), Var(2)
R, C = ['x0'], ['x1']
STRATEGIES = ('pure_structural', 'hybrid', 'retabulate')


@pytest.mark.parametrize('strategy, outcome', zip(STRATEGIES, ('pure_structural', 'pure_structural', 'full_retabulation')))
def test_selected_provenance_for_primitive(strategy, outcome):
    token, metrics = pair.compile_expr_to_cm_pair_token(And(X, Y), R, C, {}, strategy=strategy)
    assert token.token == 0b1000
    assert metrics['root_outcome'] == outcome


@pytest.mark.parametrize('strategy, outcome', zip(STRATEGIES, ('ordinary_fallback', 'full_retabulation', 'full_retabulation')))
def test_admissible_tabulation_is_not_pure_strategy_success(strategy, outcome):
    token, metrics = pair.compile_expr_to_cm_pair_token(Or(X, And(Y, Y)), R, C, {}, strategy=strategy)
    assert metrics['root_outcome'] == outcome
    assert (None if token is None else token.token) == (None if strategy == 'pure_structural' else 0b1110)


def test_structural_parent_of_tabulated_child_is_hybrid():
    token, metrics = pair.compile_expr_to_cm_pair_token(Not(Or(X, And(Y, Y))), R, C, {})
    assert token.token == 0b0001
    assert metrics['root_outcome'] == 'hybrid_pair'


@pytest.mark.parametrize('strategy', STRATEGIES)
def test_syntactic_support_survives_semantic_cancellation(strategy):
    # This denotes X but contains Y syntactically and therefore admits tabulation.
    e = Or(X, Xor(Y, Y))
    token, metrics = pair.compile_expr_to_cm_pair_token(e, R, C, {}, strategy=strategy)
    assert pair._pairable_vars(e, R, C, {}) == ('x0', 'x1')
    assert (None if token is None else token.token) == (None if strategy == 'pure_structural' else 0b1100)
    # This denotes X AND Y but the cancelled Z still prevents root tabulation.
    e3 = Or(And(X, Y), Xor(Z, Z))
    assert pair._pairable_vars(e3, R + ['x2'], C, {}) is None
    token3, _ = pair.compile_expr_to_cm_pair_token(e3, R + ['x2'], C, {}, strategy=strategy)
    assert token3 is None


@pytest.mark.parametrize('strategy', STRATEGIES)
@pytest.mark.parametrize('fixed_value', (0, 1))
def test_fixed_axis_is_retained_in_dense_output(strategy, fixed_value):
    e = Or(And(X, Y), Z)
    rows, cols, fixed = ['x0', 'x2'], ['x1'], {'x2': fixed_value}
    before = (rows.copy(), cols.copy(), fixed.copy())
    matrix, _ = pair.compile_expr_to_cm_pair(e, rows, cols, fixed, pair_strategy=strategy)
    expected = np.array([[fixed_value, fixed_value], [fixed_value, fixed_value],
                         [fixed_value, 1], [fixed_value, 1]], dtype=bool)
    assert matrix.shape == (4, 2)
    assert np.array_equal(matrix, expected)
    assert matrix.flags.owndata and matrix.flags.writeable
    assert (rows, cols, fixed) == before


@pytest.mark.parametrize('strategy', STRATEGIES)
def test_irrelevant_ambient_axis_is_retained(strategy):
    matrix, _ = pair.compile_expr_to_cm_pair(And(X, Y), ['x0', 'unused'], C, {}, pair_strategy=strategy)
    assert matrix.shape == (4, 2)
    assert matrix.tolist() == [[False, False], [False, False], [False, True], [False, True]]


@pytest.mark.parametrize('strategy', ('pure_structural', 'hybrid'))
def test_root_failure_discards_successful_children(strategy):
    e = Or(And(X, Y), Z)
    rows = R + ['x2']
    token, metrics = pair.compile_expr_to_cm_pair_token(e, rows, C, {}, strategy=strategy)
    assert token is None and metrics['root_outcome'] == 'ordinary_fallback'
    assert metrics['primitive_pair_tokens'] == 1 and metrics['pair_collapses'] > 0
    with patch.object(pair, 'compile_expr_to_cm', wraps=pair.compile_expr_to_cm) as builder:
        matrix, _ = pair.compile_expr_to_cm_pair(e, rows, C, {}, pair_strategy=strategy)
        assert builder.call_count == 1
        assert builder.call_args.args[0] is e  # original AST, no rewritten children
    expected = [[False, False], [True, True], [False, True], [True, True]]
    assert matrix.tolist() == expected


def test_token_failure_does_not_execute_builder():
    with patch.object(pair, 'compile_expr_to_cm', side_effect=AssertionError('builder called')):
        token, metrics = pair.compile_expr_to_cm_pair_token(X, R, C, {})
        assert token is None and metrics['root_outcome'] == 'ordinary_fallback'


@pytest.mark.parametrize('rows,cols', [(['x0', 'x0'], C), (R, ['x1', 'x1']), (R, R)])
def test_invalid_layout_is_an_error(rows, cols):
    with pytest.raises(ValueError):
        pair.compile_expr_to_cm_pair_token(And(X, Y), rows, cols, {})


def test_output_budget_counts_retained_axes_before_compilation():
    e = Or(And(X, Y), Z)
    with patch.object(pair, 'compile_expr_to_cm_pair_token', side_effect=AssertionError('compiled before budget')):
        with pytest.raises(OutputBudgetExceeded):
            pair.compile_expr_to_cm_pair(e, ['x0', 'x2'], C, {'x2': 0},
                                        output_budget=OutputBudget(max_output_bytes=4))


@pytest.mark.parametrize('strategy', STRATEGIES)
def test_constant_valued_formula_keeps_syntactic_pair_frame(strategy):
    e = Xor(And(X, Y), And(X, Y))
    token, metrics = pair.compile_expr_to_cm_pair_token(e, R, C, {}, strategy=strategy)
    assert pair._pairable_vars(e, R, C, {}) == ('x0', 'x1')
    assert (token.row_variable, token.column_variable, token.token) == ('x0', 'x1', 0)
    assert metrics['root_outcome'] == ('full_retabulation' if strategy == 'retabulate' else 'pure_structural')


@pytest.mark.parametrize('strategy', STRATEGIES)
def test_identity_sharing_and_separate_equal_trees_preserve_outcome(strategy):
    child = And(Var(0), Var(1))
    shared = Xor(child, child)
    separate = Xor(And(Var(0), Var(1)), And(Var(0), Var(1)))
    a, ma = pair.compile_expr_to_cm_pair_token(shared, R, C, {}, strategy=strategy)
    b, mb = pair.compile_expr_to_cm_pair_token(separate, R, C, {}, strategy=strategy)
    assert a == b and a.token == 0
    assert ma['root_outcome'] == mb['root_outcome']
    assert ma['ast_occurrences'] == mb['ast_occurrences'] == 7
    assert ma['unique_object_nodes'] == 4 and mb['unique_object_nodes'] == 7


def test_exhaustive_signed_fusion_against_direct_boolean_oracle():
    # 16^2 tokens * 8^2 signed frames * 5 supported outer functions * 4 assignments.
    def value(t, x, y):
        return (t >> (2 * x + y)) & 1

    representations = []
    for t, swapped, nf, ns in product(range(16), (False, True), (False, True), (False, True)):
        aligned = cm_align_signed_operands(t, swapped=swapped, negate_first=nf, negate_second=ns)
        values = []
        for x, y in product((0, 1), repeat=2):
            a, b = (y, x) if swapped else (x, y)
            values.append(value(t, a ^ nf, b ^ ns))
        representations.append((aligned, values))
    comparisons = 0
    for (ta, va), (tb, vb), op in product(representations, representations, ('AND', 'OR', 'XOR', 'IMP', 'EQV')):
        token = cm_compose(ta, tb, op)
        for i, (x, y) in enumerate(product((0, 1), repeat=2)):
            assert cm_token_value(token, x, y) == value(TOK[op], va[i], vb[i])
            comparisons += 1
    assert comparisons == 327_680
