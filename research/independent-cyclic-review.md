# Independent closed-set audit of the cyclic cap-20 component

Coordinating-agent review, 2026-11-02. This audit supports N's ordinary
cyclic-length exclusion; it is not a global AC invariant or a solution.

The independent Python program `audit_cyclic_component.py` imports no
search routines from N. It uses literal free strings, its own stack
reduction, explicit cyclic rotations/inverses, and unordered pair keys.
It audits N's stored set rather than trusting a successful search flag.

The cap-20 certificate passes:

- 39,840 distinct valid canonical states, containing the AK(3) start;
- 25,895,168 signed, independently rotated product candidates;
- every one of 1,394,672 admitted directed candidate edges stays inside
  the set;
- all stored states are connected to the start by those edges;
- minimum total cyclic length 13 and minimum coordinate cyclic length 5;
- exact minimum over the set of `sum(lengths)+min(lengths)+2` equal to 21.

The same program independently checks the cap-18 set: 2,128 states,
1,194,704 candidate products, and 69,240 admitted directed candidates.
Its minimum sum is 13, minimum coordinate length 6, and minimum possible
disjoint-axis neighbor energy is again 21.

## Why arbitrary conjugating tails are accounted for at these caps

For two nontrivial free-group elements, use their axes in the Cayley
tree. If the axes intersect, choose an intersection vertex as basepoint.
Both elements are then cyclically reduced and are cyclic rotations of
their respective fixed conjugacy representatives. Their product's cyclic
class is therefore one of the signed rotation products actually tested.

If the axes are disjoint, let d>=1 be the length of their shortest bridge.
Conjugate its first endpoint to the identity. The product has the reduced
and cyclically reduced form `u' q v' q^-1`: the bridge is off each axis
at its endpoint, so no attachment cancels. Its length is |u|+|v|+2d.
Retaining the donor gives total energy

    |u|+2|v|+2d = sum(lengths)+donor_length+2d.

The audited per-state minimum 21 therefore excludes every omitted
disjoint-axis neighbor at cap 20 (and at cap 18). Individual relator
conjugations do not change cyclic classes; inversions and coordinate
permutations are already included in the state key. Hence the audited
closed set accounts for all ordinary AC moves at the stated cyclic cap,
not merely literal products of chosen representatives.

Since its minimum sum is 13, no path from AK(3) to a free basis can stay
at total cyclic length at most 20. This independently verifies a cyclic
peak lower bound of 21. N's subsequent cap-21 set requires explicit
nonempty-bridge enumeration, and is covered by P's separate full-menu
audit; this particular checker deliberately rejects a set when its
minimum omitted-bridge energy is within the requested cap.

## Reproduce

    python3 experiments/audit_cyclic_component.py certificates/cyclic20_component.json.gz.b64 --cap 20 --output /tmp/cyclic20-review.json

The compressed certificate is standard base64-encoded gzip JSON. Runtime
can be longer than N's C++ enumeration because this check independently
uses Python strings. The saved exact output is
`results/cyclic20_independent_review.json`.

The resulting exclusion is finite in energy, with an unbounded-tail
completeness proof. It gives no obstruction to paths above that cap and
does not settle any of the user's four full objectives.
