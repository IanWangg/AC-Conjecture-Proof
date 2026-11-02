# R follow-up: known-trivial-side subgroup matching with exact AC bridges

Date: 2026-11-02. **No AK(3) trivialization or unrestricted obstruction
has been found.** These are two sampled reverse searches and exact
constructive controls. No novelty claim.

## Prior reading and direction

After the joint Q/R rotation-subgroup theorem, I read Q's latest
763-elite and 5,264-state distance-two-frontier results. All their
independently conjugated subgroups were primitive-free. I independently
proposed a bidirectional search on labelled **subgroups**, rather than
requiring a forward tuple to expose a primitive coordinate immediately.
The coordinating agent asked me to pursue it; Q supplied a streaming
unbased-core matcher and reviewed the constructive bridge compiler.

The two known-trivial starting points are

    AK(2):              (xxYYY, xyxYXY),
    power/meridian:     (xxxYYYY, xY).

The second shares AK(3)'s power relator exactly but has a different
second relator. It is not AK(3). Its strict **51-move** certificate to
`(x,y)` has raw peak **15** and passes the independent verifier. AK(2)
already has the published exact 46-move control. These actual certificates
anchor the known-trivial side without relying on a quotient computation.

## 1. Why an exact subgroup match would suffice

Suppose an actual AK(3)-side pair and a known-trivial-side pair have
isomorphic unbased **label-preserving** rank-two subgroup core graphs.
Their subgroups are globally conjugate in F(x,y). Rebase the common
graph at the forward pair's vertex and let p be a labelled graph path
to the reverse pair's vertex. Then

    H_forward = p H_reverse p^-1.

Both two-element generating pairs are free bases of their rank-two
subgroup. Thus a global conjugation and a coordinate basis change join
them. This is the standard spanning-tree/Nielsen description of subgroup
bases; see
[Kapovich--Myasnikov, Stallings Foldings and Subgroups of Free Groups](https://web.stevens.edu/algebraic/alexeim/Teaching/GroupTheory626/graph5.pdf).
The test is equality of full labelled adjacency graphs, not equality of
rank, vertex count, homology or an unlabelled topological type.

The bridge compiler makes that reasoning concrete:

1. Conjugate both reverse relators by the explicit path p.
2. Choose a spanning tree of the common graph. Its two non-tree edges
   give actual ambient words z0,z1 forming a subgroup basis.
3. Rewrite both pairs as formal words in z0,z1 and verify by substitution
   that the rewritten words recover the actual original words exactly.
4. Apply M's existing strict compiler to each formal free basis, joining
   it to the standard formal pair. Reverse one ledger, and transport
   every formal conjugator back to its actual word in z0,z1.
5. Expand those word conjugations into signed single-generator
   conjugations and independently replay the resulting free-word ledger.

All inversions and multiplications stay ordinary relator operations.
No ambient generator change, stabilization, or quotient-relator equality
is inserted as a move. An actual goal proof would still require the
entry ledger on each side of the bridge.

### Nontrivial positive bridge control

Take u=xxYYY and v=xyxYXY. Use the known subgroup bases `(u,v)` and
`(uv,v)`, and globally conjugate the latter by X. The matcher finds a
common labelled core with different recorded basepoints. The compiler
produces an **11-strict-move** actual bridge, raw peak **17**, from

    (xYYYxyxYXYx, yxYXYx)

to the matched rotated forward pair

    (YxxYY, YxyxYX).

The explicit base-change word is `Yx`. Both the formal spanning-tree
substitutions and the final strict endpoint pass. This tests a genuine
basis/basepoint change; it is a constructed AK(2) control, not an AK(3)
match.

## 2. Actual reverse exploration and retained provenance

The heuristic walk chooses signed cyclic rotations of the current
recipient and donor, a reduced relative word q of length at most four,
then replaces the recipient by the cyclic reduction of

    u q v q^-1.

Each such edge expands into allowed ordinary moves. The parent,
recipient, signs, rotation offsets and q are retained. Individual cyclic
normalizations are actual inversions/conjugations, not ambient basis
changes. The scoring and acceptance rules are heuristic and give no
negative theorem.

From selected states, the program enumerates independent rotations and
retains distinct unbased core keys with 7 through 21 vertices. It also
filters by a stated candidate energy cap and excludes primitive displayed
coordinates. These are sampling restrictions, not a completeness claim
for the known-trivial AC orbit. Q's core/folding implementation is shared
explicitly. R's separate Python verifier reconstructs every parent word
operation, independently folds every retained actual candidate, checks
rank two/core degree/key uniqueness, and reproduces the exact matching
TSV hash.

| Quantity | AK(2) anchor | Power/meridian anchor |
|---|---:|---:|
| Seed | 918273 | 918274 |
| Product attempts | 1,000,000 | 2,000,000 |
| Stored cyclic states | 61,864 | 112,344 |
| Independently checked parent edges | 61,863 | 112,343 |
| Maximum accepted cyclic sum | 48 | 56 |
| Candidate cyclic-sum cap | 26 | 30 |
| Candidate source states | 798 | 2,122 |
| Candidate rotation pairs examined | 75,458 | 230,958 |
| Distinct retained unbased core keys | 20,985 | 35,814 |
| Maximum parent depth | 403 | 446 |
| Exact forward C22 cyclic-pair hit | 0 | 0 |

These key sets are deduplicated **within** each corpus. Their overlap
has not been measured, so their sum is not claimed as a union cardinality.

The compact journals preserve every parent edge and every candidate's
source node/rotation offsets, not just a successful-looking endpoint.
Words are regenerated from the parent operations, avoiding repeated
copies of long paths. They are standard gzip/base64 JSON:

| Journal | Decoded bytes | ASCII bytes |
|---|---:|---:|
| AK(2) side | 1,708,079 | 456,309 |
| Power/meridian side | 3,098,489 | 837,521 |

The independent replay reconstructs respectively **20,985** and **35,814**
actual candidate pairs. Their exact TSV SHA256 hashes are

    AK2:   c0d198a18924290743a35189f95fccd28c83b130be9457bae3488199bb637945
    power: 721c34938f5fc61d6c21960ddccaca7747c8c064acaaa14477cd94f5a0886346

As compact ordinary-move controls, a selected AK(2)-side candidate has a
**39-move** ledger with raw peak **29** and cyclic peak **23**. A selected
power/meridian-side candidate has a **32-move** ledger with the same
raw/cyclic peaks **29/23**. Thus the searches really use larger cyclic
excursions; they are not merely walks confined to the known cap-22
sublevel. Both exact endpoints are replayed independently.

## 3. Complete finite comparisons, without a global negative inference

Q's new `--match-pairs` mode computes every reverse key afresh, then
streams the specified forward rotation pairs. It does not need to store
the complete 11.4-million-key forward set. A positive output would record
both actual pairs, their original bases in the common labelled graph,
and the source/reverse indices needed for strict path reconstruction.

Each reverse corpus was compared with all three explicitly stated
forward datasets:

| Forward dataset | Source pairs | Rotation pairs per comparison | Outcome for each reverse corpus |
|---|---:|---:|---|
| Full certified C22 component | 258,032 | 24,136,172 | COMPLETE_NO_MATCH |
| Q's distance-two, energy-23 frontier | 5,264 | 510,048 | COMPLETE_NO_MATCH |
| Coordinating agent's selected outside elites | 763 | 160,479 | COMPLETE_NO_MATCH |

All six matching jobs are terminal. The second row is a particular
frontier, **not** the full cyclic cap-23 component. The third is a
heuristically selected word list, not a complete component; a future
positive on that row would require its actual AK(3) entry ledger before
it could prove the goal. The finite graph comparisons themselves need
only the displayed words.

The matches sought here are particular subgroup equalities. The Q/R
rotation theorem about **primitive absence** does not imply that these
finite comparisons cover every possible subgroup match with arbitrary
tails. No new numerical peak bound or AC invariant follows from the
negative outputs.

The methods did not produce an actual forward/reverse join. The data
therefore establish neither AC triviality nor nontriviality of AK(3).

## 4. Reproduce and inspect exact paths

Place all published scripts together in `experiments/`. Python tools
use the standard library; the walk and matcher require C++17. The source
includes Q's `rotation_subgroups.cpp` under its documented library guard.

```sh
python3 experiments/cyclic_catalogue_to_tsv.py \
  certificates/cyclic22_component_manifest.json /tmp/cyclic22.tsv
c++ -std=c++17 -O3 experiments/reverse_subgroup_walk.cpp -o /tmp/r_reverse
/tmp/r_reverse /tmp/cyclic22.tsv 918273 1000000 150000 48 50000 26 \
  /tmp/r_ak2 /tmp/r_ak2_path.json
/tmp/r_reverse /tmp/cyclic22.tsv 918274 2000000 200000 56 100000 30 \
  /tmp/r_power /tmp/r_power_path.json xxxYYYY xY
```

Runtime and heuristic counts can depend on the C++ random-distribution
implementation; the published journals fix the actual observed words
and edges independently of that issue. Regenerate matching inputs from
those exact journals:

```sh
python3 experiments/reverse_journal.py \
  certificates/r_reverse_ak2_journal.json.gz.b64 \
  --tsv-output /tmp/r_ak2.tsv --output /tmp/r_ak2_review.json
python3 experiments/reverse_journal.py \
  certificates/r_reverse_power_journal.json.gz.b64 \
  --tsv-output /tmp/r_power.tsv --output /tmp/r_power_review.json
c++ -std=c++17 -O3 experiments/rotation_subgroups.cpp -o /tmp/q_rotations
/tmp/q_rotations --match-pairs /tmp/r_ak2.tsv /tmp/cyclic22.tsv /tmp/r_match.json
```

Q's [frontier report](research-q-frontier.md) gives commands to reconstruct
the two other forward datasets. The combined saved six comparisons and
their input hashes are in `results/r_reverse_search_results.json` and
`results/r_reverse_provenance.json`.

Compile any chosen reverse candidate's actual ordinary ledger by adding
`--candidate-index N --certificate /tmp/r_candidate.json` to the journal
command. The published selected indices are 1190 and 5764 respectively.
Their exact certificates, the 51-move anchor, and the 11-move bridge
control can be replayed directly:

```sh
python3 experiments/elementary_verify.py \
  certificates/r_reverse_ak2_candidate.json \
  certificates/r_reverse_power_candidate.json \
  certificates/r_power_meridian_basis.json \
  certificates/r_h_basis_bridge_control.json
python3 experiments/h_basis_bridge.py \
  certificates/r_h_match_positive_control.json \
  --certificate /tmp/r_bridge.json --output /tmp/r_bridge_review.json
```

`pack_reverse_journal.py` reconstructs the compact journal from a new
walk's `.nodes.jsonl`, `.pairs.jsonl`, `.pairs.tsv` and `.results.json`
files. The published graph and strict-path checks are constructive
calibrations. None of the four requested breakthrough objectives has
been achieved.
