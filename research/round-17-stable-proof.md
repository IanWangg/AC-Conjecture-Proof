# Stable releases through the five minimum-energy orbits

2026-11-19. Five independently replayed stable paths from AK(3) now reach the five cyclic-energy-20 orbits of its external reverse component, with cyclic peak **33** and maximum rank **3**. For the exact marked endpoint of each ledger, the minimum ordinary entry peak is **37**. A further chartless excursion reaches a new marked energy-44 projection by a complete stable replay. [Strict path receipts](../results/round17_stable_proof_minima.json), [ordinary peak-37 comparison](round-17-cyclic-peak-gap.md).

## Five shorter endpoints

The historical name E22 refers to the pair `(XXYYYxYXY, XXYYxYXXyxxY)`. Its cyclic energy is **21** because the rows have lengths 9 and 12. The initial use of 22 counted the isolated stabilization row. All comparisons use the same literal marked words and the replayed peak bounds are unaffected.

Start with the strict 1,306-instruction Round 16 stable ledger. Lift the ordinary cyclic product routes to the five minimum-energy orbits in a fixed marking, and expand each product into strict elementary instructions. The ambient signed orbit keys only guide the search. Each ledger terminates at its stated literal free words. [Signed route inputs](../certificates/round17_stable_proof_minimum_routes.json), [fixed-marking compiler](../experiments/round17_stable_proof_minima.py).

| Exact endpoint | Ordinary suffix products | Ordinary suffix cyclic peak | Full stable moves | Full stable raw peak |
| --- | ---: | ---: | ---: | ---: |
| `(XXYYYxYXY, XXXYxxyXYxY)` | 1 | 21 | 1,317 | 41 |
| `(XXYYYxYXY, XXYxYXXYxxy)` | 1 | 21 | 1,326 | 41 |
| `(XXYxxYXXyxY, XXYYxxyyy)` | 8 | 29 | 1,405 | 41 |
| `(XXYxYXXyxxY, XXYYxxyyy)` | 10 | 33 | 1,460 | 48 |
| `(XXYxYXXYxxy, XXYYXYxYY)` | 2 | 23 | 1,343 | 41 |

Each ordinary suffix reverses through cyclic peak at most 33. An ordinary AK(3) path to that literal endpoint at peak 36 would therefore give an ordinary path to E22 at peak 36, contradicting its independent closure certificate. Concatenation with the strict cap-37 ordinary path to E22 attains peak 37 for all five endpoints. [Independent cap-36 closure and strict cap-37 path](round-17-cyclic-peak-gap.md#ordinary-exclusions-through-cyclic-cap-36).

## Exact one-pivot cut at cyclic peak 32

The strict 1,031-instruction prefix of Round 16 reaches `(zXyxxyy, XXYxYXXYxxy, XXYXYxxyXyxxy)` at peak 32. Consider the cyclic graph at that cap as long as there is exactly one auxiliary occurrence in the entire tuple. Its row is the pivot. A product using the pivot as donor transfers nonzero auxiliary exponent to the receiving row while leaving the pivot unchanged. It therefore leaves this sector. All allowed products use one of the two ordinary donors, so the pivot stays in its original slot. Erasing `z` shows that the two ordinary rows stay in the independently checked ordinary cap-36 component of E22. Their combined energy is at most 31. The 9,945 eligible ordinary pairs have minimum energy 20 and minimum coordinate width 9. [Original cleared prefix](round-16-stable-proof.md#direct-clearing-of-the-cap-32-chart), [ordinary cap-36 catalogue](../certificates/round17_ak3_e22_cap36_component.tsv.gz).

Before the first isolated auxiliary singleton, the pivot contributes at least two letters. Total energy is at least 22, and the fixed donor has width at least nine. A positive shortest relative bridge adds twice its length to the sum of the current lengths and the donor length, forcing energy at least 33. The full menu through the first singleton therefore has only zero bridges. Both ordinary widths are at most 21 because the other donor contributes at least nine letters and the pivot at least two. The pivot width is at most 12. At a first singleton, only the pivot changes and the same ordinary widths remain. These bounds establish completeness of the packed width-21 enumeration through the first singleton.

The complete forward closure from the cleared chart contains **4,544,552** ordered cyclic states and zero singleton returns. Thus a cap-32 clearing path from this chart must pass through a cyclic tuple with more than one auxiliary occurrence. This concerns the specified source and the rank-three tail before destabilization. [Exact closure driver](../experiments/round17_stable_proof_one_pivot.cpp), [closure receipt](../results/round17_stable_proof_minima.json).

A separate bounded reverse run started at the 7,229 width-eligible stabilized representatives from the ordinary cap-36 component and searched for any intersection with the 4,080,631 prior reachable chartless rank-three orbits. At cyclic cap 32, per-row width 21 and bridge bound three it expanded 350,000 states and discovered 17,003,696 without a join. [Reverse probe receipt](../results/round17_stable_proof_minima.json).

## A new chartless release

From the first energy-20 orbit, stabilize and explore signed rank-three cyclic products. The exploratory bootstrap prefers states in which the least-used generator occurs across more rows. It has depth at most ten and at most 3,500 expansions, with a stop threshold of 100 selected chartless entries. The following run expands chartless states in increasing energy order and records their charted first exits. At cap 37, with word width 21, energy floor 13 and bridge length at most three, **14,000** chartless expansions record **3,177** charted exits and **356** signed rank-two projections. The primitive test gives no hit. Whitehead minimization gives 356 distinct signed minima. The 13 of energy at most 36 all belong to the verified E22 ordinary cap-36 component. The others have minimal energy at least 41. No minimized key matches the original 23,902 verified archive marks. The bootstrap and run carry explicit finite limits. [Exploratory receipts](../results/round17_stable_proof_minima.json).

The shortest minimized projection outside the E22 cap-36 catalogue has an actual marked energy-44 representative

~~~text
XXYXYxyxYXYxy  XXXYXYYxyXYXyyxyxxxYXyyxyxYXYxy
~~~

A strictly compiled rank-three prefix reaches its literal deletion chart at cyclic peak **37**. The full marking transport and deletion use **6,569** strict instructions, with maximum rank **3**, cyclic peak **167**, and raw peak **210**. The higher cyclic peak belongs to the complete stable replay and arises during the transported marking. [Rank-three chart prefix](../certificates/round17_stable_proof_release44_prefix.json), [full stable ledger](../certificates/round17_stable_proof_release44.jsonl).

## Reproduction

~~~sh
mkdir -p "$work"
python3 -B experiments/round17_stable_proof_minima.py \
  certificates/round16_stable_proof_cap33_e22.jsonl \
  certificates/round17_stable_proof_minimum_routes.json "$work/minima"
c++ -std=c++17 -O3 experiments/round06_stable_proof_strict_verify.cpp -o "$work/check"
for ledger in "$work"/minima/stable-*.jsonl
do
  "$work/check" "$ledger"
done

python3 -B experiments/round09_stable_proof_rank_three_chart.py \
  certificates/round17_stable_proof_release44_prefix.json 2 "$work/release44.jsonl" --literal x
cmp "$work/release44.jsonl" certificates/round17_stable_proof_release44.jsonl
"$work/check" "$work/release44.jsonl"

printf 'zXyxxyy\tXXYxYXXYxxy\tXXYXYxxyXyxxy\n' > "$work/pivot-start.tsv"
c++ -std=c++17 -O3 experiments/round17_stable_proof_one_pivot.cpp -o "$work/one-pivot32"
"$work/one-pivot32" "$work/pivot-start.tsv" "$work/pivot-nodes.tsv"
shasum -a 256 "$work/pivot-nodes.tsv"
~~~
