"""Generate the article's inventory table from a fresh, self-contained run.

Counts are enumerated; support/coding/teleportation columns apply the theorems.
"""
import argparse
import csv
from pathlib import Path


def table(results):
    with (results / 'A2_smith_inventory.csv').open(newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 15 or sum(int(row['count']) for row in rows) != 65536:
        raise ValueError('Expected all 15 Smith classes and 65536 matrices')
    lines = [
        r'\begin{table}[ht]\centering\small',
        r'\begin{tabular}{rrrrrrll}',
        r'\toprule',
        r'$(a,b)$ & Count & $r$ & $h$ & Binary rank & Messages & Support & Teleport\\\midrule',
    ]
    for row in rows:
        a, b, n = (int(row[k]) for k in ('a', 'b', 'count'))
        r = int(a < 4) + int(b < 4)
        h = 0 if not r else 1 + int(a == b)
        support = 'Excluded' if not r else 'Local' if r == 1 else 'Strong' if h == 2 else 'Logical'
        messages = str(2 * h) if r else 'n/a'
        teleport = 'n/a' if not r else 'Yes' if a == b == 0 else 'No'
        lines.append(f'$({a},{b})$ & {n:,} & {r} & {h} & {8-a-b} & {messages} & {support} & {teleport}' + r'\\')
    lines += [
        r'\bottomrule\end{tabular}',
        r'\caption{All fifteen Smith classes over $A=\mathbb F_2[u]/(u^4)$ for $2\times2$ matrices. Exponent $4$ denotes zero. Counts are exhaustively enumerated; the remaining columns apply the analytic formulas. Logical means logical but not strong. Zero is excluded from the resource tasks.}\label{tab:smith}',
        r'\end{table}',
    ]
    return '\n'.join(lines) + '\n'


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--results', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    args.out.write_text(table(args.results), encoding='utf-8', newline='\n')
    print(f'Generated {args.out}')
