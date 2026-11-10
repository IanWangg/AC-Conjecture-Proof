# Research R6-2: the holdout P2 has no one-move exit at its Gieseking node (O's exact method)

Date: 2026-11-10. Agent R6-2 (round 6). Short, time-boxed note.

**Status:** partial, exact. **No AC trivialization of P2, no proof that P2 is non-trivial, nothing on the full conjecture.** The results below are about *single ACM moves* (one relator held fixed, the other replaced by any conjugate of itself or its inverse in the group of the fixed relator). They rule out one route only. A one-move non-existence result is **not** an obstruction to AC-triviality.

| # | statement | label |
|---|---|---|
| R1 | P2 = (XyyxYYY, XXXYxxY) ~AC (r₄, w₀) = (XyyyyxYYYYY, xxyyXY) | proved here by certificate `certificates/r62_p2_to_r4_w0.json` (762 strict moves, peak 37, verified) |
| R2 | α = (x ↦ xy, y ↦ Y) is an involution of F₂ with α(c) = w₀, c = xyxYYXy. Applying α to the pair gives α(r₄, w₀) = (α(r₄), c), where α(r₄) = YXYYYYxyyyyyy. In G_c this is the degree-1 element (u, 1) with u = aababaabaab (a = x, b = yxY) | proved here (exact word identities, normal form by `o_gc.nf` and `th03_uniform.nf`, which agree) |
| **R3** | **α(r₄) is not conjugate in G_c to any xˢy (s ∈ ℤ).** Two independent exact proofs: I(u) = 44 ∉ σ(ℤ) = {2, 8, 26, 74, 218, …}, and L4(u) = 9 ∉ {C(s+1,4)} = {0, 1, 5, 15, 35, …} | proved here (TH03's invariants I, L4; exact integer computation plus a monotonicity lemma, §3) |
| **R4** | **No presentation with a primitive relator is one ACM move from (r₄, w₀) ~AC P2, whichever relator is held fixed, with arbitrary conjugators.** The same holds for every automorphic image of the pair, e.g. (α(r₄), c). This answers TH18 T10's open question ("whether P2 has a one-move exit there is open") negatively | proved here (R3 + O2's argument) for w₀ fixed; for r₄ fixed: TH18 T3 (t-length of w₀ in BS(4,5) is 3), cited |
| R5 | The same family: for every m with 4 ≤ m ≤ 30, I(α(r_m)) ∉ σ(ℤ), where r_m = x⁻¹yᵐxy^{−(m+1)}. So no w₀-fixed one-move exit from (r_m, w₀) (~AC AK₂(m) by TH18 T9/T10). Controls: m = 2, 3 give I = 8 = σ(3), with ε and L4 also matching s = 3, which is consistent with TH18's exits for r₂ and r₃ | proved here for each m separately (exact); a proof uniform in m is **open** |
| R6 | At the node (c, α(r₄)), no c-fixed move produces an automorphic image of the BS(1,2) relator z(k, e, δ) with \|k\| ≤ 25 (§5) | bounded experiment (exact for each k) |

## 1. Method

- research-o (O1, O2): G_c = ⟨x,y | c⟩ ≅ F(a,b) ⋊_φ ℤ with a = x, b = yxY, φ(a) = b, φ(b) = b⁻¹a, and the ℤ-coordinate is the y-exponent sum. A degree-1 element (u,1) is conjugate to xˢy = (aˢ,1) exactly when aˢ lies in the φ-twisted class of u. A ℤ-valued homomorphism G_c → ℤ (y-exponent) is a conjugacy invariant. A primitive element of F₂ with y-exponent ±1 is conjugate in F₂ to (xˢy)^{±1} for some s (Osborne–Zieschang). So a c-fixed ACM move from (c, w), deg w = ±1, reaches a primitive relator exactly when w^{±1} ~ xˢy in G_c for some s. This is O's Proposition O2; the proof there does not use the particular form of k_n.
- research-th03: the integer holonomy invariant I(u) = tr(N·conj(N)), N = ρ(u)Y (T1, T2), the degree-4 twisted trace L4 with L4(xˢy) = C(s+1,4) (T13), and the mod-2 mirror invariant ε (T16). Tools: `th03_uniform.I`, `th03_uniform.sigma`, `th03_two.eps`, `th03_two.l4_setup`.
- research-th18 T10 identifies P2 with a killer of ⟨x,y | w₀⟩ ≅ G_c. TH18 searched 300,000 twisted conjugates without finding a power of a, and could not prove that none exists. R3 replaces that bounded search with an exact invariant computation.

## 2. Step 1: the pair (c, w) with deg w = 1 (R1, R2)

1. `certificates/d_ms2b_to_ms0722.json` (research-d) takes P2 to (YYYYYXyyyyx, YYXyXyx).
2. Single-letter conjugations rotate the first relator to r₄ = XyyyyxYYYYY.
3. YYXyXyx⁻¹ is conjugate to w₀ = xxyyXY in BS(4,5) = ⟨x,y | r₄⟩. `th18_bs.bs_path` gives the exact path and `th18_bs.compile_path` compiles it into strict moves.

The script `experiments/r62_cert.py` performs these three steps and writes the certificate. The verifier reports:

```
{"endpoint": ["XyyyyxYYYYY", "xxyyXY"], "moves": 762, "path": "certificates/r62_p2_to_r4_w0.json", "peak_total_length": 37}
```

TH18 T10's identity checks out: α(c) = w₀, and α∘α = id. Applying α to the whole pair gives (α(r₄), α(w₀)) = (YXYYYYxyyyyyy, xyxYYXy). Two facts make this pair as good as P2 for our purposes:

- Lemma D2 (research-d): applying an automorphism letterwise to an AC sequence gives another AC sequence. So (α(r₄), c) is AC-trivial iff (r₄, w₀) is, iff P2 is.
- research-i item 6: Aut(F₂) is AC-realized on P2's class. So (α(r₄), c) is in fact in P2's AC class itself. I cite this and did not compose that certificate.

Cyclically reduced, α(r₄) = x⁻¹y⁻⁴xy⁵ (conjugate to r₄⁻¹ in F₂). Its normal form in G_c is (aababaabaab, 1), so its degree is +1.

## 3. Step 2: the decision (R3)

`experiments/r62_p2.py` output (exact):

```
alpha(r4) = YXYYYYxyyyyyy  nf = ('aababaabaab', 1)  o_gc.nf agrees: ('aababaabaab', 1)
I(u) = 44  eps(u) = 1
s in [-80,80] with sigma(s) = I(u): []
sigma(-10..11): [50258, 16946, 5714, 1928, 650, 218, 74, 26, 8, 2, 2, 2, 2, 8, 26, 74, 218, 650, 1928, 5714, 16946, 50258]
L4(u) = 9
```

**Lemma (monotonicity).** σ(s) := I(xˢy) satisfies the recurrence u(n+4) = 3u(n+3) − u(n+2) + 3u(n+1) − u(n) for all n ∈ ℤ (TH03 T3; it comes from the matrix powers Aˢ, so it holds for negative s too) and σ(s) = σ(1−s) (TH03).

*Proof that σ grows for s ≥ 3.* Suppose 0 < u(n), u(n+1) ≥ 2u(n), u(n+2) ≥ 2u(n+1) and u(n+3) ≥ 2u(n+2). Then
u(n+4) − 2u(n+3) = (u(n+3) − u(n+2)) + (3u(n+1) − u(n)) > 0.
The base case n = 3 holds: σ(3..6) = 8, 26, 74, 218. By induction σ(s+1) > 2σ(s) for all s ≥ 3. ∎

Hence σ(s) ≥ 74 for s ≥ 5. The values σ(−3..4) are 26, 8, 2, 2, 2, 2, 8, 26. Mirror symmetry σ(s) = σ(1−s) covers s ≤ −4. So 44 ∉ σ(ℤ). Because I is a conjugacy invariant of degree-1 elements (TH03 T2), α(r₄) ≁ xˢy for every s.

**Second proof.** L4 is a conjugacy invariant (TH03 T13) with L4(aˢ) = C(s+1,4). The computed values for s = −6..7 are 70, 35, 15, 5, 1, 0, 0, 0, 0, 1, 5, 15, 35, 70, and every value has the form C(k,4). L4(u) = 9 is not a binomial coefficient C(k,4).

ε(u) = 1 does not separate on its own; ε(aˢ) = 1 for s ≡ 1, 2 (mod 4).

**R4.** This is R3 plus O2's argument from §1. It is invariant under automorphisms because primitives map to primitives and conjugacy is preserved under the induced isomorphism. So no w₀-fixed ACM move from (r₄, w₀) reaches a primitive relator.

For the other side, r₄ fixed: `th18_bs.tlen('xxyyXY', 4) = 3`, and its class label is (3, (−1,1,1), (3,0,2)). By TH18 T3, a killer class of BS(n,n+1) contains a primitive element iff its t-length is 1. Hence no r₄-fixed one-move exit exists either.

Since R3 found no s, I did not run o_gc's BFS and compiled no trivialization.

## 4. The family r_m (R5)

For each m I computed I(α(r_m)) for the degree-1 normal form u_m. The length |u_m| = 1, 3, 6, 11, 19, 32, 53, … grows like the Fibonacci numbers.

| m | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 12 | 20 | 30 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| I(u_m) | 2 | 8 | 8 | **44** | 50 | 152 | 182 | 398 | 482 | 872 | 1688 | 11492 | 55112 |
| σ-match | s ∈ {−1,0,1,2} | {−2,3} | {−2,3} | none | none | none | none | none | none | none | none | none | none |

There is no match for any 4 ≤ m ≤ 30; each m was checked against σ(0..199), which is enough by the Lemma. For m = 2, 3, ε = 0 and L4 = 1 select s = 3, and the method does find the exits there. `o_cert.twisted_path` returns the conjugators x (m = 2) and yX (m = 3), and I checked `o_gc.nf(g·α(r_m)·g⁻¹) = nf(xxxy) = (aaa, 1)` exactly. So α(r₂) ~ α(r₃) ~ x³y in G_c, consistent with TH18. As expected from R3, the same BFS from u₄ = aababaabaab (L = 14, 300,000 nodes) finds nothing.

The values of I(u_m) grow polynomially (about cubically), while σ grows like 2.96ˢ. A closed form for I(u_m) would probably give a proof for all m, but that is not done here.

## 5. Step 3 (partial): the BS(1,2) exit at the same node, and P2's own tuple

**BS(1,2) exit, c fixed (bounded experiment).** The question is whether one c-fixed ACM move from (c, α(r₄)) can produce an automorphic image of the BS(1,2) relator yxYXX. That pair would then be a killer pair of BS(1,2), which is AC-trivial (TH18 remark n = 1, TH09).

Such an image is β(y)β(x)β(y)⁻¹β(x)⁻² with p = β(x) and q = β(y). Its G_c-degree is −deg p, so we need deg p = ±1. Then p is F₂-conjugate to (xᵏy)^δ, and every basis containing p is (p, pʲx^{±1}pˡ). So, up to conjugacy and inversion, the candidates are exactly

z(k, e, δ) = xᵉ p x⁻ᵉ p⁻², with p = (xᵏy)^δ, e, δ ∈ {±1}, k ∈ ℤ

(proved here; it uses only the standard description of bases of F₂).

`experiments/r62_bs12.py 25` computes I for |k| ≤ 25:
- for |k| ≤ 3 the values are {2, 8, 20, 26, 50, 68, 152};
- for 4 ≤ |k| ≤ 25 every value is ≥ 68;
- no candidate has I = 44 = I(α(r₄)).

So **no BS(1,2) exit with |k| ≤ 25** exists at this node. This is bounded in k. I(z(k,…)) is an exponential polynomial in k, so it can be completed into a proof, but I have not done that.

**P2's own tuple (r₂, k₂) = (XyyxYYY, XXXYxxY).**
- r₂ fixed: k₂ has x-exponent −1 and t-length 5 in BS(2,3) (`th18_bs.tlen`). So TH18 T3 excludes a one-move exit.
- k₂ fixed: `experiments/r62_node2.py` runs a BFS over the Aut(F₂)-orbit of k₂ (cyclic words of length ≤ 13, elementary Nielsen moves). It finds 58 cyclic words, all of length ≥ 7, and does not reach c or w₀. The cap 13 covers every rank-2 Whitehead automorphism applied to a word of length ≤ 7, so by Whitehead's peak reduction the minimal length in k₂'s Aut-orbit is 7. The orbit of c contains w₀, of length 6, so **k₂ is not automorphic to c^{±1}**. Control: the same BFS finds α from c to w₀.
  This means O's coordinates do not apply to this side. Whether ⟨x,y | k₂⟩ ≅ G_c by some non-automorphic isomorphism, and whether this side has a one-move exit, are not decided here.

## 6. Honest limits

- This is a one-move result at one node of P2's class. It says nothing about two or more moves, other nodes, or AC-triviality.
- The r₄-fixed half rests on TH18 T3, which I did not re-derive.
- That (α(r₄), c) lies in P2's own class rests on research-i item 6, which is cited and not re-certified here. The AC-equivalence (r₄, w₀) ~ P2 is certified.
- Step 3 is only bounded (|k| ≤ 25, §5). P1 was not attempted.

## 7. Commands and files

```
PYTHONDONTWRITEBYTECODE=1 python3 experiments/r62_p2.py                 # R2, R3 (< 1 s)
PYTHONDONTWRITEBYTECODE=1 python3 experiments/r62_cert.py certificates  # R1 certificate
python3 experiments/elementary_verify.py certificates/r62_p2_to_r4_w0.json
PYTHONDONTWRITEBYTECODE=1 python3 experiments/r62_bs12.py 25            # §5 BS(1,2) census (~1 s)
PYTHONDONTWRITEBYTECODE=1 python3 experiments/r62_node2.py              # §5 Aut-orbit BFS of k2 (~10 s)
```

Files:
- `experiments/r62_p2.py`
- `experiments/r62_cert.py`
- `experiments/r62_bs12.py`
- `experiments/r62_node2.py`
- `certificates/r62_p2_to_r4_w0.json`

The R5 table came from an inline loop over m that used `r62_p2.aut`, `th03_uniform.nf` and `th03_uniform.I`. It was stopped after m = 30 because the words grow like the Fibonacci numbers.

## Coordinator's check (2026-11-09, Los Angeles time)

- `certificates/r62_p2_to_r4_w0.json` replays under `python3 experiments/elementary_verify.py`: from exactly P2 = (XyyxYYY, XXXYxxY) to (XyyyyxYYYYY, xxyyXY) in 762 moves, peak 37.
- Independently checked by the coordinator: α = (x ↦ xy, y ↦ Y) is an involution; α(xxyyXY) = xyxYYXy = c exactly; α(XyyyyxYYYYY) = YXYYYYxyyyyyy, whose normal form in research-o's coordinates is (aababaabaab, 1) (`o_gc.nf`). With the coordinator's own exact holonomy code (written before this round for a different purpose, ℚ(ω) arithmetic) the invariant of its square is 1936 = 44², whereas the values for (xˢy)² are 4, 64, 676, 5476, 47524, 422500 for |s| ≤ 7 and grow with |s|; so I(u) = 44 is not of the form I(xˢy) in that range. The statement for all s rests on the note's monotonicity lemma from research-th03's recurrence and, independently, on the degree-4 trace L4(u) = 9 ≠ C(s+1,4); the coordinator checked neither line by line.
- Conclusion, stated precisely: at this representative of P2's class, no generalized move with c (after α) frozen reaches a primitive relator; with r₄ frozen the same follows from research-th18's T3 (t-length 3), cited. This is a one-move statement, not an obstruction; P2's AC-triviality remains open.
