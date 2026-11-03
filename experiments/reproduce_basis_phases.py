"""Reproduce T/U/V's restricted initial-subgroup phase result, not AC itself."""
import argparse
import base64
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent


def run(*args):
    completed = subprocess.run(args, cwd=ROOT, check=True, text=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return completed.stdout


def digest(data):
    return hashlib.sha256(data).hexdigest()


def decode_parts(manifest_path):
    manifest = json.loads(manifest_path.read_text())
    pieces = []
    for name in manifest['parts']:
        raw = (manifest_path.parent/name).read_bytes()
        assert digest(raw) == manifest['part_sha256'][name]
        pieces.append(raw)
    encoded = b''.join(pieces)
    assert digest(encoded) == manifest['encoded_sha256']
    decoded = gzip.decompress(base64.b64decode(encoded))
    assert digest(decoded) == manifest['decoded_jsonl_sha256']
    return decoded


def reproduce(scan_result=None):
    py = sys.executable
    with tempfile.TemporaryDirectory(prefix='ac-basis-phases-') as directory:
        folder = Path(directory)
        out = folder/'result.json'
        source = ROOT/'certificates/v_cap250_sources.jsonl.gz.b64'
        run(py, 'experiments/validate_farey_sources.py', str(source),
            '--n', '3', '--cap', '250', '--output', str(out))
        coverage = json.loads(out.read_text())
        assert coverage['actual_raw_basis_programs_independently_regenerated'] == 1111
        assert coverage['strict_Nielsen_only_source_moves_replayed'] == 33238
        assert coverage['maximum_strict_raw_source_peak'] == 254
        assert coverage['matrix_enumeration']['projective_primitive_vectors_tested'] == 1059
        assert coverage['all_source_family_keys_equal_independent_matrix_enumeration']
        binary = folder/'u-native'
        run('c++', '-std=c++17', '-O3', 'experiments/u_native_primitive.cpp', '-o', str(binary))
        run(py, 'experiments/u_native_controls.py', '--binary', str(binary),
            '--references', str(ROOT/'experiments'), '--examples-directory', str(folder/'examples'),
            '--output', str(out))
        native_controls = json.loads(out.read_text())
        reference = folder/'r-compact.jsonl'
        reference.write_bytes(decode_parts(ROOT/'certificates/r_rotation_map_pairs_manifest.json'))
        run(py, 'experiments/u_review_candidates.py',
            'certificates/q_rotation_candidates.jsonl.gz.b64', '--binary', str(binary),
            '--R-certificates', str(reference), '--output', str(out))
        hard = json.loads(out.read_text())
        assert hard['complete_decision_counts'] == {'ABSENT': 6568, 'PRIMITIVE': 0, 'INCOMPLETE': 0}
        assert hard['closed_total_map_pairs_independently_checked'] == 735712
        assert hard['entire_closed_pair_sets_equal_R_compact_certificates'] == 6568
        tsves = []
        for name in ('ak2', 'power'):
            tsv = folder/(name+'.tsv')
            run(py, 'experiments/reverse_journal.py',
                'certificates/r_reverse_'+name+'_journal.json.gz.b64',
                '--tsv-output', str(tsv), '--output', str(out))
            tsves.append(tsv)
        anchors = folder/'anchors.json'
        anchors.write_bytes(gzip.decompress(base64.b64decode(
            (ROOT/'results/v_barbell_anchor_results.json.gz.b64').read_bytes())))
        run(py, 'experiments/t_barbell_reverse_review.py', *map(str, tsves),
            '--v-result', str(anchors), '--output', str(out))
        barbell = json.loads(out.read_text())
        assert barbell['input_reverse_rows'] == 56799
        assert barbell['independently_detected_barbell_rows'] == 549
        assert barbell['distinct_collapsed_cycle_families'] == 338
        assert barbell['maximum_collapsed_cycle_energy'] == 21
        assert barbell['exact_anchor_keys_equal_V']
        if scan_result:
            scan = json.loads(Path(scan_result).read_text())
        else:
            scanner = folder/'basis-scan'
            run('c++', '-std=c++17', '-O3', 'experiments/v_one_phase_bases.cpp', '-o', str(scanner))
            generated = folder/'sources.jsonl'
            run(str(scanner), '250', str(generated), str(folder/'candidates.jsonl'),
                str(out), '4000000', '3', *map(str, tsves))
            scan = json.loads(out.read_text())
            assert digest(generated.read_bytes()) == coverage['source_jsonl_sha256']
        for key, value in {'status':'COMPLETE', 'prelude_cyclic_energy_cap':250,
                           'distinct_final_cyclic_pair_families':1111,
                           'rotation_pairs':5862545, 'distinct_unbased_core_graphs':2905457,
                           'direct_DAG_absence_graphs':2905457, 'exception_graphs':0,
                           'distinct_reverse_keys':56799, 'reverse_subgroup_match':False}.items():
            assert scan[key] == value, (key, scan[key], value)
        run(py, 'experiments/t_hidden_primitive_completion.py',
            'certificates/t_v_ak2_candidate_prefix.json',
            '--certificate', str(folder/'ak2-full.json'), '--output', str(out))
        control = json.loads(run(py, 'experiments/elementary_verify.py', str(folder/'ak2-full.json')))
        assert control['moves'] == 232 and control['peak_total_length'] == 33
        assert control['endpoint'] == ['x','y']
        return {'status':'PASS', 'ordinary_AC_goal_solved':False,
                'initial_AK3_subgroup_source_cyclic_cap':250,
                'source_classes_independently_enumerated_and_strictly_replayed':1111,
                'strict_source_Nielsen_moves':33238,
                'full_rotation_enumeration_recomputed_in_this_invocation':not bool(scan_result),
                'rotation_pairs':5862545, 'distinct_unbased_labelled_cores':2905457,
                'all_cores_have_signed_DAG_primitive_absence':True,
                'native_detector_controls':native_controls,
                'native_hard_graphs_independently_refolded_and_verified':6568,
                'native_closed_total_map_pair_states_checked':735712,
                'entire_native_closed_sets_equal_R':True,
                'reverse_barbell_rows':549, 'collapsed_families':338,
                'AK2_control_strict_moves':232, 'AK2_control_raw_peak':33,
                'arbitrary_interspersed_AC_moves_covered':False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--scan-result', help='validate an already independently regenerated full scan instead of rerunning it')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = reproduce(args.scan_result)
    Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
