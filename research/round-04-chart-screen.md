# Changing the eliminated generator on the cap-22 witness

2026-11-19. The strict 247-move rank-three witness loses all pivots for the added generator $z$. It retains at least one one-occurrence elimination chart at all 26 distinct signed cyclic states along the path. Allowing the chart to eliminate an older marked generator gives 20 distinct rank-two projections, all in the independently certified ordinary cyclic cap-26 AK(3) component. [Rank-three path and replay](round-04-stable-proof.md), [cap-26 closure](round-03-cyclic26.md).

For each cyclic state, take every generator with exactly one signed occurrence in any relator. Rotate and orient that relator to the form $g w^{-1}$, then substitute $g=w$ in the other two and freely and cyclically reduce. The two remaining letter names are put in the canonical rank-two order. There are three charts eliminating $x$ and 26 eliminating $z$, counting separate pivots. At the final state, its only chart uses $XYYZZZY$ and sets $x=YYZZZY$. Renaming $y,z$ to $x,y$ gives the canonical quotient pair (XXXXYYYxyyyxYYY, XXXYYYY), of cyclic energy 22.

Every projected rank-two pair is nongeometric. The checker verifies a unimodular determinant and performs Whitehead minimization. The minimum total lengths are greater than two, so the normalized pairs are disk-busting by the rank-two splitting argument from round one. The independent parity verifier checks every obstruction in the minimized marking. Zieschang's minimal-diagram theorem excludes any geometric realization of those pairs. If any original rank-three state on the ledger were geometric, geometry would descend through its one-occurrence chart to the corresponding rank-two tuple. Hence the full rank-three tuple is nongeometric at every vertex of this particular ledger. [Geometry descends through a defining equation](round-01-stable-proof.md), [screen results](../results/round04_chart_screen.json).

~~~sh
python3 -B experiments/round04_chart_screen.py /tmp/ac-r03-cyclic/c26.tsv \
  | diff - results/round04_chart_screen.json
~~~
