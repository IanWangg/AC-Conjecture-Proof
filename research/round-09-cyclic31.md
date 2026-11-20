# Generated cyclic cap-31 component of AK(3)

2026-11-19. The native generator exhausted the ordinary cyclic cap-31 search with **254,220,523 signed ambient orbits** and zero primitive coordinates. Its result gives a computational lower bound of **32** for the cyclic peak of an ordinary trivialization. The independent Euclidean check passes with zero primitives among 55,347,782 single-sign coordinate occurrences. The independent closure and connectivity check is active on the completed catalogue. [Generation and independent primitive receipts](../results/round09_cyclic31.json).

The native scan tests both recipient choices, inversion signs, cyclic rotations and conjugating bridges within the prescribed total-length cap. Its full count is 288,686,428,968 candidate products and 16,488,539,344 admitted neighbors. The minimum coordinate length remains five. Exactly 179,306,956 orbits have energy 31. The remaining orbits include 1,037,143 new states of energy at most 30, among them 387,572 of energy at most 29. At energy 17, 455 orbits are reached versus 454 in the cap-30 component. These increases arise from paths through higher cyclic energy. [Cap-30 independent audit](round-08-cyclic30.md).

The single new energy-17 signed orbit is `(xxyXYXy, xxYXYxYYXY)`. It is absent from the independently checked cap-30 component. Comparing the backwards search against the cap-29 catalogue gives six anchors. A five-product route reaches a selected anchor, and a further cap-29 route joins it to cap 22. The compiled **702-instruction** ordinary certificate independently replays from AK(3) to the displayed marked pair with raw peak 41 and cyclic peak 31. Its sharp ordinary entry peak of 31 therefore also follows directly from the strict certificate and the cap-30 exclusion. [Strict certificate](../certificates/round09_cyclic31_energy17.json), [route and replay](../results/round09_cyclic31_energy17.json), [compiler](../experiments/round09_cyclic31_energy17.py).

The [cyclic product completeness argument](research-n-cyclic-search.md) covers arbitrary independent conjugating tails via orientations, rotations and shortest bridges of the row axes. Signed ambient permutations preserve the product menu and preserve primitiveness. There is therefore no primitive coordinate in a bounded ordinary path if the generated component is complete and the primitive screen covers all of it. Paths with arbitrary cyclic peak are outside this calculation.

~~~sh
work=/tmp/ac-r09-cyclic
mkdir -p "$work"
c++ -std=c++17 -O3 -pthread experiments/round07_ak3_wide_orbits.cpp -o "$work/wide-orbits"
c++ -std=c++17 -O3 -pthread experiments/round07_ak3_wide_verify.cpp -o "$work/wide-verify"
"$work/wide-orbits" 31 8 "$work/c31"
"$work/wide-verify" 31 12 "$work/c31.orbit.tsv" "$work/c31.verify.json"
python3 -B experiments/round05_ak3_orbit_audit.py primitive "$work/c31.orbit.tsv"
~~~
