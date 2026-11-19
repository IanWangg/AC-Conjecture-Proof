"""Replay the Lisitsa–Vernitski ordinary AC ledgers and look for exact joins."""

import argparse
import ast
from collections import Counter
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
import re
from zipfile import ZipFile

from elementary_verify import inverse, reduce, replay
from stallings_search import apply, nielsen_move

AK3 = ("xxxYYYY", "xyxYXY")
BASIS = ("x", "y")
LETTERS = "xXyY"
FORWARD_ARCHIVE = "ak3_certificates.zip"
REVERSE_ARCHIVE = "640_simplification_paths.zip"
FILE_PATTERNS = (r"(n[0-9]+row[0-9]+)_toAK3_moves.txt",
                 r"(n[0-9]+row[0-9]+)_pureAC_moves.txt")
PRINTED_STEP = re.compile(
    r"^ *(start|[0-9]+(?= +(?:r[12]|swap))) +.*?<([xXyY]+), *([xXyY]+)>[ \r]*$", re.M
)


def decode(values):
    if type(values) is not list or any(type(value) is not int or value not in range(4)
                                       for value in values):
        raise ValueError("invalid integer word")
    return "".join(LETTERS[value] for value in values)


def entries(folder, archive, pattern):
    with ZipFile(folder / archive) as source:
        names = sorted(name for name in source.namelist()
                       if re.fullmatch(pattern, Path(name).name))
        for name in names:
            lines = source.read(name).decode("ascii").splitlines()
            words = ast.literal_eval(lines[0])
            if type(words) is not list or len(words) != 2:
                raise ValueError(f"invalid starting pair in {name}")
            start = tuple(decode(word) for word in words)
            moves = [parse_move(line) for line in lines[1:] if line.strip()]
            printed_name = name.replace("_moves.txt", ".txt")
            printed = PRINTED_STEP.findall(source.read(printed_name).decode("utf-8"))
            if len(printed) != len(moves) + 1 or printed[0][0] != "start":
                raise ValueError(f"printed ledger length mismatch in {printed_name}")
            for step, row in enumerate(printed[1:], 1):
                if int(row[0]) != step:
                    raise ValueError(f"nonconsecutive printed steps in {printed_name}")
            yield name, start, moves, [(a, b) for _, a, b in printed]


def parse_move(line):
    move = ast.literal_eval(line)
    if move == ("swap",):
        return move
    if type(move) is not tuple or len(move) < 2 or type(move[1]) is not int or move[1] not in (0, 1):
        raise ValueError(f"invalid move {move!r}")
    if len(move) == 2 and move[0] == "invert":
        return move
    if len(move) == 3 and move[0] == "conjugate":
        return move[:2] + (decode(move[2]),)
    if (len(move) == 4 and move[0] == "multiply" and type(move[2]) is int
            and move[2] == 1 - move[1] and move[3] in ("left", "right")):
        return move
    raise ValueError(f"invalid ordinary move {move!r}")


def perform(state, move, undo=False):
    if move[0] == "swap":
        return state[::-1]
    kind, index, *args = move
    words = list(state)
    word = words[index]
    if kind == "invert":
        words[index] = inverse(word)
    elif kind == "conjugate":
        conjugator = args[0] if undo else inverse(args[0])
        words[index] = reduce(conjugator + word + inverse(conjugator))
    else:
        donor, side = args
        factor = inverse(words[donor]) if undo else words[donor]
        words[index] = reduce(factor + word if side == "left" else word + factor)
    return tuple(words)


def expand(state, move, undo=False):
    if move[0] == "swap":
        initial = state
        ledger = []
        for index, left, negative in ((0, False, False), (1, False, True),
                                      (0, True, False)):
            state, part = nielsen_move(state, index, left, negative)
            ledger.extend(part)
        ledger.append({"op": "invert", "i": 1})
        if apply(state, ledger[-1]) != initial[::-1]:
            raise ValueError("swap expansion failed")
        return ledger
    kind, index, *args = move
    if kind == "invert":
        return [{"op": "invert", "i": index}]
    if kind == "multiply":
        return nielsen_move(state, index, args[1] == "left", undo)[1]
    conjugator = args[0][::-1] if undo else inverse(args[0])[::-1]
    return [{"op": "conjugate", "i": index, "g": g} for g in conjugator]


def min_rotation(word):
    """Find the lexicographically least rotation in linear time."""
    size = len(word)
    doubled = word * 2
    first, second, offset = 0, 1, 0
    while first < size and second < size and offset < size:
        a, b = doubled[first + offset], doubled[second + offset]
        if a == b:
            offset += 1
            continue
        if a > b:
            first += offset + 1
            if first == second:
                first += 1
        else:
            second += offset + 1
            if first == second:
                second += 1
        offset = 0
    start = min(first, second)
    return doubled[start:start + size]


@lru_cache(maxsize=32768)
def cyclic_word(word):
    low, high = 0, len(word)
    while high - low > 1 and word[low] == word[high - 1].swapcase():
        low += 1
        high -= 1
    return word[low:high]


@lru_cache(maxsize=32768)
def cyclic_key(word):
    word = cyclic_word(word)
    return min(min_rotation(word), min_rotation(inverse(word)))


def pair_key(state):
    return tuple(sorted(map(cyclic_key, state)))


def trace(start, moves, printed, name):
    if any(reduce(word) != word for word in start):
        raise ValueError(f"unreduced start {start!r}")
    state = start
    if state != printed[0]:
        raise ValueError(f"{name} printed start differs")
    yield state
    for step, move in enumerate(moves, 1):
        state = perform(state, move)
        if state != printed[step]:
            raise ValueError(f"{name} printed step {step} differs: {state}")
        yield state


def certificate(start, moves, undo=False):
    state = start
    strict = []
    for move in reversed(moves) if undo else moves:
        ledger = expand(state, move, undo=undo)
        next_state = perform(state, move, undo=undo)
        for operation in ledger:
            state = apply(state, operation)
        if state != next_state:
            raise ValueError(f"wrong strict expansion for {move!r}")
        strict.extend(ledger)
    cert = {"format": "ordinary-ac-elementary-v1", "start": list(start),
            "target": list(state), "moves": strict}
    replay(cert)
    return cert


def selfcheck():
    sample = ("xYx", "yXYY")
    for move in [("invert", 0), ("swap",), ("conjugate", 0, "Yx"),
                 ("multiply", 0, 1, "right"), ("multiply", 1, 0, "left")]:
        forward = certificate(sample, [move])
        target = tuple(forward["target"])
        if tuple(certificate(target, [move], undo=True)["target"]) != sample:
            raise ValueError("move inversion control failed")
    from itertools import product
    for size in range(1, 7):
        for letters in product(LETTERS, repeat=size):
            word = "".join(letters)
            if min_rotation(word) != min(word[k:] + word[:k] for k in range(len(word))):
                raise ValueError("rotation control failed")


def trim_catalogue(catalogue, cap):
    rows = sorted(catalogue, key=lambda pair: (sum(map(len, pair)), pair))
    return [row for row in rows if sum(map(len, row)) <= cap]


def write_catalogue(path, rows, locations):
    path.write_text("".join("\t".join(row) + "\n" for row in rows))
    path.with_suffix(".sources.json").write_text(
        json.dumps([locations[row] for row in rows], separators=(",", ":")) + "\n"
    )
    return sha256(path.read_bytes()).hexdigest()


def run(folder, output, cap, ledger, control):
    selfcheck()
    forward_keys, reverse_keys = {}, {}
    forward_starts, reverse_starts = set(), set()
    forward_by_name, reverse_by_name = set(), set()
    raw_forward = {}
    forward_word_peaks = []
    forward_cyclic_peaks = []
    exact_hits, cyclic_hits = {}, {}
    published_counts, move_counts = [], []
    selected = None
    selected_trivial = None
    for side, archive in enumerate((FORWARD_ARCHIVE, REVERSE_ARCHIVE)):
        paths = total_moves = 0
        names = forward_by_name if side == 0 else reverse_by_name
        starts = forward_starts if side == 0 else reverse_starts
        for name, start, moves, printed in entries(folder, archive, FILE_PATTERNS[side]):
            paths += 1
            total_moves += len(moves)
            names.add(re.fullmatch(FILE_PATTERNS[side], Path(name).name).group(1))
            starts.add(start)
            word_peak = cyclic_peak = 0
            if side == 0:
                states = list(trace(start, moves, printed, name))
                for step in range(len(states) - 1, -1, -1):
                    state = states[step]
                    key = pair_key(state)
                    energy = sum(map(len, key))
                    word_peak = max(word_peak, sum(map(len, state)))
                    cyclic_peak = max(cyclic_peak, energy)
                    raw_forward.setdefault(state, (name, step))
                    forward_keys.setdefault(key, (name, step))
                    if energy >= 29 and selected is None:
                        selected = (name, step, certificate(AK3, moves[step:], undo=True))
                if states[-1] != AK3:
                    raise ValueError(f"{name} has unexpected endpoint {states[-1]}")
                forward_word_peaks.append(word_peak)
                forward_cyclic_peaks.append(cyclic_peak)
            else:
                for step, state in enumerate(trace(start, moves, printed, name)):
                    if state in raw_forward:
                        exact_hits.setdefault(state, (raw_forward[state], (name, step)))
                    key = pair_key(state)
                    energy = sum(map(len, key))
                    if energy <= cap:
                        reverse_keys.setdefault(key, (name, step))
                    if key in forward_keys:
                        cyclic_hits.setdefault(key, (forward_keys[key], (name, step)))
                if pair_key(state) != pair_key(BASIS):
                    raise ValueError(f"{name} has nonstandard endpoint {state}")
                if selected_trivial is None or len(moves) < selected_trivial[0]:
                    selected_trivial = len(moves), name, start, moves
        published_counts.append(paths)
        move_counts.append(total_moves)
    if published_counts != [34, 640] or selected is None or selected_trivial is None:
        raise ValueError(f"unexpected input counts {published_counts}")
    name, step, strict = selected
    strict["source"] = {"archive": FORWARD_ARCHIVE, "member": name, "forward_waypoint_step": step}
    ledger.write_text(json.dumps(strict, indent=2) + "\n")

    forward_rows = trim_catalogue(forward_keys, cap)
    reverse_rows = trim_catalogue(reverse_keys, cap)
    forward_hash = write_catalogue(output / "forward.tsv", forward_rows, forward_keys)
    reverse_hash = write_catalogue(output / "reverse.tsv", reverse_rows, reverse_keys)
    reverse_control = certificate(selected_trivial[2], selected_trivial[3])
    reverse_control["source"] = {"archive": REVERSE_ARCHIVE, "member": selected_trivial[1]}
    control.write_text(json.dumps(reverse_control, indent=2) + "\n")
    result = {
        "published_paths": dict(zip((FORWARD_ARCHIVE, REVERSE_ARCHIVE), published_counts)),
        "archive_sha256": {name: sha256((folder / name).read_bytes()).hexdigest()
                           for name in (FORWARD_ARCHIVE, REVERSE_ARCHIVE)},
        "moves_replayed": dict(zip((FORWARD_ARCHIVE, REVERSE_ARCHIVE), move_counts)),
        "all_states_equal_to_printed_ledgers": True,
        "benchmark_id_overlap": sorted(forward_by_name & reverse_by_name),
        "literal_start_overlap": sorted(forward_starts & reverse_starts),
        "distinct_forward_raw": len(raw_forward),
        "distinct_forward_signed_cyclic": len(forward_keys),
        "forward_path_literal_raw_peak_range": [min(forward_word_peaks), max(forward_word_peaks)],
        "forward_path_literal_cyclic_peak_range": [min(forward_cyclic_peaks), max(forward_cyclic_peaks)],
        "cross_corpus_exact_state_hits": [{"pair": row, "locations": loc}
                                         for row, loc in exact_hits.items()],
        "cross_corpus_cyclic_key_hits": [{"pair": row, "locations": loc}
                                        for row, loc in cyclic_hits.items()],
        "catalogue_cyclic_cap": cap,
        "forward_cyclic_catalogue": {
            "rows": len(forward_rows), "sha256": forward_hash,
            "energies": dict(sorted(Counter(sum(map(len, row)) for row in forward_rows).items())),
        },
        "reverse_cyclic_catalogue": {"rows": len(reverse_rows), "sha256": reverse_hash},
        "selected_forward_strict_waypoint": {
            **replay(strict), "source": strict["source"],
            "endpoint_cyclic_energy": sum(len(cyclic_word(word)) for word in strict["target"]),
        },
        "shortest_published_reverse_control": {
            **replay(reverse_control), "archive_moves": selected_trivial[0],
            "source": selected_trivial[1], "start": selected_trivial[2],
        },
    }
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("archive_folder", type=Path)
    parser.add_argument("output_folder", type=Path)
    parser.add_argument("--cap", type=int, default=32)
    parser.add_argument("--certificate", required=True, type=Path)
    parser.add_argument("--control-certificate", required=True, type=Path)
    args = parser.parse_args()
    args.output_folder.mkdir(parents=True, exist_ok=True)
    result = run(args.archive_folder, args.output_folder, args.cap, args.certificate,
                 args.control_certificate)
    (args.output_folder / "archive.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
