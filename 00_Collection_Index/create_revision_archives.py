"""Create verified, per-revision convenience ZIPs without changing source folders.

This is a one-time, explicit selection of revisions without a separate local ZIP.
Existing original delivery ZIPs remain untouched. Do not use this as a general
workspace cleanup command or rerun it to overwrite completed archives.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import zipfile

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "00_Collection_Index"

# Each tuple is (paper home, new ZIP name, folder to archive or file list).
PLAN = [
    ("CM Computation", "CM_Compiler_2026-09-22.zip", "01_CURRENT_REVISED_COMPILER_AND_REVIEW_20260922"),
    ("ProLT", "ProLT_core_v0.6.zip", "HISTORY/CORE_V0_6"),
    ("ProLT", "ProLT_core_v0.8.zip", "HISTORY/CORE_V0_8"),
    ("Signed Integral CM Phase Calculus", "CM_Phase_Calculus_original_manuscript.zip", "CURRENT_MANUSCRIPT"),
    ("Intrinsic Boolean CM Phase Algebra", "Intrinsic_Boolean_CM_Phase_original_manuscript.zip", "CURRENT_MANUSCRIPT"),
    ("CM Structural Computation and Decomposition (Research Direction)", "CM_Structural_Computation_Draft1_v1.zip", "CM_Structural_Computation_Final_Research_Package/manuscripts/v1"),
    ("CM Structural Computation and Decomposition (Research Direction)", "CM_Structural_Computation_Draft2_v2.zip", "CM_Structural_Computation_Final_Research_Package/manuscripts/v2"),
    ("General ProLT Observation Refinement (Research Direction)", "ProLT_Homological_Foundations_v0.1.zip", [
        "01_RESEARCH_NOTES/ProLT_Homological_Foundations_v0.1.tex",
        "01_RESEARCH_NOTES/ProLT_Homological_Foundations_v0.1.pdf",
    ]),
    ("General ProLT Observation Refinement (Research Direction)", "ProLT_Observation_Refinement_Classification_v0.2.zip", [
        "01_RESEARCH_NOTES/ProLT_Observation_Refinement_Classification_v0.2.tex",
        "01_RESEARCH_NOTES/ProLT_Observation_Refinement_Classification_v0.2.pdf",
    ]),
    ("General ProLT Observation Refinement (Research Direction)", "ProLT_Controlled_Refinement_Regimes_v0.3.zip", [
        "OBSERVATION_DESIGN_AND_SAFE_REFINEMENT/HISTORY/WORKING_NOTES/ProLT_Controlled_Refinement_Regimes_v0.3.tex",
        "OBSERVATION_DESIGN_AND_SAFE_REFINEMENT/HISTORY/WORKING_NOTES/ProLT_Controlled_Refinement_Regimes_v0.3.pdf",
    ]),
    ("General ProLT Observation Refinement (Research Direction)", "ProLT_Homotopy_Preserving_Observations_v0.4.zip", [
        "OBSERVATION_DESIGN_AND_SAFE_REFINEMENT/HISTORY/WORKING_NOTES/ProLT_Homotopy_Preserving_Observations_v0.4.tex",
        "OBSERVATION_DESIGN_AND_SAFE_REFINEMENT/HISTORY/WORKING_NOTES/ProLT_Homotopy_Preserving_Observations_v0.4.pdf",
    ]),
    ("General ProLT Observation Refinement (Research Direction)", "ProLT_Simultaneous_Observation_Refinement_v0.5.zip", [
        "OBSERVATION_DESIGN_AND_SAFE_REFINEMENT/HISTORY/WORKING_NOTES/ProLT_Simultaneous_Observation_Refinement_v0.5.tex",
        "OBSERVATION_DESIGN_AND_SAFE_REFINEMENT/HISTORY/WORKING_NOTES/ProLT_Simultaneous_Observation_Refinement_v0.5.pdf",
    ]),
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def selected_files(home: Path, selection: str | list[str]) -> list[tuple[Path, str]]:
    if isinstance(selection, str):
        source = home / selection
        if not source.is_dir() or source.is_symlink():
            raise RuntimeError(f"Unsafe or missing source directory: {source}")
        files = sorted((p for p in source.rglob("*") if p.is_file()), key=lambda p: p.as_posix())
        chosen = [(p, f"{source.name}/{p.relative_to(source).as_posix()}") for p in files]
    else:
        chosen = []
        for rel in selection:
            p = home / rel
            if not p.is_file():
                raise RuntimeError(f"Missing source file: {p}")
            chosen.append((p, f"{Path(rel).stem.rsplit('_v', 1)[0]}_v{Path(rel).stem.rsplit('_v', 1)[1]}/{p.name}"))
    if not chosen:
        raise RuntimeError(f"Empty revision selection in {home}")
    names = set()
    for p, member in chosen:
        if p.is_symlink() or not p.resolve().is_relative_to(home.resolve()):
            raise RuntimeError(f"Unsafe source path: {p}")
        parts = PurePosixPath(member).parts
        if not parts or ".." in parts or member.startswith("/") or member in names:
            raise RuntimeError(f"Unsafe or duplicate member name: {member}")
        names.add(member)
    return chosen


def create_one(home_rel: str, name: str, selection: str | list[str]) -> dict:
    home = ROOT / home_rel
    archive_dir = home / "Revision_Archives"
    target = archive_dir / name
    partial = archive_dir / f"{name}.partial"
    if target.exists() or partial.exists():
        raise RuntimeError(f"Archive already exists; never overwrite: {target}")
    chosen = selected_files(home, selection)
    before = [
        {"source": p.relative_to(ROOT).as_posix(), "member": member, "size": p.stat().st_size, "sha256": sha256(p)}
        for p, member in chosen
    ]
    archive_dir.mkdir(exist_ok=True)
    with zipfile.ZipFile(partial, mode="x", compression=zipfile.ZIP_DEFLATED, compresslevel=6, allowZip64=True) as archive:
        for (p, member), record in zip(chosen, before):
            archive.write(p, arcname=member)
            if p.stat().st_size != record["size"] or sha256(p) != record["sha256"]:
                raise RuntimeError(f"Source changed while archiving: {p}")
    with zipfile.ZipFile(partial) as archive:
        if archive.testzip() is not None or set(archive.namelist()) != {r["member"] for r in before}:
            raise RuntimeError(f"ZIP integrity or member-set failure: {partial}")
        for record in before:
            with archive.open(record["member"]) as stream:
                digest = hashlib.sha256()
                size = 0
                for block in iter(lambda: stream.read(4 * 1024 * 1024), b""):
                    digest.update(block)
                    size += len(block)
            if digest.hexdigest() != record["sha256"] or size != record["size"]:
                raise RuntimeError(f"ZIP member differs from source: {record['member']}")
    os.rename(partial, target)
    return {
        "archive": target.relative_to(ROOT).as_posix(),
        "archive_size": target.stat().st_size,
        "archive_sha256": sha256(target),
        "selection": selection,
        "members": before,
        "source_folders_retained": True,
    }


def main() -> None:
    results = [create_one(*entry) for entry in PLAN]
    receipt = {
        "created_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "policy": "Separate older revision ZIPs; original delivery ZIPs and loose source folders retained; current reading heads remain unpacked.",
        "archives": results,
    }
    path = OUT / "REVISION_ARCHIVES_2026-09-30.json"
    if path.exists():
        raise RuntimeError(f"Receipt already exists: {path}")
    path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"archives": len(results), "members": sum(len(r["members"]) for r in results), "archive_bytes": sum(r["archive_size"] for r in results)}, indent=2))


if __name__ == "__main__":
    main()
