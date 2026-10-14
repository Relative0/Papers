"""Exact rational reference dispatch for real F(x,y) = x + y + xy.

The observation count is a sign-oracle count, NOT an arithmetic/runtime claim.
Zero is reported separately. Inputs are positive int/Fraction/rational strings;
floats are rejected rather than silently treated as exact decimal measurements.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from typing import Literal

RationalInput = int | str | Fraction
TRUTH_TABLES: dict[str, tuple[int, int, int, int]] = {
    'AND': (1, 0, 0, 0), 'X': (1, 1, 0, 0),
    'Y': (1, 0, 1, 0), 'XNOR': (1, 0, 0, 1),
}

@dataclass(frozen=True)
class DispatchResult:
    status: Literal['EXACT', 'BOUNDARY']
    operator: str | None
    truth_vector: tuple[int, int, int, int] | None
    observed_signs: tuple[int, ...]

    @property
    def sign_observations(self) -> int:
        return len(self.observed_signs)


def positive_rational(value: RationalInput) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, str, Fraction)):
        raise TypeError('Use an int, Fraction, or rational string; floats are not accepted.')
    result = Fraction(value)
    if result <= 0:
        raise ValueError('Magnitude parameters must be strictly positive.')
    return result


def sign(value: Fraction) -> int:
    return int(value > 0) - int(value < 0)


def score_vector(a: RationalInput, b: RationalInput) -> tuple[Fraction, ...]:
    aa, bb = positive_rational(a), positive_rational(b)
    ab = aa * bb
    return aa + bb + ab, aa - bb - ab, -aa + bb - ab, -aa - bb + ab


def dispatch(a: RationalInput, b: RationalInput,
             mode: Literal['coordinate', 'quartic'] = 'coordinate') -> DispatchResult:
    """Classify, or reject the discriminant, with exact rational arithmetic.

    coordinate: use h1,h2,h3 in that order; positive leaves permit early exit.
    quartic: use h1*h3 and h2*h3, with ternary sign and explicit zero rejection.
    The present implementation computes all scores in either mode. This is
    deliberately not a claim that two quartic observations cost less arithmetic.
    """
    if mode not in ('coordinate', 'quartic'):
        raise ValueError('mode must be coordinate or quartic')
    _, h1, h2, h3 = score_vector(a, b)
    observed: list[int] = []
    if mode == 'coordinate':
        for name, value in zip(('X', 'Y', 'XNOR'), (h1, h2, h3), strict=True):
            s = sign(value)
            observed.append(s)
            if s == 0:
                return DispatchResult('BOUNDARY', None, None, tuple(observed))
            if s > 0:
                # Negative pair sums prove every other h is strictly negative.
                return DispatchResult('EXACT', name, TRUTH_TABLES[name], tuple(observed))
        name = 'AND'
    else:
        for value in (h1 * h3, h2 * h3):
            s = sign(value)
            observed.append(s)
            if s == 0:
                return DispatchResult('BOUNDARY', None, None, tuple(observed))
        signature = tuple(int(s < 0) for s in observed)
        name = {(0, 0): 'AND', (1, 0): 'X', (0, 1): 'Y', (1, 1): 'XNOR'}[signature]
    return DispatchResult('EXACT', name, TRUTH_TABLES[name], tuple(observed))


if __name__ == '__main__':
    import argparse
    import json
    from dataclasses import asdict
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('a', help='Positive rational, e.g. 2 or 1/2')
    parser.add_argument('b', help='Positive rational')
    parser.add_argument('--mode', choices=['coordinate', 'quartic'], default='coordinate')
    args = parser.parse_args()
    try:
        result = dispatch(args.a, args.b, args.mode)
    except (TypeError, ValueError, ZeroDivisionError) as error:
        parser.error(str(error))
    print(json.dumps(asdict(result), indent=2))
