#!/usr/bin/env python3
import json,sys,itertools
sys.path.insert(0,'/mnt/data/phase5_work/structured_factorization_phase4/code')
import sdd_direct_extraction as sdd

def all_equal_bits(n):
    return (1<<0) | (1<<((1<<n)-1))

def two_var_rank2_slice(bits,n,x,y,fix):
    vals=[]
    for xv in (0,1):
      row=[]
      for yv in (0,1):
        a=0
        for v,val in fix.items(): a|=(val<<v)
        a|=xv<<x; a|=yv<<y
        row.append((bits>>a)&1)
      vals.append(row)
    det=(vals[0][0]&vals[1][1]) ^ (vals[0][1]&vals[1][0])
    return bool(det),vals

def pairwise_edges(bits,n):
    edges=[]
    for x in range(n):
      for y in range(x+1,n):
        rest=[v for v in range(n) if v not in (x,y)]
        found=False
        for z in range(1<<len(rest)):
          fix={v:(z>>i)&1 for i,v in enumerate(rest)}
          ok,_=two_var_rank2_slice(bits,n,x,y,fix)
          if ok:found=True;break
        if found:edges.append((x,y))
    return edges

def min_witness_support_for_cut(bits,n,A):
    A=sorted(A);B=[v for v in range(n) if v not in A]
    best=None; witness=None
    for a0 in range(1<<len(A)):
      for a1 in range(1<<len(A)):
        if a0==a1:continue
        da=(a0^a1).bit_count()
        for b0 in range(1<<len(B)):
          for b1 in range(1<<len(B)):
            if b0==b1:continue
            db=(b0^b1).bit_count()
            def idx(aa,bb):
              z=0
              for i,v in enumerate(A):z|=((aa>>i)&1)<<v
              for j,v in enumerate(B):z|=((bb>>j)&1)<<v
              return z
            c00=(bits>>idx(a0,b0))&1;c01=(bits>>idx(a0,b1))&1;c10=(bits>>idx(a1,b0))&1;c11=(bits>>idx(a1,b1))&1
            det=(c00&c11)^(c01&c10)
            if det:
              supp=da+db
              if best is None or supp<best:
                best=supp;witness={'a0':a0,'a1':a1,'b0':b0,'b1':b1,'support_A':da,'support_B':db,'corners':[c00,c01,c10,c11]}
    return best,witness

def run():
    out=[]
    for n in range(3,7):
      bits=all_equal_bits(n); full=sdd.full_prime_partition(bits,n); edges=pairwise_edges(bits,n)
      A=set(range(n//2)); best,w=min_witness_support_for_cut(bits,n,A)
      out.append({'n':n,'truth_support':['0'*n,'1'*n],'prime_partition':full,'pairwise_rank2_edges':edges,
                  'balanced_cut_A':sorted(A),'min_four_corner_support':best,'min_witness':w})
    json.dump(out,open('/mnt/data/phase5_output/data/defect_localization_counterexamples.json','w'),indent=2)
    print(json.dumps(out,indent=2))
if __name__=='__main__':run()
