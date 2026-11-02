# Research J: neither initial AK(n) deletion quotient admits a primitive replacement

Date: 2026-11-02. Status: an unbounded one-step obstruction, **not a global
AC invariant and not a solution of AK(3)**. No novelty claim is made.

## Previous work read and independent choice

I read the previous A–F reports, G's complementary torus-quotient report,
H's uniform torus-family proof, and the available I relation-module audit
before choosing this direction. A/F constrain the initial cyclic plateau;
E/G/H construct short paths in the two deletion quotients while exposing
their free lifting errors. These quotient paths change both coordinates.
They do not say that the original remaining relator can be replaced by a
primitive free word while the other coordinate stays fixed.

After reviewing the ordinary and quotient-conjugacy move definitions in
[Panteleev–Ushakov, Section 1.2](https://arxiv.org/html/1609.00325v1), I
independently chose to test exactly that possible shortcut. The result
rules it out at every word length, rather than just below a finite cap.

The only external primitive-word fact used below is Nielsen's rank-two
uniqueness theorem: primitive elements with the same exponent-sum vector
are conjugate. A modern primary proof is
[Clay–Conant–Ramasubramanian, *Whitehead graphs and separability in rank
two*, Corollary 4.4, p. 446](https://msp.org/involve/2014/7-4/involve-v7-n4-p01-p.pdf).
The explicit representatives and quotient comparisons below are derived
here. No broad classification of Christoffel block patterns is needed.

## Statement

Write F=F(x,y), X=x^-1, Y=y^-1, and

    p_n=x^n Y^(n+1),  b=xyxYXY,
    B=<x,y | b=1>,
    T_n=<x,y | x^n=y^(n+1)>.

A primitive element of F means a member of a free basis of F. A
quotient-conjugacy replacement of one coordinate is allowed to replace it
by any word whose image is conjugate to its image or inverse in the
quotient obtained by killing the other coordinate.

**Theorem.**

1. For every n>=2, no primitive element of F has image conjugate to p_n or
   p_n^-1 in B.
2. For every n>=3, no primitive element of F has image conjugate to b or
   b^-1 in T_n.

Consequently, starting at AK(n)=(p_n,b) for any n>=3, **neither single
quotient-conjugacy replacement can create a primitive relator**, even if
the replacement word may be arbitrarily long. The same conclusion holds
through a phase that keeps one original coordinate fixed up to free
conjugacy and inversion while changing only the other.

This result is compatible with the short E/G quotient paths: those paths
change both coordinates and use a quotient identity which is unavailable
as a free-group deletion. It does not constrain the general search after
both coordinates have changed.

## 1. Primitive words with total exponent sum one

The homomorphism e:B->Z defined by e(x)=e(y)=1 is well-defined. It sends
p_n to -1. Thus a primitive word representing a conjugate of p_n or p_n^-1 has
total exponent sum ±1. Invert it if necessary to reduce to sum one.

Its free abelianization is therefore (k+1,-k) for some integer k. Put

    c=xY,   v_k=c^k x.

The pair (c,x) is a free basis: x is the second basis element and
y=c^-1 x. Replacing its second coordinate by c^k x again gives a basis.
Thus v_k is primitive, with exponent vector (k+1,-k). Nielsen uniqueness
implies that **every** primitive word of total exponent sum one is freely
conjugate to exactly the representative v_k with its exponent vector.

Represent B in SL(2,Z) by

    U=x -> [[1,1],[0,1]],
    V=y -> [[1,0],[-1,1]].

The matrices satisfy UVU=VUV. Let M=UV^-1=[[2,1],[1,1]]. For k>=0 set

    s_k = trace(M^k U).

The characteristic equation M^2-3M+I=0 gives

    s_0=2,  s_1=4,  s_(k+2)=3s_(k+1)-s_k.

In particular the sequence begins

    2, 4, 10, 26, 68, 178, 466, 1220, ...

and is strictly increasing. For k=-l<0, free cancellation gives

    v_(-l)=(yX)^(l-1)y.

This is obtained from v_(l-1) by exchanging x and y. In B this exchange is
conjugation by Delta=xyx, so its matrix trace is s_(l-1). Inversion also
preserves the trace of a determinant-one 2-by-2 matrix. Thus the above
sequence contains the trace of every possible primitive word with total
exponent sum ±1.

For AK(3), direct matrix multiplication already gives

    p_3 -> [[13,3],[4,1]],  trace(p_3)=14.

Since 10<14<26, this trace does not occur. Matrix conjugacy would preserve
trace, proving the requested n=3 case for all word lengths.

To prove the uniform statement, combine the trace with the quotient
C_2*C_3 used in A. Write S=xyx and T=xy modulo the central element, so

    x -> T^2 S,  Y -> T S.

The image of v_k for k>=0 is cyclically syllable-reduced, with syllable
length 4k+2. For k=-l<0, exchanging x and y conjugates v_k to v_(l-1),
so its cyclic syllable length is 4(l-1)+2. Put m=k if k>=0 and m=-k-1
otherwise. In either case the primitive representative has cyclic
syllable length 4m+2 and trace s_m.

On the other hand, the image of p_n is the cyclically reduced word

    (T^2 S)^n (T S)^(n+1),

of syllable length 4n+2. Conjugacy to p_n or its inverse would therefore
force m=n. The power word's trace is n(n+1)+2. For n>=2,

    s_n > n(n+1)+2.

Indeed s_2=10>8, and the positive increasing sequence satisfies
s_(n+1)=3s_n-s_(n-1)>2s_n. If the inequality holds at n>=2, then

    s_(n+1) > 2[n(n+1)+2] > (n+1)(n+2)+2,

where the last difference is n(n-1)>0. Thus induction proves the
inequality. Trace now contradicts the necessary equality at m=n,
proving part 1 uniformly for every n>=2.

The two invariants are both useful. Trace alone would not establish the
uniform claim: trace(x^56 Y^57)=3194=s_8, but their cyclic syllable lengths
are 226 and 34. This control is included in the program. At n=1 the
conclusion correctly fails, since p_1=xY^2 is itself primitive.

## 2. Primitive words of torus abelianization one

In T_n the homomorphism

    h_n(x)=n+1,  h_n(y)=n

sends b to one. If a primitive u has image conjugate to b^-1, replace u
by u^-1. We may therefore suppose that its image is conjugate to b and
that h_n(u)=1. Its exponent vector must be

    (a,beta)=(1+nk,-1-(n+1)k),  k in Z.

Define

    m=xY,  w=m^n Y,  u_k=w^k m.

The pair (m,Y) is a free basis because x=m Y^-1 and y=Y^-1. Replacing its
second element by m^n Y gives the basis (m,w), and replacing m by w^k m
gives the basis (u_k,w). Thus u_k is primitive and has precisely the
required exponent vector. Nielsen uniqueness again says that every
primitive u with h_n(u)=1 is conjugate in F to the corresponding u_k.

Now pass to the further quotient C_n*C_(n+1). The image of b is a
cyclically reduced six-syllable word, with x-factor syllables

    x, x, X

and y-factor syllables y,Y,Y.

For k>=0 the word u_k is

    ((xY)^n Y)^k xY.

Each x is isolated, and every Y-run has length one or two. For n>=3
these are nonidentity residues in their factors. The word is cyclically
syllable-reduced and its syllable length is exactly

    2(nk+1).

This equals two at k=0 and is at least eight at k>=1, so it never equals
six.

For k=-l<0, a final free cancellation gives the explicit word

    u_(-l) = [y(yX)^n]^(l-1) y(yX)^(n-1).

Every X is isolated, and every y-run again has length one or two. The
cyclic syllable length in C_n*C_(n+1) is therefore

    2(nl-1).

It can equal six only if nl=4. With n>=3 this leaves n=4,l=1. In that
single case the candidate's three x-factor syllables are all X, whereas
b has x-factor syllables x,x,X. Since x and X are distinct in C_4, no
cyclic rotation can identify the two syllable necklaces. They are not
conjugate in the free product.

Conjugate cyclically reduced words of syllable length at least two in a
free product have the same syllable necklace up to rotation. Hence every
candidate is excluded in C_n*C_(n+1), and therefore also in T_n. This
proves part 2 uniformly for n>=3.

## 3. Exact AK(2) exception control

The exclusion deliberately starts at n=3. At n=2 the isolated x-factor
residues do not distinguish x from X. Take k=-2. The same primitive
construction gives

    u=yyXyXyyX,  w=xYxYY.

The pair (u,w) is a free basis by the construction above. In T_2 it
satisfies the exact identity

    u=Y b y.

The checker verifies this equality in the full central-extension normal
form of T_2, retaining z=x^2=y^3 rather than killing it. It also verifies
explicit inverse substitutions for the basis (u,w). Thus there really is
a primitive replacement of the braid relator in the AK(2) deletion
quotient. This is a useful positive control for the n>=3 distinction.

It is not used as a claim that a quotient identity alone is an ordinary
AC move. A filling or elementary expansion would still be needed to
produce a new ordinary-move certificate by that route; AK(2) already has
independent ordinary certificates elsewhere in this repository.

## Reproduction and validation limits

Run:

```sh
python3 experiments/primitive_deletion_obstruction.py \
  --output results/primitive_deletion_results.json
```

The program uses only the Python standard library. Its checks include:

- exact integral matrix relation UVU=VUV, the trace recurrence and cyclic
  syllable formulas for k=-20,...,20, the all-n trace inequality formula
  on n=2,...,20, and the separating AK(3) trace;
- explicit inverse free-basis substitutions for u_k,w, not merely a
  determinant test;
- the two cyclic syllable formulas for n=3,...,15 and k=-12,...,12,
  including the exceptional n=4,k=-1 necklace;
- the exact central-extension AK(2) conjugacy control;
- the n=56 trace-compatibility example, rejected by its different cyclic
  syllable length, and the n=1 primitive power exception.

All checks pass. The finite checks validate formulas and implementation;
the unbounded conclusions follow from Nielsen's theorem and the proofs
above. The trace arithmetic was corrected during coordinating review
before the report's final proof and data were recorded.

## Implication for the requested goal

A primitive relator would be a valuable waypoint: keeping it as a donor,
one can remove its occurrences from the other coordinate; normal
generation then leaves a free basis. This report shows that neither
initial one-relator quotient offers that shortcut for AK(n), n>=3, regardless
of replacement length. Both coordinate roles must leave the initial
fixed-relator regime before a primitive waypoint can occur.

The proof is specific to the initial deletion quotients. It is not
preserved by arbitrary AC moves changing both coordinates, and so cannot
prove non-AC-triviality. It gives no sequence to the standard basis.
None of the user's four requested breakthrough objectives is achieved
by this report.
