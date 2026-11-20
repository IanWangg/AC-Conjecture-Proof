"""Search three alternating ordinary receiving blocks from short AK(3) waypoints."""

import argparse
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from hashlib import sha256
import json
from pathlib import Path
import sys

from elementary_verify import reduce, replay
from free_waypoint_search import canonical
from round07_automorphism_transport import normalize_pair
from round08_ac_proof_two_donors import reverse_moves
from round08_ak3_acm_replay import compile_move
from round08_ak3_acm_search import cyclic_peak, scan
from round11_ak3_targeted_acm import BASIS, load, reverse_suffix
from round12_ak3_reciprocal_charts import candidate_donors, chart, chart_summary, reverse_index


ROOT = Path(__file__).resolve().parents[1]
LEDGERS = ('round11_ak3_cap32_minimum.json', 'round12_ak3_second_energy20.json')


def blocks(r, d, h, e, s, stages, suffix, prefix=None):
    a, b, c = stages
    first, _ = compile_move((r, d), 0, h, a)
    center, _ = compile_move((h, d), 1, e, b)
    last, _ = compile_move((s, e), 0, h, c)
    assert first['target'] == center['start']
    assert center['target'] == last['target']
    endpoint, tail = suffix
    moves = first['moves'] + center['moves'] + list(reverse_moves(last['moves']))
    moves += normalize_pair((s, e), endpoint) + tail
    if prefix is None:
        start = (r, d)
    else:
        start = prefix['start']
        moves = prefix['moves'] + normalize_pair(tuple(prefix['target']), (r, d)) + moves
    certificate = {'format': 'ordinary-ac-elementary-v1', 'start': list(start),
                   'target': list(BASIS), 'moves': moves}
    return certificate, {**replay(certificate), 'cyclic_peak': cyclic_peak(certificate),
                         'receiving_block_instructions': [len(record['moves'])
                                                          for record in (first, center, last)]}


def control(targeted):
    suffix = load('correct')
    s, e = tuple(map(canonical, suffix['start']))
    h = canonical(reduce(s + e))
    d = canonical(reduce(e + h))
    r = canonical(reduce(h + d))
    assert len({r, d, h, e, s}) == 5
    scans = [chart(targeted, pair, [word], 2, 20000)
             for pair, word in (((r, d), h), ((d, h), e), ((s, e), h))]
    stages = tuple(result['hits'][0][1] for result in scans)
    ledger, receipt = blocks(r, d, h, e, s, stages, (tuple(suffix['start']), suffix['moves']))
    assert ledger['target'] == list(BASIS)
    return {'forward': [r, d], 'reverse': [s, e], 'common_receiver': h, 'stages': stages, **receipt}


def sources(forward, acm, targeted, depth, allocation, horizon, bases):
    families = []
    for number, prefix in enumerate(forward):
        pair = tuple(map(canonical, prefix['target']))
        for r, d in (pair, pair[::-1]):
            harvest = scan(acm, depth, allocation, horizon, bases, ((r, d), 0, ()))
            assert not harvest['primitive_words']
            known = set()
            if number == 0 and d == canonical('xxxxxyXXy'):
                report = json.loads((ROOT / 'results/round12_ak3_torus_chart.json').read_text())
                known.update(row['donor_cyclic_key'] for row in report['exact_conjugacy_hits'])
            if number == 1 and d == canonical('xxxxyXXYY'):
                report = json.loads((ROOT / 'results/round12_ac_proof_amalgam_archive.json').read_text())
                known.update(row['reverse_donor'] for row in report['exact_conjugacy_hits'])
            choices = (set(harvest['words']) | known) - {r}
            check = chart(targeted, (r, d), sorted(choices), depth, allocation)
            assert choices == {target for target, _ in check['hits']}
            families.append({'source': number, 'pair': (r, d), 'harvest': harvest, 'extra_exact_contacts': sorted(known),
                             'first_intermediates': check['hits']})
    return families


def join(args):
    reverse, reverse_count = reverse_index(args.archive, args.reverse_energy)
    prefixes = [json.loads((ROOT / 'certificates' / name).read_text()) for name in LEDGERS]
    for prefix in prefixes:
        replay(prefix)
    positive = control(args.targeted)
    families = sources(prefixes, args.acm, args.targeted, args.first_depth, args.first_allocation,
                       args.first_horizon, args.first_bases)
    all_donors = sorted(reverse)
    contacts = defaultdict(lambda: defaultdict(list))
    center_runs = []
    winners = []
    normal = []
    for family in families:
        r, d = family['pair']
        for h, first_stage in family['first_intermediates']:
            words = [e for e in candidate_donors(h, all_donors) if e != d]
            if words:
                normal.append((family['source'], r, d, h, first_stage, words))

    def center(item):
        number, r, d, h, first_stage, targets = item
        scan = chart(args.index, (d, h), targets, args.center_depth, args.center_allocation)
        return number, r, d, h, first_stage, len(targets), scan

    reverse_runs = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for number, r, d, h, first_stage, count, result in pool.map(center, normal):
            center_runs.append({'pair': (d, h), 'word_checks': count, **result})
            for e, center_stage in result['hits']:
                for s in reverse[e]:
                    if s != h:
                        contacts[s, e][h].append((number, r, d, first_stage, center_stage))

        def reverse_scan(item):
            (s, e), common = item
            scan = chart(args.targeted if len(common) == 1 else args.index, (s, e), sorted(common),
                         args.reverse_depth, args.reverse_allocation)
            return s, e, len(common), scan

        if args.trace:
            print(f'Center charts {len(center_runs)}, third charts {len(contacts)}', flush=True, file=sys.stderr)
        for s, e, count, result in pool.map(reverse_scan, sorted(contacts.items())):
            reverse_runs.append({'pair': (s, e), 'word_checks': count, **result})
            for h, reverse_stage in result['hits']:
                for number, r, d, first_stage, center_stage in contacts[s, e][h]:
                    stages = first_stage, center_stage, reverse_stage
                    suffix = reverse_suffix(reverse[e][s], args.archives)
                    certificate, receipt = blocks(r, d, h, e, s, stages, suffix, prefixes[number])
                    winners.append({'forward': (r, d), 'reverse': (s, e), 'common_receiver': h,
                                    'stages': stages, 'source': number, **receipt})
                    if args.certificate:
                        args.certificate.write_text(json.dumps(certificate, separators=(',', ':')) + '\n')
                    break
                break
            if winners:
                break
    return {'archive_pairs': reverse_count, 'archive_donors': len(reverse),
            'archive_sha256': sha256(args.archive.read_bytes()).hexdigest(),
            'positive_control': positive, 'first_families': families,
            'center': chart_summary(center_runs), 'reverse': chart_summary(reverse_runs),
            'planned_reverse_charts': len(contacts), 'joins': winners}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('acm', 'targeted', 'index', 'archive', 'archives'):
        parser.add_argument(name, type=Path)
    for name, default in {
        'first-depth': 4, 'first-allocation': 1000000, 'first-horizon': 23, 'first-bases': 256,
        'center-depth': 3, 'center-allocation': 300000, 'reverse-depth': 2,
        'reverse-allocation': 225000, 'reverse-energy': 24, 'workers': 3,
    }.items():
        parser.add_argument('--' + name, default=default, type=int)
    parser.add_argument('--certificate', type=Path)
    parser.add_argument('--trace', action='store_true')
    print(json.dumps(join(parser.parse_args()), indent=2))
