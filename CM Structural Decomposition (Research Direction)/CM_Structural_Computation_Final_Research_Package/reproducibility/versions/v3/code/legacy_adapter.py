"""Adapt a legacy document after shape validation; external truth remains authority.

No legacy factor_bits, rank-minimality claim, or self-supplied digest is trusted.
The caller may pass a loader-admitted document, but must also supply expected.
"""
from artifacts import Artifact
from checker import verify

def adapt(document, expected):
    n=document['n_vars']; scope=tuple(document['variable_order'])
    p=document['payload']; kind=document['kind']
    left=tuple(document['row_variables']); right=tuple(document['column_variables'])
    if scope!=tuple(range(n)): raise ValueError('legacy variable contract')
    if kind=='xor_components':
        a=Artifact('xor',scope,(p['constant'],tuple((tuple(f['variables']),int(f['bits_hex'],16)) for f in p['factors'])))
    elif kind=='gf2_rank':
        a=Artifact('rank',scope,(left,right,tuple(p['row_coefficients']),tuple(p['basis_rows'])))
    elif kind=='cofactor_blocks':
        if p['orientation']=='columns': left,right=right,left
        elif p['orientation']!='rows': raise ValueError('orientation')
        a=Artifact('cofactor',scope,(left,right,tuple(p['representatives']),tuple(tuple(x) for x in p['references'])))
    elif kind=='kronecker':
        lr,lc=p['left_shape']; rr,rc=p['right_shape']
        if any(x<1 or x&(x-1) for x in (lr,lc,rr,rc)): raise ValueError('nonbinary shape')
        nr,nc=lr.bit_length()-1,lc.bit_length()-1
        avars=left[:nr]+right[:nc]; bvars=left[nr:]+right[nc:]
        a=Artifact('product',scope,(((avars,p['left_bits']),(bvars,p['right_bits'])),))
    else: raise ValueError('legacy kind')
    if not verify(a,expected): raise ValueError('external source mismatch / malformed payload')
    return a
