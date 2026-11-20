# An affine quotient target at the cap-33 first exit

2026-11-19. The whole compacted energy-33 first-exit boundary contains no row in the automorphism orbit of the relator `xxyXY`. This is a potential constructive target because every normally generating pair with a row in that orbit has an ordinary AC trivialization. [Scan and strict control](../results/round14_ak3_bs_atlas.json).

## Completion in the Baumslag–Solitar quotient

The relation is equivalent to $yxy^{-1}=x^2$. In its quotient, every element has a normal form $y^{-k}x^m y^l$ with $k,l\ge0$, by moving positive $y$ letters to the right and negative $y$ letters to the left. It acts as the pair $(m/2^k,l-k)$ in the affine group $\mathbb Z[1/2]\rtimes\mathbb Z$, where $y$ multiplies translations by 2. The action is faithful since the only normal form acting trivially has $m=0$ and $l=k$.

A second row of a normally generating pair has signed $y$ exponent one after choosing its orientation. Its affine image is $(b,1)$. Conjugating by $(b,0)$ sends it to $(0,1)$, the image of $y$. The fixed-donor criterion then replaces that row by $y$ through ordinary AC operations. Multiplying the other row by suitable conjugates of $y$ clears its $y$ letters and leaves $x$. An ambient automorphism of the starting relator carries this construction back to the original marking. The resulting basis can be taken to $(x,y)$ by Nielsen operations. [Fixed-donor criterion](round-10-ac-proof.md#exact-block-criteria).

For the nonprimitive control `(xxyXY, yyxYX)`, a finite quotient-conjugacy completion gives the replacement by $y$ in 18 strict instructions. The verified full path to $(x,y)$ takes **26** instructions at raw peak **12**. [Strict ordinary certificate](../certificates/round14_ak3_bs_control.json).

## Complete bounded automorphism orbit

Whitehead peak reduction connects equivalent cyclic words of length at most a fixed cap through cyclic words within that cap. In rank two, a nontrivial type-II move on a single cyclic word is a left or right shear of one generator by the other, up to signed markings and inner conjugation. The single-word search therefore uses the eight signed left and right shears, then cyclically reduces and takes the signed cyclic class. It visits **116** classes through length 31, which give **920** marked cyclic keys in the native index. All rows stored in the compacted energy-33 boundary have length at most 31. The native lookup checks both rows in all **1,258,633,777** distinct seeds and finds zero hits. [Whitehead, On Equivalent Sets of Elements in a Free Group](https://www.sciencedirect.com/science/article/abs/pii/B9780080098708500178), [atlas generator](../experiments/round14_ak3_bs_atlas.py), [native lookup](../experiments/round14_ak3_bs_scan.cpp), [seed provenance](round-14-independent-cyclic32.md#exact-first-exit-deduplication-at-cap-33).

~~~sh
python3 -B experiments/round14_ak3_bs_atlas.py "$work/bs31.tsv" \
  --control "$work/bs-control.json" "$work/bs-control.bin"
c++ -std=c++17 -O3 -pthread experiments/round14_ak3_bs_scan.cpp -o "$work/bs-scan"
"$work/bs-scan" "$work/bs31.tsv" "$work/bs-control.bin"
"$work/bs-scan" "$work/bs31.tsv" "$work"/boundary33/unique.*.bin
~~~
