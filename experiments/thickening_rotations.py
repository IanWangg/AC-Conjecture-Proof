"""Finite paired-rotation genus test for cyclic presentation words.

Darts are Whitehead-link corners.  Cyclic orders at x,y determine the
opposite orders at X,Y via the sheet pairing along each generator edge.
This module deliberately enumerates every positive-end cyclic order.
"""
import argparse
from collections import Counter
import itertools
import json
import math
from pathlib import Path

LETTERS = 'xXyY'


def link(words):
    incidence = [[] for _ in LETTERS]
    paired = {}
    endpoints = []
    offset = 0
    for word in words:
        assert word and all(c in LETTERS for c in word)
        assert all(word[i].swapcase() != word[(i+1) % len(word)] for i in range(len(word)))
        for i, a in enumerate(word):
            b = word[(i+1) % len(word)]
            ends = (LETTERS.index(a.swapcase()), LETTERS.index(b))
            endpoints.append(ends)
            for k, v in enumerate(ends):
                incidence[v].append(2*(offset+i)+k)
        for i, a in enumerate(word):
            before = 2*(offset+(i-1) % len(word))+1
            after = 2*(offset+i)
            paired[before] = after
            paired[after] = before
        offset += len(word)
    assert all(len(incidence[i]) == len(incidence[i^1]) for i in (0,2))
    return incidence, paired, endpoints


def cyclic_orders(darts):
    if not darts:
        yield ()
    else:
        for tail in itertools.permutations(darts[1:]):
            yield (darts[0],)+tail


def analyse_orders(words, orders):
    incidence, paired, endpoints = link(words)
    assert len(orders) == 4
    sigma = {}
    for v, order in enumerate(orders):
        assert sorted(order) == sorted(incidence[v])
        sigma.update({d:order[(i+1)%len(order)] for i,d in enumerate(order)})
    for v in (0,2):
        if not orders[v]:
            continue
        expected = tuple(paired[d] for d in orders[v][::-1])
        actual = tuple(orders[v^1])
        assert any(actual == expected[i:]+expected[:i] for i in range(len(expected)))
    unseen = set(sigma)
    faces = []
    while unseen:
        at = min(unseen)
        face = []
        while at not in face:
            assert at in unseen
            unseen.remove(at)
            face.append(at)
            at = sigma[at^1]
        assert at == face[0]
        faces.append(face)
    roots = list(range(4))
    def root(v):
        while roots[v] != v:
            v = roots[v]
        return v
    for a,b in endpoints:
        roots[root(a)] = root(b)
    nonempty = [v for v in range(4) if incidence[v]]
    components = len({root(v) for v in nonempty})
    vertices = len(nonempty)
    genus_twice = 2*components-vertices+len(endpoints)-len(faces)
    assert genus_twice >= 0 and genus_twice % 2 == 0
    return {'total_genus': genus_twice//2, 'faces': faces,
            'nonempty_components': components, 'nonempty_vertices': vertices,
            'edges': len(endpoints)}


def decide(words, budget=0):
    incidence, paired, endpoints = link(words)
    total = math.prod(math.factorial(max(len(incidence[i])-1,0)) for i in (0,2))
    best = None
    histogram = Counter()
    for checked, (first,second) in enumerate(itertools.product(cyclic_orders(incidence[0]),cyclic_orders(incidence[2])),1):
        if budget and checked > budget:
            return {'status':'INCOMPLETE','words':words,'full_order_count':total,
                    'checked':checked-1,'genus_histogram':dict(histogram),'best':best}
        orders = [first, tuple(paired[d] for d in first[::-1]),
                  second, tuple(paired[d] for d in second[::-1])]
        details = analyse_orders(words,orders)
        g = details['total_genus']
        histogram[g] += 1
        if best is None or g < best['total_genus']:
            best = dict(details,orders=orders)
        if g == 0:
            return {'status':'PLANAR_COMPATIBLE','words':words,'full_order_count':total,
                    'checked':checked,'genus_histogram':dict(histogram),'best':best}
    return {'status':'NO_PLANAR_COMPATIBLE','words':words,'full_order_count':total,
            'checked':sum(histogram.values()),'genus_histogram':dict(histogram),'best':best}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('words',nargs='+')
    p.add_argument('--budget',type=int,default=0)
    p.add_argument('--output',required=True)
    args = p.parse_args()
    result = decide(args.words,args.budget)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
