# Research R: exact primitive detection by finite partial-map pairs

Date: 2026-11-02. **No AK(3) trivialization, unrestricted AC obstruction,
or proof/disproof of the conjecture is established.** No novelty claim.

## Prior reading and independent choice

I fetched the current repository README and read N's complete cyclic
search report, P's independent cap-21/22 review, and O's whole-subgroup
review before choosing a direction. These reports identify a precise
remaining gap: O's subgroup theorem covered literal canonical pairs,
whereas independently conjugating the two relators can change their
generated subgroup.

I independently chose that gap, initially using shortest relative tails
and endpoint overlaps. Q independently chose the same gap and observed
the simpler axes/rotation reduction below. We coordinated: Q enumerated
all rotated pair graphs, while R independently reviewed the reduction,
refolded every exceptional graph, and developed an exact primitive-loop
decision algorithm. This algorithm replaces a sufficient graph criterion
with a complete finite test, including constructive positive witnesses.

The primary primitive-class theorem used is
[Clay--Conant--Ramasubramanian, Corollary 4.4](https://msp.org/involve/2014/7-4/involve-v7-n4-p01-p.pdf):
primitive elements of F2 with the same exponent vector are conjugate.
Its Euclidean construction is also described in Theorem 4.6. The finite
map-pair proof below is explicit; no claim of a new literature result is
made.

## 1. Arbitrary relative conjugates reduce to cyclic rotations

Let u,v be nonempty cyclically reduced free words. The following are
equivalent:

1. Some independently conjugated subgroup `<a u a^-1,b v b^-1>` contains
   an ambient primitive element.
2. Some pair of cyclic rotations u',v' generates a subgroup containing
   an ambient primitive element.

The reverse implication is immediate because rotations are conjugates.
For the forward implication use the axes of the two elements in the
free Cayley tree. If they intersect, choose an intersection vertex and
simultaneously conjugate both to that vertex. Both become cyclically
reduced, hence rotations of u,v. Simultaneous conjugation preserves
ambient primitivity.

If the axes are disjoint, their unique connecting geodesic is off each
axis at its endpoint. The folded subgroup graph is a barbell: circles
reading rotations of u,v joined by a nonempty bridge. Any closed cyclic
path crossing a bridge uses its label in both directions. A cyclic
primitive word in F2 uses only one sign of each ambient generator, so
cannot cross that bridge. Any possible primitive loop therefore lies
entirely in one circle and reads a nonzero power of a rotation of u or v.
Such a primitive requires u or v itself to be primitive; in that case
the unrotated pair already satisfies item 2. Proper powers cannot be
primitive, by their exponent vector in a free basis.

This covers arbitrary word lengths and repeated words. Inverting either
subgroup generator changes no subgroup, so at most `|u|*|v|` rotation pairs
are required; no separate generator-inverse enumeration is needed.
This improves the earlier exponential short-tail enumeration without
changing its conclusion. It is a subgroup theorem, not an AC invariant.

## 2. A complete finite primitive-loop algorithm

Let Gamma be a finite connected folded inverse graph labeled x,X,y,Y.
Its based loops represent a finitely generated subgroup H of F(x,y).
The graph need not have subgroup rank two. For any signed alphabet
`{a,b}` among `xy,xY,Xy,XY`, let T_a,T_b be its partial vertex maps.
An undefined transition is represented by a separate missing value.

For a word UV, its partial map is obtained by following T_U first and
T_V second. Write this composition as `T_U*T_V`. Starting with the
ordered map pair `(T_a,T_b)`, close under

    L(A,B)=(A,A*B),       R(A,B)=(A*B,B).                 (1)

At every reached pair test whether either component has a fixed vertex.
A fixed vertex gives an actual primitive cyclic loop. If no component
has one and the finite pair-state graph is exhausted, H contains no
ambient primitive in that signed alphabet.

### Why every positive primitive class is tested

Starting with the free basis (a,b), the word operations

    (U,V)->(U,UV),       (U,V)->(UV,V)

preserve a free basis and positivity. Their count vectors are adjacent
unimodular columns. Every coprime vector (A,B) with A,B>0 occurs as a
component. Here is a termination proof rather than an appeal to a
bounded word search.

Initially express the target as `A*(1,0)+B*(0,1)`. More generally write
it `s*u+t*v` in the current positive unimodular columns. If s>t, replacing
v by u+v changes its coordinates to `(s-t,t)`; if t>s, replacing u by
u+v changes them to `(s,t-s)`. The sum of these positive coordinates
strictly decreases. When s=t, coprimality forces s=t=1, and the target
is the next mediant u+v. The zero-count cases are the initial letters.

The corresponding component word is primitive with the target exponent
vector. Nielsen uniqueness therefore makes every positive primitive
cyclic word a rotation of one such component. Changing signs supplies
every primitive class: given any primitive exponent vector, construct
the positive word for its absolute counts and invert the appropriate
ambient letters. Uniqueness implies that every cyclic representative
uses that signed alphabet. The word-generation updates are a derivation
device for primitive test words; they are not inserted as extra allowed
moves on the target presentation.

A rotation of a word labels a closed loop somewhere in a folded inverse
graph exactly when the original word does: change the starting point
along that loop. Testing a fixed vertex of the component map therefore
accounts for every cyclic rotation, not only one chosen word.

### Why the algorithm is finite and exact

For N vertices there are at most `(N+1)^N` partial transformations, hence
at most `(N+1)^(2N)` ordered pairs. Equality of maps makes both future
successors in (1) identical, so memoizing map pairs loses no test word.
The implementation reports `INCOMPLETE` if an explicit state budget
stops it. Only actual exhaustion yields `ABSENT`.

Conversely every component word generated by (1) is primitive. If it
fixes a vertex z, choose a path p from the basepoint to z. The word
`p w p^-1` is a based primitive in H. If any primitive element of H is
initially represented by a non-cyclically-reduced based word, removing
its conjugating prefix and suffix leaves a primitive cyclic loop at
some graph vertex, because inverse paths in a folded graph are unique.
Thus this procedure decides ambient primitive existence in H exactly.

For positive outputs the code records the signed alphabet, finite L/R
basis program, component, fixed vertex, base-to-loop path, and expanded
primitive word when reasonably sized. For negative outputs it records
finite closed sets of partial-map pairs. The separate verifier checks
the initial maps occur, neither component has a fixed vertex, and both
successors of every pair stay inside the set. Connectedness of that
negative certificate is unnecessary: a closed set containing the start
already includes every generated test word.

The byte-map implementation explicitly supports graphs with at most
255 vertices. This is an implementation limit, not a restriction of the
mathematical finite-map argument. The present candidate graphs are far
smaller.

## 3. Exact classification of Q's full cap-22 rotation candidates

[Q](research-q.md) exhausts the rotations of all 258,032 cyclic-cap-22
states from N's independently checked component. The exact counts are:

| Stage | Count |
|---|---:|
| Independent rotation pairs | 24,136,172 |
| Distinct unbased labeled core graphs | 11,431,368 |
| Q's direct signed-DAG absence proofs | 11,424,800 |
| Graphs left inconclusive by that sufficient criterion | 6,568 |
| R's complete finite-map absence decisions | 6,568 |
| Incomplete R decisions / actual primitive hits | 0 / 0 |

I independently folded each exceptional **actual rotated pair**, rebased
Q's graph at its recorded original basepoint, and compared every labeled
edge. All 6,568 match. This is an independent folding check on the
exceptional graphs, not a claim to have independently refolded all
24 million rotation pairs. Q separately publishes its folding controls.

Across the four signed alphabets, the complete R decisions use **735,712
partial-map pair states** in total. The largest single graph/alphabet
needs only **76** states. Every negative result is accompanied by its
actual finite closed-set certificate, and the dataset verifier checks
all of them without rerunning the discovery search.

The exact candidate JSONL SHA256 is

    d530e68cab069aabac841a1082bf5624d657a920001a72a77a3b39365bf167a5

Q's [compressed candidate file](../certificates/q_rotation_candidates.jsonl.gz.b64)
decodes to 2,118,346 bytes. R's compact proof data pool repeated maps
within each graph while retaining every closed pair state; they decode
to 13,278,100 JSONL bytes. The
[proof manifest](../certificates/r_rotation_map_pairs_manifest.json)
names four gzip/base64 parts totaling 1,936,073 ASCII bytes and records
part, assembled, decoded and candidate hashes. Compression and map
pooling are transport formats; the verifier reconstructs the maps.

### Joint Q/R consequence

For **every** tuple whose cyclic state lies in the complete AK(3)
cap-22 component, **every independent ambient conjugation of its two
coordinates** generates a subgroup containing no ambient primitive
element at any word length. This extends O's literal canonical subgroup
theorem to all conjugating-tail representatives, using the rotation
reduction and the exhaustive rotated-graph checks.

Arbitrary subsequent coordinate Nielsen operations preserve that
subgroup, so cannot expose a primitive relator, even if their lengths
grow without a bound. Further individual conjugations after such
Nielsen mixing can change the subgroup and are not covered when the
resulting cyclic state is outside the checked component. Outside that
component need not mean high energy: this theorem does **not** claim
that a particular conjugation in every trivialization must occur at
cyclic energy at least 23. No peak-reduction theorem for arbitrary
Nielsen excursions is silently assumed.

## 4. Controls and actual detector-to-basis calibration

The standalone control script passes:

- 372 signed primitive Christoffel cycle graphs, constructed independently
  by a mechanical word formula, all with actual positive witnesses;
- their 372 proper-square cycle graphs, all exhaustively negative with
  verified closed-set certificates;
- every one of the 1,457 reduced relative conjugators of length at most
  six at the initial AK(3) tuple, all negative;
- a state-budget stop correctly labeled `INCOMPLETE`, and rejection of a
  negative certificate with its initial pair removed.

The initial AK(3) subgroup needs 72 pair states across four alphabets.
O's former difficult 17-vertex branching example needs 104, providing an
exact alternative to its balanced-run argument.

For a positive ordinary-AC calibration use O's known AK(2) prelude pair

    A=XXyyy,       B=XYxYYxy.

The detector finds the primitive cyclic word `xYxYYxYY` at vertex three,
with base-to-loop path `XX`. Its based primitive is

    w=XYxYYxYYxx = B*A^-1.

The certificate from the original AK(2) tuple to `(A,w)` uses **17 strict
elementary moves** and raw peak **15**. M's existing completion compiler
then produces an exact full AK(2) basis ledger of **337 strict moves**,
raw peak **33**, with endpoint `(x,y)`. The coordinating agent's separate
strict elementary verifier accepts both. This is a calibration, not an
improvement claim over other AK(2) certificates and not an AK(3) solution.
No ambient generator automorphism remains as an implicit certificate move.

## Reproduce

All scripts use only Python's standard library and reside together in
`experiments/`. The first command recomputes the complete map-pair
decisions; the second checks the saved closed sets instead.

```sh
python3 experiments/analyse_rotation_candidates.py \
  certificates/q_rotation_candidates.jsonl.gz.b64 \
  --output /tmp/r_decisions.json
python3 experiments/analyse_rotation_candidates.py \
  certificates/q_rotation_candidates.jsonl.gz.b64 \
  --verify-certificates certificates/r_rotation_map_pairs_manifest.json \
  --output /tmp/r_closed_sets.json
python3 experiments/r_map_pair_controls.py --output /tmp/r_controls.json
python3 experiments/elementary_verify.py \
  certificates/r_ak2_map_waypoint.json certificates/r_ak2_map_full.json
```

To regenerate the positive calibration as well, add
`--ak2-source certificates/o_ak2_tail_waypoint.json --directory /tmp/r_ak2`
to the control command. This imports M's published completion compiler.

The full AC goal remains unchanged. No primitive waypoint for AK(3) has
been found here, and these restricted exclusions are not preserved by
all unbounded AC moves.
