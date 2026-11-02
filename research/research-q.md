# Q: arbitrary-tail subgroups reduce to rotation pairs

Date: 2026-11-02. **No AK(3) trivialization or unrestricted AC invariant
is established.** This is a computer-assisted primitive-free subgroup
theorem for the published cyclic cap-22 component. No novelty claim is
made.

## Prior reading, choice, and collaboration

Before choosing a direction, I fetched the repository README and read
[N's cyclic search](research-n-cyclic-search.md),
[P's independent cap-21/22 review](research-p-cyclic21-review.md), and
[O's whole-subgroup review](research-o-cyclic-review.md). O had proved
primitive absence for all literal canonical cap-22 pairs, while expressly
excluding arbitrary independent conjugating tails from that subgroup
claim. I independently chose that gap as a possible route to an actual
primitive waypoint: a primitive hidden in a differently based subgroup
could permit an ordinary AC completion.

R independently chose the same gap. We compared the geometric ideas,
then divided the work. Q implemented exhaustive independent-rotation
enumeration, fast folding, unbased core-graph deduplication, and a
sufficient signed-DAG filter. R independently derived and checked the
rotation reduction and implemented a complete primitive-loop decision
using finite pairs of partial vertex maps. R independently refolded every
exception from Q's filter and supplied complete negative certificates.
The theorem below combines those distinct contributions. N supplied the
already independently audited source catalogue; this report does not
claim a new cyclic-peak lower bound or a new cyclic component.

## 1. A finite rotation reduction for arbitrary conjugating tails

Work in F=F(x,y). For a nonempty cyclically reduced word u, let Rot(u)
be its finite set of cyclic rotations. A subgroup is primitive-free if
it contains no member of a free basis of the ambient F.

**Rotation theorem.** For nonempty cyclically reduced u,v, the following
are equivalent:

1. For every a,c in F, the subgroup
   `<a u a^-1, c v c^-1>` is primitive-free.
2. Every subgroup `<u',v'>`, with u' in Rot(u) and v' in Rot(v), is
   primitive-free.

Independent inversion of either generator is already harmless: it does
not change the generated subgroup. Thus inverse rotations need not be
separately enumerated.

The forward implication is immediate because a cyclic rotation is a
conjugate. For the converse, condition 2 implies in particular that u
and v themselves are nonprimitive. Consider the translation axes in
the free Cayley tree of arbitrary conjugates g=a u a^-1 and h=c v c^-1.

If the axes intersect, choose an intersection vertex z and simultaneously
conjugate both elements by z^-1. Each translated word is now read from
a vertex on its own axis, so it is a cyclic rotation of its given
cyclic word. Hence `<g,h>` is globally conjugate to one of the finitely
tested rotation subgroups. Ambient primitivity is preserved by global
conjugation.

If the axes are disjoint, use their unique shortest bridge. After
simultaneous conjugation, the two generators read u' and q v' q^-1,
where q is the nonempty bridge and u',v' are cyclic rotations. Each
bridge endpoint is off the corresponding axis. The labelled graph
consisting of the two word circles joined by this bridge is therefore
folded: neither attachment can fold into a circle. It is the usual
immersed subgroup graph, with a genuine separating bridge.

A cyclically reduced primitive word in F2 uses at most one sign of each
ambient generator. This follows by constructing a positive Euclidean
primitive representative for each coprime exponent vector, changing
generator signs, and applying Nielsen's primitive conjugacy uniqueness.
See [Clay--Conant--Ramasubramanian, Corollary 4.4](https://msp.org/involve/2014/7-4/involve-v7-n4-p01-p.pdf).
A closed cyclic path crossing a bridge must traverse its edge in both
directions, and so uses both signs of that edge's generator. Such a
path cannot read a primitive cyclic word. A possible primitive loop must
stay in one word circle, where it is a nonzero power of a cyclic rotation
of u or v. Neither a nonprimitive word nor its nonzero powers can be
primitive. This excludes the disjoint-axis case.

Finally, a primitive subgroup element need not initially be cyclically
reduced at the graph's distinguished vertex. Cyclic reduction of its
accepted path leaves a cyclic closed path at another vertex: inverse
paths in a folded graph are unique. The argument above therefore covers
every subgroup element, at every length. This proves the theorem.

The ambient rank-two hypothesis enters through the one-sign property of
primitive cyclic words. No corresponding theorem is claimed in higher
rank.

This reduction removes the exponential tail-length enumeration needed
by the earlier finite-tail argument. It also gives a short alternative
explanation of why M's first-departure catalogue, once every independent
rotation is retained, suffices for that catalogue's arbitrary-tail
subgroup theorem. It does not remove the need to test all rotations of
later pairs.

## 2. Exhaustive cap-22 application

Use N's exact published cap-22 cyclic component C22, with decoded JSON
SHA-256

    2c8d0ac4c58f590de7151eae3dd09577d2365bf0e858887d801ce24c5c609c8e.

It contains 258,032 canonical pairs. Q enumerated every independent
cyclic rotation of both words in each pair. Every word here has coprime
exponent vector, so it is not a proper power; all its cyclic rotations
are distinct. Independently summing `|u|*|v|` over the input reproduces
the total rotation-pair count.

| Exact quantity | Value |
|---|---:|
| Source cyclic pairs | 258,032 |
| Independent literal rotation pairs | 24,136,172 |
| Distinct unbased labelled rank-two core graphs | 11,431,368 |
| Graphs excluded by the signed-DAG criterion | 11,424,800 |
| Remaining graphs sent to R | 6,568 |
| R's complete negative primitive decisions | 6,568 |
| R's incomplete or positive decisions | 0 |

Q's C++ program folds the actual two word loops by vertex identification.
It verifies inverse arcs, connectedness, core degree, and rank two.
Rank two also follows from the unimodular exponent matrix inherited
from AK(3); rotations do not change exponent vectors.

Primitive-loop existence is invariant under forgetting the subgroup's
basepoint: a loop at another vertex can be brought to the base by a
path and its inverse, preserving ambient primitivity. The program
therefore deduplicates unbased labelled core graphs. For a connected
rank-two core, `sum(degree-2)=2`, so there is one degree-four vertex or
two degree-three vertices. Choosing each branch vertex in turn as the
start of a fixed-letter-order breadth-first encoding and taking the
least full adjacency encoding gives an exact label-preserving unbased
key. Equal keys describe isomorphic labelled core graphs; no generator
automorphism is used. The recorded original-base index still accepts
the actual rotated generators.

The direct filter is M/O's sufficient primitive-absence criterion. For
each signed alphabet and each selected forbidden double, it checks
acyclicity of the directed edge-state graph. Every primitive cyclic
word uses a signed alphabet and has at least one isolated generator,
so it avoids at least one such double. If every corresponding graph is
acyclic, no primitive loop is possible. A filter failure is only an
exception requiring further analysis; it is never treated as a
primitive witness.

The 6,568 exception records retain actual rotated pairs and their full
graphs. Their decoded JSONL SHA-256 is

    d530e68cab069aabac841a1082bf5624d657a920001a72a77a3b39365bf167a5.

R independently refolded every pair and verified agreement with Q's
graph after rebasing to its recorded original base. R's complete
finite-map decision exhausts all signed primitive conjugacy classes,
rather than imposing a word-length bound. Across the exceptions it
checks 735,712 partial-map pair states, with at most 76 states for any
one graph and signed alphabet. All initial maps, successor closure,
and absence of fixed vertices are separately verified in the saved
negative certificates. See [R's proof and verifier](research-r.md).
Q reviewed the mathematical positive-Nielsen completeness argument and
the map composition conventions. The exact decision and its independent
certificate verification are R's work, not a second Q implementation.

**Combined theorem.** For every cyclic pair in C22 and arbitrary
independent conjugating words a,c, the generated subgroup

    <a u a^-1, c v c^-1>

contains no ambient primitive element at any word length.

## 3. Independent implementation controls

`rotation_fold_controls.py` selects 5,000 deterministic independent
rotation pairs from the source catalogue, using seed 749821, and adds
two genuine primitive-containing controls. On all 5,002 pairs:

- Q's C++ folded unbased key agrees with M's separately written
  one-fold-at-a-time implementation followed by Python unbased encoding;
- Q's C++ cycle filter agrees with O's separate line-graph/topological
  implementation;
- the actual two words are accepted at the C++ recorded original base;
- both primitive-containing controls correctly fail the absence filter.

There are 4,995 direct-DAG exclusions among these controls. The controls
check conventions and independent implementations; the complete
24,136,172-pair enumeration and R's closed negative certificates supply
the finite proof component. They are not extrapolated from the sample.

The provenance file matches the scanner's exact TSV to N's decoded
JSON, checks both hashes, recomputes the source/rotation counts, and
hashes the complete exception file. Hashes establish data identity; they
do not replace the mathematical primitive criteria.

## 4. Consequence and limitations

Arbitrary coordinate Nielsen moves preserve the generated subgroup.
Thus from any actual representative of a cyclic state in C22, an
arbitrary Nielsen-only suffix cannot expose a primitive coordinate,
even if its intermediate lengths are unbounded. This strengthens O's
literal-canonical subgroup statement by including all independent
conjugating tails.

It does not make primitive-freeness an AC invariant. After Nielsen
mixing, new individual conjugations can change the subgroup and leave
the certified family. In any proposed completion, a further subgroup-
changing conjugation is required after the last visit to C22 before
the first primitive coordinate. That conjugation's source may have
small cyclic energy in another component reached through a larger
excursion. No new numerical bound on the energy of conjugation is
claimed. The independently established overall cyclic peak lower bound
remains 23.

This investigation sought an actual hidden primitive and found none
in the exhaustively stated family. It supplies neither a free-basis
path for AK(3) nor an obstruction at all lengths for arbitrary ordinary
AC moves. None of the four requested breakthrough objectives is
achieved.

## Reproduce

All Python dependencies below are already published together in
`experiments/`; only the standard library is used. C++17 is needed for
the full enumeration.

```sh
python3 experiments/cyclic_catalogue_to_tsv.py \
  certificates/cyclic22_component_manifest.json /tmp/cyclic22.tsv
c++ -std=c++17 -O3 experiments/rotation_subgroups.cpp -o /tmp/q_rotations
/tmp/q_rotations /tmp/cyclic22.tsv /tmp/q_candidates.jsonl /tmp/q_results.json
python3 experiments/rotation_fold_controls.py \
  certificates/cyclic22_component_manifest.json /tmp/q_rotations \
  --output /tmp/q_fold_controls.json
```

The full observed scan took about 110 seconds and stored 11.4 million
graph keys; memory and runtime depend on the host. The optional final
`max_pairs` argument produces an explicitly `INCOMPLETE` result when it
stops before exhausting the input, and is not accepted as the full
theorem.

The compressed exception file
`certificates/q_rotation_candidates.jsonl.gz.b64` contains 235,473 ASCII
bytes and decodes to 2,118,346 JSONL bytes. R's report supplies commands
to regenerate or verify all negative map certificates. The saved Q
results are `results/q_rotation_results.json`,
`results/q_rotation_fold_control_results.json`, and
`results/q_rotation_provenance.json`.
