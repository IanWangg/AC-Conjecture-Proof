# Round 12 stable AC proof track

2026-11-19. A strict rank-three path from stabilized AK(3) loses all primitive relators, recovers a primitive pivot and projects to a distinct rank-two ambient class. A second strict path changes the remaining nonprimitive donor while all three rows stay nonprimitive. The first chartless entry after exactly two cyclic products from the Round 11 excursion requires peak 31. Changing that donor within the resulting chartless corridor requires peak 35. [Exact search and replay results](../results/round12_stable_proof_corridor.json).

## Complete two-product entrances and chartless corridors

Start at the ordered strict rank-three waypoint
`(XXYYxyyyxYZY, XYYXyxy, XYYXyxyz)`. The first and third rows are primitive because each has one occurrence of the generator \(z\). Whitehead descent certifies that the second row is nonprimitive. Any first entry into the chartless sector in two cyclic products must replace a primitive row in the first product and the remaining primitive row in the second. Rank-three Whitehead reduction tests primitiveness also when none of the letters has one occurrence. After the first chartless entry, the search expands only chartless states and records every adjacent charted exit. [Starting ledger](../certificates/round11_stable_proof_source_excursion.json), [native search](../experiments/round12_stable_proof_corridor.cpp).

The native menu enumerates both row signs, relative rotations and all shortest bridges within the cyclic cap, quotiented by all 48 signed ambient permutations, row inversions, cyclic rotations and row permutations. Total cyclic energy starts at three, the minimum for three nonempty rows. The search checks the 21-letter encoding width and counts admissible products beyond it. There are zero width omissions through cap 36 and 8,978 omitted occurrences in the cap-37 sample. The independent string reducer recomputes the two-product entrances and the reached chartless components at caps 31 and 34. It also counts every charted first exit, whether or not another exit gives the same quotient. At cap 34 the independent count is 1,512,072 literal menu checks. [Independent audit and compiler](../experiments/round12_stable_proof_corridor.py).

| Cyclic cap | Two-product chartless entries | Chartless orbits reached | Charted first exits | Signed rank-two projections | Chartless expansion |
| ---: | ---: | ---: | ---: | ---: | --- |
| 30 | 0 | 0 | 0 | 0 | Complete |
| 31 | 1 | 7 | 9 | 5 | Complete |
| 32 | 1 | 18 | 23 | 16 | Complete |
| 33 | 2 | 253 | 205 | 113 | Complete |
| 34 | 2 | 505 | 466 | 276 | Complete |
| 35 | 6 | 2,126,151 | 173,132 | 81,275 | First 120,000 expansions |
| 36 | 201 | 4,759,668 | 199,840 | 96,273 | First 120,000 expansions |
| 37 | 224 | 11,266,949 | 231,218 | 112,452 | First 120,000 expansions with the word-width filter |

Every tested exit has a rank-two quotient with two nonprimitive coordinates. The scanner uses one chart per primitive relator. Any other chart at that relator changes the two images by a free-group automorphism, which preserves primitiveness. At cap 34 the 276 projected Whitehead-minimal signed pairs all have independently verified planar-link parity obstructions. None of the original marked projections occurs among the 22,426 signed orbits of 23,902 known-trivial archive rows. All 58 compact Whitehead-minimum representatives through energy 32 are in the generated ordinary AK(3) catalogue. Of these 55 are already in cap 31 and three appear in the cap-32 extension. The all-tail basis index returns zero matches against the archive for those 58 representatives. [Cap-32 generation](round-11-cyclic32.md), [all-tail basis test](round-04-ak3.md), [projection receipts](../results/round12_stable_proof_corridor.json).

The geometric control starts at a chartless rank-three tuple on an independently verified 48-instruction route to a basis. At cap 30 the new scanner finds a primitive projection in a single cyclic product. Its marked 23-instruction replay ends at `(XXyyy, Xy, XXZyxzXZxZXYzyyy)`, and eliminating either of the two one-occurrence letters in `Xy` gives a quotient with primitive coordinate `X`. [Existing basis suffix](../certificates/round11_stable_proof_geometric_suffix.json), [positive control and strict replay](../results/round12_stable_proof_corridor.json).

## Strict change of chart

The cyclic product path has primitive row counts \(2,1,0,0,1\) at its five vertices. The last vertex in the marked free group is `(XYxZyxYxyzy, XYYXyxy, Z)`. Its full rank-three prefix from stabilized AK(3) has 228 elementary instructions, raw peak 43 and cyclic peak 31. Clearing the first two rows with the recovered singleton and destabilizing gives `(XYXyxYYXy,XYYXyxy)` in 256 strict stable instructions with the same peaks and maximum rank three. Its independent Whitehead minimum has total energy 15, compared with 17 for the initial chart, so the projections define different ambient classes. The new pair also belongs to the ordinary cap-22 catalogue. [Rank-three prefix](../certificates/round12_stable_proof_corridor_prefix.json), [strict stable ledger](../certificates/round12_stable_proof_corridor_chart.jsonl), [independent verification](../results/round12_stable_proof_corridor.json).

## Changing the remaining donor

The original nonprimitive row \(B=\texttt{XYYXyxy}\) must survive both entrance products. At cap 34 every chartless state after the entrance still contains exactly one word in its signed cyclic class. The independent marked menu detects zero chartless edges changing that row up to cyclic rotation and inversion in the fixed marking. At cap 35 a third cyclic product can change \(B\) while keeping the tuple chartless. The strict 223-instruction certificate from stabilized AK(3) reaches `(XXYxyzXyxYZY, XYxZyxYxyzy, XYxZyxZYxyzy)` with raw peak 43 and cyclic peak 35. All three rows lie outside the signed cyclic class of \(B\). The sampled cap-35 corridor contains 162,182 chartless states with this property. The sharp peak 35 applies to paths that enter the primitive-free sector in exactly two cyclic products from the Round 11 waypoint and stay there until the donor class disappears. [Strict donor-change ledger](../certificates/round12_stable_proof_corridor_donor_release.json), [complete lower component and larger sample](../results/round12_stable_proof_corridor.json).

While \(B\) is fixed the quotient admits an explicit free-by-cyclic normal form followed by a free product with the infinite cyclic factor on the unused generator. Put \(x_i=y^i x y^{-i}\). The quotient relation is \(x_0^{-1}x_{-2}^{-1}x_{-1}=1\), equivalently \(x_{i+2}=x_i^{-1}x_{i+1}\) for all \(i\). Writing \(a=x_0,b=x_1,t=y\) gives
\[
  \langle a,b,t\mid tat^{-1}=b,\ tbt^{-1}=a^{-1}b\rangle * \langle z\rangle .
\]
The forward substitution on \((a,b)\) has inverse \((ab^{-1},a)\). In the reverse map \(b\) goes to \(yxy^{-1}\); the second conjugation relation is the \(y^2\)-translate of the original word relation. This quotient can be used for joint tests of the remaining rows before the first release of the donor.

## Reproduction

Use the known-trivial reverse archive from the [archive replay](round-04-ak3.md#reproduction), the ordinary cap-31 catalogue and the cap-32 outside catalogue from the [cap-32 report](round-11-cyclic32.md). The large search catalogues are scratch files. The saved receipt records the complete and budgeted search counts and the two strict forward witnesses.

~~~sh
mkdir -p "$work"
c++ -std=c++17 -O3 -pthread experiments/round12_stable_proof_corridor.cpp -o "$work/corridor"
for cap in 30 31 32 33 34 35 36 37; do
  "$work/corridor" 3 "$cap" 120000 XXYYxyyyxYZY XYYXyxy XYYXyxyz "$work/final$cap" > "$work/final$cap.json"
done
"$work/corridor" 3 30 12000 XXXyyyy XXZyxzXZxZXYzyyy XXyyy "$work/finalcontrol" > "$work/finalcontrol.json"
python3 -B experiments/round12_stable_proof_corridor.py "$work" "$reverse" --certificates "$work"
python3 -B experiments/round12_stable_proof_corridor.py "$work" "$reverse" --independent-cap 34
c++ -std=c++17 -O3 experiments/round06_stable_proof_strict_verify.cpp -o "$work/strict-verify"
"$work/strict-verify" "$work/round12_stable_proof_corridor_chart.jsonl"
c++ -std=c++17 -O3 experiments/round06_ak3_orbit_index.cpp -o "$work/orbit-index"
"$work/orbit-index" "$work/projection-minima32.tsv" "$reverse" "$work/all-tail.json"
rg -x -F -f "$work/projection-minima32.tsv" "$cap31" > "$work/projection-minima32.in-cap31.tsv"
rg -x -F -f "$work/projection-minima32.tsv" "$outside32" > "$work/projection-minima32.in-outside32.tsv"
~~~
