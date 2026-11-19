# Ordinary AC projection through chartless excursions

2026-11-19. A path can descend to ordinary AC even when a whole interval has no primitive relator. It suffices for a block containing the endpoint charts and one extra row to have the same normal closure at both ends, with compatible endpoint markings. Every donor from the block that updates an outside row must vanish in the quotient by that common normal closure. The block may receive outside donors during the interval.

## A path criterion with one retained donor

Let $G$ be the ambient free group of rank $n+k$. Fix $k+1$ row slots $B$ along a finite ordinary path in $G$, tracking their identities through any row permutations. At each endpoint choose $k$ rows in $B$ whose normal closure, $K_i$ for endpoint $i$, gives a free quotient of rank $n$. Call these the endpoint charts. Let $d_i$ be the remaining row of $B$ at endpoint $i$. Suppose the two endpoint full blocks have equal normal closures $K$, so that

$$
K=K_0\vee\langle\!\langle d_0\rangle\!\rangle
 =K_1\vee\langle\!\langle d_1\rangle\!\rangle .
$$

Write $Q=G/K$. Assume the markings of $Q$ from the two free charts are Nielsen equivalent. Equivalently there are $n$ ambient words that project to a basis in both charts. Use these bases to identify the charts with a single marked $F_n$. Assume also that whenever a block row donates to a row outside $B$, its value at that step lies in $K$.

**Claim.** The two endpoint tuples, projected through their respective charts and ordered with the remaining block row in the same slot, are ordinarily AC-equivalent in the common marking.

**Proof.** Project the outside rows throughout the interval to $Q$. Every product receiving from $B$ has no effect there. An outside-only product, inversion, or conjugation still projects to that ordinary instruction, with the conjugator evaluated in $Q$. Updates inside $B$ can be ignored in this projected ledger. Hence the outside starting and ending tuples are connected in $Q$ by a path that uses only their rows. Lift these moves to the outside rows of the starting chart in $F_n$, using arbitrary preimages for the conjugators. This gives the correct terminal outside tuple modulo $Q$ while keeping the retained donor fixed.

The two endpoint images of $d_i$ have equal normal closures in $F_n$ because the two marked maps $F_n\to Q$ agree on their basis. Magnus's normal-closure theorem identifies these images up to conjugacy and inversion. Align the donor to its terminal value. The differences in all outside rows now lie in its normal closure, so multiply in products of conjugates of the donor and its inverse, restoring the donor after each use. The donor can be trivial, in which case the outside rows already agree. The lifts and corrections use ordinary moves throughout. Replacing arbitrary conjugations by their one-letter expansions and compiling row swaps into Nielsen moves produces strict moves. [Common lifted bases](round-05-ac-proof.md), [Magnus's theorem](https://msp.org/gtm/2008/14/gtm-2008-14-004s.pdf).

A closed block, meaning that none of its slots receives a product from outside, satisfies both normal-closure tests automatically. Internal operations preserve the block normal closure and every intermediate block row lies in it. This still allows the chosen pivot to change slots and every intermediate pivot candidate to become nonprimitive. More generally, the direct test concerns the actual values of the outgoing donors, so the block normal closure may change temporarily. The earlier gap result kept the outside rows and designated donor fixed at both ends. [Round-three gap result](round-03-ac-proof.md).

When explicit endpoint chart maps are given, equality of the block normal closures and membership of the outgoing donors can be checked with one-relator word problems. For equality, translate each endpoint's full block into the other endpoint's free chart and test whether every image is trivial after imposing its single donor relation. This tests the two inclusions. Once the common closure is known, translate all outgoing donors into either chart and use the same test. If the charts have a fixed marked complement, that complement supplies the common basis without any separate Nielsen test. [Magnus's original one-relator algorithm](https://arxiv.org/abs/2501.18248).

The proof also works with $k+s$ block rows for arbitrary $s$ provided the two surviving donor lists are ordinarily AC-equivalent in the common $F_n$ using their own rows. Equality of their normal closures alone gives that equivalence by Magnus when $s=1$. For larger $s$, one sufficient condition is that both lists can be normalized with their own rows to partial free bases extending the same complementary tuple $X$ in $F_n$. In that case the automorphism fixing $X$ that exchanges the normalized donors preserves the projection killing them. Piggott's formal AC characterization then changes one donor list to the other. The compatibility of arbitrary surviving donor lists is a separate problem. [Piggott, Theorem 1](https://www.degruyterbrill.com/document/doi/10.1515/JGT.2007.029/html).

## A genuine intermediate import

Write uppercase letters for inverses. Start with the usual AK(3) tuple and the isolated auxiliary row, reordered as $(z,b,r)$ where $b=\mathrm{xyxYXY}$ and $r=\mathrm{xxxYYYY}$. Set $h=xz$, $v=hbh^{-1}$, $p=zv$, and use the first two row slots as $B$.

Conjugate $b$ to $v$ and multiply the first row by $v$. The resulting $p$ is nonprimitive, as are $v$ and $r$. Send $p$ to the outside row by the update $r\mapsto u=rp$. Import $u$ into the first row by $p\mapsto pu$, then send $v$ to the outside by $u\mapsto uv$. Undo the import using the changed outside row. The first row becomes

$$
pu(uv)^{-1}=p\,uv^{-1}u^{-1}.
$$

Multiply it by the temporary donor $uvu^{-1}$ to restore $p$. Conjugate the outside row by $y$. Finish by multiplying $p$ by $b$ and then by the inverse of $b^{-1}vb$, giving $zvb(b^{-1}v^{-1}b)=zb$. Restore the donor to $b$.

Both outgoing donors $p,v$ lie in $K=\langle\!\langle z,b\rangle\!\rangle$. The block temporarily generates a different normal closure: the marking to $S_3$ taking $x$ and $y$ to adjacent transpositions and $z$ to the identity kills $K$ but sends $pu$ to the marked $x$. In the same marking, the outside word begins at the transposition $x$ and ends at $yxy^{-1}$, so the outsider actually changes in the quotient. The charts at the two ends both retain the marked $x,y$ and solve $z=1$ and $z=b^{-1}$ respectively. Under the final chart $h$ becomes $xb^{-1}$, and the outside endpoint is

$$
y\,r\,b^{-1}\big((xb^{-1})b(xb^{-1})^{-1}\big)^2y^{-1}.
$$

The strict rank-three path has 65 moves, with cyclic peak 63 and raw peak 85. Its chartless interval runs from step 3 through step 57. The exact rank-two splice takes 34 moves with raw peak 31. Individual Whitehead minimization certifies every distinct chartless tuple of the control. [Exact replays](../results/round06_ac_proof_excursions.json).

## A primitive returns in a different slot of the AK(3) ledger

In the existing 253-move chartless witness, choose block slots $0,1$ with zero-based indices. The last primitive before the gap is in slot $0$ at step 248. Its signed cyclic word is **XYYZZZY**, making the complement of $x$ a free quotient marking. At step 253 the ordered signed cyclic tuple is

~~~text
XYZZZYYxy   XYxYXy   XXYYZZY
~~~

Use two additional cyclic products, with each rotation compiled into strict moves. Multiply the outside slot $2$ by the nonprimitive slot $0$ by choosing the rotated words **YYZZYXX** and **zzzyxYXyy**. Then multiply slot $1$ by slot $0$ with rotated words **XYxYXy** and **YxyXYZZZY**. The ordered result is

~~~text
XYZZZYYxy   XYYZZZY   XXzzzyxYXZZY
~~~

The same primitive cyclic class has returned in slot $1$. The block was closed throughout the entire gap. Its two charts solve the same equation for $x$ and use the same surviving $y,z$. The first outgoing donor is the nonprimitive former pivot. In the rank-two chart its image is a conjugate of the original rank-two donor from slot $1$. Temporarily put that donor in the indicated conjugacy representative, perform the outside update, restore it, and align it to the new retained slot $0$. The existing 251-move rank-two projection reaches the entry chart, since the intervening inversion of its pivot does not change the retraction. [Rank-three prefix](../certificates/round05_stable_proof_chartless22.json), [previous ordinary projection](round-05-ac-proof.md#compiling-the-rank-three-ak3-witness).

The extended rank-three replay has 281 strict moves, cyclic peak 28 and raw peak 31. All rows are nonprimitive from steps 249 through 277. The gap splice uses 27 ordinary moves, giving 278 ordinary moves from AK(3) to the exit projection and a raw peak of 43. Its endpoint is not a basis. This gap is distinct from the intrinsic primitive projection that first enters the ordinary cyclic component at cap 29. [Rank-three continuation and ordinary replay](../results/round06_ac_proof_excursions.json).

To reproduce both controls, run from the repository root.

~~~sh
python3 -B experiments/round06_ac_proof_excursions.py \
  | diff - results/round06_ac_proof_excursions.json
~~~

The criterion leaves open gaps whose endpoint markings fail the common-lift test or whose outgoing donors contribute genuinely new changes to the outside rows in $Q$. The earlier forced-donor example shows that the marking test can fail even for a single product. [Incompatible chart control](round-05-ac-proof.md#two-forced-chart-changes).
