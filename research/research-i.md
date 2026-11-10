# Research I: shared-vertex torus-knot pairs, meridional partners, and merging the residual frontier

Date: 2026-11-02. Independent research agent I (round 3).

**Status:** final for this round; partial results. Every positive claim is either proved symbolically or backed by a replayable certificate. **No AC trivialization of AK(3), no proof of non-triviality, no counterexample, no resolution of the AC conjecture.** Novelty is **not established** for any item.

| # | statement | label |
|---|---|---|
| 1 | **Prop. M**: let one relator be (an Aut(F₂)-image of) a torus relator x^m y^n with n ≡ ±1 (mod m) or m ≡ ±1 (mod n), for example min(\|m\|,\|n\|) ∈ {2,3,4,6}. If the partner has cyclic syllable length 2 in C_m*C_n, the presentation is AC-trivial | proved here (§3) |
| 2 | On the meridian route (research-f §8, agent G), a state of AK(n)'s, C3's or C6's class that has meridian defect 2 through a relator of a qualifying torus type (T(2,k), T(3,k), T(4,k), T(k,k±1), …) is already an AC trivialization; no thickenability test is needed | proved here (Cor. M1) |
| 3 | **Lemma S**: T(a; 1+mk, q) ~AC T(a; mk+m−1, q+2) for all integers a, q and all k ≥ 0, where m = a+1 and T(a;p,q) := (x^p y^q, x^a y x⁻¹ y) | proved here (§4); 2,898 generated certificates replayed |
| 4 | **Prop. G**: if \|2p−(a−1)q\| = 1, then T(a;p,q) presents 1 iff gcd(p,a+1) = 1 or \|q\| = 1; otherwise it maps onto a von Dyck group ≠ 1 | proved here (§2) |
| 5 | **Lemma E**: (x^m y^n, x^p y^q) with mq−np = ±1 is AC-trivial | proved here (§2); 744 certificates replayed |
| 6 | **Aut(F₂) is AC-realized on the AC classes of C3, P1 (= C6), P2 and R9** | proved here: 12 certificates + the argument of research-d Lemma D6 (§5, §7) |
| 7 | **P1 ~AC C6** | external ledger, converted and re-verified here (§5) |
| 8 | **Ten published residual components (nahomar, cap-28 search, `trivial=0`) certified into fewer classes.** Into frontier classes: R212 ~AC AK(3); R327 ~AC C3; R28 ~AC P1 = C6; R82, R86 ~AC P2. Among themselves: R22, R69, R111, R114, R223 ~AC R9, so these six components form one AC class | proved here by composite certificates (Aut-orbit match + automorphism transport), §5, §7 |
| 8b | Modulo Aut(F₂), the 287 published non-trivialized residual components fall into 167 groups at cap 25; with the certificates, at most 166 independent AC-triviality questions remain | experiment (§7) |
| 9 | Certified family members: C3 ~ T(2;4,7) ~ T(2;5,9) ~ T(6;8,3); C4 ~ T(4;8,5); T(2;4,9) ~ T(2;5,11) ~ σT(8;10,3); T(4;4,3), T(−4;7,−3), T(−4;8,−3) and T(−6;11,−3) are AC-trivial | certificates (§1, §3, §5) |
| 10 | Bounded Aut-orbit separation of AK3, P1=C6, P2, C3, C4, X = [T(2;4,9)] and Y = [T(4;7,5)]; none of them meets 1.43M published AC-trivial presentations up to Aut(F₂) | experiment (§6) |
| 11 | Up to Aut(F₂): R62, R74 and X have the same AC-triviality status; so do R32, R134 and Y | experiment + Lemma D2 (§7) |
| 12 | **Prop. C**: an AC-trivial class is closed under Aut(F₂). C4, X and Y show no automorphic image of themselves up to caps 31, 29 and 31, while AK3, C3, P1 and P2 show all generator images at barrier ≤ 23. So C4 ≁AC σ(C4) for one signed permutation σ would make C4 a counterexample | Prop. C proved; data experimental (§5) |


## 0. Previous work read and choice of direction

I read `README.md` and `research/research-{a,b,c,d,e,f}.md` in full and skimmed `experiments/` and `certificates/`. I re-ran `python3 experiments/elementary_verify.py --selftest` (it passes). I reused D's engine `experiments/d_acsearch.cpp`, D's `d_certify.py`, F's `f_descent.py`/`f_thicken.py`, and the public clones that D and F left in the shared scratch area: nahomar/andrews-curtis-solver, alejandrozarco/andrews-curtis-ms14 and the ACSolverX data. The round-2 summary in my brief is accurate. In particular, F observed that the length-14 frontier splits into BS-type classes (P1, P2, MS) and torus-knot-pair classes (AK3, C3, C4, C6), and that C3's class contains (x⁴y⁷, x²yx⁻¹y) and (x⁵y⁹, x²yx⁻¹y).

**Direction (other families / counterexample side).** A torus-knot pair has two relators that are torus relators u^p v^q in two bases of F₂. By Nielsen, the kernel of Aut(F₂) → GL₂(ℤ) is Inn(F₂), so a basis up to simultaneous conjugation is an oriented Farey edge, and a pair is described by two Farey edges and their exponents. The simplest non-degenerate configuration has **two bases sharing a primitive element**. With z = x⁻¹y,

    T(a;p,q) = (x^p y^q, x^a y x⁻¹ y) = (x^p (xz)^q, x^(a+1) z²)    (free words)

uses the bases (x, xz) and (x, z). F's C3 and C4 states lie in this family; AK(n)'s two bases share no primitive. Same-basis pairs are AC-trivial (Lemma E).

My plan had three parts:
1. map the family exhaustively at small length;
2. prove uniform statements about it;
3. use the structure to merge frontier classes.

Part 3 led to a second, more consequential line. D's Aut-orbit test (research-d Cor. D7) needs Aut(F₂) to be AC-realized on a class. I proved that it is, on C3, P1 and P2, and this turned Aut-orbit matches into genuine AC equivalences between published residual classes (§5, §7). The work is disjoint from G (AK(3) meridian search) and from H (obstructions), and Prop. M feeds directly into G.

**Notation.** X = x⁻¹, Y = y⁻¹; m = a+1; c = x^m; z = Xy. The free-word identities x^a yXy = c z z and x^p y^q = x^p (xz)^q hold letter for letter after free reduction. An **ACM move** replaces r_i by any word representing a conjugate of r_i^{±1} in F/⟨⟨r_j⟩⟩. It is a composite of ordinary AC moves: conjugate r_i, then right-multiply by the finitely many factors h r_j^{±1} h⁻¹ of a witness, each factor applied as "conjugate r_j by h, multiply, conjugate back".

## 1. Experiments that located the structure (D's engine, full cyclic-product graph)

`d_acsearch` explores the Σ-quotient graph of cyclic products in barrier order and reports source collisions and primitive relators (research-d §2). I compiled it from `experiments/d_acsearch.cpp` and ran one core per job with `--maxstates` ≤ 4·10⁷. Exact commands are in §8.

- **Multi-source run, cap 24.** Sources: C3, C4, AK3, T(2;4,7), T(2;4,9), T(2;5,9), T(4;7,5), T(2;5,11). The run explored 2,579,273 states and completed. Collisions: C3–T(2;4,7) at barrier 16, T(2;4,7)–T(2;5,9) at 19, C3–T(2;5,9) at 22, T(2;4,9)–T(2;5,11) at 21. No primitive relator appeared.
- **Multi-source run, cap 25.** Sources: T(2;5,11), T(8;10,3), T(6;8,3), C4, T(4;7,5), T(4;8,5), C3, AK3. The run explored 9,250,978 states and completed. Collisions: T(6;8,3)–C3 at 20, C4–T(4;8,5) at 20.
- **Signed-permutation matching** (`--trivial-targets`, which matches up to Σ and the 8 signed letter permutations): T(8;10,3) is a signed-permutation image of a state of T(2;5,11)'s cap-25 component (barrier 25).
- **Single-source triviality probes** on all 34 trivial-group members of length ≤ 24 for a ∈ {±2,…,±12}. Each probe used cap max(22, min(L+5, 25)) and stopped at the first primitive relator.
  - Reach a primitive relator: every member of length ≤ 13, and T(4;4,3), T(−4;7,−3), T(−4;8,−3), T(−6;11,−3).
  - Do not (runs complete to the cap): T(2;4,7), T(2;4,9), T(2;5,9), T(2;5,11), T(4;7,5), T(4;8,5), T(6;8,3), T(8;10,3).

Three patterns stood out:
1. The long members that were trivialized are exactly those whose partner is *meridional*; this led to Prop. M.
2. The T(2;·) collisions pair p = 3k+1 with p = 3k+2; this led to Lemma S.
3. Members with a nontrivial group sit exactly where gcd(p, a+1) > 1; this led to Prop. G.

## 2. The family T(a;p,q): group triviality, and the same-basis case

**Prop. G (proved here).** Let G = ⟨x,y | x^p y^q, x^a yXy⟩.
1. G^ab = 0 iff |2p − (a−1)q| = 1. In that case a is even and q is odd, so m = a+1 is odd.
2. Assume |2p−(a−1)q| = 1. If gcd(p, m) = 1 or |q| = 1, then G = 1. If d = gcd(p,m) > 1 and |q| ≥ 2, then G maps onto the von Dyck group D(d,2,|q|) = ⟨s,t | s^d, t², (st)^|q|⟩ ≠ 1.

*Proof.* Part (1) is the exponent-sum determinant. For part (2):
- In G, x^p = y^{−q} commutes with x and with y, so it is central.
- Since x^a yXy = c z², we have x^m = z^{−2}. It commutes with x and with z, hence with y = xz, so it is central too.
- If gcd(p,m) = 1, then x ∈ ⟨x^p, x^m⟩ is central. So G = ⟨x,y⟩ is abelian and G = G^ab = 1.
- If |q| = 1, then x^p y^{±1} is primitive. So G is a quotient of ⟨x,y | x^p y^{±1}⟩ ≅ ℤ by a relator whose image is ±1 by (1), and G = 1.
- If d > 1, adding x^d = 1 kills x^p and x^m and leaves ⟨x,z | x^d, z², (xz)^q⟩. A von Dyck group whose three orders are all ≥ 2 is nontrivial: each generator has exactly its given order (classical). ∎

This agrees with coset enumeration (`f_descent.is_trivial_group`) on every member in §1. For example, T(2;3,5), T(4;5,3), T(−4;12,−5) and T(−6;10,−3) are nontrivial.

**Lemma E (proved here; probably folklore).** If mq − np = ±1, then (x^m y^n, x^p y^q) ~AC (x, y).

*Proof.* Put r₂ = x^p y^q.
- r₁·r₂⁻¹ = x^m y^{n−q} x^{−p}, which is conjugate to x^{m−p} y^{n−q}.
- r₁·(y^q x^p), where y^q x^p is a rotation of r₂, is conjugate to x^{m+p} y^{n+q}.

So "rotate, multiply by a rotation of r_j^{∓1}, cyclically reduce" performs the row operation r_i ← r_i ± r_j on the exponent matrix, and both relators keep the form x^e y^f. Row operations of this kind reduce every matrix of GL₂(ℤ) to a signed permutation matrix (Euclid on the first column, then clear the second). That leaves (x^{±1}, y^{±1}) up to order, and inversions plus a swap finish. ∎

`euclid_cert` in `experiments/i_torus.py` implements a greedy variant; its self-test replays all 744 instances with entries in [−6, 6]. So the Farey position of the two bases matters: same-basis pairs are always trivial, while the shared-vertex family already contains the frontier classes C3 and C4.

## 3. Meridional partners are AC-trivial (Prop. M)

**Prop. M (proved here).** Let |m|,|n| ≥ 2 be coprime, R = x^m y^n and H = F/⟨⟨R⟩⟩. Then Z(H) = ⟨x^m⟩ and H/Z(H) ≅ C_|m| * C_|n|; write s, t for the images of x, y. Let w be a word such that ⟨x,y | R, w⟩ = 1 and the image of w in C_|m|*C_|n| has cyclic syllable length 2. If n ≡ ±1 (mod m) or m ≡ ±1 (mod n), then w is conjugate in H to a primitive word of the form x^{±1} y^j or x^i y^{±1}. Consequently (R, w) is AC-trivial.

*Proof.*
1. A cyclically reduced element of syllable length 2 in a free product is conjugate to some s^i t^j with s^i ≠ 1 ≠ t^j.
2. Lift to H: w = g x^i y^j ζ g⁻¹ with ζ ∈ ⟨x^m⟩ central. So w is conjugate to x^{i'} y^j for some i' ≡ i (mod m).
3. As free words, x^{i'+m} y^{j+n} = x^{i'} · (x^m y^n) · y^j, which equals x^{i'} y^j in H. So every pair (i'+lm, j+ln) represents the same element.
4. Map H → H^ab = ℤ by x ↦ n, y ↦ −m. Since ⟨R, w⟩ is trivial, n i' − m j = ±1.
5. If n ≡ ε (mod m) with ε = ±1, then i' ≡ ±ε (mod m), so some representative has x-exponent i'+lm = ±1. If instead m ≡ ±1 (mod n), the same argument gives some j+ln = ±1.
6. Either way, w is conjugate in H to x^{±1} y^{j'} or x^{i''} y^{±1}. That word is primitive in F: it forms a basis together with y (resp. x).
7. The ACM move (R, w) → (R, π) to this primitive word π is a composite of ordinary AC moves, and a trivial-group presentation with a primitive relator is AC-trivial (research-d Lemma D3). ∎

The congruence holds automatically when min(|m|,|n|) ∈ {2,3,4,6}, because every unit mod 2, 3, 4 or 6 is ±1. It first fails for pairs such as (5,7) and (5,8). Since AC-triviality is Aut-invariant (research-d Lemma D2), Prop. M applies to any relator that is, up to conjugacy and inversion, an Aut(F₂)-image φ(x^m y^n); test φ⁻¹ of the partner. The syllable-length test is F's "meridian defect" (research-f Prop. F3, `f_knotlike.meridian_test`).

**Corollary M1.** In AK(n), both relators qualify: T(2,3), and T(n,n+1) because n+1 ≡ 1 (mod n). So any state of AK(n)'s AC class whose torus relator is an Aut-image of one of these, with meridian defect 2, is an AC trivialization. The ACM step to a primitive word is explicit, and no thickenability test or Lackenby's theorem is needed. The same holds for every relator type that occurs in the known states of C3 (T(2,3), T(2,7), T(4,7), T(5,9), T(7,2), T(8,3)) and of C6 (T(2,3)), and for C4's representative relators (T(2,5) twice). By contrast, T(5,8) (the relator x⁸y⁵ of C4 ~ T(4;8,5)) fails the congruence, so Prop. M does not cover it. F3 shows that thickenable ⇒ defect 2; for the qualifying types, defect 2 alone already suffices.

**Instances.** Each certificate below was found by F's strict ACM descent; by Prop. M a strictly shortening first step exists for the meridional ones.

| presentation | why it qualifies | certificate | moves | peak |
|---|---|---|---:|---:|
| T(4;4,3) = (x⁴y³, x⁴yXy) | torus relator x⁴y³; partner ↦ s⁻¹t² in C₄*C₃ | `certificates/i_triv_T4_4_3.json` | 31 | 19 |
| T(−4;7,−3) = (x⁷Y³, X⁴yXy) | torus relator X³z²; partner of syllable length 2 in C₃*C₂ (p ≡ 1 mod 3) | `certificates/i_triv_Tm4_7_m3.json` | 43 | 22 |
| T(−6;11,−3) = (x¹¹Y³, X⁶yXy) | torus relator X⁵z²; partner of syllable length 2 in C₅*C₂ (p ≡ 1 mod 5) | `certificates/i_triv_Tm6_11_m3.json` | 43 | 30 |
| T(−4;8,−3) | not meridional | `certificates/i_triv_Tm4_8_m3.json` (engine path to a primitive relator, then descent) | 76 | 31 |

In T(a;p,q), the partner x^p (xz)^q of the T(m,2) relator has syllable length 2|q|. It is 2|q|−4 instead when p+1 ≡ 0 (mod m) for q > 0, or when p−1 ≡ 0 (mod m) for q < 0. So meridional members need |q| = 3 together with that congruence. Combined with the determinant condition, this leaves only the sporadic members above; inside this family, Prop. M yields isolated cases rather than an infinite subfamily.

## 4. Lemma S: a uniform equivalence inside every T(a;·)

**Lemma S (proved here).** For all integers a, q and every k ≥ 0, with m = a+1,

    T(a; 1+mk, q) ~AC T(a; mk+m−1, q+2).

The sequence keeps A = x^a yXy fixed and inserts conjugates of A^{±1} 2k+1 times.

*Proof (explicit free-group derivation).* Write B = x^{1+mk} y^q. Below, "=" means free equality. Each step either inserts a conjugate h A^{±1} h⁻¹ into the first relator (an AC composite: right multiplication by that conjugate, with h chosen to place it), or rotates the first relator (conjugation).
1. Rotate: B → y^q x^{1+mk} = P · z · c^k, where P := y^q x z⁻¹ (because z⁻¹z = 1).
2. For j = 0, …, k−1: change P c^j · z c · c^{k−j−1} into P c^j · c z · c^{k−j−1} by inserting the commutator [c,z] = c z c⁻¹ z⁻¹. As a free word this equals A · z A⁻¹ z⁻¹, because A = c z². After k steps the relator is P c^k z.
3. Rotate (conjugate by z): z P c^k = z y^q x z⁻¹ c^k.
4. Insert z A z⁻¹ = z c z in front of z⁻¹: z y^q x (z c z) z⁻¹ c^k = z y^q x z c^{k+1} = X y^{q+2} x^{m(k+1)}.
5. Rotate to x^{mk+m−1} y^{q+2}. ∎

**Remark (proof sketch).** For a = 2, x²yXy is the braid relator in the basis (u,v) = (xy, y⁻¹), and T(2;p,q) = (braid(u,v), (uv)^p v^{−q}). Fix A and work in C_m*C₂ with x ↦ s, z ↦ t. A member with q ≥ 3 has image s^{p+1} t (st)^{q−1}, whose s-exponent necklace is [p+1, 1^{q−1}] if p+1 ≢ 0 and [2, 1^{q−3}] otherwise. Conjugacy in H_A is decided by this necklace (up to inversion) together with the abelianization. Hence, for members with q ≥ 3, the pairs of Lemma S are the only conjugacies with A fixed, and the family cannot be collapsed further by moves that change only the first relator.

**Generated certificates.** `python3 experiments/i_torus.py --sweep` builds and replays the strict certificate for every a ∈ [−10,10], k ∈ [0,5], q ∈ [−11,11]. All 2,898 certificates are accepted by `elementary_verify.replay`; the longest has 736 moves. Two instances are stored: `certificates/i_lemmaS_T2_4_7_to_T2_5_9.json` (44 moves, peak 29; inside C3's class) and `certificates/i_lemmaS_T2_4_9_to_T2_5_11.json` (46 moves, peak 31; inside X).

**Consequence.** For a = 2, the trivial-group members with q ≥ 1 are T(2; 3k+1, 6k+2∓1) and T(2; 3k+2, 6k+4∓1); p = 3k+3 gives nontrivial groups. Lemma S pairs these off, so T(2;·) has at most two AC classes per level k. Level 0 is trivial and level 1 is {C3, X}. Whether the levels k ≥ 2 give new classes is open (§9).

**Experiment (level 2).** T(2;7,13) (length 25) and T(2;7,15) (length 27) were tested at cap 28; their components have 93,202 and 10,706 states.
- Neither contains a primitive relator.
- Neither shares an Aut-orbit with C3 (cap 26), X, AK3, C4 or Y (cap 28).
- **Their minimal Aut-lengths are 19 and 21**, compared with 14 for C3 and 15 for X at level 1.

This is consistent with each level k being a separate class whose shortest representatives grow with k; that would be an infinite family of candidate AC-distinct presentations. It is heuristic only: the capped components see only a small part of each class.

## 5. Certified merges and Aut(F₂)-realizations

Every file below passes `python3 experiments/elementary_verify.py <file>`; the outputs are listed in §8.

**P1 ~AC C6.** The repository alejandrozarco/andrews-curtis-ms14 (commit a6c67b9; AI-produced, unreviewed) publishes a 1,066-move integer ledger from P1 to the rotation/inversion orbit of C6. I converted it with `python3 experiments/i_words.py --zarco`. The converter expands the ledger's `cycle` moves into single-letter conjugations and its negative multiplications into invert–multiply–invert, then normalizes to the exact C6 words. Result: `certificates/i_p1_to_c6.json`, from P1 = MS(2, x⁻²y⁻¹x²y) = (XyyxYYY, XXXYxxy) to C6 = (xxyxxYY, xyXYYXy), 1,091 strict moves, peak 41. Label: **externally reported, independently re-verified here.** As a positive control, the Aut-orbit comparison of §6 independently finds 4,923 shared Aut-orbits between the cap-28 components of C6 and P1. The length-14 frontier therefore has at most five classes: AK3, P1 = C6, P2, C3 and C4. Their pairwise separation is only bounded (§6).

**New certified class members.** Engine paths, compiled by D's `d_certify.py` through `experiments/i_certify.py`:

| certificate | from → to | moves | peak |
|---|---|---:|---:|
| `i_c3_to_T2_4_7.json` | C3 → (x⁴y⁷, x²yXy) | 36 | 39 |
| `i_T6_8_3_to_c3.json` | (x⁸y³, x⁶yXy) → C3 | 161 | 29 |
| `i_c4_to_T4_8_5.json` | C4 → (x⁸y⁵, x⁴yXy) | 40 | 49 |
| `i_T2_5_11_to_sigmaT8_10_3.json` | (x⁵y¹¹, x²yXy) → (x³Y¹⁰, xyxY⁸) = σT(8;10,3), with σ: x↦Y, y↦x | 339 | 36 |

So C3's class contains torus-knot pairs of the types {T(3,2), T(4,7)}, {T(3,2), T(5,9)} and {T(7,2), T(8,3)}. X's class contains {T(3,2), T(4,9)} and {T(3,2), T(5,11)}, and, after σ, {T(9,2), T(10,3)}. The apparent duality T(m−1;m+1,q) ↔ T(q−1;q+1,m) is not a family: the determinant forces (m−2)(q−2) ∈ {5,7}, which leaves only the two instances (m,q) ∈ {(3,7),(3,9)}.

**Aut(F₂) is AC-realized on the classes of C3, P1 and P2 (proved here).** Take P ∈ {C3, P1, P2} and a Nielsen generator φ ∈ {x↔y, x↦x⁻¹, x↦xy}. The exact cyclic reduction of φ(P) lies in P's own component: at cap 26 for C3, cap 27 for P1, cap 26 for P2. In fact all seven maps of research-d §4.5 were found for P1 and P2, and six of the seven for C3. The certificates are `certificates/i_{c3,p1,p2}_aut_{swap,invx,x_xy}.json` (26–366 moves, peaks 25–36).

These three maps generate Aut(F₂). The induction of research-d Lemma D6 therefore gives P ~AC φ(P) for every φ ∈ Aut(F₂). The property also holds for every presentation Q AC-equivalent to P: φ(Q) ~ φ(P) ~ P ~ Q.

Moreover, Aut-orbit links compose. Suppose A ~ φ₁(C₁), C₁ ~ φ₂(C₂), …, C_k ~ φ(P). Transporting each link by the automorphism accumulated so far gives A ~ φ₁⋯φ(P) ~ P. Hence **any chain of Aut-orbit matches that ends in the class of AK3, C3, P1 = C6 or P2 is an ordinary AC equivalence.**

`experiments/i_transport.py` makes this explicit. It recovers an automorphism by Whitehead reduction and a BFS through minimal pairs, builds the realization P₀ → φ(P₀) from the transported generator certificates, appends the transported engine path φ(P₀) → φ(s), glues to the exact residual words, and reverses the result. Its self-test runs a synthetic merge on AK(3) using D's certificates.

For C4 and Y, none of the seven automorphic images of the representative occurs in its own component even at cap 31, the engine's encoding limit (3,054,469 and 2,045,223 states). For X none occurs even at cap 29 (11,358,907 states). C6's own component contains no image by cap 28, but C6 inherits Aut-realization from P1. So for C4, X and Y an Aut-orbit match only shows that the two presentations have the same AC-triviality status (Lemma D2). The contrast with AK3, C3, P1 and P2, where every generator image appears at barrier ≤ 23, is itself an observation worth testing further; it is not an obstruction.

**Prop. C (proved here; elementary) and a chirality target for the counterexample side.** If P is AC-trivial, then P ~AC φ(P) for every φ ∈ Aut(F₂): P ~ (x,y) gives φ(P) ~ (φ(x), φ(y)), which is a basis and hence ~ (x,y) by Nielsen moves. So **closure of the AC class under Aut(F₂) is a necessary condition for AC-triviality.** For instance, a single proof that C4 ≁AC σ(C4) for one signed permutation σ (x↔y, x↦x⁻¹ or y↦y⁻¹) would show that C4 is a counterexample to the AC conjecture. C4, X, Y and R9 all present the trivial group: by Prop. G for X and Y, and by coset enumeration for C4 and R9.

The data separate the frontier classes on exactly this point (experiment):
- AK3, C3, P1 and P2 contain the images under all three Nielsen generators at barrier ≤ 23. The barriers of swap / invx / x_xy are: AK3 15/19/17 (research-d), C3 19/19/20, P1 14/21/18, P2 23/23/19.
- C4, X and Y contain none of the seven images of research-d §4.5 up to caps 31, 29 and 31 (3.05M, 11.4M and 2.05M states).

This is not evidence of non-triviality: C4's component is very thin, and the images may simply lie higher. It does give the obstruction side (agent H) a sharper target than "distinguish from (x,y)": an AC invariant that is sensitive to orientation or chirality and separates C4 (or X, or Y) from one automorphic image. Any invariant of that kind must vanish on Aut-closed classes such as AK(3)'s, and it cannot factor through the group or through finite quotients (research-b).

**Published residual classes merged into the frontier (proved here; composite certificates).** Each certificate goes from the published seed of a nahomar residual component (`residual_components16_c28.txt`, flagged `complete=1 trivial=0`) to the exact frontier representative.

| certificate | published component (seed, length) | class | moves | peak |
|---|---|---|---:|---:|
| `i_R327_to_c3.json` | R327 (xxyXYXy, xyXyyyyXy), 16 | C3 | 1,848 | 59 |
| `i_R28_to_p1.json` | R28 (xyxYXY, xxxYxYYxY), 15 | P1 = C6 | 3,592 | 97 |
| `i_R82_to_p2.json` | R82 (xxyXyXY, xxyyyXyy), 15 | P2 | 11,623 | 63 |
| `i_R86_to_p2.json` | R86 (xxyXyXY, xxYYXYYY), 15 | P2 | 19,603 | 81 |

In the published cap-28 search (which works modulo Σ and signed letter permutations) these four are separate components from their classes. My certificates route through an automorphism, so their peaks (59–97) exceed the search caps. For R28 I also checked that its exact cap-28 component (511,868 states) does not meet the cap-28 components of C6 or P1. For R82, R86 and R327 I did not test whether a direct connection exists at cap ≤ 28.

## 6. Aut-orbit separation of the frontier classes (experiment)

Components in the full cyclic-product graph, computed with D's engine. Each is complete to its cap and contains no primitive relator.

| class | cap | states |
|---|---:|---:|
| C3 | 26 | 6,674,326 |
| C4 | 28 | 216,640 |
| C6 | 28 | 201,183 |
| X = [T(2;4,9)] | 28 | 3,260,279 |
| Y = [T(4;7,5)] | 28 | 136,468 |
| AK3 (D's dump) | 28 | 69,190,160 |
| P1 (D's dump) | 28 | 5,445,188 |
| P2 (D's dump) | 28 | 15,040,328 |

Each component was reduced to Whitehead-canonical Aut(F₂)-orbits with `d_acsearch --autmatch … --autdump`.

- **Orbit counts.** C3 627,696; C4 101,941; C6 84,767; X 1,392,756; Y 67,499. From D: AK3 6,347,128; P1 464,015; P2 1,255,335. The minimal Aut-length is 14 for C3, C4 and C6, and **15 for X and Y**.
- **Published AC-trivial presentations.** These are AC-19, AC-19-ext (non-MS rows) and AC-1M, 1,432,816 presentations in total, Whitehead-reduced. **There are 0 matches** for C3, C4, C6, X and Y. Any match would have trivialized the class (Lemma D2).
- **Pairwise comparison** with `--autcompare`: 25 pairs here, plus D's 3 pairs among AK3, P1 and P2. **There are 0 common orbits, except for C6–P1 (4,923)**, which is the certified equivalence P1 ~ C6.

- **Higher caps** (`experiments/i_hicap_compare.txt`):

  | class | cap | states | Aut-orbits |
  |---|---:|---:|---:|
  | C4 | 31 | 3,054,469 | 1,451,137 |
  | Y | 31 | 2,045,223 | 1,015,056 |
  | X | 29 | 11,358,907 | 4,803,344 |

  Cap 31 is the engine's encoding limit. Against the datasets there are 0 matches. Against AK3 (28), C3 (26), P1 (28), P2 (28) and each other there are 0 common orbits. As positive controls, every cap-28 orbit of each class is recovered at the higher cap. The minimal Aut-length stays 14 for C4 and 15 for X and Y.

Interpretation. No state of C3's cap-26 component is an automorphic image of a state in the cap-28 component of AK3, P1 or P2, and the same holds for the other pairs. Because Aut(F₂) is AC-realized on AK3 (D), C3, P1 and P2, any such match would have proved an AC equivalence; none occurs at these caps. In particular, C4, X and Y are not linked to the Aut-realized classes AK3, C3, P1 or P2 by any cyclic-product path whose peak is ≤ 31 (≤ 29 for X) on their side and ≤ 26–28 on the other side, even after an automorphism. This is a bounded search result, not an invariant.

## 7. The published residual landscape modulo Aut(F₂) (experiment, plus certificates for the genuine merges)

nahomar/andrews-curtis-solver publishes 838 residual classes of length 13–16, and also a component file (`residual_components16_c28.txt`). The component file lists 335 components of the cap-28 search, which works modulo Σ and the signed letter permutations; 287 of them are flagged `trivial=0`. Its seeds have lengths 13 (1), 14 (5), 15 (71) and 16 (210).

`experiments/i_landscape.py` computes, for each of these 287 components and for X and Y, the component in D's full cyclic-product graph to total length CAP. It reduces every state to its Whitehead-canonical Aut(F₂)-orbit and unions components that share an orbit.

Sharing an orbit means that a state of one component is an automorphic image of a state of the other. By Lemma D2 the two are then simultaneously AC-trivial or not. If the union-find group contains AK3, C3, P1 or P2, all of its members are ordinary-AC-equivalent to that class (§5). Raw output: `experiments/i_landscape_cap22.txt`.

**Cap 22** (545,966 states in total, all components complete, no primitive relator anywhere; `experiments/i_landscape_cap22.txt`):
- **The 289 components fall into 173 groups**, of which 68 contain more than one component.
- Groups with an Aut-realized member: **{AK3, R212}** and **{C3, R327}**.
- Other groups include {C6, R28}, {R82, R86}, {R62, R74, X} and {R32, R134, Y}. The largest is {R14, R59, R68, R108, R172, R272, R277}.

**Cap 25** (14,005,468 states in total, no component hit the 6·10⁶-state budget, no primitive relator anywhere; `experiments/i_landscape_cap25.txt`):
- **The 289 components fall into 167 groups**, of which 67 contain more than one component: 38 groups of size 2, 14 of size 3, 9 of size 4, 2 of size 5, 3 of size 6 and 1 of size 7.
- Groups with an Aut-realized member: **{P1, C6, R28}**, **{AK3, R212}** and **{C3, R327}**.
- {R82, R86}, {R62, R74, X} and {R32, R134, Y} stay as at cap 22.

**Genuine new AC equivalences, certified.** These are the four certificates of §5, plus:

| certificate | published component (seed, length) | class | moves | peak |
|---|---|---|---:|---:|
| `i_R212_to_ak3.json` | R212 (xxyxyXY, xxxyyyxxY), 16 | **AK(3)** | 611 | 49 |

So R212 is one more published residual class that lies in AK(3)'s AC class. The certificate starts at the published seed and ends at the exact pair (x³y⁻⁴, xyxy⁻¹x⁻¹y⁻¹).

**Larger components.** Matching the Aut-realized components at higher caps (C3 at cap 26; P1, P2 and AK3 at cap 28, D's dumps) against all 838 residual representatives with `experiments/i_residual_merge.py`:
- C3 meets labels C3 and R327.
- P1 meets P1, C6 and R28.
- P2 meets P2, R82 and R86.
- C4 meets only C4; C6 meets C6 and R28; X meets R62 and R74; Y meets R32 and R134.
- AK3 (D's cap-28 dump, 69,190,160 states) meets only the labels AK3 and R212. So, up to Aut(F₂) and within these caps, R212 is the only published residual class outside nahomar's AK3 component that falls into AK(3)'s class.

**Which published seeds are Aut-closed (cap 25).** `experiments/i_autreal_sweep.py` asks, for each of the 287 seeds, whether the exact cyclic reductions of swap(P), invx(P) and x_xy(P) lie in P's own cap-25 component (`experiments/i_autreal_sweep_cap25.txt`).
- **All three are found for 6 seeds: AK3, C3, P1, P2, R9 and R24.** R24 = (xyxYXY, x⁵y⁻⁴) is an image of AK(4); this agrees with Panteleev–Ushakov's theorem for AK(n).
- 13 further seeds have one or two of the three images (9 only swap, 1 swap and x_xy, 3 only x_xy).
- 268 seeds have none at cap 25. With only 9–12 letters of excursion above the seed length, this is weak information.

Combined with the cap-25 groups, four multi-member groups contain an Aut-closed seed, and are therefore single AC classes: {P1, C6, R28}, {AK3, R212}, {C3, R327} and **{R9, R22, R69, R111, R114, R223}**. All five members of the last group share Aut-orbits *directly* with R9's cap-25 component (744,424 states; 249, 57, 6, 5,299 and 40 common orbits). I certified every link:

| certificate | published seed | → | moves | peak |
|---|---|---|---:|---:|
| `i_r9_aut_{swap,invx,x_xy}.json` | R9 (xxyxYY, xxxxYXYXy) | cyc φ(R9) | 475 / 593 / 470 | 33 / 36 / 33 |
| `i_R22_to_r9.json` | R22 (xxyXYY, xxxYYXYxY) | R9 | 47,437 | 144 |
| `i_R69_to_r9.json` | R69 (xxyxyXY, xyyyxYxY) | R9 | 23,139 | 101 |
| `i_R111_to_r9.json` | R111 (xxxxyyy, xxyxyXYxy) | R9 | 37,269 | 167 |
| `i_R114_to_r9.json` | R114 (xxxyxyy, xxyXyxyxY) | R9 | 8,161 | 50 |
| `i_R223_to_r9.json` | R223 (xxyxyXY, xyyxyyxYY) | R9 | 26,376 | 113 |

Each R_i → R9 certificate is built in three steps:
1. an engine path R_i → r (cap 25);
2. the transport r = φ(s) → R9, produced by `i_transport.py merge` from an engine path R9 → s and the three R9 realization certificates;
3. a concatenation (`i_transport.py concat`).

So **six published components (one of length 15, five of length 16) are a single ordinary AC class.** Whether that class is AC-trivial is unknown: no primitive relator and no dataset match occurs in R9's cap-25 component.

**Meaning.** X and Y only join existing groups, so the 287 published non-trivialized components fall into 167 groups modulo Aut(F₂) at cap 25. The certificates add {R82, R86} = P2, which leaves **at most 166 distinct AC-triviality questions**. Certified ordinary AC equivalences cover 13 published components: R28, R82, R86, R212 and R327 into frontier classes, and R22, R69, R111, R114 and R223 into R9's class. The "same-status" groups become genuine AC classes as soon as Aut(F₂) is AC-realized on one member, for example by repeating §5's search for φ(seed) in the seed's component.

## 8. Reproduction (executed in this session)

Write `$S` for a scratch directory, and `ZARCO` / `NAHOMAR` for read-only clones of github.com/alejandrozarco/andrews-curtis-ms14 (commit a6c67b9) and github.com/nahomar/andrews-curtis-solver. `$S/{AC19,AC19Xtail,AC1M}.tgt` are D's converted datasets (research-d §5).

```sh
g++ -O2 -std=c++17 -o $S/d_acsearch experiments/d_acsearch.cpp; export DACS=$S/d_acsearch
python3 experiments/elementary_verify.py --selftest
python3 experiments/i_words.py --selftest          # i_words self-test passed
python3 experiments/i_family.py --selftest         # i_family self-test passed
python3 experiments/i_torus.py --selftest          # 192 Lemma S + 744 Euclid certificates replayed
python3 experiments/i_torus.py --sweep             # Lemma S sweep: 2898 certificates replayed ...; max moves 736
python3 experiments/i_transport.py --selftest      # synthetic AK(3) merge, 1330 moves
python3 experiments/i_residual_merge.py --selftest; python3 experiments/i_landscape.py --selftest
for a in 2 4 -4 6 -6 8 -8 10 -10 12; do python3 experiments/i_family.py --list $a 24; done
# §1 multi-source runs (fam24.txt, fam25.txt)
$DACS --cap 24 --maxstates 40000000 --source xxyXy,xyyyyyxYY --source xxxxyXy,xyyyxYY --source xxxYYYY,xyxYXY \
  --source xxxxyyyyyyy,xxyXy --source xxxxyyyyyyyyy,xxyXy --source xxxxxyyyyyyyyy,xxyXy \
  --source xxxxxxxyyyyy,xxxxyXy --source xxxxxyyyyyyyyyyy,xxyXy > fam24.txt
$DACS --cap 25 --maxstates 30000000 --source xxxxxyyyyyyyyyyy,xxyXy --source xxxxxxxxxxyyy,xxxxxxxxyXy \
  --source xxxxxxxxyyy,xxxxxxyXy --source xxxxyXy,xyyyxYY --source xxxxxxxyyyyy,xxxxyXy \
  --source xxxxxxxxyyyyy,xxxxyXy --source xxyXy,xyyyyyxYY --source xxxYYYY,xyxYXY > fam25.txt
# §3, §5 certificates
python3 experiments/i_words.py --zarco $ZARCO/certs/P1_equiv_C6.json certificates/i_p1_to_c6.json
python3 experiments/i_certify.py coll fam24.txt 0-3 xxyXy xyyyyyxYY xxxxyyyyyyy xxyXy certificates/i_c3_to_T2_4_7.json
python3 experiments/i_certify.py coll fam25.txt 2-6 xxxxxxxxyyy xxxxxxyXy xxyXy xyyyyyxYY certificates/i_T6_8_3_to_c3.json
python3 experiments/i_certify.py coll fam25.txt 3-5 xxxxyXy xyyyxYY xxxxxxxxyyyyy xxxxyXy certificates/i_c4_to_T4_8_5.json
python3 experiments/i_torus.py --lemma-s 2 1 7 certificates/i_lemmaS_T2_4_7_to_T2_5_9.json
python3 experiments/i_torus.py --lemma-s 2 1 9 certificates/i_lemmaS_T2_4_9_to_T2_5_11.json
python3 -I experiments/f_descent.py --cert xxxxyyy xxxxyXy 3 certificates/i_triv_T4_4_3.json      # also Tm4_7_m3, Tm6_11_m3
$DACS --cap 23 --maxstates 2000000 --maxhits 1 --source xxxxxxxxYYY,XXXXyXy > tm4_8.txt
python3 experiments/i_certify.py trivial tm4_8.txt xxxxxxxxYYY XXXXyXy certificates/i_triv_Tm4_8_m3.json
# Aut realization: phi_<c>.tgt holds the cyclic reductions of phi(rep) for the 7 maps
$DACS --cap 26 --maxstates 20000000 --no-stop --maxhits 20 --source xxyXy,xyyyyyxYY --exact-targets phi_c3.tgt > phi_c3_run.txt
python3 experiments/i_certify.py path phi_c3_run.txt swap xxyXy xyyyyyxYY yyxYx yxxxxxyXX certificates/i_c3_aut_swap.json   # etc.
# §6: components, Aut-orbits, comparisons
$DACS --cap 26 --maxstates 30000000 --source xxyXy,xyyyyyxYY --dumpkeys 0 k26_c3.bin
$DACS --autmatch k26_c3.bin --autdump aut26_c3.bin $S/AC19.tgt $S/AC19Xtail.tgt $S/AC1M.tgt    # hits 0, min_aut_length 14
$DACS --autcompare <agent-d>/aut_ak3.bin aut26_c3.bin                                       # common 0
# §7: residual landscape and composite certificates
python3 experiments/i_residual_merge.py --convert $NAHOMAR/proof-track/proof_direction/data/residual_classes16.txt resid16.tgt
python3 experiments/i_residual_merge.py k26_c3.bin resid16.tgt c3          # c3 labels C3:50 R327:20
python3 experiments/i_landscape.py $NAHOMAR/proof-track/proof_direction/data/residual_components16_c28.txt 22 land22 \
  X:xxxxyyyyyyyyy,xxyXy Y:xxxxxxxyyyyy,xxxxyXy     # components 289 groups 173 merged_groups 68
# same with cap 25 (land25):                       # components 289 groups 167 merged_groups 67
echo "s212 xyXyXYY xyyXyyyxYYxYY" > s212.tgt
$DACS --cap 22 --maxstates 3000000 --maxhits 1 --source xxxYYYY,xyxYXY --exact-targets s212.tgt > s212_run.txt
python3 experiments/i_certify.py path s212_run.txt s212 xxxYYYY xyxYXY xyXyXYY xyyXyyyxYYxYY ak3_to_s212.json
python3 experiments/i_transport.py merge xxxYYYY xyxYXY ak3_to_s212.json certificates d_ak3 xxyxyXY xxxyyyxxY \
  certificates/i_R212_to_ak3.json             # likewise R327 (C3, i_c3), R28 (P1, i_p1), R82/R86 (P2, i_p2)
python3 experiments/elementary_verify.py certificates/i_*.json     # 33 lines, exit 0
# R9 group: components with --dumpkeys/--dump 25, --autmatch k_R9.bin vs states of R_i -> pair (s, r),
# engine paths R9->s and R_i->r (i_certify.py path), then
python3 experiments/i_transport.py merge xxyxYY xxxxYXYXy R9_to_s.json <dir with R9_aut_*.json> R9 r1 r2 r_to_R9.json
python3 experiments/i_transport.py concat R22_to_r.json r_to_R9.json certificates/i_R22_to_r9.json
python3 experiments/i_autreal_sweep.py $NAHOMAR/.../residual_components16_c28.txt 25 land25.log   # aut_realized_seeds 6 of 287
```

Verifier output (`python3 experiments/elementary_verify.py certificates/i_*.json`, exit 0; the R9-group files are listed in §7). Columns: moves, peak, endpoint.

| file | moves | peak | endpoint |
|---|---:|---:|---|
| i_R212_to_ak3 | 611 | 49 | xxxYYYY, xyxYXY |
| i_R28_to_p1 | 3592 | 97 | XyyxYYY, XXXYxxy |
| i_R327_to_c3 | 1848 | 59 | xxyXy, xyyyyyxYY |
| i_R82_to_p2 | 11623 | 63 | XyyxYYY, XXXYxxY |
| i_R86_to_p2 | 19603 | 81 | XyyxYYY, XXXYxxY |
| i_p1_to_c6 | 1091 | 41 | xxyxxYY, xyXYYXy |
| i_c3_to_T2_4_7 | 36 | 39 | xxxxyyyyyyy, xxyXy |
| i_T6_8_3_to_c3 | 161 | 29 | xxyXy, xyyyyyxYY |
| i_c4_to_T4_8_5 | 40 | 49 | xxxxxxxxyyyyy, xxxxyXy |
| i_T2_5_11_to_sigmaT8_10_3 | 339 | 36 | xxxYYYYYYYYYY, xyxYYYYYYYY |
| i_lemmaS_T2_4_7_to_T2_5_9 | 44 | 29 | xxxxxyyyyyyyyy, xxyXy |
| i_lemmaS_T2_4_9_to_T2_5_11 | 46 | 31 | xxxxxyyyyyyyyyyy, xxyXy |
| i_triv_T4_4_3 / Tm4_7_m3 / Tm4_8_m3 / Tm6_11_m3 | 31 / 43 / 76 / 43 | 19 / 22 / 31 / 30 | x, y |
| i_c3_aut_{swap,invx,x_xy} | 209 / 186 / 214 | 29 / 29 / 36 | cyc φ(C3) |
| i_p1_aut_{swap,invx,x_xy} | 26 / 73 / 55 | 33 / 28 / 25 | cyc φ(P1) |
| i_p2_aut_{swap,invx,x_xy} | 366 / 275 / 54 | 34 / 34 / 26 | cyc φ(P2) |

## 9. Honest limits

- **Prop. M.** It needs a meridional partner through a torus relator of the stated congruence type. It says nothing about classes in which no state reaches defect 2, and that is exactly the open situation for AK(3), C3 and C4.
- **Lemma S and Prop. G.** Both are uniform but leave the frontier unchanged, since Lemma S stays inside a single class. Whether the level-k classes of T(2;·) for k ≥ 2 coincide with C3 or X was tested only at cap 28 (§4: no shared Aut-orbit), which is far from conclusive.
- **Separation results** (§6, §7) are cap-relative statements about the cyclic-product graph, which does not contain every elementary path (research-d §6).
- **"Same-status" groups.** These are equalities of AC-triviality status, not ordinary AC equivalences, until Aut(F₂) is realized on one member. The 173- and 167-group counts depend on the cap.
- **External inputs.** P1 ~ C6 rests on an external, AI-produced ledger; what is verified here is the replay of its conversion by the repository's strict verifier. The residual lists are nahomar's unreviewed data. They are used only as a source of seeds: every merge certificate starts at the published seed and is checked here, and nothing depends on that repository's completeness claims.
- **Correctness of the Aut-orbit computations.** This rests on Whitehead's peak-reduction theorem and on D's implementation (research-d §6). Every merge that I call genuine was turned into an explicit certificate whose replay does not depend on that code.
- **Novelty.** Literature access was limited to the public repositories above and the earlier notes, so novelty is not established for any item. Prop. M and Lemma E are likely folklore in some form.

## 10. Insight and recommended next directions

1. **Make Prop. M the stopping rule on the meridian route.** Every torus relator in sight in AK(3)'s class has type T(2,3), T(3,4), T(2,k) or T(k,k±1). G's meridian-guided search can therefore stop at the first defect-2 state, because the ACM step to a primitive word is explicit. In the other direction, a proof that AK(3)'s class never reaches defect 2 through such a relator would give a necessary condition for a counterexample that can be checked state by state.
2. **Aut-realize the remaining classes.** At cap 25 only 6 of the 287 seeds are Aut-closed (§7). Rerun `i_autreal_sweep.py` at caps 27–29 on the same-status groups, e.g. {R14, R59, R68, R108, R172, R272, R277} and {R16, R64, R90, R184, R211, R303}. Each success turns its group into a single certified AC class, and `i_transport.py` produces the certificates mechanically. The pipeline costs seconds per small component.
3. **Rerun §7 at larger caps** (AK3, C3, P1, P2 at caps 28–30 against the whole residual list; all 287 seeds at caps 25–26). Each merge into an Aut-realized class is a new certified member, and each other merge reduces the number of independent open questions.
4. **Chirality route on the counterexample side (Prop. C).** C4, X and Y are the tested classes whose components contain no automorphic image of themselves (caps 29–31). Two concrete tasks follow. First, push the search for σ(C4) in C4's component beyond cap 31; this needs a wider state encoding than D's 64-bit keys, and the component is small enough (3.05M states at cap 31). Second, look for an AC invariant that is sensitive to orientation or chirality; one that separated C4 from σ(C4) would disprove the AC conjecture.
5. **Level-shift question in T(2;·).** Is T(2;7,13) ~ C3? A symbolic step T(2;3k+1,6k+1) → T(2;3k+4,6k+7) would place an infinite family in C3's class. A proof that the levels are AC-distinct would instead give infinitely many AC-inequivalent candidates on the counterexample side. Moves that keep the second relator fixed are exhausted by Lemma S, so any level shift has to change both relators.

## 11. Files written

- `research/research-i.md` (this note).
- `experiments/i_words.py`: word utilities; a strict certificate builder with composite moves (conjugation by words, multiplication by conjugates, rotations, swap); the `--zarco` converter; self-test.
- `experiments/i_torus.py`: generators for Lemma S and Lemma E certificates, and syllable lengths in C_m*C_n; `--selftest`, `--sweep`.
- `experiments/i_family.py`: enumeration of T(a;p,q), coset-enumeration triviality test, engine driver; self-test.
- `experiments/i_certify.py`: turns engine PATH/COLLISION/TRIVIAL output into strict certificates (via `d_certify`, `f_descent`).
- `experiments/i_transport.py`: automorphism recovery, letterwise transport, glueing, reversal, and composite certificates from Aut-orbit matches; self-test.
- `experiments/i_residual_merge.py`: matches residual labels by Aut-orbit, with iteration past the engine's 50-hit print limit; self-test.
- `experiments/i_landscape.py`: union-find of residual components modulo Aut(F₂); self-test. Its outputs at caps 22 and 25: `experiments/i_landscape_cap22.txt`, `experiments/i_landscape_cap25.txt`.
- `experiments/i_autreal_sweep.py`: tests which seeds are closed under the Nielsen generators, and lists the genuine groups; self-test. Output: `experiments/i_autreal_sweep_cap25.txt`.
- `experiments/i_hicap_compare.txt`: the higher-cap Aut-orbit comparisons of §6.
- Certificates (`ordinary-ac-elementary-v1`, 33 files, 7.0 MB, each < 2 MB): `i_R22_to_r9`, `i_R69_to_r9`, `i_R111_to_r9`, `i_R114_to_r9`, `i_R223_to_r9`, `i_r9_aut_{swap,invx,x_xy}`, `i_R212_to_ak3`, `i_R327_to_c3`, `i_R28_to_p1`, `i_R82_to_p2`, `i_R86_to_p2`, `i_p1_to_c6`, `i_c3_to_T2_4_7`, `i_T6_8_3_to_c3`, `i_c4_to_T4_8_5`, `i_T2_5_11_to_sigmaT8_10_3`, `i_lemmaS_T2_4_7_to_T2_5_9`, `i_lemmaS_T2_4_9_to_T2_5_11`, `i_triv_{T4_4_3,Tm4_7_m3,Tm4_8_m3,Tm6_11_m3}`, `i_{c3,p1,p2}_aut_{swap,invx,x_xy}`.

## References

- Research notes A–F of this repository, especially research-d Lemmas D2, D3, D6 and Cor. D7, and research-f Prop. F3.
- J. Nielsen, *Die Isomorphismengruppe der freien Gruppen*, Math. Ann. 91 (1924). Generators of Aut(F₂); Aut(F₂) → GL₂(ℤ) has kernel Inn(F₂).
- J. H. C. Whitehead, *On equivalent sets of elements in a free group*, Ann. of Math. 37 (1936). Peak reduction, used through D's canonical forms.
- D. Panteleev, A. Ushakov, *Conjugacy search problem and the Andrews–Curtis conjecture*, arXiv:1609.00325. ACM moves; Aut(F₂) realized on AK(n).
- G. Burde, H. Zieschang, *Knots*, de Gruyter. Torus-knot groups, centre, meridian.
- J. Carr(eras), arXiv:2607.23611, and github.com/joe-carr-data/ac-certificates.
- nahomar/andrews-curtis-solver: residual lists and component file, unreviewed.
- alejandrozarco/andrews-curtis-ms14: P1 ~ C6 ledger, AI-produced, unreviewed, commit a6c67b9.
- M. Lackenby, arXiv:2606.06122: thickenable ⇒ AC-trivial (as reported in research-e/f).
- L. Fagan et al., arXiv:2606.21611: AC-19 / AC-1M datasets (via research-d).

## Coordinator's review (second reader, 2026-11-03)

- All 33 certificates in `certificates/i_*.json` replay under `python3 experiments/elementary_verify.py` (exit 0); the coordinator checked every start/target tuple against the stated presentations. `i_R327_to_c3.json` makes R327 ~AC C3 a plain ordinary-AC equivalence (agent G independently obtained it up to an explicit automorphism). `i_p1_to_c6.json` is self-verifying, so P1 ~AC C6 is established by this repository's verifier whatever the provenance of the external ledger it was converted from.
- Proofs re-derived by hand and correct: Prop. G (xᵖ and xᵐ = z⁻² are central; the von Dyck quotient for gcd(p,m) > 1), Lemma E (Euclid on exponent rows), Prop. M (the congruence n ≡ ±1 mod m turns n·i′ − m·j = ±1 into a representative with x-exponent ±1), and all five steps of Lemma S (each inserted word is freely equal to a product of conjugates of A^{±1}, with A = c z² as free words).
- Naming: the tuple called P2 here, (XyyxYYY, XXXYxxY), is the image of research-f's P2 = (x⁻¹y²xy⁻³, x⁻¹yx²yx⁻²) under y ↦ y⁻¹ (first relator then inverted and rotated); since Aut(F₂) is AC-realized on this class (`i_p2_aut_*.json`), both tuples lie in one AC class. Likewise (XyyxYYY, XXXYxxy) is a rotation of P1.
- Scripts: `i_words`, `i_torus`, `i_family`, `i_transport`, `i_residual_merge`, `i_landscape`, `i_autreal_sweep` pass `--selftest`; `i_certify.py` has no self-test mode (`--selftest` prints its usage and exits 1), contrary to the agent's summary. Its outputs are the certificates, which are verified independently.
- The "proof sketch" remark after Lemma S (that Lemma S exhausts the conjugacies with A fixed for q ≥ 3) is a sketch and nothing else in the note depends on it. All separation and "same-status" statements are cap-relative, as §9 says.

- **Round-5 audit (research-th08.md), finding F5.** The congruence hypothesis of Proposition M (n ≡ ±1 mod m or m ≡ ±1 mod n) is not needed for AC-triviality: a torus relator x^m y^n with a partner of syllable length 2 can be replaced by x^c y^d with unimodular exponents, and Lemma E (equivalently research-g §2.4(b)) finishes. So the caveat about the type T(5,8) for C4 ~ T(4;8,5) is unnecessary. Proposition M as stated remains correct.
