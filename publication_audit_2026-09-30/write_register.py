from pathlib import Path
import hashlib, html, json

WORK=Path(__file__).resolve().parent.parent
SITE=WORK/'sf-site-release/deliverables_n22_24/master_explainer_2026_08_03'
OUT=SITE/'results/2026-09-30/research-register'
rows=[]
def row(identity,date,status,finding,evidence,next_step):
    rows.append(dict(id=identity,date=date,status=status,finding=finding,evidence=evidence,next_step=next_step))

row('P1–P13 / P7B and September 18 audit','2026-09-18','COMPLETED; DIRECT CROSSOVER NOT ESTABLISHED',
    'Includes the original per-phase source/results and the audit, Gate A S1/S2 context, replay runtimes, and diagnostic results. These are completed experiments, not the open tasks described by some historical prompts.',
    ['p-series/P1_P13_source_results_and_audit.zip','p-series/AUDIT_REPORT.md','p-series/EXECUTIVE_VERDICT.md'],
    'Do not restart the unchanged sequence. Reproduction in a new directory or a materially new algorithm requires a stated purpose and separate run identity.')
row('P14 exact dispatcher','2026-09-18','COMPLETED; NO-GO',
    '51,102 timing rows and 2,455 memory observations. Exact/direct ratios 1.0508 synthetic and 1.0607 natural. Five synthetic and zero natural encodings selected folding. September 26 replay reproduced all 17 archived interval sets; exact historical imported-runtime identity remains unresolved.',
    ['p-series/P14_EXECUTION_REPORT.md','p-series/P14_frozen_trial.zip','compiler/03_STUDY_DESIGN_20260926/P14_RUNTIME_IDENTITY_NEXT_STEPS.md'],
    'No unchanged P14-PY1 replication is recommended. Preserve the runtime-identity limitation; reproducing compatible code cannot establish historical byte identity.')
row('P15 late scan','2026-09-21','CLOSED; SEMANTICS PASS / TIMING INCONCLUSIVE',
    '490 accepted fresh semantic cases and 2,450 memory observations; zero accepted timing worker artifacts. Invalid Python 3.10 evidence, host drift, v3 and v4 aborts are retained with the final disposition.',
    ['p-series/P15_FINAL_DISPOSITION_20260921.json','p-series/P15_closed_trial.zip'],
    'Do not extend the observed cap or resume the frozen run. Any new resource design needs prospective preregistration and a fresh freeze; no performance loss or win is inferred here.')
row('Gate A contract audit and Protocol v4 WSL pilots','2026-09-23','QUALIFICATION COMPLETE; STABILITY NO-GO',
    '147 focused tests, 95 boundary tests, 20 adversarial tests, 333,794 finite checks, native CUDD 1,000/1,000 and ABC 142/142. Four WSL pilots failed 17, 56, 14 and 20 of 200 controls. Confirmatory ledgers remained empty.',
    ['gate-a-v4/GATE_A_V4_REQUALIFICATION_REPORT_A_N.md','gate-a-v4/Gate_A_V4_NO_GO_Qualification_Package.zip'],
    'Read alongside the later v5 redesign. These timing controls are qualification evidence, not a measured CM/direct performance campaign.')
row('Gate A v4 Runpod setup attempts','2026-09-23–24','SETUP FAILURES; NO TIMING RESULT',
    'Retain the separate authentication-only preflight, supply failures, unreachable receiver, shell/image and relay failures. Identically dated local attempt names belong to different task roots; they are not duplicate measurements.',
    ['gate-a-v4/separate-auth-preflight/RUNPOD_PILOT_REPORT.md']+[f'gate-a-v4/pilot-v4-runpod-{n}/RUNPOD_STABLE_HOST_PILOT_REPORT.md' for n in ['20260923-01','20260923-02','20260924-01','20260924-02']],
    'Do not count setup failures as algorithm trials or reuse closed attempt authorizations.')
row('Gate A v4 completed Runpod pilot 20260924-03','2026-09-24','COMPLETED; STABILITY NO-GO',
    '194/200 controls passed, six failed; zero timer-overhead failures. The 0.05 rule was unchanged. Raw exploratory and environment evidence is preserved. No relative-arm performance conclusion or confirmatory run was made.',
    ['gate-a-v4/pilot-v4-runpod-20260924-03/RUNPOD_STABLE_HOST_PILOT_REPORT.md','gate-a-v4/completed-runpod-scientific-evidence.zip'],
    'Do not run another unchanged paid v4 pilot. The task moved to prospective v5 design; original host limitations do not waive this failed result.')
row('Gate A Protocol v5 repair candidate','2026-09-24','DESIGN / UNTIMED TESTS COMPLETE; PERFORMANCE UNEXECUTED',
    'Median-of-nine fresh-process design; 61 v5 tests, 147 source tests, 95 boundary tests and 333,794 finite checks passed. Six result templates remain empty. Proposed 19,800-worker stability pilot is not a completed experiment.',
    ['gate-a-v5/REVIEW_REPORT_V5.md','gate-a-v5/PROTOCOL_V5.md','gate-a-v5/Gate_A_V5_Candidate_20260924_01_NO_GO.zip'],
    'Candidate was adopted in the later hosting preparation, but Gate A remains NO-GO. A qualified host, new binding and explicit capped authorization are prerequisites to any new pilot.')
row('Gate A v5 Vultr attempt and later control phase','2026-09-24–25','TERMINAL SETUP FAILURE; SUCCESSOR BLOCKED',
    'pilot-v5-vultr-ewr-20260924-01 never reached SSH/qualification: zero launcher invocations and zero observations. A distinct prospective API attempt was prepared; the no-cost control phase did not complete authenticated probing. No completed v5 stability result exists.',
    ['gate-a-v5/HOSTING_OUTCOME_PUBLIC.md'],
    'The first identity is closed, not resumable. Resolve provider visibility/teardown and host qualification before any separately authorized new identity. No current account-state claim is made from historical records.')
row('Compiler contract revision / publication audit','2026-09-26','REVISION AND CHECKS COMPLETE; PUBLICATION LIMITS RETAINED',
    'Revised manuscript, audit/reconciliation and pinned source retained; 123 selected tests passed in the recorded clean environment. Later experiments do not confer peer review, novelty or broad performance approval.',
    ['compiler/Operator_Level_CM_Compiler_Revised_Draft.pdf','compiler/02_CONTRACT_REVISION_20260926/REVIEW_RESPONSE.md','compiler/Compiler_Studies_20260926_Publication.zip'],
    'Use the revised manuscript with its negative empirical boundaries. Historical review scores refer to their dated drafts, not an updated publication verdict.')
row('Compiler synthetic study Protocol v4 run_v4_001','2026-09-26','COMPLETED; PRIMARY UTILITY FAILED',
    '64 held-out unshared two-variable formulas, N=U=1023; 3,840 timing and 128 memory rows. Direct-packed/CM ratio 0.2479026, interval [0.2461628, 0.2494730]. Eight-formula disjoint pilot excluded. This is a separate protocol family from Gate A v4/v5.',
    ['compiler/03_STUDY_DESIGN_20260926/README.md','compiler/Compiler_Studies_20260926_Publication.zip'],
    'Do not repeat merely to search for a passing primary result. The measured cache-reset token-output boundary excludes process startup, sharing, natural circuits and prepared reuse.')
row('Compiler natural admission and correctness','2026-09-26','COMPLETED; CORRECTNESS PASS',
    '2,861 EPFL primary outputs screened; 71 admitted across ten designs. All 71 exhaustive agreements and ABC AIG checks passed; hybrid outcomes: four pure roots, one retabulation, 66 fallbacks. Frozen references to nine designs are clerical errors, disclosed by the later report.',
    ['compiler/04_NATURAL_CIRCUIT_EXTENSION_20260926/README.md','compiler/05_NATURAL_TIMING_20260926/README.md','compiler/Compiler_Studies_20260926_Publication.zip'],
    'The admission/correctness phase was followed by the next row. Its historical “no natural arm was timed” statement describes this phase only, not the final project state.')
row('Compiler natural secondary Protocol v5 run 001','2026-09-26','CLOSED INCOMPLETE; DESCRIPTIVE NEGATIVE RESULT',
    '70/71 complete paired cases, 2,100 timing rows, 142 memory rows, 1,065 ABC rows; one retained calibration shortfall. Median direct/CM producer ratio 0.0376112; all 70 complete cases favor direct. ABC subprocess wall is a different endpoint. This is NOT the Gate A v5 repair pilot.',
    ['compiler/05_NATURAL_TIMING_20260926/README.md','compiler/Compiler_Studies_20260926_Publication.zip'],
    'Do not fill the missing case by changing the frozen calibration rule. Other protocol-v3 secondary cells remain open, not implicitly completed or authorized.')
row('Structural computation baseline C01–C12 and convergence preparation N01–N14','2026-09-26–28','COMPLETED; FOLLOWED BY T3 PHASE 2',
    'Independent oracle, baseline replays, coordinate/update checks, 20-design source freeze, packed/CUDD correctness and lifecycle preparation preserved. Historical lifecycle replay: 38 cases, 570 trials, zero artifact wins versus packed. Prior delivery contains 4,912 manifest entries.',
    ['convergence-preparation/COMPUTATION_LEDGER.md','convergence-preparation/HANDOFF_TO_MASTER.md','t3/CM_Structural_Computation_C1-C4_T3_Phase2_2026-09-28.zip'],
    'The prior handoff’s C2 hold was subsequently addressed by the following frozen T3 campaign; do not restart preparation as if T3 never ran. Full prior package is nested as PRIOR_PHASE_PACKAGE.zip.')
row('Structural computation T3 Phase 2 / C1–C4','2026-09-28','COMPLETED; CORRECTNESS SUPPORTED / GENERAL SPEEDUP NOT ESTABLISHED',
    '7,445,928 campaign queries and 70,662 updates passed. Main 16,752 PASS trials plus 400 dense-cap exclusions; complement 3,072 PASS; cold and isolated memory each 115 PASS plus five cap exclusions. Nine of 32 dense-criterion-favorable case/depth pairs did not beat actual serialized raw-factor bytes. Packed binary retained lower lifecycle design medians on every natural timing design.',
    ['t3/HANDOFF_TO_MASTER.md','t3/DESIGN_LEVEL_RESULTS.md','t3/MINIMIZED_COUNTEREXAMPLES.md','t3/CM_Structural_Computation_C1-C4_T3_Phase2_2026-09-28.zip'],
    'Next gate is theory/computation convergence and precise finite-size claims, not an unchanged rerun. Correctness does not establish priority or universal runtime advantage.')
row('Structured factorization Phase 5B through repaired live integration','2026-09-29–30','COMPLETED; MECHANISM GO / ALGORITHMIC NO-GO',
    'Original Phase 5B negative result; supported live local moves; first 756-trial integration; independent audit; repaired developmental controls and Linux hostile checks; separate new 756-trial campaign. Final L1/B2 complete-time ratio 1.0379849; upper 1.1415416. Four held-out factor-exposure gains do not establish total-time improvement.',
    ['../structured-factorization/index.html','../structured-factorization/artifact-manifest.json'],
    'Preserve the frozen campaigns. Reproduction or a new algorithm requires its own labeled scope; cheaper moves alone do not justify repetition.')
row('Earlier general benchmark and proposed 80-family catalog','2026-09-13–22','PUBLISHED RESULTS PLUS UNEXECUTED PROPOSALS',
    'Existing findings, exact-count/decomposition, post-integration, feature-model, SymPy, biology and neural pages retain their endpoint-specific results. The 80-family catalog is a proposal, not evidence that all 80 families ran; no broad general CM advantage follows.',
    ['../../../findings.html','../../../latest-results.html','../../../learning-neural-evidence.html','https://github.com/Relative0/Correspondence_Matrices/blob/main/docs/research/cm-benchmark-research-2026-09-13/CATALOG.md'],
    'Check actual result records before selecting a proposed cell. Client-specific replay or genuinely new algorithms remain possible; old catalog prompts are not launch authorization.')

payload={'schema':'cm-cross-track-experiment-register/v1','reviewed':'2026-09-30','scope':'CM computation trials and publication artifacts identified through the CMs task group, their source packages, and the structured-factorization task. Not a claim to inventory every unrelated chat or private external service.','execution_policy':'Historical commands, repair prompts and authorizations are provenance, not a queue. Never overwrite or resume closed frozen runs. Reproduction uses a new directory and identity. New methods need a new prospective protocol and applicable authorization.','studies':rows}
(OUT/'experiment-register.json').write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
(OUT/'gate-a-v5/HOSTING_OUTCOME_PUBLIC.md').write_text('''# Gate A v5 hosting outcome — historical public summary

The adopted candidate was not performance-qualified. The authorized `pilot-v5-vultr-ewr-20260924-01` reached a pending provider state, disappeared before SSH/host qualification, and closed as a terminal setup failure. There were **zero pilot launcher invocations and zero performance observations**. The recorded closeout showed no active servers and no retained task credentials. This is historical evidence, not a fresh account audit.

A distinct `pilot-v5-vultr-api-ewr-20260925-02` prospective package was prepared. Its no-cost control phase recorded public availability information and provider clarification that capacity disappeared during the earlier deployment. Required authenticated account probes and operational assurances remained incomplete. No successor performance run occurred. Gate A remained **NO-GO**.

The original candidate review's “none selected / adoption required” language precedes host selection and adoption. Those administrative steps occurred; host qualification and timing did not. A selected host class is not a qualified live host.

The original attempt and prospective-control archives, provider account details, support correspondence and account-access records are preserved locally in the originating Protocol v5 task. They are not included in this public research release. This summary is an editorial derivative of their review reports and terminal records; it is not a replacement raw provider receipt. The scientific candidate ZIP is published unchanged.

Do not reuse the closed attempt's authorization or resume its identity. Any new attempt requires resolved provisioning/teardown risks, qualified host evidence, a fresh binding and explicit cost authorization. No infrastructure was queried or launched in this publication audit.
''',encoding='utf-8')

audit='''# Cross-track publication and trial-accounting audit — 30 September 2026

The first September 30 upload covered only the structured-factorization branch. This follow-up found additional completed studies and blocked qualification work. It adds a register and public evidence rather than launching experiments.

## Reviewed scope and reconciliation

- Read the CMs tasks **Complete Protocol v5 repair**, **Run Gate A contract audit**, **Runpod v4 timing-stability pilot**, **Audit CM theory and computation**, and **80 Benchmarks thread**, plus **Gluing** for the factorization predecessor. Reviewed the remaining CMs task summaries/final records: video work and worktree preservation are not new computation trials. No messages were sent to other tasks.
- Inspected the September 18 P1–P13 audit, P14 and P15 saved trials; September 23–25 Gate A packages; September 26 compiler audit/revision and synthetic/natural studies; September 28 convergence/T3 handoffs; and the already-published September 29–30 factorization archive.
- Compared these against the deployed P-series records and repository. Earlier findings and proposed benchmark catalogs remain linked; the new register does not claim every proposed catalog item executed.
- Reconciled temporal conflicts: P14 draft is followed by its negative execution; P15 aborts remain closed; Gate A v5 adoption/host selection followed candidate design but produced no timing; natural admission was followed by a separate secondary timing study; convergence preparation's C2 hold was followed by completed T3 Phase 2.
- **Two different Protocol v5 families exist.** Gate A fresh-process stability qualification remains unexecuted. The compiler natural secondary v5 study ran and closed with one calibration failure. Neither replaces the other.
- Corrected navigation uses ten natural designs, while preserving frozen files with the disclosed nine-design clerical error. Retained the historical P14 imported-runtime identity gap. No new novelty, peer-review or general performance approval is asserted.

## Preservation and distribution boundaries

Original Gate A v4 and v5 candidate ZIPs and the full T3 Phase 2 ZIP are byte-preserved. T3 contains its 4,912-file prior convergence delivery and baseline/theory evidence. P-series and compiler ZIPs are new publication snapshots: their embedded PUBLICATION_CONTENTS.json gives member hashes; original source/result bytes are unchanged. Original naming and directory layout are retained inside each ZIP.

The compiler snapshot omits the third-party Windows ABC executable and five DLLs because the source package explicitly leaves their public redistribution review unresolved. Source/tool version and hash provenance, inputs, AIGs and recorded measurements are retained. These binary omissions are enumerated in publication-exclusions.json. Reproduction must obtain the documented tool distribution separately; do not treat a missing binary as a new unperformed experiment.

Provider account-access material, support correspondence, credentials, temporary environments/caches and the redundant 194 MB repository download are not published. The v5 hosting outcome is represented by a labeled public summary. Task-private account records remain local; no secret store was accessed. Generic token/private-key pattern scans are supplementary checks, not a guarantee against every possible sensitive string.

## How to use this archive

Read experiment-register.json or index.html before old prompts, READMEs or commands. A historical “next step” may already have been completed by a later row. Completed and failed studies are not an execution queue. Reproduction must be labeled and isolated; a new algorithm or changed resource/measurement design requires a new protocol and run identity. This publication grants no new compute budget or service authorization.

Archive the present chat after the publication commit and public downloads are verified. The repository, experiment register, artifact manifests and this report carry the essential state. Account-control work belongs to the original v5 task if deliberately resumed; the broader research decision belongs to a new, explicitly scoped task. Nothing in this archival audit requires another benchmark run.
'''
(OUT/'AUDIT_REPORT.md').write_text(audit,encoding='utf-8')
inventory=json.loads((WORK/'publication_audit_2026-09-30/source_inventory.json').read_text())
(OUT/'publication-exclusions.json').write_text(json.dumps({'omitted_files':inventory['exclusions'],'other_omissions':['Provider account-access records and private correspondence: local preservation plus public outcome summary.','Temporary environments and caches; redundant source download; no secrets accessed.']},indent=2)+'\n',encoding='utf-8')

style='body{font:17px/1.6 system-ui,sans-serif;background:#f5f7fb;color:#172b3a;margin:0}main{max-width:1080px;margin:auto;padding:32px 24px}a{color:#075f91}h1{line-height:1.2}article,.notice{background:white;border:1px solid #ccd7e3;border-radius:12px;padding:22px;margin:22px 0}.status{font-size:13px;font-weight:700;letter-spacing:.04em;color:#744119}li{margin:5px 0}.notice{border-left:5px solid #075f91}footer{margin-top:40px}nav a{margin-right:14px}'
parts=['<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CM experiment register — completed trials and remaining gates</title><style>'+style+'</style></head><body><main>',
 '<nav><a href="../../../p-series-study-guide.html#research-register">Study guide</a><a href="experiment-register.json">Register JSON</a><a href="artifact-manifest.json">SHA-256 manifest</a><a href="AUDIT_REPORT.md">Publication audit</a></nav>',
 '<h1>Completed trials and remaining gates</h1><p>Cross-track research register · reviewed 30 September 2026</p>',
 '<div class="notice"><strong>Read this before running an old command.</strong><p>These are historical records, not a launch queue. Completed, failed and inconclusive runs stay closed. Reproduction belongs in a new directory; new algorithms or changed measurement rules need a new protocol and run identity.</p><p><strong>“Protocol v5” is ambiguous:</strong> Gate A stability repair has no performance observations. The separate September 26 natural secondary study has measured, negative descriptive results and one retained failure.</p></div>']
for i,r in enumerate(rows):
 parts.append(f'<article id="study-{i+1}"><p class="status">{html.escape(r["date"])} · {html.escape(r["status"])}</p><h2>{html.escape(r["id"])}</h2><p>{html.escape(r["finding"])}</p><p><strong>Disposition:</strong> {html.escape(r["next_step"])}</p><ul>')
 for link in r['evidence']:parts.append(f'<li><a href="{html.escape(link,quote=True)}">{html.escape(Path(link).name)}</a></li>')
 parts.append('</ul></article>')
parts.append('<footer><p>Downloadable evidence is for inspection and reproduction, not publication approval. The compiler tool binaries listed in <a href="publication-exclusions.json">distribution omissions</a> remain local. Provider account records are summarized, not published. See the <a href="AUDIT_REPORT.md">audit scope and preservation report</a>.</p></footer></main></body></html>')
(OUT/'index.html').write_text('\n'.join(parts)+'\n',encoding='utf-8')

template=SITE/'cm_p_series_study_guide_template.html'
text=template.read_text(encoding='utf-8')
if 'section("research-register"' not in text:
 text=text.replace('["#structured-factorization", "Factorization"]','["#research-register", "All recent trials"], ["#structured-factorization", "Factorization"]')
 marker='{\n  const s = section("structured-factorization"'
 insertion='''{
  const s = section("research-register", "All recent trials: completed work and remaining gates", "Cross-track register updated 30 September 2026",
    "The P-series is one research line. Gate A v4/v5 qualification, the September 26 compiler studies, September 28 T3 experiments and structured factorization have separate protocols and conclusions.");
  s.append(h("div", { class: "boundary-strip" }, [
    h("h2", { text: "Check the register before acting on an old next-step prompt" }),
    h("p", { text: "P1–P14 completed without a general direct-baseline crossover; P15 accepted no timing artifacts. Gate A v5 has tested repair code but no performance pilot. The separate compiler natural v5 study ran: 70 complete cases favored direct packed and one calibration failure remains. T3 correctness passed, but a broad best-comparator runtime advantage was not established." }),
    h("p", {}, [h("a", { href: "results/2026-09-30/research-register/index.html", text: "Open the experiment register and downloadable evidence" })]),
  ]));
  app.append(s);
}

'''
 assert marker in text
 text=text.replace(marker,insertion+marker)
 text=text.replace('This site identifies it for traceability but does not yet publish the P1–P14 raw audit bundles as downloadable artifacts.','The cross-track experiment register now links downloadable P1–P15 source and evidence snapshots; historical runtime-identity limitations remain explicit.')
 text=text.replace('Enough context to understand the protocol, without inventing a public raw bundle','Public evidence snapshots, with historical limitations retained')
 start='A reader can now trace every phase\'s implementation delta'
 a=text.index(start);b=text.index('");',a)
 text=text[:a]+'The September 30 cross-track register publishes P1–P13 source/results and audit evidence, P14 frozen trials and P15 closed-trial artifacts. Historical prompts remain as provenance. Read the dated register first: some proposed next steps were later executed, while blocked qualifications and unmeasured secondary cells remain explicitly unresolved.'+text[b:]
 text=text.replace('Before treating this as a rerun package','Before reproducing a trial')
 text=text.replace('Publish a reviewed, privacy-safe source bundle for each phase: preregistration, code revision, frozen inputs, command line, environment manifest, raw records, analysis, and a checksum manifest.','Use the linked publication snapshots and manifests in a separate directory. Do not overwrite or resume frozen runs, change old calibration limits, or reinterpret unavailable timing as a performance result.')
 text=text.replace('That future publication work must be separately reviewed; it is not implied by this reader guide.','The register records source/runtime gaps and distribution omissions. A changed algorithm or resource design requires a new protocol and identity.')
 text=text.replace('P-series study guide reviewed 2026-09-22','P-series guide and cross-track register reviewed 2026-09-30')
 template.write_text(text,encoding='utf-8',newline='\n')
 # Regenerate through the same substitutions as the repository verifier.
 old=(SITE/'p-series-study-guide.html').read_text(encoding='utf-8')
 # The previous generated head embeds CSS and DATA; only the final app script and meta are changed here.
 old_start=old.index('const app = document.getElementById("app");')
 new_start=text.index('const app = document.getElementById("app");')
 (SITE/'p-series-study-guide.html').write_text(old[:old_start]+text[new_start:],encoding='utf-8',newline='\n')

manifest={}
for p in sorted(OUT.rglob('*')):
 if p.is_file() and p.name!='artifact-manifest.json':
  data=p.read_bytes();manifest[p.relative_to(OUT).as_posix()]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
(OUT/'artifact-manifest.json').write_text(json.dumps({'schema':'cm-research-register-artifacts/v1','reviewed':'2026-09-30','files':manifest},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'studies':len(rows),'artifacts':len(manifest),'bytes':sum(x['bytes'] for x in manifest.values())}))
