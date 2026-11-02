# P follow-up: a genuine cyclic-length-fourteen waypoint

Date: 2026-11-02. **No free-basis endpoint or global AC obstruction is
established.** This is an exact further ordinary-AC equivalence and a
restricted primitive-absence theorem. No novelty claim is made.

## Discovery and exact free identity

After [P's arbitrary-tail audit](research-p.md), I investigated a Nielsen
prelude before a fresh individual conjugation, a regime not covered by
that theorem. To complement O's initial-tuple probe, I used the two actual
waypoints from [M's transition certificates](research-m-hump-transitions.md).
A single positive relator product from the first waypoint gave a shorter
cyclic pair. Write

    r=XXyxYxxY,
    u1=yXYXyxx,
    u2=YxYXyyx,
    g=XYxx.

There is the following exact identity in the **free group**, established
by concatenation and free cancellation:

    g (r u1) g^-1 = u2.

For clarity, `r u1` freely reduces to `XXyxYxYXyxx`, whose cyclic reduction
is `yxYxYXy`, a rotation of u2. The final certificate expands the cyclic
operations as ordinary signed-generator conjugations; it inserts no
rotation or quotient equality as a move.

Starting from the literal tuple `(u1,r)`, the five strict operations are:

1. Replace the second relator by its positive right product with the first.
2. Conjugate the second relator successively by `x,x,Y,X`.

The composite conjugator is `XYxx`, since successive conjugations compose
from right to left. The first relator remains literally u1.

Appending these five operations to M's 222-move ledger yields a complete
ordinary certificate from the original AK(3) tuple to

    (yXYXyxx, YxYXyyx).

The coordinating agent then improved the full ledger to **189 strict
moves with raw peak 25**, using M's shorter `(u2,r)` entry. The identity
can be used in reverse: conjugate u2 by `g^-1=XXyx` to obtain `r u1`,
invert r and positively right multiply it by `r u1` to obtain u1, then
restore the first coordinate by conjugation with g. This gives the same
two relators in reversed order `(u2,u1)` with ten added strict moves.
Both expansions are saved and checked; the 189-move version is preferred.

The endpoint has raw and cyclic total length **14**. This tuple is newly
explicitly recorded here relative to the earlier two displayed waypoints,
each of cyclic total length 15. The coordinating agent subsequently checked
all 49 pairs of cyclic rotations of `(u1,u2)` against the saved raw cap-21
checkpoint: every key was already in that earlier component. Thus this
explicit ledger does not escape the previously searched region, and its
raw peak is a property of the supplied path, not a minimum required peak.
No novelty claim concerning the literature is made.

| Verified quantity | Value |
|---|---:|
| Preferred strict moves / exact raw peak (coordinating agent) | 189 / 25 |
| First strict moves / exact raw peak (P) | 227 / 31 |
| Endpoint raw/cyclic total length | 14 |
| Folded endpoint graph vertices | 12 |
| Folded endpoint graph rank | 2 |

Both relators are cyclically reduced and nonprimitive. The tuple is not
the standard basis.

## All independent conjugating tails are still primitive-free

P's independently written graph code checks the new pair using the
finite-tail reduction proved in [P](research-p.md) and [O](research-o.md).
Both word lengths are seven, so the required relative-tail bound is
`floor(7/2)+floor(7/2)=6`.

All **1,457** reduced relative tails through length six give **1,404**
distinct based subgroup graphs. Every one passes all eight signed
double-free line-graph acyclicity tests: **11,232** DAG checks in total.
The separate circle tests also pass. The bridge argument therefore
extends this finite check to every relative tail at every length.
Consequently, for all a,c in F(x,y),

    <a u1 a^-1, c u2 c^-1>

contains no ambient primitive element. After such a choice, arbitrary
Nielsen operations cannot supply a primitive coordinate. Arbitrary
later interspersed conjugations and Nielsen operations remain outside
the assertion. This is not an AC invariant.

The earlier frozen-coordinate exclusions transfer to this new tuple:
modulo u1, the new u2 is conjugate to r; modulo u2, the identity implies
`r=u1^-1`. Thus the respective existing one-relator primitive-conjugacy
exclusions apply here too. These observations and the subgroup theorem
rule out particular shortcuts; they do not decide the tuple's full AC
orbit. N has independently taken up further actual free-group searches
from this new pair.

## Artifacts and replay

- [Preferred full strict ledger](../certificates/length14_low_peak.json).
- [First full strict ledger](../certificates/p_length14_waypoint.json).
- [Compiler](../experiments/p_short_waypoint.py).
- [Exact replay and arbitrary-tail counts](../results/p_length14_results.json).

The compiler uses only Python's standard library and the published
`arbitrary_tail_catalogue.py` and `elementary_verify.py`:

```sh
python3 experiments/p_short_waypoint.py \
  --u1-certificate certificates/hump_low_peak_u1.json \
  --u2-certificate certificates/hump_low_peak_u2.json \
  --certificate /tmp/p_length14_waypoint.json \
  --low-peak-certificate /tmp/length14_low_peak.json \
  --result /tmp/p_length14_results.json
python3 experiments/elementary_verify.py \
  /tmp/p_length14_waypoint.json /tmp/length14_low_peak.json
```

The strict verifier evaluates every free word and checks the literal
endpoint. The certificate consists solely of inversions, positive right
relator products, and conjugations by a single signed original generator.
It contains no stabilization, ambient generator change, or quotient step.
