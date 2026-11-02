"""Replay O's exceptional subgroup proofs with M's independent folding.

The SCC/run criteria are shared with O, not independent implementations.
This checks the difficult exceptional records, not every direct-DAG graph.
"""
import argparse
import base64
import gzip
import json
from pathlib import Path
from stallings_search import graph
from refine_primitive_cycles import refine
from balanced_run_certificate import verify, positive_controls


def audit(path):
    raw = Path(path).read_bytes()
    if str(path).endswith('.gz.b64'):
        raw = gzip.decompress(base64.b64decode(raw))
    report = json.loads(raw)
    assert report['inconclusive_graphs'] == []
    simple = balanced = 0
    for row in report['refinement_proofs']:
        encoded = tuple(row['encoded'])
        assert graph(tuple(row['pair']))[0] == encoded
        proof = refine(encoded)
        assert proof == row['refinement']
        assert proof['primitive_simple_cycles'] == []
        if proof['branching_components']:
            certificates = row['balanced_run_proofs']
            expected = {(item['alphabet'],item['blocked']) for item in proof['branching_components']}
            actual = {(item['alphabet'],item['isolated_letter']) for item in certificates}
            assert expected == actual
            for certificate in certificates:
                assert verify(encoded,certificate)
            balanced += 1
        else:
            simple += 1
    assert simple == report['simple_cycle_refined_graphs']
    assert balanced == report['balanced_run_refined_graphs']
    controls = positive_controls()
    assert controls == 364
    return dict(status='PASS', ordinary_AC_goal_solved=False,
                catalogue_sha256=report['catalogue_sha256'],
                literal_canonical_pairs=report['states'],
                exceptional_graphs_rechecked=simple+balanced,
                simple_cycle_graphs=simple, balanced_run_graphs=balanced,
                independent_folding_implementation='M versus O',
                SCC_and_run_criteria_shared_with_O=True,
                actual_primitive_control_graphs_correctly_rejected=controls,
                all_direct_DAG_graphs_recomputed_in_this_review=False,
                arbitrary_independent_conjugating_tails_covered=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('proof_data')
    parser.add_argument('--output',required=True)
    args = parser.parse_args()
    result = audit(args.proof_data)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
