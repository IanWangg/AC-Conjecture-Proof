# Research L: calibrating the search — the exact trivial hump, the barrier spectrum, and what more computation can and cannot buy for AK(3)

Date: 2026-11-02. Independent research agent L (round 3, computational strategy, constructive side).

**Status:** verified computational calibration results and 8 replayable certificates; **no AK(3) trivialization, no proof of non-triviality, no counterexample.** Everything below is labelled *proved here* (short lemmas), *experiment* (exact move set, caps and counts given), *externally reported*, or *open*. No novelty claim is made for any item; literature access in this session was limited to cached files of earlier agents (no arXiv).

**One-paragraph summary.** I computed the *complete* forward-reachable set of the trivial pair (x,y) in the full cyclic-product graph up to total length 20 ("the trivial hump" T(20): 22,205,081 Σ-states, 1,808,170 Aut(F₂)-orbits; "component" in D's terminology, but see item 6) and used it as an exact, unbiased reference set instead of the sampled AC-19/AC-1M datasets used by D. Results: (1) **no Aut(F₂)-orbit is shared** between the hump and AK(3)'s complete cap-28 component (6,347,128 orbits) — an exact meet-in-the-middle negative that strictly contains D's dataset test; (2) the **barrier spectrum** of all 18,116 unimodular Σ-classes of total length 13 is completely resolved in this graph: 18,084 are AC-trivial with barrier ≤ 18 (excess over their own length ≤ 5), 12 are in AK(3)'s class, 20 are nontrivial groups — so at length 13 there is nothing between "excess ≤ 5" and AK(3)'s "excess ≥ 16"; at length 14 the spectrum is also completely determined up to the hard classes, and it has a thin tail: 28 Σ-classes at excess 7–8 and 16 at excess 12 (trivializations through total length 26), then the six hard classes at ≥ 13 (≥ 15–17 externally) — so the data show a thin tail reaching close to the exhaustion frontier rather than a clean gap; (3) **saturation**: E's full 15-instruction elementary graph at cap 20 and D's cyclic-product graph at cap 20 contain *exactly the same* 917 complex classes of length ≤ 18, so D's negative bounds are not an artifact of the restricted move set; (4) a **feasibility model** with measured growth rates (hump ×7.5 and AK(3) ×6.7 per +2 in cap): a tenfold compute increase buys about +1.5 in cap; caps 30–32 from AK(3) (≈ 9–60 GB, hours) test excess 17–19, 5–7 units beyond the farthest known trivial example, and are the last cheap search experiment worth running — with C4/C6 (tiny forward sets) as far cheaper diagnostics of the same frontier; (5) **8 independent elementary certificates** trivializing Miller–Schupp benchmark presentations that are listed as unsolved in Shehper et al.'s data (they are among Fagan et al.'s solved rows, which carry no public elementary ledgers); (6) a **correction to D's Lemma D1(c)**: the cyclic-product graph is *directed* when the donor is fully cancelled (explicit counterexample, Lemma L2), so every "component" computed by `d_acsearch` is a forward-reachable set — D's certificates and negative bounds survive, but the wording in D and the semantics of my own "trivial hump" must be read accordingly.

## 1. Previous work read and choice of direction

I read `README.md` and `research/research-{a,b,c,d,e,f}.md` in full, skimmed every file in `experiments/` and `certificates/`, and re-ran `elementary_verify.py` on the certificates I reuse. Summary as I verified it: A proves the nonincreasing ACM plateau for AK(n), n ≥ 3 (a trivialization must reach total length ≥ 14); B gives nilpotent-quotient certificates and the finite-quotient distance reformulation; C proves MS(n, y⁻¹x²y⁻¹) ~AC AK(n) for all n ≥ 2 with certificates; D built the barrier-ordered cyclic-product engine `d_acsearch.cpp`, certified 82 equivalences, and showed that AK(3)'s cap-28 component (69,190,160 Σ-states, 6,347,128 Aut-orbits) contains no primitive relator and matches none of ≈1.29M published AC-trivial presentations even up to Aut(F₂); E proved ≥ 15 instructions and peak total length ≥ 21 for any AK(3) trivialization (exhaustive G_L components, L ≤ 20) and gave the residual-chain reformulation; F built thickenability tools, proved the AK/MS families are outside Lackenby's thickenable locus, and suggested a meridian-defect-guided search. D's key dumps (`k28_ak3.bin`, `aut_ak3.bin`) and E's class file `canon_L20_T18.txt` survived in the scratch area and were reused read-only (cross-validated below).

**Direction.** Agent G (round 3) runs the thickenability-guided constructive search F proposed, J audits, K works on obstructions, I on other families. My brief is computational strategy: *what could computation plausibly decide, and is the search space a matter of 10× more effort or hopeless at current scale?* Nobody had yet computed the **trivial side exactly**: D compared AK(3)'s component with *samples* of the trivial class (datasets produced by greedy/automorphism generators, biased toward easy presentations). I therefore (i) computed the exact trivial hump T(C) = forward-reachable set of (x,y) in G_full(C) for C ≤ 20; (ii) ran the exact Aut-orbit meet-in-the-middle against D's cap-28 dump; (iii) measured the *barrier spectrum* — for every unimodular pair of total length 13–15, the exact minimax barrier to (x,y) — which is the right calibration for "how far out is AK(3)"; (iv) tested whether the cyclic-product graph is saturated with respect to E's full elementary graph; (v) triaged the 1190-presentation Miller–Schupp benchmark against the exact components and certified what fell out; (vi) turned the measured growth rates into a feasibility table. This is new relative to A–F and disjoint from G/H/I/J/K as described to me.

## 2. Conventions (identical to D)

Words over x, X = x⁻¹, y, Y = y⁻¹. A **state** is an unordered pair of nonempty cyclically reduced words modulo Σ (rotation and inversion of either relator, swap); **energy** = total length; a **cyclic product** replaces u by cyc(rot(u)·rot(v)^{±1}); **G_full(C)** is the graph of all cyclic products on states of energy ≤ C; the **barrier** of a state (from a source) is the minimax energy over paths. Every element of Σ and every cyclic product is a composite of ordinary AC moves and the graph is undirected (D, Lemma D1), so **every state of T(C) is AC-trivial**, with an explicit certificate obtainable from the parent pointers (D's `d_certify.py`). A **complex class** adds the 8 signed permutations of {x,y} (automorphisms; AC-triviality is Aut(F₂)-invariant by D's Lemma D2). "Excess" of an AC-trivial pair of length ℓ and barrier b is b − ℓ.

**Lemma L2 (the cyclic-product graph is directed; D's Lemma D1(c) fails for fully cancelled donors; proved here by an explicit counterexample).** Let u = xyxYxyxYYYxyyxY (15 letters) and v = x. The cyclic product cyc(rot₁(u)·X) = xYxyxYYYxyyx, a 12-letter word (the donor is cancelled entirely and the cyclic reduction then removes a further letter pair of u against itself). From u' = xxYxyxYYYxyy (its Σ-form) and the same donor x, the cyclic products rot(u')·x^{±1} have cyclic lengths 7, 9, 11, 13 only (checked exhaustively over all rotations and signs), so **no single cyclic product returns from (x,u') to (x,u)**. D1(c)'s reversal formula assumes c₁ + c₂ < |V|, i.e. that the donor survives; when the donor is consumed and the remaining part of u cyclically reduces further, the step is one-way. Consequences: (i) what `d_acsearch` computes is the **forward-reachable set** Fwd(S, C) of the source, not a component; (ii) since every elementary move is invertible and the elementary realization of a cyclic product never exceeds the energy of its endpoints, Fwd(S, C) ⊆ Comp_{G_C}(S) (E's undirected elementary graph), so every state of Fwd((x,y), C) *is* AC-trivial with an elementary trivialization of peak ≤ C, and every negative statement of the form "no path from S₁ to S₂ within cap C" is unaffected (such a path would put S₂ in Fwd(S₁, C) ∩ Fwd(S₂, C), which D's collision test detects); (iii) "S ∉ Fwd((x,y), C)" does **not** imply that S has barrier > C. The example is real: (X, XYXyXYXyXYYXyyy) (energy 16, a primitive relator) is not in Fwd((x,y), 20), yet one cyclic product takes it to (x, xxYxyxYYYxyy) ∈ T(20) whose barrier is 15, so it has an elementary trivialization of peak 16. Every "component" below is therefore a forward set, and I write T(C) := Fwd((x,y), C). (This correction concerns D's wording, not D's certificates or negative bounds, and it affects my own §3.3 tables as stated there.) ∎

**Lemma L1 (exactness of staged forward barriers; proved here).** Let P ∉ T(20) and suppose a run of `d_acsearch` from P with `--target-keys T(20)` and cap C completes barrier level b−1 and reports its first hit into T(20) at barrier b ≤ C. Then the least barrier of a *forward* cyclic-product path from P into T(20) is exactly b, and P has an elementary trivialization of peak max(b, 20) (b if b ≥ 21). *Proof.* Minimality of b is Proposition D4 applied to the forward BFS from P with the target set T(20); the hit state S has a path from (x,y) of peak ≤ 20 in G_20, reversible elementarily, so P → S → (x,y) has peak ≤ max(b, 20). ∎ If the run completes level C with no hit, no forward cyclic path from P reaches T(20) within cap C. By Lemma L2 this bounds the forward cyclic barrier, not the elementary barrier, from below; the saturation results (§3.4, §3.7) are the evidence that the two agree in practice at these caps.

## 3. Results

### 3.1 The exact trivial hump T(C) (experiment)

`d_acsearch --source x,y --no-stop --cap C` (full graph, all cyclic products), caps 16, 18, 20; complete, no budget hit.

| cap C | states of T(C) | new at barrier C−1, C | Aut(F₂)-orbits | time |
|---:|---:|---|---:|---:|
| 16 | 396,497 | 129,832 / 213,012 | — | 3 s |
| 18 | 2,950,329 | 948,800 / 1,605,032 | — | 18 s |
| 20 | **22,205,081** | 7,061,348 / 12,193,404 | **1,808,170** | 169 s (+122 s orbits) |

New states per barrier (cap-20 run): 2:1, 3:4, 4:4, 5:8, 6:4, 7:68, 8:92, 9:368, 10:564, 11:2,504, 12:4,060, 13:17,684, 14:28,292, 15:129,832, 16:213,012, 17:948,800, 18:1,605,032, 19:7,061,348, 20:12,193,404. States of T(20) by energy 13/14/15/16: 18,084 / 31,408 / 131,256 / 229,508. Growth: ×7.44 (16→18), ×7.53 (18→20). For comparison D's AK(3) component grows ×6.7 per +2 (cap 26→28: ×6.74) and is **557 times smaller** than the hump at cap 20 (39,840 vs 22,205,081). 253 states of T(20) are automorphic images of (x,y) (Aut-minimal length 2).

### 3.2 Exact Aut(F₂)-orbit meet-in-the-middle (experiment; validity by D's Lemmas D2, D6, Cor. D7)

`d_acsearch --autmatch triv_k20.bin --autdump aut_triv20.bin` then `--autcompare aut_ak3.bin aut_triv20.bin`:

    autcompare distinct_orbits 6347128 1808170 common 0

**No state of AK(3)'s complete cap-28 forward set is an automorphic image of any presentation that is forward-reachable from (x,y) within cap 20** (every such presentation has an elementary trivialization of peak ≤ 20). A single common orbit would have proved AK(3) AC-trivial (Lemma D2) with an explicit certificate by transport (Lemma D6). This contains D's dataset test (AC-19/AC-1M) as a special case only in part: AC-1M reaches length 30 but is a biased sample; T(20) is complete for barrier ≤ 20. The two negatives are complementary. Why this is not implied by D's cap-28 run: a Σ-level common *state* would indeed put (x,y) in AK(3)'s cap-28 component (excluded by D), but automorphisms do not preserve barriers, so an *orbit* match between a cap-28 AK(3) state and a barrier-≤20 trivial state was open.

### 3.3 The barrier spectrum at total lengths 13, 14, 15 (experiment; group triviality by coset enumeration)

`l_spectrum.py` enumerates every Σ-class of pairs of cyclically reduced words with |a|+|b| = ℓ and unimodular exponent matrix (18,116 / 31,556 / 133,908 / 236,436 classes for ℓ = 13/14/15/16), and classifies each against T(20) = Fwd((x,y),20) (with the barrier of the (x,y)→P path, from `--dump 16`) and against D's complete cap-28 forward set of AK(3) (1,248 of its states have length ≤ 16). Leftovers are tested for group triviality with F's Todd–Coxeter (`f_descent.is_trivial_group`, 400,000 cosets) and, when that is inconclusive, with F's permutation-image search (`f_descent.nontrivial_hom`, A₅/A₆/A₇): every inconclusive pair (4 / 28 / 12 at ℓ = 14 / 15 / 16) turned out to have a nontrivial A₇ image, so no class is left undecided.

| ℓ | unimodular Σ-classes | in T(20), by excess 0/1/2/3/4/5/6 of the (x,y)→P barrier | in AK(3)'s cap-28 forward set | trivial group, not in T(20) (complex classes) | nontrivial group |
|---:|---:|---|---:|---:|---:|
| 13 | 18,116 | 17,328 / 76 / 632 / 16 / 16 / 16 / — (total 18,084) | 12 | **0** | 20 |
| 14 | 31,556 | 28,216 / 2,776 / 52 / 276 / 24 / 56 / 8 (total 31,408) | 40 | 94 (15 classes) | 14 |
| 15 | 133,908 | 126,368 / 888 / 2,884 / 504 / 452 / 160 / — (total 131,256) | 564 | 1,976 (260 classes) | 112 |
| 16 | 236,436 | 212,056 / 14,616 / 436 / 2,204 / 196 / — / — (total 229,508) | 632 | 6,072 (786 classes) | 224 |

**Consequences.**
- At length 13 the classification is complete: *every* balanced presentation of the trivial group of total length 13 is either in T(18) — hence AC-trivial with an elementary trivialization of peak ≤ 18 (excess ≤ 5) — or lies in AK(3)'s AC class (12 Σ-classes = the two Aut-orbits D found, up to Σ). This independently reproduces the Havas–Ramsay length-13 dichotomy (externally reported) *and* quantifies it: the hump's tail ends at excess 5, while AK(3) has excess ≥ 16 (D's cap-28 forward set contains no trivial state). Nothing lies in between.
- For ℓ ≥ 14 the "not in T(20)" column is, by Lemma L2, a mixture of (a) presentations with genuine barrier > 20 and (b) presentations with small barrier that are only *backward*-reachable (the primitive-relator example (X, XYXyXYXyXYYXyyy) at ℓ = 16 is of type (b)). The staged *forward* runs of §3.6 separate the two for ℓ = 14 and a sample of ℓ = 15 and give the exact forward barriers.
- The 12 (ℓ = 13) and 40 (ℓ = 14) AK(3)-class members agree with D's §4.1 (12 Σ-classes of length 13; 40 states of energy 14).

### 3.4 Saturation of the cyclic-product graph at cap 20 (experiment)

E's `e_peak` enumerates the full component of AK(3) in G_L (ordered freely reduced pairs, 15 instructions: inversions, swap, right multiplications, single-letter conjugations, total length ≤ L). Every cyclic product with energy ≤ C is realizable inside G_C (rotations are single-letter conjugations preserving length; the product is a right multiplication; cyclic reduction is by length-decreasing conjugations), so G_C ⊇ G_full(C) as sets of cyclic classes, while G_C also allows conjugation detours, left multiplication and non-cyclically-reduced intermediates. Comparing E's `canon_L20_T18.txt` (917 complex classes of cyclic length ≤ 18 in the 51,411,456-state G_20 component) with D's cap-20 component (39,840 Σ-states, dumped with `--dump 20`) via `l_classes.py compare`:

    A classes 917  B classes 917  common 917  onlyA 0  onlyB 0
    by length {13: 2, 14: 5, 15: 66, 16: 72, 17: 362, 18: 410}   (both)

**The extra freedom of the elementary graph produces no new cyclic class of length ≤ 18 at cap 20.** This is the first direct test that D's engine-relative negatives are not artifacts of the move restriction (at least at this cap). A full-cap-19 comparison (G_19 vs G_full(19)) is reported in §3.7.

### 3.5 Miller–Schupp benchmark triage and 8 certificates (experiment + certificates)

`l_ms_barriers.py triage` encodes each of the 1190 benchmark presentations (Shehper et al. `all_presentations.txt`) with a Python port of D's Σ-key (validated: all 39,840 states of the cap-20 dump are found in D's cap-28 key file, round trips and Σ-invariance hold) and looks it up in T(16), T(18), T(20), AK(3)'s cap-28 component and the two MS(2) holdout components (D's dumps):

| status in Shehper et al. | T(16) | T(18)∖T(16) | T(20)∖T(18) | AK(3) class | MS2a class | MS2b class | none of these |
|---|---:|---:|---:|---:|---:|---:|---:|
| greedy-solved (533) | 356 | 70 | 58 | 0 | 0 | 0 | 49 |
| unsolved (657) | 0 | **2** | **6** | 34 | 6 | 36 | 573 |

The 34/6/36 agree with D (§4.3–4.4). The 49 solved-but-outside have lengths 18:2, 19:4, 21:19, 22:6, 23:12, 24:4, 25:2 — 43 of them are simply longer than the cap. Their exact barriers (Lemma L1) are in §3.6. The 573 unsolved-outside have lengths 15:20, 16:6, 17:38, 18:22, 19:80, 20:34, 21:93, 22:42, 23:104, 24:38, 25:96; the 20 of length 15 therefore have barrier ≥ 21, i.e. excess ≥ 6.

**Eight presentations listed as unsolved by Shehper et al. lie in T(20)** (lines 599, 635 at barrier 18; 643, 647, 656, 673, 709, 753 at barrier 20). Paths from (x,y) were extracted (`--exact-targets`), reversed, and compiled by D's `d_certify.py` into strict `ordinary-ac-elementary-v1` certificates from the exact benchmark tuple to ("x","y"):

```
python3 experiments/elementary_verify.py certificates/l_ms*_trivialization.json
{"endpoint": ["x", "y"], "moves": 200, "path": "certificates/l_ms0599_trivialization.json", "peak_total_length": 26}
{"endpoint": ["x", "y"], "moves": 207, "path": "certificates/l_ms0635_trivialization.json", "peak_total_length": 26}
{"endpoint": ["x", "y"], "moves": 160, "path": "certificates/l_ms0643_trivialization.json", "peak_total_length": 29}
{"endpoint": ["x", "y"], "moves": 157, "path": "certificates/l_ms0647_trivialization.json", "peak_total_length": 27}
{"endpoint": ["x", "y"], "moves": 421, "path": "certificates/l_ms0656_trivialization.json", "peak_total_length": 27}
{"endpoint": ["x", "y"], "moves": 471, "path": "certificates/l_ms0673_trivialization.json", "peak_total_length": 27}
{"endpoint": ["x", "y"], "moves": 198, "path": "certificates/l_ms0709_trivialization.json", "peak_total_length": 29}
{"endpoint": ["x", "y"], "moves": 161, "path": "certificates/l_ms0753_trivialization.json", "peak_total_length": 29}
```
(The elementary peak exceeds the cyclic barrier because the compiler's swap identity and rotations pass through longer unreduced intermediates; the cyclic-product barrier is 18 resp. 20.) **Novelty check:** all eight occur in rows 533–557 of Fagan et al.'s `AC19_extended.txt`, i.e. in its block of solved Miller–Schupp presentations (none is in AC-19 proper except 599 and 635; none is in AC-1M). So they were already reported solved by the Two-Hump campaign; Carr notes that campaign published no elementary ledgers for most of its MS solutions. These eight files are therefore **independent public certificates, not new solutions.** They cost 195 s of search.

### 3.6 Exact forward barriers of the intermediate presentations (experiment; Lemma L1)

Each presentation P below was run as a single source (`--no-stop --target-keys triv_k20.bin`) with the stated cap; "barrier b" is the least barrier of a forward cyclic-product path from P into T(20) (Lemma L1), hence P has an elementary trivialization of peak ≤ max(b,20).

**(a) The 49 greedy-solved Miller–Schupp presentations outside T(20)** (cap 24, budget 12·10⁶ states per run; every reported hit was found below the budget):

| length | 18 | 19 | 21 | 22 | 23 | 24 | 25 |
|---|---|---|---|---|---|---|---|
| count | 2 | 4 | 19 | 6 | 12 | 4 | 2 |
| forward barrier (excess) | 23, 23 (5, 5) | 21, 21, 23, 23 (2, 2, 4, 4) | 18 × 21 (0), 1 × 23 (2) | 6 × 22 (0) | 12 × 23 (0) | 4 × 24 (0) | 2 × 25 (0; cap-26 runs) |

So **every greedy-solved benchmark presentation has excess ≤ 5**; 43 of the 49 are outside T(20) only because they are longer than 20, and 42 of those have excess 0 (they never need to grow at all). Together with the 8 "unsolved" presentations found inside T(20) (lengths 17–19, barriers 18–20, excess 1–3: lines 599, 635 → excess 1; 643, 647 → 3; 656, 673 → 2; 709, 753 → 1), this says that the difficulty of these presentations for greedy/RL search is about path *length* and plateaus, not about barrier *height* — consistent with Carr's observation (cached `RESULTS.md`) that Two-Hump's 167/178-move certificates have peak relator length 11.

**(b) The 15 complex classes of trivial groups of length 14 outside T(20)** (one Σ-representative each, cap 26, budget 2·10⁷ states; "complete" = the whole forward set at cap 26 was enumerated; plus the 4 classes that coset enumeration left undecided and which turned out to be nontrivial groups, as controls):

| class (Σ-classes) | representative | forward barrier into T(20) | excess | forward set at cap 26 | identification (§3.6d) |
|---|---|---|---|---:|---|
| c1 (4), c4 (8), c6 (8) | XXXXYXY XYYYXyy; XXXYYxY XXyxYYY; XXXYYxy XYXyXYY | **21** (level 20 complete) | 7 | budget | nahomar: AC-trivial at cap 22 |
| c11 (8) | XXYXyxy XXyyxYY | **22** (level 21 complete) | 8 | budget | nahomar: AC-trivial at cap 22 |
| c5 (8), c10 (8) | XXXYYxY XYXyxYY; XXYXYxy XXyyxYY | **26** (level 25 complete) | **12** | budget | nahomar: "shown AC-trivial only at cap 26" |
| c2 (8), c12 (8), c14 (4), c15 (2) | e.g. XXYxY XYYYYYXyy = C3 | none ≤ 26 | ≥ 13 | 6,674,326 (complete, identical for all four) | C3 |
| c3 (4) | XXXXYxY XYYYXyy = C4 | none ≤ 26 | ≥ 13 | 38,438 (complete) | C4 |
| c9 (4) | XXYXXyy XYYXyxy = C6 | none ≤ 26 | ≥ 13 | 37,648 (complete) | C6 |
| c8 (4) | XXXYxxy XYYYxyy = P1 | none ≤ 26 | ≥ 13 | 864,908 (complete; = D's #1 at cap 26) | P1 |
| c7 (8), c13 (8) | XXXYxxY XYYYxyy = P2 | none ≤ 26 | ≥ 13 | 2,615,296 (complete; = D's #2 at cap 26) | P2 |
| u2–u5 (controls, nontrivial groups) | XXyxy XYXyyyyyy, … | none ≤ 26 | — | 169,212 (complete, identical) | nontrivial (A₇ image) |

Bookkeeping: 31,408 (T(20)) + 20 + 8 + 16 (excess 7, 8, 12) + 50 (five named hard classes) + 40 (AK(3)'s class, excess ≥ 15 since D's cap-28 forward set has no trivial state) + 14 (nontrivial) = 31,556 = all unimodular Σ-classes of length 14. **The length-14 spectrum is therefore completely determined up to the hard classes:** excess 0–6 for 31,408 classes, 7–8 for 28, 12 for 16, and ≥ 13 (≥ 15 for AK(3)'s members; ≥ 15/17 by the external cap-28/30 exhaustions) for the 90 Σ-classes in the six hard classes. The forward-set sizes of P1 and P2 at cap 26 coincide exactly with D's independent three-source run (§4.2 of research-d), a useful cross-validation of both engines' use.

**(c) A stride sample (every 7th of the 280 representatives, 40 classes: 38 trivial groups + 2 nontrivial controls) of the 260 trivial-group classes of length 15 outside T(20)** (caps 22 then 24, budgets 2.5·10⁶ / 5·10⁶ states):

| forward barrier into T(20) | excess | classes | external label (§3.6d) |
|---|---|---:|---|
| 21 (level 20 complete) | 6 | 6 | resolved by nahomar at cap ≤ 28 |
| 22 | 7 | 2 | idem |
| 23 | 8 | 3 | idem |
| none ≤ 24, forward set complete and tiny (2,072 and 1,997 states) | 10–13 | 2 (L15c99 = XXYXyxy XXXXyyxY, L15c204 = XXYxYxy XXyxyyyy) | nahomar: flag 0 at cap 22, resolved by forward BFS at cap ≤ 28 ("48 components, 122 classes") |
| none ≤ 24 | ≥ 10 | 3 + 1 | named hard classes C3 (3), C6 (1) |
| none ≤ 24 | ≥ 10 (≥ 14 externally) | 21 | nahomar R-classes (unresolved at their cap 28) |
| none ≤ 24 (controls) | — | 2 | nontrivial groups (A₇ images) |

So the length-15 tail looks like the length-14 one: a handful of classes at excess 6–8, a couple at excess 10–13 whose forward sets are *tiny* (they reach T(20) through a narrow neck of long intermediates), and then a large unresolved population. The 21 sampled R-classes extrapolate to ≈ 113 of the 260 classes (as the full labelling in (d) confirms).

**(d) Cross-check against the published (unreviewed) length-≤16 classification.** The repository `nahomar/andrews-curtis-solver` (cached by F) lists 838 "residual" complex classes of lengths 13–16 — trivial-group presentations outside *its* cap-22 component of (x,y) — each labelled by the cap-28 component it falls into: the named classes AK3 (161 residual classes), P1 (11), P2 (37), C3 (62), C4 (5), C6 (6), and about 230 further labels R8…R334 for components that reach neither (x,y) nor a named class at cap 28 (externally reported, unreviewed; different engine). Matching by complex class:

| my leftovers (trivial groups outside T(20)) | absent from their residual list (= in their cap-22 component, or resolved by their forward BFS at cap ≤ 28) | labelled C3 / C4 / C6 / P1 / P2 | labelled R… (unresolved there) |
|---|---:|---|---:|
| length 14: 15 classes | 6 (L14c1, c4, c6, c11: flag 1 at cap 22; c5, c10: flag 0, resolved at cap 26) | 4 / 1 / 1 / 1 / 2 (c2, c12, c14, c15 / c3 / c9 / c8 / c7, c13) | 0 |
| length 15: 260 classes | 100 | 31 / 0 / 2 / 2 / 12 | 113 |

(The 4 + 20 nontrivial-group controls are, correctly, absent from their list of trivial groups. Their `classes17_c22.txt` flags c5 and c10 as *not* in the cap-22 component, and their README states that "two other length-14 residuals from the cap-24 stage were shown AC-trivial only at cap 26, via intermediate presentations of length 22–26" — exactly my c5, c10 with forward barrier 26. Likewise L15c99 and L15c204 have flag 0 and are absent from the residual list, i.e. they belong to the 122 classes their `resolve` step certified by forward BFS at cap ≤ 28, consistent with my "none ≤ 24".) Two consequences. (i) My measured forward barriers agree with their data in every case where both exist: the four "cap-22" classes have forward barrier 21–22, the two "cap-26" classes have 26, the named classes have none ≤ 26. Their cap-28 count for AK(3)'s component, 8,650,489 D8-classes, also matches D's 69,190,160 Σ-states (ratio 8.0). (ii) **The tail of the trivial population is thin but long, and the hard population is large.** At length 14, 2 of 31,542 trivial complex-class representatives (16 of 31,542 Σ-classes) have excess 12, only one unit below the cap-26 exhaustion of the five named hard classes; the external cap-28/30 exhaustions put those at excess ≥ 15–17. At length 15 there are 100 classes at excess 6–7 and then 160 classes (47 in the named hard classes, 113 in nahomar's unresolved R-classes) with nothing known below excess ≥ 10 (my sampled cap-24 runs, §3.6c) resp. ≥ 13 (their cap 28). So the "second hump" is not a handful of famous examples: already at lengths 15–16 it contains hundreds of complex classes (about 230 forward-components in the external data), none of which has ever been trivialized; but the first hump's tail does reach excess 12 at length 14, so the data do **not** exhibit a clean gap between the two populations — only a thin tail followed by a frontier beyond which nothing has been resolved.

### 3.7 Full-cap saturation at cap 19 (experiment)

`e_peak --L 19 --canon 19` (E's engine; G_19 component of AK(3): 23,609,984 ordered states, complete, 814 MB) collects the complex classes of *all* its states, and `d_acsearch --cap 19 --no-stop --dump 19` dumps D's complete cap-19 component (20,024 Σ-states):

    A classes 2530  B classes 2530  common 2530  onlyA 0  onlyB 0
    by length {13: 2, 14: 5, 15: 62, 16: 63, 17: 319, 18: 368, 19: 1711}   (both)

So at cap 19 the full elementary graph and the cyclic-product graph have **identical** sets of complex classes (2,530), not just at short lengths. Together with §3.4 this is a strong indication that, at these caps, the cyclic-product graph is *saturated*: conjugation detours, left multiplications and non-cyclically-reduced intermediates (all available in G_L) never reach a cyclic class that cyclic products with the same energy cap do not reach. D's "no trivialization below total length 29" therefore holds for the full elementary move set under the same cap, at least as far as caps 19–20 can test the mechanism. (Formally: for every C ≤ 20 tested, the Σ×D8 quotient of E's G_C component equals that of D's G_full(C) component.)

## 4. Feasibility assessment with numbers

**Measured growth.** AK(3)'s G_full component (D): 1, 26, 40, 1,000, 2,128, 20,024, 39,840, 143,988, 257,488, 886,932, 1,580,780, 5,531,256, 10,269,488, 37,161,104, 69,190,160 for caps 13, 15, …, 28: ×6.7 per +2 (×3.5 at odd, ×1.9 at even caps). The trivial hump: ×7.5 per +2. Aut-orbit compression ≈ ×11 (AK(3)) and ×12 (hump). D's engine processes ≈ 1.2·10⁵ states/s/core at ≈ 20 bytes/state (keys, parent, barrier, hash slot, bucket).

**Projection (Σ-level, AK(3) side).**

| cap | states (×6.7 per +2) | memory | single-core time |
|---:|---:|---:|---:|
| 28 (done, D) | 6.9·10⁷ | 1.5–2.5 GB | 10 min |
| 30 | ≈ 4.6·10⁸ | ≈ 9 GB | ≈ 1 h |
| 32 | ≈ 3.1·10⁹ | ≈ 60 GB | ≈ 7 h |
| 34 | ≈ 2.1·10¹⁰ | ≈ 0.4 TB | ≈ 2 days |
| 36 | ≈ 1.4·10¹¹ | ≈ 2.8 TB | ≈ 2 weeks |

Orbit-level search divides memory by ≈ 11 (cap 34 ≈ 40 GB) but multiplies per-node cost by the number of minimal representatives times the Whitehead canonicalization (≈ 7 µs), so it buys about +2 in cap for the same memory and roughly nothing in time. **A tenfold increase in compute buys ≈ +1.5 in cap.** On this machine (≤ 2.3 GB for one agent) cap 28 is the ceiling at Σ level and cap 30 at orbit level; a workstation with 64 GB reaches cap 32 (Σ) or 34 (orbits); cap 36+ needs disk-based or distributed frontier storage.

**What the calibration says.** (i) The trivial population has a thin, long tail. At length 13 every AC-trivial presentation has excess ≤ 5 (complete classification). At length 14, 31,408 of 31,542 trivial Σ-classes have excess ≤ 6, 28 have excess 7–8, and **16 (two complex classes) have excess 12**: their only known trivializations pass through total length 26, one unit below the cap at which the five named hard classes are still unresolved by my runs. At length 15 the sampled tail (§3.6c) behaves the same way, with two sampled classes at excess 10–13 whose forward sets are tiny (≈ 2,000 states at cap 24): such presentations reach the hump through a narrow neck of long intermediates, exactly the shape that a cap-limited search is worst at finding. (ii) The hard population is large: besides AK(3) (excess ≥ 16, D), P1, P2, C3, C4, C6 (≥ 13 here; ≥ 15/17 by the external cap-28/30 exhaustions), the external classification lists ≈ 230 further unresolved forward-components at lengths 15–16. Nothing in that population has ever been resolved by raising the cap beyond 26; the two excess-12 classes are the farthest resolved cases known at length 14. (iii) The hump is 557× larger than AK(3)'s forward set at cap 20 and grows faster; AK(3)'s forward set is not visibly "bending" toward it: its Aut-minimal lengths stay ≥ 13 (D) and it has no automorphic contact with the forward-reachable trivial class at cap 20 (§3.2). (iv) The benchmark presentations solved by greedy/RL methods all have excess ≤ 5 (§3.6a), and the eight "unsolved" ones found in T(20) have excess 1–3 — their difficulty for those methods is path *length*, not barrier *height*; so the RL literature's "hard" cases are not evidence about large excess at all.

**Conclusion.** The honest reading is neither "AK(3) is obviously just beyond the frontier" nor "the search space is hopeless": the data show a thin tail of genuinely trivial presentations reaching excess 12 at length 14, and a frontier at excess ≈ 13–17 beyond which *no* presentation of any kind has been resolved, with hundreds of unresolved classes sitting there. For AK(3), caps 30–32 test excess 17–19, i.e. 5–7 units beyond the farthest known trivial example at comparable length; cap 30 costs about 7× D's cap-28 run (≈ 9 GB, ≈ 1 h) and cap 32 about 45× (≈ 60 GB, hours) — affordable on one large machine, and this is the single remaining cheap experiment on the search side that could change the picture (a hit would settle AK(3); a miss would place it ≥ 7 units beyond the tail). Cap 34 and beyond (≥ 0.4 TB, days) is out of reach without distributed frontier storage, and nothing in the growth data (×6.7 per +2) suggests that the tail becomes dense out there; Bridson's results (externally reported) show that excess is unbounded in general, so no finite cap is decisive in the negative direction. The cheapest *diagnostic* of the frontier is not AK(3) at all but **C4** (and C6), whose forward sets are tiny at cap 26 (38,438 and 37,648 states; externally 623,460 and 5,307,099 D8-classes at cap 30): C4 can be pushed to cap ≈ 34 at the cost of AK(3) at cap 30, and resolving it either way (a trivialization with excess ≈ 20, or persistence) would calibrate what to expect for AK(3). The two length-15 classes with forward barrier 25–28 and forward sets of ≈ 2,000 states (§3.6c) show that "tiny forward set + late contact" is a real pattern among AC-trivial presentations, which is exactly what C4 and C6 look like so far.

## 5. Honest limits

- All negatives are engine-relative (G_full and G_C with their caps) and are **not evidence of non-triviality**. The saturation tests (§3.4, §3.7) cover caps 19–20 only; elementary paths with much longer intermediates are not excluded by anything here.
- By Lemma L2 the engine's sets are forward-reachable sets. T(20) is complete as the set of states reachable *from* (x,y) within cap 20, and all its members are AC-trivial with peak ≤ 20; but an AC-trivial presentation with elementary barrier ≤ 20 can be missing from it (one such example is exhibited). The Aut-orbit comparison (§3.2) is therefore one-sided twice over: a hit would prove AK(3) AC-trivial; a miss proves only that AK(3)'s cap-28 forward set is disjoint, up to Aut(F₂), from the forward-reachable part of the trivial class at cap 20. The §3.3 "not in T(20)" columns for ℓ ≥ 14 are mixtures (see there), disentangled only where §3.6 measured forward barriers.
- Group-triviality decisions use coset enumeration (400,000 cosets) plus permutation images in A₅–A₇; both are decisive here, but the first is only a semi-decision procedure in general.
- The growth projection is an extrapolation of a ×6.7 geometric trend over 8 data points; it could bend either way.
- Correctness of the Aut-orbit canonical form rests on D's implementation (Whitehead peak reduction; 2,925 + 258 invariance checks by D) which I reused unchanged; my Python key port was validated against 39,840 engine states.
- The 8 certificates are independent artifacts for presentations already reported solved elsewhere.
- I could not access arXiv; the literature statements are taken from A–F's notes and the cached Carr/Shehper/Fagan repositories.

## 6. Advice to the coordinator (ranked)

1. **One last, well-defined search experiment, then stop cap-raising.** Run D's engine (or an orbit-level variant) from AK(3) to cap 30, and if a ≥ 64 GB machine is available to cap 32, with primitive-relator, dataset and thickenability detection. This tests excess 17–19, which is 5–7 units beyond the farthest trivial example known at comparable length (excess 12, §3.6b), costs 7×–45× D's cap-28 run, and is the only search-side experiment left whose outcome would be informative either way. Do not plan beyond cap 32–34 on the AK(3) side: ×6.7 per +2 and ≥ 0.4 TB at cap 34.
2. **Push C4 (and C6) first — they are the cheap diagnostic of the frontier.** Their forward sets are 38,438 and 37,648 states at cap 26 (vs. 10.3·10⁶ for AK(3)); externally they are still unresolved at cap 30 with 623,460 (C4) and 5,307,099 (C6) D8-classes. C4 can be pushed to cap 34 at roughly the cost of AK(3) at cap 30; C6 grows faster but stays an order of magnitude below AK(3). A trivialization of C4 or C6 at excess ≈ 20 would be the first resolved case beyond the frontier and would make an AK(3) run to cap 32–34 well motivated; persistence to cap 36 would be the strongest evidence yet that the frontier is real.
3. **Raise the trivial side and repeat the exact orbit meet-in-the-middle.** T(22) ≈ 1.7·10⁸ states (≈ 4 GB, 25 min), T(24) ≈ 1.3·10⁹ (disk-backed). Aut-canonicalize and intersect with D's 6.3·10⁶ AK(3) orbits (§3.2 scaled up) *and* with the forward sets of P1, P2, C3, C4, C6 and the unresolved R-classes: any common orbit settles a class with a certificate by transport, and the test is complete rather than sampled. Because of Lemma L2 also run it in the other direction where affordable: backward reachability from (x,y) is not what the engine computes, and the two can differ.
4. **Publish the barrier spectrum (lengths 13–16) as the reference calibration**, including the forward-set sizes and the thin-tail classes c5, c10 (excess 12) — they are the right objects for any "hardness" discussion, and the honest replacement for the anecdotal "two humps". Complete length 15–16 with staged forward runs (tool chain ready; ≈ 4 h of single-core time for all 1,046 classes at caps 22–26).
5. **Use the 8 certificates as a public-ledger contribution**, clearly labelled as independent elementary certificates for presentations reported solved by Fagan et al. (rows 533–557 of AC-19-extended). The same pipeline (T(20) + `--exact-targets` + `d_certify.py`) certifies, in minutes, every benchmark presentation of barrier ≤ 20; at T(22) it would reach the remaining greedy-solved ones of §3.6a.
6. **For agent J (audit):** D's Lemma D1(c) must be weakened to "cyclic products whose donor is not fully cancelled are reversible by a cyclic product"; replace "component" by "forward-reachable set" throughout D (§2, Prop. D4, §4) and in F's §4.6 component sieve if it uses the same move. D's certificates, dataset tests and ≥ 29 bounds are unaffected (Lemma L2(ii)); the sentence "the graph is undirected" is false. E's G_L components are genuinely undirected and unaffected. The same caveat applies to the external nahomar classification and to this note's T(C).
7. **Theory, not search, must settle AK(3).** The only computational findings that could change the picture are (a) a thickenable or primitive-relator state (G's search), (b) an orbit contact at higher trivial-side cap (item 2), or (c) a proof that AK(3)'s class has an Aut-invariant property (e.g. F's meridian defect ≥ 6, or a growth lower bound on E's residual-chain distances) — the last is K/H territory, and the exact components computed here (hump states with their barriers, AK(3)'s cap-28 class) are the natural test beds for any candidate invariant: a candidate must be constant on T(20) ∪ Aut-images and differ on AK(3)'s 69M states.

## 7. Reproduction (executed in this session; paths relative to the repository root, scratch dir S)

```sh
g++ -O2 -std=c++17 -o S/d_acsearch experiments/d_acsearch.cpp
g++ -O2 -std=c++17 -o S/e_peak experiments/e_peak.cpp
python3 experiments/l_classes.py --selftest          # 3000 random Sigma x D8 invariance checks
python3 experiments/l_spectrum.py --selftest         # enumeration vs brute force (n<=5), key decoding
# trivial hump
for c in 16 18 20; do S/d_acsearch --source x,y --no-stop --cap $c --maxstates 40000000 --dumpkeys 0 triv_k$c.bin > triv_c$c.txt; done
S/d_acsearch --source x,y --no-stop --cap 20 --maxstates 30000000 --dump 16 triv_dump16.txt > triv_c20b.txt
# exact Aut-orbit meet in the middle (aut_ak3.bin = D's dump of AK(3)'s cap-28 component)
S/d_acsearch --autmatch triv_k20.bin --autdump aut_triv20.bin
S/d_acsearch --autcompare aut_ak3.bin aut_triv20.bin        # distinct_orbits 6347128 1808170 common 0
# barrier spectrum (k28_ak3.bin = D's cap-28 key dump)
for l in 13 14 15; do python3 experiments/l_spectrum.py classify $l triv_dump16.txt k28_ak3.bin --hump-cap 20; done
# saturation at cap 20
S/d_acsearch --cap 20 --maxstates 5000000 --no-stop --dump 20 ak3_c20_dump.txt
python3 experiments/l_classes.py compare canon_L20_T18.txt ak3_c20_dump.txt --maxlen 18 --col2   # 917 = 917, 0 differences
# Miller-Schupp triage and certificates (third-party data: Shehper et al. AC-Solver, Fagan et al. ACSolverX)
python3 experiments/l_ms_barriers.py --selftest ak3_c20_dump.txt k28_ak3.bin
python3 experiments/l_ms_barriers.py triage all_presentations.txt solved_miller_schupp_presentations.txt triv_k16.bin triv_k18.bin triv_k20.bin k28_ak3.bin k28_ms2a.bin k28_ms2b.bin
S/d_acsearch --source x,y --no-stop --cap 20 --maxstates 30000000 --exact-targets ms8.tgt --maxhits 20 > ms8_paths.txt
# reverse each PATH, then: python3 experiments/d_certify.py PATH.rev W1 W2 x y certificates/l_msNNNN_trivialization.json
python3 experiments/elementary_verify.py certificates/l_ms*_trivialization.json
# full-cap-19 saturation
S/e_peak --L 19 --cap 60000000 --canon 19 2> epeak_L19_canon.txt      # 23,609,984 states, 2,530 classes
S/d_acsearch --cap 19 --maxstates 1000000 --no-stop --dump 19 ak3_c19_dump.txt
python3 experiments/l_classes.py compare epeak_L19_canon.txt ak3_c19_dump.txt --maxlen 19 --col2    # 2530 = 2530
# exact forward barriers of intermediate classes (Lemma L1): per source, read "TKEYHIT min_barrier" and "last_complete_barrier"
S/d_acsearch --source W1,W2 --no-stop --cap 26 --maxstates 20000000 --target-keys triv_k20.bin   # length-14 classes
S/d_acsearch --source W1,W2 --no-stop --cap 24 --maxstates 12000000 --target-keys triv_k20.bin   # the 49 greedy-solved MS presentations
# Lemma L2 counterexample (pure Python): products of (xyxYxyxYYYxyyxY, x) and of (xxYxyxYYYxyy, x), see research-l.md §2
```

## 8. Files written

- `research/research-l.md` (this note).
- `experiments/l_classes.py` — Σ×D8 complex-class canonical forms, file comparison (`--selftest`).
- `experiments/l_spectrum.py` — enumeration of unimodular Σ-classes by total length; classification against hump dump and D's key dump; coset-enumeration triviality (`--selftest`).
- `experiments/l_ms_barriers.py` — Python port of D's Σ-key, key-set membership, Miller–Schupp triage (`--selftest DUMP KEYS`).
- `certificates/l_ms{0599,0635,0643,0647,0656,0673,0709,0753}_trivialization.json` — strict elementary trivializations (exact benchmark tuple → (x,y)).

## References

- Round-1/2 notes A–F of this repository and their references; D's engine `experiments/d_acsearch.cpp`, E's `experiments/e_peak.cpp`, F's `experiments/f_descent.py` (coset enumeration), all used read-only.
- A. Shehper et al., *What makes math problems hard for reinforcement learning: a case study*, arXiv:2408.15332; data `ac_solver/search/miller_schupp/data/all_presentations.txt`, `barcode_analysis/5_steps_neibourhoods/{solved,unsolved}_miller_schupp_presentations.txt` (cached clone).
- L. Fagan et al., *The Two-Hump Problem*, arXiv:2606.21611; data `AC19.txt`, `AC19_extended.txt`, `AC1M.txt.gz` (cached clone, commit 6a12515).
- J. Carr, arXiv:2607.23611 and `joe-carr-data/ac-certificates` (`RESULTS.md`, cached): bottleneck-Dijkstra results and the remark that Two-Hump solutions carry no elementary ledgers.
- G. Havas, C. Ramsay, *Breadth-first search and the Andrews–Curtis conjecture*, IJAC 13 (2003) (length-13 dichotomy; externally reported).
- M. Bridson, arXiv:1504.04187 (unbounded excess in general; externally reported).
- M. Lackenby, arXiv:2606.06122 (thickenable ⇒ AC-trivial; externally reported, via F).
