"""Public MIT-licensed PySAT documentation examples: smoke, not industry data."""
from pathlib import Path
import json
from hybrid_core import compile_extract,exact_refine,balanced_tree,brute_partition

ROOT=Path(__file__).resolve().parents[1]
EXAMPLES=[
 {'id':'pysat_readme_implication','n':3,'clauses':[[-1,2],[-2,3]],'source':'https://github.com/pysathq/pysat#usage'},
 {'id':'pysat_home_forced_literal','n':2,'clauses':[[-1,2],[-1,-2]],'source':'https://pysathq.github.io/'},
 {'id':'pysat_readme_unsat','n':2,'clauses':[[-1,2],[1,-2],[-1,-2],[1,2]],'source':'https://github.com/pysathq/pysat#usage'}]

def main():
    records=[]
    for r in EXAMPLES:
        compiled=compile_extract(r['n'],r['clauses'],balanced_tree(range(1,r['n']+1)),minimize=True)
        expected=brute_partition(r['n'],r['clauses'])
        exact=exact_refine(r['n'],r['clauses'],compiled['direct_partition']) if compiled['satisfiable'] else None
        assert (exact['partition'] if exact else None)==expected
        records.append({**r,'license':'MIT','license_source':'https://github.com/pysathq/pysat/blob/master/LICENSE.txt',
                        'scope':'public documentation smoke control, excluded from primary comparison',
                        'compiled':compiled,'exact':exact,'expected':expected,'correct':True})
    (ROOT/'data'/'public_control_results.json').write_text(json.dumps(records,indent=2)+'\n')
    print(json.dumps({'public_controls':len(records),'discrepancies':0}))

if __name__=='__main__':main()
