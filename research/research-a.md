# Research A: an exact nonincreasing plateau for AK(n)

Date: 2026-11-02. Independent research agent A.

**Status:** a limited theorem about the initial search plateau, not a solution of the Andrews–Curtis conjecture or of AK(3). No novelty claim is made. The main conclusions below are proved directly; the accompanying finite enumeration is a check of the proof's equality cases.

## Previous work read, and choice of direction

The target repository was empty when this investigation began. I subsequently read its initial README and the primary papers of Panteleev–Ushakov, *Conjugacy search problem and the Andrews–Curtis conjecture*, [arXiv:1609.00325](https://arxiv.org/abs/1609.00325), especially the quotient-conjugacy ACM move, and Carreras, *Machine-checkable equivalence certificates at the length-14 Andrews–Curtis frontier*, [arXiv:2607.23611](https://arxiv.org/abs/2607.23611), especially its insistence on specifying the move graph and distinguishing equivalence certificates from trivializations. I independently chose a structural quotient approach: determine exactly what a search can do without first increasing length. These sources supply context; the proofs below do not assume their computational claims.

Write X=x^-1, Y=y^-1 and

    b = xyxYXY,
    p_n = x^n Y^(n+1),
    q_n = y^n X^(n+1),
    AK(n) = (p_n,b).

The initial total relator length is 2n+7; it is 13 for AK(3).

## Precise move graph and length convention

All displayed word lengths are lengths of freely and cyclically reduced representatives. A **quotient-conjugacy replacement** changes (u,v) to (u',v) when the image of u' is conjugate to the image of u or u^-1 in F(x,y)/<<v>>; the symmetric replacement and relator permutations are also allowed. This is the ACM-type move used here. The definition allows arbitrary words as conjugators and imposes no search bound.

Every ordinary elementary AC move is such a replacement: multiplying u by v leaves its quotient image unchanged, inversion inverts it, and conjugation conjugates it. Thus an obstruction to a nonincreasing path in this larger graph also obstructs a nonincreasing ordinary AC path. This does **not** obstruct paths that first increase length. We use only this containment and do not need to assume that a generalized move has a length-controlled elementary expansion.

For any word w, let Orb(w) denote its cyclic rotations and the cyclic rotations of w^-1. These operations are ordinary AC operations.

## A normal-form fact used in the proofs

In a free product C_a*C_c, a reduced syllable word alternates between the two cyclic factors. A cyclically reduced syllable word with at least two syllables starts and ends in different factors. Its syllable length is invariant under conjugacy, and a conjugate cyclically reduced word has the same syllable necklace, up to cyclic rotation. These claims follow directly by reducing a conjugate by one syllable and then inducting on the conjugator's syllable length. In particular, conjugating cannot lower cyclic syllable length. Inversion reverses the necklace and inverts each syllable.

## Lemma 1: no shortening while the braid relator is frozen

**Claim.** For n>=1, if u is conjugate to p_n or p_n^-1 in

    B = <x,y | xyx=yxy>,

then its cyclic free-word length is at least 2n+1. At equality,

    u belongs to Orb(p_n) union Orb(q_n).

Here the equality conclusion concerns the free word representing u, not just its quotient element.

**Proof.** Put s=xyx and t=xy in B. The braid relation gives s^2=t^3. In fact B has the presentation <s,t | s^2=t^3>: x=t^-1 s and y=s^-1 t^2 reconstruct the original generators and relation. Quotienting further by s^2=t^3=1 therefore gives C_2*C_3, with syllables S=s and T=t. The generator images are

    x -> T^2 S,   Y -> T S,
    X -> S T,     y -> S T^2.

Consequently

    p_n -> (T^2 S)^n (T S)^(n+1),

a cyclically reduced syllable word of length 4n+2. Each x/y letter contributes two syllables before reduction. A representative of free length L therefore has cyclic syllable length at most 2L. Conjugacy to p_n or its inverse requires cyclic syllable length 4n+2, so L>=2n+1.

For equality, all 2L syllables must survive both ordinary and cyclic reduction. Each letter block has orientation TS (x or Y) or ST (X or y). A change of orientation would put two syllables from the same factor together, strictly decreasing syllable length. Thus every block has the same orientation.

For the p_n necklace, the T-exponent necklace consists of n consecutive 2s followed by n+1 consecutive 1s. In orientation TS this uniquely decodes to a cyclic rotation of x^nY^(n+1); in orientation ST it uniquely decodes to a cyclic rotation of y^nX^(n+1). Applying the same reasoning to the inverse necklace supplies precisely their inverses. This proves the necessary equality classification. The second word is indeed conjugate to the first in B: conjugation by Delta=xyx exchanges x and y. QED.

This lemma alone proves that a whole phase of moves that preserves the braid relator up to conjugacy/inversion and only updates the other relator cannot shorten the power relator. It is independent of the stronger plateau theorem below.

## Lemma 2: no shortening of the braid relator while a power relator is frozen

**Claim.** For n>=3, if u is conjugate to b or b^-1 in

    G_n = <x,y | x^n=y^(n+1)>,

then |u|>=6. At equality u belongs to Orb(b). The same conclusion holds if the frozen relator is q_n.

**Proof.** There is a quotient G_n -> C_n*C_(n+1), obtained by imposing x^n=y^(n+1)=1. The image of b is the cyclically reduced six-syllable word

    x, y, x, y^-1, x^-1, y^-1.

Every free generator letter supplies at most one syllable, so a conjugate or inverse-conjugate representative has length at least six. If the length is exactly six, no syllable combination or cancellation is possible, and the syllable necklace must be a rotation of that of b or its inverse. Since n>=3, x and x^-1 are distinct syllables in C_n; y and y^-1 are also distinct in C_(n+1). Hence this necklace decodes to exactly a cyclic rotation of b or b^-1 as a free word.

When q_n is frozen, use the quotient C_(n+1)*C_n instead. Both factor orders are still at least three, so the same proof applies. QED.

The length lower bound also holds for n=2, but this equality classification does not: in the C_2 factor x=x^-1. The plateau theorem deliberately excludes n=2.

## Theorem: closure of the nonincreasing plateau

**Claim.** For n>=3, every quotient-conjugacy-replacement path starting at AK(n), along which total cyclic relator length never increases, remains, up to relator permutation, in

    (Orb(p_n) union Orb(q_n)) x Orb(b).

In particular, all its states have length exactly 2n+7. Every ordinary AC trivialization of AK(n), if one exists, must reach total cyclic relator length at least 2n+8. For AK(3) this gives the modest lower bound 14.

**Proof by induction on path length.** The initial pair is in the displayed family. Rotating or inverting the frozen relator does not change its normal closure, so both lemmas continue to apply to all its orbit representatives. Updating the power relator with the braid relator frozen cannot produce length less than 2n+1 by Lemma 1; nonincrease forces equality, and the equality classification keeps it in Orb(p_n) union Orb(q_n). Updating the braid relator with p_n or q_n frozen cannot produce length less than six by Lemma 2; nonincrease again forces equality, and keeps it in Orb(b). Permuting the two relators only exchanges the tracked roles. Thus the family is closed. It contains no standard pair (x,y), whose total length is two. A path to that pair must leave the nonincreasing plateau by an increase, necessarily to an integer at least 2n+8. QED.

This is a plateau statement, **not** a global AC invariant. After an increasing move the proof gives no restriction on subsequent moves. In particular it gives no evidence that AK(3) is not AC-trivial, and it does not explain the much larger barriers a particular search engine might encounter. Any stronger numerical lower bound would need a separate proof.

## Independent finite checks

Run the standard-library-only artifact:

    python3 experiments/verify_plateau.py

It constructs reduced normal forms in the relevant finite-cyclic free products and exhausts cyclically reduced x/y words up to the lengths in the equality statements. It checks both the original and swapped frozen power relators. Results from the run accompanying this note:

| Check | n | Words checked | Equality candidates |
| --- | ---: | ---: | ---: |
| power relator in braid quotient | 2 | 372 | 20 = 4(2n+1) |
| power relator in braid quotient | 3 | 3,292 | 28 = 4(2n+1) |
| power relator in braid quotient | 4 | 29,540 | 36 = 4(2n+1) |
| braid in power quotient, each ordering | 3 | 1,104 | 12 = Orb(b) |
| braid in power quotient, each ordering | 4 | 1,104 | 12 = Orb(b) |

For n=2 the latter quotient test gives 96 length-six candidates instead of 12. These are **necessary quotient-test candidates**, not 96 asserted conjugates in the torus-knot group; the example confirms why the proof must distinguish its equality exception. The script also checks the 4n+2 syllable formula for n=1,...,100. Finite checks support the implementation and equality reasoning; the uniform result rests on the proofs above.

## Research insight and next direction

This gives a reason an exclusively shortening or equal-length ACM search cannot even leave AK(3)'s initial plateau: the two one-relator quotients rigidly constrain its equality states. More computation inside that plateau cannot discover a decrease. A useful next investigation should deliberately introduce increasing replacements and classify their return paths. The proof supplies a small exact starting family for such an investigation and an independent check on any purported direct shortening certificate.

No requested breakthrough has been achieved in this note. The ordinary AC status of AK(3) and the full conjecture remain unresolved by this research.
