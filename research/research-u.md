# Research U: independent native primitive detection and a calibrated positive pipeline

Date: 2026-11-02. **AK(3) and the ordinary, unstabilized Andrews–Curtis
conjecture remain unresolved.** No novelty claim is made.

The concrete contribution is an independent native implementation of R's
complete primitive-in-subgroup algorithm, with separate certificate
verification, exact agreement on all 6,568 previously exceptional graphs,
and a positive AK(2) calibration that T compiles into an ordinary AC proof.
U also supplied the explicit initial-subgroup theta decomposition used in
T's independent bounded basis-coverage proof.

## Prior reading and independent choice

Before choosing a direction I fetched the private repository README
(retrieved SHA `75d1116fb9d548f79d45e651aa27dd2b4616760c`) and read
[the cyclic-sublevel lemma](nielsen-cyclic-sublevels.md),
[Q's arbitrary-conjugation work](research-q.md),
[R's exact detector](research-r.md), and
[R's reverse-search follow-up](research-r-reverse.md).
The earlier work excludes ambient primitives from every independently
conjugated subgroup attached to the complete cyclic-cap-22 component.
It does not exclude later alternating subgroup changes.

I independently chose to examine a long Nielsen prelude inside the
initial subgroup, followed by independent conjugation and a search for
a hidden primitive. T and V independently chose that same direction.
After coordination, V owned the actual raw-basis enumeration and
rotation scan, T independently audited coverage and compiled positive
witnesses into elementary moves, and U implemented a separate native
exact detector. The root continued a different search with repeated
subgroup changes. This division avoids treating duplicate finite
searches as independent mathematical progress.

## 1. A reusable exact detector

The algorithm and completeness theorem are credited to
[R, Section 2](research-r.md). The classical input is uniqueness of a
primitive conjugacy class in rank two from its exponent vector; see
[Clay–Conant–Ramasubramanian, Corollary 4.4 and Theorem 4.6](https://msp.org/involve/2014/7-4/involve-v7-n4-p01-p.pdf).
U's contribution here is a separate implementation and audit, not a new
mathematical primitive-detection theorem.

Given a connected finite folded inverse graph on the ordered alphabet
`x,X,y,Y`, each letter acts as a partial transformation of its vertices.
For each signed alphabet `xy,xY,Xy,XY`, start with its two letter maps
and exhaust the ordered-pair states under

```
L(A,B) = (A,A B),       R(A,B) = (A B,B).
```

Here `A B` means follow `A` first and then `B`.
The corresponding positive word updates preserve a free basis, and
Euclidean reduction reaches a representative of every primitive
conjugacy class. A component fixing a real graph vertex yields a
primitive loop. Testing all vertices handles cyclic rotation of that
loop. Exhaustion with no fixed vertex therefore proves that the subgroup
contains no ambient primitive at any word length.

The native representation differs from R's byte maps. U uses total
integer maps on `N+1` points: the extra point `N` is absorbing and
represents every undefined transition. It is explicitly excluded from
fixed-point tests. A state stores both complete `uint16_t` arrays;
hash-table keys contain every byte and equality compares the complete
key. There is no hash-only equality or word-length cutoff.
For `N` real vertices the state space has at most `(N+1)^(2N)` states.
The implementation supports `1 <= N <= 65534`; this is an implementation
bound, not a mathematical bound. Large graphs can still require an
impractical number of states.

The header-only interface is:

```cpp
#include "u_native_primitive.hpp"
using Graph = std::vector<std::array<int,4>>; // x,X,y,Y; -1 = missing
auto result = u_native::decide(graph,
                              100000,   // state budget per alphabet; 0 = no budget
                              1000000,  // maximum expanded witness-word length
                              false);   // retain negative certificates
```

It returns `ABSENT`, `PRIMITIVE`, or `INCOMPLETE`, together with per-alphabet
state counts. A budget stop is always `INCOMPLETE`; it is never converted
into an absence result. Invalid or disconnected input graphs throw an
exception. A positive witness records the signed alphabet, L/R program,
component, fixed vertex and base-to-loop path. If expansion fits the
stated limit it also records both the cyclic primitive word and its based
conjugate. If expansion is too large the finite program remains a symbolic
positive witness; a literal AC compiler must expand and verify it before
claiming an elementary certificate.

`u_graph_fold.hpp` separately builds the input graph from literal words by
repeated single-conflict folding. It imports no Q/R graph code. The batch
driver can compare this independently folded graph with the supplied
candidate graph after rebasing in the fixed alphabet order. This guards
against deciding a graph that does not represent the actual candidate
word pair.

For negatives, the optional output is a finite set of total-map pairs
for each signed alphabet. The independent Python checker verifies:

- the graph's inverse arcs and connectedness;
- the initial map pair belongs to each saved set;
- every real vertex fails both fixed-point tests;
- both L/R successors of every pair remain in the saved set;
- the missing point is absorbing and the stored counts agree.

A closed set containing the initial pair suffices; no trust in the
native search order or parent pointers is required. Positive records are
checked by rebuilding the two words from the signed alphabet and L/R
program, then checking the fixed loop, base path and based primitive.
The verifier imports no native or R map-composition routine.

## 2. All previously exceptional graphs independently checked

Q's compressed candidate corpus has decompressed SHA256

```
d530e68cab069aabac841a1082bf5624d657a920001a72a77a3b39365bf167a5
```

It contains the 6,568 graphs that Q's sufficient direct signed-DAG
criterion did not settle. U independently refolded every actual word
pair, generated complete native closed-map certificates, checked those
certificates with the separate Python verifier, and expanded R's compact
sparse-map certificates for exact set comparison.

| Check | Result |
| --- | ---: |
| Candidate graphs independently refolded | 6,568 |
| Complete native `ABSENT` decisions | 6,568 |
| Primitive / incomplete decisions | 0 / 0 |
| Closed map-pair states separately checked | 735,712 |
| Largest one-graph, one-alphabet closure | 76 |
| Full closed-pair-set equalities with R | 6,568 graphs, all four alphabets |

This is stronger than merely obtaining the same status or state count:
the complete reachable pairs agree after translating the two different
map representations. The result independently corroborates R's existing
classification; it does not extend the cap-22 theorem to new AC states.
The native implementation is now available to the root's search for
primitive waypoints after later subgroup-changing moves.

For V's subsequent cap-250 phase scan, U also independently refolded
3,333 deterministic sample rotation pairs (three per source basis,
with repetitions retained) and exactly matched every supplied based
graph. The complete native detector returns `ABSENT` on all 3,333;
the separate checker verifies 277,164 closed pair states, with a maximum
of 56 states for one graph and alphabet. This is an additional sampled
audit, not an independent replay of V's entire 2,905,457-graph scan.
The sample JSONL SHA256 is
`b73e30eb1d408ac45400b1da322cd7f8243c929865060bedf5908d5975b0616e`.
[V](research-v.md) publishes the sampled input and full scan; U publishes
`results/u_v_sample_review.json` and the reusable review script.

## 3. Controls and a positive AK(2) route

The standalone control suite passes 2,205 standard-size cases:

| Control | Cases |
| --- | ---: |
| Signed primitive Christoffel cycle graphs | 372 |
| Proper-square cycle graphs | 372 |
| AK(3) relative conjugating tails of reduced length at most six | 1,457 |
| Standard basis, conjugated basis, AK(2) phase and branching negative | 4 |

It produces 375 positives, 1,830 complete negatives and zero incomplete
decisions. The separate verifier checks 170,968 closed pair states.
Every standard-size native folded graph, status and per-alphabet state
count agrees with R; all 1,461 rank-two controls also agree with M's
independent fold implementation. Further controls exercise the integer
representation beyond the old byte-map bound: a 257-vertex primitive
cycle and a 300-vertex proper-power cycle. A deliberately tiny state
budget returns `INCOMPLETE`, and deleting the initial pair from a negative
certificate is rejected.

V's complete AK(2) cap-12 phase scan has two initial-subgroup basis
families, 65 rotation pairs and 31 distinct unbased graphs. Its single
direct-DAG exception is the actual rotated pair

```
A = XXyyy,    B = YXyyXyx.
```

U's independent refolding and exact detector return a positive result:

```
signed alphabet = xY
positive basis program = RLRL
component = 1
fixed vertex = 3
base-to-loop path = XX
cyclic primitive = xYxYYxYY
based primitive = XYxYYxYYxx = B^-1 A^-1
```

The exact detector reaches 32 pair states before finding the loop
(eight in `xy`, then 24 discovered in `xY`). The Python checker rebuilds
and checks the primitive witness independently. The orientation matters:
V's B is the inverse of the B in an earlier R/O control.

[T's compiler](research-t.md) starts from the literal AK(2) pair
`(xxYYY,xyxYXY)`, reaches this actual V pair in 15 strict elementary
moves, exposes the hidden primitive by five further strict basis moves,
and finishes at literal `(x,y)`. U separately replayed T's full
[232-move certificate](../certificates/t_v_ak2_hidden_full.json) with the
strict elementary verifier; its raw total-length peak is 33.
This validates the detection-to-proof pipeline on a known trivializable
control. It is neither an AK(3) certificate nor a claim of an improved
AK(2) bound.

## 4. Initial-subgroup geometry supplied to T

For `p_n=x^n Y^(n+1)`, `b=xyxYXY`, and `n>=2`, simultaneous conjugation
by `Y` gives the basis

```
p'_n = Y x^n Y^n = P Q^-1,
b'   = YxyxYX   = P R^-1,
P = Yx,    Q = y^n X^(n-1),    R = xyXY.
```

The first letters of the three forward branch paths are `Y,y,x`; those
of the reverse paths are `X,x,y`. Their disjoint-interior theta graph is
therefore an immersion with branch lengths `2,2n-1,4` and the stated
free basis. U supplied this explicit decomposition to T and V.

For an abstract-subgroup primitive class of coprime exponent coordinates
`(a,b)`, the ambient cyclic length is

```
F_n(a,b) = 2|a+b| + (2n-1)|a| + 4|b|.
```

This assertion is for abstract primitive classes, not arbitrary words
having the same exponent vector. Counting paths in signed Euclidean
representatives proves the formula; primitive conjugacy uniqueness then
makes the cyclic length independent of representative. The coefficients
in the signed-coordinate cones are positive when `n>=2`, justifying the
monotone Farey energy pruning used by V. T supplies the full proof and an
independent matrix enumeration in [its report](research-t.md).

Actual raw words must be retained during the Nielsen prelude. Independent
cyclic normalization between prelude steps would change the subgroup and
would invalidate the claimed phase restriction. The final independent
conjugation phase is where cyclic classes may be used.

## Reproduction and scope

From a checkout containing the published repository experiments:

```sh
c++ -std=c++17 -O3 experiments/u_native_primitive.cpp -o /tmp/u-native
python3 experiments/u_native_controls.py --binary /tmp/u-native --references experiments --examples-directory /tmp/u-native-examples --output /tmp/u-native-controls.json
python3 experiments/u_review_candidates.py certificates/q_rotation_candidates.jsonl.gz.b64 --binary /tmp/u-native --output /tmp/u-native-hard-review.json
python3 experiments/elementary_verify.py certificates/t_v_ak2_hidden_full.json
```

For the optional exact equality comparison with R's full archived
certificate, first unpack R's compact JSONL as described in
[R's report](research-r.md), then add
`--R-certificates /path/to/unpacked-R-compact.jsonl` to the candidate
review command. All native negative certificates are regenerated and
separately verified even without this optional comparison.

The small published examples are
`certificates/u_native_initial_absence.json`,
`certificates/u_native_AK2_positive.json`, and
`certificates/u_native_branch_absence.json`; each is a single JSON record
accepted by `u_verify_native.py`. The summary records are
`results/u_native_control_results.json` and
`results/u_hard_candidate_review.json`; the cap-250 sample review is
`results/u_v_sample_review.json`.

The useful outcome is a faster independent exact detector with a
constructive positive witness and a verified route from such a witness
to ordinary elementary moves. It does not provide an unbounded AC
invariant, an AK(3) primitive waypoint, or any of the four unrestricted
outcomes requested in the goal.

Subsequently V established an unrestricted-length theorem for any two
independently conjugated elements of the original `H0`. U's
[independent geometric and finite-certificate review](u-voltage-phase-review.md)
checks that theorem and its AK(2) positive control. It still permits
later alternating subgroup changes. U also published a
[review of the root's repeated-phase engine and successful AK(2) calibration](u-coupled-engine-review.md).
