# Complete cyclic cap-25 component of AK(3)

2026-11-19. Any ordinary AC path from AK(3) to a primitive relator, and in particular any ordinary trivialization, must reach cyclic total relator length at least 26.

The round-one generator exhausts the cap-25 component. The independent checker verifies closure using the complete cyclic product menu, including all signed rotations and all nonempty bridge cases needed for disjoint axes. It then verifies connectedness from the original AK(3) class. The round-two verifier partitions the candidate scans across workers, with one adjacency table and a shared read-only catalogue. Its word arithmetic and distinct closure check are unchanged. [Completeness of the cyclic menu](research-n-cyclic-search.md), [independent cap-22 audit](research-p-cyclic21-review.md), [round-one extension](round-01-ak3.md).

| Check | Count |
| --- | ---: |
| Canonical states | 5,562,224 |
| Candidate products | 5,036,287,488 |
| Admitted neighbour checks | 268,363,560 |
| Nonempty-bridge product checks | 4,994,816 |
| Maximum required bridge length | 3 |
| Distinct signed cyclic coordinate classes | 4,542,536 |
| Primitive coordinate classes | 0 |

The minimum cyclic energy in this component is 13 and the minimum cyclic coordinate length is five. The coordinate test uses the exact Euclidean representative of each primitive class in rank two. It independently compares all 4,542,536 displayed classes and includes 3,208 positive signed-rotation controls. The exclusion is about a primitive coordinate in the cap-25 component. An unrestricted path can leave that component.

Run from the repository root. The optional worker count in the verifier can be lowered on machines with less memory. The verifier reconstructs every admissible edge of the generated catalogue. The report script checks that the counts agree and records the catalogue hashes.

~~~sh
mkdir -p /tmp/ac-r02-component
c++ -std=c++17 -O3 experiments/round01_ak3_cyclic_component.cpp -o /tmp/ac-r02-component/build
c++ -std=c++17 -O3 -pthread experiments/verify_full_cyclic_component.cpp -o /tmp/ac-r02-component/check
/tmp/ac-r02-component/build 25 /tmp/ac-r02-component/c25.json /tmp/ac-r02-component/c25_build.json
python3 -B experiments/cyclic_catalogue_to_tsv.py /tmp/ac-r02-component/c25.json /tmp/ac-r02-component/c25.tsv
/tmp/ac-r02-component/check /tmp/ac-r02-component/c25.tsv 25 /tmp/ac-r02-component/c25_verify.json 16
python3 -B experiments/euclidean_primitive_audit.py /tmp/ac-r02-component/c25.json --output /tmp/ac-r02-component/c25_prim.json
python3 -B experiments/round01_ak3_component_report.py /tmp/ac-r02-component 25 --output /tmp/ac-r02-component/results.json
diff results/round02_cyclic25.json /tmp/ac-r02-component/results.json
~~~

[Result and catalogue hashes](../results/round02_cyclic25.json).
