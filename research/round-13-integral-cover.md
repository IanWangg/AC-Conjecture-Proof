# The other reciprocal orientation at the second energy-20 waypoint

2026-11-19. Both reciprocal two-block orientations from the second energy-20 pair now fail against all 23,902 verified ordinary-trivial archive pairs, with arbitrary word length inside either block. Round 12 covered the orientation with `xxxxyXXYY` fixed first. Holding `xxyyxYYYxxY` fixed first leads to a rank-ten free-by-cyclic quotient. A signed Fox-cover test reduces that orientation to the original row's conjugacy class. None of its archive companions passes the opposite block. [Previous orientation and quotient marking](round-12-ac-proof.md), [complete replay](../results/round13_ak3_integral_cover.json).

## Exact first-block tests

Use $p_i=u^ipu^{-i}$ in the free-by-cyclic marking of Round 12, with $u=x^2y^{-1}$, $p=(x^2y^{-1})(x^3y^{-1})$, and free basis $p_{-11},\ldots,p_{-2}$. Write $\phi$ for conjugation by $u$ and $M$ for its action on the abelianization of the rank-ten kernel. The code verifies both free substitutions for $\phi$ and $\phi^{-1}$. A proposed receiver is oriented to height one and written as $Vu$. The source has form $Uu$. A conjugator can be made height zero by multiplying by a power of $Vu$. Its kernel word $g$ must satisfy $gV=U\phi(g)$. The exponent equation $(I-M)[g]=[U]-[V]$ determines a unique vector. The mod-two equation is also invertible and determines the sign of $g$ at each sign character.

For a sign character $\chi$, the Fox derivative $D_\chi$ satisfies the product rule. Let $J_\chi$ have columns $D_\chi(\phi(a_i))$, for the ten kernel basis elements $a_i$. The necessary recurrence is

$$
D_\chi(g)=D_\chi(U)-\chi(g)D_\chi(V)
          +\chi(U)J_\chi D_{\chi\circ\phi}(g).
$$

The nontrivial characters form three orbits of length 341. Over a chosen finite field, compose the recurrence around an orbit. Any left null vector of the resulting coefficient matrix must annihilate the constant vector. To process each archive word efficiently, transport these left null vectors around the orbit in advance. The contribution of a letter at a particular sign prefix is then a signed sum over the characters. A Walsh–Hadamard transform computes this table for every prefix parity at once. The derivative of each Schreier letter $p_i$ comes from applying the same substitution recurrence forward or backward from $p_{-2}$, which avoids writing long iterated free words. [Fox calculus](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/fox1.pdf), [modular character filter](../experiments/round13_ak3_sign_cover.py).

| Necessary test | Retained distinct marked words |
| --- | ---: |
| Archive signed marks | 147,060 |
| Height of absolute value one | 8,726 |
| Squared trace in the established $\mathrm{PSL}_2(11)$ marking | 1,634 |
| First character orbit modulo 3 | 528 |
| Third character orbit modulo 3 | 176 |
| Second character orbit modulo 11 | 17 |
| Integral evaluations on the sign cover | 1 |

For each of the last 17 words, solve the same orbit recurrence over $\mathbb Q$ with the Fox boundary equation

$$
\sum_j (\chi(a_j)-1)D_{\chi,j}(g)=\chi(g)-1 .
$$

The system forces a unique derivative vector. It contains a noninteger coordinate for 16 of these words, which excludes an actual word $g$. For integral evaluations, the script also checks integrality of the inverse Walsh transform on the full mod-two cover. Three explicit conjugates of the source pass, with their abelianization vectors independently recovered from the conjugators. [Exact integral checker](../experiments/round13_ak3_integral_cover.py).

## The sole first-block class

The remaining cyclic word is `XXXXyyxxY`, an inverse cyclic rotation of `xxxxyXXYY`. Its conversion can be undone by orientation and conjugation of that same row. There are 18 distinct archive companions with that marked word. For any of them to complete the reciprocal block, it must be conjugate up to inversion to `xxyyxYYYxxY` in the quotient by `xxxxyXXYY`. The complete Round 12 amalgam screen gives exactly two cyclic archive words with this property. Neither is one of the 18 companions. The signed archive index and hash are the same in both tests. [Amalgam test](round-12-ac-proof.md), [intersection receipt](../results/round13_ak3_integral_cover.json).

~~~sh
python3 -B experiments/round13_ak3_integral_cover.py "$reverse" \
  | diff - results/round13_ak3_integral_cover.json
~~~
