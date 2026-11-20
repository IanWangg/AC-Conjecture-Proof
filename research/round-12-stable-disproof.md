# Replacing short active intervals at one and two added pairs

2026-11-19. In the same-degree erasure of any shortest one-padding stable path from a balanced normally generating rank-two tuple, some three-active interval has length at least seven in the free group or characteristic-two Magnus degree at least eight. At total budget 20 for AK(3), the degree-nine one-padding retraction has one or two three-active intervals, each of length at least six, and a sole interval has length at least seven. A two-padding candidate has a degree-nine four-row retraction with a four-active interval of at least five instructions. These restrict the remaining branches without deciding the full budget. [Six-instruction replacements](../results/round12_stable_disproof_symbolic6.json) · [One-padding geodesic and template checks](../results/round12_stable_disproof_short_savings.json) · [Four-active interval checks](../results/round12_stable_disproof_four_active.json)

## Removing every one-padding excursion of at most six moves

Erase the added variable at the original degree and keep all three row slots. An idle vertex has exactly two nonidentity rows because the original degree-one exponent vectors retain rank two. From an idle vertex, a first-return interval with three nonidentity rows begins by importing a signed copy of an active row $a$. Its last move erases one row by multiplication by a signed equal donor. Thus formal letters $a,b$ for the initial two rows and $x,y$ for the conjugating generators give a finite family of templates. Initialize the formal triple $(a,b,a^\epsilon)$ for both signs. Enumerate four internal moves and retain both possible signs at the last cancellation whenever the two relevant rows have the same original parity. This parity test is exact as a necessary condition because $a,b$ have independent linear parts. The formal $x,y$ exponent totals are zero after any of the relator moves. Discard an internal tuple with a formally empty row, since it cannot belong to the active interval. [Earlier exact replacements through length five](round-11-stable-disproof.md#a-long-excursion-at-any-budget)

For length six there are 313,552 distinct terminal triples, each recording the removed row, a signed retained donor that must equal it, and the surviving unordered pair. The literal six-move ball from $(a,b)$ has 1,171,516 vertices. The complete classification is below.

| How the template is covered | Count |
| --- | ---: |
| Surviving pair lies literally in the formal ball | 269,896 |
| Substituting the signed removed word for the retained donor gives a pair in the ball | 37,415 |
| Impossible exponent equality modulo 16 | 5,445 |
| Impossible equality in degree three | 164 |
| At most two non-length-increasing rewrites per row give a pair in the ball | 632 |

The modulo-16 test uses independent $a,b$ exponent vectors, which form an invertible coordinate change modulo 16. Rank-one degree-eight quotients see these exponents modulo 16. The remaining 796 cases have 33 cyclic equality classes. An independent small template test enumerates the complete degree-three rank-two group of 128 elements by multiplication by its marked generators. It evaluates each equality over all 6,144 ordered pairs with independent linear parts, keeping literal $x,y$ as the conjugators. Seven classes have no solutions and exclude 164 templates.

In every other case use the last cancellation equality itself. Write it as a cyclically reduced relator $R$. Each cyclic rotation of either orientation of $R$ splits as $uv$, so $u=v^{-1}$ whenever the last cancellation is legal. Replace one contiguous occurrence of $u$ by $v^{-1}$ with no length increase, then freely reduce. Among the words obtained by up to two rewrites per surviving row, every template contains a pair in the literal six-step ball. This gives an explicit equal replacement under the actual last cancellation relation and uses no extra assumption about the ambient words. [Exact certificate generator](../experiments/round12_stable_disproof_symbolic6.py)

Therefore every excursion of length at most six has an idle replacement of no greater length. If there were only such excursions on the same-degree erasure of a shortest one-padding path, apply the replacements, discard projected waits and remove the identity slot. The resulting ordinary path saves the insertion and deletion. Hence some excursion has at least seven instructions. This conclusion concerns erasure without further degree truncation.

## Isolated intervals in the degree-nine one-padding retraction

For AK(3) at total stable budget 20, the degree-nine three-slot retraction has 18 effective instructions. If any active interval can be shortened to idle edges, the resulting path has at most 17 instructions. The saturated length-17 corridor has only idle vertices, so the saving is exactly one and the original interval is the only active interval. Its two outside idle sections connect it to the marked endpoints. Along them the active rows have auxiliary coefficient zero and the identity row has coefficient one, by the mod-two transport argument. [Length-17 saturation](round-10-stable-disproof.md) · [Auxiliary coefficient transport and widths two and three](round-11-stable-disproof.md#retraction-and-marked-coefficients)

For each span $s$ from two to six, take entry geodesic tick $t$ and return geodesic tick $t+s-1$ from the independently witnessed length-17 corridor. At each endpoint assign coefficient zero to both active rows and one to the identity. Expand the two exact active halves with their row-aligned mod-two coefficients, excluding any intermediate identity or projected wait. A product adds the donor's coefficient to the recipient. Inversion and conjugation preserve the coefficients. Intersect the marked halves at distances $\lfloor s/2\rfloor$ and $\lceil s/2\rceil$. Across the 17, 16, 15, 14 and 13 windows respectively, no intersection remains. As a control, discarding the marks recovers the nine and six nonempty windows previously found for widths two and three, followed by four, two and zero for widths four, five and six. Thus no genuine width-two through width-six interval at this budget can admit a strictly shorter idle replacement.

A comparison that ignores the marks already shortens every four- or five-instruction interval. For length four the ordinary radius-three ball contains 1,542 pairs. It covers 1,246 of the 1,296 unrestricted templates literally and 50 by the last equality. For length five the radius-four ball covers 17,446 of the 19,766 unrestricted templates literally, 2,117 by the last equality, and 32 by rewrites. Exponent equality modulo 16 excludes 161 and degree-three evaluation excludes the final 10. Therefore every interval in a budget-20 one-padding candidate has width at least six. The same comparison at length six leaves 136 possible terminal templates, all recorded in the receipt.

For an isolated interval, the same outer coefficients force a stricter symbolic comparison. At birth the imported copy alone carries coefficient one. Just before death, only the row that will be removed can carry coefficient one, because both survivors must have zero. Track these bits through every internal template and test only such last cancellations. The ordinary comparison now uses a ball of radius $s-1$. Through width six all marked templates admit a saving or an impossible last equality. The table uses the equality tests and rewrites above.

| Interval length | Terminal templates | Literal replacements | Substitute the last equality | Impossible mod 16 | Impossible in degree three | Last-equality rewrites |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 4 | 808 | 804 | 4 | 0 | 0 | 0 |
| 5 | 10,512 | 10,168 | 297 | 41 | 6 | 0 |
| 6 | 152,122 | 136,122 | 11,917 | 3,464 | 163 | 456 |

The isolated forms of width two and three already admit a saving by the round-eleven classification. The exact geodesic windows now rule out every isolated interval of width at most six, even after truncating from degree ten to degree nine. There are at most three active intervals. If there were three, each would have width six and together they would use all 18 instructions. To check that case, start from an idle pair and evaluate the 136 residual width-six templates for both orders of its two members. Include the surviving pair when the final signed cancellation equality holds. This includes every admissible width-six interval, in either direction, since the ordinary steps are reversible and a saving for the reversed interval would reverse to a saving for the original. This test only uses the necessary terminal conditions. From AK(3) the one- and two-interval sets contain 32 and 971 pairs. From the basis they contain 22 and 616 pairs. Both opposite one- and two-interval sets are disjoint, so three intervals cannot occur. [Marked symbolic and geodesic checks](../experiments/round12_stable_disproof_short_savings.py)

## Four-active windows with two added pairs

At stable budget 20 with two added pairs, every instruction in the normalized middle has a nontrivial image after erasing both added variables at degree eight. A projected wait would give a degree-eight four-slot path at middle budget 15, which is excluded. In particular the original path does not use conjugation by either erased variable. Degree nine also preserves all 16 effective instructions. A four-active interval starts at a state with three nonidentity rows, enters the region where all four rows are nonidentity, and first returns to three. Its birth is a product importing a signed copy of one of the active rows. At death, the removed row equals the signed surviving donor. Unlike the preceding rank-two test, no individual pair of the three incoming rows is required to have independent exponent vectors. [Degree-eight budget-15 exclusion](round-09-stable-disproof.md)

Use formal rows $a,b,c$, with a signed copy of $a$ as the fourth row just after birth. Because row permutations are quotiented out, permuting these formal row names covers any choice of donor. Allow every two-, three- or four-instruction first-return template and every sign of the last cancellation. This gives a finite comparison with the formal three-slot balls.

| Interval length | Terminal templates | Literal replacements | Substitute the last equality | Eliminate one row symbol | Powers substitution | Impossible odd torsion |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2 | 34 | 18 | 8 | 8 | 0 | 0 |
| 3 | 1,308 | 726 | 336 | 246 | 0 | 0 |
| 4 | 36,762 | 20,892 | 9,464 | 6,384 | 16 | 6 |

After the literal and donor replacements, use the cyclic reduction of the final equality as a formal relation. If one of $a,b,c$ occurs exactly once, solve for it and substitute the resulting word in the starting tuple and the surviving triple. In 259 of the 264 relation classes needed at length four, this gives a three-slot replacement of at most four moves. Four more classes are cyclic rotations of $U^2 V U V=1$ for signed choices of distinct row symbols. For these, $T=UV$ gives $U=T^{-2}$ and $V=T^3$. The three-slot comparison after that substitution covers all 16 templates. The last class is $a^5=1$, impossible because $a$ is nonidentity in the active starting triple and the groups considered are free or finite 2-groups. This argument uses only the final cancellation and proves a replacement of no greater length for all actual intervals of up to four instructions. [Three-slot formal replacement checks](../experiments/round12_stable_disproof_four_active.py)

If every four-active interval were this short, replace all of them and delete an identity slot at each vertex. The identity-deletion lemma applies to the remaining ordinary edges with an identity at both ends. It would give a degree-nine three-slot path at middle budget 16, already excluded. Hence any two-padding candidate must have a four-active interval of at least five instructions. If precisely three original-letter conjugations occur in the actual free words, independently apply the signed schedule `x,x,Y` and its intervening product and receiver constraints. These free-subgroup conditions are separate from the Magnus exclusions. [Identity deletion and prior retraction](round-11-stable-disproof.md#erasing-an-identity-in-a-larger-projected-tuple) · [Three original conjugations](round-11-three-conjugations.md)

A degree-nine four-slot existence search may replace every short interval before testing the other intervals. Each replacement has to preserve length, since a saving would project to the excluded degree-eight middle budget 15. There are then one or two four-active intervals, each of length at least five. The crossing from two to three active rows and the return from three to two consume at least two instructions outside those intervals, leaving at most 14 of the 16. This normalization applies to existence at degree nine. An individual replacement may change the auxiliary-variable lift.

## Reproduction

~~~sh
python3 -B experiments/round12_stable_disproof_symbolic6.py \
  | diff - results/round12_stable_disproof_symbolic6.json
python3 -B experiments/round12_stable_disproof_four_active.py \
  | diff - results/round12_stable_disproof_four_active.json
python3 -B experiments/round12_stable_disproof_short_savings.py \
  | diff - results/round12_stable_disproof_short_savings.json
~~~
