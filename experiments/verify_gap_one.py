"""Independent near-equality checks for the AK cyclic plateau theorem.

No external packages. Enumeration supports the symbolic proof; it is not
a global search of the AC graph and cannot establish non-AC-triviality.
"""
from itertools import product
import json

ALPHABET = 'xXyY'


def inverse(w):
    return w.swapcase()[::-1]


def cyclic_words(max_length):
    for size in range(1, max_length + 1):
        for letters in product(ALPHABET, repeat=size):
            if any(letters[i] == letters[(i+1) % size].swapcase()
                   for i in range(size)):
                continue
            yield ''.join(letters)


def free_product_form(word, orders):
    out = []
    for c in word:
        factor = 0 if c.lower() == 'x' else 1
        exponent = (1 if c.islower() else -1) % orders[factor]
        if out and out[-1][0] == factor:
            exponent = (exponent + out.pop()[1]) % orders[factor]
        if exponent:
            out.append((factor, exponent))
    while len(out) > 1 and out[0][0] == out[-1][0]:
        factor, left = out.pop(0)
        right = out.pop()[1]
        exponent = (left + right) % orders[factor]
        if exponent:
            out.append((factor, exponent))
    return tuple(out)


def necklace(word, orders):
    syllables = free_product_form(word, orders)
    if not syllables:
        return ()
    return min(syllables[i:] + syllables[:i] for i in range(len(syllables)))


def exponent_vector(word):
    return (word.count('x') - word.count('X'),
            word.count('y') - word.count('Y'))


def relator_lattice_test(a, b, orders):
    delta = tuple(x-y for x, y in zip(a, b))
    return delta[0] % orders[0] == 0 and delta[1] == -(delta[0] // orders[0])*orders[1]


def torus_normal_form(word, orders):
    """Canonical central-extension normal form in <x,y|x^a=y^b>."""
    central = 0
    syllables = []
    for c in word:
        factor = 0 if c.lower() == 'x' else 1
        exponent = 1 if c.islower() else -1
        if syllables and syllables[-1][0] == factor:
            exponent += syllables.pop()[1]
        carry, exponent = divmod(exponent, orders[factor])
        central += carry
        if exponent:
            syllables.append((factor, exponent))
    return central, tuple(syllables)


def check(n, swapped):
    orders = (n+1, n) if swapped else (n, n+1)
    braid = 'xyxYXY'
    targets = {necklace(braid, orders), necklace(inverse(braid), orders)}
    counts = {length: 0 for length in range(1, 8)}
    lattice_counts = dict(counts)
    for w in cyclic_words(7):
        if necklace(w, orders) not in targets:
            continue
        counts[len(w)] += 1
        # Quotient conjugacy to b and b^-1 may have the same necklace.
        # Apply abelianization against every matching orientation.
        if any(necklace(w, orders) == necklace(t, orders) and
               relator_lattice_test(exponent_vector(w), exponent_vector(t), orders)
               for t in (braid, inverse(braid))):
            lattice_counts[len(w)] += 1
    assert all(counts[k] == 0 for k in range(1, 6))
    assert counts[6] == lattice_counts[6] == 12
    assert lattice_counts[7] == 0
    if n >= 4:
        assert counts[7] == 0
    else:
        assert counts[7] > 0
    return {'n': n, 'swapped': swapped, 'factor_orders': orders,
            'free_product_candidates_by_length': counts,
            'also_passing_torus_abelianization': lattice_counts}


if __name__ == '__main__':
    reports = [check(n, swapped) for n in (3, 4, 5) for swapped in (False, True)]
    braid, witness = 'xyxYXY', 'XXyxYxxY'
    assert len(witness) == 8
    assert torus_normal_form(braid, (3, 4)) == torus_normal_form(witness, (3, 4))
    assert witness not in {t[i:]+t[:i] for t in (braid, inverse(braid)) for i in range(len(t))}
    print(json.dumps({'checks': reports, 'AK3_braid_length8_witness': witness,
                      'witness_is_equal_in_torus_quotient': True,
                      'scope': 'near-plateau checks; no global AC conclusion'}, indent=2))
