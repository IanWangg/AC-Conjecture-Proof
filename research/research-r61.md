# Research R6-1 — BS(1,2)-type relators in the frontier classes' forward sets

**Result (negative, exact within its scope).** The nine forward sets below have 64,555,150
states in all. None of them has a state with a BS(1,2)-type relator. BS(1,2) type means that,
up to conjugacy and inversion, the relator is an Aut(F₂)-image of XyxYY = x⁻¹yxy⁻². So
research-th09 Theorem 1 cannot be applied to any state of these sets, and this scan trivializes
no frontier class. Every state of a forward set is AC-equivalent to its source, so a single hit
would have proved that class AC-trivial. There was none.

## What was scanned

Scratch root `S = /tmp/claude-0/-home-user-AC-Conjecture-Proof/2793adeb-4b51-5217-aae5-371faac65e22/scratchpad`.
Outputs are in `S/agent-r61/out_*.txt`.

| key file | source (class) | cap | states | relators | BS(1,2) hits | decode / round-trip fails | min-length-5 relators: BS(1,2) / trefoil | time |
|---|---|---|---|---|---|---|---|---|
| agent-i/k28_c4.bin | C4 = (xxxxyXy, xyyyxYY) | 28 | 216,640 | 433,280 | **0** | 0 / 0 | 0 / 0 | 0.7 s |
| agent-i/k28_c6.bin | C6 = (xxyxxYY, xyXYYXy) | 28 | 201,183 | 402,366 | **0** | 0 / 0 | 0 / 147,994 | 0.4 s |
| agent-i/k28_t475.bin | Y = T(4;7,5) | 28 | 136,468 | 272,936 | **0** | 0 / 0 | 0 / 6,751 | 0.2 s |
| agent-i/k_L2a.bin | (x⁷y¹³, xxyXy) | 28 | 93,202 | 186,404 | **0** | 0 / 0 | 0 / 93,202 | 0.3 s |
| agent-i/k_L2b.bin | (x⁷y¹⁵, xxyXy) | 28 | 10,706 | 21,412 | **0** | 0 / 0 | 0 / 10,706 | 0.1 s |
| agent-d/k28_ms2a.bin | MS #1 = (XyyxYYY, XXXYxxy) | 28 | 5,445,188 | 10,890,376 | **0** | 0 / 0 | 0 / 15,108 | 5.9 s |
| agent-d/k28_ms2b.bin | MS #2 = (XyyxYYY, XXXYxxY) | 28 | 15,040,328 | 30,080,656 | **0** | 0 / 0 | 0 / 10,192 | 13.9 s |
| agent-m/kc4_34.bin (128-bit) | C4 | 34 | 42,912,295 | 85,824,590 | **0** | 0 / 0 | 0 / 0 | 44.7 s |
| agent-m/kc6_32.bin (128-bit) | C6 (M dumped barrier ≤ 29 only) | 29 | 499,140 | 998,280 | **0** | 0 / 0 | 0 / 352,476 | 0.7 s |

Sources and caps:
- **L2a, L2b.** Sources and cap 28 come from `S/agent-i/L2a_run.txt`, `L2b_run.txt` (`level2.sh`); each run is complete to barrier 28.
- **MS(2) holdouts.** The sources are MS(2, x⁻²y⁻¹x²y) and MS(2, x⁻²y⁻¹x²y⁻¹), research-d §4.4 and §4.6; their state counts match research-d's table. The brief identifies them with research-i's P1 and P2.
- **kc6_32.** M's run `S/agent-m/c6_32.txt` dumped only barrier ≤ 29 ("dumped 499140 keys (barrier <= 29, width 2)"). So the effective cap is 29, and no state exceeds it.

In every file the "total length over cap" count is 0 and every scan reports `COMPLETE`. A
"forward set" is the source's component under the engine's moves, with every intermediate total
length ≤ cap, taken modulo the engine's symmetries.

## Method and validation

- **64-bit files.** Scanned with TH21's exact scanner `experiments/th21_bs12_scan.cpp`, unchanged. The method is greedy Whitehead reduction to the minimal cyclic length, followed by membership of the length-5 minimal word in the Aut-orbit closure of XyxYY. Whitehead's theorem makes the test exact. `--selftest` passed: 30,000 planted positives, negatives and their random images, a 4-map versus 8-map check, and AK(3).
- **128-bit files.** Scanned with the new `experiments/r61_scan128.cpp`, which is TH21's scanner with four changes. Its classification code is untouched.
  1. It reads agent M's width-2 keys with `decode2`/`key2_of_pair`, copied in logic from `m_acsearch.cpp` `encode_ordered_w`/`decode_w`. M's `canon_word` and `cmpw` are identical to D's.
  2. The relator cache is keyed by the full word, two 64-bit words for n ≤ 61. TH21's 64-bit `wkey` holds only n ≤ 29, and its 5-bit length field in the cache only ml ≤ 31. Both would be unsafe at cap 34.
  3. `--probe W1 W2` counts exact-key occurrences of a known state.
  4. Selftest part 0: a width-2 round trip on 292,449 random pairs (T ≤ 60), and agreement with width-1 decoding on 234,038 pairs (T ≤ 28).
- **Encoding check on real data.** The `--selftest` passes. Each source state occurs exactly once in its file (`probe_exact_key_occurrences 1`), and decode and round-trip failures are 0 on all 43.4M keys.
- **Cache check.** On kc6_32, the run with `--nocache 1` gives output identical to the cached run, apart from the cache counter.

## Side observations (exact counts, same runs)

- **Length-5 relators.** Every relator of Whitehead-minimal length 5 in all nine sets lies in the trefoil orbit (xxYYY ~ xyxYXY ~ xxyXy). This matches TH21's finding for AK(3) at cap 29.
- **L2a and L2b.** The number of trefoil-orbit relator occurrences equals the number of states, 93,202 and 10,706. The source relator xxyXy is itself trefoil type.
- **C4.** At caps 28 and 34, no relator has Whitehead-minimal length < 7. At cap 34, 42,088,672 relator occurrences have minimal length 7, roughly one per state.
- **MS #1 and MS #2.** Many relators have minimal length 6: 327,344 and 6,911,480 occurrences respectively. Their type was not classified here.

Full histograms are in the `out_*.txt` files.

## Meaning

This is a **bounded, directed observation**. Within these caps no state is AC-trivial by the
BS(1,2) criterion of TH09. It is **not** evidence that any class is non-trivial, for two reasons:
- a trivialization may pass through longer states;
- BS(1,2) type is only one sufficient criterion. Other Baumslag–Solitar types, e.g. BS(1,3) with relator XyxYYY of minimal length 6, are not covered by TH09 Theorem 1 as stated.

## Commands (run from the repository root; `S` as above)

```
g++ -O2 -std=c++17 -pthread -o $S/agent-r61/scan    experiments/th21_bs12_scan.cpp
g++ -O2 -std=c++17 -pthread -o $S/agent-r61/scan128 experiments/r61_scan128.cpp
$S/agent-r61/scan --selftest ; $S/agent-r61/scan128 --selftest          # both: SELFTEST PASSED
for f in agent-i/k28_c4 agent-i/k28_c6 agent-i/k28_t475 agent-i/k_L2a agent-i/k_L2b agent-d/k28_ms2a agent-d/k28_ms2b; do
  nice -n 5 timeout 600 $S/agent-r61/scan $S/$f.bin 28 --threads 2; done
nice -n 5 timeout 600 $S/agent-r61/scan128 $S/agent-m/kc4_34.bin 34 --threads 2 --probe xxxxyXy xyyyxYY
nice -n 5 timeout 600 $S/agent-r61/scan128 $S/agent-m/kc6_32.bin 29 --threads 2 --probe xxyxxYY xyXYYXy [--nocache 1]
```
Wall time was about 70 s in all, on 2 threads.

## Coordinator's check (2026-11-09, Los Angeles time)

- Rebuilt `experiments/r61_scan128.cpp` and re-ran `--selftest`: passed. Independently re-ran TH21's 64-bit scanner on `k28_c4.bin`, `k28_c6.bin`, `k28_t475.bin`: 216,640 / 201,183 / 136,468 states, **0 BS(1,2)-type hits**, 0 decode, round-trip or over-cap failures — identical to this note. The other six files were scanned by the agent only.
- (The agent's remark that `experiments/r61_scan128.cpp` was "already tracked" refers to the coordinator's automatic checkpoint commit of its own in-progress version, not to a pre-existing file; nothing of anyone else's was overwritten.)
- Meaning: research-th09's BS(1,2) exit does not resolve any of the frontier classes C4, C6 (= P1), Y = T(4;7,5), the two MS(2) holdouts P1, P2, or the T(2;·) level-2 classes within these bounded, directed forward sets. Not evidence of non-triviality.
