# Stable transport to a new rank-two AK(3) waypoint

2026-11-19. The 267-move rank-three certificate ends at a presentation with two available projections. The projection using the literal $x$ chart is in the ordinary cyclic cap-27 component of AK(3). The projection using the intrinsic primitive chart has cyclic energy 22 and is absent from the independently checked ordinary cyclic cap-28 component. It is stably reachable from AK(3) with maximum rank at most four. [Rank-three path and projection screen](round-05-stable-proof.md), [transport receipts](../results/round05_stable_chart_transport.json).

The four verified Whitehead automorphisms are products of eight elementary changes of one generator. Each such change can be implemented by replacing an old generator $g$ by $a\,t$ or $t\,a$, where $a$ is a fixed signed letter and $t$ is new. For the left variant introduce $t=a^{-1}g$, and for the right variant introduce $t=g a^{-1}$. The program checks the added defining word and the elimination of $g$ after substituting the indicated expression in every original relator.

To implement this exchange with strict stable moves, first adjoin $t$ with isolated relator $t$. The previous relators normally generate the old free group, so the right-hand side of the defining equation is a product of conjugates of those relators and their inverses. Use these factors to change the isolated relator to the defining word. Then substitute for $g$ in every other row by multiplying in conjugates of the defining row. The resulting three rows normally generate the rank-three free group on the surviving letters, since adding and solving the equation presents the same trivial group. They can therefore change the defining row to the old singleton $g$ using conjugates, after inverting and rotating the defining row to put $g$ first. Delete $g$. Every exchange raises rank from three to four and returns immediately to three. This is the rank-controlled construction behind the supplementary moves in Lackenby's paper. [Lackenby, §2.1–2.2](https://arxiv.org/html/2606.06122v1#S2).

After eight exchanges, the pivot is $y^{-1}$. Multiplication by conjugates of this row erases all $y$ letters from the other rows, after which it can be inverted and deleted. The surviving marked pair in signed cyclic representatives is `(XXyxYxyXYxyXYxY, XXyyxYY)`. The expressions used to convert defining relators to and from singleton relators exist by normal generation. The replay records the defining exchanges and verifies their exact substitutions, without expanding those expressions into a strict move ledger or measuring the cyclic peak of the rank-four continuation.

This establishes stable reachability of the new rank-two waypoint and gives an ordinary peak lower bound of 29 for any ordinary connection from AK(3) to it. The waypoint remains eligible for a higher ordinary route. Its absence from the bounded component alone gives no disconnection result.

Run the checker with the full ASCII TSV catalogues for caps 27 and 28. It scans all signed versions of both projected tuples.

~~~sh
python3 -B experiments/round05_stable_chart_transport.py \
  /tmp/ac-r04-cyclic/c27.tsv /tmp/ac-r05-ak3/c28.expanded.tsv \
  | diff - results/round05_stable_chart_transport.json
~~~
