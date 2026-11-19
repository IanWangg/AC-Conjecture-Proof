# Complete cyclic cap-26 component of AK(3)

2026-11-19. Any ordinary AC path from AK(3) to a primitive relator, and in particular any ordinary trivialization, must reach cyclic total relator length at least **27**.

The round-one generator produced 10,340,996 canonical states at cyclic cap 26. The independent checker reconstructed 9,587,387,424 candidate products, 518,647,032 admissible neighbor checks and 10,641,280 candidates with nonempty shortest bridges. The maximum needed bridge length was three. It verified closure under the full geometric menu and connectedness from the original AK(3) class. A separate exact Euclidean scan of 8,561,906 distinct signed cyclic coordinate classes found zero primitives. The minimum cyclic total length remains 13 and the minimum coordinate length is five. [Cyclic menu proof](research-n-cyclic-search.md), [result and catalogue hashes](../results/round03_cyclic26.json).

Comparing the two complete components, cap 25 and cap 26 agree through cyclic energy 14. Cap 26 adds eight pairs of energy 15 and 24 pairs of energy 16. Each of these pairs has exact minimum cyclic entry peak 26, by the connectedness result at cap 26 and its exclusion from the smaller complete component. The eight energy-15 pairs form a single orbit under signed permutations of the ambient basis. [Eight energy-15 entries](../results/round03_cyclic26_energy15.tsv), [cap-25 audit](round-02-cyclic25.md).

A shortest cyclic-product route at cap 26 to the energy-15 escape set takes 30 edges. The bidirectional search exhausts disjoint balls of radii seven and 22 and checks 553,032,299 candidate products. The strict replay reaches the pair (XYXyxYYY, XXYxYxy) in 369 moves with raw peak 29 and cyclic peak 26. [Macro route](../results/round03_cyclic26_energy15_path.json), [strict certificate](../certificates/round03_cyclic26_energy15_escape.json).

The round-three two-copy primitive screen checks all 448 independent rotations of the eight new pairs, giving 232 distinct core graphs. It checks the core itself and every distinct-vertex join, including 18,384 joins. Every sign-restricted transition graph is acyclic, excluding primitives without requiring partial-map checks. When the first rotation is realized on intersecting axes, this excludes a primitive after arbitrary Nielsen moves, independent conjugations of the coordinates and a final Nielsen suffix. Disjoint first-axis bridges are outside this new screen. [Two-copy screen](../results/round03_cyclic26_energy15_two_copy.json), [phase argument and reproduction](round-03-ak3.md).

The full components and result can be regenerated using the generator and independent checker from the [cap-25 reproduction](round-02-cyclic25.md), with cap 26 and its corresponding output paths. The TSV contains the canonical signed and permuted representatives. To regenerate the reported energy-15 set, filter both complete TSVs to rows whose coordinate lengths sum to at most 15, then take the cap-26 set difference.

~~~sh
mkdir -p /tmp/ac-r03-escape
c++ -std=c++17 -O3 experiments/round03_ak3_escape_path.cpp -o /tmp/ac-r03-escape/path
/tmp/ac-r03-escape/path 26 results/round03_cyclic26_energy15.tsv /tmp/ac-r03-escape/route.json
diff results/round03_cyclic26_energy15_path.json /tmp/ac-r03-escape/route.json
python3 -B experiments/round03_ak3_escape_replay.py /tmp/ac-r03-escape/route.json \
  /tmp/ac-r03-escape/certificate.json /tmp/ac-r03-escape/replay.json
diff certificates/round03_cyclic26_energy15_escape.json /tmp/ac-r03-escape/certificate.json
c++ -std=c++17 -O3 experiments/round03_ak3_two_copy_frontier.cpp -o /tmp/ac-r03-escape/frontier
/tmp/ac-r03-escape/frontier results/round03_cyclic26_energy15.tsv rotations \
  /tmp/ac-r03-escape/candidates.jsonl /tmp/ac-r03-escape/two-copy.json
diff results/round03_cyclic26_energy15_two_copy.json /tmp/ac-r03-escape/two-copy.json
~~~
