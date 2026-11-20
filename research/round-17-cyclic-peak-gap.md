# Exact ordinary entry peak 37 for E22 and E24

The ordinary cyclic entry peak from AK(3) is **37** for both marked endpoints below. Their strict stable entries from Round 16 have peak **33** and maximum rank **3**, so the gap between the minimum ordinary and minimum stable peaks is at least **4**.

~~~text
E22 = (XXYYYxYXY, XXYYxYXXyxxY)
E24 = (XXYxYXXYxxy, XXYXYxxyXyxxy)
~~~

E22 has cyclic energy **21** after deletion. Its historical label counts the isolated auxiliary letter of the preceding rank-three triple. E24 has cyclic energy 24.

The compiled ordinary E22 path takes **1,345** strict elementary instructions at raw peak **51**. Append the existing ordinary 40-instruction E22-to-E24 suffix to obtain a **1,385**-instruction strict ordinary path to E24 at the same cyclic peak. These paths end at the exact ordered free words. [Ordinary E22 certificate](../certificates/round17_ak3_e22_ordinary37.json), [ordinary E22-to-E24 suffix](../certificates/round16_stable_proof_e22_to_e24.json), [stable ledgers and peak bounds](round-16-cyclic-peak-gap.md).

## Ordinary exclusions through cyclic cap 36

| Cyclic cap | Signed orbits | Candidate products | Admitted products |
| ---: | ---: | ---: | ---: |
| 33 | 37,659 | 65,473,912 | 1,928,110 |
| 34 | 66,819 | 119,647,008 | 3,510,226 |
| 35 | 147,862 | 279,534,568 | 8,075,870 |
| 36 | 265,026 | 514,401,544 | 14,820,320 |

For each cap the reverse search starts from E22, expands every cyclic state in its component, and finds neither AK(3) nor a primitive coordinate. A separate implementation recomputes the entire product menu with stack reduction, matches both product counts, and checks closure and connectedness. The cap-36 component contains the signed E24 orbit and excludes the signed AK(3) orbit. Any ordinary path at the fixed markings must exceed 36, since projecting the path to signed cyclic states would otherwise connect these orbits. [Cap-36 catalogue](../certificates/round17_ak3_e22_cap36_component.tsv.gz), [independent counts and membership](../results/round17_ak3_e22_ordinary_peak.json), [proof of the cyclic reduction](round-16-cyclic-peak-gap.md#ordinary-lower-bound).

## Ordinary bridge at cyclic cap 37

The reverse search meets a known energy-33 first-exit seed after a 31-product cyclic route from E22. Its recorded anchor `(xxxyxxyXYxy, xxxxyxxyxxyXXYxxy)` is in the independently verified cap-31 catalogue. The ledger uses a four-product cap-32 route from the anchor to an orbit in the cap-29 catalogue, then a bounded route to a cap-22 orbit. The compiler lifts the paths backward from literal E22 in a fixed marking, obtains the corresponding marked cap-22 prefix, and expands every cyclic product edge into ordinary inversions, conjugations by single generators and positive right multiplications. [First-exit provenance](round-14-independent-cyclic32.md), [anchor-to-cap-29 route](../certificates/round17_ak3_e22_anchor_cap32.tsv), [cap-29-to-cap-22 route](../certificates/round17_ak3_e22_anchor_cap29.tsv), [compiler](../experiments/round17_ak3_e22_ordinary.py).

The capped paths establish that the two endpoints belong to the ordinary AK(3) component. The cap-36 reverse component and the 1,141,922 states discovered by the cap-37 search through the first seed contact both fail the arbitrary-tail one-product primitive test. [Scans](../results/round17_ak3_e22_ordinary_peak.json).

## Further checks in the reverse component

The complete cap-36 catalogue has **260,392** distinct cyclic coordinates. The independent Euclidean test finds no primitive. All **447,640** retained energy-37 first-exit records from that catalogue pass a second primitive-product check with arbitrary conjugating tail and output length. The boundary generator compares its product menu with an independent string implementation at each source. Thus a route from the cap-36 component needs at least three products from its last visit to that component to reach a primitive if its next cyclic energy is 37. [First-exit receipt and primitive scans](../results/round17_ak3_e22_ordinary_peak.json).

The arbitrary-tail archive comparison checks all **23,902** verified basis-side pairs against each of the cap-34 catalogue, the cap-36 catalogue, and the states reached through the first seed contact at cap 37. All three comparisons return zero subgroup joins. The last catalogue is a partial component, and the test concerns the archive strategy described in Round 4. [Exact archive method](round-04-ak3.md), [comparison receipts](../results/round17_ak3_e22_ordinary_peak.json).

A separate archive test allows a simultaneous ambient automorphism, independent row conjugations, inversion and row order. Whitehead descent reduces each cyclic pair to minimum length, then explores the entire minimum-length level under the elementary shears. Peak reduction makes the least key of this level complete for the indicated equivalence. The archive has **19,771** such classes, the cap-36 catalogue has **235,852**, and the cap-37 partial catalogue has **1,064,425**. Both intersections are empty. The implementation uses strings throughout, including for archive pairs with a coordinate longer than 31. The basic basis control and 24 seven-substitution positive controls match as expected. [Rank-two Whitehead sublevels](round-07-stable-proof.md), [scan](../experiments/round17_ak3_ambient_join.cpp), [counts](../results/round17_ak3_e22_ordinary_peak.json).

The planar-link parity test excludes an orientable thickening for each of the **265,026 literal canonical cyclic complexes** in the cap-36 component. There are 260,587 $K_4$ links and 4,439 diamond links. The independent verifier checks the contradictory XOR witnesses, with **614,557** equations in total. The result concerns the supplied literal complexes; it leaves other presentations of the same group available for geometric searches. [Parity method](research-w.md), [complete screen](../results/round17_ak3_e22_cap36_link_screen.json), [driver](../experiments/round17_ak3_link_screen.py).

## Reproduction

Set `work` to a writable directory and `compacted` to the complete Round 14 first-exit index. The saved compressed catalogue suffices for the ordinary lower bound without regenerating the index.

~~~sh
gzip -cd certificates/round17_ak3_e22_cap36_component.tsv.gz > "$work/e22-cap36.tsv"
c++ -std=c++17 -O3 -pthread experiments/round07_ak3_wide_verify.cpp -o "$work/independent"
"$work/independent" 36 8 "$work/e22-cap36.tsv" "$work/independent.json" XXYYYxYXY XXYYxYXXyxxY
python3 experiments/elementary_verify.py certificates/round17_ak3_e22_ordinary37.json
c++ -std=c++17 -O3 -pthread experiments/round16_ak3_reverse_seed.cpp -o "$work/reverse"
"$work/reverse" XXYYYxYXY XXYYxYXXyxxY "$compacted" 2000000 8 "$work/partial37.tsv" 37 > "$work/cap37.json"
c++ -std=c++17 -O3 experiments/round03_ak3_escape_path.cpp -o "$work/literal"
python3 -B experiments/round17_ak3_e22_ordinary.py "$work/cap37.json" \
  certificates/round17_ak3_e22_anchor_cap32.tsv certificates/round17_ak3_e22_anchor_cap29.tsv \
  "$work/literal" "$work/e22-ordinary37.json"
c++ -std=c++17 -O3 -pthread experiments/round10_ak3_frontier.cpp -o "$work/frontier"
"$work/frontier" seed 37 8 "$work/e22-cap36.tsv" "$work/exit37" 0 0 audit
c++ -std=c++17 -O3 -pthread experiments/round12_ak3_primitive_step.cpp -o "$work/primitive-step"
"$work/primitive-step" "$work/exit37.boundary.bin" 8 --boundary
python3 -B experiments/round17_ak3_link_screen.py "$work/e22-cap36.tsv" --workers 8
~~~

With `archive` set to the verified 23,902-pair Round 4 archive, replay the simultaneous ambient comparisons as follows. [Archive provenance](round-04-ak3.md#reproduction).

~~~sh
c++ -std=c++17 -O3 experiments/round17_ak3_ambient_join.cpp -o "$work/ambient"
"$work/ambient" "$work/e22-cap36.tsv" "$archive"
"$work/ambient" "$work/partial37.tsv" "$archive"
~~~
