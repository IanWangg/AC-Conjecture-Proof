# An independent ordinary route to the second stable waypoint

2026-11-19. The second stable waypoint $(\texttt{XXXYxyxyXYY},\texttt{XYXYYXyXYYXy})$ has a 784-move strict ordinary certificate. This route uses a transported marking and has cyclic peak 35 and raw peak 45. The separate peak-30 certificate gives the sharper peak. [Transport certificate](../certificates/round07_automorphism_D23.json), [peak-30 certificate](../certificates/round07_ak3_marked_waypoint30.json).

Let $\alpha$ be the free-group automorphism $x\mapsto x$, $y\mapsto yx$. One deletion marking for the primitive pivot at the rank-three source gives

$$
E=(\texttt{XXYxyyXYxY},\texttt{XYYxYXyXYxYXy}).
$$

Applying $\alpha$ and then normalizing by signed cyclic operations gives the second waypoint. The literal pair $E$ is ordinarily reachable at cap 27. [Preimage cyclic route](../results/round07_automorphism_preimage_route.json), [rank-three source](round-06-stable-proof.md).

Panteleev and Ushakov showed that the ordinary AK(3) orbit is invariant under ambient automorphisms. The certificate independently verifies the anchor for this transvection. Its first 160 elementary operations take AK(3) to $\alpha(\mathrm{AK}(3))$ with cyclic peak 21. Its next 613 operations transport the ordinary path to $E$ by $\alpha$. Inversion and multiplication transport directly. A single-letter conjugation becomes conjugation by the image word of length one or two and is expanded into single-letter operations. Eleven final normalizing operations give the exact marked endpoint. The ordinary replayer checks the full ledger. [Panteleev–Ushakov, Corollary 3.8](https://arxiv.org/abs/1609.00325), [anchor route](../results/round07_automorphism_anchor_route.json), [replay receipt](../results/round07_automorphism_transport.json).

The transport explains how two deletion markings can yield short endpoints with different bounded ordinary reachability. In this certificate the marking change raises the peak above the cyclic energies of both endpoints.

~~~sh
python3 -B experiments/round07_automorphism_transport.py \
  results/round07_automorphism_anchor_route.json \
  results/round07_automorphism_preimage_route.json /tmp/ac-r07-transport.json \
  | diff - results/round07_automorphism_transport.json
cmp /tmp/ac-r07-transport.json certificates/round07_automorphism_D23.json
~~~
