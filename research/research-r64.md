# Research R6-4: relator stabilizers at the torus states of C4's class

Date: 2026-11-10 (UTC). Agent R6-4, round 6. Time-boxed (≈25 min; a first attempt was lost to a
container restart).

**Status (in progress).** Theory: the Lemma-M contributions at the known torus states of C4's
class are classified (all lie in D₆) and a class-wide "eigenline" criterion is proved. A targeted
search of the conjugacy class of x⁸y⁵ in G_A = F/⟨⟨x⁴yXy⟩⟩ for T(2,n)-type and Baumslag–Solitar-type
representatives is running. **Not achieved so far:** no element of Ŝ(C4) outside D₆.

Notation: F = F(x,y), X = x⁻¹, Y = y⁻¹; A = x⁴yXy; s₅ = x⁸y⁵; s_w = xy³xY²; C4 = (A, s_w);
T(4;8,5) = (s₅, A); z = Xy, so y = xz and A = x⁵z² up to rotation; G_A = F/⟨⟨A⟩⟩ = ⟨x,z | x⁵z²⟩;
Π = G_A/⟨x⁵⟩ = ⟨a⟩₅ * ⟨b⟩₂ (a = x̄, b = z̄). D₆ = ⟨−I, M₁, M₂⟩ ⊆ Ŝ(C4) (research-n N3,
research-th02 Cor. 2). Stab[r] = stabilizer in Out(F₂) = GL₂(ℤ) of the cyclic word r up to inversion.

## 1. Lemma-M contributions at the torus states (proved here, using research-th02 Prop. 7)

Recall Lemma M (research-th15 §2 = research-th02 Lemma 0): if φ(s) is conjugate in F to s^{±1}
("s frozen") and φ(r) is conjugate to r^{±1} in G_s = F/⟨⟨s⟩⟩, then φ(r,s) ~AC (r,s). So **every
automorphism class produced by Lemma M at a state (r,s) lies in Stab[r] ∪ Stab[s]**, and it is
produced iff it moves the *other* relator inside its G-conjugacy class up to inversion.

**Proposition 1 (the known torus states).** Let β_A = [[1,−3],[0,−1]] (x ↦ x, y ↦ xYX⁴, the hidden
reflection of A = z²x⁵ in the basis (z,x)), β_w = M₁ = [[−1,0],[−1,1]] (the hidden reflection of
s_w = w²y⁵, w = xY²). Then:

| state | frozen relator, type | Stab[·] in GL₂(ℤ) | inner on the 1-relator group | realized by Lemma M |
|---|---|---|---|---|
| T(4;8,5) | s₅ = x⁸y⁵, T(5,8) | {±I} | I only | ±I (ι(A) is a rotation of A⁻¹ in F) |
| T(4;8,5) | A = z²x⁵, T(2,5) | {±I, ±β_A} | I, β_A | all four (ι(s₅) is a rotation of s₅⁻¹) |
| C4 | A, T(2,5) | {±I, ±β_A} | I, β_A | all four (ι(s_w) is a rotation of s_w⁻¹) |
| C4 | s_w = w²y⁵, T(2,5) | {±I, ±β_w} | I, β_w | all four (ι(A) ~ A⁻¹) |

All these lie in D₆; the state T(4;8,5) alone yields only {±I, ±β_A} (order 4), and C4 yields
⟨±β_A, ±β_w⟩ = D₆ (research-th02 Cor. 2). *Proof.* Stab[x^p y^q] = {±I} for |p|,|q| ≥ 3 and
Stab[u²vⁿ] = {±I, ±β} (n odd, |n| ≥ 3) is research-th02 Prop. 7 (Whitehead's theorem, externally
reported, classical), transported by the basis change (Stab[α(r)] = αStab[r]α⁻¹). The hidden
reflection β induces the identity on G_r (th02 Thm 1(2)). ι = (x ↦ X, y ↦ Y) and ιβ act on
G_r^{ab} ≅ ℤ by −1, so they are not inner; by Lemma M they are realized iff ι(partner) is conjugate
to partner⁻¹ in G_r, which holds already in F for all three partners: ι(x⁸y⁵) = X⁸Y⁵ is a rotation
of Y⁵X⁸, ι(A) = X⁴YxY is a rotation of A⁻¹ = YxYX⁴, ι(s_w) = XY³Xy² is a rotation of s_w⁻¹ =
yyXYYYX. ∎

So, at these states, **no element outside D₆, and in particular no transvection or element of
infinite order, comes from a relator stabilizer.** A single torus-type relator (exponents ≥ 2 in
absolute value in some basis) can only ever contribute elements of order ≤ 2 (its Stab is
{±I} or {±I, ±β}); an element of infinite order from one relator needs Stab[r] infinite, which
for a Lemma-T relator x⁻¹y^m x y^{−n′} holds and for torus-type relators never does.

## 2. A class-wide criterion (proved here)

**Theorem 2 (eigenline criterion).** The six reflections of D₆ are ±M₁, ±M₂, ±M₃ with
M₂ = [[−1,3],[0,1]] = −β_A and M₃ = M₁M₂M₁ = [[2,−3],[1,−2]]; their eigenline pairs
{(−1)-line, (+1)-line} are

    M₁: {(2,1), (0,1)},   M₂: {(1,0), (3,2)},   M₃: {(1,1), (3,1)}     (vectors = [x],[y]-coordinates).

Suppose some state (r, s) ~AC C4 has a relator r conjugate to (u²vⁿ)^{±1}, (u,v) a basis of F,
n odd, |n| ≥ 3. If the unordered pair {ℚ·ab(r), ℚ·([v])} is not one of these three pairs, then
Ŝ(C4) is infinite. Likewise, if some state ~AC C4 has a relator conjugate to α(x⁻¹y^m x y^{−n′})^{±1}
(α ∈ Aut(F₂)), then Ŝ(C4) contains the transvection αT₁α⁻¹ and is infinite.

*Proof.* D₆ = {±I} × ⟨M₁, M₂⟩ with ⟨M₁,M₂⟩ ≅ S₃ = {I, R, R², M₁, M₂, M₃} (R = M₁M₂ of order 3);
the elements of determinant −1 are exactly ±M₁, ±M₂, ±M₃, each an involution with eigenvalues ±1,
and −M has the eigenlines of M interchanged. Eigenlines: direct computation (e.g. M₃(3,1) = (3,1),
M₃(1,1) = −(1,1)). The hidden reflection β_r of r (th02 Thm 1(5)) has (−1)-line ab(r) and
(+1)-line [v] and lies in Ŝ((r,s)) = Ŝ(C4) (th02 Thm 1(4); Ŝ is a class invariant, th15 Lemma 0).
A reflection is determined by its two eigenlines, so β_r ∈ D₆ iff its pair is one of the three. If
β_r ∉ D₆ then ⟨D₆, β_r⟩ ⊆ Ŝ(C4) strictly contains the maximal finite subgroup D₆ (research-n §3.2),
hence is infinite. For the BS case: ab(x⁻¹y^m x y^{−n′}) = (0, m − n′), and since (r,s) presents the
trivial group, ab(r) = ab_α-image of (0, m−n′) is primitive, so |m − n′| = 1; Lemma T (th15) gives
T₁ ∈ Ŝ((α⁻¹(r), α⁻¹(s))) = α⁻¹Ŝ(C4)α (Lemma D2 transport), i.e. αT₁α⁻¹ ∈ Ŝ(C4), of infinite order. ∎

So **"Ŝ(C4) = D₆" (i.e. C4 a counterexample) implies that every T(2,n)-type relator anywhere in the
class carries one of only three eigenline pairs, and that no relator of Baumslag–Solitar type
occurs anywhere in the class.** Conversely a single relator violating this settles the dichotomy
in the "infinite" direction. (research-th02 §4 found that all hidden reflections at relators of
length ≤ 15 in Fwd(C4, 28) lie in D₆; research-th15 §7 found no BS relator in Fwd(C4, 30).)

## 3. The two frozen families of T(4;8,5) (proved reduction + bounded search)

By Lemma M with φ = id, the class of C4 contains the **A-frozen family** {(A, s′) : s′ ~ s₅^{±1} in
G_A} and the **s₅-frozen family** {(A′, s₅) : A′ ~ A^{±1} in G_{s₅}}, G_{s₅} = ⟨x,y | x⁸y⁵⟩. These
are infinite families; Theorem 2 applies to every T(2,n)-type or BS-type word in them.

**Lemma 3 (exact conjugacy test; proved here).** Let G = ⟨x,y | r⟩ with r = x⁸y⁵ or r = A. Then
ζ (= x⁸, resp. x⁵) is central of infinite order, G/⟨ζ⟩ = Π is ℤ/8 * ℤ/5 (x ↦ a, y ↦ c), resp.
ℤ/5 * ℤ/2 (x ↦ a, y ↦ ab), and the character χ: G → ℤ (χ = (5,−8), resp. (2,−3) on (x,y)) has
χ(ζ) = 40, resp. 10 ≠ 0. Hence g ~ g′ in G ⟺ ḡ ~ ḡ′ in Π and χ(g) = χ(g′).
*Proof.* If ḡ′ = h̄ḡh̄⁻¹ then g′ = hgh⁻¹ζ^j for a lift h, and χ(g′) = χ(g) + χ(ζ)j forces j = 0.
Conjugacy in a free product of cyclic groups is decided by cyclically reduced normal forms up to
rotation (Magnus–Karrass–Solitar Thm 4.2; externally reported, classical). For r = A: x⁵z² = 1
with y = xz gives G/⟨x⁵⟩ = ⟨a,b | a⁵, b²⟩. ∎

**Proposition 4 (same-basis torus forms are rigid; proved here).** (a) x^p y^q ~ s₅^{±1} in G_A iff
(p,q) = ±(8,5). (b) x^a yXy ~ A^{±1} in G_{s₅} iff a = 4. So T(4;8,5) (with its ι-image) is the only
pair of the shape (x^p y^q, x^a yXy) on either frozen family; I's Lemma S (exponent shift by
m = a+1 = 5) has no partner of T(4;8,5), and TH17's third torus form (Theorem 4 there, which uses
the braid structure of the trefoil group, a = 2) has no analogue established for C4's class.
*Proof.* (a) In Π = ⟨a⟩₅ * ⟨b⟩₂, for q ≥ 1: x^p y^q ↦ a^{p+1}b(ab)^{q−1}, cyclically reduced with
q b-syllables and a-exponent necklace [p+1, 1^{q−1}] if p+1 ≢ 0 (5), and reducing to q−2
b-syllables with necklace [2, 1^{q−3}] if p+1 ≡ 0; x^p y^{−q} ↦ a^{p+4}b(a⁴b)^{q−1} (Y ↦ ba⁴), with
necklace [p+4, 4^{q−1}], resp. [3, 4^{q−3}] if p+4 ≡ 0. s₅ ↦ a⁴b(ab)⁴, necklace [4,1,1,1,1];
s₅⁻¹ ↦ [1,4,4,4,4]. Five b-syllables are needed. [2,1⁴] and [3,4⁴] match neither target;
[p+1,1⁴] = [4,1⁴] gives p ≡ 3 (5) and χ = 2p − 15 = 1 gives p = 8; [p+4,4⁴] = [1,4⁴] gives
p ≡ 2 (5) and χ = 2p + 15 = −1 gives p = −8; the mixed combinations have the wrong necklace;
q = 0 is elliptic. (b) In ℤ/8 * ℤ/5,
x^a yXy ↦ a^a c a⁷ c with necklace ((a,1),(7,1)), A⁻¹ ↦ ((1,4),(4,4)); equality forces a ≡ 4 (8)
and χ = 5(a−1) − 16 = −1 forces a = 4. ∎ (Brute-force confirmation for |p|,|q|,|a| ≤ 40:
`r64_search.torus_scan` returns ([(−8,−5),(8,5)], [4]).)

**Experiment 5 (bounded; exact recognizer).** `experiments/r64_search.py` enumerates bases (u,v)
of F by Nielsen moves up to |u|+|v| ≤ L, forms u²vⁿ (n odd) and u⁻¹v^m u v^{−(m±1)}, and tests
membership in the relevant conjugacy class with Lemma 3; for each T(2,n)-hit it computes the hidden
reflection and tests membership in D₆.

| family | L, range | distinct hit words | hidden reflections | BS-type hits |
|---|---|---|---|---|
| A-frozen (s′ ~ s₅^{±1} in G_A) | L = 12, \|n\|,\|m\| ≤ 15 | 140 (all n = ±5) | only M₁ = β_w | 0 |
| s₅-frozen (A′ ~ A^{±1} in G_{s₅}) | L = 10, \|n\|,\|m\| ≤ 15 | 138 (n ∈ {±5, ±11}) | only β_A = −M₂ | 0 |

So in both families every T(2,n)-type representative found carries **the same** hidden reflection
as the visible one at T(4;8,5)/C4 (on the A-side: s_w; on the s₅-side: A itself), and none lies
outside D₆. (Example of a new torus-type state: (x⁸y⁵, x⁷yX⁴y) ~AC T(4;8,5), with x⁷yX⁴y of type
T(2,11), hidden reflection β_A.) This is a bounded search, not a proof that no such word exists.

## 4. What would settle the dichotomy, and failed attempts

**Corollary 6 (proved; reformulation).** Ŝ(C4) is infinite as soon as *one* of the following
occurs at *one* state AC-equivalent to C4: (i) a T(2,n)-type relator (|n| ≥ 3 odd) whose eigenline
pair is not one of the three of Theorem 2; (ii) a relator of Baumslag–Solitar type
α(x⁻¹y^m x y^{−(m±1)}); (iii) a relator r and φ ∈ Stab[r] \ D₆ with φ(partner) conjugate to
partner^{±1} in G_r. Conversely, if C4 is a counterexample (Ŝ(C4) = D₆), none of (i)–(iii) ever
occurs in the class. *Proof.* (i), (ii): Theorem 2. (iii): Lemma M gives φ ∈ Ŝ(C4), and any element
outside the maximal finite subgroup D₆ generates with D₆ an infinite group. ∎

Note that (i)–(iii) with a torus-type relator r (|p|,|q| ≥ 2 in some basis) can only produce
reflections or ±I (Stab[r] has order ≤ 4 mod Inn), so at torus states the only route to an
infinite-order element is a *reflection outside D₆*, which then multiplies with a reflection of D₆
to a unipotent or hyperbolic element. For instance, with M₁ ∈ D₆ and a hypothetical reflection β
with (−1)-eigenvector ρ and (+1)-eigenvector v, normalized by det(v, ρ) = 2 (as for every hidden
reflection), research-th02's trace formula gives tr(M₁β) = 2 − D with D = det(v₁, v)·det(ρ₁, ρ),
v₁ = (0,1), ρ₁ = (−2,−1) (the identity tr = 2 − D is th02's Plücker computation, which does not
need det(ρ₁,ρ) = ±1; that hypothesis only makes D odd). Since det(M₁β) = 1, any D ∉ {0,…,4}
gives an element of infinite order directly.

**Failed attempts / negative findings (this session).**
1. *Hidden reflections in the frozen families* (Experiment 5): every T(2,n)-type representative
   found carries the same reflection as the visible relator (M₁, resp. β_A); none outside D₆.
   Bounded (basis length ≤ 12 / ≤ 10 so far, see §5 for the larger runs).
2. *BS-type representatives in the frozen families*: none found (same bounds). This is consistent
   with research-th15 §7 (no BS relator in Fwd(C4, 30)); it is not a proof that none exists.
3. *A third torus form for a = 4*: TH17's Theorem 4 rests on Δ = uvu in B₃ (a = 2); I did not find
   an analogue for ⟨x,z | x⁵z²⟩, and Proposition 4 shows that no same-basis torus pair other than
   T(4;8,5) lies on the two frozen families. The new T(2,11)-type state (x⁸y⁵, x⁷yX⁴y) found by
   the search lies on the s₅-frozen family and gives only β_A.
4. *Explaining "one reflection per family"*: I tried to prove that all T(2,n)-type representatives
   of a fixed conjugacy class of G_A (resp. G_{s₅}) have the same hidden reflection (via generating
   pairs of ℤ/5 * ℤ/2, resp. ℤ/8 * ℤ/5, and the image ū²v̄ⁿ); not completed. **Open.**

## 5. Honest limits and what remains open

- **The dichotomy is not settled.** No element of Ŝ(C4) outside D₆ was found, and nothing here
  proves Ŝ(C4) = D₆. All negative statements beyond Propositions 1, 4 are bounded searches.
- Proposition 1 is essentially research-th02 Prop. 7 + Cor. 2 applied state by state; the new
  content is the complete table (which elements are inner, which preserve the partner), the
  class-wide criterion Theorem 2 / Corollary 6, the exact conjugacy test Lemma 3 for the two
  frozen families, and the rigidity statement Proposition 4.
- Theorem 2 only uses *hidden* reflections and Lemma T; Lemma M with a non-hidden stabilizer
  element (Corollary 6(iii)) at non-torus states (e.g. th02's ε_x-candidates r₁, Prop. 11 there)
  is not examined here; th02's Prop. 11 candidate remains the most concrete open lead.
- Open questions made precise here: (Q1) Is every T(2,n)-type representative of the class of s₅
  in G_A of hidden reflection M₁, and every one of A's class in G_{s₅} of reflection β_A (true for
  all found)? (Q2) Does either frozen family contain a Baumslag–Solitar-type word (none found)?
  A "yes" to (Q2) or a "no" to (Q1) proves Ŝ(C4) infinite (Theorem 2); both are now pure
  conjugacy questions in ⟨x,z | x⁵z²⟩, resp. ⟨x,y | x⁸y⁵⟩, decidable word by word by Lemma 3.
- An affirmative answer to (Q1)/(Q2)-type questions for the two frozen families would *not*
  prove Ŝ(C4) = D₆: other states of the class (reached by moving both relators) are not covered.
