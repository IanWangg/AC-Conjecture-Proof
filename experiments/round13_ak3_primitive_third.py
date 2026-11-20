"""Try all primitive slope families in the last chart of sampled three-block routes."""

import argparse
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
from pathlib import Path

from elementary_verify import inverse, reduce, replay
from euclidean_primitive_audit import primitive_cyclic_word
from free_waypoint_search import canonical, conj_ops, normalize
from round07_automorphism_transport import normalize_pair
from round08_ak3_acm_replay import compile_move
from round08_ak3_acm_search import cyclic_peak, scan
from round11_ak3_targeted_acm import BASIS
from round13_ak3_three_blocks import LEDGERS, ROOT
from stallings_search import apply, nielsen_move


def changed_basis(slot, left, negative):
    basis = list(BASIS)
    direct = basis[slot]
    donor = basis[1 - slot].swapcase() if negative else basis[1 - slot]
    basis[slot] = donor + direct if left else direct + donor
    return dict(zip('xyXY', (*basis, *map(inverse, basis))))


def image(word, automorphism):
    return reduce(''.join(automorphism[c] for c in word))


def primitive_to_basis(pair):
    assert primitive_cyclic_word(canonical(pair[0]))
    state = tuple(pair)
    inverse_marking = dict(zip('xyXY', 'xyXY'))
    descent = []
    while len(canonical(state[0])) > 1:
        candidates = []
        for slot in (0, 1):
            for left in (False, True):
                for negative in (False, True):
                    auto = changed_basis(slot, left, negative)
                    candidate = tuple(image(word, auto) for word in state)
                    candidates.append((len(canonical(candidate[0])), (slot, left, negative), candidate))
        length, move, candidate = min(candidates)
        assert length < len(canonical(state[0]))
        slot, left, negative = move
        inverse_marking = {k: image(v, inverse_marking)
                           for k, v in changed_basis(slot, left, not negative).items()}
        state = candidate
        descent.append(move)

    pivot = canonical(state[0]).lower()
    state, marked_moves = normalize(state, 0, pivot)
    while pivot in state[1].lower():
        at = state[1].lower().index(pivot)
        letter, suffix = state[1][at], state[1][at + 1:]
        inversion = [{'op': 'invert', 'i': 0}] if letter.islower() else []
        operations = (inversion + conj_ops(0, inverse(suffix)) + [{'op': 'multiply', 'i': 1, 'j': 0}]
                      + conj_ops(0, suffix) + inversion)
        for operation in operations:
            state = apply(state, operation)
        marked_moves.extend(operations)
    other = 'y' if pivot == 'x' else 'x'
    state, final_marked = normalize(state, 1, other)
    assert state == (pivot, other)
    marked_moves.extend(final_marked)

    moves = []
    for move in marked_moves:
        if move['op'] == 'conjugate':
            moves.extend(conj_ops(move['i'], inverse_marking[move['g']]))
        else:
            moves.append(move)
    state = tuple(inverse_marking[letter] for letter in (pivot, other))
    marked_basis = tuple(inverse_marking[letter] for letter in BASIS)
    moves += normalize_pair(state, marked_basis)
    state = marked_basis
    for slot, left, negative in reversed(descent):
        state, nielsen = nielsen_move(state, slot, left, negative)
        moves.extend(nielsen)
    assert state == BASIS
    replay({'format': 'ordinary-ac-elementary-v1', 'start': list(pair), 'target': list(BASIS), 'moves': moves})
    return moves


def check_primitive_control():
    pair = ('xxyxy', 'xyxxyXYX')
    assert len(canonical(pair[0])) > 1
    operations = primitive_to_basis(pair)
    certificate = {'format': 'ordinary-ac-elementary-v1', 'start': list(pair),
                   'target': list(BASIS), 'moves': operations}
    return {'start': pair, **replay(certificate), 'cyclic_peak': cyclic_peak(certificate)}


def chart_job(acm, depth, allocation, horizon, bases, pair, slot):
    return scan(acm, depth, allocation, horizon, bases, (pair, slot, ()))


def run(args):
    first = json.loads(args.first_receipt.read_text())
    pending = []
    for family in first['first_families']:
        r, d = family['pair']
        pending.extend((family['source'], r, d, h, stage) for h, stage in family['first_intermediates'])
    center_runs = []
    finals = {}
    accepted = None
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        def center(item):
            _, _, d, h, _ = item
            return chart_job(args.acm, args.center_depth, args.allocation, args.horizon, args.bases, (h, d), 1)
        for (number, r, d, h, first_stage), result in zip(pending, pool.map(center, pending)):
            center_runs.append({'pair': (h, d), **result})
            for e in result['words']:
                if e == d or len(e) + len(h) > args.energy:
                    continue
                finals.setdefault((h, e), (number, r, d, first_stage, result['stages']))

        def terminal(pair):
            return chart_job(args.acm, args.last_depth, args.allocation, 0, 0, pair, 0)

        screens = []
        for pair, result in zip(sorted(finals), pool.map(terminal, sorted(finals))):
            screens.append({'pair': pair, **result})
            if result['primitive_words']:
                h, e = pair
                primitive = min(result['primitive_words'], key=lambda word: (len(word), word))
                number, r, d, first_stage, center_stage = finals[pair]
                prefix = json.loads((ROOT / 'certificates' / LEDGERS[number]).read_text())
                first_block, _ = compile_move((r, d), 0, h, first_stage)
                center_block, _ = compile_move((h, d), 1, e, center_stage)
                last_block, _ = compile_move((h, e), 0, primitive, result['stages'])
                moves = prefix['moves'] + normalize_pair(tuple(prefix['target']), (r, d))
                moves += first_block['moves'] + center_block['moves'] + last_block['moves']
                moves += primitive_to_basis((primitive, e))
                certificate = {'format': 'ordinary-ac-elementary-v1', 'start': prefix['start'],
                               'target': list(BASIS), 'moves': moves}
                accepted = {'primitive': primitive, **replay(certificate), 'cyclic_peak': cyclic_peak(certificate)}
                if args.certificate:
                    args.certificate.write_text(json.dumps(certificate, separators=(',', ':')) + '\n')
                break
    def controls(records):
        return {'charts': len(records), 'allocation_stops': sum(r['incomplete_graph'] for r in records),
                'largest_completed_graph': max((max(r['graph_sizes']) for r in records), default=0),
                'completed_stage_histogram': {
                    stage: sum(r['stages'] == stage for r in records)
                    for stage in sorted({r['stages'] for r in records})},
                'slope_tails_checked': sum(r['primitive_tails'] for r in records),
                'interior_slopes_checked': sum(r['primitive_slopes'] for r in records)}
    return {'first_receipt_sha256': sha256(args.first_receipt.read_bytes()).hexdigest(),
            'positive_control': check_primitive_control(), 'center': controls(center_runs),
            'terminal': controls(screens), 'distinct_terminal_markings': len(finals),
            'intermediate_energy': args.energy, 'center_harvested': {
                str(n): sum(len(item['words']) == n for item in center_runs)
                for n in sorted({len(item['words']) for item in center_runs})},
            'verified_ak3_basis_path': accepted}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('acm', type=Path)
    parser.add_argument('first_receipt', type=Path)
    for name, default in {
        'center-depth': 3, 'last-depth': 3, 'allocation': 300000, 'horizon': 23, 'bases': 96,
        'energy': 42, 'workers': 3,
    }.items():
        parser.add_argument('--' + name, type=int, default=default)
    parser.add_argument('--certificate', type=Path)
    print(json.dumps(run(parser.parse_args()), indent=2))
