# Exact degree-eight distances and a longer free-word exclusion

2026-11-19. The degree-eight characteristic-two Magnus quotient has ordinary and stable instruction distances **16** for AK(3), for both target orders. In degree nine both distances are **17**, also for either target order. The free ordinary instruction distance is at least **19**.

## Degree eight

The prior successive corridor checks exclude length at most 15 unpadded, and exclude all positive-padding solutions at length at most 16. The new native search meets at total radius 16 in the exact degree-eight rank-two graph for both the ordered and unordered bases. In the ordered run, the two partial balls contain 84,969,969 and 25,769,703 tuples when they meet. A separate bidirectional search reconstructs the two radius-eight halves from the recorded midpoint polynomials. The 16-instruction ordered path replays in an independent implementation representing polynomials as sets of monomials. These moves supply the stable upper bound without increasing rank. [Round-six exclusions](round-06-stable-disproof.md), [ordered native receipt](../results/round07_magnus_d8_ordered.json), [unordered native receipt](../results/round07_magnus_d8_unordered.json), [explicit ordered path](../results/round07_magnus_d8_witness.json).

The native code stores each unit as an exact packed coefficient vector. Monomials are ordered by degree and then by lexicographic index within a degree. For a nonzero degree-$i$ coefficient of index $k$, concatenation with the degree-$j$ block shifts that block to index $2^j k$ within degree $i+j$. Truncated multiplication inserts those blocks with XOR. Unit inversion uses the exponent bound from $(1+u)^{2^m}=1+u^{2^m}$ when $2^m$ exceeds the truncation degree. Exact vectors are interned, and the tuple BFS uses their integer IDs.

~~~sh
mkdir -p /tmp/ac-r07-magnus
c++ -std=c++17 -O3 experiments/round07_magnus_native.cpp -o /tmp/ac-r07-magnus/native
/tmp/ac-r07-magnus/native 8 0 16 --ordered > /tmp/ac-r07-magnus/ordered.json
/tmp/ac-r07-magnus/native 8 0 16 > /tmp/ac-r07-magnus/unordered.json
python3 -B experiments/round07_magnus_witness.py /tmp/ac-r07-magnus/ordered.json \
  | diff - results/round07_magnus_d8_witness.json
~~~

## Degree nine

The two complete degree-nine rank-two balls of radius eight contain 93,137,211 and 21,941,224 tuples and are disjoint. All positive-padding cases for a stable path of length at most 16 already fail at degree eight. Truncation carries any higher-degree path to that same test. Separate 17-instruction paths reach $(y,x)$ and $(x,y)$ in degree nine, with independent monomial-set replay in both cases. This proves both ordinary and stable distances are exactly 17. [Complete exclusion](../results/round07_magnus_d9_L16.json), [unordered path](../results/round07_magnus_d9_witness.json), [ordered path](../results/round07_magnus_d9_ordered_witness.json).

An independent arithmetic audit compares native counts to Python searches on smaller complete balls. These include degrees eight and nine with both variables and positive-padding controls in degrees four through six. [Audit results](../results/round07_magnus_native_audit.json).

~~~sh
/tmp/ac-r07-magnus/native 9 0 16
/tmp/ac-r07-magnus/native 9 0 17 > /tmp/ac-r07-magnus/degree9.json
python3 -B experiments/round07_magnus_witness.py /tmp/ac-r07-magnus/degree9.json \
  | diff - results/round07_magnus_d9_witness.json
/tmp/ac-r07-magnus/native 9 0 17 --ordered > /tmp/ac-r07-magnus/degree9-ordered.json
python3 -B experiments/round07_magnus_witness.py /tmp/ac-r07-magnus/degree9-ordered.json \
  | diff - results/round07_magnus_d9_ordered_witness.json
python3 -B experiments/round07_magnus_native_audit.py /tmp/ac-r07-magnus/native \
  | diff - results/round07_magnus_native_audit.json
~~~

## Free words

The uncapped free-word search now exhausts two radius-nine balls. The one from AK(3) contains 838,216,495 tuples and the one from the unordered basis contains 191,373,223. They are disjoint. All transitions are exact freely reduced words, so this bound excludes every ordinary path of length at most 18 in the instruction metric, regardless of its cyclic or raw peak. This run used substantially more memory than the [round-six length-17 exclusion](round-06-free-distance.md). [Free search receipt](../results/round07_free_ordinary_L18.json).

At stable budget 18 the improved padding cutoff leaves at most three extra pairs. Retractions with two and three extra rows fail at ordinary budgets 14 and 12, respectively. The final expansion tests each transition against the entire opposite ball without storing the newly expanded layer. The two boundary tests check 505,191,962 and 35,037,249 transitions. The one-padding length-16 test is still running, so the free stable lower bound remains 18 in this round. [Padding cutoff](round-07-stable-disproof.md), [retracted boundary checks](../results/round07_free_padded_L18.json).

~~~sh
c++ -std=c++17 -O3 experiments/round06_free_instruction_distance.cpp -o /tmp/ac-r07-magnus/free
/tmp/ac-r07-magnus/free 0 18
/tmp/ac-r07-magnus/free 2 14 --boundary-only
/tmp/ac-r07-magnus/free 3 12 --boundary-only
~~~
