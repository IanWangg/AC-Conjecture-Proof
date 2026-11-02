# Explicit ordinary walks beyond the certified cyclic component

Coordinating-agent investigation, 2026-11-02. **Heuristic exploration,
not an AC obstruction or a solution.** No novelty claim is made.

After the complete cap-22 component was independently audited, I sought
actual free-group paths outside it. Q and R were independently testing
arbitrary-tail subgroup completions within the component, while S
examined the remaining deletion quotients. This experiment complements
those analytic and exhaustive investigations.

## Actual free-word search

The C++ walker stores cyclic conjugacy representatives, but each edge
is an actual signed rotation, relative conjugation, relator multiplication,
and subsequent individual conjugations. It records parents and exact
word choices. No quotient equality, stabilization or ambient generator
automorphism is inserted.

Four runs use seeds 271828 through 271831, a cyclic boundary cap of 90,
at most five million proposals each, and at most 400,000 stored nodes
per run. The initial literal pairs are respectively

    (XXXXYxxxy, XYXyy),
    (XXYxY, XYYYYxyyy),
    (XXXXyxxxY, XYYXy),
    (xxxYYYY, xyxYXY).

The first three are in the independently connected cap-22 component;
the fourth is the original AK(3) tuple. Their ordinary reachability is
therefore established before the heuristic suffix begins.

The sampling favors short coordinates, new cyclic words, and tuples
outside the known component, with restarts among retained promising
nodes. This is a search policy, not a distance estimate or a completeness
argument. In particular the length and node cutoffs exclude most possible
ordinary paths. Search trajectories can depend on the host's floating
point library and tie ordering.

The recorded runs make **19,647,745 proposals**, storing **1,368,811**
nodes in total, of which **1,368,804** lie outside the known component.
These are sums of per-run counts; states across different runs are not
deduplicated. No primitive coordinate was found. The coordinate test uses
the exact rank-two Euclidean/Nielsen classification, and its implementation
passes the complete literal cyclic-word primitive census through length
nine. The failed runs themselves establish no unbounded negative result.

## Selected hidden-primitive tests

The four runs retain 763 promising literal pairs. R's new exact finite
partial-map algorithm decides that all 763 generated subgroups contain
no ambient primitive at any word length; no selected decision reaches
its state budget. This concerns those selected subgroups, not all stored
walk states or all paths outside cap 22.

Q then independently enumerates every rotation of both coordinates in
these selected pairs. Its full 160,479-rotation scan finds 78,712 distinct
unbased labelled core graphs: 78,710 pass the signed-DAG test, and R's
complete finite-map test excludes the two remaining graphs in 232 map-pair
states. By Q/R's axes theorem, all independently conjugated versions of
these 763 selected pairs are therefore primitive-free as well. See Q's
separate outside-frontier addendum for that computation and its scope.

This closes the attempted primitive completion for these endpoints. It
does not constrain later conjugations of new Nielsen words, or untested
endpoints.

## A fully expanded ordinary AK(3) ledger

For the original-AK(3) run, the saved 44 product macros compile to an
exact strict ledger with **2,159** elementary moves. Its endpoint is

    (XYXyxy, XXXXyxyXYXYxxyxyy).

The independent elementary verifier gives raw total peak **67**; replaying
every strict operation gives cyclic total peak **63**. The endpoint has
cyclic total length 23 and is not a free basis. The supplied macro path,
compiler, compressed full ledger and exact result make this ordinary
reachability independently reviewable. No minimality claim is made.

The compressed selected-pair data retain seed and node identifiers.
The C++ command can select a saved node for path recovery on an identical
trajectory. The exact published ledger above is replayable independently
of random-number or floating-point behavior.

## Reproduce

Compile `experiments/random_cyclic_escape.cpp`. Its first argument is
N's decoded explicit JSON catalogue, not the split-file manifest. For
example, using the original tuple:

    /tmp/random_cyclic_escape /tmp/cyclic22.json 271831 5000000 400000 90 /tmp/search.json /tmp/path.json xxxYYYY xyxYXY

The optional final numeric argument selects a retained node for path
recovery. Run `--primitive-selftest` to check the finite primitive census.
The wrapper compiler accepts the saved `cyclic-edge-path-v1` JSON and
expands every macro using the published ordinary move routines:

    python3 experiments/compile_cyclic_edge_path.py certificates/outside_ak3_macro_path.json --certificate /tmp/strict.json --output /tmp/replay.json
    python3 experiments/elementary_verify.py /tmp/strict.json

`experiments/audit_escape_elites.py` recomputes exact primitive decisions
on the selected-pair JSON using R's standalone detector. The selected
pairs, detailed audit and full strict ledger are stored as ordinary
gzip/base64 JSON artifacts; decode with the Python standard library.

These experiments found no actual AK(3) primitive or basis. The full
original four objectives remain unachieved.
