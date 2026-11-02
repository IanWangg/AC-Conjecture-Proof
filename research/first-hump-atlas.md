# First-departure catalogue, exact new paths, and blocked primitive shortcuts

Date: 2026-11-02. Coordinating-agent investigation, developed with K, L and
M. **No AK(3) trivialization or global AC invariant is claimed.** Novelty
is not established.

Write X=x^-1, Y=y^-1 and

    p=xxxYYYY, b=xyxYXY, r=XXyxYxxY, s=XXXyxYxxY.

The purpose was to leave the initial cyclic plateau and seek an actual
primitive free relator, which would permit a complete ordinary AC proof.
This investigation produced exact new ordinary paths and precise reasons
that the attempted primitive completions fail.

## 1. Exact first-departure enumeration

With the other coordinate kept literally at its initial relator, the
first possible increases to total cyclic length 15 are a length-eight
replacement of b or a length-nine replacement of p. A/F prove the minimum
lengths and exclude the intervening parity/near-equality cases.

The central quotients used to decide these replacement conditions have
exact conjugacy tests. In B3, a free-product C2*C3 cyclic necklace plus
total exponent sum determines a conjugacy class: lift a quotient
conjugator, and the remaining central power is detected by exponent sum.
In T(3,4), use the C3*C4 necklace plus character 4 exp_x+3 exp_y in the
same way. These are exact infinite-group tests, not finite sieves.

Exhausting the cyclically reduced words gives:

| Replacement | Literal words | Cyclic/inverse classes |
|---|---:|---:|
| b, length eight, with p fixed | 32 | 2 |
| p, length nine, with b fixed | 432 | 24 |

The two braid classes are represented by r and xyXXYxxY. They are
transported into one another by simultaneous inversion of x,y, together
with rotation/inversion of the relators. The 24 power classes split into
six four-element classes under simultaneous inversion and swapping x,y.
The complete representatives are in `results/first_hump_results.json`.
This is a first-update catalogue; it does not classify the entire
cyclic-length-15 component after subsequent changes of both coordinates.

## 2. Ordinary entry certificates

The file `certificates/first_hump_entry.json` is a 56-strict-move path from
(p,b) to (p,r), with raw peak 42. It uses the exact free identity

    r b^-1 = product_i q_i p^(epsilon_i) q_i^-1,

with (epsilon,q) equal to

    (+,XXy), (-,XX), (+,xyxYXXX), (-,xyxYXXXy).

The donor p is explicitly conjugated/inverted, used and restored. Each
left product is expanded by recipient inversions and positive right
multiplication. No quotient equality is inserted as an elementary move.
M subsequently improves this entry to 44 strict moves with raw peak 18.

For (s,b), first conjugate p by yXX. The difference between s and that
conjugate is the product of three negative braid cells with conjugators

    XXyxYXY, XyxYXY, yxYXY.

The saved 48-strict-move path has exact endpoint (s,b) and raw peak 19.
Both entries pass the independent strict elementary verifier.

## 3. Two new exact deletion models

For F/<<r>>, put t=x, a=X^2 yx, d=Xy. Direct inverse presentation changes
give

    F/<<r>> = F(a,d) semidirect_alpha Z,
    alpha(a)=d, alpha(d)=a d^-1.

The inverse sends a to da and d to a. Write fiber letters as a,b in the
program. Then

    p^-1 = (abbAbA)t,    xY=bA.

By Nielsen primitive conjugacy uniqueness, all primitive candidates with
the required total exponent sum one are (xY)^k x. Thus the sought
conjugacy becomes

    q (abbAbA) alpha(q)^-1 = (bA)^k.

A bounded exact fiber-conjugator search found no solution through length
14. That failure alone proves nothing unbounded. K subsequently supplies
the unbounded exclusion in an explicit finite group: its complete twisted
orbit misses all eight candidate powers. See [K](research-k.md).

For F/<<s>>, put t=x, a=y, d=xyX, e=xxyXX. Exact presentation changes give

    alpha(a)=d, alpha(d)=e, alpha(e)=a d^-1,
    b=(d e^-1 d^-1)t.

The inverse sends a to ea, d to a and e to d. All primitive candidates
are y^k x, with fiber coefficient a^k. An exact bounded search through
fiber length ten found no conjugator; K's independent mod-five finite
certificate then excludes every k at all lengths. See [the rank-three
follow-up](research-k-rank3.md). These results prevent only one-coordinate
primitive replacements at the selected tuples.

## 4. Positive twisted conjugacies produce new actual AC paths

K's finite short-word filter left six length-seven candidate classes in
F/<<r>>. Two of the new candidates have exact free-fiber identities:

    q=aBB: q(abbAbA)alpha(q)^-1 = aBBa,
    q=BB:  q(abbAbA)alpha(q)^-1 = BBab.

They correspond to original words

    u1=yXYXyxx,    u2=YxYXyyx.

M independently checks these identities, constructs exact free-word
fillings by r, and compiles ordinary ledgers. The improved complete
AK(3)-starting certificates have these values:

| Exact endpoint | Strict moves | Raw peak |
|---|---:|---:|
| (p,r) | 44 | 18 |
| (u1,r) | 222 | 31 |
| (u2,r) | 179 | 25 |

These are genuine positive AC-equivalences, not assertions based only on
finite quotient survival. The full free endpoints are not the basis.

Both further primitive strategies fail. In F/<<u1>>, the free basis
U=X, V=XY gives the ordinary braid quotient: u1 becomes YxyxYX in U,V,
a cyclic rotation of its braid relator. The other relator becomes
`xxYXyXXXy`, of absolute SL(2,Z) trace 14 and total exponent sum -1.
J's primitive trace sequence 2,4,10,26,... excludes a primitive conjugate.

For F/<<u2>>, use stable letter t=y, fiber a=x, d=yxY, and the same
rank-two alpha as above. Here r^-1=(D A d^2)t and primitive candidates are
a^k t. The mod-two filter leaves k=2 modulo eight, but this is a false
positive: K's separate mod-five finite group misses all five candidate
powers. See [K's further-state proof](research-k-second-hump.md).

## 5. Whole-subgroup primitive tests and an important scope correction

Checking only the displayed coordinates misses a possible completion:
their generated subgroup might contain a different ambient primitive.
We therefore tested the full signed-cycle structure, not just the words.

It is insufficient to test one canonical rotation of a recipient:
rotating one relator can change its generated subgroup. All 464 literal
replacement words were retained, and the frozen original relator was
then also allowed every cyclic rotation and inverse. This gives

    432*12 + 32*14 = 5,632 literal pairs.

M proves that every generated subgroup in this list contains no ambient
primitive at any word length. A primitive cyclic word in rank two has
only one sign of each generator; if both generators occur, at least one
is isolated throughout the cyclic word. For each signed alphabet the
finite graph checks show that every closed path instead contains both
repeated-letter patterns. The argument also excludes one-generator
primitive loops.

The coordinating agent independently repeats the audit using I's folding
implementation and a directed-edge DFS. Removing transitions with one
selected repeated letter leaves a DAG in every case: 5,632 pairs times
four alphabets times two letters. The two actual new waypoints also pass.
The independent result is `results/hump_subgroup_independent_review.json`.

This literal finite catalogue does **not** cover arbitrary independent
conjugating tails, arbitrary later AC moves, or the whole normalized AC
component. No new cyclic peak bound follows. It excludes a Nielsen-only
completion from these particular literal pairs, not unrestricted AC
triviality.

## 6. Two additional analytic power classes and the next open work

L independently verifies two further power classes. The word XXXX Y xxx y
gives BS(3,4), where the braid has cyclic Britton length three and every
primitive candidate has length one. The word XXXyXYxxy returns to the
rank-two free-by-cyclic model with a primitive family stably conjugate to
K's excluded family. Together with the rank-three branch, three of the
six power-departure symmetry classes have frozen-coordinate primitive
exclusions. See [L's analytic follow-up](research-l-branches.md).

The other three classes and later changes of both coordinates remain
available research directions. The exact new edges, finite exclusions,
subgroup tests and nonlinear lifting defect narrow attempted routes;
they do not replace the original objective with a quotient or bounded
search problem. A complete free-group path or global obstruction is
still missing.

## Reproduce

All Python scripts reside together in `experiments/` and use the standard
library:

```sh
python3 experiments/first_hump.py --entry-output certificates/first_hump_entry.json \
  --power-entry-output certificates/power9_entry.json --output results/first_hump_results.json
python3 experiments/elementary_verify.py certificates/first_hump_entry.json certificates/power9_entry.json
python3 experiments/audit_hump_subgroups.py
c++ -std=c++17 -O3 experiments/twisted_primitive_search.cpp -o /tmp/ac_twisted_search
/tmp/ac_twisted_search 14 2 aBBa
/tmp/ac_twisted_search 14 2 BBab
```

The C++ positive hits are checked again by exact free-fiber substitution
in `first_hump.py`; its bounded misses are never used as unbounded
obstructions. The later ordinary certificates and frozen-coordinate
proofs have their own reports and replay commands.
