"""Verify geometric-block and marking controls from round 02."""

import json
from collections import Counter
from itertools import combinations
from pathlib import Path

from elementary_verify import inverse, replay
from k4_rotation_parity import decide as parity_test
from thickening_rotations import analyse_orders
from verify_link_parity import verify_certificate


def reduce_word(word):
    stack = []
    for letter in word:
        if stack and stack[-1] == letter.swapcase():
            stack.pop()
        else:
            stack.append(letter)
    return "".join(stack)


def whitehead_edges(words):
    edges = Counter()
    for word in words:
        assert word and reduce_word(word) == word
        assert word[0].swapcase() != word[-1]
        for first, second in zip(word, word[1:] + word[0]):
            edges[tuple(sorted((first.swapcase(), second)))] += 1
    return edges


def checked_cut_minima(edges, generators):
    letters = "".join(c + c.upper() for c in generators)
    result = {}
    for letter in letters:
        degree = sum(weight for edge, weight in edges.items() if letter in edge)
        others = [v for v in letters if v not in (letter, letter.swapcase())]
        minimum = min(
            sum(weight for (a, b), weight in edges.items() if (a in side) != (b in side))
            for size in range(len(others) + 1)
            for selected in combinations(others, size)
            for side in [{letter, *selected}]
        )
        assert minimum == degree
        if letter.islower():
            result[letter] = degree
    return result


def check_conjugated_pivot():
    conj = "xy"
    donor = conj + "x" + inverse(conj)
    changed = reduce_word("y" + donor)
    assert changed == "yxyxYX"
    quotient = reduce_word(changed.replace("x", "").replace("X", ""))
    assert quotient == "y"
    substitution = {"x": "x", "X": "X", "y": "yX", "Y": "xY"}
    new_word = reduce_word("".join(substitution[c] for c in changed))
    assert new_word == "yyxYX"
    pair = ("x", new_word)
    degrees = checked_cut_minima(whitehead_edges(pair), "xy")
    certificate = parity_test(pair)
    assert certificate["status"] == "PARITY_OBSTRUCTION"
    parity_check = verify_certificate(certificate)
    assert parity_check["equations"] == 1
    return {
        "start": ["x", "y"],
        "conjugator": conj,
        "end": ["x", changed],
        "quotient_unchanged": quotient,
        "whitehead_minimal_pair": list(pair),
        "whitehead_cut_minima": degrees,
        "independent_parity_replay": parity_check,
    }


def check_nonprimitive_block():
    block = ("xxYYY", "xxxYYYY")
    source = Path("certificates")
    witness = json.loads((source / "w_geometric_nonprimitive_planar.json").read_text())
    assert tuple(witness["words"]) == block
    orders = analyse_orders(block, witness["best_orders"])
    assert orders["total_genus"] == 0
    path = json.loads((source / "w_geometric_nonprimitive_full.json").read_text())
    assert tuple(path["start"]) == block
    path_check = replay(path)
    assert path_check["endpoint"] == ["x", "y"]
    conj = "xZXYz"
    word = reduce_word("z" + conj + block[0] + inverse(conj))
    assert word == "zxZXYzxxYYYZyxzX"
    full = (*block, word)
    minima = {
        w: checked_cut_minima(whitehead_edges([w]), "xyz")
        for w in full
    }
    assert all(len(w) > 1 for w in full)
    edges = whitehead_edges([word])
    partition = ("Xxy", "YZz")
    assert all(tuple(sorted((a, b))) in edges for a in partition[0] for b in partition[1])
    quotient = reduce_word("".join(c for c in word if c in "zZ"))
    assert quotient == "z"
    # After normalizing the two frozen-donor rows, cancel the one factor in
    # the third row by its five signed conjugate letters.
    working = word
    for letter in inverse(block[0]):
        working = reduce_word(working + conj + letter + inverse(conj))
    assert working == "z"
    return {
        "rank_three_tuple": list(full),
        "geometric_block": list(block),
        "block_planar_witness_genus": orders["total_genus"],
        "block_ordinary_moves": path_check["moves"],
        "block_endpoint": path_check["endpoint"],
        "whitehead_cut_minima_for_each_word": minima,
        "nonplanar_K33_partition_in_last_word": list(partition),
        "quotient_by_whole_block": [quotient],
        "direct_normalization_endpoint": [*path_check["endpoint"], working],
        "final_conjugate_factors": len(block[0]),
    }


if __name__ == "__main__":
    result = {
        "one_product_with_pivot": check_conjugated_pivot(),
        "nonprimitive_geometric_block": check_nonprimitive_block(),
    }
    print(json.dumps(result, indent=2))
