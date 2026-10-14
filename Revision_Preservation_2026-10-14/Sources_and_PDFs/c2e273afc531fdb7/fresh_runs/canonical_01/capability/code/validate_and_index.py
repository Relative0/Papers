#!/usr/bin/env python3
"""Cross-check independent data against fresh reference results, then build indexes.
This script does not import supplied mathematical code. Counts are checked only
under matched conventions; the full resource comparison converts u to R explicitly.
"""
from pathlib import Path
import csv,json,re,hashlib,sys
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'; REF=ROOT/'provenance/supplied_fresh'
def readcsv(path):
    with path.open(newline='') as f:return list(csv.DictReader(f))
def save(name,obj): (DATA/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def csvsave(name,rows):
    with (DATA/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def crossvalidate():
    reference={int(r['packed']):r for r in readcsv(REF/'resource_inventory_audited_65536.csv')}
    independent=readcsv(DATA/'independent_resource_inventory.csv')
    assert len(reference)==len(independent)==65536
    def convert(a):
        result=0
        for j,c in enumerate((1,3,5,15)):
            if a>>j&1:result^=c
        return result
    for r in independent:
        entries=list(map(int,r['u_entries'].split(',')))
        packed=sum(convert(x)<<(4*j) for j,x in enumerate(entries))
        t=reference[packed]
        assert (r['a'],r['b'],r['binary_rank'])==(t['a'],t['b'],t['rank'])
    c1={(r['a'],r['b']):r for r in readcsv(DATA/'independent_smith_counts.csv')}
    c2={(r['a'],r['b']):r for r in readcsv(REF/'class_inventory_audited.csv')}
    assert len(c1)==len(c2)==15
    for k,r in c1.items():
        assert r['resources']==c2[k]['count'] and r['binary_rank']==c2[k]['literal_rank']
    c1={(r['a'],r['b']):r for r in readcsv(DATA/'independent_contextuality.csv')}
    c2={(r['a'],r['b']):r for r in readcsv(REF/'contextuality_audited_15_classes.csv')}
    mapping={'local':'LOCAL','logical_not_strong':'LOGICAL','strong':'STRONG'}
    for k,r in c1.items():
        assert mapping[r['classification']]==c2[k]['status_192']
        assert r['possible_events']==c2[k]['possible']
        assert r['unextendable_events']==c2[k]['uncovered']
    for r in readcsv(DATA/'independent_orthogonal_ablation.csv'):
        t=c2[(r['a'],r['b'])]
        assert r['global_assignments']==t['orthogonal_global_assignments']
        assert r['uncovered']==t['orthogonal_uncovered']
    # Verify each advertised data file exists and basic exhaustive totals.
    metrics=[]
    for name in ['independent_metrics.json','ablation_metrics.json','bridge_phase_metrics.json','two_setting_metrics.json']:
        for stage,m in json.loads((DATA/name).read_text()).items():
            for out in m.get('output','').split(';'):
                if out.strip():assert (DATA/out.strip()).is_file(),out
            metrics.append({'metric_file':name,'stage':stage,**m})
    save('computational_ledger.json',metrics)
    probs=json.loads((DATA/'independent_probability_certificate.json').read_text())
    assert probs['weak_completion_CHSH_ZX']=='4'
    assert sum(int(x['resources']) for x in c1.values())==65535
    result={'success':True,'all_resource_encoding_and_rank_comparisons':65536,'Smith_class_comparisons':15,'complete_measurement_contextuality_comparisons':14,'canonical_orthogonal_representative_comparisons':14,'differences':[],'encoding_conversion':'u^j -> (1+R)^j; columns [1,3,5,15]','meaning':'agreement with fresh supplied computations is corroboration; universal claims use proofs','source_data_directory':'provenance/supplied_fresh'}
    save('source_comparison.json',result)
    print(json.dumps(result),flush=True)
    return metrics

def table_rows(section):
    lines=[x for x in section.splitlines() if x.startswith('|')]
    if not lines:return []
    header=[x.strip() for x in lines[0].strip('|').split('|')]
    rows=[]
    for line in lines[2:]:
        values=[x.strip() for x in line.strip('|').split('|')]
        if len(values)!=len(header):raise ValueError('Malformed Markdown table: '+line)
        rows.append(dict(zip(header,values)))
    return rows

def index_report(metrics):
    report=ROOT/'reports/CAPABILITY_REPORT.md'; text=report.read_text()
    sections=[('capability_map',text.split('# A. Capability map',1)[1].split('# B.',1)[0]),('dependency_matrix',text.split('## B.1 ',1)[1].split('## B.2 ',1)[0]),('dependency_ablations',text.split('## B.2 ',1)[1].split('# C.',1)[0]),('prior_art_matrix',text.split('# H. ',1)[1].split('# I.',1)[0])]
    for name,section in sections:
        rows=table_rows(section);assert rows
        save(name+'.json',rows);csvsave(name+'.csv',rows)
    headings=list(re.finditer(r'^## Theorem ([A-Z][0-9]+[a-z]?): (.+)$',text,re.M))
    theorem_index=[];theorem_text=['# Formal theorem set\n\nExtracted from CAPABILITY_REPORT.md. Operational contracts and model definitions in that report are part of every statement. Imported results remain explicitly identified.\n']
    for h in headings:
        end=re.search(r'^#{1,2} ',text[h.end():],re.M)
        stop=h.end()+end.start() if end else len(text)
        body=text[h.start():stop].strip()
        theorem_text.append(body)
        theorem_index.append({'id':h.group(1),'title':h.group(2),'report':'reports/CAPABILITY_REPORT.md','priority':'imported supplied-review theorem' if h.group(1)=='R1' else 'proved/rederived in this report; priority not certified'})
    save('theorem_index.json',theorem_index)
    (ROOT/'reports/FORMAL_THEOREMS.md').write_text('\n\n---\n\n'.join(theorem_text)+'\n')
    # Display ledger retains all detailed metrics in its JSON counterpart.
    def scope(m):
        skip={'seconds','output','algorithm','metric_file','stage'}
        return '; '.join(k.replace('_',' ')+'='+str(v) for k,v in m.items() if k not in skip)
    table='| Experiment | Exact finite scope | Seconds | Output file(s) in data/ |\n|---|---|---:|---|\n'
    for m in metrics:
        table+='| '+m['stage']+' | '+scope(m).replace('|','/').replace('\n',' ')+' | '+f"{m['seconds']:.4f}"+' | '+m.get('output','')+' |\n'
    text=re.sub(r'<!-- LEDGER_START -->.*?<!-- LEDGER_END -->','<!-- LEDGER_START -->\n'+table+'<!-- LEDGER_END -->',text,flags=re.S)
    report.write_text(text)
    (ROOT/'reports/COMPUTATIONAL_LEDGER.md').write_text('# Independent exact-computation ledger\n\nWall times are environment-specific. Every exhaustive claim is limited to its stated domain. Source rerun timings are separate in provenance/.\n\n'+table)
    csvsave('computational_ledger.csv',[{'experiment':m['stage'],'scope':scope(m),'seconds':m['seconds'],'output':m.get('output',''),'metric_file':m['metric_file']} for m in metrics])
    save('package_validation.json',{'success':True,'theorems_indexed':len(theorem_index),'capability_rows':len(json.loads((DATA/'capability_map.json').read_text())),'independent_experiment_stages':len(metrics),'source_comparison':'source_comparison.json','proofs_are_not_formally_machine_verified':True})

if __name__=='__main__':
    try:index_report(crossvalidate())
    except Exception as e:
        print('VALIDATION FAILED:',str(e),file=sys.stderr);raise
