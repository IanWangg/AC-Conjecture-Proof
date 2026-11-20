# Odd-character covers in the other orientation of the first energy-20 pair

2026-11-19. The reciprocal two-block join with `xxyxxyyXYXY` fixed first fails against all 23,902 ordinary-trivial archive pairs. Together with the earlier torus test for the opposite orientation, this exhausts both orders for this pair within the indexed archive. The two orders for the other energy-20 pair have also been exhausted. [Previous torus orientation](round-12-ak3.md), [torus contact obstruction](round-12-torus-contact-fox.md), [other waypoint](round-13-integral-cover.md), [new replay](../results/round13_ak3_ascending_cover.json).

## Finite character covers

Put $t=x^{-1}$ and $a=x^2y$. Write $a_i=t^iat^{-i}$. The frozen row has height zero and becomes $a_0^2 a_2 a_3^{-1} a_2^{-1}$, so $a_3=a_2^{-1}a_0^2a_2$. With $b=a_1$ and $c=a_2$, the quotient has defining relations $twt^{-1}=\theta(w)$ for $w=a,b,c$, where

~~~text
a -> b
b -> c
c -> Caac
~~~

The exponent matrix of $\theta$ has determinant 2, and $I-M$ has determinant $-1$. The archive and source words usable in the first block have height of absolute value one. For a fixed marking, orient them to height one. Write these as $Ut$ and $Vt$. In every compatible cover, any conjugacy gives a height-zero conjugator by multiplying on the right by a power of $Vt$. Its exponent vector is determined by $(I-M)[g]=[U]-[V]$.

Choose an odd $k$ and an odd prime $p$ with a $k$th root of order exactly $k$ in $\mathbb F_p$. Use the exponent group $L=(\mathbb Z/k)^3$ and the product of Fox derivative vectors over all its characters. For a word with exponent vector $v$, multiplication acts on each character's derivative by the scalar $\chi(v)$. On this finite coefficient group, $\theta$ acts by $M$ on exponents and by $D_\chi\mapsto J_\chi D_{\chi\circ\theta}$ on derivative vectors. The matrix $M$ is invertible modulo $k$. The determinant of $J_\chi$ is $\chi(c)^{-1}(1+\chi(a))$, which is nonzero because $\chi(a)$ has odd order. Thus the action is invertible even though the original free endomorphism has a proper image. This defines a compatible image for the stable letter acting on the finite coefficient group. Using its inverse computes negative shifts $a_i$ directly. The replay checks that the frozen row vanishes in each entire coefficient group. [Fox derivative identities](round-12-torus-contact-fox.md), [cover construction and checker](../experiments/round13_ak3_ascending_cover.py).

A candidate must satisfy the orbit recurrence for $gV=U\theta(g)$. Each orbit of characters gives a linear system over $\mathbb F_p$. The checker composes the derivative transport around the orbit and applies every left null vector to the constant term. Three actual conjugates of the source pass all three covers.

| Necessary test | Retained distinct marked words |
| --- | ---: |
| All signed donor keys in the archive | 147,060 |
| Height of absolute value one | 23,839 |
| Cycle type in the verified degree-eight permutation marking | 747 |
| Odd-character cover with $(k,p)=(3,7)$ | 37 |
| Odd-character cover with $(k,p)=(5,11)$ | 2 |
| Odd-character cover with $(k,p)=(7,29)$ | 1 |

The remaining word is `XXXXXYxxY`, the signed cyclic class of `xxxxxyXXy` itself. The archive index gives 97 companions of this marked word. For the second block with this class fixed, the torus-quotient calculation identified seven exact compatible marked words against this same archive. The two sets are disjoint. The test covers arbitrary operations within the two specified receiving blocks. It leaves longer alternating orders and endpoints beyond this archive for further work. [Exact torus signature and archive keys](../results/round12_ak3_torus_chart.json), [intersection replay](../results/round13_ak3_ascending_cover.json).

~~~sh
python3 -B experiments/round13_ak3_ascending_cover.py "$reverse" \
  | diff - results/round13_ak3_ascending_cover.json
~~~
