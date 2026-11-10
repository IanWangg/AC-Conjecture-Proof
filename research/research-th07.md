# Research TH07: what really happens beyond the plateau of AK(n) — exact first-exit classification, a 4n+3 wall on the braid side, and Baumslag–Solitar shortcuts on the power side

Date: 2026-11-09 (Los Angeles). Independent research agent TH07 (round 5, theory round).

**Status:** partial results with complete proofs, uniform in n. **No AK(3) trivialization, no proof of non-triviality, no counterexample, nothing on the full conjecture.** All bounds below are bounds on *paths* in a stated move class with a stated length measure; by research-k (K2) no such bound is evidence of non-triviality.

**Central claims (all for ACM = quotient-conjugacy moves with arbitrary conjugators, cyclic lengths; n ≥ 3 unless stated).**

1. **Theorem A (proved).** The words of length 2n+3 conjugate to p_n^{±1} in the braid group B (the first-exit power relators) are exactly the rotations of 4n(n+1) explicit cyclic words U1(a,c)^{±1}, U2(a,c)^{±1}; there are exactly 4n(n+1)(2n+3) such words (432 for n = 3, matching research-j).
2. **Theorem B (proved; "4n+3 wall" on the braid side).** A cyclically reduced word conjugate to b^{±1} in ⟨x,y | xⁿ = y^{n+1}⟩ is either in Orb(b) or has length ≥ 2n+2, with exactly 4 cyclic words (8n+8 words) at length 2n+2. Hence every ACM path that leaves the plateau by changing the braid relator reaches total length ≥ 4n+3. Research-k's path AK(n) → P_n is of this kind, which explains its peak 4n+5 up to 2.
3. **Theorem C (proved; Baumslag–Solitar shortcut on the power side).** The first-exit relator w_n = xⁿyX^{n+1}Y (= U1(n−1,0)) presents BS(n+1,n); by Britton/Collins the class of b^{±1} in ⟨x,y | w_n⟩ is completely explicit. Consequences: (i) research-j's bound "first exit ≥ 2n+9" is **sharp, and the path comes straight back down**: AK(n) → (w_n, b) → (w_n, yyXYX) has lengths 2n+7, 2n+9, 2n+8; (ii) **a peak of about 4n is not necessary for ACM moves**: AK(n) → (w_n,b) → (w_n,e_n) → (d_n,e_n) with e_n = x^{n−1}yyXY, d_n = xⁿYXyy has lengths 2n+7, 2n+9, 3n+6, 2n+7, and two more ACM moves reach P_n (length n+11) with peak 3n+8 (K: 4n+5); for n = 3 the second length-13 state (d_3,e_3) is reached with ACM peak 15, equal to J's lower bound; (iii) inside this channel 3n+6 is optimal: every word in the class of b^{±1} modulo w_n is either a "frame word" y xʲ y XYX (the state is then an automorphic image of a state (u,b)) or has length ≥ n+3.
4. **Not achieved.** No lower bound of the form 2n+c with c > 9 for trivializations, and no (2+ε)n lower bound for reaching a shorter presentation: the obstacle is the conjugacy problem in ⟨x,y | U⟩ for the non-BS first-exit relators U (§6). The ACM peaks above are *not* peaks of elementary AC paths: the conjugators have length about n², and the cyclic-product expansions used for the certificates peak at about 4n+7.

Notation (research-a): X = x⁻¹, Y = y⁻¹, b = xyxYXY, p_n = xⁿY^{n+1}, q_n = yⁿX^{n+1}, AK(n) = (p_n, b). B = F/⟨⟨b⟩⟩, G_n = F/⟨⟨p_n⟩⟩, G_n′ = F/⟨⟨q_n⟩⟩. An **ACM move** replaces (u,v) by (u′,v) when u′ is conjugate to u^{±1} in F/⟨⟨v⟩⟩ (arbitrary conjugators; relator swap allowed). All lengths are **cyclic** lengths of cyclically reduced words; Orb(w) = rotations of w and of w⁻¹. Every ordinary AC move is an ACM move, so the cyclically reduced states of an ordinary AC path form an ACM path; conversely an ACM move is a composite of ordinary AC moves (research-g, Lemma G0), but its elementary expansion may be much longer than the two endpoint states.

Two classes are used throughout:

    C_n = { cyclically reduced u : u conjugate to p_n^{±1} in B }          (power side, b frozen)
    D_n = { cyclically reduced v : v conjugate to b^{±1} in G_n }           (braid side, p_n frozen; D_n′ for q_n)

## 1. Previous work read and choice of direction

(to be completed below)

## 2. Theorem A: the first-exit power relators, for all n (proved here)

Map B → C₂ * C₃ = ⟨S⟩ * ⟨T⟩ as in research-a: x ↦ T²S, Y ↦ TS (*TS-letters*, weight 2 and 1), X ↦ ST, y ↦ ST² (*ST-letters*, weight 1 and 2). A letter of weight 2 has abelianization +1 in B^ab = ℤ (x, y ↦ 1), a letter of weight 1 has −1.

**Lemma A0 (gap calculus; proved here).** Let u be a cyclically reduced word of length L. Its image is the cyclic word S T^{e_1} S T^{e_2} ⋯ S T^{e_L}, where e_i is the T-exponent between the S of the i-th letter and the S of the next letter: e_i = weight of the next letter if both letters are TS-letters; weight of the current letter if both are ST-letters; 0 at a junction TS|ST; twice the common weight at a junction ST|TS (free reducedness forces the two letters at any junction to have the same weight: the junction pairs are x·y, Y·X, resp. y·x, X·Y). Reduction in C₂ * C₃ is the rewriting "delete an entry e_i ≡ 0 (mod 3) and replace its two neighbours by their sum"; each step removes two S-syllables. If the process ends with L_f ≥ 1 entries, none ≡ 0, the image has cyclic syllable length 2L_f and its conjugacy class is the necklace (e_i mod 3). In particular (i) L_f ≡ L (mod 2); (ii) if u has r ≥ 1 maximal TS-runs (hence r ST-runs), the zeros are initially the r pairwise non-adjacent TS|ST junctions, so L_f ≤ L − 2r; (iii) if every run has length ≥ 2 then L_f = L − 2r exactly.

*Proof.* The formula for e_i is read off from the four letter images. S T⁰ S = 1 merges the neighbouring T-powers; this is the only reduction available in a cyclic word in which S-syllables and T-powers alternate, and the normal form of a free product is unique. (ii): an initial zero is flanked by non-zero entries (two consecutive gaps cannot both be TS|ST junctions), so one rewriting step removes exactly one of the initial zeros and leaves the others in place; at least r steps are needed. (iii): at a junction t|s of common weight a between runs of length ≥ 2 the neighbours of the zero are a (the T-power of t) and a (that of s), with sum 2a ≢ 0; the merged entries of different junctions are distinct entries, so after r steps no zero is left. ∎

Remark (parity). Every u ∈ C_n has odd length, because e_x(u)+e_y(u) = ∓1. This gives research-j's Lemma J1a (no length 2n+2) in one line; by (ii), |u| ≥ 2n+1+2r.

**Theorem A (proved here).** Let n ≥ 1. The cyclically reduced words of length 2n+3 conjugate to p_n^{±1} in B are exactly the rotations of U^{±1}, where U runs through

    U1(a,c) = Y xᵃ Yᶜ x · y X^{n−c} y^{n−1−a} X,      U2(a,c) = x Yᶜ xᵃ Y · X y^{n−1−a} X^{n−c} y,      0 ≤ a ≤ n−1, 0 ≤ c ≤ n.

These are 4n(n+1) distinct cyclic words, i.e. exactly **4n(n+1)(2n+3) words** (40, 168, 432, 880 for n = 1, 2, 3, 4; research-j found 432 for n = 3 by enumeration). Each consists of one TS-run A (a word in x, Y) followed by one ST-run B (a word in X, y), both of length ≥ 2.

*Proof.* Let |u| = 2n+3 = L and u ∈ C_n. The image of p_n^{±1} has 4n+2 syllables, so L_f = 2n+1 = L − 2: exactly one rewriting step. By A0(ii), r = 1 (r = 0 gives L_f = L). So u = A·B cyclically with A = a_1⋯a_k a TS-run, B = b_1⋯b_m an ST-run (we write a letter as its weight), k+m = 2n+3, and b_1 = a_k, b_m = a_1 as weights (junction rule). The gaps are a_2,…,a_k (inside A), 0 (junction A|B), b_1,…,b_{m−1} (inside B), 2a_1 (junction B|A). If k = 1 the neighbours of the zero are 2a_1 and b_1 = a_1, with sum ≡ 0, and a second step follows; if m = 1 they are a_k and 2a_1 = 2a_k, again with sum ≡ 0. Hence k, m ≥ 2, the single step merges a_k and b_1 = a_k into 2a_k, and, writing ā = 3 − a ≡ 2a, the necklace of u is

    N(u) = (ā_1, a_2, …, a_{k−1}, ā_k, b_2, …, b_{m−1})      (2n+1 entries).

By Lemma J0 (research-j), u ∈ C_n iff N(u) is a rotation of N(p_n) = 2ⁿ1^{n+1} (resp. N(p_n⁻¹) = 2^{n+1}1ⁿ) and ab(u) = −1 (resp. +1). Put sg(2) = +1, sg(1) = −1. Then ab(u) = Σ sg(a_i) + Σ sg(b_j), while the sum σ of sg over N(u) is −1 (resp. +1) and equals ab(u) − 3(sg a_1 + sg a_k). So the abelianization condition is exactly a_1 ≠ a_k.

Conversely, let c = (c_0,…,c_{2n}) be any of the 2n+1 rotations of N(p_n^{±1}) (they are distinct: n and 2n+1 are coprime) and 1 ≤ j ≤ 2n with c_j ≠ c_0. Put k = j+1, a_1 = c̄_0, a_i = c_{i−1} (1 < i < k), a_k = c̄_j, b_1 = a_k, (b_2,…,b_{m−1}) = (c_k,…,c_{2n}), b_m = a_1. The word A·B is cyclically reduced (x and Y are not mutually inverse, nor are X and y; the junctions are x·y or Y·X, and y·x or X·Y), has r = 1, k, m ≥ 2, necklace c and a_1 ≠ a_k. So the cyclic words of length 2n+3 in C_n correspond bijectively to triples (sign, c, j), i.e. to the sign and an ordered pair of positions of the necklace carrying different values: 2 · 2n(n+1) of them. A cyclic word with ab = ±1 is not a proper power, so it has 2n+3 distinct rotations.

Closed forms for the sign of p_n: let the first marked position be the (i+1)-st of the n twos and the second the (j′+1)-st of the n+1 ones. Reading from the marked 2 to the marked 1: A = Y x^{n−1−i} Y^{j′} x, B = y X^{n−j′} yⁱ X, which is U1(n−1−i, j′). Reading from the marked 1 to the marked 2: A = x Y^{n−j′} xⁱ Y, B = X y^{n−1−i} X^{j′} y, which is U2(i, n−j′). The other sign gives the inverses. ∎

Special members: U1(n−1,n) = Y x^{n−1} Yⁿ x y X is research-k's u_1 = cyc(p_n b⁻¹); **U1(n−1,0) = Y xⁿ y X^{n+1} is a rotation of research-k's w_n = xⁿ y X^{n+1} Y**, and U1(0,n) = Y^{n+1} x yⁿ X; the last two are Baumslag–Solitar relators (§4). Only O(n) of the 4n(n+1) cyclic words are single cyclic products of a plateau word with a rotation of b^{±1} (at most 48(2n+1) such products exist), so for large n most first-exit relators need longer conjugators.
