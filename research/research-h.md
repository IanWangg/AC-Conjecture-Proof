# Research H: where an AC obstruction could live — lifting theorems, "just-obstructing" quotients, and the abelian fibre-product invariants

Date: 2026-11-02. Independent research agent H (round 3, obstruction side).

**Status:** obstruction-side no-go results, proved here and checked by computation. **AK(3) is not trivialized and not obstructed. No counterexample. The AC conjecture is neither proved nor disproved.**

The main results, with labels:

| # | statement | label |
|---|---|---|
| 1 | If some coordinate of some pair AC-equivalent to U has normally generating image in Q, then Q cannot obstruct U. This generalizes E's Prop. 5 and Cor. 2. | proved here |
| 2 | **Lifting theorem.** (i) If N ⊴ Q is abelian, then Q obstructs U iff Q/(N ∩ [Q,Q]) does. (ii) If N is a nonabelian minimal normal subgroup, then Q obstructs U iff Q/N does. | proved here |
| 3 | Q never obstructs if [Q,Q] is finite, or more generally if [Q,Q] has a solvable Q-normal subgroup of finite index. This covers all virtually solvable groups. Reproves BLM and Guyot for pairs. | proved here (corollary of 2) |
| 4 | U is non-AC-trivial iff some quotient of F *just-obstructs* U: it obstructs, but none of its proper quotients do. Such a Q has no abelian normal subgroup meeting [Q,Q], no nonabelian minimal normal subgroup and no monolith. It is not simple and not virtually solvable. No coordinate of any pair in U's class normally generates it. If Q is just-infinite, it is residually finite. | proved here |
| 5 | A new candidate invariant family outside BLM, Guyot and E: the fibre products Q_G = G ×_{G_ab} ℤ² (G finite), with an exactly computable AC-monodromy class δ_G. Theorem: δ_G ≡ 0 for every finite G. | definition + proved here |
| 6 | Independent computation of the item-5 data for 57 groups and 110 epimorphisms, up to order 7200 (including A7, A5×A5, A5×S5, A5≀C2 and S_n, PGL(2,q), GL(2,p), A5×C_m×C_n, 2⁴:S5). In every case \|C/Z\| = \|O_ab\|, i.e. Λ_G = Γ. AK(1)–AK(5), MS(3), Q, P1, P2, the MS(2) holdouts, C3, C4 and C6 are never obstructed. | experiment; agrees with 5 |
| 7 | 164 cyclic words occur as coordinates in the repository's certified AK(3)-class paths. By item 1, no quotient of any F/⟨⟨r⟩⟩ with r among them obstructs AK(3); the shortest r have length 5, e.g. x⁻²yxy. | computation + proved here |

Novelty is **not established** for any item. Items 2–3 contain BLM's and Guyot's theorems in the special case of pairs coming from F₂ (see §3 and §6).

---

## 0. Previous work read and choice of direction

I read `README.md` and `research/research-{a,b,c,d,e,f}.md` in full, and skimmed `experiments/` and `certificates/` (the verifier, D's and E's engines, and the certificate formats). I also re-ran `elementary_verify.py` on every certificate my script uses (§5.3). My summary of the earlier rounds, which I checked:

- A: plateau theorem; cyclic length ≥ 14 in the ACM graph.
- B: finite-quotient distance principle; BLM/Guyot kill each single finite or solvable quotient.
- C: MS(n, y⁻¹x²y⁻¹) ~ AK(n).
- D: 82 certificates, a cap-28 component and Aut(F₂)-realization.
- E: residual-chain reformulation; simple quotients and quotients of T = F/⟨⟨x³y⁻⁴⟩⟩ or of B₃ do not obstruct; exhaustive ≥ 15 instructions and peak ≥ 21.
- F: thickenability locus and meridian defect, both word properties.

**Why this direction.** E reduces the obstruction problem to quotients: AK(3) is non-trivial iff some quotient π: F → Q has π(AK3) ≁_AC π(x,y). The identity quotient qualifies if anything does. A proof of non-triviality would therefore most plausibly come from a cleverly chosen quotient where AC classes are computable. E removed finite, solvable, simple, and T- or B₃-quotients, and suggested infinite non-solvable non-simple groups. Rather than test random such groups, I asked **which structural features of Q can create an obstruction at all**. I prove lifting theorems showing that large classes of normal subgroups are "invisible" to obstructions. Then, by Zorn's lemma, I reduce to minimal ("just-obstructing") quotients and list their necessary properties.

The analysis isolates exactly one case the lifting lemmas do not cover: central kernels outside [Q,Q], i.e. abelian fibre products. These give a natural invariant family (Q_G for finite G) that BLM, Guyot and E do not cover. I define the invariant, make it exactly computable, test it on controls and on AK(3), and then prove it vanishes identically. This is the "rigorous failure proof" outcome the brief allows. It differs from G (constructive search) and I (other families), and from E, whose quotient no-gos are single-group statements without a lifting or minimality analysis.

Literature (search snippets only; arxiv.org and ar5iv were blocked by this session's network policy): Borovik–Lubotzky–Myasnikov, arXiv:1103.1295 (finite groups; N-Frattini subgroup); Guyot, arXiv:1612.06912 (f.g. soluble groups satisfy the generalized AC conjecture; Lemma 3.1 on normal generation in soluble groups); Myropolska, arXiv:1304.2668 and her Geneva thesis (groups in which all maximal subgroups are normal, e.g. Grigorchuk groups: the AC graph is connected iff that of the abelianization is). I found no statement of Theorems 2(ii), 3 (for infinite Q), 4 or 5. Snippet-level access cannot exclude them, so novelty is not established.

## 1. Conventions

- F = F(x,y), X = x⁻¹, Y = y⁻¹.
- π: F → Q is an epimorphism, with a = π(x), b = π(y).
- A pair U = (u₀,u₁) normally generates F. Its exponent matrix M_U ∈ GL₂(ℤ) is unimodular, since AC moves preserve |det| and det M_{(x,y)} = 1. "AC moves in Q" are: inversion, right multiplication by the other coordinate or its inverse, conjugation by arbitrary elements of Q, and swap.
- **Q obstructs U** means π(U) is not AC-equivalent to (a,b) in Q (E's d_Q(U) = ∞). If Q does not obstruct U, then neither does any quotient of Q (Fact 1 of E). And U is AC-trivial iff the identity quotient F does not obstruct it.
- More generally, I say a pair (s,t) of Q is **standardizable** if it is AC-equivalent in Q to (a,b). **Q has (AC)** if every pair that normally generates Q and whose abelianization is Nielsen-equivalent in Q_ab to that of (a,b) is standardizable. This holds, for instance, for every image of a normally generating pair of F. Each lemma below is proved in this pair-level generality.
- Throughout, "multiply coordinate i by an element of ⟨⟨other coordinate⟩⟩" is a composite of AC moves: conjugate the donor, multiply, conjugate back.

## 2. Theorem 1: class coordinates (proved here)

**Theorem 1.** Suppose some pair (c,w) ~_AC U in F has ⟨⟨π(c)⟩⟩ = Q. Then Q does not obstruct U.

*Proof.*
1. Since π(⟨⟨c⟩⟩) = Q, choose n ∈ ⟨⟨c⟩⟩ ⊆ F with π(n) = π(w)⁻¹. Then (c, wn) ~_AC U in F, and w' := wn has π(w') = 1.
2. Coordinates of pairs AC-equivalent to U are rows of unimodular matrices, so e(w') = (α,β) is primitive. Choose (γ,δ) with αδ − βγ = ±1. Lift it to a primitive element p of F, with basis (p,q) (complete to GL₂(ℤ) and lift by Nielsen).
3. F/⟨⟨p⟩⟩ ≅ ℤ via a linear form λ on exponent vectors with kernel ℤe(p). Then λ(e(w')) = ±det(e(p), e(w')) = ±1, so F/⟨⟨w',p⟩⟩ = 1. Since π(w') = 1, this gives ⟨⟨π(p)⟩⟩ = Q.
4. In Q, the pair (π(c), 1) has ⟨⟨π(c)⟩⟩ = Q. Multiply the second coordinate up to π(p). Then, using ⟨⟨π(p)⟩⟩ = Q, change π(c) into π(q).
5. Finally (π(q), π(p)) → (a,b) by the Nielsen moves that take the basis (q,p) of F to (x,y). ∎

**Corollary 1.1.**
- If Q obstructs U, then for every (c,w) ~ U, neither π(c) nor π(w) normally generates Q.
- In particular ker π contains no coordinate of any pair in U's class: if π(c) = 1, then π(w) normally generates Q.
- Every quotient of every one-relator group F/⟨⟨c⟩⟩, with c such a coordinate, fails to obstruct U.

Corollary 1.1 includes E's Prop. 5 and Cor. 2 (c = x³y⁻⁴ or xyxy⁻¹x⁻¹y⁻¹), and needs no separate primitive-element hypothesis. §5.3 lists the 164 class coordinates certified in this repository. A useful consequence: if Q_ab is cyclic and no class coordinate normally generates Q, Q must still have many proper normal subgroups. If Q_ab is not cyclic, Theorem 1 never applies; this is why §3 is needed.

## 3. Theorem 2: lifting through normal subgroups (proved here)

In this section N ⊴ Q, and the target pair is the standard pair (a,b), which generates Q. For an abelian N, write additively n·g := g⁻¹ng (a right ℤ[Q]-module).

**Lemma 2.1 (module corrections).** Let N be abelian, and let n₀, n₁ ∈ N.
1. The pair (a n₀, b n₁) is AC-equivalent to (a n₀', b n₁') whenever n₀' − n₀ and n₁' − n₁ lie in [N,Q].
2. As subgroups, [N,Q] = N(a−1) + N(b−1).

*Proof of 2.* Put S = N(a−1) + N(b−1).
- S is invariant under a^{±1} and b^{±1}. For example, n(b−1)a = n(ba−1) − n(a−1), and n(ba−1) = n(b−1) + (nb)(a−1). The inverse letters are handled similarly, using n(1−a⁻¹) = (na⁻¹)(a−1). Hence S is Q-invariant.
- Since n(gh−1) = n(g−1)h + n(h−1), induction on word length gives N(g−1) ⊆ S for every g. Hence [N,Q] = Σ_g N(g−1) = S.

*Proof of 1.*
- Conjugating coordinate 0 by m ∈ N gives m⁻¹(a n₀)m = a·(n₀ + m(1−a)).
- The "multiply trick" consists of three moves: u₀ ← u₀u₁, then conjugate u₀ by m ∈ N, then u₀ ← u₀u₁⁻¹. It changes a n₀ into a·(n₀ + m·b⁻¹ − m·a), and leaves u₁ = b n₁ untouched. Expanding: m·b⁻¹ − m·a = m(b⁻¹−1) − m(a−1). Since N(b⁻¹−1) = N(b−1), the two kinds of moves together realize every correction in S on coordinate 0.
- Coordinate 1 is symmetric. ∎

**Lemma 2.2 (central step).** Let N be central, and n₀, n₁ ∈ N ∩ [Q,Q]. Then (a n₀, b n₁) ~_AC (a,b).

*Proof.*
1. Q/⟨⟨b n₁⟩⟩ is generated by the images of a and b, and b ≡ n₁⁻¹ is central there, so this quotient is abelian. Hence [Q,Q] ⊆ ⟨⟨b n₁⟩⟩, and coordinate 0 can be multiplied by n₀⁻¹.
2. Likewise [Q,Q] ⊆ ⟨⟨a⟩⟩, which removes n₁. ∎

**Theorem 2(i) (abelian kernels).** Let N ⊴ Q be abelian and N' = N ∩ [Q,Q]. A pair P of Q is standardizable if its image in Q/N' is. In particular Q has (AC) if Q/N' has (AC), and Q obstructs U iff Q/N' does.

*Proof.*
1. In Q₁ = Q/[N,Q], the image N₁ = N/[N,Q] is central. Moreover N₁ ∩ [Q₁,Q₁] = N'/[N,Q], because [N,Q] ⊆ [Q,Q].
2. Lift a path for the image of P in Q/N' = Q₁/(N₁ ∩ [Q₁,Q₁]) to Q₁. Its endpoint is (a n₀, b n₁) with n_i ∈ N₁ ∩ [Q₁,Q₁]. By Lemma 2.2 the image of P is standardizable in Q₁.
3. Lift that path to Q. The endpoint errors now lie in [N,Q], and Lemma 2.1 removes them.
4. For the (AC) form: the abelianization condition passes to Q/N', since (Q/N')_ab = Q_ab. ∎

**Theorem 2(ii) (nonabelian minimal normal subgroups).** Let N be a nonabelian minimal normal subgroup of Q, and (s,t) any pair that normally generates Q. Then for all n₀, n₁ ∈ N, the pair (s n₀, t n₁) is AC-equivalent to (s,t). Hence P is standardizable if its image in Q/N is; Q has (AC) iff Q/N does; and Q obstructs U iff Q/N does.

*Proof.* Minimality gives N ∩ ⟨⟨g⟩⟩ ∈ {1, N} for every g. The key observation:

(†) If ⟨⟨u⟩⟩ centralizes N, then N ⊆ ⟨⟨v⟩⟩ for the other coordinate v of any normally generating pair (u,v). Otherwise ⟨⟨u⟩⟩⟨⟨v⟩⟩ = Q centralizes N, so N is central, contradicting that N is nonabelian.

1. *Make N ⊆ ⟨⟨second coordinate⟩⟩.* If ⟨⟨t n₁⟩⟩ ∩ N = 1, then t n₁ centralizes N, and by (†) N ⊆ ⟨⟨s n₀⟩⟩. Choose m, z ∈ N with [m,z] ≠ 1 and replace t n₁ by t n₁ m. Then [t n₁ m, z] = [m,z] ≠ 1 lies in ⟨⟨t n₁ m⟩⟩ ∩ N, so N ⊆ ⟨⟨t n₁ m⟩⟩.
2. *Remove n₀.* Coordinate 0 becomes s; coordinate 1 is now t n₁' with n₁' ∈ N.
3. *Clean coordinate 1.* If N ⊆ ⟨⟨s⟩⟩, remove n₁' directly. Otherwise ⟨⟨s⟩⟩ centralizes N.
   - Replace s by s m' with N ⊆ ⟨⟨s m'⟩⟩, exactly as in step 1.
   - Remove n₁'.
   - Apply (†) to the pair (s,t): N ⊆ ⟨⟨t⟩⟩, so m' can be removed. ∎

**Corollary 3 (proved here).** Suppose Q has a normal subgroup S ⊆ [Q,Q] such that S is solvable and [Q,Q]/S is finite. Then Q has (AC); in particular Q obstructs nothing. This covers:
- (a) all virtually solvable Q: take S = R ∩ [Q,Q] for a solvable normal subgroup R of finite index;
- (b) all Q with finite [Q,Q], e.g. all finite Q;
- (c) all f.g. solvable Q.

So, for pairs, BLM's finitary theorem and Guyot's soluble theorem are special cases.

*Proof.*
1. Q/S has finite derived subgroup [Q,Q]/S. Take a chief series of Q/S through it. Each chief factor is either abelian and contained in the derived subgroup (Theorem 2(i)), or nonabelian minimal normal in the corresponding quotient (Theorem 2(ii)).
2. Descending from (Q/S)_ab gives (AC) for Q/S. Abelian groups have (AC): AC moves there are Nielsen moves, and pairs with Nielsen-equivalent abelianization are standardizable by definition.
3. Then lift through the derived series of S. Each term is abelian, normal in Q and contained in [Q,Q], so Theorem 2(i) applies. ∎

## 4. Theorem 4: just-obstructing quotients and their structure (proved here)

**Theorem 4 (existence).** Call Q *just-obstructing* for U if Q obstructs U and no proper quotient of Q does. Then U is not AC-trivial iff some quotient of F is just-obstructing for U.

*Proof.*
1. The set 𝒩 = {N ⊴ F : F/N obstructs U} contains 1 iff U is non-trivial.
2. *Chains have upper bounds.* Let N₁ ⊆ N₂ ⊆ … lie in 𝒩, and suppose F/(∪N_i) did not obstruct U. A finite instruction path p would then have both endpoint discrepancies p(U)₀x⁻¹ and p(U)₁y⁻¹ in ∪N_i, hence in a single N_i. So F/N_i would not obstruct U, a contradiction.
3. Zorn's lemma gives a maximal element N*. The quotient F/N* is just-obstructing. ∎

(This uses only the finiteness of paths. It is a minimality counterpart of B's and E's residual arguments.)

**Theorem 4 (structure).** Let Q be just-obstructing for some U. Then:

(a) Q is not simple and not virtually solvable. More precisely, [Q,Q] has no solvable Q-normal subgroup of finite index (Corollary 3). In particular [Q,Q] is infinite, and Q is infinite.

(b) Every abelian normal subgroup N of Q has N ∩ [Q,Q] = 1, so N is central and embeds in Q_ab, a quotient of ℤ². In particular Z(Q) ∩ [Q,Q] = 1, and [Q,Q] contains no nontrivial abelian (or solvable, or finite) normal subgroup of Q.
*Proof.* If N ∩ [Q,Q] ≠ 1, Theorem 2(i) gives a proper obstructing quotient.

(c) Q has no nonabelian minimal normal subgroup (Theorem 2(ii)). Hence every minimal normal subgroup of Q, if one exists, is central of prime order and meets [Q,Q] trivially.

(d) Q has no monolith. A monolith M would be minimal, hence central of prime order with M ∩ [Q,Q] = 1 by (c). But it would also lie in the nontrivial normal subgroup [Q,Q]; note [Q,Q] ≠ 1, since abelian groups have (AC).

(e) If Q is just-infinite, it is residually finite. Otherwise its finite residual is a monolith, contradicting (d). In that case, by B's/E's argument applied to Q, the distances over the finite quotients of Q are unbounded.

(f) For every (c,w) ~_AC U, neither π(c) nor π(w) normally generates Q (Corollary 1.1).

**Consequences for AK(3) (proved).** Any proof that AK(3) is not AC-trivial via quotients can be pushed down to a just-obstructing quotient with properties (a)–(f). Such a quotient has:
- no abelian normal subgroups inside [Q,Q];
- no nonabelian minimal normal subgroups;
- no single class coordinate normally generating it (item 7 lists 164 explicit words that it must not kill).

These are necessary conditions, not a construction. F itself satisfies (a)–(e) trivially: it has no nontrivial abelian normal subgroups and no minimal normal subgroups. So nothing here suggests that AK(3) is non-trivial.

## 5. Theorem 5: abelian fibre products and the AC-monodromy invariant δ_G

### 5.1 The gap and the family Q_G (proved here)

Theorem 2(i) loses exactly the part of an abelian normal subgroup lying outside [Q,Q]. If N is central and N ∩ [Q,Q] = 1, then Q embeds in Q/N × Q_ab, as the fibre product (Q/N) ×_{(Q/N)_ab} Q_ab. The largest instance over a finite group G = π(F) is

    Q_G := G ×_{G_ab} ℤ²  =  F / (ker π ∩ [F,F]).

Q_G is infinite, residually finite and central-by-finite. It is not solvable if G is not, and it is not a quotient of T or B₃. Theorem 1 never applies to it, since its abelianization ℤ² is not cyclic. So **BLM, Guyot, E and Theorem 1 all say nothing about Q_G**, which makes it a genuine candidate source of invariants.

**AC monodromy.** The 15 instructions generate a group 𝒜 acting on G² (and on F²). Define μ: 𝒜 → GL₂(ℤ) as the action on exponent vectors; conjugations map to I. Let Z = ker μ. Let C be the 𝒜-orbit of c₀ = (a,b) in G². By BLM, C consists of all normally generating pairs whose G_ab-image is that of a basis. Let Λ_G = μ(Stab_𝒜(c₀)) be the monodromy group of AC loops at c₀. Let Γ ≤ GL₂(ℤ) be the stabilizer of (ā,b̄) ∈ G_ab², a congruence subgroup; clearly Λ_G ≤ Γ.

**Proposition 5.1 (proved here).**
1. GL₂(ℤ) = 𝒜/Z acts transitively on C/Z with point stabilizer Λ_G. Hence [GL₂(ℤ):Λ_G] = |C/Z| and [GL₂(ℤ):Γ] = |O_ab|, where O_ab is the GL₂(ℤ)-orbit of (ā,b̄) in G_ab².
2. Z is the normal closure of the conjugation instructions: Aut(F₂) maps onto GL₂(ℤ) with kernel Inn(F₂), and each inner substitution acts on a given pair as a product of partial conjugations. So C/Z is the congruence closure, under the 7 Nielsen instructions, of the relation c ~ (conjugation)(c).
3. A pair U of F (normally generating) is AC-trivial in Q_G iff [π(U)] = [π(B_U)] in C/Z, where B_U is any basis of F with exponent matrix M_U. This is the invariant **δ_G(U)**.

*Proof of 3.* U is trivial in Q_G iff some φ ∈ 𝒜 has φ(π_G U) = c₀ and μ(φ)M_U = I. That is, π_G(U) lies in μ⁻¹(M_U)·c₀ = Zν·c₀ = Z·π_G(ν(x,y)) for a Nielsen element ν with μ(ν) = M_U. Two bases with the same exponent matrix differ by an inner substitution, which lies in Z. ∎

δ_G could only be nontrivial if Λ_G were a proper, necessarily non-congruence, subgroup of Γ. Such a Λ_G is congruence-dense, by BLM applied to the finite quotients G ×_{G_ab} (ℤ/m)². Non-congruence stabilizers do arise for the plain Nielsen action of Aut(F₂) on Epi(F₂,G). So before Theorem 5 was proved, this was a live possibility.

**Theorem 5 (proved here).** For every finite G and every epimorphism F → G, Q_G has (AC). Hence Λ_G = Γ, and δ_G(U) = 0 for every U.
*Proof.* [Q_G,Q_G] = [G,G] × 0 is finite. Apply Corollary 3(b). ∎

So the whole abelian-fibre-product family fails, together with every finite G: it cannot detect AK(3), or anything else. This is a rigorous failure proof for a natural candidate invariant that escapes all earlier no-go results.

### 5.2 Experiment: independent computation of Λ_G versus Γ

`experiments/h_monodromy.cpp` (C++17, no dependencies) does not use Theorem 5. For a permutation group G = ⟨π(x), π(y)⟩ it:
1. enumerates G with a full multiplication table;
2. finds C by BFS with the 15 instructions;
3. computes C/Z by union–find congruence closure (initial unions are conjugation edges; propagation is along the 7 Nielsen instructions);
4. computes [G,G] as the normal closure of [x,y], G_ab and O_ab;
5. evaluates δ_G on the listed pairs, building B_U by Euclidean row reduction of M_U.

`experiments/h_groups.py` builds the groups and random generating pairs.

Commands executed (B = scratch directory; one core under `nice`, ≤ 0.5 GB):

```sh
g++ -O2 -std=c++17 -Wall -o $B/h_monodromy experiments/h_monodromy.cpp
$B/h_monodromy --selftest
#  selftest A5: |G|=60 |C|=3599 |C/Z|=1 |O_ab|=1 |G_ab|=1 image_ok=1
#  selftest S5: |G|=120 |C|=10800 |C/Z|=3 |O_ab|=3 |G_ab|=2 image_ok=1
#  selftest S4: |G|=24 |C|=432 |C/Z|=3 |O_ab|=3 |G_ab|=2 image_ok=1
#  selftest C6: |G|=6 |C|=24 |C/Z|=24 |O_ab|=24 |G_ab|=6 image_ok=1
#  selftest passed     (also: 2000 random unimodular reductions; 300 random AC-trivial pairs
#                       per group and AK(1), AK(2) all test trivial)
python3 experiments/h_groups.py --selftest                       # group orders: selftest passed
python3 experiments/h_groups.py --bin $B/h_monodromy --pairs 2 --max-order 2500     # 52 s
python3 experiments/h_groups.py --bin $B/h_monodromy --pairs 1 --max-order 7300 \
        --only A7 A5xA5 A5xS5 A5wrC2
```

**Results (executed).**
- Run 1 covered 53 groups of order ≤ 2184, with 2 epimorphisms each: the catalogue pair and one random generating pair, 106 in all. Run 2 added one epimorphism each for A7 (2520, |C| = 6,350,399) and A5×A5 (3600, |C| = 12,952,801), both with |C/Z| = |O_ab| = 1, and A5×S5 (7200, |C| = 38,869,200, G_ab = ℤ/2), with |C/Z| = |O_ab| = 3. A5≀C2 (7200, |C| = 38,880,000, G_ab = ℤ/2) also gives |C/Z| = |O_ab| = 3. (The executed run-2 command also listed a name `S7`, which is not in the catalogue and only raised a KeyError at the end.)
- **In every case |C/Z| = |O_ab|, i.e. Λ_G = Γ**, and every tested pair gives δ_G = 0. The tested pairs are AK(1)–AK(5), MS(3), the length-13 presentation Q, P1, P2, the two MS(2) holdouts, C3, C4 and C6.
- The image of C in G_ab² equals O_ab in every case, which is BLM's description of C.

Selected rows (C = AC component of (a,b) in G²):

| G | \|G\| | G_ab | \|C\| | \|C/Z\| = \|O_ab\| |
|---|---:|---|---:|---:|
| A5, A6, A7, PSL(2,7/11/13), SL(2,5), SL(2,7), 2⁴:A5, A5×A5 | 60 … 3600 | 1 | \|G\|²−1 or close | 1 |
| S5, S6, PGL(2,7), PGL(2,11), PGL(2,13), 2⁴:S5 | 120 … 2184 | ℤ/2 | e.g. 3,577,392 (PGL(2,13)) | 3 |
| GL(2,5) | 480 | ℤ/4 | 172,800 | 12 |
| GL(2,7) | 2016 | ℤ/6 | 2,709,504 | 24 |
| A5×C_m, m = 2..12 | ≤ 720 | ℤ/m | e.g. 431,880 (m=11) | 3, 8, 12, 24, 24, 48, 48, 72, 72, 120, 96 |
| A5×C_m×C_k ((2,2),(2,4),(3,3),(2,6),(4,4),(5,5),(6,6)) | ≤ 2160 | ℤ/m×ℤ/k | e.g. 1,036,512 (6,6) | 6, 24, 48, 48, 96, 240, 288 |
| S5×C_m, S5 ×_{C₂} C_m, SL(2,5)×C_m, PSL(2,7)×C_m | ≤ 720 | various | — | always equal |
| solvable controls S4, SL(2,3), GL(2,3) | ≤ 48 | — | — | 3, 8, 3 |

The values |O_ab| = |P¹-type orbit| (e.g. 3 = |{(1,0),(0,1),(1,1)}| for ℤ/2, 24 for ℤ/5 and ℤ/6, 288 for (ℤ/6)²) are the indices of the congruence groups Γ. They include Γ = Γ(6) for G = A5×C₆×C₆, a level at which Γ(N) is not generated by elementary matrices. Equality there was not obvious a priori. The census and Theorem 5 are independent checks of each other: the code knows nothing of the lifting lemmas. In addition, `h_groups.py --selftest` numerically verifies the two correction identities of Lemma 2.1 (conjugation by m ∈ N, and the multiply trick) with the exact right-action conventions, in 2⁴:A5 with N = ℤ/2⁴ (300 random instances).

Run 2 finished; all four groups agree with Theorem 5.

### 5.3 Experiment: certified class coordinates of AK(3)

```sh
python3 experiments/h_class_coordinates.py --selftest
#  selftest passed: 43 certificates, 164 class coordinates, all with primitive exponent vectors
python3 experiments/h_class_coordinates.py --show 30
#  {"certificates": 43, "distinct_cyclic_coordinates": 164, "by_length": {"5": 3, "6": 7, "7": 21,
#   "8": 24, "9": 65, "10": 26, "11": 7, "12": 5, "13": 5, "16": 1}}
#  5 XXYxY (-1,-2)   5 XXyxy (-1,2)   5 XYXyy (-2,1)   6 XXYYxy ...   7 XXXXyyy ...
```

The script imports the repository verifier read-only. It fully replays each of the 42 `d_ak3_*` certificates and `ms3_to_ak3_exact.json`; the 43 that have AK(3) as an exact endpoint all qualify. It then collects every intermediate coordinate up to cyclic rotation and inversion. By Corollary 1.1, for each of these 164 words r (for example r = x⁻²yxy, x⁻²y⁻¹xy⁻¹, x⁻¹y⁻¹x⁻¹y², x³y⁻⁴, the Miller–Schupp relator x⁻¹y³xy⁻⁴, and xyxy⁻¹x⁻¹y⁻¹), **no quotient of F/⟨⟨r⟩⟩ obstructs AK(3)**. In particular, BS(3,4) = F/⟨⟨x⁻¹y³xy⁻⁴⟩⟩ and all of its quotients cannot obstruct AK(3).

## 6. Honest limits

- Nothing here shows AK(3), or anything else, is or is not AC-trivial. All results are *necessary conditions* on a would-be obstruction, plus one candidate family proved useless. F itself satisfies every condition in Theorem 4. A just-obstructing quotient exists iff the conjecture fails for U, so the theorem cannot by itself decide anything.
- The proofs are complete as written, but short. They should be checked by a second reader, particularly Lemma 2.1 (module identities, right-action conventions) and the case analysis in Theorem 2(ii). The census in §5.2 is an independent consistency check of Theorem 5, and hence of Theorem 2 on finite instances (110 epimorphisms). It is not a proof.
- Theorem 4's minimal quotient comes from Zorn's lemma and is not constructive.
- Literature access was limited to search snippets. Theorems 2 and 3 likely overlap with lemmas inside the BLM and Guyot proofs, which handle chief factors and soluble groups for k-tuples. Their statement for infinite Q with nonabelian minimal normal subgroups, Corollary 3(a), Theorem 4 and Theorem 5 were not found, but novelty is not established.
- Not covered: just-infinite residually finite groups such as SL(3,ℤ) or PSL(2,ℤ[1/p]); groups with no minimal normal subgroups (such as F itself, or hyperbolic quotients); and central kernels outside [Q,Q] over *infinite* Q/N. For the last, the analogue of Λ_G = Γ is open.

## 7. Insight and recommended next direction

1. **Most "algebraic" structure is invisible to AC obstructions.** Solvable radicals, finite normal subgroups inside [Q,Q], nonabelian chief factors and monoliths can all be quotiented away. The only kernels that survive are central ones outside [Q,Q], and Theorem 5 kills these over finite groups. A quotient-based proof of non-triviality must use a group with *no minimal normal subgroups*: just-infinite residually finite groups (e.g. arithmetic groups with the congruence subgroup property) or groups like F with no small normal subgroups at all (e.g. torsion-free hyperbolic quotients). It must also show unbounded distances over its finite quotients. This sharpens E's "infinite, non-solvable, non-simple".
2. **Concrete next step (obstruction side).** Study the open case left by §6 for an infinite base: Q = H ×_{H_ab} ℤ² with H = SL(2,ℤ), the braid group B₃ or a hyperbolic triangle group. There Λ_H can be infinite-index or non-congruence, and the δ-invariant of Proposition 5.1 still makes sense with C infinite. The computable test is whether π_H(U) and π_H(B_U) are Z-equivalent. Controls: AK(1), AK(2). For AK(3) one needs H in which neither relator dies (Corollary 1.1), e.g. H = PSL(2,ℤ[1/2]) or a (2,3,7)-triangle-group quotient with ℤ² fibre.
3. **For constructive agents.** Corollary 1.1 is also a search heuristic. Any pair in AK(3)'s class with a coordinate whose one-relator group has a "large" family of quotients removes all those quotients from consideration. Conversely, a real obstruction must survive killing every short class coordinate, and §5.3 gives 164 of them.

## 8. Files written

- `research/research-h.md` (this note).
- `experiments/h_monodromy.cpp`: AC-monodromy / δ_G computation for permutation groups (`--selftest`).
- `experiments/h_groups.py`: group catalogue and driver (`--selftest`).
- `experiments/h_class_coordinates.py`: class coordinates of AK(3) from the repository certificates (`--selftest`).

No certificates were produced: no AC equivalence is claimed.

## References

- A. V. Borovik, A. Lubotzky, A. G. Myasnikov, *The finitary Andrews–Curtis conjecture*, arXiv:1103.1295 (author copy: https://web.stevens.edu/algebraic/alexeim/Publications/AC%20Conjecture/FinitaryAC.pdf). Snippet level.
- L. Guyot, *On Andrews–Curtis conjectures for soluble groups*, arXiv:1612.06912. Snippet level.
- A. Myropolska, *Andrews–Curtis and Nielsen equivalence relations on some infinite groups*, arXiv:1304.2668, and Geneva thesis (2015). Snippet level.
- A. V. Borovik, E. I. Khukhro, A. G. Myasnikov, *The Andrews–Curtis conjecture and black box groups*, arXiv:math/0110246 (authors as recalled; snippet level; its Theorem 5.12 concerns preimages of AC-graph components of G/[G,G]).
- J. Nielsen (1917), IA(F₂) = Inn(F₂); classical.
- Repository notes A–F, and certificates `d_ak3_*.json`, `ms3_to_ak3_exact.json` (used read-only).

## Coordinator's review (second reader, 2026-11-02)

Checked by the coordinating agent after H finished; H's own files were otherwise left as written.

- Theorem 1, Lemma 2.1 (both the module identities and the right-action conventions), Lemma 2.2, Theorem 2(i), Corollary 3, Theorem 4 (existence and structure) and Theorem 5 were re-derived line by line and are correct as stated.
- **Theorem 2(ii) is stated too strongly.** The clause "for all n₀, n₁ ∈ N, the pair (s n₀, t n₁) is AC-equivalent to (s,t)" needs the extra hypothesis that (s n₀, t n₁) normally generates Q. Counterexample to the literal statement: Q = A₅ × A₅, N = 1 × A₅, (s,t) = ((g₁,g₂),(h₁,h₂)) any generating pair; with n₀ = (1,g₂⁻¹), n₁ = (1,h₂⁻¹) the pair (s n₀, t n₁) = ((g₁,1),(h₁,1)) normally generates only A₅ × 1, so it cannot be AC-equivalent to (s,t). The proof uses the missing hypothesis exactly where (†) is applied to the pairs (t n₁, s n₀) and (s,t). The hypothesis holds in every application in this note: the perturbed pair is always the endpoint of an AC path in Q starting from a pair that normally generates Q (a lifted path from Q/N), and AC moves preserve normal closure. Hence the consequences "P is standardizable if its image in Q/N is", "Q obstructs U iff Q/N does", Corollary 3, Theorem 4 and Theorem 5 are unaffected.
- Minor: in Theorem 2(ii) the direction "Q has (AC) ⇒ Q/N has (AC)" is asserted but not proved; it is never used (Corollary 3 only descends, i.e. uses "Q/N has (AC) ⇒ Q has (AC)"). The abelianization condition does pass to Q/N because a nonabelian minimal normal subgroup is perfect, so N ⊆ [Q,Q] and (Q/N)_ab = Q_ab.
- Self-tests re-run by the coordinator: `h_monodromy --selftest`, `h_groups.py --selftest`, `h_class_coordinates.py --selftest`, and `h_groups.py --bin ... --pairs 2 --max-order 2500` all passed.
