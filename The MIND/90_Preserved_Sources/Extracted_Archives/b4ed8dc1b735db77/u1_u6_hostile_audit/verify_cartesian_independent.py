#!/usr/bin/env python3
from itertools import product, combinations
import json

U = tuple(range(4))

def all_partitions(seq):
    seq=list(seq)
    if not seq:
        yield []
        return
    first=seq[0]
    for rest in all_partitions(seq[1:]):
        yield [frozenset([first])] + rest
        for i in range(len(rest)):
            nr=list(rest)
            nr[i]=frozenset(set(nr[i])|{first})
            yield nr

def canon(part):
    return tuple(sorted((tuple(sorted(b)) for b in part), key=lambda b:(b[0],len(b),b)))

parts={canon(p) for p in all_partitions(U)}
parts=[tuple(frozenset(b) for b in p) for p in sorted(parts)]

def fine_partition(coarse, label):
    out=[]
    for C in coarse:
        for bit in (0,1):
            B=frozenset(x for x in C if label[x]==bit)
            if B: out.append(B)
    return tuple(out)

def union_of_blocks(E, part):
    E=set(E)
    return all((not (E & set(B))) or set(B)<=E for B in part)

def cartesian_label_condition(E, coarse, label):
    # For every surviving coarse cell, all fine labels realized in it before remain after.
    E=set(E)
    for C in coarse:
        if not (E & set(C)):
            continue
        before={label[x] for x in C}
        after={label[x] for x in C if x in E}
        if after != before:
            return False
    return True

cases=0
fine_cases=0
fail=0
counterexample_without_fine=None
for coarse in parts:
    for bits in product((0,1), repeat=4):
        label=dict(zip(U,bits))
        fine=fine_partition(coarse,label)
        for mask in range(16):
            E={x for x in U if (mask>>x)&1}
            cases+=1
            cart=cartesian_label_condition(E,coarse,label)
            coarse_meas=union_of_blocks(E,coarse)
            fine_meas=union_of_blocks(E,fine)
            if fine_meas:
                fine_cases+=1
                if cart != coarse_meas:
                    fail+=1
            elif cart and not coarse_meas and counterexample_without_fine is None:
                counterexample_without_fine={
                    'coarse':[sorted(B) for B in coarse],
                    'label':bits,
                    'fine':[sorted(B) for B in fine],
                    'event':sorted(E),
                    'cartesian':cart,
                    'coarse_measurable':coarse_meas,
                    'fine_measurable':fine_meas,
                }

out={'partitions':len(parts),'cases':cases,'fine_measurable_cases':fine_cases,'failures':fail,'counterexample_without_fine':counterexample_without_fine}
with open('/mnt/data/u1_u6_hostile_audit/CARTESIAN_INDEPENDENT_SUMMARY.json','w') as f: json.dump(out,f,indent=2)
print(json.dumps(out,indent=2))
