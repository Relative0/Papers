#!/usr/bin/env python3
"""Exhaustive certificates for the two-basis F2-mobit no-strong-contextuality
lemma, used in the residue-layer theorem in CAPABILITY_REPORT.md.
"""
import laboratory as L
from laboratory import *

def check():
    results=[]
    for n in range(1,5):
        N=1<<n;count=0;hist=Counter();contexts=0
        for state in range(1,1<<N):
            S=(state&-state).bit_length()-1 # least nonzero coefficient
            hist[S]+=1
            # Local bases {a,b} and {a,a+b}; choose a for i not in S,
            # and respectively b or a+b for i in S.
            for C in range(N):
                varying=S&C;fixed=S^varying;sub=varying;value=0
                while True:
                    value^=(state>>(fixed|sub))&1
                    if sub==0:break
                    sub=(sub-1)&varying
                assert value==1
                contexts+=1
            count+=1
        results.append({'n':n,'nonzero_states':count,'basis_settings_per_site':2,'contexts_per_state':N,'supported_context_checks':contexts,'witness_coefficient_histogram':dict(hist)})
    save('two_setting_no_strong_certificates.json',{'canonical_pair':[['a','b'],['a','a+b']],'results':results,'generalization':'Any two distinct F2^2 dual bases have this form up to labeling and change of coordinates. The finite-local-ring extension follows by applying a linear functional to a nonzero leading radical layer.'})
    return {'all_nonzero_states_tested':sum(r['nonzero_states'] for r in results),'n_range':[1,4],'supported_context_checks':sum(r['supported_context_checks'] for r in results),'algorithm':'constructive minimum-coefficient global assignment, checked in every context','output':'two_setting_no_strong_certificates.json'}
if __name__=='__main__':
    L.METRIC_FILE='two_setting_metrics.json';L.timed('two_setting_no_strong',check)
