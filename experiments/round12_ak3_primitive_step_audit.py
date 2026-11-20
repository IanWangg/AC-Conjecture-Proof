"""Audit the one-product primitive scan against the whole rotation menu."""

import argparse
import json
from pathlib import Path
from random import Random
from struct import pack
import subprocess
from tempfile import TemporaryDirectory

from elementary_verify import inverse
from euclidean_primitive_audit import primitive_cyclic_word
from free_waypoint_search import cyclic
from round05_ak3_orbit_audit import rotations


def brute_hit(pair):
    for receiver, donor in (pair, pair[::-1]):
        for a in rotations(receiver):
            for oriented in (donor, inverse(donor)):
                for b in rotations(oriented):
                    if primitive_cyclic_word(cyclic(a + b)):
                        return True
    return False


def rows():
    rng = Random(864222)
    def sample(length):
        word = ''
        while len(word) < length:
            word += rng.choice([c for c in 'xyXY' if not word or c != inverse(word[-1])])
        return cyclic(word)
    yield ('yyyXX', 'yxYXyyX')  # A known reachable AK(2) control.
    yield ('xxxYYYY', 'xyxYXY')
    for _ in range(768):
        yield tuple(sample(rng.randrange(1, 22)) for anchor in range(2))


def check(executable):
    marked = sorted(set(rows()))
    tested = []
    with TemporaryDirectory() as dirname:
        input_path = Path(dirname) / 'input.tsv'
        def native(pairs):
            input_path.write_text(''.join('\t'.join(p) + '\n' for p in pairs))
            output = subprocess.check_output([str(executable), str(input_path), '1'],
                                             stderr=subprocess.DEVNULL)
            return json.loads(output)
        negatives = []
        consumed = 0
        for pair in marked:
            if not brute_hit(pair):
                negatives.append(pair)
                continue
            result = native([pair])
            assert result['rows_checked'] == 1 and result['hit']
            hit = result['hit']
            a, b = hit['receiver_rotation'], hit['donor_rotation']
            i = hit['receiver_index']
            assert hit['source'] == list(pair) and a in rotations(pair[i])
            assert b in rotations(pair[1 - i]) or b in rotations(inverse(pair[1 - i]))
            actual = cyclic(a + b)
            assert primitive_cyclic_word(actual) and actual in tuple(rotations(hit['primitive']))
            tested.append(hit)
            consumed += (len(a) + len(b) - len(actual)) // 2 >= min(len(a), len(b))
        result = native(negatives)
        assert result == {'rows_checked': len(negatives), 'complete': True, 'hit': None}
        ak2 = next(h for h in tested if h['source'] == ['yyyXX', 'yxYXyyX'])
        anchor = ('xxYYY', 'xyxYXY')
        encoded = [int('1' + ''.join(f'{"xXyY".index(c):02b}' for c in w), 2)
                   for w in (*ak2['source'], *anchor)]
        binary = Path(dirname) / 'boundary.bin'
        binary.write_bytes(pack('=4Q', *encoded))
        command = [str(executable), str(binary), '1', '--boundary']
        receipt = json.loads(subprocess.check_output(command, stderr=subprocess.DEVNULL))
        assert receipt == {'rows_checked': 1, 'complete': False,
                           'hit': {'anchor': list(anchor), 'last_edge': ak2}}
        binary.write_bytes(binary.read_bytes()[:-1])
        assert subprocess.run(command, capture_output=True).returncode != 0
    assert consumed and consumed < len(tested)
    return {'checked_distinct_pairs': len(marked), 'brute_negative_pairs': len(negatives),
            'witnessed_positive_pairs': len(tested), 'complete_consumption_examples': consumed,
            'ak2_positive_control': ak2, 'boundary_record_positive_control': receipt['hit'],
            'truncated_boundary_record_rejected': True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('executable', type=Path)
    print(json.dumps(check(parser.parse_args().executable.resolve()), indent=2))
