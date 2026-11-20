# Four alternating ordinary receiving blocks through a larger middle menu

2026-11-19. From the two energy-20 AK(3) waypoints, enlarging the second-product menu from cyclic energy 34 to **36** gives **73,141** fourth-block contacts. All fail at arbitrary final-block length. This adds 45,264 contacts to the Round 15 exclusion. The bounded four-block search yields no strict path to the archive. [Compact receipt](../results/round16_ak3_four_blocks36.json), [Round 15 method](round-15-ak3.md).

The four receiving blocks have the form

~~~text
(r,d) → (h,d) → (h,f) → (s,f) → (s,e).
~~~

The first block uses the same 91 verified choices. The second block uses one cyclic product across arbitrary shortest bridges at the new endpoint energy bound. An independent string menu agrees with the native menu on **531** distinct ordered midpoints, after 48,892 string rotation and bridge checks. Each third chart tests the compatible donor keys of the energy-56 one-shear archive, excluding the unchanged receiver. The third charts have 680 word hits over **32,763,878** checks. Four charts finish stage three and 527 finish stage two before reaching the next allocation cutoff. The archived partners other than the unchanged row give the 73,141 last-block contacts across 363 reverse charts. Every Round 15 contact is present in this larger collection. [Strictly reached waypoints](round-13-ak3.md), [one-shear atlas](round-14-ak3.md).

## Last-block coverage

| Quotient separator | All contacts closed | Added contacts closed |
| --- | ---: | ---: |
| Symmetric images of degree at most ten | 73,131 | 45,260 |
| Mod-3 Fox systems over free-by-cyclic groups of ranks six and ten | 9 | 4 |
| Affine quotient of a root-adjoined Baumslag–Solitar amalgam | 1 | 0 |
| Total | 73,141 | 45,264 |

The 28 marked symmetric homomorphisms from Round 15 suffice for the new test. The checker retests that each chosen homomorphism kills the frozen donor and that the two receiver cycle types differ. It independently reconstructs all nine Fox systems and checks their mod-3 dual certificates, four in rank ten and five in rank six. The original affine amalgam witness also replays. All tests exclude conjugacy up to inversion in a quotient that kills the frozen donor, which excludes the desired final block with no bound on its number of moves. The previous three block menus retain their stated bounds. [Exact quotient arguments](round-15-ak3.md#exact-fourth-block-exclusions), [checker](../experiments/round15_ak3_four_audit.py).

## Reproduction

Use the witnessed reverse archive with its adjacent source index and the native tools listed in Round 15. The comparison script verifies the inclusion of the old contacts and checks that each compact donor row expands to exactly its full list of source-target pairs. [Native tools and archive provenance](round-15-ak3.md#reproduction).

~~~sh
set -o pipefail
python3 -B experiments/round15_ak3_four_blocks.py \
  "$work/targeted" "$work/index" "$work/exact-center" "$reverse" "$archives" \
  results/round13_ak3_three_blocks_short.json results/round14_ak3_sheared_reciprocal.json \
  --middle-energy 36 > "$work/four36.json"
python3 -B experiments/round16_ak3_four_reuse.py "$work/four36.json" \
  results/round15_ak3_four_blocks34.json | diff - results/round16_ak3_four_blocks36.json
python3 -B experiments/round15_ak3_four_audit.py results/round16_ak3_four_blocks36.json
~~~
