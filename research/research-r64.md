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
