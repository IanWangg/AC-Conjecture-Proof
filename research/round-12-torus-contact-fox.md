# Fox obstruction for the last torus-quotient archive contact

2026-11-19. Free-group quotients by named fixed rows give an arbitrary-length test for ordinary receiving blocks. In the last surviving exact torus chart contact of Round 12, the second block would need to conjugate the AK(3)-side row `xxxxxyXXy` to the archive row `XXYYxyy` in the quotient by `XXYYxyXXyyxYY`. A six-equation Fox system modulo 5 excludes that conjugacy. This closes the stated torus-chart family and its indexed archive. [Torus-chart census](round-12-ak3.md), [exact receipt](../results/round12_torus_contact_fox.json).

## Reduction to a free-by-cyclic equation

Write $z=x^2y$ and $z_i=x^izx^{-i}$. Schreier rewriting of the fixed row gives

$$
z_{-2}^{-1} z_0^{-1} z_1 z_{-3} z_{-5} z_{-4}^{-1}z_{-2}^{-1}=1.
$$

Name $z_{-5},\ldots,z_0$ by $a,\ldots,f$. Introducing those names and eliminating $z_1$ gives the mapping torus of the automorphism $\phi$ with images

~~~text
a -> b
b -> c
c -> d
d -> e
e -> f
f -> fddbAC
~~~

Here uppercase is inverse. The inverse images are `BFecca,a,b,c,d,e`. Substitution checks both inverse identities in the free group. The two receiver words have height $-1$ in the cyclic factor. This fixes the sign in a possible conjugacy. Their inverses have form $Ux$ and $Vx$, where the replayer computes $U,V$ in the six-letter free group. Multiplying a possible conjugator on the right by a suitable power of $Vx$ makes its height zero and preserves the equation. Thus a conjugator would yield a free kernel word $g$ with $gV=U\phi(g)$. The abelianization equation has determinant $-1$ and uniquely forces $[g]=(-4,0,-3,5,4,7)$.

## A six-row contradiction

Let $\chi$ be a sign character of the free kernel, and let $D_\chi(w)$ denote the Fox derivative vector of $w$ evaluated at $\chi$. Each forward letter contributes the sign of its current prefix in that coordinate. Each inverse letter subtracts the sign after traversing it. The product rule gives

$$
D_\chi(gV)=D_\chi(g)+\chi(g)D_\chi(V).
$$

For $J_\chi$ with columns $D_\chi(\phi(a)),\ldots,D_\chi(\phi(f))$, substitution gives $D_\chi(\phi(g))=J_\chi D_{\chi\circ\phi}(g)$. A solution would satisfy

$$
D_\chi(g)=D_\chi(U)-\chi(g)D_\chi(V)+\chi(U)J_\chi D_{\chi\circ\phi}(g).
$$

The character `(1,1,1,1,1,-1)` is on an orbit of length 63 under precomposition by $\phi$. Iterate the displayed equations around that orbit, using the forced value of $\chi(g)$ at each character. This gives a six-row affine linear system for the initial $D_\chi(g)$ over $\mathbb F_5$. Multiplying the six augmented rows by `(4,3,1,2,1,0)` and summing gives `(0,0,0,0,0,0 | 1)`. The replayer obtains the matrix from the original words and rechecks this dual certificate. [Fox's free differential calculus](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/fox1.pdf), [certificate replayer](../experiments/round12_torus_contact_fox.py).

Together with the other eleven explicit separators, this excludes all indexed archive contacts in which the first receiver starts from the first energy-20 pair and the first fixed donor is `xxxxxyXXy`, under the signed markings and archive described in the torus census. Further alternating blocks and other archive endpoints remain available.

~~~sh
python3 -B experiments/round12_torus_contact_fox.py \
  | diff - results/round12_torus_contact_fox.json
~~~
