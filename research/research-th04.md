# Research TH04: rigidity of the torus island of AK(n) — twist rigidity in torus-knot groups, the hidden involution, and an explanation of the third island node

Date: 2026-11-09 (Los Angeles). Independent research agent TH04 (round 5, theory round).

**Status (draft, being completed).** Partial results with complete proofs. **No AC trivialization of AK(3), no proof that AK(3) is not AC-trivial, no counterexample.** The full "island theorem" (seed: *the torus-type presentations reachable from AK(n) by ACM moves with a torus-type relator frozen are exactly 3 Aut(F₂)-orbits*) is **not** proved; it is reduced to two precisely stated missing lemmas (§6). Everything concerns the ordinary (unstabilized) AC relation.

## 0. Central claims (labels)

Notation. X = x⁻¹, Y = y⁻¹. For coprime integers p, q with |p|,|q| ≥ 2: R = xᵖyᑫ, T = T_{p,q} = ⟨x,y | R⟩ (a torus-knot group), Q = C_|p| * C_|q| = ⟨s⟩ * ⟨t⟩, π: F₂ → Q (x ↦ s, y ↦ t), ab_T: F₂ → ℤ, x ↦ q, y ↦ −p. A word W is a *partner* of R if ab_T(W) = ±1 (necessary for ⟨x,y | R, W⟩ = 1, and for W to be conjugate in T to any relator of a balanced presentation of a perfect group containing R). Λ = {(a,b) ∈ ℤ² : qa − pb = ±1} is the set of exponent vectors of partners.

*Twists* are the automorphisms α: y ↦ xᵖy, β: x ↦ yᑫx, σ_x: x ↦ X, σ_y: y ↦ Y (the other generator fixed) and their products. They preserve ker π, so **a twist never changes the syllable length ("meridian defect") of the image in Q** and changes the syllable necklace only by inverting all s-exponents and/or all t-exponents. This is the mechanism that produces infinitely many torus-type (or primitive) words with the same defect; it is why G's island could only be a bounded observation.

| # | statement | label |
|---|---|---|
| T1 | **Twist rigidity.** If {|p|,|q|} ≠ {2,3}, W is a partner of R and θ is a twist such that θ(W) is again a partner (e.g. θ(W) conjugate to W^{±1} in T), then θ is, up to inner automorphisms, one of id, σ_xσ_y, ι, σ_xσ_yι, where ι exists only if 2 ∈ {|p|,|q|} (T2). All four act on T as ± the identity and give the same Aut(F₂)-orbit of the pair (R, W). So **in every torus-knot group other than the trefoil group, the infinite twist family of a partner contains no second partner** | proved here (§2, ping-pong on ℤ²) |
| T2 | **Hidden involution.** If p = ±2, the automorphism ι: x ↦ y^{−2q/p}x⁻¹, y ↦ y induces the identity of T and sends R to a conjugate of R⁻¹. Hence every conjugacy class of T(2,m) that contains a torus-type word W also contains the different cyclic word ι(W), and (R, ι(W)) is an automorphic image of (R⁻¹, W) | proved here (§3) |
| T3 | **The trefoil group is the exception.** For (p,q) = (2,−3) the twist κ: x ↦ x, y ↦ x²Y maps every partner W with exponent vector ±(1,−1) and reversal-invariant necklace to a word conjugate to W⁻¹ in T. For partners with exponent vector outside the 8-point set Λ₀ = {(±1,±1), (±1,±2)} ∩ Λ, T1 still holds | proved here (§2.3) |
| T4 | **Third island node, uniformly in n.** For every n ≥ 1, AK(n) ~AC (cyc ψκ(W_n), xyxYXY) (ψ, W_n as in research-g). For n = 3 this is G's third island orbit; certificate `certificates/th04_ak3_to_kappa_node.json` | proved here (§4) + certificate |
| T5 | **Structure of the island.** For n = 3, 4, 5 and the bounds of §5, the torus-type words conjugate to the partner or its inverse are: in T(n,n+1): b only; in the trefoil group: exactly the six words U_n, ιU_n, W_n, ιW_n, κW_n, ικW_n (two twist families); in T(2,2n+1): exactly N, ι′N | experiment (exact bounds in §5); the six memberships are proved for all n |
| T6 | **Generating pairs on the Bass–Serre tree.** If (u,v) is a basis of F₂ then (πu, πv) is: two elliptics with adjacent fixed vertices; or an elliptic whose fixed vertex lies on the axis of the hyperbolic one; or two hyperbolics with intersecting axes. In the first case every u^a v^b has defect ≤ 2 | proved here (§6.1) |

What is **not** proved: that every torus-type word in the relevant classes lies in one of the listed twist families (§6.2 states the two missing lemmas exactly).
