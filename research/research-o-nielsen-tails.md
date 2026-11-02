# O follow-up: mixing one relator before conjugating, and an exact AK(2) control

Date: 2026-11-02. Status: further unbounded exclusions for explicit
restricted phases, plus an exact positive calibration. **No AK(3)
trivialization or global obstruction is established.** No novelty claim.

## Motivation and prior reading

After proving the [finite-tail reduction](research-o.md), I continued into
its explicitly excluded regime: perform coordinate Nielsen mixing first,
then independently conjugate the resulting relators. The original
independent-conjugates theorem applies to the two original words; it
cannot simply be reused for a changed basis of their subgroup.

I retained actual free words throughout. The only earlier computational
components used are M's strict coordinate-Nielsen expansion, primitive
test, and completion compiler, plus O's independently implemented subgroup
folding and signed-cycle certificate. The finite-tail lemma itself was
independently reviewed by P and the coordinating agent. The external
rank-two primitive facts and primary references are stated in O's main
report.

## 1. Entire short-prelude families, with unbounded subsequent tails

Start at `(p,b)=(xxxYYYY,xyxYXY)`. A signed Nielsen multiplication here
means one of the following eight choices: replace either coordinate by
its left or right product with the other coordinate or its inverse. It
is expanded into the permitted positive right multiplications and
inversions. No ambient generator automorphism is inserted.

After a prelude of these operations, take arbitrary independent ambient
conjugates of the resulting two words and permit arbitrary final Nielsen
operations. I tested whether this phase can create any ambient primitive
element in the generated subgroup.

For a pair `(a,b)`, replace each word by the lexicographically least cyclic
rotation of it or its inverse, after cyclic reduction, and sort the pair.
This normalization is only for the **family of all independent
conjugates**, not an implicit elementary AC move. Stripping a conjugating
prefix, rotating, or inverting either word does not change that family
of subgroups. Swapping their roles also preserves the family.

All preludes of at most one signed multiplication yield the first five
families below, including the empty prelude. All preludes of at most
three signed multiplications whose final total cyclic length is at most
23 yield precisely the seven displayed families:

| Cyclic/inverse representatives `(u,v)` | Tail cutoff | Reduced tails | Distinct based graphs |
|---|---:|---:|---:|
| `(XXXyyyy, XYXyxy)` | 6 | 1,457 | 1,378 |
| `(XXyxYXyyy, XYXyxy)` | 7 | 4,373 | 4,186 |
| `(XXXyyyy, XXyxYXyyy)` | 7 | 4,373 | 4,266 |
| `(XXXyxyXYXyyyy, XYXyxy)` | 9 | 39,365 | 37,882 |
| `(XXXyxyXYXyyyy, XXXyyyy)` | 9 | 39,365 | 38,611 |
| `(XXyxYXYxyxYXyyy, XYXyxy)` | 10 | 118,097 | 113,698 |
| `(XXXyyyy, XXXyyyyXXyxYXyyy)` | 11 | 354,293 | 347,680 |

Every one of the 561,323 reduced-tail checks passes the signed-double
acyclicity criterion. The per-family distinct graph counts sum to
547,701; this sum need not count graphs disjointly across different
families. The first five families alone have 88,933 tails and 86,323
per-family distinct graphs.

The prelude never changes the initial subgroup, which M proved
primitive-free. Thus each individual cyclic factor remains nonprimitive.
For each table row, O's shortest-double-coset lemma upgrades the finite
tail cutoff `floor(|u|/2)+floor(|v|/2)` to **all** relative conjugators.
Every generated subgroup in the stated phase therefore contains no
ambient primitive at any word length.

This is a computer-assisted restricted theorem. Its unbounded claims
are confined to the independently conjugated families explicitly reached
by the stated preludes. The length-23 filter is applied to the final
prelude words, not to all ordinary intermediate lengths, and it is not
an AC peak bound. Later interspersed conjugations and Nielsen mixing
remain outside the theorem.

## 2. Bounded exploration beyond the seven complete families

Without the cyclic-length filter, the same depth-three enumeration gives
29 canonical families, of total cyclic length at most 53. A separate
probe checks all 485 relative tails of length at most five for each of
them, 14,065 checks in total, and finds no signed-DAG failure. Unlike the
seven table rows, these cutoffs do **not** generally reach the lemma's
required bound. This observation supplies no unbounded exclusion for the
remaining families and no proof of AC nontriviality.

## 3. Exact positive AK(2) control

The same procedure succeeds on the already known AC-trivial AK(2),
starting from `(xxYYY,xyxYXY)`. One initial Nielsen multiplication, followed
by legal individual cyclic conjugations and inversions, reaches

    (XXyyy, XYxYYxy).

Its signed-cycle criterion is inconclusive, rather than certifying
primitive absence. Testing actual Nielsen basis variants then exposes a
primitive: right multiply the first coordinate by the inverse of the
second to get

    (XXyyXyyXyx, XYxYYxy).

The first coordinate cyclically reduces to `XyyXyyXy`, a primitive word.
The saved strict waypoint certificate uses **17 elementary moves** and
has exact raw total peak **17**. The full AK(2) completion, generated by
M's previously published primitive compiler, uses **131 elementary moves**
and has exact raw peak **39**, with free endpoint `(x,y)`.

The coordinating agent's independent strict verifier passes both files.
Each instruction is an inversion, positive right multiplication, or
single-generator conjugation. The completion compiler uses ambient
automorphisms only as a derivation device, transports moves back to the
original generators, and explicitly realizes the remaining basis change.
The saved ledger contains no implicit ambient generator move.

This is a useful calibration: the subgroup test distinguishes a reachable
primitive-containing AK(2) subgroup from the excluded AK(3) families, and
the discovery actually compiles to an ordinary free-basis path. It does
not solve any of the user's four requested breakthrough objectives.

## Reproduce

All published Python scripts reside together in `experiments/`. The
standard library suffices.

```sh
python3 experiments/nielsen_tail_probe.py --depth 1 --max-cyclic-total 20 \
  --output /tmp/nielsen_depth1_tail_results.json
python3 experiments/nielsen_tail_probe.py --depth 3 --max-cyclic-total 23 \
  --output /tmp/nielsen_depth3_tail_results.json
python3 experiments/nielsen_tail_probe.py --depth 3 --max-cyclic-total 200 \
  --max-tail 5 --output /tmp/nielsen_depth3_tail5_results.json

python3 experiments/ak2_tail_control.py --directory /tmp/ak2_tail_control
python3 experiments/elementary_verify.py \
  /tmp/ak2_tail_control/o_ak2_tail_waypoint.json \
  /tmp/ak2_tail_control/o_ak2_tail_full.json
```

The larger seven-family enumeration can take substantially longer than
replaying the small AK(2) certificates. The result files retain the exact
prelude words and strict ledgers for every chosen family representative.
Runtime fields are observational and may differ on replay.

No actual AK(3) primitive waypoint has been found by this investigation.
The finite-tail reduction narrows a specified search regime; it gives no
termination argument or invariant for arbitrary ordinary AC paths.
