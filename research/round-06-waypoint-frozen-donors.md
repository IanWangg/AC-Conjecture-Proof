# Both rows must change after the new marked waypoint

2026-11-19. Let $(R,S)$ be the endpoint of the new 267-move ordinary AK(3) certificate, with

~~~text
R = XXyxYxyXYxyXYxY
S = XXyyxYY
~~~

Before either row can become primitive, each of these two row identities must receive a multiplication by the other. In particular reaching any free basis from this waypoint requires at least three alternating updates in the metric where one update may multiply a recipient by any product of conjugates of a fixed donor. [Strict entry certificate](../certificates/round06_ak3_marked_waypoint29.json), [witness receipts](../results/round06_waypoint_frozen_donors.json).

## Frozen-donor test

Track the rows even when their slots are permuted. If a marking in a group with noncommuting generator images kills the donor, then the donor cannot become primitive while it is frozen. A primitive normally killed in rank two would leave a cyclic image. The receiver image stays in its initial conjugacy class up to inversion. The exponent vectors of $(R,S)$ are $(0,-1)$ and $(-1,0)$. A primitive receiver is therefore conjugate up to inversion to $yx^j$ when $S$ is frozen and to $x^{-1}y^j$ when $R$ is frozen. Here $j$ is arbitrary. This uses the exact uniqueness of the rank-two primitive class for a given exponent vector. [Frozen-donor proof mechanism](round-03-frozen-donors.md), [Osborne and Zieschang, §3.2](https://geodesic.mathdoc.fr/item/IM_1981__63_142788/).

For $S$ as donor use the marking in $\mathrm{SL}_2(\mathbb F_7)$

$$
x\longmapsto \begin{pmatrix}0&6\\1&6\end{pmatrix},
\qquad
y\longmapsto \begin{pmatrix}0&1\\6&4\end{pmatrix}.
$$

The two matrices do not commute. The marking kills $S$ and maps $R$ to trace two. The marked $x$ has order three, and the traces of $yx^j$ over this period are four, five and five. Trace is invariant under both conjugation and inversion, so no permitted primitive can occur.

## A Heisenberg obstruction with the long row frozen

Let $H$ be the Heisenberg group over $\mathbb F_7$, with coordinates

$$
(a,b,c)(d,e,f)=(a+d,b+e,c+f-bd).
$$

Put $A=(1,0,0)$, $B=(0,1,0)$ and $C=[A,B]=(0,0,1)$. The automorphism $\phi$ sends $A$ to $W=BAB^{-1}AB^{-1}A=(3,-1,0)$ and $B$ to $A$. Its matrix on the first two coordinates has determinant one, so it preserves $C$ and is invertible. Its order is eight, by direct iteration. Form the semidirect product with $t^8=1$ and $t h t^{-1}=\phi(h)$, and mark $x=t^{-1}$ and $y=A$. This is a group of order $2744$ and the marked elements do not commute.

With $Y_i=x^i y x^{-i}$, the long row rewrites as $Y_{-2}Y_{-1}^{-1}Y_0Y_{-1}^{-1}Y_0Y_{-1}^{-1}Y_0^{-1}$. The marking sends $Y_0$ to $A$, $Y_{-1}$ to $W$, and $Y_{-2}$ to $AW A^{-1} W A^{-1} W$. It therefore kills $R$. The shorter row maps to $t c_0$ where $c_0=W^2 A^{-2}=(4,-2,-1)$.

For each primitive candidate $t A^j$, conjugation by $t$ gives $t\phi(A^j)$, which is also obtained by conjugating $t A^j$ by $\phi(A^j)^{-1}\in H$. Thus full conjugacy containment for this element is equivalent to conjugacy by an element of $H$. Write a candidate conjugator as $\phi(g)$. Equality with $t c_0$ would require

$$
c_0=g A^j\phi(g)^{-1}.
$$

If the first two coordinates of $g$ are $u,v$, the first two coordinates in this equation force $u=j-2$ and $v=-j$. The central coordinate of $g$ cancels. Substitution gives central discrepancy $(j^2+3j+8)/2$, whose numerator has discriminant $-23=5$ in $\mathbb F_7$, a nonsquare. This rules out every residue $j$. The checker also exhausts every conjugating element of the finite group for the seven candidates.

The two witnesses work with different frozen donors. To reach a basis in two consecutive single-recipient updates, the first updated row would already need to be primitive after the first update, which is excluded. Paths that multiply into both original rows before any primitive appears remain possible.

~~~sh
python3 -B experiments/round06_waypoint_frozen_donors.py \
  | diff - results/round06_waypoint_frozen_donors.json
~~~
