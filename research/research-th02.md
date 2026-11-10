# Research TH02: hidden reflections — the mechanism behind the realized automorphisms

Date: 2026-11-09 (Los Angeles). Independent research agent TH02 (round 5, theory round).

**Status.** **No AK(3) trivialization, no proof of non-triviality, no counterexample, nothing on the full conjecture.** What is achieved: the automorphisms that earlier notes found *by search* in the stabilizers Ŝ(U) = {M ∈ GL₂(ℤ) : φ_M(U) ~AC U} are explained by one symbolic mechanism, proved here and compiled to replayable certificates with no search. Every statement is labelled *proved here*, *experiment* (exact bounds), *externally reported*, or *open*.

**Central claims (all for ordinary AC moves; F = F(x,y), X = x⁻¹, Y = y⁻¹).**

| # | statement | label |
|---|---|---|
| 1 | **Hidden reflection.** If (u,v) is a basis of F, n ∈ ℤ, and r is conjugate to (u²vⁿ)^{±1}, then β = (u ↦ u⁻¹v⁻ⁿ, v ↦ v) satisfies β(r,s) ~AC (r,s) for **every** word s. β acts as the identity on F/⟨⟨r⟩⟩; its matrix is the reflection with (−1)-eigenvector ab(r) and (+1)-eigenvector [v] | proved here (Thm 1); 360 generated certificates replayed |
| 2 | N's group D₆ ⊆ Ŝ(C4) is exactly ⟨β_A, β_w⟩, the hidden reflections of the two relators of C4 = (x⁵z², w²y⁵), z = x⁻¹y, w = xy⁻²; D's swap on AK(3) is the hidden reflection of the braid relator, and it is realized on (xyxYXY, s) for every s, in particular on AK(n) for all n | proved here (Cor. 2, Thm 5); certificates |
| 3 | **Double form.** T(a;2a,q) ~AC D(a;q) := (xY²xy^{q−2}, xᵃyXy) for all a, q (one ACM move, two insertions) | proved here (Lemma 3) |
| 4 | **Trace formula.** For a pair of T(2,·)-type relators with exponent determinant ±1, tr(R₁R₂) = 2 − D, D = det(v₁,v₂)·det(ρ₁,ρ₂) odd; ⟨R₁,R₂⟩ is finite iff D ∈ {1,3}. For D(a;q): D = δ := 4a − (a−1)q. So C4 ~ D(4;5) and the C3-form D(2;7) (δ = +1) give D₆, while X = T(2;4,9) ~ D(2;9), T(6;12,5), T(−4;−8,3) (δ = −1) give an infinite dihedral group with a hyperbolic element of trace 3. **The difference between C3/C4 and X is the sign of δ, not the value of a** | proved here (Thm 4); certificates |
| 5 | For every n ≥ 1, Ŝ(AK(n)) ⊇ ⟨−I, swap, [[−1,3],[0,1]]⟩, an infinite group containing a hyperbolic element of trace 3 (uses research-g Theorem G1) | proved here (Thm 5) |
| 6 | **Ŝ(Y) is infinite for Y = T(4;7,5)** (N reported no result for Y): Y ~AC Y′ = (x⁴yXy, xyXY³Xy), a pair of types T(2,5), T(2,3) with D = −3, trace 5 | proved here by certificate (Thm 6) |
| 7 | **Limits of the mechanism.** For a torus relator xᵖy^q (coprime, \|p\|,\|q\| ≥ 2) the stabilizer of the cyclic word up to inversion in Out(F₂) is {±I} if \|p\|,\|q\| ≥ 3 and the Klein four-group {±I, ±β} if min = 2. All hidden reflections lie in the index-2 subgroup Γ_τ = ker(det · sgn(M mod 2)) of GL₂(ℤ); hence they can **never** realize x ↦ x⁻¹, y ↦ y⁻¹, x ↦ xy^{±1} or y ↦ yx^{±1} on any class | proved here (Prop. 7; uses Whitehead's peak-reduction theorem, classical) |
| 8 | In Fwd(C4, 28) (216,640 states) 203,706 states carry a T(2,n)-type relator; all have n = 5 and their hidden reflections are exactly four matrices, all in D₆. An exact frozen-relator (unbounded-conjugator) search for further T(2,n)-type partners in a box finds only the D₆-images. **No element of Ŝ(C4) outside D₆ was found** | experiment (§5) |

So the best outcome named in the brief (a matrix outside D₆ in Ŝ(C4)) was **not** reached; what is reached is a symbolic proof of everything previously known about Ŝ(C4), Ŝ(X), a new infinite stabilizer (Y), a uniform statement for AK(n), and a precise description of what this mechanism can and cannot produce (§4, §6).

## 0. Previous work read and choice of direction

Read in full: `README.md`, `research-i.md`, `research-n.md`; status paragraphs and coordinator's reviews of A–O; `research-g.md` §2–3 (Lemma 1, Lemma G0, Theorem G1), `research-d.md` (Lemmas D2, D3, D6). Facts used, as verified there: AC equivalence is Aut(F₂)-equivariant (D2); an ACM move (replace r_i by a word conjugate to r_i^{±1} modulo ⟨⟨r_j⟩⟩) is a composite of ordinary AC moves (G0); Ŝ(U) is a subgroup of GL₂(ℤ) = Out(F₂) and Ŝ(φU) = M_φ Ŝ(U) M_φ⁻¹ (N §1–3); conjugacy in ⟨x,y | xᵖy^q⟩ is decided by the syllable necklace in C_p * C_q and the central exponent (G Lemma 1); AK(n) ~AC (ψ(W_n), xyxYXY) (G Theorem G1).

**Direction** (the seed, kept): all known elements of the stabilizers were found by search (N: orbit coincidences in forward sets; D, I: images of generators). I looked for automorphisms φ that fix a relator r as a cyclic word up to inversion and act on F/⟨⟨r⟩⟩ by an inner automorphism: then φ(s) is conjugate to s modulo r for *every* partner s, so φ(r,s) ~AC (r,s) by one ACM move. The surprise is that such φ exist outside {inner, ±I} exactly for relators with an exponent 2 (type T(2,n)), and that both relators of C4 are of this type in two different bases. This is new relative to A–O (N lists the matrices; I and G work with frozen torus relators but never use automorphisms acting trivially on the one-relator quotient) and disjoint from the other nine seeds.

**Notation.** ab(w) ∈ ℤ² is the exponent vector. Matrices are written by rows, columns are the images of x and y (N's convention); automorphisms are composed as maps. A cyclic word is of **type T(2,n)** if it is conjugate to θ(x²yⁿ)^{±1} for some θ ∈ Aut(F₂); we always take n odd, |n| ≥ 3 (|n| = 1 is the primitive case). T(a;p,q) = (xᵖy^q, xᵃyXy), A = xᵃyXy, m = a+1, z = Xy (I's notation).
