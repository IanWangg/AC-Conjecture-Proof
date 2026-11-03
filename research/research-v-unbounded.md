# V follow-up: an unbounded two-conjugate primitive-free theorem

Date: 2026-11-02. **This is a restricted subgroup theorem, not a solution of AK(3) or the ordinary AC conjecture.** It supplies no invariant under arbitrary repeated AC moves. No novelty or priority claim is made.

## The result

Let `F=F(x,y)` and

    p=xxxYYYY,  b=xyxYXY,  H0=<p,b>.

Capital letters denote inverses. The following result has a finite exact computational certificate and an unbounded geometric deduction:

> **Theorem.** For every pair u,v in H0 and every a,c in F, the subgroup `<a u a^-1, c v c^-1>` contains no primitive element of the ambient free group F.

There is no word-length, cyclic-energy, exponent, Nielsen-step, or conjugating-tail bound in this statement. It strengthens [V's complete energy-250 one-phase scan](research-v.md): any initial Nielsen prelude stays in H0, and any Nielsen suffix preserves the subgroup after the independent-conjugation phase. Therefore such a phase pattern cannot expose a primitive coordinate or reach a free basis, at any energy. The theorem even permits arbitrary elements of H0 as the two sources; they need not jointly be a basis.

Further individual conjugations after Nielsen mixing can again change the subgroup. The theorem is not asserted for that larger family. It neither proves AK(3) non-AC-trivial nor increases the established global cyclic-peak lower bound of 23.

## How this direction arose

Before this follow-up, V had read the repository README, the basis-sublevel proof, Q's axes theorem, and R's detector/reverse-search work. T independently audited every source of V's energy-250 scan; all 2.9 million resulting graphs were primitive-free. Rather than extrapolate from those finite failures, V looked for a finite overgroup certificate controlling all source words at once.

Every cyclic reduction or rotation of an element of H0 labels a loop at some vertex of its fixed finite folded core. Two such loops may be based at different vertices. Identifying those two vertices gives a finite overgroup containing the rotated subgroup. The overgroup itself can contain primitive elements; treating it as primitive-free would be wrong. The useful refinement is an integer character whose kernel contains both loops. The coordinating researcher suggested auditing these kernels using edge voltages and finite sign certificates, while warning that partial maps with unbounded displacements cannot be deduplicated by their finite maps alone. V implemented the character construction and a sufficient weighted-cycle certificate. No unbounded displacement states are merged in this argument.

The coordinating researcher and U independently reviewed the finite data and the full geometric proof. U separately reconstructed all graph quotients and character pullbacks, and both reviewers recomputed the strongly connected components and checked the saved integer potential inequalities without calling V's Bellman--Ford solver. These contributions are explicitly distinguished below.

## 1. The finite graph-and-character certificate

The based folded core Γ of H0 has 10 vertices and 11 unoriented edges. Its actual full adjacency array, in letter order `x,X,y,Y`, is saved in [v_vertex_identification_results.json](../certificates/v_vertex_identification_results.json). It is the fold of the literal two-loop bouquet `(p,b)`; in particular its fundamental group has image exactly H0.

For each unordered pair of distinct vertices α,β of Γ, identify them and fold, obtaining a based labelled graph `K_{αβ}` and a labelled projection `π:Γ→K_{αβ}`. There are exactly **45** cases. Every resulting graph has rank three: **there are no rank-dropping exceptions**. The folded graph has at most nine vertices.

Choose spanning-tree paths `s_v` in Γ from its base 0 to v. In the quotient, the word

    t = s_α s_β^-1

is a loop at 0. Choose a spanning-tree basis `z_1,z_2,z_3` for K. Rewrite p,b,t in that basis and take their three integer exponent rows `r_p,r_b,r_t`. The construction sets

    d = r_t · (r_p × r_b),
    h = (r_p × r_b)/d.

In every saved case, `d=+1` or `d=-1`. Give each oriented tree edge voltage zero, each positive chord voltage `h_i`, and its inverse voltage `-h_i`. Reading a based loop and summing edge voltages defines a homomorphism

    χ_{αβ}:π_1(K_{αβ},0)→Z,
    χ(p)=χ(b)=0,    χ(t)=1.

The determinant fact is a checked finite property of these 45 cases, not an unsupported inference from a unimodular abelianization matrix to a free basis. For the proof below, the directly checked character equations suffice.

The finite audit additionally verifies that the pullback voltage on Γ is an exact integer coboundary: there are integers f(v) such that every projected oriented Γ-edge `v→w` has voltage `f(w)-f(v)`. U independently checks all **990** directed-edge equalities across the 45 projections. Hence every closed path in Γ, based at any vertex, has voltage zero after projection. This also follows from χ killing H0, but the explicit coboundary check avoids any implicit rebasing assumption.

The kernel theorem certified in the next section is:

> For every distinct α,β, the subgroup `ker χ_{αβ}`, viewed as a subgroup of F through the labelled immersion K, contains no ambient primitive element.

The kernels are infinite subgroups. Their primitive-freeness is inferred from finite cycle inequalities, rather than truncating their infinite covers.

## 2. Why the finite voltage inequalities exclude every primitive

In rank two, every cyclically reduced primitive word uses at most one sign of each ambient generator, and at least one of its two signed generators is isolated: its cyclic word avoids the double of that generator. One proof uses a signed Euclidean/Christoffel primitive representative for its coprime exponent vector. If the absolute x-exponent is at least the absolute y-exponent, its y letters can be isolated; the other case is symmetric. Pure-generator primitive words are included. Primitive conjugacy uniqueness identifies every primitive with that representative. See [Q's discussion](research-q.md) and the primary rank-two results in [Clay--Conant--Ramasubramanian](https://msp.org/involve/2014/7-4/involve-v7-n4-p01-p.pdf), especially Corollary 4.4. This is a necessary condition, not a sufficient test for primitivity.

For each K, each signed alphabet in `{xy,xY,Xy,XY}`, and either forbidden double, construct a finite directed edge-state graph. A state `(v,i)` represents the available outgoing edge with signed letter i at vertex v. It transitions to the next chosen-letter edge at its endpoint, unless that repeats the forbidden letter. Give this transition the voltage of the edge being read at the source state. Thus every cyclic loop using that alphabet and avoiding the forbidden double gives a closed directed walk of exactly the same total voltage. All graph vertices are included; the test is not restricted to the distinguished base.

Every directed closed walk lies in a strongly connected component C. Put `N=|C|`. V's solver finds a sign `ε_C` in `{+1,-1}` and integer potentials `q_C` such that every internal transition `i→j` of weight w satisfies

    q_C(j) <= q_C(i) + N ε_C w - 1.                 (*)

Summing (*) around any nonempty directed closed walk of length L gives

    N ε_C (total voltage) >= L > 0.

Its total voltage is therefore nonzero. A singleton component with a self-loop is checked by the same inequality; a zero-weight cycle cannot pass. Components with no cycle require no inequality certificate. Different components may have different signs, which is harmless because a closed walk remains inside one component.

The construction of the potentials uses Bellman--Ford on transformed weights `N ε_C w-1`. The proof and independent verifiers use only the displayed integer inequalities. Solver failure would be unresolved, not a negative primitive decision. For AK(3), all **360** signed-double-free graphs pass: their **302** cyclic strongly connected components have **822** explicitly saved transition inequalities. There are no unresolved components. See [v_voltage_cycle_results.json](../certificates/v_voltage_cycle_results.json).

Suppose an ambient primitive belonged to `ker χ` at base 0. Freely cyclically reduce its accepted based loop as `q z q^-1`. The central path z is a cyclic primitive loop at another vertex. Inverse edges have opposite voltage, so the two q paths cancel their voltages and z still has voltage zero. Its signed alphabet and isolated generator put it in one of the directed graphs above, contradicting (*). This proves the kernel theorem at all word lengths.

The [coordinator's standalone audit](../results/v_voltage_independent_review.json) independently refolds `<p,b,t>`, verifies each projection, checks inverse edge voltages and `(χ(p),χ(b),χ(t))=(0,0,1)`, reconstructs components by mutual reachability, and checks all 822 inequalities. [U's separate audit](../results/u_voltage_phase_review.json) uses an independently written equivalence-relation fold, reconstructs the character pullbacks, and independently checks the same finite inequalities. Neither auditor imports V's constructor or potential solver.

## 3. The arbitrary-word and arbitrary-tail deduction

First, H0 itself is primitive-free: it embeds in any one of the certified kernels because χ(p)=χ(b)=0. Every element of H0 accepts a based loop in Γ. Cancelling its initial and terminal inverse paths leaves its cyclic reduction as a loop at another Γ-vertex, and a cyclic rotation merely changes the starting vertex on that loop.

Take nonidentity u,v in H0 and arbitrary conjugates `g=a u a^-1`, `h=c v c^-1`. Consider their axes in the free Cayley tree.

If the axes intersect, move their common point to the identity by one common conjugation. The two elements become cyclic rotations r,s of the cyclic reductions of u,v. They label loops in Γ at some vertices α,β.

If α=β, transport that common vertex to base 0 along `s_α`. The two transported loops lie in H0, so they generate a primitive-free subgroup.

If α differs from β, their projected loops in K are based at the same identified vertex. Each has voltage zero because the pulled-back Γ-voltage is exact. Transporting both loops to 0 along the same projected path `s_α` adds the path's voltage and then subtracts it. The transported subgroup therefore lies in `ker χ_{αβ}`, which is primitive-free. Equivalently, with

    A=s_α r s_α^-1∈H0,    B=s_β s s_β^-1∈H0,

the common transported pair is `(A,t B t^-1)`, and both character values are zero. No assertion that A,B jointly form an H0 basis is used.

If the axes are disjoint, Q/R's axes proof gives, after a common conjugation, a folded barbell whose two word circles are cyclic rotations of u and v and whose nonempty bridge is the shortest axis-to-axis path. A cyclic closed path crossing a separating bridge traverses an edge of it in both directions, and hence uses both signs of an ambient generator. It cannot read a cyclic primitive word. A cyclic loop staying in a circle is a nonzero power of u or v up to conjugacy. A nonprimitive element of H0 has no primitive nonzero power, so this case is also primitive-free.

If either source is the identity, the subgroup is cyclic and the same nonprimitive-power observation applies. Ambient primitivity is preserved by common conjugation. These cases prove the theorem.

## 4. AK(2) falsification control

The same construction applied to `(xxYYY,xyxYXY)` gives 28 vertex identifications, again all rank three. The strict-cycle certificate succeeds on 25 cases and correctly fails on exactly three: vertex pairs `(1,4)`, `(3,7)`, `(5,6)` in the saved AK(2) graph. Each failed kernel has an explicit voltage-zero primitive cyclic loop

    xYxYYxYY

at vertex 0. Its primitivity is immediate from signed basis `(x,Y)` and program `RLRL`, taking the second coordinate: the successive positive updates remain free bases. The loop and its zero voltage are directly checked. It is the same primitive detected in the positive one-phase AK(2) search that compiles to a [232-move strict basis certificate](../certificates/t_v_ak2_hidden_full.json).

The AK(2) geometry is in [v_ak2_vertex_identification_results.json](../certificates/v_ak2_vertex_identification_results.json), and its intentionally partial strict-cycle result is in [v_ak2_voltage_cycle_results.json](../certificates/v_ak2_voltage_cycle_results.json). This control prevents a vacuous absence rule: the algorithm rejects its proposed negative certificate where an actual zero-voltage primitive exists. The bounded length-8 primitive enumeration here supplies explicit positive witnesses only. The AK(3) final construction uses **no bounded primitive enumeration at all**; its unbounded exclusion is supplied by the finite inequalities.

## Reproduction and completion standard

All scripts use the Python standard library and the already published R graph primitives. Put the published scripts together in `experiments/` and run:

```sh
python3 experiments/v_vertex_identification.py --n 3 --cap 0 \
  --output /tmp/v_identifications.json
python3 experiments/v_voltage_cycle_review.py /tmp/v_identifications.json \
  --output /tmp/v_voltages.json
python3 experiments/verify_vertex_voltage.py /tmp/v_identifications.json \
  /tmp/v_voltages.json --output /tmp/v_independent_review.json
python3 experiments/v_vertex_identification.py --n 2 --cap 8 \
  --output /tmp/v_ak2_identifications.json
python3 experiments/v_voltage_cycle_review.py /tmp/v_ak2_identifications.json \
  --output /tmp/v_ak2_voltages.json
```

The first weighted result must have 45 fully certified cases and zero unresolved cases. The AK(2) weighted result must instead have 25 fully certified cases and three unresolved cases with the explicitly supplied primitive loops. A partial or unresolved certificate must never be substituted for the fully certified AK(3) data.

This follow-up replaces the initial one-phase energy bound with an unbounded restricted theorem. It does not classify the unrestricted AC orbit. A general path may change both coordinates through later alternating Nielsen moves and individual conjugations, outside the stated two-conjugate family. No complete free-basis path and no invariant under all ordinary AC moves is supplied; all four requested breakthrough goals remain unachieved.
