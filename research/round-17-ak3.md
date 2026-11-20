# Constructive tests from five ordinary energy-20 minima

The ordinary cap-36 component based at E22 contains these five cyclic energy-20 pairs. Its connectedness and the strict ordinary path from AK(3) to E22 make each pair an ordinary waypoint. [Exact entry and verified component](round-17-cyclic-peak-gap.md).

| First row | Second row |
| --- | --- |
| `xxxyxYxYY` | `xyxYYxyyXYY` |
| `xxxyxYxYY` | `xyxYYYxyyXY` |
| `xxxyyXXYY` | `xyxYYxyyXYY` |
| `xxxyyXXYY` | `xyXYYxyyxYY` |
| `xxyxYxxyy` | `xyyxYYXyyxY` |

## Both frozen directions

All ten choices of a frozen coordinate exclude a primitive replacement at arbitrary length. For eight directions, choose a basis $(u,v)$ with $[u]$ equal to the receiver exponent vector and $[v]$ equal to the donor exponent vector. The independent fold checks that each pair is a basis. Primitive candidates are conjugate up to inversion to $uv^n$ for $n\in\mathbb Z$. A marked permutation homomorphism killing the donor permits only those residues of $n$ for which the receiver and $uv^n$ have the same cycle type. The combined periods are at most 60. In these eight directions the intersections are empty. The finder retains a positive slope in the torus control and excludes the known external energy-24 negative control. [Period witnesses](../results/round17_ak3_minima_slopes.json), [primitive slope criterion](round-14-ac-disproof.md).

The remaining two directions have frozen row `xxxyyXXYY`, which after exchanging the ambient generators is a cyclic conjugate of the inverse of `xxyyXXYYY`. Introduce $t=x^2$ and $a=y$ in that marking, so the quotient is the root-adjoined $\mathrm{BS}(2,3)$ amalgam from Round 16. Both receivers of height one have cyclically reduced alternating length two and their inner coefficients fail the exact $t$-power test for conjugacy to any $xa^j$. The recomputation tests the entire infinite family using the linear Britton-reduced length. [Exact criterion](round-16-root-bs-first-exit.md), [two additional exclusions](../results/round17_ak3_minima_contacts.json).

## Reciprocal archive contacts

With the original **23,902** verified archive pairs, the 10 forward orderings make **242,847** determinant-compatible word checks. Seven forward hits produce 22 contacts across 14 reverse charts. The forward charts all complete stage three. The bounded reverse charts have zero joins. The two strict positive controls replay to the basis in **213** and **245** elementary instructions. [Reciprocal chart receipt](../results/round17_ak3_minima_contacts.json).

All **22** retained contacts also fail at arbitrary last-block length. Six use verified symmetric homomorphisms of degree at most nine. The remaining 16 share the frozen row `XXXyyxxYY`, the same signed cyclic class as `xxxyyXXYY`. In the quotient where $t$ acts by $3/2$ and $a$ acts by translation by one, normalize a cyclically reduced height-one receiver to $x\beta$, with $\beta$ of inner height zero. If two such words are conjugate, the translation parameters of their inner coefficients differ by multiplication by a power of $3/2$. Both reached rows have translation $-4/3$ with sum of 2-adic and 3-adic valuations equal to 1. Twelve contacts have archived coefficient $\pm7/3$ or $\pm11/3$ with valuation sum $-1$. The remaining four use `XXY` or `XXy` as the archived receiver. Each is conjugate to a primitive in the original root-adjoined quotient, whereas neither reached row is. All these tests concern the final frozen block after the stated forward menu. [Witnesses and independent replay](../experiments/round17_ak3_minima_contacts.py).

## Alternating product menus through cap 40

All changing products from the five minima through cap 40 give 160,372 distinct ordered marked states in the first menu. The second menu changes the previously frozen row and gives 45,713 raw outputs. The union has **206,077** distinct ordered marked states. There is no primitive coordinate in this union, and no single ordinary product in either slot exposes a primitive. The complete width-31 quotient atlases find zero torus donors and zero standard consecutive Baumslag–Solitar donors in the output menus. They find **49,890** root-adjoined Baumslag–Solitar donor occurrences, for which the exact fixed-donor primitive criterion is negative in every case. The menu bounds concern the first two products. The terminal tests allow arbitrary output length and, in the root-adjoined tests, arbitrary fixed-donor block length. [Product and quotient receipts](../results/round17_ak3_minima_menu40.json).

The ordinary AK(3) trivialization remains open. The cap-38 extension of the Round 16 four-block archive search did not produce a completed receipt. Its earlier session ended after reporting 1,319 middle states, before the third-chart results were written.

## Reproduction

Use the native executables and width-31 atlases from Rounds 13–16, and an archive TSV with its source index. [Archive and previous tools](round-15-ak3.md#reproduction), [atlas builds](round-15-quotient-first-exit.md#reproduction), [root-adjoined implementation](round-16-root-bs-first-exit.md).

~~~sh
c++ -std=c++17 -O3 experiments/round17_ak3_periodic_slope.cpp -o "$work/slope"
python3 -B experiments/round17_ak3_minima_slopes.py "$work/slope" \
  | diff -u results/round17_ak3_minima_slopes.json -
head -5 "$work/e22-cap36.tsv" > "$work/minima.tsv"
python3 -B experiments/round12_ak3_reciprocal_charts.py \
  "$work/index" "$work/targeted" "$work/minima.tsv" "$reverse" \
  --forward-energy 20 --depth 4 --allocation 900000 --archives "$archives" \
  > "$work/minima-reciprocal.json"
python3 -B experiments/round17_ak3_minima_contacts.py \
  "$work/minima-reciprocal.json" "$reverse" "$work/permutations" "$work/root-bs" \
  | diff -u results/round17_ak3_minima_contacts.json -
python3 -B experiments/round17_ak3_minima_menu.py "$work/exact-center" "$work/primitive-step" \
  "$work/torus-scan" "$work/torus31.tsv" "$work/bs-normal" "$work/bs31.tsv" \
  "$work/root-bs" "$work/root-bs31.tsv" | diff -u results/round17_ak3_minima_menu40.json -
~~~
