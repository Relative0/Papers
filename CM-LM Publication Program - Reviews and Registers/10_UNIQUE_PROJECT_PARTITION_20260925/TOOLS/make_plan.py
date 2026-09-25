import json,pathlib,collections
from partition_data import *
W=pathlib.Path(__file__).parent
rows=json.loads((W/'inventory_before.json').read_text(encoding='utf-8')); tracked=set(json.loads((W/'tracked_before.json').read_text())); idx={x['path']:x for x in rows}
def mapped(s):
 folder,rest=s.split('/',1)
 if folder==PORT:return None
 if folder==GS:
  return GUARD+'/HISTORY/FORMER_GUARD_SYNTHESIS_FOLDER/'+rest if '/' not in rest else None
 if folder==ATLAS:
  return FOUND+'/HISTORY/FORMER_ATLAS_FOLDER/'+rest if '/' not in rest else None
 if folder==MODAL:
  if '/papers/' in s:
   name=s.rsplit('/',1)[1]; owner=INTR if name.startswith('Intrinsic_') else SIGNED
   return owner+('/REPRODUCIBILITY/ORIGINAL_SOURCE_ARCHIVE/' if name.endswith('.zip') else '/CURRENT_MANUSCRIPT/')+name
  return SHARED+'/'+rest
 if folder==DESIGN:
  if rest.startswith(('02_VERIFICATION/','03_RESEARCH_LEDGER/')):return None
  rest=rest.replace('01_RESEARCH_NOTES/','HISTORY/WORKING_NOTES/')
  if '/' not in rest:rest='HISTORY/FORMER_FOLDER/'+rest
  return GEN+'/OBSERVATION_DESIGN_AND_SAFE_REFINEMENT/'+rest
 if rest in {'SOURCE_MANIFEST_SHA256.csv','00_PUBLICATION_CONTEXT_2026-09-25.md','README_FIRST.md'}:
  return folder+'/HISTORY/PARTITION_BASELINE_20260925/'+rest
 if folder==COMP:
  rest=rest.replace('02_PORTFOLIO_PREDECESSOR_AND_EVIDENCE_20260921/','HISTORY/PORTFOLIO_PREDECESSOR_20260921/').replace('03_LEGACY_AND_PRECONSOLIDATION/','HISTORY/LEGACY_PRECONSOLIDATION/')
 if folder=='Finite Jet Rigitity (Paper A)':rest=rest.replace('02_REVIEW_HISTORY_AND_PARENT_CONTEXT/','HISTORY/REVIEW_AND_PARENT_CONTEXT/')
 if folder=='ProLT':
  rest=rest.replace('03_LEGACY_VERSIONS/','HISTORY/CORE_V0_6/')
 if folder==GEN:
  if rest.endswith('propositional-logical-topology-core-v0.8.pdf'):return 'ProLT/HISTORY/CORE_V0_8/propositional-logical-topology-core-v0.8.pdf'
  rest=rest.replace('02_CORE_PREDECESSOR_SOURCES/','HISTORY/CORE_PREDECESSOR_SOURCES/')
 if '/' not in rest and rest.endswith('.zip'):rest='HISTORY/ORIGINAL_RELEASES/'+rest
 return folder+'/'+rest
target={x['path']:mapped(x['path']) for x in rows}
# Deliberate manuscript/review ownership; never infer duplicate deletion from name alone.
found_names={'Correspondence_and_Logical_Matrices_Boolean_Operator_Calculus_LM_Centered.pdf','Correspondence_and_Logical_Matrices_Boolean_Operator_Calculus_LM_Centered.tex','CM_LM_Audit_Astra.md','LM_Centered_Revision_Notes.md'}
comp_reviews={'Computational_Paper_Response_to_R2.md','Computational_Paper_Review_Panel_R1.md','Computational_Paper_Review_Panel_R2.md'}
for x in rows:
 s=x['path']; f=x['folder']; n=s.rsplit('/',1)[1]
 if f==COMP and (n in found_names or n=='CM_LM_Boolean_Operator_Calculus_LM_Centered_V1.pdf' or n=='Operator-Level_Boolean_Computation_with_Correspondence_Matrices_current.pdf'):target[s]=None
 if f==FOUND and (n in comp_reviews or n=='Operator-Level_Boolean_Computation_with_Correspondence_Matrices_current.pdf'):target[s]=None
destinations=collections.defaultdict(list)
for s,d in target.items():
 if d:destinations[idx[s]['sha256']].append((s,d))
deletes=[]; moves=[]
for x in rows:
 s=x['path']; d=target[s]
 if d is None:
  candidates=destinations[x['sha256']]
  candidates=[(a,b) for a,b in candidates if a in tracked]
  assert candidates,('No tracked canonical',s)
  candidates.sort(key=lambda ab:(ab[1].startswith(REG),'/HISTORY/' in ab[1],len(ab[1])))
  old,canonical=candidates[0]
  deletes.append(dict(old=s,canonical=canonical,canonical_before=old,sha256=x['sha256'],bytes=x['bytes'],tracked=s in tracked,reason='Exact duplicate; complete portfolio coverage verified' if x['folder']==PORT else 'Exact duplicate; canonical ownership consolidated'))
 elif d!=s:moves.append(dict(old=s,new=d,sha256=x['sha256'],bytes=x['bytes']))
assert len([d for d in deletes if d['old'].startswith(PORT+'/')])==353
assert len(set(d for d in target.values() if d))==sum(d is not None for d in target.values())
plan={'starting_commit':'7b9cdedadd8d2ec75d489f82917109b723f56e0c','moves':moves,'deletes':deletes,'mapping':target}
(W/'partition_plan.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
print(json.dumps({'moves':len(moves),'deletes':len(deletes),'removed_bytes':sum(x['bytes'] for x in deletes),'surviving_original_files':sum(d is not None for d in target.values()),'after_folders':sorted({d.split('/')[0] for d in target.values() if d}),'untracked_removed':[x['old'] for x in deletes if not x['tracked']]},indent=2))
