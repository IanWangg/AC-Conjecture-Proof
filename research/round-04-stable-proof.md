# Round 04 · Sharp loss of the marked rank-three pivot

2026-11-19. The least cyclic peak needed to reach a rank-three state of the one-pair stabilization of AK(3) with no one-occurrence pivot for the marked auxiliary generator is **22**. A 247-move elementary certificate reaches such a state. This is a threshold for applying the preceding projection criterion, and leaves stable triviality unresolved. [Strict certificate](../certificates/round04_stable_proof_pivotless22.json), [cap-21 exclusion](round-03-stable-proof.md).

## Exact seeding and the witness

Start at \((xxxYYYY,xyxYXY,z)\) in \(F(x,y,z)\), with capital letters denoting inverses. A singleton sector keeps a relator conjugate to \(z\) up to sign. Its projection deletes that row and sets \(z=1\) on the others. The rank-two cap-21 component is exactly the set of projections obtainable before first leaving the rank-three singleton sector at cap 22. The forward implication is the singleton projection argument of round 03. In the other direction, every lift of an obtainable projection within the cap is obtainable: if a cyclic representative reads \(Az^\epsilon B\), multiplication by \(B^{-1}z^{-\epsilon}B\) from the singleton row changes it to \(AB\). This operation and the surrounding donor normalization do not increase cyclic length. Remove all auxiliary occurrences from the lift, normalize the projected words using inversions and conjugations, and reverse. [Full rank-two cap-21 certification](research-p-cyclic21-review.md).

Use the earlier weighted restriction \(2|\bar r|+|\bar s|+1\le 22\) on the projected donor and other row at the first exit. The implementation considers 476 projected ordered pairs, 78,316 singleton lifts within the relevant slack, and 48,096 distinct first exits. It includes reversal of cyclic cancellations after deleting \(z\), which can occur with the extra slack at cap 22. Each generated start is reachable, by the preceding argument and the actual cyclic product that produces it. [Seeding and scan counts](../results/round04_stable_proof_excursions.json).

For the displayed witness there are 17 rank-two product edges, with an isolated \(z\), to the canonical pair \((XXXXYYY,XYxYXy)\). The first exit has canonical rows \((XXXXYYY,XXXXYYYZ,XYxYXy)\). Seven more cyclic product edges give a state with two or three \(z^{\pm1}\) occurrences in each row involving \(z\). The exact free-word replay ends at \((XYYZZZY,XYxYXy,XXYYZZY)\), has cyclic peak 22 and raw peak 28, and first becomes pivotless at elementary step 235. The cap-21 audit supplies the matching lower bound. A cyclic word with no one-occurrence \(z\) pivot cannot define \(z\) as an old-generator word by free reduction and cyclic conjugation. The certificate targets this specific marking. [Elementary replay](../experiments/round04_stable_proof_paths.py).

## Partial excursions and the short rows

The cap-22 searches are partial. The literal search stops at 2,000,000 distinct states and finds 5,431 pivotless states. The larger search uses the 16 signed basis actions that permute and invert \(x,y\) and independently invert \(z\). All eight signed \(x,y\) images of the initial rank-two pair belong to the certified cap-21 component, which proves that these actions preserve the seed family and the bounded reachable graph. The search expands one representative per orbit. The 2,000,000-orbit stop covers 31,989,768 distinct discovered states, including 345,416 pivotless states. Both scans observe 432 singleton reentry projections and every one is in the rank-two cap-21 component. This check is limited to the received reentries. [Scan counts and scope](../results/round04_stable_proof_excursions.json).

In the signed scan the only length-two representative rows are \(Xz,Yz\). A unimodular exponent matrix rules out powers in length two. All short-row projections by eliminating \(z\) give 640 distinct rank-two pairs in the audited cap-26 component. None has a primitive coordinate, and none of their 2,444 signed images matches the 16,943 known-trivial reverse pairs through energy 44. Eliminating the old letter in a length-two relation instead gives exactly the same projection up to signed renaming of the two surviving letters. The scan also checks the 443 distinct \(z\)-free displayed words and finds no primitive. [Short pivot screen](../results/round04_stable_proof_short_pivots.json), [rank-two primitive test](round-03-cyclic26.md), [energy-44 archive](round-02-ak3.md).

## A free-cyclic block screen for the literal prefix

Among the 5,431 pivotless states in the literal prefix, there are 9,638 distinct two-row blocks. **None has infinite cyclic quotient.** The proof uses the following necessary cyclic-cover criterion. The exponent rows form a primitive rank-two sublattice, since they complete to a unimodular triple. Let \(v\) be their cross product and \(R=\mathbb{Z}[t,t^{-1}]\). The rank-three presentation of the block has a map to \(\mathbb Z\) with weights \(v\). For the cyclic cover, the first boundary row is \(d_1=(t^{v_i}-1)_i\), and the second boundary columns contain the two evaluated Fox gradients. Write \(h=d_1/(t-1)\). The entries of \(h\) generate the unit ideal by \(\gcd(v_i)=1\) and the Laurent-polynomial Euclidean telescoping identity. Thus \(h\) admits a splitting column. If the quotient is cyclic, the cover has trivial first homology, so the two gradient columns span \(\ker h\). Appending a splitting column gives an invertible \(3\)-by-\(3\) matrix over \(R\). Its cofactor identities force each \(2\)-by-\(2\) minor to equal the corresponding \(h_i\) times a unit \(\pm t^k\), up to sign. The script chooses a nonzero \(v_i\) and checks the full integer Laurent polynomial minor.

This excludes 9,582 blocks. The 56 survivors have five signed-basis orbits. Four admit explicit nonabelian images in \(S_5\), with both block words evaluating to the identity. The remaining representative is \((XXYZYXz,XYxYXy)\). The second word becomes a standard braid relation after inverting \(y\) and reading its signed cyclic class. The first word specifies the HNN relation \(z^{-1}(xy)^{-1}z=yx^2\) over that braid group. Both associated elements have infinite order. The first has an integral determinant-one matrix image whose trace is 3, and the second has exponent 1 under \(x\mapsto 1,\ y\mapsto-1\) in the braid group abelianization. The HNN normal-form theorem embeds the nonabelian braid group in the block quotient. This excludes the last orbit, independently of any thickening test. [Exact Fox and quotient witnesses](../results/round04_stable_proof_pivotless_blocks.json), [screen and checks](../experiments/round04_stable_proof_blocks.py).

## Reproduction

Generate the cap-26 TSV following the [preceding report](round-03-cyclic26.md) and the energy-44 reverse TSV following the [archive audit](round-02-ak3.md). In the following commands the cap-22 scans intentionally return exit code 2 after saving their partial data.

~~~sh
work=/tmp/ac-r04-stable
mkdir -p "$work"
python3 -B experiments/cyclic_catalogue_to_tsv.py certificates/cyclic21_component.json.gz.b64 "$work/c21.tsv"
python3 -B experiments/round04_stable_proof_seeds.py prepare "$work/c21.tsv" 22 "$work/seeds22.tsv"
c++ -std=c++17 -O3 experiments/round04_stable_proof_excursions.cpp -o "$work/excursions"
"$work/excursions" 22 "$work/seeds22.tsv" "$work/literal22" 2000000 > "$work/literal22.json"
"$work/excursions" 22 "$work/seeds22.tsv" "$work/sym22" 2000000 --signed-symmetries > "$work/sym22.json"
printf 'XXXXYYY\tXYxYXy\n' > "$work/rank2-target.tsv"
c++ -std=c++17 -O3 experiments/round03_ak3_escape_path.cpp -o "$work/rank2-path"
"$work/rank2-path" 21 "$work/rank2-target.tsv" "$work/rank2-path.json"
python3 -B experiments/round04_stable_proof_paths.py compile "$work/rank2-path.json" "$work/literal22.route.tsv" "$work/pivotless.json"
diff certificates/round04_stable_proof_pivotless22.json "$work/pivotless.json"
python3 -B experiments/round04_stable_proof_blocks.py "$work/literal22.states.tsv" --pivotless-only --with-witnesses \
  | diff - results/round04_stable_proof_pivotless_blocks.json
python3 -B experiments/round04_stable_proof_seeds.py short-pivots "$work/sym22.states.tsv" /tmp/ac-r03-cyclic/c26.tsv \
  --reverse /tmp/round02-ak3/reverse44.tsv | diff - results/round04_stable_proof_short_pivots.json
~~~
