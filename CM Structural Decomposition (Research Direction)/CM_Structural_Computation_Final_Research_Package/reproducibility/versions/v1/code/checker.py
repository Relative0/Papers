"""Separate scalar semantic checker. Does not import the producer/evaluator.

The external truth integer is the authority, not a digest bundled by producer.
This is tested Python, not a formally verified checker. Width limits are policy.
"""
from __future__ import annotations


def _index(scope, env):
    out = 0
    for v in scope:
        out = out * 2 + env[v]
    return out


def validate_structure(a):
    scope, payload = a.scope, a.payload
    if len(scope) > 16 or len(set(scope)) != len(scope) or any(type(v) is not int or v < 0 for v in scope):
        raise ValueError('invalid scope')
    def table(b, s):
        if type(b) is not int or b < 0 or b.bit_length() > 2**len(s):
            raise ValueError('invalid truth table')
    if a.kind == 'flat':
        if len(payload) != 1: raise ValueError('arity')
        table(payload[0], scope)
    elif a.kind in ('xor', 'product'):
        if len(payload) != (2 if a.kind == 'xor' else 1): raise ValueError('arity')
        if a.kind == 'xor' and (type(payload[0]) is not int or payload[0] not in (0, 1)):
            raise ValueError('constant')
        factors = payload[1] if a.kind == 'xor' else payload[0]
        coverage = []
        for s, b in factors:
            coverage.extend(s)
            table(b, s)
        if sorted(coverage) != sorted(scope): raise ValueError('not a disjoint scope cover')
    elif a.kind in ('rank', 'cofactor'):
        if len(payload) != 4: raise ValueError('arity')
        left, right, one, two = payload
        if sorted(left+right) != sorted(scope): raise ValueError('invalid bipartition')
        if a.kind == 'rank':
            if len(one) != 2**len(left): raise ValueError('coefficient length')
            for c in one:
                if type(c) is not int or c < 0 or c >= 2**len(two): raise ValueError('coefficient')
            for row in two: table(row, right)
        else:
            if not one or len(two) != 2**len(left): raise ValueError('prototype/references length')
            for row in one: table(row, right)
            for j, b in two:
                if type(j) is not int or not 0 <= j < len(one) or type(b) is not int or b not in (0, 1):
                    raise ValueError('reference')
    else:
        raise ValueError('unknown kind')


def evaluate(a, env):
    p = a.payload
    if a.kind == 'flat': return (p[0] >> _index(a.scope, env)) & 1
    if a.kind in ('xor', 'product'):
        factors = p[1] if a.kind == 'xor' else p[0]
        val = p[0] if a.kind == 'xor' else 1
        for s, b in factors:
            v = (b >> _index(s, env)) & 1
            val = val ^ v if a.kind == 'xor' else val * v
        return val
    left, right, one, two = p
    i, j = _index(left, env), _index(right, env)
    if a.kind == 'rank':
        out = 0
        for k in range(len(two)):
            out ^= ((one[i] >> k) & 1) * ((two[k] >> j) & 1)
        return out
    k, flip = two[i]
    return ((one[k] >> j) & 1) ^ flip


def verify(a, expected: int) -> bool:
    try:
        validate_structure(a)
        if type(expected) is not int or expected < 0 or expected.bit_length() > 2**len(a.scope):
            return False
        for index in range(2**len(a.scope)):
            env = {v: (index >> (len(a.scope)-j-1)) & 1 for j, v in enumerate(a.scope)}
            if evaluate(a, env) != ((expected >> index) & 1): return False
        return True
    except (ValueError, TypeError, IndexError, KeyError):
        return False
