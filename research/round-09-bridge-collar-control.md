# Separating cuts for a noninjective two-copy overlap

2026-11-19. Two explicitly nested AK(3) lobes admit a family of arbitrarily long bridges for which the join based at opposite attachments is primitive-free. The self-fiber-product component has a noninjective projection, so the common-subtree argument from round seven does not apply. A strict 33-instruction ordinary path verifies the first example. [Exact path and folded-graph checks](../results/round09_bridge_collar_control.json).

## Folding before reattaching the far lobes

Take two immersed rank-two barbells, each with a chosen root. Cut one bridge edge in each barbell, and fold the based join of the two components containing the roots. Keep track of the images of the two near endpoints where the edges were cut. Suppose the outward label of each cut edge is unoccupied at its near image in the folded join. If the near images agree, require the two outward labels to differ. Now reattach both far components and their cut edges. The far components retain their original labels and were kept disjoint from the fold. The two local direction tests make the resulting graph immersed, so it realizes the same based subgroup as the complete folded join.

Each reattached edge is separating. An ambient-primitive cyclic word in $F(x,y)$ uses only one sign of each generator that occurs, in the fixed marking. Its loop cannot cross a separating edge in both directions. If the folded root-containing join is primitive-free and each far lobe is nonprimitive, no primitive exists in the complete join. This condition does not require injectivity of either projection of the off-diagonal self-product component. [Rank-two primitive criterion and partial-map verifier](../experiments/primitive_map_pairs.py).

## Nested AK(3) control and an unbounded bridge family

Use cyclic representatives `XXXyyyy` and `XYXyxy` of the AK(3) rows. Conjugate the second around the old bridge `xxY`, and multiply it by the first. Rotating both resulting lobe circuits by three letters gives `yyyyXXX` and `yyyyxxYXYXyxyyXXXXX`. The longer cyclic word contains the entire shorter lobe at a different starting position. Fold these marked lobe loops at their roots. Their shared root has no outgoing `X` or `Y` in the folded graph, and the complete partial-map test certifies primitive absence there.

For every reduced bridge beginning with `X` and ending in `y`, join two copies based at their left and right attachments respectively. Cut the first edge in the left-rooted copy and the last edge in the right-rooted copy. Their two near directions are exactly the vacant `X` and `Y`. The far components each contain one of the already checked lobes. The cut criterion therefore gives primitive absence for this rebased join throughout the whole bridge family.

For the bridge `Xy`, the 33-instruction replay reaches the marked barbell at raw peak 30. The self-fiber-product component of its opposite roots contains both $(7,13)$ and $(7,16)$ in the rooted adjacency numbering, witnessing noninjectivity. A complete exact test on the full 43-vertex joined graph verifies 156 closed partial-map pairs. Other root alignments require their own cuts or separate primitive checks.

~~~sh
python3 -B experiments/round09_bridge_collar_control.py \
  | diff - results/round09_bridge_collar_control.json
~~~
