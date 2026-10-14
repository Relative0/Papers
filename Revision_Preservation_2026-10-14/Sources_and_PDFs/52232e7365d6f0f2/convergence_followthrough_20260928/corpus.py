"""Freeze and extract all primary outputs of the 20 original EPFL designs.

No best-results variants, generated local cuts, or transformed copies count as
independent designs. Structural support <=12 defines the admitted slice.
"""
from pathlib import Path
import argparse, collections, hashlib, json, shutil, time

ROOT=Path(__file__).resolve().parent
REVISION='0060e156826e733d69bf5b3322d1bdd0d03a1f9a'
SOURCE=ROOT.parent/'audit_p1_p13_20260918/p14_py0/epfl_snapshot'/('benchmarks-'+REVISION)

def sha(data):return hashlib.sha256(data).hexdigest()
def truth_hash(bits,n):return sha(n.to_bytes(4,'little')+bits.to_bytes(((1<<n)+7)//8,'little'))

def parse(path):
    lines=[];pending=''
    for line in path.read_text().splitlines():
        line=line.split('#',1)[0].strip()
        if not line:continue
        pending+=' '+line
        if pending.endswith('\\'):pending=pending[:-1];continue
        lines.append(pending.strip());pending=''
    if pending:raise ValueError('unterminated continuation')
    inputs=[];outputs=[];nodes={};i=0
    while i<len(lines):
        words=lines[i].split();i+=1
        if words[0]=='.inputs':inputs.extend(words[1:])
        elif words[0]=='.outputs':outputs.extend(words[1:])
        elif words[0]=='.names':
            deps=words[1:-1];name=words[-1];cubes=[];polarity=None
            while i<len(lines) and not lines[i].startswith('.'):
                w=lines[i].split();i+=1
                pattern,value=('',w[0]) if not deps else (w[0],w[1])
                if len(pattern)!=len(deps) or value not in ('0','1') or any(c not in '01-' for c in pattern):raise ValueError('invalid cube')
                if polarity is not None and polarity!=int(value):raise ValueError('mixed cube polarity')
                polarity=int(value);cubes.append(pattern)
            if name in nodes or name in inputs:raise ValueError('duplicate driver')
            nodes[name]=(deps,cubes,1 if polarity is None else polarity)
        elif words[0] not in ('.model','.end'):raise ValueError('unsupported BLIF directive '+words[0])
    support={v:frozenset([v]) for v in inputs};waiting={};indegree={};ready=collections.deque();order=[]
    drivers=set(nodes)|set(support)
    for name,(deps,cubes,pol) in nodes.items():
        used={deps[j] for cube in cubes for j,c in enumerate(cube) if c!='-'}
        if not used<=drivers:raise ValueError('undriven node')
        indegree[name]=sum(v not in support for v in used)
        for v in used:waiting.setdefault(v,[]).append(name)
        if not indegree[name]:ready.append(name)
    while ready:
        name=ready.popleft();deps,cubes,_=nodes[name]
        used={deps[j] for cube in cubes for j,c in enumerate(cube) if c!='-'}
        support[name]=frozenset().union(*(support[v] for v in used));order.append(name)
        for child in waiting.get(name,[]):
            indegree[child]-=1
            if not indegree[child]:ready.append(child)
    if len(order)!=len(nodes):raise ValueError('cyclic source')
    return inputs,outputs,nodes,support,order

def extract(path,output,parsed=None):
    _,_,nodes,support,order=parse(path) if parsed is None else parsed
    names=tuple(sorted(support[output]));n=len(names)
    if n>12:raise ValueError('support cap')
    full=(1<<(1<<n))-1
    values={v:sum(1<<a for a in range(1<<n) if (a>>(n-1-j))&1) for j,v in enumerate(names)}
    needed=set();stack=[output]
    while stack:
        name=stack.pop()
        if name in needed or name in values:continue
        needed.add(name);deps,cubes,_=nodes[name]
        stack.extend(deps[j] for cube in cubes for j,c in enumerate(cube) if c!='-')
    for name in order:
        if name not in needed:continue
        deps,cubes,pol=nodes[name];value=0
        for cube in cubes:
            term=full
            for dep,bit in zip(deps,cube):
                if bit!='-':term &= values[dep] if bit=='1' else full^values[dep]
            value |= term
        values[name]=value if pol else full^value
    return values[output],names

def cut_rank(bits,n,left):
    right=tuple(v for v in range(n) if v not in left);basis={}
    for a in range(1<<len(left)):
        row=0
        for b in range(1<<len(right)):
            x=sum(((a>>(len(left)-1-j))&1)<<(n-1-v) for j,v in enumerate(left))
            x|=sum(((b>>(len(right)-1-j))&1)<<(n-1-v) for j,v in enumerate(right))
            row |= ((bits>>x)&1)<<b
        while row:
            pivot=row.bit_length()-1
            if pivot in basis:row^=basis[pivot]
            else:basis[pivot]=row;break
    return len(basis)

def freeze(output):
    output.mkdir(parents=True,exist_ok=False)
    designs=[]
    for family in ('arithmetic','random_control'):
        paths=sorted((SOURCE/family).glob('*.blif'))
        held=set(p.stem for p in sorted(paths,key=lambda p:sha(('qk-corpus-v1:'+family+':'+p.stem).encode()))[:3])
        for p in paths:
            dest=output/'sources'/family/p.name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
            designs.append({'design':p.stem,'family':family,'source_path':dest.relative_to(output).as_posix(),
                'source_sha256':sha(p.read_bytes()),'upstream_revision':REVISION,
                'revision_basis':'existing pinned snapshot directory; content hashes authoritative',
                'upstream':'https://github.com/lsils/benchmarks','split':'holdout' if p.stem in held else 'development'})
    shutil.copy2(SOURCE/'LICENSE',output/'sources/LICENSE')
    config={'schema':'qk-corpus/v1','designs':designs,'eligibility':'all primary outputs; structural support 0..12; combinational .names BLIF',
        'cut_budget':2,'cuts':['balanced prefix','even coordinate indices'],
        'split_policy':'first three SHA256(qk-corpus-v1:family:design) per family held out before extraction',
        'holdout_limit':'prospective split for new study; same suite has appeared in earlier project work, not claimed historically unseen',
        'decomposition_quality_claim':False,'main_T3_campaign_enabled':False}
    (output/'PROTOCOL.json').write_text(json.dumps(config,indent=2))
    (output/'PROTOCOL.sha256').write_text(sha((output/'PROTOCOL.json').read_bytes())+'\n')
    print('Frozen',len(designs),'designs before output screening')

def screen(output):
    config=json.loads((output/'PROTOCOL.json').read_text());records=[];cases=[]
    if (output/'SCREEN.json').exists():raise FileExistsError('preserve prior screen')
    for d in config['designs']:
        path=output/d['source_path'];start=time.perf_counter_ns()
        try:
            parsed=parse(path)
            _,outputs,nodes,support,order=parsed
            parse_ns=time.perf_counter_ns()-start
        except Exception as exc:
            records.append({**d,'status':'unsupported_design','error':repr(exc)});continue
        for name in outputs:
            rec={**d,'output':name,'design_parse_ns':parse_ns,'status':'pending'}
            try:
                names=tuple(sorted(support[name]));n=len(names);rec['structural_support']=n
                if n>12:rec['status']='excluded_support_cap'
                else:
                    begin=time.perf_counter_ns();bits,actual_names=extract(path,name,parsed)
                    rec.update(status='success',source_extract_ns=time.perf_counter_ns()-begin,truth_sha256=truth_hash(bits,n))
                    assert names==actual_names
                    # Count semantically essential axes without changing the declared universe.
                    rec['semantic_support']=sum(any(((bits>>a)^(bits>>(a^(1<<(n-1-j)))))&1 for a in range(1<<n)) for j in range(n))
                    cuts=sorted({tuple(range(n//2)),tuple(range(0,n,2))})
                    for left in cuts:
                        cases.append({**rec,'case_id':f'{d["family"]}/{d["design"]}/{name}/'+','.join(map(str,left)),
                            'n':n,'p':len(left),'q':n-len(left),'left':left,'r':cut_rank(bits,n,left),
                            'truth_hex':hex(bits),'variable_names':names,'cut_order':list(left)+[j for j in range(n) if j not in left]})
            except Exception as exc:rec.update(status='failed',error=repr(exc))
            records.append(rec)
        print(d['design'],len(outputs),'outputs accounted',flush=True)
    (output/'SCREEN.json').write_text(json.dumps(records,indent=2))
    (output/'CASES.json').write_text(json.dumps(cases,indent=2))
    summary={'designs':len(config['designs']),'families':2,'outputs_or_design_errors':len(records),
        'statuses':dict(collections.Counter(r['status'] for r in records)),'admitted_designs':len({r['design'] for r in records if r['status']=='success'}),
        'cases_with_cuts':len(cases),'rank_incidence_by_design':{},'T3_favorable_parameter_incidence':'not defined; Theory pending'}
    for d in config['designs']:
        subset=[c for c in cases if c['design']==d['design']]
        summary['rank_incidence_by_design'][d['design']]={'family':d['family'],'split':d['split'],'admitted_cut_cases':len(subset),
            'rank_histogram':dict(collections.Counter(c['r'] for c in subset))}
    (output/'SUMMARY.json').write_text(json.dumps(summary,indent=2));print(json.dumps({k:v for k,v in summary.items() if k!='rank_incidence_by_design'},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['freeze','screen']);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();(freeze if a.mode=='freeze' else screen)(a.output)
