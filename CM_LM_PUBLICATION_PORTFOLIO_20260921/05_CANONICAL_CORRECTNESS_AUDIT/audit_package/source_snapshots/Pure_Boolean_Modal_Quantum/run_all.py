#!/usr/bin/env python3
"""Reproduce the pure-Boolean CM modal investigation and raw outputs."""
from __future__ import annotations

import csv, hashlib, json, os
from pathlib import Path

from src.analysis_core import (
    BASIS_X, BASIS_Y, BASIS_Z, DELTA, E0, MQT_BASES, MQT_NAMES,
    basis_permutation_classification, bell_support_coverage, bell_tables,
    bstar_teleportation_failure, gate_inventory, ghz_analysis,
    measurement_bases, offdiagonal_hardy_witnesses, smith_class_inventory,
    smith_modal_contextuality_inventory, teleportation_protocol, teleportation_resource_theorem,
    teleportation_resource_smith_summary, singular_teleportation_hierarchy, two_sat_all_bases,
    two_sat_support_coverage_all_bases, verify_known_structures,
)

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
LOGS = ROOT / "logs"
DATA.mkdir(exist_ok=True); LOGS.mkdir(exist_ok=True)


def write_csv(name, rows):
    path = DATA / name
    rows = list(rows)
    if not rows:
        path.write_text("", encoding="utf-8"); return path
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    return path


def write_json(name, obj):
    path = DATA / name
    path.write_text(json.dumps(obj, indent=2, sort_keys=True), encoding="utf-8")
    return path


def basis_rows(all_bases, unitary_bases):
    uset = set(unitary_bases)
    for idx,b in enumerate(all_bases):
        yield {
            "basis_id":idx,
            "effect0_a":b[0][0],"effect0_b":b[0][1],
            "effect1_a":b[1][0],"effect1_b":b[1][1],
            "intrinsic_unitary_projective_basis":int(b in uset),
        }


def main():
    known = verify_known_structures()
    gate_rows, GL, UNI, gates = gate_inventory()
    all_bases, unitary_bases = measurement_bases(GL,UNI)
    gates["projective_unordered_reversible_measurement_bases"] = len(all_bases)
    gates["projective_unordered_intrinsic_unitary_measurement_bases"] = len(unitary_bases)

    write_csv("gate_inventory_65536.csv", gate_rows)
    write_csv("measurement_bases_192.csv", basis_rows(all_bases,unitary_bases))

    bell_state = (E0,0,0,E0)
    bell_tab, bell_rows = bell_tables(bell_state)
    bell_globals = __import__("src.analysis_core", fromlist=["compatible_bell_globals"]).compatible_bell_globals(bell_state,MQT_BASES)
    write_csv("modal_bell_mqt_tables.csv", bell_rows)

    # Complete intrinsic-unitary projective basis family, exact support-locality.
    small_bell = {}
    for name,state in {
        "Phi_support":(E0,0,0,E0),
        "Psi_support":(0,E0,E0,0),
        "Bstar_beta00":(E0,0,0,DELTA),
    }.items():
        goods,unc = bell_support_coverage(state,unitary_bases)
        small_bell[name] = {"global_assignments":len(goods),"uncovered_possible_sections":len(unc)}

    beta_state = (E0,0,0,DELTA)
    beta_sat = two_sat_all_bases(beta_state,all_bases)
    beta_sat["measurement_basis_count_per_party"] = len(all_bases)
    beta_cov = two_sat_support_coverage_all_bases(beta_state,all_bases)
    beta_sat["support_coverage"] = beta_cov
    beta_sat["classification"] = "LOGICAL_CONTEXTUAL_NOT_STRONG" if beta_cov["satisfiable"] and beta_cov["uncovered_possible_sections"] else ("STRONG_CONTEXTUAL" if not beta_cov["satisfiable"] else "RELATIONALLY_LOCAL")
    write_json("bell_bstar_complete_reversible_basis_sat.json",beta_sat)

    modal_class_rows, modal_class_summary = smith_modal_contextuality_inventory(all_bases)
    hardy = offdiagonal_hardy_witnesses(all_bases)
    write_json("offdiagonal_hardy_witnesses.json", hardy)

    tele, tele_rows = teleportation_protocol()
    write_csv("teleportation_all_256_states_x4_outcomes.csv",tele_rows)
    write_json("teleportation_protocol.json",tele)
    bfail = bstar_teleportation_failure()
    write_json("bstar_teleportation_failure.json",bfail)

    state_inventory,class_rows,stateclass,separable,smith = smith_class_inventory(len(GL))
    tele_resource, tele_resource_rows = teleportation_resource_theorem(stateclass)
    tele_resource_classes = teleportation_resource_smith_summary(tele_resource_rows)
    write_csv("teleportation_resource_inventory_65536.csv", tele_resource_rows)
    write_csv("teleportation_resource_by_smith_class.csv", tele_resource_classes)
    write_json("teleportation_resource_theorem.json", tele_resource)
    tele_sub, tele_sub_rows = singular_teleportation_hierarchy()
    write_csv("singular_teleportation_hierarchy_by_smith_class.csv", tele_sub_rows)
    write_json("singular_teleportation_hierarchy.json", tele_sub)
    known["Bstar_basis_output_smith_classes"] = tuple(stateclass[tuple(v)] for v in known["Bstar_basis_outputs"])
    known["Bstar_basis_outputs_all_nonseparable"] = all(tuple(v) not in separable for v in known["Bstar_basis_outputs"])
    write_csv("state_local_class_inventory_65536.csv",state_inventory)
    write_csv("local_equivalence_classes.csv",class_rows)
    class_count = {(r["smith_a"],r["smith_b"]): r["state_count"] for r in class_rows}
    for r in modal_class_rows:
        r["state_count"] = class_count[(r["smith_a"],r["smith_b"])]
    write_csv("bell_contextuality_by_smith_class.csv", modal_class_rows)
    modal_class_summary["strong_contextual_states"] = sum(r["state_count"] for r in modal_class_rows if r["classification"] == "STRONG_CONTEXTUAL")
    modal_class_summary["logical_not_strong_states"] = sum(r["state_count"] for r in modal_class_rows if r["classification"] == "LOGICAL_CONTEXTUAL_NOT_STRONG")
    modal_class_summary["relationally_local_nonzero_states"] = sum(r["state_count"] for r in modal_class_rows if r["classification"] == "RELATIONALLY_LOCAL")
    modal_class_summary["degenerate_zero_states"] = sum(r["state_count"] for r in modal_class_rows if r["classification"] == "DEGENERATE_ZERO_EXCLUDED")
    perm_rows = basis_permutation_classification(separable)
    write_csv("two_party_basis_permutation_gates.csv",perm_rows)
    perm_summary = {
        "basis_permutations":len(perm_rows),
        "preserve_all_separable":sum(r["preserves_all_separable_states"] for r in perm_rows),
        "can_create_nonseparability":sum(r["can_create_nonseparability"] for r in perm_rows),
    }

    ghz,ghz_rows = ghz_analysis(MQT_BASES,MQT_NAMES,E0,E0)
    ghzd,ghzd_rows = ghz_analysis(MQT_BASES,MQT_NAMES,E0,DELTA)
    write_csv("ghz_support_mqt_contexts.csv",ghz_rows)
    write_csv("ghz_delta_mqt_contexts.csv",ghzd_rows)

    ub_names = tuple(f"U{i}" for i in range(len(unitary_bases)))
    ghz_u,_ = ghz_analysis(unitary_bases,ub_names,E0,E0)
    ghzd_u,_ = ghz_analysis(unitary_bases,ub_names,E0,DELTA)
    ghz_summary = {
        "support_GHZ_MQT":ghz,
        "delta_GHZ_MQT":ghzd,
        "support_GHZ_all_intrinsic_unitary_projective_bases":ghz_u,
        "delta_GHZ_all_intrinsic_unitary_projective_bases":ghzd_u,
    }
    write_json("ghz_hidden_variable_search.json",ghz_summary)

    summary = {
        "scope":"pure Boolean CM coefficient ring only; integer counts are external diagnostics",
        "known_structure_regressions":known,
        "gate_classification":gates,
        "modal_bell":{
            "state":"E0|00> XOR E0|11>",
            "settings_per_party":["Z","X","Y"],
            "deterministic_global_assignments_checked":64,
            "compatible_global_assignments":len(bell_globals),
            "strong_modal_contradiction":len(bell_globals)==0,
            "tables":{"/".join(k):v for k,v in bell_tab.items()},
            "complete_intrinsic_unitary_family":small_bell,
            "Bstar_beta00_complete_192_reversible_basis_contextuality":beta_sat,
            "complete_192_basis_smith_class_contextuality":modal_class_summary,
            "offdiagonal_hardy_witness_count":len(hardy),
        },
        "teleportation":{
            "universal_protocol_exact_checks":tele["checks"],
            "universal_protocol_branch_maps":tele["branch_maps"],
            "Bstar_resource_branch_determinants":bfail["branch_determinants"],
            "Bstar_resource_universal":bfail["all_branch_maps_invertible"],
            "resource_theorem":tele_resource,
            "resource_smith_classes":tele_resource_classes,
            "singular_resource_hierarchy":tele_sub,
            "singular_resource_hierarchy_by_class":tele_sub_rows,
        },
        "local_equivalence":smith,
        "basis_permutation_gates":perm_summary,
        "GHZ":ghz_summary,
    }
    (LOGS/"run_summary.json").write_text(json.dumps(summary,indent=2,sort_keys=True),encoding="utf-8")
    print(json.dumps(summary,indent=2,sort_keys=True))

if __name__ == "__main__":
    main()
