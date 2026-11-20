# Energy-30 catalogue screens and ordinary continuation probes

2026-11-19. All **718,402** additions through energy 30 in the generated cap-33 ordinary component have now been compared with the **23,902** verified archive pairs. An exact rank-two basis test allows arbitrary independent conjugators and signed simultaneous ambient permutations. It checks **1,409,556** nonempty reverse bridges and finds zero joins. A separate simultaneous ambient Whitehead comparison finds **708,820** classes in the forward prefix and zero matches. The literal link check supplies parity contradictions for all 718,402 canonical complexes. An independent witness checker verifies **1,215,264** equations. Round 20 excludes a terminal primitive in two arbitrary products from every source in this prefix. [Complete receipts](../results/round21_ak3_cap33_and_probes.json), [two-product results](../results/round20_ak3_c33_low_prefix.json).

## Two ordinary search strategies

Nine cyclic probes start at the nine literal energy-17 minima and use the energy-30 prefix as a novelty score. They sample **52,414,837** products and each retain 350,000 nodes. The product caps are 46, 50 and 54. No sampled product exposes a primitive. The union of the elite reservoirs has **524** distinct literal cyclic pairs. The uncapped two-product test is negative at all 524. A complete primitive-map test separately decides each of their literal based subgroups, covering 523 distinct folded graphs and finding no primitive. [Cyclic probe](../experiments/random_cyclic_escape.cpp), [exact based-subgroup audit](../experiments/audit_escape_elites.py).

Three subgroup-phase probes start at minima 1, 5 and 9. They make **2,400,000** total proposals with phase-end caps 75, 79 and 83. They make 610,202 graph classifications summed over runs, using prior tests or the signed transition graph, and find neither a primitive nor a direct archive core join. After deduplication the retained nodes give **65,657** literal cyclic pairs. Their simultaneous ambient comparison also has no archive join. The **5,000** lowest-energy distinct pairs whose shorter coordinate has length at least seven all pass the exact two-product exclusion. This tests trajectories that change both initial coordinates. Every one of the **1,151** resulting signed orbits through energy 33 with both coordinates of length at least seven also occurs in the generated cap-33 additions, accounting for the short returns through this search. [Subgroup probes](../experiments/coupled_h_search.cpp), [receipts](../results/round21_ak3_cap33_and_probes.json).

Twelve saved paths compile from the nine existing AK(3) ledgers using strict moves. The stored paths give actual reachability of the corresponding endpoints. Proposals and node retention in these probes are heuristic, and subgroup-phase caps refer to the selected phase boundaries. [Path bundle](../certificates/round21_ak3_probe_paths.json.gz), [entry ledgers](../certificates/round20_ak3_c33_minima_routes.json.gz).

## Sharp ordinary entries to the twenty stable endpoints

Each of the twenty literal endpoints of the stable first-chart ledgers also admits a strict ordinary path from the first energy-17 marking. A fixed-marking cyclic search gives all twenty paths up to rotation, inversion and row order at cap 22. Compiling to the literal ordered endpoints gives **23 to 92** elementary instructions. Eleven local ledgers peak at 22 and nine peak at 28, with the latter increase occurring during row-order alignment. Prefixing the 879-instruction strict ordinary entry gives peak **33** for all twenty literal endpoints. This peak is sharp. Any peak-32 ordinary entry to one of the endpoints could be followed by the reverse local path, yielding a peak-32 ordinary entry to the first energy-17 marking, which is excluded by the verified cap-32 component. [Twenty local ordinary ledgers](../certificates/round21_ak3_stable_projection_ordinary.json), [stable endpoints](round-21-stable-proof.md), [sharp first energy-17 entry](round-20-c33-minima.md).

## Independent cap-33 audit under the memory limit

The interrupted audit had loaded all 1,858,329,806 rows before its process ended. The next run preallocated exactly that many 16-byte packed rows, avoiding a transient second vector during growth. It rejects both too many and too few rows. The row vector, $2^{31}$ four-byte index slots, and four-byte connectivity parents total about **42.61 GiB**. Worker buffers have separate small bounds. A process-group monitor used a **54 GiB** cutoff for this run with additional headroom in the aggregate research budget. The cap-22 control is byte-identical to the unreserved audit, and requesting one fewer row fails before exceeding the allocation. At the requested stop, the last logged checkpoint was **1,680,555,831 rows** and this process group's sampled peak was **33.76 GiB**. The loader did not save an index checkpoint. The independent full graph verdict remains pending. [Verifier](../experiments/round07_ak3_wide_verify.cpp), [memory monitor](../experiments/round21_memory_guard.py), [control result](../results/round21_ak3_cap33_and_probes.json).

## Reproduction

Set `native` to the generated cap-33 output prefix, `reverse` to the 23,902-pair verified archive, `lower` to the cap-32 manifest, and `seeds` to the 128 compacted shard paths manifest. [Catalogue inputs](round-18-cyclic33.md#reproduction), [archive inputs](round-04-ak3.md#reproduce).

~~~sh
awk 'length($0)<=31' "$native.outside.tsv" > "$work/low30.tsv"
c++ -std=c++17 -O3 experiments/round13_stable_proof_projection_index.cpp -o "$work/projection-index"
c++ -std=c++17 -O3 experiments/round17_ak3_ambient_join.cpp -o "$work/ambient"
"$work/projection-index" "$work/low30.tsv" "$reverse" "$work/low30-joins.json"
"$work/ambient" "$work/low30.tsv" "$reverse"
python3 -B experiments/round17_ak3_link_screen.py "$work/low30.tsv" --workers 6
c++ -std=c++17 -O3 -pthread experiments/round07_ak3_wide_verify.cpp -o "$work/independent"
python3 -B experiments/round21_memory_guard.py 54 "$work/independent" \
  --parallel-complete 33 14 "@$lower" "$native.outside.tsv" "$work/independent.json" 31 "$seeds" 1858329806
~~~

The cyclic probes use the first nine rows from the [low cap-33 catalogue](../certificates/round18_ak3_c33_low20.tsv) and a JSON list of the energy-30 prefix pairs with each coordinate normalized by `free_waypoint_search.canonical`. Use seeds $2100+i$, at most 8,000,000 attempts per run, 350,000 nodes, and caps $46+4((i-1)\bmod3)$. The subgroup probes use the low prefix TSV and verified archive as their two inputs, the second archive disabled, seeds $2120+i$ for $i=1,5,9$, 800,000 attempts, at most 70,000 nodes, caps $74+i$, and raw Nielsen preludes of length at most $12+\lfloor(i-1)/2\rfloor$. The saved witnesses can be replayed directly without either search.

~~~sh
PYTHONPATH=experiments python3 -B - <<'PY'
import gzip
import json
from compile_cyclic_edge_path import compile_path as compile_cyclic
from compile_h_phase_path import compile_path as compile_subgroup
from elementary_verify import replay
from round08_ak3_acm_search import cyclic_peak

with gzip.open('certificates/round20_ak3_c33_minima_routes.json.gz', 'rt') as source:
    entries = [item['certificate'] for item in json.load(source)]
with gzip.open('certificates/round21_ak3_probe_paths.json.gz', 'rt') as source:
    paths = json.load(source)
for row in paths['cyclic']:
    parent = entries[row['seed'] - 2101]
    branch, _ = compile_cyclic(row['path'])
    assert branch['start'] == parent['target']
    proof = dict(branch, start=parent['start'], moves=parent['moves'] + branch['moves'])
    assert dict(replay(proof), cyclic_peak=cyclic_peak(proof)) == row['replay']
for row in paths['subgroup']:
    proof, _ = compile_subgroup(row['path'], entries[row['seed'] - 2121])
    assert dict(replay(proof), cyclic_peak=cyclic_peak(proof)) == row['replay']
with open('certificates/round21_ak3_stable_projection_ordinary.json') as source:
    comparisons = json.load(source)
for row in comparisons:
    branch = row['local']
    assert branch['start'] == entries[0]['target']
    assert dict(replay(branch), cyclic_peak=cyclic_peak(branch)) == row['local_strict']
    proof = dict(branch, start=entries[0]['start'], moves=entries[0]['moves'] + branch['moves'])
    assert dict(replay(proof), cyclic_peak=cyclic_peak(proof)) == row['full_strict']
PY
~~~
