# Research E: AC distances along a residual chain of finite 2-groups, exhaustive peak bounds, and thickenability of the AK(3) class

Date: 2026-11-02. Independent research agent E (round 2).

**Status:** obstruction-side partial results. **No proof that AK(3) is or is not AC-trivial, and no counterexample.** Proved here: (i) AK(3) is AC-trivial if and only if its AC distances along one explicit chain of finite 2-groups (equivalently, along the free-nilpotent quotients) are bounded, with an explicit stabilization class; (ii) no simple quotient, and no quotient of either one-relator group F/<<x^3y^-4>> or B_3 = F/<<xyxY XY>>, can carry an AC obstruction for AK(3). Exhaustive computations (finite, exact, reproducible) give: every trivialization of AK(3) by the 15 standard instructions has **at least 15 instructions**, and **passes through a pair of total freely reduced length at least 21**. AK(3), AK(2), MS(3) and all 145 complex classes of total length at most 16 in the explored AC class of AK(3) are **not thickenable**, so Lackenby's 2026 theorem on thickenable presentations does not apply to any of them. Novelty is not established for any item.

## 1. Previous work read, and choice of direction

I read `README.md`, `research/research-{a,b,c}.md`, every file in `experiments/` and `certificates/` (as of the start of this round), and re-ran the round-1 artifacts. All of them pass: `verify_plateau.py` (A's equality classification), `quotient_certificates.py` (B: 12-move class-2 path, 48-move class-3 path, distances 2/3/4 in S3/S4/A5), `elementary_verify.py --selftest`, and both MS(3)→AK(3) certificates (C: 32 strict moves, peak 23). The round-1 summary given to me is accurate.

**Literature check (limited).** In this session WebFetch could not reach arxiv.org, projecteuclid.org or the Havas web page (DNS blocked), so I relied on web-search snippets plus memory. I found no source claiming that AK(3) is AC-trivial or not AC-trivial; it is still described as open. Relevant pointers I checked at snippet level:

- Lackenby, arXiv:2606.06122 (2026). Its abstract, as reported by search, says that thickenable balanced presentations of the trivial group satisfy the stable AC conjecture with an explicit move bound, *and also the unstable AC conjecture*. Thickenable means the presentation complex embeds in a 3-manifold. I have not read the full text. This motivated Section 6.
- Bobtcheva–Quinn, math/0012212 and Fund. Math. 188 (2005). Quantum 2-complex invariants depend only on homology when χ ≥ 1, so they cannot detect AC counterexamples.
- Borovik–Lubotzky–Myasnikov (arXiv:1103.1295) and Guyot (arXiv:1612.06912): no single finite or f.g. soluble quotient obstructs (B's Section 1).
- Shehper et al., arXiv:2408.15332 (NeurIPS 2025); Lisitsa, arXiv:2501.18601 and the correction at doi:10.1016/j.jaca.2025.100041 (search did not surface the correction text; per the README it withdraws the stable AK(3) claim's basis); Panteleev–Ushakov, arXiv:1609.00325; Carreras, arXiv:2607.23611; Bridson, arXiv:1504.04187; Myropolska, arXiv:1304.2668; Havas–Ramsay, IJAC 13 (2003); Bowman–McCaul, Exp. Math. 15 (2006); Myasnikov–Myasnikov–Shpilrain (Contemp. Math. 296, 2002). The older BFS papers study length-bounded AC graphs with related but differently normalized move sets and length measures. They may contain bounds comparable to or stronger than Section 5; I could not read their full texts here.

**Direction.** B proved that AK(3) is non-trivial iff finite-quotient distances are unbounded (a supremum over *all* finite quotients), and suggested looking for a family with provable growth. I chose the obstruction side.

1. Replace "all finite quotients" by **one explicit residual chain**, with a stabilization bound.
2. Compute **exact** distances along the chain for AK(3) against the known-trivial AK(2) and AK(1). This tests whether the chain shows any signal.
3. Prove that broad classes of quotients cannot obstruct.
4. Add two exhaustive, certificate-relevant computations: a lower bound on instruction count, and a lower bound on peak length (the quantity `elementary_verify.py` reports).
5. Test thickenability, the hypothesis of Lackenby's theorem, across the explored AC class.

This differs from D (constructive search) and F (other families). Item 5 also gives D a cheap filter.

## 2. Conventions

F = F(x,y), with X = x^-1 and Y = y^-1. A pair U = (u0,u1) is "trivial" when U = (x,y). The **15 instructions** are B's alphabet, numbered as in the code:

| id | instruction | id | instruction |
|---|---|---|---|
| 0, 1 | invert u0 or u1 | 2 | swap |
| 3, 4 | u0 ← u0 u1^{±1} | 5, 6 | u1 ← u1 u0^{±1} |
| 7–10 | u0 ← g^-1 u0 g, g = x, X, y, Y | 11–14 | u1 ← g^-1 u1 g |

All words are freely reduced after every instruction. The set is closed under inverses, so the move graph is undirected. For a quotient π: F → Q, the same instructions act on Q × Q (with g replaced by π(g)), and d_Q(U) is the graph distance from π(U) to π(x,y) (∞ if there is none). d_F is the distance in F.

**Fact 0 (proved).** d_F(U) < ∞ iff U is ordinary-AC-trivial, because:
- each instruction is an ordinary AC move;
- every ordinary move (inversion; u_i ← u_i u_j^{±1}; left multiplication, which is a right multiplication followed by a conjugation; conjugation by any word; permutation) is a composite of instructions;
- each `ordinary-ac-elementary-v1` primitive is *one* instruction: `conjugate(i,g)` = u_i ← g u_i g^-1 is the instruction with conjugator g^-1.

Hence an elementary-v1 certificate of length N gives d_F ≤ N. Moreover, its intermediate states are states of an instruction path, so every lower bound below also binds every certificate in the repository's format.

**Fact 1 (proved).** If π factors through π', then d_Q ≤ d_{Q'} ≤ d_F, because instructions commute with homomorphisms. Also d_Q < ∞ iff π(U) is AC-equivalent to π(x,y) in Q, with conjugation by arbitrary elements of Q (generator conjugations generate those).

## 3. Theorems on residual chains (proved here)

**Theorem 1 (monotone convergence along a residual chain).** Let F ⊇ K_1 ⊇ K_2 ⊇ … be normal subgroups with ∩K_c = 1, and Q_c = F/K_c. Then, in ℕ ∪ {∞},

    d_{Q_1}(U) ≤ d_{Q_2}(U) ≤ … ≤ d_F(U)   and   sup_c d_{Q_c}(U) = d_F(U).

If d_F(U) < ∞, then d_{Q_c}(U) = d_F(U) for all large c.

*Proof.* Monotonicity follows from Fact 1. Take L < d_F(U). There are finitely many instruction sequences p of length ≤ L. Each has p(U) ≠ (x,y), so some coordinate ratio w_p = p(U)_i t_i^-1 (with t = (x,y)) is a nontrivial element of F. Since the K_c are nested with trivial intersection, w_p ∉ K_c for every c ≥ c(p). Instructions commute with π_c, so for c ≥ max_p c(p) no sequence of length ≤ L reaches π_c(x,y), and d_{Q_c} > L. ∎

This is B's residual-finiteness argument, but it needs only one fixed nested chain, with no products of quotients. The next lemma supplies explicit chains and a rate.

**Lemma 2 (syllable detection by Magnus expansions).** Let w = g_1^{a_1} ⋯ g_m^{a_m} ≠ 1 be reduced, with g_j alternating between x and y and a_j ≠ 0. Let μ be the Magnus map x ↦ 1+X, y ↦ 1+Y into the noncommutative power series ring, and write Z_j for the variable of g_j.

- (a) Over ℤ, the coefficient of the monomial Z_1 Z_2 ⋯ Z_m in μ(w) is ∏ a_j ≠ 0.
- (b) Over 𝔽_p, write a_j = p^{k_j} u_j with p ∤ u_j. The coefficient of Z_1^{p^{k_1}} ⋯ Z_m^{p^{k_m}} is ≡ ∏ u_j ≢ 0 (mod p).

Consequently, the truncation of μ at degree c (over ℤ, or over 𝔽_p) is ≠ 1 whenever c ≥ |w|.

*Proof.* A term of μ(w) picks Z_j^{e_j} from (1+Z_j)^{a_j} for each j. The target monomial has exactly m maximal blocks, alternating between the two variables. If some e_j = 0, its neighbours (same variable) merge, or a block disappears at the end, leaving fewer than m blocks. So every e_j > 0, and block-by-block matching forces e_j = 1 in (a), or e_j = p^{k_j} in (b). The contribution is unique.

- In (a) it is ∏ binom(a_j, 1) = ∏ a_j.
- In (b), (1+Z)^{p^k u} ≡ (1 + Z^{p^k})^u (mod p). As a power series this has coefficient u at Z^{p^k}, also for u < 0.

Finally, the degrees m and Σ p^{k_j} are at most Σ|a_j| = |w|. ∎

**Theorem 3 (two explicit chains, with a stabilization class).** Let N_c = F/γ_{c+1}(F). By Magnus's theorem, γ_{c+1}(F) is exactly the kernel of the degree-c integral truncation. Let P_c^{(p)} be the image of F in the unit group of 𝔽_p⟨X,Y⟩/(degree > c). P_c^{(p)} is a **finite p-group**: it lies in 1 + I, where I is the nilpotent augmentation ideal, and |1+I| = p^{2^{c+1}−2}.

Both families are residual chains, by Lemma 2. If d_F(U) = D < ∞ and ℓ is the total length of U, then

    d_{N_c}(U) = d_{P_c^{(p)}}(U) = D   for every c ≥ 2^{D−1}(ℓ+2) − 1.

*Proof.* Let ℓ_r be the maximal total length after r instructions. Inversions and swap preserve it, a multiplication at most doubles it, and a conjugation adds at most 2. So ℓ_r + 2 ≤ 2(ℓ_{r−1} + 2), giving ℓ_r ≤ 2^r(ℓ+2) − 2.

For a sequence p of length r ≤ D−1, the nontrivial ratio w_p has length at most ℓ_{D−1} + 1 ≤ 2^{D−1}(ℓ+2) − 1. By Lemma 2, w_p survives in N_c and in P_c^{(p)} for c at least that length. Hence d ≥ D, and Fact 1 gives d ≤ D. ∎

**Corollary 4.** For AK(3), and for every balanced presentation U of the trivial group on x, y, the following are equivalent:

- U is ordinary-AC-trivial;
- sup_c d_{N_c}(U) < ∞;
- sup_c d_{P_c^{(2)}}(U) < ∞, over explicit finite 2-groups.

Every individual term is finite. For N_c this is Guyot's theorem; for P_c it is BLM, since the exponent matrix of U is unimodular. For AK(3) it is also verified below by explicit paths for small c. So **a proof that AK(3) is not AC-trivial is exactly a proof that its AC distances in the finite 2-groups P_c^{(2)} are unbounded.** Any non-triviality is invisible in every single nilpotent quotient; if present, it lives purely in the growth rate.

## 4. Quotients that cannot obstruct (proved here)

**Proposition 5.** Let π: F → Q be onto, and let U normally generate F. Suppose that

- (a) some pair AC-equivalent to U has a coordinate s with <<π(s)>> = Q, and
- (b) some primitive element p of F has <<π(p)>> = Q.

Then d_Q(U) < ∞.

*Proof.* Fix the coordinate s. The other coordinate a can be changed into a·n for any n ∈ <<π(s)>>. Inductively, if a·n is reachable, then conjugating by h^-1, multiplying by π(s)^{±1} and conjugating by h gives a·n·(π(s)^{±1})^h. So a can be made π(p). Fixing π(p), the coordinate holding π(s) can likewise be made π(q), where (p,q) is a basis of F. Finally, the image of (p,q) is reached from π(x,y) by Nielsen moves, which are composites of instructions. ∎

**Corollaries.**

1. **Every simple quotient Q of F, finite or infinite, gives d_Q(U) < ∞.** One of π(u0), π(u1) is nontrivial, and so is one of π(x), π(y), and in a simple group any nontrivial element normally generates.
2. **Every quotient of T = F/<<x^3Y^4>> or of B_3 = F/<<xyxYXY>> gives d_Q(AK(3)) < ∞.** In such a Q one relator dies, so the other normally generates Q. Also xY normally generates T (x = y and x^3 = y^4 force x = 1), and x normally generates B_3.

   Corollary 2 covers C_3 * C_4 and PSL(2,ℤ) ≅ C_2 * C_3, which A used, as well as SL(2,ℤ), Burau and Jones images of B_3, and triangle-group quotients of T. Such quotients can give length or plateau information (as in A), never an invariant.
3. Representation-scheme invariants are trivially useless. For any group functor G, the functor A ↦ {g ∈ G(A)^2 : u_i(g) = 1} equals Hom(1, G(A)), the same as for the standard pair (folklore, a remark).

Together with BLM, Guyot and Bobtcheva–Quinn, these say that an obstruction quotient must be infinite, non-soluble, and not simple, and that no coordinate of any pair in the AC orbit of AK(3) can have a normally generating image.

## 5. Experiments (exact, exhaustive, with stated bounds)

The code is standard-library C++17 and Python 3.13. Every statement below is either an exact BFS distance or a lower bound certified by Lemma 6. Runs used one core and at most about 3.5 GB.

**Lemma 6 (bidirectional BFS certificate; proved).** In an undirected graph, suppose the balls of radii r_A about the start and r_B about the target are complete and disjoint. Then the distance is at least r_A + r_B + 1. *Proof:* on a path of length d ≤ r_A + r_B, the vertex at distance min(r_A, d) from the start lies in both balls. ∎

When one more layer produces an intersection, the distance is exactly r_A + r_B + 1, and the program reconstructs and length-checks a path.

### 5.1 Free-group AC distance (`e_acdist --mode free`)

| pair | radii completed (start, target) | states | peak RSS | result |
|---|---|---:|---:|---|
| AK(1) = (xYY, xyxYXY) | — | 20,999 | — | d_F = 8 exactly |
| AK(2) = (xxYYY, xyxYXY) | 7, 7 | 14,902,360 | not recorded | d_F ≥ 15 |
| **AK(3)** | 7, 7 | 14,961,127 | 2.3 GB | **d_F ≥ 15** |

For AK(3), the layer sizes are 1, 15, 159, 1534, 14269, 130372, 1180094, 10630928 from the start, and 1, 11, 87, 631, 4774, 37940, 312637, 2647674 from the target.

**Consequence (proved by exhaustive computation).** Every ordinary AC trivialization of AK(3) uses at least 15 instructions, and every `ordinary-ac-elementary-v1` certificate for AK(3) → (x,y) has at least 15 moves. B's quotient bound was 4 (A5). The abelianization bound N_1 below is 5.

### 5.2 Exact distances along the chains (`e_acdist --mode nil --class c [--mod 2]`)

Integral classes (N_c = F/γ_{c+1}). All values are exact except those marked ≥ (state cap reached; Lemma 6 bound).

| pair (total length) | c=1 | c=2 | c=3 | c=4 | c=5 | free |
|---|---:|---:|---:|---:|---:|---:|
| AK(1) (9) | 3 | 3 | 6 | 6 | 8 | 8 |
| AK(2) (11), trivial | 4 | 5 | 9 | 9 | ≥14 | ≥15 |
| **AK(3) (13)** | **5** | **6** | **10** | **11** | **≥14** | **≥15** |
| MS(3) (14), ~AK(3) | 4 | 7 | 9 | 13 | ≥14 | — |
| AK(4) (15) | 6 | 8 | 11 | ≥14 | ≥14 | — |

AK(1) also gives 8 at c = 6 and c = 7; it stabilizes at its free distance from c = 5 on, as Theorem 1 predicts (the theorem's crude class bound is 1407).

Finite 2-groups P_c^{(2)} (coefficients mod 2):

| pair | c=1 | 2 | 3 | 4 | 5 | 6 |
|---|---:|---:|---:|---:|---:|---:|
| AK(1) | 1 | 3 | 5 | 6 | 8 | 8 |
| AK(2) | 2 | 4 | 5 | 8 | 8 | 12 |
| **AK(3)** | 1 | 3 | 5 | 9 | 11 | ≥13 |
| MS(3) | 1 | 4 | 4 | 6 | 9 | 11 |

**Exact optimal quotient certificates for AK(3)** (`certificates/e_ak3_quotient_paths.json`, quotient-only):

- 6 instructions reach (x,y) mod γ_3 (B's path used 12);
- 10 reach it mod γ_4 (B's used 48);
- 11 reach it mod γ_5.

These lengths are minimal in the 15-instruction alphabet. Replayed on free words, the endpoints have lengths (41,23), (53,21) and (79,31): they are **not** (x,y) in F.

**Observations (experiment).**

1. AK(3)'s profile 5, 6, 10, 11 differs from that of the *known-trivial* AK(2) (4, 5, 9, 9) by at most 2 through class 4, and both are ≥ 14 at class 5. The chain gives no low-class signal distinguishing them.
2. At class 5, the radius-6 BFS layer of AK(3) has 1,179,999 states, versus 1,180,094 in F (0.008% collapse). In the feasible radius range the chain is therefore no cheaper than free search. Corollary 4 can only be used through a *uniform-in-c* argument, not by computation.
3. MS(3) and AK(3) are AC-equivalent (C), so their distances differ by at most 32 in every quotient; the data are consistent.

### 5.3 Peak total length (`e_peak`, exhaustive component enumeration)

G_L is the finite graph of ordered pairs of freely reduced words with total length ≤ L, with the 15 instructions as edges, restricted to G_L. It is undirected, and BFS enumerates the whole connected component.

| L | AK(3) component size | contains (x,y)? | min total length | AK(2) | trivial component (from AK(1)) |
|---:|---:|:---:|---:|---|---:|
| 13 | 336 | no | 13 | **reaches (x,y)** (depth 19) | 6,476,104 |
| 14 | 336 | no | 13 | | 14,399,816 |
| 15 | 13,728 | no | 13 | | 58,487,624 |
| 16 | 20,560 | no | 13 | | — |
| 17 | 857,808 | no | 13 | | — |
| 18 | 2,014,992 | no | 13 | | — |
| 19 | 23,609,984 | no | 13 | | — |
| **20** | **51,411,456** | **no** | 13 | | — |

AK(2)'s components are 240 states at L = 11 and 2,680 at L = 12, neither containing (x,y). AK(1) reaches (x,y) already at L = 9.

**Consequence (proved by exhaustive computation).** Every instruction path from AK(3) to (x,y), and in particular every `ordinary-ac-elementary-v1` certificate (whose `peak_total_length` is exactly this measure), **passes through a pair of total length ≥ 21**.

This complements A's bound, which concerns cyclic length (≥ 14) for the more general ACM moves. The two are not directly comparable.

Calibration: AK(2) is trivial with peak exactly 13 = |AK(2)| + 2. The certificate `certificates/e_ak2_peak13_trivialization.json` has 28 elementary moves and peak 13, and passes `elementary_verify.py`. Its source is a shortest 19-instruction path inside G_13, and G_12 contains no such path.

Two consistency checks:

- At L = 13 the AK(3) component is exactly 2·14·12 = 336 pairs (Orb(p_3) × Orb(b), both orders). This is half of the upper bound from A's theorem; the Orb(q_3) half needs quotient-conjugacy moves and first appears at L = 15.
- For L ≤ 20 the component contains 4,032 pairs of total length 13. Up to symmetry they form 2 complexes: AK(3) itself and **(x^-2 y^-2 x y, x^-3 y x y^-2)** ("XXYYxy, XXXyxYY").

### 5.4 Thickenability (`e_thicken`, Section 6)

| tested | result |
|---|---|
| AK(1), AK(2), AK(3), MS(3) | none thickenable |
| all pairs of total length ≤ 16 in AK(3)'s G_20 component: 597,600 pairs → 145 complex classes (by length 13/14/15/16: 2/5/66/72) | 140 classes tested exhaustively: **none thickenable** |
| the remaining 5 classes (extreme degree imbalance, 87,091,200 parity-admissible rotation systems each), run separately | **none thickenable** |

So **all 145 complex classes of total length ≤ 16 in the explored class are non-thickenable.**

## 6. The thickenability criterion (proved here in outline; classical)

For a one-vertex complex K = K⟨x,y | r_1, r_2⟩, a regular neighbourhood in a 3-manifold is a 0-handle, two 1-handles and two 2-handles. Hence **K thickens iff** there exist:

- for each generator g, a cyclic order π_g of the occurrences of g^{±1} (the rotation at link vertex g+), and
- a handle type for each generator: orientable, with rotation π_g^-1 at g−, or non-orientable, with rotation π_g at g−,

such that

1. the vertex link (4 vertices, one edge per corner) with this rotation system embeds in S^2, i.e. every component has V − E + F = 2, and
2. each relator passes through non-orientable handles an even number of times, so its attaching curve has an annular neighbourhood.

The two cyclic orders at the ends of a handle are mirror images exactly when the handle is attached orientably (reflection through the core arc). This is the one-vertex case of the classical Osborne–Stevens and Neuwirth criteria, cited from memory.

`e_thicken.cpp` enumerates all ((d_x−1)!·(d_y−1)!·4) choices. An independent Python implementation agrees on 47 cases: positive controls (wedge of discs, torus, Klein bottle, RP^2, pseudo-projective planes of orders 3 and 5, dunce hat), AK(1), AK(2), AK(3), and 38 random small presentations, 4 of which are non-thickenable.

Why it matters: per Lackenby's abstract, *one* thickenable presentation anywhere in the AC class of AK(3) would make AK(3) AC-trivial. The surveyed low-length part of the class contains none. This is a negative datum about that route, not an obstruction.

## 7. Reproduction (from the repository root)

```sh
B=/tmp/e_bin; mkdir -p $B
g++ -O2 -std=c++17 -o $B/e_acdist  experiments/e_acdist.cpp
g++ -O2 -std=c++17 -o $B/e_peak    experiments/e_peak.cpp
g++ -O2 -std=c++17 -o $B/e_thicken experiments/e_thicken.cpp
$B/e_acdist --selftest; $B/e_peak --selftest; $B/e_thicken --selftest
export E_ACDIST_BIN=$B/e_acdist E_PEAK_BIN=$B/e_peak E_THICKEN_BIN=$B/e_thicken
python3 experiments/e_nilpotent_tables.py --selftest   # independent Heisenberg BFS + Magnus replay
python3 experiments/e_peak_check.py                    # independent string BFS for G_L components
python3 experiments/e_thicken_check.py --selftest      # independent criterion implementation
python3 experiments/e_nilpotent_tables.py --check-quotient-certs     # binary-free
python3 experiments/elementary_verify.py certificates/e_ak1_trivialization.json \
        certificates/e_ak2_peak13_trivialization.json
# headline runs (one core each; peak memory in parentheses)
$B/e_acdist --mode free --start xxxYYYY xyxYXY --max-states 22000000          # >=15 (2.3 GB)
for c in 1 2 3 4; do $B/e_acdist --mode nil --class $c --start xxxYYYY xyxYXY --max-states 12000000; done
$B/e_acdist --mode nil --class 5 --start xxxYYYY xyxYXY --max-states 6500000  # >=14 (2.2 GB)
for c in 1 2 3 4 5 6; do $B/e_acdist --mode nil --class $c --mod 2 --start xxxYYYY xyxYXY --max-states 3000000; done
for L in 13 14 15 16 17 18 19 20; do $B/e_peak --L $L --cap 125000000; done   # L=20: 51.4M states, 1.6 GB, 170 s
$B/e_peak --L 13 --start xxYYY xyxYXY --path                                  # AK(2) peak 13
$B/e_peak --L 20 --dump 16 2> dump.txt; python3 experiments/e_thicken_check.py --survey-file dump.txt
```

Executed outputs from this session agree with the tables above. All self-tests and cross-checks reported "passed".

## 8. Honest limits

- The bounds 15 (instructions) and 21 (peak) are finite exhaustive results. They are not evidence that AK(3) is non-trivial. AK(2) is trivial yet needs at least 15 instructions, and its trivial component is reachable only from L = 13.
- Corollary 4 is a reformulation, not progress toward a growth proof. The computed chain distances do not separate AK(3) from AK(2).
- The thickenability survey covers only the explored low-length slice of the class, not the whole AC class.
- I rely on Lackenby's abstract (via search) for the unstable statement, and on memory for the Osborne–Stevens/Neuwirth criterion; the outline in Section 6 is mine.
- Literature access was limited to search snippets; earlier BFS literature may already contain the 15/21-type bounds in another normalization. Novelty is not claimed.

## 9. Insight and recommended next directions

1. **Uniformity is the only quotient route left.** Corollary 4 together with Section 4 shows that any quotient-based proof of non-triviality must exhibit Lipschitz functions f_c on pairs in P_c^{(2)} (|f_c(sA) − f_c(A)| ≤ 1 for each instruction s) with f_c(AK3) − f_c(x,y) → ∞. Such f_c cannot factor through bounded class, and cannot factor through quotients of T or B_3. A concrete next step is a graded "correction-cost" lower bound: how many instructions are needed to remove a nonzero degree-c Lie error, uniformly in c.
2. **Thickenability is a cheap global filter for D and F.** By Lackenby, a thickenable presentation in AK(3)'s class finishes the problem, and a thickenable candidate counterexample is ruled out. The current brute force costs (d_x−1)!(d_y−1)!; an incremental planarity search would scale to the 51M-state G_20 component and to D's search frontier.
3. **Push the peak bound** to L = 21–22 with a disk-backed or bit-packed state set (estimated ≥ 5·10^8 states). Also characterize the small AK(3) components (they grow about 10× per odd L and stay above total length 13), compared with the trivial component, which is already 58M states at L = 15.

## 10. Files written

- `research/research-e.md` (this note).
- `experiments/e_acdist.cpp`: free and nilpotent/mod-p bidirectional BFS, with a self-test.
- `experiments/e_nilpotent_tables.py`: driver, independent Heisenberg/Magnus checks, certificate writer.
- `experiments/e_peak.cpp` and `experiments/e_peak_check.py`: G_L components and independent check.
- `experiments/e_thicken.cpp` and `experiments/e_thicken_check.py`: thickenability test, independent check and survey.
- `certificates/e_ak1_trivialization.json` (ordinary AC, 12 moves).
- `certificates/e_ak2_peak13_trivialization.json` (ordinary AC, 28 moves, peak 13).
- `certificates/e_ak3_quotient_paths.json` (**quotient-only, not an AC trivialization**).

## References

- S. Akbulut, R. Kirby, *A potential smooth counterexample in dimension 4 to the Poincaré conjecture, the Schoenflies conjecture, and the Andrews–Curtis conjecture*, Topology 24 (1985) 375–390.
- W. Magnus, *Beziehungen zwischen Gruppen und Idealen in einem speziellen Ring*, Math. Ann. 111 (1935), and *Über Beziehungen zwischen höheren Kommutatoren*, J. reine angew. Math. 177 (1937): lower central series = integral dimension subgroups for free groups (cited from memory).
- A. Borovik, A. Lubotzky, A. Myasnikov, *The finitary Andrews–Curtis conjecture*: https://arxiv.org/abs/1103.1295
- L. Guyot, *On Andrews–Curtis conjectures for soluble groups*: https://arxiv.org/abs/1612.06912
- M. Lackenby, *The stable Andrews–Curtis conjecture and thickenable presentations of the trivial group* (2026): https://arxiv.org/abs/2606.06122 (abstract only, via search)
- I. Bobtcheva, F. Quinn, https://arxiv.org/abs/math/0012212 ; *The reduction of quantum invariants of 4-thickenings*, Fund. Math. 188 (2005) 21–43.
- M. Bridson, *The complexity of balanced presentations and the Andrews–Curtis conjecture*: https://arxiv.org/abs/1504.04187
- A. Myropolska, *Andrews–Curtis and Nielsen equivalence relations on some infinite groups*: https://arxiv.org/abs/1304.2668
- G. Havas, C. Ramsay, *Breadth-first search and the Andrews–Curtis conjecture*, IJAC 13 (2003) 61–68; R. Bowman, S. McCaul, *Fast searching for Andrews–Curtis trivializations*, Exp. Math. 15 (2006).
- A. D. Myasnikov, A. G. Myasnikov, V. Shpilrain, *On the Andrews–Curtis equivalence*: https://web.stevens.edu/algebraic/alexeim/Publications/AC%20Conjecture/ac1.pdf
- D. Panteleev, A. Ushakov: https://arxiv.org/abs/1609.00325 ; A. Shehper et al.: https://arxiv.org/abs/2408.15332 ; A. Lisitsa: https://arxiv.org/abs/2501.18601 and https://doi.org/10.1016/j.jaca.2025.100041 ; J. Carreras: https://arxiv.org/abs/2607.23611
- R. Osborne, R. Stevens, *Group presentations corresponding to spines of 3-manifolds I–III*, Amer. J. Math. (1974–77), and L. Neuwirth, *An algorithm for the construction of 3-manifolds from 2-complexes*, Proc. Camb. Phil. Soc. 64 (1968): cited from memory for the link criterion.
