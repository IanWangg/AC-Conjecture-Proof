# The common Wirtinger quotient and finite lifts of the middle relator

2026-11-19. The two outer donor relations jointly give an infinite cyclic quotient. In the marking where the middle relator has the exponent vector of the common row, a single permutation representation rules out every intermediate that makes the two donors equal in its quotient. The unrestricted middle block asks for conjugacy. Every finite collection of quotient tests for that middle block has a common lift, even inside one explicit coset of the commutator of the outer normal closures.

## The common quotient

Let \(F=F(x,y)\), write \(N_v=\langle\!\langle v\rangle\!\rangle_F\), and use \([a,b]=aba^{-1}b^{-1}\). The wrong and corrected marked pairs are \((A,B)\) and \((A,C)\), respectively, with

~~~text
A = XXYYxyyyxYY
B = XXYxyXyxYY
C = XXYYxyXyyxYY
~~~

Both pairs normally generate \(F\). The same-row outer pattern is \((A,B)\to(h,B)\to(h,C)\to(A,C)\). The middle block asks for conjugacy of \(B,C\) in \(F/N_h\) up to inversion. For any orientation of \(h\) allowed by the outer blocks, the class of \(B\) in \((F/N_h)^{\rm ab}\) is a generator of the infinite cyclic group. It equals the class of \(C\), so inversion of just one donor is excluded by abelianization. [Endpoint certificates](round-10-stable-proof.md#the-frozen-repair-and-its-ordinary-endpoints) · [Receiving-block criteria](round-10-ac-proof.md#exact-block-criteria)

Set \(y_i=x^i y x^{-i}\). Direct free reduction and Schreier rewriting give

$$
B^{-1}C=w[y_1^{-1},y_0^{-1}]w^{-1},\qquad w=\texttt{yyXY},\qquad
B=y_{-2}^{-1}y_{-1}y_{-2}y_{-1}^{-2}x^{-1}.
$$

In \(F/(N_BN_C)\) the first identity makes every adjacent pair \(y_i,y_{i+1}\) commute. The relation \(B=1\) then simplifies to \(y_{-1}^{-1}x^{-1}=1\), hence \(y=x^{-1}\). The homomorphism \(x\mapsto 1,\ y\mapsto -1\) onto \(\mathbb Z\) kills both \(B,C\), so the quotient is exactly \(\mathbb Z\). [Free-word identity checks](../results/round11_ac_proof_wirtinger_lifts.json)

## Equality in the middle quotient

Suppose \(h\) is a candidate for the two outer blocks and its signed exponent vector is \(\pm(0,-1)\). Orient it with exponent vector \((0,-1)\). Assume \(B=C\) as elements of \(F/N_h\), so \([y_1,y_0]=1\) in that group. In the kernel of the \(x\)-exponent map the \(y_i\) form a free basis. Cyclically reduce the Schreier word for \(h\) in that basis and translate the indices so that they range from \(0\) to \(m\). This operation only conjugates \(h\) in \(F\).

For \(m\ge1\), the presentation \(F/N_h\) is an HNN extension of \(H=\langle y_0,\ldots,y_m\mid h\rangle\) identifying the subgroup on \(y_0,\ldots,y_{m-1}\) with the shifted subgroup on \(y_1,\ldots,y_m\). The omitted extreme occurs in the cyclically reduced relator on each side, so Magnus's Freiheitssatz embeds both free associated subgroups. The HNN normal form embeds \(H\). If \(m\ge2\), the adjacent pair \(y_0,y_1\) lies in the first free associated subgroup and its commutator survives. Therefore \(m\le1\). For \(m=0\), the only oriented cyclic word is \(y_0^{-1}\). [Magnus, Freiheitssatz](https://doi.org/10.1515/crll.1930.163.141) · [Britton, The Word Problem](https://doi.org/10.2307/1970200)

If \(m=1\), then \(H\) is abelian because \(y_0,y_1\) commute. It is infinite cyclic since their two exponent coefficients \(p,-p-1\) are coprime. The word

$$
h_p=(y_0 y_1^{-1})^p y_1^{-1},\qquad p\in\mathbb Z,
$$

is primitive in the free group on \(y_0,y_1\). In the basis \((y_0 y_1^{-1},y_1^{-1})\) it is a power of the first generator times the second. Its exponent vector agrees with the specialized relator \(h\). Each quotient of the free group on \(y_0,y_1\) by one of these two words is infinite cyclic, and its kernel is the inverse image of the same rank-one sublattice of \(\mathbb Z^2\). Magnus's normal closure theorem then makes \(h\) conjugate to \(h_p\) up to inversion. The \(m=0\) word is conjugate to \(h_0\) in \(F\). [Magnus normal closure theorem and reference to the original proof](https://arxiv.org/abs/0904.1143)

Use the permutation marking in \(S_8\) with these one-line images.

~~~text
x = (1,3,4,5,6,7,8,2)
y = (2,6,8,4,3,7,5,1)
~~~

It kills \(B\) and sends \(A\) to cycle type \((4,4)\). The image of \(y_0 y_1^{-1}\) has order six. The residue types of \(h_p\), starting at \(p=0\), are \((1,7),(1,2,2,3),(3,5),(1,7),(2,6),(1,7)\). Cycle type is unchanged by conjugation and inversion, so none can satisfy the first outer block, even up to independently orienting and conjugating the relators. This excludes \(B=C\) throughout the stated exponent marking. The same exclusion covers every middle conjugator in the image of \(\langle B\rangle\) or \(\langle C\rangle\), since such a conjugation equation implies equality. At the abelianized level, the outer conditions also allow exponent vectors \([A]+k[B]\), after orienting \(h\) so that its signed determinant with \(B\) agrees with that of \(A\). The Freiheitssatz argument here treats \(k=0\). [Permutation products and power residues](../results/round11_ac_proof_wirtinger_lifts.json)

## A lift in every finite quotient

Write

$$
U=\ker(F\xrightarrow{x\mapsto 1,\ y\mapsto 0}\mathbb Z),\qquad
D=[N_B,N_C].
$$

Each word \(h\in A D\) satisfies both outer blocks without aligning any conjugates, because \(D\le N_B\cap N_C\). Moreover \(N_A D=U\). In \(F/N_A\) the images of both \(N_B\) and \(N_C\) are the whole group, so the image of \(D\) is its derived subgroup. Killing it makes the quotient abelian, with the sole abelian relation \([A]=(0,-1)\).

For any finite quotient \(q:F\twoheadrightarrow G\), put \(K=q(U)\) and \(L=q(D)\). Then \(K\) is normally generated in \(G\) by \(q(y)\), \(G/K\) is cyclic, and \(K=\langle\!\langle q(A)\rangle\!\rangle_G L\). The following finite lifting lemma gives an element \(q(A)\ell\) which normally generates \(K\) in \(G\), with \(\ell\in L\).

**Finite lifting lemma.** Let \(K\trianglelefteq G\) with \(G\) finite, \(G/K\) cyclic, and \(K\) normally generated in \(G\) by one element. If \(L\trianglelefteq G\), \(L\le K\), and \(a\in K\) satisfies \(K=\langle\!\langle a\rangle\!\rangle_G L\), then some element of \(aL\) normally generates \(K\) in \(G\).

To prove the lemma, take the maximal proper \(G\)-invariant subgroups \(M_i\) of \(K\) and their factors \(P_i=K/M_i\). An element normally generates \(K\) in \(G\) exactly when every projection into \(P_i\) is nonidentity, since \(G\) is finite. Each \(P_i\) has no proper nontrivial \(G\)-invariant subgroup. The abelian factors are distinct simple quotients of the cyclic module \(K/[K,K]\) over \(\mathbb Z[t,t^{-1}]\), where \(t\) acts by a lift of a generator of \(G/K\). They correspond to distinct maximal ideals of the Laurent polynomial ring. The Chinese remainder theorem gives surjectivity to their product.

Adjoin the nonabelian factors one at a time. Each nonabelian \(P_i\) is perfect since its derived subgroup is a nontrivial \(G\)-invariant subgroup. If the image of \(K\) in the old product times \(P_i\) omits part of this new factor over the identity in the old product, then that fibre is trivial by \(G\)-invariance. The image is then the graph of a surjective \(G\)-equivariant homomorphism from the old product to \(P_i\). Each direct factor has \(G\)-invariant image, so each maps trivially or surjectively. An abelian factor cannot surject, and two commuting factors cannot both surject onto a nonabelian group. Thus one previous nonabelian factor surjects and does so isomorphically by its own \(G\)-simplicity. The two maps from \(K\) would have the same kernel, contradicting distinctness of the \(M_i\). This proves surjectivity to the whole product, including the mixed abelian and nonabelian factors.

Now consider the image \(\bar L\) of \(L\) in that product. Its projection to any \(P_i\) is full or trivial. In a nonabelian factor with full projection, commutators of \(\bar L\) with the copy of \(P_i\) supported on that coordinate generate the entire copy, by perfectness. Thus \(\bar L\) contains those nonabelian coordinates independently. The abelian projection of \(\bar L\) is a submodule of the product of distinct simple modules. The Chinese remainder idempotents give independent choice in each abelian coordinate with full projection. After choosing the abelian projections, the nonabelian copies can adjust every nonabelian coordinate with full projection. For each coordinate where \(a\) projects to the identity, \(L\) projects onto that factor by \(K=\langle\!\langle a\rangle\!\rangle_G L\). Choose the image of \(\ell\) nonidentity there and identity in all other coordinates. This gives the claimed element of \(aL\).

Lift \(\ell\) to \(d\in D\) and choose \(h=Ad\). The image \(q(h)\) kills exactly \(K\) by normal closure in \(G\), so the middle quotient \(G/\langle\!\langle q(h)\rangle\!\rangle_G=G/K\) is cyclic. The two donors agree there because their \(x\)-exponents are equal. For finitely many quotient tests, apply the lemma once to the image of the diagonal map into their product. The same free word \(h\) then passes all of those tests and has both outer blocks in the free group. The lift generally depends on the chosen finite image. Compactness also gives a lift in \(A\overline D\subset\widehat F\) whose closed normal closure is \(\overline U\). This profinite lift alone gives no ordinary middle block in \(F\).

For a direct example take \(h=A[B,y^{-1}Cy]\). It has both outer routes by two signed conjugate products per donor. Strict replay checks each expanded route in the free group. The image of \(y\) lies in the normal closure of the image of \(h\) in each of four test markings, including both separating markings used on the Round 11 fixed-stage candidates. In the dihedral marking of order 14, \(A\) maps to the identity and \(h\) maps to a generator of the normal rotation subgroup. The example illustrates why a separator for one intermediate cannot certify the whole pattern. [Strict outer replay and finite closure checks](../results/round11_ac_proof_wirtinger_lifts.json) · [Round 11 fixed-stage witnesses](round-11-ak3.md#three-block-repair-through-a-common-middle-relator)

## Reproduction

~~~sh
python3 -B experiments/round11_ac_proof_wirtinger_lifts.py \
  | diff - results/round11_ac_proof_wirtinger_lifts.json
~~~
