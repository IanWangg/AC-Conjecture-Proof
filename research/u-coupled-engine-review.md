# U supplement: coupled subgroup-search review and AK(2) calibration

Date: 2026-11-02. **No AK(3) or unrestricted AC result is asserted.**

I independently read the root's `coupled_h_search.cpp`, its use of U's
native API, its status cache, and its constructive phase compiler. The
reviewed engine's SHA256 is
`ebbdf288ad9b934b600c659ea990954a8d9c6e14ca06c52981cdf457150e8c70`.
This identifies the first source version, before the root's subsequent
addition of a `.native.jsonl` output journal. The source audit below is
scoped to that identified version and API integration; the independent
literal certificate replay does not depend on the logging addition.
The native call and positive-hit handling are sound within their stated
search limits. The following details distinguish mathematical absence
from choices that can make this heuristic fail to find a positive.

## Native classification and caching

The call passes `g.out` directly to `u_native::decide`. Its type and
letter order are the required `vector<array<int,4>>` with `x,X,y,Y` and
`-1` for a missing arc. The 100,000-state budget applies separately to
each signed alphabet. Fixed-point tests cover every real vertex, so
the displayed pair need not itself have a primitive coordinate.

Before the native call, the engine uses two negative filters. Literal
tuple-class membership in the verified cap-22 catalogue is safe because
Q/R's theorem covers arbitrary independent conjugates of those classes.
Q's direct signed-DAG criterion is a sufficient absence test. These are
mathematical filters, unlike a score or word-length penalty. A native
`ABSENT` result is cached only after complete exhaustion.

The graph key forgets the basepoint and records the unbased labeled core.
Ambient primitive existence is invariant under simultaneous conjugation
and vertex renaming, so caching a proved negative by this key is safe.
A positive is checked before acceptance by score or duplicate-node
rejection and terminates the run. Thus neither the temperature filter
nor the accepted-node deduplication discards an already detected positive.

`INCOMPLETE` is stored under a separate cache value and logged with an
actual word pair and parent node in `.incomplete.jsonl`. The current run
does not retry that graph. This remains an unresolved case, never a
proved absence. With the same deterministic algorithm and state budget,
merely renumbering an isomorphic graph would not extend the explored
map-pair closure; a useful retry must increase the budget or use another
method. Any future resumption must preserve the unresolved status and
must not interpret mere cache membership as a negative theorem.
The successful AK(2) calibration has zero incomplete graphs.

The initial graph is not classified before the first phase. Current
AK(3) and AK(2) starts are already known primitive-free from the earlier
complete graph tests, so this does not invalidate those calibrations.
For a general supplied start, a primitive could already be present and
this engine would not explicitly recognize that initial success.

The counter `distinct_classified_graphs` counts cache entries. It
includes unresolved entries, and the final positive is not inserted into
that cache. This is a bookkeeping convention, not a count of exclusively
proved negative graphs or all positive/negative classifier returns.

## Phase construction and search limits

The engine takes a genuine spanning-tree basis of the current folded
rank-two subgroup, applies freely reduced raw Nielsen words, and only
then independently cyclically reduces, inverts and rotates the two
coordinates. Keeping raw words during the prelude is essential:
independent cyclic normalization inside the prelude could change the
subgroup. The code's final rotations are the intentional subgroup-changing
conjugation phase. A spanning-tree basis replacement is a change of
subgroup generators; the root's compiler expands it into ordinary moves
instead of treating it as a permitted free move.

The search is heuristic. It samples a bounded number of Nielsen moves,
discards a prelude when its raw length exceeds `4*cap`, limits its final
cyclic energy, and discards 90% of sampled source bases below energy 23.
It also biases acceptance by a score and temperature, and keeps only
selected nodes for later exploration. These choices can miss actual
positive routes. The low-energy discard particularly makes the known
AK(2) positive phase less likely to be sampled. None of these restrictions
supports an unbounded negative AC conclusion.

The positive JSON includes a symbolic L/R program and an `expanded` flag.
An unexpanded witness is still a positive mathematical detector result,
but a literal elementary completion must expand and verify it before
publishing a strict certificate. The successful control below is fully
expanded.

## Independent successful control replay

The root's AK(2) run with seed `20261103` finds a primitive after 138,768
sampled attempts, along a retained path of 27 subgroup phases. U
independently refolds its actual positive pair

```
(XXyyy, XYxYYxy)
```

and obtains exactly the recorded graph and positive witness:

```
alphabet xY, program RLRL, component 1, fixed vertex 3,
base path XX, cyclic primitive xYxYYxYY,
based primitive XYxYYxYYxx.
```

A separate Python word replayer, importing none of the root/T/M/R
elementary-move implementations, checks every operation in the three
literal ledgers. It permits only coordinate inversion, positive right
multiplication by the other coordinate, and conjugation by a single
signed ambient letter. The results are:

| Ledger | Strict moves from literal AK(2) | Raw total-length peak | Endpoint |
| --- | ---: | ---: | --- |
| Compiled 27-phase prefix | 1,305 | 153 | `(XXyyy,XYxYYxy)` |
| Primitive exposed | 1,309 | 153 | `(XYxYYxYYxx,XYxYYxy)` |
| Complete certificate | 1,521 | 153 | `(x,y)` |

Each ledger is an actual instruction prefix of the next. All three
start at literal `(xxYYY,xyxYXY)`, so they certify AK(2), not AK(3).
The complete ledger, published as
`certificates/coupled_ak2_full.json`, has SHA256
`d548c988f9d1d9ddd97b7feafdc30f772e4ab4fac447eeb180ae968434294274`.
This checks that the root's sampled phase path, exact detector and
literal compiler connect successfully on a known trivializable case.
It makes no claim about an improved AK(2) bound.

The reusable independent check is `experiments/u_review_h_control.py`;
the complete input hashes and replay results are in
`results/u_root_h_control_review.json`. The repository mode reads the
public `coupled_ak2_strict.json`, `coupled_ak2_exposed.json`,
`coupled_ak2_full.json`, `coupled_ak2_primitive_hit.json` and
`coupled_ak2_phase_path.json` under `certificates/`, plus
`results/coupled_ak2_control_results.json`. From the published checkout,
after building the native detector, run:

```sh
python3 experiments/u_review_h_control.py --repository-root . --binary /tmp/u-native --output /tmp/u-h-control-review.json
```

U's [main report](research-u.md) gives the native build command. The
purpose of this supplement is to validate the classifier integration
and a positive proof pipeline. Failure to find a primitive in any later
finite AK(3) run remains only a finite search outcome.
