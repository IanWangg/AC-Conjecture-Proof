# Round 05 · Ordinary AK(3) trivialization

2026-11-19. Every ordinary AK(3) trivialization requires cyclic total relator length at least **29**. The cyclic cap-28 component has 8,694,374 signed ambient basis permutation orbits and 69,541,172 literal signed cyclic pairs. An independent closure and connectivity scan checks all 8,772,461,272 candidate products on the orbit graph. A separate Euclidean screen finds no primitive coordinate. The whole component has no subgroup join to the 23,902 known-trivial archive pairs through reverse energy 56. Ordinary AK(3) triviality remains open.

## Signed ambient symmetries in a bounded search

Let $D$ be the group of eight automorphisms of $F(x,y)$ that permute and invert the marked generators. Each automorphism preserves cyclic length, takes a signed cyclic pair to another such pair, and transports every geometric cyclic product to an edge of the same kind. For a product represented by rotations $u,v$ and relative bridge $q$, the transported representatives are the corresponding images of $u,v,q$. The free reduction rules and the required bridge bound are unchanged. [Full geometric menu](research-n-cyclic-search.md).

Build the orbit graph under $D$. A quotient path lifts starting at the original marked AK(3) cyclic pair. To lift the next edge, choose the automorphism sending its displayed source to the current lift and apply that automorphism to the edge. This operation chooses the signed rotations and relative bridge of the next *ordinary* move in the already marked free group. Being primitive is invariant under $D$. Consequently a primitive-free orbit component excludes every ordinary path to a displayed primitive under that cyclic cap.

All four distinct literal signed cyclic images of AK(3) under $D$ lie in its independently verified cap-22 component. For each cap at least 22, all representatives of any reached orbit are therefore reached literal cyclic pairs. Indeed, transport the path from the original seed to one orbit representative by any element of $D$ and precede it with a path to the transformed seed. This also justifies comparing the full cap-28 expansion to the reverse archive.

The packed implementation stores at most 29 letters in two-bit slots, with the shorter coordinate length and a leading sentinel. Word and pair codes are injective on the chosen representative formats. Each orbit key minimizes over the eight *simultaneous* relabelings of the pair after independently applying cyclic rotation and inversion, and after allowing row interchange. For the cap-22 control, all 32,363 compact keys agree with the literal catalogue under a separate string-based orbit comparison. The expanded and sorted control is byte-identical to all 258,032 literal rows. [Orbit generator](../experiments/round05_ak3_orbits.cpp), [independent orbit and primitive controls](../experiments/round05_ak3_orbit_audit.py).

## Full cap-28 closure and reverse joins

| Cap | Orbit nodes | Literal signed cyclic pairs | Candidate products checked on orbit nodes | Admitted products on orbit nodes |
| ---: | ---: | ---: | ---: | ---: |
| 22 | 32,363 | 258,032 | 24,220,040 | 1,283,644 |
| 28 | 8,694,374 | 69,541,172 | 8,772,461,272 | 486,305,648 |

The independent verifier reconstructs the orbit labels via an explicit relabeling table and string cyclic minima. It stack-reduces every candidate from independently enumerated signed rotations and reduced tails. Closure is checked by literal compact key lookup, and connectivity is checked by a disjoint-set forest using that cyclic product edges are reversible. Separately, the primitive audit examines every displayed coordinate. Of the 17,388,748 coordinate occurrences at cap 28, only 386,351 use at most one sign per generator. Exact primitive conjugacy tests reject every one of those occurrences. These tests identify ambient primitives via their relatively prime exponent vectors and signed cyclic representatives. [Independent verifier](../experiments/round05_ak3_orbit_verify.cpp), [Osborne and Zieschang](https://geodesic.mathdoc.fr/item/IM_1981__63_142788/).

| Forward component | Forward pairs | Reverse archive pairs | Reverse rotated cores | Relevant disjoint bridges | Basis lookup tests |
| --- | ---: | ---: | ---: | ---: | ---: |
| Cap 27 | 37,344,580 | 23,902 | 2,675,055 | 741,714 | 784,087 |
| Cap 28 | 69,541,172 | 23,902 | 2,675,055 | 1,065,680 | 1,093,967 |

The weighted intrinsic-basis index allows arbitrary independent conjugation tails on both sides. It tests whether conjugated pairs can generate conjugate subgroups, after which a Nielsen basis path would connect them. The computations therefore address a route that could pass above the cyclic cap after leaving a forward node. Both runs find zero such joins. [Index and completeness proof](round-04-ak3.md#indexing-short-bases-of-a-reverse-subgroup), [search receipts](../results/round05_ak3_searches.json).

## Short new AK(3) states and restricted continuation tests

The cap-26 catalogue is contained in cap 27. All eight lowest-energy new pairs have energy 16, and they form one signed ambient symmetry orbit. Their least entry peak is exactly 27. Two complete disjoint product balls of radii 7 and 32 give product distance at least 40 to the set in cap 27, and an edge joining the balls realizes 40. The compiler expands the route to 451 strict moves with cyclic peak 27 and raw peak 39. The exact endpoint is `(XXXyxYXXY, XYXYxyy)`. The signed orbit path program independently returns distance 40 and replays its own strict lift. [Strict certificate](../certificates/round05_ak3_energy16_escape.json).

For these eight pairs, all intersecting-axis initial conjugations yield 264 distinct cores. Each source core and all 24,464 two-copy joins pass the signed transition DAG test. In the disjoint-axis case, the symmetry orbit reduces the test to representative `(XXXYXXYxy, XYXyyxY)`. At least one and at most eight letters on the shortest bridge give 206,640 admissible placements and 50,063,304 two-copy joins. Every one of those core and join graphs also passes. Both tests therefore exclude an ambient primitive after arbitrary Nielsen changes and a second independent conjugation, with arbitrary final Nielsen changes, in the stated first-bridge scope. [Two-copy argument](round-02-ac-disproof.md), [cap-27 escape bridge tests](../results/round05_ak3_searches.json).

The cap-28 component supplies another eight energy-16 pairs and no additions below energy 16. They form one signed ambient symmetry orbit, with representative `(XXXYYxY, XXYxxyyxy)`. The quotient graph gives disjoint completed radii 7 and 43 and one joining product, establishing distance 51 to this orbit under cap 28. Each quotient product lifts in the original marked basis. The resulting 675 strict moves have cyclic peak 28 and raw peak 39. The rank-two pair `(XXyxYxyXYxyXYxY, XXyyxYY)` obtained by a rank-three primitive deletion in the [Stable AC proof track](round-05-stable-proof.md) is absent in both the compact and the full cap-28 catalogue. [Strict cap-28 escape certificate](../certificates/round05_ak3_energy16_escape28.json).

## Reproduce

Regenerate the literal [cap-26 catalogue](round-03-cyclic26.md) and the cap-27 catalogue with the same command at cap 27. Regenerate the [round-one archive](round-01-ak3.md#replay-of-the-september-2026-paths) at energy cap 56. The commands assume those TSVs and the independently checked cap-22 TSV are available with the hashes in the linked results. Running the entire cap-28 workflow requires a C++17 compiler and several GB of disk and memory. The compact cap-28 TSV is about 254 MB.

~~~sh
work=/tmp/ac-r05-ak3
c22=/tmp/round01-ak3/work/c22.tsv
c26=/tmp/ac-r03-cyclic/c26.tsv
c27=/tmp/ac-r04-cyclic/c27.tsv
reverse=/tmp/round02-ak3/reverse56.tsv
mkdir -p "$work"
c++ -std=c++17 -O3 -pthread experiments/round05_ak3_orbits.cpp -o "$work/orbits"
c++ -std=c++17 -O3 -pthread experiments/round05_ak3_orbit_verify.cpp -o "$work/orbit-verify"
c++ -std=c++17 -O3 -pthread experiments/round05_ak3_orbit_path.cpp -o "$work/orbit-path"
c++ -std=c++17 -O3 experiments/round04_ak3_basis_index.cpp -o "$work/basis-index"
c++ -std=c++17 -O3 experiments/round03_ak3_escape_path.cpp -o "$work/escape"
c++ -std=c++17 -O3 experiments/round03_ak3_two_copy_frontier.cpp -o "$work/frontier"
c++ -std=c++17 -O3 experiments/round04_ak3_disjoint.cpp -o "$work/disjoint"
"$work/orbits" 22 2 "$work/c22.orbit.tsv" "$work/c22.orbit.json"
"$work/orbit-verify" 22 2 "$work/c22.orbit.tsv" "$work/c22.verify.json"
python3 -B experiments/round05_ak3_orbit_audit.py compare "$c22" "$work/c22.orbit.tsv" > "$work/c22.compare.json"
python3 -B experiments/round05_ak3_orbit_audit.py seed "$c22" > "$work/c22.seed.json"
"$work/orbits" expand "$work/c22.orbit.tsv" "$work/c22.expanded.tsv"
LC_ALL=C sort "$work/c22.expanded.tsv" | cmp - "$c22"
"$work/orbits" 28 4 "$work/c28.orbit.tsv" "$work/c28.orbit.json"
"$work/orbit-verify" 28 5 "$work/c28.orbit.tsv" "$work/c28.verify.json"
python3 -B experiments/round05_ak3_orbit_audit.py primitive "$work/c28.orbit.tsv" > "$work/c28.primitive.json"
"$work/orbits" expand "$work/c28.orbit.tsv" "$work/c28.expanded.tsv" > "$work/c28.expanded.json"
"$work/basis-index" "$c27" "$reverse" "$work/basis-matches56.json"
"$work/basis-index" "$work/c28.expanded.tsv" "$reverse" "$work/c28.basis-matches56.json"
python3 -B experiments/round03_ak3_escape_catalogue.py "$c26" "$c27" "$work/diff"
python3 -B experiments/round05_ak3_orbit_audit.py partition "$work/diff/lowest.tsv" > "$work/lowest.partition.json"
"$work/escape" 27 "$work/diff/lowest.tsv" "$work/escape.json"
python3 -B experiments/round03_ak3_escape_replay.py "$work/escape.json" "$work/energy16.json" "$work/escape-replay.json"
cmp "$work/energy16.json" certificates/round05_ak3_energy16_escape.json
"$work/orbit-path" 27 XXXYXXYxy XYXyyxY "$work/escape27.orbit-control.json"
python3 -B experiments/round05_ak3_lift_orbit_path.py "$work/escape27.orbit-control.json" "$work/escape27.control-certificate.json" "$work/escape27.control-replay.json"
"$work/frontier" "$work/diff/lowest.tsv" rotations "$work/two-copy-hits.jsonl" "$work/two-copy.json"
"$work/disjoint" XXXYXXYxy XYXyyxY 1 8 "$work/disjoint-hits.jsonl" "$work/disjoint-counts.json"
awk 'length($0)<=17' "$c27" > "$work/c27.short.tsv"
awk 'length($0)<=17' "$work/c28.expanded.tsv" | LC_ALL=C sort > "$work/c28.short.tsv"
python3 -B experiments/round03_ak3_escape_catalogue.py "$work/c27.short.tsv" "$work/c28.short.tsv" "$work/diff28"
python3 -B experiments/round05_ak3_orbit_audit.py partition "$work/diff28/lowest.tsv" > "$work/lowest28.partition.json"
"$work/orbit-path" 28 XXXYYxY XXYxxyyxy "$work/escape28.orbit.json"
python3 -B experiments/round05_ak3_lift_orbit_path.py "$work/escape28.orbit.json" "$work/energy16-28.json" "$work/escape28.replay.json"
cmp "$work/energy16-28.json" certificates/round05_ak3_energy16_escape28.json
python3 -B experiments/round05_ak3_orbit_audit.py contains "$work/c28.orbit.tsv" XXyxYxyXYxyXYxY XXyyxYY > "$work/stable-projection28.json"
python3 -B experiments/round05_ak3_receipts.py "$work" "$c26" "$c27" "$reverse" "$work/energy16.json" "$work/energy16-28.json" \
  | diff - results/round05_ak3_searches.json
~~~
