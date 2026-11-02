# Research K short-power filter after the length-eight braid replacement

Date: 2026-11-02. This is a necessary finite-quotient filter for potential new AC edges. **A surviving word is not asserted to be conjugate in the deletion group. No global AC conclusion is claimed.**

Use p=xxxYYYY and r=XXyxYxxY. With r held fixed, K's finite quotient of <x,y|r=1> excludes every primitive replacement at arbitrary length. The coordinating agent next requested a complete filter of all cyclic power replacements of length at most seven, aiming to find useful new candidates rather than only another negative bound.

## Complete finite filter

The independently specified quotient in the core K report has fiber group order 524,288, alpha order 24, and a completed 65,536-element twisted orbit of W=a d^2 a^-1 d a^-1. The program here enumerates every freely and cyclically reduced x,y word of lengths one through seven. The numbers at each length are

    4, 12, 28, 84, 244, 732, 2188,

for 3,292 words in total. It does not discard a noncyclic prefix during generation, which would lose cyclic final words.

Conjugacy to p or p^-1 requires total exponent sum ±1. This leaves 928 candidates: 4 at length one, 12 at length three, 100 at length five, and 812 at length seven. Each is inverted if necessary to make its exponent sum one. Its exact original-generator image in the finite semidirect group is then compared with W's full twisted orbit.

Exactly **84 words survive**, all of length seven. They form six cyclic/inverse orbits, each of size fourteen. Thus **no cyclic word of length at most six can be conjugate to p or p^-1 in <x,y|r=1>**. This is a genuine no-shortening result for the power coordinate while r stays fixed, despite allowing unbounded conjugators.

The six orbit representatives and exact normalized fiber coefficients are:

| Cyclic/inverse representative | Normalized to chi=1 | Fiber coefficient before t |
|---|---|---|
| XXXyyxy | XXXyyxy | d a^3 d^-1 |
| XXXyyyy | XXXyyyy | d a^2 d a d^-1 |
| XXYxyxY | yXYXyxx | a d^-2 a |
| XYYYxyy | YYXyyyx | d^-1 a^-1 d a^2 d |
| XYYxyXy | YxYXyyx | d^-2 a d |
| XYxYYxy | YXyyXyx | d^-1 a d^2 |

The second row is the original power orbit. The other five are candidates for an **actual twisted-conjugator search**. Their passage through the finite quotient gives no AC edge by itself. In the code and JSON, the fiber generator d is called `b`, so the coefficients are `baaaB`, `baabaB`, `aBBa`, `BAbaab`, `BBab`, and `Babb`.

## Checks and reproduction

The script recomputes alpha's order on the finite fiber generators, reconstructs the complete twisted orbit, evaluates words using x=t and y=(a d^-1)t, and checks the exact free-by-cyclic coefficients against their finite images. It also verifies that every cyclic/inverse rotation of every admitted word is admitted.

Place `short_power_filter.py` and the earlier `twisted_magnus.py` together under `experiments/`, then run:

```sh
python3 experiments/short_power_filter.py \
  --output results/k-short-power-filter.json
```

The output includes every surviving word, all six representatives, and their normalized exact fiber coefficients. The program uses only the Python standard library. The result narrows a positive search to five new potential length-seven classes; it does not prove those classes are reachable or rule out later moves changing both coordinates.
