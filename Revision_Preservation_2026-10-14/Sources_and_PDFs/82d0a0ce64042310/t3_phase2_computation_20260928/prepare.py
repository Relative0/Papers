"""Freeze selection and analysis rules before producing new T3 experiment outcomes."""
from common import *
import random,shutil

def freeze():
    protocol={
      'version':'T3-C2-20260928-v1','theory_sha256':sha((ROOT/'THEORY_PHASE2_T1_T3_HANDOFF_2026-09-28.zip').read_bytes()),
      'contract':'supplied fixed-cut factors; named MSB coordinates; source-discarded T3; cumulative distinct updates; COUNT at every prefix',
      'primary_storage_prediction':'(2**r-1)*((p+1)*D(p,k)+(q+2)*D(q,k)) < r*(2**p+2**q)',
      'prediction_decision':'Check fixed-width dense counter payload exactly, and independently check whether the same inequality predicts actual full serialized byte crossover. Metadata exceptions falsify the unqualified byte criterion, not T3 correctness or asymptotic bound.',
      'sparse_and_orientation':'secondary descriptive analyses only; never redefine dense criterion',
      'depths':[0,1,2,4,'n'],'depth_rule':'cap at n and deduplicate',
      'batches':[1,8,64,256],'batch_semantics':'actual repeated COUNT calls at initial state and after each of k legal distinct-coordinate updates; no reset horizon',
      'repetitions':2,'seed':20260928,'method_order':'seeded shuffled method order per case, k, mode, batch and repetition',
      'methods':['t3_dense_row','t3_sparse_row','t3_sparse_column','t3_adaptive','raw_factor','draft3_histogram','packed_native','cudd_native'],
      'natural_incidence':'all 2119 previous cut cases, all capped depth strata, all 20 source designs retained including excluded outputs',
      'natural_timing_selection':'one case per admitted design: largest n, tie broken by SHA256(case_id); no selection using favorable outcome',
      'synthetic':'balanced m=2,4,6,8,10; rank-one rectangles and rank-two complementary parity; random supplied widths 2,4 at m=4,8; zero, one, and width-inflated cancellation controls',
      'modes':['warm_persistent','fresh_object_reload','fresh_process_verified_page_cold'],
      'fresh_process_panel':'all selected natural cases and synthetic m=8 cases; k=min(2,n), batch=64, one trial per method; other cells use two in-process repetitions',
      'counter_allocation_cap':200000,'dense_rank_cap':12,'trial_timeout_seconds':60,
      'supported_limits':'n<=20 for packed truth construction; C++ exact uint64 counting rejects n>62; T3 arbitrary Python integers, measured bounded cases',
      'correctness':'exact direct factor oracle at every tested prefix; exhaustive all legal paths on small artifacts; residual binary round trips and source poisoning',
      'cold_policy':'stage serialized file on Linux local /tmp filesystem; fsync and POSIX_FADV_DONTNEED; mincore before read must show zero resident pages; physical device cache not claimed cold',
      'failure_policy':'retain all unsupported, failures, timeouts; no imputed times; no automatic favorable replacement',
      'analysis_unit':'design; synthetic families separate; descriptive paired medians only; no novelty claim',
      'lifecycle':'each measured trial includes actual construction, verification, serialization, load when applicable, indexing, updates and all executed counts; cold consumers add producer costs and parent wall time separately',
      'build_algorithm':'per-profile superset zeta transform; measured cost, different construction schedule from Theory Walsh construction; exact same persistent moments',
      'compiled_comparator':'CUDD via dd 0.6.0 builds and sifts a BDD from factor bit functions; C++17 -O3 exact memoized residual-count kernel with cached repeated counts; no floating point counting',
      'decomposition_claim':'none; supplied factors fixed; CUDD sifting time charged; no cross-method cut-quality superiority claim',
    }
    dest=ROOT/'PROTOCOL.json'
    if dest.exists():raise FileExistsError(dest)
    write(dest,protocol);(ROOT/'PROTOCOL.sha256').write_text(sha(dest.read_bytes())+'\n')

def prepare():
    assert sha((ROOT/'PROTOCOL.json').read_bytes())==(ROOT/'PROTOCOL.sha256').read_text().strip()
    sys.path.insert(0,str(PRIOR/'inputs/baseline/CM_COMPUTATION_BASELINE_HANDOFF/reproducibility/code'))
    from artifacts import matrix_rows,rank_factor
    rows=json.loads((PRIOR/'corpus_v1/CASES.json').read_text());cases=[];incidence=[]
    for old in rows:
        bits=int(old['truth_hex'],16);m,right=matrix_rows(bits,tuple(range(old['n'])),tuple(old['left']));u,basis=rank_factor(m)
        c={key:old[key] for key in ('case_id','design','family','split','n','p','q','left','source_path','source_sha256','upstream_revision','output','variable_names','truth_sha256')}
        c.update(right=list(right),r=len(basis),actual_rank=len(basis),U=list(u),W=[sum(((v>>y)&1)<<i for i,v in enumerate(basis)) for y in range(1<<old['q'])],kind='natural')
        assert c['r']==old['r'];c['factor_sha256']=sha(factor_bytes(c));cases.append(c)
        for k in sorted({min(c['n'],v) for v in [0,1,2,4,c['n']]}):incidence.append({'case_id':c['case_id'],'design':c['design'],'family':c['family'],'split':c['split'],'n':c['n'],'p':c['p'],'q':c['q'],'r':c['r'],'actual_rank':c['actual_rank'],'k':k,**payloads(c,k)})
    chosen=[]
    for design in sorted({x['design'] for x in cases}):chosen.append(sorted([x for x in cases if x['design']==design],key=lambda c:(-c['n'],sha(c['case_id'].encode())))[0])
    rng=random.Random(20260928)
    def add(name,p,q,r,u,w,family):
        c=dict(case_id=name,design=name,family=family,kind='synthetic',split='synthetic',n=p+q,p=p,q=q,r=r,left=list(range(p)),right=list(range(p,p+q)),U=u,W=w)
        c['actual_rank']=actual_rank(u,w);c['factor_sha256']=sha(factor_bytes(c));chosen.append(c)
    for m in [2,4,6,8,10]:
        add(f'rectangle_m{m}',m,m,1,[int(x%3==1) for x in range(1<<m)],[int(y%5<2) for y in range(1<<m)],'rank_one_rectangles')
        add(f'parity_m{m}',m,m,2,[1 if x.bit_count()%2 else 2 for x in range(1<<m)],[2 if y.bit_count()%2 else 1 for y in range(1<<m)],'rank_two_complementary_parity')
    for m in [4,8]:
        for r in [2,4]:add(f'random_m{m}_r{r}',m,m,r,[rng.randrange(1<<r) for _ in range(1<<m)],[rng.randrange(1<<r) for _ in range(1<<m)],'increasing_rank')
    add('zero_width0',2,3,0,[0]*4,[0]*8,'edge');add('constant_one',2,3,1,[1]*4,[1]*8,'edge')
    add('inflated_width_cancel',2,3,3,[7]*4,[3]*8,'edge')
    write(ROOT/'inputs/NATURAL_FACTORS.json',cases);write(ROOT/'inputs/TIMING_CASES.json',chosen)
    write(ROOT/'results/NATURAL_INCIDENCE.json',incidence)
    write(ROOT/'inputs/IDENTITY.json',{'protocol_sha256':sha((ROOT/'PROTOCOL.json').read_bytes()),'natural_cases':len(cases),'timing_cases':len(chosen),'files':{p.name:sha(p.read_bytes()) for p in (ROOT/'inputs').glob('*.json')}})
    print(json.dumps({'natural':len(cases),'timing':len(chosen),'incidence_rows':len(incidence)}))
if __name__=='__main__':
    if sys.argv[1]=='freeze':freeze()
    else:prepare()
