# O follow-up: cyclic-search review and primitive-free literal subgroups

Date: 2026-11-02. **No AK(3) trivialization or unrestricted AC obstruction
is established.** No novelty claim. The results below distinguish
coordinate primitivity, which is invariant under conjugation, from
primitive elements hidden in a generated subgroup, which can change
under independent conjugations of its generators.

## Prior reading and independently chosen work

After my arbitrary-tail and Nielsen-prelude investigations, the
coordinating agent asked me to read N's newly completed cyclic-cap-20
calculation before choosing a complementary continuation. I read
`cyclic_component.cpp`, its cap-20 data, the independent closure checker,
and then N's complete axes argument. I independently reviewed the
full-neighbor formula and chose a search for a hidden ambient primitive
in the **whole subgroup** of a reachable literal pair. Such a primitive
would provide a possible ordinary-AC completion even when neither
displayed coordinate is primitive.

The initial coordinate scan reused M's Whitehead descent. N had already
run the same routine, so that duplicate execution is **not** claimed as
an independent algorithm. I subsequently implemented a separate exact
Euclidean/Nielsen classification using no M primitive-test or word
routines. For subgroup graphs I used O's earlier batch union-find folding
implementation, M's signed-cycle proof idea, and new SCC/run-length
refinements developed here. N generated the cyclic catalogues; the
coordinating agent and P independently verified their closure and
connectivity. Their [cyclic-search report](research-n-cyclic-search.md)
records that separate evidence.

## 1. Independent review of the complete cyclic neighbor menu

Let a,b be the cyclic lengths of the receiver and retained donor. Take
arbitrary independent conjugates of those words. Their axes in the free
Cayley tree either intersect or are disjoint.

If they intersect, choose a vertex in the intersection and simultaneously
conjugate both elements to that vertex. Both words become cyclically
reduced, hence cyclic rotations of their original cyclic words. Their
product's cyclic class is therefore represented by the product of two
such rotations. Signs are supplied by relator inversions.

If their axes are disjoint, use their unique shortest bridge, labeled q,
of length d>=1. At each endpoint the bridge edge lies off the axis.
After simultaneous conjugation, the product has the form

    u' q v' q^-1.

All four cyclic junctions are reduced: an incident bridge edge and an
axis edge cannot cancel. Thus its exact cyclic length is a+b+2d. With
the donor retained, the new tuple's cyclic energy is

    a+2b+2d.

Consequently the complete finite menu under a cyclic cap C consists of
all signed rotations, with bridge words of lengths

    0<=d<=max(0,floor((C-a-2b)/2)).

The d=0 menu includes the intersecting-axis case. Extra words in this
menu may represent intersecting axes or duplicate an edge, which is
harmless; each is an actual free-word product. The axes proof shows
that no allowed product is omitted.

I checked that N's C++ implementation uses exactly the formula
`cap-receiver_length-2*donor_length`, enumerates all reduced bridge words,
uses both recipient choices and all signed rotations, and freely and
cyclically reduces before applying the cap. Its canonicalization uses
only rotations, inversion and coordinate ordering. It inserts no ambient
generator automorphism or quotient-relator equality.

The state-limit control reports `INCOMPLETE` if it fires; such a run is
not a closed-component certificate. The source's innermost break can
allow that incomplete run to slightly overshoot its nominal state
budget, but cannot convert it to `PASS`. I found no material flaw in the
mathematical neighbor menu or its implementation. The exhaustive
closed-set/connectivity checks are the separate work credited above,
not a claim that I independently reran every C++ neighbor comparison.

## 2. Exact primitive-word classification without Whitehead descent

For nonnegative coprime integers A,B, construct a positive primitive word
P(A,B) by Euclidean induction:

- P(1,0)=x, P(0,1)=y, P(1,1)=xy;
- if A>B>0, replace y by xy in P(A-B,B);
- if B>A>0, replace x by xy in P(A,B-A).

Each substitution is an automorphism of F2, so the result is primitive
and has the required exponent vector. Inverting either ambient
generator supplies every sign pattern.

Nielsen's rank-two uniqueness theorem says that primitive elements with
the same exponent vector are conjugate. A primary modern proof is
[Clay–Conant–Ramasubramanian, Corollary 4.4](https://msp.org/involve/2014/7-4/involve-v7-n4-p01-p.pdf).
Therefore a nonempty cyclically reduced word is primitive **if and only
if** it uses at most one sign of each generator, its exponent vector is
coprime, and it is a cyclic rotation of the corresponding signed
Euclidean representative. This is an exact classification, with no
search-length parameter.

The standalone script `euclidean_primitive_audit.py` implements this
criterion using only Python's standard library. It uses no Whitehead
descent code. Its 3,208 positive signed/rotated controls pass.

| Catalogue | Literal pairs | Distinct cyclic/inverse coordinates | Primitive coordinates |
|---|---:|---:|---:|
| Cyclic cap 20 | 39,840 | 25,452 | 0 |
| Cyclic cap 21 | 144,292 | 99,546 | 0 |
| Cyclic cap 22 | 258,032 | 179,630 | 0 |

I ran this classification on the cap-20/cap-21 data independently of
N's Whitehead executions, and the whole-subgroup audit below also runs
the Euclidean classification on cap 22. N separately replayed the
published standalone Euclidean script on cap 22. Its result rejects
179,086 mixed-sign cyclic words and 544 words differing from the required
signed primitive rotation. Every coordinate has coprime exponent vector,
as expected for the normally generating tuples.

Coordinate primitivity is preserved under free conjugation and
inversion. Hence these coordinate results apply to **every** actual
representative of the stored cyclic-coordinate classes, including
arbitrary conjugating tails. Combined with the independently verified
complete cap-22 component, they support N's cyclic peak lower bound 23
before an ordinary path can reach **any primitive coordinate**. This is
a finite-cap theorem, not an unrestricted obstruction.

## 3. Search for a primitive hidden in the whole literal subgroup

A different possible completion is that H=<u,v> contains a primitive
element even though neither u nor v is primitive. A primitive ambient
element z in H is also primitive in H: choose an ambient basis containing
z; in H's based Schreier graph, z is a loop at the basepoint. A spanning
tree omits that loop, so the associated non-tree-edge free basis of H
contains z. This uses the standard subgroup-graph basis construction in
[Kapovich–Myasnikov](https://web.stevens.edu/algebraic/alexeim/Teaching/GroupTheory626/graph5.pdf).
For rank-two H, a suitable Nielsen basis could then expose
it as a coordinate, permitting the existing primitive completion compiler
to be used. This motivated checking full subgroup graphs rather than
stopping at the coordinate scan.

For **each literal canonical pair in N's stored lists**, I folded its two
based word loops. This covers all elements at every length within that
specific subgroup. The result is:

| Catalogue | Literal pairs | Distinct based subgroup graphs | Direct signed DAG proof | Simple-cycle refinement | Balanced-run refinement | Unresolved |
|---|---:|---:|---:|---:|---:|---:|
| Cap 20 | 39,840 | 39,378 | 39,286 | 91 | 1 | 0 |
| Cap 21 | 144,292 | 140,874 | 140,561 | 308 | 5 | 0 |
| Cap 22 | 258,032 | 250,885 | 250,469 | 410 | 6 | 0 |

Thus **every listed literal canonical subgroup contains no ambient
primitive at any word length**. The three graph counts are per catalogue,
not disjoint counts across catalogues.

### Direct signed-cycle criterion

Every rank-two primitive cyclic word belongs to a signed alphabet
{s,t}. Moreover at least one letter is isolated: its cyclic word avoids
ss or avoids tt. This follows from the same Euclidean primitive
construction and Nielsen uniqueness used above.

For each signed alphabet, form the directed edge-state graph of the
folded subgroup graph and forbid ss transitions, and separately tt
transitions. M's previous criterion proves primitive absence when all
these graphs are acyclic. O's independently implemented folding/DAG
routine verifies the first proof column above.

### Simple-cycle SCC refinement

A closed walk lies inside a strongly connected component. If a cyclic
SCC of one of the double-free edge-state graphs is a simple directed
cycle, every closed walk in it reads a power of a rotation of its one
cycle word. The exact Euclidean primitive test decides that cycle word.
If it is nonprimitive, all its nonzero powers are nonprimitive as well.

The second proof column consists of graphs whose remaining cyclic SCCs
are all simple directed cycles of explicitly checked nonprimitive words.
The result files retain those words and their signed alphabets. No
bounded enumeration of possible subgroup words is used here.

### Balanced-run refinement for the remaining branching graphs

Suppose a positive primitive cyclic word has isolated s's and uses both
letters. Then all intervening t-runs have lengths k or k+1 for a single
integer k>=1. Here is a derivation rather than an appeal to a word-pattern
heuristic. Let its letter counts be A,B. Isolation gives B>=A. If A=1,
there is only one run. Otherwise write B=kA+r, with 0<r<A because the
counts are coprime. In the Euclidean construction, start with P(A,r),
where t is isolated, and apply s->s t exactly k times. Its old t-runs
have lengths zero or one between successive s's, so the new lengths are
k or k+1. Nielsen uniqueness transfers this pattern to every primitive
cyclic word with those counts.

For each remaining branching graph, form a weighted graph whose vertices
are its s-labeled edges. Record a directed edge of weight r when the end
of one s-edge can read exactly r>=1 t-edges and then the next s-edge.
The successful certificates have no infinite t-path reachable from such
an endpoint. Thus every possible recorded run is finite, with an
explicit maximum. If such an infinite path were encountered, the program
would return inconclusive rather than extrapolate a bound.

For **every** integer k from one to the maximum recorded run, retain
only weighted edges of weights k or k+1. All these finite graphs are
acyclic. Therefore no closed cyclic word using isolated s's can have
the required primitive run pattern. Single-letter primitive loops are
checked separately and absent. Pure powers of a single generator of
length greater than one are nonprimitive.

The parameter starts at k=1 because avoiding ss makes each intervening
t-run nonempty. For k larger than the maximum recorded run there are no
retained edges, so no additional unbounded parameter cases remain.

This supplies an unbounded exclusion for each remaining branching SCC.
The result files record every weighted transition and every topological
order, and the verifier can reconstruct them from the actual subgroup
graph. A set of 364 genuine primitive signed-cycle control graphs
correctly fails this sufficient exclusion criterion.

For a concrete example, the cap-20 exceptional pair is

    (XYxYxY, XyyXyyXyyyyyy).

Its X,y graph has two routes from vertex 0 to vertex 1, labeled X and
yXyXy, followed by the common return yyXyyXyyyyyy. Every closed cyclic
word therefore has a y-run of length two and another of length six or
seven. These cannot be the two neighboring lengths k,k+1. The general
weighted-graph check also handles the five additional cap-21/cap-22
branching cases, without assuming that a signed SCC is a simple cycle.

## 4. Exact scope of the subgroup result

The full-subgroup theorem concerns the **literal canonical based pairs**
stored in the supplied lists. Independently rotating or conjugating the
two generators can change their generated subgroup. Those altered
subgroups are **not** included in this theorem merely because their
coordinates have the same cyclic classes. No unrestricted tail theorem
for these 258,032 families has been proved here.

Consequently arbitrary Nielsen operations alone cannot expose a primitive
from any of these particular literal pairs, even at unbounded length.
This differs from the coordinate result in Section 2, whose conjugacy
invariance really does cover every representative. It also differs from
my earlier short-prelude theorem, whose explicit finite-tail reduction
covered unbounded independent conjugators for only its stated families.

Neither distinction can be dropped in order to claim AC nontriviality.
Arbitrary interspersed individual conjugations can leave the listed
literal subgroups, and caps above 22 remain available.

## Reproduce and review artifacts

The cap-22 source catalogue has decoded JSON SHA256
`2c8d0ac4c58f590de7151eae3dd09577d2365bf0e858887d801ce24c5c609c8e`,
matching N's published state manifest. The result files also record exact
hashes for the cap-20/cap-21 source lists. Counts above are obtained by
refolding the actual words, not trusting stored primitive-free flags.

Place all scripts together in `experiments/`. Decode N's published
catalogue as described in its report, then run:

```sh
python3 experiments/euclidean_primitive_audit.py /tmp/cyclic22_saved.json
python3 experiments/audit_cyclic_subgroups.py /tmp/cyclic22_saved.json \
  --output /tmp/cyclic22_subgroup_review.json
```

The whole-subgroup driver uses `arbitrary_tail_certificate.py`,
`refine_primitive_cycles.py`, `balanced_run_certificate.py`, and the
standalone Euclidean classifier. All use only Python's standard library.
The compressed subgroup review files under `results/` are ordinary
gzip/base64 JSON containing the exceptional-graph proof data; the script
regenerates the same mathematical fields, with runtime fields allowed
to vary.

Published proof data: [cap 20](../results/cyclic20_canonical_subgroup_review.json.gz.b64),
[cap 21](../results/cyclic21_canonical_subgroup_review.json.gz.b64),
and [cap 22](../results/cyclic22_canonical_subgroup_review.json.gz.b64).
The independent standalone coordinate results are
[cap 20](../results/cyclic20_euclidean_primitive_results.json),
[cap 21](../results/cyclic21_euclidean_primitive_results.json), and
[N's replay at cap 22](../results/n_cyclic22_euclidean_primitive_results.json).

This investigation found no actual primitive waypoint and supplies no
ordinary free-basis certificate for AK(3). Its checked restricted
exclusions and independent algorithm review leave all four requested
breakthrough objectives unachieved.
