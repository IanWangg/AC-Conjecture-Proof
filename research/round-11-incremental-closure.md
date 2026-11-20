# Independent closure for a one-unit cyclic extension

2026-11-19. The full cap-32 expansion uses the independently checked cap-31 component and the complete cap-32 first-exit boundary. An independent stack-reduction verifier now accepts the lower catalogue and the outside catalogue separately. The full expansion, boundary audit and independent closure are separate jobs. [Round 10 frontier construction](round-10-ak3.md), [incremental checker](../experiments/round07_ak3_wide_verify.cpp).

The verifier reads both catalogues, checks that every row is a distinct canonical orbit, and requires the lower rows to have energy at most one less than the new cap. It assumes the verified lower component is connected and identifies its nodes for connectivity checking. For every outside row it independently checks the whole cyclic product menu and its membership in the union, using stack reduction and distinct word arithmetic from the extension generator. It then checks that each outside orbit is connected to the lower component. Together with exactness of the lower component and completeness of its first exits, this proves the union is precisely the new component. The primitive-coordinate test is a separate scan of the outside catalogue.

At cap 22 the checker independently confirms closure and attachment for 14,245 new signed orbits over 18,118 verified lower orbits, using 11,215,112 product candidates. Removing the first outside row causes the closure check to fail. The usual complete mode also still verifies the cap-21 input. [Small positive and negative controls](../results/round11_incremental_closure_controls.json).

~~~sh
work=/tmp/ac-r11-closure
mkdir -p "$work"
c++ -std=c++17 -O3 -pthread experiments/round07_ak3_wide_verify.cpp -o "$work/wide-verify"
"$work/wide-verify" --extend 32 16 "$lower31" "$outside32" "$work/c32.closure.json"
python3 -B experiments/round05_ak3_orbit_audit.py primitive "$outside32"
~~~
