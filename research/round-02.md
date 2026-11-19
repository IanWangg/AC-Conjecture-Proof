# Research round 02

2026-11-19. Five agents continued the five targets, in overlapping waves. The previous round's archive entries, pivot arguments and peak-rank formula served as inputs. No target conjecture or free-group AK(3) trivialization was settled.

## Track reports

| Target | Result |
| --- | --- |
| [Ordinary AK(3) trivialization](round-02-ak3.md) | A Stallings fiber-product test allows arbitrary Nielsen basis changes before matching the separate relator conjugacy classes. No join occurred for four fixed AK(3) source cores against 16,943 known-trivial archive targets, or for all 42 initial rotation pairs against 9,257 targets. The target side includes arbitrary independent conjugating tails. A strict 22-move positive control succeeds outside the previous join test. |
| [Proof of Stable AC](round-02-stable-proof.md) | A geometric subtuple with a free quotient of the expected rank can be normalized to a partial basis while all other rows stay frozen. A lower-rank trivialization can then be lifted through that block. The rank-three control works even with every displayed row nonprimitive and the full tuple nongeometric. |
| [Proof of ordinary AC](round-02-ac-proof.md) | A padded path descends to the original rank if every vertex admits a triangular system of defining relations for the fixed extra generators. Row choices and order of elimination can change. Exact controls distinguish triangular frames, exchange-disconnected relative bases, and dynamic elimination sensitive to pivot choice. |
| [Disproof of ordinary AC](round-02-ac-disproof.md) | Finite folded joins of two rebased copies of a source core certify a class of exclusions beyond the earlier voltage-kernel test. All 137,760 sources with bridge length at most eight pass, across 24,902,640 joins. A parametric family of arbitrarily long bridges also passes. |
| [Disproof of Stable AC](round-02-stable-disproof.md) | If the least feasible padding rank is positive, each auxiliary cut in a free-group path at that rank requires at least two incoming and two outgoing relator products. The cutoff for length-minimal paths still uses the round-one estimate. Exact degree-six Magnus distances for AK(3) are 12 to the unordered basis and 13 to the ordered basis. |

## Independent extensions

- The [cap-25 cyclic component](round-02-cyclic25.md) contains 5,562,224 states. Closure and connectivity were checked across 5,036,287,488 candidate products, including 4,994,816 nonempty-bridge candidates. A separate Euclidean test excludes primitive coordinates in all 4,542,536 distinct cyclic word classes. The resulting cyclic peak lower bound is 26.
- The [braid-kernel lifting lemma](round-02-relative-quotients.md) turns the existing 533-move relation-module certificate into an ordinary AC path at every lower-central layer of the braid kernel. A separate Schreier expansion verifies the class-two case directly. Each layer is an infinite nonsolvable ambient quotient, and the strict distances still determine free-group distance through their supremum. The proved corrections may grow with the layer.
- A [finite-cover limitation](round-02-barbell-cover.md) shows that a finite family of fixed finitely generated infinite-index subgroups cannot contain all disjoint-axis barbell subgroups with two fixed lobes. An inductive certificate for unbounded phases can instead look for a uniform description that varies with the bridge.

## Interactions

- Both graph tracks use paths in a labeled fiber product. The constructive track compares separate reachable forward and reverse subgroups. The disproof track uses a self-product to control folding when two copies of a source are brought together. Forward subgroups outside the proved primitive-free classes are higher-priority sources for the next search.
- A geometric block at a padded waypoint can be normalized and used for an actual completion, with the other rows frozen. When the whole padded path admits moving triangular frames and reaches the full standard basis, the ordinary proof theorem compiles that complete path into the original rank. This separates the local goal for a stable search from the additional path property that makes the completion ordinary.
- The one-incoming elimination in the ordinary proof track supplies the local mechanism for the stable-disproof cut theorem. The completed block version constrains the least feasible rank, while the finite quotient computation continues to use the rank bound for shortest length.

## Questions for round 03

1. **AK(3) trivialization.** Apply the new fiber-product test to selected later reachable subgroups. Prioritize reachable cores that avoid the source configurations certified primitive-free under further phases. Keep exact ordinary entry ledgers and continue using a known-trivial positive control.
2. **Stable AC proof.** Search for reachable padded tuples with a geometric block whose free quotient has a marked retraction certificate. Test how the lower-rank path depends on the selected block. The rank-three positive control identifies a valid goal even when the full tuple is nongeometric.
3. **Ordinary AC proof.** Use the geometric-block criterion and the triangular-frame proof to investigate exchanges of relative free quotients outside the triangular class. A useful test is whether a common block can still be eliminated when its pivot choices are exchange-disconnected.
4. **Ordinary AC disproof.** Extend the two-copy method to positive bridges with a fixed prefix and suffix, then to bridge families with repeated readings and to longer alternating paths. The finite-cover limitation rules out a fixed finite list of infinite-index overgroups as a universal treatment of disjoint bridges.
5. **Stable AC disproof.** Distinguish minimal padding rank from shortest length. Test whether two incoming and two outgoing uses satisfy a further constraint at the minimum rank. The quotient distances can still be bounded independently at each fixed padding rank, using the sharper reductions only where their length accounting is proved.
