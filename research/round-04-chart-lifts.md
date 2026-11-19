# Two free elimination charts need not have a common lifted basis

2026-11-19. A balanced trivial rank-three tuple can have two one-occurrence elimination charts without any pair of ambient words projecting to a free basis in both. The common lifted basis hypothesis used in the [two-incoming cut lemma](round-04-stable-disproof.md) therefore needs its own check.

In $F(x,y,z)$ take the three relators

$$
p=z(xyx^{-1})^{-1},\qquad q=x(y^2z^2)^{-1},\qquad r=y.
$$

After imposing $r=1$, the first equation sets $z=1$ and the second sets $x=1$, so the tuple presents the trivial group. The relator $p$ solves $z=xyx^{-1}$, giving a free rank-two quotient marked by $(x,y)$. The relator $q$ solves $x=y^2z^2$, giving a free rank-two quotient marked by $(z,y)$.

Map to $A_5$ by $x=(1\,2\,3)$, $y=(1\,2\,3\,4\,5)$ and $z=xyx^{-1}$, composing permutations from right to left. The equations $p=q=1$ hold in the finite image. The two marked pairs generate $A_5$, and their commutators have orders three and five, respectively. These are exact evaluations. [Finite witnesses and replay](../results/round04_chart_lifts.json).

Suppose ambient words $(w_1,w_2)$ gave a basis in both free quotients. The finite pair $(\phi(w_1),\phi(w_2))$ would then be Nielsen equivalent to both $(\phi(x),\phi(y))$ and $(\phi(z),\phi(y))$. For rank-two Nielsen equivalence the commutator conjugacy class is preserved up to inversion. This follows on inversions, swaps and multiplication of one generator by the other, which generate the rank-two Nielsen operations. The different commutator orders make the two equivalences impossible.

Both projected tuples are nevertheless ordinarily trivial. Retain the row $y$ and clear its conjugates from the other row. The strict replays take eight and thirteen moves. The example excludes automatic common lifting for different marked complements. It leaves other methods of comparing the projected ordinary AC classes available. [Concrete chart change on the AK(3) witness](round-04-chart-screen.md).

~~~sh
python3 -B experiments/round04_chart_lifts.py | diff - results/round04_chart_lifts.json
~~~
