# Research Y: rotation coverage and the exact two-phase scope

Date: 2026-11-02. **AK(3) and the ordinary Andrews–Curtis conjecture
remain unresolved.** This is an independent review of the source
coverage and geometric scope of X's rotation-successor extension.
No novelty or priority claim is made.

## Prior reading and choice

Before selecting my direction I fetched the current repository README
(blob `75d1116fb9d548f79d45e651aa27dd2b4616760c`) and read V's unbounded
two-conjugate theorem, Q's Cayley-tree rotation reduction, T's review of
W's topology, and X's all-42 driver and result. I independently chose
the possible gap between a finite rotation list and an assertion about
two successive conjugation phases. T independently audited the graph,
character and weighted-cycle certificates; this review does not duplicate
that certificate computation or the long heuristic searches.

## The finite source list is complete and reachable

Write `p=xxxYYYY`, `b=xyxYXY`. For `0<=i<7` and `0<=j<6`, let

```
r_i = p[i:] p[:i],    s_j = b[j:] b[:j],    H_ij = <r_i,s_j>.
```

My separate standard-library checker imports no graph or AC code from
X, V or T. It checks the exact offset Cartesian product and independently
folds the literal two-word bouquet for every source. All **42** records
occur exactly once and match their saved based folded graphs. Six source
graphs have ten vertices, 34 have eleven, and two have twelve.

For each source, the quotient index list and its weighted-certificate
index list both contain every unordered pair of distinct graph vertices
exactly once. Consequently the total is

```
6*C(10,2) + 34*C(11,2) + 2*C(12,2) = 2,272.
```

This verifies source and index coverage, not the contents of every
character or potential certificate. X constructs those data and T's
[independent character review](research-t-x-character-review.md)
rechecks all 2,272 quotients, 18,176 signed automata, 13,756 cyclic
components and 42,876 potential inequalities. I use that separately
audited certificate theorem below.

Every source is also an actual ordinary-AC reachable tuple. A left
rotation by a prefix `u` is conjugation by `u^-1`; alternatively, writing
the word `u v`, conjugation by `v` gives `v u`. Choosing the shorter
of these two conjugators gives explicit entries using only
single-generator conjugations. The checker constructs and independently
replays all 42 ledgers: **135 total elementary moves**, at most six per
entry, with raw total length always 13. These are compact entries, not
claims of optimal AC distances.

## What the certified subgroup property says

The audited conclusion for each source is the following property:

> For arbitrary `u,v in H_ij` and arbitrary `a,c in F(x,y)`, the subgroup
> `<a u a^-1, c v c^-1>` contains no primitive element of the ambient
> free group.

The geometric deduction from finite vertex-identification kernels is
V's theorem applied to each new source. In particular it handles equal
source vertices, distinct source vertices, disjoint second-phase axes,
identity sources, and arbitrary word lengths as in
[V's proof](research-v-unbounded.md). The source words need
not form a displayed basis after they have been selected from `H_ij`.

This property is invariant under common conjugacy of the entire source
subgroup. If `H'=d H_ij d^-1` and `u'=d u d^-1`, then

```
a u' a^-1 = (a d) u (a d)^-1.
```

Thus every conjugate of a certified `H_ij` has the same property. This
invariance is elementary; it is not an assertion that arbitrary
independent conjugations preserve that property.

## Exact deduction for two phases

Consider this restricted ordinary move pattern:

1. Starting from `(p,b)`, independently conjugate its two coordinates by
   arbitrary words. At the **endpoint** of this first conjugation phase,
   require their translation axes in the free Cayley tree to intersect.
2. Apply arbitrary coordinate Nielsen operations (inversion, coordinate
   interchange, and multiplication of one coordinate by the other).
3. Independently conjugate the resulting two coordinates by arbitrary
   words, then apply any further coordinate Nielsen suffix.

This pattern cannot reach a free basis.

Here is the full reduction. Let the endpoint of step 1 be `(g,h)`.
An intersection of Cayley-tree axes contains a vertex, since the axes
are unions of whole edges. Conjugate the pair commonly so that this
vertex becomes the identity. A translation read from a vertex on its
own axis is cyclically reduced; the successive labels on the translated
axis are the repeated letters of `p` or `b`. Therefore the resulting
two words are some `r_i,s_j`. Thus

```
(g,h) = (d r_i d^-1, d s_j d^-1)
```

for a single `d`. This is exactly the intersecting-axis argument in
[Q's rotation theorem](research-q.md), now used to identify the entire
intermediate subgroup, rather than only to test its immediate primitive
content.

Every coordinate Nielsen operation in step 2 preserves the subgroup.
Its endpoint therefore has the form `(d u d^-1,d v d^-1)` with
`u,v in H_ij`. There is no need to infer that arbitrary primitive words
with unimodular exponent vectors form a basis: actual subgroup membership
alone suffices. After step 3's independent conjugations, the coordinates
are

```
((a d) u (a d)^-1, (c d) v (c d)^-1).
```

The certified property excludes ambient primitives in their generated
subgroup. The final Nielsen suffix preserves that subgroup and hence
cannot produce a primitive coordinate or a free basis. No ambient
generator substitutions, quotient rewriting or stabilization are
silently inserted in this deduction.

The axes need intersect only at the endpoint of step 1. Intermediate
conjugation steps may have disjoint axes. Initial coordinate inversions
and interchange require no additional rotation cases: they leave the
generated source subgroup unchanged, and inverse rotations generate the
same `H_ij`.

## Boundaries of the result

Two restrictions are essential to the stated coverage.

* If the first-phase axes are disjoint at their endpoint, the intermediate
  subgroup is a barbell with a potentially arbitrary nonempty bridge.
  The 42 literal rotation subgroups do not enumerate that bridge family.
  Q/V's one-phase primitive-freeness of such a barbell does not by itself
  establish the stronger all-source-words property needed after later
  Nielsen mixing.
* An arbitrary Nielsen prelude before a nonempty first conjugation phase
  changes its source words from `p,b` to arbitrary elements of `H0`.
  Their cyclic rotation list is not the fixed 7-by-6 list checked here.
  V's earlier one-phase theorem still applies in its own scope, but
  this argument does not extend the new two-phase conclusion to all
  such preludes.

The result also supplies no induction through a further alternating
phase. In particular it is not a global AC invariant, not a count of the
minimum conjugation phases in every possible trivialization, and not an
increase of the established global cyclic-peak lower bound of 23.
I found no gap in the restricted endpoint-intersection statement above.

## Reproduction

The source JSON may be plain, gzip, or base64-wrapped gzip. After decoding
X's all-42 result into a local JSON file, run:

```sh
python3 experiments/y_rotation_scope_review.py /tmp/x_all42.json --output /tmp/y_rotation_scope.json --entries /tmp/y_rotation_entries.json
```

Saved results are
`certificates/y_rotation_scope_review.json` and
`certificates/y_rotation_entry_ledgers.json`. The decoded input SHA256 is
`cf9e4a304fec9e0d24ea0e7c420dab113f20c8fb1a058f568ac996d8efd97ffc`.
All mathematical conclusions remain restricted as stated; no requested
unrestricted breakthrough outcome has been achieved.
