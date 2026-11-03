"""Construct a strict completion from a hidden ambient primitive in rank2 H.

The parent ledger supplies actual ordinary reachability.  Graph rewriting
and a formal basis bridge expose the primitive without guessing an
expression in the original two relators. No implicit generator moves.
"""
import argparse
import json
from pathlib import Path
from primitive_map_pairs import fold,follow,reduce
from h_basis_bridge import spanning_basis,compile_match
from complete_primitive import primitive_aut,complete
from stallings_search import primitive
from elementary_verify import replay


def expose(parent,word):
    replay(parent)
    state=parent['target']
    word=reduce(word)
    assert primitive(word), 'supplied witness must be ambient primitive'
    graph=fold(state)
    assert follow(graph,0,word)==0, 'witness is not in the actual based subgroup'
    paths,basis,rewrite,substitute=spanning_basis(graph,0)
    formal= rewrite(word)
    assert substitute(formal)==word
    assert primitive(formal), 'ambient primitive must be primitive in H'
    _,_,backward=primitive_aut(formal,0)
    assert backward[0]==formal
    target=[substitute(w) for w in backward]
    assert target[0]==word
    match={'status':'MATCH','canonical_unbased_graph':list(graph),
           'forward_rotated_pair':target,'reverse_pair':state,
           'forward_original_base':0,'reverse_original_base':0}
    bridge,bridge_result=compile_match(match)
    assert bridge['start']==state and bridge['target']==target
    result={'format':'ordinary-ac-elementary-v1','start':parent['start'],
            'target':target,'moves':parent['moves']+bridge['moves'],
            'scope':'Exact hidden-primitive exposure; target is not yet standard basis'}
    check=replay(result)
    details={'status':'PASS','ordinary_AC_goal_solved':False,
             'ambient_primitive_word':word,'formal_witness_in_tree_basis':formal,
             'tree_basis_words':basis,'formal_complement':backward[1],
             'actual_complement':target[1],
             'parent_strict_moves':len(parent['moves']),
             'exposure_bridge_strict_moves':len(bridge['moves']),
             'waypoint_replay':check}
    return result,details


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('parent');parser.add_argument('witness')
    parser.add_argument('--waypoint',required=True)
    parser.add_argument('--completion',required=True)
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    waypoint,result=expose(json.loads(Path(args.parent).read_text()),args.witness)
    finished=complete(waypoint)
    result['full_replay']=replay(finished)
    assert result['full_replay']['endpoint']==['x','y']
    Path(args.waypoint).write_text(json.dumps(waypoint,indent=2)+'\n')
    Path(args.completion).write_text(json.dumps(finished,indent=2)+'\n')
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
