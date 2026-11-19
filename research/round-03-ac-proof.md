# Round 03 · Ordinary Andrews–Curtis proof

2026-11-19. This round establishes projection rules for marked free quotients and relative free bases. Overlap of all but one relator suffices for a marked-quotient exchange even when deleting the common rows gives a nonfree group. For relative-basis frames, every choice of frame at a vertex gives the same ordinary AC orbit, including the exchange-disconnected example from [round 02](round-02-ac-proof.md). A padded path descends when each vertex has a frame whose actual words complete the same marked base to a free basis.

## Marked-quotient exchange with a possibly nonfree common quotient

Write $F=F(X)$ with $|X|\geq2$, $G=F(X\cup Z)$, and $|Z|=k$. A marked free-quotient frame is a choice of $k$ relator slots $A$ such that $F\to G/\langle\!\langle A\rangle\!\rangle$ is an isomorphism. Denote the resulting retraction by $\rho_A:G\to F$. Projection applies it to the other slots and discards the frame. Write $\langle\!\langle D\rangle\!\rangle$ for normal closure in the indicated ambient group. For a rank-one base, the normal closure of the projected singleton is the intersection of $F$ with the normal closure of all padded relators, so the singleton is fixed up to inversion along a padded AC path.

Suppose two frames at a vertex are $S+p$ and $S+q$, where $S$ is the common block of $k-1$ slots. With $\rho_p=\rho_{S+p}$ and $\rho_q=\rho_{S+q}$, let

$$
a=\rho_p(q),\qquad b=\rho_q(p).
$$

The two quotients $F/\langle\!\langle a\rangle\!\rangle$ and $F/\langle\!\langle b\rangle\!\rangle$ are both $G/\langle\!\langle S,p,q\rangle\!\rangle$ via the identity on the original marking $X$. Consequently $\langle\!\langle a\rangle\!\rangle=\langle\!\langle b\rangle\!\rangle$ in $F$. The Magnus normal-closure theorem gives conjugacy up to inversion. Both retractions evaluate every other word identically in the common quotient. Place the retained donor in the same slot and normalize its word to $a$. While retaining it, multiply the other rows by suitable products of conjugates of $a^{\pm1}$ to match the projections. Each factor is an ordinary AC operation expanded by temporarily changing and restoring the donor. If $a=b=1$, the two projections already agree up to ordering. The intermediate quotient by $S$ is unrestricted. [Bogopolski and Sviridov, Theorem 1.1 recalling Magnus](https://msp.org/gtm/2008/14/gtm-2008-14-004s.pdf), [round 01 correction by frozen donors](round-01-ac-proof.md#projection-along-a-path).

The same argument plugs a gap with endpoints $(S,p,d,U)$ and $(S,p',d,U)$. Here both indicated frames give marked free quotients, and we require

$$
\langle\!\langle S,p,d\rangle\!\rangle
=\langle\!\langle S,p',d\rangle\!\rangle
$$

in $G$. Projected copies of the retained donor $d$ have equal normal closure by the common marked quotient, and the retained block $U$ agrees modulo that normal closure. The end projections therefore lie in the same ordinary AC orbit. A special case is a product modifying one selected slot $p\mapsto p d^{\pm1}$ while its other selected slots stay fixed. If $d$ is also selected, the marked retraction is unchanged. Inversion and conjugation of a selected slot preserve its normal closure.

Thus one can project any padded path for which sufficiently many compatible frames are available. Across each elementary edge it suffices to choose endpoint frames sharing $k-1$ unchanged slots. A frame that omits the receiver is available on both sides. When both choices contain the receiver, they have exactly the same slots, and the preceding case applies. At any intermediate vertex, incoming and outgoing choices can be connected by successive one-row exchanges.

## Exchange across arbitrary relative-basis frames

Call $A$ a relative-basis frame if, after individual conjugations and inversions, its $k$ words adjoin to $X$ to form a free basis of $G$. Its normal closure gives a marked free quotient as above. A frame is called an exact relative-basis frame when the actual selected words already extend $X$.

**Theorem.** Any two relative-basis frames at a single vertex give ordinary AC-equivalent projections, with arbitrary overlap.

**Proof.** First kill the common slots. The resulting group is free on $X$ together with the remaining basis representatives of the first frame. The analogous statement holds for the second frame, since every subset of its normalized words is part of that marked basis. Killing the shared slots is unaffected by differing choices of their conjugations or orientations. We can thus take the reduced frames to be disjoint and independently normalize their words. This normalization affects each projection only by ordinary inversions and conjugations of the retained opposite-frame rows.

Let their residual size be $m>0$. Use the first frame as the auxiliary basis $Z=(z_1,\ldots,z_m)$ after killing the common slots. Let $\rho$ kill $Z$, and choose $\alpha\in\operatorname{Aut}(F*F(Z))$ fixing $X$ and sending $Z$ to the second frame. The two projected lists of retained opposite-frame rows are

$$
r=\rho\alpha(Z),\qquad s=\rho\alpha^{-1}(Z).
$$

Define an automorphism $\tau$ fixing $X$ by $\tau(z_i)=z_i r_i^{-1}$. Then $\beta=\alpha\tau$ fixes $X$ and satisfies $\rho\beta=\rho$. Theorem 1 of Piggott identifies exactly these automorphisms with the formal AC automorphisms. Its two tests hold here: $X,\beta(Z)$ is a basis, and $\rho\beta(Z)$ is the tuple of identities. Consequently, evaluating $\beta^{-1}(Z)$ at any tuple in $F^m$ gives an ordinary AC transform of that tuple. Use the input $(r_1^{-1},\ldots,r_m^{-1})$. Its evaluation map is $\rho\tau$, and the output is

$$
\rho\tau\beta^{-1}(Z)=\rho\alpha^{-1}(Z)=s.
$$

This relates the two donor lists by ordinary moves restricted to those slots. The other remaining rows project identically modulo $\langle\!\langle r\rangle\!\rangle=\langle\!\langle s\rangle\!\rangle$, since the common quotient kills the union of the two original frames. Correct these rows by conjugates of the now matched donor list. The case $m=0$ has the same marked retraction and survivor list. This proves the theorem. [Piggott, Theorem 1](https://www.degruyterbrill.com/document/doi/10.1515/JGT.2007.029/html).

**Corollary.** If each vertex of a fixed padded rank path admits an exact relative-basis frame over the same $X$, the projected endpoints are ordinary AC-equivalent in $F$.

For inversion, conjugation and swap, transport the frame and then use the theorem to compare to the frame chosen at the next vertex. Conjugating a selected row can transport an exact frame to a relative-basis frame, which suffices for this step. A multiplication of $r$ by $q^\epsilon$ has $r'=r q^\epsilon$ with $\epsilon=\pm1$. If one endpoint has an exact frame avoiding the receiver, use it on both sides. Otherwise choose exact frames containing the receiver at both endpoints. Interpolate through the two tuples

$$
C=(r,r',U),\qquad D=(r',r,U),
$$

using the original slots of $r,q$ for the two displayed words. From before the edge, transport the first frame to $C$. If it contains $q$, replacing $q$ by $r q^\epsilon$ is an elementary basis operation within the selected frame, preserving its kernel. If $q$ is retained, its projection is unchanged because the frame kills $r$. From after the edge, transport the second frame to $D$. The replacement is now $q\mapsto r' q^{-\epsilon}$, also a basis operation when both rows are selected. If $q$ is retained, its image changes at most by inversion because the frame kills $r'$. Finally $C$ and $D$ differ by a swap, and their projected frames compare by the theorem. Concatenation yields the claimed path. This proof of the edge criterion uses the exact basis hypothesis at multiplication endpoints, where multiplication of independently conjugated representatives need not be an elementary basis transformation.

For relative-basis frames up to individual conjugation and inversion, the following broader collection of edge tests also suffices. When one frame omits the receiver, it transports unchanged to the other side. When both select the receiver and omit the donor, use $C,D$ as above. Neither transported frame has any of its words modified. When both select the receiver and the donor, quotient by the common slots first. Their two normal closures coincide because the replacement acts inside that common block. This gives a free group marked by $X$ and the remaining auxiliary basis of either frame. The residual tuples coincide, so apply the vertex theorem in that quotient. These arguments permit different compatible frame choices for different edges. The vertex theorem connects all such choices at intermediate vertices.

## Exact controls

With capitals for inverse letters, take $c=[z,x]$ and $S=t^2 c t^{-1}c^{-1}$. A strict multiplication yields

~~~text
(S,z,X,yzxz) -> (S,zX,X,yzxz).
~~~

The same two frame slots give marked free quotients. In the first, $z=1$ forces $S=t$ and hence $t=1$. In the second, $z=x$ again gives $t=1$. Their projections are $(X,yx)$ and $(X,yxxx)$, connected by four strict operations with the donor restored. The common quotient by $S$ alone is nonfree: it has $c t c^{-1}=t^2$ with $t\ne1$. A witness for the latter maps $z=(12)$, $x=(14)(25)$, $t=(123)$ and $y=1$ to $S_5$. In a free group a nontrivial word and its square have different cyclically reduced lengths, precluding their conjugacy. Neither endpoint admits a triangular frame, as the only row containing the auxiliary $t$ has three cyclic occurrences of it.

For the exact relative-basis path theorem use auxiliary words $U=\mathrm{zttzt}$ and $V=\mathrm{tztzttzt}$, obtained from $(z,t)$ by four alternating right Nielsen multiplications. In ambient rank five and base $X=(x,y,w)$, consider the one-step multiplication

~~~text
(z,t,ZVx,UVy,w) -> (Vx,t,ZVx,UVy,w).
~~~

On the left the sole exact frame is the first and second row. On the right it is the first and fourth: the marked complement of $X$ is $(Vx,UVy)$, obtained by a Nielsen basis change in the auxiliaries followed by right multiplications by $x,y$. All other two-row auxiliary exponent minors have absolute value different from one. Thus the edge cannot be projected by retaining a common unchanged slot. The right endpoint has no triangular frame either. Its marked quotient is obtained by solving $V=x^{-1}$, $U=y^{-1}x$, and reversing the four Nielsen operations. The resulting projections agree after an independently replayed ordinary rank-two path on the first two surviving relators, with $w$ frozen on both sides.

~~~sh
python3 -B experiments/round03_ac_proof_controls.py | diff - results/round03_ac_proof_controls.json
~~~

## Scope for the AK(3) search

The one-row test can use certified free quotients of selected blocks even when the common block cannot be eliminated on its own. The vertex theorem removes the frame-exchange ambiguity for relative bases, including the disjoint frames in [round 02](round-02-ac-proof.md#exact-examples-and-scope). To trivialize AK(3) with the path criterion one still needs a padded path to a basis and frame witnesses throughout; the marked-free edge criterion provides a second option. A geometric block can give an ordinary normalization inside the padded presentation, but choosing such blocks at every vertex alone does not establish either path hypothesis. [Geometric block normalization](round-02-stable-proof.md).
