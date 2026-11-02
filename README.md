# Andrews–Curtis research

Research target: ordinary (unstabilized) Andrews–Curtis triviality of

    AK(3) = <x,y | x^3 y^-4, xyx y^-1 x^-1 y^-1>.

## Status

No proof or counterexample is established by this repository. This is a research log; bounded search failures are not proofs of nontriviality, and proofs that the presented group is trivial are not AC trivializations.

The repository was empty when this investigation began on 2026-11-02. Three independent research agents are reviewing previous primary literature before choosing their own directions. Their findings and reproducible artifacts will be recorded under `research/` and `experiments/`.

## Verification standard

A positive ordinary AC result must supply elementary relator moves and a replayable certificate, or a complete mathematical proof. Stabilization, changes of generators, and quotient rewriting must be explicitly justified rather than silently treated as elementary relator moves. An obstruction must be invariant under all permitted moves and distinguish the target from the standard tuple. Any computational exclusion states its move set and finite bounds.

## Initial sources to audit

- Lisitsa (2025), corrected published abstract: https://doi.org/10.1016/j.jaca.2025.100041 . It reports that an earlier stable AK(3) claim relied on an incorrect theorem.
- Gilman and Myasnikov, *Andrews–Curtis groups*: https://gcc.episciences.org/15972/pdf .
- Carreras (2026 preprint), machine-checkable length-14 equivalence certificates: https://arxiv.org/abs/2607.23611 .

Each research note must distinguish checked deductions, externally reported claims, experiments, and open questions.
