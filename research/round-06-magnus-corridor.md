# Exact bounded lifts along projected Magnus paths

2026-11-19. The degree-eight unordered ordinary distance is greater than 14. The degree-seven one-padding exclusion is reproduced by lifting only the lower-degree paths that can meet at the chosen midpoint.

## Midpoint filtering

Fix a path budget $L=a+b$. Map the full ordinary graph to a lower-degree graph by truncating the Magnus expansion and optionally erasing auxiliary variables while keeping their rows. Every edge projects to an edge or an unchanged state. Use the unordered graph throughout.

Compute the complete lower-degree balls $B_a(u)$ and $B_b(v)$ around the projected endpoints. Their intersection $M$ contains the projected midpoint of every candidate path. Paths of length less than $L$ can be padded with waits. For the start side, set $C_a=M$ and iterate

$$
C_i=B_i(u)\cap(C_{i+1}\cup N(C_{i+1})),
\qquad i=a-1,\dots,0,
$$

where $N(S)$ is the union of the neighbors of $S$. Starting from any state of $C_i$, the recurrence gives a legal lower-degree prefix of length at most $i$ and a continuation of length at most $a-i$ to $M$. The goal side is analogous. Every initial segment of an admissible full path stays in these layers after projection. Lift from each endpoint through the preimages of these layers, allowing waits in addition to legal moves. The two full midpoint sets intersect if and only if there is a full path of length at most $L$. The forward implication of sufficiency follows by concatenating the two lifted halves and omitting waits.

With one auxiliary generator and degree seven, the split $5+6$ uses a rank-two degree-five retraction. The lower midpoint set contains 24 states. The final lifted sets contain 308 and 276 states and are disjoint, reproducing the [direct one-padding exclusion](../results/round05_magnus_degree7_one_padding.json) without constructing either full padded ball. [Search receipts](../results/round06_magnus_corridor.json).

For degree eight at rank two, the split $7+7$ uses degree six below. Its midpoint set has 98 states. The final degree-eight sets contain 102 and 98 states and are disjoint. This excludes every ordinary path of length at most 14. The [round-five positive-padding exclusions](round-05-stable-disproof.md) already exclude all positive-padding pieces of a length-14 stable path at degree seven, and every higher-degree path projects there. At most three padded pairs could occur in an optimal stable path of length 14. Thus the degree-eight stable distance is also at least 15.

~~~sh
python3 -B experiments/round06_magnus_corridor.py 1 7 5 5 6
python3 -B experiments/round06_magnus_corridor.py 0 8 6 7 7
~~~
