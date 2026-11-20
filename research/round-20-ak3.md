# All fixed-donor primitive directions at the nine energy-17 minima

Both choices of fixed donor at each of the **nine** cap-33 energy-17 minima now exclude primitive replacement at arbitrary length. The final open direction from Round 19 held `xxxYxxYXYXY` fixed and tried to replace `xxyXYY`. A degree-three Magnus quotient in characteristic **9377** excludes it. An independent checker annihilates all 1,331 cubic operator columns and checks every primitive slope residue. Separately, an exact six-boundary test excludes four fixed-donor products from the nine minima and the sixteen new energy-20 states. [Previous 17 directions](round-19-minimum-fibre-quotients.md#all-nine-energy-17-additions), [rank-eleven certificate](../results/round20_ak3_rank11_resonance.json), [four-product receipt](../results/round20_ak3_four_products.json).

## Degree-three obstruction in the remaining fibre

Use the marking from Round 19, with new generators $u,t$ and $u_i=t^iut^{-i}$. The fixed relator becomes

$$
u_1^{-1}u_5^{-1}u_{10}^{-1}u_{11}u_7u_4u_0,
$$

and the receiver becomes $Rt$, where $R=u_1^{-1}u_5^{-1}u_4u_1$. Both extremes of the relator occur once, so its deletion quotient is free-by-cyclic with fibre basis $u_0,\ldots,u_{10}$. The shift $\phi$ takes $u_i$ to $u_{i+1}$ for $0\le i<10$ and takes $u_{10}$ to $u_{10}u_5u_1u_0^{-1}u_4^{-1}u_7^{-1}$. Its linear characteristic polynomial is $z^{11}-z^{10}+z^7-z^5+z^4-z+1$. Every height-one primitive has representative $u_0^kt$ for some integer $k$. Multiplying a conjugator by a power of the height-one source adjusts its height to zero. In the fibre, conjugacy thus requires

$$
gR=u_0^k\phi(g).
$$

[Fixed-donor criterion and slope marking](round-19-minimum-fibre-quotients.md).

In the degree-three noncommutative Magnus algebra over $\mathbb F_p$, assign $u_i$ to $1+X_i$. Write $g=1+g_1+g_2+g_3$ by homogeneous degree and let $A$ be the linear shift. The coefficient of the unknown $g_d$ in degree $d$ is $I-A^{\otimes d}$, since $R$ and $u_0^k$ have constant coefficient one. The target $u_0^k$ has degree-$j$ coefficient $\binom{k}{j}X_0^j$. For $d=1,2$, both coefficient matrices are invertible in characteristic 9377. It follows that the unique solution in degree one is polynomial in $k$ of degree at most one, and in degree two of degree at most two. Indeed a degree-$d$ coefficient of a product of homogeneous terms of degrees $i$ and $d-i$ has polynomial degree at most $i+(d-i)$, and the substitution matrix is independent of $k$. The degree-three right-hand side computed from these lower solutions therefore has polynomial degree at most three in $k$.

The retained cubic left functional kills $I-A^{\otimes3}$ and evaluates that right-hand side to

$$
8380+3516k+6036\binom{k}{2}+3761\binom{k}{3}\pmod{9377}.
$$

Four sample values determine this polynomial. The verifier independently checks the full lower-degree matrices have ranks **11** and **121**, checks the lower solutions at all four sample slopes, and evaluates the functional directly on each of the **1,331** cubic columns. It then checks that the polynomial is nonzero for all $k\in\mathbb F_{9377}$. Because $(1+X_0)^{9377}=1$ in this truncated algebra, those residues cover every integer slope. The alternative prime 821 leaves three residues and provides a comparison. [Graded generator](../experiments/round20_ak3_rank11_resonance.py), [independent verifier](../experiments/round20_ak3_rank11_verify.py).

## Four fixed-donor products

If the same donor $B$ is used for the first three products, four ordinary products can yield a primitive only at slope $[A]+j[B]$ with $j\in\{-4,-2,0,2,4\}$. The primitive may be oriented so that the coefficient of $[A]$ is one. The argument also covers a last product changing the other slot because its cyclic product can be read starting with the same occurrence of $A$. For a slope, existence is equivalent to a spherical equation on $A$, four signed copies of $B$, and $P^{-1}$ where $P$ is the Euclidean primitive of that slope. The cross-boundary contraction from Round 19 reduces this six-boundary test to the existing exact four-boundary solver. Both donor directions and all signs are checked. The nine minima give **90** slopes and **703,353** contractions. The sixteen additional energy-20 states give **160** slopes and **2,271,673** contractions. Neither group has a hit. [Exact contraction argument](round-19-ak3.md#three-products-and-five-boundary-words), [solver](../experiments/round19_ak3_three_products.cpp).

The positive control has nonprimitive coordinates and no one-product, two-product, or three fixed-donor-product primitive. Its four-product spherical witness exposes a primitive after **364** strict instructions and reaches the literal basis in **426** instructions at cyclic peak **83**. This calibrates the construction and replay. Arbitrary switches of receiver during a four-product path remain outside the fixed-donor calculation. [Strict control ledger](../certificates/round20_ak3_four_products_control.json), [witness replay](../experiments/round19_ak3_three_products_replay.py).

## Reproduction

~~~sh
python3 -B experiments/round20_ak3_rank11_resonance.py \
  | diff -u results/round20_ak3_rank11_resonance.json -
python3 -B experiments/round20_ak3_rank11_verify.py results/round20_ak3_rank11_resonance.json
c++ -O3 -std=c++17 -pthread experiments/round19_ak3_three_products.cpp -o "$work/products"
head -9 certificates/round18_ak3_c33_low20.tsv > "$work/energy17.tsv"
awk -F '\t' 'length($1)+length($2)==20' certificates/round18_ak3_c33_low20.tsv > "$work/energy20.tsv"
"$work/products" fixed4 "$work/energy17.tsv" 8
"$work/products" fixed4 "$work/energy20.tsv" 6
python3 -B experiments/elementary_verify.py certificates/round20_ak3_four_products_control.json
~~~
