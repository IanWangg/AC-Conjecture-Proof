# Andrews–Curtis research

## Status: target problem remains open in this repository

This repository records a six-agent investigation begun on 2026-11-02. It does **not** prove AK(3) AC-trivial or non-AC-trivial, and does **not** prove or disprove the Andrews–Curtis conjecture. No novelty or priority claim is made for the partial results.

The target is ordinary, unstabilized AC triviality of

    AK(3) = <x,y | x^3 y^-4, xyx y^-1 x^-1 y^-1>.

The repository was empty at the start. Six research agents worked in two rounds, with three research agents running concurrently (the maximum available alongside the coordinating agent). Each read previous work before independently choosing a direction. Each report records what it read, its rationale, proof or computation, and limitations. The coordinating agent reviewed the arguments and replayed the artifacts before publication.

## Published research

| Agent | Checked partial result | Evidence and limits |
|---|---|---|
| [A](research/research-a.md) | Exact initial nonincreasing quotient-conjugacy plateau for AK(n), n>=3 | Free-product proofs and exhaustive small equality checks; cyclic peak bound 2n+8, strengthened by F |
| [B](research/research-b.md) | Explicit nilpotent quotient certificates and finite-quotient distance principle | Uniform class-2 path; 48-move class-3 AK(3) path with nonzero higher lifting errors; no free-group trivialization |
| [C](research/research-c.md) | MS(n,y^-1 x^2 y^-1) is ordinary-AC equivalent to AK(n), n>=2 | Symbolic proof and exact elementary certificates; 6n+14 strict moves, hence 32 for n=3; this is an equivalence between unresolved candidates |
| [D](research/research-d.md) | Any ordinary AK(3) trivialization has raw freely reduced total peak at least 19 | Two independent complete cap-18 searches: 2,014,992 ordered/oriented states, 251,874 after projection; cap 19 was not exhausted |
| [E](research/research-e.md) | AK(3)'s image has exact instruction distance 10 to the standard pair in B3 | Explicit infinite-quotient certificate and exhaustive short-ball check; every quotient of B3 has distance at most 10 in the same alphabet; the free lift ends at lengths 23 and 45 |
| [F](research/research-f.md) | Any ordinary AK(n) trivialization, n>=3, has total cyclic peak at least 2n+9 | Analytic proof and independent near-equality checks; AK(3) cyclic peak at least 15; an explicit generalized replacement shows the initial-family argument stops at 15 |

The coordinating agent also recorded [finite PSL quotient distances](research/finite-quotient-experiment.md). E's braid-group certificate proves this entire quotient family's distances are uniformly bounded by 10, so their observed small-prime increase cannot prove nontriviality.

**Length and move conventions matter.** D's lower bound 19 concerns the lengths of the freely reduced relators including conjugating tails. F's lower bound 15 concerns cyclically reduced lengths, in a larger quotient-conjugacy graph. E's exact distance 10 counts a specified finite alphabet of fourteen instructions. These are different quantities.

## Reproduce

Python 3 and its standard library suffice for all Python checks:

```sh
python3 experiments/reproduce.py
```

To additionally compile and replay the independent C++ original-state cap-18 exhaustion:

```sh
python3 experiments/reproduce.py --cpp
```

The second command requires a C++17 compiler. Both commands report the target problem as unsolved. The driver checks the family certificates, plateau and gap checks, nilpotent lifting errors, complete cap-18 search, exact infinite-quotient distance, and small finite-quotient distances. Individual reports give standalone commands, exact assumptions, and the incomplete-run disclosures. The recorded cap-18 results are in [results/raw_peak_results.json](results/raw_peak_results.json).

The dependency-free [strict elementary verifier](experiments/elementary_verify.py) accepts only relator inversion, positive right multiplication, and single-generator conjugation, with an exact recorded endpoint. It performs no implicit generator changes, stabilization, quotient rewriting, or endpoint normalization. The quotient-lift certificate deliberately records its actual nontrivial free-word endpoint.

## Verification standard and remaining work

A positive ordinary-AC result must supply a complete proof or a replayable path to the standard free basis. An obstruction must be invariant under all permitted moves at unbounded length. Group triviality, quotient triviality, and finite search failures do not meet either standard. The computations here are independently checked programs, not proof-assistant formalizations.

The next unresolved steps are to find a complete free-group trivialization or a global obstruction. More narrowly, D's cap-19 component remains unclassified, and F identifies new cyclic length-15 states beyond the initial plateau. The quotient certificates expose concrete lifting errors but do not remove them by ordinary AC moves.

## Primary-literature cautions

- [Lisitsa's corrected published paper (2025)](https://doi.org/10.1016/j.jaca.2025.100041) reports that an earlier stable AK(3) claim depended on an incorrect theorem. That claim is not a solved starting point here.
- [Gilman and Myasnikov, Andrews–Curtis groups](https://gcc.episciences.org/15972/pdf) gives the problem's algebraic setting.
- [Carreras's 2026 certificate preprint](https://arxiv.org/abs/2607.23611) supplies prior n=3 equivalence context credited in C. Restricted graph bounds from outside sources are not silently transferred to ordinary AC paths.

Each report links the additional primary sources it used and separates external theorems from deductions and experiments produced in this investigation.
