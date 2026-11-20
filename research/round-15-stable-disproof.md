# Central refinements at degree six and two marked intervals

2026-11-19. At stable budget 20 for AK(3), a one-padding path cannot have its two degree-nine active intervals of widths six and seven. It would need widths at least six and eight, or at least seven each. Separately, the rank-two characteristic-two Magnus projection from degree six to degree five has an elementary abelian kernel of dimension 11. An opt-in corridor mode now adds those coordinates one at a time and reproduces the full-degree controls and their independently replayed ledgers. [Marked width-six and width-seven cut](../results/round15_stable_disproof_two_widths.json) · [Central-kernel census](../results/round15_stable_disproof_d6_kernel.json) · [Partial-tier controls](../results/round15_stable_disproof_partial_controls.json)

## Exact degree-six kernel

Let $G_d$ be the rank-two Magnus image after truncating above degree $d$. The kernel of $G_6\to G_5$ consists of images $1+u$ with $u$ homogeneous of degree six. Two such images multiply by adding their $u$ terms. Multiplication by any positive-degree term raises degree beyond six, so the kernel is central.

Enumerate the complete degree-five group with right multiplication by the two positive generators and keep one degree-six representative $t(q)$ for each degree-five element $q$. For each positive directed edge $q\to qg$, the element $t(q)g\,t(qg)^{-1}$ lies in the central kernel. These elements generate it. For an arbitrary word representing a kernel element, insert the representatives of its successive degree-five positions between adjacent letters. The resulting factors are the listed positive edge elements or their inverses. The product telescopes to the original word.

The census has 524,288 degree-five elements and 1,048,576 positive edges. There are 507,220 nonidentity edge images, whose binary span has dimension 11. An echelon basis has leading coefficients at lexicographic degree-six indices $1,3,5,7,9,11,13,15,23,27,31$. The complete echelon vectors are in the receipt. The corresponding coordinate functionals are independent on the kernel. [Schreier generator census](../experiments/round15_stable_disproof_d6_kernel.cpp)

## Partial top-degree corridor stages

Discarding any subspace of the top homogeneous degree defines an exact algebra quotient, since both left and right multiplication by positive-degree terms annihilate that subspace. The new native flag `--partial-degree-six` keeps all coefficients through degree five. It inserts ten masked degree-six stages, using the first ten independent coordinates cumulatively. It then lifts to full degree six, which adds the final independent coordinate. At each stage the existing first-arrival or layered procedure refines the previous allowable corridor by the projection that forgets a coordinate. A rank-two pair has at most four lifts per step because each row gains just one binary coordinate. Without the flag the executable lifts directly between the two full-degree groups.

The complete degree-four, degree-five and degree-six layers agree with the published unpadded budget-11 and budget-12 searches. At ordered budget 12, the full-degree comparison excludes the positive ordered basis in both modes. At degree seven and budget 14, both modes have one midpoint and replay to the positive basis using all 14 instructions. The separate monomial-set implementation verifies these positive degree-six and degree-seven paths. The layered mode and first-arrival mode also agree throughout the partial stages at degree-six budget 12. [Control verifier](../experiments/round15_stable_disproof_partial_controls.py)

The original ordinary degree-ten length-20 run continues with the executable that started it. These controls used a separately rebuilt binary.

## Excluding widths six and seven together

If the degree-nine retraction at total stable budget 20 has two active intervals, a strict idle shortening of either would give a path of at most 17 moves with the other active interval still present. The exact padded corridor of length 17 has an identity at every vertex, so this is impossible. For width six there are 136 possible terminal templates after the strict tests. For width seven the corresponding unrestricted comparison leaves 5,730. [Width-six classification](round-12-stable-disproof.md#isolated-intervals-in-the-degree-nine-one-padding-retraction) · [Width-seven classification](round-13-stable-disproof.md#the-isolated-seven-instruction-interval)

At an idle vertex the two independent original linear vectors determine a unique functional $u$ on $\mathbb F_2^2$ whose value on each active vector is that row's auxiliary bit. The identity row has auxiliary bit one. Ordinary idle instructions preserve $u$. More generally, if the input auxiliary marking of an interval is changed by any functional $v$ of the old linear vectors, its output marking is changed by the same $v$. At each instruction the two markings differ by the same linear row recurrence. Thus the interval changes $u$ by a translation determined by its template trace. Each width-six transition changes $u$ nontrivially. The endpoint markings of the complete path have $u=0$, so in a path with widths six and seven the wider interval has the same nonzero increment. This permits keeping just the width-seven traces with a nonzero increment, giving 5,769 marked terminal rules. [Marked template generator](../experiments/round15_stable_disproof_two_widths.py)

The 18 effective middle instructions consist of the two intervals and five idle instructions. Cut immediately after the second idle instruction, so the two sides have two and three idle instructions. From each endpoint build the possibilities having used neither interval, either single interval, or both. For a marked interval the terminal equality must hold at the current quotient degree. The output mark of a surviving formal word is its zero-input mark plus the initial active markings paired with the word's two old parity coordinates. Once a side has used both intervals, the active marking must be zero, since any remaining instructions are idle. On the basis side use reversals of the same true intervals, which retain the property that they cannot be shortened. Idle waits allow for projection to a lower degree.

| Quotient degree | Both on the basis side | Width six on the AK(3) side | Width seven on the AK(3) side | Both on the AK(3) side |
| --- | ---: | ---: | ---: | ---: |
| 5 | 4 | 20 | 5 | 10 |
| 6 | 0 | 0 | 0 | 0 |

The two streamed degree-six boundaries check 31,434,795 and 226,989,865 transitions. Any genuine degree-nine path with widths six and seven would project to one of these four comparisons. The empty meetings exclude this width pair. The remaining one-padding cases are a sole interval of width at least nine, or two intervals satisfying the stronger width conditions above. [Exact marked comparison](../experiments/round15_stable_disproof_two_widths.cpp) · [Sole-interval bound](round-14-stable-disproof.md#completing-the-cut-in-degree-nine)

## A width-nine interval cannot have a strict idle replacement

A strict replacement of a sole width-nine interval would give a degree-nine path of length 17. Its entry and return would occur at ticks $t$ and $t+8$ of the saturated geodesic corridor. For each of the ten pairs of ticks, expand four effective active steps from both ends and stream one additional step from the later endpoint's side. All ten intersections are empty, with 15,524,600 boundary checks. Thus an isolated width-nine candidate would need at least nine idle moves to replace its active interval. This is a necessary condition on the isolated width-nine case. [Degree-nine geodesic cut](../results/round15_stable_disproof_geodesic9.json)

## Reproduction

~~~sh
work=/tmp/ac-r15-stable-disproof
mkdir -p "$work"
c++ -std=c++17 -O3 experiments/round15_stable_disproof_d6_kernel.cpp -o "$work/d6-kernel"
"$work/d6-kernel" | diff - results/round15_stable_disproof_d6_kernel.json
c++ -std=c++17 -O3 experiments/round08_magnus_native_corridor.cpp -o "$work/corridor"
python3 -B experiments/round15_stable_disproof_partial_controls.py "$work/corridor" \
  | diff - results/round15_stable_disproof_partial_controls.json
python3 -B experiments/round15_stable_disproof_two_widths.py > "$work/two-widths.txt"
c++ -std=c++17 -O3 experiments/round15_stable_disproof_two_widths.cpp -o "$work/two-widths"
for degree in 5 6
do
  "$work/two-widths" "$degree" < "$work/two-widths.txt"
done
python3 -B experiments/round15_stable_disproof_geodesic9.py \
  | diff - results/round15_stable_disproof_geodesic9.json
~~~
