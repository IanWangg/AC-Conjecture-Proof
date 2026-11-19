# Round 01 · Ordinary AC trivialization of AK(3)

The 34 published Lisitsa–Vernitski equivalence paths to AK(3) supply
3,675 distinct cyclic waypoint pairs. I found two length-20 waypoints
outside this repository's complete cyclic cap-22 component. I also
developed a finite test for ordinary AC joins through independently
conjugated subgroups. Applying it to the archive waypoints through
cyclic energy 32 and to the full cap-22 component found zero joins with
9,257 known-trivial cyclic pairs. The new complete cyclic cap-24 audit
proves that reaching a primitive coordinate requires cyclic peak at
least 25. AK(3) remains unresolved in this round.

## Replay of the September 2026 paths

The two archives contain both human-readable intermediate states and
integer-encoded moves. The replay checks the move type and every
intermediate state against the printed ledger. It accepts inversions,
word conjugations, left or right multiplication, and swaps. Every one of
these operations expands to the repo's strict ordinary moves. For
example, the swap of `(a,b)` follows
`(a,b) → (ab,b) → (ab,a⁻¹) → (b,a⁻¹) → (b,a)`, with the negative and
left multiplications expanded into inversions and right multiplications.
The two strict sample certificates are replayed independently.

| Archive | Paths | Documented moves | Verified destination |
|---|---:|---:|---|
| Equivalences to AK(3) | 34 | 193,604 | Exactly `(xxxYYYY, xyxYXY)` |
| Pure AC trivializations | 640 | 443,569 | Standard basis up to sign and order |

All 674 ledgers and 637,173 moves pass. There is zero overlap in the
benchmark IDs, exact starting tuples, exact states or signed cyclic
keys between the two corpora. The 34 AK(3) paths contain 24,420 distinct
actual tuples and 3,675 distinct signed cyclic pairs, where normalization
allows a swap, inversion and independent cyclic conjugation of
coordinates. The published macro-boundary raw peaks range from 205
to 221. Their cyclic peaks range from 203 to 207.
[Lisitsa–Vernitski data and method](https://doi.org/10.5281/zenodo.23061803)

The archive gives 1,281 distinct AK(3) pairs of cyclic energy at most
32. Of the 574 pairs of cyclic energy at most 22, 572 belong to the
audited cap-22 component. The two shorter excursions are
`(XXyXYYYxxYxyy, XYxYYxY)` and
`(XXyyxYxyxYYXy, XYxYYxY)`, at steps 414 and 441 respectively in
`n3row36_toAK3_moves.txt`. They are ordinary AC-equivalent to AK(3)
through paths that exceed cyclic energy 22. New strict paths reach them
in 263 and 308 elementary moves, with raw peaks 27 and 29 and cyclic
peak 23 in both cases. Cap-22 closure gives the matching lower bound, so
their minimum cyclic entry peak is exactly 23. The first path reaches
the pair with its coordinates reversed. A compact exemplar reverses the
last 24 macro moves of another archive path to reach
`(xxYYYXYXXyxyxxxxxYYYXYXy, XYXYxxyxyyyXX)` in 71 strict moves,
with raw and cyclic energy 37 at the endpoint. The known-trivial archive
control replays in 24 strict moves to exactly `(x,y)`.
[Cap-22 closure proof](research-n-cyclic-search.md) ·
[Step-414 waypoint](../certificates/round01_ak3_energy20_414.json) ·
[Step-441 waypoint](../certificates/round01_ak3_energy20_441.json) ·
[AK(3) strict waypoint](../certificates/round01_ak3_archive_waypoint.json) ·
[Known-trivial strict control](../certificates/round01_ak3_archive_control.json)

Gaur's November preprint independently reports a raw total-length
cap-25 exhaustion for AK(3). This report uses cyclic energy, which is
unchanged by the conjugations represented inside our subgroup tests.
[November 2026 preprint](https://zenodo.org/records/24035724) ·
[Computation repository](https://github.com/pragyaangaur/Andrews-Curtis-Conjecture)

## Exact subgroup matching for a single independent conjugation phase on each side

Take two finite catalogues of rank-two free relator pairs. The question
is whether some pair from each catalogue can undergo arbitrary
independent coordinate conjugations and then generate globally
conjugate subgroups of the ambient free group. The tested presentation
pairs normally generate the ambient group, so their exponent matrix
remains unimodular and the independently conjugated subgroup still
has rank two. A positive match suffices for an ordinary AC join.
Both pairs are bases of their rank-two subgroups. After a single global
conjugation, a Nielsen basis change connects them. Previously verified
strict path and basis-bridge compilers provide the required expansions.
[Repository's earlier constructive subgroup bridge](research-r-reverse.md)

For any nonempty cyclic words `u,v`, consider the translation axes of
the chosen conjugates in the Cayley tree. If the axes meet, rebase at
an intersection vertex. The two words become cyclic rotations of
`u,v`, and folding their two circles gives their unbased labelled
core graph. Every such rotation pair is itself allowed.
Signs of the two generators can be discarded at the subgroup level.
[Earlier Cayley-tree reduction](research-q.md)

If the axes are disjoint, rebase at the endpoint of their unique
shortest bridge on the first axis. The generators become
`u', q v' q⁻¹` with `q` the nonempty bridge. At each end, the bridge
uses a direction distinct from either incident axis direction. A
labelled circle for `u'` and a labelled circle for `v'` attached by
that bridge therefore already form a folded rank-two core. Its two
lobes are distinguished by the graph topology, and their cyclic labels
are the starting pair up to rotation, sign and order. Conversely, for
any such folded graph the two oriented lobe words based at the first
branch vertex, using the bridge as a conjugator for the second,
generate its fundamental group. This realizes a disjoint-axis
representative of the lobe key. This argument also covers cyclic words
that are proper powers.
[Stallings core and conjugacy constructions](https://web.stevens.edu/algebraic/alexeim/Teaching/GroupTheory626/graph5.pdf)

This gives a finite exact decision procedure for the specified join.
Two intersecting-axis representatives match when their canonical
unbased labelled graphs match. An intersecting-axis representative
matches a disjoint-axis representative exactly when the former graph
has two lobes joined by a bridge and the lobe pair equals the other
catalogue's cyclic key. Two disjoint-axis representatives can match
only when their starting cyclic keys agree. In that event one can
already join by sign, order and conjugations. No enumeration of bridge
lengths is required. The implementation has a positive control for
each of these cases, including both directions of the mixed case.
For the mixed control, strict moves starting at `(x,y)` reach
`(x,yxyXY)` and then `(xyxyXY,yxyXY)`. An independent Stallings
fold confirms that the native match witnesses have the required
labelled graph. The AK(3) versus standard-basis control returns no match.

| AK(3) side | Cyclic pairs | Rotation folds | Known-trivial cyclic pairs | Reverse rotation folds | Matches |
|---|---:|---:|---:|---:|---:|
| Archive through cyclic energy 32 | 1,281 | 155,216 | 9,257 | 1,117,474 | 0 |
| Full cap-22 component | 258,032 | 24,136,172 | 9,257 | 1,117,474 | 0 |

The test exhausts this particular kind of join between the listed
states. It leaves paths that mix coordinates and conjugate them again
before reaching a matching subgroup.

## Primitive screen

For the 1,281 AK(3) archive waypoint pairs through cyclic energy 32,
the complete rotation scan yields 71,753 distinct unbased labelled
cores. The signed-DAG criterion excludes ambient primitives in 71,724
cores directly. The independent native fold and finite-map detector
return `ABSENT` for all 29 exceptions, and the Python certificate
checker verifies all 3,036 closed map-pair states. The disjoint-axis
case is also excluded by the earlier barbell argument. A cyclic
primitive uses at most one sign of each ambient generator. Crossing a
bridge forces both signs of its edge, while staying in a lobe reads a power
of one coordinate, which is already excluded by the rotation scan.
Thus none of these waypoint pairs yields a primitive after one
arbitrary independent conjugation phase followed by any Nielsen suffix.
[Primitive-in-subgroup proof and detector](research-r.md) ·
[Independent implementation](research-u.md)

## Complete cyclic cap-23 and cap-24 components

The Cayley-tree edge lemma bounds a nonempty shortest relative bridge of
length `d` by `a + 2b + 2d ≤ C`, where `a` is the current recipient
cyclic length, `b` the donor length and `C` the cyclic energy cap.
We enumerate signed rotations for intersecting axes and every reduced
relative bridge admitted by this bound for disjoint axes. Thus the
quotient graph captures all ordinary paths under the cyclic cap,
including paths with arbitrarily long actual relator tails.
[Geometric completeness proof](research-n-cyclic-search.md)

The accelerated generator reduces a product of two cyclically reduced
words by canceling across the two seams before normalizing the cyclic
key. If a seam removes one factor entirely, it cyclically reduces the
surviving fragment. It checks this computation against the reference
reducer on all cyclically reduced input pairs through length five.
The independent closure program performs stack reduction and verifies
every edge in the complete menu and reachability from AK(3). It
computes the signed cyclic representative only after the cyclically
reduced product passes the length cap. The original checker and this
version use the same candidate set, cap test and canonicalizer.

| Cyclic cap | States | Candidate products | Nonempty bridge checks | Distinct cyclic coordinates | Primitive coordinates |
|---:|---:|---:|---:|---:|---:|
| 23 | 891,748 | 726,524,736 | 440,960 | 674,322 | 0 |
| 24 | 1,596,072 | 1,339,662,272 | 1,037,696 | 1,234,376 | 0 |

The independent Euclidean scan checks every displayed cyclic
relator class through the cap. The minimum cyclic total length is 13
and the minimum individual cyclic length is 5. Every ordinary path
from AK(3) to a primitive coordinate must reach cyclic energy **25**
or higher. This also applies to a full ordinary AC trivialization.
[Hashes and audit results](../results/round01_ak3_cyclic_components.json)

## Reproduce

Run from the repository root. The download archives stay outside the
repository. The saved result records both SHA-256 hashes and the
catalogue hashes. The two strict controls replay without downloads.

```sh
mkdir -p /tmp/ac-r01-archives /tmp/ac-r01-output
curl -fL https://zenodo.org/records/23061803/files/ak3_certificates.zip \
  -o /tmp/ac-r01-archives/ak3_certificates.zip
curl -fL https://zenodo.org/records/23061803/files/640_simplification_paths.zip \
  -o /tmp/ac-r01-archives/640_simplification_paths.zip
python3 experiments/round01_ak3_archive.py /tmp/ac-r01-archives /tmp/ac-r01-output \
  --certificate /tmp/ac-r01-output/waypoint.json \
  --control-certificate /tmp/ac-r01-output/control.json
python3 experiments/elementary_verify.py /tmp/ac-r01-output/waypoint.json \
  /tmp/ac-r01-output/control.json
python3 experiments/cyclic_catalogue_to_tsv.py certificates/cyclic22_component_manifest.json \
  /tmp/ac-r01-output/c22.tsv
c++ -std=c++17 -O3 experiments/round01_ak3_all_tails.cpp -o /tmp/ac-r01-output/join
/tmp/ac-r01-output/join /tmp/ac-r01-output/forward.tsv /tmp/ac-r01-output/reverse.tsv \
  /tmp/ac-r01-output/all_tails.json
/tmp/ac-r01-output/join /tmp/ac-r01-output/reverse.tsv /tmp/ac-r01-output/c22.tsv \
  /tmp/ac-r01-output/c22_all_tails.json
c++ -std=c++17 -O3 experiments/rotation_subgroups.cpp -o /tmp/ac-r01-output/rotations
/tmp/ac-r01-output/rotations /tmp/ac-r01-output/forward.tsv \
  /tmp/ac-r01-output/dag_candidates.jsonl /tmp/ac-r01-output/dag_summary.json
python3 experiments/u_candidate_adapter.py /tmp/ac-r01-output/dag_candidates.jsonl \
  /tmp/ac-r01-output/map_candidates.tsv
c++ -std=c++17 -O3 experiments/u_native_primitive.cpp -o /tmp/ac-r01-output/maps
/tmp/ac-r01-output/maps /tmp/ac-r01-output/map_candidates.tsv \
  /tmp/ac-r01-output/map_results.jsonl 0 1
python3 experiments/round01_ak3_controls.py /tmp/ac-r01-output /tmp/ac-r01-output/join \
  --output /tmp/ac-r01-output/archive-audit.json
diff results/round01_ak3_archive.json /tmp/ac-r01-output/archive-audit.json
```

The component reproduction regenerates the exact catalogue and then
independently checks closure, connectedness and primitive coordinates.

```sh
c++ -std=c++17 -O3 experiments/round01_ak3_cyclic_component.cpp -o /tmp/ac-r01-output/build
c++ -std=c++17 -O3 experiments/verify_full_cyclic_component.cpp -o /tmp/ac-r01-output/check
for cap in 23 24; do
  /tmp/ac-r01-output/build "$cap" "/tmp/ac-r01-output/c$cap.json" \
    "/tmp/ac-r01-output/c${cap}_build.json"
  python3 experiments/cyclic_catalogue_to_tsv.py "/tmp/ac-r01-output/c$cap.json" \
    "/tmp/ac-r01-output/c$cap.tsv"
  /tmp/ac-r01-output/check "/tmp/ac-r01-output/c$cap.tsv" "$cap" \
    "/tmp/ac-r01-output/c${cap}_verify.json"
  python3 experiments/euclidean_primitive_audit.py "/tmp/ac-r01-output/c$cap.json" \
    --output "/tmp/ac-r01-output/c${cap}_prim.json"
done
python3 experiments/round01_ak3_component_report.py /tmp/ac-r01-output 23 24 \
  --output /tmp/ac-r01-output/cyclic-components.json
diff results/round01_ak3_cyclic_components.json /tmp/ac-r01-output/cyclic-components.json
python3 experiments/elementary_verify.py certificates/round01_ak3_energy20_414.json \
  certificates/round01_ak3_energy20_441.json
```

The two length-20 pairs supplied exact exterior inputs for this round's
disproof team's arbitrary-Nielsen, then-conjugation successor checks.
The remaining 707 sampled pairs at cyclic energy 23–32 provide
ordinary entry provenance for a later alternating-phase search.
[Disproof team's checked successor exclusions](round-01-ac-disproof.md)
