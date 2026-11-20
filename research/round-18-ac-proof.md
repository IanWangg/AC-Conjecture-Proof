# Width-two exceptional Magnus intersections in the Wirtinger middle equation

2026-11-19. At Schreier width two, Howie's classification reduces an exceptional intersection to equality of two cyclic powers or equality of conjugates of powers of the common generator. The cyclic-power case requires the signed extreme exponents of the middle relator to differ by one. In the conjugated-power case both powers must be primitive, the relator has an explicit form in a two-generator subgroup, and the middle conjugator has a one-term Laurent coordinate. No conjugator of the corresponding simplest free-word form solves the equation. [Round 13 middle equation](round-13-ac-proof.md), [Howie, Theorem C and Lemmas 5.3–5.5](https://doi.org/10.1307/mmj/1133894169).

## The exceptional generator and class two

Write $a=y_{-2}$, $b=y_{-1}$, and $c=y_0$. In the base group $H=\langle a,b,c\mid h\rangle$, the associated free subgroups are $L=F(a,b)$ and $M=F(b,c)$. Round 13 reduces the middle conjugacy for $h$ of total $y$ exponent $-1$ and $x$ exponent zero to
$$
\iota_L(\eta)Q=P\,\sigma(\iota_M(\eta)),\qquad
P=a^{-1}bab^{-2},\quad Q=a^{-2}ba^2b^{-2},
$$
where $\sigma(b)=a$, $\sigma(c)=b$, and $\eta$ belongs to the exceptional intersection. We identify the intersection with $F(b,T)$ by a free basis consisting of the overlap generator $b$ and an exceptional generator $T$. The two embeddings $\iota_L,\iota_M$ take $T$ to the corresponding free representatives $T_L$ and $T_M$. Both images of $\eta$ have zero exponent vector. The two class-two coordinates, evaluated in $F(a,b)$ after shifting the right-hand image, differ by $1$, since $PQ^{-1}=a^{-2}[a,b]a^2$.

Set $A=\exp_a T_L$ and $C=\exp_c T_M$. If $(A,C)\ne(0,0)$, the two exponent conditions force $\exp_T\eta=\exp_b\eta=0$. If $I$ is the class-two coordinate of $\eta$ on $[b,T]$, the two images have coordinates $-AI$ and $CI$ by the determinants of the embeddings. Therefore
$$
(-A-C)I=1.
$$
Denote the signed exponent vector of $h$ in the base by $(h_a,h_b,h_c)$. Because $T_L=T_M$ in $H$, their exponent difference has the form $n(h_a,h_b,h_c)$ for an integer $n$. The difference of the first and third coordinates gives $A+C=n(h_a-h_c)$. Thus
$$
|A+C|=|I|=|n|=|h_a-h_c|=1.
$$

If $A=C=0$ and the two representatives of $T$ have different $b$ exponents, the exponent conditions on $\eta$ again force it to have zero exponent vector. In this case both embedding determinants vanish, so the class-two coordinate difference is zero. Hence when both extreme exponents of $T$ vanish, the two overlap exponents must be equal.

## The cyclic-power branch

By Howie's Theorem C and its proof, the first type of exceptional intersection at width two has a conjugate of $h$ in $F(X,Y)=\langle X\rangle*\langle Y\rangle$, where $X\in L$, $Y\in M$. The rank-one factors in Howie's theorem are cyclic here because they are finitely generated subgroups of free groups. If $R$ represents this conjugate in $F(X,Y)$, the exceptional cyclic factor is the common subgroup of $\langle X\rangle$ and $\langle Y\rangle$ in $\langle X,Y\mid R\rangle$. Thus the representatives of an exceptional generator are $X^m$ and $Y^n$, with $m,n\ne0$ and the equality holding in that two-generator quotient. This branch also covers the product case isolated in the proof of Howie's Lemma 5.5.

Writing $(r_X,r_Y)$ for the exponent vector of $R$, abelianization gives $(m,-n)=k(r_X,r_Y)$ with $k\ne0$. Under the inclusion into $F(a,b,c)$ the total exponent sum of the right side is $-k$. Therefore the total exponent sums of $X^m$ and $Y^n$ differ. If $A=C=0$, their $b$ exponents differ and the class-two argument already rules them out. Every solution in this branch has $|h_a-h_c|=1$. In addition, $k$ is exactly the integer multiplying the ambient vector of $h$ in the preceding comparison, so $|k|=1$. In particular the exponent vector of $R$ agrees up to sign with $(m,-n)$. It is primitive because its image has total exponent $-1$.

## The conjugated-overlap branch

In the other case of Howie's Lemma 5.5, there are $x_0\in L\setminus\langle b\rangle$, $y_0\in M\setminus\langle b\rangle$, $z=x_0y_0$, and a subgroup $D\le\langle b\rangle$ such that a conjugate of $h$ lies in $\langle z\rangle*D$. The exceptional generator has representatives $x_0^{-1}b^m x_0$ and $y_0 b^n y_0^{-1}$, where $b^m$ generates $D\cap zDz^{-1}$ in the corresponding one-relator quotient. Here $m,n\ne0$. The previous argument forces $m=n$. The class-two coordinates of the images of $\eta$ now differ by
$$
m\exp_T(\eta)\big(-\exp_a x_0+\exp_c y_0\big).
$$
Indeed replacing $T$ by $Tb^{-m}$ changes the other basis generator by a Nielsen operation. Its two images lie in the commutator subgroups, and their class-two coordinates are $-m\exp_a x_0$ and $-m\exp_c y_0$ in the left and shifted right bases. The displayed difference must equal $1$, forcing $|m|=|\exp_T(\eta)|=1$. We may orient $T$ so that $m=1$.

In particular $D=\langle b\rangle$ and $[b,z]=1$ in the subgroup quotient $\langle b,z\mid R\rangle$ supplied by Howie's lemma. This quotient is abelian. Its abelianization is infinite cyclic because the nonzero exponent vector of $R$ is primitive, as follows from the ambient total exponent $-1$. Put $e=\exp_{a+b+c}(z)$ and $\alpha=\exp_z R$. The word
$$
(zb^{-e})^\alpha b^{-1}
$$
is primitive in $F(b,z)$ and has the same exponent vector as $R$. Its quotient is infinite cyclic with the same kernel as the quotient by $R$, since both quotient maps kill the commutator subgroup and impose the same exponent relation. Magnus's normal-closure theorem makes $R$ conjugate to this word up to orientation. The sign is fixed by the ambient total exponent $-1$. The width forces $\alpha\ne0$. [Magnus normal-closure theorem](https://arxiv.org/abs/0904.1143).

## One Laurent term is necessary

Let $X=x_0^{-1}$ in $F(a,b)$ and $Y=\sigma(y_0)$ in that same free group. In the intersection set $S=Tb^{-1}$. The conjugator $\eta$ has zero $b$ exponent in the basis $(b,S)$, so write $G(t)$ for its abelianized $S$-derivative with $S$ specialized to $1$ and $b$ to $t$. Equivalently this is its coordinate in the abelianization of the kernel of $\exp_b$ with basis $b^j S b^{-j}$. Then $G(1)=s=\exp_S\eta\in\{-1,1\}$. The left image of $S$ is $[X,b]$, and the shifted right image is $[Y,a]$.

Use the Alexander module of $F(a,b)$ with abelian variables $A_0,B_0$ in the basis $[a,b]$. The coordinates of $[X,b]$ and $[Y,a]$ are $\partial_a X$ and $-\partial_b Y$. Each conjugate of an $S$ letter contributes one signed Laurent translate on the appropriate side. Conjugation by $P$ multiplies the module coordinate by $B_0^{-1}$. The middle equation therefore requires
$$
G(B_0)\partial_a X+B_0^{-1}G(A_0)\partial_b Y=A_0^{-2}.
$$
Put $\lambda=\exp_a X$, $\mu=\exp_b Y$. Evaluating at the identity gives $\lambda+\mu=s$. Setting one abelian variable equal to $1$ at a time shows that $G(t)$ divides both
$$
1-st^{-1}[\mu]_t,\qquad t^{-2}-s[\lambda]_t,\qquad
[j]_t=\frac{t^j-1}{t-1}.
$$
A common nonzero root different from $1$ would satisfy
$$
t^\mu=1+s(t^2-t),\qquad
t^\lambda=1+s(t^{-1}-t^{-2}).
$$
Multiply the two identities, use $\lambda+\mu=s$, and clear $t^{-2}$. After dividing out $t-1$, the remaining factor is $t^3-t+1$ for $s=1$ or $t^3-t^2+1$ for $s=-1$, up to an overall sign. On the first cubic the expression for $t^\mu$ becomes $-t^5$, and on the second it becomes $-t^4$. Either would make $t$ a root of unity. Both cubics are irreducible over the rationals by the rational-root test and have a real root of absolute value different from one. They therefore have no root of unity. Since $G(1)=s$, the Laurent polynomial has no nonzero complex root and must be $G(t)=st^j$ for some integer $j$.

## The shortest lift of that term is impossible

Suppose $\eta=b^j S^s b^{-j}$. For $s=1$, the two free images give
$$
b^j[X,b]b^{-j}Q=P a^j[Y,a]a^{-j}.
$$
Isolating $YaY^{-1}$ and conjugating the resulting identity yields a necessary condition on $b^{-1}QaP^{-1}$. It must be a product of a conjugate of $b^{-1}$ and a conjugate of $a$. Explicitly, if $K=a^{-j}P^{-1}b^j$, then
$$
K^{-1}YaY^{-1}K=XbX^{-1}b^{-j-1}QaP^{-1}b^j,
$$
and conjugating the wing product by $b^j$ removes $j$. If $s=-1$, invert the isolated commutator equation to get the same condition with $P,Q$ interchanged.

A product of the two indicated conjugates is conjugate to $b^{-1}Z a Z^{-1}$ for some reduced $Z$. Strip initial $b$ powers and terminal $a$ powers from $Z$ by cyclic conjugation and free reduction. This gives a cyclically reduced word with $b^{-1}$ at the start, $a$ at the midpoint, and inverse intervening words. Both fixed targets are cyclically reduced of length fourteen. The replay checks every rotation with the indicated start and midpoint and finds no inverse-half match. The same calculation with $j=0$ also excludes $\eta=[b,T]^{\pm1}$ in the cyclic-power branch, since its images are $[T_L,b]^{\mp1}$ and $[\sigma(T_M),a]^{\mp1}$. [Exact rotation and polynomial controls](../results/round18_ac_proof_wirtinger_overlap.json).

Thus a survivor of the conjugated-overlap branch needs a nontrivial correction to $b^jS^s b^{-j}$ in the derived subgroup of $\ker(\exp_b:F(b,S)\to\mathbb Z)$. The remaining cyclic-power branch and these corrected conjugators have yet to be resolved.

~~~sh
set -o pipefail
python3 -B experiments/round18_ac_proof_wirtinger_overlap.py \
  | diff -u results/round18_ac_proof_wirtinger_overlap.json -
~~~
