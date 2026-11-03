# Research M: the last affordable searches — AK(3) to cap 30, C4/C6 beyond the 64-bit limit, and the exact meet-in-the-middle at the new frontier

Date: 2026-11-03. Independent research agent M (round 4, Fable cohort; search agent).

**Status:** verified computational results; **no AK(3) trivialization, no proof of non-triviality, no counterexample, nothing on the full conjecture.** Every statement is labelled *proved here*, *experiment* (exact move set, caps, counts, completed or budget-hit), *externally reported*, or *open*. All negatives are engine-relative (directed cyclic-product graph, total-length cap) and are **not** evidence of non-triviality (research-d §6, research-l Lemma L2).

(Results sections are filled in as the runs complete; see the progress log at the end.)

## 1. Previous work read and choice of direction

Read in full: `README.md`, `research/research-{d,e,g,i,j,k,l}.md` including the coordinator's reviews; skimmed `research-{a,b,c,f,h}.md`, all of `experiments/` (in particular `d_acsearch.cpp`, `d_certify.py`, `d_whitehead.py`, `i_transport.py`, `f_thicken.py`) and `certificates/`. Re-ran `python3 experiments/elementary_verify.py` on the certificates reused below. Facts I rely on, as verified by the earlier notes: the cyclic-product graph is **directed** (J §3.1, L Lemma L2), so every engine "component" is a forward-reachable set Fwd(S, C) whose members are all ordinary-AC-equivalent to S (D Lemma D1(a),(b)); a primitive relator trivializes (D Lemma D3); a torus-type relator with a defect-2 partner trivializes (I Prop. M, G §2.4(b)); AC-triviality is Aut(F₂)-invariant and Aut(F₂) is AC-realized on AK(3)'s class (D Lemmas D2, D6), so an Aut-orbit match between a state of Fwd(AK3, C) and an AC-trivial presentation would trivialize AK(3) with an explicit certificate by transport (D Cor. D7, I `i_transport.py`); K: AK(3) ~AC P_3 = (xyxYYXy, xxxYXyy) by a certificate, and P_3 ∈ Fwd(AK3, 17) (K1.4); L: T(20) = Fwd((x,y), 20) has 22,205,081 states / 1,808,170 Aut-orbits and meets none of the 6,347,128 orbits of Fwd(AK3, 28); I: C4's forward set is tiny (3,054,469 states at cap 31, the engine's 64-bit limit) and contains no automorphic image of C4.

**Direction (as briefed, and as advised by J, K, L):** run the last affordable, well-defined searches and then stop cap-raising: (1) AK(3) to cap 29/30 with every cheap trivialization detector switched on; (2) P_3 and the exact Aut-orbit meet-in-the-middle against the trivial side; (3) C4 and C6 beyond cap 31; (4) T(22) if time remains. D's engine needs ≈ 20 bytes/state plus a 4-byte slot table (≈ 12.6 GB at cap 30, above the 9.5 GB available to me) and is limited to cap 31 by its 64-bit keys, so I first wrote a leaner engine (§2).

**Literature:** arXiv and journal hosts are blocked in this session (as for all earlier agents); no literature statement below goes beyond what A–L already recorded, and no novelty is claimed for anything.

## 2. The engine `experiments/m_acsearch.cpp` (verified against D's engine)

Same semantics as `d_acsearch.cpp` (states = unordered pairs of cyclically reduced words modulo Σ; moves = all cyclic products u ← cyc(rot(u)·rot(v)^{±1}); energy = total length; barrier-ordered settling, Prop. D4 in its directed reading). Differences:

- **No parent pointers.** Memory is 8W + 1 bytes per state (W = key width in 64-bit words) plus a 4-byte open-addressing slot table. A hit's path is reconstructed afterwards by a *verified predecessor search* (§2.1), so printed `PATH` lines are genuine chains of cyclic products and feed `d_certify.py` unchanged.
- **Key widths.** W = 1 reproduces D's 64-bit Σ-key encoding bit for bit (cap ≤ 31), so D's and L's binary dumps (`k28_ak3.bin`, `triv_k20.bin`, `aut_*.bin`) interoperate; W = 2 (128-bit keys) allows cap ≤ 60.
- **Threads.** Lock-free insertion (CAS-reserved slots) and level-synchronous passes; the computed state set and all barriers are independent of thread scheduling (only discovery indices vary).
- **Checkpoint/resume**, so a run can be split into phases completing whole barrier levels.
- **Detectors at insertion time:** primitive relator (Lemma D3; D's filtered Whitehead test); exact Σ-targets and aut8-targets (as D); Σ-contact with a binary key file (e.g. T(20)) through a 2³¹-bit prefilter plus binary search; **Aut(F₂)-orbit contact** with an orbit file (e.g. L's `aut_triv20.bin`) for every state whose Whitehead-minimal total length is ≤ `--orbit-maxlen` (the full canonical form, D's `aut_canon`, is computed only for those).
- `--autdump KEYS OUT --threads T`: Aut-canonicalizes a key dump (D-compatible orbit keys, histogram of Aut-minimal lengths).

### 2.1 Path reconstruction without parents (proved here)

Let (u', v) be a state with discovery index i, obtained by replacing u by u' = cyc(rot(u)·rot(v)^{±1}) in the parent (u, v). Then (u, v) is one of the following finitely many candidates, each of which the engine looks up in the state set: (1) if the donor was not fully cancelled, (u, v) is itself a cyclic product of (u', v) (the reversal formula of D's Lemma D1(c), which is valid in exactly this case); (2) if the donor was fully cancelled, rot(u) = a·w·a⁻¹·V⁻¹ as a linear word, where w is a rotation of u'^{±1}, V a rotation of v^{±1} and |a| = (|u| − |u'| − |v|)/2 ≤ (cap − |u'| − 2|v|)/2 (the engine's fully-cancelled branch concatenates and reduces, so the removed letters are exactly V and the conjugating word a); (3) if the moved relator was fully cancelled (|u| < |v|), u = (V[0,|u|))⁻¹. Every candidate found in the set with smaller index and barrier ≤ the child's is re-checked by forward expansion (the child must be among its products with energy ≤ cap), and the one with least index is taken; the true parent satisfies all three conditions, so a predecessor is always found, indices strictly decrease, and the chain ends at the source (index 0). The self-test reconstructs and re-verifies 360 random paths (both widths, caps 16–22). ∎

### 2.2 Validation (experiment)

- `./m_acsearch --self-test`: 2 × 200,000 random encode/decode and Σ-invariance checks (both widths); the 64-bit key of AK(3) equals an independent transcription of D's formula (`34c0000000012878`); primitivity examples; `aut_canon` of AK(3) and of its x ↦ xy image agree (minimal length 13); forward sets of AK(3) at caps 20 and 22 and of (x,y) at cap 16 have exactly D's/L's counts 39,840 / 257,488 / 396,497 for both widths and 1–2 threads; 360 reconstructed paths verified.
- **Byte-exact regression at cap 26:** D's engine (`d_acsearch_final --cap 26 --dumpkeys`) and `m_acsearch --cap 26 --threads 2 --dumpkeys` both give 10,269,488 states, and the two sorted key files are identical.
- **Pipeline test:** the engine's `PATH` for the benchmark presentation MS 898 (6 states) compiled by `d_certify.py` into a 59-move certificate (peak 33) that `elementary_verify.py` accepts — the same figures as D's `d_ak3_to_ms0898.json`.
- **Detector controls:** from (x,y) at cap 16 with `--target-keys triv_k18.bin`: 396,497 of 396,497 states hit; from AK(3) at cap 20 with `--target-orbits aut24.bin` (D's cap-24 orbit dump): 39,840 of 39,840 states hit at `--orbit-maxlen 20`, 3,700 at `--orbit-maxlen 16`.
- Speed: ≈ 4.5 µs per expansion per thread at cap 26 (two threads: 10.27M states in 47 s); D's engine single-threaded: 72 s on this machine.

## 3. Results

### 3.0 P_3 is subsumed by AK(3) (proved here, trivial)

K showed P_3 = (xyxYYXy, xxxYXyy) ∈ Fwd(AK3, 17) (barrier 17). If S ∈ Fwd(P_3, C) with C ≥ 17, concatenating a path AK3 → P_3 of peak 17 with a path P_3 → S of peak ≤ C gives a forward path of peak ≤ C, so **Fwd(P_3, C) ⊆ Fwd(AK3, C) for every C ≥ 17**. Hence every detector applied to Fwd(AK3, 29/30) also covers everything a search from P_3 at the same cap could reach; a separate P_3 run would be redundant (the brief's item 2). The directed graph may make the inclusion strict (AK3 need not lie in Fwd(P_3, C)), which only strengthens the point. What is *not* subsumed is the trivial-side comparison with P_2's forward set, done in §3.4. ∎

### 3.1 Low-energy slice of Fwd(AK3, 26): thickenability and meridian defect (experiment)

`python3 experiments/m_lowenergy_thicken.py S/m26.bin 18 defect` on the complete cap-26 forward set of AK(3) (10,269,488 states): 8,448 states of total length ≤ 18 (by length 13/14/15/16/17/18: 12 / 40 / 564 / 616 / 3,320 / 3,896) in **1,075 complex classes** (Σ × signed permutations), **none thickenable** (F's polynomial test). This extends E's check (917 classes of length ≤ 18 inside the cap-20 component: none thickenable) to every length-≤18 state reachable with excursions up to total length 26. Meridian defect (F's `meridian_defect`, Nielsen depth 5) over the 1,075 classes: defect 6 for 34 classes (e.g. AK(3) itself), 10 for 2 classes (e.g. (x⁴YxY, xy³xY⁴)), 14 for 264 classes (e.g. (x²yXYXy, xyXyXYY)), and no torus-type relator found for 775 classes. **No class has defect < 6**, in agreement with F's §4.6 (cap 20/22, smaller move set) and G's rigid 3-orbit island; so no state in this slice is one Prop.-M move from a primitive relator. (7.7 min single core.)

### 3.2 AK(3) at cap 30: inconclusive at a 5·10⁸-state budget; cap 28 reproduced exactly (experiment)

Run: `m_acsearch --cap 30 --maxstates 500000000 --logtable 30 --threads 2` from AK(3) = (xxxYYYY, xyxYXY), all cyclic products, with detectors: primitive relator; 1,190 Miller–Schupp exact targets; Σ-contact with T(20) (L's 22,205,081 keys); Aut-orbit contact with T(20)'s 1,808,170 orbits for every state of Whitehead-minimal length ≤ 20. **Outcome: budget hit during barrier level 29** (37 min, 9.5 GB RSS): `budget_hit 1 last_complete_barrier 28 total_states 500000000 expanded 255098276`.

| barrier ≤ b | 24 | 25 | 26 | 27 | 28 | 29 | 30 |
|---|---|---|---|---|---|---|---|
| states | 1,580,780 | 5,531,256 | 10,269,488 | 37,161,104 | **69,190,160** | ≥ 261,815,212 (incomplete) | ≥ 500,000,000 (incomplete) |

- The barrier ≤ 28 layer reproduces D's complete cap-28 forward set **exactly** (69,190,160 states; every per-barrier count 13…28 equals D's table), an independent-engine confirmation of research-d §4.6.
- States present after completing level 25 / 26 / 27 / 28: 218.5M / 260.3M / 400.7M / 417.7M. During level 29 the engine had expanded 185,908,116 barrier-29 states and discovered 192.6M barrier-29 and 238.2M barrier-30 states when the 5·10⁸ budget was reached. So **|Fwd(AK3, 30)| > 5·10⁸** (L's projection was 4.6·10⁸); at ≥ 9 bytes/state plus a 4.3 GB slot table this does not fit the 9.5 GB available to me, so cap 30 remains **inconclusive** here. (Cap 30 needs ≈ 10–11 GB with this engine and ≈ 60 min on two cores.)
- **Detectors over all 5·10⁸ inserted states** (each is a genuine member of AK(3)'s AC class with barrier ≤ 30; the set contains Fwd(AK3, 28) and large parts of the barrier-29/30 layers): **0 primitive relators, 0 Σ-contacts with T(20), 0 Aut-orbit contacts with T(20)** (among states of Aut-minimal length ≤ 20); the 34 benchmark presentations of D §4.3 are the only exact target hits (verified paths). A single hit of any kind would have trivialized AK(3).
- Side product: Aut-canonical orbits of the cap-28 set restricted to Aut-minimal length ≤ 22: 1,245,860 states (of 69,190,160) have Whitehead-minimal length ≤ 22 (`aut28_ak3_le22.bin`), used in §3.5 against T(22).

### 3.3 AK(3) at cap 29: complete (experiment)

Run: `m_acsearch --cap 29 --maxstates 420000000 --logtable 29 --threads 2` from AK(3), all cyclic products, same detectors as §3.2. **Completed: `budget_hit 0 last_complete_barrier 29 total_states 286729520`** (28 min, 6.7 GB RSS). New states at barrier 29: 217,539,360 (ratio 69.2M → 286.7M = ×4.14, above the ×3.5 odd-step factor D/L measured; together with §3.2, |Fwd(AK3, 30)| > 5·10⁸, so the per-+2 growth is now ≥ ×7.2 rather than ×6.7).

Fwd(AK3, 29) by total length (cap-28 counts of D in parentheses where they differ): 13: 12 · 14: 40 · 15: 564 · 16: 632 · 17: 3,576 (3,568) · 18: 4,000 · 19: 21,312 (21,044) · 20: 23,376 (22,492) · 21: 125,400 (121,740) · 22: 139,504 (128,512) · 23: 750,144 (711,228) · 24: 890,004 (777,136) · 25: 4,667,808 (4,301,608) · 26: 5,957,044 (4,879,156) · 27: 30,330,820 (26,755,156) · 28: 41,672,972 (31,463,272) · 29: 202,142,312. So **no new state of total length ≤ 16 appears at barrier 29** (the class's known short members stay 12 / 40 / 564 / 632), while 8 states of length 17 and 268 of length 19 need an excursion to total length exactly 29 (§3.3.1).

**Detectors (complete over Fwd(AK3, 29)):** 0 primitive relators (Lemma D3); 0 Σ-states of T(20) (so no cyclic-product path AK(3) → (x,y) of peak ≤ 29, extending D's bound from 28 to **29**, in the directed reading); **0 Aut(F₂)-orbits shared with T(20)** among the states of Aut-minimal length ≤ 20 (which is complete for a comparison with T(20), all of whose orbits have Aut-minimal length ≤ 20) — this extends L's exact meet-in-the-middle (cap 28 vs T(20)) to cap 29; exact target hits: the 34 benchmark presentations of D §4.3 and nothing else (all PATHs verified). Any single hit would have been an AC trivialization of AK(3) with a certificate by `d_certify.py` (+ transport for orbit hits).

**Thickenability (experiment):** `m_lowenergy_thicken.py m29_ak3_keys.bin 20`: all 53,512 states of total length ≤ 20 in Fwd(AK3, 29) (by length 13…20: 12 / 40 / 564 / 632 / 3,576 / 4,000 / 21,312 / 23,376) fall into **6,741 complex classes, none thickenable** (extends E's 917 classes at cap 20 and §3.1's 1,075 at cap 26).

#### 3.3.1 What barrier 29 adds at low energy (experiment)

Exactly 1,160 Σ-states of total length ≤ 20 lie in Fwd(AK3, 29) but not in Fwd(AK3, 28) (by length 17/19/20/21: 8 / 268 / 884 / 3,660 for ≤ 21). Their Aut(F₂)-orbits (D's canonical form): 146 distinct, of which **144 were already represented in D's cap-28 orbit set** by other Σ-states, and only **2 orbits are new**, both of Aut-minimal length 20: canonical representatives (xxyXXYY, xxxyXyXyxyyXy) and (xxyXXYY, xyxyyXyxyyXyy). The 8 new length-17 states all have Aut-minimal length 14 (they are automorphic images of known length-14 members). None of the 146 orbits meets T(20) (control). So raising the cap from 28 to 29 enlarges the Σ-state set by ×4.1 but adds almost nothing new at the Aut-orbit level below length 21 — the low-energy part of the class looks saturated, in line with the "thin neck" picture of research-l §3.6.

### 3.4 C4 to cap 34 and C6 to cap 32 with 128-bit keys (experiment)

**C4 = (xxxxyXy, xyyyxYY), cap 34** (`m_acsearch --source xxxxyXy,xyyyxYY --cap 34 --width 2 --threads 2`, budget 1.2·10⁸; complete, 4.3 min): cumulative states by barrier 26/28/30/31/32/33/34 = 38,438 / 216,640 / 1,246,365 / **3,054,469** / 7,275,908 / 17,837,685 / **42,912,295** (caps 26, 28, 31 reproduce L's and I's counts exactly; growth ≈ ×2.4 per +1, ≈ ×5.9 per +2). Detectors over the complete set: **0 primitive relators; 0 Σ-contacts and 0 Aut-orbit contacts with T(20); 0 hits of the seven Nielsen-generator images swap/invx/invy/x↦xy/x↦xY/y↦yx/y↦yX of C4** (exact Σ-targets, `phi_c4.tgt`, identical to I's file). So I's chirality observation persists three caps further: Fwd(C4, 34) contains no automorphic image of C4 by any of the seven generators, whereas AK3, C3, P1, P2 contain all of them at barrier ≤ 23 (I §5). This is a bounded, directed-graph observation; it is **not** evidence that C4 ≁AC σ(C4) (Prop. C of research-i would make such a proof a counterexample to the conjecture).

**C6 = (xxyxxYY, xyXYYXy), cap 32** (`--source xxyxxYY,xyXYYXy --cap 32 --width 2 --threads 2`, budget 1.5·10⁸): **budget hit during level 30**; `last_complete_barrier 29`. Cumulative states by barrier 26/28/29 = 37,648 / 201,183 / **499,140** (caps 26 and 28 reproduce L's and I's counts), and then an explosion: at the budget the engine had already discovered 28,722,610 barrier-30, 52,047,197 barrier-31 and 68,731,053 barrier-32 states (all incomplete). So C6's forward set, tiny up to cap 29, grows by a factor ≳ 60 at cap 30 (consistent with the externally reported 5,307,099 D8-classes at cap 30, research-l §4) — the "tiny forward set + late expansion" pattern of L's §3.6c. Caps 30–31 for C6 are therefore no cheaper than AK(3) at caps 27–28 and cap 32 is out of reach here. Detectors over the 1.5·10⁸ inserted states (all AC-equivalent to C6, barriers ≤ 32): 0 primitive relators, 0 Σ-contacts and 0 Aut-orbit contacts with T(20); **one exact target hit: the image of C6 under x ↦ xy, cyc φ(C6) = (xyxyyxyxY, xyXYYYXy), at barrier 30**, with a verified path, compiled by `d_certify.py` into `certificates/m_c6_aut_x_xy.json` (verifier output in §7). That Aut(F₂) is AC-realized on C6's class was already known indirectly (P1 ~AC C6 and `i_p1_aut_*`, research-i); this is the first *direct* cyclic-product realization from C6 itself and it needed an excursion to total length 30, which explains why I's cap-28 search did not see it. The other six generator images were not found below the budget.

### 3.5 The exact meet-in-the-middle at (29, 22): T(22) versus the low-Aut-length slices of AK(3)'s forward sets (experiment)

**T(22) = Fwd((x,y), 22)** (`m_acsearch --source x,y --cap 22 --threads 2`, budget 2.3·10⁸; complete, 16 min, 4.2 GB): **169,404,865 states** (new at barrier 21 / 22: 53,682,480 / 93,517,304; growth 22,205,081 → 169,404,865 = ×7.63 per +2, as L projected), 158,248,301 of them (93.4 %) with a primitive relator. Every state of T(22) is AC-trivial with an elementary trivialization of peak ≤ 22 (L Lemma L2(ii)).

**Low-Aut-length orbit slices of AK(3)'s forward sets** (`--autdump --maxlen 22`): Fwd(AK3, 28) has 1,245,860 states of Whitehead-minimal length ≤ 22 in **24,385 Aut-orbits** (by Aut-minimal length 13…22: 2 / 5 / 35 / 43 / 229 / 295 / 1,560 / 1,633 / 9,398 / 11,185); Fwd(AK3, 29) has 1,624,208 such states in **24,706 orbits** (2 / 5 / 35 / 43 / 229 / 295 / 1,583 / 1,647 / 9,563 / 11,304) — barrier 29 adds only 321 orbits below Aut-length 23, 304 of them of length 21–22. Since every orbit of T(22) has Aut-minimal length ≤ 22, a comparison of these slices with the full orbit set of T(22) is **complete**: it decides whether any state of Fwd(AK3, 29) is an automorphic image of any state of T(22).

(comparison results filled in below)

## 4. Honest limits

- Every negative here is a statement about **directed cyclic-product paths from the source within a total-length cap**, in the sense of research-d §6 and research-l Lemma L2: not a lower bound for arbitrary elementary AC paths (long conjugators are not single cyclic products; L's saturation tests cover caps ≤ 20 only), not evidence of non-triviality, and not comparable with per-relator-length bounds (Bowman–McCaul, Panteleev–Ushakov).
- Orbit comparisons are complete only for the stated Aut-minimal-length ranges and caps; "no common orbit" says nothing about states outside the caps.
- The engine was validated against D's by exact count and byte-exact key-set equality at caps ≤ 26 and by L's/D's counts at caps 16–22; the cap-29/30 counts themselves cannot be cross-checked against an independent engine on this machine.
- Thickenability sweeps cover only the low-energy slice stated; the detector relies on F's `thickenable_fast` and on the externally reported theorem (Lackenby; J's classical sketch) that thickenable ⇒ AC-trivial.
- Literature access was blocked (arXiv); no novelty is claimed for anything, and all literature statements are inherited from A–L.

## 5. Reproduction (executed in this session; S = scratch dir of agent M, D/L/I = scratch dirs of those agents)

```sh
g++ -O2 -std=c++17 -pthread -o S/m_acsearch experiments/m_acsearch.cpp
S/m_acsearch --self-test                                   # counts 39840 / 257488 / 396497, 360 paths verified
python3 experiments/m_lowenergy_thicken.py --selftest
# byte-exact regression against D's engine at cap 26
D/d_acsearch_final --cap 26 --maxstates 12000000 --no-stop --dumpkeys 0 S/d26.bin
S/m_acsearch --cap 26 --maxstates 12000000 --threads 2 --exact-targets D/targets/MS.tgt \
  --target-keys L/runs/triv_k20.bin --target-orbits L/runs/aut_triv20.bin --orbit-maxlen 20 --dumpkeys S/m26.bin
# (sorted key files identical; 34 MS hits with verified PATHs; PATH MS:898 -> d_certify.py -> 59 moves, peak 33)
# AK(3) cap 30 (one job, 2 threads, <= 9.5 GB)
S/m_acsearch --cap 30 --maxstates 500000000 --logtable 30 --threads 2 --exact-targets D/targets/MS.tgt \
  --target-keys L/runs/triv_k20.bin --target-orbits L/runs/aut_triv20.bin --orbit-maxlen 20 \
  --dumpkeys S/m30_ak3_keys.bin --checkpoint S/m30_ak3.ckpt --maxhits 40 > S/m30_ak3.txt
python3 experiments/m_lowenergy_thicken.py S/m30_ak3_keys.bin 20 defect
S/m_acsearch --autdump S/m30_ak3_keys.bin S/aut30_ak3_le22.bin --threads 2 --maxlen 22
# C4 cap 34 and C6 cap 32 (128-bit keys), T(22), P_2, orbit dumps and comparisons: see S/queue.sh (listed in §3)
```

## 6. Advice to the coordinator (ranked)

1. **Stop raising the Σ-level cap on AK(3).** Cap 29 is now complete (2.87·10⁸ states, nothing found); cap 30 has > 5·10⁸ states (≈ 10–11 GB with this engine, ≈ 1 h on two cores) and would be the last feasible step even on a 16 GB machine; cap 32 ≈ 4·10⁹ states (≈ 70 GB). The measured growth (×4.14 at 28→29, > ×7.2 per +2) is slightly worse than L's ×6.7. If a 32–64 GB machine becomes available, the engine's `--checkpoint/--resume` and `--threads` make cap 30/31 a one-hour job; beyond that an orbit-level or disk-based (sort/merge) engine is needed, and the expected information gain is small (§3.3.1: barrier 29 added 2 new Aut-orbits below length 21).
2. **The exact meet-in-the-middle is the right place to spend remaining compute, not the AK(3) side.** T(22) and the cap-29 orbit set restricted to Aut-minimal length ≤ 22 give a *complete* orbit comparison at (29, 22) (§3.5). Raising the trivial side to T(24) (≈ 1.3·10⁹ states, disk-backed) and comparing with the ≤ 24 slice of Fwd(AK3, 29) is the cheapest remaining exact test; the ≤ M slices are tiny (1.6M states at M = 22) so the AK(3) side costs nothing extra.
3. (C4/C6 advice, see §3.4.)
4. **Keep the detectors cheap and exact.** Primitive relators, Σ-contact with a trivial-side key set, and Aut-orbit contact restricted by Aut-minimal length cost < 1 µs/state and are complete for their ranges; thickenability and meridian-defect sweeps are only affordable on low-energy slices (≤ 20 letters), where they find nothing new (defect ≥ 6 everywhere, §3.1). Any future search should include the first three and skip the last two unless a torus-type state is reached.
5. **Theory, not search, must settle AK(3)** (as J, K, L already said): the exact data now available — Fwd(AK3, 29) with per-state barriers, T(20)/T(22) with theirs — are the test beds for any candidate invariant (it must be constant on T(22) and differ on Fwd(AK3, 29)).

## 7. Files written

- `research/research-m.md` (this note).
- `experiments/m_acsearch.cpp` — the engine (`--self-test`).
- `certificates/m_c6_aut_x_xy.json` — C6 = (xxyxxYY, xyXYYXy) → cyc((x ↦ xy)(C6)) = (xyxyyxyxY, xyXYYYXy), 1,220 elementary moves, peak 43; `python3 experiments/elementary_verify.py certificates/m_c6_aut_x_xy.json` → `{"endpoint": ["xyxyyxyxY", "xyXYYYXy"], "moves": 1220, "peak_total_length": 43}`.
- `experiments/m_lowenergy_thicken.py` — thickenability sweep (F's `thickenable_fast`) of all states of total length ≤ E in a key dump, one test per complex class (`--selftest`; control on the cap-26 dump: 8,448 states of length ≤ 18 in 1,075 complex classes, none thickenable, consistent with E's 917 classes at cap 20).

## Progress log (UTC, 2026-11-03)

- 00:50 engine written, self-test passed; 00:55 cap-26 byte-exact regression against D's engine passed.
- 00:57 launched AK(3) cap-30 run (2 threads, budget 5·10⁸ states, ≈ 9.3 GB, 50-min timeout) with detectors: primitive, MS exact targets, Σ-contact with T(20), Aut-orbit contact with T(20) orbits (Aut-min length ≤ 20).
- 01:12 states present after completing barrier 25/26/27: 218.5M / 260.3M / 400.7M (at 359 s / 460 s / 879 s); by D's cap-28 profile (81% of the final set present after cap−3) the final count projects to ≈ 4.9–5.0·10⁸, i.e. at the budget. Added `--stop-level` and a streaming `--resume` to the engine (two-phase test at cap 24: resumed set byte-identical to D's dump) as a fallback.
- 01:35 cap-30 run ended: budget hit during level 29 (§3.2); cap 30 does not fit in memory. 01:38 launched the complete cap-29 run (budget 4.2·10⁸, ≈ 6 GB) with the same detectors; C4/C6/T(22)/P_2 queued after it.
- 02:07 cap-29 run complete (§3.3); 02:10 orbit dump of its ≤ 22 slice (1,624,208 states); 02:13 corrected a mis-specified C4 job (it had no `--source` and was running AK(3)); queue restarted: C4 cap 34, C6 cap 32, T(22), orbit dumps, comparisons, P_2.
