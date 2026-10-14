"""Screen the pinned original EPFL primary outputs without invoking a CM compiler."""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from hashlib import sha1, sha256
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'epfl_original'
CM_SOURCE = HERE.parent / '02_CONTRACT_REVISION_20260926' / 'reproducibility' / 'source'
sys.path.insert(0, str(CM_SOURCE))
from cm_exprlib import And, Not, Or, Var  # noqa: E402

MAX_BYTES, MAX_NODES, MAX_IO = 16_000_000, 500_000, 4096
MAX_FANIN, MAX_CUBES, MAX_AST = 6, 64, 4096
COMMIT = '0060e156826e733d69bf5b3322d1bdd0d03a1f9a'


@dataclass(frozen=True)
class Node:
    fanins: tuple[str, ...]
    cubes: tuple[str, ...]
    polarity: int


def logical_lines(raw: bytes):
    pending = ''
    for physical in raw.decode('utf-8').splitlines():
        line = physical.split('#', 1)[0].strip()
        if not line:
            continue
        pending = (pending + ' ' + line).strip() if pending else line
        if pending.endswith('\\'):
            pending = pending[:-1].rstrip()
            continue
        yield pending
        pending = ''
    if pending:
        raise ValueError('unterminated line continuation')


def parse(path: Path):
    raw = path.read_bytes()
    if len(raw) > MAX_BYTES:
        raise ValueError('16 MB bound')
    lines = list(logical_lines(raw))
    inputs, outputs, nodes = [], [], {}
    model = None
    ended = False
    i = 0
    while i < len(lines):
        words = lines[i].split()
        directive = words[0]
        if directive == '.model':
            if model is not None or len(words) != 2:
                raise ValueError('invalid model')
            model = words[1]
        elif directive == '.inputs':
            if inputs or len(words) < 2:
                raise ValueError('invalid inputs')
            inputs.extend(words[1:])
        elif directive == '.outputs':
            if outputs or len(words) < 2:
                raise ValueError('invalid outputs')
            outputs.extend(words[1:])
        elif directive == '.names':
            fanins, name = tuple(words[1:-1]), words[-1]
            if (len(words) < 2 or len(fanins) > MAX_FANIN or name in nodes
                    or name in inputs or len(set(fanins)) != len(fanins)):
                raise ValueError('invalid node')
            cubes, polarity = [], None
            i += 1
            while i < len(lines) and not lines[i].startswith('.'):
                row = lines[i].split()
                if not fanins:
                    if row not in (['0'], ['1']):
                        raise ValueError('invalid constant row')
                    pattern, value = '', int(row[0])
                else:
                    if (len(row) != 2 or len(row[0]) != len(fanins)
                            or set(row[0]) - set('01-') or row[1] not in ('0', '1')):
                        raise ValueError('invalid cube')
                    pattern, value = row[0], int(row[1])
                if polarity is not None and polarity != value:
                    raise ValueError('mixed cube polarity')
                polarity = value
                cubes.append(pattern)
                if len(cubes) > MAX_CUBES:
                    raise ValueError('64-cube bound')
                i += 1
            nodes[name] = Node(fanins, tuple(cubes), 1 if polarity is None else polarity)
            if len(nodes) > MAX_NODES:
                raise ValueError('500000-node bound')
            continue
        elif directive == '.end':
            if ended or len(words) != 1 or i != len(lines) - 1:
                raise ValueError('invalid end')
            ended = True
        else:
            raise ValueError(f'unsupported directive {directive}')
        i += 1
    if (not model or not ended or not inputs or not outputs or len(inputs) > MAX_IO
            or len(outputs) > MAX_IO or len(set(inputs)) != len(inputs)
            or len(set(outputs)) != len(outputs)):
        raise ValueError('incomplete or oversized model')
    return tuple(inputs), tuple(outputs), nodes


def relevant(node: Node):
    return tuple(child for j, child in enumerate(node.fanins)
                 if any(cube[j] in '01' for cube in node.cubes))


def bounded_cone(root: str, inputs: tuple[str, ...], nodes: dict[str, Node]):
    input_set = set(inputs)
    if root not in nodes:
        return None, 'undriven_or_direct_input'
    seen, support, stack = set(), set(), [root]
    while stack:
        signal = stack.pop()
        if signal in input_set:
            support.add(signal)
            if len(support) > 12:
                return None, 'support_over_12'
            continue
        if signal in seen:
            continue
        node = nodes.get(signal)
        if node is None:
            return None, 'missing_driver'
        seen.add(signal)
        if len(seen) > 128:
            return None, 'source_nodes_over_128'
        stack.extend(relevant(node))
    if len(support) < 2:
        return None, 'support_under_2'
    depths = {name: 0 for name in support}
    active = set()

    def depth(signal):
        if signal in depths:
            return depths[signal]
        if signal in active:
            raise ValueError('cyclic dependency')
        active.add(signal)
        value = 1 + max((depth(child) for child in relevant(nodes[signal])), default=0)
        active.remove(signal)
        depths[signal] = value
        return value

    height = depth(root)
    if height > 128:
        return None, 'depth_over_128'
    return {'support': tuple(sorted(support)), 'source_nodes': len(seen),
            'source_edges': sum(len(relevant(nodes[n])) for n in seen),
            'depth': height}, None


def balanced(values, operator):
    level = list(values)
    while len(level) > 1:
        level = [level[j] if j + 1 == len(level) else operator(level[j], level[j + 1])
                 for j in range(0, len(level), 2)]
    return level[0]


def translated(root, support, nodes):
    vars_by_name = {name: Var(j) for j, name in enumerate(support)}
    anchor = vars_by_name[support[0]]
    one, zero = Or(anchor, Not(anchor)), And(anchor, Not(anchor))
    memo = {}
    active = set()

    def build(signal):
        if signal in vars_by_name:
            return vars_by_name[signal]
        if signal in memo:
            return memo[signal]
        if signal in active:
            raise ValueError('cyclic dependency')
        active.add(signal)
        node = nodes[signal]
        terms = []
        for pattern in node.cubes:
            literals = [build(child) if bit == '1' else Not(build(child))
                        for bit, child in zip(pattern, node.fanins) if bit != '-']
            terms.append(balanced(literals, And) if literals else one)
        value = balanced(terms, Or) if terms else zero
        if node.polarity == 0:
            value = Not(value)
        active.remove(signal)
        memo[signal] = value
        return value

    return build(root)


def ast_stats(root):
    ordered, seen, stack = [], set(), [(root, False)]
    while stack:
        expr, done = stack.pop()
        identity = id(expr)
        if done:
            ordered.append(expr)
            continue
        if identity in seen:
            continue
        seen.add(identity)
        if len(seen) > MAX_AST:
            raise ValueError('unique AST nodes over 4096')
        stack.append((expr, True))
        if isinstance(expr, Not):
            stack.append((expr.a, False))
        elif isinstance(expr, (And, Or)):
            stack.extend(((expr.b, False), (expr.a, False)))
    indices = {id(expr): j for j, expr in enumerate(ordered)}
    rows, signatures, references = [], [], Counter()
    for expr in ordered:
        if isinstance(expr, Var):
            row = ['Var', expr.i]
            signature = ('Var', expr.i)
        elif isinstance(expr, Not):
            row = ['Not', indices[id(expr.a)]]
            signature = ('Not', signatures[row[1]])
            references[id(expr.a)] += 1
        else:
            row = [type(expr).__name__, indices[id(expr.a)], indices[id(expr.b)]]
            signature = (row[0], signatures[row[1]], signatures[row[2]])
            references[id(expr.a)] += 1
            references[id(expr.b)] += 1
        rows.append(row)
        signatures.append(sha256(repr(signature).encode('utf-8')).hexdigest())
    occurrences = Counter({id(root): 1})
    for expr in reversed(ordered):
        count = occurrences[id(expr)]
        if isinstance(expr, Not):
            occurrences[id(expr.a)] += count
        elif isinstance(expr, (And, Or)):
            occurrences[id(expr.a)] += count
            occurrences[id(expr.b)] += count
    sig_counts = Counter(signatures)
    return {'translated_ast_sha256': sha256(json.dumps(rows, separators=(',', ':')).encode()).hexdigest(),
            'ast_unique_object_nodes': len(ordered),
            'ast_occurrences': sum(occurrences.values()),
            'identity_shared_nodes': sum(n > 1 for n in references.values()),
            'equal_but_distinct_object_nodes': sum(n - 1 for n in sig_counts.values() if n > 1)}


def truth_digest(root, support, nodes):
    width = 1 << len(support)
    mask = (1 << width) - 1
    values = {}
    for j, name in enumerate(support):
        values[name] = sum(((assignment >> j) & 1) << assignment for assignment in range(width))

    def evaluate(signal):
        if signal in values:
            return values[signal]
        node = nodes[signal]
        result = 0
        for pattern in node.cubes:
            cube = mask
            for bit, child in zip(pattern, node.fanins):
                if bit != '-':
                    value = evaluate(child)
                    cube &= value if bit == '1' else (~value) & mask
            result |= cube
        if node.polarity == 0:
            result = (~result) & mask
        values[signal] = result
        return result

    truth = evaluate(root)
    data = len(support).to_bytes(1, 'little') + truth.to_bytes((width + 7) // 8, 'little')
    return sha256(data).hexdigest()


def main():
    cases_file = HERE / 'NATURAL_CASES.jsonl'
    screen_file = HERE / 'NATURAL_SCREEN.jsonl'
    manifest_file = HERE / 'NATURAL_ADMISSION.json'
    if any(path.exists() for path in (cases_file, screen_file, manifest_file)):
        raise RuntimeError('Admission output already exists; work in a copy for replication')
    paths = sorted(SOURCE.glob('arithmetic/*.blif')) + sorted(SOURCE.glob('random_control/*.blif'))
    assert len(paths) == 20
    all_cases, all_screen, designs = [], [], []
    for path in paths:
        raw = path.read_bytes()
        design = path.stem
        descriptor = {'design': design, 'relative_path': path.relative_to(SOURCE).as_posix(),
                      'bytes': len(raw), 'sha256': sha256(raw).hexdigest(),
                      'git_blob_sha1': sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()}
        try:
            inputs, outputs, nodes = parse(path)
            descriptor.update({'primary_inputs': len(inputs), 'primary_outputs': len(outputs),
                               'source_nodes': len(nodes)})
        except Exception as exc:
            descriptor['parse_error'] = f'{type(exc).__name__}: {exc}'
            designs.append(descriptor)
            continue
        eligible = []
        screened = []
        for output in outputs:
            try:
                metadata, reason = bounded_cone(output, inputs, nodes)
            except Exception as exc:
                metadata, reason = None, f'{type(exc).__name__}: {exc}'
            row = {'design': design, 'output': output, 'structural_status':
                   'eligible' if metadata is not None else reason}
            if metadata is not None:
                row.update(metadata)
                row['rank_sha256'] = sha256(f'EPFL-v5:{design}:{output}'.encode()).hexdigest()
                eligible.append(row)
            screened.append(row)
        selected = sorted(eligible, key=lambda item: (item['rank_sha256'], item['output']))[:8]
        selected_names = {row['output'] for row in selected}
        for row in screened:
            row['selected'] = row['output'] in selected_names
            all_screen.append(row)
        descriptor['structurally_eligible_outputs'] = len(eligible)
        descriptor['selected_outputs'] = len(selected)
        descriptor['screen_reasons'] = dict(Counter(row['structural_status'] for row in screened))
        for row in selected:
            case = {key: row[key] for key in ('design', 'output', 'support', 'source_nodes',
                    'source_edges', 'depth', 'rank_sha256')}
            case['source_sha256'] = descriptor['sha256']
            try:
                expression = translated(row['output'], row['support'], nodes)
                case.update(ast_stats(expression))
                case['source_truth_sha256'] = truth_digest(row['output'], row['support'], nodes)
                case['status'] = 'ADMITTED_PREMEASUREMENT'
            except Exception as exc:
                case['status'] = 'TRANSLATION_EXCLUDED'
                case['reason'] = f'{type(exc).__name__}: {exc}'
            all_cases.append(case)
        designs.append(descriptor)
        print(f'{design}: {len(eligible)}/{len(outputs)} eligible, {len(selected)} selected', flush=True)
    groups = defaultdict(list)
    for case in all_cases:
        if case['status'] == 'ADMITTED_PREMEASUREMENT':
            groups[(len(case['support']), case['source_truth_sha256'])].append(
                [case['design'], case['output']])
    for case in all_cases:
        if case['status'] == 'ADMITTED_PREMEASUREMENT':
            case['semantic_duplicate_group_size'] = len(groups[(len(case['support']), case['source_truth_sha256'])])
    summary = {'status': 'ADMISSION_ONLY_NO_CM_COMPILATION_OR_TIMING',
               'source_repository': 'https://github.com/lsils/benchmarks',
               'source_commit': COMMIT, 'source_license': 'MIT',
               'rule_sha256': sha256((HERE / 'NATURAL_ADMISSION_RULES.md').read_bytes()).hexdigest(),
               'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
               'designs': designs, 'selected_cases': len(all_cases),
               'admitted_cases': sum(c['status'] == 'ADMITTED_PREMEASUREMENT' for c in all_cases),
               'translation_exclusions': sum(c['status'] == 'TRANSLATION_EXCLUDED' for c in all_cases),
               'semantic_duplicate_groups': [items for items in groups.values() if len(items) > 1]}
    for destination, rows in ((cases_file, all_cases), (screen_file, all_screen)):
        destination.write_text(''.join(json.dumps(row, sort_keys=True) + '\n' for row in rows), encoding='utf-8')
    manifest_file.write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'designs': len(designs), 'selected': len(all_cases),
                      'admitted': summary['admitted_cases'],
                      'translation_exclusions': summary['translation_exclusions']}))


if __name__ == '__main__':
    main()
