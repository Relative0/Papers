"""Read a one-output combinational AIGER file and evaluate its full truth table."""
from __future__ import annotations

from pathlib import Path


def _varint(data: bytes, offset: int):
    value = shift = 0
    while True:
        if offset >= len(data) or shift > 63:
            raise ValueError('invalid AIGER delta')
        byte = data[offset]
        offset += 1
        value |= (byte & 0x7f) << shift
        if byte < 128:
            return value, offset
        shift += 7


def truth_bits(path: Path, support: tuple[str, ...]):
    data = path.read_bytes()
    header, rest = data.split(b'\n', 1)
    words = header.decode('ascii').split()
    if len(words) < 6 or words[0] != 'aig':
        raise ValueError('expected binary AIGER')
    maximum, inputs, latches, outputs, ands = map(int, words[1:6])
    if latches != 0 or outputs != 1 or inputs != len(support) or maximum != inputs + ands:
        raise ValueError('unexpected AIGER shape')
    if len(words) > 6 and any(int(value) for value in words[6:]):
        raise ValueError('AIGER properties not admitted')
    line, rest = rest.split(b'\n', 1)
    output_literal = int(line)
    offset = 0
    gates = []
    for gate in range(ands):
        delta0, offset = _varint(rest, offset)
        delta1, offset = _varint(rest, offset)
        lhs = 2 * (inputs + gate + 1)
        rhs0 = lhs - delta0
        rhs1 = rhs0 - delta1
        if not (0 <= rhs1 <= rhs0 < lhs):
            raise ValueError('invalid AIGER AND fanin')
        gates.append((rhs0, rhs1))
    symbol_lines = rest[offset:].decode('utf-8', errors='replace').splitlines()
    symbols = {}
    for line in symbol_lines:
        if line.startswith('i') and ' ' in line:
            index, name = line[1:].split(' ', 1)
            if index.isdigit():
                symbols[int(index)] = name
    if symbols and (len(symbols) != inputs or
                    any(symbols[j] != support[j] for j in range(inputs))):
        raise ValueError('AIGER input symbols differ from frozen support order')
    width = 1 << inputs
    mask = (1 << width) - 1
    values = {0: 0}
    for j in range(inputs):
        values[j + 1] = sum(((assignment >> j) & 1) << assignment for assignment in range(width))

    def literal_value(literal):
        value = values[literal >> 1]
        return value ^ (mask if literal & 1 else 0)

    for gate, (left, right) in enumerate(gates):
        values[inputs + gate + 1] = literal_value(left) & literal_value(right)
    return literal_value(output_literal), {'inputs': inputs, 'and_gates': ands,
                                           'input_symbols_present': bool(symbols)}
