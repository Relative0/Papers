"""Implementation B: relative F2 chain matrix, independently constructs cells.

Does not import or call repair_graph. Vertices are all retained, so C0rel=0.
"""
from itertools import combinations

def analyze(n, pairs, q):
    less = [[False]*n for _ in range(n)]
    for a,b in pairs:
        less[a][b]=True
    labels = [(q>>i)&1 for i in range(n)]
    deleted_edges = []
    for a,b in combinations(range(n),2):
        if less[a][b] and labels[a]>labels[b]:
            deleted_edges.append((a,b))
    edge_number = {e:i for i,e in enumerate(deleted_edges)}
    columns = []
    for triple in combinations(range(n),3):
        a,b,c=triple
        if not (less[a][b] and less[b][c] and less[a][c]):
            continue
        # A simplex survives precisely when its labels are nondecreasing.
        if labels[a]<=labels[b]<=labels[c]:
            continue
        column=0
        for edge in combinations(triple,2):
            if edge in edge_number:
                column ^= 1<<edge_number[edge]
        columns.append(column)
    pivots = {}
    for col in columns:
        while col:
            pivot=col.bit_length()-1
            if pivot not in pivots:
                pivots[pivot]=col
                break
            col ^= pivots[pivot]
    rank=len(pivots)
    return len(columns)==len(deleted_edges)==rank, len(deleted_edges),len(columns),rank
