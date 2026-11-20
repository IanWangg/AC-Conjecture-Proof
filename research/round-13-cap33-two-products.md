# Two-product test through the whole generated cap-33 first exit

2026-11-19. For every generated ordinary cap-32 AK(3) orbit, the exact first-exit menu at energy 33 has been generated and checked for a primitive on the following cyclic product. The following product uses arbitrary conjugating tails and has no output energy bound. Both source partitions finish without finding a primitive. [Full native receipts](../results/round13_cap33_two_products.json), [uncapped product proof](round-12-primitive-step.md).

| Source partition | Orbits | Anchored energy-33 records | Primitive on next product |
| --- | ---: | ---: | ---: |
| Independently verified cap-31 component | 254,220,523 | 2,456,594,139 | 0 |
| New generated cap-32 orbits | 285,484,620 | 1,842,133,617 | 0 |
| Total | 539,705,143 | 4,298,727,756 | 0 |

Records carry one actual old parent for each destination found in a batch. A destination can occur in multiple batches. Every record was checked, so duplicates do not affect coverage. The cap-33 generator agrees with the independent full product menu on the 59,515 short source orbits tested in Round 12. The completed full first-exit generation uses the packed generator. The independent cap-32 outside-closure check is still running. [Cap-32 sources](round-11-cyclic32.md), [cap-33 reference control](../results/round12_ak3_primitive_step.json).

Take the last visit of an ordinary path to the generated cap-32 component before its first primitive coordinate. If the immediate exit reaches energy 33, there must be at least three cyclic products from that last visit to the first primitive coordinate. Consecutive inversions and conjugations preserve the signed cyclic orbit, and the test accounts for them through the product menu. The calculation imposes no bound on a path that first exits at a higher energy. It does not expand the whole cap-33 component.

~~~sh
mkdir -p "$work"
c++ -std=c++17 -O3 -pthread experiments/round10_ak3_frontier.cpp -o "$work/frontier"
c++ -std=c++17 -O3 -pthread experiments/round12_ak3_primitive_step.cpp -o "$work/primitive-step"
"$work/frontier" seed 33 6 "$cap31" "$work/from31" 0 0
"$work/frontier" seed 33 6 "$outside32" "$work/from32-additions" 0 0
"$work/primitive-step" "$work/from31.boundary.bin" 7 --boundary
"$work/primitive-step" "$work/from32-additions.boundary.bin" 7 --boundary
~~~
