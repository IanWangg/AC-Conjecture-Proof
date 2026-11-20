# Strict ordinary entries to all nine cap-33 minima

Every energy-17 addition in the generated ordinary cap-33 component now has an explicit strict ordinary entry from AK(3) to its literal ordered words. The paths take **869 to 941** elementary instructions and have cyclic peak **33**. None of the nine signed orbits occurs in the independently verified cap-32 component. The cap-31 catalogue has 616 rows through energy 17, and the checked cap-32 addition catalogue has no such rows. Thus 33 is the exact entry peak at each of the nine markings. [Compressed strict ledgers](../certificates/round20_ak3_c33_minima_routes.json.gz), [individual replay receipts](../results/round20_ak3_c33_minima_routes.json), [native cap-33 provenance](round-18-cyclic33.md).

The compiler follows the actual parent records in reverse until it reaches a compacted energy-33 first-exit seed. The seed's stored parent supplies the old anchor. It searches back to the lower catalogues, lifts the whole reversed route from the literal terminal pair, and recovers a corresponding fixed-marking prefix from AK(3). Every cyclic product expands into elementary ordinary instructions. The published bundle records the parent route, intermediate lower routes and complete elementary ledger for each of the nine entries. [Ancestry and replay compiler](../experiments/round20_ak3_c33_minima_routes.py).

## Further constructive screens

All **109,894** cap-33 additions through energy 28 fail the arbitrary two-product primitive test. Complete subgroup comparisons with arbitrary independent conjugators give zero joins to the **23,902** verified archive pairs. Simultaneous ambient Whitehead minimization gives **108,404** classes, none matching the archive's 19,771 classes. Each of the 109,894 literal cyclic presentation complexes has a planar-link parity obstruction. The independent checker validates **167,939** equations in those witnesses. The nested energy-26 catalogue of 18,243 additions gives the same negative results under each test. [Checked prefix receipts](../results/round20_ak3_c33_low_prefix.json), [two-product method](round-18-ak3.md), [archive and planar-link methods](round-17-cyclic-peak-gap.md#further-checks-in-the-reverse-component).

The arbitrary two-product test also covers all **718,402** additions through energy 30, with no primitive witness. [Energy-30 receipt](../results/round20_ak3_c33_low_prefix.json).

## Parallel independent audit

The independent cap-33 verifier now validates catalogue rows in parallel before inserting them into its exact index in their original order. The stack reduction and boundary checks are unchanged. The cap-22 control matches the sequential report byte for byte across all **32,363** states, and dropping a boundary state still fails closure. The parallel production audit passed the older loader's catalogue checkpoint, so the duplicate sequential job was retired. The independent full audit continues. [Control and audit details](../results/round20_ak3_c33_minima_routes.json), [verifier](../experiments/round07_ak3_wide_verify.cpp).

## Reproduction

Replaying the saved ordinary ledgers needs only the Python standard library. To regenerate the ancestry routes, use the final Round 18 parent ledger after removing its first 1,258,633,777 32-byte seed records, the compacted seed directory, the cap-29 catalogue prefix through energy 24, and the full cap-22 catalogue. [Anchored data provenance](round-18-cyclic33.md#reproduction).

~~~sh
gzip -cd certificates/round20_ak3_c33_minima_routes.json.gz > "$work/minimums.json"
PYTHONPATH=experiments python3 -B - "$work/minimums.json" <<'PY'
import json
import sys
from elementary_verify import replay
from round08_ak3_acm_search import cyclic_peak
with open(sys.argv[1]) as reader:
    for row in json.load(reader):
        proof = row["certificate"]
        assert dict(replay(proof), cyclic_peak=cyclic_peak(proof)) == row["strict_replay"]
PY
c++ -std=c++17 -O3 experiments/round03_ak3_escape_path.cpp -o "$work/literal"
python3 -B experiments/round20_ak3_c33_minima_routes.py \
  certificates/round18_ak3_c33_low20.tsv "$ledger_tail" "$compacted" \
  "$waypoint_search" "$cap29_low24" "$cap22" "$work/literal" > "$work/routes.json"
c++ -std=c++17 -O3 -pthread experiments/round18_ak3_two_products.cpp -o "$work/two-products"
awk 'length($0)<=31' "$native.outside.tsv" > "$work/c33-low30.tsv"
"$work/two-products" "$work/c33-low30.tsv" 16
c++ -std=c++17 -O3 -pthread experiments/round07_ak3_wide_verify.cpp -o "$work/independent"
"$work/independent" --parallel-complete 33 14 "@$lower" "$native.outside.tsv" \
  "$work/c33-independent.json" 31 "$work/seed-manifest.txt"
~~~
