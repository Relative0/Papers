"""Generate collection navigation; never replace pre-existing scientific or navigation files."""
from snapshot import ROOT,OUT,dump,sha
import pathlib,os,json,re
P=[]
def add(id,home,title,kind,start,history,evidence,questions,relationship):
    P.append(dict(id=id,home=home,title=title,kind=kind,start=start,history=history,evidence=evidence,open_questions=questions,relationship=relationship))
add('FO','CM-LMs and lifting','Correspondence and Logical Matrices: A Typed Boolean Operator Calculus','Foundations / synthesis manuscript','CM_LM_Final_Adversarial_Review_and_Revision_2026-09-27/final_bundle/revised_manuscript/CM_LM_Boolean_Operator_Calculus_Revised.pdf',
    'September 22 LM-centered handoff; September 27 foundations revision; final September 27 adversarial revision. The final source explicitly narrows the contribution to symbolic/numeric coherence.',
    ['CM_LM_Final_Adversarial_Review_and_Revision_2026-09-27/final_bundle/README.md','CM_LM_Final_Adversarial_Review_and_Revision_2026-09-27/final_bundle/Publication_Readiness_Adversarial_Review_2026-09-27.md'],
    'Author and venue checks; constituent algebra is classical and theorem priority is not certified by the finite checker. The final package records closure of earlier blockers; the older README_FIRST is not the current readiness record.',
    'Foundations used by the compiler and guarded-operator work. The correction audit, LM/modal bridge, phase companions and program register retain separate roles.')
add('CO','CM Computation','Operator-Level Boolean Computation with Correspondence Matrices','Compiler methods / negative systems results','02_CONTRACT_REVISION_20260926/Operator_Level_CM_Compiler_Revised_Draft.pdf',
    'September 22 draft; September 26 contract revision, then synthetic and natural timing updates. Same-date full-evidence and study ZIPs are distinct snapshots: the study package includes the later natural timing result.',
    ['README_FIRST.md','02_CONTRACT_REVISION_20260926/REVIEW_RESPONSE.md','03_STUDY_DESIGN_20260926/README.md','05_NATURAL_TIMING_20260926/README.md'],
    'Matched systems comparisons, historical P14 imported-runtime identity and release preparation remain open. Existing negative results must remain visible.',
    'FO owns the representation calculus. SC owns the separate conditioning/decomposition Draft 3; the SC package repeated here is a reference copy, not the compiler manuscript head.')
add('P01','Chain Ring Contextuality and Exact Resources (P01)','Contextuality and Exact Information Resources over Finite Chain Rings','Research manuscript','REVISION_2026-09-26/manuscript/main.pdf',
    'September 19 source preserved under the portfolio source package; September 26 revised manuscript is the reviewed head. The sibling extraction with manuscript/Chain Ring.tex is retained as delivered.',
    ['REVISION_2026-09-26/README.md','REVISION_2026-09-26/REVISION_RESPONSE.md','REVISION_2026-09-26/supplement/README.md'],
    'Author/venue and specialist priority review remain. Historical clean-extraction checksums are stale for three manuscript/supplement variants; current package checksums pass.',
    'Keep the computational supplement with P01. The Boolean-interface note is optional; the full process-semantics companion PC has a different model contract and stays separate.')
add('P02','Exact Query Bounds in Characteristic Two (P02)','Exact Bernstein–Vazirani Query Complexity in Characteristic-Two Modal Computation','Focused research note','P02_Final_Reviewed_Source_2026-09-27/P02_Final_Reviewed_Source_2026-09-27/manuscript/main.pdf',
    'Original broader exact-query manuscript; September 27 audit and revision; final specialist gate narrows the title and principal contribution to the adaptive modal BV bound.',
    ['P02_Final_Reviewed_Source_2026-09-27/P02_Final_Reviewed_Source_2026-09-27/README.md','P02_Final_Reviewed_Source_2026-09-27/P02_Final_Reviewed_Source_2026-09-27/reports/FINAL_SPECIALIST_GATE_REVIEW_2026-09-27.md','P02_Recovered_Original_Reproduction_Supplement.zip'],
    'Priority and operational-contract scope remain bounded. SHA256SUMS includes its own stale hash; payloads and ZIP integrity are assessed separately. No checksum file was rewritten.',
    'Related to chain-ring and phase work, but its pointwise oracle/adaptive recorded-readout contract is separate. Literal detector patterns in IP do not establish this query advantage.')
add('A','Finite Jet Rigitity (Paper A)','Finite-Jet Rigidity and Exact Realization of Boolean Sign Laws','Focused mathematical note','FINAL_REVIEWED_PACKAGE_2026-09-27/FINAL_SUBMISSION_PACKAGE/FINAL_MANUSCRIPT/finite_jet_sign_laws_FINAL_SUBMISSION_CANDIDATE.pdf',
    'Original submission candidate; fresh referee package; final September 27 source-of-record package. The original folder spelling is retained for compatibility.',
    ['FINAL_REVIEWED_PACKAGE_2026-09-27/FINAL_SUBMISSION_PACKAGE/README_FIRST.md','FINAL_REVIEWED_PACKAGE_2026-09-27/FINAL_SUBMISSION_PACKAGE/EDITORIAL/HOSTILE_HANDLING_EDITOR_REPORT.md'],
    'Venue/significance and author review remain. The source credits classical smooth-flatness mechanisms; do not count those mechanisms as new results.',
    'Sign realizability/regularity is distinct from Paper B’s fixed guard-library dispatch question.')
add('GU','Guarded Boolean Operator (Paper B)','Exact Guarded Boolean Dispatch: Coordinates, Degree, and Observation Cost','Mathematical methods / expository note','REVIEWED_PACKAGE_2026-09-28/Guarded_Boolean_Paper_B_Reviewed_2026-09-28/manuscript/guarded_boolean_dispatch_revised.pdf',
    'September 24 restricted-dispatch manuscript and review remain; September 28 revision adds the exact degree/test tradeoff for x+y+xy. Newly exposed from its intact original ZIP.',
    ['REVIEWED_PACKAGE_2026-09-28/Guarded_Boolean_Paper_B_Reviewed_2026-09-28/README.md','REVIEWED_PACKAGE_2026-09-28/Guarded_Boolean_Paper_B_Reviewed_2026-09-28/audit/REVIEW_AND_REVISION_REPORT.md'],
    'Conditional submission only after author/venue checks. Coordinate dependence, promised zero-free inputs and boundary rejection are essential. Fewer tests are not demonstrated runtime speedups.',
    'Uses fixed-frame FO representations; shares an observation-selection motif with ProLT, without merging their theorem scopes. Former guard-synthesis material remains nested history.')
add('PL','ProLT','Observation Topologies for Finite Propositional Logic','Expository synthesis','ProLT_v0.9_Submission_Package/ProLT_v0.9_Submission_Package/ProLT_Observation_Topologies_Submission_v0.9_FINAL.pdf',
    'Earlier v0.6/v0.8 audit context; v0.8.1 release at this folder root; v0.9 submission revision supersedes it as the reading head. Original README and release notes remain historical.',
    ['ProLT_v0.9_Submission_Package/ProLT_v0.9_Submission_Package/REVISION_NOTES_v0.9.md','RELEASE_NOTES.md'],
    'Venue and author checks. The current abstract explicitly calls the work an expository synthesis of standard finite constructions.',
    'Framework for BT and GR. The MIND develops later carrier splitting, observation refinement and measurement branches in its own home.')
add('BT','ProLT-Homology','Binary Order Thinning of Finite Posets: Homology, Collapses, and Sharp Limits','Research manuscript','ProLT-Homology-Reviewed-2026-09-27/02_REVIEWED_MANUSCRIPT_20260927/binary_order_thinning_finite_posets_reviewed_v3.pdf',
    'September 24 post-audit v2 remains; reviewed September 27 v3 is the current head. Historical homological foundations notes also belong to GR, not just this fixed-carrier result.',
    ['ProLT-Homology-Reviewed-2026-09-27/02_REVIEWED_MANUSCRIPT_20260927/CHANGELOG_20260927.md','ProLT-Homology-Reviewed-2026-09-27/02_REVIEWED_MANUSCRIPT_20260927/PUBLICATION_READINESS_AUDIT_20260927.md','ProLT-Homology-Reviewed-2026-09-27/02_REVIEWED_MANUSCRIPT_20260927/reproducibility/README.md'],
    'Specialist priority/venue review; finite exhaustive minimality is distinct from analytic proof. Generalize neither one-bit nor height-two assumptions.',
    'Fixed-carrier thinning links PL to GR and The MIND RF-IDENT work; bounded least/greatest-element RF-IDENT is not a solution of arbitrary height-two RF-IDENT.')
add('SP','Signed Integral CM Phase Calculus','Signed and Integral Lifts of Correspondence Matrices','Technical / correction companion','CM_Phase_Calculus_Submission_Revision/paper.pdf',
    'Original verified phase manuscript and modular source retained; September 27 submission revision is the current 30-page companion. Original archive paper.tex has been safely restored beside the unchanged renamed CM Phase Calculus.tex.',
    ['CM_Phase_Calculus_Submission_Revision/README.md','CM_Phase_Calculus_Submission_Revision/REFEREE_PANEL_REPORT.md','CM_Phase_Calculus_Submission_Revision/REVISION_MEMO.md'],
    'Author/venue checks and novelty positioning as a correction companion. No new physical quantum theory, Born rule or simulation speedup is established.',
    'Separate from intrinsic Boolean IP: changes of scalar domain and XOR carry matter. FO, BR, PC and AU supply related model boundaries.')
add('IP','Intrinsic Boolean CM Phase Algebra','Boolean CM Phase Algebra: Native Operations, Tags, and Readout','Technical companion','REVIEWED_PACKAGE_2026-09-28/CM_Phase_Research_Revision_2026-09-28/manuscript/CM_Phase_Algebra_Revised.pdf',
    'September 17 standalone/modular originals retained; September 28 substantial rewrite is the current head and changes the older publication-track disposition to a focused companion.',
    ['REVIEWED_PACKAGE_2026-09-28/CM_Phase_Research_Revision_2026-09-28/README.md','REVIEWED_PACKAGE_2026-09-28/CM_Phase_Research_Revision_2026-09-28/audit/Theory_Audit_and_Review.md','REVIEWED_PACKAGE_2026-09-28/CM_Phase_Research_Revision_2026-09-28/audit/Claim_Crosswalk.md'],
    'Author review and actual venue/form remain open. The detector lower bound credits established coding theory; the package recommends against a substantial standalone original-research submission.',
    'Native F2[C4] operations and tag/readout contracts are distinct from SP’s integral/signed lift and P02’s modal query model.')
add('PC','Chain Ring Process Semantics (Technical Companion)','Process Closure and Restricted Conversion in a Chain-Ring Modal Model','Technical companion','01_SOURCE_PACKAGE_FROM_PORTFOLIO_20260921/technical_companion_20260920/main.tex',
    'September 20 companion; September 21 verification supplement and no-go memo. P03_STUB is historical exploratory material, not an additional promoted paper.',
    ['README_FIRST.md','01_SOURCE_PACKAGE_FROM_PORTFOLIO_20260921/research_verification_20260921/GO_NO_GO_MEMO.md'],
    'Specialist priority/model-contract review; some historical build byproducts named in manifests are unavailable. The binary completion changes tensor semantics.',
    'Substantial companion to P01; keeps conditioning, restricted effects, disposal and conversion boundaries explicit. Do not absorb it wholesale into P01.')
add('BR','LM-Modal Bridge (Technical Companion)','Does the Symbolic LM Calculus Canonically Induce the Modal Measurement Theory?','Technical bridge / synthesis','01_RECOVERED_BRIDGE_PACKAGE/report/LM_Modal_Bridge_Report.tex',
    'Recovered bridge research package with historical inputs and reports; retained as a separate companion.',
    ['README_FIRST.md','CLAIMS_AND_UNIQUENESS.md'],
    'Review the scalar-enrichment choices, restricted effects and support-update result; stronger independent novelty requires new substance.',
    'Connects FO to P01/PC without claiming that Boolean valuation alone creates chain-ring amplitudes.')
add('AU','CM Correctness Audit and Model Boundaries (Technical Report)','Correctness Audit of Boolean/Modal CM Models','Correction report / shared evidence','01_SOURCE_PACKAGE_FROM_PORTFOLIO_20260921/audit_package/paper/CM_Correctness_Audit_Standalone.tex',
    'Canonical correction report with source snapshots, tests and model ledger. Historical source claims are retained as audit inputs.',
    ['README_FIRST.md','CLAIMS_AND_UNIQUENESS.md'],
    'Cite the exact downstream corrections; some package dependency/build paths remain historical. Finite enumerations do not replace general proofs.',
    'Serves the broader Boolean/modal, phase and chain-ring program; not primarily supporting only FO or CO.')
add('SC','CM Structural Computation and Decomposition (Research Direction)','Exact Boolean Decomposition Artifacts under Conditioning: Algebraic Contracts and a Reproducibility Audit','Draft 3 technical report + continuing research','CM_Structural_Computation_Final_Research_Package/manuscripts/v3/paper_v3.pdf',
    'Three-draft September 26 package: v1 → v2 → v3. September 28 convergence audit and later C1–C4 T3 Phase 2 evidence are supplements; the handoff explicitly leaves Draft 3 unchanged.',
    ['CM_Structural_Computation_Final_Research_Package/00_READ_ME_FIRST.md','CM_Structural_Computation_Final_Research_Package/04_UNRESOLVED_ISSUES.md','CONVERGENCE_EVIDENCE_2026-09-28/Reading_Entry_Points/t3_phase2_computation_20260928/HANDOFF_TO_MASTER.md','CONVERGENCE_EVIDENCE_2026-09-28/Original_Packages'],
    'Master convergence decision and manuscript integration are still unlocated. Dense storage formula success does not imply serialized-byte or best-baseline runtime superiority; later T3 results do not silently supersede Draft 3.',
    'Related to CO but distinct endpoints and manuscript. Exact duplicate Draft 3 package under CM Computation stays as a reference. Structured Factorization is a separate live project linked through The MIND.')
add('GR','General ProLT Observation Refinement (Research Direction)','Observation Refinement Beyond a Fixed Carrier, with Constrained Observation Design','Shared / exploratory research','RESEARCH_BRIEF.md',
    'v0.1 homological foundations and v0.2 classification; v0.3–v0.5 design notes retained. The zero-byte v0.3 source is preserved, not silently reconstructed. Later integrated MIND v0.5 has a separate canonical home.',
    ['README_FIRST.md','01_RESEARCH_NOTES/ProLT_Observation_Refinement_Classification_v0.2.tex','OBSERVATION_DESIGN_AND_SAFE_REFINEMENT/HISTORY/WORKING_NOTES/ProLT_Simultaneous_Observation_Refinement_v0.5.tex'],
    'Historical relative-dimension equality and dependent complexity argument are explicitly rejected in the brief. Further scope/priority questions remain. Do not treat the older v0.5 label as the newer MIND manuscript.',
    'Genuinely shared input to PL, BT and The MIND observation-refinement/measurement branches. Original path remains because The MIND explicitly references this research.')
add('RG','CM-LM Publication Program - Reviews and Registers','CM–LM Publication Program: Reviews, Registers and Shared Evidence','Program register; not a paper','PROJECT_REGISTER.md',
    'Theorem bank, portfolio provenance, September 25 partition and September 26 viability reviews. Original decisions are dated evidence, not immutable current classifications.',
    ['THEOREM_BANK_OWNERSHIP.md','08_PORTFOLIO_PROGRAM_REPORTS_20260921','10_UNIQUE_PROJECT_PARTITION_20260925'],
    'Use this collection’s dated crosswalk for later revisions. Older manifest paths and readiness labels can be superseded without loss of their source bytes.',
    'Shared across the publication program; no paper receives exclusive ownership of shared reviews or theorem-bank material.')

def link(label,path):return f'[{label}](<{path}>)'
def write_new(path,text):
    path.parent.mkdir(parents=True,exist_ok=True)
    # All targets are generated paths declared by this script, absent from baseline.
    originals={x['original_path'] for x in json.loads((OUT/'baseline_sources.json').read_text(encoding='utf-8'))}
    assert path.relative_to(ROOT).as_posix() not in originals,f'Would overwrite original {path}'
    path.write_text(text.rstrip()+'\n',encoding='utf-8')
def main():
    for p in P:
        home=ROOT/p['home'];start=home/p['start'];assert start.exists(),start
        source=start.with_suffix('.tex')
        # The final Finite-Jet PDF deliberately has a different suffix from its source.
        if p['id']=='A':source=home/'FINAL_REVIEWED_PACKAGE_2026-09-27/FINAL_SUBMISSION_PACKAGE/FINAL_MANUSCRIPT/finite_jet_sign_laws_FINAL_SUBMISSION.tex'
        p['source']=source.relative_to(home).as_posix() if source.exists() else None
        p['start_sha256']=sha(start)
        body=f"# {p['title']}\n\nCollection guide updated 30 September 2026. **{p['kind']}.**\n\nStart with {link('the recommended artifact',p['start'])}."
        if p['source'] and p['source']!=p['start']:body+=' '+link('LaTeX source',p['source'])+'.'
        body+=f"\n\n**Version history.** {p['history']}\n\n**Evidence and review.**\n\n"
        for e in p['evidence']:
            assert (home/e).exists(),home/e
            body+='- '+link(pathlib.PurePosixPath(e).name,e)+'\n'
        body+=f"\n**Relationships.** {p['relationship']}\n\n**Open questions.** {p['open_questions']}\n\nThe review judgments quoted here are recorded project assessments, including AI review, not new certification or external human peer review. Original scientific bytes, ZIPs, prior README files and manifests remain preserved.\n\n{link('Workspace index','../README.md')} · {link('Classification and relationship crosswalk','../00_Collection_Index/PAPER_CROSSWALK.md')} · {link('Full source manifest','../00_Collection_Index/source_manifest.json')}\n"
        write_new(home/'COLLECTION_README.md',body)
    dump('paper_catalog.json',P)
    intro='# Papers for Publication\n\nPaper-centered collection, organized 30 September 2026. Start with the reading links below. Existing paper folders retain their paths; newer reviewed packages take precedence over older README_FIRST entries where specified.\n\n'
    for category,ids in [('Manuscripts and notes',['FO','CO','P01','P02','A','GU','PL','BT']),('Technical companions and correction reports',['SP','IP','PC','BR','AU']),('Continuing and shared research',['SC','GR','RG'])]:
        intro+='## '+category+'\n\n| Work | Recommended start | Status |\n|---|---|---|\n'
        for p in P:
            if p['id'] in ids:intro+=f"| {link(p['title'],p['home']+'/COLLECTION_README.md')} | {link('Read',p['home']+'/'+p['start'])} | {p['kind']} |\n"
        intro+='\n'
    intro+='## Connected collections and delivery copies\n\n'
    intro+='- '+link('The MIND — its own canonical collection','The MIND/README.md')+' owns Observation Refinement v0.5, Paper U v0.3 and Structured Boolean Factorization; its measurement/RF-IDENT branch stays shared research.\n'
    intro+='- '+link('Linked MIND workspaces and current live-work caveats','00_Collection_Index/LINKED_MIND_WORKSPACES.md')+' accounts for both Paper U review folders and Structured Factorization, all left in place.\n'
    intro+='- '+link('B-Theory delivery PDFs','B-Theory Website/COLLECTION_README.md')+' are delivery copies, not additional papers.\n'
    intro+='- '+link('Preserved root ZIPs','90_Preserved_Sources/README.md')+' contains 10 relocated original root archives and verified pre-move safety copies of all 11. The process-semantics ZIP stays at the root for P01’s validation script.\n'
    intro+='- '+link('Original publishing shortlist','To publish.txt')+', '+link('partition report','CM_LM_UNIQUE_PROJECT_PARTITION_AND_OVERLAP_REPORT.md')+' and '+link('partition receipt','PARTITION_VERIFICATION_RECEIPT.json')+' remain unchanged as historical records.\n\n'
    intro+='## Verification and provenance\n\n'
    intro+='See '+link('collection records','00_Collection_Index/README.md')+', '+link('final verification','00_Collection_Index/FINAL_VERIFICATION.md')+', '+link('remaining uncertainties and access limits','00_Collection_Index/UNRESOLVED_AND_ACCESS.md')+' and '+link('complete folder tree','00_Collection_Index/FOLDER_TREE.txt')+'. Every inventoried source and archive member has a location or explicit status. ZIP integrity does not make every embedded historical checksum current. Scientific content was not edited; no files were deleted, committed, pushed or published.\n'
    write_new(ROOT/'README.md',intro)
    cross='# Paper identities, boundaries and later decisions\n\nClassification uses manuscript abstracts, package readmes/review decisions and project chats, rather than the old partition alone. The recommended reading head is distinct from a claim of publication readiness.\n\n'
    for p in P:cross+=f"## {p['id']} — {p['title']}\n\n{p['kind']}. {p['history']}\n\n{p['relationship']}\n\n{link('Paper guide','../'+p['home']+'/COLLECTION_README.md')}\n\n"
    cross+='## Cross-program boundaries\n\nFO → CO is foundations to compiler, not a shared manuscript. SC conditioning/decomposition Draft 3 is a separate methods report; the later T3 handoff is unintegrated evidence. P01, P02, PC, SP and IP use different scalar, resource, oracle or readout contracts. BR and AU record why those contracts cannot be collapsed. PL → BT → GR traces framework, fixed-carrier sharp theorem and general refinement research; The MIND owns the later integrated refinement paper and shared measurement work. Paper A studies sign realization under regularity; Paper B studies dispatch under specified guards. RG and website deliveries are not papers.\n\nThe historical “To publish” list remains useful evidence of intended releases but does not override later technical-companion decisions for IP/SP or identify a newer SC manuscript.\n'
    write_new(OUT/'PAPER_CROSSWALK.md',cross)
    write_new(ROOT/'90_Preserved_Sources/README.md','# Preserved original root ZIPs\n\nTen root ZIPs moved to '+link('Former_Root_ZIPs','Former_Root_ZIPs')+' only after complete copying and SHA-256 verification in '+link('Verified_PreMove_Copies','Verified_PreMove_Copies')+'. The process-semantics ZIP was restored to its root path after finding that P01 validation/prepare_companion.py loads it there. Its verified safety copy remains here too: all 11 original root ZIPs have a safety copy. Both copies are intentionally retained because this task forbids deletion. No original archive was rebuilt.\n\nThese are historical delivery snapshots, not current manuscript directories. Archive-only members remain recoverable inside their intact ZIPs and are reconciled by member name, size, CRC and SHA-256 in the archive manifests. '+link('Movement receipt','../00_Collection_Index/organization_operations.json')+' · '+link('Workspace index','../README.md')+'.')
    write_new(OUT/'LINKED_MIND_WORKSPACES.md','# Linked MIND workspaces — preserved in place\n\nThe MIND was not inventoried or modified. Only its root README was read; prior chat records supply additional historical verification evidence. Use '+link('The MIND index','../The MIND/README.md')+' for canonical paper locations.\n\n| Existing sibling | Role and starting point | Current interpretation |\n|---|---|---|\n| Paper_U_Fresh_Referee_2026-09-29 | '+link('Original fresh referee report','../Paper_U_Fresh_Referee_2026-09-29/00_FINAL_REFEREE_REPORT.md')+' | Original v0.3 source/review recovered; The MIND owns the reading collection. |\n| Paper_U_Independent_Review_2026-09-29 | '+link('Rebuilt package','../Paper_U_Independent_Review_2026-09-29/Paper_U_Complete_Rebuilt.zip')+' | Reconstructed review documents explicitly labelled; preserve alongside original fresh review. |\n| Structured Factorization | '+link('Latest local revision report','../Structured Factorization/live_integration_revision_2026-09-30/REVISION_REPORT.md')+' | Active workflow: later live-PySDD integration audit/repair follows frozen Phase 5B. No workflow files modified. |\n\nThe MIND README recommends Phase 5B as its collection status, while the live sibling now has September 30 development/audit results. The live chat qualifies its earlier algorithmic NO-GO: the first dataset had no additional factor headroom, and the next gate is capped-worker/larger-SDD checking. This does not establish publication novelty or replace the frozen campaign. The MIND index may need a future refresh by its owner; it was left untouched.\n\nGeneral ProLT Observation Refinement also stays in place: it is shared precursor research referenced by The MIND. No additional MIND manuscript home was created here.\n\n**Exact duplicate evidence:** the prior “Organize The MIND research” chat reported SHA-256 identity for Paper U v0.3 TeX (`7c50938b401468d412f3df3d7d5b0765bf3aec8af4bc17c8d32983bc55e69c30`) and bibliography (`401a939eb529b727e3918cbd1e3563899ac32b2dc31dbf16aaa19cc471c22646`) against its rebuilt MIND copy. The original and rebuilt PDFs differ. The current sibling hashes have been rechecked; MIND-side bytes were not reread under this task’s scope. Other MIND overlaps are reported lineage/copy relationships, not newly measured exact duplicate claims. See '+link('prior verification transcript','mind_prior_verification_evidence.json')+' and '+link('machine-readable overlap map','mind_overlap_map.json')+'.')
    # Website PDFs are compared by hash later in reconciliation; no PDF is moved.
    write_new(ROOT/'B-Theory Website/COLLECTION_README.md','# Website delivery copies\n\nThese four PDFs are delivery artifacts, not four new manuscript homes. They remain at their original paths. The exact duplicate mapping is in '+link('website delivery mappings','../00_Collection_Index/website_delivery_map.json')+'.\n\n- `CM_LM_Boolean_Operator_Calculus_Revised.pdf`: FO / CM–LM foundations.\n- `Characteristic-Two Modal Computation.pdf`: P02; compare its hash before assuming it is the current final gate PDF.\n- `binary_order_thinning_finite_posets_reviewed_v3.pdf`: BT / ProLT-Homology.\n- `ProLT_Observation_Topologies_Submission_v0.9_FINAL.pdf`: PL / ProLT exposition.\n\nUse the '+link('workspace index','../README.md')+' and paper guides to select current sources. Publication/upload state is not inferred from this folder’s name. No website was changed.')
    print('Wrote 16 paper/program guides and collection navigation.')
if __name__=='__main__':main()
