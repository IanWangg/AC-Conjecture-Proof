# Short strict paths recovered from the existing raw cap-18 component

Coordinating-agent follow-up, 2026-11-02. No AC solution or novelty claim.

P explicitly recorded the reachable pair

    u1=yXYXyxx, u2=YxYXyyx,

of total raw/cyclic length 14, originally with 227 strict moves and raw
peak 31. A coordinating-agent construction from M's other entry gave
189 strict moves and peak 25. N independently recorded the cyclic-length
13 pair

    (XXXYYxy, XXyxYY),

with 250 strict moves and peak 27. The discovery and structural analysis
are credited to P and N, respectively; the underlying long entry paths
are credited to M. Both endpoint families already occurred in the
previously exhausted raw cap-18 component. They are newly explicit
ledgers here, rather than newly reached components or improved global
energy exclusions.

Reading the previously checked packed checkpoint and lifting its paths
while carrying the coordinate map gives substantially shorter strict
certificates:

| Literal free endpoint | Strict moves | Maximum raw total length |
|---|---:|---:|
| (YxYXyyx, yXYXyxx) | 32 | 18 |
| (XXXYYxy, XXyxYY) | 43 | 18 |

The independent strict elementary verifier replays both exact endpoints.
Neither is a free basis. P's additional finite-tail theorem excludes
primitive elements from all independently conjugated subgroups of the
length-14 pair; this does not restrict arbitrary later interspersed AC
moves. See [P's follow-up](research-p-length14.md).

## Lifting without actual normalization swaps

The packed state key identifies relator inversions and permutations.
An earlier compiler explicitly swapped coordinates whenever the next
canonical key changed their order, which can raise the raw peak.
Those swaps are unnecessary when either endpoint order is acceptable.

Maintain the actual ordered free words and the permutation/sign map to
the current canonical key. To perform a recorded product, choose the
actual recipient and donor through this map; invert the recipient and/or
donor when needed, multiply, and restore the donor's orientation. The
raw lengths of the inverted entries do not change, and the product has
exactly the recorded recipient length. For a conjugation, conjugate the
corresponding actual entry by the same signed letter; conjugation
commutes with inversion. Recompute the coordinate map by comparison
with the next key. No permutation of the actual tuple is inserted.

At the endpoint, invert and cyclically rotate each actual entry to the
requested literal word in its carried order. Each cyclic rotation is
implemented by a single-letter conjugation removing the leading letter
and appending it at the end. Its raw length stays constant. Thus the
lift stays within the recorded raw cap. This is bookkeeping for allowed
moves, not an additional generator automorphism or an implicit swap.

The script checks every intermediate actual free tuple against the
recorded inversion/permutation orbit. The resulting certificates also
pass the separate verifier, which knows nothing about the checkpoint.
Their proof of reachability therefore does not require trusting the
checkpoint generator.

## Checkpoint controls and reproduction

The complete checkpoint contains 251,874 inversion/permutation states.
All 49 independent rotation keys for (u1,u2), and all 42 for N's pair,
are present. Among the recovered parent paths the selected indices are
22,179 and 92,131, with 18 and 33 recorded orbit edges respectively.
No shortest-path or globally minimum-peak claim is made for the strict
ledgers.

Replay the small certificates directly:

    python3 experiments/elementary_verify.py certificates/length14_cap18.json certificates/length13_cap18.json

To regenerate them, first use `packed_peak_search.cpp` to save the cap-18
checkpoint (a budget of one million states suffices), then run:

    python3 experiments/packed_waypoint_paths.py /tmp/cap18.bin yXYXyxx YxYXyyx --certificate /tmp/length14.json --output /tmp/length14-result.json
    python3 experiments/packed_waypoint_paths.py /tmp/cap18.bin XXyxYY XXXYYxy --certificate /tmp/length13.json --output /tmp/length13-result.json

The report supplies ordinary free-group equivalences, not a quotient
endpoint and not a trivialization. AK(3)'s full AC status remains open
within this investigation.
