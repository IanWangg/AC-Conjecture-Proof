# A free-word restriction on width-two Wirtinger shifts

2026-11-19. A width-two singleton solution of the aligned Wirtinger middle equation must have determinant two. Stripping maximal powers of the affected letter from both ends of the shift word must leave a conjugate of the inverse square of the unaffected letter. The proof gives these necessary conditions without a bound on the shift word or the middle conjugator. [Width-two reduction](round-13-ac-proof.md), [minimum input count](round-14-ac-proof.md), [sign test](../results/round15_ac_proof_wirtinger_sparse.json).

## The count for arbitrary shift words

In the upper case put $c=a$, $d=b$, $U=P^{-1}gQ$, $L=P$, and $R=Q^{-1}$. In the lower case put $c=b$, $d=a$, $U=g$, $L=P^{-1}$, and $R=Q$. The equations in both conventions become

$$
\theta(U)=LUR,\qquad \theta(c)=d,\quad \theta(d)=W.
$$

The words $P=a^{-1}bab^{-2}$ and $Q=a^{-2}ba^2b^{-2}$ are fixed. Let $\Delta\in\{0,2\}$ be the determinant in the two remaining cases and let $\epsilon\in\{-1,1\}$ be the singleton sign. Then $W$ has exponent vector $(-\Delta,1+\Delta+\epsilon)$ in the ordered basis $(c,d)$. The word $U$ has zero exponent vector, distinguished class-two coordinate $\Delta-1$ on $[c,d]$, and at least four occurrences of $d^{\pm1}$. The shift word contains the letter $c^{\pm1}$ because the opposite Magnus subgroup embeds freely on $d,W$. [Round 13 exponent calculation](round-13-ac-proof.md), [Round 14 free-word bound](round-14-ac-proof.md).

Write $W=d^p Vd^q$ by stripping maximal end powers of $d$. The nonempty reduced word $V$ begins and ends in $c^{\pm1}$. Write $V=JTJ^{-1}$ by cyclic reduction, so $T$ is nonempty. Write the reduced input with its individual affected letters,

$$
U=c^{e_0}d^{\sigma_1}c^{e_1}\cdots d^{\sigma_m}c^{e_m},\qquad \sigma_i\in\{-1,1\}.
$$

Set $p_+=p$, $q_+=q$, $p_-=-q$, $q_-=-p$. The substitution initially has the form $d^{f_0}V^{\sigma_1}d^{f_1}\cdots V^{\sigma_m}d^{f_m}$, with

$$
f_0=e_0+p_{\sigma_1},\quad
f_i=e_i+q_{\sigma_i}+p_{\sigma_{i+1}}\ (1\le i<m),\quad
f_m=e_m+q_{\sigma_m}.
$$

At a sign change $f_i=e_i\ne0$ by reduction of $U$. An interior separator with $f_i=0$ therefore joins two powers of $V$ of the same sign. After all such joins, let $k$ be the number of remaining $V$ powers. The corresponding exponents have absolute values summing to $m$. Both signs occur, so $k\ge2$. Every nonempty reduced power of $V$ begins and ends in $c^{\pm1}$ and satisfies $|V^v|_d=|v||T|_d+2|J|_d$, where $|Z|_d$ counts the individual letters $d^{\pm1}$ of the reduced word $Z$. The nonzero $d$ separators therefore prevent any further cancellation. Also $\sum_i f_i=0$ by the two zero exponent sums of $U$, and at least one $f_i\ne0$ by the sign change. This gives

$$
m|T|_d+2k|J|_d+\sum_{i=0}^{m}|f_i|
=|\theta(U)|_d=|LUR|_d\le m+6,\qquad \sum_{i=0}^{m}|f_i|\ge2.
$$

The six in the upper bound is $|L|_d+|R|_d$ in each convention. Since $m\ge4$, this excludes $|T|_d\ge3$.

The class-two coordinate can be computed directly with the modified gaps:

$$
\Delta-1=\sum_{i=0}^{m} f_i\sum_{j=i+1}^{m}\sigma_j .
$$

Indeed, replacing powers $e_i$ by $f_i$ is the substitution fixing $c$ and sending $d$ to $c^pdc^q$. Its determinant is one, so it preserves the $[c,d]$ coordinate for a word with zero exponent vector. In the word after the substitution the coefficient of the degree-two Magnus monomial $cd$ adds the signed $c$ prefix exponent at every $d$ letter, which gives the formula.

## Two affected letters in the cyclic core are impossible

If $|T|_d=2$, the count forces $m=4$ and $|J|_d=0$. Among the five separators exactly one is $+1$ and one is $-1$. The two sides each have all ten of their affected letters after reduction. In particular the affected sign sequence on the right is the concatenation of the sequences of $L$, $U$ and $R$.

The possible input signs are $(s,s,-s,-s)$ or $(s,-s,-s,s)$ with $s\in\{-1,1\}$. The alternating sequences have three sign changes and need three nonzero separators. The $(s,-s,-s,s)$ sequence needs $f_1=-f_3=\pm1$ and has class-two coordinate $-sf_1+sf_3=\mp2$. For $(s,s,-s,-s)$ the only class-two values $\pm1$ occur when the nonzero pair is $(f_1,f_2)$ or $(f_2,f_3)$. One separator at an end would instead leave only $f_2$ in the class-two sum with weight $-2s$. Thus $f_0=f_4=0$.

On the left the first and last pairs of signs are those of $V^s$ and $V^{-s}$. Each pair is obtained from the other by reversing and changing signs. The lower right side begins $-+$ and ends $++$, contradicting this relation. The upper right side begins $+-$ and ends $+-$, so all four copies of $V^{\pm1}$ on the left have signs $+-$. The upper right side has third sign $-$. This forces $f_1=-1$ and $f_2=1$ on the left. The first five signs on the left are then $+--+-$, while on the right they are $+--++$ when $s=1$ and $+----$ when $s=-1$.

A finite replay considers six balanced input sign sequences, twenty choices of the two labeled separator positions, and four possible sign pairs for the core, for each side and determinant. In each of the four sets of 480 cases, reducedness excludes 400 and the class-two condition excludes 64. The comparison of affected signs excludes the remaining 16. This test uses only signs and is independent of both $\epsilon$ and the $c$-power lengths. [Replay](../experiments/round15_ac_proof_wirtinger_sparse.py).

## One affected letter in the cyclic core is impossible

If $|T|_d=1$ and $|J|_d>0$, the count forces $k=2$, $|J|_d=1$, and $\sum_i|f_i|=2$. Thus the two opposite sign blocks of the input each contain $n=m/2\ge2$ affected letters. The only nonzero interior separator, at their sign change, is $f_n=\pm1$. The class-two formula then has absolute value $n$, contrary to $|\Delta-1|=1$.

Consequently the case $|T|_d=1$ requires

$$
W=d^p c^\ell d^\eta c^r d^q,\qquad
\ell r\ne0,\quad \ell+r=-\Delta,\quad \eta\in\{-1,1\},\quad
p+q=1+\Delta+\epsilon-\eta.
$$

For this form, let $F=\sum_i|f_i|$. The reduced left side has $m+F$ affected letters, so reducing $LUR$ removes exactly $(6-F)/2\le2$ pairs of affected letters. The freely reduced middle factor survives because losing it would require pairing all $m\ge4$ of its affected letters with exterior letters. In particular any affected letter removed from $L$ or $R$ consumes a distinct pair. An affected letter's height is the signed $c$ exponent of its prefix. This height stays fixed for every surviving letter under free reduction.

In the upper convention the first affected letter of $L$ is at height $-1$ and the last affected letter of $R$ is at height $-2$. Each survives. Removing either would first cancel all three affected letters of its fixed exterior factor. In the lower convention $L$ has affected heights $(2,1)$ and $R$ has heights $(1,1,2,2)$, where $R$ starts at the height $1$ carried by $LU$. The last affected letter of $R$ survives.

When $\Delta=0$, the left side lies in $\langle d,c^\ell d c^{-\ell}\rangle$ and every affected letter has height $0$ or $\ell$. The upper surviving heights $-1,-2$ are incompatible with this set. The lower surviving height $2$ forces $\ell=2$, so all three height-one letters of the fixed exterior factors would have to be removed, exceeding the two pairs available.

When $\Delta=2$, all separators $d^{f_i}$ have even height. Within the expanded copies of $V$ and $V^{-1}$, every affected letter has height $\ell$ modulo two. These heights persist after reduction. A nonzero $f_0$ or $f_m$ gives the first or last affected letter height zero, respectively. With a zero end separator the corresponding height lies in $\{\ell,\ell+2\}$. For the first end this follows from the initial $c$ powers of $V$ and $V^{-1}$, which are $\ell$ and $-r=\ell+2$. At the last end the final copy of $V$ or $V^{-1}$ has total $c$ exponent $-2$ or $2$ and finishes at height zero, giving the same pair of possibilities. The upper surviving heights $-1,-2$ require two zero end separators and have different parity. In the lower case the surviving final height $2$ requires $f_m=0$ and $\ell=2$ because $\ell$ is nonzero. Every affected letter on the left then has even height. The three height-one exterior letters again need more cancellation than is available.

## The remaining shift family

The nonempty cyclic core has zero affected letters, so $T=c^{-\Delta}$ and $\Delta=2$. Thus the necessary form is $W=d^p J c^{-2}J^{-1}d^q$, where $J c^{-2}J^{-1}$ is reduced and begins and ends with $c^{\pm1}$, and $p+q=3+\epsilon$ is $2$ or $4$. In particular this excludes every shift word beginning and ending with $c^{\pm1}$.

The class-four condition modulo $3$ further restricts $J$. Write $J=c^u d^v[c,d]^z$ modulo $\gamma_3$. Replacing $J$ by $Jc^{-u}$ preserves the conjugate of $c^{-2}$ exactly. Modulo $\gamma_3$ this replaces $J$ by $d^v[c,d]^{z+uv}$. Consequently $W$ has the same class-three image as

$$
d^{j}[c,d]^{z'}c^{-2}[c,d]^{-z'}d^{3+\epsilon-j},
\qquad j=p+v,\quad z'=z+uv.
$$

Modulo $3$, increasing $j$ by three transfers the central series $1+d^3$ between the two ends in the class-three Magnus expansion, where $d^3$ denotes the third-degree monomial. This leaves the expansion unchanged. Increasing $z'$ by three also leaves the expansion unchanged. Applying the Round 14 mod-$3$ table to these nine inputs in each convention and sign yields the following sole allowed residue of $z'$ for a given $j$.

| Singleton | $\epsilon$ | $j\equiv0$ | $j\equiv1$ | $j\equiv2$ |
| --- | ---: | ---: | ---: | ---: |
| Upper | $-1$ | $1$ | $0$ | $0$ |
| Upper | $1$ | $1$ | $2$ | $1$ |
| Lower | $-1$ | $0$ | $0$ | $1$ |
| Lower | $1$ | $2$ | $1$ | $1$ |

In particular, $\epsilon=1$ excludes $J=1$ and every conjugating word with $z+uv\equiv0\pmod3$. [Round 14 class-four conditions](round-14-ac-proof.md#the-complete-degree-four-condition-in-determinant-two), [residue calculation](../experiments/round15_ac_proof_wirtinger_sparse.py).

The remaining family must still satisfy the full middle equation and the outer membership condition. The ordinary conjecture remains unresolved.

~~~sh
set -o pipefail
python3 -B experiments/round15_ac_proof_wirtinger_sparse.py \
  | diff -u results/round15_ac_proof_wirtinger_sparse.json -
~~~
