"""Minimize a finite-byte crossover exception by total dimension, then p,q,r,k.
Factor entries use the lexicographically least nonzero single-profile tables.
This is not a T3 answer-correctness counterexample.
"""
from common import *
from state import State
from comparators import Raw
def main():
    checked=0
    for n in range(2,9):
        for p in range(1,n):
            q=n-p
            for r in range(1,5):
                c=dict(n=n,p=p,q=q,r=r,left=list(range(p)),right=list(range(p,n)),U=[0]*((1<<p)-1)+[1],W=[0]*((1<<q)-1)+[1])
                for k in range(n+1):
                    vals=payloads(c,k);checked+=1
                    if not vals['dense_favorable']:continue
                    state=State(c,k,dense=True);dense=state.dumps();raw=Raw(c).dumps()
                    if len(dense)<len(raw):continue
                    write(ROOT/'results/MINIMIZED_MATCHED_BYTE_WITNESS.json',{'status':'FOUND','ordering':'n,p,q,r,k; nonempty blocks; r<=4 bounded search; least nonzero single-profile tables',
                      'checked_parameter_tuples':checked,'case':c,'k':k,'dense_payload_bits':vals['dense_row_bits'],'raw_factor_bits':vals['raw_factor_bits'],
                      'dense_bytes':len(dense),'raw_bytes':len(raw),'counts_equal':state.count()==oracle(c,{}),'scope':'finite serialized-byte crossover only'})
                    (ROOT/'results/minimal_dense_state.bin').write_bytes(dense);(ROOT/'results/minimal_raw_factors.bin').write_bytes(raw);return
    raise AssertionError('witness not found')
if __name__=='__main__':main()
