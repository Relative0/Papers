"""Executable boundary audit of the unmodified archived source snapshot.

Run with --source pointing to a recovered cmbench source directory.
"""
from pathlib import Path
import argparse, sys, hashlib, json, copy

def run(source):
    sys.path.insert(0, str(source))
    from cmbench.recognition.gf2_decomposition import (
        rank_artifact, xor_component_artifact, ExactGF2Artifact,
        canonical, analyze_exact_gf2, truth_sha256)
    events = []
    n = 6
    truth = sum((((a >> 5) & 1) & ((a >> 2) & 1)) << a for a in range(64))
    art = rank_artifact(truth, n, (0,1,2))
    assert art is not None and art.reconstruct() == truth
    original = art.to_dict()
    def reseal(doc):
        body = {k:v for k,v in doc.items() if k != 'payload_sha256'}
        doc['payload_sha256'] = hashlib.sha256(canonical(body)).hexdigest()
        return doc
    changed = copy.deepcopy(original)
    changed['factor_bits'] = 1
    changed['compression_ratio'] = 64
    admitted = ExactGF2Artifact.from_dict(reseal(changed))
    events.append({'id':'H1','finding':'factor_bits is not recomputed by loader',
                   'original_factor_bits':original['factor_bits'], 'admitted_factor_bits':admitted.document['factor_bits'],
                   'truth_unchanged': admitted.reconstruct() == truth})
    changed = copy.deepcopy(original)
    changed['payload']['rank'] += 1
    changed['payload']['basis_rows'].append(0)
    admitted = ExactGF2Artifact.from_dict(reseal(changed))
    events.append({'id':'H2','finding':'declared rank may be nonminimal inner dimension',
                   'actual_rank':original['payload']['rank'],'admitted_rank':admitted.document['payload']['rank'],
                   'truth_unchanged':admitted.reconstruct() == truth})
    changed = copy.deepcopy(original)
    changed['payload']['basis_rows'][0] ^= 1
    temp = ExactGF2Artifact(changed)
    newtruth = temp.reconstruct()
    changed['source_sha256'] = truth_sha256(newtruth, n)
    admitted = ExactGF2Artifact.from_dict(reseal(changed))
    events.append({'id':'H3','finding':'self-supplied digest does not authenticate external source',
                   'admitted_changed_truth':admitted.reconstruct() != truth,
                   'interpretation':'integrity contract is not externally rooted source-equivalence certification'})
    original_admitted = ExactGF2Artifact.from_dict(original)
    original_admitted.document['payload']['basis_rows'][0] ^= 1
    events.append({'id':'H4','finding':'frozen dataclass does not deep-freeze document',
                   'post_admission_mutation_changes_truth':original_admitted.reconstruct()!=truth})
    for nv in (0,1):
        try:
            analyze_exact_gf2(0, nv)
            rejected = False
        except ValueError:
            rejected = True
        events.append({'id':'H5' if nv==0 else 'H6', 'finding':'boundary dimension unsupported',
                       'n_vars':nv,'rejected':rejected})
    return {'status':'observations reproduced', 'events':events,
            'source_file_sha256':hashlib.sha256((source/'cmbench/recognition/gf2_decomposition.py').read_bytes()).hexdigest(),
            'scope_note':'No claim of a malicious use case; these are contract and metadata limits. Producer reconstruction was correct for the tested witness.'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    result = run(args.source)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
