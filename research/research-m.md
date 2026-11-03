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

(further results filled in below as runs complete)

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

(see end)

## 7. Files written

- `research/research-m.md` (this note).
- `experiments/m_acsearch.cpp` — the engine (`--self-test`).
- `experiments/m_lowenergy_thicken.py` — thickenability sweep (F's `thickenable_fast`) of all states of total length ≤ E in a key dump, one test per complex class (`--selftest`; control on the cap-26 dump: 8,448 states of length ≤ 18 in 1,075 complex classes, none thickenable, consistent with E's 917 classes at cap 20).

## Progress log (UTC, 2026-11-03)

- 00:50 engine written, self-test passed; 00:55 cap-26 byte-exact regression against D's engine passed.
- 00:57 launched AK(3) cap-30 run (2 threads, budget 5·10⁸ states, ≈ 9.3 GB, 50-min timeout) with detectors: primitive, MS exact targets, Σ-contact with T(20), Aut-orbit contact with T(20) orbits (Aut-min length ≤ 20).
- 01:12 states present after completing barrier 25/26/27: 218.5M / 260.3M / 400.7M (at 359 s / 460 s / 879 s); by D's cap-28 profile (81% of the final set present after cap−3) the final count projects to ≈ 4.9–5.0·10⁸, i.e. at the budget. Added `--stop-level` and a streaming `--resume` to the engine (two-phase test at cap 24: resumed set byte-identical to D's dump) as a fallback.
