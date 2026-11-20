# Round 14 · Sheared archive and exact final receiving blocks

2026-11-19. The one-shear enlargement of the reverse archive contributes **1,012,360** new ordered marked pairs through cyclic energy 56. Exact first-block tests at the two energy-20 waypoints give 43 reciprocal contacts. All 43 fail the second block at arbitrary length. In a genuine three-block calculation, 91 first choices and their completed middle charts give 471 last-block contacts. Each of those also fails at arbitrary last-block length. The three-block result retains its first-choice and middle-chart bounds. [Energy-20 paths](round-13-ak3.md), [reciprocal receipt](../results/round14_ak3_sheared_reciprocal.json), [three-block receipt](../results/round14_ak3_sheared_three_blocks.json).

## A larger ordinary-trivial target family

For each of the 23,902 verified archive pairs, apply one of $x\mapsto xy^{\pm1}$ or $y\mapsto yx^{\pm1}$, and then any signed ambient permutation. Retain the images whose cyclic length sum is at most 56 and remove ordered marked pairs already present in the original archive. The four shears give 74,111 retained source-and-shear entries before signed expansion and deduplication. In the final index, 421,750 distinct frozen words have at least one new partner.

A transported suffix substitutes into every relator, and expands each conjugation by the corresponding basis image into elementary conjugations. After reaching the image of the basis, the inverse shear is one signed Nielsen product. The signed permutation is then removed by the strict basis normalization. A positive three-block control starts with five distinct relator classes, uses all three receiving blocks, and uses a transported archive suffix. It replays to `(x,y)` in **5,234** elementary instructions with cyclic peak 358. [Atlas and suffix compiler](../experiments/round14_ak3_sheared_archive.py), [control and search driver](../experiments/round14_ak3_sheared_three.py).

## Exact two-block tests

At the first energy-20 pair freeze `xxxxxyXXy`, and at the second freeze `xxxxyXXYY`. The torus normal form and the amalgam normal form give complete first-block tests in those orientations. The first produces 21 sheared donor words with 41 partner contacts. The second produces one donor with two contacts. The forward finite charts verify all 22 exact first contacts by stage four. The reverse charts find none of the required words in the stages completed with allocation cap 500,000. [Torus and amalgam first-block tests](round-12-ak3.md), [amalgam details](round-12-ac-proof.md).

If the unchanged forward donor is $d$ and the proposed archive pair is $(s,e)$, the second block requires the images of $d$ and $s$ to be conjugate up to inversion in $F(x,y)/N_e$. The permutation scanner looks for markings that kill $e$ and give distinct cycle types to $d,s$. Independent Python replay verifies all 40 resulting separators in symmetric groups of degree at most ten. Inversion preserves cycle type. [Native search](../experiments/round14_ak3_permutation_contacts.cpp), [independent permutation replayer](../experiments/round14_ak3_sheared_separators.py), [permutation witnesses](../results/round14_ak3_sheared_reciprocal_permutations.json).

The three remaining contacts involve two frozen donors. The first has Schreier indices from $-8$ to $2$ after applying $y\mapsto yx^{-2}$, and the second from $-5$ to $1$ after applying $y\mapsto yx^{-1}$. Both extreme indexed letters occur once. Eliminating the upper extreme gives free-by-cyclic kernels of ranks ten and six. On their respective free bases the monodromy shifts each basis letter up one, with last images `hffA` and `eecA`. The replayer checks the Schreier relation and both inverse substitution identities. [Fox receipts](../results/round14_ak3_sheared_reciprocal_fox.json).

Orient the compared words to height one and write them as $ut,vt$. A conjugator can be taken to have height zero by multiplying by a power of $vt$. In the free kernel it must satisfy $gv=u\phi(g)$. The abelianization equation determines $[g]$. At a sign character $\chi$, Fox derivatives then satisfy

$$
D_\chi(g)=D_\chi(u)-\chi(g)D_\chi(v)+\chi(u)J_\chi D_{\chi\circ\phi}(g),
$$

where $J_\chi$ is the character-evaluated Fox matrix of the monodromy. Composing over one character orbit gives a linear system over $\mathbf F_3$. The rank-ten witness uses an orbit of length 1,023 and the rank-six witness uses one of length 14. In every contact, the stored dual combination of augmented rows gives $0=1$. The replayer also tests a known twisted conjugate in each kernel. This completes the exclusion of the 43 exact contacts. [Fox recurrence and replayer](../experiments/round14_ak3_sheared_fox.py), [previous sign-cover construction](round-13-integral-cover.md).

## Three changing rows in the enlarged archive

The search uses the sequence $(r,d)\to(h,d)\to(h,e)\to(s,e)$ with $h\ne r$, $e\ne d$, and $s\ne h$ as cyclic classes. It combines the 71 short first choices of Round 13 with 20 additional choices from the exact sheared tests. From these 91 first choices, completed middle charts give 28 word hits among **5,956,464** exact membership queries. Four charts complete through stage one, 86 through stage two, and one through stage three. The resulting 471 required third memberships fail in the completed stages of 245 reverse charts. [Three-block profile and full final queries](../results/round14_ak3_sheared_three_blocks.json).

For the exact last block, 470 contacts admit independent permutation witnesses killing $e$ and separating $h$ from $s$. The remaining triple has `h = XXYYxxYYXXyxyXy`, `e = XXXXXyxxYxYXYxxy`, and `s = XXXYxxy`. The rank-six quotient above and its 14-character orbit give another mod-3 contradiction. Thus all 471 last-block contacts from the stated finite middle charts are excluded at arbitrary last-block length. [470 permutation witnesses](../results/round14_ak3_sheared_third_permutations.json), [last Fox witness](../results/round14_ak3_sheared_third_fox.json).

## Reproduction

Use the verified reverse TSV with its adjacent `.sources.json`, and the original archive directory. [Archive and provenance](round-04-ak3.md#reproduction).

~~~sh
mkdir -p "$work"
c++ -std=c++17 -O3 experiments/round11_ak3_targeted_acm.cpp -o "$work/targeted"
c++ -std=c++17 -O3 experiments/round12_ak3_chart_index.cpp -o "$work/index"
c++ -std=c++17 -O3 experiments/round14_ak3_permutation_contacts.cpp -o "$work/permutations"
python3 -B experiments/round14_ak3_sheared_archive.py "$work/targeted" "$reverse" "$archives" \
  --energy 56 > "$work/reciprocal.json"
python3 -B experiments/round14_ak3_sheared_separators.py "$work/permutations" "$work/reciprocal.json" \
  --degree 10 > "$work/reciprocal-permutations.json"
python3 -B experiments/round14_ak3_sheared_fox.py "$work/reciprocal-permutations.json"
python3 -B experiments/round14_ak3_sheared_three.py "$work/targeted" "$work/index" "$reverse" "$archives" \
  results/round13_ak3_three_blocks_short.json "$work/reciprocal.json" > "$work/three-blocks.json"
python3 -B experiments/round14_ak3_sheared_separators.py "$work/permutations" "$work/three-blocks.json" \
  --degree 10 > "$work/third-permutations.json"
python3 -B experiments/round14_ak3_sheared_fox.py "$work/third-permutations.json"
~~~
