# Research TH20: referee report on the round-5 theory notes TH10–TH18

Date: 2026-11-09 (Los Angeles) / 2026-11-10 UTC. Agent TH20 (round 5, referee). No new AC result is claimed here; this note records what I could and could not verify in the nine notes `research/research-th10.md` … `research-th18.md`.

**Verdict labels.** VERIFIED = I re-derived the proof myself or re-checked the claim by an independent exact computation (which one is stated). PLAUSIBLE-UNCHECKED = read, no objection, not re-derived. GAP / ERROR / OVERCLAIM as usual. Re-running an author's self-test is recorded separately and is *not* counted as verification.

**Versions refereed.** Snapshot of 04:54 UTC (line counts 220, 290, 269, 267, 306, 468, 215, 217, 263 for TH10…TH18); changes after that are listed in §11 (final re-read).

**Overall summary (five lines).**
1. No note claims an AC trivialization of AK(3), an obstruction, or a counterexample, and I found none hidden in the certificates: all 52 `certificates/th1x_*.json` files replay (51 with `elementary_verify.py`, one rank-3 *stable* certificate with my own strict rank-3 replayer), and I recomputed the start and target of each against the note's statement.
2. Strongest verified results: **TH10 Theorem A/B** (metabelian-quotient filter; hence no periodic, just-infinite or residually-finite-at-the-BS-coordinate quotient obstructs any AK(n) or any Miller–Schupp presentation); **TH15 Theorem 1** (Aut(F₂) is AC-realized on AK(n) for all n — a five-line symbolic proof plus closed-form paths, both re-derived by hand); **TH12** (generator area of AK(n) is exactly n+4, and every elementary trivialization of AK(n) has ≥ 2n−1 moves for n ≥ 4).
3. Also verified: TH13 duality and plateau depth for AK(k;p); TH14 stable theorems A, B, B2 and Prop. E3; TH16 Theorems A–C (Miller–Schupp nodes are ACM local minima) and the two-node structure of D's 34 benchmark members; TH17 dictionary/coincidence theorems; TH18 classification of ℓ ≤ 3 killer classes of BS(n,n+1) and P2 ~AC (x⁴y⁻⁵, xy⁻²xy²x⁻¹y⁻¹) (certificate); TH11 Out(G_c) ≅ ℤ/2, the invariants (κ, Ĵ) and the uniform "no primitive exit from P_n, n ≥ 3".
4. Errors found: one, in the first draft of TH11 (Stab(p_n^{±1}) = {±I} claimed for n ≥ 2; false for n = 2) — **corrected by TH11 in its final text**. One wording OVERCLAIM remains in TH18 ("P2 is a torus-knot pair": only one relator is of torus type). Unchecked for lack of time: TH17 Theorem 6 (restricted-graph rigidity), TH11's cokernel table at levels 5–8, TH14 §2.1 move counts and §5.2, TH12 Cor. 2.1(c), TH16 T7.
5. Everything labelled "stable" (TH14) is correctly labelled; every "no exit / local minimum / lower bound" statement is correctly labelled as a statement about a restricted move class or about complexity, not as evidence of non-triviality.

My check scripts (standard library only; each < 2 min, < 200 MB): `experiments/th20_lib.py` (words, automorphisms, own torus-group conjugacy invariant cross-validated against `g_torus.torus_class` on 27,000 random words, pieces, coset-enumeration wrapper, certificate replay with endpoints), `th20_macro.py` (macro replayer, strict replayer in any rank), `th20_bs.py` (own Baumslag–Solitar conjugacy: Britton + Collins + slide lattice), `th20_stab.py` (own Whitehead level-graph stabilizers), `th20_theta_holonomy.py` (own exact figure-eight holonomy in ℚ(ω)), and one `th20_thNN_check.py` per note.

## 0. Pre-check of the coordinator's findings given to TH11 (04:11 UTC, before any draft existed)

`python3 experiments/th20_theta_holonomy.py 14 40` → `theta: c -> conj of c^-1; x^s y -> conj of x^(1-s) y; k_n -> X^(n+1) Yxyxyx [free identities OK]` and `trace coincidences (n,s), n<=14, |s|<=40: (1,-2),(1,3),(2,-2),(2,3),(4,-4),(4,5),(5,-5),(5,6)` (the same list for θ(k_n)).

| claim (coordinator → TH11) | verdict |
|---|---|
| θ = (x ↦ x⁻¹, y ↦ yx) sends c = xyxYYXy to a conjugate of c⁻¹ (θ(c) = XyXYXYxyx, cyclically yXYXYxy) | VERIFIED (hand + script) |
| θ(xˢy) = x⁻ˢyx ~ x^{1−s}y; θ(k_n) = x^{−(n+1)}y⁻¹xyxyx with normal form (a⁻ⁿbab, 1) | VERIFIED (hand: reading rule of O1; script) |
| the exact invariants of k_n² and of (xˢy)², y(xˢy)²y⁻¹ coincide for (n,s) ∈ {(1,−2),(1,3),(2,−2),(2,3),(4,−4),(4,5),(5,−5),(5,6)} only (n ≤ 14, \|s\| ≤ 40) | VERIFIED (independent exact arithmetic; trace triple (1−ω, 2+ω, 2+ω) re-derived as the fixed point of the trace map of φ²; relations TAT⁻¹ = B⁻¹A, TBT⁻¹ = A⁻¹B² asserted exactly) |

## 1. TH10 — exotic quotients: the metabelian-quotient filter

Self-test re-run: `th10_torus_coords.py --selftest` passes (103 s). The note changed substantially between 04:14 (abelian filter, "order divisible by 42") and 04:45 (metabelian filter, "infinite order"); the verdicts are for the later, stronger statements.

| claim | verdict | what I did |
|---|---|---|
| A: an admissible pair (s,t) of Q with Q/⟨⟨s⟩⟩ **metabelian** is standardizable; so a class coordinate with metabelian one-relator quotient of Q forbids obstruction | VERIFIED (proof checked line by line; the abelian case I had proved independently before reading) | steps 1–7: p̄ ∈ M = [Q̄,Q̄]; M = ⟨⟨p̄⟩⟩ = ℤ[τ^{±1}]p̄ = ℤp̄ + (τ⁻¹−1)M; m(q̄p̄ⁱ)m⁻¹ = q̄(τ⁻¹m + ip̄ − m) = t̄ — all correct; then two "multiply by an element of the normal closure" steps and Nielsen moves. |
| A1, A2, A3 | VERIFIED (formal consequences of A) |
| A4: if ⟨⟨π(c)⟩⟩ ∩ [Q,Q] is virtually solvable, Q does not obstruct | VERIFIED given H's Theorem 2 (coordinator- and TH08-checked) | the image of π(c) is central modulo N₁, so Q₁/⟨⟨w₁⟩⟩ is cyclic. |
| B: BS coordinate c = v⁻¹uᵖvu^{−q}, \|p−q\| = 1: if ū has finite order (or a central power) in Q̄, or Q̄ is residually finite, then Q̄ is metabelian | VERIFIED (re-derived) | conjugate elements ūᵖ, ū^q have equal order ⇒ gcd(m,p) = gcd(m,q) = 1 ⇒ ⟨ū⟩ normal with cyclic quotient. |
| B1: no periodic group (any B(2,N)), no central extension of one, no just-infinite group, no group with the normal subgroup property obstructs AK(n) or any MS(n,w) | VERIFIED given C's theorem M_n ~AC AK(n) (or TH15 Lemma H: AK(n) ~AC (β_n, b)) | the BS(n,n+1) relator is a class coordinate. |
| B2: if Q obstructs AK(3), every primitive element has image of infinite order with no central power; same for P1, P2 | VERIFIED given D6 (Aut-closure) and I §5 |
| C, C1: torus coordinates vs torsion; primitive order 10 \| m for C4, 210 \| m for C3 | VERIFIED (own proof of C; W_n ~ u²v^{−(2n+1)} with (u,v) = ((xy)ⁿx, xy) and b ~ (xyx)²(xy)⁻³ checked by hand); the list of torus types met in C3's certificates is TH10's experiment, not recomputed |
| Prop. 4.1 (finite residual of B(2,N)), 4.3 (power twists) | VERIFIED from the quoted external facts (X1–X2 not checked, labelled as such). Remark: 4.3 follows at once from A — for *every* automorphism α of Q, Q/⟨⟨α(a)⟩⟩ ≅ Q/⟨⟨a⟩⟩ is cyclic, so α(a,b) is standardizable as soon as it is admissible. |
| Prop. 5.2 / Cor. 5.3 (glide length λ(xⁿy^{−(n+1)}) = ⌊3n/2⌋+1 vs λ ∈ {1,2} for primitives; no braid-frozen primitive exit, all n ≥ 2) | VERIFIED (all isometry compositions recomputed by hand: ση: z ↦ ω̄z − ω̄, σησ = ηση: z ↦ ωz̄, ησ⁻¹: z ↦ ωz; both parities of n) | a second proof of G2(b), uniform in n. |
| E (Q₂ = ⟨x,y \| [x,y]²⟩ obstructs no AK(n); Q_n, n ≥ 3, passes the filters; U AC-trivial iff sup_n d_{Q_n}(U) < ∞) | VERIFIED for Q₂ (d₁ = d₀d₂ from the braid relation; D is a quotient of V₄) and for the residual-chain statement; the structure E_n ≅ D(n,n,n) ⋊ ℤ and "passes filter B" are PLAUSIBLE-UNCHECKED (quoted facts). |

## 2. TH11 — relator stabilizers, nilpotent Reidemeister invariants of G_c, relations between the k_n

Self-tests re-run: `th11_nil.py`, `th11_stab.py`, `th11_trace.py`, `th11_cert.py --selftest` all pass. My checks: `th20_stab.py`, `th20_th11_check.py` (uses TH11's `KJ`/`KJ_ser` for the definition of the invariants and my own exact holonomy for N), outputs:
```
c = xyxYYXy  Stab(w^+-1): [((-1,1),(0,1)), ((1,0),(0,1))] | Stab(w): {I}        b: Stab(w^+-1) = {+-I, +-swap}
p_2: Stab(w^+-1) = {+-I, +-((1,0),(-3,-1))}   p_3..p_7: {+-I}   k_3, k_4: trivial
(1) closed forms kappa, Jhat = J - kappa agree with th11_nil.KJ for n in [-40,60], s in [-40,40]
(3) (n,s) with equal (kappa,Jhat), |n| <= 2000: [(-1,-1), (-1,0), (0,-1), (0,0), (1,-2), (2,-2), (9,5)];  tau(k_9^2) in tau-set of x^5 y: False
(4) pairs n<m<=3000 with Jhat(k_n)=Jhat(k_m): [(1,2,'same kappa'), (6,7,'kappa differs')]; tau-sets of k_6, theta0(k_7) and of k_7, theta0(k_6) disjoint
N(k_n), n=-1..9: 2,2,8,8,20,74,218,632,1880,5588,16562;  N(x^s y), s=-1..9: 2,2,2,2,8,26,74,218,650,1928,5714;  reflection identity holds for n = -12..16
```

| claim | verdict | what I did |
|---|---|---|
| T1: Out(G_c) ≅ ℤ/2 = ⟨[θ₀]⟩; Stab(c^{±1}) = {1,[θ₀]}, Stab(c) = 1; θ₀(u,1) = (ι(u)b, 1) | VERIFIED | own proof: the fibre [G_c,G_c] = F(a,b) is characteristic, so Out(G_c) = N_{GL₂(ℤ)}(⟨A⟩)/⟨A⟩, A = [[0,1],[1,−1]]; tr A ≠ tr A⁻¹ and C(A) = {±Aᵏ} (units of ℤ[(1+√5)/2]); θ₀ acts on the fibre by ι and y ↦ (b,1) (hand computation). Stabilizers: own level-graph computation (rests on Whitehead/McCool, recalled). |
| T2: Stab(b^{±1}) = {±I, ±swap}; Stab(p_n^{±1}) = {±I} for n ≥ 3, one extra class ±(x ↦ xy⁻³, y ↦ y⁻¹) for n = 2 | VERIFIED (b, n = 2..7 by my computation) | **The 04:24 draft claimed {±I} for all n ≥ 2 — an ERROR for n = 2, which I found independently ((xY³)²y³ = xY³x ~ x²Y³); the final text states the n = 2 exception correctly.** |
| T3: κ ∈ ℤ/2 is the complete invariant mod γ₃; κ∘θ₀ = κ + 1; hence θ₀(g) ≁ g | VERIFIED (proof read; κ(b) = 1 via w = a⁻¹b⁻¹, w·b·φ(w)⁻¹ = [a⁻¹,b⁻¹] recomputed) |
| T4: (κ, Ĵ) complete mod γ₅; closed forms Ĵ(xˢy) = −C(s+1,4), Ĵ(k_n) = −n(n+1)(n²−11n+22)/24 | VERIFIED for levels 1–4 (own argument: I−A, I+A unimodular, level 2 gives ℤ/2, coker(I−Φ₄) ≅ ℤ since the 2×2 minors of I−Φ₄ have gcd 1; stabilizer of a normal form is γ₄) and for the closed forms (≥ 5 points per residue class mod 4, degree ≤ 4). The cokernels at levels 5–8 are PLAUSIBLE-UNCHECKED. |
| T5: xˢy ~ x^{s′}y iff s = s′ or {s,s′} = {−1,0}, {1,2} | VERIFIED given T4 (s²−s determines Ĵ except for the values 0, 2; κ separates s from 1−s) |
| T6: k_n ≁ xˢy for all n ≥ 3 (uniform O6, second proof) | VERIFIED given T4 | (s²−s−1)² = (n²−5n−7)² − 48(n+1) checked by expansion; my Runge bound: no solutions for n ≥ 31 or n ≤ −19; brute force gives exactly TH11's list; (9,5) excluded by my exact holonomy. Agrees with O6 and with TH03's independent proof. |
| T7: k_n ~ k_m iff n = m or {n,m} = {1,2}; k_n ≁ θ₀(k_m) | VERIFIED given T4 (Ĵ(k_n) strictly decreasing for n ≥ 9; the only coincidences are (1,2) and (6,7); the pair (6,7) is excluded for θ₀ by holonomy, both twists) |
| T8: reflection identity N(k_n) + N(k_{4−n}) = N(x^{n+1}y) + N(x^{n−4}y) | VERIFIED (own exact values identical to TH11's; identity checked on 29 consecutive n, 4 suffice by the 4-dimensional exponential-polynomial argument) |
| T9: P₃ ~AC θ₀(P₃) = (c, x⁻³y⁻¹xyxy) | VERIFIED (certificate replayed: (xyxYYXy, xxxYXyy) → (xyxYYXy, XXXYxyxy), 1,190 moves; target = cyc θ₀(k₃), recomputed) |
| T10: three mirror pairs of c-frozen classes in AK(3)'s class, none with a c-frozen primitive exit | VERIFIED (two new certificates (c, yxxYXyX) → AK(3) and (c, YYYxyxyX) → AK(3) replayed; invariants (κ,Ĵ,N) = (0,1,20), (0,−6,32), (0,−32,110) recomputed; −C(s+1,4) never equals 1, −6, −32) |

## 3. TH12 — generator area of AK(n) and linear lower bounds on the number of moves

Self-test re-run: `th12_area.py --selftest` passes. `python3 experiments/th20_th12_check.py`:
```
(1) identities OK, n = 1..30        (2) trace(r) = n^2+n+2 in SL2(Z), braid relation holds
(3) n <= 6: mu <= n+1 forces mu = n+1 and count matrix [[1,n+1],[1,n]]  (so mu >= n+2 by c_r >= 3)
(4) permutation model OK, n = 4..40
(5) TH12 Prop. 8 (P1)-(P3) and Prop. 9 identities hold as free identities, n = 2..30; x = Y b y has 4 + 7 = 11 factors
```

| claim | verdict | what I did |
|---|---|---|
| Thm 1 (count-matrix calculus; A(U₀) ≤ F_{μ+2}; radius ≤ κ) | VERIFIED (proof read) |
| Thm 2: Area_{AK(n)}(x) = n+4, Area(y) = n+3; c_r ≥ 3 odd, c_s ≥ n+1 (resp. n) in every expression | VERIFIED | identities (I_x), (I_y) re-typed and freely reduced (n ≤ 30); signed counts from E⁻¹ = [[−1,n+1],[−1,n]]; c_r = 1 impossible because tr = 2 ≠ n²+n+2 under B₃ → SL₂(ℤ) (recomputed). |
| Thm 3: every instruction path AK(n) → (x,y) has μ ≥ n+2 multiplications | VERIFIED (proof read step by step: L = ab, R = ab⁻¹ in ℤ/2*ℤ/3; class lengths 2n+3, 2n+2; loss 0, 1, never 2; loss 0 forces count matrix \|Σ\|; exhaustive check n ≤ 6) |
| Thm 4: κ ≥ n−3 conjugations for n ≥ 4 | VERIFIED (proof read; Lemma 4.1 checked by hand and script; the conjugators are sub-products over distinct conjugation instructions, so the point v = κ⁻+1 would be fixed) |
| Cor. 5: d_F(AK(n)) ≥ 2n−1 (n ≥ 4); every elementary-v1 certificate for AK(n) has ≥ 2n−1 moves | VERIFIED given Thm 3, 4. Correctly labelled: a complexity statement that also holds for the AC-trivial AK(1), AK(2). |
| Prop. 8, 9 (over P_n: 3 ≤ Area(x) ≤ 11 for every n) and Cor. 10 (≥ 2n multiplications between AK(n) and P_n) | VERIFIED (identities by free reduction, n ≤ 30; Cor. 10: −RⁿL^{−n−1} = E_{P_n}E_{AK(n)}⁻¹ and its class length 4n+1 recomputed) |
| Cor. 2.1(c) (Dehn function ≤ (n+4)ℓ), Props 6, 7, radius experiments | PLAUSIBLE-UNCHECKED |

## 4. TH13 — the family AK(k;p) = (xᵖY^{p+1}, W_k)

Self-test re-run: `th13_family.py --selftest` passes. `python3 experiments/th20_th13_check.py` and `th20_th13_plateau.py` (own enumeration of *all* cyclically reduced words below the claimed bounds, own torus invariant):
```
(1),(2) OK for k,p <= 8: phi_k(p_p) ~ V_{k,p} in <x^2=y^(2k+1)>, necklace (k+1)^p k^(p+1)
(3) coset enumeration: AK(k;p), D(k;p) trivial for k<=4, p<=5
power side k=2 p=2: nothing off the plateau for L <= 10; L=11: 264 words     k=2 p=3: plateau 28 words at L=7, nothing for L <= 12, L=13: 624 words
braid side k=2 p=3 (G_p and G_p'): Orb(W_2) at L=10, nothing at L=11, L=12: 144 words     k=1 p=3: 432 words at L=9, 32 words at L=8 (J's numbers)
```

| claim | verdict | what I did |
|---|---|---|
| T1: F(a,b;i,j;m) trivial iff \|bi−aj\| = 1; admissible (i,j) give AC-equivalent presentations | VERIFIED (proof read; triviality of AK(k;p) also proved independently: z = xᵖ = y^{p+1} central, x ~ y) |
| T2: duality AK(k;p) ~AC (ψ_k(V_{k,p}), W_k) by one W_k-frozen ACM move | VERIFIED (own hand proof in C₂*C_{2k+1} incl. central exponent via abelianization = −1; script k,p ≤ 8; three certificates start at AK(k;p) and end at (red ψ_k(V_{k,p}), W_k)). D(k;p) is reached up to the automorphism ψ_k only — the note says so. |
| T3: AK(3) ~AC AK(3;2) = (xxYYY, xyxyxyxYXYXYXY); AK(2;2), AK(k;1) AC-trivial | VERIFIED (certificates replayed, endpoints checked; logically G1 + D6/TH15). Not new information on AK(3). |
| T4: plateau — first exit from AK(k;p), p ≥ 3, at cyclic length ≥ 2p+4k+3+min(4k−2, 2k+2, 2p−4) | VERIFIED (Lemma P and Lemma B read line by line — zigzag table, parity of 2J, M+N = 0 ⇒ ν ∈ {0} ∪ [2,∞); brute force above for (1,3), (2,2), (2,3), partially (3,3)). A statement about ACM paths. |
| T5: no primitive relator one ACM move from AK(k;p), p ≥ 2, (k,p) ≠ (1,2) | VERIFIED given Fact C of research-g (both cases re-derived: \|l\|/\|m\| ∈ (1,2) resp. (k,k+1), balanced necklaces vs (k+1)ᵖk^{p+1}) |
| T6: Aut(F₂) is AC-realized on AK(2;3) and AK(2;4) | VERIFIED (certificates for σ and τ = (x ↦ xy) replayed; targets recomputed: (yyyXXXX, yxyxyXYXYX), (xyxyxYYY, xyyxyyxYXYYXY), and the p = 4 analogues; σ, τ generate GL₂(ℤ); mirror certificate → (XXXYYYY, XyXyXYxYxY) replayed) |
| T7 (Lemma 7), X8 and the "caution" about bounded mirror searches | PLAUSIBLE-UNCHECKED (Lemma 7 read; searches not re-run) |

