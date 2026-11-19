# Round 03 · Ordinary AC trivialization of AK(3)

2026-11-19. Every ordinary AK(3)-reachable pair generates a malnormal subgroup of \(F(x,y)\). At cyclic cap 25 the lowest-energy new tuples have energy 17, and the minimum cyclic product distance to any of those tuples is exactly 22. A strict 284-move certificate realizes one endpoint. The phase and join searches below found no free-group trivialization.

## Malnormality of a rank-two core with unimodular homology

**Proposition.** Let \(H\) be a rank-two subgroup of a finite-rank free group \(F\). Suppose the inclusion on integral \(H_1\) is injective with saturated image. Then \(H\) is malnormal in \(F\).

**Proof.** Let \(\Gamma\) be the finite unbased core of \(H\), immersed in the basis rose of \(F\). If \(H\) is not malnormal, the off-diagonal self-fiber product of \(\Gamma\) has a circuit. Hence some cyclically reduced word labels loops at two distinct core vertices. Replace this word by its root-free cyclic root \(w\). In the pullback of the word circle for \(w\) to \(\Gamma\), the circular components then have total degree at least two over the word circle. This covers both the case of separate circular components and the case of two points over the same position in one circular component. [Kapovich and Myasnikov, *Stallings foldings and subgroups of free groups*](https://arxiv.org/abs/math/0202285).

The Louder–Wilton W-cycles theorem applies to the root-free loop for \(w\). Because \(-\chi(\Gamma)=1\), some unoriented edge \(e\) of \(\Gamma\) is traversed at most once in total by the circular components. [Louder and Wilton, Theorem 2](https://doi.org/10.4153/CMB-2016-078-3).

If \(e\) is used once, the corresponding component traces a closed path crossing a nonseparating edge exactly once. Choose a spanning tree omitting \(e\). In its free basis the path has one occurrence of the basis letter for \(e\), so it is a primitive element of \(H\). Its homology is primitive in \(H_1(H;\mathbb Z)\), and saturation and injectivity make its ambient homology primitive as well. A component of degree \(k\) has ambient homology \(k[w]\), so \(k=1\). Any other circular component has \(H\)-homology proportional to this one's by injectivity of \(H_1(H)\to H_1(F)\), but has zero coefficient on \(e\). In a graph, homology classes are the integral cycle chains themselves. The first component has coefficient \(\pm1\) on \(e\), so there is no second component. This contradicts total degree at least two.

If \(e\) is unused, remove it. When \(e\) is nonseparating, the remaining graph has a single rank-one core. When \(e\) separates, each side has rank one, since the original graph has rank two and no leaves. A rank-one core on either side is a single simple cycle. Its homology is primitive in \(H\) and thus in \(F\), so its label is root-free. Its circular pullback with the word \(w\) has degree at most one: the two cyclic root words must agree in one orientation, and a second alignment in that orientation would imply a nontrivial period. The opposite orientation cannot also occur, since the cycle has nonzero ambient homology. The two sides in the separating case cannot both carry \(w\), because their cycle classes are independent in \(H_1(H)\) and remain independent in \(H_1(F)\). In either case the total degree is at most one, again a contradiction. This proves malnormality. \(\square\)

For a normally generating pair in \(F(x,y)\), the two exponent columns form an integral basis of \(\mathbb Z^2\). Its subgroup has rank two. Since the pair generates the subgroup, the integral map on its abelianization is an isomorphism onto \(\mathbb Z^2\). All ordinary AC descendants satisfy the same hypothesis, independent of length and order of moves. This supplies the off-diagonal forest premise of the round-two barbell comparison for every actual AK(3) source core. The graph test in this round separately confirmed it on all 5,562,224 *displayed* cap-25 tuples. [Round 02 comparison](round-02-ak3.md#arbitrary-target-conjugation-tails).

## A sharp low-energy escape at cyclic cap 25

Merging the full sorted cap-24 and cap-25 catalogues confirms inclusion and counts the difference. There are no new tuples through energy 16, and there are exactly 56 energy-17 pairs in the difference. Every one of those 56 pairs requires cyclic entry peak exactly 25, since its pair is reachable with cap 25 and absent under cap 24. [Previous cap 24](round-01-ak3.md), [complete cap 25](round-02-cyclic25.md).

A second search uses the complete geometric cyclic multiplication menu with cap 25. Its vertices are unordered signed cyclic pairs. Each edge is one signed right product, with independent conjugations, inversions and an unordered choice of row slots allowed in choosing representatives. In particular an edge can be reversed under the same cap. From the original class and from the set of all 56 targets, the search expands complete breadth-first layers on one side at a time. Two disjoint completed balls of radii 8 and 13 exclude every path of length at most 21. The next layer hits, and the separate compiler expands the resulting 22-product path to 284 strict ordinary moves with cyclic peak 25 and raw peak 35. The endpoint is

~~~text
XXYXYxyXY    XYYXyyxY
~~~

The shortest statement concerns the number of cyclic product edges **within cap 25**. The strict length 284 comes from the compiled certificate. The two radius counts, 396,351,188 products inspected and every boundary receipt are saved. [Strict certificate](../certificates/round03_ak3_energy17_escape.json), [round results](../results/round03_ak3_frontier.json).

## Two-copy screens

For each core \(\Gamma\), fold two rebased copies at every pair of distinct vertices as in round two. The resulting finite subgroup contains the output of intersecting-axis second-phase pairs at those two vertices. The source core itself covers the identical-vertex case, and disjoint second axes have the separate barbell primitive exclusion. The signed double-free cycle test handles most cases. Each exception is resolved by exact partial-map primitive detection with no state cutoff. [Two-copy argument](round-02-ac-disproof.md), [exact primitive-loop decision](research-r.md).

| Source family | Distinct source cores | Distinct-vertex joins | Exact decisions after the DAG test |
| --- | ---: | ---: | ---: |
| All 3,675 displayed AK(3) archive cyclic pairs | 3,615 | 5,394,613 | 232 |
| All independent rotations of the 56 energy-17 escapes | 1,976 | 209,056 | 80 |
| 1,048 stratified literal cap-25 escapes | 1,048 | 155,999 | 6,669 |

Every test, including the source core test, excludes ambient primitives. For the 56 two-word classes the rotations cover all intersecting-axis preliminary choices. The screen on these 56 does not include preliminary choices with disjoint axes. The archive and stratified rows in the other two runs use only the displayed cores. The sample is obtained by deterministic per-energy reservoir sampling of the catalogue difference.

## Reverse joins and finite bridge maps

Three exact waypoints from the new route were each compared against the 9,257 known-trivial reverse pairs through energy 32. The round-two fiber solver found no match in 3,352,422 intersecting-axis comparisons. Its only rank-two cases had the full ambient group as the reverse subgroup, while all three forward cores pass the signed-DAG primitive exclusion. All proper target products have at most one cyclic component. [Reverse catalogue and basis-join criterion](round-02-ak3.md).

For the disjoint-axis branch, a complete lift of a bridge word \(q\) to a forward core gives a source vertex and its image. Once the lobe-product components are contracted, the contribution of the bridges to the cycle rank depends only on this partial transition map. The admissible attachment positions depend on the first and last letters of \(q\). Thus it suffices to enumerate states consisting of the partial map and those boundary letters. Start with a signed generator and repeatedly append a letter different from the inverse of the current last letter. A map defined at fewer than two vertices can be dropped, since further letters cannot enlarge its domain. The other maps are finite in number for a finite core. If the lobe products have intrinsic cycle rank at most one, all dropped bridges are covered, and the enumeration computes the total cycle rank for all multi-lift bridge types. This rank test also works on nonmalnormal cores. A rank of at least two is a candidate that still requires a basis-join test.

For the three actual waypoints there are 38, 36 and 54 multi-lift states respectively, with 35,594,855 allowable state and attachment combinations in total. Every configuration has cycle rank at most one. There is no target with two intrinsic lobe cycles. Together with the intersecting-axis test this excludes a join in the tested scope with arbitrary Nielsen basis changes on both sides and arbitrary preliminary conjugating tails on the reverse side. The forward sides are the three specified cores.

As a nonmalnormal rank test control, take the source \(\langle x^2,y\rangle\) and target lobes \(y,y^{-1}\). Each \(x^{2m}\), \(m\ge 1\), has the same partial identity map, while the source has a cyclic off-diagonal product. The finite map scan gives four states and four rank-at-least-two cases. This is a rank-filter control, not a basis-join certificate. The prior round's actual basis-join positive control independently replays in 22 strict moves. [Positive basis-join certificate](../certificates/round02_ak3_fiber_control.json).

## Reproduce

Use the cap-24 and cap-25 catalogues from the linked component reports. Regenerate the round-one forward and reverse archive catalogues with cap 210, which retains all 3,675 cyclic forward pairs. Filter its reverse TSV at energy 32. The temporary paths below refer to those regenerated inputs.

~~~sh
work=/tmp/ac-r03-track1
mkdir -p "$work"
c++ -std=c++17 -O3 experiments/round03_ak3_escape_path.cpp -o "$work/escape"
c++ -std=c++17 -O3 experiments/round03_ak3_two_copy_frontier.cpp -o "$work/frontier"
c++ -std=c++17 -O3 experiments/round03_ak3_bridge_maps.cpp -o "$work/bridge-maps"
c++ -std=c++17 -O3 experiments/round02_ak3_fiber_join.cpp -o "$work/fiber"
python3 -B experiments/round03_ak3_escape_catalogue.py /tmp/ac-r01-output/c24.tsv \
  /tmp/ac-r02-component/c25.tsv "$work"
"$work/escape" 25 "$work/lowest.tsv" "$work/escape.json"
python3 -B experiments/round03_ak3_escape_replay.py "$work/escape.json" \
  "$work/energy17_escape.json" "$work/escape_replay.json"
diff certificates/round03_ak3_energy17_escape.json "$work/energy17_escape.json"
"$work/frontier" /tmp/ac-r01-output/forward.tsv literal "$work/archive_hits.jsonl" "$work/archive_scan.json"
"$work/frontier" "$work/lowest.tsv" rotations "$work/lowest_hits.jsonl" "$work/lowest_scan.json"
"$work/frontier" "$work/sample.tsv" literal "$work/sample_hits.jsonl" "$work/sample_scan.json"
"$work/bridge-maps" audit /tmp/ac-r02-component/c25.tsv "$work/malnormal_cap25.json"
python3 -B - "$work" /tmp/ac-r01-output <<'PY'
import json, sys
from pathlib import Path
work, archive = map(Path, sys.argv[1:])
route = json.loads((work / "escape.json").read_text())["route"]
(work / "escape_sources.tsv").write_text("".join("\t".join(route[i]) + "\n" for i in (-1, -2, -6)))
(work / "reverse32.tsv").write_text("".join(row for row in (archive / "reverse.tsv").read_text().splitlines(keepends=True) if len(row) - 2 <= 32))
PY
"$work/bridge-maps" scan "$work/escape_sources.tsv" "$work/reverse32.tsv" "$work/map_results.json"
"$work/fiber" "$work/escape_sources.tsv" "$work/reverse32.tsv" rotations "$work/route_fiber.json"
printf 'xx\ty\n' > "$work/barbell_control_source.tsv"
printf 'y\tY\n' > "$work/barbell_control_target.tsv"
"$work/bridge-maps" scan "$work/barbell_control_source.tsv" "$work/barbell_control_target.tsv" "$work/map_control.json"
"$work/bridge-maps" audit "$work/barbell_control_source.tsv" "$work/malnormal_control.json"
python3 -B experiments/elementary_verify.py certificates/round02_ak3_fiber_control.json
~~~
