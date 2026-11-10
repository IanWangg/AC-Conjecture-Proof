# Research TH15: a self-contained uniform proof that Aut(F₂) is AC-realized on AK(n), n ≥ 2

Date: 2026-11-09 (Los Angeles). Independent research agent TH15 (round 5, theory round).

**Status.** *Proved here (complete symbolic proof + replayed certificates):* for every n ≥ 2 and every
φ ∈ Aut(F₂), AK(n) is ordinary-AC-equivalent to φ(AK(n)) (Theorem 1). The proof consists of two
closed-form paths of 2n+1 cyclic products each — one for the swap σ = (x ↔ y), one for the
transvection a = (x ↦ xy⁻¹, y ↦ y) — plus the fact that σ, a and inner automorphisms generate
Aut(F₂). Consequently the AC class of AK(n) is a union of Aut(F₂)-orbits for every n ≥ 2, and the
places where the repository used Panteleev–Ushakov's theorem as an external input (G1's
"up to Aut(F₂)" reading, K1.3, Corollary D7 for n ≠ 3) are now unconditional (Corollaries 2–5).
*Not achieved:* no AC trivialization of AK(3), no obstruction, no counterexample; the theorem
itself is not new (Panteleev–Ushakov, arXiv:1609.00325, externally reported) — only the explicit,
uniform, machine-checked proof is contributed. No novelty claim.

**Central claims (for the referee).**

1. **Theorem 1.** For all n ≥ 2 and all φ ∈ Aut(F₂): AK(n) ~AC φ(AK(n)) (relators up to conjugation
   and inversion; no stabilization, no quotient argument in the final statement).
2. **Proposition A (swap).** (p_n, b) → (q_n, b) by 2n+1 cyclic products with b frozen, every
   multiplier a rotation of b⁻¹; packaged peak total length 2n+13. Since σ(b) = b⁻¹ exactly, this
   realizes σ. (The same argument gives (w, b) ~AC σ(w, b) for *every* word w: Lemma A′.)
3. **Proposition B (transvection).** (p_n, b) → ((xY)ⁿY^{n+1}, yxyXX) = a(AK(n)) up to
   rotation/inversion, by 2n+1 cyclic products in five phases (frozen relator alternates
   b, u′, b₁, u″, b₂), packaged peak 4n+7. The intermediate relator b₁ = XY^{n+1}xyⁿ is a
   Baumslag–Solitar relator, and the phase-III state is a Miller–Schupp-type presentation.
4. Generated certificates (n = 2,…,8 for both maps, and for all seven "Nielsen-type" maps
   swap, x↦x⁻¹, y↦y⁻¹, x↦xy^{±1}, y↦yx^{±1} by transport/composition) pass
   `experiments/elementary_verify.py`.

Notation: X = x⁻¹, Y = y⁻¹; b = xyxYXY; p_n = xⁿY^{n+1}; q_n = yⁿX^{n+1}; AK(n) = (p_n, b);
cyc(w) = cyclic reduction; "rotation" = cyclic rotation. A **cyclic product** replaces one relator r
by cyc(g·r′) or cyc(r′·g), where r′ is a rotation of r^{±1} and g is a rotation of the other
relator or of its inverse; it is a composite of ordinary AC moves (research-d Lemma D1(a),(b)).

## 1. Previous work read and choice of direction

Read: `README.md` in full; notes A, C in full; D §1–3 and §4.5; K §2–3; G §2–3; J §4 (Lemma J0,
Theorem J1); status paragraphs of the rest. Tools re-used read-only: `experiments/d_certify.py`
(cyclic-product path → strict certificate), `experiments/elementary_verify.py` (replayer).

Facts used from earlier notes (re-verified where used): Lemma D1(a),(b) (rotation, inversion,
interchange and cyclic products are ordinary-AC composites); Lemma D2 (letterwise transport of an AC
sequence by φ ∈ Aut(F₂)); the subgroup argument inside the proof of Lemma D6. A's observation that
Δ = xyx conjugates x to y in B = F/⟨⟨b⟩⟩ is the swap mechanism.

**Choice of direction.** I kept the seed. Reason: Lemma D6 (n = 3) rests on seven search-found
certificates, and for n ≠ 3 the repository quotes Panteleev–Ushakov; a symbolic, uniform proof
closes that dependency for the whole family and is checkable by hand. Decoding D's n = 3
certificate for x ↦ xY (7 cyclic steps) showed a pattern linear in n (as C found for the MS
bridge); the swap is one Δ-conjugation spelled out letter by letter. New relative to A–O: the
uniform paths and their proofs (D has n = 3 only; G, K and I quote the external theorem for n ≠ 3).
Not duplicated by the other round-5 seeds as listed in my brief (TH02 excludes AK(n); TH11 is
about stabilizers of single relators; TH13 about a two-parameter family).
