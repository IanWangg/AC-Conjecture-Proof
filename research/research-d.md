# Research D: AK(3)'s bounded AC component, certified class members, and a meet-in-the-middle test against published AC-trivial datasets

Date: 2026-11-02. Independent research agent D (round 2).

**Status:** partial, fully verified results. **No AC trivialization of AK(3), no proof of non-triviality, no counterexample.**

*Proved here* (82 replayable ordinary-AC certificates, all accepted by `experiments/elementary_verify.py`, plus short lemmas): 34 Miller–Schupp benchmark presentations, and a second length-13 presentation Q = (x²yx⁻¹y⁻², x³y⁻²x⁻¹y) lying in a different Aut(F₂)-orbit, are ordinary-AC-equivalent to AK(3); every automorphism of F₂ is AC-realized on AK(3), with explicit certificates for generators (Panteleev–Ushakov's theorem, made explicit for n = 3).

*Experiments* (exact and engine-relative; the engine reproduces every published count of Carr's GS searches): AK(3)'s component in the full cyclic-product graph up to total length 28 (69,190,160 states) contains no primitive relator. None of its states matches the ≈1.29 million presentations reported AC-trivial in the AC-19/AC-1M datasets, up to Σ and **all** of Aut(F₂) (Whitehead canonical forms; 6,347,128 orbits checked), and no state is an automorphic image of a presentation of length ≤ 12. The two uncertified MS(2) holdouts are separated from AK(3) and from each other by bottleneck ≥ 29, improving the published GS bound ≥ 27. These negative results are search bounds, **not** obstructions. Novelty of the equivalences themselves is not established (§6).

## 1. Previous work read and choice of direction

I read `README.md`, `research/research-a.md`, `research-b.md`, `research-c.md`, all of `experiments/` and `certificates/`, and re-ran the repository checks: `python3 experiments/elementary_verify.py --selftest` (passes) and `python3 experiments/elementary_verify.py certificates/ms3_to_ak3_exact.json` (32 moves, peak 23, endpoint `(xyxYXY, xxxYYYY)`), confirming C's bridge. A's plateau theorem is consistent with my data below: in the cyclic-product graph the barrier-13 layer of AK(3) is a single state and no state has barrier 14 (§4.1); A's theorem concerns a larger (quotient-conjugacy) move graph, so this is a consistency check, not a re-proof. B's quotient results imply that no single finite/solvable quotient can help, which is one reason I chose a free-group, certificate-producing direction.

**Literature check (network-limited).** arxiv.org, ar5iv, projecteuclid and stevens.edu were blocked by this session's network policy; I used web-search summaries, the public GitHub artifact of Carr (`joe-carr-data/ac-certificates`, manuscript v3.1 and `RESULTS.md`, read in full where relevant) and a clone of the public ACSolverX repository (Fagan et al.). Facts used below, all **externally reported**:

- Length ≤ 12 presentations are AC-trivial (Miasnikov–Myasnikov); at length 13 every presentation is AC-trivial or AC-equivalent to AK(3) (Havas–Ramsay; also discussed by Panteleev–Ushakov) — as summarized in Carr §1.
- Bowman–McCaul (2006) exhaustively enumerated AK(3)'s constrained search space for maximum individual relator length 10,…,17 without finding a trivialization (as cited by Lisitsa, arXiv:2501.18601).
- Panteleev–Ushakov (arXiv:1609.00325; GCC 2019) enumerated, with ACM moves and modulo Aut(F₂), presentations AC-equivalent to AK(3) with relators of length up to 20 (previous record 17), and proved that every automorphism of F₂ is AC-realized on AK(n).
- J. Carr (arXiv:2607.23611, manuscript v3.1; the project brief calls the author "Carreras", but the manuscript byline is Joe Carr, so I write Carr below): in the canonical substitution ("GS") graph, 1,532,732 states of AK(3)'s component lie below total length 25; d_GS(MS(3,yx²y),AK(3)) = 19; the two uncertified MS(2) claims of Shehper et al. need GS bottleneck ≥ 27 (cap-27 run exhausted 13,504,944 states; cap 28 inconclusive at a 40M budget).
- Fagan et al., "The Two-Hump Problem" (arXiv:2606.21611, ICML 2026) released AC-19 (140,535 presentations of length ≤ 19) and AC-1M (1,136,154 presentations) as AC-trivial datasets; Carr audited that AK(3) itself is absent from AC-19.
- Shehper et al. (arXiv:2408.15332) stated four MS → AK(3) equivalences without published ledgers; their stable-AK(3) claim was later undercut, and Lisitsa's corrected journal version (doi:10.1016/j.jaca.2025.100041) leaves stable AK(3) unresolved (repository README; I could not open the journal page). I found no 2026 report of an AK(3) trivialization; AK(3) appears open.

**Choice of direction (constructive).** Existing exhaustive searches bound either individual relator length (Bowman–McCaul 17; Panteleev–Ushakov 20 with very strong ACM moves) or total length in the GS graph (Carr ≤ 26/27). Repeating such a search with modest hardware cannot move those frontiers much. Instead I combined three things that, as far as I could check, had not been combined:

1. **Meet in the middle against the trivial side's published data.** AC-triviality is invariant under Aut(F₂) (Lemma D2). Hence if *any* state of AK(3)'s bounded component is, up to Σ and an automorphism, one of the ≈1.29M presentations reported AC-trivial, then AK(3) is AC-trivial — even if the connecting trivialization runs far above the search cap. AC-1M contains presentations up to total length 30, produced by an automorphism-based generator.
2. **Primitive-relator detection** (Lemma D3) as an extended target: any state with a primitive relator is AC-trivial, again regardless of cap.
3. **Certified class extraction:** every benchmark presentation that falls into AK(3)'s component yields an exact, replayable ordinary-AC certificate, reducing the set of independent open classes.

Agent E (obstructions) and F (other families) work in parallel; this note is about AK(3)'s own component and stays on the constructive side.

## 2. Precise graph, conventions and engine

Words use x, X=x⁻¹, y, Y=y⁻¹. A **state** is an unordered pair of nonempty cyclically reduced words modulo the group Σ generated by cyclic rotation of either relator, inversion of either relator, and interchange of relators. No automorphism of F₂ is used to identify states. **Energy** = total length. A **cyclic product** replaces u by the cyclic reduction of rot_k(u)·rot_l(v)^{±1}, v the other relator, for any rotations k, l and either sign.

- **G_full(C):** all cyclic products, states of energy ≤ C.
- **G_GS(C):** only cyclic products in which at least one letter cancels (the substitution graph of Fagan et al. and Carr).

The **barrier** of a state is the least, over paths from the source, of the maximum energy on the path. `experiments/d_acsearch.cpp` (C++17, no dependencies) settles states in nondecreasing barrier order with a bucket queue, stores 64-bit packed canonical keys (canonical rotation via the two-pointer minimum-expression algorithm, both orientations), and keeps a parent pointer per state. It reports per-barrier counts, cross-source collisions, primitive relators, and target hits. A separate mode reduces dumped states to Whitehead-canonical Aut(F₂)-orbit keys (Lemma D6 / Corollary D7) for orbit-level comparisons.

## 3. Lemmas (proved here)

**Lemma D1 (moves are ordinary AC composites; the graph is undirected).** (a) Rotating a cyclically reduced relator by one letter is a single-letter conjugation g r g⁻¹ with g the inverse of its first letter; the result is again cyclically reduced, so no length change occurs. Inversion is AC1. Interchange (a,b)→(b,a) is the composite (a,b)→(ab,b)→(ab,b⁻¹)→(ab,b⁻¹ab)→(ab,a)→(ab,a⁻¹)→(aba⁻¹,a⁻¹)→(b,a⁻¹)→(b,a), using right multiplication, inversion and conjugation by the words b and a⁻¹. (b) A cyclic product is: rotate u, optionally invert v, rotate v, multiply, then remove a cancelling first/last letter pair by conjugating with the inverse of the first letter until cyclically reduced. (c) If u' = cyc(UV) with U, V rotations of u, v^{±1}, and c₁ letters cancel at the junction and c₂ at the wrap, then cyc(UV) = X·Y with X = U[c₂, |U|−c₁), Y = V[c₁, |V|−c₂); multiplying the rotation XY by the rotation Y⁻¹·V[0,c₁)⁻¹·V[|V|−c₂,|V|)⁻¹ of V⁻¹ gives X·U[|U|−c₁,|U|)·U[0,c₂), a rotation of U. So every edge can be reversed by a cyclic product. ∎

`experiments/d_certify.py` implements exactly (a)–(b), re-discovering each step independently of the C++ engine (its own canonical forms), and emits the strict `ordinary-ac-elementary-v1` format.

**Lemma D2 (AC-triviality is Aut(F₂)-invariant).** Let φ ∈ Aut(F₂). Applying φ letterwise to an AC sequence R=R₀→…→R_m gives an AC sequence φ(R₀)→…→φ(R_m): inversion and right multiplication commute with φ, and conjugation by a letter g becomes conjugation by the word φ(g), a composite of single-letter conjugations. If R_m=(x,y) then φ(R) ~ (φ(x),φ(y)), a basis of F₂. By Nielsen's theorem a basis is carried to (x,y) by elementary Nielsen transformations (inversion, right multiplication by the other element or its inverse, interchange), all AC composites. Hence φ(R) is AC-trivial whenever R is, and conversely with φ⁻¹. ∎ (The construction is explicit, so a certificate could be produced from any concrete hit.)

**Lemma D3 (a primitive relator forces AC-triviality).** Let (r₁,r₂) present the trivial group with r₁ primitive, φ(r₁)=x for some φ ∈ Aut(F₂). Then F/⟨⟨x,φ(r₂)⟩⟩=1 forces φ(r₂) ≡ y^{±1} modulo ⟨⟨x⟩⟩. Deleting each x-letter of φ(r₂)=u x^ε v is right multiplication by v⁻¹x^{−ε}v, i.e. conjugate the first relator by v⁻¹, optionally invert, multiply, undo. So (x,φ(r₂)) ~ (x,y^{±1}) ~ (x,y), and Lemma D2 gives the claim. ∎ Primitivity of a cyclic word is decided by Whitehead reduction: in rank two, up to inner automorphisms and length-preserving permutations, the Whitehead automorphisms are x↦xy^{±1}, y↦yx^{±1}; a non-minimal cyclic word is shortened by one of them, and a word is primitive iff it reduces to length 1. As a speed filter the engine first applies the classical necessary condition (externally reported, e.g. Cohen–Metzler–Zimmermann 1981) that a cyclically reduced primitive word of length ≥ 2 uses each generator with one sign only; `--self-test` checks that the filtered and unfiltered tests agree on all 797,184 cyclically reduced words of length ≤ 12 (1,500 primitive).

**Proposition D4 (search semantics).** If states are inserted with barrier max(b, energy) when discovered from a settled state of barrier b, and buckets are processed in increasing b, the first discovery of a state has its minimal barrier, and after bucket c is complete the set of states of barrier ≤ c is exactly the component of the source in G(c). Proof: barriers of processed states are nondecreasing, so later discoveries have barrier ≥ the first; conversely every state of G(c)'s component is reached along a path of barrier ≤ c, by induction on the path. ∎ With several sources, a cross-source edge found while processing barrier b certifies a connection of barrier max(b, barrier of the other endpoint); absence of such edges after completing bucket c proves the components of G(c) are disjoint.

**Corollary D5.** If some state S of AK(3)'s component is φ(T) up to Σ, with φ one of the 8 signed permutations of {x,y} and T AC-trivial, then AK(3) is AC-trivial (Lemmas D1, D2). If S has a primitive relator, AK(3) is AC-trivial (Lemma D3).

**Lemma D6 (every automorphism is AC-realized on AK(3); proved here with certificates, re-deriving Panteleev–Ushakov's theorem for n=3).** For every φ ∈ Aut(F₂), AK(3) is ordinary-AC-equivalent to φ(AK(3)) (relators taken up to conjugation, itself an AC operation). *Proof.* The seven certificates `certificates/d_ak3_aut_{swap,invx,invy,x_xy,x_xY,y_yx,y_yX}.json` (verifier-checked, §4.5) take AK(3) exactly to the cyclic reductions of φ(AK(3)) for φ = x↔y, x↦x⁻¹, y↦y⁻¹, x↦xy, x↦xy⁻¹, y↦yx, y↦yx⁻¹. By Nielsen, swap, x↦x⁻¹ and x↦xy generate Aut(F₂). If AK(3) ~ α(AK(3)) and AK(3) ~ β(AK(3)), applying α letterwise to the second sequence (as in Lemma D2) gives α(AK(3)) ~ αβ(AK(3)), hence AK(3) ~ αβ(AK(3)); applying α⁻¹ to the first gives α⁻¹(AK(3)) ~ AK(3). Induction on word length in the generators finishes the proof. ∎

**Corollary D7.** If a presentation T has, in its AC component, a state whose Aut(F₂)-orbit meets AK(3)'s AC component, then T ~AC AK(3). (If φ(S) ~ AK(3) with S ~ T, apply φ⁻¹ to get S ~ φ⁻¹(AK(3)) ~ AK(3) by Lemma D6.) So Aut-orbit matching (Whitehead canonical forms) is a valid, certifiable *equivalence* test against AK(3), and a valid *triviality* test against known AC-trivial presentations (Lemma D2).

## 4. Results

### 4.1 Regression gate and component growth (experiment)

GS mode from AK(3), cap 24 (states below 25): **1,532,732** states — exactly the AK(3)-side count reported by Carr (§5 "independent re-derivation"), from an independently written engine. Per-barrier cumulative counts (GS / full):

| barrier ≤ | 13 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| GS | 1 | 26 | 40 | 1,000 | 2,128 | 19,604 | 38,612 | 136,720 | 246,856 | 855,208 | 1,532,732 |
| full | 1 | 26 | 40 | 1,000 | 2,128 | 20,024 | 39,840 | 143,988 | 257,488 | 886,932 | 1,580,780 |

No state has barrier 14, so every path from AK(3) out of its own Σ-orbit in either graph climbs to energy ≥ 15 — compatible with (weaker than) A's plateau theorem in its larger graph. Nevertheless the cap-27 component contains **12 Σ-classes of total length 13**, all needing an excursion (Whitehead canonical forms from `d_whitehead.py`):

| state | barrier | Aut(F₂)-orbit |
|---|---|---|
| (xyxYXY, xxxYYYY) = AK(3) | 13 | AK(3) |
| (xyxYXY, xxxxYYY) = x↔y image | 15 | AK(3) |
| (xyXyxY, xxxxyyy), (xyXyxY, xxxyyyy) | 19 | AK(3) |
| (xxYXyy, xxxyyXY), (xxYXyy, xxyyyXY), (xxyyXY, xxYXyyy), (xxyyXY, xxxYXyy) | 17 | Q |
| (xxYYXy, xxxyXYY), (xxYYXy, xxyXYYY), (xxyXYY, xxYYYXy), (xxyXYY, xxxYYXy) = Q | 19 | Q |

The energy-14 states number 40 (12 at barrier 17, 28 at barrier 19).

### 4.2 Three-source exhaustive run in the full graph at cap 27 (experiment)

Sources: AK(3); #1 = MS(2, x⁻²y⁻¹x²y) = (XyyxYYY, XXXYxxy) (Johnson / Burns–Macedońska candidate up to rotation); #2 = MS(2, x⁻²y⁻¹x²y⁻¹) = (XyyxYYY, XXXYxxY) — the two Shehper et al. claims that Carr left uncertified. Move set: all cyclic products (G_full); cap 27; barrier order; no budget hit. Targets: the 1190 MS benchmark (exact Σ match), and AC-19 (140,535), AC-19-extended minus its 634 MS rows (155,933 usable), AC-1M (938,686 usable at length ≤ 27), each inserted with all 8 signed-permutation images.

| source | states with barrier ≤ 24 | ≤ 25 | ≤ 26 | ≤ 27 |
|---|---|---|---|---|
| AK(3) | 1,580,780 | 5,531,256 | 10,269,488 | **37,161,104** |
| #1 | 140,796 | 366,604 | 864,908 | 2,350,516 |
| #2 | 174,512 | 434,648 | 2,615,296 | 8,689,072 |

Total 48,200,692 states, 361 s on one core. Results:

1. **No cross-source edge.** By Proposition D4, AK(3), #1 and #2 are pairwise disconnected in G_full(27). Since G_GS ⊂ G_full, every GS path joining any two of them also has bottleneck ≥ 28. This improves Carr's engine-relative bound d_GS ≥ 27 (his cap-28 run was inconclusive at barrier 27) to **≥ 28, and extends it to the larger full graph**.
2. **No primitive relator** occurs in any of the 48.2M states (so none of the three is trivialized through a primitive-relator state below 28).
3. **No match with the AC-trivial datasets** up to Σ and the 8 length-preserving automorphisms: no state of AK(3)'s component (nor of #1's, #2's) at energy ≤ 27 is, as far as these datasets go, known to be AC-trivial. By Corollary D5 a single hit would have trivialized AK(3).
4. **Benchmark membership:** AK(3)'s component contains exactly the 34 presentations of §4.3 (all at barrier ≤ 20; none newly enters at barriers 21–27). #1's contains 6 benchmark presentations, #2's contains 34, including 18 MS(4,·) presentations (lengths 17–19) and 10 MS(5,·) presentations (lengths 19–21), all entering at barriers 26–27; these 40 also have certificates (§4.4). All 74 hits are at line indices ≥ 640 of `1190MS.txt`; none is among its first 634 lines (which ACSolverX re-uses as training data).

Second regression gate (GS mode, same three sources, cap 26): **13,504,944** states, exactly Carr's "exclusive-cap-27" figure, with his per-source counts 135,892 / 356,836 / 851,836 (#1, barrier ≤ 24/25/26) and 168,304 / 424,352 / 2,534,472 (#2) all reproduced. The full graph is genuinely larger: 13,749,692 states at cap 26.

### 4.3 Certified members of AK(3)'s AC class from the Miller–Schupp benchmark (proved here by certificate)

The 1190-presentation Miller–Schupp benchmark (`data/1190MS.txt` of ACSolverX, commit 6a12515; stored in their Σ-canonical form) was matched exactly (Σ only). **34 benchmark presentations lie in AK(3)'s component**, all with barrier ≤ 20, and none appear at barriers 21–28. For each, `d_ms_certificates.py` built a strict elementary certificate from the exact tuple AK(3) = (xxxYYYY, xyxYXY) to the exact benchmark tuple, and the repository verifier `experiments/elementary_verify.py` accepted all 34. Every one has first relator YYYYXyyyx (a rotation of the inverse of x⁻¹y³xy⁻⁴), so each is MS(3,w) for a w with x⁻¹w equal, up to rotation/inversion, to the second relator listed.

| line (0-based) | relators | total length | barrier (full graph) | cyclic steps | elementary moves | elementary peak |
|---|---|---|---|---|---|---|
| 898 | YYYYXyyyx, YXYxx | 14 | 19 | 5 | 59 | 33 |
| 939 | YYYYXyyyx, YXXYx | 14 | 19 | 25 | 228 | 33 |
| 954 | YYYYXyyyx, YXYxyx | 15 | 15 | 3 | 29 | 21 |
| 716 | YYYYXyyyx, YYxyXX | 15 | 17 | 17 | 133 | 26 |
| 654 | YYYYXyyyx, YXyXYx | 15 | 19 | 23 | 185 | 28 |
| 818 | YYYYXyyyx, YYxxyX | 15 | 19 | 31 | 248 | 29 |
| 640 | YYYYXyyyx, YXYXYx | 15 | 20 | 28 | 244 | 35 |
| 1060 | YYYYXyyyx, YXYxYx | 15 | 20 | 8 | 77 | 35 |
| 755 | YYYYXyyyx, YYxyXyX | 16 | 17 | 14 | 106 | 26 |
| 970 | YYYYXyyyx, YYYXXyx | 16 | 17 | 16 | 121 | 26 |
| 1103 | YYYYXyyyx, YYXyxyX | 16 | 17 | 12 | 85 | 25 |
| 1034 | YYYYXyyyx, YYxyXYX | 16 | 18 | 20 | 162 | 27 |
| 687 | YYYYXyyyx, YYxyxyX | 16 | 19 | 28 | 223 | 29 |
| 830 | YYYYXyyyx, YYYXyxx | 16 | 19 | 30 | 237 | 29 |
| 861 | YYYYXyyyx, YYxyXyx | 16 | 19 | 26 | 194 | 27 |
| 940 | YYYYXyyyx, YYxYxyX | 16 | 19 | 34 | 276 | 29 |
| 1063 | YYYYXyyyx, YYxYXYx | 16 | 20 | 11 | 101 | 33 |
| 1166 | YYYYXyyyx, YYXYxYX | 16 | 20 | 31 | 269 | 33 |
| 769 | YYYYXyyyx, YYYXyXyx | 17 | 17 | 13 | 93 | 25 |
| 934 | YYYYXyyyx, YYYXyxyX | 17 | 17 | 15 | 114 | 26 |
| 1143 | YYYYXyyyx, YYxYXyyx | 17 | 17 | 11 | 79 | 25 |
| 1119 | YYYYXyyyx, YYYXYXyx | 17 | 18 | 19 | 149 | 27 |
| 735 | YYYYXyyyx, YYYXYYxx | 17 | 19 | 41 | 328 | 29 |
| 768 | YYYYXyyyx, YYYXXYYx | 17 | 19 | 27 | 215 | 28 |
| 847 | YYYYXyyyx, YYYXyxYx | 17 | 19 | 33 | 264 | 29 |
| 867 | YYYYXyyyx, YYxYYxyX | 17 | 19 | 37 | 294 | 29 |
| 1170 | YYYYXyyyx, YYXyyxYX | 17 | 19 | 26 | 216 | 43 |
| 1174 | YYYYXyyyx, YYYXyxyx | 17 | 19 | 27 | 215 | 29 |
| 1182 | YYYYXyyyx, YYYxyXyx | 17 | 19 | 29 | 231 | 29 |
| 1189 | YYYYXyyyx, YYXYYxyX | 17 | 19 | 23 | 190 | 28 |
| 669 | YYYYXyyyx, YYYXYxYX | 17 | 20 | 34 | 287 | 35 |
| 715 | YYYYXyyyx, YYYYxYXX | 17 | 20 | 36 | 295 | 31 |
| 1005 | YYYYXyyyx, YYYYxxYX | 17 | 20 | 16 | 130 | 31 |
| 1010 | YYYYXyyyx, YYYxYXYx | 17 | 20 | 14 | 120 | 35 |

Lines 898 and 939 (0-based line indices of `1190MS.txt`) are MS(3, y⁻¹x²y⁻¹) and MS(3, yx²y), Carr's Theorems 4 and 3 (also Research C for the first); their full-graph barrier 19 equals Carr's exact GS bottleneck 19 for MS(3,yx²y). The other 32 (lengths 15–17) are additional class members with public certificates.

Consequence (proved here, by the certificates): each of these 34 presentations is AC-trivial if and only if AK(3) is, and any AC invariant separating one of them from the trivial presentation would also separate AK(3). This reduces the benchmark's open classes but does not touch AK(3)'s own status.

### 4.4 By-product: certified members of the two MS(2) holdout classes (proved here by certificate)

From the same cap-27 run, `d_ms_certificates.py … 1 XyyxYYY XXXYxxy d_ms2a` and `… 2 XyyxYYY XXXYxxY d_ms2b` produced 6 + 34 certificates (`certificates/d_ms2a_to_msNNNN.json`, `certificates/d_ms2b_to_msNNNN.json`), all accepted by `elementary_verify.py`. Two of them (lines 1059, 802) only identify the sources with their benchmark rows. #1's class gains 5 further benchmark presentations (lengths 14–15). #2's class gains 33, including benchmark presentations whose first relator is x⁻¹y⁴xy⁻⁵ (18 of them) or x⁻¹y⁵xy⁻⁶ (10), i.e. MS(4,·) of lengths 17–19 and MS(5,·) of lengths 19–21, reached only at barriers 26–27. This enlarges Carr's certified blocks C₁, C₂ (his Theorems 1–2) but does not join them to AK(3). (This is in agent F's area; it is reported because it came for free.)

### 4.5 Automorphism realizations and a second minimal Aut-orbit in AK(3)'s class (proved here by certificate)

- **Aut-generators.** With exact targets φ(AK(3)) (cyclically reduced) for the seven maps of Lemma D6, all seven are in AK(3)'s G_full component, at barriers swap 15; x↦xy and y↦yx 17; x↦xy⁻¹, y↦yx⁻¹, x↦x⁻¹, y↦y⁻¹ 19. Certificates `d_ak3_aut_*.json`: 45–173 elementary moves, elementary peaks 21–41. This makes Panteleev–Ushakov's realization theorem (externally reported for all n) explicit and machine-checked for n = 3.
- **Two minimal Aut-orbits.** Whitehead canonical forms (C++ `--autmatch`; cross-checked by the independent `experiments/d_whitehead.py`) show that AK(3)'s component already at cap 20 meets exactly two Aut(F₂)-orbits of total length 13: AK(3)'s own and that of **Q = (x²yx⁻¹y⁻², x³y⁻²x⁻¹y) = (xxyXYY, xxxYYXy)**. Q itself is in AK(3)'s exact component (barrier 19); `certificates/d_ak3_to_len13b.json` (270 moves, peak 28) certifies AK(3) ~AC Q with no automorphism. Python: AK(3) ↦ canonical (XXXXYYY, XYxYXy), Q ↦ (XXXYYxy, XXyxYY): different orbits. By Havas–Ramsay's length-13 classification (externally reported) such an equivalence is expected; the explicit certificate and the orbit separation are, as far as I know, not published (novelty not established).

### 4.6 AK(3) alone at cap 28, and the holdouts at cap 28 (experiment)

**AK(3), G_full(28):** 69,190,160 states (barrier 28 adds 32,029,056 to the 37,161,104 at ≤ 27); 582 s, ~2.5 GB RSS. No primitive relator; no match with AC-19 / AC-19-ext / AC-1M up to Σ and the 8 signed permutations; benchmark hits: exactly the same 34 as at cap 20. The full key set was dumped (`--dumpkeys`) for the following tests.

**Holdouts, G_full(28), tested against the dumped components (`--target-keys`):**

| source | states, barrier ≤ 28 | meets AK(3)'s cap-28 component? | meets #1's? |
|---|---|---|---|
| #1 = MS(2, x⁻²y⁻¹x²y) | 5,445,188 | no | — |
| #2 = MS(2, x⁻²y⁻¹x²y⁻¹) | 15,040,328 | no | no |

(The ≤ 27 counts, 2,350,516 and 8,689,072, agree with the three-source run, as they must.) Hence **every G_full path, and so every GS path, joining any two of AK(3), #1, #2 reaches total length ≥ 29** (experiment, engine-relative). Neither holdout component contains a primitive relator or a dataset match.

**Aut(F₂)-orbit matching (experiment; validity of the conclusions by Lemma D2 and Corollary D7).** Every one of the 69,190,160 states of AK(3)'s G_full(28) component was reduced to its Whitehead-canonical Aut(F₂)-orbit: no closure overflow, 6,347,128 distinct orbits. The same was done for 1,432,816 dataset presentations (AC-19, AC-19-ext minus MS rows, AC-1M, all lengths, Whitehead-reduced; one entry could not be encoded). One core, 489 s. Results:

- **0 matches.** No state of the component is an automorphic image of any presentation reported AC-trivial in these datasets. A single match would have trivialized AK(3) (Lemma D2), pending re-verification of the dataset entry.
- **Minimum Aut-length 13.** No state is an automorphic image of a presentation of total length ≤ 12. All of those are AC-trivial (Miasnikov–Myasnikov, externally reported), so a single exception would also have trivialized AK(3). Histogram (Aut-minimal length: states): 13: 404 · 14: 1,464 · 15: 6,700 · 16: 5,508 · 17: 26,744 · 18: 26,236 · 19: 117,376 · 20: 97,892 · 21: 483,960 · 22: 479,576 · 23: 2,062,732 · 24: 1,787,604 · 25: 7,743,612 · 26: 6,734,012 · 27: 27,103,296 · 28: 22,513,044.
- The length-13 orbits met are exactly two (AK(3)'s and Q's, §4.5); five orbits of length 14 occur.
- **Holdouts up to automorphism.** #1's and #2's G_full(28) components have 464,015 and 1,255,335 Aut-orbits, both with minimum Aut-length 14. The three orbit sets are **pairwise disjoint** (`--autcompare`). By Corollary D7, an orbit shared with AK(3) would have proved the corresponding Shehper et al. claim, with a certificate obtainable by transport. None exists at this cap.

## 5. Reproduction (executed in this investigation)

```sh
g++ -O2 -std=c++17 -o d_acsearch experiments/d_acsearch.cpp
./d_acsearch --self-test
#   primitivity filter agrees with unfiltered Whitehead on all 797184 cyclically reduced words of length <= 12 (1500 primitive)
#   aut-canonical invariance checks passed: 2925
#   self-test passed: 200000 random encode/decode + Sigma-invariance checks, 15 primitivity checks
python3 experiments/d_whitehead.py --self-test        # self-test passed: 258 random automorphism-invariance checks
python3 experiments/d_certify.py --self-test          # self-test passed: 33 moves
python3 -I experiments/d_prepare_targets.py --self-test
./d_acsearch --gs --cap 24 --maxstates 30000000       # regression: total_states 1532732
./d_acsearch --cap 24 --maxstates 30000000            # full graph: 1580780
# targets (third-party data, not redistributed):
git clone --depth 1 https://github.com/Math-AI-Caltech/ACSolverX   # commit 6a12515fe1d9...
python3 -I experiments/d_prepare_targets.py ACSolverX/data targets
awk -F'[: ]' '$2>=634' targets/AC19X.tgt > targets/AC19Xtail.tgt   # drop the 634 MS rows
# second regression gate (GS, three sources, cap 26): total_states 13504944
./d_acsearch --gs --cap 26 --maxstates 40000000 --source xxxYYYY,xyxYXY --source XyyxYYY,XXXYxxy --source XyyxYYY,XXXYxxY
T="--exact-targets targets/MS.tgt --trivial-targets targets/AC19.tgt --trivial-targets targets/AC19Xtail.tgt --trivial-targets targets/AC1M.tgt"
# §4.2 (361 s, ~2.1 GB): three sources, full graph, cap 27
./d_acsearch --cap 27 --maxstates 125000000 --source xxxYYYY,xyxYXY --source XyyxYYY,XXXYxxy --source XyyxYYY,XXXYxxY $T --maxhits 400 > run_r3.txt
python3 experiments/d_ms_certificates.py run_r3.txt targets/MS.tgt certs 1 XyyxYYY XXXYxxy d_ms2a   # 6 written and replayed
python3 experiments/d_ms_certificates.py run_r3.txt targets/MS.tgt certs 2 XyyxYYY XXXYxxY d_ms2b   # 34 written and replayed
# §4.6: AK(3) alone, cap 28, key dump, then Aut-orbit matching
./d_acsearch --cap 28 --maxstates 110000000 $T --dumpkeys 0 k28_ak3.bin > run_r4.txt
./d_acsearch --autmatch k28_ak3.bin --autdump aut_ak3.bin targets/AC19.tgt targets/AC19Xtail.tgt targets/AC1M.tgt
./d_acsearch --cap 28 --maxstates 60000000 --source XyyxYYY,XXXYxxy --target-keys k28_ak3.bin --dumpkeys 0 k28_ms2a.bin   # target_key_hits 0
cat k28_ak3.bin k28_ms2a.bin > k28_ak3_ms2a.bin
./d_acsearch --cap 28 --maxstates 100000000 --source XyyxYYY,XXXYxxY --target-keys k28_ak3_ms2a.bin --dumpkeys 0 k28_ms2b.bin   # target_key_hits 0
./d_acsearch --autmatch k28_ms2a.bin --autdump aut_ms2a.bin; ./d_acsearch --autmatch k28_ms2b.bin --autdump aut_ms2b.bin
./d_acsearch --autcompare aut_ak3.bin aut_ms2a.bin; ./d_acsearch --autcompare aut_ak3.bin aut_ms2b.bin; ./d_acsearch --autcompare aut_ms2a.bin aut_ms2b.bin
# §4.5
printf 'L13b xxyXYY xxxYYXy\n' > l13.tgt; ./d_acsearch --cap 24 --maxstates 3000000 --exact-targets l13.tgt --maxhits 5
python3 experiments/d_whitehead.py xxxYYYY xyxYXY xxyXYY xxxYYXy
./d_acsearch --cap 20 --maxstates 5000000 --exact-targets targets/MS.tgt --maxhits 1000 > run_ms20.txt
python3 experiments/d_ms_certificates.py run_ms20.txt targets/MS.tgt certs/   # 34 certificates written and replayed
printf 'swap yyyXXXX yxyXYX\ninvy xxxyyyy xYxyXy\ninvx XXXYYYY XyXYxY\nx_xy xyxyxYYY xyyxYXY\nx_xY xYxYxYYYYY xxYXY\ny_yx xxYXYXYXY xyxYXXY\ny_yX xxxxYxYxYxY xyxYY\n' > phi.tgt
./d_acsearch --cap 19 --maxstates 3000000 --exact-targets phi.tgt --maxhits 20 > phi_run.txt   # 7 hits; paths -> d_certify.py
python3 experiments/elementary_verify.py certificates/d_*.json        # 82 lines, exit 0
```

SHA-256 of the uncompressed inputs: `AC19.txt` f72df134e4deca4cb9c040099b6e09b2b45516f9aa460fc460a120669f1f1e19, `AC19_extended.txt` d028cd4d54f9204be8b2d811f9b6d428bc2920fa83a0e2143a32ad52f55660c0. The AC-trivial labels of AC-19/AC-1M are the dataset authors' claims; they are used only as potential targets, and any hit would have had to be re-trivialized and certified here before being claimed.

## 6. Honest limits

- **Engine-relative negatives.** "No trivialization / no MS(2) connection below energy C" refers to paths in G_full(C) only. An elementary AC path can multiply by a long conjugate h r_j h⁻¹ while all cyclic lengths stay small; such a step is not a single cyclic product, so these bounds are not lower bounds for ordinary AC paths, not lower bounds on intermediate word lengths, and not evidence of non-triviality. They are also incomparable with Bowman–McCaul's and Panteleev–Ushakov's per-relator bounds (17 and 20): a total cap of 28 admits a relator of length 22 but excludes pairs with both relators near 17–20.
- **The dataset test is only as strong as the datasets.** AC-19/AC-1M are finite samples of the trivial class produced by greedy/automorphism-based generators, so they are biased toward "easy" presentations. The in-search test uses only the 8 signed permutations. The post-hoc test uses all of Aut(F₂), but it compares orbits of states. It is not a search of the Aut-orbit graph, so the cap still applies to actual representatives. Its correctness relies on Whitehead's peak-reduction theorem for tuples of cyclic words (classical, externally reported) and on implementation checks (2,925 random invariance tests in C++; an independent Python implementation, 258 tests, agreeing on the examples in §4.5).
- **Novelty.** Fagan et al.'s classification table groups the unsolved benchmark presentations into classes without published paths; Carr argues this records unpublished connections. So the *equivalences* in §4.3–4.4 may already be known to them, and Q ~ AK(3) is implied by Havas–Ramsay's classification. Panteleev–Ushakov proved Lemma D6 for all n. As far as I could check, what is new is public replayable certificates (32 new MS(3) members, 38 holdout-class members, Q, the seven Aut generators), the full-graph and Aut-orbit negative tests, and the improved holdout bound. Literature access was partial (no arXiv full texts), so novelty is not established.
- No stabilization, no quotient argument, and no automorphism is used in any certificate.

## 7. Insight and recommended next direction

- **What the data say about AK(3)'s class near the bottom.** AK(3)'s cyclic-product component is thin at first (1 state at barrier 13, none at 14, 26 at 15) and then grows by roughly ×3.5 at odd and ×1.9 at even caps (a cyclic product changes total length by |v|−2c, so parity flips only through odd-length donors). Inside it, the class already contains two distinct minimal Aut-orbits, all seven Aut-generator images, and 34 MS(3,·) benchmark presentations — all by barrier 20. From barrier 21 up to 28 nothing further from the benchmark, nothing primitive and nothing from the ≈1.29M-presentation trivial datasets appears. In the Two-Hump language: no state of AK(3)'s energy-≤ 28 component lies in the sampled "easy" trivial set, even after closing that set under all automorphisms of F₂. The Aut-closure of the whole ≤ 12 stratum, which is AC-trivial by Miasnikov–Myasnikov, is not reached either.
- **The MS(2) holdouts are farther than previously certified.** No cyclic-product path joins either of them to AK(3), or to each other, without reaching total length 29. If Shehper et al.'s two remaining claims are true, their connecting paths need larger excursions, moves outside the cyclic-product graph, or both.
- **Recommended next step (constructive).** Use Lemma D6/Corollary D7 to search the *Aut-orbit graph*: vertices = Whitehead-canonical Aut(F₂)-orbits, edges = cyclic products applied to orbit representatives, barrier = Aut-minimal total length. Every hit stays certifiable: transport moves through φ (Lemma D2) and splice in the Lemma D6 certificates. The cap-24 component compresses ×12 (1,580,780 states → 130,326 orbits) and the cap-28 component ×10.9 (69,190,160 → 6,347,128), so the same memory reaches higher caps, and AC-1M's long automorphism-generated presentations become comparable after Whitehead reduction. A second, independent extension is to add short-conjugator products r_i ← r_i·h r_j^{±1} h⁻¹ (|h| ≤ 2). This narrows the gap between cyclic-product paths and arbitrary elementary paths, which is the main caveat on every bound in this note.

## 8. Files written

- `experiments/d_acsearch.cpp` — barrier-ordered exhaustive search engine: GS and full modes, multi-source collisions, primitive detection, Σ / aut8 target matching, `--dumpkeys` / `--target-keys` for sequential component comparison, `--autmatch` / `--autdump` / `--autcompare` for Whitehead (Aut(F₂)) orbit matching, and `--self-test`.
- `experiments/d_certify.py` — independent expansion of a canonical path into a strict elementary certificate (`--self-test`).
- `experiments/d_prepare_targets.py` — converter for the ACSolverX datasets (`--self-test`).
- `experiments/d_ms_certificates.py` — batch certificate builder for benchmark hits, with replay.
- `experiments/d_whitehead.py` — independent Python Whitehead/Aut(F₂) canonical form (`--self-test`).
- `certificates/d_ak3_to_msNNNN.json` (34) — AK(3) → exact 1190MS benchmark tuple NNNN (§4.3).
- `certificates/d_ak3_to_len13b.json` — AK(3) → Q (§4.5).
- `certificates/d_ak3_aut_{swap,invx,invy,x_xy,x_xY,y_yx,y_yX}.json` (7) — AK(3) → φ(AK(3)) (Lemma D6).
- `certificates/d_ms2a_to_msNNNN.json` (6), `certificates/d_ms2b_to_msNNNN.json` (34) — holdout classes (§4.4).

All 82 certificates (1.1 MB) pass `python3 experiments/elementary_verify.py certificates/d_*.json` (exit 0).

## 9. Primary references

- S. Akbulut, R. Kirby, *A potential smooth counterexample in dimension 4 to the Poincaré conjecture, the Schoenflies conjecture, and the Andrews–Curtis conjecture*, Topology 24 (1985).
- R. S. Bowman, S. B. McCaul, *Fast searching for Andrews–Curtis trivializations*, Experimental Math. 15 (2006) 193–197, https://projecteuclid.org/euclid.em/1175789740 (bounds as cited by Lisitsa, https://arxiv.org/html/2501.18601v1).
- G. Havas, C. Ramsay, *Breadth-first search and the Andrews–Curtis conjecture*, IJAC 13 (2003).
- A. D. Miasnikov, A. G. Myasnikov, *Balanced presentations of the trivial group on two generators and the Andrews–Curtis conjecture*, arXiv:math/0304305.
- D. Panteleev, A. Ushakov, *Conjugacy search problem and the Andrews–Curtis conjecture*, arXiv:1609.00325; Groups Complex. Cryptol. 11 (2019) 43–60, https://doi.org/10.1515/gcc-2019-2005.
- A. Shehper et al., *What makes math problems hard for reinforcement learning: a case study*, arXiv:2408.15332; code https://github.com/shehper/AC-Solver.
- L. Fagan et al., *The Two-Hump Problem*, arXiv:2606.21611; data and code https://github.com/Math-AI-Caltech/ACSolverX (commit 6a12515).
- J. Carr, *Machine-checkable equivalence certificates at the length-14 Andrews–Curtis frontier*, arXiv:2607.23611; artifacts https://github.com/joe-carr-data/ac-certificates.
- A. Lisitsa, arXiv:2501.18601 and the corrected journal version https://doi.org/10.1016/j.jaca.2025.100041.
- R. Gilman, A. Myasnikov, *Andrews–Curtis groups*, arXiv:2506.23031 (not used in the arguments).
