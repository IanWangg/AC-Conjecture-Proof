# M follow-up: strict paths through the first hump, and whole-subgroup exclusions

Date: 2026-11-02. Status: new exact ordinary-AC waypoint certificates and
computer-assisted primitive-free subgroup statements for an explicit
finite catalogue. **No AK(3) trivialization or global AC obstruction is
established.** No novelty claim is made.

## Previous work, attribution, and task

After my initial subgroup result and L's independent diagnostic review,
the coordinating agent supplied two concrete quotient-conjugacy identities
in its newly derived free-by-cyclic deletion quotient. I independently
checked those identities and constructed actual free-group AC paths,
retaining the other relator as an available donor throughout each
transition. I then reduced their strict raw peaks by compiling local word
rewrites through short cyclic rotations.

The coordinating agent also enumerated the first short-departure word
catalogue and detected two branching signed subgraphs that were not
covered by a simple-cycle test. I proved the needed forced-double-letter
criterion for those graphs and expanded the check to all cyclic rotations
and inverses of the frozen literal relator. The candidate identities and
upstream quotient catalogue are credited to the coordinating agent; the
strict expansions and signed-line-graph certificate are M's follow-up.

## Exact reachable waypoints

Write

    p=xxxYYYY,  b=xyxYXY,  b'=XXyxYxxY,
    u1=yXYXyxx,  u2=YxYXyyx.

The following **strict elementary** certificates start at the actual
AK(3) tuple `(p,b)`:

| Endpoint | Strict moves | Exact raw peak |
|---|---:|---:|
| `(p,b')` | 44 | 18 |
| `(u1,b')` | 222 | 31 |
| `(u2,b')` | 179 | 25 |

Each primitive is relator inversion, positive right multiplication, or
conjugation by one of x,X,y,Y. Both input generators remain fixed. No
quotient equality, generator change, stabilization, or unexpanded
conjugation is treated as a move. The repository's independent strict
verifier passes all three saved ledgers against their exact free targets.

The coordinating agent's original entry certificate had 56 moves and
peak 42; the new 44-move version is an alternative exact implementation
with a smaller peak. No optimality claim is made.

### Discovery identities

In `Q=<x,y | b'=1>`, the coordinating agent uses stable generator x and
free fiber generators

    a=XXyx,  d=Xy,
    alpha(a)=d,  alpha(d)=aD.

Its exact normal forms give `p^-1=(a d^2 A d A)x`. The two fiber
conjugators are `aD^2` and `D^2`, represented in the original alphabet by

    q1=XXyxYxYx,  q2=YxYx.

Independent evaluation in that model confirms

    q1 p^-1 q1^-1 = u1 in Q,
    q2 p^-1 q2^-1 = u2 in Q.

These equalities guided the filling search. The final strict certificates
do not rely on silently applying them: their free differences are
explicitly filled by conjugates of b'. The saved waypoint verifier
reconstructs those factor products as exact free words without importing
the quotient evaluator.

### Local-rewrite compilation

The entry certificate uses these four exact one-relator rewrites of b,
with the power word p retained as donor:

    xyxYXY
    XXyyyyyxYXY
    XXyxxxxYXY
    XXyxyyyXY
    XXyxYxxY.

Each step replaces a substring A by B^-1 where AB is a cyclic rotation of
p or p^-1. The longest receiver has length eleven. The strict raw peak
of the expanded pair is eighteen.

After inversion and conjugation of p by q_i, the two transitions to u_i
have fillings with seven and six b'-cells, respectively. Their exact
cell data are recorded in the certificates. The finite rewrite searches
only discover these paths; no general Dehn algorithm or exhaustion claim
is required.

Here is the legal expansion of any recorded local rewrite. Write the
current receiver as `P A S`, and a signed donor rotation as

    d=U^-1 r^epsilon U=A B.

Rotate the donor to d and conjugate the receiver by P^-1, giving `A S P`.
Invert the receiver, positively multiply it by the donor, and invert it
back. This left-multiplies it by d^-1 and gives `B^-1 S P`. Conjugate by P
to obtain exactly `P B^-1 S`. Finally restore the donor's rotation and
sign. All conjugations are expanded letter by letter and every free
endpoint is checked. Keeping only short rotations on the donor avoids
the large intermediate words caused by conjugating it by an entire disk
boundary prefix.

## The new waypoint subgroups still contain no primitive element

The exact folded graphs of `<u1,b'>` and `<u2,b'>` have respectively
10 and 13 vertices, both of rank two. In **each** graph every directed
subgraph on one of the signed alphabets

    xy,  xY,  Xy,  XY

is acyclic. Explicit topological orders are saved in
`results/hump_waypoint_audit.json`.

As proved in M's earlier report using Nielsen's rank-two conjugacy
uniqueness theorem, every cyclically reduced primitive word belongs to
one of these signed alphabets. A primitive element in either subgroup
would give a nonempty closed path of that type at some vertex of its
folded graph. Acyclicity rules this out at **every word length**.

Thus neither new pair can reach a primitive coordinate, or the basis, by
Nielsen operations alone. This is a subgroup-specific statement; future
individual ambient conjugations can change the subgroup.

## A joint short-departure catalogue extension

The coordinating agent's exact quotient calculation records:

- a set R8 of 32 literal cyclically reduced length-eight words, given by
  rotations and inverses of two representatives;
- a set R9 of 432 literal cyclically reduced length-nine words, given by
  rotations and inverses of 24 representatives.

Its original 464 pairs have the frozen relator literally equal to p or b:

    {(p,r): r in R8} union {(s,b): s in R9}.

I additionally allowed every cyclic rotation and inverse of the frozen
word. Since the orbit sizes of p and b are 14 and 12, this gives

    Orb(p) times R8  union  R9 times Orb(b),

an explicit set of **5,632 literal pairs**. They generate **1,340 distinct
based subgroup graphs**. Every one of these subgroups contains no
primitive element of F2.

This finite-catalogue theorem covers all words in each listed subgroup;
it is not a bounded enumeration of possible primitive words. Its scope
is nevertheless the stated **literal** word pairs. Arbitrary independent
conjugating tails on the two relators are not included, and no stronger
cyclic-peak bound or global AC invariant is inferred.

### Why branching signed components are also excluded

The coordinating agent found two exceptional literal relators for which
a signed strongly connected component branches:

    xxyXXyXY,  yxYxxYXX.

They are literal inverses, so they generate the same subgroup together
with p. In its x,Y graph, every closed walk contains the shared path
labeled `xYYY`, followed by one of two return paths labeled `Yxx` or
`xYxxY`. Hence every such cyclic word contains **both xx and YY**. The
inverse signed alphabet has the inverse statement; xy and XY are
acyclic.

A cyclically reduced primitive word in a signed rank-two alphabet cannot
contain doubles of both letters. To see this, use the positive primitive
representative from Euclidean induction in M's first report. If the first
letter count exceeds the second, the outer substitution is `y->xy`, so
the second letter is isolated, including at the cyclic boundary. If the
second count exceeds the first, `x->xy` makes the first letter isolated.
The equal coprime case is xy. Nielsen uniqueness transfers this property
to every primitive cyclic representative. The zero-count generator cases
also avoid one of the two doubles.

The branching case therefore contains no primitive element either. This
does not assume that a strongly connected component is a simple cycle.

### Explicit line-graph certificate for every catalogue graph

The compressed certificate records the 26 upstream representatives,
all 1,340 actual folded based graphs, and topological orders for 10,720
finite directed line graphs. For each signed alphabet `{a,b}`, form a
directed graph whose vertices are the allowed edges of the subgroup graph.
An edge-state e can be followed by f when their endpoints match. First
delete transitions labeled aa, and separately delete transitions labeled
bb. Both resulting graphs are acyclic in every recorded case.

A closed cyclic word avoiding aa would give a cycle in the first line
graph; one avoiding bb would give a cycle in the second. Thus every
nonempty signed closed word contains both doubles and cannot be primitive.
This criterion handles the simple-cycle and branching cases uniformly.

The saved verifier recomputes every one of the 5,632 subgroup folds,
matches its actual graph to the recorded list, validates inverse labeled
arcs, and checks every claimed topological order edge by edge. It does
not trust a stored `primitive_free` flag. All checks pass. The certificate
is 669,422 bytes after decoding and 99,177 ASCII bytes in gzip/base64 form.

The upstream quotient membership/classification is the coordinating
agent's result. The signed-line-graph proof verifies primitive absence
for exactly the supplied explicit catalogue and its stated rotations.

## Reproduce

The new scripts use only the Python standard library and the already
published strict verifier and M's `stallings_search.py` graph routine.

```sh
python3 experiments/low_peak_rewrite.py --directory /tmp/ac_hump
python3 experiments/elementary_verify.py \
  /tmp/ac_hump/hump_low_peak_entry.json \
  /tmp/ac_hump/hump_low_peak_u1.json \
  /tmp/ac_hump/hump_low_peak_u2.json

python3 experiments/verify_hump_waypoints.py \
  certificates/hump_low_peak_u1.json certificates/hump_low_peak_u2.json \
  --output /tmp/ac_hump/waypoint_review.json

python3 experiments/hump_catalogue_obstruction.py \
  --verify certificates/hump_catalogue_dag_certificate.json.gz.b64 \
  --output /tmp/ac_hump/catalogue_review.json
```

The catalogue certificate is self-contained after decoding. To regenerate
it from the coordinating agent's enumeration, provide that result file
with `--source`, and an output path with `--certificate`.

The new strict paths are genuine reachable free-group waypoints. The
primitive-free subgroup checks rule out their Nielsen-only completion,
including hidden primitive elements not present in the displayed pair.
Finding a further permitted move leading to a primitive waypoint or a
complete basis path remains necessary. No requested breakthrough has
been achieved here.
