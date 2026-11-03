"""Compile an actual hidden primitive subgroup witness into strict AC moves.

This glue reuses R's complete detector/spanning-tree basis bridge and M's
primitive completion. It never treats a graph match or finite quotient
as a completed AC proof: the final free-word ledger is strictly replayed.
"""
import argparse
import json
from pathlib import Path
from primitive_map_pairs import fold,decide,follow
from h_basis_bridge import spanning_basis,compile_match
from complete_primitive import primitive_aut,complete
from elementary_verify import replay


def compile_hidden(parent,budget=1000000):
    prefix=replay(parent)
    source=parent['target']
    encoded=fold(source)
    decision=decide(encoded,budget)
    if decision['status']!='PRIMITIVE':
        return None,{'status':decision['status'],'ordinary_AC_goal_solved':False,
                     'detector':decision,'prefix_replay':prefix}
    witness=decision['witness']
    if 'based_primitive_word' not in witness:
        return None,{'status':'POSITIVE_SLP_REQUIRES_EXPANSION','ordinary_AC_goal_solved':False,
                     'detector':decision,'prefix_replay':prefix}
    word=witness['based_primitive_word']
    assert follow(encoded,0,word)==0
    paths,z,rewrite,substitute=spanning_basis(encoded,0)
    formal=rewrite(word)
    assert substitute(formal)==word
    ops,forward,backward=primitive_aut(formal,0)
    target=list(map(substitute,backward))
    assert target[0]==word
    match={'status':'MATCH','canonical_unbased_graph':list(encoded),
           'forward_rotated_pair':target,'reverse_pair':source,
           'forward_original_base':0,'reverse_original_base':0}
    bridge,bridge_result=compile_match(match)
    waypoint={'format':'ordinary-ac-elementary-v1','start':parent['start'],
              'target':target,'moves':parent['moves']+bridge['moves'],
              'scope':'Actual hidden primitive exposed by strict AC basis bridge'}
    waypoint_result=replay(waypoint)
    final=complete(waypoint)
    final_result=replay(final)
    assert final['target']==['x','y']
    return final,{'status':'PASS','ordinary_AC_goal_solved':False,
                  'detector_witness':witness,'spanning_tree_basis_words':z,
                  'formal_hidden_primitive':formal,
                  'formal_primitive_to_generator_derivation':ops,
                  'strict_prefix_replay':prefix,
                  'strict_hidden_primitive_bridge':bridge_result['strict_subgroup_basis_bridge'],
                  'strict_waypoint_replay':waypoint_result,
                  'strict_complete_basis_replay':final_result,
                  'actual_start':parent['start'],
                  'scope':'A complete path for the supplied start; no AK3 claim unless its literal start is AK3'}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('prefix_certificate')
    parser.add_argument('--budget',type=int,default=1000000)
    parser.add_argument('--certificate',required=True);parser.add_argument('--output',required=True)
    args=parser.parse_args();certificate,result=compile_hidden(json.loads(Path(args.prefix_certificate).read_text()),args.budget)
    if certificate:Path(args.certificate).write_text(json.dumps(certificate,indent=2)+'\n')
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
