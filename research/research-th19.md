# Research TH19: referee report on the round-5 theory notes TH01–TH09

Date: 2026-11-10 (UTC). Referee agent TH19 (round 5). This file is written incrementally.

**Scope.** Independent check of the central claims of `research/research-th01.md` … `research-th09.md`.
Verdicts: **VERIFIED** (proof re-derived by me, or claim re-checked by an independent exact computation — stated which),
**PLAUSIBLE-UNCHECKED**, **GAP**, **ERROR**, **OVERCLAIM**. Nothing here is a new result; no AK(3) trivialization,
obstruction or counterexample is claimed by any of the nine notes as far as I have read them.
My check scripts are `experiments/th19_*.py` (standard library only, each < 1 minute).

(Sections follow, one per note; the version of each note I refereed is identified by its line count and time.)

## TH03 (uniform O6 via the Gieseking holonomy) — draft verdicts (version read: 151 lines, 04:15 UTC; to be updated)

| claim | verdict | how checked |
|---|---|---|
| T1: A, B, Y ∈ SL(2,ℤ[ω]) with Y·conj(A) = BY, Y·conj(B) = B⁻¹AY; T = Y·conj(Y) gives a representation of H | VERIFIED | `experiments/th19_th03_check.py` (my own ℤ[ω] arithmetic): all identities of T1(i),(iii),(iv) asserted exactly |
| T2: I(u) = tr(ρ(u)Y·conj(ρ(u)Y)) ∈ ℤ is a conjugacy invariant of (u,1) in G_c | VERIFIED | re-derived: (u,k) ↦ ρ(u)(Y∘conj)^k is a homomorphism into SL₂(ℂ)⋊⟨conj⟩; the square of a degree-1 element is linear and its trace changes at most by complex conjugation under conjugation; it is real |
| T3–T5: recurrence, σ(s) = σ(1−s), σ(n) < τ(n) < σ(n+1) for n ≥ 6, solutions of τ(n) = σ(s) exactly n ∈ {1,2,4,5} | VERIFIED | same script: recurrence and symmetry for |n| ≤ 120; solutions in the box n, |s| ≤ 120 are exactly (1,−2),(1,3),(2,−2),(2,3),(4,−4),(4,5),(5,−5),(5,6) (agrees with the coordinator's `fig8_check.py`); for all n: d(k+1) ≥ 2d(k) > 0 for three consecutive k propagates through u(n+4) = 3u(n+3) − u(n+2) + 3u(n+1) − u(n) (then 3u(n+1) − u(n) > 0 and u(n+2) ≤ u(n+3)/2, so u(n+4) ≥ 2.5u(n+3)); bases hold from k = 2 (τ−σ, Δσ, Δτ) and k = 6 (σ(n+1)−τ(n)) |
| T6: n = 4, 5 isospectral but not conjugate | VERIFIED | `experiments/th19_th03_n45.py`, a third independent PSL(2,7)/PSL(2,13) check (176 and 416 homs of H, as in O): each of (4,−4),(4,5),(5,−5),(5,6) is separated by some hom; the true conjugacies (1,−2),(2,−2) never are. So holonomy traces alone do NOT suffice for n = 4, 5, and the note says so |
| **T7: for all n ≥ 3 and all s, k_n ≁ xˢy in G_c (no c-frozen one-move primitive exit from P_n)** | VERIFIED (scope: c frozen only; says nothing about k_n-frozen moves or ≥ 2 moves) | T2 + T5 + T6 + O's Prop. O2 |
| T8: τ strictly increasing on n ≥ 2, so no c-frozen move joins P_n, P_m (n ≠ m ≥ 2) | VERIFIED | Δτ doubling base from n = 2 |

Output of `python3 experiments/th19_th03_check.py 120`: σ(0..9) = 2, 2, 2, 8, 26, 74, 218, 650, 1928, 5714; τ(1..9) = 8, 8, 20, 74, 218, 632, 1880, 5588, 16562.
`python3 experiments/th19_th03_n45.py`: separating homs (p = 7 / p = 13): (4,−4) 64/208, (4,5) 64/208, (5,−5) 64/96, (5,6) 64/96; (1,−2), (2,−2), (1,3), (2,3): 0/0.
`python3 experiments/th19_th03_J.py`: J(k₁) = J(k₂) = J(x⁻²y) = J(x³y) = 3751/7776; J(k₄) = 110490491431/362797056 ≠ J(x⁵y) = J(x⁻⁴y) = 15320479/31104; J(k₅) = 59111013559/40310784 ≠ 925644326431/362797056 — exactly the values of TH03 Prop. T6.

## TH01 (two-pair abelian lifting) — draft verdicts (version read: 102 lines, 04:21 UTC; to be updated)

| claim | verdict | how checked |
|---|---|---|
| T1 Substitution Lemma 2.1, Cor. 2.2, Lemma 2.3 (torsion collapse) | VERIFIED | re-derived line by line (four (M)-steps; c·p·c⁻¹·t⁻¹ct = cu) |
| T2 Prop. 3.1, Thm 3.2 (transfer lattice), Thm 3.3 (central lifting when [⟨⟨s⟩⟩,⟨⟨t⟩⟩] = 1) | VERIFIED | re-derived, including [R₊,G] ⊇ [G,G] and z_S, z_T central |
| T3(b) (ω,t) ~ (zω,t) in G = ⟨SL(2,3), t \| [t,z]⟩ | VERIFIED | by hand in the Hurwitz quaternions: [j,i] = (ji)² = −1; iω = (−1−i−j+k)/2 has order 3, so iω = (iω)⁴ ∈ ⟨⟨ω[t,i]⟩⟩, hence K ⊆ ⟨⟨p⟩⟩; Cor. 2.2 applies |
| T3(a) one-coordinate rigidity (Gerstenhaber–Rothaus degree argument), Λ = 1 × ⟨z⟩ | VERIFIED (modulo the classical degree fact deg(τ ↦ k₀τ^{n₁}k₁⋯) = Σnᵢ) | re-derived; Z(G) = ⟨z⟩ |
| "the two-pair problem is not settled in general" | accurate (no overclaim) | — |
