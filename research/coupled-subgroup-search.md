# Coupled subgroup search with an independently checked primitive pipeline

Date: 2026-11-02. **No ordinary AC completion or obstruction for AK(3) is
established.** This report records heuristic searches and positive AK(2)
controls, not a complete search component or a novelty claim.

## Why change the search

Q/R exclude ambient primitives from every independently conjugated
representative of the complete cyclic-cap-22 component. T/U/V separately
test higher bases of the original subgroup. A general ordinary AC path
can alternate subgroup changes many times. The coordinating agent
therefore tested a different search which detects hidden primitives in
every distinct generated boundary subgroup, including score-rejected
proposals, rather than only testing displayed relators or selected elites.

The graph folding, signed-DAG filter and exact unbased graph key are Q's;
the native complete primitive detector is U's independently implemented
version of R's theorem. These shared components are credited explicitly.
The phase sampler and strict path compiler are the new glue here.

## Literal phases and sound classifications

A node stores an actual cyclically reduced pair, its rank-two folded
graph, a parent, and a literal phase program. A breadth-first spanning
tree and sorted non-tree edges specify an actual basis of its subgroup.
The sampler starts from that basis, applies a random raw Nielsen prelude,
and only then independently cyclically reduces, optionally inverts, and
rotates both coordinates. Raw words are retained throughout the prelude.
An explicit formal-basis bridge compiles the change to the spanning basis
into ordinary moves; it is not a cost-free relator or generator change.

The source cyclic-energy limit is 100 or 120, with a raw-prelude rejection
threshold four times that limit. The prelude has at most 10 or 14 sampled
multiplications. Sources below cyclic energy 23 are discarded with
probability 0.9. Annealing, restarts, graph deduplication and score
penalties for original coordinate classes further restrict sampling.
These are search choices, not completeness arguments.

For each admitted graph, an exact unbased key is first compared with the
56,799 known-trivial reverse-subgroup keys. A repeated classified graph
reuses its conjugacy-invariant decision. A cyclic class in the certified
cap-22 catalogue has Q/R's all-tail absence theorem. Other graphs first
receive the sufficient signed-DAG test; every exception receives U's
complete finite partial-map-pair detector, with a per-alphabet budget of
100,000. A budget stop is recorded as `INCOMPLETE`, never as absence.
The engine does not automatically retry an incomplete key. There were no
incomplete cases in these runs. The initial graph is not classified by
this engine; the chosen AK(2)/AK(3) starts are covered separately by the
earlier results. An arbitrary new start needs its own initial check.

All classifications occur before score acceptance. The reported totals
cover sampled phase boundaries; they do not claim every intermediate
subgroup in the expanded elementary ledgers was tested. The cyclic cap
does not bound all expanded intermediate moves or their raw lengths.

## Four completed AK(3) runs

The first two start at literal `(xxxYYYY,xyxYXY)`. The third starts at
`(YxYXyyx,yXYXyxx)`, reached by the existing 32-move raw-peak-18 entry.
The fourth starts at `(XXXYYxy,XXyxYY)`, reached by the existing 43-move
raw-peak-18 entry. Both entries are in the certified cap-22 component.

| Seed | Source cyclic cap | Maximum prelude | Proposals | Distinct classified graph keys within run |
| ---: | ---: | ---: | ---: | ---: |
| 20261104 | 100 | 10 | 4,186,609 | 1,488,911 |
| 20261105 | 120 | 14 | 5,000,000 | 1,851,362 |
| 20261106 | 100 | 10 | 3,981,937 | 1,423,755 |
| 20261107 | 120 | 14 | 4,313,103 | 1,622,045 |

Together these are 17,481,649 proposals and 6,386,073 within-run distinct
graph classifications, **without cross-run deduplication**. Of those,
15,507 use the cap-22 theorem, 6,368,278 pass the signed-DAG criterion,
and 2,288 require and receive complete exact absence decisions. No
hidden primitive, known-trivial subgroup match, or incomplete decision
occurs. This finite heuristic failure is not an AC obstruction.

The first run was repeated with an I/O-only addition that archives all
native exceptions. Every statistic except timing matches exactly. R's
independent Python implementation refolds all 2,288 actual tuples,
recomputes their complete decisions, and separately verifies closure of
all 277,992 map-pair states. It agrees with every native status and state
count. The compressed exception log and checker permit independent
repetition; this is an audit of those exceptions, not global exhaustion.

The first run's selected 40-phase path compiles into a strictly replayed
2,152-move ordinary certificate from the original AK(3) to

```
(XyyyyXXXyxYxxYX, xyXXyXYx).
```

Its raw total-length peak is 233. The endpoint is not a free basis.
The large intermediate peak also illustrates why the phase-boundary
cyclic cap must not be described as a full elementary-path bound.

## Positive control: detection all the way to a free basis

Using the same engine, with reverse matching disabled, the AK(2) run
with seed 20261103 finds a primitive-containing subgroup after 138,768
proposals. Its actual endpoint pair is

```
(XXyyy, XYxYYxy).
```

U's detector supplies the actual based primitive `XYxYYxYYxx`, with
signed alphabet `xY` and program `RLRL`. The 27-phase path compiles from
literal `(xxYYY,xyxYXY)` to the actual pair in 1,305 strict moves.
`expose_hidden_primitive.py` independently checks ambient primitivity
and based subgroup membership, rewrites the word in a spanning-tree
basis, constructs its formal complement, and uses R/M's transported
basis bridge to expose it in four more moves. M's completion then
finishes at literal `(x,y)` in **1,521 total strict moves, raw peak 153**.

This deliberately long control validates the sampled-path-to-proof
pipeline. It is not an AK(3) completion or an improved AK(2) bound.
T's separate one-phase control is much shorter: 232 moves and raw peak
33. Both use the dependency-free strict elementary verifier, whose only
operations are inversion, positive right multiplication and
single-letter relator conjugation. There is no implicit stabilization,
ambient generator change, quotient equality, coordinate swap, or
endpoint normalization in either emitted ledger.

## Reproduction

The search needs C++17 and the published Q and U sources beside it. The
cap-22 TSV and reverse TSVs can be reconstructed from their published
manifests and journals using `cyclic_catalogue_to_tsv.py` and
`reverse_journal.py`, as in the earlier reports.

```
c++ -std=c++17 -O3 experiments/coupled_h_search.cpp -o /tmp/coupled-h
/tmp/coupled-h /tmp/c22.tsv /tmp/r_ak2.tsv /tmp/r_power.tsv 20261104 5000000 300000 100 10 /tmp/h-ak3
python3 experiments/compile_h_phase_path.py certificates/coupled_ak3_best_phase_path.json --certificate /tmp/h-ak3-strict.json --output /tmp/h-ak3-check.json
python3 experiments/review_coupled_native_cases.py certificates/coupled_native_cases.jsonl.gz.b64 --output /tmp/native-review.json
python3 experiments/elementary_verify.py certificates/coupled_ak2_full.json
```

To reconstruct the positive pipeline rather than just replay its output:

```
python3 experiments/compile_h_phase_path.py certificates/coupled_ak2_phase_path.json --certificate /tmp/ak2-prefix.json --output /tmp/ak2-prefix-result.json
python3 experiments/expose_hidden_primitive.py /tmp/ak2-prefix.json XYxYYxYYxx --waypoint /tmp/ak2-exposed.json --completion /tmp/ak2-full.json --output /tmp/ak2-result.json
```

The stored phase path format includes every raw prelude opcode and exact
boundary target. The compiler regenerates the deterministic tree basis,
compiles its bridge, expands the prelude and literal conjugacy choices,
and replays the entire concatenated ledger. A bare native hit or graph
match is never accepted as an AC completion.

Separately, the coordinator regenerated V's entire cap-250 computation:
all 1,111 source JSONL records match byte for byte, all 5,862,545 rotation
pairs produce the same 2,905,457 graphs, and the exception file is empty.
`reproduce_basis_phases.py` additionally replays T's source coverage,
U's controls, every exceptional graph from the earlier cap-22 work,
whole-set equality of native/R map-pair closures, the reverse-barbell
audit, and T's 232-move control. Its saved run validates the separately
regenerated scan; the default command regenerates that scan itself:

```
python3 experiments/reproduce_basis_phases.py --output /tmp/basis-review.json
```

The stronger [unbounded initial-subgroup theorem](research-v-unbounded.md)
is recorded separately in V's follow-up, with finite voltage certificates
and [the coordinator's independent audit](../results/v_voltage_independent_review.json).
The checker `verify_vertex_voltage.py` imports no voltage constructor or
Bellman–Ford solver: it refolds all 45 overgroups, verifies the characters,
reconstructs all 360 directed graphs, computes strongly connected sets by
mutual reachability, and checks all 822 integer inequalities. Neither
that theorem nor these heuristic searches
cover arbitrary later alternating subgroup changes. The original four
unrestricted breakthrough objectives remain unachieved.
