# Round 07 · Separating a deletion chart from its marked ordinary peak

2026-11-19. Three rank-two projections from the cap-23 rank-three sample have strict stable paths of maximum rank three. Their displayed Whitehead minima have sharp ordinary cyclic entry peak **31** from AK(3). One of the original marked projections has sharp entry peak **37**, even though it is automorphic to a minimum that enters at 31. This compares bounded ordinary reachability within one ordinary component. Stable AC remains open.

## The earlier intrinsic projection already has ordinary ancestry

The round-six rank-three endpoint is `(XzyZYYZxy, XXzYZ, XYXzYZxyy)`. Each of its three rows is primitive. For each row, there is a marking in which it supplies a literal deletion chart and the other two rows project to a member of the exact ordinary cyclic cap-29 component. Round-six Whitehead stages supply the marked changes for the first and third rows. The second row already supplies a literal $y$ chart in the initial marking. [Rank-three endpoint](round-06-stable-proof.md), [three exact anchors](../results/round07_stable_proof_anchors.json).

Two marked rank-two quotients by the same primitive row differ by an ambient automorphism of $F_2$. This follows by identifying both quotients with $F_3$ modulo the normal closure of that row. Panteleev and Ushakov show that ambient automorphisms preserve the ordinary AK(3) component. Thus **every** primitive-chart projection of this particular endpoint belongs to the ordinary AK(3) component. For the intrinsic projection of energy 23, the literal $z$-chart at stage four has pivot `Xz` and pair `(XXYxyyXYxY, XYYxYXyXYxYXy)` in the exact cap-27 component. The final Whitehead map fixes $x$ and sends $y\mapsto yx$ and $z\mapsto zx$. Killing $z$ makes it descend from the chart equation $z=x$ to $x\mapsto x$, $y\mapsto yx$ in rank two, which takes the cap-27 pair to the round-six projection. [Panteleev–Ushakov, Proposition 3.7 and Corollary 3.8](https://arxiv.org/pdf/1609.00325), [word substitution check](../results/round07_stable_proof_anchors.json).

## Shortening strict chart transport

From that endpoint, exhaust all sequences of at most three single-generator left or right multiplications by another signed marked letter, with symbolic rank-three cyclic energy at most 40. There are 1, 24, 392 and 2,926 successive states and 27 signed rank-two projection classes of energy at most 29. Nineteen appear in the exact cap-29 component. Of the eight others, two first appear at depth one, two at depth two, and four at depth three. None has a primitive coordinate. The depth counts concern this specified substitution menu and symbolic cap. [Short chart census](../results/round07_stable_proof_short_charts.json).

Three defining exchanges followed by a literal deletion produce the same round-six energy-23 pair in **1,108,470** strict stable moves, compared with 21,528,218 in its original chart transport. The new trace has maximum rank four, cyclic peak 251 and raw peak 767. One defining exchange and a literal deletion produce `(XXXXXXyxxxYxxy, XXXXyXYxxyxxY)` in **144,955** strict stable moves, maximum rank four, cyclic peak 210 and raw peak 514. This energy-27 pair is outside the cap-29 component, and the earlier argument still gives an ordinary component anchor. Independent stack replay checks both complete traces. These counts refer to the chart-transport construction. [Strict chart and replay receipts](../results/round07_stable_proof_strict_charts.json).

## Checking complete ambient-marking classes

Revisit the 725 signed projection classes from the round-six cap-23 sample. After Whitehead minimization, 415 source classes have minimum cyclic energy above 29. The remaining 310 classes give 96 ambient automorphism orbits. Enumerating the entire cap-29 Whitehead sublevel of these orbits gives 858 signed pairs. Of the 96 ambient orbits, 93 meet the exact cap-29 ordinary catalogue, accounting for 307 source classes. This identifies their ordinary ancestry by Panteleev–Ushakov, even when none of their originally projected markings lay in the ordinary cap-29 catalogue. The three remaining low orbits have Whitehead minimum energies 26, 28 and 29. Whitehead peak reduction makes this finite comparison exact, since each image at energy at most 29 connects to a minimum through the same sublevel. In rank two the type-II conjugation of the one other generator is an inner automorphism and fixes cyclic classes. The search uses all remaining left and right substitutions and quotients by signed permutations. [Whitehead's algorithm](https://www.sciencedirect.com/science/article/pii/B9780080098708500166), [ambient sublevel results](../results/round07_stable_proof_ambient_projections.json).

All three unresolved low orbits have literal deletion charts with actual routes. The fixed rank-three prefixes take 271, 271 and 277 elementary moves at cyclic cap 23. No change of marked basis is needed before deletion. Transport the explicit normal-generation identities through each prefix, use the literal defining row to substitute out its letter in the retained rows, then use the projected proof of the eliminated generator to clear its defining row. Independent replay checks **27,600,129**, **18,790,714**, and **27,778,917** strict stable moves respectively, with maximum rank three and one singleton insertion and deletion in each trace. The full cyclic peaks are 407, 562 and 417. [Three rank-three prefixes](../certificates/round07_stable_proof_literal0_prefix.json), [second prefix](../certificates/round07_stable_proof_literal1_prefix.json), [third prefix](../certificates/round07_stable_proof_literal2_prefix.json), [strict deletion and independent replay receipts](../results/round07_stable_proof_strict_charts.json).

## Sharp ordinary entries for the three minima and one marked chart

The three minimum-energy pairs have complete primitive-free cyclic cap-30 components containing respectively 25, 87 and 13 signed orbits. The independent checker verifies seed reachability and closure under all admissible relative bridges and signed rotations. Each closed component misses the root orbit of AK(3), which has energy 13. At cap 31 exact product paths lead to checked cap-29 ordinary states in 7, 10 and 8 products respectively. The full paths lift to fixed markings and strictly replay in **537**, **472**, and **546** moves, with cyclic peak 31 in each case. Thus 31 is the precise minimum ordinary cyclic peak for entering each of these marked minimum-energy pairs. [Closure and anchor paths](../results/round07_stable_proof_ordinary_peaks.json), [first strict entry](../certificates/round07_stable_proof_entry0.json), [second strict entry](../certificates/round07_stable_proof_entry1.json), [third strict entry](../certificates/round07_stable_proof_entry2.json).

The original marked energy-28 projection of the first orbit is `(XXYxyXYxyxYXy, XXyXYXyxYxyxYxy)`. Its independently checked ordinary cap-36 component consists of 175 signed orbits, is primitive-free, and has minimum cyclic energy 27. At cap 37 eight product edges connect it to a checked cap-29 ordinary state. The full fixed-marking route strictly replays in 540 moves with cyclic peak 37 and raw peak 52. This gives minimum ordinary peak 37 for the original marking. Taking an ambient automorphism of an ordinarily reachable AK(3) pair can therefore change its exact bounded entry peak by six in this example. The stabilized rank-three prefix at cyclic cap 23 is followed by a deletion sequence that reaches cyclic peak 407 in the strict ledger, so its prefix peak cannot be compared as the peak for the full stable connection. [Cap-36 closure and cap-37 bridge](../results/round07_stable_proof_ordinary_peaks.json), [strict ordinary entry](../certificates/round07_stable_proof_entry3.json), [original rank-three chart replay](../results/round07_stable_proof_strict_charts.json).

The unrestricted rank-three singleton-excursion scanner from round six is still running. There is no complete cap-22 result in this report. [Scanner and proof invariant](round-06-stable-proof.md).

## Reproduction

Use the exact cap-27 TSV, the exact compact cap-29 TSV, and the literal partial cap-23 rank-three scan from rounds four and six. The following commands regenerate the bounded chart and ambient-orbit receipts.

~~~sh
work=/tmp/ac-r07-stable
prior=/tmp/ac-r04-stable
c29=/tmp/ac-r05-ak3/c29.orbit.tsv
mkdir -p "$work"
python3 -B experiments/round07_stable_proof_anchor_check.py \
  /tmp/ac-r04-cyclic/c27.tsv "$c29" | diff - results/round07_stable_proof_anchors.json
python3 -B experiments/round07_stable_proof_short_chart.py "$c29" > "$work/chart3.json"
diff "$work/chart3.json" results/round07_stable_proof_short_charts.json
python3 -B experiments/round07_stable_proof_automorphic_charts.py "$prior/exact23.states.tsv" "$c29" \
  > "$work/ambient_projections.json"
diff "$work/ambient_projections.json" results/round07_stable_proof_ambient_projections.json
c++ -std=c++17 -O3 experiments/round06_stable_proof_strict_verify.cpp -o "$work/strict_verify"
for case in 0 4; do
  python3 -B experiments/round07_stable_proof_compile_chart.py "$work/chart3.json" "$case" \
    --write-ledger "$work/short$case.jsonl" > "$work/short$case.json"
  "$work/strict_verify" "$work/short$case.jsonl" > "$work/short${case}_verify.json"
done
c++ -std=c++17 -O3 experiments/round05_stable_proof_route.cpp -o "$work/chart-route"
c++ -std=c++17 -O3 experiments/round03_ak3_escape_path.cpp -o "$work/pair-route"
"$work/chart-route" 23 "$prior/seeds23.tsv" "$work/unanchored0.tsv" 2000000 XXyyxY XYYZyzy XYxZyyZYz
"$work/chart-route" 23 "$prior/seeds23.tsv" "$work/unanchored1.tsv" 2000000 XXXYxyy XXYxzxzxZ XYxzXZy
"$work/chart-route" 23 "$prior/seeds23.tsv" "$work/unanchored2.tsv" 2000000 XXyyxY XYYZyzy XZYzYxZyy
printf '%s\t%s\n' XXXYxyy XXyyxY > "$work/e13.tsv"
"$work/pair-route" 22 "$work/e13.tsv" "$work/e13_route.json"
for case in 0 1 2; do
  python3 -B experiments/round07_stable_proof_unanchored.py "$work/e13_route.json" "$work/unanchored$case.tsv" \
    "$work/ambient_projections.json" "$case" "$work/literal${case}_prefix.json" \
    --write-ledger "$work/unanchored$case.jsonl" > "$work/unanchored$case.json"
  "$work/strict_verify" "$work/unanchored$case.jsonl" > "$work/unanchored${case}_verify.json"
  diff "$work/literal${case}_prefix.json" "certificates/round07_stable_proof_literal${case}_prefix.json"
done
c++ -std=c++17 -O3 experiments/round07_stable_proof_waypoint_search.cpp -o "$work/waypoint"
awk 'length($1)+length($2)<=22' "$c29" > "$work/low22.tsv"
for cap in 30 31; do
  "$work/waypoint" "$cap" 250000 XXYXyxYxyXYxy XYXyXYXyyxYxy \
    "$work/cap${cap}_anchored" "$work/low22.tsv" > "$work/cap${cap}_anchored.json"
  "$work/waypoint" "$cap" 250000 XXXYXyyxYYxyXYYxy XYXyXyxYYxy \
    "$work/minimum28_c$cap" "$work/low22.tsv" > "$work/minimum28_c$cap.json"
  "$work/waypoint" "$cap" 250000 XXXYXyxxYXyyxYxy XXYXyxYxyXYxy \
    "$work/minimum29_c$cap" "$work/low22.tsv" > "$work/minimum29_c$cap.json"
done
for cap in 36 37; do
  "$work/waypoint" "$cap" 250000 XXYxyXYxyxYXy XXyXYXyxYxyxYxy \
    "$work/marked0_c$cap" "$work/low22.tsv" > "$work/marked0_c$cap.json"
done
python3 -B experiments/round07_stable_proof_local_audit.py "$work" "$c29" \
  | diff - results/round07_stable_proof_ordinary_peaks.json
~~~

For the full ordinary fixed-marking replays, generate the four cap-29 signed orbit paths to the anchors printed by the audit. Use `round05_ak3_orbit_path.cpp` and write them as `anchor26.orbit.json`, `anchor28.orbit.json`, `anchor29.orbit.json`, and `anchor_marked0.orbit.json` in that order. Then compile the fixed-marked routes.

~~~sh
for case in 0 1 2 3; do
  python3 -B experiments/round07_stable_proof_compile_join.py prepare "$work" "$case" > "$work/signed_root$case.tsv"
  "$work/pair-route" 22 "$work/signed_root$case.tsv" "$work/signed_root$case.json"
  python3 -B experiments/round07_stable_proof_compile_join.py finish "$work" "$case" \
    --certificate "$work/join$case.cert.json" > "$work/join$case.replay.json"
  python3 -B experiments/elementary_verify.py "$work/join$case.cert.json"
  diff "$work/join$case.cert.json" "certificates/round07_stable_proof_entry$case.json"
done
~~~
