# The exact two-auxiliary-occurrence cut at cap 32

2026-11-19. A rank-three clearing from the literal chart `(zXyxxyy, XXYxYXXYxxy, XXYXYxxyXyxxy)` at cyclic peak 32 must visit a cyclic tuple with **at least three** auxiliary occurrences. The complete signed reverse graph with at most two auxiliary occurrences has **265,229** orbits and misses the entire one-occurrence component of the chart. A verified cap-33 path clears with one occurrence, giving the sharp peak **33** under the two-occurrence restriction. [Search receipt](../results/round18_stable_proof_two_tails.json), [strict cap-33 clearing](round-16-stable-proof.md).

## The two-tail model

Count occurrences of `z` and `Z` in the individually cyclically reduced rows. In the one-occurrence sector the unique charged row can be oriented and rotated to $zu$ for a reduced $x,y$ tail $u$. Using this row as a donor gives the receiver a nonzero auxiliary exponent. Thus the first state with two occurrences has two different charged rows, each with exactly one. Write it as $(zu,zv,b)$ up to row order and signs. If the two ordinary donors before the entry were $a,b$, then

$$
v=u h a^\epsilon h^{-1}
$$

in $F(x,y)$ for some $h\in F(x,y)$ and $\epsilon\in\{-1,1\}$. To see this, cut the charged cyclic factor before its unique positive auxiliary letter. The other factor, its conjugating bridge, and the parts of the charged word used for the cyclic cut all lie in $F(x,y)$. A shortest positive bridge containing an auxiliary letter would contribute its two extra auxiliary occurrences and exceed support two. Reversing the original sign of the charged factor only reverses the oriented product and the sign of the ordinary factor. Hence $uv^{-1}$ is in the original cyclic class of $a$ up to inversion.

An interior product in the two-occurrence sector changes one charged row using the ordinary donor $b$. A product using a charged donor on the ordinary row would create a third charged row. With both receiver and donor charged, the new exponent is $0$ or $\pm2$. Staying within two occurrences forces the receiving row to lose both auxiliary letters and returns to support one. Consequently every interior update multiplies one tail on the right by a conjugate of $b^{\pm1}$, with $b$ frozen. The argument by auxiliary exponent also excludes two occurrences in the same relator throughout any path with support at most two.

At a return, the two charged relators are multiplied with opposite orientations. The product has no essential positive bridge since a disjoint-axes product would retain both auxiliary letters. Write the two rotated factors as $u_2 z u_1$ and $v_1^{-1} Z v_2^{-1}$, with $u=u_1u_2$ and $v=v_1v_2$. The auxiliary letters disappear only when $u_1v_1^{-1}=1$ or $v_2^{-1}u_2=1$. In either case the new cyclic class is that of $uv^{-1}$, up to inversion according to the receiving slot. This class is realized by aligning and multiplying $zu$ and $(zv)^{-1}$. In particular, a two-product departure and return with no interior update can be contracted, up to row order: it restores one ordinary donor's cyclic class and either keeps $zu$ as pivot or replaces it by $zv$, a single allowed pivot change using that same ordinary donor. [Cyclic shortest-bridge convention](round-12-primitive-step.md), [complete two-tail product menu](../experiments/round18_stable_proof_two_tails.cpp).

## Exact bounds for the reverse graph

In the two-occurrence sector define the projected pair to be $(uv^{-1},b)$, freely and cyclically reducing each row. The pair is in the ordinary cap-36 component of E22 at entry. If either $u$ or $v$ changes by one conjugate of $b^{\pm1}$, the difference changes by one conjugate of the same donor, as an ordinary product. The projected pair has cyclic energy at most $|u|+|v|+|b|\le30$. On return it becomes the exact cyclic pair of the two ordinary rows. In the one-occurrence sector, ordinary donor moves project to ordinary products at cyclic energy at most 31. This inductively keeps every projected pair in the independent E22 component. Its eligible pairs have minimum energy 20 and minimum coordinate width nine. E22 is the historical label of the marked energy-21 pair. [Ordinary closure and lower bounds](round-17-stable-proof.md#exact-one-pivot-cut-at-cyclic-peak-32).

In the two-occurrence sector the total energy is therefore at least 22 and the ordinary donor has length at least nine. An interior positive bridge would have energy at least $22+9+2=33$. The same zero-bridge restriction holds for ordinary donors in the one-occurrence sector before a literal `z` appears. First entries with the pivot as donor may have a positive $x,y$ bridge, so the search includes all such bridges permitted by the cap. The independent stack scan also enumerates bridges over all three letters and filters the resulting support.

Before the first literal auxiliary singleton, a single charged row uses at least two letters, and if there are two charged rows, both use at least two. In the one-occurrence sector both ordinary rows then have width at most 21. In the two-occurrence sector the ordinary donor is unchanged since entry, and each charged row has width at most $32-9-2=21$. At the first singleton only one row changes, so the other rows retain their covered widths. A literal `z` can immediately clear the remaining auxiliary occurrence, if any, by one length-decreasing product. The first singleton thus extends to an isolated auxiliary row with two ordinary donors of widths at most 21 and total energy at most 31. No other generator can be the first destabilization because the ordinary donors have widths at least nine, and the charged rows contain `z`. The reverse search can therefore start with the **7,229** eligible pairs from the full ordinary cap-36 catalogue with an isolated auxiliary row. Products are reversible at the cyclic-state level. The width omissions counted during the reverse search are outside the required graph through the first singleton.

The calculation keeps simultaneous signed ambient markings that preserve the auxiliary generator up to sign, independent cyclic rotations and inversions, and row order as orbit symmetries. The key for the complete one-occurrence forward component from Round 17 collapses the 4,544,552 ordered states to **568,106** such orbits. The reverse search processes **239,182,900** rotation and bridge candidates plus **515,376** direct tail-difference checks, closes completely, and finds no intersection. An independent product menu recomputes **609,977,128** candidates with stack reduction, both orientations and all three-letter bridges, then filters by support. The two emitted sorted catalogues are byte-identical. The strict positive control starts at `(zx,zYx,x)` and reaches the literal rank-three basis `(y,z,x)` in eight moves at cyclic peak six. Its native search exercises the tail-difference edges. [Rank-three positive control](../certificates/round18_stable_proof_two_tails_control.json).

The separate 500-root reverse probe started in Round 17 has also completed its budget. The unrestricted-support, bridge-three search expands **450,000** states and discovers **28,283,636** with no join to the earlier chartless catalogue. This is a bounded search result. [Replay and probe receipts](../results/round18_stable_proof_two_tails.json).

## Reproduction

Regenerate `pivot-nodes.tsv` from the Round 17 one-pivot command. Generate the reverse roots from the published ordinary catalogue. The two scanners emit sorted closed catalogues for direct comparison.

~~~sh
mkdir -p "$work"
gzip -cd certificates/round17_ak3_e22_cap36_component.tsv.gz \
  | awk 'length($1)+length($2)<=31 && length($1)<=21 && length($2)<=21 {
      print "Z\t" $1 "\t" $2
    }' > "$work/reverse-roots.tsv"
c++ -std=c++17 -O3 experiments/round18_stable_proof_two_tails.cpp -o "$work/two-tails"
"$work/two-tails" 32 5000000 "$work/pivot-nodes.tsv" "$work/reverse-roots.tsv" \
  "$work/reverse32.tsv" --signed
"$work/two-tails" 32 5000000 "$work/pivot-nodes.tsv" "$work/reverse-roots.tsv" \
  "$work/audit32.tsv" --signed --stack-audit
cmp "$work/reverse32.tsv.states.tsv" "$work/audit32.tsv.states.tsv"
python3 -B experiments/round04_stable_proof_paths.py verify \
  certificates/round18_stable_proof_two_tails_control.json
~~~
