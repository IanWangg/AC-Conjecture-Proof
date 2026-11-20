# Primitive replacements at the cap-33 first exit

Two complete scans of the **1,258,633,777** distinct energy-33 first-exit seeds classify arbitrary-length primitive replacements with the donor fixed and of the given type. Counts are donor-coordinate occurrences. [Boundary provenance](round-14-independent-cyclic32.md#exact-first-exit-deduplication-at-cap-33).

| Standard donor type | Types | Marked keys through width 31 | Occurrences | Primitive replacements |
| --- | ---: | ---: | ---: | ---: |
| Coprime torus relators, 2 ≤ p < q, p + q ≤ 31 | 124 | 6,242 | 1,010,621,864 | 0 |
| Consecutive Baumslag–Solitar relators, 2 ≤ n ≤ 14 | 13 | 228 | 4,137,817 | 0 |

The second count comprises **3,248,527** matches for $n=2$ and **889,290** for $n=3$. Round 14 checked the $n=1$ orbit and found no donor match. Full cap-33 closure remains in progress. [Torus receipt](../results/round15_ak3_torus_atlas.json), [Baumslag–Solitar receipt](../results/round15_ak3_bs_normal.json), [case $n=1$](round-14-bs-first-exit.md).

Both atlases apply Whitehead peak reduction to single cyclic words using signed permutations and signed left and right shears. All standard roots pass the minimality check under these substitutions. Each marked key stores an inverse automorphism checked against the original relator class. Each row at the first exit has width at most 31 because both rows are nonempty and nonprimitive. Each native scan tests both coordinates. [Whitehead's theorem](https://www.sciencedirect.com/science/article/abs/pii/B9780080098708500178), [atlas implementation](../experiments/round15_ak3_torus_atlas.py).

## Coprime torus relation

In the standard marking let $G=\langle x,y\mid x^py^q\rangle$ and $c=x^p=y^{-q}$. The central quotient $G/\langle c\rangle$ is $C_p*C_q$. Define $\chi(x)=q$ and $\chi(y)=-p$. Its restriction to $\langle c\rangle$ is injective since $\chi(c)=pq$. Two elements of $G$ are conjugate precisely when their cyclic normal forms in $C_p*C_q$ are conjugate and their $\chi$ values agree. A lift of any quotient conjugator leaves a difference in $\langle c\rangle$, and equality of characters forces that difference to be the identity.

Unimodularity of the exponent vectors gives $|\chi(s)|=1$ for the other row $s$. Invert $s$ if needed. Choose positive words $u,w$ whose exponent vectors sum to $(p,q)$ and have characters $1,-1$ respectively. The atlas chooses cyclic representatives beginning in $x$ and ending in $y$ and checks by Stallings folding that $u,w$ form a basis. Set $v=uw$. The exponent vectors of the primitive classes of character $1$ are exactly those of $uv^j$ and $(wv^j)^{-1}$ for integers $j\ge0$. These words are primitive because $(u,v)$ and $(w,v)$ are bases. Uniqueness of the rank-two primitive conjugacy class for a signed exponent vector gives exhaustiveness. [Rank-two primitive enumeration](round-10-ac-proof.md).

The words $u,w,v$ each start in $x$, end in $y$, and have each generator run shorter than its order in $C_p*C_q$. Their projected syllable counts therefore add under the displayed products. For each family, the cyclic syllable count of $s$ determines at most one possible $j$. The scan rotates the candidate syllables to test equality of cyclic signatures. All tested occurrences had character of absolute value one. [Native torus test](../experiments/round15_ak3_torus_scan.cpp).

The native fixture finds a primitive replacement from the nonprimitive pair `(xxyyy,yxxxyyy)`. Independent strict replay reaches `(x,y)` in **109** ordinary instructions at raw peak **31**. [Strict certificate](../certificates/round15_ak3_torus_control.json).

## Consecutive Baumslag–Solitar indices

Use the marking $y x^n y^{-1}=x^{n+1}$ and height $\exp_y$. The other row of a normally generating pair has height of absolute value one. The free primitive classes at height $\pm1$ have representatives $x^k y^{\pm1}$ over all integers $k$. In the quotient they are conjugate to $y^{\pm1}$, using $x^{n\ell}y x^{-n\ell}=x^{-\ell}y$ and inversion.

A quotient word at either height is conjugate to $y^{\pm1}$ exactly when its cyclically Britton-reduced stable-letter count is one. Cyclically reduced stable-letter length is invariant under conjugacy of positive-length HNN forms. The identity above applies to the single remaining stable letter and coefficient. The native implementation removes each opposite-sign pinch with its exact subgroup divisibility test, including pinches across the cyclic seam. [Native cyclic HNN test](../experiments/round15_ak3_bs_normal.cpp).

The first actual $n=3$ match can be read as `(xxxxyXXXY, x^19 yxxYY)`. In the standard marking the receiver has three cyclic stable letters and opposite-sign pinch residues $2\pmod 3$ and $3\pmod 4$. The separate $n=2$ fixture reports a hit, and independent strict replay reaches `(x,y)` in **67** instructions at raw peak **40**. [Strict certificate](../certificates/round15_ak3_bs_family_control.json).

## Reproduction

Set `work` to a writable directory and `compacted` to the directory containing the 128 `unique.*.bin` files regenerated from the Round 14 boundary report. The torus sweep checks the number of processed rows against the byte lengths of its disjoint shard assignments. Both native controls report a hit before the full scan.

~~~sh
python3 -B experiments/round15_ak3_torus_atlas.py "$work/torus31.tsv" \
  --control "$work/torus-control.json" "$work/torus-control.bin"
c++ -std=c++17 -O3 -pthread experiments/round15_ak3_torus_scan.cpp -o "$work/torus-scan"
"$work/torus-scan" "$work/torus31.tsv" "$work/torus-control.bin"
python3 -B experiments/round15_ak3_torus_sweep.py \
  "$work/torus-scan" "$work/torus31.tsv" "$compacted" "$work" 6
python3 -B experiments/round15_ak3_bs_family_atlas.py "$work/bs31.tsv" \
  --control "$work/bs-control.json" "$work/bs-control.bin"
c++ -std=c++17 -O3 -pthread experiments/round15_ak3_bs_normal.cpp -o "$work/bs-normal"
"$work/bs-normal" "$work/bs31.tsv" "$work/bs-control.bin"
"$work/bs-normal" "$work/bs31.tsv" "$compacted"/unique.*.bin
python3 experiments/elementary_verify.py "$work/torus-control.json" "$work/bs-control.json"
~~~
