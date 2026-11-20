"""Clear a literal stable pivot using a bounded two-donor word proof."""

import json
import sys
from collections import deque
from io import BytesIO
from pathlib import Path

from free_waypoint_search import normalize
from round06_stable_proof_strict_escape import StrictPath, value
from round08_ak3_acm_replay import donor_rotations
from stallings_search import inverse, reduce


def rewrites(rows, indices):
    rules = {}
    for i in indices:
        for relation, (g, sign) in donor_rotations(rows[i]).items():
            for n in range(len(relation) + 1):
                piece, right = relation[:n], inverse(relation[n:])
                rules.setdefault(piece, set()).add((right, i, -sign, g))
    return {lhs: sorted(forms) for lhs, forms in rules.items()}


def prove(rows, indices, word, cap, limit):
    if not word:
        return []
    rules = rewrites(rows, indices)
    predecessors = {word: None}
    queue = deque([word])
    iterations = 0
    while queue and iterations < limit and "" not in predecessors:
        current = queue.popleft()
        fresh = []
        iterations += 1
        for i in range(len(current) + 1):
            before = current[:i]
            for j in range(i, len(current) + 1):
                sub, suffix = current[i:j], current[j:]
                for right, slot, sign, g in rules.get(sub, ()):
                    proposed = reduce(before + right + suffix)
                    if len(proposed) > cap or proposed in predecessors:
                        continue
                    predecessors[proposed] = (
                        current,
                        (slot, sign, reduce(inverse(suffix) + g)),
                    )
                    fresh.append(proposed)
        queue.extend(sorted(fresh, key=lambda w: (len(w), w)))
    if "" not in predecessors:
        return None
    factors = []
    at = ""
    while predecessors[at] is not None:
        at, factor = predecessors[at]
        factors.append(factor)
    proof = factors[::-1]
    assert value(proof, rows) == inverse(word)
    return proof


def compile_chart(prefix, slot, generator, work):
    with BytesIO() as buffer:
        path = StrictPath(prefix["start"][:2], buffer)
        path.add({"op": "stabilize", "generator": "z"})
        path.extend(prefix["moves"])
        assert path.rows == prefix["target"]
        pivot = path.rows[slot]
        assert pivot.lower().count(generator) == 1
        if generator.upper() in pivot:
            pivot = inverse(pivot)
        cut = pivot.index(generator)
        pivot = pivot[cut:] + pivot[:cut]
        _, moves = normalize(tuple(path.rows), slot, pivot)
        path.extend(moves)
        others = [j for j in range(3) if j != slot]
        for j in others:
            path.change_occurrences(j, generator, inverse(pivot[1:]), slot)
            _, moves = normalize(tuple(path.rows), j)
            path.extend(moves)
        cleared = path.rows[:]
        proof = None
        for cap in range(len(pivot) - 1, 15):
            proof = prove(path.rows, others, pivot[1:], cap, 50000)
            print(
                "normal factor cap",
                cap,
                "hit",
                proof is not None,
                file=sys.stderr,
                flush=True,
            )
            if proof is not None:
                break
        if proof is None:
            return {"completed": False, "cleared": cleared}
        path.append_normal_product(slot, inverse(pivot[1:]), proof)
        path.add({"op": "destabilize", "generator": generator, "i": slot})
        path.record(
            (json.dumps({"target": path.rows}, separators=(",", ":")) + "\n").encode()
        )
        work.write_bytes(buffer.getvalue())
        return {
            "completed": True,
            "cleared": cleared,
            "donor_factors": proof,
            "factor_path_cap": cap,
            "target": path.rows,
            "moves": path.total,
            "cyclic_peak": path.cyclic_peak,
            "raw_peak": path.raw_peak,
        }


if __name__ == "__main__":
    prefix, slot, g, output = sys.argv[1:]
    print(
        json.dumps(
            compile_chart(
                json.loads(Path(prefix).read_text()), int(slot), g, Path(output)
            ),
            indent=2,
        )
    )
