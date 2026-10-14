"""Audit protocol provenance, summarize complement closure, then hash artifacts."""
import csv,hashlib,json
from collections import Counter
from pathlib import Path
import boundary_matrix

HERE=Path(__file__).resolve().parent

def main():
    protocols=json.loads((HERE/'OPTIMAL_PROTOCOLS.json').read_text(encoding='utf-8'))
    nodes=0
    for case in protocols:
        original=case['queries'];pairs=set(map(tuple,case['pairs']))
        def annotate(node,rf,used=frozenset()):
            nonlocal nodes
            nodes+=1
            if 'query_on_states' not in node:return
            states=node['states'];local=node['query_on_states']
            matches=[q for q in original if sum((q>>s&1)<<i for i,s in enumerate(states))==local]
            assert matches,'Synthesized query!'
            q=matches[0]
            assert q not in used
            node['original_query_mask']=q
            assert node['children'][0]['states']==[s for s in states if not(q>>s&1)]
            assert node['children'][1]['states']==[s for s in states if q>>s&1]
            if rf:
                rel=tuple((i,j) for i,a in enumerate(states) for j,b in enumerate(states) if (a,b) in pairs)
                assert boundary_matrix.analyze(len(states),rel,local)[0]
            for child in node['children']:annotate(child,rf,used|{q})
        annotate(case['ordinary_protocol'],False)
        annotate(case['repair_safe_protocol'],True)
    (HERE/'OPTIMAL_PROTOCOLS.json').write_text(json.dumps(protocols,indent=2),encoding='utf-8')
    closed=Counter();minima={};all_counts=Counter()
    with (HERE/'FIXED_LIBRARY_RESULTS.csv').open(newline='',encoding='utf-8') as f:
        for row in csv.DictReader(f):
            n=int(row['n']);L=int(row['library_mask']);full=(1<<n)-1
            ad=int(row['ordinary_depth']);rf=int(row['repair_safe_depth'])
            all_counts[row['sampling']]+=1
            if all(((L>>(q-1))&1)==((L>>(full-q-1))&1) for q in range(1,full)):
                closed[n,ad,rf,row['sampling']]+=1
                if ad<rf<99:
                    key=str(n)
                    if key not in minima or int(row['query_count'])<int(minima[key]['query_count']):minima[key]=row
    with (HERE/'COMPLEMENT_CLOSED_DEPTHS.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['n','ordinary_depth','repair_safe_depth','sampling','case_count'])
        for key,count in sorted(closed.items()):w.writerow([*key,count])
    out={'protocol_nodes_verified':nodes,'library_case_counts':dict(all_counts),'minimal_complement_closed_finite_gaps':minima}
    (HERE/'FINAL_CHECKS.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out,indent=2))
    with (HERE/'SHA256SUMS.txt').open('w',encoding='utf-8') as f:
        for path in sorted(HERE.iterdir()):
            if path.is_file() and path.name!='SHA256SUMS.txt':
                f.write(hashlib.sha256(path.read_bytes()).hexdigest()+'  '+path.name+'\n')

if __name__=='__main__':main()
