# Andrews–Curtis research

## Status

The ordinary AC triviality of AK(3) and both the ordinary and stable Andrews–Curtis conjectures remain unresolved in this repository. No novelty or priority claim is made for the partial results.

The five research tracks seek an ordinary AC trivialization of AK(3), a proof of Stable AC, a proof of ordinary AC, a counterexample to ordinary AC, and a counterexample to Stable AC. The marked AK(3) presentation is

    AK(3) = <x,y | x^3 y^-4, xyx y^-1 x^-1 y^-1>.

The initial investigation began on 2026-11-02 and involved twenty-six research agents. The numbered rounds continue that work across the five tracks. Each round records the proofs, computations, their scope, and questions shared across tracks. The current collaboration environment has three researcher slots alongside the coordinator, so each round runs its five researchers in waves.

| Round | Date | Synthesis |
|---|---|---|
| [01](research/round-01.md) | 2026-11-19 | Archive replay, geometric and algebraic descent, disjoint-axis obstructions, and stable distance by peak rank |
| [02](research/round-02.md) | 2026-11-19 | Cyclic peak at least 26, fiber-product joins, geometric blocks, triangular paths, and relative quotient lifts |
| [03](research/round-03.md) | 2026-11-19 | Cyclic peak at least 27, rank-three stable bound, malnormal cores, and wider frame descent |
| [04](research/round-04.md) | 2026-11-19 | Full cap-26 subgroup join audit, sharp fixed-pivot loss, and simultaneous finite/relative corrections |
| [05](research/round-05.md) | 2026-11-19 | Complete cyclic cap 28, stable transport to a new rank-two waypoint, and exact degree-seven stable quotient distance |
| [06](research/round-06.md) | 2026-11-19 | Complete cyclic cap 29, ordinary reachability of the first stable waypoint, and free-group instruction bounds |
| [07](research/round-07.md) | 2026-11-19 | Sharp ordinary waypoint peaks 30, 31 and 37, plus exact Magnus distances in degrees eight and nine |
| [08](research/round-08.md) | 2026-11-19 | Complete cyclic cap 30, free instruction bounds in both metrics, and simultaneous donor changes |
| [09](research/round-09.md) | 2026-11-19 | Generated cyclic cap 31, strict rank-three chart transport, and two spanning trees in stable product graphs |

## Current strongest checked results

- **Ordinary AK(3) cyclic peak at least 31, with a generated bound of 32.** The full cap-30 component passes independent closure, connectivity and primitive tests. Cap 31 exhausts 254,220,523 signed orbits and separately passes the primitive scan. Its independent closure check is active. [Cap-30 audit](research/round-08-cyclic30.md), [cap-31 generation](research/round-09-cyclic31.md).
- **Free-group instruction distances at least 19, ordinary and stable.** Two complete ordinary radius-nine balls are disjoint, and the exact padded retractions exclude every stable path of at most 18 instructions. [Native ordinary search](research/round-07-native-distances.md), [stable padding cases](research/round-08-free-distance.md).
- **Stable AK(3) at ranks at most three needs cyclic peak at least 22.** The independently audited cap 21 covers repeated insertions and deletions. Cap-22 generation gives a bound of 23, with all 432 returns in the ordinary cap-22 component and independent rank-three closure still active. The generated rank-three catalogue has no primitive deletion projection. [Cap-21 proof](research/round-03-stable-proof.md), [cap-22 generation](research/round-08-stable-proof.md), [primitive screen](research/round-09-stable-proof.md).
- **Ordinary and stable waypoints.** The first two stable projections enter the ordinary component at exact cyclic peaks 29 and 30. Three later Whitehead-minimal projections enter at 31, while one of their original markings first enters at 37. A further cap-24 rank-three waypoint projects to a pair whose ordinary entry peak is exactly 36. [Marked peak comparisons](research/round-07-stable-proof.md), [peak-36 certificate](research/round-08-stable-proof.md).
- **Magnus instruction distances in degrees eight through ten.** Both metrics equal 16 in degree eight and 17 in degree nine, for either target order. In degree ten both are at least 19. At budget 19 only zero or one padded pair remains possible in the quotient or in the free group. [Exact paths in degrees eight and nine](research/round-07-native-distances.md), [degree-ten stable checks](research/round-09-stable-disproof.md).
- **Two spanning trees in the stable crossing graph.** A shortest normalized path from any balanced normally generating tuple to an unordered positive basis has two edge-disjoint spanning trees in its contracted crossing graph. This requires at least $2k$ crossing products for $k$ added pairs. [Proof and exact schedule tests](research/round-09-stable-disproof.md).
- **Unbounded initial one-phase exclusion:** for every `u,v` in `H0=<xxxYYYY,xyxYXY>` and arbitrary independent conjugators, their two-conjugate subgroup is primitive-free. V certifies 45 infinite kernels with 822 integer inequalities; the coordinator and U independently verify them. This excludes an arbitrary initial Nielsen prelude, one conjugation phase and a Nielsen suffix at every length. Further alternating subgroup changes remain outside the theorem. [V's theorem](research/research-v-unbounded.md), [U's review](research/u-voltage-phase-review.md).
- **Restricted two-phase exclusion:** all 42 literal initial rotation successors satisfy the same unbounded two-conjugate property, with 2,272 kernel cases and 42,876 independently replayed inequalities. This excludes an initial pure conjugation phase whose endpoint axes intersect, arbitrary Nielsen mixing, another independent conjugation phase and a Nielsen suffix. A preceding arbitrary Nielsen prelude and disjoint first endpoint axes remain outside the result. [X's proof](research/research-x.md), [T's certificate audit](research/research-t-x-character-review.md), [Y's scope and actual-entry review](research/research-y-rotation-scope-review.md).
- **Literal cap-22 presentation complexes are not thickenable:** W supplies planar-link parity contradictions for all 258,032 literal canonical cyclic tuples, with a separate checker and T's independent review. A uniform three-equation proof excludes the initial literal AK(n) complexes for n>=2. This is a local embedding condition, not an AC invariant or an all-tail theorem. [W's proof and controls](research/research-w.md), [T's review](research/research-t-w-topology-review.md).
- **Direct raw cap-21 audit:** a complete cap-21 component has 27,380,372 inversion/permutation orbit states, no total length below 13, and no primitive relators. A separate string-based checker verifies its closure, including 112,696,624 allowed-neighbor checks. See the [packed extension](research/packed-peak-extension.md), [results](results/packed_peak_extension.json), and [independent source review](research/packed-audit-review.md).
- **Cyclic peak at least 23 for AK(3):** the complete cap-22 component contains 258,032 cyclic states and no primitive coordinate. A separate checker verifies closure and connectedness with 193,140,064 candidate products, including every permitted nonempty bridge. The Cayley-tree axes proof covers arbitrary conjugating tails. Thus any ordinary trivialization must reach cyclic total length at least 23, and therefore raw total length at least 23. See [N's full search](research/research-n-cyclic-search.md), [P's independent proof and audit](research/research-p-cyclic21-review.md), and the [explicit certificate manifest](certificates/cyclic22_component_manifest.json). The earlier all-n analytic bound 2n+9 remains valid for n>=3.
- **A necessary high-energy conjugation:** before the first primitive coordinate, some subgroup-changing conjugation must occur at cyclic energy at least 23. The [rank-two basis-sublevel proof](research/nielsen-cyclic-sublevels.md) controls Nielsen excursions in the cyclic-state quotient; [S's independent review](research/research-s-nielsen-sublevels-review.md) checks the geometry and finite core. It does not claim literal Nielsen-only low paths or raw peak reduction.
- **No initial primitive replacement, at any length:** neither one-relator deletion quotient permits a primitive free relator as a single quotient-conjugacy replacement for AK(n), n>=3. This unbounded one-step theorem is not preserved after both coordinates change.
- **Constructive infinite-quotient paths:** AK(3)'s image has exact instruction distances 10 in the braid quotient and 8 in the torus quotient. A synchronized 191-strict-move path works in their combined product. An optimized path works in the nonsolvable braid relation-module extension F/[N,N] in 533 fully replayed strict moves, improving the earlier 531,377-move expansion. Its actual free endpoint remains nontrivial, and greedy shortening gives an exact loop back to AK(3).

- **Every cap-22 representative has a primitive-free subgroup:** Q/R's axes theorem reduces arbitrary independent conjugating tails to rotation pairs. All 24,136,172 rotation pairs are classified: 11,424,800 unbased graphs pass the signed-DAG criterion, and all 6,568 exceptions have complete finite partial-map absence certificates. Thus any actual tuple in this cyclic component has no primitive in its generated subgroup at any word length, even after an unbounded Nielsen-only suffix. This is not invariant under later individual conjugations. The earlier uniform n>=2 cyclic braid-preimage theorem remains valid. [Q's reduction and scan](research/research-q.md), [R's exact detector and certificates](research/research-r.md).
- **Explicit short free-group paths:** existing cap-18 data now yield a 32-strict-move path to a cyclic-length-14 pair and a 43-move path to a different cyclic-length-13 pair, both with raw peak 18. These are exact free words, not bases, and were already inside the earlier exhausted component. [Certificates and lifting method](research/short-waypoint-paths.md). Earlier 222/179-move entries and their quotient analyses remain useful derivations.

These results constrain the ordinary AK(3) search. The numbered rounds also cover Stable AC and track how the two conjectures interact.

## Research reports

| Agent | Result | Scope |
|---|---|---|
| [A](research/research-a.md) | Exact initial nonincreasing quotient-conjugacy plateau for AK(n), n>=3 | Analytic cyclic bound 2n+8, strengthened by F |
| [B](research/research-b.md) | Explicit nilpotent paths and finite-quotient distance principle | Uniform class-2 path; 48-move class-3 AK(3) path with nonzero lifting errors |
| [C](research/research-c.md) | MS(n,y^-1 x^2 y^-1) is ordinary-AC equivalent to AK(n) | Symbolic all-n proof; 6n+14 strict moves, including 32 for n=3; not a trivialization |
| [D](research/research-d.md) | Complete raw cap-18 exclusion in two independent implementations | Original raw bound 19; superseded by the coordinating agent's [cap-21 extension](research/packed-peak-extension.md) |
| [E](research/research-e.md) | Exact distance 10 in the braid quotient B3 | Every quotient annihilating the braid relator has the same uniform upper bound |
| [F](research/research-f.md) | Cyclic peak at least 2n+9 for AK(n), n>=3 | AK(3) cyclic bound 15; explicit length-15 generalized replacement shows where the initial-family argument stops |
| [G](research/research-g.md) | Exact distance 8 in the complementary torus quotient | Exact free lift errors factored into 6 and 5 conjugates of the power relator |
| [H](research/research-h.md) | Uniform torus-family path with 2n+2 strict moves | Jointly develops G's pattern; pseudo-meridian distinction does not obstruct these two-coordinate AC paths |
| [I](research/research-i.md) | Braid lift errors have exact areas 5 and 13 | Nonzero relation-module errors; proper rank-2 endpoint subgroup prevents a Nielsen-only completion |
| [J](research/research-j.md) | Unbounded initial primitive-replacement exclusion | Uniform AK(n), n>=3 theorem using Nielsen uniqueness, traces and free-product normal forms |
| [K](research/research-k.md) | Explicit finite conjugacy obstructions after selected first departures | Three verified finite-group certificates exclude all primitive parameters in the specified frozen-coordinate quotients; they are not global AC obstructions |
| [L](research/research-l.md) | Small aligned prefix, 533-move first-order lift, exact free loop and next-central defect | Independent alternate-Schreier-basis review reproduces every coefficient of the nonzero next-central classes |
| [M](research/research-m.md) | Uniform primitive-free subgroup theorem and direct free-group search | Exact 246-move AK(2) control; [new reachable states and 5,632 literal-pair certificates](research/research-m-hump-transitions.md) |
| [N](research/research-n.md) | Primitive-free cyclic braid preimages and [complete cyclic cap-22 exclusion](research/research-n-cyclic-search.md) | Uniform n>=2 subgroup theorem; AK(3) cyclic peak at least 23 after independent audit |
| [O](research/research-o.md) | Finite reduction for arbitrary relative tails in rank two | Proved shortest-double-coset bridge lemma and explicit 1,457-tail graph certificate |
| [P](research/research-p.md) | Arbitrary-tail exclusion and [independent full cap-21/22 audit](research/research-p-cyclic21-review.md) | Independent word arithmetic, complete bridge menu, connectedness, and Euclidean scan of 179,630 nonprimitive coordinates |
| [Q](research/research-q.md) | Arbitrary conjugating tails reduce to independent rotation pairs | Complete cap-22 all-tail subgroup exclusion via 24,136,172 pairs and 11,431,368 unbased graphs |
| [R](research/research-r.md) | Exact finite primitive-in-subgroup detector | 735,712 closed partial-map pair states resolve all 6,568 exceptions; constructive AK(2) calibration |
| [S](research/research-s.md) | Remaining three power-nine frozen-coordinate exclusions | Seventeen dual linear witnesses and two closed finite orbits complete all six atlas classes |
| [T](research/research-t.md) | Independent initial-subgroup basis coverage through energy 250 | 1,111 classes and 33,238 strict source instructions; later reviews independently audit W's topology and X's exact character/phase results |
| [U](research/research-u.md) | Independent native exact primitive detector and voltage review | All 6,568 difficult graphs and 735,712 states checked; separately reviews V's unbounded theorem |
| [V](research/research-v.md) | Complete energy-250 initial-basis scan and [unbounded one-phase theorem](research/research-v-unbounded.md) | Arbitrary two source words in H0 and arbitrary independent conjugators; later alternating phases remain open |
| [W](research/research-w.md) | Uniform initial AK(n) thickening obstruction and complete literal cap-22 parity exclusion | Local presentation-complex topology, with positive nonprimitive-coordinate controls; not a global AC obstruction |
| [X](research/research-x.md) | Unbounded theorem for all 42 rotation successors and exact second-character audit | Restricted two-phase exclusion; 551 extension failures, 353 certified kernels, 111 method-family failures remain carefully separated |
| [Y](research/research-y-rotation-scope-review.md) | Independent rotation coverage, actual entries and phase-scope proof | All 42 sources and 2,272 indices; 135-move total ordinary entry controls, raw peak 13 |

Further research:

- The [computability and proof-translation note](research/computability-and-proof-translation.md) distinguishes semidecision, promised triviality, and recursive bounds. Ordinary AC is equivalent to a total computable compiler from finite triviality certificates to AC paths; a recursive bound based only on presentation size additionally requires decidability of balanced triviality. These are elementary reformulations, not an undecidability or AC-resolution theorem.

- [X's exact character audit](research/research-x.md) classifies 1,015 second vertex identifications of V's coarse kernel graphs. All 551 rank-two quotients are the ambient rose and cannot extend the specified nonzero character. Another 353 extension kernels have unbounded primitive-free certificates; 111 affine families fail the sufficient cycle-sign criterion for every real parameter. In 58 of those, actual primitives lie in every coarse extension kernel, without implying an eligible rank-two successor basis. T independently checks the real-parameter and primitive-witness arguments.
- [X's explicit barbell entries](research/research-x.md) retain long conjugating bridges before later raw Nielsen mixing. Six heuristic AK(3) runs make 15,000,000 proposals without a completion or saved reverse join; 26,130 instructions replay their selected actual paths. The same pipeline finishes an AK(2) control in 1,954 strict moves. These failed walks are not completeness arguments.
- The [basis-sublevel lemma and conjugation bottleneck](research/nielsen-cyclic-sublevels.md), [independently reviewed by S](research/research-s-nielsen-sublevels-review.md), identify a specific operation that must cross the energy-23 barrier. This strengthens the necessary condition without raising the numerical peak bound or proving non-AC-triviality.
- [R's two known-trivial reverse corpora](research/research-r-reverse.md) contain 20,985 and 35,814 subgroup keys respectively (V subsequently checks that all 56,799 keys are distinct). No match occurs against the complete cap-22 rotation set, the stated energy-23 frontier, or selected exploratory tuples. A generic subgroup-basis bridge is calibrated by an 11-move strict ledger. These finite failures are not an unrestricted obstruction.
- [Q's targeted frontier](research/research-q-frontier.md) reaches 5,264 new cyclic-energy-23 states; all independent conjugates remain primitive-free. All 5,264 macros replay in 115,441 strict moves, including a full 47-move AK(3) example with raw peak 27. This is not the full cap-23 component.
- [S's separate integer-map certificate review](research/research-s-rotation-review.md) rechecks every exceptional graph, source index and actual rotation with M's graph construction and an independent map implementation.

- [Q/R's all-tail theorem](research/research-q.md) extends O's literal-canonical subgroup result to every actual representative of every state in the cap-22 component. [R's finite-map algorithm](research/research-r.md) decides hidden ambient primitive existence exactly after finite exhaustion; explicit budget stops remain incomplete. The coordinating agent replays the entire 24-million-rotation computation and all 735,712 saved map-pair states in [the combined replay](results/round19_reproduction.json).
- [S's three finite obstructions](research/research-s.md) complete the frozen-coordinate primitive-replacement exclusions for all six power-nine first-departure classes. Short ordinary entries of 21, 10 and 13 moves are explicitly replayed. These do not classify later simultaneous-coordinate updates.
- [Explicit exploratory ordinary walks outside the component](research/outside-cyclic-search.md) make 19,647,745 heuristic proposals without finding a primitive coordinate. The failed search is not a completeness argument; a saved 2,159-move strict ledger has raw peak 67 and cyclic peak 63.

- [N's complete cyclic searches](research/research-n-cyclic-search.md) and [P's full independent audit](research/research-p-cyclic21-review.md) strengthen the ordinary cyclic peak bound from 15 to 23. The coordinating agent's [separate Python cap-20 audit](research/independent-cyclic-review.md) checks 25,895,168 rotation products. All are finite-energy exclusions with proved coverage of arbitrary tails, not unbounded AC obstructions.

- [O's full-subgroup refinement](research/research-o-cyclic-review.md) proves that all 258,032 literal canonical cap-22 pairs generate primitive-free subgroups, using DAG, simple-cycle and balanced-run certificates. This particular subgroup statement excludes independently conjugated representatives from its scope. The coordinating agent [rechecks all 416 exceptional graphs with M's separate folding routine](results/subgroup_refinement_review.json).
- [O's Nielsen-prelude extension](research/research-o-nielsen-tails.md) excludes primitive elements after the specified seven short-prelude families and arbitrary subsequent independent conjugating tails: 561,323 finite tail checks with an unbounded reduction. Its AK(2) calibration gives an exact 131-move basis path.
- [P's length-14 discovery](research/research-p-length14.md) and [the coordinating agent's checkpoint lifts](research/short-waypoint-paths.md) provide compact ordinary paths of 32 and 43 moves, both at raw peak 18. Their endpoint subgroups remain proper; these paths do not improve the previously exhausted search region.
- [N's cyclic-preimage theorem](research/research-n.md) and the coordinating agent's [complementary torus theorem](research/torus-cyclic-preimage.md) remove the old arbitrary-tail limitation for first-departure pairs. The torus representation also works for n=3 or 8 modulo 12. [O's finite-tail lemma](research/research-o.md) and [P's full independent computation](research/research-p.md) supply a different proof, including both later waypoints. These are subgroup theorems, not invariants under later interspersed AC operations.

- The coordinating agent's [first-departure atlas](research/first-hump-atlas.md) classifies 32 length-eight braid replacements and 432 length-nine power replacements from the literal initial tuple. The latter have six signed-symmetry classes. It includes exact ordinary entry certificates and positive twisted-conjugacy edges; it does not classify the whole length-15 component. Its historical arbitrary-tail limitation is resolved by N/O/P.
- [K's rank-three](research/research-k-rank3.md) and [further-state](research/research-k-second-hump.md) certificates independently exclude additional one-coordinate primitive routes. [L's analytic branches](research/research-l-branches.md) cover two further power-departure classes; together three of six have these exclusions.
- [L's optimized correction](research/research-l.md) uses 533 strict moves, with free endpoint lengths 635 and 1,867 and peak 2,502. The supplied 4,734-move strict loop returns exactly to the original AK(3) tuple. Its residual next-central classes have supports 67/148 and norms 322/469. [M's independent tensor review](research/research-m-second-central-review.md) confirms them. This blocks automatic repetition of the particular correction, not arbitrary AC moves.
- [M's new strict waypoints](research/research-m-hump-transitions.md) have 222/179 moves and peaks 31/25. The saved literal-catalogue certificate checks 1,340 folded graphs and 10,720 acyclic line graphs; [P](research/research-p.md) subsequently extends primitive absence to arbitrary tails. A [separate folding/DFS audit](results/hump_subgroup_independent_review.json) verifies all 5,632 pairs independently.

- [G's product synchronization](research/research-g-product.md) supplies a 191-strict-move path in B3 times T(3,4), with exact fourteen-instruction distance between 13 and 191. [Independent review](results/product_independent_review.json) replays the certificate using separately written quotient evaluators.
- [I's actual first-order correction](research/research-i-first-order.md) removes the braid-kernel module errors in F/[N,N], N the braid-relator normal closure. [Independent free-word and Fox replay](results/first_order_independent_review.json) confirms this quotient endpoint. The actual free words have lengths 230,627 and 946,303. The correction preserves braid images and need not preserve the torus factor; it is not claimed to refine the product result simultaneously.
- The coordinating agent's [finite PSL quotient experiment](research/finite-quotient-experiment.md) is now bounded uniformly by E's ten-move certificate, ruling out distance divergence in that entire representation family.

## Reproduce

Replay the new unbounded rotation-successor kernels, exact character-family certificates, archive hashes and strict barbell controls:

```sh
python3 experiments/verify_x_archives.py --certificates certificates --directory /tmp/x-review --output /tmp/x-review.json
```

The [combined archive replay passes](results/x_archive_reproduction.json). A [publication integrity audit](results/x_publication_integrity.json) verifies X's 24 research artifacts, the two restored control files and this README. [T's independent audit](research/research-t-x-character-review.md) and [Y's separate scope review](research/research-y-rotation-scope-review.md) give standalone commands. [W's report](research/research-w.md) gives the complete literal-topology replay and its exact scope. The earlier reproduction modes below retain their original certified scopes.

Python 3 and its standard library replay the main certificates, formula tests, the cap-18 baseline, selected complete instruction balls, finite conjugacy tests, the optimized free loop, and the catalogue/next-central audits:

```sh
python3 experiments/reproduce.py
```

Replay just the new cyclic-preimage arithmetic and arbitrary-tail checks:

```sh
python3 experiments/reproduce.py --tails-only
```

The [saved new replay](results/tail_reproduction.json) independently recomputes all 123,901 folds; [publication audit](results/tail_publication_integrity.json) matches all thirteen new theorem artifacts byte for byte. Earlier baseline replay is recorded separately in [results/reproduction.json](results/reproduction.json).

Replay the original cap-22 cyclic certificate, independent primitive scan, and the short strict paths with a C++17 compiler.

```sh
python3 experiments/reproduce.py --cyclic-only
```

The [combined replay passed](results/cyclic_reproduction.json), including the full 193,140,064-candidate cap-22 audit, 179,630-coordinate primitive scan, and strict path controls. A [publication integrity audit](results/round16_publication_integrity.json) matches all 74 new researcher/coordinator artifacts against their published Git blob SHAs.

Replay the new saved subgroup/branch certificates and independent folding controls:

```sh
python3 experiments/reproduce.py --subgroups-only
```

Also regenerate the complete 24,136,172-rotation enumeration (C++17 and about 2 GB memory):

```sh
python3 experiments/reproduce.py --subgroups-only --full-rotations
```

The [full combined replay passed](results/round19_reproduction.json), including the complete rotation enumeration, all 6,568 closed primitive-absence certificates, the three new finite branch obstructions, and positive AK(2) calibration. The [final publication audit](results/round19_publication_integrity.json) matches all 93 new researcher/coordinator artifacts to their Git blob SHAs. Both reverse-search journals also [replay completely](results/reverse_journal_reproduction.json), covering 174,206 parent edges and 20,985/35,814 independently folded candidate cores respectively. A [further replay](results/round19_followup_reproduction.json) checks S's separate integer-map implementation and every energy-23 frontier macro. The geometric basis-sublevel theorem has its own mathematical proof and independent finite controls; no proof-assistant formalization is claimed.

Add the independent original-state C++ cap-18 exhaustion, long endpoint's subgroup fold, full cyclic audit, and saved subgroup certificates:

```sh
python3 experiments/reproduce.py --cpp
```

Regenerate and independently audit the entire cap-21 component, including its primitive-relator scan:

```sh
python3 experiments/reproduce.py --cpp --packed
```

The C++ options require a C++17 compiler. The cap-21 option generates a roughly 356 MB native checkpoint and needs memory for the state sets. The default and `--cpp` runs explicitly report `raw_cap_replayed: 18`; the separately checked published cap-21 evidence is in [results/packed_peak_extension.json](results/packed_peak_extension.json). Only the `--packed` run regenerates that full result. Individual reports give standalone commands and precise finite bounds.

The dependency-free [strict elementary verifier](experiments/elementary_verify.py) accepts only relator inversion, positive right multiplication, and single-generator conjugation, with exact endpoints. It performs no implicit generator changes, stabilization, quotient rewriting, or endpoint normalization. The first-order certificate has a distinct word-conjugation format and [independent verifier](experiments/verify_first_order.py), with its finite ordinary expansion proved explicitly. The compact `.json.gz.b64` certificate contains all actual words after standard-library decoding.

## Completion standard and remaining work

A positive ordinary-AC result needs a complete proof or replayable path to the standard **free** basis. An obstruction must be invariant under all permitted moves at unbounded length. Group triviality, success in a quotient, and finite search failure do not meet either standard. Computations here are checked programs and explicit certificates, not proof-assistant formalizations.

The independently checked cap-30 component and the generated cap-31 component give the current ordinary cyclic exclusions. The frozen-coordinate, primitive-free subgroup and bridge theorems apply within the hypotheses of their individual reports. The quotient paths leave free errors, including after the known finite-layer corrections. The next round pursues the remaining length-19 instruction cases and searches for strict free suffixes and unbounded arguments. [Round 09 synthesis](research/round-09.md).

## Primary-literature cautions

- [Lackenby's 2026 preprint, Theorem 1.3](https://arxiv.org/pdf/2606.06122) proves ordinary AC triviality for balanced trivial presentations with thickenable presentation complexes. It requires an actual thickenable waypoint; W's local failures do not give a global AC obstruction.
- [Lisitsa's corrected published paper (2025)](https://doi.org/10.1016/j.jaca.2025.100041) reports that an earlier stable AK(3) claim depended on an incorrect theorem. That claim is not a solved starting point here.
- [Gilman and Myasnikov, Andrews–Curtis groups](https://gcc.episciences.org/15972/pdf) gives the algebraic setting.
- [Carreras's 2026 certificate preprint](https://arxiv.org/abs/2607.23611) supplies prior n=3 equivalence context credited in C. Restricted graph bounds from other sources are not silently transferred to ordinary AC paths.

Each report links the additional primary sources it used and distinguishes external theorems from deductions and experiments produced here.
