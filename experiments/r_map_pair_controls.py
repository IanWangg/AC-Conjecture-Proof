"""Positive/negative controls and a strict AK2 calibration for R's detector."""
import argparse
from collections import deque
import json
from math import gcd
from pathlib import Path
from primitive_map_pairs import (ALPHABETS,compact_absence,decide,fold,inverse,
                                 reduce,verify_absence)


def mechanical(a,b):
    """A cyclic Christoffel representative, independently from Farey updates."""
    assert gcd(a,b) == 1
    length = a+b
    return ''.join('x' if ((i+1)*a)//length > (i*a)//length else 'y'
                   for i in range(length))


def reduced_words(cap):
    layer = ['']
    yield ''
    for _ in range(cap):
        layer = [w+c for w in layer for c in 'xXyY'
                 if not w or c != w[-1].swapcase()]
        yield from layer


def controls():
    positive = negative = 0
    largest = 0
    for a in range(13):
        for b in range(13):
            if gcd(a,b) != 1:
                continue
            original = mechanical(a,b)
            for alphabet in ALPHABETS:
                word = original.translate(str.maketrans(dict(zip('xy',alphabet))))
                result = decide(fold((word,)))
                assert result['status'] == 'PRIMITIVE'
                positive += 1
                result = decide(fold((word*2,)),save_certificate=True)
                assert result['status'] == 'ABSENT'
                verify_absence(result)
                verify_absence(compact_absence(result))
                largest = max(largest,*(r['pair_states_discovered'] for r in result['alphabets']))
                negative += 1
    # Independent conjugating tails, including arbitrary based hairs, do not
    # confuse primitive loops at any vertex with loops only at the basepoint.
    tails = 0
    p,b = 'xxxYYYY','xyxYXY'
    for q in reduced_words(6):
        result = decide(fold((p,reduce(q+b+inverse(q)))))
        assert result['status'] == 'ABSENT'
        tails += 1
    initial = decide(fold((p,b)),save_certificate=True)
    assert decide(fold((p,b)),budget=1)['status'] == 'INCOMPLETE'
    damaged = json.loads(json.dumps(initial))
    damaged['alphabets'][0]['closed_map_pairs'].pop(0)
    try:
        verify_absence(damaged)
    except AssertionError:
        pass
    else:
        raise AssertionError('missing initial pair accepted')
    assert positive == negative == 372 and tails == 1457
    return {'status':'PASS','ordinary_AC_goal_solved':False,
            'positive_signed_Christoffel_cycle_graphs':positive,
            'negative_proper_square_cycle_graphs':negative,
            'all_initial_AK3_relative_tails_through_length6':tails,
            'budget_stop_correctly_INCOMPLETE':True,
            'tampered_closed_certificate_rejected':True,
            'maximum_pair_states_in_proper_square_controls':largest}


def ak2_control(source,directory):
    from complete_primitive import complete
    from elementary_verify import replay
    old = json.loads(Path(source).read_text())
    prefix = old['moves'][:-3]
    cert = {'format':'ordinary-ac-elementary-v1','start':old['start'],
            'target':['XXyyy','XYxYYxy'],'moves':prefix}
    replay(cert)
    detection = decide(fold(cert['target']))
    assert detection['status'] == 'PRIMITIVE'
    found = detection['witness']['based_primitive_word']
    assert found == reduce(cert['target'][1]+inverse(cert['target'][0])) == 'XYxYYxYYxx'
    cert['moves'] += [{'op':'invert','i':0},{'op':'multiply','i':1,'j':0},{'op':'invert','i':0}]
    cert['target'] = ['XXyyy',found]
    cert['scope'] = 'R finite-map witness calibrated on known AK2; no AK3 claim'
    full = complete(cert)
    first,last = replay(cert),replay(full)
    assert first['moves'] == 17 and first['peak_total_length'] == 15
    assert last['moves'] == 337 and last['peak_total_length'] == 33
    assert last['endpoint'] == ['x','y']
    target = Path(directory)
    target.mkdir(parents=True,exist_ok=True)
    (target/'r_ak2_map_waypoint.json').write_text(json.dumps(cert,indent=2)+'\n')
    (target/'r_ak2_map_full.json').write_text(json.dumps(full,indent=2)+'\n')
    return {'status':'PASS','ordinary_AC_goal_solved':False,
            'actual_detector_witness':detection['witness'],
            'basis_expression_for_based_witness':'B*A^-1',
            'strict_primitive_waypoint':first,'strict_AK2_completion':last,
            'completion_compiler_shared_with_M':True,
            'not_an_AK3_solution':True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',required=True)
    parser.add_argument('--ak2-source')
    parser.add_argument('--directory')
    args = parser.parse_args()
    result = controls()
    if args.ak2_source:
        assert args.directory
        result['AK2_pipeline'] = ak2_control(args.ak2_source,args.directory)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
