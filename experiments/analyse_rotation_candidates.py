"""Refold Q's rotation candidates and apply R's exact map-pair decision.

A candidate is only a failure of Q's sufficient DAG absence criterion.
This script either finds an actual primitive loop or exhausts a finite,
complete partial-transformation pair graph for all signed primitive classes.
"""
import argparse
import base64
from collections import deque
import hashlib
import gzip
import json
from pathlib import Path
from primitive_map_pairs import LETTERS,compact_absence,decide,fold,validate_graph,verify_absence


def load_bytes(source):
    path = Path(source)
    raw = path.read_bytes()
    if str(path).endswith('.gz.b64'):
        return gzip.decompress(base64.b64decode(raw))
    if str(path).endswith('_manifest.json'):
        manifest = json.loads(raw)
        assert manifest['format'] == 'f2-primitive-map-pair-jsonl-gzip-base64-parts-v1'
        chunks = []
        for name in manifest['parts']:
            data = (path.parent/name).read_bytes()
            assert hashlib.sha256(data).hexdigest() == manifest['part_sha256'][name]
            chunks.append(data)
        encoded = b''.join(chunks)
        assert len(encoded) == manifest['encoded_bytes']
        assert hashlib.sha256(encoded).hexdigest() == manifest['encoded_sha256']
        decoded = gzip.decompress(base64.b64decode(encoded))
        assert len(decoded) == manifest['decoded_jsonl_bytes']
        assert hashlib.sha256(decoded).hexdigest() == manifest['decoded_jsonl_sha256']
        return decoded
    return raw


def rebased(encoded,base):
    size = validate_graph(encoded)
    assert 0 <= base < size
    names = {base:0}
    queue = deque([base])
    result = []
    while queue:
        at = queue.popleft()
        for end in encoded[4*at:4*at+4]:
            if end >= 0 and end not in names:
                names[end] = len(names)
                queue.append(end)
            result.append(names[end] if end >= 0 else -1)
    return tuple(result)


def run(source,budget,certificate_path=None):
    raw = load_bytes(source)
    rows = [json.loads(line) for line in raw.splitlines() if line.strip()]
    certificates = Path(certificate_path).open('w') if certificate_path else None
    analyses = []
    total_pairs = maximum_pairs = 0
    try:
        for i,row in enumerate(rows):
            encoded = fold(row['pair'])
            assert encoded == rebased(row['graph'],row['original_base'])
            result = decide(encoded,budget,save_certificate=True)
            counts = [r['pair_states_discovered'] for r in result['alphabets']]
            total_pairs += sum(counts)
            maximum_pairs = max(maximum_pairs,*counts)
            if result['status'] == 'ABSENT':
                verification = verify_absence(result)
                assert verification['status'] == 'PASS'
            if certificates:
                certificates.write(json.dumps({'candidate_index':i,'pair':row['pair'],
                                                'certificate':compact_absence(result) if result['status']=='ABSENT' else result},separators=(',',':'))+'\n')
            summary = {'candidate_index':i,'source_index':row['source_index'],
                       'pair':row['pair'],'status':result['status'],
                       'vertices':len(encoded)//4,'map_pair_states_per_alphabet':counts}
            if 'witness' in result:
                summary['witness'] = result['witness']
            analyses.append(summary)
            if result['status'] == 'PRIMITIVE':
                break
    finally:
        if certificates:
            certificates.close()
    positive = [row for row in analyses if row['status']=='PRIMITIVE']
    incomplete = [row for row in analyses if row['status']=='INCOMPLETE']
    return {'status':'PRIMITIVE' if positive else 'INCOMPLETE' if incomplete else 'ABSENT',
            'ordinary_AC_goal_solved':False,
            'input_sha256':hashlib.sha256(raw).hexdigest(),
            'input_candidate_records':len(rows),'candidate_records_tested':len(analyses),
            'independent_refolding_matches_Q_all_tested':True,
            'complete_absence_records':sum(r['status']=='ABSENT' for r in analyses),
            'incomplete_records':len(incomplete),'primitive_records':len(positive),
            'finite_map_pair_states_total':total_pairs,
            'maximum_states_for_one_graph_alphabet':maximum_pairs,
            'primitive_witnesses':positive,'incomplete_witnesses':incomplete,
            'analyses':analyses}


def verify_dataset(source,proof_data):
    raw = load_bytes(source)
    rows = [json.loads(line) for line in raw.splitlines() if line.strip()]
    manifest = (json.loads(Path(proof_data).read_bytes())
                if str(proof_data).endswith('_manifest.json') else None)
    if manifest:
        assert hashlib.sha256(raw).hexdigest() == manifest['candidate_jsonl_sha256']
        assert len(rows) == manifest['candidate_records']
    proofs = load_bytes(proof_data)
    seen = set()
    total = 0
    for line in proofs.splitlines():
        row = json.loads(line)
        i = row['candidate_index']
        assert type(i) is int and 0 <= i < len(rows) and i not in seen
        seen.add(i)
        source_row = rows[i]
        assert row['pair'] == source_row['pair']
        encoded = fold(row['pair'])
        assert encoded == rebased(source_row['graph'],source_row['original_base'])
        assert tuple(row['certificate']['encoded_graph']) == encoded
        result = verify_absence(row['certificate'])
        assert result['status'] == 'PASS'
        total += result['closed_map_pair_states_checked']
    assert seen == set(range(len(rows)))
    if manifest:
        assert total == manifest['finite_map_pair_states']
    return {'status':'PASS','ordinary_AC_goal_solved':False,
            'candidate_jsonl_sha256':hashlib.sha256(raw).hexdigest(),
            'proof_jsonl_sha256':hashlib.sha256(proofs).hexdigest(),
            'complete_candidate_absence_certificates_checked':len(seen),
            'closed_map_pair_states_checked':total,
            'all_candidates_independently_refolded':True,
            'all_closed_sets_contain_initial_maps_and_no_fixed_points':True,
            'all_closed_sets_closed_under_both_positive_Nielsen_updates':True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source')
    parser.add_argument('--budget',type=int,default=1000000)
    parser.add_argument('--certificates-jsonl')
    parser.add_argument('--verify-certificates')
    parser.add_argument('--output',required=True)
    args = parser.parse_args()
    result = (verify_dataset(args.source,args.verify_certificates) if args.verify_certificates
              else run(args.source,args.budget,args.certificates_jsonl))
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='analyses'},indent=2))
