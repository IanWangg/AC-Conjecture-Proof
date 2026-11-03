# Andrews–Curtis research

Research target: ordinary (unstabilized) Andrews–Curtis triviality of

    AK(3) = <x,y | x^3 y^-4, xyx y^-1 x^-1 y^-1>.

## Status

No proof or counterexample is established by this repository. This is a research log; bounded search failures are not proofs of nontriviality, and proofs that the presented group is trivial are not AC trivializations.

The repository was empty when this investigation began on 2026-11-02. Findings and reproducible artifacts are recorded under `research/`, `experiments/` and `certificates/`. As of 2026-11-02, AK(3) remains open: none of the notes below trivializes it, obstructs it, or settles the AC conjecture.

## Research notes

Round 1 (independent agents A–C):

- [A](research/research-a.md): every non-length-increasing quotient-conjugacy path from AK(n), n ≥ 3, stays on an explicit plateau, so an AC trivialization of AK(3) must reach cyclic total length ≥ 14.
- [B](research/research-b.md): explicit nilpotent-quotient certificates; AK(3) is non-AC-trivial iff its finite-quotient AC distances are unbounded.
- [C](research/research-c.md): uniform proof that MS(n, y⁻¹x²y⁻¹) is ordinary-AC-equivalent to AK(n) for all n ≥ 2.

Round 2 (independent agents D–F, each read round 1 first and chose its own direction):

- [D](research/research-d.md), constructive: 82 verified certificates, including 34 Miller–Schupp benchmark presentations and a second length-13 presentation AC-equivalent to AK(3), and AC realizations of the generators of Aut(F₂) on AK(3). The set of states forward-reachable from AK(3) by directed cyclic-product moves within total length 28 (69.2M states) has no primitive relator and matches none of the 1.43M published AC-trivial presentations (77,430 Aut(F₂)-orbits), even up to Aut(F₂). These are directed search bounds, not obstructions. **Correction (audit J):** D's Lemma D1(c) "every cyclic-product edge is reversible" is false — see the coordinator's review at the end of D's note — so D's "components" are forward-reachable sets and its separation bounds are for directed paths.
- [E](research/research-e.md), obstructions: AK(3) is AC-trivial iff its AC distances along an explicit chain of finite 2-groups stay bounded; no simple quotient and no quotient of ⟨x,y | x³=y⁴⟩ or B₃ can obstruct. Exhaustively, any trivialization by the 15 standard instructions needs ≥ 15 moves and passes through total freely reduced length ≥ 21.
- [F](research/research-f.md), other families: no Aut(F₂)-image of AK(n), of any MS(n,w), or of the trivial members of Johnson's P(m,n) is thickenable, so Lackenby's 2026 "thickenable ⇒ AC-trivial" theorem cannot apply to them directly. Every thickenable trivial-group class of length ≤ 16 is trivialized by strict descent.

Round 3 (independent agents G–L; each read all earlier notes first; G, I, K, L are still in progress unless listed here):

- [H](research/research-h.md), obstructions: a quotient in which some coordinate of some pair AC-equivalent to U normally generates cannot obstruct U; obstruction lifts through abelian normal subgroups (modulo their intersection with the derived subgroup) and through nonabelian minimal normal subgroups, so no virtually solvable quotient obstructs anything; U is non-AC-trivial iff some "just-obstructing" quotient exists, and such a quotient has no abelian normal subgroup inside its derived subgroup, no nonabelian minimal normal subgroup and no monolith; the abelian fibre-product family G ×_{G_ab} ℤ² carries no invariant. A coordinator's review records one too-strong clause in Theorem 2(ii) (consequences unaffected).
- [G](research/research-g.md), constructive via the 3-manifold locus: makes generalized (ACM) moves with a frozen torus-knot relator exact (conjugacy in ⟨x,y | xᵖyᑫ⟩ is decidable with arbitrary conjugators) and compiles them to certificates. Proves AK(n) ~AC (ψ((xy)ⁿx((yx)ⁿy)⁻¹), xyxYXY) for all n ≥ 1 — a form in which the trefoil and T(2,2n+1) roles swap (certificate for n = 3: 4,055 moves) — and that for n ≥ 3 no single ACM move from AK(n), with arbitrary conjugators or automorphisms, reaches a presentation with a primitive relator (for AK(2) one does, giving a 606-move trivialization). Within its bounds AK(3)'s torus-type states form a rigid 3-orbit island with no primitive or meridional exit. Also shows, by explicit certificates, that two pairs of residual length-15/16 classes (R327 with C3; a member of R74 with one of R62) are AC-equivalent up to an explicit automorphism, so their triviality questions coincide. No AK(3) trivialization or obstruction.
- [K](research/research-k.md), theory: proves for every n ≥ 2 that AK(n) is ordinary-AC-equivalent to P_n = (xyxy⁻²x⁻¹y, xⁿy⁻¹x⁻¹y²) by 4n−1 cyclic products (certificates for n = 3–7, 10; symbolic identities re-derived by the coordinator). |P_n| = n+11, so every AK(n) with n ≥ 5 is AC-equivalent to a strictly shorter presentation, and the whole AK series becomes the killers xⁿ·y⁻¹x⁻¹y² of the single one-relator group ⟨x,y | xyxy⁻²x⁻¹y⟩; AK(3) is AC-trivial iff P_3 = (xyxYYXy, xxxYXyy) is. Also closes two proposed programs: no quantity that differs between AK(2) and (x,y) can be monotone along any complete move class, and E's "uniform correction cost" grows only logarithmically and is otherwise a restatement of the problem. Shehper et al. report a one-parameter family with the same length-reducibility consequence, so novelty is not established.
- [J](research/research-j.md), audit and strategy: proof-checked A–F; found the Lemma D1(c) error above (everything else checked out); proved that the first exit from A's plateau has total cyclic length ≥ 2n+9, i.e. any AC trivialization of AK(3) reaches cyclic length ≥ 15 (A: 14); ranked strategic advice in its §7.

Cross-check: D and E independently found the same second length-13 class in AK(3)'s AC class, (x²yx⁻¹y⁻², x³y⁻²x⁻¹y) up to signed generator permutation. All 89 strict ordinary-AC certificates pass `python3 experiments/elementary_verify.py <file>`. Two files use other formats: `certificates/ms3_to_ak3.json` (C's packaged certificate, checked by `python3 experiments/ms_ak_family.py --verify certificates/ms3_to_ak3.json`) and `certificates/e_ak3_quotient_paths.json` (quotient-only paths, explicitly **not** AC trivializations).

## Verification standard

A positive ordinary AC result must supply elementary relator moves and a replayable certificate, or a complete mathematical proof. Stabilization, changes of generators, and quotient rewriting must be explicitly justified rather than silently treated as elementary relator moves. An obstruction must be invariant under all permitted moves and distinguish the target from the standard tuple. Any computational exclusion states its move set and finite bounds.

## Initial sources to audit

- Lisitsa (2025), corrected published abstract: https://doi.org/10.1016/j.jaca.2025.100041 . It reports that an earlier stable AK(3) claim relied on an incorrect theorem.
- Gilman and Myasnikov, *Andrews–Curtis groups*: https://gcc.episciences.org/15972/pdf .
- Carreras (2026 preprint), machine-checkable length-14 equivalence certificates: https://arxiv.org/abs/2607.23611 .

Each research note must distinguish checked deductions, externally reported claims, experiments, and open questions.
