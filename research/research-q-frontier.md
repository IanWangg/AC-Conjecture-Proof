# Q follow-up: targeted ordinary branches beyond the cap-22 component

Date: 2026-11-02. **No AK(3) free-basis path or unrestricted obstruction
has been found.** No novelty claim. These are two explicitly finite
searches for an actual hidden primitive, using the rotation theorem in
[Q's main report](research-q.md) and R's complete primitive-loop decision.

## 1. Selected tuples from ordinary exploratory walks

The coordinating agent supplied 763 selected word pairs from four
ordinary exploratory walks, retaining seed/node metadata. I took the
fixed input file with SHA-256

    3dc9da8012f74eef4aa2d1b32bdff5492ab5011e79d2b52dfac9175a9a88fcc7.

The input is published as `results/q_outside_elite_pairs.json`. These
selected tuples are not a complete cyclic component. Their cyclic total
lengths can be as large as 90. This report does not independently replay
an entry ledger for every selected tuple; the primitive-absence statements
below are statements about the actual displayed words and need no
reachability assumption. The coordinating agent retains the walk
provenance for any future positive match requiring a full AC ledger.

Q enumerated all independent rotations:

| Quantity | Exact value |
|---|---:|
| Listed source pairs | 763 |
| Rotation pairs | 160,479 |
| Distinct unbased labelled core graphs | 78,712 |
| Direct signed-DAG exclusions | 78,710 |
| Exceptions | 2 |

R's exact finite-map code refolded and completely excluded both remaining
graphs, checking 232 map-pair states in total. There are no incomplete
records and no primitive witness. The two actual exceptional pairs and
their compact closed negative certificates are saved separately.

By the proved rotation theorem, **every independent conjugate pair of
each of these 763 tuples generates a primitive-free subgroup at every
word length**. The selection of the 763 tuples was heuristic; the
primitive-absence conclusion for their fixed displayed words and all
their independent conjugates is exhaustive. This distinction prevents
a finite search failure from becoming an unrestricted AC claim.

## 2. New distance-two bridge moves at cyclic energy 23

To seek a different possible primitive waypoint, I next targeted a new
ordinary branch directly outside N's certified cap-22 component.

Write a,b for the receiver and retained donor cyclic lengths. The axes
lemma gives new cyclic energy `a+2b+2d` for a disjoint-axis product whose
geodesic bridge has length d. For d=2 and target energy 23, the source
must satisfy

    a+2b=19.

There are exactly twenty oriented source/recipient choices satisfying
this equation in the published cap-22 catalogue. The new C++ program
enumerates every signed rotation of both source words and every reduced
two-letter bridge, forms the actual free-word product, and retains only
cyclic energy 23. Retaining energy 23 ensures these are genuine distance-
two cases: a shorter bridge or intersecting axes would give smaller
cyclic length. This is the entire stated distance-two frontier; it is
not every energy-23 edge or the full cap-23 component.

| Quantity | Exact value |
|---|---:|
| Oriented source choices | 20 |
| Signed rotation/bridge candidates | 41,472 |
| Admitted energy-23 candidates | 10,528 |
| Distinct resulting cyclic states | 5,264 |
| Independent rotations of those states | 510,048 |
| Distinct unbased labelled core graphs | 256,360 |
| Direct signed-DAG exclusions | 256,360 |
| Exceptions or primitive witnesses | 0 |

The full frontier records retain the source index, both source words,
chosen receiver/donor rotations, bridge, and resulting state. They decode
to 1,033,592 JSONL bytes with SHA-256

    bdcc0ff56ccedb5c9a4917bec6d9d0d8eb3e38614cf82c641a511dced11238ec.

Thus all independently conjugated pairs in this stated new frontier also
generate primitive-free subgroups at every word length. Arbitrary
subsequent Nielsen operations cannot expose a primitive there either.
Further individual conjugations after mixing remain available.

## 3. Exact ordinary entry verification

The independent Python control program uses the repository's strict
free-word arithmetic and elementary verifier, rather than Q's C++
reducers. It compiles **every one of the 5,264 source-to-frontier macros**
to permitted inversions, positive right multiplications, and single-letter
conjugations. It replays 115,441 strict instructions in total. Every
macro has exact raw peak 27 and cyclic endpoint energy 23.

For a complete starting example, the coordinating agent's packed-path
compiler extracts a 22-strict-move, raw-peak-17 path from AK(3) to

    (XXXXyyy, XYXyxy).

Composing the first verified bridge macro gives an exact **47-strict-move**
AK(3) path with raw peak **27** and cyclic peak **23**, ending at

    (XXXXXXXYXyxyxxyyy, XYXyxy).

Both the entry and full certificates are published and replay with the
independent strict verifier. The endpoint is not a free basis; its whole
subgroup is among the directly certified primitive-free frontier graphs.
This example reaches a newly considered energy-23 branch and supplies no
upper bound for the peak of an actual trivialization.

## 4. A matching interface for the next completion attempt

The published rotation scanner now also has a library guard and the mode

    rotation_subgroups --match-pairs reverse.tsv forward.tsv match.json

It computes exact unbased core keys for the reverse word pairs, then
streams all rotations of the forward pairs and records a first identical
labelled core. It retains both actual tuples, their input indices and
original-base positions. It never declares the AC goal solved merely
because a key matches. A positive completion would still require the
actual forward and reverse AC paths, the subgroup conjugacy, and an
explicit Nielsen change between their two subgroup bases.

R is pursuing known AC-trivial reverse tuples. This can succeed even
when both matching subgroups are primitive-free: AK(2)'s original
subgroup is a calibrated example of a primitive-free subgroup generated
by an AC-trivial tuple. No actual cross-family matching success is
claimed in this report.

## Reproduce

Use the scripts together in `experiments/` and Python's standard library.
The exact data and combined results are in
`results/q_targeted_frontier_results.json`.

```sh
python3 experiments/cyclic_catalogue_to_tsv.py \
  certificates/cyclic22_component_manifest.json /tmp/cyclic22.tsv
c++ -std=c++17 -O3 experiments/bridge_two_frontier.cpp -o /tmp/q_bridge2
/tmp/q_bridge2 /tmp/cyclic22.tsv /tmp/q_frontier.tsv \
  /tmp/q_frontier.jsonl /tmp/q_frontier_result.json
c++ -std=c++17 -O3 experiments/rotation_subgroups.cpp -o /tmp/q_rotations
/tmp/q_rotations /tmp/q_frontier.tsv /tmp/q_frontier_candidates.jsonl \
  /tmp/q_frontier_rotations.json
python3 experiments/q_frontier_controls.py \
  certificates/cyclic22_component_manifest.json /tmp/q_frontier.jsonl \
  --entry-certificate certificates/q_bridge_two_example_entry.json \
  --full-certificate /tmp/q_example.json --output /tmp/q_macro_controls.json
python3 experiments/elementary_verify.py \
  certificates/q_bridge_two_example_AK3.json
```

The saved frontier certificate is standard gzip/base64 JSONL. To repeat
the selected-elite scan, convert each published `words` pair to a TSV row
and invoke the same rotation scanner; use R's candidate analyser for its
two exceptions. The elite closed-map certificates are also ordinary
gzip/base64 JSONL and use R's compact certificate verifier.

The numerical lower bound for a full AK(3) trivialization remains 23.
These targeted searches found no primitive waypoint and settle none of
the four full breakthrough objectives.
