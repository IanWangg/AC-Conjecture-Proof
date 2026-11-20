# Frozen primitive exclusion at five external projections

2026-11-19. Both receiving directions at the external energy-24 pair and at each of the four shortest energy-23 pairs exclude primitive replacement while the other relator is held fixed up to conjugacy and inversion. Nine directions use explicit permutation markings. The remaining direction uses Fox flow over a quartic character cover of a rank-seven free-by-cyclic quotient. [Replay data](../results/round14_ac_disproof_frozen.json), [external projection and four short pairs](round-13-ac-disproof.md), [strict stable route to the energy-24 pair](round-14-stable-proof.md).

## Exhausting primitive candidates

Let $d$ be the fixed row and $r$ the receiving row. A sequence of products by conjugates of $d^{\pm1}$, conjugations and inversions must send $r$ to the class of a conjugate of $r^{\pm1}$ in $F(x,y)/\langle\!\langle d\rangle\!\rangle$. The two exponent vectors retain determinant of absolute value one. Choose a basis $(u,v)$ of $F(x,y)$ with exponent vectors $\overline u=\overline r$ and $\overline v=\pm\overline d$. The replayer verifies each basis by folding its two loops to the ambient rose. Every primitive candidate can be oriented to have exponent vector $\overline r+n\overline v$ for an integer $n$. Rank-two primitive conjugacy classification then gives the representative $uv^n$. [Rank-two primitive classification and controls](round-12-ak3.md).

A finite permutation marking killing $d$ gives a necessary equality between the cycle types of the receiver and $uv^n$. These types survive inversion, and the order of the image of $v$ gives a period in $n$. Intersecting the allowed residues in a common period gives an empty set in all nine directions checked by permutations.

For the new energy-24 direction, hold `XXYxYXXYxxy` fixed and use $(u,v)=(y,xyy)$. In both markings the one-line image of $x$ is $(2,3,4,5,6,7,8,9,1)$. The two images of $y$ are $(1,4,6,2,3,8,9,7,5)$ and $(2,4,6,7,9,1,8,5,3)$. The image of $v$ has order nine in each marking. The first permits only $n\equiv3\pmod 9$, and the second permits only residues in $\{1,2,6\}$ modulo nine. The energy-24 direction with the other row fixed replays the prior degree-six witness. [All cycle types and intersections](../results/round14_ac_disproof_frozen.json), [earlier degree-six witness](round-13-ac-disproof.md).

| Energy-23 pair in catalogue order | Fixed first row | Fixed second row |
| --- | --- | --- |
| `(xxxyxYxyxYY, xxyxxYYxxyxY)` | $S_9$, period 9 | Fox flow, period 20 |
| `(xxxyyxyyXYY, xxyXYYYYXXyy)` | $S_7$ and $S_8$, common period 4 | $S_8$, period 4 |
| `(xxyxYYXXY, xyxYXyXYxyxYXY)` | $S_9$, period 9 | $S_5$ and $S_6$, common period 5 |
| `(xxyxyXYXyy, xxyXyxxyXYYXy)` | $S_8$ and $S_9$, common period 7 | $S_5$ and $S_6$, common period 5 |

## The rank-seven quotient

Fix `xxyxxYYxxyxY`, put $z=yx^{-7}$ and write $z_i=x^izx^{-i}$. The fixed word has $x$-height zero and rewrites as $z_2 z_4^{-1}z_{-3}^{-1} z_{-1}z_0^{-1}$. Each extreme occurs once. With $a,\ldots,g=z_{-3},\ldots,z_3$, eliminating $z_4$ gives the automorphism induced by conjugation by $x$, with one-line basis images `(b,c,d,e,f,g,AcDf)`. The two substitutions for this marking replay inversely.

Orient the current receiver and a candidate to height one, as $Ux$ and $Vx$. Multiplying any conjugator by a suitable power of the second word reduces it to a kernel element $h$. The necessary equation is $hV=U\theta(h)$, where $\theta$ is the shift. Abelianization gives the unique vector $(I-M)^{-1}(\overline U-\overline V)$ for $\overline h$. The replayer verifies that $I-M$ has an integral inverse. For each character $\chi$ with values in the fourth roots of unity in $\mathbb F_5$, evaluated Fox derivatives satisfy

$$
D_\chi(h)=D_\chi(U)-\chi(h)D_\chi(V)+\chi(U)J_\chi D_{\chi\circ\theta}(h),
$$

along with the Fox boundary identity. The matrices for an entire character orbit give a finite necessary system for $D_\chi(h)$.

Here the basis $(u,v)$ is `(Yxxxxxx, Yxxxxxxx)`. The height-zero word $v$ has order dividing 20 in the abelian-and-derivative representation. Its fourth power has zero exponent vector modulo four, and the derivative part of that kernel is additive modulo five. The replay checks that $v^{20}$ vanishes in every evaluated representation. The systems for the 20 residue classes cover all integers, including after height orientation. Every residue gives a dual row annihilating the coefficients and yielding a nonzero constant. The recorded witnesses use character orbits of lengths 105 or 210. An actual twisted conjugate of the source passes every one of the 100 character orbits. [Exact systems and dual rows](../results/round14_ac_disproof_frozen.json), [Fox calculus and orbit replayer](round-12-torus-contact-fox.md).

~~~sh
set -o pipefail
python3 -B experiments/round14_ac_disproof_frozen.py \
  | diff -u results/round14_ac_disproof_frozen.json -
~~~
