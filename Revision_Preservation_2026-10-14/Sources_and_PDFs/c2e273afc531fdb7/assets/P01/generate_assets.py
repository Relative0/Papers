from pathlib import Path
import csv, hashlib, json, math, platform, sys, time
import sympy as sp
HERE=Path(__file__).resolve().parent
OUT=HERE.parent
source=OUT/'runs/canonical_01/independent/resource_inventory_summary.json'
data=json.loads(source.read_text())
lines=[r'\begin{table}[ht]\centering\small',r'\begin{tabular}{rrrrrrll}',r'\toprule',r'$(a,b)$ & Count & $r$ & $h$ & Binary rank & Messages & Support & Teleport\\\midrule']
for x in data:
    a,b=x['a'],x['b']; r=int(a<4)+int(b<4); h=0 if r==0 else (2 if a==b else 1)
    typ='Excluded' if not r else ('Local' if r==1 else ('Strong' if h==2 else 'Logical'))
    msg=str(x['shared_messages']) if r else 'n/a'; tp='Yes' if x['universal_teleportation'] else ('No' if r else 'n/a')
    lines.append(f'$({a},{b})$ & {x["count"]:,} & {r} & {h} & {x["binary_rank"]} & {msg} & {typ} & {tp}'+r'\\')
lines.extend([r'\bottomrule\end{tabular}',r'\caption{All fifteen Smith classes over $A=\mathbb F_2[u]/(u^4)$ for $2\times2$ matrices. Exponent $4$ denotes zero. Logical means logical but not strong. Counts include the zero matrix; the resource tasks exclude it.}\label{tab:smith}',r'\end{table}'])
(HERE/'smith_table.tex').write_text('\n'.join(lines)+'\n')

def rank(rows,p):
    if not rows:return 0
    a=[[int(v)%p for v in row] for row in rows]; k=0
    for j in range(len(a[0])):
        pivot=next((i for i in range(k,len(a)) if a[i][j]),None)
        if pivot is None:continue
        a[k],a[pivot]=a[pivot],a[k]; inv=pow(a[k][j],-1,p);a[k]=[(x*inv)%p for x in a[k]]
        for i in range(len(a)):
            if i!=k:
                c=a[i][j];a[i]=[(x-c*y)%p for x,y in zip(a[i],a[k])]
        k+=1
        if k==len(a):break
    return k

t=time.monotonic();results=[]
for p,modulus in [(2,4),(2,8),(3,9)]:
    for d in [2,3,4]:
        eye=sp.eye(d);candidates=[eye]
        for i in range(d):
            for j in range(d):
                if i!=j:
                    e=sp.zeros(d);e[i,j]=1;candidates.append(eye+e)
            j=(i+1)%d;perm=sp.eye(d);perm.row_swap(i,j);e=sp.zeros(d);e[j,i]=1
            candidates.extend([perm,perm*(eye+e)])
        selected=[];flat=[]
        for mat in candidates:
            row=list(mat)
            if rank(flat+[row],p)>len(flat):selected.append(mat);flat.append(row)
        assert len(flat)==d*d
        assert all(math.gcd(int(m.det()),modulus)==1 for m in selected)
        analysis=sp.Matrix(flat)
        assert math.gcd(int(analysis.det()),modulus)==1
        results.append(dict(residue=p,ring=f'Z/{modulus}Z',d=d,outcomes=d*d,
                            analysis_determinant=int(analysis.det()),effects=[[[int(m[i,j])%modulus for j in range(d)] for i in range(d)] for m in selected]))
record=dict(purpose='Finite check of both analyzer invertibilities; general result uses the analytic proof.',command=[sys.executable,str(Path(__file__).resolve())],python=sys.version,platform=platform.platform(),seed=None,seconds=time.monotonic()-t,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),input_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),cases=results,status='PASS')
(HERE/'ANALYZER_CHECK.json').write_text(json.dumps(record,indent=2)+'\n')
print(f'Generated 15-class table and verified {len(results)} analyzer configurations.')
