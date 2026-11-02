# Supplement: finite PSL(2,p) instruction distances

Date: 2026-11-02. Root-agent experiment supporting Research B's metric
discussion. This is a finite computation, with no claim of unbounded growth
or an obstruction to AC triviality.

Use the quotient F(x,y) -> PSL(2,p) defined by the matrices

    x -> [[1,1],[0,1]],  y -> [[1,0],[-1,1]].

The braid relator maps to the identity. The ordered starting tuple is
the image of `(xxxYYYY, xyxYXY)` and the target is the image of `(x,y)`.
Matrices differing by sign are identified.

The finite symmetric alphabet has exactly fourteen instructions: invert
either coordinate (2), right multiply either coordinate by the other or its
inverse (4), and conjugate either coordinate by one of x,X,y,Y (8). Each
instruction costs one. Relator interchange is not a separate instruction.
These conventions differ from Research B's fifteen-instruction experiment
and from counting arbitrary-word conjugations as single moves.

Exact breadth-first search gave:

| p | Group order | Distance | States processed before target discovery |
|---:|---:|---:|---:|
| 3 | 12 | 3 | 18 |
| 5 | 60 | 6 | 1,114 |
| 7 | 168 | 9 | 22,892 |
| 11 | 660 | 9 | 387,278 |
| 13 | 1,092 | 9 | 436,909 |
| 17 | 2,448 | 9 | 1,561,263 |
| 19 | 3,420 | 10 | 10,125,578 |

The program constructs the group by generator closure, checks its order
against p(p^2-1)/2, builds the exact multiplication table, and searches the
ordered-pair graph. It stores a shortest path and independently replays that
path using direct matrix multiplication. First target discovery in a
breadth-first traversal proves the stated distance in this finite graph.

Run from the repository root:

```sh
python3 experiments/finite_quotient_distances.py 3 5 7 11
python3 experiments/finite_quotient_distances.py 13 17 19
```

The second command needs more memory and time because its largest graph has
11,696,400 possible ordered pairs. The script uses only the Python standard
library. Outputs include matrix representatives, search counts and shortest
instruction sequences.

Projection implies that any free-group path in this fourteen-instruction
metric has length at least ten. This modest bound does not apply to an
alternative convention that assigns unit cost to an arbitrary-word
conjugation or to arbitrary changes of generators. The displayed values do
not prove asymptotic growth. A single path valid in PSL(2,Z) would give a
uniform upper bound in every one of these congruence quotients, and is a
useful next question investigated separately by Research E.

## Follow-up resolved during this investigation

[Research E](research-e.md) supplies an explicit ten-instruction path in B3 itself and proves its distance is exactly ten under the same fourteen-instruction alphabet. Every congruence quotient above therefore has distance at most ten, and the value at p=19 attains this uniform ceiling. This entire fixed-braid representation family cannot yield unbounded quotient distances. The certificate's free-group lift is explicitly not a trivialization.
