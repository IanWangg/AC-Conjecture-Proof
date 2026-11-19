# Round 05 · The cap-22 boundary for every primitive row

2026-11-19. The least cyclic total-length peak at which the standard rank-three stabilization of AK(3) can lose every one-occurrence chart is **22**. The same exact threshold holds for losing every primitive relator, so the obstruction at the endpoint persists in every ambient free basis. The checked cap-22 sample finds no geometric endpoint after loss of the fixed auxiliary chart. Stable AC remains open.

## Two strict rank-three paths

Extend the preceding round's 247 elementary moves with six moves. The new path first loses all literal charts at step 249 and ends at the signed cyclic tuple

```text
XXYYZZY   XYZZZYYxy   XYxYXy
```

The strict replay verifies 253 moves, cyclic peak 22, and raw total-length peak 28. Its rows have unsigned occurrence vectors $(2,3,2),(2,4,3),(3,3,0)$ in the marked order $x,y,z$. A cyclic conjugacy class has a one-occurrence letter in some free basis exactly when it is primitive. Whitehead descent gives individual minimum lengths 7, 9 and 5 by checking all cuts of the six-vertex Whitehead graph. Thus no free basis supplies any chart for these three rows. The cap-21 theorem preserves a literal $z$ chart in every reached rank-three state and supplies the matching lower bound. [Strict certificate](../certificates/round05_stable_proof_chartless22.json), [replay and cut and Fox data](../results/round05_stable_proof_chartless22.json), [cap-21 theorem](round-03-stable-proof.md).

A separate **267-move** certificate at cyclic peak 22 reaches the signed cyclic tuple

```text
XXYZyzxYZ   XYZYzy   XZxYxzy
```

It has no marked $z$ chart. Four Whitehead reductions take the primitive row `XZxYxzy` through `XyzYZ`, `XzYZ`, `XY` to `Y`. Apply those same automorphisms to the other rows, then eliminate the isolated `Y` and rename the survivors. This gives `(XXyxYxyXYxyXYxY, XXyyxYY)`, of cyclic energy 22. None of the eight signed rank-two versions appears in the generated cap-27 ordinary catalogue. The ambient automorphisms identify the deletion chart. The 267-move certificate ends at the displayed rank-three tuple. [Strict certificate](../certificates/round05_stable_proof_chart_escape22.json), [rank-two projections](../results/round05_stable_proof_projections.json).

## Two-row blocks without an exposed primitive

The earlier partial cap-22 signed excursion scan contains 2,000,000 representative states. It includes 661 representatives lacking every literal one-occurrence chart, or 10,576 expanded states under the certified signed symmetries. Of those, 216 representatives, or 3,456 expanded states, have no primitive row in any marking. The audit checks all 379 distinct two-row blocks of those 216 representatives. The cyclic-cover Fox minor excludes an infinite cyclic quotient for 375 blocks. In each of the four remaining cases, one product using explicit signed rotations produces a one-occurrence row. Solving that row leaves one rank-two relator. The reduced relator fails the independent signed Euclidean primitive test. If its quotient were infinite cyclic, its normal closure in a suitable rank-two basis would equal the normal closure of a basis letter. Magnus's normal-closure theorem would then make the relator primitive up to conjugacy and inversion. [Block reductions](../results/round05_stable_proof_chartless_scan.json), [Fox criterion](round-04-stable-proof.md), [Magnus's theorem](https://msp.org/gtm/2008/14/gtm-2008-14-004s.pdf).

## Geometry after loss of the fixed auxiliary chart

The 216 representatives with no primitive row give 127 different joint Whitehead minima after signed changes of basis. Each tuple has unimodular abelianization and is disk-busting. In a nontrivial free splitting of $F_3$, at least one free factor has rank one. If all three relators were elliptic, the unimodular exponent matrix would require exactly one row in that rank-one factor, with exponent $\pm 1$, giving a primitive row. By Zieschang's minimal-diagram theorem, a geometric realization of such a tuple yields a spherical paired rotation in the length-minimizing marking. [Minimal-diagram criterion](round-01-stable-proof.md), [rank-three rotation checks](../results/round05_stable_proof_geometry.json).

The rotation test enumerates orders at one end of each handle and induces reversed paired orders at the other end. In a sphere embedding the cyclic orders on a set of parallel edges are opposite at their two ends. Also, if deleting those two vertices leaves at most one connected component of the remaining incident vertices, the parallel edges form a contiguous block at each end. The parallel edges partition the sphere into sectors, and the connected remainder fits into a single sector. These necessary conditions prune the enumeration. For every remaining paired system, the cycles of the face permutation give its Euler characteristic directly. The test checks 22,528 surviving rotation systems across the 127 diagrams, with no spherical rotation. It recognizes the standard basis and the earlier geometric nonprimitive rank-two block with an isolated auxiliary row.

In the full partial scan, **21,597** representatives lack a fixed $z$ chart. For these the program checks all literal charts and one intrinsic Whitehead reduction per primitive row without a literal chart. The 44,396 literal and 5,854 intrinsic charts give 9,969 signed rank-two projection classes. None displays a primitive relator or matches a signed member of the known-trivial archive through energy 56. The 9,113 distinct signed rank-two minima all yield planar-link parity contradictions that the independent verifier replays. Geometry descends when attaching a 2-handle along a primitive relator, so these contradictions exclude geometry in the rank-three source. Together with the direct checks on the 216 representatives with no primitive row, this excludes geometricity for the entire observed no-$z$-pivot part of the partial scan. The search leaves the remaining cap-22 component and higher caps open. [Projection screen](../results/round05_stable_proof_projections.json), [geometric descent](round-01-stable-proof.md), [signed scan provenance](round-04-stable-proof.md).

The weighted intrinsic-basis index compares all 34,636 signed minimized pairs of energy at most 28 with the 23,902 archived trivial pairs. It finds no subgroup match with arbitrary independent conjugating tails. This includes the new energy-22 projection and leaves longer minimized pairs and other kinds of joins open. [Join receipt](../results/round05_stable_proof_projection_joins.json), [weighted index](round-04-ak3.md).

## Reproduction

Rebuild the signed cap-22 partial scan and its first-exit seeds from the [round-four commands](round-04-stable-proof.md), and use its cap-21 path to `(XXXXYYY,XYxYXy)`. Reconstruct the cap-26 and cap-27 TSV catalogues and the [energy-56 archive](round-04-ak3.md). The backward route search uses the same complete cyclic product menu as the bounded search and tests membership in the symmetry-invariant first-exit set. It stores literal predecessors, and the returned route uses 11 states.

~~~sh
work=/tmp/ac-r05-stable
prior=/tmp/ac-r04-stable
mkdir -p "$work"
python3 -B experiments/round05_stable_proof_chartless.py build "$work/chartless22.json" \
  | diff - results/round05_stable_proof_chartless22.json
diff "$work/chartless22.json" certificates/round05_stable_proof_chartless22.json
python3 -B experiments/round05_stable_proof_chartless.py scan "$prior/sym22.states.tsv" \
  | diff - results/round05_stable_proof_chartless_scan.json
python3 -B experiments/round05_stable_proof_geometry.py --scan "$prior/sym22.states.tsv" \
  | diff - results/round05_stable_proof_geometry.json
c++ -std=c++17 -O3 experiments/round05_stable_proof_route.cpp -o "$work/chart-route"
"$work/chart-route" 22 "$prior/seeds22.tsv" "$work/escape.tsv" 1000000 XXYZyzxYZ XYZYzy XZxYxzy
python3 -B experiments/round04_stable_proof_paths.py compile "$prior/rank2-path.json" "$work/escape.tsv" "$work/escape.json"
diff "$work/escape.json" certificates/round05_stable_proof_chart_escape22.json
python3 -B experiments/round05_stable_proof_projections.py "$prior/sym22.states.tsv" \
  /tmp/ac-r04-archive/reverse.tsv 26:/tmp/ac-r03-cyclic/c26.tsv 27:/tmp/ac-r04-cyclic/c27.tsv \
  --basis-index-tsv "$work/minima28.tsv" | diff - results/round05_stable_proof_projections.json
c++ -std=c++17 -O3 experiments/round04_ak3_basis_index.cpp -o "$work/basis-index"
"$work/basis-index" "$work/minima28.tsv" /tmp/ac-r04-archive/reverse.tsv "$work/joins.json"
diff "$work/joins.json" results/round05_stable_proof_projection_joins.json
~~~
