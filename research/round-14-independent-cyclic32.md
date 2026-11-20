# Independent ordinary cyclic cap-32 closure

2026-11-19. The complete ordinary AK(3) cyclic cap-32 component is now independently verified. It has **539,705,143 signed orbits**, including **285,484,620** that first enter at that cap. It contains no primitive coordinate. The ordinary cyclic peak lower bound is **33**. [Independent checks and combined receipt](../results/round14_cyclic32_independent.json).

The first-exit audit independently compared the entire product menu at every cap-31 source and reproduced 1,073,329,989 anchored records byte for byte. The cap-31 component had already passed its own closure, connectivity and primitive screens. The new independent outside verifier recomputed each outgoing product from all the appended nodes with stack reduction, checked membership in the combined set, and verified that every appended node connects to the verified lower component. It checked **328,010,482,664** product candidates and **12,567,099,338** admitted products. These exactly match the native generator. The independent Euclidean scan checked every new row, with zero primitives among its 101,668,360 sign-pure coordinate occurrences. [Boundary audit](round-12-primitive-step.md), [earlier cap-31 verification](round-10-independent-closures.md), [generation](round-11-cyclic32.md).

The cyclic Cayley-tree product theorem accounts for rotations and arbitrary conjugating tails. These coverage checks therefore apply to the signed cyclic orbit of every tuple on any ordinary path whose cyclic peak never exceeds 32. A path to the basis must expose a primitive coordinate, so no such path can stay under this cap. [Cyclic product theorem](research-n-cyclic-search.md).

## Exact first-exit deduplication at cap 33

The completed cap-33 first-exit generation has 4,298,727,756 anchored records. Partitioning the records by a fixed hash of their child, sorting each of the 128 shards, and retaining the least parent for each child gives **1,258,633,777 distinct seeds**. All input records passed the length-scope check. A cap-22 control gave identical sorted child-parent pairs to an independent in-memory dictionary, including when the input was repeated twice. Each cap-33 shard file has exactly the recorded number of 32-byte rows. [Complete record counts and controls](../results/round14_cap33_compacted_boundary.json), [compactor](../experiments/round14_ak3_boundary_compact.cpp).

The new expansion mode uses fixed-size open-addressed sets with exact full pair keys and mixes the entire packed pair hash before assigning a slot. The code checks table load before accepting a new key and uses the existing full cyclic product menu. A manifest accepts the lower cap-31 and cap-32 addition files directly. The flat reader requires distinct compacted seeds and retrieves their anchors from the existing shards, saving the storage for one in-memory parent per seed. The cap-22 flat-table control closes with the same 14,245 outside orbits as the earlier generator, in a byte-identical sorted catalogue. An undersized table or duplicate compact seed fails with a precise error. The full cap-33 expansion from the compacted seeds is active. [Expanded native mode](../experiments/round10_ak3_frontier.cpp), [control receipt](../results/round14_cap33_compacted_boundary.json).

~~~sh
mkdir -p "$work"
c++ -std=c++17 -O3 -pthread experiments/round07_ak3_wide_verify.cpp -o "$work/verify"
"$work/verify" --extend 32 16 "$cap31" "$outside32" "$work/c32.independent.json"
c++ -std=c++17 -O3 -pthread experiments/round14_ak3_boundary_compact.cpp -o "$work/compact"
c++ -std=c++17 -O3 -pthread experiments/round10_ak3_frontier.cpp -o "$work/frontier"
"$work/compact" 33 8 "$work/boundary33" 128 "$boundary_from31" "$boundary_from32"
printf '%s\n' "$cap31" "$outside32" > "$work/lower32.txt"
"$work/frontier" expand-flat 33 14 "@$work/lower32.txt" "$work/c33" 0 30 31 "$work"/boundary33/unique.*.bin
~~~
