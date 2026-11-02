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

- [D](research/research-d.md), constructive: 82 verified certificates, including 34 Miller–Schupp benchmark presentations and a second length-13 presentation AC-equivalent to AK(3), and AC realizations of the generators of Aut(F₂) on AK(3). AK(3)'s component in the cyclic-product graph to total length 28 (69.2M states) has no primitive relator and matches none of ≈1.29M published AC-trivial presentations, even up to Aut(F₂). These are search bounds, not obstructions.
- [E](research/research-e.md), obstructions: AK(3) is AC-trivial iff its AC distances along an explicit chain of finite 2-groups stay bounded; no simple quotient and no quotient of ⟨x,y | x³=y⁴⟩ or B₃ can obstruct. Exhaustively, any trivialization by the 15 standard instructions needs ≥ 15 moves and passes through total freely reduced length ≥ 21.
- [F](research/research-f.md), other families: no Aut(F₂)-image of AK(n), of any MS(n,w), or of the trivial members of Johnson's P(m,n) is thickenable, so Lackenby's 2026 "thickenable ⇒ AC-trivial" theorem cannot apply to them directly. Every thickenable trivial-group class of length ≤ 16 is trivialized by strict descent.

Cross-check: D and E independently found the same second length-13 class in AK(3)'s AC class, (x²yx⁻¹y⁻², x³y⁻²x⁻¹y) up to signed generator permutation. All 89 strict ordinary-AC certificates pass `python3 experiments/elementary_verify.py <file>`. Two files use other formats: `certificates/ms3_to_ak3.json` (C's packaged certificate, checked by `python3 experiments/ms_ak_family.py --verify certificates/ms3_to_ak3.json`) and `certificates/e_ak3_quotient_paths.json` (quotient-only paths, explicitly **not** AC trivializations).

## Verification standard

A positive ordinary AC result must supply elementary relator moves and a replayable certificate, or a complete mathematical proof. Stabilization, changes of generators, and quotient rewriting must be explicitly justified rather than silently treated as elementary relator moves. An obstruction must be invariant under all permitted moves and distinguish the target from the standard tuple. Any computational exclusion states its move set and finite bounds.

## Initial sources to audit

- Lisitsa (2025), corrected published abstract: https://doi.org/10.1016/j.jaca.2025.100041 . It reports that an earlier stable AK(3) claim relied on an incorrect theorem.
- Gilman and Myasnikov, *Andrews–Curtis groups*: https://gcc.episciences.org/15972/pdf .
- Carreras (2026 preprint), machine-checkable length-14 equivalence certificates: https://arxiv.org/abs/2607.23611 .

Each research note must distinguish checked deductions, externally reported claims, experiments, and open questions.
