"""Agent O: exact proof that k_n = x^n YXyy is NOT conjugate in G_c = <x,y | xyxYYXy> to any
primitive word x^s y (s in Z), for 3 <= n <= 8 -- hence no presentation with a primitive relator is
one ACM move (arbitrary conjugators) from P_n = (c, k_n) with c frozen (research-o Prop. O2).

Method (research-o Sec. 6).  G_c = F(a,b) x|_phi Z (o_gc.py).  Let H = F(a,b) x| <t>, t = y^2, the
index-2 subgroup of even degree:  H = <a,b,t | t a T = B a,  t b T = A b b>.
If k_n ~ x^s y in G_c then k_n^2 is conjugate in G_c to (x^s y)^2, and since G_c = H u H y,
k_n^2 is H-conjugate to (x^s y)^2 or to y (x^s y)^2 Y (Y w y and y w Y are H-conjugate via t).
In normal form: (x^s y)^2 = a^s b^s t,  y (x^s y)^2 Y = b^s (Ba)^s t,  k_n^2 = u_n phi(u_n) t,
u_n = a^n B A.  For every hom rho: H -> PSL(2,p) the traces (up to sign) must then agree for some s.
The candidates are periodic in s with period o = lcm of the PSL-orders of A, B, B^-1 A, so each hom
restricts s to a union of residue classes mod o; an empty intersection over finitely many homs is an
exact proof that no s exists.  Homs are enumerated completely up to conjugation: T over class
representatives, A over SL(2,p), B := A T A^-1 T^-1 forced (up to sign) by the first relation, the
second relation checked up to sign.

    python3 experiments/o_sieve.py --selftest      # p = 7 and 13; n = 1..8; prints the witness hom
"""
import os
import sys
from math import lcm

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import o_gc as G  # noqa: E402


# ------------------------------------------------------------ SL(2,p) utilities
def mmul(A, B, p):
    a, b, c, d = A
    e, f, g, h = B
    return ((a * e + b * g) % p, (a * f + b * h) % p, (c * e + d * g) % p, (c * f + d * h) % p)


def minv(A, p):
    a, b, c, d = A
    return (d % p, (-b) % p, (-c) % p, a % p)


def is_pm_I(M, p):
    return M in ((1, 0, 0, 1), (p - 1, 0, 0, p - 1))


def tr(M, p):
    t = (M[0] + M[3]) % p
    return min(t, (-t) % p)


def psl_order(M, p):
    N, k = M, 1
    while not is_pm_I(N, p):
        N = mmul(N, M, p)
        k += 1
    return k


def sl2(p):
    els = []
    for a in range(p):
        for b in range(p):
            for c in range(p):
                if a:
                    els.append((a, b, c, ((1 + b * c) * pow(a, -1, p)) % p))
                elif (b * c) % p == p - 1:
                    els.extend((a, b, c, d) for d in range(p))
    return els


def conj_reps(els, p):
    seen, reps = set(), []
    for g in els:
        if g in seen:
            continue
        reps.append(g)
        for h in els:
            seen.add(mmul(mmul(minv(h, p), g, p), h, p))
    return reps


def evab(word, A, B, T, p):
    img = {"a": A, "A": minv(A, p), "b": B, "B": minv(B, p), "t": T, "T": minv(T, p)}
    M = (1, 0, 0, 1)
    for ch in word:
        M = mmul(M, img[ch], p)
    return M


def homs_H(p):
    """All homs H -> PSL(2,p) up to conjugation, as SL(2,p) lifts (A, B, T)."""
    els = sl2(p)
    out = []
    for T in conj_reps(els, p):
        Ti = minv(T, p)
        for A in els:
            Ai = minv(A, p)
            B = mmul(mmul(mmul(A, T, p), Ai, p), Ti, p)      # t a T = B a  (B^-1 A = T A T^-1)
            lhs = mmul(mmul(T, B, p), Ti, p)                  # t b T = A b b ?
            rhs = mmul(mmul(Ai, B, p), B, p)
            if lhs == rhs or lhs == tuple((-x) % p for x in rhs):
                out.append((A, B, T))
    return out


def sq_word(n):
    u = "a" * n + "BA"
    assert G.nf(G.killer(n)) == (u, 1)
    return u + G.apply_endo(G.PHI, u) + "t"


def constraints(p, ns):
    """For each n: dict modulus -> bytearray of allowed residues (1 = not excluded)."""
    cons = {n: {} for n in ns}
    H = homs_H(p)
    used = 0
    for (A, B, T) in H:
        if is_pm_I(mmul(mmul(A, B, p), mmul(minv(A, p), minv(B, p), p), p), p):
            continue                                   # abelian fibre image: no information
        o = lcm(psl_order(A, p), psl_order(B, p), psl_order(mmul(minv(B, p), A, p), p))
        used += 1
        cand = [{tr(evab("a" * s + "b" * s + "t", A, B, T, p), p),
                 tr(evab("b" * s + "Ba" * s + "t", A, B, T, p), p)} for s in range(o)]
        for n in ns:
            t = tr(evab(sq_word(n), A, B, T, p), p)
            arr = cons[n].setdefault(o, bytearray(b"\x01") * o)
            for s in range(o):
                if t not in cand[s]:
                    arr[s] = 0
    return cons, len(H), used


def combine(cons_list, cap=400_000_000):
    """Intersect residue constraints by CRT; return (M, surviving residues mod M)."""
    byo = {}
    for cons in cons_list:
        for o, arr in cons.items():
            cur = byo.setdefault(o, bytearray(b"\x01") * o)
            for s in range(o):
                cur[s] &= arr[s]
    M, used = 1, []
    for o in sorted(byo, key=lambda o: sum(byo[o])):
        if lcm(M, o) <= cap:
            M = lcm(M, o)
            used.append(o)
    acc = int.from_bytes(bytes([1]) * M, "big")
    for o in used:
        acc &= int.from_bytes(bytes(byo[o]) * (M // o), "big")
    surv = acc.to_bytes(M, "big")
    return M, [s for s in range(M) if surv[s]]


def witness(p, n, period=None):
    """A small set of homs H -> PSL(2,p) (all with the same period o) whose constraints on s
    jointly exclude every residue mod o for k_n; returns a list of dicts, or [] if none."""
    data = []
    for (A, B, T) in homs_H(p):
        if is_pm_I(mmul(mmul(A, B, p), mmul(minv(A, p), minv(B, p), p), p), p):
            continue
        o = lcm(psl_order(A, p), psl_order(B, p), psl_order(mmul(minv(B, p), A, p), p))
        if period is not None and o != period:
            continue
        t = tr(evab(sq_word(n), A, B, T, p), p)
        cands = [sorted({tr(evab("a" * s + "b" * s + "t", A, B, T, p), p),
                         tr(evab("b" * s + "Ba" * s + "t", A, B, T, p), p)}) for s in range(o)]
        allowed = frozenset(s for s in range(o) if t in cands[s])
        data.append((o, allowed, {"A": A, "B": B, "T": T, "period": o, "trace_k_n_squared": t,
                                  "candidate_traces_by_s": cands, "allowed_s": sorted(allowed)}))
    for o in sorted({d[0] for d in data}):
        pool = [d for d in data if d[0] == o]
        remaining = set(range(o))
        chosen = []
        while remaining and pool:
            best = min(pool, key=lambda d: len(remaining & d[1]))
            if len(remaining & best[1]) == len(remaining):
                break
            chosen.append(best[2])
            remaining &= best[1]
            pool.remove(best)
        if not remaining:
            return chosen
    return []


def selftest(primes=(7, 13), ns=range(1, 9)):
    # relation sanity: the words encode H correctly for a hom, and k_n normal forms
    for n in ns:
        sq_word(n)
    results = {}
    cons_all = {n: [] for n in ns}
    for p in primes:
        cons, nh, used = constraints(p, ns)
        print(f"p={p}: {nh} homs H->PSL(2,{p}) up to conjugation, {used} with nonabelian fibre image")
        for n in ns:
            cons_all[n].append(cons[n])
    for n in ns:
        M, surv = combine(cons_all[n])
        small = sorted(surv, key=lambda s: min(s, M - s))[:6]
        results[n] = (M, len(surv), [s if s <= M // 2 else s - M for s in small])
        print(f"  k_{n}: surviving s mod {M}: {len(surv)}  smallest |s|: {results[n][2]}")
    # controls: k_1 ~ k_2 ~ x^-2 y is a true conjugacy (research-o Cor. O3), so s = -2 must survive
    for n in (1, 2):
        M, cnt, _ = results[n]
        assert cnt > 0, "control failed"
    # the exact exclusions
    excluded = [n for n in ns if results[n][1] == 0]
    print("  excluded n (no s in Z with k_n ~ x^s y in G_c):", excluded)
    for n in (3, 4):
        ws = witness(13, n, period=7)
        print(f"  witness homs H -> PSL(2,13) jointly excluding every s mod {ws[0]['period'] if ws else '?'} for k_{n}:")
        for w in ws:
            print("    A=%s B=%s T=%s  tr(k_n^2)=%s  allowed s=%s  candidate traces by s=%s"
                  % (w["A"], w["B"], w["T"], w["trace_k_n_squared"], w["allowed_s"], w["candidate_traces_by_s"]))
    assert set(excluded) >= {3, 4, 5, 6, 7, 8}, excluded
    print("o_sieve self-test passed")
    return results


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
    else:
        ps = tuple(int(a) for a in sys.argv[1:]) or (7, 13)
        selftest(primes=ps)
