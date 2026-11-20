"""Independently replay the complete middle-product menu in marked rank two."""

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

from elementary_verify import inverse, replay
from euclidean_primitive_audit import primitive_cyclic_word
from free_waypoint_search import canonical, variants, words_upto
from round04_stable_proof_paths import edge
from round07_automorphism_transport import normalize_pair
from round08_ak3_acm_replay import compile_move
from round08_ak3_acm_search import catalogue_key, cyclic_peak
from round13_ak3_primitive_third import primitive_to_basis
from round13_ak3_three_blocks import LEDGERS, ROOT


def record_choices(first_receipt):
    records = []
    for family in json.loads(first_receipt.read_text())['first_families']:
        r, d = family['pair']
        records.extend((family['source'], r, d, h, stage) for h, stage in family['first_intermediates'])
    return records


def independent_menu(h, d, cap):
    if len(h) + abs(len(h) - len(d)) > cap:
        return set(), 0
    answer, checks = set(), 0
    bridges = tuple(words_upto(max(0, (cap - len(d) - 2 * len(h)) // 2)))
    for a in variants(d):
        for b in variants(h):
            for bridge in bridges:
                word = canonical(a + bridge + b + inverse(bridge))
                checks += 1
                if word and word != d and len(h) + len(word) <= cap:
                    answer.add(word)
    return answer, checks


def prefix(record, receiver, cap):
    number, r, d, h, stage = record
    entry = json.loads((ROOT / 'certificates' / LEDGERS[number]).read_text())
    first, _ = compile_move((r, d), 0, h, stage)
    center, steps = edge((h, d), tuple(sorted((h, receiver))), max(cap, len(h) + len(d)), 'xXyY')
    assert center == (h, receiver)
    moves = entry['moves'] + normalize_pair(tuple(entry['target']), (r, d)) + first['moves'] + steps
    return {'format': 'ordinary-ac-elementary-v1', 'start': entry['start'],
            'target': list(center), 'moves': moves}


def low_membership(targets, catalogues, cap):
    keys = {catalogue_key(pair): pair for pair in targets if sum(map(len, pair)) <= cap}
    before = len(keys)
    counts = []
    for catalogue in catalogues:
        count = 0
        with catalogue.open('rb') as rows:
            for row in rows:
                if len(row) - 2 > cap:
                    break
                if row in keys:
                    count += 1
                    del keys[row]
                    if not keys:
                        break
        counts.append(count)
    return {'through_energy': cap, 'distinct_keys': before, 'catalogue_matches': counts,
            'missing': sorted(keys.values())}


def run(args):
    records = record_choices(args.first_receipt)
    data = ''.join(h + '\t' + d + '\n' for _, _, d, h, _ in records)
    result = subprocess.run([str(args.exact_center), str(args.energy)], input=data, text=True,
                            check=True, capture_output=True)
    reported = json.loads(result.stderr)
    groups = defaultdict(set)
    targets = {}
    for row in result.stdout.splitlines():
        position, h, product = row.split()
        at = int(position)
        assert h == records[at][3]
        receiver = canonical(product)
        groups[at].add(receiver)
        targets.setdefault((h, receiver), records[at])
    checks = 0
    for number, (_, _, d, h, _) in enumerate(records):
        independent, count = independent_menu(h, d, args.energy)
        assert independent == groups[number]
        checks += count
    assert all(not any(map(primitive_cyclic_word, pair)) for pair in targets)
    with TemporaryDirectory() as directory:
        file = Path(directory) / 'outputs.tsv'
        payload = ''.join('\t'.join(pair) + '\n' for pair in sorted(targets))
        file.write_text(payload)
        scan = json.loads(subprocess.check_output([str(args.primitive_step), str(file), '3'], text=True))
    successful = None
    if scan['hit']:
        hit = scan['hit']
        pair = tuple(hit['source'])
        primitive = canonical(hit['primitive'])
        slotted = list(pair)
        slot = hit['receiver_index']
        slotted[slot] = primitive
        answer = prefix(targets[pair], pair[1], args.energy)
        cap = max(sum(map(len, pair)), sum(map(len, slotted)))
        endpoint, steps = edge(pair, tuple(sorted(slotted)), cap, 'xXyY')
        assert endpoint == tuple(slotted)
        oriented = (primitive, endpoint[1 - slot])
        answer['moves'] += steps + normalize_pair(endpoint, oriented) + primitive_to_basis(oriented)
        answer['target'] = ['x', 'y']
        successful = {**replay(answer), 'cyclic_peak': cyclic_peak(answer)}
        if args.certificate:
            args.certificate.write_text(json.dumps(answer, separators=(',', ':')) + '\n')
    return {'input_receipt_sha256': sha256(args.first_receipt.read_bytes()).hexdigest(),
            'middle_energy_cap': args.energy, 'native': reported, 'independent_rotation_checks': checks,
            'distinct_marked_middle_outputs': len(targets), 'middle_outputs_sha256': sha256(payload.encode()).hexdigest(),
            'middle_energy_histogram': dict(sorted(Counter(sum(map(len, pair)) for pair in targets).items())),
            'uncapped_final_product': scan, 'strict_success': successful,
            'optional_low_membership': low_membership(targets, args.catalogues, 31) if args.catalogues else None}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('exact_center', 'primitive_step', 'first_receipt'):
        parser.add_argument(name, type=Path)
    parser.add_argument('--energy', type=int, default=38)
    parser.add_argument('--certificate', type=Path)
    parser.add_argument('--catalogues', nargs=2, type=Path)
    print(json.dumps(run(parser.parse_args()), indent=2))
