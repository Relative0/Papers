"""One-time link update after the 1 October paper-folder copy. Do not rerun."""

import hashlib
import json
import os
import re
import zipfile
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "00_Collection_Index"
PLAN = json.loads((INDEX / "PAPER_FOLDER_RENAME_PLAN_2026-10-01.json").read_text())
FORWARD = sorted(
    [(ROOT / row["source"], ROOT / row["destination"]) for row in PLAN],
    key=lambda pair: len(pair[0].parts),
    reverse=True,
)
REVERSE = sorted(
    [(new, old) for old, new in FORWARD],
    key=lambda pair: len(pair[0].parts),
    reverse=True,
)
LINK = re.compile(r"(?<!!)\[[^\]]*\]\((<[^>]*>|[^)\r\n]*)\)")


def remap(path, pairs):
    for old, new in pairs:
        try:
            return new / path.relative_to(old)
        except ValueError:
            pass
    return path


def rewrite_link(match, old_document, new_document):
    original = match.group(0)
    wrapper = match.group(1)
    url = wrapper[1:-1] if wrapper.startswith("<") and wrapper.endswith(">") else wrapper
    path, marker, suffix = re.match(r"([^?#]*)([?#]?)(.*)", url).groups()
    if not path or "://" in path or path.startswith(("mailto:", "#")):
        return original
    if re.match(r"^[A-Za-z]:[/\\]", path):
        old_target = Path(unquote(path))
    else:
        old_target = (old_document.parent / unquote(path.replace("\\", "/"))).resolve()
    if not old_target.exists():
        return original
    new_target = remap(old_target, FORWARD)
    new_path = os.path.relpath(new_target, new_document.parent).replace("\\", "/")
    if new_path == unquote(path.replace("\\", "/")):
        return original
    new_url = new_path + marker + suffix
    if wrapper.startswith("<") or any(c in new_url for c in " ()"):
        new_url = "<" + new_url + ">"
    return original[: -(len(wrapper) + 1)] + new_url + ")"


def main():
    changes = []
    for base, dirs, files in os.walk(ROOT):
        folder = Path(base)
        dirs[:] = [
            name
            for name in dirs
            if name not in {".git", "90_Preserved_Sources", "Extraction_Staging", "Verification_Work", "Before_Fresh_Referee_Restore"}
            and not any(folder / name == old for old, _ in FORWARD)
        ]
        for name in files:
            if not name.lower().endswith(".md"):
                continue
            document = folder / name
            try:
                before = document.read_bytes()
                source = before.decode("utf-8")
            except UnicodeError:
                continue
            old_document = remap(document, REVERSE)
            after, count = LINK.subn(
                lambda match: rewrite_link(match, old_document, document), source
            )
            if after != source:
                changes.append((document, before, after.encode("utf-8"), count))

    backup = INDEX / "PAPER_FOLDER_NAVIGATION_PREEDIT_2026-10-01.zip"
    receipt = INDEX / "PAPER_FOLDER_NAVIGATION_EDITS_2026-10-01.json"
    if backup.exists() or receipt.exists():
        raise RuntimeError("One-time link update already ran; refusing overwrite")
    with zipfile.ZipFile(backup, "x", zipfile.ZIP_DEFLATED) as archive:
        for document, before, _, _ in changes:
            archive.writestr(document.relative_to(ROOT).as_posix(), before)
    with zipfile.ZipFile(backup) as archive:
        assert archive.testzip() is None
        for document, before, _, _ in changes:
            assert archive.read(document.relative_to(ROOT).as_posix()) == before

    rows = []
    for document, before, after, count in changes:
        document.write_bytes(after)
        assert document.read_bytes() == after
        rows.append(
            {
                "path": document.relative_to(ROOT).as_posix(),
                "links_inspected": count,
                "before_sha256": hashlib.sha256(before).hexdigest(),
                "after_sha256": hashlib.sha256(after).hexdigest(),
                "backup_member": document.relative_to(ROOT).as_posix(),
            }
        )
    receipt.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Updated", len(rows), "documents; backup SHA-256", hashlib.sha256(backup.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
