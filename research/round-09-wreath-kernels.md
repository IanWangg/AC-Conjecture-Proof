# Simultaneous ordinary paths in infinite perfect wreath kernels

2026-11-19. A quotient path to the marked basis in $F/R$, with $R\subseteq[F,F]$, can be synchronized with any finite collection of surjective markings of $F$ into restricted wreath products $S\wr\mathbb Z$ with nonabelian finite simple lamp groups $S$. This applies to AK(3) in every finite derived layer of the braid kernel. A separate exact two-row control synchronizes the braid relation-module path with a marking into $A_5\wr\mathbb Z$.

## The infinite chief factor

Write $W=(\bigoplus_{i\in\mathbb Z}S_i)\rtimes\langle t\rangle$, where $t$ shifts sites by one. Its lamp subgroup $D=\bigoplus_i S_i$ is perfect, and $W'=D$ because $W/D$ is cyclic. It is a minimal $W$-normal subgroup. Indeed if a $W$-normal subgroup $K\subseteq D$ contains a nontrivial finitely supported element, choose a site at which its value is nontrivial. The center of the simple group at that site is trivial. A commutator with a suitable single-site element therefore gives a nontrivial element of $K$ supported only at that site. The intersection $K\cap S_i$ is normal in $S_i$, so $S_i\subseteq K$. Shifting gives $K=D$.

Let $\phi:F\twoheadrightarrow W$ and $G=F/(R\cap\ker\phi)$. The kernel of $G\to F/R$ is identified by $\phi$ with $\phi(R)\subseteq D$. It is either trivial or $D$. The action by conjugation on this kernel factors through the surjection $G\to W$, so in the latter case it is minimal normal in $G$ as well. It lies in $[G,G]$ since it is the image of $R\subseteq[F,F]$. The [relative minimal-normal lifting argument](round-05-finite-kernel.md#kernel-lifting-theorem) therefore lifts ordinary equivalence to the basis from $F/R$ to $G$. Iteration synchronizes any finite sequence of these markings. Each step uses the intersection produced at the previous step in place of $R$. One can interleave the finite or solvable-kernel markings covered by the [earlier lifting results](round-08-solvable-kernels.md).

For AK(3), take $R=N^{(s)}$ for any $s\ge1$, where $N$ is the normal closure of its braid relator and $N^{(s)}$ is the $s$-th derived subgroup. The known [braid kernel paths](round-05-finite-kernel.md#application-to-ak3) satisfy the hypotheses. When the image of the braid relator in $W/D$ is nonzero, $\phi(N)=\pi^{-1}(\pi\phi(N))$ where $\pi:W\to\mathbb Z$ is the projection. In fact a nonzero shift fails to commute with an appropriate single-site element, so $\phi(N)\cap D$ is nontrivial and contains all of $D$. Since $D$ is perfect, $\phi(N^{(s)})=D$ for every $s\ge1$. Such a joint lift corrects an infinite perfect kernel.

## Explicit rank-two marking and corrections

Mark $x=t$ and put $y=a_0 b_1$, where $a=(1\ 2\ 3)$ and $b=(1\ 2\ 3\ 4\ 5)$ generate $A_5$. The commutator $[y,xyx^{-1}]$ is nontrivial at site 1 and has no other support. Conjugation by $y$ and $xyx^{-1}$ acts at site 1 by $b,a$. Hence the generated subgroup contains the whole copy of $A_5$ at that site and, by shifting, every lamp. This proves the marking is onto. The braid relator has shift one.

In the code, start with $c=[y,xyx^{-1}]$ and $d=[r,c]$ for braid relator $r$. The lamp image of $d$ has support $\{1,2\}$. Conjugate $xdx^{-1}$ by a word of shift zero to ensure that its value at site 2 fails to commute with that of $d$. Their commutator is the identity outside site 2, and it belongs to $[N,N]$ because both entries lie in $N$. Shifting it to site zero and taking products of conjugates gives an explicit $[N,N]$ lift of each of the 60 local permutations.

First replay the existing 533-instruction ordinary path. Its endpoint $(U,V)$ agrees with $(x,y)$ modulo $[N,N]$ and $U$ has shift one. For $g,h\in[N,N]$ supported at site zero in the wreath image, $[g,U]$ is supported at sites zero and one. The double commutator $[h,[g,U]]$ is supported at site zero with value $[h_0,g_0]$. Its free word is a product of four conjugates of $U^{\pm1}$, so that donor can stay fixed at the end of the update. Using translated conjugates of this block corrects $V$ to its marked image. With that image fixed, a single-site commutator with the second row gives a nontrivial single-site block and corrects $U$. Every update block lies in $[N,N]$ and its translated conjugates do too. Thus the exact updates preserve the braid relation-module marking as they correct the wreath marking.

The complete ordinary sequence replays in **24,649 strict free instructions**. The second row is corrected at instruction 19,661. The [existing Fox evaluator](../experiments/braid_relation_module.py) separately checks that the final free residuals project to the identity in the braid group and have zero support in both Fox derivatives there. This verifies membership in $[N,N]$ via the abelianization of the kernel's covering graph. The free endpoint lengths are 2,436,675 and 63,987. [Exact joint replay and final digests](../results/round09_wreath_kernel.json).

~~~sh
python3 -B experiments/round09_wreath_kernel.py \
  | diff - results/round09_wreath_kernel.json
~~~
