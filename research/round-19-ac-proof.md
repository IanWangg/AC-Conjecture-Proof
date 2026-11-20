# A finite exponent condition from the outer Wirtinger block

2026-11-19. In the conjugated-overlap branch at Schreier width two, write the normalized middle relator as $h=V^\alpha b^{-1}$ using Round 18. The outer block with donor $C$ forces $|\alpha|$ to be a divisor of $30$. This restriction holds for arbitrarily long words in both Magnus subgroups. It comes from a degree-six obstruction in the free-by-cyclic quotient of the outer donor and four separate finite-field checks. [Round 18 reduction](round-18-ac-proof.md), [exact replay](../results/round19_ac_proof_wirtinger_outer.json).

## The free-by-cyclic quotient of the donor

Use the outer height $\phi(x)=1,\ \phi(y)=-1$, so $\phi(C)=0$ and $\phi(A)=1$. Let $t_i=x^i(xy)x^{-i}$ be the free basis of the height kernel before quotienting by $C$. The Schreier relation for $C$ is
$$
t_{-2}^{-1}t_{-1}^{-1}t_0t_{-2}t_{-3}t_{-2}^{-1}t_{-1}^{-1}=1.
$$
The two extremes occur once, so the relations at all translated indices express every $t_i$ in the three generators $u=t_{-3}$, $v=t_{-2}$, and $w=t_{-1}$. These form a free basis of the kernel in the quotient. Indeed the expression $t_0=wvwvu^{-1}v^{-1}$ gives the shift automorphism $\Theta=(v,w,wvwvu^{-1}v^{-1})$ on the three generators. Its inverse follows by solving the same relation for $u$. The semidirect product of the free group on $u,v,w$ by this automorphism has the full Schreier presentation, with translated relations satisfied by the iterated shifts.

The common generator $b=y_{-1}$ has $b^{-1}=w^{-1}x$. Take $b^{-1}$ as the stable letter instead of $x$. It acts on the kernel by
$$
\Psi=\operatorname{Inn}_{w^{-1}}\circ\Theta
=\big(w^{-1}vw,\ w,\ vwvu^{-1}v^{-1}w\big).
$$
The word $A$ is $A_0 b^{-1}$ with
$$
A_0=wv u^{-1}v^{-1}wv w^{-1}vu v^{-1}w^{-1}v^{-1}.
$$

The outer block requires the normalized $h=V^\alpha b^{-1}$ to be conjugate to $A$ in $F(x,y)/\langle\!\langle C\rangle\!\rangle$. Here $V=zb^{-e}$ has height zero. Any conjugator can be multiplied on the right by a power of $h$ to make its height zero. The resulting necessary equation is
$$
k V^\alpha=A_0\Psi(k),\qquad k\in F(u,v,w).
$$

## Obstruction in the Magnus algebra

Work in the noncommutative truncated Magnus algebra through degree $d$ over $\mathbb F_p$, sending $u,v,w$ to one plus the corresponding variables. The shift $\Psi$ acts by substitution. The group of series with constant term one has exponent dividing the least power of $p$ greater than $d$, since $(1+n)^{p^j}=1+n^{p^j}$. Thus if this power divides $\alpha$, the outer equation would give
$$
k=A_0\Psi(k)
$$
in the algebra. We allow all series $k$ with constant term one. Inconsistency in this larger set excludes the free-group conjugator.

The linear part of $\Psi$ is $T$ with $U\mapsto V$, $V\mapsto W$, and $W\mapsto -U+V+2W$. Its characteristic polynomial is $X^3-2X^2-X+1$, with discriminant $49$. Let $p_d(X)$ be the characteristic polynomial of $\operatorname{Sym}^d(T)$. The tensor action $T_d=T^{\otimes d}$ on degree $d$ is annihilated by $p_d$. To see this over characteristic zero, diagonalize $T$ and compare eigenvalues. Any degree-$d$ product of eigenvalues occurs in the symmetric power. The resulting matrix identity is integral and holds after reduction in every prime characteristic.

For $d=1,\ldots,5$ put $q_d(X)=(p_d(X)-p_d(1))/(X-1)$. The identity $(I-T_d)q_d(T_d)=p_d(1)I$ determines the unique degree-$d$ correction to $k$ whenever $p_d(1)$ is invertible. The five values of $p_d(1)$ are $-1,1,-26,1352,-95992$, with product $D=-3,374,310,784$. The replay carries a common denominator for the successive corrections and obtains $k$ through degree five with denominator dividing $D$.

At degree six, $p_6(1)=0$. Let $q_6$ be the quotient after removing all factors of $X-1$ from $p_6$. Then $q_6(T_6)(I-T_6)=0$, again by diagonalization and the integral matrix identity. Apply this operator to the degree-six residual of $A_0\Psi(k)-k$, after scaling by $D$. The replay gets a nonzero integral vector with 700 nonzero coefficients and coefficient gcd $E=2,778,890,025,987,712$. A solution modulo $p$ is impossible whenever $p\nmid DE$ because the first five degrees are uniquely determined and the projected residual remains nonzero. The exceptional prime factors of $DE$ are $2,7,13,71$.

The degree-six argument therefore rules out all prime divisors of $\alpha$ at least seven outside the exceptional set. It also rules out $9\mid\alpha$ and $25\mid\alpha$, since those powers exceed six and the obstruction survives in characteristics three and five. For the exceptional primes, direct linear elimination gives the following additional obstructions. The columns span the possible positive-degree coefficients of $(I-A_0\Psi)(k-1)$, and the nonzero remainder shows that $A_0-1$ lies outside that span.

| Prime | Truncation degree | Rank | Number of columns | Excluded divisor of $\alpha$ |
| ---: | ---: | ---: | ---: | ---: |
| 2 | 3 | 33 | 39 | 4 |
| 7 | 6 | 951 | 1,092 | 7 |
| 13 | 4 | 114 | 120 | 13 |
| 71 | 6 | 1,001 | 1,092 | 71 |

Consequently $|\alpha|\in\{1,2,3,5,6,10,15,30\}$. Since $\exp_a x_0-\exp_c y_0=\pm1$ in the conjugated-overlap branch, $|h_a-h_c|=|\alpha|$. The cyclic-power branch already required $|h_a-h_c|=1$. Thus the same list bounds the absolute signed difference of the extreme exponents for every aligned width-two repair regardless of the exceptional-intersection branch. This outer condition leaves the eight values open in the conjugated-overlap branch.

## An exact condition on the outer normalization

The Laurent constraint from the middle equation also gives the abelianized outer kernel coordinate of $V$ before imposing either outer relator. Use $T$ now as the Laurent variable for the shift by $x$ and represent a word of outer height $r$ by $(r,m)$ with multiplication $(r,m)(s,n)=(r+s,m+T^r n)$. The three indexed generators $a,b,c$ have height $-1$ and coordinates $T^{-3},T^{-2},T^{-1}$. Retain the Round 18 notation $X=x_0^{-1}$ and $Y=\sigma(y_0)$, with $\sigma(b)=a,\ \sigma(c)=b$. Let $n_X$ be the total signed exponent of $X$ in $a,b$. Take the middle equation's Laurent monomial as $G(t)=s t^j$.

Evaluate Fox derivatives of $X,Y$ at $(A_0,B_0)=(T^{-1},T^{-1})$, using the abelian variables of Round 18. The coordinate of $X$ is $T^{-2}([n_X]_{T^{-1}}+(T^{-1}-1)\partial_a X)$. The coordinate of the unshifted $y_0$ is $T^{-2}([n_Y]_{T^{-1}}+(T-1)\partial_bY)$, where $n_Y$ is its total signed exponent. Taking $V=X^{-1}y_0 b^{-e}$ cancels the terms with the geometric sums and gives
$$
m_V=T^{n_X-2}(T-1)(\partial_bY+T^{-1}\partial_a X)
=sT^{n_X+j-1}(T-1).
$$
The last equality is the specialization of the middle Alexander equation on the diagonal.

Before imposing $B$ or $C$, both $A$ and $b^{-1}$ have coordinate $(1,-T^{-1})$. Also $[N_B,N_C]$ maps trivially in this semidirect product, since both outer normal closures lie in the height kernel. Hence if a conjugator with coordinate $(r,m)$ carries the normalized $V^\alpha b^{-1}$ into $A[N_B,N_C]$, the multiplication formula forces
$$
m=s\alpha T^{r+n_X+j-1}.
$$
This fixes the full Laurent coordinate of any such conjugator. Its remaining lift to the outer height kernel has yet to be determined.

~~~sh
set -o pipefail
python3 -B experiments/round19_ac_proof_wirtinger_outer.py \
  | diff -u results/round19_ac_proof_wirtinger_outer.json -
~~~
