# Round 08 · Alternating quotient-conjugacy moves for AK(3)

2026-11-19. Two successive fixed-donor Andrews–Curtis moves take AK(3) to `(XXXXXyxYXYxxyyy, XXyxYXYxxyyyxYYY)`. The 208-move elementary replay reaches cyclic peak **31** and raw peak 49. The endpoint is absent from the independently verified cap-30 component, so 31 is its least ordinary cyclic entry peak. Continuing the previously reached energy-18 chamber by five fixed-donor moves reaches a different energy-31 orbit with the same least entry peak. [Direct certificate](../certificates/round08_ak3_acm_ak3.json), [five-move continuation](../certificates/round08_ak3_acm_chamber18.json), [cap-30 closure](round-08-cyclic30.md).

## Finite completion on one fixed donor

Let $r,d$ be the receiver and donor, with exponent vectors $a,b$ satisfying $\det(a,b)=\pm1$. Start with a loop labelled $r$. At each stage, attach loops labelled by every cyclic rotation of $d^{\pm1}$ at every vertex of the previous folded graph, then fold again. Any loop labelled $w$ at any vertex gives a conjugate of $w$ in the based subgroup. Modulo the normal closure of $d$, each new based generator is trivial, so this conjugate equals $r^e$ for some $e$. The exponent is

$$
e=\frac{\det(\operatorname{ab}(w),b)}{\det(a,b)}.
$$

Thus $e=\pm1$ identifies a legal replacement of $r$ by $w$ while keeping $d$. The folded graph needs only ordinary letter labels. The determinant recovers the weight from the word itself. This specializes the weighted completion of Panteleev and Ushakov to a rank-two pair with a unimodular exponent matrix. [Panteleev–Ushakov, §2](https://arxiv.org/html/1609.00325v1#S2).

The Python compiler independently folds a bouquet of based loops and retains exact edge provenance. At a collision it records the path between the identified vertices whose label freely reduces to the empty word. A target loop expands to a product of signed copies of $r$ and conjugates of $d^{\pm1}$. The compiler verifies the free-word identity before gathering the copies of $r$ to the right. It then implements the donor factors by elementary conjugations, inversions and right multiplications. The strict verifier separately replays the resulting ledger.

## All primitive lengths in a finite completion

Up to inversion, any primitive receiver candidate has exponent vector $a+kb$ for an integer $k$. In rank two this vector determines the primitive conjugacy class. For each tail direction $b_*=b$ or $b_*=-b$, sign the ambient generators so that both coordinates of $b_*$ are nonnegative. In a coordinate where it is zero, choose the sign that makes the corresponding entry of $a$ nonnegative. Write $a,b_*$ in this signed basis and choose the least nonnegative $K$ for which $a+Kb_*$ is nonnegative. The columns $a+Kb_*,b_*$ form a nonnegative unimodular matrix. If the columns are comparable, subtract the smaller one from the larger one. In the incomparable case the determinant condition forces the two standard coordinate columns. Reversing the subtractions by positive Nielsen multiplications yields a basis $U,V$ with the prescribed columns. Consequently every tail class has cyclic representative $UV^j$ for some $j\ge0$. Test the finitely many remaining slopes by their Euclidean words. [Osborne–Zieschang, Theorem 1.2](https://geodesic.mathdoc.fr/item/IM_1981__63_142788/).

In the completion graph, reading $V$ defines a partial injection. Its directed components are paths and cycles. At each vertex $v$ where $U$ can be read, test whether the endpoint is in the same $V$-component as $v$ and can return to $v$ by proceeding forward. This tests the entire $UV^j$ family without enumerating primitive words by length. The control `(xyxYXY,y)` yields `x` and the independent elementary replay reaches `(x,y)` in 41 moves.

## Alternating search results

The search starts at AK(3), $W_{22}$, $W_{23}$, the energy-18 chamber, three Whitehead minima with known cap-31 entries, and the first literal cap-37 marking. It scans both orientations on entry and switches the receiver after each continuation. Each seed has up to five layers and 20 retained states per layer. Each chart completes up to four stages at a cap of 350,000 allocated vertices, and samples bounded returns of length at most 19 from at most 64 vertices. The primitive test covers all lengths in the last fully completed graph at each of the **172** scanned charts. It finds no primitive. Further stages, longer nonprimitive intermediate returns, and other alternating choices remain open. [Round-seven markings](round-07-stable-proof.md#sharp-ordinary-entries-for-the-three-minima-and-one-marked-chart), [search and replay receipts](../results/round08_ak3_acm.json).

For each seed with an endpoint outside cap 30, retain a strict certificate for its shortest selected endpoint. The energy-23 and energy-25 certificates shorten two previously connected Whitehead markings through one and two quotient-conjugacy moves respectively. The known cap-30 exclusions give sharp entry peak 31 to the five endpoints with matching replay peaks. The shortest endpoint obtained from the literal cap-37 marking has cyclic peak at most 37.

| Source | Endpoint energy | Alternating moves | Elementary moves | Cyclic peak |
| --- | ---: | ---: | ---: | ---: |
| AK(3) | 31 | 2 | 208 | 31 |
| $W_{23}$ | 29 | 1 | 1,226 | 41 |
| Energy-18 chamber | 31 | 5 | 1,003 | 31 |
| Entry 0 | 25 | 2 | 575 | 31 |
| Entry 1 | 23 | 1 | 499 | 31 |
| Entry 2 | 27 | 3 | 673 | 31 |
| Entry 3 | 27 | 1 | 571 | 37 |

The search reaches 699 distinct signed orbits, including 104 absent from cap 30. Whitehead minimization strictly shortens 39 of the 104 external orbit representatives and gives 100 distinct minima. Independent replay verifies a planar-link parity obstruction to geometry for all 100 minima. Their alternative markings and deeper completions remain candidates for further ordinary searches. [Geometry receipts](../results/round08_ak3_acm_geometry.json).

## Reproduce

~~~sh
acm=/tmp/ac-r08-acm/acm
mkdir -p /tmp/ac-r08-acm
c++ -std=c++17 -O3 -pthread experiments/round08_ak3_acm.cpp -o "$acm"
python3 -B experiments/round08_ak3_acm_search.py "$acm" results/round08_ak3_acm.json \
  --catalogue /tmp/ac-r07-ak3/c30.orbit.tsv --certificates certificates
python3 -B experiments/elementary_verify.py certificates/round08_ak3_acm_*.json
python3 -B - <<'PYTHON' > /tmp/ac-r08-acm/outside30.tsv
import json
with open('results/round08_ak3_acm.json') as source:
    for pair in json.load(source)['orbits_outside_catalogue']:
        print(*pair, sep='\t')
PYTHON
python3 -B experiments/round01_geometric_archive.py /tmp/ac-r08-acm/outside30.tsv \
  | diff - results/round08_ak3_acm_geometry.json
~~~
