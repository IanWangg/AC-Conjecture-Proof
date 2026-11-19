# Round 01 ordinary AC proof track

19 November 2026. A fixed extra generator can be eliminated from a class of stable paths even when the relator that solves for it changes. An extension using Magnus's theorem eliminates some segments with no such relator at intermediate states. A separate calculation gives a control for projections that retain an extra relator coordinate. The general conjecture and AK(3) remain open in this track.

## Projection along a path

Let $F=F(x_1,\ldots,x_n)$ and $G=F*\langle z\rangle$. Use ordinary AC inversion, right multiplication by another coordinate, and conjugation. Swapping two relators, signed multiplication, left multiplication, and word conjugation all expand into ordinary AC moves. These expansions take place in the same ambient free group throughout. [Panteleev and Ushakov, Sections 1.2 and 2](https://arxiv.org/html/1609.00325v1).

A **pivot for $z$** is a relator $p$ conjugate in $G$ to $(za^{-1})^{\pm1}$ for $a\in F$. A cyclically reduced representative of $p$ then contains exactly one $z$ or $z^{-1}$, and the converse follows by cyclic rotation and inversion. The unique word $a\in F$ is obtained by solving $p=1$ for $z$ while fixing $F$. Write $\pi_a:G\to F$ for this substitution. A projection of a tuple with pivot $p$ applies $\pi_a$ to each other coordinate and drops $p$. Fagan's stable substitution-and-removal lemma explains elimination at an individual trivial presentation. The argument here tracks several choices of pivot through rank-preserving moves. [Fagan, Lemma 3.2](https://escholarship.org/content/qt6fm617h4/qt6fm617h4.pdf?v=lg).

We use two elementary facts. With a donor $d$ occupying its own coordinate, AC can update another coordinate $u$ to $v$ while restoring all other coordinates whenever $u=v$ in $F/\langle\!\langle d\rangle\!\rangle$. Indeed, factor $u^{-1}v$ into conjugates of $d^{\pm1}$ and right multiply by those factors one at a time, conjugating or inverting the donor temporarily and restoring it each time. The same argument allows several retained donors. Also, for $a,b\in F$ and $d=ab^{-1}$, all evaluations $\pi_a(w)$ and $\pi_b(w)$ agree modulo $\langle\!\langle d\rangle\!\rangle$, because $a=b$ in that quotient. Factoring their difference can be done by replacing the occurrences of $z^{\pm1}$ one at a time. In each replacement the ratio of the new word to the old word is a conjugate of $d$ or $d^{-1}$.

**Lemma 1.** All pivot choices at a given tuple have AC-equivalent projections in $F$.

**Proof.** Suppose pivots $p,q$ solve $z=a,b$, respectively. Project using $p$ and keep $\pi_a(q)$, or project using $q$ and keep $\pi_b(p)$. Both kept relators are conjugate to $d=ab^{-1}$ or $d^{-1}$, since their unconjugated forms are powers of sign ±1 of $ab^{-1}$ and $ba^{-1}$. Put the kept relators in the same position by a relator permutation and normalize them to $d$. The remaining coordinates are evaluations of the same words under the two substitutions. Replace each while keeping $d$ via the two facts above. If $a=b$, the evaluations coincide and the kept relators are identities. ∎

**Proposition 2.** Let an ordinary AC path in $G$ have a pivot for the same $z$ at every vertex. Arbitrary pivot projections of its two endpoints are ordinarily AC-equivalent in $F$. The conclusion holds without assuming triviality or requiring an actual destabilization at either endpoint.

**Proof.** Each step changes at most one coordinate. If an unchanged pivot is present at both vertices, select it on both sides by Lemma 1. Its evaluation sends the move to the corresponding move in $F$, except that multiplication by the erased pivot evaluates to the identity operation. If there is no unchanged pivot, the changed coordinate is the pivot before and after the step. Inversion and conjugation leave its substitution unchanged. It remains to consider right multiplication $p'=pq$ by an unchanged coordinate $q$. Let the old and new pivots solve $z=a$ and $z=b$. As $q=p^{-1}p'$, we have $\pi_a(q)=\pi_a(p')$ and $\pi_b(q)=\pi_b(p^{-1})$. Again both are conjugate up to inversion to $d=ab^{-1}$. Normalize both to $d$ and change the other evaluations while keeping it. Inverse edges follow by reversing their compiled paths. Lemma 1 lets the projected steps be concatenated despite changes in the pivot choice. ∎

In particular, for $n$-tuples $R,S$ in $F$, starting from $(R,z)$ and ending at $(S,z)$ through this class of paths in $G$ is equivalent to ordinary AC equivalence of $R,S$. One direction is Proposition 2 with the endpoint pivots $z$. The reverse direction appends the unchanged $z$ to every state of an ordinary path. This holds for any words and with any positive finite $n$. It places no length bound on the moves that implement the projected path.

## Segments with a single other donor

**Proposition 3.** Write the two endpoint tuples as $(p,q,U)$ and $(p',q,U)$ in $G$, where $p,p'$ are pivots for $z$. If the normal closures of $\{p,q\}$ and $\{p',q\}$ in $G$ coincide, then their projections using $p,p'$ are ordinarily AC-equivalent in $F$. Thus some path segments with pivotless intermediate states can also be eliminated.

**Proof.** Let the endpoint substitutions be $z=a,b$, and set $d=ab^{-1}$. Evaluation at $a$ sends $p$ to 1 and $p'$ to a conjugate of $d^{\pm1}$. Applying it to the equality of normal closures gives $d\in\langle\!\langle\pi_a(q)\rangle\!\rangle$. Evaluation at $b$ similarly gives $d\in\langle\!\langle\pi_b(q)\rangle\!\rangle$. The two evaluations of $q$ agree modulo $d$, so the normal closures of $\pi_a(q)$ and $\pi_b(q)$ coincide in $F$. Magnus's normal-closure theorem therefore makes them conjugate up to inversion. Normalize the two projected donor words to $\pi_a(q)$ and change all evaluations of $U$ while keeping that donor, using the fact that it normally contains $d$. This also handles the identity donor, which forces $d=1$. [Bogopolski and Sviridov, Theorem 1.1 citing Magnus](https://msp.org/gtm/2008/14/gtm-2008-14-004s.pdf). ∎

For example, the hypothesis is automatic if all changed coordinates and all multiplication donors in a segment belong to the two slots occupied by $p,q$, with $q$ restored at the end. Conjugating words can use the entire ambient basis. Given the segment, a compilation can check conjugacy of the evaluated donor words directly in the free group, and enumerate a factorization of $d$ in the normal closure of the donor, guaranteed by the proof. The endpoint condition can also be used without retaining the segment if factorizations witnessing the two normal-closure inclusions are available.

There is a quotient version. Append a common list $L\subset F$ of fixed $z$-free donors, and assume equality of the normal closures generated by $(p,q,L)$ and $(p',q,L)$ in $G$. In $K=F/\langle\!\langle L\rangle\!\rangle$ the projected $q$ words then have the same normal closure by the proof above. If these particular images are conjugate up to inversion in $K$, lift a conjugator to $F$. The projected donor moves to the other by conjugation or inversion followed by corrections using $L$. The $U$ coordinates are then corrected using that donor and $L$. The Magnus property of $K$ is sufficient for the needed conjugacy. This reduces the use of a second $z$-free donor to a specific marked conjugacy problem in its deletion quotient.

## Controls on retraction

A single-stabilization excursion can lose every pivot even when it starts at the free basis. In $F(x,z)$ four positive right multiplications give

```
(x,z) -> (xz,z) -> (xz,zxz) -> (xzzxz,zxz) -> (xzzxz,zxzxzzxz)
```

The last words contain three and five $z$'s, respectively, with positive signs. After $z=1$, their images are $x^2,x^3$. The pair generates $F(x)$, but neither singleton normally generates $F(x)$. The walk can be reversed to make an excursion with isolated $z$ at both ends. This gives an explicit failure of dropping one coordinate at every retracted vertex. Nor can the one-donor hypothesis of Proposition 3 be assumed on a general pivotless segment, since the kept relators can change under several independent multiplications.

**Proposition 4.** Every normally generating pair $(r,s)$ of $F(x,y)$ has a finite AC path $(r,s,1)\to(x,y,1)$ on three relator coordinates in that same $F(x,y)$.

**Proof.** Factor $x$ as a product of conjugates of $r^{\pm1},s^{\pm1}$. Accumulate these factors in the third coordinate, restoring each donor after use. In the first two coordinates substitute $x=1$ by deleting one occurrence at a time with $x$ as the donor, giving powers $y^i,y^j$. Their images normally generate the quotient $F(x,y)/\langle\!\langle x\rangle\!\rangle=\langle y\rangle$, so $\gcd(i,j)=1$. Ordinary relator multiplication, inversion and permutation implement the Euclidean algorithm and give $(y,1,x)$, then $(x,y,1)$. ∎

For AK(3), let $p=x^3y^{-4}$, $b=xyxy^{-1}x^{-1}y^{-1}$, and write uppercase letters for inverses in the saved trace. The identity below uses the products computed in the [torus-quotient study](research-g.md) and [its parameter-uniform extension](research-h.md), now interpreted wholly as free-word identities with a spare coordinate.

$$
f=(x^2bx^{-2})(xbx^{-1})b,
\qquad D=(pyp^{-1}y^{-1})((yx)p(yx)^{-1}),
\qquad f=D b^{-1}x.
$$

Indeed $f=x^3 yx y^{-3}x^{-1}y^{-1}$ by free reduction, and direct substitution of $p$ gives $D=f(b^{-1}x)^{-1}$. Thus $x=bD^{-1}f$ uses seven signed conjugates of $p,b$. The exact control accumulates $x$ in the third coordinate and finishes at $(1,y,x)$ in 92 operations, with conjugations by one signed letter and peak total length 28. The same construction is tested for $2\le n\le8$. These three-coordinate paths used only two ambient generators. A legal stabilization would introduce $z$ and a relator $z$, so a three-coordinate free-word path starting with an identity in $F(x,y)$ is outside both conjectures' certificate formats. In particular, getting such a path by applying the map $z\mapsto1$ to a rank-three certificate adds no evidence for ordinary AK(3) equivalence beyond normal generation.

```sh
python3 -B experiments/round01_ac_proof_controls.py | diff - results/round01_ac_proof_controls.json
```

## Interaction with the stable proof track

The [stable proof track](round-01-stable-proof.md) shows that projecting a geometric tuple through a primitive pivot gives a geometric quotient tuple, using a dual disk for the attaching curve. Proposition 2 applies even when the rank-$(n+1)$ endpoint is merely geometric and carries a pivot. Taken together, the results give an ordinary AC certificate strategy for any balanced trivial rank-$n$ tuple. Add $z$, use a path covered by Proposition 2 or by concatenating supported segments from Proposition 3, and test whether a rank-$(n+1)$ waypoint has a geometric realization and a pivot for $z$. The projected endpoint is geometric, so Lackenby's result supplies ordinary AC triviality. For AK(3), this makes recognition of such a waypoint a distinct search target from matching $(x,y,z)$. The existence of a path to such a waypoint is unresolved. [Lackenby, Theorems 1.3 and 6.4](https://arxiv.org/html/2606.06122v1).
