# Synchronizing both finite witnesses with the braid-kernel path

2026-11-19. A new 1,793-move ordinary certificate takes AK(3) to a tuple whose images are the marked basis in the braid relation-module quotient and in both finite frozen-donor witnesses at once. The free endpoint has lengths 39,291 and 162,135. The same synchronization argument applies at every finite layer of the braid kernel.

Let $b=xyxYXY$ and $N=\langle\!\langle b\rangle\!\rangle$ in $F(x,y)$. Let $\phi$ be the combined homomorphism given by the two markings from round three. Its target is $K=\mathrm{SL}_2(\mathbb F_{11})\times A_5$, since both permutations in the second marking are even. The proof uses $\phi$ as one simultaneous map. [Round-three finite markings and obstruction](round-03-frozen-donors.md).

The three words

$$
[b,xbx^{-1}],\qquad [b,yby^{-1}],\qquad [b,x^{-1}bx]
$$

lie in $[N,N]$. Their finite images generate all $79{,}200=1320\cdot 60$ elements of $K$, as checked by closure with both signs. This computation also provides explicit lift words for every element, including those supported in only one factor. The separate class checks verify that in each factor, for every noncentral $d$, the elements $g d g^{-1}d^{-1}$ generate that factor. To see why the class check suffices, take one representative per conjugacy class and enumerate all its conjugates. Conjugating a donor transports the resulting generated subgroup, so the check holds for the whole class. These facts also prove that $K$ is perfect.

## Corrections that preserve the earlier quotient

Suppose $D$ is the donor row and $g\in[N,N]$. Conjugate the donor by $g$, multiply the recipient by it, and undo the conjugation. Then multiply the recipient by $D^{-1}$, using inversion and restoration of the donor. This changes the recipient by the right factor $gDg^{-1}D^{-1}$. The factor is trivial in $F/[N,N]$, and the donor is exactly restored in the free group. If $\phi(g)$ has support in only one finite factor, the correction also leaves the other finite factor unchanged.

The 533-move prefix reaches the marked basis in $F/[N,N]$. Its endpoint $(U,V)$ has finite components of the form $(A,1)$ and $(1,B)$, with $A$ noncentral in the matrix factor and $B$ nonidentity in $A_5$. First use $U$ to move the matrix component of $V$ to the image of $y$. Next fix the two finite components of $U$ using $V$. Finally use the corrected $U$ to fix the permutation component of $V$. Each move of one component is implemented by factoring a finite correction into products of $g D g^{-1} D^{-1}$. Every chosen $g$ is supplied by the explicit derived-subgroup lifts. The replayer expands the conjugations into single-letter moves, then checks the full certificate from the original AK(3) pair.

The corrected free tuple agrees with the marked basis in the three quotient factors. It supplies a new reachable source whose finite images no longer have the frozen-donor signatures of $(U,V)$. Folding the two final free words gives a graph with 157,360 vertices. An independent topological sort certifies acyclicity of all eight signed transition graphs used in the rank-two test. Thus the displayed endpoint subgroup contains no ambient primitive, including after a Nielsen-only suffix. [Strict certificate](../certificates/round04_finite_corrections.json), [correction receipts](../results/round04_finite_corrections.json), [folded endpoint test](../results/round04_finite_core.json), [primitive test](research-q.md).

## Synchronization at arbitrary finite braid-kernel depth

For $m\ge 1$, put $G_m=F/\gamma_{m+1}(N)$. Since $\phi([N,N])=K$ and $K$ is perfect, induction gives $\phi(\gamma_{m+1}(N))=K$ for every $m$. In particular the marked map from $F$ onto $G_m\times K$ is surjective. One can lift an element of $G_m$ first, then correct its finite image by multiplying by an element of $\gamma_{m+1}(N)$.

The round-two lifting theorem gives an ordinary path starting at AK(3) whose endpoint matches the marked basis in $G_m$. The two rows together normally generate each finite factor, so in each factor at least one row has noncentral image. Use that row as donor to set the other row's component to its marked target, which is noncentral. Then use the newly set row as donor to correct the first. Choose all conjugators in $\gamma_{m+1}(N)$ and with support in the finite factor being corrected. The operations leave $G_m$ unchanged at every completed correction. Hence all $G_m\times K$ have ordinary paths to the marked basis. The strict lengths can grow with $m$, and the displayed free-group sequence ends at the longer free tuple above. [Round-two braid-kernel proof](round-02-relative-quotients.md).

~~~sh
python3 -B experiments/round04_finite_corrections.py /tmp/ac-r04-finite.json \
  | diff - results/round04_finite_corrections.json
diff /tmp/ac-r04-finite.json certificates/round04_finite_corrections.json
python3 -B experiments/elementary_verify.py certificates/round04_finite_corrections.json
c++ -std=c++17 -O3 experiments/round04_finite_core.cpp -o /tmp/ac-r04-finite-core
python3 -B -c 'import json; print(*json.load(open("certificates/round04_finite_corrections.json"))["target"])' \
  | /tmp/ac-r04-finite-core | diff - results/round04_finite_core.json
~~~
