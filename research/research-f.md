# Research F: the 3-manifold (thickenable) locus and the hard rank-2 families

Date: 2026-11-02. Independent research agent F (round 2).

**Status:** partial structural results with verified code and certificates. **No AK(3) trivialization, no counterexample, no proof or disproof of the AC conjecture.** The main theorems below say that every presentation in the Aut(F₂)-orbits of AK(n) (all n ≥ 1), of every Miller–Schupp presentation MS(n,w) (n ≥ 1), and of all six known residual length-14 classes, is **not** thickenable, so the recent theorem "thickenable ⇒ AC-trivial" can never be applied to them directly; and that, conversely, every thickenable presentation of the trivial group of total length ≤ 16 (relative to a published complete class enumeration) is trivialized by a short, strictly length-decreasing descent whose compiled elementary certificates replay with peak ≤ 25. Novelty of all statements is **not established**.

**Summary of results, with labels.**

| # | statement | label |
|---|---|---|
| 1 | Thickenable balanced presentations of the trivial group are (unstably) AC-trivial | externally reported (Lackenby 2026); classical sketch in §2 |
| 2 | Link criterion for orientable thickenability; two decision procedures, cross-validated | proved here (§1) + experiment (validation) |
| 3 | Thickenable ⇒ both one-relator quotients have symmetric Alexander polynomial (F2); hence every Aut(F₂)-image of every MS(n,w), n ≥ 1, and of Johnson's P(m,n), is non-thickenable | proved here, using Perelman/Seifert (or Milnor duality) |
| 4 | Torus-knot meridian obstruction (F3); hence every Aut(F₂)-image of AK(n), all n ≥ 1, is non-thickenable | proved here, using classical 3-manifold theorems (§3) |
| 5 | All six length-14 residual classes and 835 of the 838 residual classes of length 13–16 carry Aut-invariant non-thickenability certificates | computer-assisted (§3, §4.5) |
| 6 | Every thickenable trivial-group class of length ≤ 16 (312 classes) is trivialized by strict ACM descent; all 312 certificates replay with peak ≤ 25; all 32 thickenable non-AC-trivial-flagged classes are nontrivial groups | experiment with replayable certificates (§4.3–4.4) |
| 7 | No presentation with thickenable cyclic reduction of length ≤ 16 lies in AK(3)'s cap-25 component | conditional on an external exhaustive search (§5) |
| 8 | Bounded GS-class explorations of AK3, C3, C4, C6, P1 contain no thickenable state; AK(3)'s never improves the "meridian defect" below its own value 6, C3's and C4's do (to 4) | experiment (§4.6) |
| 9 | Whether the meridian defect is ≥ 6 on the whole AC class of AK(3) | open question |

---

## 0. Previous work read and choice of direction

**Repository.** I read `README.md`, `research/research-a.md`, `research-b.md`, `research-c.md` in full and every file in `experiments/` and `certificates/` (the round-1 files; files `d_*`, `e_*` appearing during this session belong to agents D and E and were not used). I re-ran `python3 experiments/elementary_verify.py --selftest` and `... certificates/ms3_to_ak3_exact.json` (32 moves, peak 23: passes). Summary I verified: A proves a nonincreasing ACM plateau for AK(n), n ≥ 3 (so any AK(3) trivialization reaches total length ≥ 14); B gives explicit nilpotent-quotient certificates and the finite-quotient distance reformulation; C proves MS(n, y⁻¹x²y⁻¹) ~AC AK(n) for all n ≥ 2 with certificates.

**Literature check (and its limits).** In this session `arxiv.org`, journal hosts and most mirrors were blocked; I used search-engine result snippets plus read-only clones of public GitHub repositories. Statements below marked *externally reported* were checked only at that level.

- AK(n) = ⟨x,y | xyx=yxy, xⁿ=yⁿ⁺¹⟩ (Akbulut–Kirby 1985); AK(1), AK(2) AC-trivial; AK(n), n ≥ 3, open. Gompf (1991) proved the AK homotopy spheres standard. Shehper et al. (arXiv:2408.15332, NeurIPS 2025) report length-reducibility of AK(n) for n ≥ 5 ("all but two" of the series), many MS(n,w) solved, and an AK(3) stable trivialization; Lisitsa's corrected publication (doi:10.1016/j.jaca.2025.100041) reports that the stable claim relied on an incorrect theorem, so stable AK(3) is again open. No source found claims ordinary AC-triviality of AK(3) as of this date.
- Length-14 frontier: Carreras (arXiv:2607.23611, repo `joe-carr-data/ac-certificates`, read in full) certifies MS(3,yx²y), MS(3,y⁻¹x²y⁻¹) ~ AK(3) and the two MS(2) σ-pairs; P1 = ⟨x,y | x⁻¹y²x=y³, y⁻¹x²y=x³⟩ (Johnson; Burns–Macedońska "possible counterexample 1") is MS(2,x⁻²y⁻¹x²y). An unreviewed exhaustive classification (repo `nahomar/andrews-curtis-solver`, proof-track; read) reports that every length-≤14 trivial-group presentation is AC-trivial or AC-equivalent (up to a signed letter permutation) to one of **AK3, P1, P2, C3, C4, C6** (C3 = (x²yx⁻¹y, xy⁵xy⁻²), C4 = (x⁴yx⁻¹y, xy³xy⁻²), C6 = (x²yx²y⁻², xyx⁻¹y⁻²x⁻¹y)), plus residual lists at lengths 15–16 (838 classes in total) and exhaustive capped components (AK(3): no trivialization below total length 26). An unreviewed AI-produced repository (`alejandrozarco/andrews-curtis-ms14`) gives a 1066-move certificate P1 ~ C6 and capped exhaustions to length 32.
- Romary–Zupan (arXiv:2304.03196, Geom. Dedicata 2024): uniform AC trivializations of a subfamily of R-link presentations via trisections (externally reported).
- **Lackenby, arXiv:2606.06122 (June 2026)**: "thickenable" balanced presentations of the trivial group (2-complex embeds in a 3-manifold) satisfy the **unstable** AC conjecture, with explicit bounds for the stable version (externally reported; abstract-level only).
- Also consulted/known: Miasnikov–Myasnikov (length ≤ 12 all AC-trivial), Havas–Ramsay (length 13 ⇒ AC-trivial or ~AK(3)), Panteleev–Ushakov arXiv:1609.00325 (Aut(F₂) is AC-realized on AK(n)), Bridson 2015 (huge AC lengths), Gilman–Myasnikov arXiv:2506.23031, Burns–Macedońska 1993. The SAIR/Caltech ACC Challenge repo (`SAIRcompetition/Andrews-Curtis`, 10,115 problem presentations) was used as a test bed.

**Direction chosen.** Lackenby's theorem turns *thickenability* into a checkable sufficient condition for ordinary AC-triviality. Nothing in A, B, C (nor, to my knowledge, in the length-14 literature) asks where the hard families sit relative to this "3-manifold locus". My direction, aligned with the "other families / counterexample side" brief: (i) build a verified decision procedure for thickenability of rank-2 presentation complexes; (ii) prove uniform structural theorems placing whole infinite families (and their automorphic images) **outside** the locus — a necessary property of any counterexample and an explanation of why the 3-dimensional route cannot apply directly; (iii) sieve all published hard lists; (iv) show the locus is "easy" in practice (explicit descent certificates). This is complementary to D (search on AK(3)) and E (AC obstructions): my obstructions are **not** AC invariants, and I say so throughout.

---

## 1. Thickenability of rank-2 presentation complexes (proved here; implementation verified)

Let P = (r₁, r₂) be cyclically reduced words in F(x,y) and K(P) the presentation 2-complex (one vertex, edges e_x, e_y, two 2-cells). *K(P) is thickenable* if it embeds in some 3-manifold.

**Lemma 1.1.** If P presents the trivial group and K(P) is thickenable, then a regular neighbourhood N of K(P) is a compact orientable 3-manifold with ∂N ≅ S², N = h⁰ ∪ h¹_x ∪ h¹_y ∪ h²₁ ∪ h²₂.
*Proof.* N collapses to K(P), so π₁(N)=1 and N is orientable. χ(N)=χ(K)=1, so χ(∂N)=2. Lefschetz duality gives H₃(N,∂N) ≅ H⁰(N) = ℤ → H₂(∂N) → H₂(N) = 0, so ∂N has one component, which is a sphere. ∎

**Lemma 1.2 (link criterion).** Let Γ be the vertex link (Whitehead graph): vertices x⁺, x⁻, y⁺, y⁻; one edge for each cyclic corner (a, b) of a relator, joining the head-end of a to the tail-end of b. Every occurrence of a letter g^{±1} is a strand through the 1-cell e_g and owns one half-edge at g⁺ and one at g⁻. Then K(P) has an orientable thickening iff Γ has an embedding in S² in which, for g = x, y, the cyclic order of strands around g⁺ is the **reverse** of their cyclic order around g⁻.
*Proof.* (⇒) Restrict an orientable thickening to the boundary sphere of the 0-handle: Γ is embedded there, and each 1-handle D²×I is glued to the disks around g⁻ and g⁺ by maps that, for an orientable result, have opposite orientation behaviour with respect to the sphere's orientation, so the strands' cyclic orders are reversed. (⇐) Given such an embedding, attach orientable 1-handles carrying the strands as parallel arcs on the annuli ∂D²×I (possible exactly because the orders are reversed), obtaining disjoint simple closed curves on the genus-2 surface that read r₁, r₂; attach 2-handles along them. ∎
By Lemma 1.1 the orientable test suffices for presentations of the trivial group. Equivalently: r₁, r₂ are read by disjoint simple closed curves on ∂(genus-2 handlebody) w.r.t. a fixed pair of meridian disks (a Heegaard-type diagram); the test is a form of Neuwirth's/Berge's realizability test.

**Algorithms** (`experiments/f_thicken.py`). (a) `thickenable_bruteforce`: enumerate cyclic orders at x⁺, y⁺ (forced reversal at x⁻, y⁻), trace faces, require genus 0 on every component — exponential, small words only. (b) `thickenable`: enumerate planar *band graphs* (maximal classes of parallel link edges; a pair carries ≤ 2 bands, and 2 only if the complementary pair carries no edge, since two non-parallel bands separate the other two link vertices), band weights, and the two handle twists; trace the resulting disjoint curves and compare cyclic words — polynomial. (c) `thickenable_fast`: as (b) but the twists are determined while tracing r₁.

**Validation (experiment).** (1) Both (a) and (b) accept 200 pairs generated from random band diagrams and agree on 373 random pairs (177 thickenable). (2) (b) and (c) agree on 3,000 further pairs (1,418 thickenable). (3) Geometric control independent of the code's theory: images (CR φ(x), CR φ(y)) of the standard basis under 298 random automorphisms (products of ≤ 9 Nielsen moves; total length ≤ 40) are realized by handle slides of the standard diagram, hence must be thickenable: **298/298** accepted. (4) Torus controls: (x³, y) accepted; (x², x) (needs a Klein-bottle gluing) rejected, as the orientation analysis predicts. (5) Section 3's theorem-based obstruction never contradicts the exact test (426 unimodular random pairs, 221 obstructed, 190 thickenable, 0 contradictions).

---

## 2. Thickenable ⇒ AC-trivial (externally reported; classical argument sketched)

**Theorem 2.1 (Lackenby, arXiv:2606.06122, externally reported).** Thickenable balanced presentations of the trivial group are AC-trivial (unstably), with explicit bounds in the stable setting. (Abstract, as returned by search: "We also present a proof that thickenable balanced presentations of the trivial group satisfy the (unstable) Andrews-Curtis conjecture"; the introduction notes that the stable statement was known, via the Poincaré conjecture. I could not read the full text.)

For the reader, a classical route in rank 2 (my sketch; not a substitute for the cited proof): by Lemma 1.1 and Perelman, N ≅ B³, so S³ = H ∪ H′ is a genus-2 Heegaard splitting where H = h⁰ ∪ h¹'s and the relator curves β bound a complete disk system of H′. By Waldhausen the splitting is standard; complete disk systems of a handlebody are related by disk slides and isotopy. Slides of β (with the meridian system α of H fixed) change the words by ordinary AC moves (r_i ↦ r_i·g r_j^{±1} g⁻¹, free/cyclic reductions); slides of α change all words by one Nielsen automorphism, and since AC-equivalence is Aut(F₂)-equivariant, these can be postponed to the end, where the words form a conjugated basis, which is AC-trivial by Nielsen moves. Section 4.4 shows the procedure is also effective in practice.

---

## 3. Structural theorems: the hard families avoid the locus (proved here, modulo classical theorems)

Write G_i = ⟨x,y | r_i⟩ and N_i = h⁰ ∪ h¹'s ∪ h²_i ⊂ N.

**Lemma 3.1.** If P presents the trivial group and K(P) is thickenable, then each N_i is a compact orientable 3-manifold with ∂N_i a torus and H₁(N_i) ≅ ℤ; N_i is a solid torus or the exterior of a nontrivial knot K_i ⊂ S³, and N_i ∪ h²_j ∪ B³ = S³.
*Proof.* N = N_i ∪ h²_j with h²_j attached along an annulus A ⊂ ∂N_i, and ∂N = S² = (∂N_i − A) ∪ two disks; so ∂N_i − A is an annulus and ∂N_i (orientable) is a torus. The exponent-sum matrix of P is unimodular, so each row is primitive and H₁(N_i)=ℤ. By Perelman N ≅ B³ ⊂ S³; Alexander's torus theorem says N_i or its complement is a solid torus; a knot exterior with group ℤ is a solid torus. ∎

**Proposition F2 (Alexander obstruction).** If K(P) is thickenable and P presents the trivial group, then each G_i has a **symmetric** Alexander polynomial, Δ_i(t) ≐ Δ_i(t⁻¹).
*Proof.* By Lemma 3.1, G_i = π₁ of a knot exterior or ℤ; knot polynomials are symmetric (Seifert); Δ = 1 for ℤ. (Alternative avoiding Perelman: Milnor's torsion duality for compact orientable 3-manifolds with torus boundary and H₁=ℤ.) Δ_i is a group invariant: for a 2-generator 1-relator presentation with x ↦ t^p, y ↦ t^q (ap+bq=0 for the exponent sums (a,b)), the first elementary ideal is principal, generated by Δ = (∂r/∂y)^φ·(t−1)/(t^p−1) (when p ≠ 0), because ((t^p−1)/(t−1), (t^q−1)/(t−1)) is the unit ideal for gcd(p,q)=1. ∎

**Corollary F2.1 (uniform; all n ≥ 1, all w).** If P presents the trivial group and one relator r satisfies ⟨x,y | r⟩ ≅ BS(n,n+1) (n ≥ 1) — e.g. r is any automorphic image, rotation or inverse of x⁻¹yⁿxy⁻⁽ⁿ⁺¹⁾ — then K(P) is not thickenable. Hence **no presentation in the Aut(F₂)-orbit of any Miller–Schupp presentation MS(n,w) (n ≥ 1) of the trivial group, nor of any member of Johnson's family P(m,n) = ⟨x,y | x⁻¹yᵐx=yᵐ⁺¹, y⁻¹xⁿy=xⁿ⁺¹⟩ = MS(m, x⁻ⁿy⁻¹xⁿy) that presents the trivial group, is thickenable.** (Coset enumeration confirms P(m,n) is trivial for 1 ≤ m,n ≤ 4; both of its relators are BS-type.)
*Proof.* Fox calculus gives Δ_{BS(n,n+1)} ≐ n − (n+1)t, which is not symmetric. Isomorphic one-relator groups have equal Δ, and φ ∈ Aut(F₂) induces ⟨x,y|r⟩ ≅ ⟨x,y|φ(r)⟩. ∎

**Proposition F3 (torus-knot meridian obstruction).** Suppose P presents the trivial group and some φ ∈ Aut(F₂) carries r_i to a cyclic conjugate of x^p y^q with |p|,|q| ≥ 2 (so G_i is the T(|p|,|q|) torus-knot group). If the image of φ(r_j) in G_i/Z(G_i) ≅ C_|p| * C_|q| has cyclic syllable length ≠ 2, then no presentation in the orbit of P under Aut(F₂), rotations, inversions and relator swap is thickenable.
*Proof.* If K(P) were thickenable, by Lemma 3.1 N_i is the exterior of a knot K_i with group ≅ G_i (nonabelian, so K_i is nontrivial), hence K_i is the torus knot T(|p|,|q|) or its mirror (Burde–Zieschang 1966). N_i ∪ h²_j ∪ B³ = S³ says that Dehn filling of N_i along the curve r_j gives S³, so r_j is the meridian slope (Moser 1971 for torus knots; Gordon–Luecke in general), hence r_j is conjugate in G_i to μ^{±1}. In ⟨a,b | a^p = b^q⟩ the meridian is a^v b^u with up + vq = ±1 (Burde–Zieschang, *Knots*, torus-knot chapter), so v ≢ 0 (mod p), u ≢ 0 (mod q) and its image in C_p * C_q has cyclic syllable length 2. The center ⟨a^p⟩ is characteristic; by Kurosh/Fouxe-Rabinovitch every automorphism of C_p * C_q (p ≠ q, both factors abelian, so partial conjugations are inner) is a product of inner and factor automorphisms, which preserve cyclic syllable length. Hence the cyclic syllable length of the image of r_j in G_i/Z(G_i) is an invariant of (G_i, r_j^{±1} up to conjugacy), independent of the identification, and must be 2. Contradiction. Orbit invariance: φ ∈ Aut(F₂) induces isomorphisms of both one-relator groups carrying the partner relator along. ∎

**Corollary F3.1 (uniform, all n ≥ 1).** No presentation in the Aut(F₂)-orbit of **AK(n)** is thickenable, for every n ≥ 1.
*Proof.* The automorphism φ: x ↦ xy⁻¹, y ↦ y²x⁻¹ (inverse ψ: x ↦ xyx, y ↦ yx) satisfies φ(xyxy⁻¹x⁻¹y⁻¹) = x²y⁻³ after cyclic reduction; equivalently the braid relator is the free reduction of a²b⁻³ with a = xyx, b = yx. So G₂ = ⟨x,y | b⟩ is the trefoil group. The partner maps to φ(xⁿy⁻⁽ⁿ⁺¹⁾) = (xy⁻¹)ⁿ(xy⁻²)ⁿ⁺¹, whose image in C₂ * C₃ = ⟨s⟩ * ⟨t⟩ is (st²)ⁿ(st)ⁿ⁺¹: a cyclically reduced alternating word of syllable length 4n+2 ≥ 6 (this matches research-a Lemma 1; also checked by code for n ≤ 60). Apply F3. (For n ≥ 2 the other side also works: research-a Lemma 2 gives syllable length 6 for the braid relator in C_n * C_{n+1}.) ∎

**Corollary F3.2 (computer-assisted check of the hypotheses).** The six length-14 residual classes all have Aut-invariant obstructions (`f_knotlike.meridian_test`, `f_knotlike.alexander`):

| class | relators | Δ₁, Δ₂ | obstruction |
|---|---|---|---|
| AK3 | x³y⁻⁴, xyxy⁻¹x⁻¹y⁻¹ | T(3,4), T(2,3) polys | F3: partner syllables 6 (in C₃*C₄) and 14 (in C₂*C₃) |
| P1 | x⁻¹y²xy⁻³, y⁻¹x²yx⁻³ | 3t−2, 2t−3 (asym.) | F2 |
| P2 | x⁻¹y²xy⁻³, x⁻¹yx²yx⁻² | asym. | F2 |
| C3 | x²yx⁻¹y, xy⁵xy⁻² | T(2,3), T(2,7) polys | F3: 14 (C₃*C₂), 6 (C₂*C₇) |
| C4 | x⁴yx⁻¹y, xy³xy⁻² | T(2,5), T(2,5) polys | F3: 10 and 10 (C₅*C₂) |
| C6 | x²yx²y⁻², xyx⁻¹y⁻²x⁻¹y | t⁴−t²+1, T(2,3) poly | F3 via 2nd relator: 18 (C₂*C₃) |

The automorphisms (found by a bounded Nielsen search, then checked by free reduction) are: braid relator: x ↦ xy⁻¹, y ↦ y²x⁻¹ (image x²y⁻³); C3 r₁ and C4 r₁: y ↦ yx (images x²y²x and x⁴y²x, i.e. x³y² and x⁵y² cyclically); C3 r₂ and C4 r₂: x ↦ xy² (images xy⁷x and xy⁵x, i.e. x²y⁷ and x²y⁵ cyclically); C6 r₂: x ↦ xy⁻¹xy⁻², y ↦ y²x⁻¹ (image x⁻²y³ cyclically). So the length-14 frontier splits into **BS-type** classes (P1, P2, and all MS) and **torus-knot-pair** classes (AK3, C3, C4, C6): in the latter both one-relator quotients are (cable or) torus-knot groups and each relator kills the other's group, as in AK(n) itself. This is a structural reason why AK(n), C3, C4 look alike.

**What this does and does not say.** These obstructions concern specific words; they are **not** AC invariants (an AC move changes the one-relator groups). They show that Theorem 2.1 cannot apply to these presentations or to any automorphic image; any proof of AC-triviality via 3-manifolds must first move by AC moves to a presentation in which both relators define knot groups (or ℤ) with meridional partners. They give **no** evidence of AC-nontriviality.

---

## 4. Experiments (exact commands; outputs from this session)

All scripts are standard-library Python, single-threaded.

**4.1 Self-tests.**
```
python3 experiments/f_thicken.py --selftest     # 200 positives, 373 random pairs agree (177 thickenable)
python3 experiments/f_knotlike.py --selftest    # 426 unimodular pairs, 221 obstructed, 190 thickenable, 0 contradictions
python3 experiments/f_descent.py --selftest     # coset enumeration, descent certificate (27 moves, peak 15), AK(3) no strict step
python3 experiments/f_landscape.py --selftest
python3 experiments/f_sieve.py --selftest
python3 experiments/f_component_sieve.py --selftest
python3 experiments/elementary_verify.py certificates/f_*.json
```
All passed in this session.

**4.2 Sieve of published hard lists** (`experiments/f_sieve.py`; a "hit" would prove AC-triviality via Theorem 2.1).

| list | presentations | thickenable |
|---|---:|---:|
| AK(n), 1 ≤ n ≤ 40 (exact words) | 40 | 0 (consistent with F3.1) |
| six named length-14 residuals + 2 MS(3) | 8 | 0 |
| same, with Aut-ball depth 8, slack 12 | 8 | 0 (as F2/F3 predict) |
| all 1190 Miller–Schupp benchmark presentations (Shehper et al. data) | 1190 | 0 (as F2.1 predicts) |
| all residual classes of lengths 13–16 (`residual_classes16.txt`) | 838 | 0 |
| SAIR ACC challenge problems (`competition/problems/ac.jsonl`) | 10,115 | 1 (ac-01635, see 4.4) |

Commands (paths to the cloned public data; see Section 7):
```
python3 experiments/f_sieve.py --ak 40
python3 experiments/f_sieve.py --list .../nahomar/.../named.txt --format nahomar --depth 8 --slack 12
python3 experiments/f_sieve.py --list .../AC-Solver/.../all_presentations.txt --format ms
python3 experiments/f_sieve.py --list .../nahomar/.../residual_classes16.txt --format nahomar
python3 experiments/f_sieve.py --list .../sair/competition/problems/ac.jsonl --format sair
```

**4.3 Calibration: how common is thickenability?** Over all det ±1 classes (rotation, inversion, swap, signed letter permutations) of the published enumeration `classes17_c22.txt` (flag 1 = in the cap-22 component of (x,y)):

| length | AC-trivial classes (flag 1) | thickenable | flag-0 classes | thickenable |
|---|---:|---:|---:|---:|
| 12 | 590 | 18 (3.1%) | 1 | 1 |
| 13 | 2352 | 49 (2.1%) | 7 | 5 |
| 14 | 4050 | 35 (0.9%) | 20 | 4 |
| 15 | 16731 | 80 (0.5%) | 290 | 13 |
| 16 | 29220 | 56 (0.2%) | 709 | 9 |
| 17 | 121370 | 121 (0.1%) | 5972 | 16 |

Thickenability is rare even among AC-trivial classes, so "0 of 838 residuals" is only mildly informative statistically (≈3 hits expected at the base rate). **All 32 thickenable flag-0 classes of lengths 12–16 present nontrivial groups**, certified here by explicit permutation images (`f_descent.nontrivial_hom`: a nontrivial homomorphism into A5, A6 or A7 for each of the 32; my HLT coset enumeration independently finds a finite index > 1 for 21 of them). This is consistent with theory: they are spines of punctured homology 3-spheres. None of them is in the residual list. At length 17, 15 of the 16 thickenable flag-0 classes are nontrivial or undecided groups and one, (x, xyxyxY²xyxYxyxY²), is a trivial group that is obviously AC-trivial — revealing that the published length-17 flags are unreliable (13 length-17 classes with a relator equal to x are flagged 0). The length ≤ 16 flags were independently checked by their authors; I use length-17 flags only as hints.

**4.4 The locus is easy: strict descent with certificates.** `f_descent.descend` searches for quotient-conjugacy replacements u ← CR(rot(u)·c·v^{±1}·c⁻¹), |c| ≤ K, that *strictly* lower the total cyclic length (the word-level shadow of a Homma–Ochiai–Takahashi wave), and `compile_path` turns them into strict elementary moves of `ordinary-ac-elementary-v1` ending exactly at (x,y).
- All **312/312** thickenable trivial-group classes of lengths 2–16 (the flag-1 thickenable classes; Section 4.3 shows every thickenable flag-0 class is a nontrivial group) were trivialized with K = 2, beam 10 (under a minute in total); every compiled certificate was replayed by `elementary_verify.replay`. Counts per length 2..16: 1,1,1,2,2,7,6,12,11,31,18,49,35,80,56; maximal elementary peak per length: 2,4,5,6,7,8,10,12,12,17,21,22,23,25,25 (so ≤ 25 throughout, and peak − start ≤ 10). The one thickenable trivial-group class found at length 17 also descends.
- One command regenerates all 312 certificates, replays each with `elementary_verify.replay`, and re-certifies the 32 thickenable flag-0 classes as nontrivial groups (93 s):
```
python3 experiments/f_descent.py --batch .../nahomar/proof-track/proof_direction/data/classes17_c22.txt 16
{"certified_trivializations_by_length": {"2": 1, "3": 1, "4": 1, "5": 2, "6": 2, "7": 7, "8": 6, "9": 12, "10": 11, "11": 31, "12": 18, "13": 49, "14": 35, "15": 80, "16": 56}, "max_peak_by_length": {"2": 2, "3": 4, "4": 5, "5": 6, "6": 7, "7": 8, "8": 10, "9": 12, "10": 12, "11": 17, "12": 21, "13": 22, "14": 23, "15": 25, "16": 25}, "thickenable_flag0_certified_nontrivial": 32, "problems": []}
```
- Descent never succeeds on the thickenable nontrivial groups (control) and finds no strict first step for AK(3) (consistent with research-a).
- Stored certificates (replay output):
```
python3 experiments/elementary_verify.py certificates/f_thick15_a.json certificates/f_thick16_a.json certificates/f_thick16_b.json
{"endpoint": ["x", "y"], "moves": 27, "path": "certificates/f_thick15_a.json", "peak_total_length": 15}
{"endpoint": ["x", "y"], "moves": 22, "path": "certificates/f_thick16_a.json", "peak_total_length": 21}
{"endpoint": ["x", "y"], "moves": 21, "path": "certificates/f_thick16_b.json", "peak_total_length": 16}
```
These trivialize (xyxyxY, xyxYxyyxY), (x²yxyxy, x²yxyx²y²) and (x²yx²y², x³y²x²y²); they were already AC-trivial by the published enumeration — the point is the method, not the instances. The single thickenable SAIR challenge problem, ac-01635 = (y⁻²x⁻¹, y⁻³x⁻¹y⁻³x⁻¹y⁻¹x⁻¹) in its exact published words, is trivialized the same way:
```
python3 experiments/f_descent.py --cert YYX YYYXYYYXYX 3 certificates/f_sair_ac01635.json
python3 experiments/elementary_verify.py certificates/f_sair_ac01635.json
{"endpoint": ["x", "y"], "moves": 23, "path": "certificates/f_sair_ac01635.json", "peak_total_length": 13}
```
(It is an easy instance: the peak never exceeds the starting length 13.)

**4.5 Landscape of the 838 residual classes (lengths 13–16).** `python3 experiments/f_landscape.py .../residual_classes16.txt` (2.3 s):

| length | Alexander-asymmetric (F2) | torus-meridian (F3) | unobstructed |
|---|---:|---:|---:|
| 13 | 1 | 1 | 0 |
| 14 | 10 | 4 | 0 |
| 15 | 211 | 21 | 0 |
| 16 | 544 | 43 | 3 |
| total | 766 | 69 | 3 |

So **835 of the 838 residual classes carry an Aut(F₂)-invariant certificate of non-thickenability**. The three unobstructed ones (R180, R182, R185, all with first relator x²yx²y⁻², the C6-type relator with Δ = t⁴−t²+1) are non-thickenable as words and have no thickenable image in an Aut-ball of depth 8 and slack 12 (`f_sieve.py --depth 8 --slack 12`). The two length-13 residual representatives of AK(3)'s class illustrate that the obstruction *type* is not an AC invariant: AK(3) itself is torus-meridian, while (x²yx⁻¹y⁻², x³y⁻²x⁻¹y), reported in the same class up to a signed letter permutation, has a relator with asymmetric Δ = t²−t−1.

**4.6 Component sieve (bounded experiment).** `experiments/f_component_sieve.py w1 w2 --cap C --K 0` explores, by breadth-first search, the classes (modulo rotation, inversion, swap, signed letter permutations) reachable by GS-type moves u ← CR(rot(u)·rot(v^{±1})) with total cyclic length ≤ C. Every move is a composite of ordinary AC moves, so every visited state is AC-equivalent to the start up to a signed letter permutation; a thickenable visited state would prove the start AC-trivial (Theorem 2.1) and descent would make it explicit. This graph is much sparser than the elementary graph (e.g. AK(3) has 11 classes at cap 16) and the search is *not* exhaustive for elementary paths.

| start | cap | classes (complete) | thickenable | both Δ symmetric | seconds |
|---|---:|---:|---:|---:|---:|
| AK3 | 20 | 5,020 | 0 | 170 | 25 |
| AK3 | 22 | 32,295 | 0 | 725 | 198 |
| C3 | 22 | 16,091 | 0 | 771 | 83 |
| C4 | 22 | 634 | 0 | 46 | 3 |
| C6 | 22 | 726 | 0 | 33 | 4 |
| P1 | 22 | 2,738 | 0 | **3** | 20 |
| P1 | 24 | 17,600 | 0 | **17** | 160 |
| C4 | 26 | 19,275 | 0 | 465 | 151 |
| C6 | 26 | 18,873 | 0 | 342 | 140 |
| AK3 | 24 | not completed (killed at the 20-min timeout; no result is claimed) | – | – | >1200 |

**Meridian defect along the components** (`f_landscape.meridian_defect`: smallest syllable length of a partner relator over the relators admitting a torus-knot form; Proposition F3 requires 2 for thickenability). Distribution over the Alexander-symmetric classes found by `--dump`:

| start, cap | defect 2 | 4 | 6 | 8 | 10 | 14 | 18 | no torus form |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| AK3, 20 | 0 | 0 | 24 | 0 | 0 | 140 | 0 | 6 |
| C3, 20 | 0 | 5 | 43 | 3 | 0 | 128 | 0 | 1 |
| C4, 22 | 0 | 1 | 0 | 0 | 45 | 0 | 0 | 0 |
| C6, 22 | 0 | 0 | 0 | 0 | 0 | 0 | 15 | 18 |

In AK(3)'s explored class the defect never drops below AK(3)'s own value 6, while the C3 and C4 classes contain strictly better states, e.g. (x²y⁷x², x²yx⁻¹y) and (x³y⁹x², x²yx⁻¹y) in C3's class (a T(4,7) resp. T(5,9) torus-knot relator whose partner has 4 syllables in C₄*C₇ resp. C₅*C₉) and (x⁴y⁵x⁴, x⁴yx⁻¹y) in C4's class (T(8,5), 4 syllables). No visited state reaches defect 2.

The last column of the first table is a crude "distance to the knot-like world": the BS-type class P1 almost never has both one-relator quotients Alexander-symmetric (3 of 2,738 classes), whereas the torus-knot-pair classes do 2–7% of the time. This matches the finding of Carreras and of the length-32 exhaustions that the MS(2)/P1 blocks are the hardest to connect to anything.

---

## 5. A conditional consequence for AK(3)

*Conditional on the completeness of the published class enumeration up to length 16 and on its exhaustive Theorem A (the Σ-quotient component of AK(3) in the elementary move graph with total length ≤ 25 contains no (x,y); both externally reported, unreviewed):* by Section 4.4, every thickenable trivial-group class of length ≤ 16 has an explicit elementary trivialization of peak ≤ 25, starting from its cyclically reduced representative. Cyclic reduction, rotation and relator inversion never increase total length, and signed letter permutations and the relator swap act on the length-capped graph as automorphisms. Hence **no presentation whose cyclic reduction is thickenable and has total length ≤ 16 lies in AK(3)'s cap-25 component; any ordinary AC path from AK(3) to such a presentation reaches total length ≥ 26.** Unconditionally (from Corollary F3.1 and research-a), AK(3) itself, every automorphic image of it, and its whole A-plateau are non-thickenable.

---

## 6. Honest limits

- The obstructions of Section 3 are properties of words, not of AC classes. They neither prove nor suggest that AK(3), P1, P2, C3, C4, C6 are AC-nontrivial.
- Proposition F2 uses Perelman (or Milnor's torsion duality); F3 additionally uses Alexander's torus theorem, Burde–Zieschang (torus knots are determined by their groups), Moser/Gordon–Luecke and the structure of Aut(C_p * C_q). These are standard but I did not re-derive them. Corollaries F2.1 and F3.1 are uniform proofs; F3.2 is computer-assisted (an automorphism search and syllable counts, both elementary and replayable).
- Theorem 2.1 is externally reported (I could only read its abstract); my Waldhausen sketch is not a full proof.
- The decision procedure is validated by two independent algorithms, a geometric control (automorphic bases), and a theorem-based control (F2), but it is not formally verified.
- Literature access was restricted (no arXiv full texts); "novelty not established" applies to everything, in particular F3.1 may be folklore.
- The component sieves of 4.6 are tiny compared with the published exhaustive capped searches (AK(3) to cap 25, P1/P2/C4 to cap 32, C3 to cap 30, externally reported). Combined with the descent behaviour of 4.4 (peak ≤ start + 10 for lengths ≤ 16), those searches already make short thickenable members of these classes implausible; a thickenable member, if one exists, must be long or reachable only through high intermediate length.

## 7. Files and reproduction

Written by agent F: `research/research-f.md`; `experiments/f_thicken.py` (thickenability, two algorithms + self-test), `experiments/f_knotlike.py` (Fox-calculus Alexander polynomials, torus-form search, syllable lengths), `experiments/f_landscape.py` (obstruction classifier, meridian defect), `experiments/f_sieve.py` (list sieve, Aut-ball), `experiments/f_component_sieve.py` (bounded class exploration), `experiments/f_descent.py` (strict ACM descent, compilation to elementary certificates, Todd–Coxeter, permutation-image nontriviality, batch mode); `certificates/f_thick15_a.json`, `f_thick16_a.json`, `f_thick16_b.json`, `f_sair_ac01635.json` (format `ordinary-ac-elementary-v1`).


Public data used (read-only clones, not committed): `github.com/nahomar/andrews-curtis-solver` (`proof-track/proof_direction/data/{named,residual_classes16,classes17_c22}.txt`), `github.com/shehper/AC-Solver` (`ac_solver/search/miller_schupp/data/all_presentations.txt`), `github.com/SAIRcompetition/Andrews-Curtis` (`competition/problems/ac.jsonl`). Commands are listed in Section 4; total CPU time of all runs in this note is under 30 minutes on one core.

## 8. Insight and recommended next direction

1. **Two kinds of hardness at the frontier.** BS-type classes (all MS, P1, P2) contain a relator whose one-relator group is not a 3-manifold group at all; torus-knot-pair classes (AK(n), C3, C4, C6) consist of two torus-knot relators each of which kills the other's knot group without being its meridian. A path to the thickenable locus must *repair* this: make one one-relator quotient a knot group and the other relator its meridian. That is a graded, checkable target ("meridian defect" = syllable length of the partner in C_p * C_q, 2 being necessary) far richer than reaching (x,y).
2. **Recommended next step:** a *meridian-guided search*: best-first search in the AC classes of C3 and C4 (which already contain defect-4 states such as (x²y⁷x², x²yx⁻¹y)) and of AK(3), scored by the meridian defect, followed by the thickenability test; any defect-2 thickenable state gives an AC trivialization through the descent of Section 4.4 (and, for C3/C4, would shrink the length-14 residual list). The structured family (x^p y^q, x^a y x⁻¹ y) suggested by these states is a natural parametric target for uniform proofs. Conversely, a proof that the defect cannot drop below 6 in AK(3)'s class would be a genuinely new (non-finite-quotient) constraint. For the stable question, extend `f_thicken` to genus 3 (rank-3 stabilizations of AK(3)); a thickenable rank-3 presentation stably equivalent to AK(3) would settle stable AK(3).
3. **Counterexample side.** A counterexample must have an AC class disjoint from the thickenable locus. Families whose every relator in every AC-equivalent presentation stays "BS-like" or "non-meridional" would be candidates; proving such persistence is the precise missing invariant, and it cannot be detected by finite quotients (research-b).

## References

- S. Akbulut, R. Kirby, *A potential smooth counterexample in dimension 4…*, Topology 24 (1985).
- R. Gompf, *Killing the Akbulut–Kirby 4-sphere…*, Topology 30 (1991).
- C. F. Miller III, P. E. Schupp, *Some presentations of the trivial group*, Contemp. Math. 250 (1999).
- A. D. Myasnikov, A. G. Myasnikov, V. Shpilrain, *On the Andrews–Curtis equivalence*, Contemp. Math. 296 (2002), https://arxiv.org/abs/math/0302080 ; Miasnikov–Myasnikov, https://arxiv.org/abs/math/0304305 ; G. Havas, C. Ramsay, IJAC 13 (2003).
- R. G. Burns, O. Macedońska, *Balanced presentations of the trivial group*, Bull. LMS 25 (1993).
- M. Bridson, *The complexity of balanced presentations and the Andrews–Curtis conjecture*, https://arxiv.org/abs/1504.04187 .
- D. Panteleev, A. Ushakov, https://arxiv.org/abs/1609.00325 .
- A. Shehper et al., *What makes math problems hard for reinforcement learning: a case study*, https://arxiv.org/abs/2408.15332 ; data https://github.com/shehper/AC-Solver .
- A. Lisitsa, https://arxiv.org/abs/2501.18601 and corrected publication https://doi.org/10.1016/j.jaca.2025.100041 .
- J. Carr(eras), https://arxiv.org/abs/2607.23611 ; https://github.com/joe-carr-data/ac-certificates .
- E. Romary, A. Zupan, *A family of Andrews–Curtis trivializations via 4-manifold trisections*, https://arxiv.org/abs/2304.03196 .
- M. Lackenby, *The stable Andrews–Curtis conjecture and thickenable presentations of the trivial group*, https://arxiv.org/abs/2606.06122 .
- R. Gilman, A. Myasnikov, *Andrews–Curtis groups*, https://arxiv.org/abs/2506.23031 .
- Unreviewed computational repositories: https://github.com/nahomar/andrews-curtis-solver , https://github.com/alejandrozarco/andrews-curtis-ms14 , https://github.com/SAIRcompetition/Andrews-Curtis .
- Classical: F. Waldhausen, Topology 7 (1968); Homma–Ochiai–Takahashi, Osaka J. Math. 17 (1980); L. Neuwirth, Proc. Camb. Phil. Soc. 64 (1968); G. Burde, H. Zieschang, Math. Ann. 167 (1966); L. Moser, Pacific J. Math. 38 (1971); C. Gordon, J. Luecke, JAMS 2 (1989); J. Milnor, Ann. of Math. 76 (1962).
