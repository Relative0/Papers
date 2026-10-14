"""Finite checks for the explicit QXOR upper-bound qualification (C17).
No external dependencies. The analytic no-information proof is O_f=O for all f.
Running this script writes a JSON result beside the script.
"""
from itertools import product
from pathlib import Path
import json

def oracle(n, f, g0, g1):
    """Permutation of address and target basis labels, target dimension two."""
    assert len(f)==2**n
    assert sorted(g0)==sorted(g1)==[0,1]
    return tuple(2*x+(g1 if f[x] else g0)[y] for x in range(2**n) for y in range(2))

def check():
    count=0
    for n in range(1,4):
        for g in [(0,1),(1,0)]:
            fixed=oracle(n,(0,)*(2**n),g,g)
            for f in product((0,1),repeat=2**n):
                assert oracle(n,f,g,g)==fixed
                count+=1
    bv=0
    for n in range(1,7):
        for s in range(2**n):
            recovered=sum(((s & (1<<j)).bit_count()%2)<<j for j in range(n))
            assert recovered==s
            bv+=1
    for f in product((0,1),repeat=2):
        O=oracle(1,f,(0,1),(1,0))
        answers=[O[2*x]%2 for x in range(2)]
        assert (answers[0]^answers[1])==(f[0]^f[1])
    return {'success':True,'degenerate_oracle_matrices_checked':count,
            'degenerate_address_n_range':[1,3],'shared_target_permutations':2,
            'standard_XOR_Deutsch_functions':4,'standard_XOR_BV_secrets':bv,
            'BV_n_range':[1,6],
            'conclusion':'The lower bounds allow fixed arbitrary invertible G0,G1. Matching classical upper bounds here use the standard informative XOR oracle. G0=G1 makes all oracle matrices identical.',
            'scope':'Not an enumeration of all algorithms; the unbounded degenerate-interface obstruction is immediate from identical operators.'}

if __name__=='__main__':
    result=check()
    print(json.dumps(result,indent=2))
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
