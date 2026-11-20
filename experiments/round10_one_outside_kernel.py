"""Certify all finite vertex-identification cases for one outside conjugator."""

import argparse
import hashlib
from itertools import combinations
import json
from pathlib import Path

from primitive_map_pairs import decide, fold, inverse, reduce
from round09_rank_two_overgroups import AK3, ENERGY17
from v_vertex_identification import cross, dot, fold_identification, spanning
from v_voltage_cycle_review import review
from verify_vertex_voltage import verify

ROOT = Path(__file__).resolve().parents[1]


def build(rows):
    original = fold(rows)
    paths, *_ = spanning(original)
    identifications, potentials = [], []
    for first, second in combinations(range(len(paths)), 2):
        graph, projection = fold_identification(original, first, second)
        _, chords, arcs, coordinates = spanning(graph)
        assert len(chords) == 3
        representative = reduce(paths[first] + inverse(paths[second]))
        character = cross(*map(coordinates, rows))
        determinant = dot(character, coordinates(representative))
        assert abs(determinant) == 1
        weights = [0] * len(graph)
        for (source, label, _), (chord, orientation) in arcs.items():
            weights[4 * source + label] = orientation * character[chord] // determinant
        vertex_pair = [first, second]
        result = review(graph, weights)
        assert result["status"] == "PASS"
        identifications.append({"identified_vertices": vertex_pair, "graph": graph, "rank": len(chords),
                                "vertex_projection": projection, "extra_generator": representative,
                                "edge_voltages": weights})
        potentials.append({"identified_vertices": vertex_pair, **result})
    return {"identifications": {"original_pair": list(rows), "original_graph": original,
                                "records": identifications}, "potentials": {"results": potentials}}


def read_old(name):
    return json.loads((ROOT / "certificates" / name).read_text())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    new = build(ENERGY17)
    text = json.dumps(new, separators=(",", ":")) + "\n"
    args.certificate.write_text(text)
    audit_new = verify(new["identifications"], new["potentials"])
    audit_old = verify(read_old("v_vertex_identification_results.json"), read_old("v_voltage_cycle_results.json"))
    assert audit_new["rank_three_cases"] == 91 and audit_old["rank_three_cases"] == 45
    checks = {}
    for name, rows in (("ak3", AK3), ("energy17", ENERGY17)):
        record = decide(fold(rows))
        assert record["status"] == "ABSENT"
        checks[name] = sum(item["pair_states_processed"] for item in record["alphabets"])
    print(json.dumps({"old_ak3_certificate": audit_old, "energy17_certificate": audit_new,
                      "base_core_primitive_map_states": checks,
                      "energy17_certificate_sha256": hashlib.sha256(text.encode()).hexdigest()}, indent=2))


if __name__ == "__main__":
    main()
