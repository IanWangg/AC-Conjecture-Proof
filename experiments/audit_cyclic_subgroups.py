"""Check literal canonical subgroup graphs of an exact cyclic catalogue.

Canonical representatives only: independent conjugating tails and rotations
are NOT included unless they are explicitly supplied as separate pairs.
"""
import argparse
import hashlib
import json
from pathlib import Path
import time
import arbitrary_tail_certificate as ac
from refine_primitive_cycles import refine,primitive_cyclic_word
from balanced_run_certificate import make as run_certificate,positive_controls


def run(catalogue):
    content=Path(catalogue).read_bytes()
    states=json.loads(content)
    bad=[]
    seen={}
    dag_graphs=0
    simple_graphs=0
    balanced_graphs=0
    refinements=[]
    start=time.monotonic()
    for pair in states:
        encoded=ac.fold(pair)
        if encoded in seen:continue
        seen[encoded]=pair
        try:
            ac.orders(encoded)
            dag_graphs+=1
        except AssertionError:
            proof=refine(encoded)
            if proof['primitive_simple_cycles']:
                bad.append({'pair':pair,'encoded':encoded,'refinement':proof})
            elif not proof['branching_components']:
                simple_graphs+=1
                refinements.append({'pair':pair,'encoded':encoded,'refinement':proof})
            else:
                branches={(part['alphabet'],part['blocked'])
                          for part in proof['branching_components']}
                runs=[run_certificate(encoded,alphabet,blocked)
                      for alphabet,blocked in sorted(branches)]
                if all(runs):
                    balanced_graphs+=1
                    refinements.append({'pair':pair,'encoded':encoded,
                                        'refinement':proof,'balanced_run_proofs':runs})
                else:bad.append({'pair':pair,'encoded':encoded,'refinement':proof})
    words=sorted({word for pair in states for word in pair})
    primitive_coordinates=[word for word in words if primitive_cyclic_word(word)]
    return {'states':len(states),'distinct_based_graphs':len(seen),
            'catalogue_sha256':hashlib.sha256(content).hexdigest(),
            'inconclusive_graphs':bad,'seconds':time.monotonic()-start,
            'direct_DAG_graphs':dag_graphs,'simple_cycle_refined_graphs':simple_graphs,
            'balanced_run_refined_graphs':balanced_graphs,'refinement_proofs':refinements,
            'distinct_cyclic_coordinate_orbits':len(words),
            'primitive_coordinates_Nielsen_Euclidean_test':primitive_coordinates,
            'balanced_run_positive_controls':positive_controls(),
            'ordinary_AC_goal_solved':False,
            'scope':'Literal canonical pairs only; arbitrary independent conjugating tails excluded'}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('catalogue')
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    result=run(args.catalogue)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('inconclusive_graphs','refinement_proofs')},indent=2))
    print('inconclusive',len(result['inconclusive_graphs']))
    print([row['pair'] for row in result['inconclusive_graphs'][:10]])
