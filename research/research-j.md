# Research J: critical audit of notes A–F, a sharpened plateau-exit theorem, and strategy

Date: 2026-11-02. Independent research agent J (round 3, Fable cohort; brief: critical audit + strategy).

**Status:** audit complete; one small theorem proved (J1); strategic assessment given. **No AK(3) trivialization, no proof of non-triviality, no counterexample, and no proof or disproof of the AC conjecture is claimed.** Every statement is labelled *proved here*, *experiment* (exact bounds), *externally reported*, or *open*.

## 1. Previous work read and choice of direction

Read in full: `README.md`, `research/research-{a,b,c,d,e,f}.md`, `experiments/elementary_verify.py`, `verify_plateau.py`, `d_acsearch.cpp`, `d_prepare_targets.py`, the header/move table of `e_peak.cpp`; skimmed the remaining experiments and all certificates. The in-progress round-3 notes G, H, I, K were skimmed read-only to avoid duplication (G: exact ACM moves with frozen torus-type relators; H: no-go theorems for quotient obstructions; I: torus-knot pairs sharing a Farey vertex; K: theory). Direction, as briefed: a skeptical proof-check of A–F with selected re-runs, one proved sharpening that fell out of the audit (Theorem J1, §4), two quantitative audit experiments (§5), and a ranked strategic assessment (§7).

## 2. Re-runs (experiment; all passed in this session; one core, < 1 GB, each < 15 min)

| what | command | result |
|---|---|---|
| all 90 strict certificates present at the start of my session (82 D, 2 E, 4 F, 1 C, 1 I) | `python3 experiments/elementary_verify.py <all certificates/*.json except ms3_to_ak3.json, e_ak3_quotient_paths.json>` | exit 0; 6 end at `(x,y)` (AK(1), AK(2), four F descents), the rest are equivalences |
| C packaged certificate | `ms_ak_family.py --verify certificates/ms3_to_ak3.json` | peak 23, passes |
| A equality checks | `verify_plateau.py` | 28 = 4(2n+1) candidates at n = 3; 12 braid candidates for n = 3, 4; formula for n ≤ 100 |
| B quotient paths | `quotient_certificates.py` | class-2/3 paths and S3/S4/A5 distances 2/3/4 reproduced |
| D engine regression | `d_acsearch --cap 20 --no-stop` | new states per barrier 1/25/14/960/1128/17896/19816, total 39,840 (= D §4.1); energy-13 states 12, energy-14 states 40 |
| D cap 24 | `d_acsearch --cap 24 --dumpkeys` | 1,580,780 states (= D), no primitive relator |
| D self-tests | `d_acsearch --self-test`, `d_whitehead.py --self-test`, `d_certify.py --self-test` | pass |
| E peak components | `e_peak --L 13..16` | 336 / 336 / 13,728 / 20,560, none contains (x,y) (= E §5.3); AK(2) at L = 13 reaches (x,y) at depth 19 |
| E free distance (small budget) | `e_acdist --mode free --max-states 1500000` | layers 1,15,159,1534,14269,130372 and 1,11,87,631,4774,37940,312637 (= E §5.1) |
| E/F self-tests | `e_acdist`, `e_peak`, `e_thicken`, `e_thicken_check.py`, `e_nilpotent_tables.py --selftest/--check-quotient-certs`, `f_thicken.py`, `f_knotlike.py`, `f_descent.py` | all pass |

## 3. Audit findings

Severity: **S1** = a claim labelled "proved" is false as stated; **S2** = conclusion correct, wording too strong or a hidden assumption; **S3** = labelling/presentation.

### 3.1 [S1] research-d, Lemma D1(c): the cyclic-product graph is *not* undirected

**Claim audited.** `research-d.md` §3, Lemma D1(c): "every edge can be reversed by a cyclic product", hence (§2 and the header of `d_acsearch.cpp`) the graph is "undirected" and the settled set is "the connected component".

**What is wrong.** The reversal formula X·U[|U|−c₁,|U|)·U[0,c₂) assumes that the cancellation at the junction and at the wrap consumes at most the donor V (c₁ + c₂ ≤ |V|). When the donor is consumed entirely and the cyclic reduction then continues *inside U*, the result is a proper cyclic subword of U with extra cancellation and no single cyclic product recovers U.

**Minimal counterexample (checked; `python3 experiments/j_cyclic_graph.py`).** (u, v) = (yxYYX, xy) is cyclically reduced, unimodular (exponent rows (0,−1), (1,1)) and presents the trivial group (y = x⁻¹ gives yxYYX = x). The product with U = yxYYX, V = xy cancels X·x and Y·y at the junction (all of V), leaving yxY, whose cyclic reduction is x. So (yxYYX, xy) → (x, xy) is an edge of G_full. The complete set of cyclic-product neighbours of the Σ-class of (x, xy) is {(X,XXY), (X,Y), (XY,XXY), (Y,XY)} (canonical spellings, all of total length ≤ 4); the class of (yxYYX, xy) (total length 7) is not among them. D's engine does generate such edges: in `d_acsearch.cpp` the branch `c1 == min(nu,nv)` applies full `reduce_cyc` to the concatenation, which is exactly this case (the other branch, with the "represented by a shifted alignment" skip, is correct: a wrap cancellation is the same cyclic word as the alignment shifted by one letter with one more junction cancellation).

**Consequences.** (i) "Component" in research-d means the *forward-reachable* set from the source(s). Proposition D4 stays valid for directed graphs (its proof uses only paths from the source). (ii) The negative statements "no primitive relator / no dataset match / no (x,y) in AK(3)'s component at cap C" are statements about *directed* cyclic-product paths from AK(3). Every edge is an AC composite, so every reached state is AC-equivalent to AK(3); the positive uses (certificates, Corollaries D5/D7) are unaffected. (iii) The holdout statements "AK(3), #1, #2 pairwise disconnected in G_full(27)/G_full(28)" and "every GS path joining any two of them reaches total length ≥ 29" are proved for directed paths in either direction (a directed path from source A to source B inside the cap contains an edge from an A-labelled to a B-labelled state, which the engine records as a collision). A configuration A ← S → B with S reached from neither source is *not* excluded by the runs, although it is an AC equivalence through cyclic lengths ≤ cap (the reverse of a cyclic product is an ACM move whose elementary expansion keeps cyclic lengths within the two endpoint states). The sentence "improves Carr's bound" inherits this caveat; I could not check Carr's graph semantics (arXiv blocked). (iv) In practice the asymmetry does not occur low in AK(3)'s class: in the forward sets at cap 17 (1,000 Σ-classes) and cap 19 (20,024 classes; both counts reproduce D's table with my independent Python implementation) all 3,380 resp. 78,944 internal directed edges have their reverse present (experiment, `j_cyclic_graph.py --cap 17|19`, 18 s and 11 min). **Fix:** state D1(c) as "every edge is an AC composite, so every state reached is AC-equivalent to the source", delete "undirected", and read "component" as "forward-reachable set" throughout D and in the README.

### 3.2 [checked, no error] research-a, Lemmas 1–2 and the plateau theorem

Correct as stated. I re-derived the normal-form facts, the orientation argument of Lemma 1 and the decoding of the equality case; the finite checks reproduce. Remarks (S3): Lemma 1 only uses the quotient C₂ * C₃ = B/Z(B), so its hypothesis "conjugate in B" can be weakened to "conjugate in PSL(2,ℤ)"; the equality classification is a necessary condition that happens to be complete for n ≥ 3. The bound 14 is not sharp in A's own ACM graph: Theorem J1 (§4) proves ≥ 15 for AK(3) and 2n+9 for AK(n), n ≥ 3.

### 3.3 [checked] research-b

The class-2 identity r_n s⁻ⁿ = y⁻¹c^{−A} was re-derived by hand in the normal form (a,b,k)(d,e,l) = (a+d, b+e, k+l−bd): s = (1,−1,−1), s⁻¹ = (−1,1,2), s⁻ⁿ = (−n, n, 2n + n(n−1)/2), product (0, −1, −n(n−1)/2). The distance principle (§4) is correct and its essential hypothesis (finite instruction alphabet) is stated. S3: BLM's Theorem 1.1 is quoted with hypothesis k ≥ max(w(G),2); I could not open the paper, so this stays externally reported (as B labels it).

### 3.4 [checked] research-c

Symbolic table and tail induction re-read; the n = 3 exact certificate replays (32 moves, peak 23). No issue.

### 3.5 [checked, with S2 remarks] research-d, remaining lemmas and the dataset test

Lemma D1(a)–(b), D2, D3, D6 and Corollaries D5, D7 are correct (D1(a)'s nine-move interchange identity re-checked step by step; D6's composition argument is sound because each generator certificate ends exactly at the cyclically reduced image and conjugation to the exact image is an AC move). S2: "component" should read "forward-reachable set" (§3.1). S2: the headline "none of ≈1.29 million published AC-trivial presentations" overstates coverage: after Whitehead reduction the 1,432,816 dataset presentations (AC-19, AC-19-extended without the 634 MS rows, AC-1M; SHA-256 of the two text files as in D §5) fall into only **77,430 distinct Aut(F₂)-orbits** (experiment, §5.2). My initial guess that most of them reduce to length ≤ 12 was wrong: only 15,940 presentations (1.1 %) do; 1,408,364 have Aut-minimal length 13–19 and 8,512 have 20–31. So the dataset test is not subsumed by the "minimum Aut-length 13" test, but it samples a small set of orbits (for comparison, F §4.3 counts 121,370 AC-trivial Σ×D₈-classes at length 17 alone). Reproduced here at cap 24: 0 matches (`--autmatch`).

### 3.6 [checked] research-e

Lemma 2 (Magnus syllable detection over ℤ and mod p) re-proved; the mod-p step (1+Z)^{p^k u} ≡ (1+Z^{p^k})^u is valid for negative u as a power series. Theorem 1 and Theorem 3 (stabilization class 2^{D−1}(ℓ+2) − 1 from ℓ_r ≤ 2^r(ℓ+2) − 2) are correct. Proposition 5 and its corollaries are correct; I re-checked that xY normally generates T = ⟨x,y | x³ = y⁴⟩ and x normally generates B₃. §5.3's peak bound is correctly scoped to instruction paths (equivalently `ordinary-ac-elementary-v1` certificates) and is **not** a bound for elementary paths with word conjugators; E says so. §6's convention check with ⟨x | x³⟩ is right (I verified by hand: reversed strand orders at x⁺/x⁻ give 3 faces, equal orders give 1).

### 3.7 [checked, with S2 remarks] research-f, and the weight carried by Lackenby's unstable statement

Lemma 1.1 (∂N = S² via χ and Lefschetz duality) is correct. Lemma 1.2 is the standard one-vertex Neuwirth/Osborne–Stevens criterion; the proof is a sketch, but the orientation convention is pinned down by E's ⟨x | x³⟩ check and F's 298 automorphic-basis controls. Lemma 3.1, F2, F3 are correct modulo the classical theorems F lists (Perelman; Alexander's torus theorem; "knot group ℤ ⇒ solid torus"; Burde–Zieschang; Moser/Gordon–Luecke; Aut(C_p * C_q) for p ≠ q is generated by inner and factor automorphisms, the partial conjugations being inner because the factors are abelian). I re-derived F3.1's automorphism φ: x ↦ xy⁻¹, y ↦ y²x⁻¹ (φ(xyxYXY) = xxYYY as a free word) and the syllable count 4n+2.

**Lackenby (S2).** arxiv.org, export.arxiv.org and maths.ox.ac.uk are blocked in this session; I could only confirm through a search engine's summary of arXiv:2606.06122 that (a) "thickenable" means the presentation 2-complex embeds in some 3-manifold, (b) the stable statement was already known via Perelman, and (c) the paper also presents a proof of the unstable statement. Independently of that paper, in rank 2 the unstable statement has a short proof from classical results (this is F's §2 sketch, which I re-checked): if K(P) ⊂ M³ for a balanced trivial-group presentation P, a regular neighbourhood N is a homotopy 3-ball, hence B³ (Perelman), so S³ = N ∪ B³ is a genus-2 Heegaard splitting (H = 0- and 1-handles, H′ = 2-handles ∪ B³) in which the relator curves form a complete meridian system β of H′ and the dual disks of the 1-handles a complete system α of H. By Waldhausen (1968) the splitting is standard; any two complete meridian systems of a handlebody are related by disk slides and isotopy; a slide of β_i over β_j changes r_i to the free/cyclic reduction of r_i·g r_j^{±1} g⁻¹ (an AC composite), and isotopies across α change words by free reduction only. Sliding β to the standard system β₀ of H′ with α fixed therefore takes P by AC moves to the words read by β₀ against α, a basis of F₂ up to conjugacy, and any basis is carried to (x,y) by Nielsen moves, which are AC moves. So "thickenable ⇒ unstable AC-trivial" is classical modulo Perelman (for every rank, since Waldhausen's theorem holds in every genus), and E's and F's uses of it do not rest on an unverified new theorem. I have not read Lackenby's proof and make no claim about its content or its bounds.

### 3.8 [S3] README and labelling

"All 89 strict ordinary-AC certificates pass" is out of date (round-3 agents are adding certificates). "Component" should be "forward-reachable set" in the D summary. No instance was found in A–F of a bounded search presented as a proof, of group triviality presented as AC-triviality, or of a stable/generalized result presented as ordinary AC. A trivial observation: Carr's two MS(3) theorems, MS(3, y⁻¹x²y⁻¹) and MS(3, yx²y), are images of each other under y ↦ y⁻¹ up to Σ (they share an Aut-orbit, §5.2), so one is a corollary of the other by Lemma D2.

## 4. Theorem J1: the first exit from A's plateau has total cyclic length ≥ 2n+9 (proved here)

Notation as in research-a: X = x⁻¹, Y = y⁻¹, p_n = xⁿY^{n+1}, q_n = yⁿX^{n+1}, b = xyxYXY, AK(n) = (p_n, b). Moves are A's quotient-conjugacy (ACM) replacements (u,v) → (u′,v), with the image of u′ conjugate to the image of u^{±1} in F/⟨⟨v⟩⟩, plus relator permutation; lengths are cyclic. Every ordinary AC move is such a replacement, so an ordinary AC path's sequence of cyclically reduced states is an ACM path.

**Lemma J0 (conjugacy in torus-knot groups; proved here, classical).** Let G = ⟨a,b | a^m = b^n⟩ with m, n ≥ 2 coprime, Z = ⟨a^m⟩ its centre, π: G → G/Z = C_m * C_n, and ab: G → ℤ the abelianization (a ↦ n, b ↦ m, so a^m ↦ mn). Then w, w′ ∈ G are conjugate iff π(w), π(w′) are conjugate in C_m * C_n and ab(w) = ab(w′).
*Proof.* (⇒) clear. (⇐) If ḡπ(w)ḡ⁻¹ = π(w′), then g w g⁻¹ = w′ z^k with z = a^m and k ∈ ℤ; abelianizing, ab(w) = ab(w′) + k·mn, so k = 0. ∎
It applies to B = ⟨x,y | xyx = yxy⟩ = ⟨s,t | s² = t³⟩ (x = t⁻¹s, y = s⁻¹t², abelianization x, y ↦ 1), to G_n = ⟨x,y | xⁿ = y^{n+1}⟩ (x ↦ n+1, y ↦ n) and to G_n′ = ⟨x,y | yⁿ = x^{n+1}⟩ (x ↦ n, y ↦ n+1). (Agent I's checkpoint records the criterion for B₃ independently.)

**Lemma J1a (no power partner of length 2n+2).** No cyclically reduced word u of length 2n+2 is conjugate to p_n^{±1} in B.
*Proof.* Use A's map to C₂ * C₃ = ⟨S⟩ * ⟨T⟩: x ↦ T²S, Y ↦ TS (orientation TS), X ↦ ST, y ↦ ST² (orientation ST). A cyclically reduced word of length L gives 2L syllables before reduction, L of them equal to S. The reduced cyclic word in C₂ * C₃ alternates between S and a nontrivial power of T, so its cyclic syllable length is exactly twice the number of surviving S-syllables, and S-syllables are never created. If all letters have the same orientation the syllable word is already alternating and cyclically reduced: length 2L. Otherwise there is a boundary TS|ST around the cycle, where S·S cancels, so at least two S's are lost: length ≤ 2L − 4. The image of p_n has cyclic syllable length 4n+2 (A, Lemma 1). For L = 2n+2 the possible values are 4n+4 or ≤ 4n, so no conjugate of p_n^{±1} in C₂ * C₃, a fortiori in B, has length 2n+2. ∎

**Lemma J1b (no braid partner of length 7).** For n ≥ 3, no cyclically reduced word of length 7 is conjugate to b^{±1} in G_n or in G_n′.
*Proof.* In G_n/Z = C_n * C_{n+1} the image of b is the alternating necklace (x, y, x, y⁻¹, x⁻¹, y⁻¹) of syllable length 6. Each maximal block of equal-generator letters of a free word gives at most one syllable, so a length-7 word with six syllables has six blocks, one of size 2 and five of size 1, and conjugacy in the quotient forces the block exponents to be ≡ (1,1,1,−1,−1,−1) up to rotation, or the inverse pattern, modulo n for x-blocks and modulo n+1 for y-blocks. A double block has exponent ±2, and ±2 ≡ ∓1 modulo m happens only for m = 3. For n ≥ 4 there is therefore no candidate at all. For n = 3 the double block is an x-block with exponent ±2 ≡ ∓1 (mod 3): the word is b (or b⁻¹) with one letter x^{∓1} replaced by x^{±2}, which changes e_x by ±3 while e_y = −1 (resp. +1) is unchanged, so ab(w) = 4e_x + 3e_y ∈ {13, −11, 11, −13}, whereas ab(b^{±1}) = ±1; by Lemma J0 no such w is conjugate to b^{±1} in G₃. For G_n′ exchange the roles of x and y (for n = 3: double y-block, ab = 3e_x + 4e_y ∈ {11, −13, 13, −11} ≠ ±1). ∎

**Theorem J1 (proved here).** Let n ≥ 3. Every ACM path from AK(n) to (x,y) — in particular every ordinary AC trivialization with arbitrary conjugators, measured by cyclic length — contains a state of total cyclic length ≥ 2n+9, and the first state off A's plateau has total cyclic length ≥ 2n+9. For AK(3): ≥ 15 (A: ≥ 14).
*Proof.* By A's theorem the path stays on (Orb(p_n) ∪ Orb(q_n)) × Orb(b) (either order) until the first length-increasing move, which lands at total length ≥ 2n+8. A landing at exactly 2n+8 would be either (u′, b′) with b′ ∈ Orb(b), |u′| = 2n+2 and u′ conjugate in F/⟨⟨b′⟩⟩ = B to p_n^{±1} or q_n^{±1} (q_n = Δp_nΔ⁻¹ with Δ = xyx, so again to p_n^{±1}) — excluded by Lemma J1a — or (p′, b′) with p′ ∈ Orb(p_n) ∪ Orb(q_n), |b′| = 7 and b′ conjugate to b^{±1} in F/⟨⟨p′⟩⟩ ∈ {G_n, G_n′} — excluded by Lemma J1b. ∎

**Finite check (experiment, `python3 experiments/j_first_increase.py`, 7 s).** For n = 3 and n = 4, all cyclically reduced words of lengths 2n+1…2n+3 (power side) and 6…8 (braid side, both frozen relators) were enumerated. n = 3: length 7 gives exactly the 28 words of Orb(p₃) ∪ Orb(q₃); length 8 gives **0** quotient-conjugate candidates; length 9 gives 756 quotient candidates of which 432 have the right abelianization (by Lemma J0 these are exactly the length-9 words conjugate to p₃^{±1} in B: the first off-plateau power relators, total length 15). Braid side, n = 3: length 6 gives exactly Orb(b); length 7 gives 42 quotient-conjugate candidates (e.g. xxyxyXY) and **0** with the right abelianization, for both G₃ and G₃′; length 8 gives 96 candidates, 32 exact. n = 4: length 10 gives 0 power candidates; length 7 gives 0 braid candidates already in the quotient; length 8 gives 48 quotient candidates and 0 exact. The abelianization refinement is essential for n = 3: A's quotient-only test leaves 42 length-7 candidates.

**What J1 does and does not say.** It is a proved, search-independent lower bound on the peak cyclic length of any AC trivialization of AK(n), n ≥ 3 (2n+9 instead of A's 2n+8). For n = 3 it is consistent with D's observation "no state of barrier 14" in the cyclic-product subgraph and with E's instruction-path peak ≥ 21 (incomparable: free length, letter conjugators only). It is **not** evidence about whether AK(3) is AC-trivial. Extending it to 2n+10 by the same method needs the ACM neighbours of all states at 2n+9, whose frozen relators are no longer torus-type words, so Lemma J0 no longer applies directly; agent G's exact torus-type ACM graph is the natural continuation.

## 5. Further experiments (exact commands; outputs from this session)

### 5.1 Directed edges in AK(3)'s cyclic-product forward set (`experiments/j_cyclic_graph.py`)
```
python3 experiments/j_cyclic_graph.py --cap 17   # 1000 classes, 3380 directed edges, 0 irreversible (18 s)
python3 experiments/j_cyclic_graph.py --cap 19   # 20024 classes, 78944 directed edges, 0 irreversible (11 min)
```
Both class counts equal D's full-graph counts (1,000 at barrier ≤ 17; 20,024 at ≤ 19), an independent regression of D's engine. The script also prints the §3.1 counterexample.

### 5.2 Aut(F₂)-orbits in AK(3)'s cap-24 forward set, and the dataset's orbit count (D's engine)
```
S=<scratch>; printf 'AK3 xxxYYYY xyxYXY\nP1 XyyxYYY YxxyXXX\nP2 XyyxYYY XyxxyXX\nC3 xxyXy xyyyyyxYY\nC4 xxxxyXy xyyyxYY\nC6 xxyxxYY xyXYYXy\nMS3a YYYYXyyyx YXYxx\nMS3b YYYYXyyyx YXXYx\nQ xxyXYY xxxYYXy\n' > $S/named14.tgt
./d_acsearch --cap 24 --maxstates 2500000 --no-stop --dumpkeys 0 $S/k24.bin     # 1,580,780 states, 13 s
./d_acsearch --autmatch $S/k24.bin $S/named14.tgt                                # 18 s
```
Result: min Aut-length 13; Aut-minimal-length histogram 13: 208, 14: 776, 15: 3,608, 16: 3,020 states. Exactly 2 orbits of length 13 (AK(3)'s and Q's, as D found at cap 28) and **5 orbits of length 14**: one is the MS(3, y⁻¹x²y⁻¹) = MS(3, yx²y) orbit (both named rows canonicalize to the same key, i.e. they are Aut-related — by y ↦ y⁻¹); the other four, canonical representatives (xxxyXYY, xyyXYxY), (xxyxYXY, xyXyXYY), (xxyXyXY, xyxyXYY), (xxyXyXY, xyXYYXy), are further length-14 members of AK(3)'s class and match **none** of P1, P2, C3, C4, C6. So no new length-14 equivalence appears at cap 24 (negative datum, experiment). Then, with a scratch copy of the engine that additionally histograms the targets (not committed; three added lines, no change to matching), against D's converted datasets (`d_prepare_targets.py`, hashes equal to D's):
```
./d_acsearch_jhist --autmatch $S/k24.bin $S/targets/AC19.tgt $S/targets/AC19Xtail.tgt $S/targets/AC1M.tgt   # 57 s
TARGET_AUT_HIST total 1432816 distinct_orbits 77430
target_aut_min_length: 2:178 6:764 7:205 8:295 9:803 10:3171 11:5059 12:5465 13:20135 14:34787 15:90297
  16:97967 17:250967 18:343789 19:570422 20:2579 21:4005 22:834 23:661 24:154 25:195 26..31: 84
autmatch states 1580780 closure_fail 0 targets 1432816 target_fail 1 hits 0 min_aut_length 13
```

## 6. Honest limits

- The audit is a human-style proof-check plus re-runs of the cheap parts; the large runs (D cap 27/28, E L = 19/20, E class-5 distances) were not repeated (memory budget), only their small-cap regressions.
- Theorem J1 is a plateau-exit bound only; it says nothing after the first excursion and nothing about AC-triviality. Its finite part is exhaustive for n = 3, 4; the proofs are uniform for n ≥ 3.
- Lemma J0 is classical; the observation that it makes ACM moves with frozen torus-type relators exactly decidable is also in agents G's and I's checkpoints, found independently.
- Literature access: arXiv, journal and university hosts are blocked here; Lackenby's abstract was confirmed only through a search-engine summary; the classical 3-manifold input (Waldhausen, slide-connectivity of disk systems) is quoted from memory. Novelty is not claimed for anything in this note.
- The reversibility count (§5.1) covers only caps 17 and 19; irreversible edges may exist higher up, which does not affect the directed reading of D's results.

## 7. Advice to the coordinator (ranked, opinionated)

1. **Correct the record before the next round (cheap, do it).** In research-d and the README replace "undirected graph / connected component" by "directed cyclic-product graph / forward-reachable set", restate the holdout bounds as directed-path bounds, and replace "≈1.29 M presentations" by "1.43 M presentations in 77,430 Aut(F₂)-orbits". Update the certificate count. None of this changes any positive result.
2. **Realistic targets.** None of the four user targets is attackable this year with the tools in this repository, and the project should say so plainly. The only target where incremental, verifiable progress is even definable is "AK(3) is AC-trivial" (a certificate). "AK(3) is not AC-trivial" has exactly one formally correct route left (E's Corollary 4: unbounded distances in the 2-groups P_c^{(2)}) and no known technique; every local/quotient/TQFT invariant is dead (B, E, H, Bobtcheva–Quinn), and the computed chain distances do not separate AK(3) from the trivial AK(2). Proving or disproving the full conjecture is out of scope.
3. **The single most promising constructive program:** exact ACM moves at torus-type states (G, I), combined with D's Aut-orbit compression and certificate transport. Lemma J0 makes every ACM move with a frozen relator that is a torus word in some basis *exactly decidable with arbitrary conjugators*; this is the first move set in the project that is strictly larger than bounded-conjugator products, and AK(n), C3, C4, C6 all live in that world (F §3). Require `ordinary-ac-elementary-v1` certificates for every claimed connection. Also certify the four length-14 orbits of §5.2 as explicit class members (cheap) and run the same orbit test against the residual lists at lengths 15–16.
4. **Dead ends — stop spending compute on them:** raising caps in the cyclic-product or 15-instruction graphs without new move types (×2–3.5 states per unit of cap, memory-bound, and the trivial side is hopelessly large); finite, solvable or low-class nilpotent quotient invariants; chain distances at feasible classes (no collapse, E §5.2); thickenability sieves of low-length class members (base rate ~1 %, and F2/F3 exclude the hard families structurally); meet-in-the-middle against AC-19/AC-1M (77k orbits).
5. **Thickenability: keep as a filter, not a program.** Its logical content ("thickenable ⇒ AC-trivial") is classical modulo Perelman (§3.7), so it is safe to use; but every thickenable class found so far descends strictly (F §4.4), i.e. the locus is the easy part of the trivial class. F's meridian-defect idea deserves exactly one targeted experiment (best-first search by defect from C3/C4, where defect-4 states exist); if the defect never drops below 4 there, drop it.
6. **A clearly separate, labelled target worth one agent:** *stable* AC-triviality of AK(3) (rank-3 engine), which the literature left open after Lisitsa's correction. Any result must be labelled stable and never conflated with the user's ordinary targets.
7. **Infrastructure:** ask the user to allow arxiv.org/export.arxiv.org in the session network; several labels "externally reported" (Lackenby, BLM's exact hypothesis, Carr's graph semantics) could then be upgraded or corrected.

## 8. Files written

- `research/research-j.md` (this note).
- `experiments/j_first_increase.py` — exhaustive finite part of Theorem J1 for n = 3, 4 (`python3 experiments/j_first_increase.py`).
- `experiments/j_cyclic_graph.py` — independent cyclic-product implementation, the D1(c) counterexample and the reversibility census (`python3 experiments/j_cyclic_graph.py --cap 17`).
- No certificates (no new AC equivalence is claimed).

## References

- Research notes A–F of this repository and their references (Akbulut–Kirby; Panteleev–Ushakov arXiv:1609.00325; Borovik–Lubotzky–Myasnikov arXiv:1103.1295; Guyot arXiv:1612.06912; Carr(eras) arXiv:2607.23611; Fagan et al. arXiv:2606.21611 and `github.com/Math-AI-Caltech/ACSolverX`, data files with SHA-256 f72df134… and d028cd4d… as in research-d).
- M. Lackenby, *The stable Andrews–Curtis conjecture and thickenable presentations of the trivial group*, arXiv:2606.06122 (2026); abstract-level only, via search-engine summary (arXiv blocked in this session).
- F. Waldhausen, *Heegaard-Zerlegungen der 3-Sphäre*, Topology 7 (1968); G. Perelman (2002–03); classical slide-connectivity of complete meridian systems in handlebodies (e.g. Johannson, *Topology and Combinatorics of 3-Manifolds*); cited from memory.
- J. Nielsen (1924) on Aut(F₂); J. H. C. Whitehead (1936) on minimal cyclic words; Burde–Zieschang, *Knots*, for torus-knot groups and their centres; cited from memory.
