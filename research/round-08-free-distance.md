# Free ordinary and stable instruction distances are at least 19

2026-11-19. All free-group stable paths of length at most 18 from AK(3) to a basis are excluded, for either target order. This bound places no restriction on the word lengths. [Complete exclusion receipt](../results/round08_free_stable_L18.json).

The [peak-rank formula](round-01-stable-disproof.md), the [necessary original-letter conjugations](round-06-stable-disproof.md), and the [tight-product cut refinement](round-07-stable-disproof.md) restrict a minimum path of this length to at most three added pairs. With no padding, the two complete radius-nine free balls are disjoint by the [round-seven ordinary test](round-07-native-distances.md).

With $k$ added pairs, retract the ambient generators to the original two while keeping every row. A path would give at most $18-2k$ instructions in the retracted problem. All three resulting exact free-word graphs fail at these thresholds.

| Added pairs | Tested middle budget | Completed radii | Final boundary queries |
| ---: | ---: | ---: | ---: |
| 1 | 16 | 8 and 8 | 3,365,404,011 |
| 2 | 14 | 7 and 7 | 505,191,962 |
| 3 | 12 | 6 and 6 | 35,037,249 |

The last expansion queries every new neighbor against the complete opposite ball. A zero intersection is sufficient for exclusion, so this final layer need not be retained in memory. The first calculation holds 136,739,554 and 416,079,086 states before the boundary-only expansion. The signed right-product and conjugation instructions operate on exact reduced words throughout.

~~~sh
mkdir -p /tmp/ac-r08-free
c++ -std=c++17 -O3 experiments/round06_free_instruction_distance.cpp -o /tmp/ac-r08-free/search
for k in 1 2 3; do
  /tmp/ac-r08-free/search "$k" "$((18 - 2*k))" --boundary-only
done
~~~
