# Exact instruction bounds in the free group

2026-11-19. The ordinary and stable instruction distances of AK(3) to a basis are both at least **18**, for either target order. The calculations use exact free words and allow every word length.

## Search model

The instructions are inversion, conjugation by one of $x^{\pm1},y^{\pm1}$, and signed right multiplication by a distinct row. Row permutations are taken as a symmetry, so a negative result applies to either basis order and to the defining AC moves. The search interns exact reduced words and stores tuples of their integer IDs. Products cancel the maximal matching boundary because the input words are already reduced. The two frontiers expand in complete layers, each time choosing the smaller current frontier. A disjointness result after total radius $L$ excludes paths of length at most $L$.

There is no cyclic-length or raw-length cutoff. In particular the balls may contain words above the cyclic caps searched in parallel. A separate implementation with literal strings, stack reduction and independently enumerated neighbors checks the small ball counts for all the relevant row counts. [Native search](../experiments/round06_free_instruction_distance.cpp), [independent ball checks](../results/round06_free_distance_audit.json).

The extended ordinary search checks total radius 17. The completed radii are eight from AK(3) and nine from the basis, with respectively 93,768,030 and 191,373,223 visited tuples. The balls are disjoint. [Ordinary search counts](../results/round06_free_distance.json).

## Retaining rows when retracting stable paths

For positive padding, project the fixed-rank ordinary middle section by deleting the auxiliary variables while retaining the rows. The two padded endpoints become $(p,b,1,\ldots,1)$ and $(x,y,1,\ldots,1)$ up to row order. The letter deletion maps conjugations by an erased letter to identity instructions and preserves all products and inversions. This is the free-group version of the [finite Magnus retraction](round-05-stable-disproof.md). An exclusion in the retracted graph applies to all lifted paths of the same tested length.

For a shortest stable path of length at most 17, the [peak-rank formula and cut bound](round-01-stable-disproof.md) restrict the padding $k$ to $0,\ldots,4$. Its normalized ordinary middle section would have at most $17-2k$ instructions. The native search exhausts disjoint balls in all five cases. For $k=0$ this is the exact original rank-two graph up to row order. [Search counts](../results/round06_free_distance.json).

| Spare identity rows | Tested total radius | Completed radii | Visited states from both ends |
| ---: | ---: | --- | --- |
| 0 | 17 | 8 and 9 | 93,768,030 and 191,373,223 |
| 1 | 15 | 7 and 8 | 136,739,554 and 416,079,086 |
| 2 | 13 | 6 and 7 | 14,691,033 and 63,089,488 |
| 3 | 11 | 5 and 6 | 891,942 and 4,458,757 |
| 4 | 9 | 4 and 5 | 55,205 and 298,814 |

This retraction has a finite upper bound independent of Magnus degree. The three-row AK(3) control reaches $(1,x,y)$ in **30** instructions using only the two ambient generators. Its spare identity row becomes $y$ in 18 instructions, by the identity

$$
y=p^{-1}(x p x^{-1})((xy)p^{-1}(xy)^{-1})b(yby^{-1})(y^2by^{-2}),
\qquad p=x^3y^{-4},\quad b=xyxy^{-1}x^{-1}y^{-1}.
$$

The donor $y$ then changes the first two rows to $x^3,x$. Three negative products clear $x^3$. The path works in every further quotient and permits any number of unused additional identity rows. [Exact 30-instruction control](../results/round06_identity_row_control.json).

More generally for any normally generating pair of $F(x,y)$, one can use one spare identity row to store $y$ using a normal-closure factorization. With that row frozen, replace the original two words by their evaluations at $y=1$. The remaining words are powers of $x$ whose exponents have greatest common divisor one, since they must normally generate the cyclic quotient. The Euclidean algorithm makes them $x,1$. Thus rank-two retractions with a spare identity row eventually reach a basis for every normally generating pair. The original stabilization introduces a new independent generator, so the 30-instruction path in the retracted problem is an exact limitation of this relaxation.

## Reproduction

~~~sh
mkdir -p /tmp/ac-r06-free-distance
c++ -std=c++17 -O3 experiments/round06_free_instruction_distance.cpp \
  -o /tmp/ac-r06-free-distance/search
for k in 0 1 2 3 4; do
  /tmp/ac-r06-free-distance/search "$k" "$((17 - 2*k))"
done
python3 -B experiments/round06_free_distance_audit.py /tmp/ac-r06-free-distance/search \
  | diff - results/round06_free_distance_audit.json
python3 -B experiments/round06_identity_row_control.py \
  | diff - results/round06_identity_row_control.json
~~~
