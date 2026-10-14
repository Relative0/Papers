#!/usr/bin/env python3
"""Run all finite checks in this research package."""
import subprocess, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
for script in ["unfolding_boolean_audit.py","finite_complex_audit.py"]:
    print(f"\n=== {script} ===")
    subprocess.run([sys.executable, str(HERE/script)], check=True)
print("\nAll checks completed successfully.")
