#!/usr/bin/env python3
# Independent verifier of the closed-form construction and obstruction only.
import json, math, os
OUT=os.path.dirname(__file__)

def redundant(w): return all(a<=b for a,b in zip(w,w[1:]))
def defective(w):
    return bool(w and 0 in w and 1 in w and all(w[i]>=w[i+1] for i in range(len(w)-1)))
def neutral(w): return not defective(w)
def alt(n): return [i&1 for i in range(n)]
def depth(n):
    if n<=1:return 0
    if n==2:return 1
    w=alt(n)
    assert neutral(w) and not redundant(w)
    return 1+max(depth(w.count(0)),depth(w.count(1)))
checks=[]
for n in range(2,31):
    d=depth(n)
    checks.append({'n':n,'constructed_depth':d,'lower_bound':math.ceil(math.log2(n)),'ok':d==math.ceil(math.log2(n))})
# At n=2, the only informative words are 01 (redundant) and 10 (defective).
base_words=[[0,1],[1,0]]
base={'01_redundant':redundant(base_words[0]),'10_defective':defective(base_words[1])}
summary={'checks':checks,'base_case':base,'all_ok':all(x['ok'] for x in checks) and all(base.values())}
with open(os.path.join(OUT,'CHAIN_ADAPTIVE_INDEPENDENT.json'),'w') as f: json.dump(summary,f,indent=2)
print(json.dumps({'n_through':30,'all_ok':summary['all_ok'],'base':base},indent=2))
