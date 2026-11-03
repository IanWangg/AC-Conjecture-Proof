# Research O: the frozen relator of P_n is the Gieseking group — exact ACM moves in K's coordinates, one-move trivializations of P_1 and P_2, and the primitive-exit question for P_3

Date: 2026-11-03. Independent research agent O (round 4, Fable cohort; structural/constructive side).

**Status:** partial, verified results; **no AC trivialization of AK(3), no proof of non-triviality, no counterexample, nothing on the full conjecture.** Every statement is labelled *proved here*, *experiment* (exact move set and bounds), *externally reported / recalled*, or *open*.

| # | statement | label |
|---|---|---|
| O1 | K's frozen relator c = xyxYYXy has y-exponent sum 0, and G_c = ⟨x,y \| c⟩ ≅ F(a,b) ⋊_φ ℤ with a = x, b = yxY, φ(a) = b, φ(b) = b⁻¹a (φ⁻¹: a ↦ ab, b ↦ a, abelianization [[1,1],[1,0]]). Normal forms are canonical; conjugacy of degree-1 elements (u,1) is φ-twisted conjugacy of u. | proved here (§2) |
| O1' | G_c is the fundamental group of the punctured-torus bundle with monodromy [[1,1],[1,0]] (det −1), i.e. (as recalled) the Gieseking manifold, whose orientable double cover is the figure-eight knot complement; so G_c is a non-orientable hyperbolic 3-manifold group with a Klein-bottle cusp. K's remark that G_c is "not a 3-manifold group" should read "not a knot group". | proved here up to the recalled identification (§2.3) |
| O2 | In P_n coordinates the killers are k_n = (aⁿBA, 1). An ACM move (c, k_n) → (c, p) with c frozen and p *primitive* exists iff k_n is conjugate in G_c to x^s y for some s ∈ ℤ (one-parameter family of exits). | proved here (§3) |
| O3 | k_1 ~ k_2 ~ x⁻²y in G_c and xy ~ x²y, y ~ x⁻¹y, with explicit two-to-six-letter conjugators (e.g. (xY)(xy)(yX) = x c⁻¹ x⁻¹ · x²y as free words). Hence **P_1 and P_2 are each AC-trivial by one ACM move with c frozen followed by the primitive finish**, and (c,k_1) → (c,k_2) is one c-frozen move. Certificates `o_p1_one_acm_move_trivialization.json` (305 moves), `o_p2_…` (543), `o_p1_to_p2.json` (57), `o_c_xy_to_c_xxy.json` (13). | proved here by certificate (§4) |
| O4 | The two Klein-bottle-cusp classes of degree-1 elements of G_c are exactly the primitive classes {s = −1, 0} and {s = 1, 2} of x^s y; for \|s\| ≤ 6 the x^s y fall into classes {−1,0}, {1,2} and singletons (bounded) | proved (cusp) + experiment (§4.3) |
| O5 | Compiler `o_cert.py`: any c-frozen ACM move with a known conjugator is compiled to a strict `ordinary-ac-elementary-v1` certificate through explicit factorisation of ⟨⟨c⟩⟩-elements into conjugates of c (four local rules), asserted as free-group identities | proved here + verified code (§5) |
| O6 | **For n = 3, …, 8, k_n is not conjugate in G_c to any x^s y; hence no presentation with a primitive relator is one ACM move (arbitrary conjugators) from P_n with c frozen** — the P_3-coordinate analogue of G2. Proof: an exact sieve over the finite quotients PSL(2,7), PSL(2,13) of the index-2 figure-eight subgroup H ≤ G_c, applied to squares; the control n = 1, 2 (where the exit exists, s = −2) passes | proved by exact computation (§6, `o_sieve.py`) |
| O7 | Small quotients of G_c (permutation degree ≤ 7, PSL(2,p), p ≤ 13) are all metabelian or have x central, so they cannot separate anything; informative quotients are semilinear (PΓL(2,p²)) or come from the index-2 figure-eight subgroup H = F(a,b) ⋊ ⟨y²⟩ for p ≡ 1 (mod 3) | experiment (§6) |

## 1. Previous work read and choice of direction

I read `README.md` and all twelve notes `research/research-{a..l}.md` in full, including the coordinator's reviews at the ends of D, G, H, I, K, L, and skimmed `experiments/` and `certificates/`. I re-ran `python3 experiments/elementary_verify.py --selftest` and the verifier on C's and K's certificates. The round-3 summary in my brief is accurate; in particular K's Theorem K1 (AK(n) ~AC P_n = (c, k_n), c = xyxYYXy, k_n = xⁿYXyy) is what I build on, and G's torus-group machinery (exact ACM moves with a frozen relator whose group has decidable conjugacy) is the model.

**Literature.** arxiv.org and journal hosts are blocked in this session (no attempt was made beyond what earlier notes report). The identification of G_c with the Gieseking manifold group is from memory (the Gieseking manifold is the punctured-torus bundle with monodromy [[1,1],[1,0]], double covered by the figure-eight knot complement); I label it *recalled*. Nielsen's theorem that primitive elements of F₂ with equal abelianization are conjugate is classical (Nielsen 1917; Osborne–Zieschang 1981; Cohen–Metzler–Zimmermann 1981) and is also checked computationally below for lengths ≤ 11. Novelty of anything here is **not established**.

**Why this direction (angle 1 of the brief).** K asked for conjugacy in G_c = ⟨x,y | xyxy⁻²x⁻¹y⟩ and said he could not decide it. The observation that unlocks it is elementary: c has y-exponent sum 0, so Magnus rewriting makes G_c free-by-cyclic with a free group of rank two as fibre. That turns every c-frozen ACM move into a *twisted conjugacy* question in F₂, gives canonical normal forms (hence an exact compiler for certificates, like G's for torus groups), and connects the P_n coordinates to a famous hyperbolic 3-manifold whose finite quotients are well understood. M (big searches) and N (invariants) run in parallel; nothing here duplicates them.

## 2. The structure of G_c (proved here)

Notation: X = x⁻¹, Y = y⁻¹; words are freely reduced; c = xyxYYXy; k_n = xⁿYXyy; P_n = (c, k_n) (K's P_n = (c, d_n) with d_n = k_n).

### 2.1 Theorem O1

Put a := x, b := yxY (free words), and let φ be the automorphism of F(a,b) with φ(a) = b, φ(b) = b⁻¹a; its inverse is φ⁻¹(a) = ab, φ⁻¹(b) = a (check: φ⁻¹(φ(b)) = φ⁻¹(b)⁻¹φ⁻¹(a) = a⁻¹ab = b). Let S = F(a,b) ⋊_φ ⟨y⟩ with y u y⁻¹ = φ(u), i.e. elements (u,k) with (u,k)(u′,k′) = (u φ^k(u′), k+k′).

**Theorem O1.** The maps Ψ: G_c → S, x ↦ (a,0), y ↦ (1,1), and Θ: S → G_c, a ↦ x, b ↦ yxY, y ↦ y, are mutually inverse isomorphisms. Consequently every element of G_c has a unique normal form (u,k), u a reduced word in a^{±1}, b^{±1}, k ∈ ℤ, computed from an (x,y)-word by reading letters left to right: x ↦ u ← u·φ^k(a), X ↦ u ← u·φ^k(a⁻¹), y ↦ k+1, Y ↦ k−1.

*Proof.* Write x_i = yⁱ x y⁻ⁱ. As free words, c = x · (yxY) · (YXy) = x_0 x_1 x_{−1}⁻¹, so c = 1 says x_{−1} = x_0 x_1; conjugating by y gives x_0 = x_1 x_2, i.e. y b y⁻¹ = x_2 = b⁻¹a. Hence Θ respects the relations of S: y a y⁻¹ = yxY = b is a free identity, and y b y⁻¹ = b⁻¹ a holds in G_c as just shown (explicitly, (yXYx)⁻¹·yyxYY = XyxyxYY is a rotation of c). Ψ is well defined because Ψ(c) = (a,0)(1,1)(a,0)(1,−1)(1,−1)(a⁻¹,0)(1,1) = (a φ(a) φ⁻¹(a⁻¹) , 0) = (a·b·(ab)⁻¹, 0) = (1,0). Ψ∘Θ fixes a, b, y and Θ∘Ψ fixes x, y, so both are isomorphisms. The reading rule is y^k·x^{±1} = φ^k(a^{±1})·y^k. ∎

`experiments/o_gc.py --selftest` checks: Ψ(c) = (1,0); Ψ(w g c^{±1} g⁻¹) = Ψ(w) for 500 random w, g; the homomorphism property and inverses; and the relation y b y⁻¹ = b⁻¹a.

### 2.2 Conjugacy of degree-1 elements is twisted conjugacy

The abelianization of G_c is ℤ, generated by y (c has exponent vector (1,0)), so the y-exponent ("degree") of an element is a conjugacy invariant. For degree 1: (v,m)(u,1)(v,m)⁻¹ = (v φ^m(u) φ(v)⁻¹, 1) and, since φ(u) = u⁻¹·u·φ(u⁻¹)⁻¹ lies in R(u) := {v u φ(v)⁻¹ : v ∈ F(a,b)}, the conjugacy class of (u,1) meets F(a,b)×{1} exactly in R(u), the **Reidemeister class** of u. Deciding twisted conjugacy in F₂ is possible in general (Bogopolski–Martino–Maslakova–Ventura, externally reported) but I did not implement a complete algorithm; I use (i) a breadth-first search in the graph u → v u φ(v)⁻¹ (v a letter), u → φ^{±1}(u), with a length cap, for *positive* answers with explicit conjugators, and (ii) finite quotients of G_c for *exact negative* answers (§6).

### 2.3 Geometry (recalled identification; matrix facts proved)

φ has abelianization matrix A = [[0,1],[1,−1]] (columns = images of a, b), det −1, trace −1, so φ⁻¹ has matrix [[1,1],[1,0]]. S is therefore π₁ of the punctured-torus bundle over S¹ with this monodromy — a non-orientable manifold with a Klein-bottle cusp (the monodromy reverses orientation). The bundle with monodromy [[1,1],[1,0]] is (recalled) the **Gieseking manifold**, whose orientable double cover is the punctured-torus bundle with monodromy A² ~ [[2,1],[1,1]], the figure-eight knot complement; A² = [[1,−1],[−1,2]] is indeed GL(2,ℤ)-conjugate to [[2,1],[1,1]] (conjugate by diag(1,−1), then by the swap). A is GL(2,ℤ)-conjugate to −A⁻¹ (by P = [[−3,−2],[5,3]]) but, in a bounded search, not to A⁻¹ or −A. In any case G_c is a 3-manifold group; its Alexander polynomial t²+t−1 is asymmetric, so it is not a knot group in S³ (F's criterion F2), which is what K's phrase "not a 3-manifold group at all" should say.

The cusp group: ∂ := [a,b] = aBAB satisfies φ(∂) = b⁻¹∂⁻¹b (free computation), so (b,1) = yx conjugates ∂ to ∂⁻¹ and ⟨∂, yx⟩ is a Klein-bottle group — the peripheral subgroup. Its degree-1 elements fall into two conjugacy classes, those of (b,1) = yx and of (b,1)∂ = (baBAb, 1).

## 3. The primitive exit from P_n with c frozen (proved here)

**Proposition O2.** Let n ≥ 1. There is a presentation with a primitive relator one ACM move away from P_n = (c, k_n) with c frozen (i.e. (c, p) with p primitive and p ≡ g k_n^{±1} g⁻¹ mod ⟨⟨c⟩⟩) iff k_n is conjugate in G_c to x^s y for some s ∈ ℤ. In normal form k_n = (aⁿBA, 1) and x^s y = (a^s, 1), so the condition is a^s ∈ R(aⁿBA) for some s.

*Proof.* If (c,p) is such a state, p^{±1} has degree 1 (degree is a conjugacy invariant and deg k_n = 1); replacing p by p⁻¹ we may assume deg p = 1 and p ~ k_n in G_c. A primitive element of F₂ is determined up to conjugacy by its abelianization (Nielsen; checked here for all primitive cyclic words of length ≤ 11: 84 primitive vectors, one conjugacy class each, `research-o` §7), and x^s y is primitive with abelianization (s,1), so p is conjugate in F to x^s y, hence k_n ~ x^s y in G_c. Conversely, if k_n ~ x^s y in G_c then (c,k_n) → (c, x^s y) is an ACM move (Lemma G0) and x^s y is primitive. The normal forms are computed by the reading rule of Theorem O1: k_n = xⁿ·Y·X·y·y ↦ (aⁿ·φ⁻¹(a⁻¹), 1) = (aⁿ (ab)⁻¹, 1) = (aⁿBA, 1). ∎

So the whole question "one c-frozen move from P_n to a primitive relator" is the one-parameter twisted-conjugacy question **Q1(n): is a^s ∈ R(aⁿBA) for some s ∈ ℤ?** By Lemma D3 a positive answer trivializes P_n, hence AK(n) (K1). For n = 3 this would settle AK(3).

Symmetrically (**Q2**), with k_3 frozen: ⟨x,y | k_3⟩^{ab} = ℤ via λ(x) = 1, λ(y) = −2, λ(c) = 1, and in the basis (x, t = yx²) a primitive with λ = 1 is conjugate to x tʲ; so "one k_3-frozen move from P_3 to a primitive" iff c ~ x(yxx)ʲ in ⟨x,y | k_3⟩ for some j. (Rewriting k_3 in (x,t) with x as stable letter shows ⟨x,y | k_3⟩ ≅ F(t_0,t_1,t_2) ⋊ ℤ, t_i ↦ t_{i+1}, t_2 ↦ t_2 t_0; not used further.)

## 4. Positive answers: n = 1, 2 (proved here by certificate)

### 4.1 Explicit conjugacies in G_c

The BFS of §2.2 (length cap 14) finds, with the conjugators written as (x,y)-words g such that g·W·g⁻¹ ≡ W′ mod ⟨⟨c⟩⟩:

| W | W′ | g | free-group witness |
|---|---|---|---|
| xy | xxy | xY | (xY)(xy)(yX) · (xxy)⁻¹ = x c⁻¹ x⁻¹ |
| y | Xy | XyXYX | g y g⁻¹ · (Xy)⁻¹ ∈ ⟨⟨c⟩⟩ (normal form (1,0)) |
| k_1 = xYXyy | k_2 = xxYXyy | xyxy | idem |
| k_2 = xxYXyy | XXy | XYYYXX | idem |

The first line is a one-line proof that **xy ~ x²y in G_c**: as free words xY·xy·yX = xYxyyX and x·c⁻¹·X·xxy = x·YxyyXYX·X·xxy = xYxyyX. Each of the other three is verified by the normal-form algorithm (`o_gc.nf` of the quotient word is (1,0)) and, independently, by the replayed certificates below.

### 4.2 Consequences and certificates

**Corollary O3.** k_1 ~ k_2 ~ x⁻²y in G_c. Hence (c,k_1) → (c,k_2) is one ACM move with c frozen, and both P_1 and P_2 reach the primitive-relator state (c, XXy) in one ACM move with c frozen; by Lemma D3 they are AC-trivial. (AK(1), AK(2) and P_2 were of course known to be AC-trivial — E's certificates, K's barrier-13 path; what is new is the *mechanism*: a single conjugacy in the Gieseking group, with the fibre relator never touched. This is the exact analogue of G's one-ACM-move trivialization of AK(2) in the torus coordinates, now in K's coordinates, and it is the control for the compiler of §5.)

Certificates (all produced by `python3 experiments/o_cert.py --write certificates`, all replayed by the repository verifier):

```
python3 experiments/elementary_verify.py certificates/o_*.json
{"endpoint": ["xyxYYXy", "xxy"],    "moves": 13,  "path": "certificates/o_c_xy_to_c_xxy.json", "peak_total_length": 13}
{"endpoint": ["x", "y"],            "moves": 305, "path": "certificates/o_p1_one_acm_move_trivialization.json", "peak_total_length": 33}
{"endpoint": ["xyxYYXy", "xxYXyy"], "moves": 57,  "path": "certificates/o_p1_to_p2.json", "peak_total_length": 28}
{"endpoint": ["x", "y"],            "moves": 543, "path": "certificates/o_p2_one_acm_move_trivialization.json", "peak_total_length": 50}
```

The P_2 certificate starts at exactly K's P_2 = (xyxYYXy, xxYXyy); concatenated with K's AK(2) → P_2 path (`k_ak_family.py --cert 2`) it gives a third independent trivialization of AK(2), not stored.

### 4.3 The degree-1 primitive classes (proved for the cusp; bounded otherwise)

Within the BFS cap 14, the elements x^s y for |s| ≤ 6 fall into the classes {s = −1, 0}, {s = 1, 2} and singletons for the other s (two BFS sets with a length cap are equal or disjoint, since every edge is reversible). The two merged classes are precisely the two peripheral classes of §2.3: (b,1) = yx ~ xy (s = 1) and (b,1)∂ = (baBAb,1), which the BFS finds in the class of y (s = 0). So the primitive exits (c, x^s y) with s ∈ {−1,0,1,2} are the two *cusp* classes of degree 1, and all other x^s y, as well as k_1 ~ k_2 ~ x⁻²y, are non-peripheral (hyperbolic glide reflections of the Gieseking manifold, if the recalled identification is right). This gives the geometric meaning of a c-frozen primitive exit: the moved killer must be conjugate to a degree-1 element that is either peripheral or one of the explicit glide-reflection classes a^s y.

## 5. The compiler (proved here; verified code)

`experiments/o_cert.py` compiles an ACM move (c, W) → (c, W′) with c frozen, given an (x,y)-word g with nf(g W^{±1} g⁻¹) = nf(W′), into strict elementary moves:

1. invert/conjugate W by ordinary moves (single-letter conjugations);
2. rewrite the result to the canonical word C = red(u(x, yxY) y^k) of its normal form (u,k);
3. rewrite C to W′ by the reverse of the same procedure applied to W′.

Step 2 uses the factorisation W = C · ∏ h_i c^{ε_i} h_i⁻¹ (free equality, asserted), obtained by scanning W and moving each y^{±1} past the fibre letters with the four local identities (all free-group identities, checked in `_check_rules`):

    y·x = (yxY)·y,                    y·(yxY) = (yXYx)·y·(h c h⁻¹),   h = yXYX,
    Y·(yxY) = x·Y,                     Y·x = (xyxY)·Y·(h c⁻¹ h⁻¹),      h = Xy,
    (and the inverse-letter versions: y·(yXY) = (XyxY)·y·(h c⁻¹h⁻¹), h = yxYYXy;  Y·X = (yXYX)·Y·(h c h⁻¹), h = xyyXYX).

Each factor h c^ε h⁻¹ is then removed by one `mult_by_conj` (conjugate c by h, invert if ε < 0, multiply, restore c) — the same composite G uses (Lemma G0). The output is checked by `elementary_verify.replay` in the self-test and, for the stored files, by the command above. `o_cert.twisted_path` is the BFS with parent pointers that produces g. Self-test: `python3 experiments/o_cert.py --selftest` (300 random factorisations, the commutation identities for |k| ≤ 3, and the four certificates).

The same scheme works for any one-relator group obtained by Magnus rewriting with free-by-cyclic structure (e.g. ⟨x,y | k_3⟩ after the basis change t = yx², §3); only the rule table changes. It is the "BS rewriting compiler" G asked for, specialised to the relators that actually occur in K's coordinates.

## 6. The primitive exit from P_3: exact finite-quotient sieve (experiment / proved by computation)

**Method.** If k_n ~ x^s y in G_c for some s ∈ ℤ, then in every finite quotient π: G_c → Q the images are conjugate, so s lies in the set of residues mod ord(π(x)) for which π(k_n) ~ π(x)^s π(y). A fixed s must survive every quotient; the set of consistent s ∈ ℤ is the intersection of unions of residue classes, computed by a sieve over s mod L (L = lcm of the orders used). **An empty intersection is an exact proof that Q1(n) has a negative answer.** The control n = 1, 2 (true conjugacy with s = −2) must survive. Soundness of each test: equal conjugacy class in Q is necessary; I use cycle type (S_d), trace up to sign (PSL(2,p)), the semilinear invariant tr(MM^σ)²/det(MM^σ) (PΓL(2,p²), invariant under all conjugations, §6.2), and, for the index-2 subgroup H, traces of the *squares* (§6.3), which is legitimate because k_n ~ g in G_c implies k_n² ~ g² in G_c, and conjugacy in G_c of elements of H by elements of G_c∖H is H-conjugacy after twisting by y, i.e. k_n² must be H-conjugate to (x^s y)² or to y(x^s y)²y⁻¹ (Y(·)y and y(·)Y are H-conjugate via y² ∈ H).

### 6.1 Small quotients are useless (experiment)

- Transitive permutation quotients of degree 3–7 (`o_gc.perm_quotients`, exhaustive): image orders 3, 4, 12, 5, 20, 6, 12, 24, 7 — all metabelian (cyclic, A₄, F₂₀, S₄, …); cycle types and conjugacy in the image never separate k_n from the x^s y, for any n ≤ 12.
- Homs G_c → PSL(2,p), p ≤ 13 (exhaustive, η up to conjugacy): every one has π(x) central, of order 2, or a metabelian image with tr(π(x)^sπ(y)) independent of s. No separation.
- Explanation (recalled geometry): the figure-eight group has its discrete faithful representation in PSL(2, ℤ[ω]); G_c's extra orientation-reversing generator acts as complex conjugation, so reductions of G_c land in PGL(2,p²)⋊Frobenius = PΓL(2,p²) for p ≡ 2 (mod 3) and in wreath-type groups for p ≡ 1 (mod 3), never in PSL(2,p) with a faithful-looking image. This matches the data exactly: homs H → PSL(2,p) with non-abelian fibre image exist for p = 7, 13, 19 and not for p = 5, 11.

### 6.2 Semilinear quotients PΓL(2,25) (experiment, exact)

`q_pgammal.py 5 Q1` (scratch; 15,773 homs with y ↦ (Y, Frobenius)): homs with π(x) of order 12 and 13 separate. Surviving residues mod 720720 for k_3: 36,960 (5.1 %), smallest |s|: s ∈ {−19, 20, −45, 46, −58, 59, …}, i.e. s ≡ 7 (mod 13) and a parity-type condition mod 12. For k_4: smallest |s| ∈ {−4, 5, −9, 10, …}. For k_1, k_2: s = −2 survives (control ✓).

### 6.3 The figure-eight subgroup H = F(a,b) ⋊_{φ²} ⟨t⟩, t = y² (experiment, exact)

H = ⟨a,b,t | t a t⁻¹ = b⁻¹a, t b t⁻¹ = a⁻¹b²⟩. Homs H → PSL(2,p) are enumerated exactly: T up to conjugacy, A arbitrary, B := A T A⁻¹ T⁻¹ forced by the first relation, second relation checked up to sign. Squares in normal form: (x^s y)² = (a^s b^s, 2), y(x^s y)²Y = (b^s (b⁻¹a)^s, 2), k_n² = (u_n φ(u_n), 2) with u_n = aⁿBA (so k_3² = (a³BAb³A, 2)). Candidate traces are periodic in s with period lcm(ord A, ord B, ord(B⁻¹A)).

**Results** (`python3 experiments/o_sieve.py --selftest`, 222 homs for p = 7 (176 with non-abelian fibre image, periods 12 and 28) and 498 for p = 13 (416 non-abelian, periods 7, 42, 91); one core, about one minute):

| n | allowed residues per period (p = 7: 12, 28; p = 13: 7, 42, 91) | surviving s mod 1092 |
|---|---|---|
| 1, 2 | 4/12, 8/28, 2/7, 12/42, 12/91 | **8**, smallest \|s\|: −2, 3, −93, 94, … (control: the true conjugacy k_1 ~ k_2 ~ x⁻²y survives) |
| 3 | 4/12, 8/28, **0/7**, 12/42, 12/91 | **0** |
| 4 | 2/12, 8/28, **0/7**, 4/42, 12/91 | **0** |
| 5 | 4/12, 8/28, 4/7, 6/42, 12/91 | **0** |
| 6 | 6/12, 8/28, 4/7, 4/42, 12/91 | **0** |
| 7 | 2/12, 8/28, 4/7, 4/42, 12/91 | **0** |
| 8 | 6/12, 4/28, 2/7, 4/42, 12/91 | **0** |

**Theorem O6 (proved by exact computation).** For n = 3, 4, 5, 6, 7, 8, the killer k_n is not conjugate in G_c to x^s y for any s ∈ ℤ. Consequently (Prop. O2) **no presentation with a primitive relator is one ACM move, with arbitrary conjugators and c frozen, from P_n = (c, k_n)** for these n; in particular not from P_3 ~AC AK(3). For n = 3 and 4 a **single** hom ρ: H → PSL(2,13) suffices, namely (matrices mod 13)

    ρ(a) = [[0,2],[6,8]],  ρ(b) = [[1,11],[6,2]],  ρ(t) = [[0,1],[12,5]],

for which ρ(a), ρ(b), ρ(b⁻¹a) all have order 7 in PSL(2,13), the two relations of H hold, and the traces (up to sign) are: tr ρ((x^s y)²) = tr ρ(a^s b^s t) = 5, 5, 5, 3, 0, 3, 5 and tr ρ(y(x^s y)²y⁻¹) = tr ρ(b^s(b⁻¹a)^s t) = 5, 5, 5, 3, 0, 3, 5 for s = 0, …, 6, whereas tr ρ(k_3²) = tr ρ(a³b⁻¹a⁻¹b³a⁻¹t) = 4 and tr ρ(k_4²) = 1. (Control: tr ρ(k_1²) = 3 equals the candidate trace at s ≡ −2 (mod 7).) This witness was re-verified with an independent 30-line script (relations, orders, traces). For n = 5–8 the exclusion needs the CRT combination of the p = 7 and p = 13 constraints (`o_sieve.combine`). This is the P_3-coordinate analogue of G's Proposition G2 (no primitive relator one ACM move from AK(n), n ≥ 3), with the frozen relator now the Gieseking relator instead of a torus relator. By contrast n = 1, 2 do have the exit (§4), and the sieve correctly lets s = −2 through.

### 6.4 What the sieve does and does not say

A negative outcome for n = 3 is an exact theorem ("no presentation with a primitive relator is one ACM move from P_3 with c frozen, with arbitrary conjugators"), the P_3-coordinate analogue of G2 for AK(3). Like G2 it says nothing about two or more moves, and nothing about AC-triviality. A finite set of quotients can never give a statement uniform in n: a quotient with ord(π(x)) = N cannot exclude n ≡ 1, 2 (mod N) because k_{n+N} ≡ k_n there and k_1 ~ k_2 ~ x⁻²y genuinely holds. A uniform statement would need the geometry (translation lengths of k_n² grow linearly in n, those of (x^s y)² in |s|), which I did not implement exactly.

## 7. Reproduction (executed in this session; one core, < 300 MB each)

```
python3 experiments/o_gc.py --selftest          # o_gc self-test passed
python3 experiments/o_cert.py --selftest        # o_cert self-test passed: {'P1': (305, 33, 'XXy'), 'P2': (543, 50, 'XXy'), 'xy->xxy': (13, 13), 'k1->k2': (57, 28)}
python3 experiments/o_sieve.py --selftest       # Theorem O6: excluded n = [3, 4, 5, 6, 7, 8]; controls k_1, k_2 keep s = -2; witness homs printed
python3 experiments/o_cert.py --write certificates
python3 experiments/elementary_verify.py certificates/o_*.json      # four lines, exit 0 (listed in §4.2)
python3 experiments/o_gc.py xxxYXyy xy yx                            # normal forms, e.g. xxxYXyy ('aaaBA', 1)
# scratch drivers (scratchpad/agent-o): q1_quot.py, q1_perm_fine.py, q_psl.py, q_sieve.py, q_pgammal.py, q_h.py
```

The primitive-conjugacy check of §3 (all cyclically reduced words of length ≤ 11, Whitehead-reduction primitivity test, grouped by exponent vector up to sign): 84 primitive vectors, each a single class up to rotation and inversion.

## 8. Honest limits

- Nothing here bears on whether AK(3) is AC-trivial. The positive results concern P_1, P_2 (known AC-trivial) and the class structure inside G_c; the negative results (if any, §6) concern single ACM moves.
- The twisted-conjugacy BFS is bounded (length cap 14–16); "different classes" statements in §4.3 are bounded observations except where the cusp argument applies. I did not implement a complete twisted-conjugacy algorithm.
- The Gieseking identification is recalled, not proved; only the free-by-cyclic structure (Theorem O1) and the matrix facts are proved here. Nothing downstream depends on the identification except the interpretation in §4.3 and §6.1.
- Finite-quotient exclusions are exact but only for the n and s they cover; they cannot be uniform in n (§6.4).
- Q2 (k_3 frozen) was tested only with PSL(2,p), p ≤ 13, and PΓL(2,25): 480,480 of 720,720 residues j survive — essentially no information; Q2 is open.
- Literature access was limited; novelty is not established for any item. The free-by-cyclic structure of ⟨x,y | xyxy⁻²x⁻¹y⟩ is a routine Magnus rewriting and the Gieseking group is classical; the P_n connection is K's.

## 9. Advice to the coordinator (ranked)

1. **Treat P_n coordinates as "killers of the Gieseking group".** Every c-frozen ACM move is now exact and certifiable (`o_cert.py`), and the one-move exits of P_1, P_2 show the mechanism that must be generalised: find a *two-move* path (c,k_3) → (c,k′) → (c′,k′) with c′ primitive, or (c,k_3) → (c′,k_3) → (c′,k″). The first move's targets k′ are the elements of R(a³BA): the BFS lists all of them up to any length cap with explicit conjugators (shortest: XyXYxxy, yxxxYXy, yxyXYXy, yXYxxyX, length 7). For each k′ the second move needs conjugacy in ⟨x,y | k′⟩ — decide it exactly where k′ is torus-type (G's tools) or free-by-cyclic (this note's method), otherwise bound it. This is the cheapest exact search not yet done, and every hit is a certificate.
2. **Use H = F(a,b) ⋊ ⟨y²⟩ (figure-eight group) for all exact negatives in G_c.** Its PSL(2,p) quotients for p ≡ 1 (mod 3) are the informative ones (§6); PSL(2,p²) for p ≡ 2 (mod 3) would add more. The same sieve decides, for any proposed target word w of degree 1, whether k_3 ~ w in G_c can be excluded; use it as a filter before any conjugator search.
3. **Implement the holonomy.** The figure-eight representation into PSL(2,ℤ[ω]) gives exact complex lengths; translation length is a complete invariant up to finite ambiguity and bounds |s| in Q1 for all n at once. This would turn §6 into a uniform theorem for all n ≥ 3 (expected: no primitive exit) and give an exact conjugacy test for the second move of item 1.
4. **Record the correction to K:** G_c is a (non-orientable, cusped) hyperbolic 3-manifold group, not "not a 3-manifold group"; it is not a knot group. F's thickenability obstruction for P_n is unaffected.
5. **Do not expect uniform-in-n statements from finite quotients** (§6.4); the n = 1, 2 coincidences k_1 ~ k_2 ~ x⁻²y are genuine and block them.
6. For N (invariants): the Reidemeister-class structure of φ on F₂ (two peripheral degree-1 classes, infinitely many non-peripheral ones) is a concrete, computable setting in which to test any proposed chirality-sensitive quantity on P_n vs. P_2.

## 10. Files written

- `research/research-o.md` (this note).
- `experiments/o_gc.py` — G_c normal forms, φ, twisted conjugation, permutation quotients; `--selftest`.
- `experiments/o_cert.py` — compiler of c-frozen ACM moves to strict certificates, twisted-conjugacy BFS with parents, `--selftest`, `--write`.
- `experiments/o_sieve.py` — exact non-conjugacy sieve through PSL(2,p) quotients of the figure-eight subgroup H (Theorem O6), with witness homs; `--selftest`.
- `certificates/o_p1_one_acm_move_trivialization.json`, `o_p2_one_acm_move_trivialization.json`, `o_p1_to_p2.json`, `o_c_xy_to_c_xxy.json` (all `ordinary-ac-elementary-v1`, < 25 kB each).
- Scratch (not committed): `scratchpad/agent-o/q*.py` and logs.

## References

- Research notes A–L of this repository, especially K (Theorem K1, P_n), G (Lemma G0, exact ACM moves, `finish_primitive`), D (Lemmas D2, D3, D6), F (Prop. F2).
- W. Magnus, A. Karrass, D. Solitar, *Combinatorial Group Theory*, §4.4 (Magnus rewriting of one-relator groups with a generator of exponent sum 0; Moldavanskii's free-by-cyclic case).
- J. Nielsen (1917); R. P. Osborne, H. Zieschang, Invent. Math. 63 (1981); M. Cohen, W. Metzler, A. Zimmermann, Math. Ann. 257 (1981): primitive elements of F₂ up to conjugacy ↔ primitive vectors (classical; recalled).
- H. Gieseking (1912); W. Thurston, *The geometry and topology of 3-manifolds*, §4 (the Gieseking manifold as the punctured-torus bundle with monodromy [[1,1],[1,0]], double covered by the figure-eight knot complement); R. Riley (1975) for the figure-eight representation in PSL(2,ℤ[ω]) — all recalled, not consulted.
- O. Bogopolski, A. Martino, O. Maslakova, E. Ventura, *The conjugacy problem is solvable in free-by-cyclic groups*, Bull. LMS 38 (2006) — externally reported (twisted conjugacy in free groups is decidable); not used.

## Coordinator's review (second reader, 2026-11-03)

- Re-ran `o_gc.py --selftest`, `o_cert.py --selftest`, `o_sieve.py --selftest` (all pass) and `python3 experiments/elementary_verify.py certificates/o_*.json` (all four replay; the two trivializations start exactly at P₁ = (c, xYXyy) and P₂ = (c, xxYXyy) and end at (x,y)).
- Re-derived by hand: Theorem O1 (Ψ(c) = (1,0) step by step; Ψ∘Θ and Θ∘Ψ fix the generators; the relation y b y⁻¹ = b⁻¹a from x₀ = x₁x₂), the Reidemeister-class description of §2.2, the normal forms k_n = (aⁿBA, 1), (xˢy)² = (aˢbˢ, 2), y(xˢy)²y⁻¹ = (bˢ(b⁻¹a)ˢ, 2), k_n² = (aⁿBAbⁿA, 2), the free-word identity (xY)(xy)(yX) = x c⁻¹ x⁻¹ · x²y, and Proposition O2 (degree is a conjugacy invariant since G_c^ab = ℤ generated by y; primitives of F₂ are determined up to conjugacy by their exponent vector). All correct.
- Theorem O6, n = 3 and 4: the coordinator re-verified the PSL(2,13) witness with independent code — both relations of H hold, ρ(a), ρ(b), ρ(b⁻¹a) have order 7, the candidate |traces| over all s are {0, 3, 5}, |tr ρ(k₃²)| = 4 and |tr ρ(k₄²)| = 1 (excluded), while k₁², k₂² have trace 3 (controls not excluded). The n = 5–8 exclusions rest on the CRT sieve in `o_sieve.py` (self-test passes) and were not re-derived separately.
- The Gieseking identification is recalled, as the note says; the free-by-cyclic structure (Theorem O1) is what the results use. O's correction to research-k is right: ⟨x,y | c⟩ is a punctured-torus bundle group, hence a 3-manifold group, and F's Alexander criterion shows only that it is not a knot group in S³; a note has been added to research-k's review section.
