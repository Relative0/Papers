"""Verify the 1 October 2026 paper-folder relocation after source retirement."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "00_Collection_Index"
PLAN = INDEX / "PAPER_FOLDER_RENAME_PLAN_2026-10-01.json"
MAP = INDEX / "PAPER_FOLDER_RELOCATION_MAP_2026-10-01.jsonl"
DIRS = INDEX / "PAPER_FOLDER_PRENAME_DIRECTORIES_2026-10-01.jsonl"
PRECHECK = INDEX / "PAPER_FOLDER_PRE_RETIRE_HASH_CHECK_2026-10-01.json"
RECEIPT = INDEX / "PAPER_FOLDER_POST_RETIRE_VERIFICATION_2026-10-01.json"
LINK = re.compile(r"(?<!!)\[[^\]]*\]\((<[^>]*>|[^)\r\n]*)\)")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    previous = json.loads(PRECHECK.read_text(encoding="utf-8"))
    rows = [json.loads(line) for line in MAP.read_text(encoding="utf-8").splitlines()]
    directory_rows = [json.loads(line) for line in DIRS.read_text(encoding="utf-8").splitlines()]
    absent_sources = [p["source"] for p in plan if not (ROOT / p["source"]).exists()]
    present_sources = [p["source"] for p in plan if (ROOT / p["source"]).exists()]
    missing_destinations = []
    missing_destination_directories = [
        row["destination_directory"] for row in directory_rows
        if not (ROOT / row["destination_directory"]).is_dir()
    ]
    changed_destinations = []
    verified = 0
    for row in rows:
        path = ROOT / row["destination"]
        if not path.is_file():
            missing_destinations.append(row["destination"])
            continue
        actual = sha256(path)
        if actual != row["destination_sha256"]:
            changed_destinations.append(
                {"path": row["destination"], "previous_sha256": row["destination_sha256"], "current_sha256": actual}
            )
        else:
            verified += 1

    docs = [ROOT / "README.md", *(INDEX.glob("*.md")), ROOT / "The MIND" / "README.md", ROOT / "The MIND" / "01_Papers" / "README.md"]
    docs.extend((ROOT / "The MIND" / "01_Papers").glob("*/README.md"))
    docs.extend((ROOT / "The MIND" / "01_Papers").glob("*/Review_Workspaces/README.md"))
    for folder in ROOT.iterdir():
        if not folder.is_dir() or folder.name in {"The MIND", "00_Collection_Index", "90_Preserved_Sources", ".git"}:
            continue
        for name in ("README.md", "README_FIRST.md", "COLLECTION_README.md", "CLAIMS_AND_UNIQUENESS.md", "RESEARCH_BRIEF.md"):
            docs.append(folder / name)
        docs.append(folder / "REPRODUCIBILITY" / "README.md")
    docs = sorted({p for p in docs if p.is_file()})
    broken_links = []
    local_links = 0
    for doc in docs:
        content = doc.read_text(encoding="utf-8-sig", errors="replace")
        for match in LINK.finditer(content):
            target = match.group(1).strip().strip("<>").strip()
            if not target or target.startswith(("#", "http:", "https:", "mailto:", "codex:")):
                continue
            target = unquote(target.split("#", 1)[0])
            if not target:
                continue
            local_links += 1
            resolved = (doc.parent / target).resolve()
            if not resolved.exists():
                broken_links.append({"document": doc.relative_to(ROOT).as_posix(), "target": target})

    allowed_post_retire_navigation_edits = {
        "The MIND/01_Papers/02 Hierarchical Concepts (Research Note)/README.md"
    }
    unexpected_hash_changes = [
        row for row in changed_destinations if row["path"] not in allowed_post_retire_navigation_edits
    ]
    receipt = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if (
            len(absent_sources) == len(plan)
            and not missing_destinations
            and not missing_destination_directories
            and not broken_links
            and not unexpected_hash_changes
            and sha256(PLAN) == previous["plan_sha256"]
            and sha256(MAP) == previous["map_sha256"]
        ) else "FAIL",
        "old_source_folders_absent": len(absent_sources),
        "old_source_folders_present": present_sources,
        "mapped_files": len(rows),
        "mapped_directories": len(directory_rows),
        "destination_hashes_matching_pre_retire_map": verified,
        "destination_hashes_changed_since_map": changed_destinations,
        "unexpected_destination_hash_changes": unexpected_hash_changes,
        "missing_destinations": missing_destinations,
        "missing_destination_directories": missing_destination_directories,
        "pre_retire_source_and_destination_hash_check": previous["source_and_destination_sha256"],
        "pre_retire_plan_sha256_unchanged": sha256(PLAN) == previous["plan_sha256"],
        "pre_retire_map_sha256_unchanged": sha256(MAP) == previous["map_sha256"],
        "primary_navigation_documents": len(docs),
        "primary_local_links": local_links,
        "broken_primary_links": broken_links,
    }
    RECEIPT.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in receipt.items() if k not in {"destination_hashes_changed_since_map", "missing_destinations", "broken_primary_links"}}, indent=2))
    print(f"Changed destination hashes: {len(changed_destinations)}; missing destinations: {len(missing_destinations)}; broken links: {len(broken_links)}")
    if changed_destinations:
        for row in changed_destinations:
            print("Changed:", row["path"])
    if broken_links:
        for row in broken_links:
            print("Broken:", row)
    if receipt["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
