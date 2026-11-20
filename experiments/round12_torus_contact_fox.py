"""Verify the mod-5 Fox obstruction for the last Round 12 torus contact."""

from fractions import Fraction
import json

from stallings_search import inverse, reduce


DONOR = 'XXYYxyXXyyxYY'
SOURCE = 'xxxxxyXXy'
ARCHIVE = 'XXYYxyy'
NAMES = 'abcdef'
IMAGES = ('b', 'c', 'd', 'e', 'f', 'fddbAC')
CHARACTER = (0, 0, 0, 0, 0, 1)
CONJUGATOR_ABELIANIZATION = (-4, 0, -3, 5, 4, 7)
MODULUS = 5
DUAL_CERTIFICATE = (4, 3, 1, 2, 1, 0)


def schreier(word):
    """Rewrite y=x^-2*z and report the z_i factors before the final x power."""
    word = reduce(''.join({'x': 'x', 'X': 'X', 'y': 'XXz', 'Y': 'Zxx'}[c] for c in word))
    terms = []
    height = 0
    for c in word:
        if c in 'xX':
            height += 1 if c == 'x' else -1
        else:
            terms.append((height, 1 if c == 'z' else -1))
    return terms, height


def substitute(word, images=IMAGES):
    return reduce(''.join(images[NAMES.index(c.lower())] if c.islower()
                          else inverse(images[NAMES.index(c.lower())]) for c in word))


def abelian(word):
    return [word.count(c) - word.count(c.upper()) for c in NAMES]


def dot(left, right):
    return sum(a * b for a, b in zip(left, right))


def identity_matrix():
    return [[int(a == b) for b in NAMES] for a in NAMES]


def determinant(rows):
    rows = [list(map(Fraction, row)) for row in rows]
    answer = 1
    for i in range(len(rows)):
        pivot = next((j for j in range(i, len(rows)) if rows[j][i]), None)
        if pivot is None:
            return 0
        if pivot != i:
            rows[i], rows[pivot] = rows[pivot], rows[i]
            answer *= -1
        answer *= rows[i][i]
        for j in range(i + 1, len(rows)):
            ratio = rows[j][i] / rows[i][i]
            rows[j] = [a - ratio * b for a, b in zip(rows[j], rows[i])]
    return int(answer)


def words():
    donor, hd = schreier(DONOR)
    source, hs = schreier(SOURCE)
    archive, ha = schreier(ARCHIVE)
    assert hd == 0 and hs == ha == -1
    assert donor == [(-2, -1), (0, -1), (1, 1), (-3, 1), (-5, 1), (-4, -1), (-2, -1)]
    assert source == [(3, 1), (-1, 1)]
    assert archive == [(-2, -1), (0, -1), (1, 1), (-1, 1)]
    inverse_images = ('BFecca', 'a', 'b', 'c', 'd', 'e')
    assert tuple(substitute(w) for w in inverse_images) == tuple(NAMES)
    assert tuple(substitute(w, inverse_images) for w in IMAGES) == tuple(NAMES)

    def kernel_word(factors):
        terms = []
        for level, sign in factors:
            if level <= 0:
                term = NAMES[level + 5]
            else:
                term = NAMES[-1]
                for _ in range(level):
                    term = substitute(term)
            terms.append(term if sign == 1 else inverse(term))
        return reduce(''.join(terms))

    assert kernel_word(donor) == ''
    u = substitute(inverse(kernel_word(source)))
    v = substitute(inverse(kernel_word(archive)))
    return u, v, donor, source, archive


def fox(word, signs):
    monomial = 1
    flow = [0] * len(NAMES)
    for c in word:
        i = NAMES.index(c.lower())
        if c.islower():
            flow[i] += monomial
            monomial *= signs[i]
        else:
            monomial *= signs[i]
            flow[i] -= monomial
    return flow, monomial


def cycle_system(u, v, columns):
    orbit, current = [], CHARACTER
    while current not in orbit:
        orbit.append(current)
        current = tuple(dot(col, current) % 2 for col in columns)
    assert current == CHARACTER and len(orbit) == 63

    coefficients, constant = identity_matrix(), [0] * len(NAMES)
    for character in reversed(orbit):
        signs = tuple((-1)**e for e in character)
        u_flow, u_sign = fox(u, signs)
        v_flow, _ = fox(v, signs)
        g_sign = (-1)**(dot(character, CONJUGATOR_ABELIANIZATION) % 2)
        transport = list(zip(*(fox(image, signs)[0] for image in IMAGES)))
        transport = [[u_sign * c for c in row] for row in transport]
        constant = [(a - g_sign * b + dot(row, constant)) % MODULUS
                    for a, b, row in zip(u_flow, v_flow, transport)]
        coefficients = [[dot(row, col) % MODULUS for col in zip(*coefficients)]
                        for row in transport]
    return [[(a - b) % MODULUS for a, b in zip(row, matrix_row)] + [c]
            for row, matrix_row, c in zip(identity_matrix(), coefficients, constant)]


def main():
    u, v, donor, source, archive = words()
    columns = tuple(map(abelian, IMAGES))
    linear = [[a - b for a, b in zip(row, col)]
              for row, col in zip(identity_matrix(), zip(*columns))]
    determinant_value = determinant(linear)
    assert abs(determinant_value) == 1
    assert [dot(row, CONJUGATOR_ABELIANIZATION) for row in linear] == [
        a - b for a, b in zip(abelian(u), abelian(v))]
    augmented = cycle_system(u, v, columns)
    contradiction = [dot(DUAL_CERTIFICATE, col) % MODULUS for col in zip(*augmented)]
    assert contradiction == [0] * len(NAMES) + [1]
    print(json.dumps({
        'literal_words': {'donor': DONOR, 'ak3_row': SOURCE, 'archive_row': ARCHIVE},
        'schreier_factors': {'donor': donor, 'ak3_row': source, 'archive_row': archive},
        'automorphism_images': IMAGES, 'inverse_side_equation_words': [u, v],
        'determinant_I_minus_automorphism_abelianization': determinant_value,
        'conjugator_kernel_abelianization': CONJUGATOR_ABELIANIZATION,
        'character': CHARACTER, 'orbit_length': 63, 'modulus': MODULUS,
        'augmented_system': augmented, 'dual_certificate': DUAL_CERTIFICATE,
        'dual_product': contradiction, 'conjugate': False,
    }, indent=2))


if __name__ == '__main__':
    main()
