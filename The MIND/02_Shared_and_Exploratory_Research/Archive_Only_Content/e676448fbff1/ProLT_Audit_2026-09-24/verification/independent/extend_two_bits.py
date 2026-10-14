"""Exhaustive extension to five naturally labelled points, height <= 2.
Checks ranks over F2,F3,F5 and actual free-face collapse; no source-verifier imports.
"""
from audit_checks import *
import argparse

def main(n=5):
    if n not in (5,6): raise ValueError("Only documented n=5,6 runs are supported")
    started=time.time()
    counts={'n':n,'posets':0,'profiles':0,'F2_neutral':0,'F3_neutral':0,'F5_neutral':0,
            'neutral_but_not_direct_collapse':0,'coefficient_differences':0,'destructive':0}
    examples=[]
    for p in natural_posets(n,2):
        counts['posets']+=1
        pc=cells(n,p);pe=pc[1] if len(pc)>1 else[];pt=pc[2] if len(pc)>2 else[]
        safe={}
        for bs in it.product(range(2),repeat=n):
            safe[bs]=not any(relative_betti(n,p,thin(n,p,bs),2))
        for labels in it.product(range(4),repeat=n):
            q=thin(n,p,labels)
            de=[e for e in pe if e not in q]
            dt=[t for t in pt if any((t[i],t[j]) not in q for i,j in ((0,1),(0,2),(1,2))) ]
            b=matrix(de,dt)
            neutral={pr:len(de)==len(dt)==rank_mod(b,pr) for pr in (2,3,5)}
            counts['profiles']+=1
            for pr in (2,3,5):counts[f'F{pr}_neutral']+=neutral[pr]
            if len(set(neutral.values()))>1:counts['coefficient_differences']+=1
            if neutral[2] and not greedy_collapse(de,dt)[1]:
                counts['neutral_but_not_direct_collapse']+=1
                if len(examples)<10: examples.append({'P':sorted(p),'labels':labels})
            if not neutral[2] and all(safe[tuple((x>>bit)&1 for x in labels)] for bit in (0,1)):
                counts['destructive']+=1
    counts['seconds']=time.time()-started
    counts['examples']=examples
    dump(f'two_bit_n{n}_extension.json',counts)
    print(json.dumps(counts,indent=2))
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--n',type=int,default=5)
    main(parser.parse_args().n)
