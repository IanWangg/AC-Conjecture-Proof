# Ordinary splices across the energy-20 chart boundary

2026-11-19. Two specific chart changes in the strict rank-three AK(3) ledger have ordinary rank-two replacements of 1,803 and 1,719 moves. Each attains the exact least ordinary cyclic peak of 37. Both relator identities must receive products in any replacement. An audit of the entire rank-three ledger excludes a descent assembled from the earlier one-donor interval criterion, even when every interval passing two necessary tests is treated as available. [Exact interval audit](../results/round09_ac_proof_e20_intervals.json), [splice replays and orbit routes](../results/round09_ac_proof_e20_splices.json).

## The first chart in the energy-20 component

Immediately before strict step 394, the three rows are `(XYYXy, yXYzyyx, XYZXzyxY)`. Step 394 multiplies the third row on the right by the second, giving `(XYYXy, yXYzyyx, XYZXzzyyx)`. The last two rows are primitive at both endpoints. One Whitehead chart for the third row changes across the product from

~~~text
x ↦ XYxyxYXyx     y ↦ XYXyx    z ↦ XYxyxy
~~~

to

~~~text
x ↦ yyxY         y ↦ x        z ↦ y
~~~

The latter has ordered cyclic projection `(XXyXYYxyXYY, XXYxyyxYXyXYY)`. Its signed key lies in the independently checked 265,026-orbit cap-36 component of the energy-20 pair. The component excludes the AK(3) root, with least energy 20. The former chart has ordered cyclic projection `(XXyxYxyxY, XYXyxYXyXYxyxy)` and has an independently replayed AK(3) entrance at cyclic peak 23. At the step-394 vertex one can also select the second row, using the chart `x ↦ x`, `y ↦ y`, `z ↦ yxYXYY`. Its ordered cyclic projection `(XYYXy, XYXyxYXYxYXyxy)` has an AK(3) entrance at cyclic peak 21. [Original strict prefix](../certificates/round09_stable_proof_e20_rank3.json), [independent cap-36 enclosure](round-09-ak3.md#a-marked-endpoint-shared-by-stable-and-ordinary-paths).

For each alternative, reverse its checked AK(3) entrance, then concatenate the cap-37 join from AK(3) into the energy-20 component and a 14-product course from there to the common target. The compiler lifts each signed orbit edge to its literal marking. When row order needs to change, it performs the elementary swap at the short AK(3) end and exchanges the row indices on the rest of that entrance. The two certificates replay in rank two with only inversion, right multiplication and single-letter conjugation. Both have raw peak 46. If either splice stayed within cyclic cap 36, its initial AK(3) entrance and the splice would connect the two independently separated components at cap 36. [Strict same-vertex certificate](../certificates/round09_ac_proof_e20_vertex_splice.json), [strict product certificate](../certificates/round09_ac_proof_e20_product_splice.json).

The two individual relator automorphism orbits on either left endpoint are disjoint from the two orbits at the right endpoint. Whitehead descent and traversal of the complete minimum-length plateau give exact orbit keys. A row identity that never receives a product can only be inverted or conjugated. Even changing the free marking would preserve its individual automorphism orbit. Thus a splice must multiply into both rows. This remains true even though the projected donor immediately across step 394 has Whitehead length 13 on both sides. Its two minimum-plateau keys differ. [Whitehead orbit computation](../experiments/round07_ac_proof_cap23.py), [all endpoint orbit keys](../results/round09_ac_proof_e20_splices.json).

## One-donor interval audit

Replay the 544 strict steps and retain the initial tuple and the cyclic tuple at each of the 57 products. Inversions and conjugations leave all primitive pivot choices and retained donor orbits unchanged. Every product stage has an intrinsic primitive chart. For each ordered pair of stages and charts, and every two-slot block containing both deleted slots, test two necessary conditions for a one-donor splice. The block's endpoint abelianized lattices must coincide. The retained donor on each end must belong to the same marked rank-two automorphism orbit, allowing inversion and conjugation. For the lattice test the cross product of the two row exponent vectors is primitive, because the three vectors at each stage form a unimodular basis. Its direction up to sign therefore determines the entire saturated block lattice. The tests permit intervals with imports from the exterior row during the excursion. [One-donor endpoint criterion](round-07-ac-proof.md#necessary-and-sufficient-endpoint-condition).

Of 6,266 candidate intervals, 5,411 fail the lattice condition and 439 more fail the donor orbit condition. Allow the remaining 416 intervals and the 63 fixed-pivot product transitions. From the initial isolated pivot this graph reaches 68 of 94 chart occurrences. The last reached product stage is strict step 448. Neither final pivot is reachable. Accepting every pass intentionally enlarges the graph, so the absence of an endpoint in this reachability test rules out the prescribed class of one-donor descents on this particular ledger.

The 94 chart occurrences give 47 distinct signed cyclic projections. Thirty-five classes belong to the verified ordinary AK(3) cap-30 component and eight to the energy-20 cap-36 component. The latter eight are ordinarily reachable through the single cap-37 entrance. Four classes have unsettled ancestry in this comparison. The replacement certificates show that the obstruction is compatible with ordinary projection when the two retained relator identities both change. In rank two the [round-eight common-complement donor hypothesis](round-08-ac-proof.md#comparing-donor-blocks) would require ordinary moves on the surviving pair to expose a primitive relator. For a balanced trivial pair this would already give a trivialization, since killing a primitive leaves a cyclic quotient and the other relator has exponent one up to sign.

## Limits of noninvertible transport with a frozen relator

A nontrivial word in (F_2) can be preserved up to conjugation and inversion by a nonsurjective endomorphism with unimodular abelianization exactly when the word is a power of a primitive. To prove necessity, the image has rank two by unimodularity, so the endomorphism is injective by the Hopf property of rank-two free groups. Compose with an inner automorphism to send the word to itself or its inverse, then square. The resulting endomorphism is still injective and nonsurjective and fixes the word. Turner's stable-image theorem makes its stable image a proper free factor, hence cyclic because it contains the word. This gives the required power. For sufficiency take a basis ((a,b)) with (a) the primitive root and use (a\mapsto a), (b\mapsto b^2ab^{-1}). The abelianization is unimodular. Folding the two based loops gives an immersed graph with an (a) loop at the base and a (b) edge to a distinct vertex, so the image omits (b). [Turner's theorem in Ciobanu–Logan, Lemma 3.2](https://arxiv.org/pdf/2009.04937).

Each relator of a balanced normally generating pair has a primitive exponent vector. For such a relator, being a power of a primitive forces the relator itself to be primitive. Consequently an ordinary rank-two counterpart to the [once-stabilized substitution method](round-09-stable-proof.md#endomorphisms-preserving-the-component) cannot hold one nonprimitive relator fixed up to conjugation and inversion. As a bounded cross-check, replace one AK(3) generator by a reduced word of length four or five, with self-exponent (+1) and at least three occurrences of that generator or its inverse. There are 72 substitutions and 28 signed cyclic images. None lies in either of the two checked components. Each substitution in this menu is nonsurjective. After removing the initial and terminal words in the other generator, its image word begins and ends in the replaced generator and contains it at least three times. The image subgroup is represented by the cyclically reduced part attached by its conjugating stem to the base loop of the fixed generator. The replaced generator still has no based loop. [Substitution census](../results/round09_ac_proof_e20_intervals.json).

## Reproduce

Use the ordinary cap-30 catalogue and the independently checked energy-20 cap-36 catalogue from the [ordinary waypoint report](round-09-ak3.md#reproduce). The two certificates have standalone exact replays.

~~~sh
work=/tmp/ac-r09-ac-proof
mkdir -p "$work"
c++ -std=c++17 -O3 experiments/round05_ak3_orbit_path.cpp -o "$work/orbit-path"
c++ -std=c++17 -O3 experiments/round03_ak3_escape_path.cpp -o "$work/pair-route"
c++ -std=c++17 -O3 experiments/round07_stable_proof_waypoint_search.cpp -o "$work/waypoint"
"$work/orbit-path" 22 XYYXy XYXyxYXYxYXyxy "$work/vertex_left.json"
"$work/orbit-path" 29 XXyxYxyxY XYXyxYXyXYxyxy "$work/product_left.json"
PYTHONPATH=experiments python3 -B - <<'PY' > "$work/destination.tsv"
import sys
from round06_stable_proof_cap23_charts import compact_row
sys.stdout.buffer.write(compact_row(('XXyXYYxyXYY', 'XXYxyyxYXyXYY')))
PY
"$work/waypoint" 36 300000 XXXYXyXyy XYXyyXYYxyy "$work/e20-right" "$work/destination.tsv" > "$work/e20-right.json"
python3 -B experiments/round09_ac_proof_e20_splices.py "$work" "$work/pair-route" "$work" \
  | diff - results/round09_ac_proof_e20_splices.json
python3 -B experiments/round09_ac_proof_e20_intervals.py "$cap30" "$e20_cap36" \
  | diff - results/round09_ac_proof_e20_intervals.json
python3 -B experiments/elementary_verify.py certificates/round09_ac_proof_e20_*_splice.json
~~~
