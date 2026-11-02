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


def tail_checks():
    """New unbounded theorems have finite exact arithmetic/graph controls."""
    py = sys.executable
    braid = run(py, 'experiments/cyclic_braid_preimage.py')
    assert braid['status'] == 'PASS' and braid['determinant_commutator_constant'] == -1
    torus = run(py, 'experiments/torus_cyclic_preimage.py')
    assert torus['status'] == 'PASS' and torus['braid_trace'] == 4
    with tempfile.TemporaryDirectory(prefix='ac-tail-checks-') as directory:
        path = Path(directory) / 'result.json'
        initial = run(py, 'experiments/arbitrary_tail_certificate.py', '--verify',
                      'certificates/arbitrary_tail_graphs.json.gz.b64', '--output', str(path))
        assert initial['finite_reduced_tails'] == 1457
        assert initial['checked_acyclic_line_graphs'] == 11024
        run(py, 'experiments/arbitrary_tail_catalogue.py', '--source',
            'results/first_hump_results.json', '--crosscheck-directory', 'experiments',
            '--output', str(path), json_output=False)
        catalogue = json.loads(path.read_text())
        assert catalogue['status'] == 'PASS'
        assert catalogue['representative_pairs'] == 29
        assert catalogue['total_short_tails_tested'] == 123901
        assert catalogue['distinct_graphs_counted_within_each_pair_family'] == 118802
        assert catalogue['signed_acyclic_line_graphs_checked'] == 950416
        assert catalogue['crosschecked_against_prior_fold']
    return {'status': 'PASS', 'ordinary_AC_goal_solved': False,
            'braid_cyclic_preimage_all_n_at_least_2': True,
            'torus_cyclic_preimage_n_mod12': [3, 8],
            'arbitrary_tail_representative_families': 29,
            'short_tails_recomputed_and_independently_folded': 123901,
            'signed_line_DAG_checks': 950416,
            'unbounded_extension_proved_in_reports': True,
            'arbitrary_interspersed_AC_moves_covered': False}


def cyclic_checks():
    """Audit the explicit full cap-22 certificate with independent code."""
    py = sys.executable
    with tempfile.TemporaryDirectory(prefix='ac-cyclic-checks-') as directory:
        tsv = str(Path(directory) / 'states.tsv')
        output = Path(directory) / 'review.json'
        certificate = 'certificates/cyclic22_component_manifest.json'
        conversion = run(py, 'experiments/cyclic_catalogue_to_tsv.py', certificate, tsv)
        assert conversion['rows'] == 258032
        binary = str(Path(directory) / 'verify_cyclic')
        run('c++', '-std=c++17', '-O3', 'experiments/verify_full_cyclic_component.cpp',
            '-o', binary, json_output=False)
        run(binary, tsv, '22', str(output), json_output=False)
        audit = json.loads(output.read_text())
        assert audit['status'] == 'PASS' and audit['canonical_states'] == 258032
        assert audit['all_menu_candidates_checked'] == 193140064
        assert audit['admitted_neighbor_checks'] == 10204280
        assert audit['positive_tail_candidates_checked'] == 50688
        assert audit['minimum_cyclic_sum'] == 13
        assert audit['all_states_reachable_from_original_AK3']
        assert audit['closed_under_full_geometric_neighbor_menu']
        run(py, 'experiments/scan_cyclic_primitives.py', certificate,
            '--output', str(output), json_output=False)
        primitive = json.loads(output.read_text())
        assert primitive['status'] == 'PASS'
        assert primitive['catalogue_states'] == 258032
        assert primitive['distinct_cyclic_coordinates_tested'] == 179630
        assert primitive['primitive_coordinates'] == []
        assert primitive['catalogue_sha256'] == '2c8d0ac4c58f590de7151eae3dd09577d2365bf0e858887d801ce24c5c609c8e'
        for name, expected_moves in (('length14_cap18', 32), ('length13_cap18', 43),
                                     ('n_ak2_cyclic13', 46)):
            replay = run(py, 'experiments/elementary_verify.py', 'certificates/'+name+'.json')
            assert replay['moves'] == expected_moves and replay['peak_total_length'] == 18
            if name == 'n_ak2_cyclic13':
                assert replay['endpoint'] == ['x', 'y']
    return {'status': 'PASS', 'ordinary_AC_goal_solved': False,
            'cyclic_cap_replayed': 22, 'minimum_required_cyclic_peak': 23,
            'canonical_states': 258032, 'all_menu_candidates_checked': 193140064,
            'admitted_neighbor_checks': 10204280,
            'independent_canonicalizer_and_connectedness': True,
            'primitive_coordinate_scan_replayed': True,
            'AK3_short_waypoint_moves': [32, 43], 'AK3_waypoint_raw_peaks': [18, 18],
            'AK2_basis_control_strict_moves': 46}


def main(cpp=False, packed=False):
    py = sys.executable
    tail_audit = tail_checks()
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
    finite_k = run(py, 'experiments/twisted_magnus.py', '--degree', '5', '--group-order')
    assert finite_k['complete_twisted_orbit'] and finite_k['orbit_states'] == 65536
    assert finite_k['finite_semidirect_quotient_order'] == 12582912
    assert finite_k['candidate_k_residues_seen'] == []
    rank3 = run(py, 'experiments/rank3_compact_quotient.py')
    assert rank3['finite_semidirect_group_order'] == 2421875 and rank3['candidate_k_residues_seen'] == []
    rank3_check = run(py, 'experiments/rank3_mod5_independent.py')
    assert rank3_check['all_parameters_excluded'] and rank3_check['central_normal_forms_checked'] == 625
    further = run(py, 'experiments/second_hump_compact.py')
    assert further['finite_semidirect_group_order'] == 312500 and further['candidate_k_residues_seen'] == []
    further_check = run(py, 'experiments/second_hump_mod5_independent.py')
    assert further_check['all_parameters_excluded'] and further_check['normal_forms_checked'] == 625
    branches = run(py, 'experiments/remaining_branch_obstructions.py')
    assert branches['both_relators_conjugate_to_original_power_in_B3']
    signed = run(py, 'experiments/signed_cycle_obstruction.py', '--verify', 'results/signed_cycle_results.json')
    assert signed['saved_AK3_signed_cycle_certificate_verified']
    m_control = run(py, 'experiments/elementary_verify.py', 'certificates/m_ak2_full.json')
    assert m_control['endpoint'] == ['x', 'y'] and m_control['moves'] == 246
    atlas = run(py, 'experiments/first_hump.py')
    assert atlas['enumeration']['braid8_in_torus']['raw_candidates'] == 32
    assert atlas['enumeration']['power9_in_braid']['raw_candidates'] == 432
    assert len(atlas['enumeration']['power9_signed_symmetry_classes']) == 6
    independent_catalogue = run(py, 'experiments/audit_hump_subgroups.py')
    assert independent_catalogue['literal_pairs_with_frozen_rotations_and_inverses'] == 5632
    central = run(py, 'experiments/central_search.py', '--depth', '6', '--budget', '1000000')
    assert central['complete'] and central['distance'] == 12
    optimized = run(py, 'experiments/elementary_verify.py', 'certificates/optimized_first_order_strict.json')
    assert optimized['moves'] == 533 and optimized['peak_total_length'] == 2502
    optimized_fox = run(py, 'experiments/verify_first_order.py', 'certificates/optimized_first_order.json.gz.b64')
    assert optimized_fox['expanded_single_generator_moves'] == 533
    with tempfile.TemporaryDirectory(prefix='ac-current-checks-') as directory:
        result_path = str(Path(directory) / 'result.json')
        catalogue = run(py, 'experiments/hump_catalogue_obstruction.py', '--verify',
                        'certificates/hump_catalogue_dag_certificate.json.gz.b64', '--output', result_path)
        assert catalogue['expanded_literal_pairs'] == 5632 and catalogue['certified_acyclic_line_graphs'] == 10720
        waypoint = run(py, 'experiments/verify_hump_waypoints.py', 'certificates/hump_low_peak_u1.json',
                       'certificates/hump_low_peak_u2.json', '--output', result_path)
        assert [entry['strict_moves'] for entry in waypoint['waypoints']] == [222, 179]
        expected = Path(directory) / 'second-central.json'
        expected.write_bytes(gzip.decompress(base64.b64decode((ROOT / 'results/second_central_results.json.gz.b64').read_bytes())))
        audit = run(py, 'experiments/review_second_central.py', 'certificates/optimized_first_order.json.gz.b64',
                    str(expected), '--strict', 'certificates/optimized_first_order_strict.json', '--output', result_path)
        assert [entry['next_central_l1'] for entry in audit['residuals']] == [322, 469]
        loop_path = str(Path(directory) / 'loop-strict.json')
        expanded_loop = run(py, 'experiments/expand_lift.py', 'certificates/central_lift_closed_loop.json.gz.b64', '--output', loop_path)
        assert expanded_loop['strict_moves'] == 4734
        loop = run(py, 'experiments/elementary_verify.py', loop_path)
        assert loop['endpoint'] == ['xxxYYYY', 'xyxYXY'] and loop['moves'] == 4734
    if cpp:
        cyclic_checks()
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
            finite_binary = str(Path(directory) / 'twisted_magnus')
            run('c++', '-std=c++17', '-O3', 'experiments/twisted_magnus_independent.cpp',
                '-o', finite_binary, json_output=False)
            finite_independent = run(finite_binary, '5')
            assert finite_independent['orbit_states'] == 65536 and finite_independent['candidate_k_residues_seen'] == []
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
                      'cyclic_AK3_peak_lower_bound': 23,
                      'cyclic_cap_replayed': 22 if cpp else None,
                      'MS3_to_AK3_strict_moves': 32, 'braid_quotient_distance': 10,
                      'torus_quotient_distance': 8, 'product_strict_certificate_moves': 191,
                      'minimal_braid_lifting_areas': [5, 13],
                      'first_order_quotient_word_operations': 205,
                      'first_order_quotient_strict_expansion': 531377,
                      'optimized_first_order_strict_moves': 533,
                      'optimized_lift_returns_to_AK3_loop_moves': 4734,
                      'next_central_defect_norms': [322, 469],
                      'literal_primitive_free_catalogue_pairs': 5632,
                      'new_actual_free_waypoint_strict_moves': [222, 179],
                      'arbitrary_tail_representative_families': tail_audit['arbitrary_tail_representative_families'],
                      'short_tails_recomputed_and_independently_folded': 123901,
                      'independent_Cpp_exhaustion_replayed': cpp,
                      'first_order_endpoint_fold_replayed': cpp}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cpp', action='store_true', help='also compile and run the original-state C++ search')
    parser.add_argument('--packed', action='store_true', help='also regenerate, audit and scan the full cap-21 component')
    parser.add_argument('--tails-only', action='store_true', help='replay only the new arbitrary-tail theorem controls')
    parser.add_argument('--cyclic-only', action='store_true', help='audit the full cyclic cap-22 certificate and short strict paths; needs C++17')
    args = parser.parse_args()
    if args.cyclic_only:
        print(json.dumps(cyclic_checks(), indent=2))
    elif args.tails_only:
        print(json.dumps(tail_checks(), indent=2))
    else:
        main(args.cpp, args.packed)
