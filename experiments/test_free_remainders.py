"""Test actual free remainders of the finite correction variants.

This is a finite experiment only. A return to AK(3)'s cyclic orbit is not
an invariant of arbitrary AC paths, and no nontriviality inference is made.
"""
import argparse
import itertools
import json
from pathlib import Path
import optimized_correction as o
from dehn_shorten import shorten


def orbit(word):
    words=[]
    for s in (word,o.m.free_inverse(word)):
        words.extend(s[k:]+s[:k] for k in range(len(s)))
    return min(words)


def canonical(pair):
    return sorted(orbit(w) for w in pair)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('prefixes',nargs='+')
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    representative=o.Representatives()
    initial=['xxxYYYY','xyxYXY'];records=[]
    for path in args.prefixes:
        parent=json.loads(Path(path).read_text())
        for order in ((0,1),(1,0)):
            for own_first in itertools.product((False,True),repeat=2):
                cert=o.compile_prefix(parent,representative,order,own_first)
                target,moves,trace=shorten(cert['target'])
                # Recheck the appended ledger against its actual free start.
                state=cert['target'][:]
                for move in moves:state=o.f.apply(state,move)
                assert state==target
                record={'prefix':Path(path).name,'coordinate_order':order,'own_first':own_first,
                        'initial_lengths':list(map(len,cert['target'])),
                        'final_lengths':list(map(len,target)),'final_words':target,
                        'shortening_steps':len(trace),
                        'returns_to_initial_cyclic_orbit':canonical(target)==canonical(initial),
                        'free_basis_reached':sorted(target)==['x','y']}
                records.append(record)
                print(json.dumps(record),flush=True)
    report={'variants':records,'variant_count':len(records),
            'all_returned_to_initial_cyclic_orbit':all(r['returns_to_initial_cyclic_orbit'] for r in records),
            'any_free_basis':any(r['free_basis_reached'] for r in records),
            'scope':'Finite construction variants and greedy free-group probe only; not a global obstruction'}
    Path(args.output).write_text(json.dumps(report,indent=2)+'\n')
