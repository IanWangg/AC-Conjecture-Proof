# Research TH21 — BS(1,2)-type relators in AK(3)'s forward set to cap 29

**Result (negative, exact within its scope).** No state of Fwd(AK(3), 29) has a relator of
BS(1,2) type. Fwd(AK(3), 29) is AK(3)'s complete forward component to total length 29 in D's
cyclic-product graph, modulo Σ: 286,729,520 states, M's dump `m29_ak3_keys.bin`. BS(1,2) type
means that, up to conjugacy and inversion, the relator is an Aut(F₂)-image of XyxYY = x⁻¹yxy⁻².
So TH09's Theorem 1 ("a BS(1,2)-type relator in a balanced presentation of the trivial group
implies AC-trivial") cannot be applied to any state of this set. Every one of the 573,459,040
relators has Whitehead-minimal length ≥ 5, and every relator of minimal length 5 lies in the
trefoil orbit (xxYYY ~ xyxYXY).

## Data
- `scratchpad/agent-m/m29_ak3_keys.bin`: 2,293,836,160 bytes = 286,729,520 keys. Per
  research-m §3.3 this is Fwd(AK3, 29) (complete).
- `scratchpad/agent-m/m30_ak3_keys.bin`: 553,521,280 bytes = 69,190,160 keys. This is the
  barrier ≤ 28 part of M's incomplete cap-30 run, equal to D's complete cap-28 component
  (research-m §3.2, research-d §4.6). It was used as a quick first pass.
- Encoding: D's 64-bit Σ-key (`experiments/d_acsearch.cpp`, `encode_ordered` / `decode`;
  M's width-1 keys are identical, `experiments/m_acsearch.cpp`). The scanner copies D's
  routines.

## Method (`experiments/th21_bs12_scan.cpp`)
For every key, the scanner decodes the pair, checks it, and classifies both relators.
- **Checks.** Decoding must succeed, the total length must be ≤ cap, and re-encoding must
  return the same key (`key_of_pair(decode(k)) == k`). It also counts matches with the keys
  of AK(3) = (xxxYYYY, xyxYXY) and of its 8 signed-permutation images.
- **Exact test.** The cyclic word is Whitehead-reduced with x ↦ xy^{±1} and y ↦ yx^{±1}
  while its cyclic length strictly decreases. Up to inner automorphisms, which fix cyclic
  words, and signed permutations, which preserve length, these are all the rank-2 Whitehead
  automorphisms. By Whitehead's theorem the result has minimal length. The relator is
  accepted iff the minimal length is 5 and the minimal word, canonical under rotation and
  inversion, lies in S. S is the closure of XyxYY under signed permutations, rotation,
  inversion and length-preserving Whitehead moves (x ↦ y^{±1}x and y ↦ x^{±1}y included).
  By the second half of Whitehead's theorem, S is exactly the set of minimal words of the
  orbit: S = {xxYXy, xxyXY, xyyXY, xyXYY}. The same closure of xxYYY gives the 8 length-5
  words of the trefoil orbit, which splits the minimal-length-5 counts.
- **Cache.** A per-thread, direct-mapped cache (2²⁴ entries) is keyed by the exact packed
  word, so it cannot produce false matches. 2 threads; about 0.3 GB of memory by
  construction; the key file is streamed in 8 MB blocks.

## Validation
- `--selftest` (PASSED):
  - 200,000 random encode → decode → re-encode round trips.
  - 30,000 planted positives, all detected with 4 and with 8 maps: random Aut-images of
    XyxYY and XYxyy, of length 5–120, randomly rotated and inverted.
  - 15 negatives rejected with the expected minimal length, and so were 3,000 random
    Aut-images of each:
    - primitive: x, xy, xxy, xyxyY;
    - AK(3) relators: xyxYXY (min 5, trefoil class), xxxYYYY (min 7);
    - xxYYY (min 5);
    - BS(3,4): XyyyxYYYY (min 9); BS(1,3): XyxYYY; BS(2,3): XyyxYYY;
    - commutators xyXY and xxyyXXYY, XyxY, XYxyyy, xyyxYY.
  - On 100,000 random words, reduction with 4 maps and with 8 maps agree.
- Cross-check against TH09's own test, `experiments/th21_crosscheck.py`. TH09's test is
  `d_whitehead.aut_canon((w,)) == aut_canon((R_BS,))`, as in
  `th09_killers.forward_bs_scan`. The 3,957 words were random cyclically reduced words of
  length ≤ 14 and random Aut-images (length ≤ 16) of XyxYY, xyxYXY, xxYYY, XyxYYY, xxxYYYY
  and XyyxYYY. Both tests agree on the minimal length and the verdict for all of them; 638
  are positive.
- On the data, both files gave:
  - 0 decode failures, 0 round-trip failures and 0 states over the cap;
  - the AK(3) key `34c0000000012878` exactly once, and 8 matches for its 8
    signed-permutation images. The component is D8-closed, as research-l notes (8,650,489
    D8-classes against 69,190,160 Σ-states at cap 28, ratio 8.0).
  - The histogram has no minimal length 1. This agrees independently with D and M: no
    primitive relator.

## Commands (D = scratchpad/agent-th21, M = scratchpad/agent-m)
```
g++ -O2 -std=c++17 -pthread -o $D/th21_bs12_scan experiments/th21_bs12_scan.cpp
$D/th21_bs12_scan --selftest
python3 experiments/th21_crosscheck.py $D/th21_bs12_scan 4000
nice -n 5 timeout 1200 $D/th21_bs12_scan $M/m30_ak3_keys.bin 30 --threads 2   # 53 s
nice -n 5 timeout 1200 $D/th21_bs12_scan $M/m29_ak3_keys.bin 29 --threads 2   # 4 min 14 s
```
Outputs are in `$D/scan_m29.txt`, `$D/scan_m30.txt`, `$D/selftest.txt` and
`$D/crosscheck.txt`.

## Results
| file | states | relators | BS(1,2) hits | min-len 5 (all trefoil) | min-len 6 | min-len 7 |
|---|---|---|---|---|---|---|
| m30 (= Fwd(AK3, 28)) | 69,190,160 | 138,380,320 | **0** | 43,841,336 | 18,489,272 | 4,157,840 |
| m29 (= Fwd(AK3, 29)) | 286,729,520 | 573,459,040 | **0** | 196,167,568 | 72,984,856 | 10,902,748 |

Whitehead-minimal length histogram for cap 29. Counts are relator occurrences, two per
state. Minimal lengths 1–4 do not occur.
5:196,167,568 · 6:72,984,856 · 7:10,902,748 · 8:1,122,464 · 9:3,417,948 · 10:865,036 ·
11:879,232 · 12:305,356 · 13:777,212 · 14:589,396 · 15:1,544,492 · 16:1,134,512 ·
17:4,440,972 · 18:4,134,656 · 19:15,020,664 · 20:11,229,868 · 21:46,130,128 ·
22:37,632,840 · 23:106,804,372 · 24:57,374,720. The counts sum to 573,459,040.

## Meaning
This extends TH09's cap-20 check (39,840 states) to the full cap-29 forward set, about 7,200
times larger. The result is negative. It is a **bounded, directed, engine-relative
observation**:
- it covers only cyclic-product moves (D's graph), Σ-states and total length ≤ 29;
- BS(1,2)-type relators may still occur in AK(3)'s AC-class at larger total length, or
  after moves the cyclic-product graph does not reach under this cap;
- it is **not evidence that AK(3) is non-trivial**.

One by-product of this set: whenever a relator of AK(3)'s forward set is Whitehead-minimal
at length 5, it is trefoil-type. Its Aut-class is that of xyxYXY, AK(3)'s own second
relator, so the trefoil class is the only Aut-orbit of minimal length ≤ 5 that occurs in
this set.

## Coordinator's check (2026-11-09, Los Angeles time)

- The coordinator rebuilt `experiments/th21_bs12_scan.cpp` independently and re-ran `--selftest` (passed), `python3 experiments/th21_crosscheck.py <binary> 2000` (1,975 distinct words, all agree with TH09's own BS(1,2)-type test, 321 of them positive) and the full scan of `m30_ak3_keys.bin`: 69,190,160 states, 138,380,320 relators, **0 BS(1,2)-type hits**, 0 decode or round-trip failures, AK(3) present exactly once — identical to the agent's numbers. The larger cap-29 scan (286,729,520 states, 0 hits) was run by the agent only.
- Meaning, stated plainly: no state in AK(3)'s directed cyclic-product forward set up to total length 29 has a relator whose one-relator group is BS(1,2), so research-th09's BS(1,2) exit does not trivialize AK(3) within this bounded set. This is a bounded, directed, engine-relative observation, not evidence that AK(3) is non-trivial.
