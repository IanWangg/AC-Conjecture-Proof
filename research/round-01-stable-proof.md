# Round 01 · Stable Andrews–Curtis proof

2026-11-19

A geometric realization of a relator tuple descends through elimination
of a defining generator. Consequently, adding arbitrarily many defined
generators and rewriting the old equations with them cannot make the
initial AK(n) tuple geometric, for any n ≥ 2. This excludes a particular
way to reach a thickenable presentation. Stable AC remains unresolved.

## Why geometry is a target

Call a tuple *geometric* if its conjugacy classes can be represented
simultaneously by disjoint oriented simple closed curves on the boundary
of a marked orientable handlebody. Repetitions, if any, require disjoint
representatives. The marking identifies the handlebody's fundamental
group with the ambient free group. Hence geometry is invariant under a
simultaneous automorphism, independent conjugations, inversions and
permutations. A literal orientably thickenable presentation supplies such
curves with the specified crossings of the meridian disks. Geometry
allows the curves to record unreduced words relative to those disks.
[Lackenby, §3.1 and §6](https://arxiv.org/html/2606.06122v1)

For a balanced trivial tuple, geometry suffices for ordinary AC
triviality. From a geometric realization take a complete meridian disk
system in the handlebody and record the actual signed crossings of the
curves. Read in the disk system's basis, the resulting literal words are
a thickenable presentation of the trivial group. The curves, disk
system and attached 2-handles give the thickening. The new words differ
from the original group elements by the change of basis and choices of
basepoints and orientations. Lackenby's Theorem 1.3 gives ordinary
triviality of the literal presentation. Apply the inverse basis
automorphism to the sequence, then use usual Nielsen moves on the final
free basis. Equivalently, Theorem 6.4 removes the ambient automorphism
from the trivialization. A thickenable balanced trivial complex has an
orientable regular neighborhood, since that neighborhood has trivial
fundamental group. [Lackenby, Theorems 1.3 and 6.4](https://arxiv.org/html/2606.06122v1)

## Geometry descends through a defining equation

Let $F=F(X)$, adjoin a fresh $z$, fix $w\in F$, and let
$\rho\colon F(X,z)\to F$ fix $X$ and take $z$ to $w$. Call
$(s_1,\ldots,s_m,zw^{-1})$ a defining expansion of
$(r_1,\ldots,r_m)$ when $\rho(s_i)=r_i$ for every $i$. This includes
replacing selected occurrences of $w$ or $w^{-1}$ by $z$ or $z^{-1}$,
including across several relators, as well as any other lifts satisfying
the same retraction identity.

**Lemma.** If the expanded tuple is geometric, the original tuple is
geometric.

**Proof.** In a geometric realization let $C$ be the boundary circle
with free homotopy class $zw^{-1}$. This element is primitive because
substituting $z\mapsto zw^{-1}$ and fixing $X$ is an automorphism.
Algebraic and geometric primitivity agree for simple closed curves on
the boundary of a handlebody. Thus a properly embedded meridian disk
meets $C$ transversely once. Cutting along that nonseparating disk
exhibits the handlebody as a smaller handlebody with one 1-handle.
Attaching a 2-handle along $C$ cancels this 1-handle, leaving a handlebody.
Choose the attaching annulus disjoint from the other circles. They
remain disjoint simple boundary circles after the attachment. By
van Kampen, the map on fundamental groups kills exactly the normal
closure of $zw^{-1}$, and the quotient is naturally $F(X)$ via $\rho$.
The remaining circles therefore represent the $r_i$ in a marking of
the smaller handlebody. [Valdez-Sánchez, preceding Lemma 5.2](https://msp.org/gtm/2004/07/gtm-2004-07-002s.pdf)

For a balanced trivial input, the forward defining expansion is
available by stable AC moves. After adding the isolated pair $z,z$,
express $w^{-1}$ as a product of conjugates of the $r_i^{\pm1}$, then
multiply these into the new relator, restoring each donor after use.
This creates $d=zw^{-1}$. Since $r_i^{-1}s_i$ lies in the normal
closure of $d$, use the same construction with $d$ as donor to get each
$s_i$ while keeping $d$ at the end. The existence of a normal-closure
expression uses triviality of the input group.
[Lackenby, Proposition 2.1 and Lemma 2.8](https://arxiv.org/html/2606.06122v1)

An isolated destabilization preserves geometry in both directions. The
lemma handles removal, and the reverse direction uses a boundary
connected sum with a solid torus carrying a longitude disjoint from
all old curves. In a sequence of defining expansions, isolated
destabilizations and the basis and relator operations listed above,
geometry of the endpoint therefore implies geometry of the input.
There is no rank or word-length bound in this statement.

## Application to the initial AK(n) tuple

Use uppercase letters for inverses. The relators are
`(x^n Y^(n+1), xyxYXY)`. Their literal diagram has no compatible
spherical rotation. [Planar-link parity proof](research-w.md),
[independent review](research-t-w-topology-review.md)

The weighted Whitehead graph is K4 on $x,X,y,Y$. The weights of $xX$
and $yY$ are $n-1$ and $n$, respectively, and each of the four
remaining edges has weight two. The four cuts separating each pair of
inverse vertices have sizes

| Pair | Two singleton-side cuts | Two cuts with two vertices on each side |
| --- | ---: | ---: |
| $x,X$ | $n+3$ | $2n+3$ |
| $y,Y$ | $n+4$ | $2n+3$ |

A Whitehead length decrease would require one such cut to have size
less than the degree of the separated vertices. The degrees are
$n+3$ and $n+4$. Since $n\ge2$, no cut decreases length. Whitehead
minimization now gives global minimality of the displayed basis for the
two conjugacy classes. [Manning, Theorem 2.4](https://arxiv.org/pdf/0904.0724)

The multiclass is disk-busting. In a nontrivial free splitting of
$F_2$ each factor is cyclic. The exponent-sum determinant of the two
relators is one, so if both classes were elliptic, they would lie in
distinct factors and be conjugate to generators of those factors or
their inverses. This would give total cyclic length two in some basis,
contradicting the minimal length $2n+7$ just proved. Zieschang's
minimal-diagram theorem gives a realization of a geometric disk-busting
multiclass at its algebraically minimal cyclic length in the selected
basis. Every curve would then spell its cyclically reduced word. A
diagram in that basis would give the compatible spherical rotation
already excluded by the parity proof. Thus the multiclass is
nongeometric. [Zieschang, *Simple path systems on full pretzels*](https://www.mathnet.ru/eng/sm4303),
[Berge, §5](https://www.math.uic.edu/t3m/hg/old/heegaard/Documentation/Heegaard_Documentation.pdf)

In particular, the defining expansions used to compress relators into
triangles in Lackenby's Lemma 2.8 cannot produce a thickenable
presentation from the initial AK(3) tuple. The same applies to arbitrary
defining expansions interleaved with changes of ambient basis and
isolated destabilizations. [Lackenby, Lemma 2.8](https://arxiv.org/html/2606.06122v1)

## Scope and interaction with the ordinary-AC proof track

Elimination of a nonisolated defining equation is a different operation
from the isolated destabilizations allowed above. Eliminating by a
different relator can even implement an ordinary relator
multiplication. For distinct slots $i,j$, start with $r_i,r_j$, adjoin
$d=zr_j^{-1}$ and use the lifts $s_i=r_i r_j z^{-1}$, $s_j=z$. These
project to $r_i,r_j$ under $z\mapsto r_j$. Now eliminate $z$ using
$s_j=z$, which instead projects by $z\mapsto 1$. The remaining two
relators are $r_i r_j,r_j^{-1}$. Inverting the second realizes the
multiplication. A claim covering arbitrary defining eliminations would
need additional information at this step. AK(2) is an exact scope
control. Its initial tuple is nongeometric by the same cut and parity
arguments. The paired-rotation checker exhausts all 2,880 orders and
gives minimum genus one for its literal diagram. The existing certificate
replays to $(x,y)$ in 1,521 ordinary moves with a total length peak of 153.
[AK(2) certificate](../certificates/coupled_ak2_full.json)

The ordinary-proof track projects a rank-raising section with one fixed
extra generator $z$ if every vertex has some relator whose cyclically
reduced word contains exactly one occurrence of $z^{\pm1}$, allowing
the relator slot to change. At a geometric endpoint, eliminate its
one-occurrence relator by the lemma above. The projected endpoint is
geometric and therefore ordinarily trivial. Under the projection
hypothesis, such a stable geometric bridge already gives an ordinary
trivialization of the starting tuple. An AK(3) search can therefore
distinguish single-extra-generator paths whose geometry can be used at
the original rank from paths that pass through a vertex lacking that
one-occurrence relator.

Replay the AK(2) scope controls from the repository root.

```sh
python3 experiments/thickening_rotations.py xxYYY xyxYXY --output /tmp/ac_round01_ak2_rotation.json
python3 experiments/elementary_verify.py certificates/coupled_ak2_full.json
```
