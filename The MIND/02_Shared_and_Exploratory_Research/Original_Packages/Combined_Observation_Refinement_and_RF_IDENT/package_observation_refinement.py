"""Create and independently verify the consolidated paper archive."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile


HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parents[1]
DOWNLOADS = Path(r"C:\Users\brian\Downloads")
ATTACHMENTS = Path(r"C:\Users\brian\.codex\attachments")
ARCHIVE_NAME = "MIND_Observation_Refinement_RF_IDENT_All_Artifacts_2026-09-29.zip"

PROJECT_FOLDERS = [
    "The MIND/Transferred Research",
    "The MIND/Interaction Core Gate 2026-09-29",
    "The MIND/Manuscript Convergence 2026-09-29",
    "The MIND/Independent Expert Review",
    "The MIND/Manuscript Referee Repairs 2026-09-29",
    "The MIND/Height2 Fixed Library Gate 2026-09-29",
    "The MIND/RF-IDENT Bounded Height2 2026-09-29",
    "The MIND/RF-IDENT Bounded Height2 Independent Review 2026-09-29",
]

SOURCE_ARCHIVES = [
    WORKSPACE / "ProLT.zip",
    WORKSPACE / "ProLT-Homology.zip",
    DOWNLOADS / "MIND_TWO_OPERATION_ACCOUNT_TRANSFER_FULL_2026-09-29.zip",
    DOWNLOADS / "MIND_TWO_OPERATION_ACCOUNT_TRANSFER_CORE_2026-09-29.zip",
    DOWNLOADS / "ASTRA_PRO_ProLT_Master_Audit_2026-09-23.zip",
    DOWNLOADS / "ProLT_Binary_Order_Thinning_Post_Audit_v2.zip",
    DOWNLOADS / "ProLT_Master_Audit_Completed_2026-09-24.zip",
    DOWNLOADS / "ProLT_PostAudit_Update_2026-09-24.zip",
]

USER_SUPPLIED = {
    "HEIGHT2_FIXED_LIBRARY_PROMPT.txt":
        ATTACHMENTS / "ca795a1d-9879-404d-aa5b-c0301fc53c84" / "Pasted text.txt",
    "RF_IDENT_INDEPENDENT_REVIEW_FEEDBACK.txt":
        ATTACHMENTS / "a2894ef2-14bf-4542-86e8-4cb603996913" / "Pasted text.txt",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def check_path(path: Path) -> None:
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"Expected a regular file: {path}")
    parts = [part.lower() for part in path.parts]
    if any(part.startswith(".env") or part.endswith((".key", ".pem", ".p12", ".pfx")) for part in parts):
        raise ValueError(f"Sensitive file name excluded: {path}")


def sources() -> dict[str, Path]:
    result: dict[str, Path] = {}
    for relative in PROJECT_FOLDERS:
        folder = WORKSPACE / relative
        if not folder.is_dir():
            raise FileNotFoundError(folder)
        for path in folder.rglob("*"):
            if path.is_dir():
                continue
            if "__pycache__" in path.parts or path.suffix.lower() == ".pyc":
                continue
            check_path(path)
            member = "project/" + path.relative_to(WORKSPACE).as_posix()
            if member in result:
                raise ValueError(f"Duplicate member: {member}")
            result[member] = path
    for path in SOURCE_ARCHIVES:
        check_path(path)
        member = "source_archives/" + path.name
        if member in result:
            raise ValueError(f"Duplicate member: {member}")
        result[member] = path
    for name, path in USER_SUPPLIED.items():
        check_path(path)
        result["user_supplied/" + name] = path
    check_path(HERE / "START_HERE.md")
    check_path(Path(__file__).resolve())
    result["START_HERE.md"] = HERE / "START_HERE.md"
    result["package_observation_refinement.py"] = Path(__file__).resolve()
    return result


def main() -> None:
    files = sources()
    hashes = {member: sha256_file(path) for member, path in sorted(files.items())}
    manifest = "".join(f"{digest}  {member}\n" for member, digest in hashes.items()).encode("utf-8")
    target = HERE / ARCHIVE_NAME
    pending = HERE / (ARCHIVE_NAME + ".pending")
    if pending.exists():
        raise FileExistsError(f"Pending archive exists; inspect it before rebuilding: {pending}")
    with ZipFile(pending, "w", allowZip64=True) as archive:
        for member, path in sorted(files.items()):
            compression = ZIP_STORED if path.suffix.lower() == ".zip" else ZIP_DEFLATED
            archive.write(path, member, compress_type=compression, compresslevel=6)
        archive.writestr("SHA256_MANIFEST.txt", manifest, compress_type=ZIP_DEFLATED)

    with ZipFile(pending) as archive:
        if archive.testzip() is not None:
            raise AssertionError("Archive CRC check failed")
        if set(archive.namelist()) != set(files) | {"SHA256_MANIFEST.txt"}:
            raise AssertionError("Archive member list differs from source list")
        if archive.read("SHA256_MANIFEST.txt") != manifest:
            raise AssertionError("Manifest differs from recorded hashes")
        for member, digest in hashes.items():
            if hashlib.sha256(archive.read(member)).hexdigest() != digest:
                raise AssertionError(f"Archive content hash mismatch: {member}")

    os.replace(pending, target)
    receipt = {
        "status": "verified",
        "archive": str(target),
        "archive_sha256": sha256_file(target),
        "archive_bytes": target.stat().st_size,
        "payload_files": len(files),
        "manifest_entries": len(hashes),
        "project_folders": PROJECT_FOLDERS,
        "source_archives": [path.name for path in SOURCE_ARCHIVES],
        "user_supplied_files": sorted(USER_SUPPLIED),
        "verification": "ZIP CRC, member list, manifest bytes, and SHA-256 of every archived payload",
    }
    (HERE / "PACKAGE_RECEIPT.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
