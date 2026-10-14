"""Strict native Boolean CM block-matrix engine.

All matrices are over Boolean bits. Row-by-column composition is performed by
AND on routed bits and XOR on converging routes. The only phase generator is
the native 4x4 CM rotation P. There is no separate coefficient-product
primitive.

For speed, a Boolean matrix is stored as a tuple of Python integers, one bitset
per row. This is only a compact representation of ordinary 0/1 matrices.
"""
from __future__ import annotations

from itertools import product
from typing import Iterable, Sequence, Tuple

Rows = Tuple[int, ...]


def identity(n: int) -> Rows:
    return tuple(1 << i for i in range(n))


def zero(nrows: int) -> Rows:
    return tuple(0 for _ in range(nrows))


def xor_matrix(A: Rows, B: Rows) -> Rows:
    assert len(A) == len(B)
    return tuple(a ^ b for a, b in zip(A, B))


def compose(A: Rows, B: Rows) -> Rows:
    """Boolean row-by-column composition using only routed AND and XOR.

    A is r x m and B is m x n. Rows are bitsets; len(B)=m. The width n is
    implicit in B's row masks.
    """
    out = []
    m = len(B)
    for ar in A:
        row = 0
        bits = ar
        k = 0
        while bits:
            lsb = bits & -bits
            k = lsb.bit_length() - 1
            if k >= m:
                raise ValueError("matrix width mismatch")
            row ^= B[k]
            bits ^= lsb
        out.append(row)
    return tuple(out)


def apply(A: Rows, v: int) -> int:
    """Apply a Boolean matrix to a Boolean column vector bitset."""
    out = 0
    for i, row in enumerate(A):
        if (row & v).bit_count() & 1:
            out |= 1 << i
    return out


def transpose(A: Rows, ncols: int) -> Rows:
    out = [0] * ncols
    for i, row in enumerate(A):
        for j in range(ncols):
            if (row >> j) & 1:
                out[j] |= 1 << i
    return tuple(out)


def rank(A: Rows, ncols: int) -> int:
    rows = list(A)
    r = 0
    for c in range(ncols):
        p = next((i for i in range(r, len(rows)) if (rows[i] >> c) & 1), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        pivot = rows[r]
        for i in range(len(rows)):
            if i != r and ((rows[i] >> c) & 1):
                rows[i] ^= pivot
        r += 1
        if r == len(rows):
            break
    return r


def inverse(A: Rows, n: int) -> Rows | None:
    if len(A) != n:
        raise ValueError("square matrix required")
    left = list(A)
    right = [1 << i for i in range(n)]
    r = 0
    for c in range(n):
        p = next((i for i in range(r, n) if (left[i] >> c) & 1), None)
        if p is None:
            return None
        left[r], left[p] = left[p], left[r]
        right[r], right[p] = right[p], right[r]
        for i in range(n):
            if i != r and ((left[i] >> c) & 1):
                left[i] ^= left[r]
                right[i] ^= right[r]
        r += 1
    if tuple(left) != identity(n):
        return None
    return tuple(right)


def power(A: Rows, k: int) -> Rows:
    R = identity(len(A))
    X = A
    while k:
        if k & 1:
            R = compose(R, X)
        X = compose(X, X)
        k >>= 1
    return R


def rows_to_lists(A: Rows, ncols: int) -> list[list[int]]:
    return [[(row >> j) & 1 for j in range(ncols)] for row in A]


def matrix_key(A: Rows) -> tuple[int, ...]:
    return tuple(A)


def direct_sum(A: Rows, a_cols: int, B: Rows, b_cols: int) -> Rows:
    return tuple(A) + tuple(row << a_cols for row in B)


def block_matrix(blocks: Sequence[Sequence[Rows]], block_size: int = 4) -> Rows:
    """Assemble a rectangular matrix of equal square Boolean blocks."""
    br = len(blocks)
    bc = len(blocks[0]) if br else 0
    out = []
    for i in range(br):
        assert len(blocks[i]) == bc
        for r in range(block_size):
            row = 0
            for j in range(bc):
                B = blocks[i][j]
                assert len(B) == block_size
                row |= B[r] << (j * block_size)
            out.append(row)
    return tuple(out)


def extract_block(A: Rows, block_row: int, block_col: int, block_size: int = 4) -> Rows:
    mask = (1 << block_size) - 1
    start = block_row * block_size
    return tuple((A[start + r] >> (block_col * block_size)) & mask for r in range(block_size))


def block_row(A: Rows, block_row_index: int, block_cols: int, block_size: int = 4) -> Rows:
    start = block_row_index * block_size
    width = block_cols * block_size
    mask = (1 << width) - 1
    return tuple(A[start + r] & mask for r in range(block_size))


def left_compose_small(U: Rows, E: Rows) -> Rows:
    """U (4x4) composed with E (4xn)."""
    return compose(U, E)


def kron_f2(A: Rows, a_cols: int, B: Rows, b_cols: int) -> Rows:
    """Ordinary Kronecker product of Boolean matrices over XOR/AND."""
    out = []
    for ar in A:
        for br in B:
            row = 0
            for aj in range(a_cols):
                if (ar >> aj) & 1:
                    row ^= br << (aj * b_cols)
            out.append(row)
    return tuple(out)


# ---------------------------------------------------------------------------
# Native CM phase register
# cyclic coordinate order (E0,E1,E2,E3)
# ---------------------------------------------------------------------------
I4 = identity(4)
Z4 = zero(4)
P: Rows = (
    0b1000,  # output E0 gets previous E3
    0b0001,  # output E1 gets previous E0
    0b0010,  # output E2 gets previous E1
    0b0100,  # output E3 gets previous E2
)
P2 = compose(P, P)
P3 = compose(P2, P)
K: Rows = (
    0b0001,
    0b1000,
    0b0100,
    0b0010,
)
N = xor_matrix(P, I4)          # native finite-difference / rotation-defect operator
N2 = compose(N, N)             # I XOR P^2
N3 = compose(N2, N)            # I XOR P XOR P^2 XOR P^3
N4 = compose(N3, N)
N_POWERS = (I4, N, N2, N3, Z4)
P_POWERS = (I4, P, P2, P3)
E0_VEC = 0b0001


def phase_operator(selector: int) -> Rows:
    """XOR the selected native rotations I,P,P^2,P^3."""
    A = Z4
    for k in range(4):
        if (selector >> k) & 1:
            A = xor_matrix(A, P_POWERS[k])
    return A


PHASE_OPS: tuple[Rows, ...] = tuple(phase_operator(m) for m in range(16))
PHASE_VECTORS: tuple[int, ...] = tuple(apply(A, E0_VEC) for A in PHASE_OPS)
assert PHASE_VECTORS == tuple(range(16))
UNIT_SELECTORS = tuple(m for m, A in enumerate(PHASE_OPS) if rank(A, 4) == 4)


def selector_from_operator(A: Rows) -> int:
    """Recover selector from a native phase operator by its action on E0."""
    v = apply(A, E0_VEC)
    if PHASE_OPS[v] != A:
        raise ValueError("operator not in the P-generated phase algebra")
    return v


def phase_compose_selector(a: int, b: int) -> int:
    """Composition in the P-generated algebra, derived by actual 4x4 matrices."""
    return selector_from_operator(compose(PHASE_OPS[a], PHASE_OPS[b]))


def expand_selector_matrix(entries: Sequence[int], nrows: int, ncols: int) -> Rows:
    assert len(entries) == nrows * ncols
    blocks = []
    for i in range(nrows):
        blocks.append([PHASE_OPS[entries[i*ncols+j]] for j in range(ncols)])
    return block_matrix(blocks, 4)


def phase_row_blocks(effect: Rows) -> tuple[Rows, Rows]:
    """Split a 4x8 effect row-block into its two 4x4 phase blocks."""
    return extract_rect_block(effect, 0), extract_rect_block(effect, 1)


def extract_rect_block(effect: Rows, block_col: int, block_size: int = 4) -> Rows:
    mask = (1 << block_size) - 1
    return tuple((row >> (block_col * block_size)) & mask for row in effect)


def canonical_effect(effect: Rows) -> Rows:
    candidates = [left_compose_small(PHASE_OPS[u], effect) for u in UNIT_SELECTORS]
    return min(candidates)


def canonical_unordered_basis_from_gate(G: Rows) -> tuple[Rows, Rows]:
    e0 = canonical_effect(block_row(G, 0, 2, 4))
    e1 = canonical_effect(block_row(G, 1, 2, 4))
    return tuple(sorted((e0, e1)))  # type: ignore[return-value]


def enumerate_phase_block_gates():
    """Enumerate all 2x2 block matrices whose 4x4 blocks are generated by P."""
    rows = []
    invertible = []
    orthogonal = []
    I8 = identity(8)
    for entries in product(range(16), repeat=4):
        G = expand_selector_matrix(entries, 2, 2)
        r = rank(G, 8)
        inv = r == 8
        orth = inv and compose(transpose(G, 8), G) == I8
        rows.append((entries, r, inv, orth))
        if inv:
            invertible.append((entries, G))
        if orth:
            orthogonal.append((entries, G))
    return rows, invertible, orthogonal


def measurement_bases(invertible_gates):
    all_bases = sorted({canonical_unordered_basis_from_gate(G) for _, G in invertible_gates})
    return all_bases


def unitary_measurement_bases(orthogonal_gates):
    return sorted({canonical_unordered_basis_from_gate(G) for _, G in orthogonal_gates})


# ---------------------------------------------------------------------------
# States and effects
# ---------------------------------------------------------------------------

def pack_phase_branches(branches: Sequence[int]) -> int:
    v = 0
    for i, b in enumerate(branches):
        v |= (b & 0xF) << (4 * i)
    return v


def unpack_phase_branches(v: int, nbranches: int) -> tuple[int, ...]:
    return tuple((v >> (4*i)) & 0xF for i in range(nbranches))


def effect_blocks(effect: Rows, nblocks: int) -> tuple[Rows, ...]:
    return tuple(extract_rect_block(effect, j, 4) for j in range(nblocks))


def joint_effect2(e: Rows, f: Rows) -> Rows:
    eb = effect_blocks(e, 2)
    fb = effect_blocks(f, 2)
    blocks = [[None for _ in range(4)]]
    flat = []
    for i in range(2):
        for j in range(2):
            flat.append(compose(eb[i], fb[j]))
    return block_matrix([flat], 4)


def support2(state16: int, e: Rows, f: Rows) -> bool:
    J = joint_effect2(e, f)
    return apply(J, state16) != 0


def support_table2(state16: int, basis_a, basis_b) -> tuple[int, int, int, int]:
    return tuple(int(support2(state16, e, f)) for e in basis_a for f in basis_b)


def joint_effect3(e: Rows, f: Rows, g: Rows) -> Rows:
    eb = effect_blocks(e, 2)
    fb = effect_blocks(f, 2)
    gb = effect_blocks(g, 2)
    flat = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                flat.append(compose(compose(eb[i], fb[j]), gb[k]))
    return block_matrix([flat], 4)


def support3(state32: int, e: Rows, f: Rows, g: Rows) -> bool:
    J = joint_effect3(e, f, g)
    return apply(J, state32) != 0


def support_table3(state32: int, basis_a, basis_b, basis_c) -> tuple[int, ...]:
    return tuple(int(support3(state32, e, f, g)) for e in basis_a for f in basis_b for g in basis_c)


def embedded_basis(rows2: Sequence[Sequence[int]]) -> tuple[Rows, Rows]:
    """Make two 4x8 effects from a 2x2 embedded Boolean basis."""
    effects = []
    for row in rows2:
        effects.append(block_matrix([[I4 if row[j] else Z4 for j in range(2)]], 4))
    return tuple(effects)  # type: ignore[return-value]


BASIS_Z = embedded_basis(((1,0),(0,1)))
BASIS_X = embedded_basis(((1,1),(1,0)))
BASIS_Y = embedded_basis(((0,1),(1,1)))
MQT_BASES = (BASIS_Z, BASIS_X, BASIS_Y)
MQT_NAMES = ("Z", "X", "Y")


def canonical_state(a: int, b: int) -> int:
    """diag(N^a,N^b) state, with a,b in 0..4 and N^4=0."""
    va = apply(N_POWERS[a], E0_VEC)
    vb = apply(N_POWERS[b], E0_VEC)
    return pack_phase_branches((va,0,0,vb))


def bell_support_state() -> int:
    return canonical_state(0,0)


def bell_delta_state() -> int:
    return canonical_state(0,2)


def ghz_state(a111: int = 0) -> int:
    """Phase E0 on |000>, N^a111 E0 on |111>."""
    branches = [0]*8
    branches[0] = E0_VEC
    branches[7] = apply(N_POWERS[a111], E0_VEC)
    return pack_phase_branches(branches)


# ---------------------------------------------------------------------------
# Logical block gates with a shared 4-bit phase register
# ---------------------------------------------------------------------------
SHEAR2 = block_matrix([[I4,Z4],[I4,I4]],4)
H_ROT = block_matrix([[I4,N2],[N2,I4]],4)
X_LOGICAL = block_matrix([[Z4,I4],[I4,Z4]],4)
K_UPPER = block_matrix([[I4,I4],[Z4,I4]],4)


def lift_single_bit_gate(G8: Rows, nbits: int, target: int) -> Rows:
    """Lift a 2-branch phase-block gate to n logical bits with shared phase."""
    nbranches = 1 << nbits
    blocks = [[Z4 for _ in range(nbranches)] for _ in range(nbranches)]
    gblocks = [[extract_block(G8, r, c,4) for c in range(2)] for r in range(2)]
    for inp in range(nbranches):
        ibit = (inp >> (nbits-1-target)) & 1
        rest_mask = inp & ~(1 << (nbits-1-target))
        for obit in range(2):
            out = rest_mask | (obit << (nbits-1-target))
            blocks[out][inp] = gblocks[obit][ibit]
    return block_matrix(blocks,4)


def logical_cnot(nbits: int, control: int, target: int) -> Rows:
    nbranches = 1 << nbits
    blocks = [[Z4 for _ in range(nbranches)] for _ in range(nbranches)]
    for inp in range(nbranches):
        c = (inp >> (nbits-1-control)) & 1
        out = inp
        if c:
            out ^= 1 << (nbits-1-target)
        blocks[out][inp] = I4
    return block_matrix(blocks,4)


def logical_branch_permutation(nbits: int, mapping) -> Rows:
    nbranches=1<<nbits
    blocks=[[Z4 for _ in range(nbranches)] for _ in range(nbranches)]
    for inp in range(nbranches):
        blocks[mapping(inp)][inp]=I4
    return block_matrix(blocks,4)


# ---------------------------------------------------------------------------
# Teleportation analyzer and resource branch maps
# ---------------------------------------------------------------------------
# Four embedded-F2 2x2 matrices I, X, K, KX are vectorized as columns.
I2_F2 = (0b01,0b10)
X2_F2 = (0b10,0b01)
K2_F2 = (0b11,0b10)
KX2_F2 = compose(K2_F2, X2_F2)


def vectorize2(A: Rows) -> tuple[int,int,int,int]:
    # row-major entries
    return ((A[0]>>0)&1,(A[0]>>1)&1,(A[1]>>0)&1,(A[1]>>1)&1)


def columns_to_matrix(cols: Sequence[Sequence[int]]) -> Rows:
    nrows=len(cols[0]); ncols=len(cols)
    rows=[]
    for i in range(nrows):
        row=0
        for j,c in enumerate(cols):
            if c[i]: row |= 1<<j
        rows.append(row)
    return tuple(rows)


BELL_COLUMNS = tuple(vectorize2(A) for A in (I2_F2,X2_F2,K2_F2,KX2_F2))
BELL_Q_F2 = columns_to_matrix(BELL_COLUMNS)
BELL_ANALYZER_F2 = inverse(BELL_Q_F2,4)
assert BELL_ANALYZER_F2 is not None
BELL_ANALYZER_16 = kron_f2(BELL_ANALYZER_F2,4,I4,4)


def resource_prep_map(resource_selectors: Sequence[int]) -> Rows:
    """32x8 map from unknown one-bit phase state to input x resource.

    Branch ordering is (input_bit, alice_resource_bit, bob_bit), binary 000..111.
    Each resource coefficient is a P-generated 4x4 Boolean phase operator.
    """
    assert len(resource_selectors)==4
    blocks=[[Z4 for _ in range(2)] for _ in range(8)]
    for i in range(2):
        for a in range(2):
            for b in range(2):
                out=(i<<2)|(a<<1)|b
                blocks[out][i]=PHASE_OPS[resource_selectors[2*a+b]]
    return block_matrix(blocks,4)


def analyzer_on_alice_pair(analyzer4_f2: Rows = BELL_ANALYZER_F2) -> Rows:
    """32x32 embedded analyzer on (input, Alice-half), identity on Bob."""
    # 8 logical branches; analyzer index m over first two bits, Bob untouched.
    blocks=[[Z4 for _ in range(8)] for _ in range(8)]
    for m in range(4):
        for ia in range(4):
            if (analyzer4_f2[m] >> ia) & 1:
                for b in range(2):
                    out=(m<<1)|b
                    inp=(ia<<1)|b
                    blocks[out][inp]=I4
    return block_matrix(blocks,4)


GLOBAL_BELL_ANALYZER = analyzer_on_alice_pair()


def outcome_selector(m: int) -> Rows:
    """8x32 selector for Bob's two phase branches after Alice outcome m."""
    blocks=[[Z4 for _ in range(8)] for _ in range(2)]
    blocks[0][2*m]=I4
    blocks[1][2*m+1]=I4
    return block_matrix(blocks,4)


def teleport_branch_maps(resource_selectors: Sequence[int]) -> tuple[Rows, Rows, Rows, Rows]:
    prep=resource_prep_map(resource_selectors)
    after=compose(GLOBAL_BELL_ANALYZER,prep)  # 32x8
    return tuple(compose(outcome_selector(m),after) for m in range(4))  # type: ignore[return-value]


def resource_transfer_matrix(resource_selectors: Sequence[int]) -> Rows:
    return expand_selector_matrix(resource_selectors,2,2)


# ---------------------------------------------------------------------------
# Rotation-filtration / derived Smith classification
# ---------------------------------------------------------------------------
N_GLOBAL_POWERS = tuple(block_matrix([[N_POWERS[j],Z4],[Z4,N_POWERS[j]]],4) for j in range(5))


def rotation_rank_profile(resource_selectors: Sequence[int]) -> tuple[int,int,int,int]:
    M=resource_transfer_matrix(resource_selectors)
    return tuple(rank(compose(N_GLOBAL_POWERS[j],M),8) for j in range(4))


def canonical_profiles():
    d={}
    for a in range(5):
        for b in range(a,5):
            entries=(apply(N_POWERS[a],E0_VEC),0,0,apply(N_POWERS[b],E0_VEC))
            prof=rotation_rank_profile(entries)
            if prof in d:
                raise AssertionError((prof,d[prof],(a,b)))
            d[prof]=(a,b)
    return d

CANONICAL_PROFILES=canonical_profiles()


def rotation_class(resource_selectors: Sequence[int]) -> tuple[int,int]:
    return CANONICAL_PROFILES[rotation_rank_profile(resource_selectors)]


def simple_tensor_states() -> set[int]:
    states=set()
    for x0,x1,y0,y1 in product(range(16),repeat=4):
        xb=(x0,x1); yb=(y0,y1)
        branches=[]
        for i in range(2):
            for j in range(2):
                branches.append(apply(PHASE_OPS[xb[i]], yb[j]))
        states.add(pack_phase_branches(branches))
    return states


# ---------------------------------------------------------------------------
# Contextuality SAT helpers
# ---------------------------------------------------------------------------
def compatible_bell_globals(state16: int, bases) -> list[tuple[int,...]]:
    n=len(bases)
    tables={(i,j):support_table2(state16,bases[i],bases[j]) for i in range(n) for j in range(n)}
    good=[]
    for assignment in product((0,1),repeat=2*n):
        if all(tables[(i,j)][2*assignment[i]+assignment[n+j]] for i in range(n) for j in range(n)):
            good.append(assignment)
    return good


def bell_support_coverage_small(state16: int, bases):
    n=len(bases)
    good=compatible_bell_globals(state16,bases)
    uncovered=[]
    for i in range(n):
        for j in range(n):
            t=support_table2(state16,bases[i],bases[j])
            for idx,possible in enumerate(t):
                if not possible: continue
                a,b=idx//2,idx%2
                if not any(g[i]==a and g[n+j]==b for g in good):
                    uncovered.append((i,j,a,b))
    return good,uncovered


def two_sat_support_coverage(state16: int, bases):
    n=len(bases); Nvars=2*n
    adj=[[] for _ in range(2*Nvars)]
    clauses=[]
    tables={}
    def node(v,val): return 2*v+val
    def neg(x): return x^1
    def add_clause(v1,val1,v2,val2):
        clauses.append((v1,val1,v2,val2))
        adj[node(v1,1-val1)].append(node(v2,val2))
        adj[node(v2,1-val2)].append(node(v1,val1))
    for i,A in enumerate(bases):
        for j,B in enumerate(bases):
            t=support_table2(state16,A,B); tables[(i,j)]=t
            for a in (0,1):
                for b in (0,1):
                    if not t[2*a+b]:
                        add_clause(i,1-a,n+j,1-b)
    idx=0; stack=[]; on=[False]*(2*Nvars)
    ids=[-1]*(2*Nvars); low=[0]*(2*Nvars); comp=[-1]*(2*Nvars); cc=0
    import sys; sys.setrecursionlimit(max(10000,4*Nvars+100))
    def dfs(v):
        nonlocal idx,cc
        ids[v]=low[v]=idx; idx+=1; stack.append(v); on[v]=True
        for w in adj[v]:
            if ids[w]<0:
                dfs(w); low[v]=min(low[v],low[w])
            elif on[w]:
                low[v]=min(low[v],ids[w])
        if low[v]==ids[v]:
            while True:
                w=stack.pop(); on[w]=False; comp[w]=cc
                if w==v: break
            cc+=1
    for v in range(2*Nvars):
        if ids[v]<0: dfs(v)
    possible_sections=sum(sum(t) for t in tables.values())
    sat=not any(comp[2*v]==comp[2*v+1] for v in range(Nvars))
    if not sat:
        return dict(satisfiable=False,clauses=len(clauses),possible_sections=possible_sections,
                    extendable_possible_sections=0,uncovered_possible_sections=possible_sections,
                    first_uncovered=None)
    reachable=[]
    for start in range(2*Nvars):
        seen=1<<start; st=[start]
        while st:
            v=st.pop()
            for w in adj[v]:
                bit=1<<w
                if not seen&bit:
                    seen|=bit; st.append(w)
        reachable.append(seen)
    def reaches(x,y): return bool(reachable[x]&(1<<y))
    uncovered=[]; extendable=0
    for (i,j),t in tables.items():
        for a in (0,1):
            for b in (0,1):
                if not t[2*a+b]: continue
                l=node(i,a); m=node(n+j,b)
                bad=(reaches(l,neg(l)) or reaches(m,neg(m)) or reaches(l,neg(m)) or reaches(m,neg(l)))
                if bad: uncovered.append((i,j,a,b))
                else: extendable+=1
    return dict(satisfiable=True,clauses=len(clauses),possible_sections=possible_sections,
                extendable_possible_sections=extendable,uncovered_possible_sections=len(uncovered),
                first_uncovered=None if not uncovered else uncovered[0])


def analyzer_on_alice_pair_phase(analyzer16: Rows) -> Rows:
    """Lift a 4-branch x 4-phase (16x16) analyzer to three logical bits.

    It acts on the first two logical bits and leaves Bob's logical bit alone.
    """
    blocks=[[Z4 for _ in range(8)] for _ in range(8)]
    ablocks=[[extract_block(analyzer16,m,ia,4) for ia in range(4)] for m in range(4)]
    for m in range(4):
        for ia in range(4):
            A=ablocks[m][ia]
            if A != Z4:
                for b in range(2):
                    blocks[(m<<1)|b][(ia<<1)|b]=A
    return block_matrix(blocks,4)


def teleport_branch_maps_with_phase_analyzer(resource_selectors: Sequence[int], analyzer16: Rows) -> tuple[Rows,Rows,Rows,Rows]:
    prep=resource_prep_map(resource_selectors)
    global_A=analyzer_on_alice_pair_phase(analyzer16)
    after=compose(global_A,prep)
    return tuple(compose(outcome_selector(m),after) for m in range(4))  # type: ignore[return-value]


def block_selectors_2x2(G8: Rows) -> tuple[int,int,int,int]:
    vals=[]
    for i in range(2):
        for j in range(2):
            vals.append(selector_from_operator(extract_block(G8,i,j,4)))
    return tuple(vals)  # type: ignore[return-value]


def block_selectors_square(G: Rows, nblocks: int) -> tuple[int,...]:
    vals=[]
    for i in range(nblocks):
        for j in range(nblocks):
            vals.append(selector_from_operator(extract_block(G,i,j,4)))
    return tuple(vals)
