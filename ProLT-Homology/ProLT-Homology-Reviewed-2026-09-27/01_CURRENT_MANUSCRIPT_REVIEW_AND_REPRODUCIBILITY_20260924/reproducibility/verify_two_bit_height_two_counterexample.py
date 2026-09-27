"""Standalone exact verification of the 7-vertex, 2-bit, height-2 counterexample.
No project verifier is imported.
"""
from itertools import permutations

V = tuple(range(7))
P = {
    (0,2),(0,3),(0,4),(0,5),(0,6),
    (1,2),(1,4),(1,5),(1,6),
    (2,5),(2,6),(3,5),(3,6),(4,5),
}
labels = (2,1,1,0,3,0,1)  # 10,01,01,00,11,00,01

# Transitivity and height<=2.
for x,y in P:
    for u,z in P:
        if y == u:
            assert (x,z) in P
assert not any((a,b) in P and (b,c) in P and (c,d) in P
               for a in V for b in V for c in V for d in V)

Q = {(x,y) for x,y in P if labels[x] & ~labels[y] == 0}
DE = sorted(P - Q)
DT = sorted({(x,y,z) for x in V for y in V for z in V
             if (x,y) in P and (y,z) in P
             and not ((x,y) in Q and (x,z) in Q and (y,z) in Q)})
assert len(DE) == len(DT) == 7

row = {e:i for i,e in enumerate(DE)}
B = [[0]*7 for _ in range(7)]
for j,(x,y,z) in enumerate(DT):
    for e,s in [((y,z),1), ((x,z),-1), ((x,y),1)]:
        if e in row:
            B[row[e]][j] = s

def bareiss_det(A):
    A = [r[:] for r in A]
    n = len(A)
    sign = 1
    prev = 1
    for k in range(n-1):
        if A[k][k] == 0:
            p = next((i for i in range(k+1,n) if A[i][k]), None)
            if p is None:
                return 0
            A[k],A[p] = A[p],A[k]
            sign *= -1
        pivot = A[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                A[i][j] = (A[i][j]*pivot - A[i][k]*A[k][j]) // prev
        prev = pivot
        for i in range(k+1,n):
            A[i][k] = 0
    return sign*A[-1][-1]

def rank_f2(A):
    rows = [sum((x & 1) << j for j,x in enumerate(r)) for r in A]
    rank = 0
    n = len(A[0])
    for c in range(n):
        p = next((i for i in range(rank,len(rows)) if (rows[i] >> c) & 1), None)
        if p is None:
            continue
        rows[rank],rows[p] = rows[p],rows[rank]
        for i in range(len(rows)):
            if i != rank and ((rows[i] >> c) & 1):
                rows[i] ^= rows[rank]
        rank += 1
    return rank

support = [[bool(x) for x in r] for r in B]
matchings = [p for p in permutations(range(7))
             if all(support[i][p[i]] for i in range(7))]

def beat_sequence(rel):
    alive = set(V)
    seq = []
    while len(alive) > 1:
        chosen = None
        for v in sorted(alive):
            lo = [u for u in alive if (u,v) in rel]
            hi = [u for u in alive if (v,u) in rel]
            greatest = next((w for w in lo
                             if all(u == w or (u,w) in rel for u in lo)), None)
            least = next((w for w in hi
                          if all(u == w or (w,u) in rel for u in hi)), None)
            if greatest is not None:
                chosen = (v,"down",greatest)
                break
            if least is not None:
                chosen = (v,"up",least)
                break
        if chosen is None:
            break
        seq.append(chosen)
        alive.remove(chosen[0])
    return seq, alive

degrees = [sum(r) for r in support]

assert bareiss_det(B) == -1
assert rank_f2(B) == 7
assert len(matchings) == 3
assert min(degrees) >= 2  # no first deleted-edge free face
assert len(beat_sequence(P)[1]) == 1
assert len(beat_sequence(Q)[1]) == 1

print("P =", sorted(P))
print("labels =", [format(x,"02b") for x in labels])
print("Q =", sorted(Q))
print("deleted edges =", DE)
print("deleted triangles =", DT)
print("relative matrix:")
for r in B:
    print(r)
print("det(B) =", bareiss_det(B))
print("rank_F2(B) =", rank_f2(B))
print("perfect matchings =", len(matchings))
for p in matchings:
    print(" ", p)
print("deleted-edge triangle-degrees =", degrees)
print("P beat reduction =", beat_sequence(P))
print("Q beat reduction =", beat_sequence(Q))
print("VERIFIED")
