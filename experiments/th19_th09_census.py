"""TH19 re-count of TH09's census (§7.2): necklaces N in {1,2}^k, k odd, sum(N) not 0 mod 3, up to
rotation / reversal / complement; W_N = <s,t | s^2, t^3, prod s t^{e_i}> trivial?  Coset enumeration over <s>
with the repository's Todd-Coxeter (research-f, experiments/f_descent.coset_index); W_N perfect, so index 1 over <s>
means W_N = 1.  The enumeration of classes is my own."""
import sys, itertools
sys.path.insert(0, "experiments")
import f_descent as F
def classes(k):
    seen, reps = set(), []
    for N in itertools.product((1, 2), repeat=k):
        if N in seen: continue
        orbit = set()
        for M in (N, N[::-1]):
            for C in (M, tuple(3 - e for e in M)):
                for i in range(k): orbit.add(C[i:] + C[:i])
        seen |= orbit
        reps.append(min(orbit))
    return reps
for k in (1, 3, 5, 7, 9):
    perfect = [N for N in classes(k) if sum(N) % 3 != 0]
    kill, non = [], []
    for N in perfect:
        w = []
        for e in N: w += [1] + [2]*e
        idx = F.coset_index([(1, 1), (2, 2, 2), tuple(w)], (1,), 200000)
        (kill if idx == 1 else non).append(("".join(map(str, N)), idx))
    print(f"k={k}: perfect classes {len(perfect)}; killers {len(kill)}: {[n for n, _ in kill]}; non-killers: {non}")
