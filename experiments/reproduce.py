"""Replay the bounded research checks; nothing here claims an AC solution."""
import argparse
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


def main(cpp=False):
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
    print(json.dumps({'status': 'PASS', 'ordinary_AC_goal_solved': False,
                      'raw_AK3_peak_lower_bound': 19, 'cyclic_AK3_peak_lower_bound': 15,
                      'MS3_to_AK3_strict_moves': 32, 'braid_quotient_distance': 10,
                      'independent_Cpp_exhaustion_replayed': cpp}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cpp', action='store_true', help='also compile and run the original-state C++ search')
    main(parser.parse_args().cpp)
