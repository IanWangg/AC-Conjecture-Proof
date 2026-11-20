# Round 15 · Four alternating ordinary receiving blocks

2026-11-19. From the two strictly reached energy-20 AK(3) pairs, a genuine four-block search produces **27,877** last-block contacts with the energy-56 one-shear archive. All those contacts fail at arbitrary last-block length. The earlier block menus have the bounds below. Separately, **1,319** exact second-product endpoints through cyclic energy 38 give no primitive coordinate after any one ordinary product in either receiving slot. [Round 14 archive](round-14-ak3.md), [four-block receipt](../results/round15_ak3_four_blocks34.json), [primitive scan](../results/round15_ak3_primitive_product38.json).

## Four changing receiving blocks

For a marked pair `(r,d)` and an archived pair `(s,e)`, the search tests

~~~text
(r,d) → (h,d) → (h,f) → (s,f) → (s,e).
~~~

Each row changes cyclic class when it is the receiver. The 91 first choices combine the 71 short choices of Round 13 and the 20 additional exact sheared choices of Round 14. The second block uses a single ordinary product and arbitrary shortest conjugating bridges subject to a bound of 34 on the cyclic length sum at its endpoint. Native and independent string menus agree on 215 distinct ordered pairs `(h,f)`. The first choice that realizes each `(h,f)` suffices for testing the later blocks. [First-choice receipt](../results/round15_ak3_first_choices.json), [complete menu construction](round-13-ak3.md#primitive-targets-in-the-third-block).

The third block freezes `f` and tests all 421,750 donor keys of the 1,012,360-pair sheared atlas that meet the determinant condition and change the other cyclic class. Across all 215 charts the determinant filter leaves 12,510,492 word checks and 350 word hits. Of those charts, 211 complete at stage two and four at stage three, with allocation cap 450,000. Each hit `s` gives all archived partners `e` paired with `s` other than `f`. The fourth block freezes `s` and tests whether it can replace `f` by `e`. In reverse, the 363 charts test 27,877 contacts with no hits through the completed stages. The control uses six distinct cyclic classes and replays to the basis in 3,493 strict instructions, including four changing segments of lengths 121, 3, 49 and 7. Its cyclic and raw peaks are both 358. [Search and strict replay](../experiments/round15_ak3_four_blocks.py).

## Exact fourth-block exclusions

A single frozen donor block requires conjugacy of the receiver and target up to inversion after killing that donor. Verified permutation images in symmetric groups of degree at most ten exclude 27,871 contacts by cycle type. The compact receipt saves 28 marked homomorphisms and reconstructs the individual contact checks from the two word lists at each frozen donor. Replaying the mod-3 Fox systems of Round 14 excludes two further contacts in the rank-ten free-by-cyclic quotient and three in the rank-six quotient. [Permutation runner](../experiments/round15_ak3_four_separators.py), [independent replay and retained Fox certificates](../experiments/round15_ak3_four_audit.py), [Round 14 Fox argument](round-14-ak3.md#exact-two-block-tests).

The final contact has frozen donor `XXYxxYxxYxxyXXy`, receiver `XXYxxyXXyXYYxxy` and target `XXXYxxy`. After the shear `y → yxx`, the donor is cyclically equivalent, up to inversion, to `XXYYYxxyy`. Write $a=y$ and $t=x^2$. The quotient is the amalgam

$$
\langle x\rangle *_{\langle x^2\rangle=\langle t\rangle}
\langle a,t\mid t^{-1}a^3t=a^2\rangle .
$$

The Baumslag–Solitar factor maps onto an affine group by sending $a$ to translation by 1 and $t$ to multiplication by $3/2$. The generator $t$ has infinite order, so its affine image can serve as the edge subgroup in a further amalgam quotient. Both marked rows can be cyclically rotated to have first factor $x^{-1}$, followed by a Baumslag–Solitar factor whose translation is nonzero. For the receiver the second factor is `ATAtaTAtaa`, with affine pair $(2/3,0)$. For the target it is `TTAtat`, with pair $(2/9,0)$. Uppercase letters denote inverses and the second coordinate is the exponent of the scaling. These are cyclically reduced length-two forms in the affine amalgam. Conjugacy of the rows up to inversion would require their affine factors to have the same $\langle t\rangle$ double coset up to inversion. Left and right multiplication by powers of $t$ and inversion preserve $v_2(b)+v_3(b)$ for every nonzero translation $b$. The two sums differ by 1, excluding this last contact. [Magnus, Karrass and Solitar, *Combinatorial Group Theory*, Theorem 4.6](https://books.google.com/books/about/Combinatorial_Group_Theory.html?hl=en&id=mIMpAQAAMAAJ).

## Unbounded single-product primitive test

Running the independent second-product menu at cap 38 gives 1,319 distinct marked pairs after 63,184 rotation and bridge checks. The existing primitive slope scanner tests both slots for any ordinary single product taking that coordinate to a primitive row, with arbitrary conjugating bridge and no final energy bound. It completes all 1,319 pairs with no hit. The earlier first and second choices stay fixed for this conclusion. [Native primitive scanner](../experiments/round12_ak3_primitive_step.cpp), [independent driver](../experiments/round13_ak3_exact_center.py).

## Reproduction

Use the replayed reverse TSV and adjacent source index, the original archive directory, and the binaries named below. Build each native tool with `c++ -std=c++17 -O3`, adding `-pthread` for the primitive scanner. [Archive provenance](round-04-ak3.md#reproduction), [targeted completion](../experiments/round11_ak3_targeted_acm.cpp), [indexed completion](../experiments/round12_ak3_chart_index.cpp), [native second product](../experiments/round13_ak3_exact_center.cpp), [native permutation search](../experiments/round14_ak3_permutation_contacts.cpp).

~~~sh
python3 -B experiments/round15_ak3_four_blocks.py \
  "$work/targeted" "$work/index" "$work/exact-center" "$reverse" "$archives" \
  results/round13_ak3_three_blocks_short.json results/round14_ak3_sheared_reciprocal.json \
  --middle-energy 34 --control-ledger "$work/control.json" > "$work/four34.json"
python3 -B experiments/elementary_verify.py "$work/control.json"
python3 -B experiments/round15_ak3_four_separators.py "$work/permutations" "$work/four34.json" \
  --degree 10 > "$work/perm34.json"
python3 -B experiments/round15_ak3_four_audit.py "$work/four34.json" \
  --permutations "$work/perm34.json" > "$work/packed34.json"
python3 -B experiments/round15_ak3_four_audit.py results/round15_ak3_four_blocks34.json
python3 -B experiments/round13_ak3_exact_center.py "$work/exact-center" "$work/primitive-step" \
  results/round15_ak3_first_choices.json --energy 38
~~~
