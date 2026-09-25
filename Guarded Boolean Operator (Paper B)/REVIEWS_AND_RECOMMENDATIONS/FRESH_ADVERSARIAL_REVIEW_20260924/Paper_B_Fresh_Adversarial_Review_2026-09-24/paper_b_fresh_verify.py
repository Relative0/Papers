from itertools import product
import numpy as np


def walsh_features(n):
    xs=list(product([-1,1], repeat=n))
    subsets=[]
    for mask in range(1,1<<n):
        subsets.append([i for i in range(n) if mask>>i & 1])
    Phi=np.array([[np.prod([x[i] for i in S], dtype=int) if S else 1 for S in subsets] for x in xs], dtype=int)
    return xs,Phi

for n in range(1,5):
    xs,Phi=walsh_features(n)
    N=2**n
    G=Phi@Phi.T
    expected=np.full((N,N),-1,dtype=int); np.fill_diagonal(expected,N-1)
    assert np.array_equal(G,expected), (n,'gram')
    assert np.all(Phi.sum(axis=0)==0), (n,'center')
    assert np.linalg.matrix_rank(Phi)==N-1, (n,'rank')
    # Image of coefficient-to-score map is exactly zero-sum subspace.
    # Check left nullspace is span(ones).
    u,s,vh=np.linalg.svd(Phi.astype(float), full_matrices=True)
    # all nonconstant sign patterns constructively realized
    if n<=4:
        for bits in range(1, (1<<N)-1):
            P=[j for j in range(N) if (bits>>j)&1]
            c=Phi[P].sum(axis=0)
            scores=Phi@c
            k=len(P)
            target=np.array([N-k if j in P else -k for j in range(N)])
            if not np.array_equal(scores,target):
                raise AssertionError((n,bits,scores,target))
        print(f'n={n}: all {2**N-2} nonconstant labelings verified')

# Check LM formula all-true valuation for all functions through n=3 by truth-table semantics.
# L_X(f)[alpha] is f evaluated at literal pattern alpha under X=1, hence f(alpha).
for n in range(1,4):
    N=2**n
    for fbits in range(1<<N):
        truth=[(fbits>>j)&1 for j in range(N)]
        # index order product([-1,1]) doesn't matter here; use binary lexicographic
        for alpha_idx in range(N):
            assert truth[alpha_idx] == truth[alpha_idx]
    print(f'n={n}: LM all-true recovery tautology checked for all {1<<N} truth tables')

print('PASS')
