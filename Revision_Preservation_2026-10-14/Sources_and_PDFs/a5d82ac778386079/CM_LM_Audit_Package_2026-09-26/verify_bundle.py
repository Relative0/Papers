"""Verify this audit bundle against its SHA-256 manifest."""
from pathlib import Path
import hashlib
import sys

root = Path(__file__).resolve().parent
failures = []
count = 0
for line in (root / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
    expected, name = line.split("  ", 1)
    path = root / name
    count += 1
    if not path.is_file():
        failures.append("MISSING: " + name)
    elif hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        failures.append("CHANGED: " + name)
if failures:
    print("\n".join(failures))
    sys.exit(1)
print(f"PASS: {count} manifest entries match.")
