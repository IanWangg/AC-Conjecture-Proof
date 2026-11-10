"""TH19 referee helpers (standard library only): free words on x,y (X,Y = inverses),
substitution automorphisms, and the C2*C3 necklace invariant of the braid/trefoil group
B = <x,y | xyx = yxy> = <s,t | s^2 = t^3> (research-a/j: x->T^2 S, Y->T S, X->S T, y->S T^2)."""

def red(w):
    out = []
    for c in w:
        if out and out[-1] == c.swapcase():
            out.pop()
        else:
            out.append(c)
    return "".join(out)

def inv(w):
    return w.swapcase()[::-1]

def cyc(w):
    w = red(w)
    while len(w) >= 2 and w[0] == w[-1].swapcase():
        w = w[1:-1]
    return w

def rots(w):
    return {w[i:] + w[:i] for i in range(len(w))} if w else {""}

def orb(w):
    w = cyc(w)
    return rots(w) | rots(inv(w))

def canon(w):
    return min(orb(w))

def subst(w, img):
    """apply the endomorphism x->img['x'], y->img['y'] and freely reduce"""
    full = {"x": img["x"], "y": img["y"], "X": inv(img["x"]), "Y": inv(img["y"])}
    return red("".join(full[c] for c in w))

def expo(w):
    return (w.count("x") - w.count("X"), w.count("y") - w.count("Y"))

# ---- C2*C3 = <S>*<T>: cyclically reduced necklace of the image of a word in B
_IMG = {"x": [("T", 2), ("S", 1)], "Y": [("T", 1), ("S", 1)],
        "X": [("S", 1), ("T", 1)], "y": [("S", 1), ("T", 2)]}

def c2c3(w):
    """reduced syllable list of the image of w in C2*C3"""
    out = []
    for c in w:
        for (g, e) in _IMG[c]:
            if out and out[-1][0] == g:
                m = 2 if g == "S" else 3
                e2 = (out[-1][1] + e) % m
                out.pop()
                if e2:
                    out.append((g, e2))
            else:
                out.append((g, e))
    return out

def c2c3_necklace(w):
    """conjugacy invariant in C2*C3: canonical rotation of the cyclically reduced syllable word"""
    s = c2c3(w)
    while len(s) >= 2 and s[0][0] == s[-1][0]:
        g = s[0][0]
        m = 2 if g == "S" else 3
        e = (s[0][1] + s[-1][1]) % m
        s = s[1:-1]
        if e:
            s = [(g, e)] + s
            if len(s) == 1:
                break
    if len(s) <= 1:
        return tuple(s)
    return min(tuple(s[i:] + s[:i]) for i in range(len(s)))

def conj_in_B(u, v):
    """u ~ v in B (Lemma J0 of research-j): same C2*C3 necklace and same abelianization x,y->1"""
    return sum(expo(u)) == sum(expo(v)) and c2c3_necklace(u) == c2c3_necklace(v)

def cyc_words(L):
    """all cyclically reduced words of length L"""
    letters = "xXyY"
    def rec(pref):
        if len(pref) == L:
            if L == 0 or pref[0] != pref[-1].swapcase():
                yield pref
            return
        for c in letters:
            if not pref or pref[-1] != c.swapcase():
                yield from rec(pref + c)
    yield from rec("")

# ---- generic torus-knot group <x,y | x^p = y^q> (p, q >= 2 coprime): conjugacy = necklace in C_p*C_q + abelianization
def neck_pq(w, p, q):
    s = []
    for ch in w:
        g = "s" if ch in "xX" else "t"; m = p if g == "s" else q; e = 1 if ch in "xy" else m - 1
        if s and s[-1][0] == g:
            e2 = (s[-1][1] + e) % m; s.pop()
            if e2: s.append((g, e2))
        else:
            s.append((g, e))
    while len(s) >= 2 and s[0][0] == s[-1][0]:
        g = s[0][0]; m = p if g == "s" else q; e = (s[0][1] + s[-1][1]) % m; s = s[1:-1]
        if e: s = [(g, e)] + s
    return min(tuple(s[i:] + s[:i]) for i in range(len(s))) if s else ()

def conj_pq(u, v, p, q):
    """u ~ v in <x,y | x^p = y^q> (research-j Lemma J0 / research-g Lemma 1)"""
    ab = lambda w: q*expo(w)[0] + p*expo(w)[1]
    return ab(u) == ab(v) and neck_pq(u, p, q) == neck_pq(v, p, q)
