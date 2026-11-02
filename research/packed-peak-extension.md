# Packed elementary search: AK(3) raw peak at least 22

Date: 2026-11-02. Coordinating-agent continuation of Research D. Status:
completed finite exclusion with an independent closed-set audit. **No
trivialization or counterexample is proved. No novelty claim is made.**

## Objective and prior work

Research D completely classified the component through raw total length 18
and left cap 19 incomplete. A/F concern a different, cyclic length; E/G/H
give paths in deletion quotients, with nontrivial free lifts. Here the aim
was to cross the explicitly unresolved raw boundary and look for an actual
free-group path, including primitive-relator shortcuts. The original target
remains a complete ordinary AC trivialization or global obstruction.

## Checked conclusions

In the full raw freely reduced elementary graph, the AK(3) component under
total length cap **21** contains **27,380,372** states after quotienting only
by individual relator inversions and relator permutation. No state has
total length below 13. No individual relator in any of these states is
primitive in F(x,y).

Thus any ordinary AC trivialization must reach raw total relator length
**at least 22**. In fact, a path must cross that bound before it can first
reach a tuple containing a primitive free-group relator. This is a finite
peak exclusion, not a global AC invariant. It does not give a cyclic peak
bound of 22 or imply non-AC-triviality.

Completed component counts:

| Cap | States | Minimum raw total length |
|---:|---:|---:|
| 18 | 251,874 | 13 |
| 19 | 2,951,248 | 13 |
| 20 | 6,426,432 | 13 |
| 21 | 27,380,372 | 13 |

The cap-18 count and every energy count agree with D's independent earlier
implementations. At cap 21 the energy histogram is:

| Total length | States |
|---:|---:|
| 13 | 504 |
| 14 | 1,928 |
| 15 | 31,976 |
| 16 | 43,044 |
| 17 | 340,000 |
| 18 | 434,512 |
| 19 | 2,792,936 |
| 20 | 3,368,920 |
| 21 | 20,366,552 |

## Exact graph and compact representation

The underlying moves are inversion, positive right multiplication, and
conjugation by x,X,y,Y. Words are always freely reduced; conjugating tails
are retained. No cyclic reduction, free-group automorphism, quotient
identity, or GS substitution restriction is used to identify search states.

Inversions and permutations form a length-preserving finite orbit. To
generate its full quotient graph, products of both orientations of the
recipient and both orientations of the donor are emitted for each
coordinate. All four signed-generator conjugations are emitted as well.
The proof of coverage is the same orbit argument as D; using both
recipient signs is essential. Primitive inversions and permutations are
already absorbed by the orbit representation. Signed donor multiplication
expands into donor inversion, positive multiplication, and restoration,
without changing its raw peak.

The new C++ implementation stores a letter in two bits and a pair in a
single 64-bit integer, including its two lengths. At the supported caps no
encoding is truncated. Canonicalization chooses inverse orientations by
numeric packed order and then sorts by length and numeric value; this
differs from D's lexicographic choice but represents the same orbits.
An exact open-addressed set stores keys; hash collisions are resolved by
full-key equality. Parent indices and edge codes permit path extraction.

An arbitrary-word conjugation can be refined peak-preservingly into signed
generator conjugations: remove the source conjugating tail, rotate its
cyclic core, and grow the target tail. Therefore the exclusion also covers
ordinary AC definitions allowing arbitrary conjugating words in one move.

## Independent closed-set certificate audit

The independent `verify_packed_closure.cpp` does not trust the BFS queue,
parent pointers, hash table, or packed multiplication. It reads the saved
list of states and uses separately implemented **string** inversion,
concatenation, free reduction and normalization. It checks:

1. Every listed key decodes to a valid freely reduced canonical pair under
   the cap, and all keys are distinct.
2. The exact starting tuple is present.
3. Every permitted neighboring orbit under the cap belongs to the list.
4. Every listed state has total length at least 13.

These checks alone prove exclusion: any capped path from the starting
tuple stays in a closed set that excludes the standard basis. They do not
require trusting the assertion that BFS visited every reachable state.
The checker additionally confirms unimodular exponent matrices.

The cap-21 audit passed for all **27,380,372** states and **112,696,624**
allowed-neighbor checks, with exactly the displayed energy histogram.
The earlier cap-20 audit also passed independently.

## Primitive-relator audit

The state list contains 2,018,904 distinct stored raw relator words,
representing 99,546 cyclic/inverse orbits. The smallest individual raw
relator length is five. Exact rank-two Whitehead minimization found **zero
primitive relators**.

The test cyclically reduces a word and repeatedly applies any of the eight
signed left/right Nielsen generator changes that strictly decrease cyclic
length. The remaining rank-two Whitehead operations are signed
permutations or inner conjugations, which do not lower cyclic length.
Whitehead minimization therefore reaches length one exactly for primitive
words. These automorphisms are used only to test a property of individual
words; they are not extra edges in the search graph. The primary background
is Clay–Conant–Ramasubramanian, [Whitehead graphs and separability in rank
two](https://msp.org/involve/2014/7-4/involve-v7-n4-p01-p.pdf), Sections 3–4.

Besides explicit primitive and nonprimitive controls, the scanner exhausts
all cyclically reduced words of lengths 1 through 9 in its self-test. It
matches the primitive census: four at length one, and 4 L phi(L) otherwise.
This census follows from primitive conjugacy uniqueness for each coprime
abelianization vector: at L>1 there are 4 phi(L) such cyclic conjugacy
classes and each has L rotations. All controls pass.

## Positive certificate and continuation controls

AK(2) at cap 12 again has 335 orbit states and no target. At cap 13 the
packed search reaches the basis. The extracted path compiles to **101
strict elementary moves**, independently replayed to exactly `(x,y)` with
expanded raw peak **23**. Its orbit path has cap 13; expanding normalizing
swaps into strict primitives raises that peak. We make no strict-peak-13
claim for this particular compiled certificate. The positive control tests
path extraction and move compilation rather than merely a negative search.

Budget-limited runs save the entire queue, parent array, edge array, and
processed index. Resuming reconstructs the exact membership set and
continues at the saved queue position. A small interrupt/resume control
reproduces the cap-18 census. Cap 21 stopped at 20,000,001 discoveries, then
resumed the same checkpoint and completed at 27,380,372. It was not restarted
after an observation timeout. Checkpoint replacement uses a temporary file
and rename after a successful write.

## Reproduction

From the repository root, with a C++17 compiler:

```sh
c++ -std=c++17 -O3 experiments/packed_peak_search.cpp -o /tmp/ac_packed
c++ -std=c++17 -O3 experiments/verify_packed_closure.cpp -o /tmp/ac_closure
c++ -std=c++17 -O3 experiments/scan_primitive_relators.cpp -o /tmp/ac_primitives
/tmp/ac_packed 3 21 20000000 /tmp/ac_cap21.bin
/tmp/ac_packed 3 21 40000000 /tmp/ac_cap21.bin resume
/tmp/ac_closure /tmp/ac_cap21.bin
/tmp/ac_primitives --selftest
/tmp/ac_primitives /tmp/ac_cap21.bin
python3 experiments/elementary_verify.py certificates/packed_ak2_certificate.json
```

The generated cap-21 checkpoint is about 356 MB; the searches and audits
also need memory for their state sets. Checkpoints are native binary work
files, not portable proof-assistant objects. They are regenerated by the
commands rather than committed as large repository files. Compact JSON
counts and audit outputs are in `results/packed_peak_extension.json`.
The standalone `packed_path_certificate.py` compiles a saved result's
`best_path` field to the strict verifier's format.

This investigation found neither a free-group trivialization nor a
primitive-relator shortcut. Cap 22 and all unbounded paths remain outside
the exclusion. The full objective is still unachieved.
