# Exact reciprocal archive test at the second energy-20 waypoint

2026-11-19. With `xxxxyXXYY` held fixed at the second energy-20 waypoint, the quotient conjugacy test finds two compatible donors in the complete marked archive of 23,902 verified trivial pairs. Both are reached by strict forward paths. Three reciprocal contacts remain, all excluded by explicit finite permutation markings. This establishes failure for this full orientation of the two-block splice, allowing arbitrary word lengths in both blocks. A separate projective marking excludes an arbitrary-length primitive replacement with `xxyyxYYYxxY` fixed. Together with the other track's results this covers all four frozen-donor directions of the two new waypoints. [Strict AK(3) entry](../certificates/round12_ak3_second_energy20.json), [exact scans and witnesses](../results/round12_ac_proof_amalgam_archive.json), [other frozen directions](round-12-ak3.md).

## Quotient conjugacy normal form

Write $D=\texttt{xxxxyXXYY}$, $R=\texttt{xxyyxYYYxxY}$ and let $Q=F(x,y)/\langle\!\langle D\rangle\!\rangle$. With $t=x^2$ and $b=y$, the quotient is the amalgam $H*_{t=x^2}\langle x\rangle$, where $H=\langle t,b\mid t^2 b=b^2t\rangle$. In $H$ let $u_i=b^i (tb^{-1})b^{-i}$. The relation is $u_2=u_0u_1$, so $H=U\rtimes_\beta\langle b\rangle$ for $U=F(u_0,u_1)$, with $\beta(u_0)=u_1$ and $\beta(u_1)=u_0u_1$. Conjugation by $t=u_0b$ is $\alpha=\operatorname{Inn}(u_0)\beta$. Both $t$ and $b$ have height one in $H$. In particular $H=U\rtimes_\alpha\langle t\rangle$. [Amalgam derivation and strict waypoint calculation](round-12-ak3.md#the-second-energy-20-waypoint).

Let $V=xUx^{-1}$. An equivalent presentation is $Q=(U*V)\rtimes_\phi\langle x\rangle$, where $\phi(u)=xux^{-1}\in V$ and $\phi(xux^{-1})=\alpha(u)\in U$. Indeed, adjoining the generators for $V$ records the conjugation by $x$. Substituting them out gives exactly the relation that $x^2$ acts on $U$ by $\alpha$. In the checker, $a,b,c,d$ represent $u_0,u_1,xu_0x^{-1},xu_1x^{-1}$, respectively. The forward images are `c,d,abA,aabA`. The inverse images are `dC,cDcdC,a,b`. The checker verifies both compositions. The original $y$ is $u_0^{-1}x^2$.

The height character of $Q$ is $\chi(x)=1$ and $\chi(y)=2$. Since $\chi(R)=1$, a candidate must have height $1$ up to inversion. Orient it to height $1$ and write it as $w x$, with $w\in U*V$. Split the reduced $w$ into alternating nonempty syllables in the two factors. If its first and last syllables lie in different factors, conjugate by the first syllable's inverse. This moves the first syllable to the end with $\phi$ applied, so it merges with the last. Continue until the syllable count is zero or odd. If the first syllable is in $V$, conjugate by $x$ to begin in $U$.

An odd $r$-syllable result represents a cyclically reduced amalgam word with $2r$ syllables. Substitution of the $V$-syllables by $x U x^{-1}$ gives this explicitly, and every nonempty $U$-syllable lies outside $\langle t\rangle$ by height. The zero-syllable case represents a conjugate of $x$. The receiver $R$ is conjugate to $u_{-3}^2 x$ and has two amalgam syllables. Only a one-syllable result $q\in U$ can match. The conjugacy theorem for amalgams allows cyclic permutations followed by conjugation by an element of the amalgamating subgroup. Aligning the $H$-syllables first in both two-syllable words then gives $q=\alpha^k(u_{-3}^2)$, as $t^k$ commutes with $x$. [Amalgam conjugacy criterion, §4.2](https://eprints.maths.manchester.ac.uk/113/1/amalgam_Ie.pdf).

The action of $\alpha$ on $U^{\rm ab}$ is the Fibonacci matrix $M=\begin{pmatrix}0&1\\1&1\end{pmatrix}$. The vector for $\alpha^k(u_{-3}^2)$ is $2M^{k-3}(1,0)^T$. The forward and backward Fibonacci sequences give at most one such $k$, found by stopping when each sequence's increasing absolute norm exceeds the candidate norm. The algorithm first performs the syllable and Fibonacci tests in the quotient with both free factors abelianized separately. This quotient preserves the factors and the action of $\phi$, so rejection there is sufficient. Remaining candidates are then tested for equality of the exact reduced free words in $U$.

## Complete archive and strict controls

| Stage | Candidate donor keys |
| --- | ---: |
| Signed marked donor keys from the verified reverse pairs | 147,060 |
| Height of absolute value one | 23,839 |
| One syllable after reduction in the quotient by the two factor commutators | 1,890 |
| Fibonacci orbit match | 132 |
| Exact reduced free word match | 2 |

Both surviving donors appear in the first completed forward chart stage. Compiling those conversions and independently replaying each produces strict ordinary paths of 86 and 60 moves from the second energy-20 waypoint. The finite reciprocal test compares the image of $D$ with each associated reverse receiver after killing the common donor. Cycle types distinguish all three and are unchanged under inversion. The exact archive suffixes for those three receivers replay to `(x,y)`. [First forward ledger](../certificates/round12_ac_proof_amalgam_forward1.json), [second forward ledger](../certificates/round12_ac_proof_amalgam_forward2.json), [permutations, cycle types and suffix sources](../results/round12_ac_proof_amalgam_archive.json).

| Common donor | Archive receiver | Separating group |
| --- | --- | --- |
| `XXXXYYxxyyyXYYYYxxxxyy` | `XXXXYYxxyyyXYYYYxyyxxYYxxyy` | $S_9$ |
| `XXXXYYxxyyyXYYYYxxxxyy` | `XXYYxyy` | $S_9$ |
| `XXXXyxxyyxYxxYY` | `XXXyXYY` | $S_{10}$ |

The fixed donor $D$ can first be changed instead, or the path can alternate receivers again after a failed reciprocal splice. Those directions remain outside this test.

## The other frozen primitive direction

With $R$ fixed, orient a candidate primitive so its exponent vector is $(2,-1)+k(5,-2)$ for some $k\in\mathbb Z$. For $k\ge0$ the classes are represented by `xxY (xxYxxYx)^k`. For $k\le-1$, the inverses are represented by `xxxY (xxxYxxY)^j` with $j=-k-1\ge0$. In each family the initial word and period form a free basis, verified by Stallings folding, so the displayed representatives are primitive. The vectors run through the required slopes, and rank-two primitive uniqueness makes the list exhaustive. [Primitive slope uniqueness, Osborne–Zieschang §3.2](https://geodesic.mathdoc.fr/item/IM_1981__63_142788/).

In $\mathrm{PSL}_2(11)$ take the lifts below. The image of $R$ upstairs is $-I$, so this gives a quotient representation that kills the frozen row. The squared trace of $D$ is $9$. In both tails the period has projective order five and the squared traces belong to $\{0,1,5\}$, for all exponents and for their inverses. Since squared trace is invariant under conjugation and independent of the lift's sign, no primitive replacement exists at any length. [Exact matrix and residue replay](../results/round12_ac_proof_amalgam_archive.json).

~~~text
x = [[0,10],[1,1]]
y = [[0,2],[5,4]]
~~~

## Free-by-cyclic marking for the other reciprocal orientation

Let $u=x^2y^{-1}$ and $v=x^3y^{-1}$ and set $p=uv$. The pair $(u,p)$ is a basis, since $x=u^{-1}pu^{-1}$ and $y=u^{-1}x^2$. Write $p_i=u^ipu^{-i}$. In this marking the second energy-20 receiver `xxyyxYYYxxY` has height zero and Schreier word

$$
p_{-1}p_{-3}p_{-6}p_{-8}p_{-11}p_{-10}^{-1}p_{-8}^{-1}p_{-5}^{-1}p_{-3}^{-1}.
$$

Each extreme index occurs once. Naming $p_{-11},\ldots,p_{-2}$ by $a,\ldots,j$ gives a rank-ten free-by-cyclic quotient with shift images `(b,c,d,e,f,g,h,i,j,igdbADFI)`. The final image contains exactly one $a^{-1}$, so the images form a free basis. The row `xxxxyXXYY` has height one and kernel factor $p_{-1}p_{-3}p_{-5}p_{-7}p_{-8}^{-1}p_{-6}^{-1}p_{-3}^{-1}p_{-1}^{-1}$. This provides explicit input for testing the other reciprocal orientation.

## Reproduction

Use the verified cap-56 reverse TSV with its adjacent `.sources.json` and the original archive zip directory. [Archive replay commands](round-04-ak3.md#reproduction).

~~~sh
python3 -B experiments/round12_ac_proof_amalgam_archive.py "$reverse" --archives "$archives" \
  | diff - results/round12_ac_proof_amalgam_archive.json
~~~
