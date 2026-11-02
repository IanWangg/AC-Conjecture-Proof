# Independent review of L's next-central diagnostic

Reviewer: research agent M. Date: 2026-11-02.

**Finding:** no flaw was found in the claimed path-specific nonzero
next-central classes. An independently implemented degree-two tensor
calculation, using a different genuine Schreier free basis, reproduced
**every recorded coefficient**, not only the support sizes and norms.
This review does not establish a global AC invariant or decide AK(3).

## Material and exact replay

I reviewed L's `second_central_audit.py`, the corresponding section of
`research-l.md`, `second_central_results.json`, and the optimized
first-order certificate. I replayed the original audit. It reported:

| Residual | L's Schreier length | Coinvariant support | l1 norm |
|---|---:|---:|---:|
| r0 X | 166 | 67 | 322 |
| r1 Y | 472 | 148 | 469 |

I also ran the coordinating agent's strict elementary verifier on the
fully expanded 533-move free ledger. It reached exactly the saved free
endpoint, of coordinate lengths **635 and 1,867**, at raw peak **2,502**.
The endpoint is not the free basis.

The reviewed SHA-256 values are:

| File | SHA-256 |
|---|---|
| `second_central_audit.py` | `ee22a82b18798e3b5f7210cf3929cbed5b83e1025952adde33822d0fca1a1080` |
| `second_central_results.json` | `30b2bf37a4986a54009622140d03e564d51a885aa7dbc97d23b2089b718d8f1c` |
| `optimized_first_order.json.gz.b64` | `c57f756e367fec54881a269874fc205a64a375c4f880986b87029abbdaff750b` |
| `optimized_first_order_strict.json` | `0d195a1cc1a8dda57f1785c724ea7b27a49d6eaa60ea4e5aa90c7c257b767fd9` |
| M's `review_second_central.py` | `367b4b84d46614bbc0599d724855e77557174e3c7c82cb9b9d251cf236e0b700` |

## Why the mathematical target is the stated quotient

Let N be the normal closure of the braid relator in F2 and let N'=[N,N].
The covering graph for N is the Cayley graph of B=F2/N. A spanning tree
gives a genuine free basis of N: each positive non-tree edge g--c-->h
gives the loop word `t_g c t_h^-1`, and the reversed edge gives its inverse.
This is stronger than choosing arbitrary conjugates of the braid relator
as though those were a free basis. Such arbitrary lifts need not be free.

The shortlex tree used by L is prefix-closed. Its finite portion contains
all vertices needed for the two residual paths and all their tree paths.
It can be extended to a full spanning tree of the infinite Cayley graph.
Hence its nonempty edge loops really are members of a Schreier free basis.
The explicit free-word reconstructions and zero exponent sums in every
used Schreier generator also pass. In particular, the input errors are in
N', not merely undetected by one chosen approximate coordinate.

For a free group N with abelianization A, commutator collection gives

    N'/[N,N'] = exterior-square A.

The conjugation action of N is trivial on this quotient. The remaining
F2 action therefore factors through B, so taking B coinvariants gives

    N'/[F2,N'] = (exterior-square A)_B.

I's earlier graded Fox proof identifies A with the regular integral
module Z[B]. The diagonal B action sends `e_g wedge e_h` to
`e_(ag) wedge e_(ah)`. Its orbit is determined by `g^-1 h`, with inversion
of that relative element reversing the sign. B3 has no nonidentity
order-two elements, so there are no self-inverse relative elements
producing extra two-torsion. This also follows directly from E's exact
description: an order-two element has exponent sum zero, whereas a
nontrivial order-two image in C2*C3 is conjugate to S and has exponent
sum congruent to three modulo six. An element with trivial free-product
image is a central power with exponent sum 6k, which forces the identity
in the remaining case. One representative of each inverse pair
therefore gives exactly the free abelian coordinate system used in L's
calculation. No additional relations between different relative pairs
are being omitted.

L's streaming exterior-area formula has the correct factor of two for a
word with zero Schreier abelianization. The commutator control fixes its
orientation. My independent calculation below avoids that factor-of-two
formula altogether.

## A different free basis and a different calculation

The independent script `review_second_central.py` does **not** import L's
audit implementation. It shares only the previously checked exact B3
normal-form and Fox-module arithmetic from I; that shared dependency is
recorded explicitly in its output.

I changed the breadth-first letter order from `xXyY` to `yYxX`, thereby
choosing a different Schreier transversal. I checked literal prefix
closure, constructed all actual loop words, and reconstructed each free
residual exactly from them. The alternate tree uses **31** nonempty free
basis generators, rather than L's 34. Their Fox module coefficient vectors
have rank 31 modulo 101. This rank is a consistency check, not the reason
they are a free basis: their basis status follows from the spanning-tree
construction.

I then computed degree-two Magnus tensors in those actual Schreier basis
symbols. A positive symbol contributes `1+X_i`; its inverse contributes
`1-X_i+X_i^2`. If the current abelian vector is A, multiplication by a
signed symbol updates the degree-two tensor by `A tensor (+/- e_i)`, with
the extra `e_i tensor e_i` term for an inverse symbol. Both final abelian
vectors vanish; the resulting tensors are antisymmetric with zero
diagonal. Their upper-triangle coefficients therefore give the genuine
commutator class without dividing an exterior-area sum by two.

Mapping those basic commutators through their Fox vectors into the
relative-element coinvariant basis produced:

| Residual | Alternate Schreier length | Tensor support | Coinvariant support | l1 norm |
|---|---:|---:|---:|---:|
| r0 X | 122 | 154 | 67 | 322 |
| r1 Y | 350 | 166 | 148 | 469 |

All coinvariant coefficients agree with L's saved data exactly. The change
of tree and Schreier word lengths, while leaving the final classes
unchanged, is a useful check that the result is not an artifact of one
chosen generator list. An independent commutator tensor control confirms
the sign convention.

The alternate exact tree has depth eleven and 22,579 vertices, covering
the same 105 required prefix vertices. This is a finite part of an
infinite-group calculation, not a finite quotient or a capped replacement
of B3.

## Reproduce

With the scripts together in `experiments/`, the reviewed L artifact names
give the command:

```sh
python3 experiments/review_second_central.py \
  certificates/optimized_first_order.json.gz.b64 \
  results/second_central_results.json \
  --strict certificates/optimized_first_order_strict.json \
  --output results/second_central_independent_review.json
```

The script accepts alternate paths if the publication names differ. It
uses the Python standard library and the earlier `first_order_correction.py`,
`braid_relation_module.py`, and strict `elementary_verify.py`.

## Supported scope

The two actual first-order residuals have nonzero images in
`N'/[F2,N']`; they do not already vanish in the next central quotient.
Conjugations by words from N' alone act trivially on that central kernel
and cannot remove these particular nonzero classes. This blocks the
stated automatic continuation of this path.

It does not show that another AC path has the same defects, nor that
ordinary AC moves cannot change them. These coordinates are not asserted
to be global invariants. The free-group objective remains unresolved.
