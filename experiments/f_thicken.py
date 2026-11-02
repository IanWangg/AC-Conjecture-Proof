#!/usr/bin/env python3
"""Thickenability (3-manifold embeddability) test for rank-2 presentation complexes.

Research agent F, 2026-11-02.  Python standard library only.

Words are tuples over {1,-1,2,-2} (x, x^-1, y, y^-1); strings over x X y Y are
accepted by `parse`.  The presentation complex K(r1,r2) has one vertex, two
edges e_x, e_y, and two 2-cells attached along the given cyclically reduced
words.  K is *thickenable* if it embeds in some 3-manifold; for a presentation
of the trivial group K is contractible, any thickening is simply connected and
hence orientable, so it suffices to test ORIENTABLE thickenings.

Criterion (see research/research-f.md, Section 2): K has an orientable
3-manifold regular neighbourhood iff its vertex link Lk(v) (the Whitehead
graph: vertices x+, x-, y+, y-; one edge per cyclic corner of each relator)
has an embedding in S^2 such that, for each generator g, the cyclic order of
the strands (letter occurrences of g^{+-1}) around g+ is the REVERSE of their
cyclic order around g-.  Equivalently the relators are read by disjoint simple
closed curves on the boundary of a genus-2 handlebody with respect to a fixed
pair of meridian discs (a Heegaard-type diagram).

Two independent decision procedures are implemented:

  * `thickenable_bruteforce`: enumerate the cyclic orders of the strands at
    x+ and y+ (forcing the reversed orders at x-, y-), trace faces, test
    genus 0 on every connected component.  Exponential; small words only.
  * `thickenable`: enumerate planar "band graphs" (parallel classes of link
    edges) on the four link vertices, band weights, and the two handle twist
    parameters; trace the resulting disjoint curves and compare their cyclic
    words with the relators.  Polynomial in the word length.

`python3 experiments/f_thicken.py --selftest` cross-checks both procedures.
"""
import itertools
import random
import sys

# ----------------------------------------------------------------- words

LET = {"x": 1, "X": -1, "y": 2, "Y": -2}
SYM = {1: "x", -1: "X", 2: "y", -2: "Y"}


def parse(s):
    return tuple(LET[c] for c in s)


def fmt(w):
    return "".join(SYM[a] for a in w)


def free_reduce(w):
    out = []
    for a in w:
        if out and out[-1] == -a:
            out.pop()
        else:
            out.append(a)
    return tuple(out)


def cyc_reduce(w):
    w = list(free_reduce(w))
    while len(w) >= 2 and w[0] == -w[-1]:
        w = w[1:-1]
    return tuple(w)


def inverse(w):
    return tuple(-a for a in reversed(w))


def cyc_canon(w):
    """Canonical representative of a cyclic word up to rotation and inversion."""
    w = tuple(w)
    if not w:
        return ()
    best = None
    for u in (w, inverse(w)):
        for k in range(len(u)):
            r = u[k:] + u[:k]
            if best is None or r < best:
                best = r
    return best


def is_cyc_reduced(w):
    return len(w) > 0 and free_reduce(w) == tuple(w) and (len(w) == 1 or w[0] != -w[-1])


# ------------------------------------------------------- link structure
# vertex ids: x+ = 0, x- = 1, y+ = 2, y- = 3

def plus(g):
    return 2 * (g - 1)


def minus(g):
    return 2 * (g - 1) + 1


def start_v(a):          # vertex where the traversal of letter a begins
    g = abs(a)
    return minus(g) if a > 0 else plus(g)


def end_v(a):            # vertex where the traversal of letter a ends
    g = abs(a)
    return plus(g) if a > 0 else minus(g)


PAIRS = [(0, 1), (2, 3), (0, 2), (0, 3), (1, 2), (1, 3)]


def corner_counts(rels):
    m = {p: 0 for p in PAIRS}
    for r in rels:
        n = len(r)
        for i in range(n):
            u, v = end_v(r[i]), start_v(r[(i + 1) % n])
            if u == v:
                raise ValueError("relator not cyclically reduced")
            m[(min(u, v), max(u, v))] += 1
    return m


# ------------------------------------------ procedure 1: brute force

def _faces_genus_ok(rot, mate, vertex_of):
    """rot: dict half-edge -> next half-edge around its vertex.
    mate: dict half-edge -> other half-edge of the same edge.
    Returns True iff every connected component is embedded with genus 0."""
    halves = list(rot)
    # faces: orbits of h -> rot[mate[h]]
    seen = set()
    face_of = {}
    nf = 0
    for h in halves:
        if h in seen:
            continue
        cur = h
        while cur not in seen:
            seen.add(cur)
            face_of[cur] = nf
            cur = rot[mate[cur]]
        nf += 1
    # components via union find on vertices
    parent = {}

    def find(a):
        while parent.setdefault(a, a) != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for h in halves:
        a, b = find(vertex_of[h]), find(vertex_of[mate[h]])
        if a != b:
            parent[a] = b
    comp_v, comp_e, comp_f = {}, {}, {}
    for v in set(vertex_of.values()):
        c = find(v)
        comp_v[c] = comp_v.get(c, 0) + 1
    for h in halves:
        c = find(vertex_of[h])
        comp_e[c] = comp_e.get(c, 0) + 0.5
    fset = {}
    for h in halves:
        fset.setdefault(find(vertex_of[h]), set()).add(face_of[h])
    for c in comp_v:
        V, E, F = comp_v[c], comp_e.get(c, 0), len(fset.get(c, ()))
        if E == 0:
            continue
        if V - E + F != 2:
            return False
    return True


def thickenable_bruteforce(r1, r2, limit=2_000_000):
    rels = [tuple(r1), tuple(r2)]
    for r in rels:
        if not is_cyc_reduced(r):
            raise ValueError("relators must be cyclically reduced")
    # occurrences
    occ = {1: [], 2: []}
    for k, r in enumerate(rels):
        for i, a in enumerate(r):
            occ[abs(a)].append((k, i))
    # half-edges: ('in', k, i) at start_v(r_k[i]); ('out', k, i) at end_v(r_k[i])
    vertex_of, mate = {}, {}
    for k, r in enumerate(rels):
        n = len(r)
        for i, a in enumerate(r):
            vertex_of[("in", k, i)] = start_v(a)
            vertex_of[("out", k, i)] = end_v(a)
        for i in range(n):
            a, b = ("out", k, i), ("in", k, (i + 1) % n)
            mate[a], mate[b] = b, a

    def half_at(vertex, o):
        k, i = o
        a = rels[k][i]
        return ("out", k, i) if end_v(a) == vertex else ("in", k, i)

    def cyclic_orders(items):
        if not items:
            yield []
            return
        first, rest = items[0], items[1:]
        for p in itertools.permutations(rest):
            yield [first] + list(p)

    total = 1
    for g in (1, 2):
        n = len(occ[g])
        for t in range(2, n):
            total *= t
    if total > limit:
        raise ValueError(f"bruteforce too large ({total})")
    for ox in cyclic_orders(occ[1]):
        for oy in cyclic_orders(occ[2]):
            rot = {}
            for g, order in ((1, ox), (2, oy)):
                n = len(order)
                for j in range(n):
                    # at g+: order; at g-: reversed order
                    rot[half_at(plus(g), order[j])] = half_at(plus(g), order[(j + 1) % n])
                    rot[half_at(minus(g), order[(j + 1) % n])] = half_at(minus(g), order[j])
            if _faces_genus_ok(rot, mate, vertex_of):
                return True
    return False


# ------------------------------------------ procedure 2: band graphs

def _band_systems(m):
    """Yield (bands, rotation) for planar band graphs compatible with counts m.
    bands: list of (u, v); rotation: dict vertex -> cyclic list of band ends
    (band_index, end) with end 0 at u and 1 at v."""
    present = [p for p in PAIRS if m[p] > 0]
    # Two non-parallel bands on a pair (u,v) bound a circle through u and v
    # with one of the two remaining vertices on each side (otherwise the bands
    # are consecutive at u and v and merge into one band); hence the
    # complementary pair carries no edge.  Three bands would need three other
    # vertices.  So a pair has at most 2 bands, and 2 only if its complement
    # has m = 0.
    comp = {(0, 1): (2, 3), (2, 3): (0, 1), (0, 2): (1, 3), (1, 3): (0, 2),
            (0, 3): (1, 2), (1, 2): (0, 3)}
    choices = [range(1, (2 if (m[p] >= 2 and m[comp[p]] == 0) else 1) + 1)
               for p in present]
    for mult in itertools.product(*choices):
        bands = []
        for p, b in zip(present, mult):
            bands += [p] * b
        ends = {v: [] for v in range(4)}
        for bi, (u, v) in enumerate(bands):
            ends[u].append((bi, 0))
            ends[v].append((bi, 1))
        per_vertex = []
        for v in range(4):
            items = ends[v]
            if len(items) <= 1:
                per_vertex.append([items])
            else:
                per_vertex.append([[items[0]] + list(p)
                                   for p in itertools.permutations(items[1:])])
        for combo in itertools.product(*per_vertex):
            rot = {}
            vertex_of = {}
            mate = {}
            for v, order in enumerate(combo):
                n = len(order)
                for j, h in enumerate(order):
                    rot[h] = order[(j + 1) % n]
                    vertex_of[h] = v
            for bi in range(len(bands)):
                mate[(bi, 0)], mate[(bi, 1)] = (bi, 1), (bi, 0)
            if _faces_genus_ok(rot, mate, vertex_of):
                yield bands, {v: combo[v] for v in range(4)}


def _curves(bands, rotation, weights, twist, ngen):
    """Trace the disjoint curves of a weighted band diagram with twists.
    Returns list of cyclic words."""
    slots = {v: [] for v in range(4)}   # vertex -> list of (band, edge index)
    for v in range(4):
        for (bi, end) in rotation[v]:
            w = weights[bi]
            idx = range(w) if end == 0 else range(w - 1, -1, -1)
            for e in idx:
                slots[v].append((bi, e))
    pos = {}
    for v in range(4):
        for j, s in enumerate(slots[v]):
            pos[(v, s)] = j
    # edge partner of slot (v, j)
    edge_partner = {}
    for v in range(4):
        for j, (bi, e) in enumerate(slots[v]):
            u, w_ = bands[bi]
            other = w_ if v == u else u
            edge_partner[(v, j)] = (other, pos[(other, (bi, e))])
    # handle partner
    handle = {}
    for g in (1, 2):
        n = ngen[g]
        if len(slots[plus(g)]) != n or len(slots[minus(g)]) != n:
            return None
        c = twist[g]
        for j in range(n):
            a, b = (plus(g), j), (minus(g), (c - j) % n)
            handle[a], handle[b] = b, a
    visited = set()
    words = []
    for start in handle:
        if start in visited:
            continue
        word = []
        cur = start
        while True:
            visited.add(cur)
            nxt = handle[cur]
            visited.add(nxt)
            v = cur[0]
            g = v // 2 + 1
            word.append(g if v == minus(g) else -g)
            cur = edge_partner[nxt]
            if cur == start:
                break
            if cur in visited:
                return None   # should not happen
        words.append(tuple(word))
    return words


def thickenable(r1, r2, want_witness=False):
    rels = [tuple(r1), tuple(r2)]
    for r in rels:
        if not is_cyc_reduced(r):
            raise ValueError("relators must be cyclically reduced")
    m = corner_counts(rels)
    ngen = {g: sum(1 for r in rels for a in r if abs(a) == g) for g in (1, 2)}
    target = sorted(cyc_canon(r) for r in rels)
    for bands, rotation in _band_systems(m):
        # weight splits: bands of the same pair share m[p]
        by_pair = {}
        for bi, p in enumerate(bands):
            by_pair.setdefault(p, []).append(bi)
        split_choices = []
        for p, bis in by_pair.items():
            if len(bis) == 1:
                split_choices.append([((bis[0], m[p]),)])
            else:
                split_choices.append([((bis[0], a), (bis[1], m[p] - a))
                                      for a in range(1, m[p])])
        for split in itertools.product(*split_choices):
            weights = {}
            for part in split:
                for bi, w in part:
                    weights[bi] = w
            for cx in range(max(1, ngen[1])):
                for cy in range(max(1, ngen[2])):
                    words = _curves(bands, rotation, weights, {1: cx, 2: cy}, ngen)
                    if words is None or len(words) != 2:
                        continue
                    if sorted(cyc_canon(w) for w in words) == target:
                        if want_witness:
                            return True, {"bands": bands, "rotation": rotation,
                                          "weights": weights, "twist": (cx, cy)}
                        return True
    return (False, None) if want_witness else False


# ------------------------------------- procedure 2b: twist-determined

def _slot_tables(bands, rotation, weights):
    slots = {v: [] for v in range(4)}
    for v in range(4):
        for (bi, end) in rotation[v]:
            w = weights[bi]
            idx = range(w) if end == 0 else range(w - 1, -1, -1)
            for e in idx:
                slots[v].append((bi, e))
    pos = {}
    for v in range(4):
        for j, s in enumerate(slots[v]):
            pos[(v, s)] = j
    partner = {}
    for v in range(4):
        for j, (bi, e) in enumerate(slots[v]):
            u, w_ = bands[bi]
            other = w_ if v == u else u
            partner[(v, j)] = (other, pos[(other, (bi, e))])
    return slots, partner


def _trace_fixed(word, start, partner, twist, ngen):
    """Trace `word` from slot `start` (at start_v(word[0])) with twists given
    (dict g -> c or None).  Returns (ok, used_slots, twist) trying all values
    of an undetermined twist on its first use (generator over solutions)."""
    def rec(i, cur, tw, used):
        if i == len(word):
            if cur == start:
                yield tw, used
            return
        a = word[i]
        g = abs(a)
        v = cur[0]
        if v != start_v(a):
            return
        n = ngen[g]
        cvals = [tw[g]] if tw[g] is not None else range(n)
        for c in cvals:
            ext_v = end_v(a)
            ext = (ext_v, (c - cur[1]) % n)
            if cur in used or ext in used:
                continue
            nxt = partner[ext]
            t2 = dict(tw)
            t2[g] = c
            yield from rec(i + 1, nxt, t2, used | {cur, ext})
    yield from rec(0, start, twist, frozenset())


def thickenable_fast(r1, r2):
    rels = [tuple(r1), tuple(r2)]
    for r in rels:
        if not is_cyc_reduced(r):
            raise ValueError("relators must be cyclically reduced")
    m = corner_counts(rels)
    ngen = {g: sum(1 for r in rels for a in r if abs(a) == g) for g in (1, 2)}
    for bands, rotation in _band_systems(m):
        by_pair = {}
        for bi, p in enumerate(bands):
            by_pair.setdefault(p, []).append(bi)
        split_choices = []
        for p, bis in by_pair.items():
            if len(bis) == 1:
                split_choices.append([((bis[0], m[p]),)])
            else:
                split_choices.append([((bis[0], a), (bis[1], m[p] - a))
                                      for a in range(1, m[p])])
        for split in itertools.product(*split_choices):
            weights = {}
            for part in split:
                for bi, w in part:
                    weights[bi] = w
            slots, partner = _slot_tables(bands, rotation, weights)
            w1, w2 = rels
            v0 = start_v(w1[0])
            for j in range(len(slots[v0])):
                for tw, used in _trace_fixed(w1, (v0, j), partner,
                                             {1: None, 2: None}, ngen):
                    # r2 must be traced by the complementary strands
                    v1 = start_v(w2[0])
                    for k in range(len(slots[v1])):
                        s = (v1, k)
                        if s in used:
                            continue
                        for tw2, used2 in _trace_fixed(w2, s, partner, tw, ngen):
                            if len(used) + len(used2) == 2 * (ngen[1] + ngen[2]):
                                return True
    return False


# ------------------------------------------------------------ self test

def random_cr_word(n, rng):
    while True:
        w = []
        for _ in range(n):
            choices = [a for a in (1, -1, 2, -2) if not w or a != -w[-1]]
            w.append(rng.choice(choices))
        if is_cyc_reduced(tuple(w)):
            return tuple(w)


def random_diagram_pair(rng, max_len=12):
    """Generate a genuinely realizable pair by building a random weighted band
    diagram and keeping it when it yields exactly two curves (independent of
    the brute-force procedure)."""
    for _ in range(10000):
        m = {p: 0 for p in PAIRS}
        for p in PAIRS:
            if rng.random() < 0.7:
                m[p] = rng.randint(1, 3)
        nx = m[(0, 1)] + m[(0, 2)] + m[(0, 3)]
        if nx != m[(0, 1)] + m[(1, 2)] + m[(1, 3)]:
            continue
        ny = m[(2, 3)] + m[(0, 2)] + m[(1, 2)]
        if ny != m[(2, 3)] + m[(0, 3)] + m[(1, 3)]:
            continue
        if nx + ny == 0 or nx + ny > max_len or nx > 6 or ny > 6:
            continue
        systems = list(_band_systems(m))
        if not systems:
            continue
        bands, rotation = rng.choice(systems)
        weights = {}
        by_pair = {}
        for bi, p in enumerate(bands):
            by_pair.setdefault(p, []).append(bi)
        ok = True
        for p, bis in by_pair.items():
            if len(bis) == 1:
                weights[bis[0]] = m[p]
            else:
                if m[p] < 2:
                    ok = False
                    break
                a = rng.randint(1, m[p] - 1)
                weights[bis[0]], weights[bis[1]] = a, m[p] - a
        if not ok:
            continue
        ngen = {1: nx, 2: ny}
        tw = {1: rng.randrange(max(1, nx)), 2: rng.randrange(max(1, ny))}
        words = _curves(bands, rotation, weights, tw, ngen)
        if words and len(words) == 2 and all(is_cyc_reduced(w) for w in words):
            return words
    raise RuntimeError("no diagram found")


def selftest(seed=2026, trials=400):
    rng = random.Random(seed)
    # basic facts
    assert thickenable(parse("x"), parse("y"))
    assert thickenable_bruteforce(parse("x"), parse("y"))
    assert thickenable(parse("xxx"), parse("y"))          # (3,1) torus curve
    assert not thickenable(parse("xx"), parse("x"))       # needs a Klein bottle
    assert not thickenable_bruteforce(parse("xx"), parse("x"))
    # positive controls from random diagrams, checked by brute force
    pos = 0
    for _ in range(trials // 2):
        r1, r2 = random_diagram_pair(rng)
        assert thickenable_bruteforce(r1, r2), (fmt(r1), fmt(r2))
        assert thickenable(r1, r2), (fmt(r1), fmt(r2))
        pos += 1
    # random pairs: the two procedures must agree
    agree = yes = 0
    for _ in range(trials):
        n1, n2 = rng.randint(1, 6), rng.randint(1, 6)
        r1, r2 = random_cr_word(n1, rng), random_cr_word(n2, rng)
        if any(len([a for a in r1 + r2 if abs(a) == g]) > 6 for g in (1, 2)):
            continue
        a = thickenable(r1, r2)
        b = thickenable_bruteforce(r1, r2)
        assert a == b, (fmt(r1), fmt(r2), a, b)
        agree += 1
        yes += a
    print(f"self-test passed: {pos} diagram-generated positives confirmed by both "
          f"procedures; {agree} random pairs agree ({yes} thickenable)")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest()
    elif len(sys.argv) == 3:
        r1, r2 = cyc_reduce(parse(sys.argv[1])), cyc_reduce(parse(sys.argv[2]))
        ok, wit = thickenable(r1, r2, want_witness=True)
        print({"r1": fmt(r1), "r2": fmt(r2), "thickenable": ok, "witness": wit})
    else:
        print(__doc__)
