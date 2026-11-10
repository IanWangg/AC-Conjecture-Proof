# Research TH07: what really happens beyond the plateau of AK(n) — exact first-exit classification, a 4n+3 wall on the braid side, and Baumslag–Solitar shortcuts on the power side

Date: 2026-11-09 (Los Angeles). Independent research agent TH07 (round 5, theory round).

**Status:** partial results with complete proofs, uniform in n. **No AK(3) trivialization, no proof of non-triviality, no counterexample, nothing on the full conjecture.** All bounds below are bounds on *paths* in a stated move class with a stated length measure; by research-k (K2) no such bound is evidence of non-triviality.

**Central claims (all for ACM = quotient-conjugacy moves with arbitrary conjugators, cyclic lengths; n ≥ 3 unless stated).**

1. **Theorem A (proved).** The words of length 2n+3 conjugate to p_n^{±1} in the braid group B (the first-exit power relators) are exactly the rotations of 4n(n+1) explicit cyclic words U1(a,c)^{±1}, U2(a,c)^{±1}; there are exactly 4n(n+1)(2n+3) such words (432 for n = 3, matching research-j).
2. **Theorem B (proved; "4n+3 wall" on the braid side).** A cyclically reduced word conjugate to b^{±1} in ⟨x,y | xⁿ = y^{n+1}⟩ is either in Orb(b) or has length ≥ 2n+2, with exactly 4 cyclic words (8n+8 words) at length 2n+2. Hence every ACM path that leaves the plateau by changing the braid relator reaches total length ≥ 4n+3. Research-k's path AK(n) → P_n is of this kind, which explains its peak 4n+5 up to 2.
3. **Theorem C (proved; Baumslag–Solitar shortcut on the power side).** The first-exit relator w_n = xⁿyX^{n+1}Y (= U1(n−1,0)) presents BS(n+1,n); by Britton/Collins the class of b^{±1} in ⟨x,y | w_n⟩ is completely explicit. Consequences (§5), all proved, with certificates for n = 3, 5:
   - (i) research-j's bound "first exit ≥ 2n+9" is **sharp, and the path comes straight back down**: AK(n) → (w_n, b) → (w_n, yyXYX) has lengths 2n+7, 2n+9, 2n+8;
   - (ii) **a peak of about 4n is not necessary for ACM moves**: AK(n) → (w_n,b) → (w_n,e_n) → (d_n,e_n) → P_n, with e_n = x^{n−1}yyXY, d_n = xⁿYXyy, has lengths 2n+7, 2n+9, 3n+6, 2n+7, n+11 (research-k's path: peak 4n+5), and a longer chain has peak 2n+8+⌊(2n+1)/3⌋ ≈ 8n/3. For n = 3 the ACM barrier from AK(3) to P_3 and to the second length-13 class Q = (d_3,e_3) is **exactly 15**;
   - (iii) inside this channel 3n+6 is optimal: a class member of b^{±1} modulo w_n is either a "frame word" y xʲ y XYX (the state is then an automorphic image of a state (u,b)) or has length ≥ n+3;
   - (iv) **a new family**: F_n = (XyXyxYY, y x^{n−1} y XYX), of length n+11 like P_n but in a different Aut(F₂)-orbit, is AC-equivalent to AK(n); it is the image under the automorphism y ↦ x^{n−2}y of the first-exit state (U2(n−2,1), b), i.e. **one ACM move from AK(n) up to an automorphism**.
4. **Not achieved.** No lower bound of the form 2n+c with c > 9 for trivializations, and no (2+ε)n lower bound for reaching a shorter presentation: the obstacle is the conjugacy problem in ⟨x,y | U⟩ for the non-BS first-exit relators U (§6). The ACM peaks above are *not* peaks of elementary AC paths: the conjugators have length about n², and the cyclic-product expansions used for the certificates peak at about 4n+6.

Notation (research-a): X = x⁻¹, Y = y⁻¹, b = xyxYXY, p_n = xⁿY^{n+1}, q_n = yⁿX^{n+1}, AK(n) = (p_n, b). B = F/⟨⟨b⟩⟩, G_n = F/⟨⟨p_n⟩⟩, G_n′ = F/⟨⟨q_n⟩⟩. An **ACM move** replaces (u,v) by (u′,v) when u′ is conjugate to u^{±1} in F/⟨⟨v⟩⟩ (arbitrary conjugators; relator swap allowed). All lengths are **cyclic** lengths of cyclically reduced words; Orb(w) = rotations of w and of w⁻¹. Every ordinary AC move is an ACM move, so the cyclically reduced states of an ordinary AC path form an ACM path; conversely an ACM move is a composite of ordinary AC moves (research-g, Lemma G0), but its elementary expansion may be much longer than the two endpoint states.

Two classes are used throughout:

    C_n = { cyclically reduced u : u conjugate to p_n^{±1} in B }          (power side, b frozen)
    D_n = { cyclically reduced v : v conjugate to b^{±1} in G_n }           (braid side, p_n frozen; D_n′ for q_n)

## 1. Previous work read and choice of direction

Read in full: `README.md`; research-a; research-j (audit and §4); research-k §2–3; research-g §1–3. Read the status paragraphs (and, where present, the coordinator's reviews) of b–f, h, i, l–o, and skimmed e §5.3 and l §3.3/3.6. Reused code: `j_first_increase.py` (enumeration, exact conjugacy test of Lemma J0), `d_certify.py`, `d_whitehead.py`, `elementary_verify.py` (all read-only).

Starting point: research-a's plateau theorem and research-j's Theorem J1 (first exit ≥ 2n+9), whose extension "needs the ACM neighbours of states whose frozen relator is no longer a torus word". My seed asked for (a) a uniform classification of the first-exit states and the next level, (b) whether a peak of about 4n is necessary to reach a shorter presentation, (c) potential functions. Chosen direction: do (a) completely at the first level (Theorems A, B), then attack the second level at the first frozen relators that are *not* torus words. It turned out that the simplest of them, w_n, is a Baumslag–Solitar relator, for which Britton's and Collins' lemmas give exact answers (Theorem C) — and the answers refute the natural conjecture behind (b) for ACM moves: the 4n wall exists only on the braid side. I therefore redirected the remaining time from "prove 2n+c, c > 9" to "determine exactly what the first two levels contain", which is new relative to A–O: J has the n = 3 counts only; G treats frozen *torus* relators (and uses BS(3,4)-conjugates in one experiment, without a classification); K's path is shown here to be the braid-side route, and its words a_m, b_m, c_m are identified as frame words and automorphic images of first-exit words. Overlap check with this round's seeds: TH04 (torus-type words in the partner's class) is adjacent to Theorem B but concerns a different question; nothing here uses stable moves, quotient invariants or searches.

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

## 3. Theorem B: the braid side — a wall at 4n+3 (proved here)

G_n = ⟨x,y | xⁿ = y^{n+1}⟩ has centre ⟨xⁿ⟩, quotient C_n * C_{n+1} and abelianization x ↦ n+1, y ↦ n (b ↦ 1). Put b_1 = X^{n−1}·y·x·Y·x^{n−1}·Y and b_2 = x·y·X^{n−1}·Y·x^{n−1}·Y (b with one letter x replaced by X^{n−1} and the letter X replaced by x^{n−1}).

**Theorem B (proved here).** Let n ≥ 3 and let v be a cyclically reduced word conjugate to b^{±1} in G_n. Then v ∈ Orb(b), or |v| ≥ 2n+2; and |v| = 2n+2 exactly for v ∈ Orb(b_1) ∪ Orb(b_2) (4 cyclic words, 8n+8 words; for n = 3 these are research-j's 32 words of length 8). The same holds in G_n′ = ⟨x,y | yⁿ = x^{n+1}⟩ with x and y exchanged in b_1, b_2 (apply the swap x ↔ y, which maps q_n to p_n and b to b⁻¹).

*Proof.* v is not a power of a letter (its image must have six syllables), so cyclically v = x^{α_1}y^{β_1}⋯x^{α_r}y^{β_r} with all exponents non-zero and |v| = Σ|α_i| + Σ|β_i|. By Lemma J0, (n+1)Σα_i + nΣβ_i = ε = ±1, hence (Σα_i, Σβ_i) = ε(1,−1) + m(n,−(n+1)) for some m ∈ ℤ. Call a block *vanishing* if n | α_i, resp. (n+1) | β_i.

*No vanishing block.* The image of v in C_n * C_{n+1} is cyclically reduced with 2r syllables, so r = 3 and, after a rotation, α_i = α_i⁰ + nk_i, β_i = β_i⁰ + (n+1)l_i, where (α⁰, β⁰) are the exponents ±1 of b^ε. The abelianization gives Σk_i + Σl_i = 0. If all k_i, l_i vanish, v ∈ Orb(b) (n ≥ 3, so the residues determine the exponents ±1). Otherwise at least two of them are non-zero; a block with k_i ≠ 0 has |α_i| ≥ n−1, with equality iff α_i = (1−n)α_i⁰, and a block with l_i ≠ 0 has |β_i| ≥ n. Hence |v| ≥ 4 + 2(n−1) = 2n+2, with equality iff exactly two blocks are changed, both x-blocks, with k_i = −α_i⁰ and k_i + k_{i′} = 0, i.e. one block x becomes X^{n−1} and one block X becomes x^{n−1}: these are the rotations of b_1^{±1}, b_2^{±1}.

*Some vanishing block.* Deleting a trivial syllable merges its neighbours, so the image has at most 2r−2 syllables and r ≥ 4. If an x-block vanishes, Σ|α| ≥ n+3 and Σ|β| ≥ 4; for m = 0 the other x-blocks sum to ε − α_i, of absolute value ≥ n−1, so |v| ≥ (2n−1)+4; for m ≠ 0, Σ|β| ≥ |Σβ_i| ≥ n and |v| ≥ (n+3)+n. If a y-block vanishes, Σ|β| ≥ n+4 and Σ|α| ≥ 4; for m = 0 the other y-blocks sum to −ε − β_i, so Σ|β| ≥ 2n+1; for m ≠ 0, Σ|α| ≥ max(4, n−1) and |v| ≥ 2n+3. In every case |v| ≥ 2n+3. ∎

**Corollary B1 (the two exits; proved here).** Let n ≥ 3 and 𝒜 = {(u, b′) : u ∈ C_n, b′ ∈ Orb(b)} (either order). An ACM path from AK(n) stays in 𝒜 until its first move of one of two kinds:

- *(braid-side exit)* (p′, b′) → (p′, v) with p′ a plateau word and v ∉ Orb(b); then |p′| + |v| ≥ **4n+3**;
- *(power-side exit)* (u, b′) → (u, v) with u ∈ C_n off the plateau, so |u| ≥ 2n+3 (odd), and v ∉ Orb(b), v conjugate to b^{±1} in ⟨x,y | u⟩.

Every state of 𝒜 has total length ≥ 2n+7, so every ACM path from AK(n) to (x,y), or to any state of total length < 2n+7, contains one of these moves. *Proof.* Moving u with b′ frozen stays in C_n; moving b′ with a plateau word frozen is governed by Theorem B; the remaining moves are power-side exits. ∎

Research-k's path AK(n) → P_n starts with the braid-side exit b → u_1 (length 2n+3, total 4n+4); Theorem B shows that no braid-side exit is cheaper than 4n+3, so the 4n+5 observed in research-k is forced, up to 2, **for paths that begin on the braid side** — and only for those (§5).

## 4. Theorem C: the Baumslag–Solitar relator w_n and the class of b modulo w_n (proved here)

Let w_n = xⁿ y X^{n+1} Y (a rotation of U1(n−1,0)) and G = ⟨x,y | w_n⟩ = ⟨x,y | y x^{n+1} y⁻¹ = xⁿ⟩, an HNN extension of ⟨x⟩ ≅ ℤ with stable letter y. Put β = b⁻¹ = yxyXYX and

    v_j = y xʲ y X Y X  (j ∈ ℤ; v_1 = β, v_0 = yyXYX),      e_n = x^{n−1} y y X Y,      d_n = xⁿ Y X y y.

**Lemma C0 (w_n ∈ C_n by short cyclic products; proved here).** z_i = x^{n−1} Yⁱ x y X^{n+1−i} Y (0 ≤ i ≤ n+1) satisfies z_{n+1} ~ p_n, z_0 = w_n, |z_i| = 2n+3 for 0 ≤ i ≤ n, and z_{i−1} arises from z_i by replacing the subword Y·x·y by x·y·X, i.e. by one cyclic product with a rotation of b⁻¹ (YXyxyX). So (p_n, b) → (w_n, b) is one ACM move, and also n+1 cyclic products through states of total length 2n+9.

**Theorem C (proved here; Britton's lemma and Collins' lemma).** Let n ≥ 2. A cyclically reduced word v is conjugate to β in G iff either

- (i) v is a rotation of y x^{j_1} y x^{j_2} Y x^{j_3} with j_1 ∈ ℤ arbitrary, j_2 ≡ −1 (mod n+1), j_3 ≡ −1 (mod n) (length 3+|j_1|+|j_2|+|j_3|); or
- (ii) v contains, cyclically, a pinch y x^{(n+1)k} Y or Y x^{nk} y with k ≠ 0, in which case |v| ≥ n+6.

Consequently, for n ≥ 3, the words of length ≤ n+3 conjugate to b^{±1} in G are exactly the rotations of v_j^{±1} with |j| ≤ n−2 (length 5+|j|) and of e_n^{±1} (length n+3; (j_1,j_2,j_3) = (0,−1,n−1)); the minimum 5 is attained only on Orb(yyXYX); every class member that is not a frame word v_j^{±1} has length ≥ n+3, and after e_n the next ones are d_n (triple (0,n,−1)) and the triples (±1,−1,n−1), of length n+4.

*Proof.* The cyclic word β = y·x·y·x⁻¹·Y·x⁻¹ has no pinch (n+1 ∤ −1, n ∤ −1), so it is cyclically reduced in the HNN sense, with three stable letters. (ii): if v has a cyclic pinch, cyclic Britton reduction ends in a cyclically reduced conjugate, which by Collins' lemma has three stable letters; so v has at least five, its sign sequence has at least two cyclic sign changes, the x-syllable at each sign change is non-empty (v is freely reduced), and one of them is the pinch, of length ≥ n: |v| ≥ 5+n+1. (i): otherwise v is cyclically reduced in the HNN sense, so by Collins' lemma it has three stable letters and a rotation of v ending in a stable letter equals z β* z⁻¹ in G, with β* a rotation of β ending in a stable letter and z ∈ ⟨x⟩. Equal reduced words have equal sign sequences (Britton), so after rotating we may take v* = x^{j_3} y x^{j_1} y x^{j_2} Y and β* = X y x y X Y, z = xᵗ:

    x^{j_3} y x^{j_1} y x^{j_2} Y · xᵗ y x Y X Y x^{1−t} = 1.

By Britton's lemma the successive pinches must occur at the junction: Y xᵗ y forces t = nm and equals x^{(n+1)m}; then y x^{j_2+(n+1)m+1} Y forces j_2 + 1 + (n+1)m = (n+1)m′ and equals x^{nm′}; then y x^{j_1+nm′−1} Y forces j_1 − 1 + nm′ = (n+1)m″ and equals x^{nm″}; finally j_3 + nm″ + 1 − t = 0. So j_2 = −1 + (n+1)(m′−m), j_3 = −1 + n(m−m″), j_1 = 1 + m − n(m′−m) − (n+1)(m−m″): given j_2, j_3 in these residue classes, j_1 is arbitrary (choose m). Conversely every such triple makes the displayed word trivial. Such a word is freely and cyclically reduced because j_2, j_3 ≠ 0. The length statements are read off: a non-frame triple has |j_2| ≥ n or |j_3| ≥ n−1. ∎

Explicit conjugators (checked by Britton reduction, §7): v_j = x^{n(j−1)} β x^{−n(j−1)} and e_n = x^{n²−1} β x^{−(n²−1)} in G. The conjugators have length of order n², which is why cyclic-product searches see these moves only at high barrier.

**Frames.** Let θ_j ∈ Aut(F): x ↦ x, y ↦ x^{j−1}y. Then v_j = cyc θ_j(β) and θ_j(w_n) is a conjugate of w_n. So (w_n, v_j) is the θ_j-image of the state (w_n, b⁻¹); ⟨x,y | v_j⟩ ≅ B and the class of w_n modulo v_j is θ_j(C_n): every state reachable from (w_n, v_j) by moving only the first relator is an automorphic image θ_j(u, b⁻¹) of a state of 𝒜. The word e_n is not of this kind in the w_n-channel: it is the cheapest genuinely new exit there.

By the symmetries of the plateau (x ↔ y; x ↦ X, y ↦ Y) the same holds for the other three Baumslag–Solitar relators among the first-exit words, U1(0,n) = Y^{n+1}xyⁿX, U2(n−1,0), U2(0,n).

## 5. Consequences: what lies beyond the plateau (proved here)

**Lemma T (triangles).** If t = cyc(r′s′) with r′, s′ rotations of r^{±1}, s^{±1}, then modulo any one of r, s, t the other two are conjugate up to inversion. So two states sharing a relator f, whose other relators are each in a triangle with f and a common word h, differ by one ACM move.

Research-k's words, in the notation of this note (1 ≤ m ≤ n): a_m = x^m yXYXy, b_m = xⁿYXyX^{n−m}y, c_m = x^{n−1}yX^{n−m}yXY, c = xyxYYXy. K's identities are the triangles (w_n, a_m, b_m), (w_n, b_m, c_m), (w_n, c_m, a_{m+1}), (w_n, a_n, d_n), (d_n, a_n, c); the second also holds for m = n: XYxⁿyXⁿ · xⁿYXyy = XYx^{n−1}yy. **Dictionary (checked for n ≤ 12):** a_m is the frame word v_m; b_m = θ_m(U1(n−1,1)⁻¹), so b_1 is a first-exit relator and b_n = d_n; c_m = θ_m(c_1), and c_n = e_n. So research-k's phase B walks through the frames θ_2, …, θ_n, and (b_m, a_m) is the θ_m-image of the first-exit state (U1(n−1,1)⁻¹, b⁻¹), of total length 2n+9 for every m.

**Corollary C1 (the bound 2n+9 of research-j is sharp, and the path comes back down).** For n ≥ 3,

    (p_n, b) → (w_n, b) → (w_n, yyXYX)        total lengths 2n+7, 2n+9, 2n+8

is an ACM path. So the least peak of an ACM path from AK(n) to a state off the plateau is exactly 2n+9; and a bound "2n+10" for trivializations cannot come from a first-exit argument: it needs the full set of states reachable below 2n+10, which contains states of length 2n+8.

**Corollary C2 (a second state of length 2n+7, and P_n, with ACM peak 3n+6).** For n ≥ 3,

    (p_n, b) → (w_n, b) → (w_n, e_n) → (d_n, e_n) → (d_n, c) = P_n       total lengths 2n+7, 2n+9, 3n+6, 2n+7, n+11

is an ACM path: move 1 is Lemma C0, move 2 is Theorem C, move 3 is d_n⁻¹ = cyc(w_n e_n⁻¹) (= xyXⁿYY), move 4 holds because modulo d_n the words e_n, w_n, a_n, c are conjugate up to inversion (triangles (w_n,d_n,e_n), (w_n,a_n,d_n), (d_n,a_n,c)). In particular **S_n = (xⁿYXyy, x^{n−1}yyXY) is AC-equivalent to AK(n) for every n**, has the same length 2n+7 and is not on the plateau; S_3 is, up to x ↦ X, the second length-13 class Q of research-d/e. For n = 3 the peak 3n+6 = 15 equals the lower bound of research-j: **the ACM barrier between AK(3) and Q (and P_3) is exactly 15.**

**Corollary C3 (a balanced chain: peak about 8n/3).** For 2 ≤ m ≤ n−1,

    (p_n,b) → (w_n,b) → (w_n,a_m) → (b_m,a_m) → (b_m,c_m) → (a_{m+1},c_m) → (a_{m+1},b_{m+1}) → (b_{m+1},c_{m+1}) → ⋯ → (b_n,c_n) = (d_n,e_n) → P_n

is an ACM path (Theorem C for the third state; Lemma T with hub w_n for the others) with total lengths 2n+8+m at (w_n,a_m), 2n+9 at (b_k,a_k) and (a_{k+1},c_k), and 4n+7−2k at (b_k,c_k). Its peak is max(2n+8+m, 4n+7−2m), minimal for m = ⌊(2n+1)/3⌋: **2n+8+⌊(2n+1)/3⌋**, which beats 3n+6 for n ≥ 8. Hence

    ACM peak needed to reach P_n from AK(n)  ≤  min(3n+6, 2n+8+⌊(2n+1)/3⌋)   (15, 18, 21, 24, 27, 29, 32, 35 for n = 3,…,10; research-k's path: 4n+5).

Remark. The automorphic images τ^{m−n}(P_n) = (b_m, τ^{m−n}(c)), τ: y ↦ xy, have total length 4n+9−3m and are one ACM move from (b_m, a_m); they are shorter than 2n+7 for m > (2n+2)/3. So a presentation shorter than AK(n) is reached in four ACM moves with peak 2n+9+⌊(2n+2)/3⌋.

**Corollary C4 (what the two exits cost).** Combining B1, Theorem C and C2: a path that leaves 𝒜 on the braid side has peak ≥ 4n+3; a path that leaves 𝒜 through the relator w_n (or one of its three symmetric images) either lands on a frame state θ_j(w_n, b⁻¹) or reaches total length ≥ 3n+6, with equality exactly for (w_n, e_n). Nothing is proved about power-side exits through other relators u ∈ C_n (§6).

| n | plateau 2n+7 | first exit (J1, sharp) 2n+9 | to S_n and P_n: 3n+6 | balanced chain | K's path as ACM path 4n+5 | braid-side wall 4n+3 |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | 13 | 15 | 15 | 16 | 17 | 15 |
| 5 | 17 | 19 | 21 | 21 | 25 | 23 |
| 10 | 27 | 29 | 36 | 35 | 45 | 43 |
| 30 | 67 | 69 | 96 | 88 | 125 | 123 |

**Move class and measure, once more.** All numbers in this section are peaks of *ACM* paths in *cyclic* length. They are not peaks of elementary AC paths: one ACM move here hides a conjugator of length about n². Expanded into single cyclic products (the form used for the certificates), route C2 has peak 4n+6 (the transfer moves of Theorem C pass through the triple (−n,−1,n−1) of length 2n+3), slightly *worse* than research-k's 4n+5; the cyclic-product barrier 4n+5 measured in research-k for n ≤ 6 is therefore not contradicted.

**Corollary C5 (a frame state of length n+11; proved here, certificates for n = 3, 5).** Let f = XyXyxYY and F_n = (f, y x^{n−1} y XYX) = (f, v_{n−1}). For n ≥ 3,

    (p_n, b) → (w_n, b) → (w_n, v_{n−1}) → (f, v_{n−1}) = F_n        total lengths 2n+7, 2n+9, 3n+7, n+11

is an ACM path, so **AK(n) ~AC F_n**. Indeed θ_{n−1}(U2(n−2,1)) = x·YX^{n−2}·x^{n−2}·YX^{n−2}·X·x^{n−2}y·X^{n−1}·x^{n−2}y = xYYXyXy, a rotation of f, and U2(n−2,1) ∈ C_n by Theorem A, so f lies in θ_{n−1}(C_n), the class of w_n modulo v_{n−1}. Thus F_n = θ_{n−1}(U2(n−2,1), b⁻¹): **the first-exit state (U2(n−2,1), b), of length 2n+9, is carried by an automorphism to a presentation of length n+11**, shorter than AK(n) for n ≥ 5. F_n and P_n are in different Aut(F₂)-orbits: v_{n−1} is an automorphic image of b, so ⟨x,y | v_{n−1}⟩ is the trefoil group, while neither relator of P_n has this property (their Alexander polynomials are t²+t−1 and tⁿ+t−1, research-k K1.3; the trefoil's is t²−t+1). The word f is the image of a rotation of c⁻¹ under y ↦ Y, so F_n and the mirror image of P_n share a relator up to inversion (whether they differ by one ACM move with f frozen is a twisted-conjugacy question in research-o's group; not decided here).

*Experiment (Whitehead minimization with research-d's `d_whitehead.py`, n = 3,…,8, §7).* Among the 2n(n+1) first-exit states (U, b) up to inversion, exactly four — U ∈ {U1(1,n−1), U1(n−2,1), U2(1,n−1), U2(n−2,1)} — have Aut(F₂)-minimal length n+11 (the orbit of F_n), exactly four (the Baumslag–Solitar relators) have 2n+8, and all others are Whitehead-minimal at 2n+9 (for n = 3 the two special orbits both have length 14). The Whitehead-minimal forms are AK(n): 2n+7; S_n: 2n+7; P_n: (XⁿYYxy, XYXYxyy), n+11; F_n: (X^{n−1}YxyxY, XYYxyXy), n+11.

## 6. What is not proved, and attempts that failed (with reasons)

**6.1 A bound 2n+c with c > 9 for trivializations (not obtained).** By C1 one must determine the whole set R of states reachable from AK(n) below total length 2n+10. Besides the plateau and the 4n(n+1) first-exit states it contains (w_n, yyXYX) and its three symmetric images (length 2n+8), (w_n, yXyXYX) (2n+9), the frame-θ_0 states (u′, yyXYX) with u′ ∈ θ_0(C_n), |u′| ≤ 2n+4 (for n = 3: 18 cyclic words of length 10 up to rotation besides the four Baumslag–Solitar words), and for n = 3 also (w_3,e_3), (d_3,e_3), P_3. To close R one needs, for every relator u that occurs, the class of the partner modulo u. I could do this only for torus-type u (Lemma J0) and for the Baumslag–Solitar words (Theorem C). **The first undecided question:** for the 4n(n+1)−8 other first-exit relators U, is there a word of length ≤ 6 outside Orb(b) conjugate to b^{±1} in ⟨x,y | U⟩? What I tried:
- *Abelianization.* U has exponent vector ±(t, −1−t), t = a+c−n, so a class member v has exponent vector in ±(1,−1) + ℤ(t,−1−t). This leaves many candidates, including the primitive word xY for every U (⟨x,y | U, xY⟩ is always trivial), so no cheap necessary condition excludes a two-move ACM trivialization (p_n,b) → (U,b) → (U,xY); research-g's G2 excludes only the one-move version.
- *Metabelian quotient (fails for a structural reason).* ⟨x,y | U⟩ has abelianization ℤ and b maps to a generator. In G/G″ = ℤ ⋉ A, A = ℤ[t^{±1}]/(Δ_U), the classes over a generator are A/(1−t)A = ℤ/Δ_U(1) = 0: all elements over a generator are conjugate. (Same phenomenon as research-h's no-go results.)
- *HNN structure.* For t = −1 or t = 0 one exponent sum of U vanishes and ⟨x,y | U⟩ is an HNN extension of a free group in which b has stable-letter length one (hand computation for U1(a,n−1−a), a ≤ n−2: the group is F_{n−a} ⋊ ℤ); conjugacy of b is then a twisted conjugacy problem in a free group, as in research-o. For other t a Magnus rewriting is needed first. Not carried out: no uniform treatment found in the time available.

**6.2 A lower bound (2+ε)n for reaching a shorter presentation (not obtained; the natural 4n version is false for ACM moves).** Rigorous: braid-side exits cost ≥ 4n+3 (Theorem B); in the w_n-channel non-frame exits cost ≥ 3n+6 (Theorem C); upper bounds 3n+6 and ≈ 8n/3 (C2, C3). Nothing is proved for power-side exits through other u ∈ C_n, and C5 shows why a potential-function argument is delicate: automorphic images of first-exit states can have length n+11, and the least length in the frame classes θ_m(C_n) is not monotone in m (§7). I do not know whether the true ACM barrier to a shorter presentation is 2n+O(1), about 8n/3, or in between.

**6.3 Cheaper frame changes (not found).** A change of frame θ_m → θ_{m+1} inside one ACM move needs a pivot u lying in θ_m(C_n) ∩ θ_{m+1}(C_n). Among the first-exit words only w_n and its mirror U2(n−1,0) lie in C_n ∩ τ^{±1}(C_n) (experiment, n ≤ 8), and these have length 2n+3 in every frame, which is what makes the pivot state (w_n, v_m) cost 2n+8+m. Longer pivots were not examined.

**6.4 Things deliberately not done.** No search for new states (the cyclic-product engines of D, K, M already cover n ≤ 6 far beyond these lengths); no attempt to extend the plateau method to S_n, P_n or F_n.

## 7. Experiments (exact commands; outputs from this session; each < 1 min, one core, < 100 MB)

```
python3 experiments/th07_exits.py --selftest
A  n=1..4: 40 / 168 / 432 / 880 words of length 2n+3 in C_n = 4n(n+1)(2n+3), closed forms match enumeration
B  n=3, 4: class of b in G_n and G_n' up to length 2n+2 = Orb(b) + 32 / 40 words of length 2n+2      (--full: n=5, 48 words)
C  w_n in C_n via the chain z_i (n <= 12); frame words, e_n, d_n conjugate to b^-1 modulo w_n
C  n=3 / n=4: class of b modulo w_n up to length n+3 (bounded conjugators x^t): 46 / 76 words, as in Theorem C
D  n=3..6: ACM paths verified; peaks 2n+9 (to (w_n,yyXYX)), 3n+6 (to (d_n,e_n) and P_n), 3n+7 (to F_n), balanced chain 16/19/21/24
E  n=3 routes v0 / de / P / F: certificates replay, 47 / 86 / 109 / 107 moves, elementary peaks 22 / 24 / 24 / 27
selftest passed
```
The check C for n = 3, 4 is a consistency test of Theorem C against an independent search (all cyclically reduced words of length ≤ n+3, conjugators xᵗ with |t| ≤ 2n(n+1)+2, Britton reduction); completeness rests on the proof. In D every ACM move is validated by an exact test when the frozen relator is b, w_n or a frame word, and by chains of triangle identities otherwise.

```
python3 experiments/th07_exits.py --whitehead 3 8
n=3: {14: 8, 15: 16}   n=4: {15: 4, 16: 4, 17: 32}   n=5: {16: 4, 18: 4, 19: 52}   n=6: {17: 4, 20: 4, 21: 76}
n=7: {18: 4, 22: 4, 23: 104}   n=8: {19: 4, 24: 4, 25: 136}       (Aut-minimal length: number of first-exit states (U,b), up to inversion)
shortest orbit for n >= 4: U1(1,n-1), U1(n-2,1), U2(1,n-1), U2(n-2,1) -> (X^(n-1)YxyxY, XYYxyXy), the orbit of F_n; P_n: (X^nYYxy, XYXYxyy)
python3 experiments/th07_exits.py --frames 3 10 -2 5        # least total length in frame m: 16, 15, 14, 13, 14, 15, 15, 17 for m = -2..5
python3 experiments/th07_exits.py --frames 6 9 3 7          # m=4: 18, m=5: 17 (F_6), m=6: 18 ((c, a_6)), m=7: 21; m=3: none of length <= 9
```
Certificates (format `ordinary-ac-elementary-v1`; all pass `python3 experiments/elementary_verify.py <file>`):

| file | from → to | moves | elementary peak |
|---|---|---:|---:|
| `certificates/th07_ak3_v0.json` | AK(3) → (xxxyXXXXY, yyXYX), length 14 | 47 | 22 |
| `certificates/th07_ak3_de.json` | AK(3) → S_3 = (xxxYXyy, xxyyXY), length 13 | 86 | 24 |
| `certificates/th07_ak5_de.json` | AK(5) → S_5 = (x⁵YXyy, x⁴yyXY), length 17 | 138 | 32 |
| `certificates/th07_ak5_P.json` | AK(5) → P_5 = (x⁵YXyy, xyxYYXy), length 16, by route C2 | 168 | 32 |
| `certificates/th07_ak3_F.json` | AK(3) → F_3 = (XyXyxYY, yxxyXYX), length 14 | 107 | 27 |
| `certificates/th07_ak5_F.json` | AK(5) → F_5 = (XyXyxYY, yxxxxyXYX), length 16 | 223 | 45 |

The elementary peaks are free-length peaks of the compiled certificates (cyclic-product expansions), not the ACM peaks of §5. For comparison, research-k's stored certificates AK(5) → P_5 have elementary peaks 37 and 39.
