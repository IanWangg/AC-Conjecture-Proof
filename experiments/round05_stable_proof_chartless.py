"""Build the cap-22 loss-of-all-charts witness and audit rank-three tuples."""

import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from euclidean_primitive_audit import primitive_cyclic_word
from round03_stable_proof_pivot import canonical, det, rotations
from round04_chart_screen import chart_projections
from round04_stable_proof_blocks import cyclic_cover_obstruction
from round04_stable_proof_paths import edge, replay
from round04_stable_proof_seeds import orbit
from stallings_search import apply

ROOT = Path(__file__).resolve().parents[1]
PRIOR = ROOT / "certificates/round04_stable_proof_pivotless22.json"
TARGET = ("XXYYZZY", "XYZZZYYxy", "XYxYXy")
LETTERS = "xXyYzZ"


def chart_count(rows):
    return sum(w.lower().count(g) == 1 for w in rows for g in "xyz")


def whitehead_image(rows, multiplier, side):
    opposite = multiplier.swapcase()
    substitution = {
        a: a if a in (multiplier, opposite) else
        (multiplier if a in side else "") + a + (opposite if a.swapcase() in side else "")
        for a in LETTERS
    }
    return tuple(canonical("".join(substitution[a] for a in row)) for row in rows)


def minima(words):
    """Whitehead-minimize a cyclic tuple, then return its cut table."""
    rows = tuple(map(canonical, words))
    moves = []
    while True:
        edges = Counter(
            tuple(sorted((a.swapcase(), b)))
            for row in rows for a, b in zip(row, row[1:] + row[:1])
        )
        degrees = {}
        cuts = {}
        choices = []
        for letter in LETTERS:
            opposite = letter.swapcase()
            degrees[letter] = sum(n for e, n in edges.items() if letter in e)
            others = [a for a in LETTERS if a not in (letter, opposite)]
            cuts[letter], side = min(
                (
                    sum(n for (a, b), n in edges.items() if (a in side) != (b in side)),
                    "".join(sorted(side)),
                )
                for k in range(len(others) + 1)
                for part in combinations(others, k)
                for side in [frozenset((letter, *part))]
            )
            if cuts[letter] < degrees[letter]:
                choices.append((cuts[letter] - degrees[letter], letter, side))
        if not choices:
            return rows, moves, edges, degrees, cuts
        delta, letter, side = min(choices)
        changed = whitehead_image(rows, letter, side)
        assert sum(map(len, changed)) - sum(map(len, rows)) == delta
        moves.append(dict(multiplier=letter, cut=side, result=changed))
        rows = changed


@lru_cache(maxsize=None)
def primitive(word):
    return len(minima((word,))[0][0]) == 1


def build(path):
    certificate = json.loads(PRIOR.read_text())
    final, moves = edge(certificate["target"], TARGET,
                        certificate["maximum_cyclic_length"], LETTERS)
    certificate["target"] = final
    certificate["moves"].extend(moves)
    certificate["macro_boundaries"].append(len(certificate["moves"]))
    path.write_text(json.dumps(certificate, indent=2) + "\n")


def verify(path):
    certificate = json.loads(path.read_text())
    proof = replay(certificate)
    assert tuple(sorted(map(canonical, proof["target"]))) == TARGET
    state = tuple(certificate["start"])
    seen = {}
    for step, move in enumerate([None, *certificate["moves"]]):
        if move:
            state = apply(state, move)
        cyclic_state = tuple(sorted(map(canonical, state)))
        seen.setdefault(cyclic_state, step)
    first_literal = min(step for rows, step in seen.items() if chart_count(rows) == 0)
    intrinsic = [step for rows, step in seen.items() if all(not primitive(w) for w in rows)]
    result = dict(proof, distinct_cyclic_states=len(seen), first_all_chartless_step=first_literal,
                  first_all_nonprimitive_step=min(intrinsic, default=None))
    result["final_rows"] = {
        w: dict(occurrence_counts=[w.lower().count(g) for g in "xyz"],
                whitehead_minimum=minima((w,))[0][0], is_primitive=primitive(w))
        for w in TARGET
    }
    result["final_two_row_blocks"] = [
        dict(rows=pair, fox_obstruction=obstruction, weights=weights, omitted_column=column,
             minor=minor)
        for pair in combinations(TARGET, 2)
        for obstruction, weights, column, minor in [cyclic_cover_obstruction(pair)]
    ]
    joint, descent, edges, degrees, cuts = minima(TARGET)
    result["joint_whitehead_minimum"] = dict(
        rows=joint, moves=descent, edges={"".join(edge): n for edge, n in sorted(edges.items())},
        degrees=degrees, cut_minima=cuts,
    )
    return result


def scan(path):
    triples = []
    count = 0
    digest = sha256()
    with path.open("rb") as stream:
        for raw in stream:
            digest.update(raw)
            count += 1
            rows = tuple(raw.decode("ascii").split())
            if chart_count(rows) == 0:
                assert abs(det(rows)) == 1
                triples.append(rows)
    words = {w for rows in triples for w in rows}
    primitive_words = sorted(w for w in words if primitive(w))
    essential = [rows for rows in triples if not any(primitive(w) for w in rows)]
    blocks = {pair for rows in essential for pair in combinations(rows, 2)}
    surviving = sorted(pair for pair in blocks if not cyclic_cover_obstruction(pair)[0])
    return dict(
        scan_sha256=digest.hexdigest(), inspected_orbits=count, chartless_orbits=len(triples),
        chartless_states=sum(len(orbit(rows)) for rows in triples),
        distinct_chartless_words=len(words), primitive_words=primitive_words,
        nonprimitive_row_orbits=len(essential),
        nonprimitive_row_states=sum(len(orbit(rows)) for rows in essential),
        nonprimitive_row_energy_histogram=dict(sorted(Counter(sum(map(len, s)) for s in essential).items())),
        unordered_two_row_blocks=len(blocks),
        excluded_by_cyclic_cover=len(blocks) - len(surviving),
        fox_survivor_reductions=[reduce_block(pair) for pair in surviving],
    )


def reduce_block(pair):
    """Expose a primitive relation by one bounded-form multiplication."""
    for r, s in (pair, pair[::-1]):
        for a, b in product(rotations(r), rotations(s)):
            changed = canonical(a + b)
            for eliminated, pivot, (quotient,) in chart_projections((changed, s)):
                if pivot != changed:
                    continue
                assert not primitive_cyclic_word(quotient)
                return dict(pair=pair, recipient_rotation=a, donor_rotation=b,
                            new_pivot=pivot, eliminated=eliminated, quotient_row=quotient,
                            quotient_row_is_primitive=False)
    raise ValueError(f"No block reduction for {pair}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("build", "verify", "scan"))
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    if args.mode == "build":
        build(args.path)
    output = scan(args.path) if args.mode == "scan" else verify(args.path)
    print(json.dumps(output, indent=2))
