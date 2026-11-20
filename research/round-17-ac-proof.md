# Exclusion of width-two singleton Wirtinger repairs

2026-11-19. The aligned Wirtinger middle equation has no solution at Schreier width two when either extreme occurs exactly once. The proof combines the unbounded word-length reduction from Round 16 with exact quotient tests on the resulting 19,464 marked shifts. The finite-field tests use an equation in the rank-one Alexander module of the free base. [Round 16 finite reduction](round-16-ac-proof.md), [exact exclusion results](../results/round17_ac_proof_wirtinger_alexander.json).

## The Alexander equation

Continue with $\theta(U)=LUR$ in the free group $F=F(c,d)$, where $U\in F'$ and
$$
\theta(c)=d,\qquad \theta(d)=W=d^p Jc^{-2}J^{-1}d^{S-p},
\qquad S\in\{2,4\}.
$$
Use the Laurent ring $\mathcal R=\mathbb Z[C^{\pm1},D^{\pm1}]$, with $C,D$ the images of $c,d$ in the abelianization. In the universal abelian cover of the two-petal rose, the chain boundary is $(C-1,D-1)$. The kernel is the free $\mathcal R$-module on $(1-D,C-1)$, the lifted cycle for $[c,d]$. This identifies $F'/F''$ with $\mathcal R$ in that basis. Write $u$ for the coordinate of $U$ and let $\tau$ be the ring substitution
$$
\tau(C)=D,\qquad \tau(D)=C^{-2}D^S.
$$
The abelianized Fox derivatives are the coefficients of lifted paths in the two oriented edges. Denote them by $\partial_c,\partial_d$. On the generator $(1-D,C-1)$ the image under $\theta$ has first coordinate $(D-1)\partial_c W$. Thus $\theta$ acts on the module by $u\mapsto f\tau(u)$, with $f=-\partial_c W$.

On the other side, $LUR=(LUL^{-1})(LR)$ has coordinate $\ell u+b$, where $\ell$ is the image of $L$ in the abelianization and $b$ is the coordinate of $LR$. In the upper orientation, $L=P$, $R=Q^{-1}$, and direct reduction gives $PQ^{-1}=c^{-2}[c,d]c^2$. Thus $\ell=D^{-1}$ and $b=C^{-2}$. In the lower orientation, $L=P^{-1}$, $R=Q$, and the basis reverses $a,b$. The identity $P^{-1}Q=P^{-1}(PQ^{-1})^{-1}P$ then gives $\ell=C$ and $b=CD^{-2}$.

Let $H=1+(D-1)\partial_d J$. The product rule for the derivative, applied to the displayed form of $W$, gives
$$
f=C^{-2}(1+C)D^p\left(\overline J-(C-1)\partial_c J\right)
  =C^{-2}(1+C)D^p H,
$$
where the bar is abelianization and the second equality follows from $\overline J-1=(C-1)\partial_c J+(D-1)\partial_d J$. Consequently putting $v=\ell u/b$ converts the necessary equation to
$$
v+1=g\tau(v),\qquad
g=
\begin{cases}
 C^{-2}(1+C)D^{p+S-2}H & \text{upper},\\
 C(1+C)D^{p+2-2S}H & \text{lower}.
\end{cases}
$$

## The finite-field cycle obstruction

For a prime $l$, evaluate the equation on $(\mathbb F_l^\times)^2$. The substitution $\tau$ corresponds to the point map $\Phi(C,D)=(D,C^{-2}D^S)$. Along a directed cycle $z_0,\ldots,z_{n-1}$ of $\Phi$, put $g_i=g(z_i)$. Iterating $v(z_i)=g_i v(z_{i+1})-1$ gives
$$
\left(1-\prod_{i=0}^{n-1} g_i\right)v(z_0)
  =-\left(1+g_0+g_0g_1+\cdots+g_0\cdots g_{n-2}\right).
$$
A product of one and a nonzero prefix sum therefore rule out the Laurent polynomial equation. The replay uses the actual finite point map and exact modular arithmetic. It computes $\partial_d J$ by adding the monomial for the prefix at each positive affected letter, and subtracting the monomial for the prefix after each negative affected letter.

The replay first applies the verified degree-three and degree-four congruences from Rounds 13 and 14. If $J=c^u d^w[c,d]^z$ modulo $\gamma_3$, the input to those congruences only needs the normalized first power $p+w$ and the area $z+uw$. Modulo $\gamma_4$ the shift has the same image as $d^{p+w}[c,d]^{z+uw}c^{-2}[c,d]^{-z-uw}d^{S-p-w}$. The area is the degree-two $cd$ coefficient of the Magnus expansion of $J$, so its value is the sum of signed $c$-prefix exponents at its affected letters. The replay recovers the three Hall coefficients and checks reconstruction through degree three before applying the earlier congruences. These coefficients only need residues of $p+w$ and $z+uw$ modulo each test prime. For primes at least five the generator powers have that period through degree three. Modulo three a cube of a generator is central through degree three, so shifting the end power by three transfers the same central factor between the two ends. [Round 13 residue](round-13-ac-proof.md), [Round 14 residue tables](round-14-ac-proof.md).

## Exhaustive counts

The counts agree between orientations, with each orientation computed separately.

| Trace | Round 16 candidates per orientation | After nilpotent tests | Finite-field primes in order | Survivors after each prime |
| ---: | ---: | ---: | --- | --- |
| 2 | 4,017 | 10 | 11, 29, 31, 61, 67 | 8, 7, 4, 2, 0 |
| 4 | 5,715 | 376 | 19, 29, 31, 37, 43, 47, 61, 71, 83, 103 | 371, 275, 230, 129, 79, 61, 48, 30, 21, 0 |

The result file records the last rejecting cycle for each candidate still present at the final prime. Thus all remaining determinant-two shifts in the finite list fail a necessary condition of the exact free middle equation. Earlier rounds excluded the other determinants. Within the aligned exponent marking, a width-two repair requires that both extremes occur more than once in the cyclically reduced Schreier relator. The higher-width exceptional Magnus-intersection cases remain open, as does the ordinary Andrews–Curtis conjecture. [Round 13 HNN reduction and intersection condition](round-13-ac-proof.md).

~~~sh
set -o pipefail
python3 -B experiments/round17_ac_proof_wirtinger_alexander.py \
  | diff -u results/round17_ac_proof_wirtinger_alexander.json -
~~~
