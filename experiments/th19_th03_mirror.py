"""TH19 check of TH03 Theorem T16 / Cor. T17: eps(u) = C(p+1,2) + C(q+1,2) + mu_ab(u) mod 2 on F(a,b);
(a) invariant under u -> v u phi(v)^-1 (phi(a) = b, phi(b) = b^-1 a); (b) flipped by alpha: (u,1) -> (iota(u) b, 1);
values on x^s y = (a^s,1) and k_n = (a^n B A, 1); the eight candidate pairs of T5(d)."""
import random
def fred(u):
    out = []
    for c in u:
        if out and out[-1] == c.swapcase(): out.pop()
        else: out.append(c)
    return "".join(out)
PHI = {"a": "b", "b": "Ba", "A": "B", "B": "Ab"}
def phi(u): return fred("".join(PHI[c] for c in u))
def eps(u):
    p = u.count("a") - u.count("A"); q = u.count("b") - u.count("B"); mu = 0; acc = 0
    for c in u:
        if c == "a": acc += 1
        elif c == "A": acc -= 1
        elif c == "b": mu += acc
        else: mu -= acc
    return ((p+1)*p//2 + (q+1)*q//2 + mu) % 2
random.seed(2); v1 = v2 = 0
for _ in range(2000):
    u = fred("".join(random.choice("aAbB") for _ in range(random.randint(0, 12))))
    v = fred("".join(random.choice("aAbB") for _ in range(random.randint(1, 8))))
    if eps(fred(v + u + phi(v).swapcase()[::-1])) != eps(u): v1 += 1
    if eps(fred(u.swapcase() + "b")) != (eps(u) + 1) % 2: v2 += 1
print("(a) invariance violations:", v1, " (b) flip violations:", v2, " (2000 random pairs)")
xs = lambda s: "a"*s if s >= 0 else "A"*(-s)
print("eps(x^s y), s=-5..6:", [eps(xs(s)) for s in range(-5, 7)], " eps(k_n), n=1..8:", [eps("a"*n + "BA") for n in range(1, 9)])
for (n, s) in [(1, -2), (1, 3), (2, -2), (2, 3), (4, -4), (4, 5), (5, -5), (5, 6)]:
    print(f"   (n,s)=({n},{s}): eps(k_n)={eps('a'*n+'BA')} eps(x^s y)={eps(xs(s))}")
