# Excluding two six-instruction excursions at one added pair

2026-11-19. At total budget 20 for AK(3), a one-padding candidate in degree ten or in the free group has either one degree-nine active interval of length at least eight or two active intervals with lengths at least six and seven. The degree-five group census also gives an exact compact layout for the breadth-first search that is still running. [Marked corridor counts](../results/round13_stable_disproof_two_sixes.json) · [Isolated width-seven checks](../results/round13_stable_disproof_width_seven.json) · [Degree-five group census](../results/round13_stable_disproof_d5_fibers.json)

## Two six-instruction intervals

The length-20 one-padding branch has 18 effective instructions after erasing the added generator and truncating to degree nine. The only possible short form after round twelve has two intervals with three nonidentity rows, each of length six, and six other instructions between idle vertices. Each interval must be one of the 136 residual templates from the strict-savings comparison. The same reduction applies to a reversed interval because a shorter reversed idle replacement would give a shorter forward replacement. [Round-twelve width and multiplicity proof](round-12-stable-disproof.md#isolated-intervals-in-the-degree-nine-one-padding-retraction)

Track the mod-two coefficient of the added variable through the templates. Mark the formal initial active rows by zero and the added row by one. Propagate the marks using row addition for either sign of a product. Inversion and conjugation preserve the marks. All 136 surviving terminal templates give a unique marked endpoint under this starting assignment. For actual starting marks $u_a,u_b$, add $u_a\deg_a(w)+u_b\deg_b(w)$ modulo two to the recorded mark of each surviving formal word $w$. This follows by induction because the change in a row's mark obeys the same linear recurrence as the formal exponent vector. The identity after return has mark one. [Marked template generator](../experiments/round13_stable_disproof_templates.py)

In the degree-six rank-two quotient, allow a template transition whenever its final cancellation relation holds. Projecting from degree nine preserves this equality, so the transitions include every admissible interval. Use the attached marked endpoint for that transition. The ordinary transitions at idle vertices act on the two active rows and transport the marks. Include an idle wait to accommodate any such instruction that becomes trivial in degree six.

Cut immediately after the third of the six idle instructions. The two halves each have three idle instructions and altogether have two intervals. From each marked endpoint the exact table enumerates every order of the permitted idle and interval transitions. The three required comparisons have interval counts $(2,0)$, $(1,1)$ and $(0,2)$. The occurrence of a positive meeting in the degree-five control is only a property of the relaxed lower-quotient test.

| Quotient degree | Two intervals on the AK(3) side | One interval on each side | Two intervals on the basis side |
| --- | ---: | ---: | ---: |
| 5 | 12 | 2 | 0 |
| 6 | 0 | 0 | 0 |

The degree-six search checks 19,462,284 and 9,813,423 transitions at the two streamed boundaries. Thus either there is a single interval or the two interval lengths are at least six and seven. [Native exact cut](../experiments/round13_stable_disproof_two_sixes.cpp)

## The isolated seven-instruction interval

An isolated width-seven interval with an idle replacement of at most six instructions would give a path of length at most 17 in degree nine. Its endpoints would lie at ticks $t$ and $t+6$ of the saturated corridor of length 17. The exact active-half comparisons at depths three and four are disjoint for all twelve values of $t$. This already excludes a strict saving without requiring an auxiliary mark in the geodesic comparison. [Saturated corridor](round-12-stable-disproof.md#isolated-intervals-in-the-degree-nine-one-padding-retraction)

The same symbolic comparison as in round twelve, now with five interior instructions and a radius-six ordinary ball, leaves 5,730 distinct terminal cases. A sole interval has x,y-pure active rows on both sides and the identity row projects from literal $z$. Along all outside idle edges, a move involving the projected identity would either wait in degree nine or start an active interval. Thus these edges involve only the original letters and the two active rows. In the symbolic interval, require the sole nonzero $z$ coefficient to be on the recipient just before the last cancellation. This gives 1,440 terminal cases.

For each of the six ordered independent choices of the old mod-two exponent vectors, lift the compatible marked instructions to the rank-three degree-two quotient. Check that every mixed quadratic coefficient involving $z$, including $z^2$, vanishes after the last move. The coefficients depend on the old linear terms and on the intervening instructions. They are independent of which pure quadratic terms the two initial active rows have, because a degree-two product can combine a $z$ coefficient only with a degree-one term. This leaves the same eight templates for all six choices. [Symbolic and mixed-coefficient checks](../experiments/round13_stable_disproof_width_seven.py)

Let $a$ be the active row copied at birth and $b$ the other. Each of the eight templates uses a signed original letter $g$. Write $B=g a^3 g^{-1}$. In one form put $C=a^{-2}B$. The last equality is $C^{-1}=C a^{-2}$, so $C^2=a^2$. The surviving conjugated row is $a^2 C^{-1}=C$. In the other form put $C=B a^{-2}$. The last equality is $C=a^4 B^{-1}$, again giving $C^2=a^2$ with surviving row $C$. The other surviving row is $b$ in both forms. Because the removed row becomes literal $z$ at the end of the interval, the equality between the removed and signed donor words holds after original-degree erasure. In the free case it also holds after projection to degree ten.

The equality $C^2=a^2$ in degree ten implies $C=a$ through degree nine in these forms. If $C-a$ had a first nonzero homogeneous term $E$ of degree $d\le9$, then $d\ge2$ because the linear parts agree. Writing $L$ for their nonzero common linear term, the degree-$(d+1)$ part of the square equality gives $LE+EL=0$. In the free associative algebra a homogeneous element commuting with a nonzero linear form is a scalar power of that form. To see this, change linear coordinates to make $L$ a generator. The equality forces every monomial of $E$ to start with that generator, and cancellation and induction give the claim. Erase one of the original generators so that $L$ has a nonzero rank-one image. The rank-one images of $C$ and $a$ coincide, since the conjugation in $B$ disappears and $a^{-2}a^3=a$. This rules out a nonzero image of $E=L^d$. The surviving pair in degree nine is therefore $(a,b)$, which gives a strict saving. This excludes the last eight templates and raises the isolated interval bound to eight instructions.

## Compact degree-five storage

The independent group census enumerates 524,288 degree-five elements by right multiplication with the two positive generators. Projection yields 8,192 degree-four elements with 64 preimages each. The three nonzero degree-one parity classes each contain 2,048 degree-four elements. A pair with independent parity vectors uses two distinct nonzero classes. Sorting the rows by parity class fixes the orientation without affecting the unordered search. It gives exactly $3\cdot 2{,}048^2=12{,}582{,}912$ possible degree-four pair indices. Each index has $64^2=4{,}096$ aligned degree-five lifts. [Exact census](../experiments/round13_stable_disproof_d5_fibers.cpp)

A direct index can concatenate the degree-four pair index and the two six-bit fiber slots. Store the first-arrival depth zero through ten or an unseen flag in a four-bit field. The whole per-side table takes 24 GiB, with a 6 GiB one-bit layout for a single subset such as a frontier. The prescribed degree-four layers can use one bit per pair per layer. Ordinary moves can still use the existing exact degree-five operations, then map each resulting row back to its fiber slot. For faster transitions, the degree-five kernel is central and elementary abelian. In homogeneous coordinates a product adds the two kernel vectors and the offset computed from the chosen representatives, while inversion and conjugation add an offset to the one input vector. This removes the need for a hash record for each visited degree-five pair. The group census is complete. The smaller frontier layout has been specified and the original degree-ten search continues with its existing implementation.

## Reproduction

~~~sh
work=/tmp/ac-r13-stable-disproof
mkdir -p "$work"
python3 -B experiments/round13_stable_disproof_templates.py > "$work/marked.txt"
c++ -std=c++17 -O3 experiments/round13_stable_disproof_two_sixes.cpp -o "$work/two-sixes"
"$work/two-sixes" 5 < "$work/marked.txt"
"$work/two-sixes" 6 < "$work/marked.txt"
python3 -B experiments/round13_stable_disproof_width_seven.py \
  | diff - results/round13_stable_disproof_width_seven.json
c++ -std=c++17 -O3 experiments/round13_stable_disproof_d5_fibers.cpp -o "$work/d5-fibers"
"$work/d5-fibers"
~~~
