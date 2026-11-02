# N follow-up: complete ordinary-AC components for cyclic length

Date: 2026-11-02. **Full cap-21 independent audit passed.**
No novelty claim is made. This is a finite-energy exclusion, not an
unrestricted AC obstruction or an AK(3) trivialization.

## Previous work and independently chosen continuation

After my cyclic braid-preimage report, the coordinating agent relayed P's
new exact transition from `(u1,r)` to `(u1,u2)`, where

    u1=yXYXyxx,  u2=YxYXyyx,  r=XXyxYxxY.

I read P's report and probe, then independently chose an actual free-word
search from this length-fourteen waypoint. P investigated arbitrary
conjugating tails there, O investigated Nielsen preludes at the original
tuple, and I interleaved signed products, cyclic rotations and short
relative conjugations. Every positive edge was expanded into strict
ordinary moves. No ambient generator automorphism was used as a move.

This search reached the length-thirteen tuple

    (XXyxYY, XXXYYxy).

The coordinating agent checked its old packed cap-18 component and
extracted shorter ordinary ledgers: [43 strict moves and raw peak 18](../certificates/length13_cap18.json) to
the reversed length-thirteen tuple, and [32 strict moves and raw peak 18](../certificates/length14_cap18.json)
to `(u2,u1)`. These states were already in the previously classified raw
component. The new paths do not escape that component or solve AK(3).

The useful further development was an exact completeness criterion for
the cyclic search. The coordinating agent and O independently reviewed
the axes argument below; the coordinating agent independently checked
the cap-18 and cap-20 closed sets. P wrote a separate full cap-21 checker.
The reports and checker results identify which portions are independent.

## Energy and exact move graph

Let `cl(w)` be the length of the cyclically reduced free word conjugate
to w, and put

    E(r0,r1)=cl(r0)+cl(r1).

This differs from the **raw** sum of freely reduced word lengths. All
conjugating tails disappear from E. Inversion and individual relator
conjugation preserve E; multiplication can change it.

The graph here is the graph of ordinary, unstabilized AC moves with
fixed ambient generators x,y. It is factored computationally by cyclic
rotation, relator inversion, and permutation of the two coordinates.
Generator automorphisms and generalized quotient-conjugacy/ACM
replacements are not edges. In particular, an arbitrary equality modulo
the other relator is not inserted as one move.

The unordered representation requires no physical swap of relators:
one tracks which displayed word is the recipient. Every signed rotation
is realized by relator inversion and ordinary conjugation, and a product
is one ordinary multiplication with the appropriate orientation. These
normalizations preserve cyclic energy. Thus each enumerated edge lifts
to an actual ordinary path with the same cyclic energy bound.

Conversely, the next lemma ensures that *all* ordinary multiplications
under a cyclic energy cap are represented by a finite menu, even when
the actual words carry arbitrarily long independent conjugating tails.

## A self-contained axes lemma

Let u,v be nonempty cyclically reduced free words of lengths a,b. Take
arbitrary conjugates of u and v (signs can be absorbed into u,v).
Their product's cyclic word has one of these two forms:

1. A cyclic reduction of `u' v'`, where u',v' are cyclic rotations of u,v.
2. A cyclically reduced word `u' q v' q^-1`, with q freely reduced and
   nonempty. Its exact length is `a+b+2|q|`.

Here is a proof that also explains why long conjugating tails cause no
unbounded hidden cases. Use the Cayley graph of F(x,y), which is a tree
with directed edges labeled x,X,y,Y. A nonidentity element g acts by
left translation. If g=h u h^-1 with u cyclically reduced, its invariant
axis is the bi-infinite line obtained from the translates of the path
reading u; its translation length is |u|. Reading g from a vertex on
this axis gives a cyclic rotation of u. The same holds for the other
element and v.

If their axes meet, their intersection contains a vertex z. Conjugate
both elements by z^-1. Both resulting words are cyclically reduced,
with labels u',v'. Their product has cyclic representative obtained by
cyclically reducing u'v'. This is case 1, even if the product becomes
the identity or experiences extensive cancellation.

If the axes are disjoint, let the unique shortest joining path go from
a vertex z on the first axis to a vertex t on the second. Read its
nonempty reduced label as q. After simultaneous conjugation by z^-1,
the two elements have the forms u' and q v' q^-1. The first and last
edges of this bridge lie off the respective axes: otherwise the joining
path would not be shortest. Consequently none of the four junctions in
the cyclic word `u' q v' q^-1` cancels. At a bridge endpoint an axis edge
and an off-axis edge are distinct; inside each axis translation and the
bridge the words are already reduced. Thus the displayed word is
cyclically reduced, with length a+b+2|q|. This proves case 2 and the lemma.

This argument works for arbitrary powers, repeated words and arbitrary
relative conjugators; it does not assume that either word is primitive.

## The finite complete neighbor menu

Suppose the receiver has cyclic length a and the retained donor has
cyclic length b. Under the cap E<=C, a disjoint-axis product is possible
only if

    a+2b+2d <= C,       d=|q|>=1.

Therefore a complete menu is:

- all signed cyclic rotations u',v' with product u'v';
- all such rotations and all reduced q of lengths
  `1<=|q|<=floor((C-a-2b)/2)`, with product `u' q v' q^-1`.

Freely and cyclically reduce each resulting receiver, retain the donor,
and discard pairs whose cyclic energy exceeds C. Iterate for either
recipient coordinate. Every listed edge is legal ordinary AC; the axes
lemma proves there are no omitted multiplication edges under the cap.
All conjugation/inversion edges are already represented by the quotient
normalization.

For the rotation-only cap-18, cap-19 and cap-20 components, the exact
minimum of `E+min(cl(r0),cl(r1))+2` over the stored states is 21.
Thus no nonempty bridge can occur under those caps, and their rotation
menus are already complete. For cap 21 the full menu is used. Its
maximum required bridge length is one; only twenty oriented
source/recipient choices require nonempty bridge words. These controls
are checked from every stored state, not inferred from initial lengths.

## Finite results and resulting lower bound

All calculations start with the actual AK(3) tuple

    (xxxYYYY, xyxYXY).

| Cyclic cap | States modulo the stated symmetries | Minimum energy | Minimum coordinate length |
|---|---:|---:|---:|
| 18 | 2,128 | 13 | 6 |
| 19 | 20,024 | 13 | 5 |
| 20 | 39,840 | 13 | 5 |
| 21, full bridge menu | 144,292 | 13 | 5 |

The cap-21 histogram by cyclic energy is

    13:12, 14:40, 15:548, 16:572, 17:3108,
    18:3488, 19:17688, 20:18792, 21:100044.

The generator tests 103,553,312 signed rotation/bridge products, of which
5,544,208 stay within the cap. The separately written saved-state checker
verifies closure, actual canonical words, the start state, and connectivity.
It reproduces both counts exactly, including 13,824 positive-tail checks.
No stored boolean claiming completeness is trusted.

**Theorem (computer-assisted finite component):** any ordinary AK(3)
path to the standard tuple `(x,y)` must attain cyclic energy at
least **22**.
Indeed, the stored finite set contains the initial tuple and is closed
under every ordinary move under cap 21, while every stored tuple has
energy at least thirteen. A free basis reached as the standard tuple
`(x,y)` has energy two, so such a path must leave the cap.

This is a bound on cyclic energy. It strengthens the prior raw-energy
bound of 22 because cyclic energy is never larger than raw energy. It
does not assert that an arbitrary target free basis has energy two;
the lower bound concerns a complete path to the standard trivial tuple,
as required for ordinary AC triviality. One can alternatively continue
any basis by Nielsen operations, but no monotonicity assertion for that
continuation is needed here.

The finite coordinate scan finds no primitive word among the 99,546
distinct stored cyclic/inverse word classes. That scan uses M's shared
rank-two Whitehead routine and is separately labeled as such. The
minimum-energy closure argument alone proves the stated standard-basis
lower bound, without relying on this scan or on a global primitivity
criterion.

## Independent checks and positive control

The initial exploration and cap-18 generator were written in Python.
The later generator `cyclic_component.cpp` is standard C++17 and uses
literal free strings, without bit-packed raw-state checkpoints or any
quotient evaluator. The [independent cap-18/cap-20 Python checker](../experiments/audit_cyclic_component.py)
uses its own reduction and canonicalization code and checks connectivity;
the [cap-20 review](independent-cyclic-review.md) records 25,895,168
candidate checks. [P's cap-21 review](research-p-cyclic21-review.md) uses a
separately written [C++ checker](../experiments/verify_full_cyclic_component.cpp),
with independent word routines, and tests the full bridge menu. Its
[machine-readable result](../results/cyclic21_independent_review.json)
reproduces the counts above.

As a positive ordinary-AC control, the same Python cyclic-menu search
on AK(2) finds a strict path to `(x,y)` with

    46 strict moves, raw peak 18, cyclic peak 13.

The saved ledger `certificates/n_ak2_cyclic13.json` is replayed by the
repository's independent elementary verifier. Its conjugations are
single letters, multiplications are positive right multiplications, and
its endpoint is the exact free basis. It contains no ambient generator
changes or quotient deletions. This is a control on the algorithm and
strict expansion, not one of the requested AK(3)/general breakthroughs.

## Certificate and reproduction

The cap-21 certificate stores all 144,292 actual canonical word pairs,
as a JSON list compressed with gzip and base64. It decodes to 4,100,882
bytes; the ASCII file has 669,981 bytes including its final newline.
The compression is solely an artifact transport format.

```sh
c++ -std=c++17 -O3 experiments/cyclic_component.cpp -o /tmp/ac_cyclic
/tmp/ac_cyclic 21 /tmp/cyclic21.json /tmp/cyclic21_results.json 1000000 1

# Decode the published state certificate with the Python standard library.
python3 -c 'import base64,gzip,pathlib; p=pathlib.Path("certificates/cyclic21_component.json.gz.b64"); pathlib.Path("/tmp/cyclic21_saved.json").write_bytes(gzip.decompress(base64.b64decode(p.read_text())))'

# Independently audit every ordinary cyclic neighbor and connectivity.
python3 experiments/cyclic_catalogue_to_tsv.py certificates/cyclic21_component.json.gz.b64 /tmp/cyclic21.tsv
c++ -std=c++17 -O3 experiments/verify_full_cyclic_component.cpp -o /tmp/ac_cyclic_review
/tmp/ac_cyclic_review /tmp/cyclic21.tsv 21 /tmp/cyclic21_review.json

# Replay the exact positive control.
python3 experiments/elementary_verify.py certificates/n_ak2_cyclic13.json
```

The last numeric argument to the generator enables the full bridge menu.
State-budget exhaustion is explicitly reported as `INCOMPLETE` and is
not accepted as a closed component. The cap-19 exploratory Python run
stopped at a time limit and was never used as a completeness certificate;
the complete C++ set supersedes it. The final bound requires the axes
proof and an actual closed-set audit, rather than interpreting a bounded
failure as an unrestricted obstruction.

No finite cap can by itself prove non-AC-triviality. This report provides
no free-basis certificate for AK(3), no invariant under all unbounded
ordinary moves, and no proof or disproof of the full AC conjecture.
