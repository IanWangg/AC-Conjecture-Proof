# Round 10 · Exact boundary search at cyclic cap 32

2026-11-19. An incremental search now extends an exact cyclic catalogue by one energy unit and preserves the old-orbit anchor of every new branch. Three controls recover the exact differences between complete lower-cap catalogues. A separate search from the marked energy-17 pair produces a strict 875-instruction ordinary path to a new energy-31 pair with sharp ordinary cyclic entry peak **32**. The local search found no primitive coordinate. The full cap-32 expansion remains open. [Incremental controls](../results/round10_ak3_frontier.json), [marked cap-32 certificate](../certificates/round10_ak3_e17_cap32.json).

## Exact boundary and expansion

Let $C_h$ be the bounded AK(3) component at cyclic energy at most $h$. From a state of $C_{h-1}$, an edge leaving that component in $C_h$ must land at exactly energy $h$. Generate all these boundary edges and retain one actual old-orbit parent for each new seed. Then expand all seeds using the full bounded product menu, leaving out states already in $C_{h-1}$. A path can enter the old component again, but the first edge at each later exit is already in the same boundary menu. If the old component and the boundary scan are complete and the queue closes, the resulting new states are exactly $C_h\setminus C_{h-1}$. [Cyclic product completeness](research-n-cyclic-search.md).

For recipient length $n$ and donor length $m$, a cyclic product with a connecting word of length $d$ has energy congruent to $n$ modulo two. This rejects a recipient orientation immediately when its parity differs from $h$. Inverting the whole product and cyclically rotating gives the same orbit using the inverse recipient and inverse donor. It suffices to use every cyclic rotation of one receiver orientation and both donor orientations. For the zero-bridge case, skip $n+2m<h$. Otherwise compare two-bit packed rotations to count the two seams by their longest common prefixes, finish trimming any surviving single word, and keep exactly the required length $h-m$. For a positive shortest bridge, the four seams have no cancellation and force $d=(h-n-2m)/2>0$. Check all reduced bridges of precisely that length with the admissible endpoint directions. [Incremental generator](../experiments/round10_ak3_frontier.cpp).

The boundary command streams old rows in batches and writes native four-word binary records containing the destination and its actual old parent. Each checkpoint gives the number of whole records and the first unread byte of the old catalogue. A resumed command takes that byte offset and writes a second segment. The expansion command deduplicates these records together and preserves a parent for every new state it discovers. Its closure field is relative to the supplied segments. Completeness requires that the input catalogue and its scanned byte ranges cover the entire lower component. The binary records stay in scratch storage.

The cap-32 boundary run finished all **254,220,523** old rows. It checked 60,161,897,580 zero-bridge rotation pairs and 228,249,632 positive-bridge candidates. From the 3,509,580,702 admitted candidate occurrences it wrote **1,073,329,989** anchored records, deduplicated within batches. None contains a primitive coordinate. The binary file has exactly 34,346,559,648 bytes. The first-exit calculation uses the independently verified cap-31 catalogue. Deduplication across the full boundary and expansion past its first edge are in progress. [Complete boundary receipt](../results/round10_ak3_frontier.json), [completed cap-31 audit](round-10-independent-closures.md).

An additional sample of 16,384 cap-31 rows, selected by reproducible byte offsets across the full catalogue, gives complete row-by-row agreement with the reference boundary product menu at cap 32. This check includes 14,112 positive-bridge candidates. The full row-by-row boundary audit is in progress. The expansion has already loaded all records and deduplicated them to 281,402,118 initial boundary seeds. [Reference-boundary sample and full generation receipt](../results/round10_ak3_frontier.json).

## Complete controls

| Extension | Old orbits | Boundary seeds | All new orbits | Complete union |
| --- | ---: | ---: | ---: | ---: |
| 20 to 21 | 5,020 | 10,796 | 13,098 | 18,118 |
| 21 to 22 | 18,118 | 13,164 | 14,245 | 32,363 |
| 22 to 23 | 32,363 | 72,863 | 79,308 | 111,671 |

Every old source in these tests has its exact boundary independently recomputed by the existing string-based cyclic product menu. The completed expansions agree with independent comparisons of entire catalogue sets. The cap-21 run also produces byte-identical final output when its input is split into two byte-offset segments. The Python audit checks the predecessor order for all **106,651** new states and strictly replays 24 sampled edges per extension and each minimum-energy anchored route. A separate two-relator positive control starts with no primitive row and detects a length-seven primitive in a boundary state of energy 14. Its single cyclic product expands to a verified 22-instruction ordinary path. [Independent comparison and replays](../experiments/round10_ak3_frontier_audit.py), [complete receipts](../results/round10_ak3_frontier.json).

## A sharp cap-32 entry from the marked energy-17 pair

Begin with `(xxyXYXy, xxYXYxYYXY)` at the end of the [702-instruction round-nine ledger](round-09-cyclic31.md). The exact one-source boundary menu gives 3,780 seeds. Expand 600,000 frontier orbits using the 135,156 known cap-31 states through energy 23 as the omitted lower set. This is a selected partial search from the marked pair. It discovers 777,475 orbits and checks 812,787,144 product candidates. Comparing the discovered keys with all 254,220,523 rows of the full cap-31 catalogue leaves 67 new orbits of energy 31 and 397,734 of energy 32. There is no primitive in the discovered set and no new orbit through energy 30. [Exact local membership and replay receipt](../results/round10_ak3_e17_frontier.json).

Six cyclic products from the energy-17 anchor reach the new marked endpoint `(XXYxyxY, XXXYXYxxxYYXYxxYxxyxyXXY)`. The independently replayed suffix takes 173 elementary instructions, giving 875 from the original AK(3) presentation with raw peak 41 and cyclic peak 32. Its signed orbit is absent from the independently verified cap-31 catalogue, establishing the sharp entry peak. Joint Whitehead minimization of the 67 external energy-31 orbits gives 67 distinct minima, all with planar-link parity obstructions. All 67 exact marked orbits also fail the all-tail reverse subgroup join test against 23,902 archived trivial pairs. [Cap-31 catalogue audit](round-10-independent-closures.md), [marking-preserving compiler](../experiments/round10_ak3_e17_frontier.py), [geometry and reverse-archive receipts](../results/round10_ak3_e17_frontier.json).

A second local continuation alternates the quotient-conjugacy moves from the same marked pair. The search visits 799 marked continuation states in 752 signed orbits, with 236 absent from cap 31. Its primitive test finds none in the last completed finite graphs of the inspected charts. Five such updates reach the chosen external energy-31 endpoint in 1,588 ordinary instructions from AK(3), with raw peak 73 and cyclic peak 39. [Search and replay](../results/round10_ak3_e17_acm.json), [strict fixed-donor continuation](../certificates/round10_ak3_e17_acm.json).

## Reproduction

~~~sh
work=/tmp/ac-r10-ak3-repro
mkdir -p "$work"
c++ -std=c++17 -O3 -pthread experiments/round10_ak3_frontier.cpp -o "$work/frontier"
c++ -std=c++17 -O3 -pthread experiments/round07_ak3_wide_orbits.cpp -o "$work/reference"
"$work/reference" 20 3 "$work/reference20"
"$work/reference" 21 3 "$work/reference21"
"$work/frontier" seed 21 3 "$work/reference20.orbit.tsv" "$work/c21" 0 0 audit
"$work/frontier" expand 21 3 "$work/reference20.orbit.tsv" "$work/c21" 0 "$work/c21.boundary.bin"
python3 -B experiments/round10_ak3_frontier_audit.py \
  "$work/reference20.orbit.tsv" "$work/reference21.orbit.tsv" "$work/c21"
"$work/frontier" seed 32 8 "$cap31" "$work/c32" 0 0
"$work/frontier" expand 32 8 "$cap31" "$work/c32" 0 "$work/c32.boundary.bin"
~~~

The last command reads the full generated cap-31 orbit TSV at `$cap31`. The optional `audit` argument after the row budget and byte offset requests the exact string-based boundary comparison. For the split control, scan the first 2,510 rows of cap 20 and use the first checkpoint's `next_offset` as the second segment's byte offset. Run `expand` on both segment files and pass `--split` with its output prefix to the Python audit.
