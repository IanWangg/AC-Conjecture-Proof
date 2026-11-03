# Research K: a uniform one-parameter normal form for the Akbulut–Kirby series, the killer dictionary, and two closed programs

Date: 2026-11-02 (finished 2026-11-03 UTC). Independent research agent K (round 3, Fable cohort; theory emphasis).

**Status:** partial, fully verified results. **No AK(3) trivialization, no proof of non-triviality, no counterexample, nothing on the full conjecture.**

*Proved here* (complete symbolic proof + replayable `ordinary-ac-elementary-v1` certificates): for every n ≥ 2,

    AK(n) = (xyxYXY, xⁿY^(n+1))   ~AC   P_n := (xyxYYXy, xⁿ·YXyy),

by 4n−1 cyclic products (packaged peak cyclic length 4n+5 for n ≥ 3). Consequences: |P_n| = n+11 < 2n+7 = |AK(n)| exactly when n ≥ 5, so every AK(n), n ≥ 5, is AC-equivalent to a strictly shorter presentation, with explicit uniform certificates; the entire AK series is the family of *killers* k_n = xⁿ·u (u = YXyy) of one fixed one-relator group G_c = ⟨x,y | c⟩, c = xyxYYXy; and AK(3) ~AC P_3 = (xyxYYXy, xxxYXyy), a length-14 presentation whose two one-relator groups both have asymmetric Alexander polynomial (so AK(3)'s class contains "BS-type" members, uniformly in n). *Externally reported*: Shehper et al. (arXiv:2408.15332, NeurIPS 2025) state that for each n, AK(n) is AC-equivalent to a one-parameter family and that "all but two" AK(n) are length-reducible; their ledgers were not available here, so P_n may coincide with their family — novelty is **not** established. *Proved here, elementary*: (i) no "monotone defect" quantity can obstruct AK(3) (any quantity monotone along a complete move class is an AC invariant, and must agree on AK(2) and (x,y)); (ii) E's "uniform correction-cost" program is equivalent to the problem itself, with a trivial logarithmic lower bound ⌊log₂((c+1)/4)⌋+1 on clearing any degree-c Lie error.

## 1. Previous work read and choice of direction

Read in full: `README.md`, `research/research-{a,b,c,d,e,f}.md`; `experiments/elementary_verify.py`; replayed the controls `e_ak1_trivialization.json` (12 moves, peak 10), `e_ak2_peak13_trivialization.json` (28, 13), `ms3_to_ak3_exact.json` (32, 23). Skimmed all of `experiments/` and `certificates/`, and the in-progress round-3 notes G (exact torus-type ACM graph; Euclid for meridional partners), H (quotient-obstruction structure; fibre-product invariants), I (Farey-vertex torus pairs; P1 ~ C6), J (audit; Theorem J1: first plateau exit at cyclic length ≥ 15) — read-only, to avoid duplication. Agent L works on constructive computation in parallel.

**Network.** arxiv.org, ar5iv, papers.nips.cc, openreview.net and cambridge.org all fail DNS in this session; literature facts below are from search-engine snippets only and are labelled *externally reported*.

**Why this direction.** A–F and G–J treat AK(3) as an isolated object (searches from it; plateau theorems; torus-knot structure of its two specific relators; quotient no-go theorems). Nobody had asked the *family* question in a provable form: what is the AC class of AK(n) as a function of n? C proved MS(n, y⁻¹x²y⁻¹) ~ AK(n) but that family has the same length growth 2n+8. Shehper et al. reported (externally; no public ledger) that AK(n) is AC-equivalent to a one-parameter family and is length-reducible for all but two n. A verified, uniform, *symbolic* version of this — in C's style — is a theorem, not a search result, and it changes the coordinates in which AK(3) is written. I also close two of the suggested theory angles (E's correction-cost program; monotone defect quantities) with short proofs, so that nobody spends more time on them.

## 2. Notation

X = x⁻¹, Y = y⁻¹. Words are exact free words; `cyc(w)` is the cyclically reduced form; "rotation" means cyclic rotation. b = xyxYXY, p_n = xⁿY^(n+1), AK(n) = (b, p_n) (relator order is immaterial: swap is an AC composite, research-d Lemma D1). A **cyclic product** replaces one relator r by cyc(g·r) where g is a rotation of the other relator or of its inverse; it is a composite of ordinary AC moves (a rotation of r is a conjugation; left multiplication by g is right multiplication followed by a conjugation; cyclic reduction is conjugation), so every statement "~" below is ordinary AC equivalence with no stabilization, no automorphism and no quotient.

## 3. Theorem K1: AK(n) ~AC P_n for all n ≥ 2 (proved here)

Define, for n ≥ 2, the exact words

| name | word | length | range |
|---|---|---:|---|
| u_k | x^(n−1) Y^(n+1−k) x y X^k Y | 2n+3 | 1 ≤ k ≤ n+1 |
| v_n | x^(n−1) y X^(n−1) y X Y | 2n+2 | |
| w_n | xⁿ y X^(n+1) Y (= u_(n+1)) | 2n+3 | |
| a_m | x^m y X Y X y | m+5 | 1 ≤ m ≤ n |
| b_m | xⁿ Y X y X^(n−m) y | 2n+4−m | 1 ≤ m ≤ n−1 |
| c_m | x^(n−1) y X^(n−m) y X Y (c_1 = v_n) | 2n+3−m | 1 ≤ m ≤ n−1 |
| d_n | xⁿ Y X y y | n+4 | |
| c | x y x Y Y X y | 7 | |

and the fixed multipliers (each a rotation of the relator that is frozen at the time it is used)

    ρ = y X Y x^(n−1) y X^(n−1)          rotation of v_n
    σ⁻¹ = X y x^(n+1) Y X^(n−1)          rotation of w_n
    τ_m⁻¹ = X^(n−m) y x^(n+1) Y X^m      rotation of w_n
    κ⁻¹ = X Y xⁿ y Xⁿ                    rotation of w_n⁻¹
    w' = y x^(n+1) Y Xⁿ                  rotation of w_n.

**Theorem K1.** For every n ≥ 2 the following 4n−1 cyclic products take AK(n) = (b, p_n) to P_n = (c, d_n) = (xyxYYXy, xⁿYXyy):

- **A1.** (b, p_n) → (u_1, p_n), u_1 = cyc(p_n · b⁻¹); then (u_1, p_n) → (u_1, v_n), v_n = cyc(s⁻¹ · p_n⁻¹) with s = yⁿX^(n−1)yxYX a rotation of u_1 (inverting p_n first is an AC move).
- **A2.** (u_k, v_n) → (u_(k+1), v_n), u_(k+1) = cyc(ρ · u_k), for k = 1, …, n. Afterwards the pair is (w_n, v_n) = (w_n, c_1).
- **B.** With w_n frozen: c_1 → a_2 by a_2 = cyc(σ⁻¹ · c_1); then for m = 2, …, n−1: a_m → b_m = cyc(τ_m⁻¹ · a_m), b_m → c_m = cyc(κ⁻¹ · b_m), c_m → a_(m+1) = cyc(σ⁻¹ · c_m). Afterwards the pair is (w_n, a_n).
- **C.** (w_n, a_n) → (d_n, a_n), d_n = cyc(a_n · w'); then (d_n, a_n) → (d_n, c), c = cyc(d_n · a_n⁻¹).

The packaged peak cyclic total length is 4n+5 for n ≥ 3 (attained at every state (u_k, v_n)) and 14 for n = 2.

*Proof.* Each step is a free-reduction identity valid for all n in the stated range; the cancellations are displayed so that uniformity in n is visible. All equalities are as cyclic words (a rotation is an AC move).

A1. p_n b⁻¹ = xⁿY^(n+1)·yxyXYX = xⁿYⁿxyXYX; cyclic reduction cancels the outer x…X, leaving x^(n−1)YⁿxyXY = u_1. Next, u_1⁻¹ = yxYXyⁿX^(n−1), so s = yⁿX^(n−1)yxYX is a rotation of u_1⁻¹ and s⁻¹ = xyXYx^(n−1)Yⁿ is a rotation of u_1. Then s⁻¹·p_n⁻¹ = xyXYx^(n−1)Yⁿ·y^(n+1)Xⁿ = xyXYx^(n−1)yXⁿ; cyclic reduction cancels x…X once: yXYx^(n−1)yX^(n−1), whose rotation x^(n−1)yX^(n−1)yXY is v_n. (The engine's representative, x^(n−1)YX^(n−1)yxY, is its inverse rotated; both are the same Σ-class.)

A2. ρ·u_k = yXYx^(n−1)yX^(n−1)·x^(n−1)Y^(n+1−k)xyX^kY = yXYx^(n−1)Y^(n−k)xyX^kY (the block yX^(n−1)x^(n−1)Y^(n+1−k) collapses to Y^(n−k); for k = n it is empty). Cyclic reduction cancels the outer y…Y: XYx^(n−1)Y^(n−k)xyX^k, and rotating gives x^(n−1)Y^(n−k)xyX^(k+1)Y = u_(k+1). For k = n: XYxⁿyXⁿ → xⁿyX^(n+1)Y = w_n.

B, first step and c_m → a_(m+1) (m ≥ 1, c_1 = v_n): σ⁻¹·c_m = Xyx^(n+1)YX^(n−1)·x^(n−1)yX^(n−m)yXY = Xyx^(n+1)X^(n−m)yXY = Xyx^(m+1)yXY, cyclically reduced (X…Y), and its rotation x^(m+1)yXYXy = a_(m+1). ✓ for 1 ≤ m ≤ n−1.

a_m → b_m: τ_m⁻¹·a_m = X^(n−m)yx^(n+1)YX^m·x^myXYXy = X^(n−m)yx^(n+1)YyXYXy = X^(n−m)yxⁿYXy, cyclically reduced; rotation xⁿYXyX^(n−m)y = b_m. ✓

b_m → c_m: κ⁻¹·b_m = XYxⁿyXⁿ·xⁿYXyX^(n−m)y = XYxⁿyYXyX^(n−m)y = XYx^(n−1)yX^(n−m)y, cyclically reduced; rotation x^(n−1)yX^(n−m)yXY = c_m. ✓

C. a_n·w' = xⁿyXYXy·yx^(n+1)YXⁿ. Cyclic reduction: the outer xⁿ…Xⁿ cancel (n letters), leaving yXYXy²x^(n+1)Y; then y…Y cancel, leaving XYXy²x^(n+1); then X…x cancel, leaving YXy²xⁿ; rotation xⁿYXyy = d_n. ✓ Finally d_n·a_n⁻¹ = xⁿYXyy·YxyxYXⁿ = xⁿYXyxyxYXⁿ; the outer xⁿ…Xⁿ cancel, leaving YXyxyxY (cyclically reduced: Y…Y), whose rotation is xyxYYXy = c. ✓

Counting: A has 2+n steps, B has 1+3(n−2), C has 2: total 4n−1. Lengths: |u_k|+|v_n| = 4n+5; |u_1|+|p_n| = 4n+4; |w_n|+|a_m| = 3n+8−(n−m) ≤ 3n+8 ≤ 4n+5 iff n ≥ 3; |w_n|+|b_m| = 4n+7−m ≤ 4n+5 for m ≥ 2; |w_n|+|c_m| ≤ 4n+4; phase C ≤ 3n+8. ∎

Every multiplier is a rotation of the frozen relator (or its inverse), so each step is a composite of ordinary AC moves; `experiments/k_ak_family.py` checks exactly this (that the multiplier is a rotation of the frozen relator and that the displayed identity holds) for n = 2, …, 200, then compiles the path to strict elementary moves with D's `d_certify.py` and replays it with `elementary_verify.py`.

**Machine checks (experiment).** `python3 experiments/k_ak_family.py --check 2 200` passes. `--batch 2 30` replays elementary certificates for n = 2..30 (67 moves/peak 29 for n = 2; 88/35 for n = 3; 136/39 for n = 5; 271/67 for n = 10; 1061/187 for n = 30). Stored: `certificates/k_ak{3,7,10}_to_p{3,7,10}_uniform.json` (closed-form path) and `certificates/k_ak{3,4,5,6}_to_p{3,4,5,6}.json` (compiled from the engine paths of §5.2; 68/91/114/138 moves, peaks 25/31/37/43). All seven pass `python3 experiments/elementary_verify.py`.

### 3.1 Corollaries (proved here)

**K1.1 (length reduction of the AK series).** |P_n| = n+11, |AK(n)| = 2n+7. Hence for every n ≥ 5, AK(n) is AC-equivalent to a presentation shorter by n−4 letters, with an explicit certificate of 4n−1 cyclic products; for n = 4 the equivalent P_4 has the same length 15; for n = 3 the equivalent P_3 has length 14. This is the uniform, certified version of Shehper et al.'s externally reported "length reducibility of all but two presentations in the Akbulut–Kirby series". Their one-parameter family is not available to me; P_n may well be it, or Aut-equivalent to it.

**K1.2 (one fixed group, a sequence of killers).** All AK(n), n ≥ 2, are AC-equivalent to (c, k_n) with the *same* first relator c = xyxYYXy and k_n = xⁿu, u = YXyy, so k_(n+1) = x·k_n. Thus the AK series is the sequence of killers (normal generators) k_n of the single one-relator group G_c = ⟨x, y | xyxy⁻²x⁻¹y⟩. AK(1) and AK(2) are AC-trivial (certificates E), so (c, k_1) (length 12, in any case AC-trivial by Miasnikov–Myasnikov) and (c, k_2) are AC-trivial; AK(3) is AC-trivial iff (c, k_3) = (xyxYYXy, xxxYXyy) is.

**K1.3 (invariants of the new coordinates; computed with F's tools).** Fox calculus: Δ_{G_c}(t) ≐ t² + t − 1 and Δ_{⟨x,y|k_n⟩}(t) ≐ tⁿ + t − 1, both asymmetric for every n ≥ 1, so P_n is "Alexander-asymmetric / BS-type" in F's classification and is not thickenable for any n (checked directly with `f_thicken` for n ≤ 8). F had observed on one example that the obstruction *type* (torus-knot pair vs BS-type) is not an AC invariant; K1 makes this uniform: every torus-knot pair AK(n) is AC-equivalent to a BS-type pair. In particular no argument that works only for torus-knot-pair words (or only for BS-type words) can be an AC obstruction. Whitehead-canonical Aut(F₂)-orbit of P_n (D's `d_whitehead.py`): (XⁿYYxy, XYXYxyy) for n ≥ 3, i.e. AK(n) ~AC (x⁻ⁿy⁻²xy, (xyxy)⁻¹xy²) up to Aut(F₂) (and Aut-images are AC-realized, research-d Lemma D6); P_3's orbit is distinct from D's second length-13 orbit Q.

**K1.4 (consistency with earlier bounds).** P_3 enters AK(3)'s cyclic-product forward set at barrier 17 (it is one of D's 12 energy-14 states of barrier 17), and A's plateau/J1 are respected: the first increasing step of the K1 path lands at cyclic length 4n+4 = 16 for n = 3.

## 4. The killer / pseudo-meridian dictionary (externally reported facts + proved remarks)

*Externally reported* (Silver–Whitten–Williams, "Knot groups with many killers", Bull. Aust. Math. Soc. 81 (2010); arXiv:0909.3275; Tsau 1988): a **killer** of a knot group is an element whose normal closure is the whole group; a killer that is not an automorphic image of a meridian is a **pseudo-meridian**; nontrivial torus-knot groups have infinitely many pairwise inequivalent killers; for torus knots Out(G) has order two (generated by the inversion of both standard generators).

*Proved here (one line from research-f Prop. F3).* The braid relator b is a pseudo-meridian of the T(n,n+1) group ⟨x,y | xⁿ=y^(n+1)⟩ for every n ≥ 2: its image in C_n * C_(n+1) has cyclic syllable length 6 while every meridian has 2, and Out of order two (inversion of both generators) preserves syllable length. Symmetrically p_n is a pseudo-meridian of the trefoil group B₃ = ⟨x,y | b⟩ for n ≥ 1 (syllable length 4n+2 in C₂*C₃, research-a Lemma 1). So AK(n) is, in two ways, a (torus knot group, pseudo-meridian) pair; thickenable pairs are exactly (knot group, meridian) pairs (F, Lemma 3.1/F3); and K1.2 adds a third description, (G_c, killer xⁿu), with G_c not a 3-manifold group at all.

*Experiment (knot-theoretic profile of the AK(2) trivialization; `scratchpad/agent-k/profile_cert.py`, using F's modules read-only).* Along E's 28-move certificate: moves 0–3 keep both relators T(2,3)-type (torus-knot pair, partner syllable lengths 6/10, non-thickenable); at move 4 one one-relator group becomes Alexander-asymmetric (Δ = 2t−1, a BS(1,2)-type word); moves 9–12 have both relators asymmetric; at move 13 one Δ becomes 1; the pair becomes thickenable only at move 17, when a relator becomes the primitive word xY. So the only known AK trivialization repairs the "meridian defect" not inside the torus-knot world but by leaving it through BS-type states and landing on a primitive relator. This is consistent with K1.3 and is a hint for G's/F's meridian-guided searches: the thickenable locus was entered via a primitive relator, not via a meridional torus pair.

## 5. Experiments (exact commands; outputs from this session; one core, < 1 GB each)

### 5.1 Shortening probes of the AK series with D's engine (forward-reachable sets in the cyclic-product graph; J's caveat applies: these are forward sets, not components)

```
g++ -O2 -std=c++17 -o d_acsearch experiments/d_acsearch.cpp
./d_acsearch --cap 27 --maxstates 30000000 --source xxxxYYYYY,xyxYXY --no-stop --dump 14 ak4_short27.txt   # 8,174,660 states, 117 s
./d_acsearch --cap 29 --maxstates 30000000 --source xxxxxYYYYYY,xyxYXY --no-stop --dump 16 ak5_short29.txt # 14,401,328 states, 165 s
```
AK(4): no state of total length ≤ 14 up to barrier 27 (energy-15 states: 36). AK(5): **24 states of total length 16** (none shorter) up to barrier 29 — 12 at barrier 25, 12 at barrier 28 — forming exactly three Aut(F₂)-orbits (`d_whitehead.py`): (X⁵YYxy, XYXYxyy) = P_5's orbit, (X⁴YxyxY, XYYxyXy) and (X⁴YxYxy, XYXyyxY). The latter two suggest two further one-parameter normal forms for the AK series; not pursued here.

### 5.2 Targeted runs AK(n) → P_n (exact Σ-targets)
```
printf 'P3 xyxYYXy xxxYXyy\n' > p3.tgt   # similarly p2, p4, p5, p6
./d_acsearch --cap 19 --maxstates 20000000 --source xxYYY,xyxYXY --exact-targets p2.tgt --maxhits 3 --no-stop        # HIT barrier 13
./d_acsearch --cap 21 ... --source xxxYYYY,xyxYXY --exact-targets p3.tgt ...                                            # HIT barrier 17 (143,988 states)
./d_acsearch --cap 23 ... --source xxxxYYYYY,xyxYXY --exact-targets p4.tgt ...                                          # HIT barrier 21 (57,024 states)
./d_acsearch --cap 25 ... --source xxxxxYYYYYY,xyxYXY --exact-targets p5.tgt ...                                        # HIT barrier 25 (67,114 states)
./d_acsearch --cap 29 ... --source xxxxxxYYYYYYY,xyxYXY --exact-targets p6.tgt ...                                      # HIT barrier 29 (881,782 states)
```
Barriers 13, 17, 21, 25, 29 = 4n+5 (n = 2: the engine found a barrier-13 path, better than the K1 path's 14). The engine's PATH lines (4n−1 cyclic steps for n = 3..6) were decoded step by step (`scratchpad/agent-k/movefind.py`: for each step, which relator changed and which rotation/sign of the frozen relator multiplies it); the closed forms of §3 are the general-n reading of those decodings, then proved by hand. (`--cap` is limited to 31 by the engine's packing, so n = 7 was certified only by the closed form.)

### 5.3 Closed-form verification and certificates
```
python3 experiments/k_ak_family.py --check 2 200      # closed-form path verified for n = 2..200
python3 experiments/k_ak_family.py --batch 2 30       # elementary certificates n=2..30 replayed
python3 experiments/k_ak_family.py --cert 3 certificates/k_ak3_to_p3_uniform.json   # 88 moves, peak 35
python3 experiments/elementary_verify.py certificates/k_*.json                      # 7 files, exit 0
```

## 6. Two suggested programs, closed (proved here, elementary)

**Proposition K2 (no monotone word-level obstruction).** Let M be any set of moves that generates AC equivalence (e.g. the 15 instructions of E, or all elementary moves, or all cyclic products together with their reversals). If a function δ on presentations satisfies δ(sU) ≥ δ(U) for every s ∈ M and every U, then δ is constant on AC classes. *Proof.* If V ~AC U then V is reached from U by a finite M-sequence, so δ(V) ≥ δ(U); by symmetry of ~AC also δ(U) ≥ δ(V). ∎ Consequently a "non-decreasing" quantity must agree on AK(2) and (x,y). F's meridian defect is 6 on AK(2) and is undefined (no torus-type relator) on (x,y) and on every presentation with a primitive relator, and §4 shows the only known AK(2) trivialization abandons torus-type relators at move 4. So no monotonicity theorem for the meridian defect, or for any other quantity differing between AK(2) and (x,y), can exist, on any complete move class. The brief's angle (iii) in that form is closed; what remains meaningful is the *question* (F's #9) whether some complete AC-invariant exists, which is the original problem.

**Proposition K3 (uniform correction cost is logarithmic and tautological).** Notation of research-e: N_c = F/γ_(c+1), d_{N_c} the 15-instruction distance. For c ≥ 2 let
m_c = min { d_{N_c}((x e₀, y e₁), (x, y)) : e₀, e₁ ∈ γ_c, (e₀, e₁) ∉ γ_(c+1)² }
be the least number of instructions that clears some nonzero degree-c Lie error. Then (a) m_c ≥ ⌊log₂((c+1)/4)⌋ + 1 → ∞; (b) for every pair U of total length ℓ and every c, d_{N_c}(U) ≤ d_F(U), and the family f_c := d_{N_c}(·, (x,y)) is 1-Lipschitz for every c with f_c(AK3) − f_c(x,y) = d_{N_c}(AK3) → ∞ iff AK(3) is not AC-trivial. *Proof.* (a) An instruction sequence of length L from (x,y) produces words of total length ≤ 2^L·4 − 2 (research-e, proof of Theorem 3); if it ends at (x e₀, y e₁) with (e₀,e₁) ≠ (1,1) in F then by E's Lemma 2 the nontrivial e_i survives in N_c for c ≥ |e_i|, and |e_i| ≤ 2^L·4 − 1; so for c ≥ 2^L·4 − 1 every instruction sequence of length ≤ L from (x,y) whose endpoint is ≡ (x,y) mod γ_(c+1) ends at (x,y) exactly; reading the sequence backwards, no pair (x e₀, y e₁) with a nonzero error of degree exactly c is within L instructions of (x,y) in N_c. Hence m_c ≥ L+1 whenever 2^L ≤ (c+1)/4, i.e. m_c ≥ ⌊log₂((c+1)/4)⌋ + 1. (b) is E's Theorem 1 and Corollary 4 restated. ∎

*Consequence for the brief's angle (i).* "Clearing a degree-c error cannot be done in O(1) instructions" is true but trivially so (logarithmic growth), and it holds equally for the AC-trivial AK(2), so it carries no information about AK(3); conversely a lower bound g(c) → ∞ on d_{N_c}(AK3) *is* the non-triviality statement. The natural computable Lipschitz functions are useless: log₂ of the N_c-word length of the pair is 1-Lipschitz but bounded by log₂(15) on AK(3) uniformly in c; abelian and bounded-class data are killed by Guyot. The program has content only if someone exhibits a *new computable* 1-Lipschitz f_c on N_c² — I see no candidate, and I recommend against further effort here unless such a candidate appears.

## 7. Failed attempts (and why)

- *A theorem connecting P_n to P_(n−1) or P_(n−2).* With c frozen, (c, k) ~ (c, k′) only if k, k′ are conjugate in G_c up to inversion; k_n and k_(n−1) differ by the factor x, which is a nontrivial element of G_c (x maps to a generator of G_c's quotient ⟨x,y | c, y⟩ = ⟨x | x⟩… more simply, x ∉ ⟨⟨c⟩⟩ since c ↦ y² ≠ 1 under x ↦ 1), and I could not decide conjugacy in G_c in the time available. No bounded search was run for P_n ~ P_(n−1) (recommended below).
- *An obstruction from the killer viewpoint.* Being a pseudo-meridian is a property of (G_i, [r_j]) and changes under multiplication moves; §4 shows the AC-trivial AK(2) starts as a pseudo-meridian pair. No invariant results.
- *Reading Lackenby / Shehper / Silver–Whitten–Williams in full.* Blocked network; everything from these sources is labelled externally reported.

## 8. Honest limits

- Theorem K1 is an *equivalence*; it does not trivialize anything, does not lower n, and does not give evidence for or against AC-triviality of AK(3). For n ≥ 5 it shortens, for n = 4 it preserves length, for n = 3 it lengthens by one.
- The engine data of §5 are forward-reachable sets in the cyclic-product graph with fixed caps (J's correction to D's "component" applies); they are not obstructions.
- Novelty: Shehper et al. report a one-parameter family and length reducibility; P_n may be their family. C's MS(n, y⁻¹x²y⁻¹) ~ AK(n) and Panteleev–Ushakov's Aut-realization are the closest published uniform statements I know. The explicit words, the closed-form 4n−1-step path and the public certificates are, as far as I could check, new; no novelty claim is made.
- Alexander polynomials and thickenability in K1.3 were computed with F's modules (validated by F and J); Out(T(p,q)) of order two is cited from the Silver–Whitten–Williams snippet and from F's note.

## 9. Advice to the coordinator (ranked)

1. **Change coordinates: work on P_3 = (xyxYYXy, xxxYXyy) and on the family (c, xⁿu).** It is a certified member of AK(3)'s class (length 14) in which the n-dependence is a single power of x and the "difficulty" sits in a fixed one-relator group G_c = ⟨x,y | xyxy⁻²x⁻¹y⟩ (Δ = t²+t−1). Two concrete, cheap tasks for L/G: (a) run D's engine from P_n and from AK(n) simultaneously for n = 2,3,4 with Aut-orbit matching (`--autmatch`) to test whether P_3's class meets P_2's class (= the trivial class) or P_4's; (b) search for a uniform move P_(n+1) → P_n with c frozen first (decide conjugacy of k_(n+1), k_n^(±1) in G_c, e.g. via the C₂-type quotients or a one-relator normal form) and then with k frozen. A positive answer for n = 2 would trivialize AK(3); a *proof* that k_3 is not conjugate to any k_2-conjugate in G_c is expected and uninformative, so budget this as a search, not a theorem hunt.
2. **Pin down Shehper et al.'s family** as soon as any agent has arXiv access (arXiv:2408.15332, Section on AK(n)); if it equals P_n (or an Aut-image), cite them for priority and keep our certificates as the public ledger; if it differs, we have two independent normal forms and their relation is itself a cheap search.
3. **Exploit the two other length-16 Aut-orbits of AK(5)** (§5.1): decode their paths the same way (`movefind.py` + hand generalization) to get two more uniform families; each gives another fixed-relator description of the AK series and more starting points at length n+11.
4. **Do not spend theory time on monotone-defect obstructions or on E's correction-cost program** (Props. K2, K3): both are closed unless a genuinely new computable Lipschitz function on nilpotent quotients is proposed. H's fibre-product invariants are the only quotient-type candidates left standing; test them first on P_2 vs P_3 (same fixed relator, so the computation is cleaner than on AK(2) vs AK(3)).
5. **For the thickenability route (F, G):** §4 shows the one known AK trivialization enters the thickenable locus through a primitive relator after passing BS-type states, not through a meridional torus pair; meridian-guided search should therefore also reward Alexander-asymmetric intermediate states and primitive-relator detection (D's Lemma D3), not only torus forms.
6. **Audit request (J):** the proof of K1 is six displayed free-reduction identities; please re-derive them independently (10 minutes) and re-run `k_ak_family.py --check 2 200` and `elementary_verify.py certificates/k_*.json`.

## 10. Files written

- `research/research-k.md` (this note).
- `experiments/k_ak_family.py` — closed-form path, identity checker (`--check lo hi`), certificate generator (`--cert n out.json`, `--batch lo hi`); uses D's `d_certify.py` compiler and `elementary_verify.py`.
- `certificates/k_ak{3,4,5,6}_to_p{3,4,5,6}.json` — engine paths compiled to strict elementary moves (68/91/114/138 moves, peaks 25/31/37/43).
- `certificates/k_ak{3,7,10}_to_p{3,7,10}_uniform.json` — closed-form path compiled (88/187/271 moves, peaks 35/49/67).
- Scratch (not committed): `scratchpad/agent-k/{movefind.py, profile_cert.py, ak*_cap*.log, ak*_p.log, path_p*.txt}`.

## References

- S. Akbulut, R. Kirby, *A potential smooth counterexample in dimension 4 …*, Topology 24 (1985).
- A. Shehper et al., *What makes math problems hard for reinforcement learning: a case study*, arXiv:2408.15332, NeurIPS 2025 (abstract via search: one-parameter family AC-equivalent to AK(n); "length reducibility of all but two presentations in the Akbulut–Kirby series"; a stable AK(3) claim later undercut per the README/Lisitsa).
- D. Silver, W. Whitten, S. Williams, *Knot groups with many killers*, Bull. Aust. Math. Soc. 81 (2010), arXiv:0909.3275 (snippet level); C. M. Tsau, *Nonalgebraic killers of knot groups*, Proc. AMS 1988 (cited there).
- D. Panteleev, A. Ushakov, arXiv:1609.00325; A. D. Miasnikov, A. G. Myasnikov, arXiv:math/0304305; M. Lackenby, arXiv:2606.06122 (abstract only); J. Carr(eras), arXiv:2607.23611.
- Repository notes A–J and their tools (`d_acsearch.cpp`, `d_certify.py`, `d_whitehead.py`, `f_thicken.py`, `f_knotlike.py`, `elementary_verify.py`).

## Coordinator's review (second reader, 2026-11-03)

- **Theorem K1.** All six displayed free-reduction identities (A1 both steps, A2 including k = n, B's three recurrences c_m → a_(m+1), a_m → b_m, b_m → c_m, and C's two steps) were re-derived by hand, uniformly in n ≥ 2, and are correct. The coordinator also re-ran `python3 experiments/k_ak_family.py --check 2 200`, `--batch 2 30`, and `python3 experiments/elementary_verify.py certificates/k_*.json` (all seven certificates replay; the four engine-path certificates start at (p_n, b) and the three closed-form ones at (b, p_n), all ending at P_n up to order).
- **Labelling slip, harmless.** In the multiplier table, σ⁻¹ = Xyx^(n+1)YX^(n−1), τ_m⁻¹ = X^(n−m)yx^(n+1)YX^m and w′ = yx^(n+1)YXⁿ are rotations of w_n⁻¹ (not of w_n), and κ⁻¹ = XYxⁿyXⁿ is a rotation of w_n (not of w_n⁻¹). Since a cyclic product may use a rotation of the frozen relator or of its inverse, every step remains an ordinary AC composite and the theorem is unaffected.
- **Proposition K3(a).** The bound m_c ≥ ⌊log₂((c+1)/4)⌋ + 1 is correct, but the sentence "every instruction sequence ... whose endpoint is ≡ (x,y) mod γ_(c+1) ends at (x,y) exactly; reading the sequence backwards ..." does not by itself give the conclusion. The direct argument: a path of length L in N_c from (x e₀, y e₁) to (x,y) reverses and lifts to a path in F from (x,y) ending at (x e₀′, y e₁′) with e_i′ ≡ e_i mod γ_(c+1), so some e_i′ ∈ γ_c \ {1}; by Magnus's theorem (γ_c is the kernel of the degree-(c−1) truncation) and E's Lemma 2(a) a nontrivial element of γ_c has free length ≥ c, while E's length bound gives |e_i′| ≤ 2^L·4 − 2; hence c ≤ 2^L·4 − 2, i.e. m_c ≥ L+1 whenever 2^L ≤ (c+1)/4.
- Novelty of K1 is not established: Shehper et al. (arXiv:2408.15332) report a one-parameter family AC-equivalent to AK(n) with the same length-reducibility consequence; whether it coincides with P_n could not be checked (arXiv blocked in this session).
- **Correction (from agent O, 2026-11-03).** §4's phrase "with G_c not a 3-manifold group at all" is wrong: c has y-exponent sum 0 and G_c = ⟨x,y | xyxy⁻²x⁻¹y⟩ ≅ F(a,b) ⋊_φ ℤ (a = x, b = yxy⁻¹, φ(a) = b, φ(b) = b⁻¹a), the fundamental group of a punctured-torus bundle (research-o, Theorem O1; recalled identification: the Gieseking manifold). The correct statement is that G_c is not a knot group in S³, by F's Alexander-polynomial criterion (Δ = t²+t−1 is asymmetric). Nothing else in this note depends on the phrase.
