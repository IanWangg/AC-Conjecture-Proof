# Independent review of the packed cap-21 and primitive audits

Reviewer: research agent J. Date: 2026-11-02.

**Finding:** no mathematical or code defect was found that invalidates the
reported completed cap-21 exclusion or its absence of primitive relators.
This was a source-and-record review with a small census replay, not a
second run of the 27-million-state jobs. It does not establish AK(3)
non-AC-triviality.

## Material inspected

I read the complete sources `packed_peak_search.cpp`,
`verify_packed_closure.cpp`, `scan_primitive_relators.cpp`, and the report
`packed-peak-extension.md`. I also read the three stored cap-21 result
records. Those records consistently give 27,380,372 states, complete
processing and closure, minimum total length 13, and 112,696,624 allowed
neighbor checks. The scanner records 2,018,904 stored raw relator words,
99,546 cyclic/inverse orbits, and zero primitive words.

The reviewed source SHA-256 values are:

| File | SHA-256 |
|---|---|
| `packed_peak_search.cpp` | `438a1bcedcd9c329c373fa971c6d2e1c21d48cbe36f1f9816e8a664897cbaeec` |
| `verify_packed_closure.cpp` | `dcaa296640ac4ad40bf5c406af1661607153b9c8daa339d18d8eb289c3ed8d90` |
| `scan_primitive_relators.cpp` | `5a10e4a7104ad8cbe7e4378c177e6e45b525755a6ac297ac1363b2cbafa54c46` |
| `packed-peak-extension.md` | `c7df2110c169da4478c15966d18e4090bfbbcab023e5b77e8b2ff041c816ea78` |

## Checks of the mathematical coverage

- **Packing is injective at the supported caps.** Each letter occupies two
  bits. At cap 21 the payload occupies at most 42 bits, and at the maximum
  supported cap 25 at most 50. The two five-bit length fields occupy bits
  54–58 and 59–63. They do not overlap the payload. All reached temporary
  multiplication words have length at most the current pair's total
  length; a generator conjugation can add only two letters. The code's
  temporary-word and state limits therefore suffice. The hash table tests
  full keys and resolves collisions by probing.
- **The orbit generator covers the full raw graph.** Inversion and
  permutation preserve lengths. Products from both recipient signs and
  both donor signs cover primitive multiplications from every orbit
  representative; using a negative recipient also supplies the otherwise
  omitted left-product orbits. Conjugating a negative recipient gives the
  inverse of the corresponding positive-recipient conjugate, so the four
  signed conjugators emitted on a positive representative suffice. The
  donor's inverse orientation is immaterial after canonicalization.
- **The closure checker suffices without trusting BFS parents.** It
  independently uses string operations, checks canonical validity and
  uniqueness, includes the start, and checks every allowed capped
  successor. A set with these properties and minimum total length 13
  contains every capped path from the start and excludes the basis. Even
  if a closed list had extra unreachable states, this lower-bound argument
  would remain valid.
- **The primitive test has the required rank-two coverage.** A type-two
  Whitehead automorphism fixes its multiplier. With only one other
  generator, its choices are identity, left multiplication, right
  multiplication, or conjugation by that multiplier. The conjugation is
  an inner automorphism of the whole rank-two group and preserves cyclic
  length. Type-one signed permutations also preserve length. Thus the
  eight signed left/right Nielsen maps in the scanner contain every
  possible cyclic length decrease. Whitehead minimization implies that a
  primitive word of cyclic length greater than one has such a decrease;
  any chosen decrease preserves primitivity. Reaching length one is
  therefore equivalent to being primitive. See the primary background in
  [Clay–Conant–Ramasubramanian, Sections 3–4](https://msp.org/involve/2014/7-4/involve-v7-n4-p01-p.pdf).

Cyclic reduction, cyclic rotation and inversion are used only in the
individual-word property cache; they are not added as identifications of
the search graph. Since primitivity is invariant under those operations,
the cache does not omit a potentially primitive raw word.

## Executed small check

I reran `scan_primitive_relators --selftest`. It passed its exhaustive
cyclically reduced word census through length nine: four primitive words
at length one and `4 L phi(L)` at each larger tested length. I did not
rerun the large BFS, closure, or whole-checkpoint scan. Their numerical
outputs were inspected as recorded evidence rather than independently
recomputed in this review.

## Minor robustness observations

These do not affect the reviewed completed cap-21 result:

1. The primitive scanner accepts a checkpoint without requiring
   `processed == count`, and does not itself repeat the closure checker's
   per-state length/canonical validation. Thus its output alone must not
   be interpreted as a full-component claim for an incomplete or malformed
   checkpoint. The reported run is tied to the independently audited
   complete state list. Adding these guards would make standalone use
   clearer.
2. On resume, the producer initializes `minimum_processed_length` from
   all saved discovered states, including those not yet processed. The
   field name is consequently slightly broader than its value in a
   partial resumed run. Completed runs process all states, so their
   minimum and the independent checker's minimum are unaffected.

The supported conclusion remains the stated finite one: any ordinary
AK(3) trivialization must exceed raw total length 21, and must do so
before reaching a primitive relator. No claim about unbounded paths or a
cyclic length bound of 22 follows.
