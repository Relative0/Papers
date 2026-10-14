from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Dict, FrozenSet, Iterable, List, Optional, Sequence, Set, Tuple, Union

# CM truth-table ordering follows the paper/user specification:
# (theta_11, theta_12, theta_21, theta_22) corresponds to
# (X,Y)=(1,1),(1,0),(0,1),(0,0).
CM = Tuple[int, int, int, int]


def cm_eval(cm: CM, x: int, y: int) -> int:
    if x:
        return cm[0] if y else cm[1]
    return cm[2] if y else cm[3]


def cm_from_callable(fn: Callable[[int, int], int]) -> CM:
    return (fn(1, 1) & 1, fn(1, 0) & 1, fn(0, 1) & 1, fn(0, 0) & 1)


def cm_compose(phi: CM, a: CM, b: CM) -> CM:
    """Pointwise composition: phi(a(X,Y), b(X,Y))."""
    return tuple(cm_eval(phi, cm_eval(a, x, y), cm_eval(b, x, y))
                 for x, y in ((1,1),(1,0),(0,1),(0,0)))  # type: ignore[return-value]


def cm_not_output(cm: CM) -> CM:
    return tuple(1-v for v in cm)  # type: ignore[return-value]


def cm_swap_operands(cm: CM) -> CM:
    # transpose: 11 fixed, 12<->21, 22 fixed
    return (cm[0], cm[2], cm[1], cm[3])


def cm_negate_left_operand(cm: CM) -> CM:
    # f(~X,Y): rows X=1 and X=0 exchange in the semantic table.
    return (cm[2], cm[3], cm[0], cm[1])


def cm_negate_right_operand(cm: CM) -> CM:
    # f(X,~Y): columns exchange.
    return (cm[1], cm[0], cm[3], cm[2])


def cm_anf_coeffs(cm: CM) -> Tuple[int,int,int,int]:
    t11,t12,t21,t22 = cm
    a = t22
    b = t12 ^ t22
    c = t21 ^ t22
    d = t11 ^ t12 ^ t21 ^ t22
    return a,b,c,d


def cm_is_nonlinear(cm: CM) -> bool:
    return bool(cm_anf_coeffs(cm)[3])


def cm_feature_parity(cm: CM) -> int:
    return (cm[0] ^ cm[1] ^ cm[2] ^ cm[3]) & 1


OPS: Dict[str, CM] = {
    "FALSE": (0,0,0,0),
    "AND":   (1,0,0,0),
    "X_AND_NOT_Y": (0,1,0,0),
    "NOT_X_AND_Y": (0,0,1,0),
    "NOR":   (0,0,0,1),
    "X":     (1,1,0,0),
    "Y":     (1,0,1,0),
    "XOR":   (0,1,1,0),
    "OR":    (1,1,1,0),
    "XNOR":  (1,0,0,1),
    "NOT_Y": (0,1,0,1),
    "NOT_X": (0,0,1,1),
    "IMP":   (1,0,1,1),   # X -> Y
    "RIMP":  (1,1,0,1),   # Y -> X
    "NAND":  (0,1,1,1),
    "TRUE":  (1,1,1,1),
}
CM_TO_NAME = {v:k for k,v in OPS.items()}


@dataclass(frozen=True)
class Var:
    name: str

@dataclass(frozen=True)
class Bin:
    op: CM
    left: 'Expr'
    right: 'Expr'

Expr = Union[Var, Bin]


def op(name: str, left: Expr, right: Expr) -> Bin:
    return Bin(OPS[name], left, right)


def eval_expr(expr: Expr, env: Dict[str,int]) -> int:
    if isinstance(expr, Var):
        return int(bool(env[expr.name]))
    return cm_eval(expr.op, eval_expr(expr.left, env), eval_expr(expr.right, env))


def vars_of(expr: Expr) -> FrozenSet[str]:
    if isinstance(expr, Var):
        return frozenset([expr.name])
    return vars_of(expr.left) | vars_of(expr.right)


def expr_key(expr: Expr) -> tuple:
    if isinstance(expr, Var):
        return ("V", expr.name)
    return ("B", expr.op, expr_key(expr.left), expr_key(expr.right))


def expr_key_cached(expr: Expr, memo: Optional[Dict[int, tuple]] = None) -> tuple:
    """Structural key with object-identity memoization for DAGs/large trees."""
    if memo is None:
        memo = {}
    ident = id(expr)
    if ident in memo:
        return memo[ident]
    if isinstance(expr, Var):
        key = ("V", expr.name)
    else:
        key = (
            "B",
            expr.op,
            expr_key_cached(expr.left, memo),
            expr_key_cached(expr.right, memo),
        )
    memo[ident] = key
    return key


@dataclass
class RewriteCertificate:
    rule: str
    before: tuple
    after: tuple
    details: Dict[str, object]


def _align_pair(a: Bin, b: Bin) -> Optional[Tuple[CM,CM,Expr,Expr,str]]:
    ka0,ka1 = expr_key(a.left), expr_key(a.right)
    kb0,kb1 = expr_key(b.left), expr_key(b.right)
    if (ka0,ka1)==(kb0,kb1):
        return a.op,b.op,a.left,a.right,"same"
    if (ka0,ka1)==(kb1,kb0):
        return a.op,cm_swap_operands(b.op),a.left,a.right,"transpose"
    return None


def fold_cm(expr: Expr, certs: Optional[List[RewriteCertificate]]=None) -> Expr:
    """CM-specific same-operand folding with transpose orientation normalization.

    Deliberately conservative: only folds where both children are explicit two-input
    operator nodes over the same ordered operands (possibly reversed). Quotient is
    represented as ordinary pointwise A AND NOT B and therefore is already covered
    when the exact structure is present; no speculative containment rewrite is used.
    """
    if isinstance(expr, Var):
        return expr
    l = fold_cm(expr.left, certs)
    r = fold_cm(expr.right, certs)
    node = Bin(expr.op,l,r)
    if isinstance(l,Bin) and isinstance(r,Bin):
        aligned = _align_pair(l,r)
        if aligned:
            lop,rop,x,y,orientation = aligned
            h = cm_compose(expr.op,lop,rop)
            out = Bin(h,x,y)
            if certs is not None:
                certs.append(RewriteCertificate(
                    rule="CM_SAME_OPERAND_COMPOSITION",
                    before=expr_key(node), after=expr_key(out),
                    details={"orientation":orientation,"phi":expr.op,"theta1":lop,"theta2":rop,"result":h}
                ))
            return fold_cm(out, certs)
    return node


def fold_generic_2support(expr: Expr, certs: Optional[List[RewriteCertificate]]=None) -> Expr:
    """Strong generic comparator: identical semantic 2-support LUT folding.

    This intentionally tests whether the apparent CM advantage is representation-
    specific or simply the benefit of doing cut-level truth-function composition.
    """
    if isinstance(expr, Var):
        return expr
    l = fold_generic_2support(expr.left, certs)
    r = fold_generic_2support(expr.right, certs)
    node = Bin(expr.op,l,r)
    if isinstance(l,Bin) and isinstance(r,Bin):
        aligned = _align_pair(l,r)
        if aligned:
            lop,rop,x,y,orientation = aligned
            h = cm_compose(expr.op,lop,rop)
            out = Bin(h,x,y)
            if certs is not None:
                certs.append(RewriteCertificate(
                    rule="GENERIC_2SUPPORT_LUT_COMPOSITION",
                    before=expr_key(node), after=expr_key(out),
                    details={"orientation":orientation,"phi":expr.op,"f":lop,"g":rop,"result":h}
                ))
            return fold_generic_2support(out, certs)
    return node
