#!/usr/bin/env python3
"""Exhaustive tests for the strict F_2[C4] models. No historical counts are inputs.
Encoding: bit k is the coefficient of g**k; CM rows are [[a0,a1],[a3,a2]].
Every candidate matrix is tested on ALL 256 states, not a random sample.
"""
from __future__ import annotations
import itertools, json, time
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'; OUT.mkdir(exist_ok=True)

def rmul(a:int,b:int)->int:
    out=0
    for i in range(4):
        for j in range(4):
            if ((a>>i)&1) and ((b>>j)&1): out ^= 1<<((i+j)%4)
    return out

def rotate(a:int,k:int=1)->int:
    return sum(((a>>j)&1)<<((j+k)%4) for j in range(4))

def main():
    start=time.monotonic()
    mul=np.array([[rmul(a,b) for b in range(16)] for a in range(16)],dtype=np.uint8)
    w=np.array([a.bit_count() for a in range(16)],dtype=np.int16)
    coeff=np.array([[(a>>j)&1 for j in range(4)] for a in range(16)],dtype=np.int16)
    corr=np.zeros((16,16,4),dtype=np.int16)
    for k in range(4): corr[:,:,k]=coeff @ np.roll(coeff,k,axis=1).T
    x=np.repeat(np.arange(16),16); y=np.tile(np.arange(16),16)
    W=w[x]+w[y]; shell=np.flatnonzero(W==4)
    selfc=corr[x,x]+corr[y,y]
    selfq=selfc[:,0]-selfc[:,2]
    mats=np.array(list(itertools.product(range(16),repeat=4)),dtype=np.uint8)
    masks={s:np.zeros(65536,dtype=bool) for s in
      ['weight','shell','profile','profile_shell','signed_self','signed_shell','invertible','involution','split_involution']}
    for lo in range(0,len(mats),1024):
        A,B,C,D=mats[lo:lo+1024].T
        u=mul[A[:,None],x]^mul[B[:,None],y]
        v=mul[C[:,None],x]^mul[D[:,None],y]
        acts=16*u.astype(np.int16)+v
        sl=slice(lo,lo+len(A))
        masks['weight'][sl]=(W[acts]==W).all(axis=1)
        masks['shell'][sl]=(W[acts[:,shell]]==4).all(axis=1)
        masks['profile'][sl]=(selfc[acts]==selfc).all(axis=(1,2))
        masks['profile_shell'][sl]=(selfc[acts[:,shell]]==selfc[shell]).all(axis=(1,2))
        masks['signed_self'][sl]=(selfq[acts]==selfq).all(axis=1)
        masks['signed_shell'][sl]=(selfq[acts[:,shell]]==selfq[shell]).all(axis=1)
        det=mul[A,D]^mul[B,C]
        masks['invertible'][sl]=(w[det]%2==1)
        inv=(mul[A,A]^mul[B,C]==1)&(mul[A,B]^mul[B,D]==0)&(mul[C,A]^mul[D,C]==0)&(mul[C,B]^mul[D,D]==1)
        masks['involution'][sl]=inv
        masks['split_involution'][sl]=inv&(mul[B,9]==9)&(mul[D,9]==9)
    def action(M):
        A,B,C,D=M
        return 16*(mul[A,x]^mul[B,y]).astype(np.int16)+(mul[C,x]^mul[D,y])
    fullc=corr[x[:,None],x[None,:]]+corr[y[:,None],y[None,:]]
    fullq=np.stack((fullc[:,:,0]-fullc[:,:,2],fullc[:,:,1]-fullc[:,:,3]),axis=2)
    inner=[]; qinner=[]
    for idx in np.flatnonzero(masks['profile']):
        act=action(mats[idx])
        if np.array_equal(fullc[act[:,None],act],fullc): inner.append(int(idx))
    probes=np.array([0,1,2,4,8,15,16,17,31,32,63,64,127,128,240,255])
    for idx in np.flatnonzero(masks['signed_self']):
        act=action(mats[idx])
        if not np.array_equal(fullq[act[probes,None],act[probes]],fullq[probes[:,None],probes]): continue
        if np.array_equal(fullq[act[:,None],act],fullq): qinner.append(int(idx))
    shell_ids=np.flatnonzero(masks['shell'])
    shell_actions={tuple(action(mats[i])[shell]) for i in shell_ids}
    kernel=[int(i) for i in shell_ids if np.array_equal(action(mats[i])[shell],shell)]
    expected=set()
    for a,b in itertools.product([1,2,4,8],repeat=2):
        expected.add((a,0,0,b)); expected.add((0,a,b,0))
    assert {tuple(map(int,M)) for M in mats[masks['weight']]}==expected
    # phase responses in branch order (|1>,|0>)
    seq_counts={}
    phase_acts=[]
    for g in (1,2,4,8): phase_acts.append(16*mul[g,x[shell]].astype(np.int16)+y[shell])
    fringe=[]
    targets=set()
    for base in [(0,2,4,2),(4,2,0,2)]:
        for k in range(4): targets.add(base[k:]+base[:k])
    for i in shell_ids:
        act=action(mats[i]); seq=np.stack([w[act[p]//16] for p in phase_acts],axis=1)
        for j,row in enumerate(seq):
            t=tuple(map(int,row)); seq_counts[t]=seq_counts.get(t,0)+1
            if t in targets: fringe.append((int(i),int(shell[j])))
    # All 1024 interference combinations and orbits.
    tables={str(k):[[a^rotate(b,k) for b in range(16)] for a in range(16)] for k in range(4)}
    orbits=[]; seen=set()
    for a in range(16):
        if a in seen: continue
        orbit=[]; b=a
        while b not in orbit: orbit.append(b); seen.add(b); b=rotate(b)
        orbits.append(orbit)
    # Matrices in the proposed ring-valued Bell state, order 11,10,01,00.
    target=(6,0,0,9)
    factorizations=[]
    for a,b,c,d in itertools.product(range(16),repeat=4):
        if (rmul(a,c),rmul(a,d),rmul(b,c),rmul(b,d))==target: factorizations.append([a,b,c,d])
    # Checks independent of the exhaustive candidate search.
    P=np.roll(np.eye(4,dtype=int),1,axis=0)
    Q=np.array([[1,0,-1,0],[0,1,0,-1]])
    J=np.array([[0,-1],[1,0]])
    assert np.array_equal(Q@P,J@Q)
    assert np.array_equal(Q.T@Q,np.eye(4,dtype=int)-P@P)
    for a,b in itertools.product(range(16),repeat=2):
        assert w[a^b]==w[a]+w[b]-2*w[a&b]
        assert np.array_equal(Q@coeff[a^b],Q@coeff[a]+Q@coeff[b]-2*(Q@coeff[a&b]))
        for k in range(4):
            assert corr[a,b,k]==w[a&rotate(b,k)]
    popcount_ok=True
    for a in range(16):
        bits=coeff[a]; q0=int(bits.sum())%2
        q1=sum(int(bits[i]*bits[j]) for i in range(4) for j in range(i+1,4))%2
        q2=int(np.prod(bits)); popcount_ok &= (q0+2*q1+4*q2==w[a])
    summary={k:int(v.sum()) for k,v in masks.items()}
    summary.update({
        'operators_tested':65536,'states_tested_per_operator':256,'normalized_shell_size':len(shell),
        'full_integer_correlation':len(inner),'full_signed_correlation':len(qinner),
        'shell_invertible':int((masks['shell']&masks['invertible']).sum()),
        'shell_involutions':int((masks['shell']&masks['involution']).sum()),
        'distinct_shell_actions':len(shell_actions),'shell_action_kernel':len(kernel),
        'shell_exact_fringe_hits':len(fringe),
        'profile_shell_equals_weight_shell':bool(np.array_equal(masks['profile_shell'],masks['shell'])),
        'K_preserves_shell':bool(masks['shell'][list(map(tuple,mats)).index((1,5,5,1))]),
        'ring_Bell_factorizations':len(factorizations),
        'popcount_boolean_formula':bool(popcount_ok),
        'rotation_orbits':orbits,
        'phase_response_counts':{','.join(map(str,k)):v for k,v in sorted(seq_counts.items())},
        'elapsed_seconds':round(time.monotonic()-start,3),
    })
    for name in masks: summary[name+'_operators']=[list(map(int,M)) for M in mats[masks[name]]] if name in ('weight','split_involution') else None
    (OUT/'finite_summary.json').write_text(json.dumps(summary,indent=2))
    (OUT/'interference_tables.json').write_text(json.dumps({'encoding':'bit k = g^k; CM [[a0,a1],[a3,a2]]','tables':tables},indent=2))
    np.savez_compressed(OUT/'finite_classification.npz',operators=mats,**masks,
                       full_correlation=np.array(inner),full_signed_correlation=np.array(qinner))
    print(json.dumps({k:v for k,v in summary.items() if not k.endswith('_operators')},indent=2))

if __name__=='__main__': main()
