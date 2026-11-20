"""Prepare the two Whitehead-product seed menus and check their receipts."""

import argparse
import json
from collections import Counter, deque
from pathlib import Path

from euclidean_primitive_audit import primitive_cyclic_word
from round01_geometric_archive import image
from round06_stable_proof_cap23_charts import compact_row
from round07_stable_proof_local_audit import successors


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text())


def pair(line):
    return tuple(line.split())


def words(path):
    return [pair(line) for line in path.read_text().splitlines()]


def energy(state):
    return sum(map(len, state))


def state(key):
    return tuple(key.decode('ascii').split())


def write_tsv(path, pairs):
    path.write_text(''.join('\t'.join(row) + '\n' for row in pairs))


def seeds(work):
    source = ROOT / 'results/round09_stable_proof_c22_energy16_anchors.json'
    stable = read(source)['shortest_unanchored_sources'][:12]
    write_tsv(work / 'targets.tsv', [row['projected'] for row in stable])
    files = sorted((ROOT / 'certificates').glob('round08_ak3_acm_*.json'))
    files.append(ROOT / 'certificates/round08_stable_proof_branch27_ordinary.json')
    write_tsv(work / 'ordinary-seeds.tsv', [read(file)['target'] for file in files])


def whitehead_path(before, after):
    start, end = compact_row(before), compact_row(after)
    seen = {start: None}
    pending = deque([start])
    while end not in seen:
        at = pending.popleft()
        for letter, donor in (('x', 'y'), ('y', 'x')):
            for sign in (donor, donor.upper()):
                for replacement in (letter + sign, sign + letter):
                    result = image(state(at), letter, replacement)
                    key = compact_row(result)
                    if energy(result) <= energy(before) and key not in seen:
                        seen[key] = at, {'generator': letter, 'replacement': replacement,
                                         'raw_image': result, 'signed_key': state(key)}
                        pending.append(key)
    path = []
    while seen[end] is not None:
        end, step = seen[end]
        path.append(step)
    return path[::-1]


def edge_rows(path):
    return {row[:2]: (row[2:4], row[4:6], row[6:8]) for row in words(path)}


def joins(table, sources):
    records = []
    for target in sources:
        at = target
        route = []
        while at in table:
            parent, mark, product = table[at]
            tested, _, _ = successors(mark, 36)
            assert compact_row(product) in tested
            route.append({'parent': parent, 'source_marking': mark, 'product_pair': product,
                          'child': at, 'source_marking_changes': whitehead_path(parent, mark),
                          'target_marking_changes': whitehead_path(product, at)})
            at = parent
        records.append({'root': at, 'cap30_target': target, 'edges': route[::-1]})
    return records


def audit(work, cap30):
    stable_seeds = words(work / 'targets.tsv')
    checked = {compact_row(row): index for index, row in enumerate(stable_seeds)}
    membership = set((work / 'e20x36.tsv').read_bytes().splitlines(keepends=True))
    group = sorted(index for key, index in checked.items() if key in membership)
    assert len(group) == 11 and 4 not in group
    scans = {}
    for kind in ('ordinary', 'stable'):
        report = read(work / f'min{kind}.json')
        catalogue = words(work / f'min{kind}.tsv')
        assert not report['primitive_product_hits'] and len(set(catalogue)) == report['generated_short_classes']
        assert report['seed_classes'] + sum(layer['new_short_classes'] for layer in report['layers']) == len(catalogue)
        assert not any(primitive_cyclic_word(row) for p in catalogue for row in p)
        scans[kind] = {**report, 'energy_histogram': dict(sorted(Counter(map(energy, catalogue)).items()))}
    con = read(work / 'control.json')
    guide = words(work / 'control-seed.tsv')
    assert len(guide) == 1 and not any(primitive_cyclic_word(word) for word in guide[0])
    counts = []
    for child, (parent, mark, product) in edge_rows(work / 'control.edges.tsv').items():
        if any(primitive_cyclic_word(word) for word in child):
            assert compact_row(product) in successors(mark, 16)[0]
            assert not any(primitive_cyclic_word(word) for word in parent)
            assert compact_row(product) == compact_row(child)
            counts.append(product)
    assert counts and len(counts) == con['primitive_product_hits']

    stable_keys = set((work / 'minstable.tsv').read_bytes().splitlines(keepends=True))
    with cap30.open('rb') as stream:
        targets = sorted(state(row) for row in stream if row in stable_keys)
    verified = joins(edge_rows(work / 'edgesstable.tsv'), targets)
    assert len(verified) == 8 and {x['root'] for x in verified} == {('xxyXXYY', 'xyxYXyyyxYXy')}
    projection = stable_seeds[4]
    outlier_mark = whitehead_path(projection, verified[0]['root'])
    assert outlier_mark
    return {'short_stable_projection_pairs': stable_seeds, 'shared_cap36_component_indices_zero_based': group,
            'sharp_ordinary_cyclic_entry_peak_for_shared_component': 37,
            'scans': scans, 'positive_control': {**con, 'primitive_pairs': counts},
            'remaining_projection_to_seed_whitehead_moves': outlier_mark,
            'remaining_projection_C30_routes': verified,
            'nonprimitive_and_geometry': {label: read(work / file) for label, file in (
                ('stable_geometry', 'minstable.geometry.json'), ('stable_reverse_archive', 'minstable.reverse56.json'),
                ('ordinary_through_energy23_geometry', 'minordinary.low23.geometry.json'),
                ('ordinary_through_energy23_reverse_archive', 'minordinary.low23.reverse56.json'))}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('seeds', 'audit'))
    parser.add_argument('work', type=Path)
    parser.add_argument('--cap30', type=Path)
    args = parser.parse_args()
    if args.mode == 'seeds':
        seeds(args.work)
    else:
        print(json.dumps(audit(args.work, args.cap30), indent=2))
