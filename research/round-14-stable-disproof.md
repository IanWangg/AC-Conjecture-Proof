# Excluding the isolated eight-instruction excursion

2026-11-19. For the one-padding budget-20 branch of AK(3), the degree-nine retraction can have a sole active interval only at width nine or larger. The width-eight test reduces the interval to 148 terminal templates up to exchange of the original generators, then excludes all guarded paths with ten idle moves and one such interval. The restriction on a two-interval candidate remains one width at least six and the other at least seven. [Symbolic comparison](../results/round14_stable_disproof_mixed_eight.json) · [Cubic and quartic lift](../results/round14_stable_disproof_lift_eight.json) · [Complete degree-nine cut](../results/round14_stable_disproof_width_eight_cut.json)

## The quadratic screen and the ordinary replacement test

An isolated interval has pure original-letter active rows and a literal $z$ row on both sides. Every instruction outside the interval preserves this because the degree-nine retraction has no waits. The birth step imports a signed copy of the active row $a$ into the spare, leaving six internal steps and the last signed cancellation. The other starting active row is $b$. [Isolated interval setup](round-13-stable-disproof.md#the-isolated-seven-instruction-interval)

For the internal steps, record a formal word in $a,b,x,y$ for each row together with six bits of its lifted quadratic expansion. The six bits are the three linear coefficients, the coefficients of $zx,zy$, and that of $z^2$. In a product the retained quadratic coefficients are the sum of the two inputs, plus the coefficient of $z$ in the first input times the corresponding linear coefficient of the second. This defines an exact quotient of the rank-three degree-two Magnus group. An independent check enumerates all 512 group elements and verifies the compact product on all 262,144 ordered pairs. Its image has 64 elements.

Use the 18 possible ordered compact terminal triples with a literal $z$ row and two independent original linear vectors. The reverse reachable layer widths through radius seven are 18, 162, 1,224, 7,212, 27,618, 40,476, 9,162 and 144. At each formal step keep the compact state only if it can reach one of the prescribed terminal states within the remaining budget. Among the six ordered independent incoming original linear vectors, exchanging $x$ and $y$ reduces the enumeration to three. The terminal move must erase the unique row carrying the auxiliary coefficient and use a donor with the same original parity. This yields 10,019,768 distinct terminal templates across the three markings. [Native template enumerator](../experiments/round14_stable_disproof_mixed_eight.cpp)

A strict saving on a width-eight interval would give a degree-nine path of length 17 or less. The exact length-17 corridor is idle and has minimum length 17. The replacement endpoints must lie at ticks $t,t+7$ of that corridor. All eleven active-half intersections at distances four and four are empty, even with the auxiliary coefficient dropped. Thus any strict idle replacement excludes its template at the budget under study. [Corridor and equality checks](../experiments/round14_stable_disproof_mixed_eight.py)

The formal ordinary radius-seven ball contains 10,514,136 pairs. It gives literal replacements for 9,840,202 terminal templates and another 126,658 after substituting the last signed equality. Exponent equality modulo 16 excludes 41,229. Of the remaining 11,679, degree-three evaluation excludes 1,189 and up to two last-equality rewrites per row give strict replacements for 9,638. The remaining 852 templates require a stronger lift test.

## Checking the actual instructions in degrees three and four

Trace all labelled symbolic instructions that give one of the remaining terminal templates. The three old linear markings give 1,270, 1,260 and 742 traces. For each trace, enumerate the old rank-two degree-three group elements with the prescribed independent linear markings. Enforce the final old-word equality and apply the actual instructions in rank three. The removed row must return to literal $z$, and both surviving rows must have every $z$-supported coefficient zero. This leaves 202 templates.

The same input assignments determine all $z$-supported terms through degree four. Pure degree-four terms of the incoming old rows can only add in degree four, since every product with a positive-degree term would raise the degree. They therefore cannot change any $z$-supported outcome. Embed the degree-three old polynomials with zero degree-four terms, replay the same instructions at degree four, and test only the coefficients involving $z$. This leaves 148 templates, 96 of which have a tautological terminal equality in the old formal words. [Exact marked trace lift](../experiments/round14_stable_disproof_lift_eight.py)

## Completing the cut in degree nine

Record every exact old degree-three input pair passing both full-rank tests for at least one trace of the template. Include the corresponding rules under exchange of the two original letters. There are 9,504 distinct rules, each specifying an ordered cubic input pair, a last signed equality and two resulting old words. In any higher-degree quotient, allow the rule only when the input projects to that cubic pair and the equality holds at the current degree. Evaluate the two resulting old words to get the next idle pair. This includes every genuine isolated width-eight interval and its reversal. Reversing a genuine interval preserves the width, the pure outer data and the absence of a shorter replacement.

The 18 effective middle instructions consist of eight in the interval and ten idle instructions. Cut immediately after the fifth idle instruction. On the two sides of the cut, enumerate all positions of the interval, requiring five idle instructions on each side and precisely one interval overall. Waits in the idle graph can represent instructions that become trivial in a lower quotient. The last two-branch expansion on each side is streamed against the opposite five-idle set.

| Degree | Interval on the AK(3) side | Interval on the basis side |
| --- | ---: | ---: |
| 6 | 4 | 0 |
| 7 | 2 | 0 |
| 8 | 1 | 0 |
| 9 | 0 | 0 |

The degree-nine run checks 15,475,997 and 630,832 streamed boundary transitions. It excludes every isolated width-eight interval at this budget and raises the isolated lower bound to nine in degree ten and the free group. [Guarded degree-nine search](../experiments/round14_stable_disproof_width_eight_cut.cpp)

The unrestricted degree-ten ordinary length-20 search remains active. The degree-four stage retained 6,254,117 midpoints, and degree five is still in progress. The one- or two-padding branches at length 20 also remain open.

## Reproduction

~~~sh
work=/tmp/ac-r14-stable-disproof
mkdir -p "$work"
c++ -std=c++17 -O3 experiments/round14_stable_disproof_mixed_eight.cpp -o "$work/mixed-eight"
"$work/mixed-eight" | "$work/mixed-eight" --strict \
  | python3 -B experiments/round14_stable_disproof_mixed_eight.py \
  | diff - results/round14_stable_disproof_mixed_eight.json
python3 -B experiments/round14_stable_disproof_lift_eight.py \
  --targets results/round14_stable_disproof_mixed_eight.json \
  | "$work/mixed-eight" --traces > "$work/traces.txt"
python3 -B experiments/round14_stable_disproof_lift_eight.py < "$work/traces.txt" \
  | diff - results/round14_stable_disproof_lift_eight.json
python3 -B experiments/round14_stable_disproof_lift_eight.py --guards < "$work/traces.txt" > "$work/guards.txt"
c++ -std=c++17 -O3 experiments/round14_stable_disproof_width_eight_cut.cpp -o "$work/width-eight-cut"
for degree in 6 7 8 9
do
  "$work/width-eight-cut" "$degree" < "$work/guards.txt"
done
~~~
