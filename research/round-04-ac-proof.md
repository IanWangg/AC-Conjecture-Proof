# Round 04 · Ordinary AC projection across donor mismatches

2026-11-19. The mismatch left in round three can always be compiled with at most two auxiliary pairs if the endpoints have conjugacy-relative frames. The local compilation covers marked-free frames with sufficient overlap, even if one endpoint has no conjugacy-relative frame. At larger padding, a normalization test applies after killing the common rows. A forced three-auxiliary example shows why simply carrying forward the old relative frame can fail. Its projected tuples still have an ordinary AC path.

## Interpolation and overlap

Write $G=F(X\cup Z)$ and $F=F(X)$ with $|X|\ge 2$ and $k=|Z|$. A marked-free frame is a choice of $k$ relator slots whose normal closure gives the marked quotient $F$, with the quotient map fixing $X$. A conjugacy-relative frame has representatives that can be individually conjugated or inverted to extend $X$ to a free basis. The latter is a marked-free frame. Round three proves that any two conjugacy-relative frames at one vertex give AC-equivalent projections. It also proves the one-row exchange for marked-free frames without any hypothesis on the quotient by the common rows. [Round 03 projection and exchange](round-03-ac-proof.md).

Suppose the edge replaces $r$ by $r'=r q^\epsilon$ with $\epsilon=\pm1$. Choose marked-free frames $P,Q$ before and after. Both select the changed receiver, and $P$ selects the unchanged donor $q$ while $Q$ omits it. The opposite mismatch follows by reversing the edge and changing the sign. Let $S$ be the common unchanged slots of $P,Q$ apart from the receiver and donor. Work with the intermediate tuples

$$
C=(r,r',U),\qquad D=(r',r,U),
$$

in the original receiver and donor slots. In $C$ use the old frame with $q$ replaced by $r'$. Both $r,r'$ are selected, so its normal closure and the projection on the surviving slots are exactly those of $P$. In $D$ use the new frame $Q$ without changing any selected word. Its projection changes only in the retained donor slot, from $\rho_Q(q)$ to $\rho_Q(r)=\rho_Q(q)^{-\epsilon}$. This is at most an inversion. Swap the two displayed slots to compare $C$ and $D$. The transported frames share the word $r'$ in the same slot and all of $S$, and remain marked-free.

Consequently the edge descends whenever $|S|\ge k-2$, by the one-row exchange. At $k=2$ this covers every mismatch, even for a chosen pair of merely marked-free frames. It yields a whole-path theorem when every vertex admits a **conjugacy-relative** frame and $k\le2$. For donor agreement, or when a frame omits the receiver, use the other edge rules from round three. The round-three same-vertex theorem connects the edge choices, including for inversions, conjugations and swaps. A path of arbitrarily selected marked-free frames may still need additional compatibility at an intermediate vertex. [Round 03 edge rules and same-vertex theorem](round-03-ac-proof.md).

## Two sufficient tests for larger padding

**Relative conjugator test.** Normalize the old frame to a relative basis with $r,q^\epsilon$ conjugate to distinct basis letters $z_1,z_2$. Write these conjugations by $a,b$ respectively, so $r'$ is conjugate to $W=z_1wz_2w^{-1}$ for $w=a^{-1}b$. A word in the double coset $\langle z_1\rangle w\langle z_2\rangle$ can replace $w$, since this changes only the conjugacy representative of $W$. If the chosen word avoids $z_2^{\pm1}$, replacing $z_2$ by $W$ while fixing all other basis words is an automorphism. Thus the old frame transported to $C$ is already conjugacy-relative, and the general same-vertex theorem compares the frames in $C$. If the word avoids $z_1^{\pm1}$, replacing $z_1$ by $W$ similarly gives a conjugacy-relative old frame directly at the endpoint with $q$ unchanged. Its marked quotient is unchanged, since it kills both $q$ and $r'$. The same-vertex theorem applies again. No restriction on the overlap is needed for this test.

**Residual normalization test.** In the mismatch interpolation, suppose $Q$ is conjugacy-relative, and kill the common slots $S$ and $r'$ in $C$. The current ambient group $H$ is free on $X$ and $m=k-|S|-1$ more letters. Indeed the killed rows are a subset of a conjugacy-relative frame and their normal closure can be read in its normalized basis. The remaining selections $P_0,Q_0$ are disjoint in $H$. The second is conjugacy-relative and the first is marked-free. If $P_0$ can be normalized to a basis extending $X$ by AC moves using its own rows in $H$, perform that normalization while keeping $Q_0$ and all other rows fixed. The projection through $P_0$ stays the same. The projection through $Q_0$ sees ordinary moves from the normalization, since all the modified rows are retained and the conjugating words project into $F$. The round-three same-vertex theorem then compares the two projections of the normalized tuple. The argument also works when both residual blocks need such a normalization. It does not require that the original transported frame be conjugacy-relative.

One explicit case of this test is when $m-1$ rows in $P_0$ already extend $X$ partway to a basis after individual inversions and conjugations. Normalize those rows and kill them. The resulting group is $F*\langle v\rangle$. The sole remaining frame row normally generates the kernel of the retraction to $F$, which is the normal closure of $v\rho_{P_0}(v)^{-1}$. Magnus's theorem identifies that row up to inversion and conjugation in the quotient. Lift those moves and correct the row to $v\rho_{P_0}(v)^{-1}$ using products of conjugates of the other frame rows. This gives the required basis, using only $P_0$. In particular, a single relative primitive suffices when the residual old frame has two rows. [Magnus normal-closure theorem](https://msp.org/gtm/2008/14/gtm-2008-14-004s.pdf), [round 01 donor correction](round-01-ac-proof.md).

## Exact controls

Use uppercase letters for inverses. For two auxiliaries, let $r=\mathrm{zztZTzzt}$, $q=r^{-1}z$, and apply the edge

~~~text
(r,q,tX,ytt) -> (z,q,tX,ytt).
~~~

The selected frames use slots $\{0,1\}$ and $\{0,2\}$. The first implies $z=rq=1$ and $t=1$ because $r$ evaluates to $t$ at $z=1$. The second implies $z=1$ and $t=x$. The projections $(X,y)$ and $(X,yxx)$ are joined by four strict operations. On the left the auxiliary determinant leaves only the stated choice, and $r$ is nonprimitive in $F(z,t)$. It has exponent vector $(3,1)$ and cyclic length eight, while the unique primitive conjugacy class of that vector has cyclic length four. Hence it cannot be part of a conjugacy-relative frame extending $X=(x,y)$. There are no shared unchanged slots for the chosen edge. [Osborne and Zieschang, §3.2](https://geodesic.mathdoc.fr/item/IM_1981__63_142788/).

For three auxiliaries take $w=tuz$, $r=z$, $q=w t w^{-1}$ and $R=rq$. The tuple $(R,z,w)$ is a free basis of $F(z,t,u)$, using the consecutive replacements $u\mapsto w$ and $t\mapsto R$. Set $A=z^{-1}$, $B=w^{-1}$, $B_1=BA$, $\beta=AB_1^2$, $\gamma=B_1\beta$, $b=R^2\beta x$ and $c=R^5\gamma y$. Use the edge

~~~text
(z,q,u,b,c) -> (R,q,u,b,c).
~~~

The left frame is $(z,q,u)$ up to conjugacy. The right frame $(R,b,c)$ is a relative basis by the specified Nielsen operations with $R$ and $X$ fixed. The auxiliary determinant permits only the left choice on the left, and only $(R,q,u)$ or the stated right choice on the right. The two natural transports of the old frame, $(R,q,u)$ on the right and $(z,R,u)$ through the interpolation, both fail to be conjugacy-relative. After adjoining the singleton classes $x,y$, their proved global Whitehead minima are ten, while a five-generator basis has cyclic total length five. Each certificate gives the length-decreasing automorphisms and all signed-generator separating cut minima at the final tuple. This is a failure of relative-frame transport under a genuine donor mismatch. [Whitehead minimization for tuples](https://ems.press/content/serial-article-files/42594?nt=1).

Here the two transported frames share only $R$. Killing it leaves the basis $(x,y,z,w)$ and the residual old frame $(z,w^{-1}z w^2z^{-1})$. Its second row is nonprimitive after killing $x,y$, by the exponent vector $(0,1)$ and cyclic length five. Its first row is a marked basis generator, so the residual normalization test applies. In the final marked quotient by $(R,b,c)$, put $B_1=y^{-1}x$, $A=x^{-1}B_1^{-2}$ and $B=B_1A^{-1}$. The projected rows are $A,B A^{-1}B^{-2}A$. The other projection is $(x,y)$. The saved replay uses 39 strict operations, starting by clearing the two occurrences of the donor $A$ from the second row, and then performing the specified Nielsen operations.

~~~sh
python3 -B experiments/round04_ac_proof_controls.py | diff - results/round04_ac_proof_controls.json
~~~

The result yields descent for paths with at most two padded pairs under the stated path hypothesis. At higher padding the unresolved part is compatibility when the shared quotient retains at least two auxiliaries and the old residual block lacks a certified relative normalization. The three-auxiliary control motivates testing residual normalization as well as immediate frame transport.
