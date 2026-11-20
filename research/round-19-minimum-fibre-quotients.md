# No primitive replacement with either row of the new energy-17 pair fixed

The sharp cap-33 waypoint `(xxyXYY, xxxxYxYxYXY)` has no primitive replacement in either fixed-donor direction, with no bound on the number of products or the length of the output. Each deletion quotient is free-by-cyclic. Twisted conjugacy in finite Magnus algebras rules out every primitive slope for the first donor. For the second donor it combines with a permutation witness to rule out every slope. [Sharp ordinary entry](round-18-cyclic33.md), [full arithmetic and dual certificates](../results/round19_ak3_minimum_fibre_quotients.json).

## Exact fibre markings

Write $u,t$ for the new free generators, with $t$ the height generator and $u_i=t^iut^{-i}$. For the first donor substitute $x=ut$, $y=t$. The relator is $u_0u_1u_2^{-1}$, so its fibre is free of rank two on $u_0,u_1$, with shift $(u_0,u_1)\mapsto(u_1,u_0u_1)$.

For the second donor use $x=ut^{-4}$ and $y=t^{-1}ut^{-4}$. The inverse marking is $t=xy^{-1}$ and $u=x(xy^{-1})^4$. The relator rewrites as $u_0u_{-4}u_{-8}u_{-5}^{-1}u_{-1}^{-1}$. Both extreme indices appear once. Eliminating the upper index gives a free fibre on $u_{-8},\ldots,u_{-1}$, and eliminating the lower index gives the inverse shift. Thus the second fibre has rank eight. The replay verifies both original markings, the relator and the shift inverse. [Indexed words and class-two tests](../experiments/round19_ak3_minimum_class_two.py).

In each marking the other row has height one and can be written $Rt$. Every free primitive class of height one has a cyclic representative $u^kt$ for some integer $k$. A fixed-donor primitive replacement requires conjugacy of $Rt$ to one of these representatives in the deletion quotient. A conjugator can be chosen at height zero by multiplying it by a suitable power of the height-one element that it conjugates. The conjugacy equation is then $gR=u^k\phi(g)$ in the fibre. [Fixed-donor conjugacy criterion](round-10-ac-proof.md#exact-block-criteria).

## Complete slope exclusions

Map the fibre generators to $1+X_i$ in the characteristic-two noncommutative Magnus algebra, truncated by degree. The constant-one units include every free conjugator image. The equation is linear in the nonconstant coefficients of $g$. The image of $u$ has finite order, so each test covers all integers $k$ by enumerating one period. For each rejection, the code computes and checks a linear functional killing every coefficient column and taking value one on the inhomogeneous right-hand side. The small rank-two degree-two control also enumerates the entire unit group to check the linear solver.

| Fixed donor | Fibre rank | Degree | Slope period | Surviving residues |
| --- | ---: | ---: | ---: | --- |
| `xxyXYY` | 2 | 2 | 4 | 1, 2 |
| `xxyXYY` | 2 | 4 | 8 | 1, 2 |
| `xxyXYY` | 2 | 6 | 8 | none |
| `xxxxYxYxYXY` | 8 | 2 | 4 | 0, 1, 2, 3 |
| `xxxxYxYxYXY` | 8 | 3 | 4 | 1 |
| `xxxxYxYxYXY` | 8 | 4 | 8 | 1, 5 |

For the rank-eight fibre, the degree-seven permutation marking from Round 18 uses the same $u,t$. It kills the donor and allows only residues **0 and 3 modulo 4** by cycle type. Its intersection with residue 1 from the degree-three Magnus test is empty. Class-two finite fibre quotients alone meet the rank-two modulo-four condition but leave the rank-eight slope open. [Prior permutation witness](../results/round18_ak3_c33_minimum.json), [Magnus solver](../experiments/round19_ak3_minimum_magnus.py).

## All nine energy-17 additions

Every one of the nine cap-33 minima has the same short row `xxyXYY`. With that row fixed, degree six excludes every primitive replacement of every other row. When the longer row is fixed, the calculation selects the free basis using $t=xy^{-1}$ and the donor exponent vector. Both extreme Schreier letters occur once in each marking. The reverse fibres have ranks **8, 10, 10, 11, 8, 6, 3, 5, 6** in catalogue order. Independent permutation and Magnus residue tests exclude eight reverse directions, giving **17 of 18** directions overall. The remaining donor is `xxxYxxYXYXY`. Its four-stage graph completion has no primitive among the 51 tested slopes with $|k|\le25$. The unbounded direction remains open. [Nine-source replay](../results/round19_ak3_minima_fibres.json), [catalogue](../certificates/round18_ak3_c33_low20.tsv), [multi-source verifier](../experiments/round19_ak3_minima_fibres.py).

~~~sh
python3 -B experiments/round19_ak3_minimum_class_two.py
python3 -B experiments/round19_ak3_minimum_magnus.py
c++ -std=c++17 -O3 experiments/round17_ak3_periodic_slope.cpp -o "$work/periodic-slope"
python3 -B experiments/round19_ak3_minima_fibres.py \
  certificates/round18_ak3_c33_low20.tsv "$work/periodic-slope"
~~~
