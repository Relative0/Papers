from pathlib import Path
import csv, json
p=Path('/mnt/data/u1_u6_hostile_audit')
checks={}
for f in sorted(p.glob('*.csv')):
    with f.open(newline='',encoding='utf-8') as h:
        rows=list(csv.reader(h))
    widths={len(r) for r in rows}
    checks[f.name]={'rows_including_header':len(rows),'widths':sorted(widths),'ok':len(widths)==1 and (len(rows)>0)}
    if not checks[f.name]['ok']:
        raise SystemExit(f'CSV validation failed: {f}: {widths}')
# required JSON readable
for name in ['U1_U6_FINITE_SUMMARY.json','U4_OCTAHEDRAL_F2_SUMMARY.json','U4_OCTAHEDRAL_Q_SUMMARY.json','CHAIN_ADAPTIVE_SUMMARY.json','CHAIN_ADAPTIVE_INDEPENDENT.json','CARTESIAN_INDEPENDENT_SUMMARY.json','U3_ABSTRACT_INDEPENDENT_SUMMARY.json','AUDIT_SUMMARY.json']:
    with (p/name).open(encoding='utf-8') as h: json.load(h)
checks['json']='all required JSON parsed'
with (p/'VALIDATION_SUMMARY.json').open('w',encoding='utf-8') as h: json.dump(checks,h,indent=2)
print(json.dumps(checks,indent=2))
