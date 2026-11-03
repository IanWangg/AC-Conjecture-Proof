# V: complete initial-subgroup basis scan through cyclic energy 250

Date: 2026-11-02. **AK(3) and the ordinary, unstabilized AC conjecture remain unsolved here.** No novelty or priority claim is made.

## Reading and independent choice

Before choosing a direction, I fetched the private repository README and read [the basis-sublevel proof](nielsen-cyclic-sublevels.md), [Q's arbitrary-tail reduction](research-q.md), [R's exact primitive detector](research-r.md), and [R's reverse-search follow-up](research-r-reverse.md). The complete cap-22 component and its all-tail primitive-free subgroup theorem were already established. Repeating frozen-coordinate checks would not address the remaining freedom.

I independently chose to enumerate **all initial-subgroup Nielsen basis classes through a much higher final cyclic energy**, then allow arbitrary independent conjugations and an unbounded Nielsen suffix. T and U independently chose overlapping directions before communication. We coordinated explicitly: V built the complete Farey-source/rotation scanner; T independently enumerated source classes by integer matrices, audited every actual source program, and compiled a positive control; U independently implemented an exact integer-map primitive detector and checked controls. The theta length calculation was independently shared by T/U. The folding, exact graph keys, and sufficient primitive-absence filter below extend Q's existing implementation; they are not claimed to be independently rewritten algorithms.

## Result and exact scope

Put

    p = xxxYYYY,  b = xyxYXY,  H0 = <p,b> <= F(x,y).

Let `(u,v)` be any free basis of H0 obtained by arbitrary coordinate Nielsen moves from `(p,b)`. Write `E(u,v)` for the sum of the lengths of their cyclic reductions. The checked result is:

> If E(u,v) <= 250, then for every a,c in F(x,y), the subgroup `<a u a^-1, c v c^-1>` contains no primitive element of the ambient free group, at any word length.

The Nielsen prelude need not have a prescribed number of steps or an intermediate energy bound: its final basis classes are what the source enumeration covers. Consequently, no path consisting of such a prelude, one simultaneous phase of arbitrary independent conjugations, and an arbitrary Nielsen-only suffix can expose a primitive coordinate or reach a free basis. Any actual general AC path may use further interspersed subgroup-changing conjugations; those are outside this result. The result does not increase the established global cyclic-peak lower bound of 23.

| Final source energy cap | Source families | Rotation pairs | Distinct unbased labelled cores | Primitive-filter exceptions |
|---:|---:|---:|---:|---:|
| 40 | 26 | 4,436 | 2,175 | 0 |
| 120 | 253 | 315,206 | 156,039 | 0 |
| 200 | 706 | 2,399,748 | 1,188,989 | 0 |
| 250 | 1,111 | 5,862,545 | 2,905,457 | 0 |

The cap-250 result is `COMPLETE`, with 2,224 retained signed Farey nodes, maximum core size 249 vertices, and maximum freely reduced raw source sum 254. Every one of the 2,905,457 graph keys passes the sufficient absence criterion. There are no unresolved graphs requiring the exact detector. Saved results are [v_cap250_results.json](../results/v_cap250_results.json); the smaller scans are corroborating runs rather than additional unbounded claims.

## Complete source enumeration

More generally, let `p_n=x^n Y^(n+1)` and `H_n=<p_n,b>`, n>=2. Its marked folded theta core has path lengths `(2,2n-1,4)`. For a primitive abstract H-coordinate with exponent vector `(a,b)`, its ambient cyclic length is

    F_n(a,b) = 2|a+b| + (2n-1)|a| + 4|b|.

This is the theta primitive-length formula in the basis-sublevel proof, with the indicated marking. Equivalently, the three oriented chain coefficients are `a+b,a,b`; an efficient primitive representative runs each theta path in only its indicated direction. Primitive conjugacy uniqueness then gives the length for every representative of that abstract primitive conjugacy class. The external rank-two fact used here is [Clay--Conant--Ramasubramanian, Corollaries 4.4 and 4.5](https://msp.org/involve/2014/7-4/involve-v7-n4-p01-p.pdf). The geometric formula and its application to this marking are deductions here and in T's independent audit, rather than claims taken verbatim from that paper.

Start with four signed actual bases `(p_n^s,b^t)`, s,t in {+1,-1}, and apply positive Farey updates

    L: (U,V) -> (U,U V),       R: (U,V) -> (U V,V).

Both use actual freely reduced words, and both retain the marked signed exponent columns. In particular, **no individual cyclic reduction, rotation, or conjugation is applied before the next update**. Doing that would generally change H_n and invalidate the prelude. Final cyclic classes are deduplicated only after children have been generated. Every retained record contains signs, the literal L/R program, signed matrix columns, actual raw basis words, final cyclic words, and final cyclic energy.

For completeness, up to inverting and interchanging its columns, every unimodular 2-by-2 integer matrix has both columns in one signed coordinate orthant. After choosing column signs so that first entries are nonnegative, opposite nonzero signs of the second entries would make the absolute determinant a sum of two positive integer products, at least two. Zero-entry boundary cases give the coordinate rays and obey the same conclusion. A nonnegative unimodular matrix is generated from the coordinate rays by the two column additions above: except for the initial rays, the columns are coordinatewise comparable, and subtracting the smaller from the larger decreases their positive sum and preserves determinant. This gives the terminating Euclidean inverse algorithm. Primitive conjugacy uniqueness in the abstract rank-two H_n shows that this matrix coverage covers the two cyclic coordinate classes of every actual basis. Independent column inversion/order does not change the all-conjugates subgroup question.

Energy pruning is safe on every signed orthant. With unsigned a,b>=0, same signs give `(2n+1)a+6b`; opposite signs give `(2n+1)a+2b` when a>=b and `(2n-3)a+6b` when a<=b. All coordinate slopes are positive for n>=2. Every Farey child strictly increases the total source energy, so a source over cap cannot have an admissible descendant.

[T's independent source audit](research-t.md) enumerates primitive integer columns and determinant-one pairs without using V's Farey traversal. At cap 250, it finds 1,059 projective primitive vectors and exactly the same 1,111 cyclic basis families. It separately replays all 1,111 retained raw programs as **33,238 strict ordinary Nielsen instructions**, with maximum raw peak 254 and cyclic peak 250. In particular, the raw source provenance is checked in addition to equality of the final cyclic class set. Source JSONL SHA-256 is

    4de92fdc35db0dd2011580bf3994407a59c348bc06806c0a98ca36b2ed6395db

## Arbitrary tails and primitive absence

For each final source family, V tests every independent cyclic rotation. The [Q/R axes theorem](research-q.md) proves that arbitrary independent conjugating tails contain an ambient primitive if and only if some such rotation subgroup does. Intersecting axes give a rotation pair after common conjugation; disjoint axes give a folded barbell in which a cyclic primitive cannot traverse the bridge in both directions. Inverting a source generator does not change its generated subgroup, so inverse rotations need not be scanned separately.

The scanner folds actual word loops and checks inverse arcs, core degree, and rank two. It keeps the full exact adjacency string for each unbased labelled graph, using Q's branch-based canonical encoding. Keys are not just numeric hashes. The byte encoding is injective on the permitted sizes; the program rejects source caps above 250 rather than silently exceeding its representation. For cap 250, even the unfolded pair has at most 249 vertices. The implementation extends Q's folding guard from 120 to 255 vertices while retaining the same fold algorithm.

For each signed ambient alphabet and each choice of a forbidden double letter, Q's existing edge-state cycle check tests acyclicity. A cyclic primitive has a signed-positive representative with at least one isolated generator, so it avoids at least one of the two doubles. If all these directed graphs are acyclic, no primitive cyclic loop exists. This excludes primitives of unbounded length, not just words up to a search cutoff. The full finite graph enumeration supplies the computation, while the axes theorem supplies the arbitrary-tail reduction.

As a separate implementation check, V selected three deterministic rotations from each of all 1,111 cap-250 sources (seed 2718281828). R's independently written batch-identification fold agrees exactly, including the distinguished base, on all **3,333** resulting graphs, including sizes through 249 vertices. U independently refolds the same pairs and runs its complete integer-map detector: all 3,333 are `ABSENT`, with zero incomplete decisions and **277,164** closed map-pair states independently checked. These are sample checks, not second full enumerations. See [V's fold result](../results/v_fold_sample_review.json) and [U's exact sample review](../certificates/u_v_sample_review.json).

## Positive AK(2) control

Running the identical scanner with n=2 and cap 12 finds two source families, 65 rotation pairs, 31 distinct graphs, and one exception. Its signed source program is `(-,+), L`; its actual raw basis is

    (yyyXX, yyyXyxYXY),

and the exceptional rotation pair is

    (XXyyy, YXyyXyx).

U's independent integer-map detector refolds it and finds the based primitive `XYxYYxYYxx`, whose cyclic reduction is `xYxYYxYY`, with signed alphabet `xY` and positive-basis program `RLRL`. In the displayed actual pair `(A,B)`, the based primitive is `B^-1 A^-1` after free reduction. T compiles the actual signed source program and rotations, exposes this hidden primitive, and completes to the exact free basis. V independently replays the [complete certificate](../certificates/t_v_ak2_hidden_full.json): **232 strict ordinary moves, raw peak 33, exact endpoint `(x,y)`**, starting from literal `(xxYYY,xyxYXY)`.

This calibrates source programs, rotations, hidden-primitive detection, and an actual strict completion pipeline. It is AK(2), not AK(3). The positive control also shows why graph-filter exceptions must not be discarded or called negative.

## Matching known-trivial reverse corpora

The cap-250 scanner also compares every forward core key to R's two independently replayed known-trivial reverse corpora: 20,985 rows from the AK(2) anchor and 35,814 from the `(p_3,xY)` anchor. Their combined **56,799 keys are distinct**, and no key matches. The TSV SHA-256 values are respectively

    c0d198a18924290743a35189f95fccd28c83b130be9457bae3488199bb637945
    721c34938f5fc61d6c21960ddccaca7747c8c064acaaa14477cd94f5a0886346

Unlike primitive existence, arbitrary-tail subgroup equality does not generally reduce to rotation keys: the disjoint-axis case can have an arbitrarily long bridge. V separately closes that gap **for the saved reverse targets**, rather than silently treating the rotation scan as all-tail matching.

For a reverse core that is a barbell, choose a branch vertex A as base. Reading the two cycles and the connecting bridge gives a geometric basis `(u,q v q^-1)`. Its actual reverse tuple is a basis of that rank-two graph after rebasing, so an ordinary Nielsen change and a common conjugation reach this geometric basis; conjugating its second coordinate by q^-1 reaches `(u,v)`. Thus the two cycle conjugacy classes are a short known-trivial anchor. A disjoint-axis source can match that reverse core only if its two source cyclic coordinate classes equal these two cycle classes, up to order and inversion.

V explicitly extracts all such anchors. Exactly **549** reverse rows have barbell cores, giving **338** distinct collapsed cycle families; the largest sum of the two cycle lengths is **21**. None matches the 26 source families through cap 40, which cover every possible initial-H0 source of that energy. T independently reclassifies every reverse graph by deleting undirected edges and testing connectivity, rather than using V's branch tracing, and obtains the exact same 549 rows and 338 family keys. This has the following restricted unbounded consequence:

> No Nielsen basis of H0, even at arbitrarily high source energy, followed by independent conjugations with disjoint axes, can generate a subgroup conjugate to any of these 56,799 saved reverse subgroups.

A matching disjoint-axis basis would necessarily have cyclic energy at most 21, so the finite comparison is complete for this case. T reviewed the geometric argument and recognition conditions. The separately saved anchor records permit inspection and reproduction; this does not exclude other reverse targets, intersecting-axis matches above energy 250, or paths with further interspersed conjugations. See [the barbell result](../results/v_barbell_anchor_results.json.gz.b64).

## Reproduction and artifacts

All Python code uses only the standard library. Compile and repeat the complete final scan from the repository root (C++17; the observed run took about 106 seconds and stored 2.9 million exact graph keys):

```sh
python3 experiments/reverse_journal.py \
  certificates/r_reverse_ak2_journal.json.gz.b64 \
  --tsv-output /tmp/r_ak2.tsv --output /tmp/r_ak2_review.json
python3 experiments/reverse_journal.py \
  certificates/r_reverse_power_journal.json.gz.b64 \
  --tsv-output /tmp/r_power.tsv --output /tmp/r_power_review.json
c++ -std=c++17 -O3 experiments/v_one_phase_bases.cpp -o /tmp/v_one_phase
/tmp/v_one_phase 250 /tmp/v_sources.jsonl /tmp/v_candidates.jsonl /tmp/v_result.json \
  4000000 3 /tmp/r_ak2.tsv /tmp/r_power.tsv
```

The reverse-journal commands independently replay their provenance and reconstruct the exact hashed TSV inputs. Omitting both final TSV arguments repeats the complete primitive-absence scan without the separate known-trivial-key lookup. An explicitly exhausted graph budget gives `INCOMPLETE`, never a proof of absence. A key match gives `MATCH` and a record for subsequent strict bridge compilation, never an automatic AC claim.

The archived raw source corpus is [v_cap250_sources.jsonl.gz.b64](../certificates/v_cap250_sources.jsonl.gz.b64). Decode any `.gz.b64` artifact with standard-library `base64.b64decode` followed by `gzip.decompress`. T's source audit accepts this transport directly; its exact reproduction command is in T's report.

```sh
/tmp/v_one_phase 12 /tmp/v_ak2_sources.jsonl /tmp/v_ak2_candidates.jsonl \
  /tmp/v_ak2_result.json 4000000 2
python3 experiments/elementary_verify.py certificates/t_v_ak2_hidden_full.json
python3 experiments/v_barbell_anchors.py certificates/v_cap40_sources.jsonl \
  /tmp/r_ak2.tsv /tmp/r_power.tsv \
  --output /tmp/v_barbell_result.json
```

The barbell comparison can also use the full cap-250 source corpus; its reported source-family count then changes, while the negative matching conclusion and 549/338 reverse counts do not. The saved run used the smaller cap-40 corpus as above. Source, results, positive-control records, deterministic fold-audit code, and byte/hash manifest are published alongside this report. No inference from these finite failures is promoted to a global AC obstruction. A complete free-basis path or an invariant under every ordinary move at unbounded length is still missing.
