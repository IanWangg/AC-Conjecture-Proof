# Research M: primitive-free initial subgroups and a direct free-group search

Date: 2026-11-02. Status: an unbounded theorem about a restricted initial
regime, plus a heuristic ordinary-AC search with an exact positive control.
**No AK(3) trivialization or global AC obstruction is established.** No
novelty claim is made.

## Previous work read and independent direction

I read the actual A–J reports, G's product synchronization follow-up, and
I's first-order correction addendum before choosing this direction. The
reports distinguish success in a quotient from an exact free-group
endpoint and establish substantial finite and initial-quotient
obstructions. I also read the primary graph definitions and folding
argument in [Kapovich–Myasnikov, *Stallings Foldings and Subgroups of Free
Groups*](https://web.stevens.edu/algebraic/alexeim/Teaching/GroupTheory626/graph5.pdf).

I independently chose a direct free-group approach: use the folded based
subgroup graph as a search state and geometric score. Nielsen operations
preserve the generated subgroup, whereas individual ambient conjugations
can change it. Thus a search can deliberately try long Nielsen-basis
variants and graph-changing conjugations while retaining an exact ledger
of ordinary AC moves. This avoids relying on a quotient endpoint as a
substitute for the actual target.

This investigation also yielded an unbounded subgroup obstruction that
explains why arbitrary initial Nielsen preludes cannot produce a primitive
waypoint. It differs from J's one-coordinate quotient-conjugacy theorem:
the subgroup statement permits both coordinates to undergo arbitrary
Nielsen operations, but does not permit arbitrary external conjugations.

## Uniform theorem

Write X=x^-1, Y=y^-1 and let

    p_n=x^n Y^(n+1),   b=xyxYXY,
    H_n=<p_n,b> <= F(x,y).

**Theorem.** For every n>=2, H_n contains **no primitive element of F(x,y)**.
Here primitive means a member of some free basis of the ambient rank-two
free group. The assertion concerns all elements of H_n at all word
lengths, not just the displayed generators or a finite collection of bases.

Consequences:

1. No arbitrary sequence of Nielsen operations on the initial tuple can
   reach a primitive-relator waypoint. They preserve H_n.
2. More generally, if all ambient conjugators remain in the fixed H_n,
   the relators stay inside H_n and cannot become primitive. Simultaneous
   conjugation of the whole subgroup also preserves its primitive-free
   property.
3. Any ordinary trivialization requires at least **two single-coordinate
   ambient conjugation operations**, even when conjugation by an arbitrary
   word is counted as one operation and Nielsen operations are unrestricted.

For the last claim, suppose there is only one such conjugation. Before it,
the tuple is a Nielsen basis of H_n, so both entries are nonprimitive in
F. The unchanged entry remains nonprimitive after the conjugation. If the
following Nielsen operations reached the free basis, the pair immediately
after the conjugation would itself generate F as a subgroup and hence be
a free basis of F, contradicting that unchanged nonprimitive entry.

The theorem is not invariant under general AC moves. Indeed it holds also
for AK(2), which is AC-trivial. The explicit AK(2) certificate below shows
that the primitive-free property can be left by permitted individual
conjugations and subsequent Nielsen operations.

## A primitive rank-two conjugacy fact

Nielsen's theorem says that two primitive elements of F2 with the same
abelianization vector are conjugate. A modern primary proof is
[Clay–Conant–Ramasubramanian, *Whitehead graphs and separability in rank
two*, Corollary 4.4](https://msp.org/involve/2014/7-4/involve-v7-n4-p01-p.pdf).

It follows that every cyclically reduced primitive word uses at most one
sign of x and at most one sign of y. Here is a construction supplying the
needed positive representative. For nonnegative coprime a,b, construct a
positive primitive word with exponent vector (a,b) by Euclidean induction.
Use x or y when one coordinate is zero, and xy at (1,1). If a>b>0,
construct the word at (a-b,b) and substitute y->xy, x->x. If b>a>0,
construct the word at (a,b-a) and substitute x->xy, y->y. Both substitutions
are free-group automorphisms and preserve positivity. Inverting either
ambient generator supplies the representative for any signs of a,b.

Nielsen uniqueness now makes any primitive word with that vector conjugate
to this representative. Cyclically reduced conjugate free words differ by
a cyclic rotation. Therefore its cyclic word belongs to one of the four
signed alphabets

    {x,y},  {x,Y},  {X,y},  {X,Y}.

This argument is special to ambient rank two.

## The exact folded graph of H_n

Start with a directed cycle on vertices v_0,...,v_(2n), labeled

    x^n Y^(n+1).

Attach a four-edge path from v_1 to v_(2n), with three new internal
vertices A,B,C:

    v_1 --y--> A --x--> B --Y--> C --X--> v_(2n).

Include the inverse labeled edge for every edge. The basepoint is v_0.
This graph has 2n+4 vertices and 2n+5 unoriented edges, hence rank two.

The power relator reads the original cycle. The braid relator reads the
first x edge to v_1, the four-edge attached path, and the last Y edge back
to v_0. Conversely, this is exactly the folding of the two based word
loops: their initial x edges are identified and their final Y edges are
identified, with no further folds. For n>=2 every vertex has at most one
outgoing edge of each signed label, as is checked directly from the
displayed construction. Thus it is the folded based graph representing
the precise subgroup H_n, not merely a graph accepting its generators.

The primary folding theorem implies that a freely reduced word belongs to
H_n exactly when it reads a based loop in this graph.

## Signed cycles prove the theorem

Restrict the directed graph to labels x and y. The cycle's x edges form
the path from v_0 to v_n; the inverse Y edges form the y-labeled path
from v_0 through v_(2n) to v_n. The additional allowed edges are

    v_1 --y--> A --x--> B,
    v_(2n) --x--> C --y--> B.

This directed graph is acyclic: the two original paths terminate at v_n,
and the additional branches terminate at B. The inverse-label graph on X,Y
is also acyclic.

In the graph restricted to x,Y, the original power cycle remains. Outside
it the allowed edges are

    A --Y--> v_1,   A --x--> B --Y--> C,
    v_(2n) --x--> C.

A has no allowed incoming edge and C has no allowed outgoing edge. Hence
the unique cyclic strongly connected component is the original power
cycle. Every nonempty closed path in that restricted graph is a power of
a cyclic rotation of p_n. In the inverse-label graph X,y the corresponding
closed paths are powers of cyclic rotations of p_n^-1.

Suppose a primitive h belongs to H_n. After cyclically reducing it, write
h=q v q^-1 with v cyclically reduced. The based loop for h consists of a
path q, a closed path for v at the endpoint of q, and the reverse path q^-1.
The middle path is closed because the graph is folded and inverse paths
are unique. By the preceding primitive conjugacy fact, v uses one of the
four signed alphabets. The cycle classification forces v to be a cyclic
rotation of p_n^k or p_n^-k for some k>=1.

When k>=2 its exponent vector is divisible by k, so it is not primitive.
At k=1, p_n is also nonprimitive for n>=2. To see this without a search,
the word

    w_n=(xY)^n Y

is primitive: (xY,Y) is a free basis and replacing its second member by
(xY)^nY again gives a basis. It has the same exponent vector as p_n. If
p_n were primitive, Nielsen uniqueness would make it conjugate to w_n.
Both are cyclically reduced, but p_n has consecutive x letters while
w_n has none, including across its cyclic boundary. They cannot be cyclic
rotations. This contradiction proves the theorem for all n>=2.

The n=1 exception is real: p_1=xYY is itself primitive. It is included as
a positive control in the checker.

## Direct ordinary-AC search

`stallings_search.py` retains actual free-word tuples and exact strict move
ledgers. A candidate consists of a random short sequence of left/right
signed coordinate Nielsen moves, one individual generator conjugation,
and a greedy Nielsen length reduction. Every signed multiplication and
left multiplication is expanded into positive right multiplication and
inversions. Graphs are canonicalized by a deterministic basepoint-first
labelled traversal and used to avoid revisiting the same subgroup.

This graph identification is a heuristic pruning choice: retaining one
tuple basis per subgroup can omit useful future basis choices. The random
Nielsen preludes partly compensate but do not supply completeness. The
search tests every retained candidate for a primitive coordinate, including
candidates whose subgroup was already visited.

A deliberately nonmonotone AK(3) run used seed 314159, 100,000 attempted
macro moves, random Nielsen preludes of length at most 12, retained macro
boundary length at most 200, acceptance base 0.9, and uniform-restart
probability 0.5. It visited **47,671 distinct based subgroups**, discarded
50,496 over-length proposals, and found no primitive waypoint. The minimum
folded graph size stayed at the initial ten vertices; the minimum retained
total word length stayed thirteen. These are observations of this
specified heuristic, not exclusions of all paths under any peak bound.

## Exact positive control and primitive-waypoint compiler

With n=2, seed 137, and the stated smaller prelude, the same method reaches

    (YYxxY, xYYxYxY)

after **139 strict elementary moves**, with peak raw total length 29. Its
second coordinate is primitive in F2. This occurred at attempt 5,509,
after 4,516 distinct based subgroups had been visited.

`complete_primitive.py` supplies an actual ordinary-AC completion from
such a waypoint. It finds a Whitehead automorphism taking the primitive
coordinate to its corresponding generator, derives donor-letter
elimination in those coordinates, then transports each move back through
the inverse automorphism. Finally it explicitly realizes the remaining
free-basis change by legal relator operations. No ambient automorphism is
silently inserted as an elementary AC move.

The resulting AK(2) certificate has **246 strict elementary moves**, exact
free endpoint `(x,y)`, and peak raw total length **31**. It passes the
coordinating agent's independently written strict `elementary_verify.py`.
It is a calibration of the search and compiler, not a new solution of one
of the user's four requested breakthrough objectives, since AK(2) was
already known AC-trivial.

## Reproduce

All scripts use only the Python standard library and reside together in
`experiments/`:

```sh
python3 experiments/signed_cycle_obstruction.py \
  --output results/signed_cycle_results.json
python3 experiments/signed_cycle_obstruction.py \
  --verify results/signed_cycle_results.json

python3 experiments/stallings_search.py --n 2 --iterations 10000 \
  --seed 137 --max-prelude 7 \
  --output results/m_ak2_search.json \
  --certificate certificates/m_ak2_waypoint.json
python3 experiments/complete_primitive.py certificates/m_ak2_waypoint.json \
  --output certificates/m_ak2_full.json
python3 experiments/elementary_verify.py certificates/m_ak2_full.json

python3 experiments/stallings_search.py --iterations 100000 --seed 314159 \
  --max-length 200 --max-prelude 12 --temperature 0.9 --restart-mix 0.5
```

The signed-cycle checker compares the explicit graph with an independently
folded pair of word loops, checks its signed components and inverse-basis
formulas, and tests n=1,...,50. It also checks the positive Euclidean
primitive construction for coprime coordinates between zero and fifteen.
The saved n=3 certificate records all graph arcs and its signed cyclic
components. The uniform theorem rests on the proof above, not extrapolation
from those finite checks.

The next genuinely useful search must leave the primitive-free initial
subgroup by individual external conjugations and find a primitive
waypoint, or produce a different complete route. Neither the graph theorem
nor the finite heuristic run establishes AK(3)'s AC status or the full
conjecture.
