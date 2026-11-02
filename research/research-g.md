# Research G: the torus-knot-pair locus of AK(3) — exact long-conjugator moves, a trefoil/T(2,2n+1) form of AK(n), and one-move exclusions

Date: 2026-11-02. Independent research agent G (round 3).

**Status:** partial results, all verified. **No AC trivialization of AK(3), no proof that AK(3) is not AC-trivial, and no counterexample.** Everything below concerns the ordinary (unstable) AC relation. No stabilization is used anywhere.

**Summary, with labels.**

| # | statement | label |
|---|---|---|
| G0 | A quotient-conjugacy (ACM) move with a frozen relator of torus type x^p y^q (up to Aut) is decided exactly, with no bound on conjugators. It is compiled into strict elementary moves | proved (§2) + verified code |
| G1 | For every n ≥ 1, AK(n) ~AC (w_n, xyxY⁻¹X⁻¹Y⁻¹), where w_n = cyc ψ((xy)ⁿx((yx)ⁿy)⁻¹) is a T(2,2n+1) relator and ψ: x↦xyx, y↦yx. Hence, up to Aut(F₂), AK(n) ~ ⟨x,y \| (xy)ⁿx = y(xy)ⁿ, x² = y³⟩ | proved (uniform normal-form proof); certificate for n = 3 |
| G2 | For n ≥ 3, no presentation with a primitive relator is one ACM move away from AK(n), even with arbitrary conjugators and with Aut(F₂) applied freely. AK(2) is one such move away from a primitive relator | proved (abelianization plus Christoffel structure); AK(2) certificate |
| G3 | Primitive neighbours of any torus node reduce to a finite check (Lemma G4). Neither of AK(3)'s two other torus nodes has a primitive neighbour | proved + exact finite computation |
| G4 | Torus graph (bounded: \|M\| ≤ 16, exponents ≤ 24, length ≤ 160): AK(3), AK(4) and AK(5) each have exactly 3 Aut-orbits, none with a meridian or primitive relator. AK(2) reaches a primitive relator in one move. C3 (73 orbits) and C4 (6 orbits) reach meridian defect 4, not 2. The graphs of AK(3), AK(2), C3 and C4 are pairwise disjoint | experiment (exact bounds below) |

Certificates (all replayed by `experiments/elementary_verify.py`):
- `certificates/g_ak3_to_trefoil_t2_7.json`: AK(3) → (w₃, xyxYXY), 4,055 moves, peak 157.
- `certificates/g_ak2_torus_acm_trivialization.json`: AK(2) → (x, y), 606 moves, peak 55.

## 1. Previous work read and choice of direction

I read `README.md` and `research/research-{a,b,c,d,e,f}.md` in full, and skimmed every file in `experiments/` and `certificates/`. I re-ran `python3 experiments/elementary_verify.py --selftest` (passes) and `... certificates/ms3_to_ak3_exact.json` (32 moves, peak 23). In brief:

- A proves a non-increasing plateau, so a trivialization reaches cyclic length ≥ 14.
- B and E reduce non-triviality to unbounded distances in finite (2-)groups. E also proves the exhaustive bounds of ≥ 15 instructions and peak ≥ 21, and finds 917 non-thickenable low-length classes.
- C and D certify many class members, and D shows that Aut(F₂) is AC-realized on AK(3) (Lemma D6), so Aut-orbits may be used freely.
- F proves thickenable ⇒ both one-relator quotients are knot groups and each relator is a *meridian* of the other's knot (via Lackenby's theorem). F shows that no Aut-image of AK(n) is thickenable (torus-knot meridian obstruction F3), and defines the "meridian defect".

**Literature (limited).** arxiv.org and the Essex repository are blocked from this session, so I used web-search snippets only.
- Lackenby, arXiv:2606.06122: thickenable balanced presentations of the trivial group satisfy the unstable AC conjecture, with a doubly exponential stable bound (abstract only).
- Gompf–Scharlemann–Thompson (Geom. Topol. 14, 2010) relate AK-type presentations ⟨x,y \| xyx = yxy, x^{n+1} = yⁿ⟩ to links containing the square knot.
- Romary–Zupan (Geom. Dedicata 2024) give AC trivializations of a related trisection family.
- Search results still describe AK(3) as open in the unstable sense. Snippets also report Shehper et al.'s stable claim and Lisitsa's second proof of it, but the repository README records a corrected Lisitsa publication withdrawing the basis of the stable claim. I could not check either text, so I make no statement about stable AK(3).
- I found no source for G1 or G2. **Novelty is not established.**

**Why this direction.** F's analysis shows the 3-manifold locus is reached only through states where one relator presents a knot group and the other is its meridian. AK(n) is a *torus-knot pair*: x^n y^-(n+1) presents the T(n,n+1) group and the braid relator presents the trefoil group. For a frozen relator of torus type, the replacement move "r ↦ any word conjugate to r^{±1} modulo the frozen relator" is decided exactly by normal forms in Z *_Z Z, with *unbounded* conjugators. Every bounded search so far, by D, E and F (and, by report, Panteleev–Ushakov's ACM search to relator length 20), covers only short replacement words. So this route can reach far-away states and also *prove* exclusions. The constructive target is a state of meridian defect 2 or with a primitive relator: such a state is AC-trivial by an explicit Euclidean algorithm (§2.4) or by Lemma D3.

## 2. Tools (proved here)

Notation: X = x⁻¹, Y = y⁻¹, b = xyxYXY, ψ = (x ↦ xyx, y ↦ yx), φ = ψ⁻¹ = (x ↦ xY, y ↦ yyX). One checks by free reduction that φ(b) = xxYYY exactly, ψ(xxYYY) is a cyclic conjugate of b, and ψφ = φψ = id on letters (`g_torus --selftest`).

### 2.1 Conjugacy in torus groups

Let T = T_{p,q} = ⟨x,y \| x^p y^q⟩ with |p|,|q| ≥ 2 and gcd(p,q) = 1. Then z = x^p = y^{-q} is central, T/⟨z⟩ = C_|p| * C_|q|, and T is the amalgam Z *_Z Z. With fixed syllable representatives x^i (0<i<|p|) and y^j (0<j<|q|), every element is z^k times a reduced alternating syllable word.

**Lemma 1 (complete conjugacy invariant).** Two elements of T are conjugate iff their cyclically reduced normal forms have the same syllable necklace (up to rotation) and the same z-exponent.

*Proof.* By the conjugacy theorem for free products (Magnus–Karrass–Solitar, Thm 4.2), the images in C_|p| * C_|q| are conjugate iff their cyclically reduced syllable necklaces agree. Rotating a normal form is conjugation by a syllable and leaves the central exponent unchanged. If g ~ g′z^d, abelianizing gives d·ab(z) = 0 with ab(z) = ±pq ≠ 0, so d = 0. ∎

`g_torus.torus_class` computes this invariant. Its self-test checks invariance under conjugation and insertion of conjugates of the relator. It also checks, against all homomorphisms from ⟨x,y \| x²y⁻³⟩ to S₅ found by brute force, that equal invariants give equal cycle types.

### 2.2 Torus-type words

By Nielsen, Out(F₂) = GL(2,Z). Hence the cyclic words of torus type (p′,q′) are exactly cyc θ_M(x^{p′}y^{q′}), M ∈ GL(2,Z), where θ_M is any automorphism with abelianization M (`aut_from_matrix`, by Euclid on columns). Primitive cyclic words are the case |p′| = 1 or |q′| = 1.

Primitive conjugacy classes correspond bijectively to primitive vectors (m,k) (inverse class ↔ −(m,k)), represented by the Christoffel word C(m,k) with letters inverted according to sign (Osborne–Zieschang 1981; Cohen–Metzler–Zimmermann 1981; externally reported, classical). `christoffel` is checked against θ_M(x) for all |M| ≤ 7.

**Fact C (classical; checked by `check_lemma_g4` for |m|+|k| < 60).** In C(m,k) with 1 ≤ |m| < |k|, the x-letters are isolated and the y-runs have lengths ⌊|k|/|m|⌋ or ⌈|k|/|m|⌉. The cyclic sequence of y-run lengths is *balanced*: a binary necklace that contains the factor "aa" cannot contain "bb".

### 2.3 Lemma G0: ACM moves are explicit AC composites

If r′ ≡ g r^ε g⁻¹ modulo ⟨⟨v⟩⟩, then (r, v) → (r′, v) is a composite of ordinary AC moves: conjugate r, invert, then multiply successively by conjugates h v^{±1} h⁻¹. Each such multiplication is: conjugate v by h, multiply, conjugate v back.

`experiments/g_cert.py` makes this explicit. It works in θ-coordinates and maps moves back letterwise: invert ↦ invert, multiply ↦ multiply, conjugation by a letter g ↦ conjugation by the word θ(g). Since θ is a homomorphism and free reduction is canonical, the real state always equals red(θ(state)), and this is asserted at the end of each edge. It then conjugates the frozen relator to exactly x^p y^q.

The moved relator is rewritten to a canonical linear word: canonical residues, read from the minimal necklace rotation, followed by one trailing central power. Each rewrite replaces a chunk A S B → A S′ B with S⁻¹S′ = h R^{±1} h⁻¹, which is checked in F. The same is done for the target, and that step list is appended reversed. Nothing is trusted: certificates are replayed by `elementary_verify.py`.

### 2.4 Two exits to triviality

- (a) A primitive relator gives AC-triviality (Lemma D3; `g_cert.finish_primitive` builds the certificate).
- (b) Suppose v = θ(x^p y^q) and the partner relator has cyclic syllable length 2 in C_|p| * C_|q| (defect 2). Then its image is x^i y^j z^k = x^{i+pk} y^j, and the abelianization forces q(i+pk) − pj = ±1. So it can be replaced by the word x^c y^d with |pd − qc| = 1. The pair (x^p y^q, x^c y^d) is AC-trivial by row operations: r·s⁻¹ = x^p y^{q−d} x^{−c} rotates to x^{p−c} y^{q−d}; inversion negates a row; Euclid ends at (x^{±1}, y^{±1}).

So a defect-2 torus node is AC-trivial (proved). This sharpens F3, which only gives the necessity of defect 2 for thickenability.

## 3. Results

### 3.1 Theorem G1 (uniform trefoil / T(2,2n+1) form of AK(n); proved)

Let W_n = (xy)ⁿ x · Y(XY)ⁿ = (xy)ⁿx((yx)ⁿy)⁻¹, the Wirtinger-type relator of the torus knot T(2,2n+1), and let w_n = cyc ψ(W_n). Then for every n ≥ 1,

    AK(n) = (xⁿ y^-(n+1), b)  ~AC  (w_n, b),

by a single replacement of the first relator with b frozen.

*Proof.* φ maps ⟨⟨b⟩⟩ onto ⟨⟨x²y⁻³⟩⟩, so it induces F/⟨⟨b⟩⟩ ≅ H = ⟨x,y \| x² = y³⟩. Here z = x² = y³ is central and H/⟨z⟩ = ⟨s⟩ * ⟨t⟩ = C₂ * C₃, with X = s z⁻¹ and Y = t² z⁻¹.

- U_n := φ(xⁿY^{n+1}) = (xY)ⁿ(xYY)^{n+1}. Since xY = st² z⁻¹ and xYY = st z⁻¹, U_n = (st²)ⁿ(st)^{n+1} z^{-(2n+1)}. Its inverse is U_n⁻¹ = (t²s)^{n+1}(ts)ⁿ z^{-(2n+1)}, using (st)⁻¹ = t²s z⁻² and (st²)⁻¹ = ts z⁻².
- W_n = (st)ⁿ s · t² z⁻¹ · (s t² z⁻²)ⁿ = (st)ⁿ(st²)^{n+1} z^{-(2n+1)}.

Both normal forms are alternating and cyclically reduced. They have the same t-exponent necklace 2^{n+1}1ⁿ and the same central exponent, so W_n ~ U_n⁻¹ in H by Lemma 1. Applying ψ gives ψ(W_n) ≡ g (xⁿY^{n+1})⁻¹ g⁻¹ modulo ⟨⟨b⟩⟩, and Lemma G0 turns the replacement into AC moves. ∎

**Interpretation.**
- Applying φ, (W_n, x²y⁻³) ~AC φ(AK(n)).
- φ(AK(n)) ~AC AK(n): for n = 3 by D's certificates (Lemma D6); for general n by Panteleev–Ushakov's theorem (externally reported).
- So AK(n) ≅_AC ⟨x,y \| (xy)ⁿx = y(xy)ⁿ, x² = y³⟩. The original is "Wirtinger trefoil relation + torus T(n,n+1) relation"; the new form is "torus trefoil relation + Wirtinger T(2,2n+1) relation", a role swap.
- Total length 4n+7, Aut-minimal length 2n+10 (16 for n = 3; Whitehead canonical form (XXXXYXY, XYYYYXyyy) from `d_whitehead.py`).

**Certificate (n = 3).** `certificates/g_ak3_to_trefoil_t2_7.json` runs from exactly ("xxxYYYY", "xyxYXY") to exactly ("xyxyxxyxyxxyxyxYXXYXYXXYXYXXY", "xyxYXY"): **4,055 strict moves, peak 157**. As further replay checks of the uniform statement (not stored): n = 1, 2, 4, 5 give 433, 1,647, 8,033 and 13,957 moves with peaks 61, 109, 205 and 253, all accepted by the verifier. The certificates are long because the compiler goes through normal forms; minimality is not claimed.

### 3.2 Proposition G2 (no primitive relator one ACM move from AK(n), n ≥ 3; proved)

Let n ≥ 3. Then:

- (a) no primitive element of F₂ is conjugate to b^{±1} in G_n = ⟨x,y \| xⁿ = y^{n+1}⟩;
- (b) for n ≥ 2, no primitive element is conjugate to (xⁿy^{-(n+1)})^{±1} in B = F/⟨⟨b⟩⟩.

Consequently, every pair obtained from AK(n), n ≥ 3, by replacing one relator with a word conjugate to it or its inverse modulo the other has no primitive relator. Since automorphisms carry primitives to primitives and transport the move, the same holds for φ(AK(n)) for every φ ∈ Aut(F₂). The frozen relators x^n y^-(n+1) and b are not primitive.

*Proof of (a).* G_n → Z, x ↦ n+1, y ↦ n, sends b to 1. If p is primitive with exponent vector (m,k) and p ~ b^{±1}, then (n+1)m + nk = ±1.
- Both m, k ≠ 0 and of opposite signs, so |k| = ((n+1)|m| ∓ 1)/n.
- If |m| = 1, then p has length 2 and its image in C_n * C_{n+1} has 2 syllables.
- Otherwise |m| < |k| < 2|m|. By Fact C the x-letters of p are isolated and the y-runs have length 1 or 2. Their images ā^σ (σ = sign m) and b̄^{±1}, b̄^{±2} are nontrivial (n+1 ≥ 4), so the image is cyclically reduced with **all x-syllables equal to ā^σ**.
- The image of b has the six nontrivial syllables ā b̄ ā b̄⁻¹ ā⁻¹ b̄⁻¹, with x-syllables (ā, ā, ā⁻¹); for b⁻¹ = yxyXYX they are (ā, ā⁻¹, ā⁻¹). Since n ≥ 3, ā ≠ ā⁻¹.
- Cyclically reduced conjugates in a free product are syllable rotations, so the images are not conjugate. ∎

*Proof of (b).* Transport by φ to H = ⟨x,y \| x² = y³⟩, H → Z by x ↦ 3, y ↦ 2. Then U_n ↦ −1, so a primitive p ~ U_n^{±1} has 3m + 2k = ±1 with m, k of opposite signs.
- If |m| = 1, the image has 2 syllables, but U_n has 4n+2 ≥ 6.
- Otherwise |m| < |k| < 2|m|: x isolated, y-runs of length 1 or 2, images s and t^{±1}, t^{±2}, all nontrivial.
- The t-exponent necklace of p's image is the run-length necklace under the bijection 1 ↔ 2 or the identity, so it is balanced (Fact C).
- The necklaces of U_n and U_n⁻¹ are 2ⁿ1^{n+1} and 2^{n+1}1ⁿ. For n ≥ 2 each contains both "22" and "11", so neither is balanced. ∎

For n = 2, (a) fails, as it must since ā = ā⁻¹ in C₂. The complete search (`primitive_complete`) finds exactly the primitive vectors (±3, ∓4) and (±3, ∓5), e.g. the word yXyXyXy, conjugate to b^{±1} in ⟨x,y \| x² = y³⟩. Compiling this single move plus the primitive finish gives **`certificates/g_ak2_torus_acm_trivialization.json`: AK(2) → (x,y), 606 moves, peak 55** — a one-ACM-move proof that AK(2) is AC-trivial. AK(2) was already known to be AC-trivial; this certificate tests the pipeline, not a new fact.

**Remark (thickenable at ACM distance 1).** If one relator is frozen, the moved relator's class in the frozen relator's group, and hence its defect, is unchanged. By F3 (research-f), no state one ACM move from AK(n) is thickenable, since the defects are 6 and 4n+2. This is immediate from F's proposition.

### 3.3 Lemma G4 (finite reduction) and the AK(3) torus nodes (proved + exact computation)

**Lemma G4.** Let 2 ≤ |p| < |q|, gcd(p,q) = 1, and let c be a conjugacy class of T_{p,q} with ab(c) = ±1 (x ↦ q, y ↦ −p) and cyclic syllable length L. If a primitive element with exponent vector (m,k) lies in c^{±1}, then qm − pk = ±1 and |m| ≤ max(1, L/2).

*Proof.* As in G2(a): |k| = (|q||m| ∓ 1)/|p| > |m| for |m| ≥ 2, so x is isolated. The y-run lengths are at most ⌈|k|/|m|⌉ ≤ (|q|+1)/2 < |q| when |q| ≥ 3, so no y-run vanishes. The image therefore has exactly 2|m| syllables. ∎

The case |p| > |q| is symmetric. So "is there a primitive neighbour?" is a finite, exact computation (`g_torus.primitive_complete`). With it:

- AK(n), n = 2..7: primitive neighbours only for n = 2 (the four vectors above), confirming G2.
- AK(3)'s two other torus nodes, in normalized coordinates with frozen x⁻²y³:
  - other relator W₃ = xyxyxyxYXYXYXY (T(2,7)): neither move yields a primitive. Moving W₃ is excluded by G2(b). Moving the trefoil relator inside T_{−2,7}, its partner xY³xY³xY⁴xY⁴xY⁴ has 10 syllables and the **unbalanced** run necklace 3,3,4,4,4.
  - other relator YxxxYxxxYxxxYXyXXXyXXXyX (T(2,7)): no primitive in either move; the partner has 14 syllables.

So **every path of ACM moves from AK(3) to a primitive relator has ≥ 2 moves (proved). A 2-move path must pass through an intermediate state that is not one of AK(3)'s three torus nodes; if that state is of torus type, it lies outside the enumeration bounds of §4.** Both other nodes have defects ≥ 10, so by F3 the same holds for thickenable targets.

## 4. Experiments (exact commands, executed outputs)

Every run below used one niced core and less than 200 MB RAM.

**Self-tests.**
```
python3 experiments/g_torus.py --selftest
#  g_torus self-test passed: 744 matrices, conjugacy invariants checked  (+ Lemma G4 premises)
python3 experiments/g_cert.py --selftest
#  g_cert self-test passed; AK(2) one-ACM-move certificate: 606 moves, peak 55
```

**Certificates.**
```
python3 experiments/g_cert.py --write certificates
python3 experiments/elementary_verify.py certificates/g_ak2_torus_acm_trivialization.json certificates/g_ak3_to_trefoil_t2_7.json
{"endpoint": ["x", "y"], "moves": 606, "path": "certificates/g_ak2_torus_acm_trivialization.json", "peak_total_length": 55}
{"endpoint": ["xyxyxxyxyxxyxyxYXXYXYXXYXYXXY", "xyxYXY"], "moves": 4055, "path": "certificates/g_ak3_to_trefoil_t2_7.json", "peak_total_length": 157}
```

**Torus graph.** Nodes are pairs of torus-type relators, deduplicated up to Aut(F₂), relator order, rotation and inversion (Whitehead canonical form, D's `d_whitehead.aut_canon`). An edge replaces one relator by a torus-type or primitive word θ_M(x^{p′}y^{q′}) that is conjugate to it or its inverse in the other relator's group. Bounds: |entries of M| ≤ K, |p′|,|q′| ≤ P, word length ≤ L, BFS depth ≤ 6, ≤ 3,000 nodes.

A "winner" is a node with a primitive relator, defect 2, or (with `complete=True`) a primitive neighbour by the exact Lemma G4 test.

| start | K, P, L | nodes (Aut-orbits) | winners | min defect |
|---|---|---:|---:|---:|
| AK(3) | 16, 24, 160 | **3** | 0 | 6 |
| AK(4) | 16, 24, 160 | 3 | 0 | 6 |
| AK(5) | 16, 24, 160 | 3 | 0 | 6 |
| AK(2) | 12, 20, 120 | 38 | 2 | 2 |
| C3 = (x²yXy, xy⁵xY²) | 12, 20, 120 | 73 | 0 | 4 |
| C4 = (x⁴yXy, xy³xY²) | 12, 20, 120 | 6 | 0 | 4 |

The three AK(3) orbits (normalized frozen relator \| other; defects; Aut-minimal length):
- x³y⁻⁴ \| xyxYXY; defects 6, 14; length 13 (AK(3) itself);
- x⁻²y³ \| xyxyxyxYXYXYXY; defects 14, 10; length 16 (Theorem G1);
- x⁻²y³ \| YxxxYxxxYxxxYXyXXXyXXXyX; defects 14, 14; length 19.

AK(4) and AK(5) show the same pattern with T(2,9) and T(2,11). The node sets of AK(3), C3, C4 and AK(2) are pairwise disjoint, so the torus graphs give no new equivalence among the length-14 residual classes. The defect-4 states of C3 and C4 agree with F's §4.6.

Commands (scratch drivers call only `g_torus` functions; equivalent one-liners):
```
python3 -c "import sys; sys.path.insert(0,'experiments'); import g_torus as G; \
 n,p,w=G.bfs(G.start_node('xxxYYYY','xyxYXY'),K=16,P=24,maxlen=160,depth=6,max_nodes=3000,complete=True); print(len(n),len(w))"
# -> 3 0   (AK(3); 19 s)
```
(AK(4)/AK(5): replace the first word by xxxxYYYYY / xxxxxYYYYYY; C3: 'xxyXy','xyyyyyxYY'; C4: 'xxxxyXy','xyyyxYY'; AK(2): 'xxYYY'.)

## 5. Honest limits

- No result here bears on whether AK(3) is AC-trivial. G2 and G3 exclude only very short paths in the coarse ACM metric (one relator replacement counts as one step, however long). A trivialization may need many moves. AK(2) is a reminder that short ACM distance does not mean short elementary paths.
- The torus graph is **bounded** (K, P, L as stated) and covers only states in which *both* relators are of torus type. AK(3)'s class contains many other states (e.g. D's MS(3,w) members with a BS(3,4) relator, and Q with asymmetric Alexander polynomial) that this graph cannot reach. The 3-node island is a bounded observation, not a theorem.
- G2 and Lemma G4 use the classical description of primitive cyclic words in F₂ (Osborne–Zieschang, Cohen–Metzler–Zimmermann), cited and checked numerically, not re-proved. Lemma 1 uses the conjugacy theorem for free products.
- G1's "up to Aut" form uses Panteleev–Ushakov for n ≠ 3; the stated AC equivalence (w_n, b) ~ AK(n) does not.
- The orbit (XXXXYXY, XYYYYXyyy) has Aut-minimal length 16. It may well lie in D's cap-28 component (5,508 states of Aut-length 16 there). I did not regenerate that 2.5 GB component (above my memory cap), so I claim G1 as a *structural identification*, not a new class member.
- Literature access was limited to search snippets. Novelty is not established for any item.

## 6. Insight and recommended next direction

1. **AK(2) versus AK(n≥3) is visible in exact ACM moves.** For AK(2), the braid relator is conjugate in ⟨x,y \| x² = y³⟩ to a primitive word, because in C₂ the syllables ā and ā⁻¹ coincide. For n ≥ 3 two mechanisms block every primitive or meridian exit near AK(n): the sign mixing (ā, ā, ā⁻¹) of the braid relator in C_n * C_{n+1}, and *unbalanced block necklaces* (2ⁿ1^{n+1}; 3,3,4,4,4) in the trefoil and T(2,7) groups. Primitive and meridian images are always balanced. A natural candidate quantity for H's obstruction work is the "balance defect" of the partner's necklace over the torus-type states of the class. It is not an AC invariant, and I have no proof that it persists.
2. **Constructive next step: exact moves beyond torus groups.** The same machinery works for any frozen relator with a computable conjugacy invariant. The next targets are Baumslag–Solitar-type relators (HNN normal forms with Collins' lemma), which would join the torus island to D's 34 MS(3,w) members, and two-bridge knot relators. A meridian (defect 2) or primitive state reachable through such moves would trivialize AK(3) with a certificate, through `g_cert.py` and the Euclid exit §2.4. A combined torus/BS graph is the cheapest experiment not yet done.
3. **For H and I.** Lemma G4 turns "one-move-to-primitive" into a finite computation at every torus-type state. It can be run on any torus-type state found by other searches; the C3/C4 graphs above are ready to rerun.

## 7. Files written

- `research/research-g.md` (this note).
- `experiments/g_torus.py`: torus-group conjugacy invariant, GL(2,Z) → Aut(F₂), torus-type edge enumeration, torus-graph BFS, Christoffel words, `primitive_complete` (Lemma G4), self-test.
- `experiments/g_cert.py`: compiler from exact torus ACM moves to strict elementary certificates (normal-form rewriting with checked relator insertions, θ-coordinate views, exact inverse automorphisms, primitive finish, swap), self-test.
- `certificates/g_ak3_to_trefoil_t2_7.json`, `certificates/g_ak2_torus_acm_trivialization.json`.

## References

- S. Akbulut, R. Kirby, Topology 24 (1985).
- W. Magnus, A. Karrass, D. Solitar, *Combinatorial Group Theory* (conjugacy theorem in free products, Thm 4.2; amalgams Ch. 4).
- J. Nielsen (Out(F₂) = GL(2,Z)); R. P. Osborne, H. Zieschang, *Primitives in the free group on two generators*, Invent. Math. 63 (1981); M. Cohen, W. Metzler, A. Zimmermann, *What does a basis of F(a,b) look like?*, Math. Ann. 257 (1981); J. Berstel, A. Lauve, C. Reutenauer, F. Saliola, *Combinatorics on Words: Christoffel Words and Repetitions in Words* (CRM, 2008).
- M. Lackenby, arXiv:2606.06122 (abstract via search).
- R. Gompf, M. Scharlemann, A. Thompson, Geom. Topol. 14 (2010), https://msp.org/gt/2010/14-4/gt-v14-n4-p13-s.pdf (snippet).
- E. Romary, A. Zupan, Geom. Dedicata (2024), https://link.springer.com/10.1007/s10711-024-00891-6 (snippet).
- D. Panteleev, A. Ushakov, arXiv:1609.00325.
- Repository notes research-a … research-f (Lemma D3, Lemma D6, Proposition F3 are used as stated there).
