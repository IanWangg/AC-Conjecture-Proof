# Root-adjoined Baumslag–Solitar tests at the cap-33 first exit

For $k\ge2$ and $n\ge1$, consider the standard relator $x^k y^n x^{-k} y^{-n-1}$. The full ordinary first-exit scan covers all **1,258,633,777** compacted energy-33 seeds. Across **91** standard types through width 31, the atlas has **4,668** marked keys and finds **1,904,464** donor-coordinate occurrences. None admits a fixed-donor primitive replacement at any length. The largest class, $(k,n)=(2,1)$, accounts for 1,821,106 occurrences. [Receipt](../results/round16_ak3_root_bs_atlas.json), [boundary provenance](round-14-independent-cyclic32.md#exact-first-exit-deduplication-at-cap-33).

## Exact test

Introduce $t=x^k$ and $a=y$. The one-relator quotient is

$$
\langle x\rangle *_{x^k=t} \langle a,t\mid t a^n t^{-1}=a^{n+1}\rangle.
$$

Both edge maps inject since $x$ and $t$ have infinite order in the respective factors. The companion of a normally generating pair has absolute $x$ exponent one. Invert it if necessary. The primitive classes of height one have representatives $xa^j$ for all integers $j$, by the rank-two primitive conjugacy classification. [Primitive enumeration](round-10-ac-proof.md).

For $j=0$, the target is the outer vertex element $x$. For $j\ne0$, $xa^j$ is cyclically reduced of alternating length two in the amalgam. A cyclically reduced receiver of length one can be conjugate to $x$ only when it lies in the outer factor, since all inner heights are multiples of $k$ and $x$ does not lie in the edge subgroup. In that case the height already makes the receiver $x$. A receiver of alternating length greater than two cannot be conjugate to either kind of target.

In the remaining case rotate the receiver to $x^r\beta$ with $\beta$ in the inner factor. If $\beta$ has stable-letter height $h$, then $r+kh=1$, so this is $x\beta'$ with $\beta'=t^{-h}\beta$. By the cyclic conjugacy theorem for amalgams, it is conjugate to $xa^j$ precisely when $\beta'$ is conjugate to $a^j$ by a power of $t$. In detail, the rotation preserving the outer-first form is unique. The two edge multipliers must be the same because the two outer factors are both $x$, which commutes with $t$. [Amalgam conjugacy theorem](https://books.google.com/books/about/Combinatorial_Group_Theory.html?hl=en&id=mIMpAQAAMAAJ).

To decide whether a reduced inner word $\beta'$ lies in $t^m\langle a\rangle t^{-m}$ for some integer $m$, count its linear Britton-reduced stable letters. A word of the form $t^m a^j t^{-m}$ reduces by innermost pinches to $t^{m'}a^{j'}t^{-m'}$, with stable-letter count $2|m'|$. This count is invariant under change of reduced HNN representative. If the receiver's count is $2u>0$, therefore test only conjugation by $t^u$ and $t^{-u}$. If the count is zero, it is already a base power. This covers arbitrary exponents for both the conjugator and the primitive target. [Britton's lemma](https://doi.org/10.2307/1970200), [native reduction](../experiments/round16_ak3_root_bs_scan.cpp).

Whitehead peak reduction gives the complete atlas from the $91$ pairs with $2k+2n+1\le31$. The native test uses the stored inverse marking for both donor slots. It validates two positive fixtures, one conjugate to $x$ and one to $xy$ in its marking. A strict ordinary control reaches the literal basis in **269** elementary instructions at raw peak **55**. The separate **29,812** deterministic checks compare the expected decision before and after conjugation, inversion and insertion of conjugated relators. One negative family is elliptic in the inner factor but does not lie in a $t$-conjugate of the base. [Atlas and fixtures](../experiments/round16_ak3_root_bs_atlas.py), [controls](../experiments/round16_ak3_root_bs_controls.cpp), [strict certificate](../certificates/round16_ak3_root_bs_control.json).

## Reproduction

Use a writable directory for `work` and the compacted first-exit directory from the Round 14 reproduction for `compacted`.

~~~sh
python3 -B experiments/round16_ak3_root_bs_atlas.py "$work/root-bs.tsv" \
  --control "$work/control.json" "$work/vertex.bin" "$work/mixed.bin"
c++ -std=c++17 -O3 -pthread experiments/round16_ak3_root_bs_scan.cpp -o "$work/root-bs"
c++ -std=c++17 -O3 -pthread experiments/round16_ak3_root_bs_controls.cpp -o "$work/root-bs-controls"
"$work/root-bs-controls"
"$work/root-bs" "$work/root-bs.tsv" "$work/vertex.bin"
"$work/root-bs" "$work/root-bs.tsv" "$work/mixed.bin"
"$work/root-bs" "$work/root-bs.tsv" "$compacted"/unique.*.bin
python3 experiments/elementary_verify.py "$work/control.json"
~~~
