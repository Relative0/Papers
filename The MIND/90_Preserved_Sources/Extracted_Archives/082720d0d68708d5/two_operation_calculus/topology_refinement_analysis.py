#!/usr/bin/env python3
import csv,json,os
OUT=os.path.dirname(os.path.abspath(__file__))
FULL=15

def parse_opens(s):return frozenset(int(x) for x in s.split(';') if x!='')
def topo_generated(gens):
 t={0,FULL};t.update(gens);ch=True
 while ch:
  ch=False;cur=list(t)
  for a in cur:
   for b in cur:
    for c in (a|b,a&b):
     if c not in t:t.add(c);ch=True
 return frozenset(t)
def rel(t):
 return frozenset((x,y) for x in range(4) for y in range(4) if all(not((u>>x)&1) or ((u>>y)&1) for u in t))
def eq_partition(t):
 r=rel(t);seen=set();blocks=[]
 for x in range(4):
  if x in seen:continue
  b=frozenset(y for y in range(4) if (x,y) in r and (y,x) in r);seen|=b;blocks.append(b)
 return frozenset(blocks)
def t0(t):return len(eq_partition(t))==4
rows=[];counts={};t0counts={}
with open(os.path.join(OUT,'POSITIVE_TOPOLOGIES.csv')) as f:
 for rr in csv.DictReader(f):
  tid=int(rr['topology_id']);tau=parse_opens(rr['open_masks']);p=eq_partition(tau);src_t0=t0(tau)
  for e in range(16):
   q=topo_generated(list(tau)+[e]);p2=eq_partition(q)
   if q==tau:cl='redundant'
   elif p2!=p:cl='splits_indiscernibility_class'
   else:cl='same_carrier_order_thinning'
   counts[cl]=counts.get(cl,0)+1
   if src_t0:t0counts[cl]=t0counts.get(cl,0)+1
   rows.append({'source_topology_id':tid,'source_T0':src_t0,'event_id':e,'source_num_opens':len(tau),'target_num_opens':len(q),'class':cl,'source_partition_blocks':len(p),'target_partition_blocks':len(p2)})
with open(os.path.join(OUT,'TOPOLOGY_REFINEMENT_TRANSITIONS.csv'),'w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
out={'all_topology_refinement_transitions':len(rows),'class_counts':counts,'T0_source_transitions':sum(t0counts.values()),'T0_source_class_counts':t0counts}
with open(os.path.join(OUT,'TOPOLOGY_REFINEMENT_SUMMARY.json'),'w') as f:json.dump(out,f,indent=2)
print(json.dumps(out,indent=2))
