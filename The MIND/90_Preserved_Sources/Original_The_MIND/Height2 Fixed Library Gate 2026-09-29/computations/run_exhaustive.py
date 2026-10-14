"""Exhaustive reproducible finite audit. Python standard library only.

Natural labels mean every strict pair is i<j as integers. This covers every
isomorphism class (often repeatedly), not every labelled order. Height counts
strict comparisons. Fixed libraries contain arbitrary oriented Boolean tests;
constants are omitted because they cannot affect identification depth.
"""
import csv, json, math, random, time
from collections import Counter
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import repair_graph
import boundary_matrix

HERE=Path(__file__).resolve().parent
INF=99
START=time.time()

def log(message):
    line=f'[{time.time()-START:.2f}s] {message}'
    print(line,flush=True)
    with (HERE/'run.log').open('a',encoding='utf-8') as f:f.write(line+'\n')

def csv_writer(name, fields):
    f=(HERE/name).open('w',newline='',encoding='utf-8')
    w=csv.writer(f);w.writerow(fields)
    return f,w

def posets(n):
    possible=list(combinations(range(n),2))
    for mask in range(1<<len(possible)):
        pairs=tuple(e for i,e in enumerate(possible) if mask>>i&1)
        relation=set(pairs)
        if any((a,b) in relation and (b,c) in relation and (a,c) not in relation
               for a,b,c in combinations(range(n),3)):
            continue
        levels=[0]*n
        for a,b in pairs:levels[b]=max(levels[b],levels[a]+1)
        height=max(levels,default=0)
        if height<=2:yield mask,pairs,height

def project_label(q,T):
    out=0;i=0
    while T:
        bit=T&-T;T-=bit
        if q&bit:out|=1<<i
        i+=1
    return out

ORDERS={}
SAFETY={}
INDUCED={}
TRANSITION_COUNTS={}
EXAMPLES={}
SUMMARY={'conventions':{'labels':'0,...,n-1; natural labels only',
    'height':'number of strict comparisons in a longest chain',
    'queries':'integer q; bit i is the value at state i; orientations retained',
    'libraries':'integer L; bit q-1 includes nonconstant query q',
    'infinity':INF},'posets':{},'safety':{},'transitions':{},'libraries':{}}

def setup():
    fp,wp=csv_writer('HEIGHT2_POSETS.csv',['n','relation_mask','height','strict_pairs','coarse_components'])
    fq,wq=csv_writer('QUERY_REPAIR_SAFETY.csv',['n','relation_mask','query_mask','graph_safe','matrix_safe','deleted_edges','deleted_triangles','matrix_rank','nonredundant'])
    for n in range(1,7):
        counts=Counter()
        for rel,pairs,height in posets(n):
            ORDERS[n,rel]=(pairs,height)
            safety=[]
            for q in range(1<<n):
                a=repair_graph.analyze(n,pairs,q)
                b=boundary_matrix.analyze(n,pairs,q)
                assert a[:3]==b[:3],(n,rel,q,a,b)
                safety.append(a[0])
                wq.writerow([n,rel,q,int(a[0]),int(b[0]),a[1],a[2],b[3],int(bool(a[1]))])
                counts['queries']+=1
                counts['safe']+=a[0]
                counts['nonredundant_safe']+=a[0] and a[1]>0
                counts['height_exact2_nonredundant_safe']+=height==2 and a[0] and a[1]>0
                counts['height_exact2_queries']+=(height==2)
            SAFETY[n,rel]=tuple(safety)
            counts['posets']+=1;counts[f'height_{height}']+=1
            wp.writerow([n,rel,height,';'.join(f'{a}<{b}' for a,b in pairs),a[3]])
        SUMMARY['posets'][n]=dict(counts)
        log(f'n={n}: {dict(counts)}; graph/matrix mismatches=0')
    fp.close();fq.close()
    # Canonical induced orders preserve the inherited natural label order.
    for (n,rel),(pairs,height) in ORDERS.items():
        for T in range(1,1<<n):
            states=[i for i in range(n) if T>>i&1]
            possible=list(combinations(states,2))
            relation=set(pairs)
            induced_mask=sum(1<<i for i,e in enumerate(possible) if e in relation)
            INDUCED[n,rel,T]=(len(states),induced_mask)

def safe_on(n,rel,T,q):
    ns,rs=INDUCED[n,rel,T]
    return SAFETY[ns,rs][project_label(q,T)]

def transitions():
    f,w=csv_writer('SAFETY_TRANSITIONS.csv',['n','relation_mask','query_mask','all_support_SS','all_support_SU','all_support_US','all_support_UU','legal_conditioning_SS','legal_conditioning_SU','legal_conditioning_US','legal_conditioning_UU'])
    aggregate=Counter()
    for (n,rel),(pairs,height) in ORDERS.items():
        full=(1<<n)-1
        safe=SAFETY[n,rel]
        # Pair masks record oriented legal q -> informative r transitions.
        pair_masks={q:{'US':0,'SU':0} for q in range(1,full) if safe[q]}
        for r in range(1,full):
            cnt=Counter()
            for T in range(1,full):
                if not (r&T) or (r&T)==T:continue
                after=safe_on(n,rel,T,r)
                kind=('S' if safe[r] else 'U')+('S' if after else 'U')
                cnt['all_'+kind]+=1
                if kind in ('US','SU'):
                    EXAMPLES.setdefault('arbitrary_'+kind,{'n':n,'relation_mask':rel,'pairs':pairs,'r':r,'T':T,'height':height})
            for q in pair_masks:
                if q==r:continue
                for outcome,T in ((0,full^q),(1,q)):
                    if not (r&T) or (r&T)==T:continue
                    after=safe_on(n,rel,T,r)
                    kind=('S' if safe[r] else 'U')+('S' if after else 'U')
                    cnt['legal_'+kind]+=1
                    if kind in ('US','SU'):
                        pair_masks[q][kind]|=1<<(r-1)
                        EXAMPLES.setdefault('legal_'+kind,{'n':n,'relation_mask':rel,'pairs':pairs,'r':r,'conditioning_q':q,'outcome':outcome,'T':T,'height':height})
            keys=[prefix+kind for prefix in ('all_','legal_') for kind in ('SS','SU','US','UU')]
            w.writerow([n,rel,r]+[cnt[k] for k in keys])
            aggregate.update({f'n{n}_{k}':v for k,v in cnt.items()})
        if n<=4:TRANSITION_COUNTS[n,rel]=pair_masks
        if rel==0:log(f'transitions reached n={n}')
    f.close()
    SUMMARY['transitions']=dict(aggregate)
    log('All support / legal one-step informative-query transitions enumerated')
    (HERE/'MINIMAL_EXAMPLES.json').write_text(json.dumps(EXAMPLES,indent=2),encoding='utf-8')

@lru_cache(None)
def project_library(n,T,library):
    ns=T.bit_count();full=(1<<ns)-1
    result=0
    while library:
        bit=library&-library;library-=bit
        q=bit.bit_length()
        qp=project_label(q,T)
        if qp not in (0,full):result|=1<<(qp-1)
    return result

@lru_cache(None)
def solve(n,rel,library,rf):
    if n<=1:return 0
    full=(1<<n)-1
    lower=(n-1).bit_length()
    best=INF
    queries=library
    while queries:
        bit=queries&-queries;queries-=bit
        q=bit.bit_length()
        if rf and not SAFETY[n,rel][q]:continue
        worst=0
        for T in (full^q,q):
            ns,rs=INDUCED[n,rel,T]
            childlib=project_library(n,T,library)
            child=solve(ns,rs if rf else 0,childlib,rf)
            worst=max(worst,child)
            if 1+worst>=best:break
        best=min(best,min(INF,1+worst))
        if best==lower:break
    return best

def protocol(n,rel,library,rf,original_states=None):
    if original_states is None:original_states=list(range(n))
    if n<=1:return {'states':original_states}
    depth=solve(n,rel,library,rf)
    if depth==INF:return {'states':original_states,'impossible':True}
    queries=library;full=(1<<n)-1
    while queries:
        bit=queries&-queries;queries-=bit;q=bit.bit_length()
        if rf and not SAFETY[n,rel][q]:continue
        children=[]
        for T in (full^q,q):
            ns,rs=INDUCED[n,rel,T]
            L=project_library(n,T,library)
            children.append((ns,rs if rf else 0,L,T))
        if 1+max(solve(ns,rs,L,rf) for ns,rs,L,T in children)!=depth:continue
        return {'states':original_states,'query_on_states':q,'depth':depth,'children':[
            protocol(ns,rs,L,rf,[original_states[i] for i in range(n) if T>>i&1])
            for ns,rs,L,T in children]}
    raise AssertionError('No optimal protocol found')

def independent_tree_feasible(n,pairs,queries,depth,rf):
    """No DP/cache, no graph safety, original fixed queries on support masks."""
    def visit(states,budget):
        if len(states)<=1:return True
        if budget==0 or len(states)>1<<budget:return False
        induced_pairs=tuple((i,j) for i,a in enumerate(states) for j,b in enumerate(states) if (a,b) in pairs)
        for q in queries:
            left=[s for s in states if not(q>>s&1)]
            right=[s for s in states if q>>s&1]
            if not left or not right:continue
            qp=sum((q>>s&1)<<i for i,s in enumerate(states))
            if rf and not boundary_matrix.analyze(len(states),induced_pairs,qp)[0]:continue
            if visit(left,budget-1) and visit(right,budget-1):return True
        return False
    return visit(list(range(n)),depth)

def libraries():
    f,w=csv_writer('FIXED_LIBRARY_RESULTS.csv',['n','relation_mask','library_mask','query_count','ordinary_depth','repair_safe_depth','finite_penalty','legal_root_queries','activation_pairs','deactivation_pairs','sampling'])
    fg,wg=csv_writer('REPAIR_SAFETY_GAPS.csv',['n','relation_mask','library_mask','ordinary_depth','repair_safe_depth','finite_penalty','kind'])
    depths=Counter();examples={};verified=0
    rng=random.Random(20260929)
    for (n,rel),(pairs,height) in ORDERS.items():
        if n>4:continue
        universe=(1<<n)-2
        safemask=sum(1<<(q-1) for q in range(1,(1<<n)-1) if SAFETY[n,rel][q])
        for L in range(1<<universe):
            ad=solve(n,0,L,False);rf=solve(n,rel,L,True)
            assert rf>=ad
            penalty=rf-ad if rf<INF else ''
            ac=dc=0
            for q,pm in TRANSITION_COUNTS[n,rel].items():
                if L>>(q-1)&1:
                    ac+=(L&pm['US']).bit_count();dc+=(L&pm['SU']).bit_count()
            w.writerow([n,rel,L,L.bit_count(),ad,rf,penalty,(L&safemask).bit_count(),ac,dc,'exhaustive'])
            depths[n,ad,rf,'exhaustive']+=1
            kind='impossible' if ad<INF==rf else 'strict_finite' if ad<rf<INF else None
            if kind:
                wg.writerow([n,rel,L,ad,rf,penalty,kind])
                key=(kind,n)
                if key not in examples or L.bit_count()<examples[key]['query_count']:
                    examples[key]={'n':n,'relation_mask':rel,'pairs':pairs,'library_mask':L,'query_count':L.bit_count(),'queries':[q for q in range(1,1<<n) if L>>(q-1)&1], 'd_ad':ad,'d_rf':rf}
            if n<=3 or (n==4 and rng.random()<0.002):
                queries=[q for q in range(1,1<<n) if L>>(q-1)&1]
                for isrf,d in ((False,ad),(True,rf)):
                    expected=d if d<INF else n
                    if expected>0:assert not independent_tree_feasible(n,pairs,queries,expected-1,isrf)
                    if d<INF:assert independent_tree_feasible(n,pairs,queries,d,isrf)
                verified+=1
        log(f'libraries n={n} rel={rel}: {1<<universe} exhaustive')
    # Restricted random reconnaissance on n=5,6: bounded, seeded, explicit.
    for n in (5,6):
        orderkeys=[key for key in ORDERS if key[0]==n]
        chosen=orderkeys if n==5 else rng.sample(orderkeys,200)
        for _,rel in chosen:
            pairs,height=ORDERS[n,rel]
            full=(1<<n)-1
            for trial in range(20):
                queries=rng.sample(range(1,full),rng.randint((n-1).bit_length(),min(10,full-1)))
                L=sum(1<<(q-1) for q in queries)
                ad=solve(n,0,L,False);rf=solve(n,rel,L,True)
                penalty=rf-ad if rf<INF else ''
                safemask=sum(1<<(q-1) for q in queries if SAFETY[n,rel][q])
                w.writerow([n,rel,L,len(queries),ad,rf,penalty,safemask.bit_count(),'not_counted','not_counted','seeded_random'])
                depths[n,ad,rf,'seeded_random']+=1
                kind='impossible' if ad<INF==rf else 'strict_finite' if ad<rf<INF else None
                if kind:
                    wg.writerow([n,rel,L,ad,rf,penalty,kind])
                    examples.setdefault((kind,n),{'n':n,'relation_mask':rel,'pairs':pairs,'library_mask':L,'query_count':len(queries),'queries':queries,'d_ad':ad,'d_rf':rf})
        log(f'seeded libraries n={n}: {len(chosen)*20}')
    f.close();fg.close()
    fd,wd=csv_writer('ADAPTIVE_DEPTHS.csv',['n','ordinary_depth','repair_safe_depth','sampling','case_count'])
    for key,count in sorted(depths.items()):wd.writerow([*key,count])
    fd.close()
    output=[]
    for (kind,n),case in sorted(examples.items()):
        case['kind']=kind
        case['ordinary_protocol']=protocol(n,0,case['library_mask'],False)
        case['repair_safe_protocol']=protocol(n,case['relation_mask'],case['library_mask'],True)
        output.append(case)
    (HERE/'OPTIMAL_PROTOCOLS.json').write_text(json.dumps(output,indent=2),encoding='utf-8')
    SUMMARY['libraries']={'depth_distribution':[{**dict(zip(('n','ordinary_depth','repair_safe_depth','sampling'),key)),'count':count} for key,count in sorted(depths.items())], 'independent_tree_cases':verified,'dp_cache':str(solve.cache_info()),'seed':20260929}
    log(f'Independent uncached matrix/tree verification: {verified} library instances; mismatches=0')

if __name__=='__main__':
    (HERE/'run.log').write_text('',encoding='utf-8')
    setup();transitions()
    # Save transition examples before the longer library run.
    (HERE/'SUMMARY.json').write_text(json.dumps(SUMMARY,indent=2),encoding='utf-8')
    libraries()
    SUMMARY['elapsed_seconds']=time.time()-START
    (HERE/'SUMMARY.json').write_text(json.dumps(SUMMARY,indent=2),encoding='utf-8')
    log('COMPLETE')
