"""Run a bounded alternating ACM beam and retain labelled routes."""

import argparse
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import json
from pathlib import Path
import subprocess

from euclidean_primitive_audit import primitive_cyclic_word
from free_waypoint_search import canonical, cyclic
from round05_ak3_orbit_audit import MAPS, rotations
from round08_ak3_acm_replay import FORMAT, compile_move, inverse, replay
from stallings_search import apply


ROOT = Path(__file__).resolve().parents[1]
START = ('xxxYYYY', 'xyxYXY')
SEEDS = {
    'AK3': None,
    'W22': 'round06_ak3_marked_waypoint29',
    'W23': 'round07_ak3_marked_waypoint30',
    'chamber18': 'round07_ak3_waypoint_chamber18',
    **{f'entry{i}': f'round07_stable_proof_entry{i}' for i in range(4)},
}


def source_for(seed):
    name = SEEDS[seed]
    if name is None:
        return {'format': FORMAT, 'start': list(START), 'target': list(START), 'moves': []}
    source = json.loads((ROOT / 'certificates' / (name + '.json')).read_text())
    replay(source)
    return source


def scan(executable, stages, cap, horizon, bases, node):
    pair, slot, _ = node
    args = [str(executable), pair[slot], pair[1 - slot], str(stages), str(cap), '0',
            str(horizon), str(bases)]
    return json.loads(subprocess.check_output(args))


def order(node):
    pair, slot, route = node
    return (sum(map(len, pair)), max(map(len, pair)), pair, slot, route)


def record(node):
    pair, slot, route = node
    return {'pair': pair, 'next_receiver': slot, 'route': route}


def key(pair, slot):
    return tuple(map(canonical, pair)), slot


def search(seed, pair, runner, width, depth, maximum, workers):
    queue = [(pair, slot, ()) for slot in (0, 1)]
    seen = {key(pair, slot) for slot in (0, 1)}
    endpoints = {}
    rounds = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        for _ in range(depth):
            if not queue:
                break
            children = []
            metadata = {'inputs': len(queue), 'vertices': 0, 'return_states': 0,
                        'allocation_stops': 0, 'primitive_tails': 0, 'interior_slopes': 0,
                        'exact_primitive_hits': []}
            for node, scan_result in zip(queue, executor.map(runner, queue)):
                pair, slot, route = node
                metadata['vertices'] += scan_result['graph_sizes'][-1]
                metadata['return_states'] += scan_result['return_states']
                metadata['allocation_stops'] += int(scan_result['incomplete_graph'])
                metadata['primitive_tails'] += scan_result['primitive_tails']
                metadata['interior_slopes'] += scan_result['primitive_slopes']
                for word in scan_result['words']:
                    if canonical(pair[slot]) == word:
                        continue
                    changed = list(pair)
                    changed[slot] = word
                    changed = tuple(changed)
                    path = route + ((slot, word, scan_result['stages']),)
                    child = (changed, 1 - slot, path)
                    if word in scan_result['primitive_words']:
                        if not primitive_cyclic_word(word):
                            raise AssertionError('independent primitive check failed')
                        metadata['exact_primitive_hits'].append(record(child))
                    if sum(map(len, changed)) > maximum:
                        continue
                    state_key = key(changed, 1 - slot)
                    if state_key in seen:
                        continue
                    seen.add(state_key)
                    endpoints[state_key] = child
                    children.append(child)
            metadata['novel_states'] = len(children)
            rounds.append(metadata)
            queue = sorted(children, key=order)[:width]
    return {'seed': seed, 'rounds': rounds}, list(endpoints.values())


def catalogue_key(pair):
    encode = str.maketrans('xXyY', '0123')
    decode = str.maketrans('0123', 'xXyY')

    def cyclic_key(word):
        return min(min(rotations(word.translate(encode))),
                   min(rotations(inverse(word).translate(encode))))

    key = min(tuple(sorted((cyclic_key(w.translate(change)) for w in pair),
                           key=lambda word: (len(word), word))) for change in MAPS)
    return ('\t'.join(w.translate(decode) for w in key) + '\n').encode('ascii')


def memberships(path, pairs):
    outstanding = {catalogue_key(pair) for pair in pairs}
    present = set()
    with path.open('rb') as catalogue:
        for row in catalogue:
            if row in outstanding:
                outstanding.remove(row)
                present.add(row)
                if not outstanding:
                    break
    return present


def certify(seed, route):
    source = source_for(seed)
    pair = source['target']
    receipts = []
    for slot, word, stages in route:
        suffix, receipt = compile_move(pair, slot, word, stages)
        pair = suffix['target']
        source['moves'].extend(suffix['moves'])
        receipts.append(receipt)
    source['target'] = pair
    replay(source)
    return source, receipts


def cyclic_peak(certificate):
    state = tuple(certificate['start'])
    peak = sum(len(cyclic(word)) for word in state)
    for move in certificate['moves']:
        state = apply(state, move)
        peak = max(peak, sum(len(cyclic(word)) for word in state))
    if list(state) != certificate['target']:
        raise AssertionError('cyclic peak replay failed')
    return peak


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('executable', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--catalogue', type=Path)
    parser.add_argument('--certificates', type=Path)
    parser.add_argument('--workers', type=int, default=5)
    parser.add_argument('--stages', type=int, default=4)
    parser.add_argument('--allocation', type=int, default=350_000)
    parser.add_argument('--horizon', type=int, default=19)
    parser.add_argument('--bases', type=int, default=64)
    parser.add_argument('--width', type=int, default=20)
    parser.add_argument('--alternations', type=int, default=5)
    parser.add_argument('--maximum', type=int, default=34)
    args = parser.parse_args()
    runner = partial(scan, args.executable, args.stages, args.allocation, args.horizon, args.bases)
    control = runner((('xyxYXY', 'y'), 0, ()))
    if 'X' not in control['primitive_words']:
        raise AssertionError('exact primitive scan failed positive control')
    _, control_replay = compile_move(('xyxYXY', 'y'), 0, 'x', 1)
    results = []
    endpoints = []
    for seed in SEEDS:
        pair = tuple(source_for(seed)['target'])
        result, nodes = search(seed, pair, runner, args.width, args.alternations, args.maximum, args.workers)
        results.append(result)
        endpoints.append((pair, nodes))
    all_orbits = {catalogue_key(node[0]) for _, nodes in endpoints for node in nodes}
    present = set()
    certificates = {}
    if args.catalogue:
        present = memberships(args.catalogue, [node[0] for _, nodes in endpoints for node in nodes])
    for result, (pair, nodes) in zip(results, endpoints):
        result['start_pair'] = pair
        result['smallest_reached_pair'] = record(min(nodes, key=order)) if nodes else None
        result['visited_orbits'] = len({catalogue_key(node[0]) for node in nodes})
        if args.catalogue:
            unseen = [node for node in nodes if catalogue_key(node[0]) not in present]
            result['orbits_outside_catalogue'] = len({catalogue_key(node[0]) for node in unseen})
            result['smallest_outside_catalogue'] = [record(node) for node in sorted(unseen, key=order)[:7]]
            if unseen and args.certificates:
                seed = result['seed']
                endpoint = result['smallest_outside_catalogue'][0]
                certificate, receipts = certify(seed, endpoint['route'])
                filename = f'round08_ak3_acm_{seed.lower()}.json'
                (args.certificates / filename).write_text(json.dumps(certificate, separators=(',', ':')) + '\n')
                certificates[seed] = {'file': filename, 'route': endpoint['route'],
                                      'cyclic_peak': cyclic_peak(certificate), 'replay': replay(certificate),
                                      'suffix_receipts': receipts}
    params = {key: value for key, value in vars(args).items() if isinstance(value, int)}
    output = {'parameters': params, 'results': results, 'positive_control': control_replay,
              'distinct_reached_orbits': len(all_orbits), 'strict_certificates': certificates}
    if args.catalogue:
        output['orbits_outside_catalogue'] = [row.decode('ascii').split() for row in sorted(all_orbits - present)]
    args.output.write_text(json.dumps(output, indent=2) + '\n')


if __name__ == '__main__':
    main()
