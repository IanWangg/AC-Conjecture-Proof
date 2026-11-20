# A finite reduction for width-two singleton Wirtinger shifts

2026-11-19. The remaining aligned width-two singleton middle equations reduce to 19,464 explicit shifts across both orientations and singleton signs. This reduction bounds the shift word independently of the unknown middle conjugator. A free-group twisted conjugacy decision algorithm applies to each of the remaining equations. [Round 15 free-word reduction](round-15-ac-proof.md), [finite enumeration](../results/round16_ac_proof_wirtinger_finite.json).

## Substitution seams

Use the Round 15 notation $c,d,U,L,R,\theta$, so $\theta(U)=LUR$, $\theta(c)=d$, and
$$
\theta(d)=W=d^p Jc^{-2}J^{-1}d^q,\qquad S=p+q=3+\epsilon\in\{2,4\}.
$$
The word $U$ has zero exponent vector and coefficient $1$ on $[c,d]$ in the class-two quotient. Its $m\ge4$ affected letters $d^{\sigma_i}$ have intervening $c$ powers $e_i$ and modified separator powers $f_i$, as in Round 15. Put $F=\sum_i|f_i|$ and let $N$ count the nonzero $f_i$ including at the ends. At a change of sign in $(\sigma_i)$ the separator has $f_i=e_i\ne0$. Thus the reduced substituted word consists of $k$ blocks $Jc^{-2n_i}J^{-1}$ separated by nonzero affected powers, with $\sum_i |n_i|=m$. An end separator may be zero. Each block collects a nonempty sequence of same-sign copies. If $J$ is nonempty, cyclic reduction of the stripped shift ensures that $J$ starts in $c^{\pm1}$ and ends in $d^{\pm1}$. The block description also holds for $J=1$.

There are at least three blocks. With two, the signs would form $s^n(-s)^n$, where $n=m/2\ge2$ and $s\in\{-1,1\}$. The only nonzero interior separator would be $f_n$. The class-two coordinate from Round 15 would have magnitude $n|f_n|$, contrary to its value $1$.

For any freely reduced word, count the adjacent pairs of affected letters. This is the number of affected letters minus the number of maximal affected runs. A product of two reduced words deletes an inverse suffix and prefix and can create at most one adjacent pair at its seam. Let $z$ count the interior gaps with $e_i=0$. This is the adjacent-pair count of $U$. The two fixed wings have two adjacent pairs altogether in each orientation, so $LUR$ after reduction has at most $z+4$.

Write $j=|J|_d$ and $r$ for the number of affected runs of $J$. This also counts its $c$ runs. In the substituted word the exact adjacent-pair count is
$$
2k(j-r)+F-N.
$$
If $e_i=0$ at an interior gap, its two affected letters have the same sign and $|f_i|=S$. These $z$ positions alone contribute $(S-1)z\ge z$ to $F-N$. Hence $2k(j-r)\le4$. Since $k\ge3$, every affected run of $J$ has length one, so $j=r$. The same estimate gives a uniform bound on the remaining seams. At any position outside the $z$ zero gaps, the total contribution to $F-N$ is at most $z+4-(S-1)z\le4$. Therefore
$$
|f_i|\le5\quad(0\le i\le m),\qquad |e_i|\le S+5\quad(1\le i<m).
$$

## At most two runs in the stem

Let $Q_d$ be the number of affected pairs removed during free reduction of $LUR$. Counting affected letters gives
$$
m=2kr+F-6+2Q_d.
$$
Here $F\ge2$ because some separator is nonzero and their sum is zero. For $r\ge1$, this also implies $Q_d\le m/2$. The middle factor therefore retains affected letters. Until a reduced middle factor disappears, every removed affected letter from it pairs with an exterior letter, since its surviving part is contiguous.

Suppose $r\ge3$. Each central run $c^{-2n_i}$ has at least $r$ preceding and $r$ following affected letters. If such a run touches $L$ or the original initial $c$ power of $U$, all its preceding affected letters belong to the surviving prefix of $L$. There are at most three. The run must lie in the first substituted block, since a preceding block would contribute another $2r$ affected letters. Because the surviving prefix of $L$ starts in $c^{\pm1}$, the initial separator is zero. The preceding segment on the substituted side is then $J$, which has no adjacent affected letters. The prefix of $L$ has at most two affected runs and at least three affected letters, so it has an adjacent pair. This is impossible. The same reasoning at the right end applies to a central run touching $R$ or the original final $c$ power of $U$. The surviving suffix of $R$ ends in $c^{\pm1}$, has at most two affected runs and at most four affected letters. The run would have to be the last central run and the suffix $J^{-1}$ would have to contain an adjacent affected pair.

Thus every central run for $r\ge3$ is an original interior $c$ run of $U$ and has length at most $S+5$. It follows that $m=\sum_i|n_i|\le 4k$. But the affected-letter count gives $m\ge 2kr-4\ge6k-4$, which exceeds $4k$ for $k\ge3$. Consequently $r\le2$.

Each $c$ run of $J$ has length at most $S+7$. It appears as a maximal $c$ run $2k$ times on the substituted side. On the right, at most two runs contain material from the original end $c$ powers of $U$. Every other run has length at most $S+5$ from an interior $c$ power of $U$, plus at most two letters from a fixed wing at a seam. The two seams cannot lie in the same $c$ run, since the surviving middle still contains affected letters.

At most one $c$ run of $J$ can have length different from $S$. To prove this, count runs with length different from $S$. The substituted side has at least $2k$ copies of each such run in $J$. In $U$ each such interior run has $f_i\ne0$, so there are at most $k-1$ of them, plus at most two end runs. The fixed wings have two runs of lengths different from $S$ when $S=2$ and four when $S=4$. Multiplying two reduced words increases the sum of the two counts by at most one. At a maximal cancellation seam, a surviving run can be shortened on at most one side. If a $c$ run is shortened, the other side cannot then supply a $c$ run at the seam, since cancellation would continue. If neither is shortened, two intact runs can merge. Thus if $b$ counts the runs in $J$ with length different from $S$, then $2kb\le k+5$ for $S=2$ and $2kb\le k+7$ for $S=4$. Since $k\ge3$, both bounds force $b\le1$.

## The end powers are bounded

Both fixed left wings end in $d^{\pm1}$ and both fixed right wings start in $d^{\pm1}$. If $e_0,e_m$ are both nonzero, there is no cancellation at either seam. In the upper orientation the first and last affected heights would then be $-1,-2$. When $J=1$ all affected heights of the substituted word are even. When $J$ is nonempty, a nonzero end separator gives height zero at that end, while two zero end separators give the same height for the first affected letter in $J$ and the last in $J^{-1}$, because the total $c$ exponent is zero. Both cases contradict the upper heights.

In the lower orientation the fixed right wing is $R=d^{-2}cd^2c^{-2}$. If $J=1$, an affected letter at odd height from this wing contradicts the even heights of the substituted word. If $J$ is nonempty, $R$ ends in $c^{\pm1}$, requiring $f_m=0$. The substituted word then ends in $J^{-1}$ and has a final affected run of length one, whereas the final affected run of $R$ has length two.

It follows that $e_0=0$ or $e_m=0$. From the formulas for the corresponding $f$ and the bound $|f_i|\le5$ one gets $-5\le p\le S+5$. The other end power is $q=S-p$.

## Remaining decisions

For $S=2$ there are 309 stems and 13 choices of $p$ in each orientation. For $S=4$ there are 381 stems and 15 choices of $p$. Each stem consists of at most two runs $c^\alpha d^\beta$ where $1\le|\alpha|\le S+7$, $|\beta|=1$, and at most one $|\alpha|$ differs from $S$. This gives 19,464 marked shift words before previous nilpotent tests. The arithmetic and fixed-wing counts have a deterministic replay. [Enumeration](../experiments/round16_ac_proof_wirtinger_finite.py).

For each candidate, the middle equality is equivalent to the free-group twisted conjugacy equation $R=U^{-1}L^{-1}\theta(U)$. Logan's Lemma 2.2 gives a decision algorithm for precisely this equation for any endomorphism of a finitely generated free group. An arbitrary solution would have zero exponent vector since the signed exponent sums of $L$ and $R$ cancel and $I-\theta_{\rm ab}$ is invertible over the integers. The finite list therefore reduces the middle block to a finite collection of exact decisions. Those decisions and the outer compatibility checks have yet to be completed. [Logan, Lemma 2.2](https://doi.org/10.1112/plms.70088).

~~~sh
set -o pipefail
python3 -B experiments/round16_ac_proof_wirtinger_finite.py \
  | diff -u results/round16_ac_proof_wirtinger_finite.json -
~~~
