"""Verify the delivered ABC executable, dependencies, version, and AIG behavior."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import tempfile

from aiger_check import truth_bits


HERE = Path(__file__).resolve().parent


def main():
    provenance = json.loads((HERE / 'ABC_TOOL_PROVENANCE.json').read_text(encoding='utf-8'))
    for name, expected in provenance['files'].items():
        blob = (HERE / 'abc_tool' / name).read_bytes()
        if len(blob) != expected['bytes'] or sha256(blob).hexdigest() != expected['sha256']:
            raise ValueError(f'ABC component differs from provenance: {name}')

    executable = HERE / 'abc_tool' / 'yosys-abc.exe'
    version = subprocess.run([str(executable), '-c', 'version'], cwd=HERE,
                             capture_output=True, text=True, timeout=30, check=True)
    if 'ABC 1.01 (compiled Jul 29 2026 04:36:08)' not in version.stdout:
        raise ValueError('ABC version differs from provenance')

    with tempfile.TemporaryDirectory(prefix='abc_smoke_') as directory:
        scratch = Path(directory)
        (scratch / 'tiny.blif').write_text(
            '.model tiny\n.inputs a b\n.outputs y\n.names a b y\n11 1\n.end\n',
            encoding='ascii')
        command = 'read_blif tiny.blif; strash; dc2; write_aiger tiny.aig'
        run = subprocess.run([str(executable), '-c', command], cwd=scratch,
                             capture_output=True, text=True, timeout=30, check=True)
        bits, shape = truth_bits(scratch / 'tiny.aig', ('a', 'b'))
        if bits != 8 or shape['inputs'] != 2:
            raise ValueError('ABC tiny AIG smoke test failed')

    result = {'status': 'PASS', 'component_files_checked': len(provenance['files']),
              'version': 'ABC 1.01 (compiled Jul 29 2026 04:36:08)',
              'smoke_command': command, 'smoke_truth_bits': bits,
              'smoke_and_gates': shape['and_gates']}
    (HERE / 'ABC_TOOL_VALIDATION.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
