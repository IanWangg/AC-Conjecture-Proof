# Research TH09: killers of one-relator groups — the BS(1,2) exit, its exact reach from AK(n), and a census of killers of the trefoil group

Date: 2026-11-09 (Los Angeles). Independent research agent TH09 (round 5, theory round).

**Status.** Partial results, each labelled. **No AC trivialization of AK(3), no proof that AK(3) is not AC-trivial, no
counterexample.** Everything concerns the ordinary (unstabilized) AC relation; no stabilization is used.
Novelty is not claimed (Theorem 1 for the standard Miller–Schupp marking is reported to be in
Myasnikov–Myasnikov–Shpilrain 2002, which I could not read here).

## 0. Central claims (read this first)

Notation: F = F(x,y), X = x⁻¹, Y = y⁻¹, G_r = F/⟨⟨r⟩⟩. A **killer** of a group is an element whose normal closure
is the whole group. (r,s) presents the trivial group iff s is a killer of G_r. b = xyxYXY (braid/trefoil relator),
B = G_b. A **BS(1,2)-type word** is θ(XyxYY) for some θ ∈ Aut(F) (XyxYY = x⁻¹yxy⁻²).

| # | statement | label |
|---|---|---|
| T1 | **BS(1,2) exit.** If (r,s) is a balanced presentation of the trivial group and G_r ≅ BS(1,2) (as an abstract group, any marking), then (r,s) is AC-trivial. Reason: BS(1,2) has exactly one killer class up to inversion, and it contains the image of a primitive word. Hence: *a state with a BS(1,2)-type relator anywhere in an AC class trivializes the class* | proved here (§2); compiler + 6 stored certificates; standard-marking case = MS(1,w), externally reported known |
| T2 | Among Baumslag–Solitar relators BS(1,m), only m = 2 (and m = 0, where G_r = ℤ) can occur in a balanced presentation of the trivial group; so seed question (i) is completely answered by T1 | proved here (§2) |
| T3 | BS(1,2)-type conjugacy classes are parametrized by (primitive vector u = [θ(y)], sign δ = det θ); θ(XyxYY) kills G_r iff det([r],u) = ±1. So the BS(1,2)-type killers of any G_r form a **one-parameter family** v_j^±, j ∈ ℤ | proved here (§3) |
| T4 | **Trefoil side.** In B the BS(1,2)-type killers have syllable necklaces α_j = 112(21)^j and β_j = 111(21)^{j−1}22 in C₂*C₃ (up to rotation/inversion). The partner xⁿY^{n+1} of AK(n) has necklace 1^{n+1}2ⁿ. Hence a BS(1,2)-type word is conjugate in B to (xⁿY^{n+1})^{±1} **iff n ≤ 2** | proved here (§4), formulas machine-checked for \|j\| ≤ 40 |
| T5 | **T(n,n+1) side.** In ⟨x,y \| xⁿ = y^{n+1}⟩ the BS(1,2)-type killers have 2n\|j\|+6 or 2n\|j\|+2 syllables; for n ≥ 3 none is conjugate to b^{±1} | proved here (§5), machine-checked n ≤ 9, \|j\| ≤ 12 |
| T6 | **Gieseking side (K/O's coordinates P_n = (c,k_n)).** For n = 3, 4 no BS(1,2)-type word is conjugate to k_n^{±1} in G_c | proved by exact finite computation (§6; one hom to PSL(2,13), O's witness) |
| T7 | So for AK(3) the new exit is **not** one generalized (ACM) move away in any of the three known coordinate systems (same status as the primitive exit: G2, O6). For AK(2) it is: AK(2) → (BS(1,2)-type word, b) in one move with b frozen, although no primitive word is conjugate to x²Y³ in B (G2(b)) | proved (corollary of T1, T4–T6) |
| T8 | **Killers of the trefoil group.** g ∈ ⟨x,y \| x^p = y^q⟩ is a killer iff ab(g) = ±1 and its image kills C_p*C_q. Killer classes of B up to inversion and Aut ↔ necklaces in {1,2}^k (k odd, Σe ≢ 0 mod 3) up to rotation/reversal/complement with ⟨s,t \| s²,t³,∏st^{e_i}⟩ = 1 | proved here (§7) |
| T9 | **Census** (k = number of t-syllables; syllable length 2k; classes up to inversion and Aut). Killer classes: k=1: 1; k=3: 1; k=5: 2; k=7: 5; k=9: 15. All classes with k ≤ 5 are AC-trivial by exits. At k=7: 1121212 (primitive exit), 1112122 (**BS(1,2) exit, new**), 1121122 (**exchange exit**, T10; certificate, 6,998 moves) are AC-trivial. **The undecided killer classes of the trefoil group at the first undecided syllable length 14 are exactly two: 1111222 = AK(3) and 1111112 = C3** (I's frontier class (x²yXy, xy⁵xY²)) | exact enumeration (Todd–Coxeter) + T1, D3, certificate; "undecided" = no exit known to me, not a hardness claim |
| T10 | **Exchange exit.** If the killer class of s in G_r contains a word v such that r lies in an AC-trivial killer class of G_v, then (r,s) is AC-trivial. With both groups trefoil groups this gives a graph on necklaces; within bounds its only edges among k ≤ 9 are 112 — 11122 (AK(2)) and 112 — 1121122; AK(3) and C3 have no trefoil-type word in their class (bounds in §7.4) | proved (principle) + bounded experiment + certificate `certificates/th09_x7_trivialization.json` |

Not achieved: any exit for AK(3) or C3; a classification of the killers of C₂*C₃ beyond k ≤ 9; 11 of the 15 classes
at k = 9 have no exit known to me (they include C6 = 111212212 and AK(4) = 111112222).

## 1. Previous work read and choice of direction

Read: `README.md` in full; status paragraphs and coordinator reviews of all notes A–O; in full G §2–3, I §2–3, O §2–4,
K §4, F §3, D Lemmas D1–D7. Tools re-used read-only: `g_torus.py` (torus normal forms, `aut_from_matrix`,
`christoffel`, `edges`, `primitive_complete`), `g_cert.py` (ACM-move compiler), `f_descent.py` (Todd–Coxeter),
`d_whitehead.py`, `o_gc.py`, `elementary_verify.py`.

What the earlier notes give: every state (r,s) of a class is a (one-relator group, killer) pair in two ways; the
r-frozen moves see exactly the conjugacy class of s^{±1} in G_r (G Lemma G0); the only *exits* known were a primitive
word (D3), a meridional torus pair (I Prop. M, Lemma E) and thickenability (Lackenby, externally reported). G2 and O6
showed that the primitive exit is not one generalized move away from AK(n), n ≥ 3, in torus resp. Gieseking coordinates.

**Direction chosen (seed TH09, refined).** (1) Find a *new exit*: a second kind of word whose appearance as a relator
forces AC-triviality. The seed's question (i) has a clean answer: BS(1,2) has a unique killer class, so every
BS(1,2)-type relator is such an exit (T1); K §4 had observed, without explanation, that E's AK(2) trivialization
passes through a "BS(1,2)-type word" before it reaches a primitive relator. (2) Decide *exactly* (unbounded
conjugators, all automorphisms) whether AK(n) reaches the new exit in one generalized move, in each of the three
coordinate systems of G, K/O (T4–T6): the analogue of G2/O6 for the new exit. (3) Seed question (ii): organize all
states with a frozen trefoil relator as killers of the trefoil group, enumerate the short ones and decide as many as
possible (T8–T10). This is new relative to A–O: no earlier note uses BS(1,2), classifies killers of B, or lists
which killer classes are decided. It does not overlap TH18's BS(n,n+1), n ≥ 2 (only BS(1,m) is treated here).

## 2. The exit principle and the BS(1,2) exit (proved here)

**Lemma 2.1 (framework; restates G Lemma G0, D Lemmas D1–D3).** Let (r,s) be a pair of words.
(a) If s′ is conjugate to s^{±1} in G_r, then (r,s) ~AC (r,s′). (b) (r,s) ~AC (s,r). (c) If α ∈ Aut(F), then
(r,s) is AC-trivial iff (α(r),α(s)) is; in particular if α(r) is conjugate to r^{±1}, then (r,s) is AC-trivial iff
(r,α(s)) is. (d) If r is primitive and ⟨⟨r,s⟩⟩ = F, then (r,s) is AC-trivial.

So for fixed r the AC class of (r,s) depends only on the **killer class** of s (its conjugacy class in G_r up to
inversion), and AC-triviality only on the killer class up to the automorphisms of G_r induced from Stab_{Aut(F)}(±[r]).

**Definition.** Call r **universally trivializing** (r ∈ 𝒰) if every balanced presentation (r,s) of the trivial
group is AC-trivial. 𝒰 is closed under Aut(F), conjugation and inversion (Lemma 2.1(c)); primitive words are in 𝒰
(Lemma 2.1(d)). The AC conjecture for rank 2 says that every r is in 𝒰.

**Lemma 2.2 (exit principle).** Let ⟨⟨r,s⟩⟩ = F. (i) If some u ∈ 𝒰 is conjugate to s^{±1} in G_r, then (r,s) is
AC-trivial. (ii) *(exchange exit)* More generally, if some word v is conjugate to s^{±1} in G_r and (v, r) is
AC-trivial — e.g. because the killer class of r in G_v contains a member of 𝒰 — then (r,s) is AC-trivial.
*Proof.* (r,s) ~ (r,v) ~ (v,r) by Lemma 2.1(a),(b). ∎

**Theorem 1 (BS(1,2) exit).** Let r ∈ F with G_r ≅ BS(1,2) = ⟨a,t | t⁻¹at = a²⟩ (an abstract isomorphism; no
assumption on the marking). Then r ∈ 𝒰: every balanced presentation (r,s) of the trivial group is AC-trivial, by one
generalized move (r,s) → (r,p) with p primitive, followed by Lemma 2.1(d).

*Proof.* Write G = BS(1,2) = A ⋊ ⟨t⟩ with A = ℤ[1/2] (additive), a = 1 ∈ A, and t⁻¹ut = 2u for u ∈ A. The
abelianization is G → ℤ, a ↦ 0, t ↦ 1 (the relation gives a = 2a); call it deg.

*Step 1: the killers of G are exactly the conjugates of t and t⁻¹.* A killer generates G^ab = ℤ, so has deg = ±1.
Conversely, for u, v ∈ A: v·(u t⁻¹)·v⁻¹ = v + u + t⁻¹(−v)t (then t⁻¹) = (u − v)·t⁻¹, so with v = u the element
u t⁻¹ is conjugate to t⁻¹; and v·(u t)·v⁻¹ = (u + v − v/2)·t = (u + v/2)·t, so with v = −2u the element u t is
conjugate to t. Every element of degree ±1 has the form u t^{±1}. Finally t is a killer: modulo t, a = a², so a = 1.

*Step 2: a primitive word represents a conjugate of t.* Let π: F → G be the quotient map. deg∘π: F → ℤ is onto and
factors through F^ab = ℤ²; choose a basis (e₁,e₂) of ℤ² with e₁ ↦ 1, and (Nielsen: Aut(F) → GL₂(ℤ) is onto) a basis
(p,q) of F with [p] = e₁. Then deg π(p) = 1, so π(p) is conjugate to t by Step 1.

*Step 3.* If ⟨⟨r,s⟩⟩ = F then π(s) is a killer of G, hence conjugate to t^{±1}, hence to π(p)^{±1}: s is conjugate to
p^{±1} in G_r. Lemma 2.1(a) gives (r,s) ~AC (r,p), and (r,p) is AC-trivial by Lemma 2.1(d). ∎

**Corollary 1.1 (MS(1,w)).** For r = XyxYY the balanced presentations (r,s) of the trivial group are exactly the
pairs with s of x-exponent sum ±1, i.e. up to inverting s the Miller–Schupp presentations
MS(1,w) = ⟨x,y | x⁻¹yx = y², x = w⟩ with w of x-exponent sum 0 (s = x⁻¹w). All of them are AC-trivial.
*(Externally reported as known: Myasnikov–Myasnikov–Shpilrain 2002; proved here independently, and compiled:
`th09_killers.bs12_trivialize(s)` outputs a strict elementary certificate for any such s. Its length is not bounded
polynomially in |s| — the Dehn function of BS(1,2) is exponential — consistent with the known role of BS(1,2)-type
words as "hard but trivial" instances.)*

**Corollary 1.2 (BS(1,2)-type relators are exits).** If any presentation in the AC class of (r,s) has a relator v
that is BS(1,2)-type (v = θ(XyxYY), θ ∈ Aut(F)) or, more generally, has G_v ≅ BS(1,2), then (r,s) is AC-trivial.
Recognition is as cheap as primitivity: v is BS(1,2)-type iff its Whitehead-minimal cyclic form is one of the
length-5 signed-permutation images of XyxYY or its inverse. *(Proof: Theorem 1 and Lemma 2.1(c); Whitehead's
theorem for the recognition.)*

**Theorem 2 (BS(1,m): only m = 2 occurs).** If G_r ≅ BS(1,m) = ⟨a,t | t⁻¹at = a^m⟩ and (r,s) presents the trivial
group, then m = 2 or m = 0. For m = 0, G_r ≅ ℤ and the pair is covered by Lemma 2.1(d) (r is then primitive, by
Whitehead's classical theorem on one-relator presentations of free groups; alternatively repeat Steps 2–3 with
G = ℤ).
*Proof.* BS(1,m)^ab ≅ ℤ × ℤ/|m−1| (ℤ² if m = 1). A group with a killer has cyclic abelianization generated by the
image of the killer, in fact G_r^ab ≅ ℤ here because the exponent matrix of (r,s) is unimodular. So |m−1| = 1. ∎

Together: **every balanced presentation of the trivial group with a relator defining a solvable Baumslag–Solitar
group BS(1,m) is AC-trivial.** This answers seed question (i) completely; it is a statement about *all* killers, not
about bounded searches.

**Remark 2.3 (why this cannot be iterated naively).** Step 1 says that the twisted conjugation u ↦ v + u − 2v on
A is transitive (Reidemeister number 1). For G_r = N ⋊ ℤ with N = [G_r,G_r] non-abelian the killers of degree 1
correspond to twisted conjugacy classes of N, and these are infinite in number for the groups of this project (torus
knot groups: T8 below; G_c: O §2.2). Among one-relator groups with G^ab = ℤ and abelian commutator subgroup only ℤ
and BS(1,2) occur (N abelian forces G metabelian; the solvable one-relator groups on two generators are the BS(1,m)
and ℤ — classical, externally reported). So "unique killer class" is special to BS(1,2); new members of 𝒰 must come
from somewhere else (e.g. Lemma 2.2(ii)).

## 3. BS(1,2)-type words: classes and the one-parameter family of killers (proved here)

For a basis (P,Q) of F put v(P,Q) := P⁻¹QPQ⁻², so that θ(XyxYY) = v(θ(x),θ(y)). [w] denotes the exponent vector.

**Theorem 3.** (a) The conjugacy class of v(P,Q) depends only on the conjugacy class of Q and on
δ = det([P],[Q]) ∈ {±1}. (b) v(P,Q⁻¹) is conjugate to v(P,Q)⁻¹. (c) [v(P,Q)] = −[Q], and for any r:
⟨⟨r, v(P,Q)⟩⟩ = F iff det([r],[Q]) = ±1 iff ⟨⟨r,Q⟩⟩ = F. (d) Consequently, if [r] = ρ is a primitive vector and u₀
is one solution of det(ρ,u₀) = 1, the BS(1,2)-type killer classes of G_r, up to inversion, are the classes of

    v_j^+ = v(P_j, Q_j),   v_j^- = v(P_j⁻¹, Q_j),   j ∈ ℤ,   [Q_j] = u₀ + jρ,

where Q_j is a primitive word with that exponent vector (unique up to conjugacy) and P_j any complement of Q_j.

*Proof.* (a) Simultaneous conjugation of (P,Q) conjugates v. Let (P,Q) and (P′,Q) be bases with the same second
element. The automorphism α: P ↦ P′, Q ↦ Q has matrix [[ε,0],[i,1]] in the basis ([P],[Q]), the same as
β: P ↦ P^ε Qⁱ, Q ↦ Q; so αβ⁻¹ is inner (Nielsen), αβ⁻¹ = conjugation by g, and g commutes with Q, so g = Q^a
(Q is primitive, hence not a proper power, and centralizers in F are cyclic). Hence P′ = Q^a P^ε Q^{i−a}, and
v(P′,Q) = Q^{a−i}·(P^{−ε}QP^{ε}Q⁻²)·Q^{i−a} is conjugate to v(P^ε,Q); here ε = det([P′],[Q])/det([P],[Q]).
(b) v(P,Q)⁻¹ = Q²P⁻¹Q⁻¹P is conjugate to P⁻¹Q⁻¹PQ² = v(P,Q⁻¹). (c) The exponent vector is clear. G_v with
v = v(P,Q) is BS(1,2) with a = Q, t = P, so by Theorem 1 (Step 1) r is a killer of G_v iff deg r = ±1, where deg is
the P-exponent of r modulo [Q], i.e. deg r = det([r],[Q])/det([P],[Q]). And ⟨⟨r,Q⟩⟩ = F iff r ↦ generator of
F/⟨⟨Q⟩⟩ = ℤ iff det([r],[Q]) = ±1. (d) The primitive vectors u with det(ρ,u) = ±1 are ±(u₀ + jρ); primitive
conjugacy classes correspond to primitive vectors (Nielsen; G §2.2); use (a), (b). ∎

So, exactly like the primitive killers Q_j of G_r, the BS(1,2)-type killers form a one-parameter family, and
"is the killer s conjugate in G_r to a BS(1,2)-type word?" becomes a one-parameter question, which the next three
sections answer for AK(n) in the three coordinate systems of this repository.
(Observation, checked for all families below: the cyclic length of v_j^± is |Q_j| + 4, as
v(P,Q) = [P⁻¹,Q]·Q⁻¹ and [P⁻¹,Q] is a conjugate of [x,y]^{±1}.)

## 4. The trefoil side: BS(1,2)-type killers of B = ⟨x,y | xyx = yxy⟩ (proved here)

Coordinates. b = xyxYXY, [b] = (1,−1). By G §2/F3.1, φ = (x ↦ xY, y ↦ yyX) maps b to xxYYY, so
B/Z(B) ≅ C₂*C₃ = ⟨s⟩*⟨t⟩ with x ↦ st², X ↦ ts, y ↦ t²s, Y ↦ st (indeed φ(x) = xY ↦ s·t⁻¹, φ(Y) = xYY ↦ s·t⁻²).
Every element of C₂*C₃ of infinite order is conjugate to a cyclically reduced word st^{e₁}st^{e₂}…st^{e_k}, e_i ∈ {1,2}; its
**necklace** is the cyclic word e₁e₂…e_k. By G Lemma 1 two elements of B are conjugate iff they have the same
necklace and central exponent, and the central exponent is determined by the abelianization (6·d = 0 ⇒ d = 0).
Inversion acts on necklaces by reversal composed with the complement 1 ↔ 2.

The primitive vectors u with det((1,−1),u) = ±1 are ±(j+1, −j). Take P = xY and

    Q_j = P^j x   (j ∈ ℤ),   [Q_j] = (j+1, −j);   (P, Q_j) is a basis since x = P^{−j}Q_j, Y = x⁻¹P.

**Proposition 4.1 (explicit words).** Up to conjugacy,
- for j ≥ 0: v_j^+ = yxYX·(yX)^j·X and v_j^- = YxyXX·(yX)^j;
- for j = −i ≤ −1: v_{−i}^+ = yxYY·(xY)^{i−1}·X and v_{−i}^- = YxyXY·(xY)^{i−1}.

*Proof.* v(P,Q_j) = P^{j−1}xP·x⁻¹P^{−j}x⁻¹P^{−j}, which is conjugate (by P^{−j}) to P⁻¹xPx⁻¹·P^{−j}x⁻¹, and
P⁻¹xPx⁻¹ = yX·x·xY·X = yxYX. Likewise v(P⁻¹,Q_j) = P^{j+1}xP⁻¹·x⁻¹P^{−j}x⁻¹P^{−j} is conjugate to
PxP⁻¹x⁻¹·P^{−j}x⁻¹ = xYxyXX·P^{−j}X. For j ≥ 0, P^{−j} = (yX)^j: the first word is yxYX(yX)^jX, the second
xYxyXX(yX)^jX is cyclically YxyXX(yX)^j. For j = −i, P^{−j} = (xY)^i: yxYX·(xY)^i·X = yxYY(xY)^{i−1}X, and
xYxyXX·(xY)^i·X = xYxyXY(xY)^{i−1}X, cyclically YxyXY(xY)^{i−1}. ∎

**Proposition 4.2 (necklaces).** Put α_j = 112(21)^j (j ≥ 0), β_j = 111(21)^{j−1}22 (j ≥ 1), β_0 = 112. Then, up to
rotation: N(v_j^+) = α_j and N(v_j^-) = β_j for j ≥ 0; N(v_{−i}^+) = β_{i−1} and N(v_{−i}^-) = α_{i−1} for i ≥ 1.
The primitive killers have N(Q_j) = (21)^j2 for j ≥ 0 and N(Q_{−i}) = (12)^{i−1}2 for i ≥ 1.

*Proof.* Substitute x ↦ st², X ↦ ts, y ↦ t²s, Y ↦ st and reduce (s² = t³ = 1).
- yxYX ↦ t²s·st²·st·ts = t·s·t²·s, yX ↦ t²sts, X ↦ ts. So v_j^+ ↦ (ts)(t²s)(t²s·ts)^j(ts): an alternating word,
  cyclically reduced, with necklace 1,2,(2,1)^j,1, a rotation of α_j.
- YxyXX ↦ st·st²·t²s·ts·ts = (st)⁴s. So v_j^- ↦ (st)⁴s·(t²sts)^j. For j = 0 the cyclic reduction of (st)⁴s is
  t²·s·t·s·t·s: necklace 2,1,1 = β_0. For j ≥ 1 the final s cancels the initial s and t·t = t² merges twice:
  the cyclic word is t²s·(ts)³·(t²s·ts)^{j−1}·t²s, necklace 2,1,1,1,(2,1)^{j−1},2, a rotation of β_j.
- yxYY ↦ t²s·st²·st·st = t·s·t·s·t, xY ↦ st²st. So v_{−i}^+ ↦ (ts)(ts)t·(st²st)^{i−1}·ts. For i = 1 this is
  ts·ts·t²s: necklace 1,1,2 = β_0. For i ≥ 2 the last t of the block merges with the following t:
  (ts)(ts)(ts·t²s)^{i−2}(ts)(t²s)(t²s), necklace 1,1,(1,2)^{i−2},1,2,2 = 111(21)^{i−2}22 = β_{i−1}.
- YxyXY ↦ st·st²·t²s·ts·st = (st)(st)(st²). So v_{−i}^- ↦ (st)(st)(st²)(st²·st)^{i−1}: necklace 1,1,2,(2,1)^{i−1} = α_{i−1}.
- Q_j = (xY)^jx ↦ (st²·st)^j·st² for j ≥ 0, and Q_{−i} = (yX)^{i−1}y ↦ (t²s·ts)^{i−1}·t²s. ∎

**Theorem 4 (trefoil side).** Let n ≥ 1. A BS(1,2)-type word is conjugate in B to (xⁿY^{n+1})^{±1} iff n ≤ 2.
For n = 2: x²Y³ is conjugate in B to the inverse or to a conjugate of yxYXyXX = v(xY, xYx), a word of length 7.

*Proof.* The image of xⁿY^{n+1} is (st²)ⁿ(st)^{n+1}: necklace 2ⁿ1^{n+1} (G Theorem G1, A Lemma 1). The number of
maximal runs of a necklace is invariant under rotation, reversal and complement, hence under inversion. 2ⁿ1^{n+1}
has two runs and k = 2n+1 entries. By Theorem 3(d) and Prop. 4.2 every BS(1,2)-type killer of B has, up to
inversion, necklace α_j or β_j with k = 2j+3 entries; for j ≥ 1 both have exactly 2j runs (α_j: 111, 22, then
j−1 pairs 1, 2; β_j: 111, j−1 pairs 2, 1, then 22). Equal length forces j = n−1, and 2j = 2 forces n = 2
(j = 0: α_0 = β_0 = 112 = necklace of xYY up to inversion, n = 1). For n = 2, α_1 = 11221 is a rotation of 11122;
the central exponents agree automatically, so v_1^+ = yxYXyXX is conjugate in B to (x²Y³)^{±1}. ∎

**Corollary 4.3.** AK(2) = (x²Y³, b) ~AC (yxYXyXX, b) by one generalized move with b frozen, and the right-hand
side is AC-trivial by Theorem 1. This is a new mechanism for AK(2): by G2(b) *no primitive* word is conjugate to
x²Y³ in B, but a BS(1,2)-type word is. (It explains K §4's observation that E's AK(2) trivialization passes
through a BS(1,2)-type relator.) For n ≥ 3 this exit is closed on the trefoil side.

## 5. The T(n,n+1) side (proved here)

Let n ≥ 2, r_n = xⁿY^{n+1}, T_n = G_{r_n}, T_n/Z(T_n) ≅ C_n*C_{n+1} = ⟨a⟩*⟨c⟩ (a, c the images of x, y). Conjugacy
classes of cyclically reduced elements are their cyclic syllable sequences (G Lemma 1). [r_n] = (n, −(n+1)); the
primitive vectors u with det([r_n],u) = ±1 are ±((1,−1) + j(n,−(n+1))). Put P₀ = xY and u = P₀ⁿY (a basis:
Y = P₀⁻ⁿu), and Q_j = P₀u^j, which is primitive with complement u and [Q_j] = (1,−1) + j(n,−(n+1)).

**Proposition 5.1.** Up to conjugacy, v_j^+ = v(u,Q_j) = yxYX·u^{−j}·yX and
v_j^- = v(u⁻¹,Q_j) = Yx(yX)^{n+1}·u^{−j}·(xY)^{n−1}, where u⁻¹ = y(yX)ⁿ. Their images in C_n*C_{n+1} have cyclic
syllable length 2nj + 6 for j ≥ 0 and 2n|j| + 2 for j ≤ −1.

*Proof.* u⁻¹P₀u = yP₀Y = yxYY, so v(u,Q_j) = (u⁻¹P₀u)·u^{j}·u^{−j}P₀⁻¹u^{−j}P₀⁻¹ = yxYY·yX·u^{−j}·yX = yxYX·u^{−j}·yX.
v(u⁻¹,Q_j) = uP₀u⁻¹P₀⁻¹u^{−j}P₀⁻¹ is conjugate (by u⁻¹) to P₀u⁻¹P₀⁻¹·u^{−j}·P₀⁻¹u, with
P₀u⁻¹P₀⁻¹ = P₀yP₀^{−(n+1)} and P₀⁻¹u = P₀^{n−1}Y; moving P₀^{n−1}Y to the front gives
P₀^{n−1}(YP₀y)P₀^{−(n+1)}u^{−j} = (xY)^{n−1}·Yx·(yX)^{n+1}·u^{−j}, a rotation of the stated word.
Syllables (all exponents a^{±1}, c^{±1}, c^{±2} are nontrivial because n ≥ 2, n+1 ≥ 3):
- v_j^+, j ≥ 0: c·a·c⁻¹·a⁻¹·[c²a⁻¹(ca⁻¹)^{n−1}]^j·c·a⁻¹ — alternating and cyclically reduced: 4 + 2nj + 2.
- v_{−i}^+, i ≥ 1: yxYX·((xY)ⁿY)^i·yX = yxYY(xY)^{n−1}Y·((xY)ⁿY)^{i−1}·yX. For i = 1 this is
  yxYY(xY)^{n−1}X = c·a·c⁻²·(ac⁻¹)^{n−1}·a⁻¹: 2n + 2 syllables. For i ≥ 2 it is
  c·a·c⁻²·[(ac⁻¹)^{n−2}ac⁻²]·[(ac⁻¹)^{n−1}ac⁻²]^{i−2}·(ac⁻¹)ⁿ·a⁻¹: 3 + 2(n−1) + 2n(i−2) + 2n + 1 = 2ni + 2.
- v_j^-, j ≥ 1: c⁻¹·a·(ca⁻¹)^{n+1}·[c²a⁻¹(ca⁻¹)^{n−1}]^{j}·(ac⁻¹)^{n−1}; the last (ca⁻¹)^{n−1} cancels freely
  against (ac⁻¹)^{n−1}, leaving c⁻¹·a·(ca⁻¹)^{n+1}·[c²a⁻¹(ca⁻¹)^{n−1}]^{j−1}·c²a⁻¹: 2 + 2(n+1) + 2n(j−1) + 2 = 2nj + 6.
- v_0^- = Yx(yX)² ↦ c⁻¹·a·c·a⁻¹·c·a⁻¹: 6 syllables.
- v_{−i}^-, i ≥ 1: Yx(yX)^{n+1}((xY)ⁿY)^i(xY)^{n−1} = YxyXY·((xY)ⁿY)^{i−1}·(xY)^{n−1}; cyclically the final c⁻¹
  merges with the initial c⁻¹ to c⁻²: a·c·a⁻¹·c⁻¹·[(ac⁻¹)^{n−1}ac⁻²]^{i−1}·(ac⁻¹)^{n−2}·a·c⁻²: 4 + 2n(i−1) + 2(n−2) + 2 = 2ni + 2. ∎

**Theorem 5 (T(n,n+1) side).** For n ≥ 3 no BS(1,2)-type word is conjugate to b^{±1} in T_n. (For n = 2 there
are such words, e.g. yxYXyX = v₀^+; this is the same fact as Theorem 4 for n = 2, with the roles of the two
trefoil relators of AK(2) exchanged.)

*Proof.* b ↦ a·c·a·c⁻¹·a⁻¹·c⁻¹ has 6 syllables (A Lemma 2). By Prop. 5.1 a BS(1,2)-type killer with 6 syllables has
2nj + 6 = 6 (j = 0) or 2n|j| + 2 = 6 (n|j| = 2, impossible for n ≥ 3). So only v₀^+ ↦ c·a·c⁻¹·a⁻¹·c·a⁻¹ and
v₀^- ↦ c⁻¹·a·c·a⁻¹·c·a⁻¹ remain. For n ≥ 3, a ≠ a⁻¹ and c ≠ c⁻¹. The a-syllables of b are (a,a,a⁻¹), those of
v₀^± are (a,a⁻¹,a⁻¹): not conjugate to b. b⁻¹ ↦ c·a·c·a⁻¹·c⁻¹·a⁻¹ has a-syllables (a,a⁻¹,a⁻¹); reading the cyclic
word from its unique syllable a: b⁻¹ gives (c, a⁻¹, c⁻¹, a⁻¹, c), v₀^+ gives (c⁻¹, a⁻¹, c, a⁻¹, c), v₀^- gives
(c, a⁻¹, c, a⁻¹, c⁻¹). All three differ. By Theorem 3(d) these are all BS(1,2)-type killer classes up to inversion,
and comparing with both b and b⁻¹ covers inversion. ∎

## 6. The Gieseking side: P_n = (c, k_n) (proved by exact finite computation)

K/O: AK(n) ~AC P_n = (c, k_n), c = xyxYYXy, k_n = xⁿYXyy, G_c ≅ F(a,b) ⋊_φ ℤ (O Theorem O1). [c] = (1,0), so the
primitive killers are Q_j = x^jy (j ∈ ℤ, O Prop. O2) with complement x, and by Theorem 3(d) the BS(1,2)-type
killers of G_c are, up to inversion and conjugacy,

    v_j^+ = v(x, x^jy) ~ yxY·X^j·YX,    v_j^- = v(X, x^jy) ~ xyXY·X^j·Y     (j ∈ ℤ),

(direct free reduction; checked by machine for |j| ≤ 5), all of y-degree −1.

**Theorem 6.** For n = 3 and n = 4, no BS(1,2)-type word is conjugate to k_n^{±1} in G_c. Hence no generalized move
with c frozen takes P_3 (or P_4) to a presentation with a BS(1,2)-type relator.

*Proof (exact computation, `th09_killers.check_gieseking`).* Let H ≤ G_c be the index-2 subgroup of even degree,
H = ⟨a,b,t = y²⟩, and ρ: H → PSL(2,13) O's witness homomorphism (O Theorem O6): ρ(a) = [[0,2],[6,8]],
ρ(b) = [[1,11],[6,2]], ρ(t) = [[0,1],[12,5]]; the script re-checks the two relations of H and uses O's normal form.
If v ~ k_n⁻¹ in G_c then v² ~ k_n⁻² in G_c, so v² is H-conjugate to k_n⁻² or to y·k_n⁻²·y⁻¹, and
tr ρ(v²) ∈ {±tr ρ(k_n²), ±tr ρ(y k_n² Y)} (traces of inverses agree in SL₂). ρ(a), ρ(b) have order 7 and every
φ^m(a) is H-conjugate to a or b, so ρ(v_j²) depends only on j mod 7. Computed traces (up to sign, mod 13):
v_j^+: 5, 3, 5, 5, 2, 0, 3 and v_j^-: 3, 5, 3, 0, 2, 5, 5 for j ≡ 0,…,6 (the same values for y v² Y), whereas
k_3 gives 4 and k_4 gives 1. ∎

For n = 1, 2, 8 the value is 3 and for n = 5, 6, 7 it is 5, so this single homomorphism does not decide those n
(for n = 1, 2 no exclusion is expected: P_1, P_2 are one move from a primitive relator by O Cor. O3).

**Corollary 6.1 (T7).** For AK(3), in each of the three coordinate systems in which a relator can be frozen with
a solvable conjugacy problem in this repository (b; x³Y⁴; c), neither a primitive word (G2, O6) nor a BS(1,2)-type
word (Theorems 4–6) lies in the killer class of the partner. Any trivialization of AK(3) through these two exits
needs at least two generalized moves, with an intermediate relator that is neither primitive nor BS(1,2)-type.

## 7. Killers of the trefoil group: criterion, census, exchange graph

### 7.1 Killer criterion (proved here)

**Theorem 8.** Let T = ⟨x,y | x^p = y^q⟩ with coprime |p|,|q| ≥ 2 and Z = ⟨x^p⟩ its centre. Then g ∈ T is a killer
iff (i) its image in T^ab = ℤ is ±1 and (ii) its image ḡ kills T/Z = C_|p|*C_|q|.
*Proof.* Necessity is clear. Conversely let Q = T/⟨⟨g⟩⟩. By (ii), Q/(image of Z) = (T/Z)/⟨⟨ḡ⟩⟩ = 1, so Q is the image
of the cyclic group Z, hence abelian, hence a quotient of T^ab/⟨ab(g)⟩ = 1 by (i). ∎

**Corollary 8.1 (trefoil group, coordinates x² = y³, ab(x) = 3, ab(y) = 2).** The killer classes of B, up to
inversion, correspond bijectively to necklaces N = e₁…e_k ∈ {1,2}^k up to rotation and inversion (reversal +
complement) such that W_N := ⟨s,t | s², t³, st^{e₁}⋯st^{e_k}⟩ is trivial. Necessarily k is odd and Σe_i ≢ 0 mod 3
(perfectness of W_N), and then the central exponent is forced: ab = 3k + 2Σe_i + 6d = ±1 has exactly one solution
(d, sign). The automorphism x ↦ X, y ↦ Y of F preserves ⟨⟨xxYYY⟩⟩ and acts on necklaces by complement, so by
Lemma 2.1(c) **AC-triviality of (trefoil relator, s) depends only on the necklace of s up to rotation, reversal and
complement.** *Proof.* G Lemma 1 (conjugacy = necklace + central exponent), Theorem 8, and mod 6:
3k + 2Σe_i ≡ ±1 iff k odd and 3 ∤ Σe_i. ∎

So "all states of all AC classes that contain a trefoil-type relator" are indexed by one combinatorial object:
the set 𝒦 of necklaces N with W_N = 1 (the trivial one-relator quotients of the modular group), and the AC
conjecture restricted to these states says that every N ∈ 𝒦 is "AC-trivial". AK(n) is N = 1^{n+1}2ⁿ.

### 7.2 Census for k ≤ 9 (exact enumeration; `--census 9`)

W_N = 1 is decided by Todd–Coxeter (`f_descent.is_trivial_group`, index 1 over a generator) on the presentation
(xxYYY, s_N). Perfect necklaces up to rotation/reversal/complement:

| k | necklaces N ∈ 𝒦 (killers) | not killers |
|---|---|---|
| 1 | 1 | — |
| 3 | 112 | — |
| 5 | 11122, 11212 | 11111 (W = A₅) |
| 7 | 1111112, 1111222, 1112122, 1121122, 1121212 | 1111111 (W = (2,3,7) triangle group, infinite; classical) |
| 9 | 111111112, 111111122, 111111212, 111112112, 111112222, 111121112, 111121222, 111122122, 111211222, 111212122, 111212212, 111221122, 112112122, 112121122, 112121212 (all 15 perfect classes) | — |

### 7.3 Which classes are decided

Exits available: **P** = the class contains a primitive word (necklace (21)^j2 up to symmetry, Prop. 4.2; then
D3); **BS** = the class contains a BS(1,2)-type word (necklace α_j or β_j, Prop. 4.2; then Theorem 1);
**X** = exchange exit (Lemma 2.2(ii)) through a trefoil-type word.

| k | N | identification | status |
|---|---|---|---|
| 1 | 1 | meridian (x in AK coordinates) | AC-trivial: P (and I Prop. M) |
| 3 | 112 | AK(1); partner of AK(2) with x²Y³ frozen | AC-trivial: P, BS |
| 5 | 11122 | AK(2) | AC-trivial: BS (Cor. 4.3); X via 112; known certificates |
| 5 | 11212 | — | AC-trivial: P |
| 7 | 1121212 | — | AC-trivial: P |
| 7 | 1112122 | — (shortest form found: (x⁻⁴y⁻¹x⁻¹y⁻¹x²y, x⁻¹y⁻²x⁻¹y), length 15) | AC-trivial: **BS (new exit)** |
| 7 | 1121122 | "X7" = (x⁻³y⁻¹x⁻²y⁻¹x²y, x⁻¹y⁻²x⁻¹y), length 15 | AC-trivial: **X via 112**; certificate `th09_x7_trivialization.json` (6,998 moves, peak 364) |
| 7 | 1111222 | **AK(3)** | **undecided** |
| 7 | 1111112 | **C3** = (x²yXy, xy⁵xY²) (trefoil relator x²yXy) | **undecided** |
| 9 | 112121212 | — | AC-trivial: P |
| 9 | 111212122 | — | AC-trivial: BS |
| 9 | 112121122 | — | AC-trivial: X via the meridian class 1 (bounded search hit, see §7.4) |
| 9 | 111112222 | AK(4) | undecided |
| 9 | 111212212 | C6 = P1 (trefoil relator xyXYYXy) | undecided |
| 9 | ten others | — | no exit known to me |

**Answer to the seed question.** Ordered by syllable length, the first undecided killers of the trefoil group occur
at length 14 (k = 7), and there are exactly two of them up to symmetry: AK(3) and C3. All eight classes of smaller
or equal length other than these two are AC-trivial by a primitive, BS(1,2) or exchange exit. (The identification
of C3, C6, AK(n) is by computing the necklace of the partner of their trefoil-type relator, `cen2.py` in the scratch
directory; "undecided" means only that none of these exits applies within the stated bounds.)

### 7.4 The exchange graph (principle proved; data = bounded experiment + two certificates)

Let r, v be trefoil-type words with ⟨⟨r,v⟩⟩ = F. Then v has a necklace N in G_r ≅ B and r has a necklace N′ in
G_v ≅ B; call N, N′ **exchange neighbours**. By Lemma 2.1(a),(b) and Corollary 8.1 the AC-triviality of the
classes N and N′ is the same question. So AC-triviality is constant on connected components of the exchange graph
on 𝒦, and every component containing a P- or BS-class consists of AC-trivial classes (Lemma 2.2(ii)).
(G's "torus graph" is the same construction for all torus types; what is added here is the indexing of nodes by
killer necklaces, the BS exit, and the census.)

Bounded enumeration (`--exchange 12 9 160`: trefoil-type words θ_M(x^{±2}y^{±3}), θ_M(x^{±3}y^{±2}) with matrix
entries ≤ 12 and length ≤ 160 inside each killer class with k ≤ 9) finds exactly these edges:

    1 — 1 (loop),   1 — 112121122,   112 — 11122,   112 — 1121122,   1111112 — 1111112 (loop at C3).

- 112 — 1121122 gives the AC-triviality of X7. Certificate: `certificates/th09_x7_trivialization.json`, from
  (XXXYXXYxxy, XYYXy) to (x,y): relator 0 is moved, with the trefoil relator XYYXy frozen, to a trefoil-type word
  v of length 17; then XYYXy, which has 6 syllables (necklace 112) in G_v, is moved to a primitive word; then D3.
- 1 — 112121122 gives the AC-triviality of the k = 9 class 112121122:
  `certificates/th09_k9_112121122_trivialization.json`, from (XyXyXYXyXYxyxyxYxY, xxYYY) to (x,y), 7,147 moves.
- AK(3) = 1111222: no trefoil-type word in its class within these bounds (consistent with G's rigid 3-node torus
  island: its class contains torus-type words of types T(2,7), T(3,4), T(4,3) only, within |M| ≤ 6, exponents ≤ 14,
  length ≤ 70 here and within G's larger bounds).
- C3 = 1111112: one trefoil-type word in its class, and it leads back to the class 1111112 itself.

**Depth-2 exits at all torus nodes (experiment, negative).** For AK(3) (3 nodes) and C3 (14 nodes of types (2,7),
(3,4), (3,8), (4,7), (4,9), (5,7), (5,8), (5,9), (7,9), (8,3), (8,13), (9,11) within |M| ≤ 6, exponents ≤ 14,
length ≤ 70) I froze each torus-type word v in the class and tested the partner xxYYY in G_v for a primitive word
(`g_torus.primitive_complete`, exact by G Lemma G4) and for a BS(1,2)-type word (the one-parameter family of
Theorem 3(d) with |m| ≤ 30; the syllable length grows like 2|m|+4, so the window is generous but the growth
formula is proved here only for T(2,3) and T(n,n+1)). No exit at any node. In particular at AK(3)'s T(2,7) node the
partner has 10 syllables and the four BS(1,2)-type classes with 10 syllables ((m,k) = ±(3,−10), ±(3,−11)) are
different from it (tested for |m| ≤ 80).

## 8. Failed attempts and negative results (precise)

1. **BS(1,2) exit for AK(3), one generalized move.** Closed exactly in all three coordinate systems (Theorems 4–6)
   — a rigorous failure. Depth 2 through torus-type intermediate words: negative within the bounds of §7.4.
2. **Strict length descent** (`f_descent.descend`, K = 3, beam 60) from the shortest representatives of the k = 7
   classes: fails immediately for all five classes, including the three that are AC-trivial. So "no strict
   descent" carries no information here; the exits P, BS, X are what decides.
3. **"Unique killer class" for other relators.** I looked for further one-relator groups with a single killer class
   (which would give new members of 𝒰 as in Theorem 1). For G_r = N ⋊ ℤ this means that the twisted conjugation
   action on N = [G_r,G_r] is transitive; when N is abelian this happens only for ℤ and BS(1,2) (Remark 2.3), and
   for the groups of this project (torus knot groups, G_c) there are infinitely many killer classes (§7; O). I
   found no further example and no proof that none exists with N non-abelian.
4. **A structural reason why AK(3) and C3 have no exit.** I do not have one. The census shows that at k = 7 three
   of five classes exit, by three different mechanisms; I see no invariant separating {AK(3), C3} from the other
   three, and (by notes B, E, H) none can come from solvable or finite simple quotients.
5. **Classification of 𝒦.** Not attempted beyond k ≤ 9. Which elements of C₂*C₃ are killers is the question
   "which one-relator quotients of the modular group are trivial"; all 15 perfect classes at k = 9 are killers,
   so 𝒦 is large and no pattern excluding AK-type necklaces is visible.

## 9. Experiments and reproduction (executed in this session; one core, < 300 MB, each run < 2 min)

`experiments/th09_killers.py` (standard library; imports `g_torus`, `g_cert`, `f_descent`, `o_gc`,
`elementary_verify` read-only).

```
python3 experiments/th09_killers.py --selftest
# th09 self-test passed: 40 random BS(1,2) certificates replayed; braid-side BS exits for n in [1, 2] only (n < 20);
# torus-side hits (n: j) {2: [-1, 0], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []};
# Gieseking side: candidate traces [({5},{3}), ({3},{5}), ({5},{3}), ({5},{0}), ({2},{2}), ({0},{5}), ({3},{5})],
# k_n traces {1: [3], 2: [3], 3: [4], 4: [1], 5: [5], 6: [5], 7: [5], 8: [3]}, excluded n = [3, 4];
# killers with k <= 7: 1, 112, 11122, 11212, 1111112, 1111222, 1112122, 1121122, 1121212 (with tags)
```
The self-test checks: (1) the four rewriting rules of the BS(1,2) compiler are free-group identities
α⁻¹β = h R^{±1} h⁻¹; (2) Theorem 1 on 40 random words s of x-degree ±1 (each certificate replayed by
`elementary_verify.replay`); (3) Prop. 4.1/4.2 for |j| ≤ 40: the explicit words equal P^{∓1}Q_jP^{±1}Q_j⁻²,
they realize both classes θ(XyxYY) with [θ(y)] = (j+1,−j) and det θ = ±1 (`g_torus.aut_from_matrix`), their
necklaces are α_j, β_j as stated, and N(Q_j) is as stated; the AK(n) necklace is BS(1,2)-type only for n = 1, 2
(n < 20); (4) Prop. 5.1 for n = 2,…,9 and |j| ≤ 12 (words, syllable lengths, and conjugacy with b^{±1} only for
n = 2); (5) Theorem 6 (relations of H under ρ, orders 7, periodicity for |j| ≤ 21, trace tables); (6) the census
for k ≤ 7.

```
python3 experiments/th09_killers.py --census 9        # the table of §7.2 with words s_N and exit tags (about 20 s)
python3 experiments/th09_killers.py --exchange 12 9 160   # the edges of §7.4 (about 2 min)
python3 experiments/th09_killers.py --write certificates  # regenerates the certificates below
for f in certificates/th09_*.json; do python3 experiments/elementary_verify.py $f; done
```
Verifier output (this session):
```
{"endpoint": ["x", "y"], "moves": 48,   "path": "certificates/th09_ms1_1.json", "peak_total_length": 19}
{"endpoint": ["x", "y"], "moves": 24,   "path": "certificates/th09_ms1_2.json", "peak_total_length": 11}
{"endpoint": ["x", "y"], "moves": 215,  "path": "certificates/th09_ms1_3.json", "peak_total_length": 39}
{"endpoint": ["x", "y"], "moves": 170,  "path": "certificates/th09_ms1_4.json", "peak_total_length": 39}
{"endpoint": ["x", "y"], "moves": 208,  "path": "certificates/th09_ms1_5.json", "peak_total_length": 35}
{"endpoint": ["x", "y"], "moves": 52,   "path": "certificates/th09_ms1_6.json", "peak_total_length": 23}
{"endpoint": ["x", "y"], "moves": 6998, "path": "certificates/th09_x7_trivialization.json", "peak_total_length": 364}
{"endpoint": ["x", "y"], "moves": 7147, "path": "certificates/th09_k9_112121122_trivialization.json", "peak_total_length": 122}
```
(BS-exit certificates: see the addendum at the end of this section.)

- `th09_ms1_*.json`: Theorem 1 for (XyxYY, s), s = XyxyX, XYxyyX, XyXYxxYxYXX, XXyxyyxYX, XyyXYYxxyXY, XYYxyXy.
- `th09_x7_trivialization.json`: (x⁻³y⁻¹x⁻²y⁻¹x²y, x⁻¹y⁻²x⁻¹y) → (x,y), exchange exit (§7.4).
- `th09_k9_112121122_trivialization.json`: (XyXyXYXyXYxyxyxYxY, xxYYY) → (x,y), exchange exit through a
  trefoil-type word that is a meridian (conjugate to a primitive word of length 2 in adapted coordinates).

Scratch scripts (not stored; they only call the functions above): identification of C3, C6, AK(n) necklaces;
shortest representatives; the depth-2 scan of §7.4 (`d2.py`: C3 and AK(3) with |M| ≤ 6, exponents ≤ 14, length ≤ 70;
the twelve undecided k = 9 classes with |M| ≤ 5, exponents ≤ 9, length ≤ 60: no P or BS exit at any torus node).

## 10. Honest limits

- **AK(3) is not trivialized and not obstructed.** Theorems 4–6 are *exclusions of one mechanism at distance one*;
  they say nothing about longer paths and are not evidence of non-triviality (AK(2) is a reminder: its primitive
  exit is closed on the trefoil side while its BS exit is open).
- Theorem 1 for the standard marking (MS(1,w)) is reported to be known (Myasnikov–Myasnikov–Shpilrain 2002);
  I could not read the paper here. I do not know whether the statements "any marking", Theorem 3, or the census
  are in the literature; the triviality question for one-relator quotients of the modular group has been
  studied (Conder–Havas–Newman, externally reported), so the list 𝒦 for small k is probably tabulated there.
  **No novelty is claimed.**
- "G_v ≅ BS(1,2), any marking": I do not know whether a two-generator one-relator presentation of BS(1,2) other
  than the Aut(F)-images of XyxYY exists; Theorem 1 covers it if it does, but Theorems 3–6 concern
  BS(1,2)-type words (Aut-images) only.
- Theorem 6 is proved for n = 3, 4 only; for n ≥ 5 the single homomorphism does not decide (more quotients, as in
  O's sieve, would be needed). The Gieseking-side statement uses O's normal form and O's witness homomorphism,
  re-checked here (relations, orders).
- The exchange graph and the depth-2 scans are **bounded** enumerations (matrix entries, exponents and word
  lengths as stated). "No trefoil-type word in AK(3)'s class" is not proved here (TH04's topic).
- "Undecided" in §7.3 means: none of the exits P, BS, X applies within the stated bounds, and I know no
  trivialization. The ten unnamed classes at k = 9 were not compared with published residual lists.
- The census uses Todd–Coxeter for triviality (exact when it terminates with index 1); the two non-killers are
  justified separately (A₅; the (2,3,7) triangle group).
- The certificates are long (thousands of moves) because the compilers go through normal forms; no minimality.

## 11. Advice to the coordinator (ranked)

1. **Add the BS(1,2)-type test to every search engine** (D's/M's cyclic-product engine, F's descent, G's torus
   graph). By Corollary 1.2 a state with a BS(1,2)-type relator is an immediate trivialization, exactly like a
   primitive relator, and the test costs one Whitehead reduction (minimal form of length 5). The cap-29 forward
   set of AK(3) (2.9·10⁸ states) was only tested for primitive relators and contact with T(22); a BS(1,2)-type
   relator with a long partner would not have been noticed. Same for C3, C4, C6, P2.
2. **Treat AK(3) and C3 together.** They are the only two undecided killers of the trefoil group at the first
   undecided syllable length; C3's class has 14+ torus nodes (types (2,7), (3,4), …) while AK(3)'s has 3. A proof
   or trivialization technique should be tested on the three decided neighbours 1112122, 1121122, 1121212 first:
   any proposed obstruction must vanish on them, and they have certificates.
3. **Extend the exit list.** 𝒰 (universally trivializing relators) now contains primitives and BS(1,2)-type
   words. Each new member closes the whole one-parameter family of its Aut-images in every G_r. Candidates:
   relators whose group has finitely many killer classes each containing a member of 𝒰; a concrete test case
   is whether the trefoil relator's ten undecided k = 9 classes reduce to shorter ones by exchange through
   non-trefoil torus types (G's torus graph with the BS exit added).
4. **Do not expect a strict-descent or length argument**: three of the five k = 7 classes are AC-trivial but
   admit no strictly decreasing generalized move (§8.2).
5. For the Gieseking coordinates, combine O's sieve with the families v_j^± of §6 to decide n = 5,…,8.

## 12. Files written

- `research/research-th09.md` (this note).
- `experiments/th09_killers.py` (self-test: `--selftest`).
- `certificates/th09_ms1_{1..6}.json`, `certificates/th09_x7_trivialization.json`,
  `certificates/th09_k9_112121122_trivialization.json`, `certificates/th09_bs7_bs_exit.json` (see §9 addendum).

## References

- Repository notes A–O (this repository), in particular D (Lemmas D1–D3), F (§3), G (§2–3), I (§2–3), K (§4), O (§2–6).
- A. D. Myasnikov, A. G. Myasnikov, V. Shpilrain, *On the Andrews–Curtis equivalence*, Contemp. Math. 296 (2002) — externally reported; not read here.
- C. F. Miller III, P. E. Schupp, *Some presentations of the trivial group*, Contemp. Math. 250 (1999) — externally reported.
- D. Silver, W. Whitten, S. Williams, *Knot groups with many killers*, Bull. Aust. Math. Soc. 81 (2010) — externally reported (via K §4).
- M. Conder, G. Havas, M. Newman, *On one-relator quotients of the modular group*, in Groups St Andrews 2009 — externally reported; not read here.
- W. Magnus, A. Karrass, D. Solitar, *Combinatorial Group Theory* (conjugacy in free products; Nielsen's theorems; Whitehead's theorem).
