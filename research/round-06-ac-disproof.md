# Basis constraints for three conjugation phases

2026-11-19. Exact scans retain the simultaneous rank-two Nielsen basis at each of the first two phases. Intrinsic basis masses at most four and three, with intersecting axes at both placements, produce 172,298 distinct rank-two cores. Their 103,017,706 possible third-phase rebased joins contain no ambient primitive. At masses three and three, the same exclusion allows an intersecting placement at one phase and a geodesic gap of at most one at the other. The third independent conjugation and the final Nielsen suffix are unrestricted.

## Where the third all-elements envelope loses information

The [round-five literal envelope](round-05-ac-disproof.md#limits-and-control) excludes a primitive after a first zero-gap conjugation and an arbitrary second conjugation, even with arbitrary Nielsen changes. Therefore both actual rows just before a third independent conjugation are nonprimitive. Their cyclic classes are preserved by those conjugations. If the resulting two words generated all of the ambient free group, they would be a free basis, with both words primitive. This rules out the entire ambient rose as an actual third-phase subgroup under these hypotheses. A proper rank-two subgroup could still contain a primitive that becomes a coordinate after a Nielsen suffix.

## Exact test of a fixed witness in a rank-four rebased join

Let $H$ be an ambient-primitive-free rank-two subgroup with its source marking $(A,B)$. For vertices $a,b$ of its immersed core, write $H_a,H_b$ for the groups of loop labels at those vertices. Transport $(A,B)$ from the source basepoint to both vertices, keeping the same source marking. If $J=\langle H_a,H_b\rangle$ has rank four, the natural map $H_a*H_b\to J$ is an isomorphism. One proof is to fold the rooted wedge of the two copies. A fold either preserves the rank or decreases it, and an equal-rank fold induces an isomorphism on fundamental groups. This gives an explicit free-product marking by the four transported basis words. [Stallings, topology of finite graphs](https://doi.org/10.1007/BF02095993).

Fix a based element $w\in J$ that is primitive in the ambient group. Consider its cyclic free-product normal form. It uses both factors, since otherwise an ambient conjugate of $w$ would lie in one of the primitive-free copies. There are $u\in H_a$ and $v\in H_b$ whose source intrinsic conjugacy classes are a simultaneous Nielsen basis and for which $w$ is conjugate in $J$ into $\langle u,v\rangle$ exactly when the following conditions hold.

1. In each factor all the syllables are powers of one common nontrivial root in that factor.
2. Both maximal roots are primitive in their respective marked free groups.
3. Their signed exponent vectors, in the common source marking, have determinant of absolute value one.

For necessity, cyclically reducing a word in $\langle u,v\rangle$ in the free product leaves an alternating word of powers of $u,v$. The conjugacy theorem for a free product identifies reduced cyclic forms of syllable length at least two up to cyclic rotation of syllables. As intrinsically primitive elements, $u,v$ are root-free. For sufficiency, use the two roots as the placed words. Their source conjugacy classes have basis representatives together, since a unimodular matrix lifts to a rank-two Nielsen basis and a primitive conjugacy class is determined by its exponent vector. Independent ambient conjugations realize the root in each indicated copy. The cyclic form is already a word in the two placed rows. Thus the test applies to an actual subgroup that can be obtained from $H$ by a Nielsen change and one conjugation phase. When a cyclic primitive label is given without a basepoint, check the finitely many loops with that label in the join core. This accounts for all based representatives up to conjugation in $J$. [Osborne and Zieschang](https://geodesic.mathdoc.fr/item/IM_1981__63_142788/).

The test uses exact free reduction, maximal periodic roots after stripping conjugating ends, cyclic centralizers in a free group, and Euclidean primitive representatives. A rank-deficient join has relations between the two factors, so its quotient words cannot use this free-product normal-form criterion. The fixed-word test also requires a separate enumeration if one seeks every ambient primitive in a given join.

The three known primitive-positive joins of the literal AK(2) pair have rank four and supply positive controls. Their common ambient primitive cyclic word is **xYxYYxYY**. The intrinsic free-product forms are **cDa**, **cDa**, and **cBa**, where $a,b$ mark the first factor and $c,d$ mark the second. Each form passes the cyclic-root and determinant conditions. An 11-move strict ordinary replay from the literal AK(2) pair reaches the actual first witness **YxYYxYYx** as a coordinate. Abstract controls separately reject noncommuting block syllables, nonprimitive roots, and root slopes of determinant two. [Exact controls and replay](../results/round06_ac_disproof_basis_phases.json).

## Enumerating the two actual bases

At each stage use the current placed pair as the marking of its subgroup. The two rows normally generate $F(x,y)$, and their ambient exponent vectors have determinant of absolute value one. Consequently the subgroup is rank two and the two current rows are a free basis for it. For a Nielsen output let $(a,b)$ and $(c,d)$ be its two intrinsic exponent vectors relative to this marking. Its **basis mass** is $|a|+|b|+|c|+|d|$. Enumerate every pair of primitive slopes at the stated mass bound with determinant of absolute value one. Construct the exact intrinsic cyclic conjugacy classes via Euclidean words. For each such pair, arbitrary independent conjugation makes all independent rotations possible when the final axes intersect, and all rotations with admissible shortest bridges when they are disjoint. Signs and row order can be normalized because mass and subgroup membership are invariant under their changes. The bounds refer to the geodesic distance between the axes, with zero denoting intersection. They leave the lengths of the individual conjugators unrestricted. [Geometric conjugation menu](research-n-cyclic-search.md).

After the second placement, retain the actual rank-two core up to labelled isomorphism and common conjugation. The third phase needs just the finite two-copy joins of that core. Adjacent vertex pairs in its self-fiber product give conjugate joins: a path with the same label in both copies transports both based loop groups by that common conjugation. It therefore suffices to test one unordered pair of vertices per off-diagonal fiber-product component, along with the original core. The disjoint third-axis case follows from the separating-bridge argument, since a cyclic primitive word in rank two uses only one sign of each letter. [Two-copy proof](round-02-ac-disproof.md#finite-join-in-place-of-the-infinite-voltage-kernel).

| First and second basis masses | First and second geodesic gap caps | Distinct second cores | Third join placements covered | Fiber-product representatives checked |
| --- | --- | ---: | ---: | ---: |
| 3, 3 | 0, 0 | 45,400 | 14,379,815 | 6,860,232 |
| 2, 3 | 1, 0 | 11,229 | 1,907,262 | 894,921 |
| 3, 2 | 0, 1 | 489 | 66,109 | 31,038 |
| 3, 4 | 0, 0 | 116,765 | 60,081,093 | 28,921,301 |
| 3, 3 | 0, 1 | 139,397 | 48,530,663 | 23,206,928 |
| 3, 3 | 1, 0 | 155,196 | 56,489,073 | 27,011,215 |
| 4, 3 | 0, 0 | 172,298 | 103,017,706 | 49,629,356 |

Every tested representative passes the signed double-free transition DAG test. The first row of the table was also run over every vertex pair, giving the same exclusion. An independent Python batch fold reconstructs the finite second core counts and checks sampled joins by folding the four based generator words and topologically sorting their signed transition graphs. For mass at most four its Nielsen menu uses the fact that one coordinate has norm one: the two distinct mixed slopes of norm two have determinant of absolute value two. The other row is then obtained up to sign and conjugacy by multiplying by a power of the norm-one row.

For a concrete path with a one-edge first bridge, first multiply the initial power word by the braid word. Cyclic normalization and independent conjugation place the two resulting cyclic words **XYxxxYYYYxyxY** and **YXYxyx** across a bridge labelled **Y**. Their original loops in the literal AK(3) core each have a unique lift. The needed outgoing bridge directions are absent at both lifts, so this first placement has unread gap one in the original core. Its length-13 lobe also distinguishes it from every literal first one-edge barbell. A second Nielsen product followed by a conjugation gives intersecting axes. The receipt replays all 18 elementary moves to that second placement. [Strict path and exact scan data](../results/round06_ac_disproof_basis_phases.json).

## Reproduce

~~~sh
work=/tmp/ac-r06-basis-phases
mkdir -p "$work"
c++ -std=c++17 -O3 experiments/round06_ac_disproof_basis_phases.cpp -o "$work/scan"
"$work/scan" 3 3 0 0 "$work/3300.exceptions.jsonl" > "$work/3300.json"
"$work/scan" 2 3 1 0 "$work/2310.exceptions.jsonl" > "$work/2310.json"
"$work/scan" 3 2 0 1 "$work/3201.exceptions.jsonl" > "$work/3201.json"
"$work/scan" 3 4 0 0 "$work/3400.exceptions.jsonl" > "$work/3400.json"
"$work/scan" 3 3 0 1 "$work/3301.exceptions.jsonl" > "$work/3301.json"
"$work/scan" 3 3 1 0 "$work/3310.exceptions.jsonl" > "$work/3310.json"
"$work/scan" 4 3 0 0 "$work/4300.exceptions.jsonl" > "$work/4300.json"
"$work/scan" 3 3 0 0 "$work/3300_raw.exceptions.jsonl" --all-final-vertices > "$work/3300_raw.json"
python3 -B experiments/round06_ac_disproof_basis_controls.py \
  "$work/3300.json" "$work/2310.json" "$work/3201.json" \
  "$work/3400.json" "$work/3301.json" "$work/3310.json" "$work/4300.json" \
  --uncompressed "$work/3300_raw.json" \
  | diff - results/round06_ac_disproof_basis_phases.json
~~~
