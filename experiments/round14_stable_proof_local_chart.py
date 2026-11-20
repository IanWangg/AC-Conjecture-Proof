"""Replay the alternate literal frame and clear its remaining tail locally."""

import argparse
import json
import subprocess
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory

from free_waypoint_search import normalize
from round03_stable_proof_pivot import canonical
from round04_stable_proof_paths import replay
from round06_stable_proof_strict_escape import StrictPath, value
from round09_stable_proof_rank_three_chart import (
    IDENTITY,
    START,
    apply_marking,
    basic_ledger,
    compose,
    transport,
    whitehead_factors,
)
from round11_stable_proof_reverse import certificate
from stallings_search import inverse, reduce

CHANGES = (
    {"multiplier": "y", "cut": "yzZ"},
    {"multiplier": "z", "cut": "zx"},
    {"multiplier": "x", "cut": "xZ"},
)
MARK = ("z", "y", "yzXY")
LITERAL = ("XXYxZYY", "XYXYxZYYZyzyz", "XYxZYZyzyyz")
TARGET = ("XXYxYXXYxxy", "XXYXYxxyXyxxy")


def remark(source):
    assert tuple(source["start"]) == START
    replay(source)
    with BytesIO() as sink:
        path = StrictPath(START[:2], sink)
        path.add({"op": "stabilize", "generator": "z"})
        mark = IDENTITY
        for change in reversed(CHANGES):
            for basic in whitehead_factors(change, True):
                transport(path, basic_ledger(basic), mark)
                mark = compose(mark, basic)
        assert mark == MARK
        assert tuple(path.rows) == tuple(apply_marking(w, mark) for w in START)
        initial = dict(moves=path.total, raw_peak=path.raw_peak, cyclic_peak=path.cyclic_peak)
        transport(path, source["moves"], mark)
        assert tuple(path.rows) == tuple(apply_marking(w, mark) for w in source["target"])
        assert tuple(map(canonical, path.rows)) == LITERAL
        for slot, target in enumerate(LITERAL):
            _, moves = normalize(tuple(path.rows), slot, target)
            path.extend(moves)
        moves = [json.loads(row) for row in sink.getvalue().splitlines()[2:]]
    proof = certificate(START, moves, LITERAL)
    return proof, initial


def clear(prefix, binary, output):
    with output.open("wb") as sink, TemporaryDirectory() as scratch:
        path = StrictPath(START[:2], sink)
        path.add({"op": "stabilize", "generator": "z"})
        path.extend(prefix["moves"])
        assert tuple(path.rows) == LITERAL

        pivot = inverse(path.rows[0])
        position = pivot.index("z")
        word = pivot[position + 1 :] + pivot[:position]
        _, moves = normalize(tuple(path.rows), 0, "z" + word)
        path.extend(moves)
        for slot in (1, 2):
            path.change_occurrences(slot, "z", inverse(word), 0)
            _, moves = normalize(tuple(path.rows), slot)
            path.extend(moves)
        cleared = dict(rows=path.rows[:], moves=path.total, cyclic_peak=path.cyclic_peak)
        assert tuple(path.rows[1:]) == TARGET

        factor_file = Path(scratch) / "factors.tsv"
        searches = []
        for cap in (12, 13):
            process = subprocess.run(
                [str(binary.resolve()), *TARGET, word, str(cap), "400000", str(factor_file)],
                text=True,
                capture_output=True,
                check=True,
            )
            searches.append(json.loads(process.stdout))
        assert not searches[0]["hit"] and searches[1]["hit"]
        factors = []
        for row in factor_file.read_text().splitlines():
            slot, sign, tail = row.split("\t")
            factors.append((int(slot) + 1, int(sign), tail))
        assert value(factors, path.rows) == inverse(word)
        lengths = [len(word)]
        for slot, sign, tail in factors:
            row = path.rows[slot] if sign == 1 else inverse(path.rows[slot])
            word = reduce(word + tail + row + inverse(tail))
            lengths.append(len(word))
        assert word == "" and max(lengths) == 13
        path.append_normal_product(0, inverse(cleared["rows"][0][1:]), factors)
        path.add({"op": "destabilize", "generator": "z", "i": 0})
        assert tuple(path.rows) == TARGET
        path.record((json.dumps({"target": path.rows}, separators=(",", ":")) + "\n").encode())
        result = dict(moves=path.total, cyclic_peak=path.cyclic_peak, raw_peak=path.raw_peak,
                      rank_peak=path.peak_rank, final_words=path.rows, sha256=path.digest.hexdigest())
    return dict(cleared=cleared, tail_searches=searches, tail_factors=factors,
                intermediate_tail_lengths=lengths, complete=result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("source", "binary", "prefix", "output"):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    source = args.source.read_bytes()
    prefix, initial = remark(json.loads(source))
    args.prefix.write_text(json.dumps(prefix, separators=(",", ":")) + "\n")
    result = dict(source_sha256=sha256(source).hexdigest(), marking=dict(zip("xyz", MARK)),
                  whitehead_moves=CHANGES, initial_realization=initial,
                  prefix=replay(prefix), literal_clearing=clear(prefix, args.binary, args.output))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
