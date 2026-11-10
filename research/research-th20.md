# Research TH20: referee report on the round-5 theory notes TH10–TH18

Date: 2026-11-09 (Los Angeles) / 2026-11-10 UTC. Agent TH20 (round 5, referee). No new AC result is claimed here; this note records what I could and could not verify in the nine notes `research/research-th10.md` … `research-th18.md`.

**Verdict labels.** VERIFIED = I re-derived the proof myself or re-checked the claim by an independent exact computation (which one is stated). PLAUSIBLE-UNCHECKED = read, no objection, not re-derived. GAP / ERROR / OVERCLAIM as usual. Re-running an author's self-test is recorded separately and is *not* counted as verification.

**Versions refereed.** Main pass on the snapshot of 04:54 UTC; final re-read of the versions current at 05:04 UTC (line counts TH10 225, TH11 306, TH12 270, TH13 268, TH14 437, TH15 468, TH16 219, TH17 217, TH18 287; TH10, TH11, TH14, TH16 stopped at 04:56–04:57 UTC because of an API error), §11.

**Overall summary (five lines).**
1. No note claims an AC trivialization of AK(3), an obstruction or a counterexample, and none is hidden in the certificates: all 52 `certificates/th1x_*.json` replay (51 with `elementary_verify.py`, one rank-3 *stable* certificate with my own strict replayer); starts and targets match the notes; none goes from AK(3) (or P₃, Q, M₃) to (x,y).
2. Strongest verified results: **TH15 Thm 1** (Aut(F₂) is AC-realized on AK(n) for every n; short symbolic proof and closed-form paths re-derived by hand); **TH12 Thms 2–4, Cor. 5** (generator area of AK(n) is exactly n+4; every elementary trivialization of AK(n) has ≥ 2n−1 moves, n ≥ 4); **TH10 Thms A, B** (metabelian-quotient filter ⇒ no periodic, just-infinite or residually-finite-at-the-BS-coordinate quotient obstructs any AK(n) or MS(n,w)); **TH16 Thm H** (Q is an ACM local minimum — re-proved with my own exact invariants in both frozen groups).
3. Also verified: TH11 T1–T11 (Out(G_c) ≅ ℤ/2; (κ,Ĵ); uniform no-primitive-exit from P_n, n ≥ 3; P₃ ~AC θ₀(P₃)); TH13 T1–T6 (duality, plateau depth, Aut-realization on AK(2;3), AK(2;4)); TH14 A, B, B2, E3, F (all **stable**, correctly labelled); TH16 Thms A–C; TH17 Thms 1–5; TH18 T1–T7, T9, T10 (P2 ~AC (x⁴y⁻⁵, xy⁻²xy²x⁻¹y⁻¹), certificate).
4. Errors: one ERROR in TH11's first draft (Stab(p₂^{±1}) = {±I}; false, order 4) — corrected in TH11's final text. One OVERCLAIM remains: TH18 calls AK₂(4) / P2 "a torus-knot pair" (only x⁴y⁻⁵ is of torus type). Minor: TH14's claims table drops the hypothesis "⟨p,q⟩ non-cyclic" of Lemma C (the lemma itself has it).
5. Not checked (time): TH17 Thm 6 (restricted-graph rigidity), TH14 Prop. B3 / §2.1 counts / F-exp, TH12 Cor. 2.1(c), TH10 E (structure of Q_n), TH18 E3 survey — all PLAUSIBLE-UNCHECKED, none labelled as a headline.

My check scripts (standard library only; each < 2 min, < 200 MB): `experiments/th20_lib.py` (words, automorphisms, own torus-group conjugacy invariant cross-validated against `g_torus.torus_class` on 27,000 random words, pieces, coset-enumeration wrapper, certificate replay with endpoints), `th20_macro.py` (macro replayer, strict replayer in any rank), `th20_bs.py` (own Baumslag–Solitar conjugacy: Britton + Collins + slide lattice), `th20_stab.py` (own Whitehead level-graph stabilizers), `th20_theta_holonomy.py` (own exact figure-eight holonomy in ℚ(ω)), `th20_k3_traces.py` (own normal forms and twisted traces for G_{k₃} = F₃ ⋊ ℤ), `th20_th16_Q.py`, `th20_lie_coker.py` (cokernels of 1 − φ on the free Lie ring), `th20_th13_plateau.py`, and one `th20_thNN_check.py` per note.

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
| T4: (κ, Ĵ) complete mod γ₅; closed forms Ĵ(xˢy) = −C(s+1,4), Ĵ(k_n) = −n(n+1)(n²−11n+22)/24 | VERIFIED for levels 1–4 (own argument: I−A, I+A unimodular, level 2 gives ℤ/2, coker(I−Φ₄) ≅ ℤ since the 2×2 minors of I−Φ₄ have gcd 1; stabilizer of a normal form is γ₄) and for the closed forms (≥ 5 points per residue class mod 4, degree ≤ 4). The cokernels at levels 5–8 are VERIFIED by my own free-Lie-ring computation (`th20_lie_coker.py`, Lyndon basis, Smith form): 0, ℤ/2, 0, ℤ, (ℤ/2)², ℤ/2⊕(ℤ/6)², (ℤ/2)⁵⊕ℤ/22, ℤ⁸⊕(ℤ/2)² for k = 1..8 — identical to TH11's table. |
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
| T7 (Lemma 7: for k ≥ 2 no basis of F maps to a simultaneous conjugate of (s, t^k) in C₂*C_{2k+1}) | VERIFIED (first part re-derived: [α,β] ~ [x,y]^{±1} ↦ necklace {1,−1}, while [s,t^k] has {k,−k}, equal mod 2k+1 only for k = 1); second part read |
| X8 and the "caution" about bounded mirror searches | experiment, not re-run |

## 5. TH14 — **stable** theory (one stabilization)

Every statement of this note is about tuples (U, z) in rank n+1 and is labelled *stable* there; nothing in it is an ordinary AC result. Self-tests re-run: `th14_verify3.py`, `th14_stallings.py --selftest` pass. The rank-3 certificate `th14_c4_invy_stable1.json` (format `stable1-ac-elementary-rank3-v1`, not readable by `elementary_verify.py`) was replayed with **my own** strict replayer `th20_macro.replay_strict`: 695 moves, (xxxxyXy, xyyyxYY, z) → (xxxxYXY, xYYYxyy, z) = (ε_y(C4), z), peak 33.

| claim | verdict | what I did |
|---|---|---|
| A: the AC class of (U, z) is invariant under Aut(F_{n+1}) | VERIFIED (proof read line by line: the two letter-replacement identities, z ∈ ⟨⟨σ_iU⟩⟩, generation by star transpositions, one inversion, one transvection). Classical in content, as the note says. |
| B: ⟨⟨p,q⟩⟩ = F₂ and ⟨p,q,t⟩ = F₂ ⇒ (U∘(p,q), z) ~ (U, z) in rank 3 | VERIFIED (I proved it independently before TH14's proof was written; same argument: Nielsen equivalence of the generating triple (p,q,t) to (x,y,1) gives α with ker π = ⟨⟨α(z)⟩⟩; exponent of z in α(z) is ±1; transport by α⁻¹; delete z-letters) |
| B2: (U(x), P(z)) ~ (U(P(z)), x₁..x_n); for P trivial, (U∘P, z₁..z_n) ~ U ⊔ P | VERIFIED (proof read; both substitution identities checked) |
| Lemma C: w(p,q) primitive in F ⇒ w primitive, **for ⟨p,q⟩ non-cyclic** | VERIFIED (Kurosh). The claims table omits the hypothesis; without it the statement fails (p = x, q = 1, w = u[u,v]); the lemma itself is stated correctly. |
| Prop. E3: for s₁ ~ (x³y⁻⁴)^{±1} mod ⟨⟨b⟩⟩, no g, h, t with ⟨g s₁g⁻¹, h b h⁻¹, t⟩ = F | VERIFIED (read in full and recomputed: ρ = [[13,3],[4,1]], f_ρ = 4X² − 12XY − 3Y² ∈ {0,4,5} mod 8; Grushko step; Fricke identity with tr[S,ST] = 3; the Vieta descent γ ≤ 3, 48γ² − 191 a square only for γ = 2, neighbours 13 and 15; parabolic q* forces c = ±1) |
| Prop. B3 (rank reduction by duality) | PLAUSIBLE-UNCHECKED (same technique as B; read once) |
| §2.1 macro-move counts, §5.2 bounded search for exits | not checked (experiment / bookkeeping) |

## 6. TH15 — Aut(F₂) is AC-realized on AK(n), all n (Panteleev–Ushakov's theorem, with a self-contained proof)

Self-tests re-run: `th15_aut_family.py`, `th15_transport.py --selftest` pass. `python3 experiments/th20_th15_check.py` (words typed from the note's closed formulas, own cyclic-product test, TH15's code not imported):
```
TH15 closed-form chains: every step is one cyclic product, endpoints = sigma(AK(n)), a(AK(n)) up to rotation/inversion, n = 2..12   (n = 3 and 5 printed in full)
TH15 Prop. C (AK(n) -> H_n = (XY^(n+1)xy^n, xxYXY)) and Prop. D (AK(n) -> M_n): n+3 cyclic products each, n = 2..10
```
Symbolic identities re-derived by hand for general n (free reduction): swap, b frozen: yxyXYX·(xy·x^{n−k+1}Y^{n+1}XYX·yᵏ) = yxy·x^{n−k}Y^{n+1}XYX·yᵏ ~ w_{k+1}; for k = n it is ~ w′₁ = y^{n+1}xYⁿXYX; XyxyXY·(yxY^{n+1−j}XYX·yⁿX^{j−1}) = XyxY^{n−j}XYX·yⁿX^{j−1} ~ w′_{j+1}; for j = n it is XXyⁿX^{n−1} ~ q_n. Transvection a = (x ↦ xY): (Xu_kx)·XyxyXY = u_{k+1}; for k = n−1 it gives YⁿxyⁿXY ~ b₁; (Y^{n+1}xyⁿX)·u_{n−1} ~ v₀; (xyⁿXY^{n+1})·(y^{n+1}xY^{n−1}XXy) = xyXXy ~ a(b)⁻¹; YxxYX·(xy^{n−1−m}XY^{n+2}x(Yx)ᵐ) ~ v_{m+1}, ending at (xY)ⁿY^{n+1} = a(p_n).

| claim | verdict | what I did |
|---|---|---|
| Lemmas M, S, T, H, N | VERIFIED (each free identity recomputed: ΔxΔ⁻¹ = b·y, ΔyΔ⁻¹ = x·b⁻¹; T_k(β) = y^{−k}βyᵏ and T_k ≡ conjugation by y^{mi} mod ⟨⟨β⟩⟩; xyX ≡ Yxy mod ⟨⟨b⟩⟩ ⇒ β_n ~ p_n; σ and T generate GL₂(ℤ)) |
| **Theorem 1** (short proof): S(AK(n)) = S((β_n, b)) ∋ σ (b frozen), T (β_n frozen) ⇒ Aut(F₂) | VERIFIED (complete, valid for all n ≥ 1). Not new as a theorem (Panteleev–Ushakov), as the note says; the proof and the "hub" (β_n, b) are explicit. |
| Props A, B (2n+1 cyclic products each), C, D (n+3 each) | VERIFIED (A, B by hand for all n and by script n ≤ 12; C, D by script n ≤ 10) |
| Prop. E (generalized-move distances 1 and 3) | VERIFIED (lower-bound case analysis read; syllable counts and abelianization values recomputed) |
| Cor. 2–8 (Aut-invariance of the class for all n; G1 unconditional; ℤ-family (β_n, T^k(b)); every MS(n,w) has the hidden transvection T; Sym_n, P1 = C6 symbolically) | VERIFIED as consequences of Lemmas M, T (Sym₂ = P1 up to rotation checked) |
| certificates `th15_*.json` (13 files) | VERIFIED: all replay; targets recomputed: σ(AK(n)) = (yⁿX^{n+1}, yxyXYX), a(AK(n)) = ((xY)ⁿY^{n+1}, xxYXY) for n = 2, 4, 8; ε_x(AK(4)), (x ↦ xy)(AK(4)); hub (XYYYYxyyy, xyxYXY); AK(3) → M₃ in 57 moves; the two hidden-transvection certificates. |

## 7. TH16 — small cancellation; Miller–Schupp nodes as local minima of the ACM graph

Self-test re-run: `th16_rigidity.py --selftest` passes. `python3 experiments/th20_th16_check.py` (own BS code, own torus invariant, own enumeration):
```
(A) BS(3,4), BS(4,3), BS(4,5), BS(5,4), w1 and w2: no conjugate of w_i^+-1 of length < 5; at L=5 exactly Orb(w_i) (10 words)
(B) n=3 and n=4, G_w1 and G_w2: no conjugate of m_n^+-1 of length < 2n+3; at length 2n+3 exactly Orb(m_n) u Orb(m_n') (36, 44 words)
(C) 34 benchmark targets (first relator ~ m_3^+-1 in F): {'w1': 17, 'w2': 17, 'other': 0} | w1 ~ w2^+-1 in BS(3,4): False
(D) m_n ~ p_n in B (n <= 8); b ~ w_1 in BS(n,n+1) (2 <= n <= 8)
```
**Are the small-cancellation hypotheses verified for the words they are applied to?** They are verified to *fail*, and the note applies no small-cancellation theorem. I recomputed the pieces (`th20_lib.pieces`, star-graph triangle test): (max piece, min number of pieces, triangle) = b (2,4,no), p₃ (3,4,no), c (2,4,yes), k₃ (2,6,yes), q₁ (1,6,yes), q₂ (2,6,yes), m₃ (3,5,yes), w₁, w₂ (1,5,yes); joint maximal pieces AK(3) 3, P₃ 3, Q 2, MS(3,w_i) 3 — identical to TH16's table. Lyndon–Schupp is quoted only in Remark 2 (Dehn's algorithm V.4.4 with the bound (1−3λ)|r|, Britton IV.2.1, Collins IV.2.5, "numbering from memory", labelled externally reported), and the thin-annulus statement is explicitly *not* used.

| claim | verdict | what I did |
|---|---|---|
| T1: C′(1/6) forces \|r\| ≤ 2 or ≥ 13; C′(1/8): ≤ 2, 17, 18 or ≥ 25 | VERIFIED (pigeonhole 2ℓ ≤ 4·3^μ re-derived; brute force ℓ ≤ 9) |
| T2 (displacement lemma) | VERIFIED (two-line proof) |
| T3 = Thm A: shortest conjugates of w_i^{±1} in BS(P,Q) are Orb(w_i); b ~ w₁ if Q = P+1 | VERIFIED (slide formula recomputed: a′ = (−1+P(k₁−k₂), Qk₂−Pk₃, −1+Q(k₃−k₁)); brute force (A)); rests on Britton/Collins (classical) |
| T4 = Thm B: shortest conjugates of m_n^{±1} in G_{w_i} are Orb(m_n) ∪ Orb(m_n′), length 2n+3, all n ≥ 3 | VERIFIED (case analysis read: (n_x,n_y) list, loss table for the eight sign patterns, ε₁ = −ε₂; brute force (B)) |
| T5 = Thm C + Prop. D: MS(n,w_i) are plateaus of the ACM graph; AK(n) → (m_n,b) → MS(n,w₁) | VERIFIED given A, B; Prop. D recomputed (in B: Xyⁿx = yxⁿY) |
| T6: D's 34 benchmark members are two ACM nodes | VERIFIED (independent exact computation (C)) |
| T7 / **Theorem H (final version): Q = (xxyXYY, xxxYYXy) is a local minimum of the ACM graph; its plateau is the single orbit Orb(q₁) × Orb(q₂)** | **VERIFIED by independent exact computation** | (a) q₁ frozen: transported by β = (x ↦ xYX, y ↦ YX) to G_c (β(q₁) ~ c checked); every cyclically reduced word of length ≤ 7 and degree ±1 is separated from q₂^{±1} by my holonomy (squares, both twists) and (κ, Ĵ), except exactly the 14 words of Orb(q₂) (`th20_th16_Q.py`; q₂′ is excluded). (b) q₂ frozen: G_{q₂} ≅ G_{k₃} via θ = (x ↦ x⁻¹); my own twisted traces on ℚ⟨X₀,X₁,X₂⟩/(deg > 3) for G_{k₃} = F₃ ⋊_ψ ℤ (3-dimensional space; invariance re-tested on 300 random conjugates/relator insertions; soundness is the standard identity l(M(v)M(u)M(ψv)⁻¹) = l(M(u))) leave, among all words of length ≤ 6 and degree ±1, exactly the 12 words of Orb(q₁) (`th20_k3_traces.py`). In particular no primitive relator is one ACM move from Q (x^{±1}, y^{±1} excluded on both sides). The cheap PSL/S_n sieves are useless here (my S₅, S₆ sieve leaves 20 of 54 words, incl. x^{±1}), as TH16 says. Prop. G (P₃ is not a local minimum) — certificates replay: `th16_p3_to_len13.json` (P₃ → (yxYYXX, xxxYXyy), 23 moves), `th16_ak3_to_len13_via_p3.json` (AK(3) → same, 91 moves). |

## 8. TH17 — T(2;p,q) as killers of the trefoil group; level shifts

Self-test re-run: `th17_levels.py --selftest` passes. Certificates replayed with endpoints: `th17_c3_to_T2_4_7_one_move.json` (274 moves, (xxyXy, xy⁵xY²) → (x⁴y⁷, xxyXy)), `th17_r74member_to_T2_4_9.json` (374, (xxyXy, xy⁷xY²) → (x⁴y⁹, xxyXy)), `th17_T2_4_7_to_third_form.json` (189), `th17_T2_7_13_to_third_form.json` (574).

| claim | verdict | what I did |
|---|---|---|
| 1: dictionary — class of xᵖy^q in H = ⟨x,z \| x³z²⟩ is (k;1^q), (k;2·1^{q−1}), (k;2·1^{q−3}) for p = 3k+0,1,2 | VERIFIED (re-derived by hand from xᵖ(xz)^q, x³ = ζ, z² = ζ⁻¹) |
| 2: Lemma S (a = 2) is this necklace identity | VERIFIED |
| 3: coincidences — only the Lemma S pairs; AK(n)'s killer class (0;2ⁿ1^{n+1}) is a T(2;·) class only for n = 1; xy^{2i+1}xY² ~ x⁴y^{2i+3} | VERIFIED ((c) recomputed: ζ(xz)^{2i+2}x²z; (a), (b) are necklace comparisons; "up to automorphisms" uses Out(H) = ℤ/2, classical, quoted) |
| 4: (x²yXy, xy⁷xY²) ~AC T(2;4,9) = X — a plain AC equivalence | VERIFIED (certificate replay with endpoints + the conjugacy by hand) |
| 5: family K(a,b,c), trivial iff \|a−b+6c\| = 1 and gcd(a,b) = 1; contains AK(n) and T(2;·) | VERIFIED (own proof of the criterion: modulo ζ, uᵃ = vᵇ and vᵃ = uᵇ are central; gcd = d > 1 gives a (2,3,d) triangle quotient) |
| 6: third torus form x^{3k+1}y^q ~ (x²y)^{2k+1}(xy)^{−(q+1)} in H | VERIFIED (braid computation redone; ν(xyXyXy) = x²yXy by free reduction; two certificates replayed) |
| 7: Theorem 6 — rigidity of each level in the restricted graph 𝔖 | **not checked** (Lemmas 6.1–6.3 not verified for lack of time) — PLAUSIBLE-UNCHECKED. Correctly labelled by the note as a statement about a restricted move class, not an AC invariant. |
| 8: Prop. 5 — a uniform level shift is equivalent to AC-triviality of all members; inequivalence of two levels would disprove AC | VERIFIED (formal; level 0 has the primitive killers xy, xy³) |

## 9. TH18 — killers of BS(n,n+1); Miller–Schupp classes; generalized AK pairs

Self-test re-run: `th18_bs.py --selftest` passes. `python3 experiments/th20_th18_check.py` (own BS conjugacy code):
```
(1) n=2,3,4,5: t-length-3 killer classes with sigma=+1: 2, 6, 12, 20 (claimed n(n-1));  n=2, t-length 5: 12 + 4 = 16 classes (claimed 2n^3(n-1))
(2) T4 class formula verified for n = 2,3,4 (all residues b', c'; a in [-2,2])
(3) bridge word in C_{2n+1} and Q_gamma classes, n = 2..8;  P_beta ~ x^2 y^b X y^-b with b = beta (mod n+1), b = 1 (mod n), n = 2..7
```
All 16 `th18_*.json` certificates replay. **None is a trivialization of AK(3)**: `th18_ak3_beta1/beta2_trivialization.json` start at (xxxYYYY, xYxyXY) and (xxxYYYY, xYYxyyXY), i.e. at AK₁(3), AK₂(3) — the torus relator x³y⁻⁴ with a different partner; `th18_m3_to_ak3_via_t9.json` is M₃ → AK(3) (C's equivalence).

| claim | verdict | what I did |
|---|---|---|
| T1: killers of BS(n,n+1) are the elements with σ = ±1 (Miller–Schupp) | VERIFIED (classical proof re-derived) |
| T2: complete conjugacy invariant (sign necklace + exponents mod Λ_d), class counts | VERIFIED (lattice, determinant ∏q_i − ∏p_i, well-definedness of Britton-reducedness mod Λ_d re-derived; counts confirmed by (1)); rests on Britton/Collins (classical, quoted) |
| T3: primitive in the class ⇔ ℓ = 1 ⇔ w ~ x^{±1} | VERIFIED (own proof) |
| T4: the n(n−1) classes C_b of t-length 3 and the membership criterion | VERIFIED (own derivation: (a,b′,c′) ↦ (b′ mod n+1, c′ mod n) is a bijection on ℤ³/Λ; script (2)) |
| T5: bridge word XYx²Y ∈ C_{2n+1}; no primitive relator one ACM move from M_n | VERIFIED (class by hand and script; other direction: (x ↦ xy)(r_n) = p_n in B, by hand, then G2(b) — or TH10 Cor. 5.3) |
| T6, T6′: divisor classes are AC-trivial; sharpness for the representatives w_b | VERIFIED (both conjugations recomputed; amalgam length argument read) |
| T7: MS(2,w), ℓ ≤ 3, AC-trivial; MS(3,w), ℓ ≤ 3, AC-trivial or ~AC AK(3) | VERIFIED (residue arithmetic redone; uses C's and D's certificates) |
| T8: half classes are one ACM move from a T(2,m) pair | VERIFIED for (a) by hand; (b) read only |
| T9: MS(n,w) ~AC AK_β(n) = (xⁿy^{−(n+1)}, xy^{−β}xy^{β}x⁻¹y⁻¹) for w ∈ C_b^{±1}; AK₁(n) AC-trivial; **P2 ~AC AK₂(4) ~AC AK₋₂(5)** | VERIFIED (own derivation: modulo P_β, x⁻¹yx = y^{−β}xy^{β}, so r_n = y^{−β}p_n y^{β}; `th18_p2_to_ak_4_beta2.json`: (XyyxYYY, XXXYxxY) → (xxxxYYYYY, xYYxyyXY), 914 moves; `th18_p2_to_ak_5_betam2.json`: → (xxxxxYYYYYY, xyyxYYXY), 1,547 moves). **OVERCLAIM in wording**: the note calls AK₂(4) "a torus-knot pair" and says "P2 is a torus-knot pair". In the repository's usage (F §9: "two torus-knot relators") this is not the case: only x⁴y⁻⁵ is of torus type; the Whitehead-minimal forms of P₂ = xy⁻²xy²x⁻¹y⁻¹ are x⁻²y⁻²xy and relatives (4 syllables; my level-graph computation). Suggested wording: "P2's class contains a presentation whose first relator is the torus relator x⁴y⁻⁵ (resp. x⁵y⁻⁶); the partner is not of torus type". The note is clear that P2 remains open. |
| E3 and the survey of benchmark classes (C_{±6} of BS(4,5) trivial via L's certificates, C_{±7} open, …) | PLAUSIBLE-UNCHECKED (classes of the benchmark relators not recomputed, except D's 34 in §7) |

## 10. Certificates

52 files `certificates/th1x_*.json` existed at 04:54 UTC and are the final set: TH11 3, TH13 13, TH14 1 (rank 3, stable), TH15 13, TH16 2, TH17 4, TH18 16. All 51 rank-two files pass `experiments/elementary_verify.py` (replayed through `th20_lib.cert_info`, which calls `elementary_verify.replay` and prints start, target, moves, peak); for each I compared start and target with the presentation named in the note (targets that are automorphic images were recomputed with `th20_lib.aut`). No certificate has start AK(3) (or P₃, Q, M₃) and target (x,y).

## 11. Final re-read (05:04–05:10 UTC) and verdicts on material added after 04:54

Final versions refereed (line counts at 05:04 UTC): TH10 225, TH11 306, TH12 270, TH13 268, TH14 437, TH15 468, TH16 219, TH17 217, TH18 287. Per the coordinator, TH12, TH13, TH15, TH17, TH18 handed back final notes; TH10, TH11, TH14, TH16 stopped at 04:56–04:57 UTC (API error), so their files are their last saved versions. TH15 and TH17 did not change after my 04:54 snapshot. The set of 52 `certificates/th1x_*.json` is unchanged since 04:54 (TH11 3, TH13 13, TH14 1, TH15 13, TH16 2, TH17 4, TH18 16); all replay (§10).

| note: claim added after 04:54 | verdict | what I did |
|---|---|---|
| TH11 T11: the reflection μ = ψ∘θ₀ is realized on P₃ by three generalized moves (c-frozen rewriting k₃ → r = xxxyXYXy; one cyclic product on c giving a rotation of ψ(c); one ACM move) | VERIFIED (ACM level) | o_gc normal forms: r ≡ k₃ mod ⟨⟨c⟩⟩; nf(g r′ g⁻¹) = (a⁻²ba, 1) for g = yXYXX, r′ = xYxyXXy, and (a⁻²ba, 1) is the twisted conjugate by v = a of θ₀(k₃) = (a⁻³bab, 1); ψ(r′) ~ r and three cyclic products of c^{±1}, r^{±1} give a rotation of ψ(c) = xyxyxYXYXyx (own script). No ordinary certificate for this path; the AC equivalence P₃ ~ θ₀(P₃) itself is certified (T9). |
| TH11 cokernel table (T4), levels 5–8 | VERIFIED (see §2) |
| TH16 Theorem H (Q is an ACM local minimum) | VERIFIED (see §7) |
| TH18 T10: α = (x ↦ xy, y ↦ y⁻¹) maps c to w = x²y²x⁻¹y⁻¹; θ(P₂) = w for θ = (x ↦ xy², y ↦ y); α(k_n) = (xy)ⁿx⁻¹y⁻²; P2 ~AC (x⁻¹y⁴xy⁻⁵, w) | VERIFIED (free reductions by script, n ≤ 12; w ~ P₂ in BS(m,m+1) for m = 2..6 by my BS code, so MS(4,w) ~AC AK₂(4) ~AC P2 by T9 + certificate). The "one-move exit" part is a bounded experiment, correctly labelled. |
| TH18 wording "AK₂(4) … a torus-knot pair", "0. P2 is a torus-knot pair" (still in the final text) | **OVERCLAIM** (see §9) — only one relator is of torus type. |
| TH14 F (generator exchange "subgroup-ACM": AK(3) ~₁ V_k = (x³zx⁻⁴z⁻¹, xzx^{4k+1}z⁻²), stable) and F-exp (V_k in AK(3)'s ordinary class for \|k\| ≤ 2, engine collisions, no certificates) | F: VERIFIED (proof read; application re-derived by hand: in ⟨x,y \| x³ = y⁴⟩, w = x^{3i+1}y^{4j+1} ≡ (central)·xy, so y⁻¹·wxw⁻¹ = y⁻¹(xy)x(xy)⁻¹ is a rotation of b; V = (x³zx⁻⁴z⁻¹, z⁻¹x^{3i+1}zx^{4j+1}z⁻¹) and x^{3i}z ≡ zx^{4i} give V_k; same for AK(n)). **Stable** statement, correctly labelled. F-exp: experiment, not re-run (no certificates, so "V_k in AK(3)'s ordinary class" is unverified). |
| TH14 E-exp (no E1/E2 hits among 47 known members) | experiment, not re-run |
| TH12 §4.6 sharpness: d_F(V_n) ∈ {2n+1, 2n+2} for V_n = (xⁿY^{n+1}, xY), explicit (2n+2)-instruction path | VERIFIED for the upper bound (the 2n+2 instructions replayed by my own code, n = 2..40) and for the lower bound 2n+1 (same arguments as Thms 3–4, read); the BFS values d_F(V_n) = 2n+2, n ≤ 4, not re-run. It shows Theorems 3–4 are sharp up to 1 on an AC-trivial family with AK(n)'s exponent matrix. |
| TH16 T8 (P₃ is not a local minimum: y⁻¹cy = yxy⁻²x⁻² in G_{k₃}) | VERIFIED (equal normal forms in my own F₃ ⋊ ℤ model of G_{k₃}; certificate replays; target (yxYYXX, xxxYXyy) = θ(Q) up to rotation/inversion, θ = (x ↦ x⁻¹), checked) |
| TH16 T1, added clause "C′(1/4)–T(4) forces \|r\| ≤ 2 or ≥ 9" | VERIFIED by brute force (no non-power cyclically reduced word of length 3–8 has C′(1/4) and a triangle-free star graph; T(4) tested through the star-graph criterion that TH16 quotes) |
| TH13 Remark (iv) of §3 (no literal Wirtinger relator of T(p,p+1), p ≥ 3; uses bridge numbers, cited from memory) | PLAUSIBLE-UNCHECKED (external facts) |
| TH10 `--mechanism` replay (1,374 epimorphisms onto small groups) | experiment, self-test re-run passes; not counted as verification |


## Coordinator's note (2026-11-09, Los Angeles time)

This referee was interrupted by the usage-credit stop at about 04:56 UTC and resumed on another model at 05:05 UTC with its saved transcript; it read the final or last-saved versions of TH10–TH18 as of 05:04 UTC (line counts listed above). Its two findings are recorded in the coordinator's checks of research-th18 (the "torus-knot pair" wording) and research-th14 (Lemma C's hypothesis in the claims table; F-exp unverified); its remark on an earlier TH11 draft is recorded in research-th11. The coordinator found no disagreement between these verdicts and the coordinator's own checks of TH12, TH13, TH15, TH17 and TH18. "VERIFIED" here means re-derived or independently recomputed by the referee, as defined at the top; it is the referee's judgement, not a formal proof check.
