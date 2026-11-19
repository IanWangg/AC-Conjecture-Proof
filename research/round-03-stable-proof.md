# Round 03 · Stable Andrews–Curtis proof

2026-11-19. Every stable AC trivialization of AK(3) that stays at ranks at most three has cyclic total length peak at least **22**. The result also applies to the ordinary rank-three section after adding one isolated pair. At peak at most 21, every rank-three state admits a one-occurrence pivot for the new generator. The finite audit excludes a geometric two-row block with free quotient in every reached state where the original singleton has disappeared.

## The first change of chart

Start with the standard stabilization of AK(3), with an added marked generator $z$ and relator $z$. Write $|w|_{\rm cyc}$ for free cyclic length. Catalogue words represent conjugacy classes up to inversion, and tuples are unordered. Call a rank-three state *a singleton state* if its catalogue includes the signed conjugacy class of $z$, stored as capital Z. There is at most one such row, since the three exponent rows are unimodular. Deleting the $z$ row and setting $z=1$ on the other two rows gives its rank-two projection. Between two singleton states, every elementary edge projects to an ordinary rank-two move, a row reindexing, or the identity. If the recipient of a multiplication was the singleton and is still a singleton afterwards, both retained rows are unchanged. In every case the projected cyclic lengths sum to at most the original cyclic total length minus one.

Let $C$ be the independently certified ordinary cyclic cap-25 AK(3) component. The projection of the starting singleton belongs to $C$. On a singleton segment of peak at most 21, the finite closure of $C$ preserves membership of every projection that starts in $C$. Write $\bar r,\bar s$ for the projections of the donor and the other retained word on a step that first leaves the singleton states. The only such step is multiplying the singleton by the donor, with the units and conjugacies allowed in AC. Both the donor $r$ and the new row $q$ project to the signed conjugacy class of $\bar r$. If the cyclic donor contains a $z$-letter, then $|r|_{\rm cyc}\geq|\bar r|_{\rm cyc}+1$. If it contains none, the new row has $z$-exponent $1$ or $-1$, so $|q|_{\rm cyc}\geq|\bar r|_{\rm cyc}+1$. Therefore the output cyclic energy is at least

$$
|\bar s|_{\rm cyc}+2|\bar r|_{\rm cyc}+1.
$$

In $C$ this expression has minimum 20, attained by 20 ordered donor choices. The first loss of a singleton is therefore impossible below cap 20. The lower bound is sharp for changing the chart. At the initial stabilized tuple multiply $z$ on the right by the braid relator $xyxYXY$. The result has cyclic lengths $7,6,7$ and still has a one-occurrence pivot. Capital letters here denote inverses. [Certified rank-two component](round-02-cyclic25.md).

## Finite excursions at caps 20 and 21

To close the range where a singleton can disappear, enumerate possible first-exit states independently of whether their singleton predecessors are reachable. For an ordered pair $(\bar r,\bar s)$ in $C$, retain it only when its lower bound above is at most the rank-three cap $L$. Enumerate lifts of the donor and the retained row with total excess over their projected cyclic lengths at most $L-2|\bar r|_{\rm cyc}-|\bar s|_{\rm cyc}$. This follows because the new row still projects to $\bar r$. At caps 20 and 21 the excess is at most two. Any such lift is obtained by inserting that many signed $z$-letters, because cyclic cancellations after deletion remove an even number of letters. There can be no cancellation with zero inserted letters, since the lift is already cyclically reduced. The code also implements reversal of cyclic cancellations for larger excess.

For each lift, enumerate all bounded cyclic products with the singleton in the recipient slot. Then compute the component of these first exits while excluding new singleton states, recording the projected pair at every reentry into the singleton states. In any ambient rank, axes of two conjugates in the Cayley tree either meet or are separated by a unique shortest bridge. In the first case rebasing at an intersection produces signed cyclic rotations of the two words. In the second case, the product cyclic length is the sum of their lengths plus twice the bridge length. Thus with current cyclic total $E$ and donor length $d$, the finite menu uses all signed rotations, and bridge words of length at most $\max(0,\lfloor(L-E-d)/2\rfloor)$ from the signed rank-three alphabet. Some short words in this menu may represent intersecting axes as well. Every accepted multiplication is still an actual AC step after conjugations at the same cyclic energy. The untouched third row adds the same length to both sides. [All-tail cyclic menu proof in rank two](research-n-cyclic-search.md).

| Cap | First-exit seeds | Non-singleton states examined | Product candidates | Distinct reentry projections |
| ---: | ---: | ---: | ---: | ---: |
| 20 | 224 | 224 | 235,776 | 20 |
| 21 | 4,208 | 4,208 | 4,802,688 | 56 |

All reentry projections belong to $C$. The minimum row length while the singleton is absent is five in both audits. These are complete checks on a possibly larger class of excursions than actually reachable. Induct on the excursions. The singleton sections preserve $C$, each first exit enters the audited set, and every possible return projects back into $C$. A rank-three standard basis is a singleton state whose projection is outside $C$, so it cannot be reached. An $x$ or $y$ singleton is impossible in the non-singleton set by row length and impossible in the singleton set by the primitive-coordinate exclusion for $C$.

The last observation also handles general stable paths of rank at most three, even if they contain several rank changes. Every rank-three segment starts by adding a fresh marked $z$ to a rank-two state in $C$. Consequently any deletion must delete this added generator, leaving a rank-two state in $C$. The first drop from rank two to rank one would already require a primitive row of cyclic length one in $C$, so no further rank is needed in the argument. An ordinary rank-two segment of peak at most 21 stays in $C$ by its verified closure.

## Screening for geometric blocks

Every non-singleton state retains a row with exactly one occurrence of $z^{\pm1}$. The audit solves each such row for $z$, including every choice when there are two possible pivots. At cap 21 the resulting 928 distinct rank-two pairs all lie in $C$. A block of two rows containing a pivot therefore cannot have infinite cyclic quotient. Otherwise the second block row projected under the pivot would normally generate the kernel of an epimorphism $F_2\to\mathbb Z$. A marked Nielsen basis puts this kernel in the form $\langle\!\langle x\rangle\!\rangle$, and Magnus's normal-closure theorem would make that projected row primitive. No projected pair in $C$ has a primitive coordinate. The same argument excludes using the $z$ singleton in a block during a singleton segment. [Magnus's theorem](https://msp.org/gtm/2008/14/gtm-2008-14-004s.pdf), [primitive audit](round-02-cyclic25.md).

Of the 4,208 non-singleton states, 3,456 have two pivots, so every block of two rows in them contains a pivot. In each other state, the pair omitting the sole pivot is $z$-free. The 56 such pairs give 52 Whitehead-minimized pairs, all with independently replayed planar-link parity obstructions. They are disk-busting in $F(x,y)$: a splitting into two cyclic factors could normally kill both factors with two rows only if both rows represented primitive factors. The earlier Whitehead and parity screen therefore excludes rank-two geometry. A geometric realization in rank three of a multicurve supported in the free factor $F(x,y)$ would lift to the cover of the handlebody corresponding to that free factor. The cover is built from the core genus-two handlebody with balls and one-handles along trees. The compact lifted curves lie in the boundary of a finite genus-two sub-handlebody, obtained by retaining a finite connected set of pieces containing the core and all pieces met by those curves. The same curves would then give exactly a rank-two geometric realization. This proves the block exclusion in the non-singleton sector. Blocks in singleton states that omit the singleton and still mix $z$ are outside this geometric screen. [Geometricity criterion and parity verification](round-01.md), [related free splitting reduction](https://msp.org/agt/2016/26-3/agt-v26-n3-s.pdf).

## Reproduce

First reconstruct the round-two cap-25 file. The compressed excursion audit verifies its SHA-256 itself. The independent native rank-three check completes cap 18 with 275,488 states and 191,029,456 candidate products. Its direct cap-19 run is partial, stopping at 2,000,000 states. All its recorded states in both runs have a singleton. The cap-19 theorem uses the weighted bound, not this truncated run.

~~~sh
python3 -B experiments/round03_stable_proof_pivot.py /tmp/ac-r02-component/c25.tsv 19 20 21 \
  | diff - results/round03_stable_proof_pivot.json
mkdir -p /tmp/ac-r03-stable
c++ -std=c++17 -O3 experiments/round03_stable_proof_rank3.cpp -o /tmp/ac-r03-stable/rank3
/tmp/ac-r03-stable/rank3 3 18 2000000 /tmp/ac-r03-stable/ak3-18.tsv \
  > /tmp/ac-r03-stable/ak3-18-counts.json
/tmp/ac-r03-stable/rank3 3 19 2000000 /tmp/ac-r03-stable/ak3-19.tsv \
  > /tmp/ac-r03-stable/ak3-19-counts.json
python3 -B experiments/round03_stable_proof_catalogue.py /tmp/ac-r03-stable \
  | diff - results/round03_stable_proof_rank3.json
~~~

The cap-19 native run returns status 2 after recording its partial catalogue. The signed cyclic canonicalizers and closure checks in the two programs differ. The result leaves larger cyclic peaks and higher intermediate ranks open. The next geometric search can look for a first excursion with no exposed pivot or a larger-cap two-row block that escapes the projected primitive and planar-link filters.
