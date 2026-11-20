"""Audit fixed-donor primitive slopes at all nine new energy-17 waypoints."""

import argparse
import json
from math import lcm
from pathlib import Path

from round10_ac_proof_blocks import vectors
from round15_ak3_torus_atlas import apply
from round17_ak3_minima_slopes import scan
from round19_ak3_minimum_class_two import MARKINGS, indexed_word, inverse
from round19_ak3_minimum_magnus import audit

DEGREES = (3, 3, 4, 4, 3, 3, 5, 3, 3)


def power(word, k, opposite):
    return (word if k >= 0 else opposite) * abs(k)


def reverse_mark(donor):
    x, y = vectors(donor)
    if x + y == 1:
        tail = power("y", 1-x, "Y")
        chart = "x"+tail, "Yx"+tail
        back = "x"+power("xY", x-1, "yX"), "xY"
    else:
        assert x + y == -1
        tail = power("y", x, "Y")
        chart = "yX"+tail, "X"+tail
        back = power("xY",x,"yX")+"Y", "xY"
    assert tuple(apply(w, chart) for w in back) == ("x","y")
    assert tuple(apply(w, back) for w in chart) == ("x","y")
    return chart, back


def indexed_pair(donor, receiver, chart):
    relation, h0 = indexed_word(apply(donor,chart))
    row, h1 = indexed_word(apply(receiver,chart))
    assert h0 == 0 and abs(h1) == 1
    if h1 < 0:
        row = tuple((i-h1,sign) for i,sign in inverse(row))
    return relation, row


def check(catalogue, executable):
    pairs = [tuple(line.split()) for line in catalogue.read_text().splitlines()
             if sum(map(len,line.split())) == 17]
    assert len(pairs) == len(DEGREES) and all(donor == "xxyXYY" for donor,_ in pairs)
    results = []
    for (donor, receiver), degree in zip(pairs, DEGREES):
        first = audit(*indexed_pair(donor,receiver,MARKINGS[0]),6)
        assert not first["surviving_residues"]
        chart, back = reverse_mark(receiver)
        relator, word = indexed_pair(receiver,donor,chart)
        second = audit(relator,word,degree)
        permutation = scan(executable,receiver,donor,9)
        assert tuple(map(vectors,permutation["basis"])) == tuple(map(vectors,back[::-1]))
        period = lcm(second["slope_period"],permutation["combined_period"])
        allowed = [k for k in range(period)
                   if k%second["slope_period"] in second["surviving_residues"]
                   and k%permutation["combined_period"] in permutation["survivors"]]
        results.append({"source":[donor,receiver],"first_fixed_direction":first,
                        "second_fixed_direction":{
                            "marking":chart,"inverse_marking":back,
                            "indexed_donor":relator,"indexed_receiver":word,
                            "magnus":second,"permutation":permutation,
                            "common_period":period,"surviving_residues":allowed}})
    return {"minima":len(results),
            "excluded_directions":sum(1+(not row["second_fixed_direction"]["surviving_residues"])
                                      for row in results),
            "cases":results}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalogue",type=Path)
    parser.add_argument("periodic_slope",type=Path)
    arguments = parser.parse_args()
    print(json.dumps(check(arguments.catalogue,arguments.periodic_slope),indent=2))
