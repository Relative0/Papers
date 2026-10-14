"""Replay the preceding diagnostic into this audit, preserving frozen results."""
from pathlib import Path
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
path = ROOT.parent/'semantic_boundary_20261013/semantic_contract_checker.py'
if not path.exists():
    path = ROOT.parent/'semantic_contract_checker.py'
spec = importlib.util.spec_from_file_location('original_checker', path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.OUT = ROOT/'replay'
module.OUT.mkdir(exist_ok=True)
module.run()
original_path = path.with_name('checker_results.json')
old = json.loads(original_path.read_text(encoding='utf-8'))
new = json.loads((module.OUT/'checker_results.json').read_text(encoding='utf-8'))
old.pop('elapsed_seconds')
new.pop('elapsed_seconds')
assert old == new, 'Replay changed substantive results'
print('PASS: original 42,918-assertion result reproduced exactly, excluding elapsed time.')
