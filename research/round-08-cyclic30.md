# Complete cyclic cap-30 component of AK(3)

2026-11-19. Any ordinary AC path reaching a primitive relator from AK(3), including any ordinary trivialization, has cyclic total-length peak at least **31**.

The complete cap-30 orbit generator and independent stack-reduction closure checker agree on 73,876,424 signed ambient orbits, 78,886,780,816 candidate products and 4,543,003,748 admitted neighbor checks. The checker verifies connectivity from the original AK(3) orbit. The independent Euclidean screen checks both cyclic coordinates in every orbit and compares the 18,450,241 single-sign occurrences against the exact primitive classes. It finds zero primitive coordinates. The minimum length of a coordinate is five. [Independent reports and catalogue digest](../results/round08_cyclic30.json).

The orbit quotient uses the eight signed permutations of the free basis. Equivariance ensures that every projected path in the original graph stays in the checked orbit component, and every node lifts to a reachable marking. The [cap-22 signed symmetry control](round-05-ak3.md) also has every signed image of the starting tuple within the original component. This permits expansion from each orbit to all its signed markings. Complete cyclic products include every admissible relative bridge by the [Cayley-tree product argument](research-n-cyclic-search.md).

The [round-seven constructive and archive tests](round-07-ak3.md) used this same catalogue. They certify the exact cap-30 entrance to the second stable waypoint and exclude arbitrary-tail subgroup joins against 23,902 known-trivial archive pairs. The cap-30 component exclusion concerns the entire bounded graph. The archive comparison is an additional restriction on possible higher-peak continuations.

~~~sh
mkdir -p /tmp/ac-r08-cyclic
c++ -std=c++17 -O3 -pthread experiments/round07_ak3_wide_orbits.cpp \
  -o /tmp/ac-r08-cyclic/wide-orbits
c++ -std=c++17 -O3 -pthread experiments/round07_ak3_wide_verify.cpp \
  -o /tmp/ac-r08-cyclic/wide-verify
/tmp/ac-r08-cyclic/wide-orbits 30 8 /tmp/ac-r08-cyclic/c30
/tmp/ac-r08-cyclic/wide-verify 30 12 /tmp/ac-r08-cyclic/c30.orbit.tsv \
  /tmp/ac-r08-cyclic/c30.verify.json
python3 -B experiments/round05_ak3_orbit_audit.py primitive /tmp/ac-r08-cyclic/c30.orbit.tsv
~~~
