# Round 09 · Ordinary entries for low-energy stable projections

2026-11-19. Twelve short rank-two projections from the cap-22 rank-three catalogue have ordinary AC paths from AK(3). Eleven have sharp ordinary cyclic entry peak **37**. One strict ordinary ledger ends at exactly the same marked pair as the stable track's independently replayed rank-three ledger. The twelfth projection is ordinarily reachable by a verified combination of ambient automorphisms and cyclic products. Its least ordinary peak remains unknown. [Exact ordinary ledger](../certificates/round09_ak3_e20_ordinary.json), [finite witnesses](../results/round09_ak3_whitehead_products.json).

## A marked endpoint shared by stable and ordinary paths

The source signed projection was `(XXXYYXYXy, XYYXyXYYxyy)`. Inverting the ambient letter $x$ and normalizing the two cyclic words gives the exact stable endpoint

~~~text
XXXYXyXyy    XYXyyXYYxyy
~~~

The strict rank-three prefix to the chart uses 544 moves and has cyclic peak 22. Realizing the actual deletion marking and removing the isolated generator gives the same displayed pair in the 1,871-move strict stable replay, of maximum rank three. The ordinary ledger reaches that literal endpoint in **1,274 moves**, with raw peak 50 and cyclic peak **37**. [Rank-three prefix and signed chart](../results/round09_stable_proof_e20_rank3.json), [strict stable ledger](../certificates/round09_stable_proof_e20_stable.jsonl), [ordinary replay and orbit route](../results/round09_ak3_e20.json).

The entire ordinary cap-36 component of that pair has **265,026 signed orbits**. An independent stack-reduction checker verifies closure and connectivity over 514,401,544 candidate products, including 14,820,320 admitted products. Its least energy is 20, above the AK(3) energy 13. The independent primitive scan finds zero single-sign coordinates. At cap 37, a 32-product route joins the energy-25 pair `(xxxyxxyXYxy, xxxyxYXyxxyxxy)` in the verified cap-29 component. A second search supplies a 40-product cap-29 path from the AK(3) signed orbit. Align the signed marking by a cap-22 path and lift both product segments to elementary moves. The disjoint cap-36 component and the replay at 37 establish sharpness. [Independent counts and complete signed route](../results/round09_ak3_e20.json), [cap-29 enclosure](round-06-cyclic29.md).

Ten further charts from the first twelve short unanchored sources of the stable track have their exact signed projection keys in this cap-36 component. Each therefore has the same sharp ordinary peak 37. The recorded strict ledger is for the displayed endpoint. [Projection list and membership](../results/round09_ak3_whitehead_products.json), [source chart census](../results/round09_stable_proof_c22_energy16_anchors.json).

## Complete product menus at selected Whitehead minima

For a pair of cyclic conjugacy classes, enumerate all nonincreasing rank-two Whitehead transvections up to signed ambient symmetries. First descend in joint cyclic length. Then traverse the entire equal-length plateau of the minimum. Rank-two Whitehead peak reduction identifies this plateau with the signed markings of the minimal class. For each chosen class, use the complete ordinary cyclic product menu at **every** marking in that plateau to permit one product up to cyclic cap 36. Minimize each product endpoint and retain classes of minimum energy at most 27. After each layer expand at most 128 newly reached classes in increasing minimum energy order. The original seed classes may be above the retention threshold. The beam bounds the number of expanded classes, while each selected marking has a complete product menu including arbitrary tails via the shortest-bridge reduction. [Cap-30 product and arbitrary-tail argument](round-08-cyclic30.md), [native menu](../experiments/round09_ak3_whitehead_products.cpp).

Eight established ordinary endpoints from Round 08 represent six distinct minimal classes. Across five layers their menus produce **70,878** distinct retained or seed classes and no primitive product. Independent tests find a planar-link parity obstruction for all 5,488 of these classes through energy 23. None of those 5,488 has an arbitrary-tail join to the 23,902 known-trivial reverse pairs.

The twelve stable projections represent nine minimal seed classes. Four layers produce **2,023** classes with zero primitive products. Independent planar-link parity checks exclude all 2,023 minimized diagrams, and the reverse archive again gives no join. The positive control starts from `(XXYxY, XYxyy)`, with both coordinates independently nonprimitive, and gives two primitive products in its first selected menu. [Beam counts, independent primitive and parity tests](../results/round09_ak3_whitehead_products.json).

Eight of the stable beam's generated minima are in the verified ordinary cap-30 component. All eight trace to the sole initial chart outside the shared cap-36 component, namely `(XXyxYYYXyxY, XYxYxyyXy)`. Two paths use three cyclic products, and six use four. The receipt independently checks every marked product and all of the intermediate Whitehead transformations along these paths. The shortest target is `(xxyXYxxyXYY, xyxYxyXYYXy)`. By ambient invariance of the ordinary AK(3) orbit, the automorphism and product paths from this cap-30 target to the initial chart give ordinary equivalence. Compiling the ambient transformations into elementary ordinary moves can raise the peak above the tested product cap. The least ordinary peak for this projection remains open. [Panteleev and Ushakov, Corollary 3.8](https://arxiv.org/abs/1609.00325), [verified mixed paths](../results/round09_ak3_whitehead_products.json).

## Reproduce

~~~sh
work=/tmp/ac-r09-ak3
cap30=/tmp/ac-r07-ak3/c30.orbit.tsv
reverse=/tmp/round02-ak3/reverse56.tsv
mkdir -p "$work"
python3 -B experiments/round09_ak3_beam_audit.py seeds "$work"
awk 'length($1)+length($2)<=26' "$cap30" > "$work/c30le26.tsv"
c++ -std=c++17 -O3 experiments/round07_stable_proof_waypoint_search.cpp -o "$work/waypoint"
c++ -std=c++17 -O3 -pthread experiments/round07_ak3_wide_verify.cpp -o "$work/wide-verify"
c++ -std=c++17 -O3 experiments/round05_ak3_orbit_path.cpp -o "$work/orbit-path"
c++ -std=c++17 -O3 experiments/round03_ak3_escape_path.cpp -o "$work/literal-path"
for cap in 36 37; do
  "$work/waypoint" "$cap" 1400000 XXXYYXYXy XYYXyXYYxyy "$work/e20x$cap" "$work/c30le26.tsv" > "$work/e20x$cap.json"
done
"$work/wide-verify" 36 6 "$work/e20x36.tsv" "$work/e20x36.audit.json" XXXYYXYXy XYYXyXYYxyy
python3 -B experiments/round05_ak3_orbit_audit.py primitive "$work/e20x36.tsv" > "$work/e20x36.primitive.json"
"$work/orbit-path" 29 xxxyxxyXYxy xxxyxYXyxxyxxy "$work/e20anchor.orbit.json"
python3 -B experiments/round09_ak3_e20.py "$work" "$work/literal-path" "$work/e20.cert.json" \
  | diff - results/round09_ak3_e20.json
cmp "$work/e20.cert.json" certificates/round09_ak3_e20_ordinary.json

c++ -std=c++17 -O3 experiments/round09_ak3_whitehead_products.cpp -o "$work/whitehead-products"
"$work/whitehead-products" 36 27 5 128 "$work/ordinary-seeds.tsv" "$work/minordinary.tsv" "$work/edgesordinary.tsv" > "$work/minordinary.json"
"$work/whitehead-products" 36 27 4 128 "$work/targets.tsv" "$work/minstable.tsv" "$work/edgesstable.tsv" > "$work/minstable.json"
printf 'XXYxY\tXYxyy\n' > "$work/control-seed.tsv"
"$work/whitehead-products" 16 14 2 8 "$work/control-seed.tsv" "$work/control.tsv" "$work/control.edges.tsv" > "$work/control.json"
awk 'length($1)+length($2)<=23' "$work/minordinary.tsv" > "$work/minordinary.low23.tsv"
c++ -std=c++17 -O3 experiments/round06_ak3_orbit_index.cpp -o "$work/orbit-index"
for stem in minstable minordinary.low23; do
  python3 -B experiments/round01_geometric_archive.py "$work/$stem.tsv" > "$work/$stem.geometry.json"
  "$work/orbit-index" "$work/$stem.tsv" "$reverse" "$work/$stem.reverse56.json"
done
python3 -B experiments/round09_ak3_beam_audit.py audit "$work" --cap30 "$cap30" \
  | diff - results/round09_ak3_whitehead_products.json
~~~
