"""Replay the bounded research checks; nothing here claims an AC solution."""
import argparse
import base64
import gzip
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent


def run(*arguments, json_output=True):
    result = subprocess.run(arguments, cwd=ROOT, check=True, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if json_output:
        return json.loads(result.stdout[result.stdout.index('{'):])
    return result.stdout


def main(cpp=False, packed=False):
    py = sys.executable
    run(py, 'experiments/elementary_verify.py', '--selftest', json_output=False)
    exact = run(py, 'experiments/elementary_verify.py', 'certificates/ms3_to_ak3_exact.json')
    assert exact['endpoint'] == ['xyxYXY', 'xxxYYYY'] and exact['moves'] == 32
    family = run(py, 'experiments/ms_ak_family.py', '--self-test', '--n', '3')
    assert family['packaged_moves'] == 13 and family['strict_elementary_moves'] == 26
    plateau = run(py, 'experiments/verify_plateau.py')
    assert plateau['formula_checks_n_1_through_100']
    gap = run(py, 'experiments/verify_gap_one.py')
    assert gap['witness_is_equal_in_torus_quotient']
    for entry in gap['checks']:
        assert entry['also_passing_torus_abelianization']['7'] == 0
    nilpotent = run(py, 'experiments/quotient_certificates.py')
    assert nilpotent['ak3_literal_move_count'] == 12
    assert nilpotent['ak3_class3_literal_move_count'] == 48
    peak = run(py, 'experiments/raw_peak_search.py', '--selftest', '--n', '3', '--cap', '18')
    assert peak['complete_component_exhaustion'] and not peak['target_reached']
    assert peak['states_processed'] == peak['states_discovered'] == 251874
    assert peak['minimum_total_length'] == 13
    infinite = run(py, 'experiments/psl2z_search.py', '--depth', '5')
    assert infinite['complete'] and infinite['shortest_distance_within_complete_search'] == 10
    lift = run(py, 'experiments/elementary_verify.py', 'certificates/psl2z_quotient_lift.json')
    assert lift['moves'] == 16 and list(map(len, lift['endpoint'])) == [23, 45]
    finite = run(py, 'experiments/finite_quotient_distances.py', '3', '5', '7', '11')
    assert [entry['distance'] for entry in finite['results']] == [3, 6, 9, 9]
    torus = run(py, 'experiments/torus_search.py', '--depth', '4')
    assert torus['complete'] and torus['distance'] == 8
    factors = run(py, 'experiments/torus_search.py', '--verify-factorizations',
                  'certificates/torus_quotient_lift.json')
    assert factors['factor_counts'] == [6, 5]
    family_t = run(py, 'experiments/torus_family.py', '--n', '3', '--selftest')
    assert family_t['strict_moves'] == 8 and family_t['meridian_strict_moves'] == 6
    lift_t = run(py, 'experiments/elementary_verify.py', 'certificates/torus_quotient_lift.json')
    assert lift_t['moves'] == 8 and list(map(len, lift_t['endpoint'])) == [45, 32]
    module = run(py, 'experiments/braid_relation_module.py', '--verify',
                 'certificates/braid_relation_module.json')
    assert module['minimal_braid_areas'] == [5, 13]
    assert module['endpoint_subgroup_vertices'] == 44 and module['endpoint_subgroup_rank'] == 2
    deletion = run(py, 'experiments/primitive_deletion_obstruction.py')
    assert deletion['status'] == 'PASS' and deletion['AK3_power_trace'] == 14
    product = run(py, 'experiments/product_search.py', '--verify-certificate',
                  'certificates/product_quotient_lift.json')
    assert product['strict_moves'] == 191 and product['quotient_endpoint'] == ['x', 'y']
    assert product['free_endpoint_lengths'] == [2539, 2159]
    product_balls = run(py, 'experiments/product_search.py', '--depth', '6', '--budget', '1200000')
    assert product_balls['complete'] and not product_balls['path_found']
    assert product_balls['forward_states'] == 904605 and product_balls['backward_states'] == 331694
    first_order = run(py, 'experiments/first_order_correction.py', '--verify',
                      'certificates/first_order_correction.json.gz.b64')
    assert first_order['word_operations'] == 205 and first_order['expanded_single_generator_move_count'] == 531377
    first_order_independent = run(py, 'experiments/verify_first_order.py',
                                  'certificates/first_order_correction.json.gz.b64')
    assert first_order_independent['independent_free_and_Fox_replay']
    assert first_order_independent['actual_free_endpoint_lengths'] == [230627, 946303]
    if cpp:
        with tempfile.TemporaryDirectory(prefix='ac-replay-') as directory:
            binary = str(Path(directory) / 'raw_peak')
            run('c++', '-std=c++17', '-O2', 'experiments/raw_peak_independent.cpp',
                '-o', binary, json_output=False)
            independent = run(binary, '18')
            assert independent['raw_ordered_oriented_states'] == 2014992
            assert independent['projected_states'] == 251874
            assert independent['minimum_total_length'] == 13
            assert not independent['target_reached']
            assert independent['energy_counts'] == peak['energy_counts']
            folded_binary = str(Path(directory) / 'fold_endpoint')
            run('c++', '-std=c++17', '-O2', 'experiments/fold_endpoint.cpp',
                '-o', folded_binary, json_output=False)
            compressed = (ROOT / 'certificates/first_order_correction.json.gz.b64').read_bytes()
            long_certificate = json.loads(gzip.decompress(base64.b64decode(compressed)))
            endpoint_file = Path(directory) / 'first_order_endpoint.txt'
            endpoint_file.write_text('\n'.join(long_certificate['target'])+'\n')
            folded = run(folded_binary, str(endpoint_file))
            assert folded['vertices'] == 1176895 and folded['unoriented_edges'] == 1176896
            assert folded['rank'] == 2 and not folded['accepts_x'] and not folded['accepts_y']
    if packed:
        with tempfile.TemporaryDirectory(prefix='ac-packed-') as directory:
            binaries = {}
            for name in ('packed_peak_search', 'verify_packed_closure', 'scan_primitive_relators'):
                binary = str(Path(directory) / name)
                run('c++', '-std=c++17', '-O3', 'experiments/'+name+'.cpp',
                    '-o', binary, json_output=False)
                binaries[name] = binary
            checkpoint = str(Path(directory) / 'cap21.bin')
            partial = run(binaries['packed_peak_search'], '3', '21', '20000000', checkpoint)
            assert not partial['complete']
            full = run(binaries['packed_peak_search'], '3', '21', '40000000', checkpoint, 'resume')
            assert full['complete'] and full['states_processed'] == full['states_discovered'] == 27380372
            audit = run(binaries['verify_packed_closure'], checkpoint)
            assert audit['closed'] and audit['start_present'] and audit['minimum_total_length'] == 13
            assert audit['allowed_neighbor_checks'] == 112696624
            assert audit['energy_counts'] == full['energy_counts']
            census = run(binaries['scan_primitive_relators'], '--selftest')
            assert census['primitive_census_selftest'] == 'PASS'
            primitive = run(binaries['scan_primitive_relators'], checkpoint)
            assert primitive['primitive_raw_relators'] == 0 and primitive['unique_cyclic_inverse_orbits'] == 99546
    print(json.dumps({'status': 'PASS', 'ordinary_AC_goal_solved': False,
                      'published_raw_AK3_peak_lower_bound': 22, 'raw_cap_replayed': 21 if packed else 18,
                      'cyclic_AK3_peak_lower_bound': 15,
                      'MS3_to_AK3_strict_moves': 32, 'braid_quotient_distance': 10,
                      'torus_quotient_distance': 8, 'product_strict_certificate_moves': 191,
                      'minimal_braid_lifting_areas': [5, 13],
                      'first_order_quotient_word_operations': 205,
                      'first_order_quotient_strict_expansion': 531377,
                      'independent_Cpp_exhaustion_replayed': cpp,
                      'first_order_endpoint_fold_replayed': cpp}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cpp', action='store_true', help='also compile and run the original-state C++ search')
    parser.add_argument('--packed', action='store_true', help='also regenerate, audit and scan the full cap-21 component')
    args = parser.parse_args()
    main(args.cpp, args.packed)
