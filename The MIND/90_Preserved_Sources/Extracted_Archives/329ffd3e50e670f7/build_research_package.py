"""Validate and package this gate's new research, leaving sources unchanged."""
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent
REQUIRED = [
    "HEIGHT2_ADAPTIVE_MASTER_AUDIT.md", "FORMAL_ADAPTIVE_MODEL.md",
    "BRANCH_CANCELLATION.md", "REPAIR_GRAPH_DYNAMICS.md",
    "QUERY_ACTIVATION_DEACTIVATION.md", "FIXED_LIBRARY_IDENTIFICATION.md",
    "ADAPTIVE_DEPTH_THEORY.md", "COMPLEXITY_AUDIT.md",
    "MATROID_INTERPRETATION.md", "STRUCTURED_LIBRARY_RESULTS.md",
    "LITERATURE_PRIORITY_AUDIT.md", "HOSTILE_REFEREE_REPORTS.md",
    "MAIN_THEOREM.md", "COUNTEREXAMPLES.md", "OPEN_PROBLEMS.md",
    "HANDOFF_TO_MASTER.md",
]
DATA = [
    "HEIGHT2_POSETS.csv", "QUERY_REPAIR_SAFETY.csv", "SAFETY_TRANSITIONS.csv",
    "FIXED_LIBRARY_RESULTS.csv", "ADAPTIVE_DEPTHS.csv",
    "REPAIR_SAFETY_GAPS.csv", "OPTIMAL_PROTOCOLS.json",
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    for name in REQUIRED:
        assert (ROOT / "research" / name).stat().st_size > 0, name
    for name in DATA:
        assert (ROOT / "computations" / name).stat().st_size > 0, name
    for line in (ROOT / "computations" / "SHA256SUMS.txt").read_text().splitlines():
        expected, name = line.split("  ", 1)
        assert digest(ROOT / "computations" / name) == expected, name
    transfer = json.loads((ROOT / "TRANSFER_VERIFICATION.json").read_text(encoding="utf-8-sig"))
    assert not transfer["full_core_differences"]
    assert all(not item["hash_failures"] for item in transfer["manifests"])
    files = [ROOT / "README.md", ROOT / "TRANSFER_VERIFICATION.json", Path(__file__).resolve()]
    for folder in ("research", "computations"):
        files.extend(
            p for p in (ROOT / folder).rglob("*")
            if p.is_file() and "__pycache__" not in p.parts
        )
    files = sorted(files)
    manifest = ROOT / "RESEARCH_SHA256SUMS.txt"
    manifest.write_text(
        "".join(f"{digest(p)}  {p.relative_to(ROOT).as_posix()}\n" for p in files),
        encoding="utf-8",
    )
    target = ROOT / "HEIGHT2_FIXED_LIBRARY_RESEARCH_2026-09-29.zip"
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files + [manifest]:
            archive.write(path, path.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None
        assert len(archive.namelist()) == len(files) + 1
    print(json.dumps({
        "required_reports": len(REQUIRED), "required_data": len(DATA),
        "packaged_files": len(files) + 1, "zip_bytes": target.stat().st_size,
        "zip_sha256": digest(target), "output": str(target),
    }, indent=2))


if __name__ == "__main__":
    main()
