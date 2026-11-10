# Research TH18: killers of BS(n,n+1) and the t-length filtration of the Miller–Schupp family

Date: 2026-11-09 (Los Angeles). Independent research agent TH18 (round 5, theory round).

**Status (draft in progress — central claims first).** Partial results with complete proofs. **No AC trivialization of AK(3), no proof that AK(3) is not AC-trivial, no counterexample.** Everything concerns ordinary (unstable) AC equivalence; "ACM move" means a quotient-conjugacy move, an explicit composite of ordinary AC moves (Lemma G0 of note G).

Notation: X = x⁻¹, Y = y⁻¹; G_n = BS(n,n+1) = ⟨x,y | r⟩, r = r_n = x⁻¹yⁿxy⁻⁽ⁿ⁺¹⁾, an HNN extension of ⟨y⟩ ≅ ℤ with stable letter x; σ(w) = x-exponent sum; MS(n,w) = (r_n, w). ℓ(w) = number of x-letters of a cyclically (Britton-)reduced conjugate of w in G_n (the *t-length*; a conjugacy invariant by Collins' lemma).

**Central claims (all proved in §2 unless marked).**

| # | statement | label |
|---|---|---|
| T1 | The killers (normal generators) of G_n are exactly the elements with σ = ±1 (Miller–Schupp 1999; proof reproduced) | classical, proof included |
| T2 | Complete conjugacy invariant for elements with σ ≠ 0: the sign necklace d of the cyclically reduced form x^{d₁}y^{a₁}⋯x^{d_ℓ}y^{a_ℓ} together with a mod Λ_d, where Λ_d ⊂ ℤ^ℓ is the explicit lattice spanned by q_ie_i − p_ie_{i−1}; its index is (n(n+1))^{(ℓ−1)/2} when σ = ±1. So conjugacy with **unbounded** conjugators is decided exactly, and for every ℓ there are only finitely many killer classes of t-length ℓ | proved here (Britton + Collins) |
| T3 | The class of w (σ(w) = ±1) contains a primitive element of F₂ ⇔ w ~ x^{±1} in G_n ⇔ ℓ(w) = 1. Hence MS(n,w) is AC-trivial whenever ℓ(w) = 1, by one r-frozen ACM move and Lemma D3; and for n = 1 every MS(1,w) is of this kind | proved here |
| T4 | ℓ = 3: for n ≥ 2 there are exactly n(n−1) classes with σ = +1, namely C_b = [x²y^bx⁻¹y^{−b}], b ∈ ℤ/n(n+1), n ∤ b, (n+1) ∤ b; x y^a x y^{b′} X y^{c′} lies in C_b iff b ≡ b′ (mod n+1), b ≡ −c′ (mod n) | proved here |
| T5 | C's bridge word XYx²Y (the AK(n) partner) lies in C_{2n+1} for every n ≥ 2; it has ℓ = 3, so **for every n ≥ 2 (also n = 2) no primitive element is conjugate to it in G_n**; and no single ACM move from M_n = MS(n, XYx²Y) reaches a primitive relator (the other direction is G2(b) transported by x ↦ xy) | proved here (+ G2(b)) |
| T6 | "Divisor classes": if b divides n or n+1 (and n ∤ b, n+1 ∤ b), then every MS(n,w) with w ∈ C_b^{±1} is AC-trivial by two ACM moves and D3: in ⟨x,y | y^bxy^{−b} = x²⟩ the relator r is conjugate to the primitive y⁻¹x^{±(2^m−1)}. Among the representatives x²y^bXy^{−b} this is sharp: r is conjugate to a primitive there iff b | n or b | n+1 | proved here; certificates §4 |
| T7 | n = 2: the bridge class C_5 = C_{−1} **is** the Johnson class (−1 ≡ 1 mod 2), so every MS(2,w) with ℓ(w) ≤ 3 is AC-trivial (a new 2-ACM-move proof for AK(2)'s class). n = 3: the six ℓ = 3 classes are C_{±1}, C_{±2} (AC-trivial by T6) and C_{±5} = the classes of the bridge word and its mirror; so **every MS(3,w) with ℓ(w) ≤ 3 is AC-trivial or AC-equivalent to AK(3)** (using D6 for the mirror), and the bridge class coincides with a divisor class iff n ≤ 2 | proved here |

