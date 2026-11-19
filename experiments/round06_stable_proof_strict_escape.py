"""Expand the defining exchanges of the cap-23 escape into strict stable moves."""

import argparse
from collections import Counter
from contextlib import nullcontext
from hashlib import sha256
import json
from pathlib import Path

from free_waypoint_search import conj_ops, normalize
from round03_stable_proof_pivot import canonical
from round05_stable_chart_transport import evaluate
from stallings_search import inverse, reduce

ROOT = Path(__file__).resolve().parents[1]


def concatenate(lhs, rhs):
    overlap = 0
    while overlap < len(lhs) and overlap < len(rhs) and lhs[-1 - overlap] == rhs[overlap].swapcase():
        overlap += 1
    return lhs[:len(lhs) - overlap] + rhs[overlap:]


def cyclic_size(word):
    trim = 0
    while 2 * trim + 1 < len(word) and word[trim] == word[-1 - trim].swapcase():
        trim += 1
    return len(word) - 2 * trim


def inverse_factors(factors):
    return [(slot, -sign, word) for slot, sign, word in reversed(factors)]


def letters_as_factors(word, proofs):
    result = []
    for letter in word:
        positive = proofs[letter.lower()]
        result.extend(positive if letter.islower() else inverse_factors(positive))
    return result


def value(factors, rows):
    word = ""
    for i, sign, g in factors:
        piece = rows[i] if sign == 1 else inverse(rows[i])
        word = concatenate(word, concatenate(concatenate(g, piece), inverse(g)))
    return word


def initial_proofs(rows):
    # Let A=x^3, c=xy, P=Ay^-4, B=(cxc^-1)y^-1. Then
    # y=P^-1[c,A]^-1(cAc^-1 y^-3), and x=c^-1 B y c.
    y = [(0, -1, ""), (0, 1, "x"), (0, -1, "xy"),
         (1, 1, ""), (1, 1, "y"), (1, 1, "yy")]
    x = [(1, 1, "YX")] + [(i, sign, reduce("YX" + g)) for i, sign, g in y]
    proofs = {"x": x, "y": y, "z": [(2, 1, "")]}
    assert all(value(factors, rows) == g for g, factors in proofs.items())
    return proofs


def transport(proofs, move):
    changed = move["i"]
    for letter, factors in proofs.items():
        result = []
        for i, sign, g in factors:
            if i != changed:
                result.append((i, sign, g))
            elif move["op"] == "invert":
                result.append((i, -sign, g))
            elif move["op"] == "conjugate":
                result.append((i, sign, concatenate(g, inverse(move["g"]))))
            elif sign == 1:
                result.extend([(i, 1, g), (move["j"], -1, g)])
            else:
                result.extend([(move["j"], 1, g), (i, -1, g)])
        proofs[letter] = result


class StrictPath:
    def __init__(self, start, sink=None):
        self.rows = list(start)
        self.generators = set("xy")
        self.cyclic_lengths = list(map(cyclic_size, start))
        self.total = 0
        self.counts = Counter()
        self.sink = sink
        self.digest = sha256()
        self.record((json.dumps({"start": start}, separators=(",", ":")) + "\n").encode("ascii"))
        self.peak_rank = len(self.generators)
        self.raw_peak = sum(map(len, start))
        self.cyclic_peak = sum(self.cyclic_lengths)

    def record(self, row):
        self.digest.update(row)
        if self.sink is not None:
            self.sink.write(row)

    def add(self, move):
        op = move["op"]
        if op == "stabilize":
            g = move["generator"]
            assert len(g) == 1 and g not in self.generators and g.islower()
            self.generators.add(g)
            self.rows.append(g)
            self.cyclic_lengths.append(1)
        else:
            i = move["i"]
            assert 0 <= i < len(self.rows)
            if op == "destabilize":
                g = move["generator"]
                assert self.rows[i] == g and g in self.generators
                assert all(g not in row.lower() for k, row in enumerate(self.rows) if k != i)
                self.generators.remove(g)
                del self.rows[i]
                del self.cyclic_lengths[i]
            elif op == "invert":
                self.rows[i] = inverse(self.rows[i])
            elif op == "multiply":
                j = move["j"]
                assert j != i and 0 <= j < len(self.rows)
                self.rows[i] = concatenate(self.rows[i], self.rows[j])
                self.cyclic_lengths[i] = cyclic_size(self.rows[i])
            elif op == "conjugate":
                g = move["g"]
                assert len(g) == 1 and g.lower() in self.generators
                self.rows[i] = concatenate(concatenate(g, self.rows[i]), inverse(g))
            else:
                raise ValueError(move)
        assert len(self.generators) == len(self.rows)
        if op == "conjugate":
            line = f'{{"op":"conjugate","i":{i},"g":"{g}"}}\n'
        elif op == "multiply":
            line = f'{{"op":"multiply","i":{i},"j":{j}}}\n'
        elif op == "invert":
            line = f'{{"op":"invert","i":{i}}}\n'
        elif op == "stabilize":
            line = f'{{"op":"stabilize","generator":"{g}"}}\n'
        else:
            line = f'{{"op":"destabilize","generator":"{g}","i":{i}}}\n'
        self.record(line.encode("ascii"))
        self.total += 1
        self.counts[op] += 1
        self.peak_rank = max(self.peak_rank, len(self.rows))
        self.raw_peak = max(self.raw_peak, sum(map(len, self.rows)))
        self.cyclic_peak = max(self.cyclic_peak, sum(self.cyclic_lengths))

    def extend(self, moves):
        for move in moves:
            self.add(move)

    def factor(self, i, donor, sign, conjugator):
        if sign < 0:
            self.add({"op": "invert", "i": donor})
        self.extend(conj_ops(donor, conjugator))
        self.add({"op": "multiply", "i": i, "j": donor})
        self.extend(conj_ops(donor, inverse(conjugator)))
        if sign < 0:
            self.add({"op": "invert", "i": donor})

    def append_normal_product(self, recipient, word, proof):
        assert value(proof, self.rows) == word
        based = {}
        for donor, sign, g in proof:
            assert recipient != donor
            old_sign, old_g = based.get(donor, (1, ""))
            if sign != old_sign:
                self.add({"op": "invert", "i": donor})
            self.extend(conj_ops(donor, concatenate(g, inverse(old_g))))
            self.add({"op": "multiply", "i": recipient, "j": donor})
            based[donor] = sign, g
        for donor, (sign, g) in sorted(based.items()):
            self.extend(conj_ops(donor, inverse(g)))
            if sign < 0:
                self.add({"op": "invert", "i": donor})

    def change_occurrences(self, recipient, marked, replacement, donor):
        original_donor = self.rows[donor]
        while marked in self.rows[recipient].lower():
            row = self.rows[recipient]
            position = row.lower().index(marked)
            letter = row[position]
            image = replacement if letter == marked else inverse(replacement)
            correction = inverse(letter) + image
            _, to_correction = normalize(tuple(self.rows), donor, correction)
            suffix = row[position + 1:]
            self.extend(to_correction)
            self.factor(recipient, donor, 1, inverse(suffix))
            _, to_original = normalize(tuple(self.rows), donor, original_donor)
            self.extend(to_original)
            assert self.rows[recipient] == reduce(row[:position] + image + suffix)


def exchange(path, proofs, labels, letter, multiplier, left):
    g = labels[letter]
    a = labels[multiplier.lower()]
    if multiplier.isupper():
        a = a.upper()
    t = next(candidate for candidate in "abcdefghijklmnopqrstuvw" if candidate not in path.generators)
    definition = inverse(a) + g if left else g + inverse(a)
    replacement = a + t if left else t + a
    projected = {key: [(i, sign, evaluate(word, g, replacement)) for i, sign, word in factors]
                 for key, factors in proofs.items()}
    old_rows = tuple(path.rows)
    path.add({"op": "stabilize", "generator": t})
    donor = len(path.rows) - 1
    path.append_normal_product(donor, inverse(definition), letters_as_factors(inverse(definition), proofs))
    assert path.rows[donor] == t + inverse(definition)
    for recipient in range(donor):
        path.change_occurrences(recipient, g, replacement, donor)
    assert path.rows[:donor] == [evaluate(word, g, replacement) for word in old_rows]
    _, moves = normalize(tuple(path.rows), donor, g + inverse(replacement))
    path.extend(moves)
    path.append_normal_product(donor, replacement, projected[g])
    path.add({"op": "destabilize", "generator": g, "i": donor})

    # A projected proof for the old expression defining t gives a proof
    # for its new single marked letter.
    proofs[t] = [(i, sign, evaluate(word, g, replacement))
                 for i, sign, word in letters_as_factors(definition, proofs)]
    for key, factors in projected.items():
        if key == g:
            del proofs[g]
        else:
            proofs[key] = factors
    labels[letter] = t
    assert all(value(factors, path.rows) == key for key, factors in proofs.items())


def translation(source, target):
    return str.maketrans(source + source.upper(), target + target.upper())


def compile_escape(prefix, receipt, sink=None):
    path = StrictPath(prefix["start"][:2], sink)
    path.add({"op": "stabilize", "generator": "z"})
    proofs = initial_proofs(path.rows)
    for move in prefix["moves"]:
        path.add(move)
        transport(proofs, move)
    assert path.rows == prefix["target"]
    assert all(value(factors, path.rows) == g for g, factors in proofs.items())
    labels = dict(zip("xyz", "xyz"))
    stages = []
    for stage in receipt["whitehead_stages"]:
        multiplier, cut = (stage["descent"][key] for key in ("multiplier", "cut"))
        for letter in "xyz":
            if letter == multiplier.lower():
                continue
            if letter in cut:
                exchange(path, proofs, labels, letter, multiplier, left=True)
            if letter.upper() in cut:
                exchange(path, proofs, labels, letter, inverse(multiplier), left=False)
        physical = "".join(labels.values())
        mark = translation("xyz", physical)
        for i, target in enumerate(stage["rows"]):
            _, moves = normalize(tuple(path.rows), i, target.translate(mark))
            for move in moves:
                path.add(move)
                transport(proofs, move)
        assert [row.translate(translation(physical, "xyz")) for row in path.rows] == stage["rows"]
        stages.append(path.total)

    deleted = labels["z"]
    donor = path.rows.index(deleted.upper())
    for i in range(len(path.rows)):
        if i != donor:
            path.change_occurrences(i, deleted, "", donor)
    path.add({"op": "invert", "i": donor})
    path.add({"op": "destabilize", "generator": deleted, "i": donor})
    named = [row.translate(translation(labels["x"] + labels["y"], "xy")) for row in path.rows]
    assert sorted(map(canonical, named)) == receipt["rank_two_projection"]
    path.record((json.dumps({"target": path.rows}, separators=(",", ":")) + "\n").encode("ascii"))
    return path, stages, labels


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-ledger", type=Path)
    args = parser.parse_args()
    prefix = json.loads((ROOT / "certificates/round06_stable_proof_cap23_escape.json").read_text())
    receipt = json.loads((ROOT / "results/round06_stable_proof_cap23_escape.json").read_text())
    with args.write_ledger.open("wb") if args.write_ledger else nullcontext() as sink:
        path, stages, labels = compile_escape(prefix, receipt, sink)
    print(json.dumps({"moves": path.total, "move_counts": dict(path.counts),
                      "rank_peak": path.peak_rank, "raw_peak": path.raw_peak, "cyclic_peak": path.cyclic_peak,
                      "whitehead_stage_boundaries": stages, "final_marking": {g: labels[g] for g in "xy"},
                      "final_words": path.rows, "strict_ledger_sha256": path.digest.hexdigest()}, indent=2))
