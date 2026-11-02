"""Exact primitive-in-subgroup decisions for selected heuristic endpoints.

This does not cover all stored search nodes or all ordinary AC paths.
The selected pairs come from random_cyclic_escape.cpp's elite reservoir.
"""
import argparse
import json
from pathlib import Path
from primitive_map_pairs import fold, decide


def audit(path,budget):
    records=json.loads(Path(path).read_text())
    cache={}
    outcomes=[]
    for row in records:
        encoded=fold(row['words'])
        if encoded not in cache:
            cache[encoded]=decide(encoded,budget)
        decision=cache[encoded]
        outcome={k:row[k] for k in ('seed','node','words')}
        outcome.update(status=decision['status'],vertices=decision['vertices'],
                       map_pair_states=sum(a['pair_states_discovered'] for a in decision['alphabets']))
        if decision['status']=='PRIMITIVE':
            outcome['witness']=decision['witness']
        outcomes.append(outcome)
        if decision['status']=='PRIMITIVE':
            break
    result={'status':'SELECTED_ENDPOINT_AUDIT','ordinary_AC_goal_solved':False,
            'selected_pairs':len(records),'selected_pairs_processed':len(outcomes),
            'distinct_based_graphs_decided':len(cache),
            'primitive_subgroups_found':sum(r['status']=='PRIMITIVE' for r in outcomes),
            'incomplete_selected_decisions':sum(r['status']=='INCOMPLETE' for r in outcomes),
            'scope':'Selected heuristic endpoint subgroups only; no global obstruction',
            'outcomes':outcomes}
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('pairs')
    parser.add_argument('--budget',type=int,default=100000)
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    result=audit(args.pairs,args.budget)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='outcomes'},indent=2))
