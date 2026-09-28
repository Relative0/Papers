from itertools import product, combinations, chain
from math import inf


def powerset(s):
    s=list(s)
    for r in range(len(s)+1):
        for c in combinations(s,r):
            yield frozenset(c)

def topology_from_subbasis(n, obs):
    X=frozenset(range(n))
    basis=[]
    for J in powerset(range(len(obs))):
        b=X
        for i in J:
            b=b & obs[i]
        basis.append(b)
    opens={frozenset()}
    # all unions of basis; deduplicate iteratively
    opens={frozenset()}
    for b in basis:
        opens |= {u|b for u in list(opens)}
    return opens

def sigs(n, obs):
    return [frozenset(i for i,O in enumerate(obs) if v in O) for v in range(n)]

def preorder_from_topology(n, opens):
    return {(v,w) for v in range(n) for w in range(n) if all((v not in U) or (w in U) for U in opens)}

def smallest_nbh(n, opens, v):
    X=frozenset(range(n))
    N=X
    for U in opens:
        if v in U: N &= U
    return N

def dplus(sv, sw, weights):
    return sum(weights[i] for i in sv-sw)

def dhamm(sv, sw, weights):
    return sum(weights[i] for i in sv^sw)

def ball_topology(n, sig, weights):
    vals={dplus(sig[v],sig[w],weights) for v in range(n) for w in range(n)}
    radii={0.5}
    # enough radii to realize strict-threshold balls
    for x in vals:
        radii.add(x+0.5)
        if x>0: radii.add(x/2)
    subs=[]
    for v in range(n):
        for r in radii:
            if r>0:
                subs.append(frozenset(w for w in range(n) if dplus(sig[v],sig[w],weights)<r))
    # generated topology
    opens={frozenset()}
    X=frozenset(range(n))
    # intersections of subbasis balls; but balls should already basis in quasi metric; brute generate topology by closure
    opens={frozenset(),X}
    changed=True
    subs=set(subs)|{frozenset(),X}
    opens |= subs
    while changed:
        changed=False
        cur=list(opens)
        for A in cur:
            for B in cur:
                for C in (A|B,A&B):
                    if C not in opens:
                        opens.add(C); changed=True
    return opens

def closure(n, opens, E):
    return frozenset(v for v in range(n) if all((v not in U) or bool(U&E) for U in opens))

def interior(opens,E):
    return frozenset().union(*(U for U in opens if U<=E)) if opens else frozenset()

checks=0
assignments=0
for n in range(1,5):
  for m in range(0,4):
    # observation memberships are arbitrary subsets of carrier
    all_subsets=list(powerset(range(n)))
    for obs_tuple in product(all_subsets, repeat=m):
        obs=[frozenset(o) for o in obs_tuple]
        assignments += 1
        opens=topology_from_subbasis(n,obs)
        sig=sigs(n,obs)
        pre=preorder_from_topology(n,opens)
        realized=set(sig)
        # Signature representation: opens exactly inverse images of upper sets of realized signatures
        upper_inv=set()
        rs=list(realized)
        for mask in range(1<<len(rs)):
            U={rs[j] for j in range(len(rs)) if mask>>j & 1}
            if all(not (s in U and s<=t) or t in U for s in realized for t in realized):
                upper_inv.add(frozenset(v for v,s in enumerate(sig) if s in U))
        assert upper_inv==opens
        checks+=1
        # indistinguishability
        for v in range(n):
          for w in range(n):
            sameopens=all((v in U)==(w in U) for U in opens)
            assert sameopens == (sig[v]==sig[w])
            assert ((v,w) in pre) == (sig[v] <= sig[w])
            checks+=2
        # smallest neighborhood formula
        for v in range(n):
            N=smallest_nbh(n,opens,v)
            expect=frozenset(w for w in range(n) if sig[v]<=sig[w])
            assert N==expect
            checks+=1
        # two-sided topology equals signature partition topology
        obs_pm=[]
        X=frozenset(range(n))
        for O in obs:
            obs_pm += [O, X-O]
        opens_pm=topology_from_subbasis(n,obs_pm)
        partition_opens={frozenset(v for v in range(n) if sig[v] in chosen)
                         for chosen in map(set,powerset(realized))}
        assert opens_pm==partition_opens
        checks+=1
        # T0/T1 criteria
        t0=all(v==w or any((v in U)!=(w in U) for U in opens) for v in range(n) for w in range(n))
        assert t0 == (len(set(sig))==n)
        t1=all(v==w or (any(v in U and w not in U for U in opens) and any(w in U and v not in U for U in opens)) for v in range(n) for w in range(n))
        antichain_inj=(len(set(sig))==n and all(v==w or (not sig[v]<=sig[w] and not sig[w]<=sig[v]) for v in range(n) for w in range(n)))
        assert t1==antichain_inj
        checks+=2
        # distances unit weights: pseudometric, zero, symmetrization, triangle, topology
        weights=[i+1 for i in range(m)]  # positive distinct weights
        for v in range(n):
          for w in range(n):
            dh=dhamm(sig[v],sig[w],weights)
            dp=dplus(sig[v],sig[w],weights)
            assert (dh==0)==(sig[v]==sig[w])
            assert (dp==0)==(sig[v]<=sig[w])
            assert dh==dp+dplus(sig[w],sig[v],weights)
            for u in range(n):
                assert dhamm(sig[v],sig[u],weights)<=dh+dhamm(sig[w],sig[u],weights)
                assert dplus(sig[v],sig[u],weights)<=dp+dplus(sig[w],sig[u],weights)
            checks+=5
        assert ball_topology(n,sig,weights)==opens
        checks+=1
        # interior/closure neighborhood formulas for all E
        for E in powerset(range(n)):
            Ei=interior(opens,E)
            Ec=closure(n,opens,E)
            Ei2=frozenset(v for v in range(n) if smallest_nbh(n,opens,v)<=E)
            Ec2=frozenset(v for v in range(n) if smallest_nbh(n,opens,v)&E)
            assert Ei==Ei2 and Ec==Ec2
            checks+=1

print(f'PASS: {checks:,} theorem/example checks across {assignments:,} arbitrary finite observation presentations (carrier size 1..4, observations 0..3).')
