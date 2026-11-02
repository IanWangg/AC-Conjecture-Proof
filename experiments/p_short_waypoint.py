"""Compile an exact AK(3) path to a cyclic-total-length fourteen tuple."""
import argparse
import json
from pathlib import Path
from arbitrary_tail_catalogue import reduce, inverse, run, folded_graph, passes
from elementary_verify import replay

U1='yXYXyxx'
U2='YxYXyyx'
R='XXyxYxxY'
G='XYxx'


def compile_waypoint(source):
    certificate=json.loads(Path(source).read_text())
    assert certificate['start']==['xxxYYYY','xyxYXY']
    assert certificate['target']==[U1,R]
    replay(certificate)
    certificate={key:certificate[key] for key in ('format','start','target','moves')}
    assert reduce(G+R+U1+inverse(G))==U2
    extension=[{'op':'multiply','i':1,'j':0}]
    extension += [{'op':'conjugate','i':1,'g':letter} for letter in reversed(G)]
    certificate['moves'] += extension
    certificate['target']=[U1,U2]
    certificate['scope']='P length14 waypoint from M u1/r; no free basis'
    audit=replay(certificate)
    assert audit['moves']==227 and audit['peak_total_length']==31
    graph_audit=run(U1,U2)
    assert not graph_audit['signed_criterion_failures']
    assert graph_audit['tail_bound']==6 and graph_audit['tails_tested']==1457
    assert all(passes(folded_graph(u,u,'')) for u in (U1,U2))
    graph=folded_graph(U1,U2,'')
    vertices=len(graph)//4
    rank=sum(e>=0 for e in graph)//2-vertices+1
    assert (vertices,rank)==(12,2)
    return certificate, {'status':'PASS','ordinary_AC_goal_solved':False,
                         'strict_replay':audit,'extra_strict_moves':len(extension),
                         'endpoint_raw_and_cyclic_total_length':14,
                         'endpoint_folded_graph_vertices':vertices,
                         'endpoint_folded_graph_rank':rank,
                         'arbitrary_tail_subgroup_audit':graph_audit,
                         'arbitrary_independent_conjugates_primitive_free_by_bridge_lemma':True,
                         'scope':'Genuine reachable free-group tuple; not a free basis or global AC invariant'}


def compile_low_peak(source):
    """Root's improvement of P's identity, using M's shorter u2 entry."""
    certificate=json.loads(Path(source).read_text())
    assert certificate['start']==['xxxYYYY','xyxYXY']
    assert certificate['target']==[U2,R]
    replay(certificate)
    certificate={key:certificate[key] for key in ('format','start','target','moves')}
    # g^-1 u2 g = r u1. Conjugate u2, then use r^-1 to obtain u1.
    certificate['moves'] += [{'op':'conjugate','i':0,'g':c} for c in reversed(inverse(G))]
    certificate['moves'] += [{'op':'invert','i':1},{'op':'multiply','i':1,'j':0}]
    certificate['moves'] += [{'op':'conjugate','i':0,'g':c} for c in reversed(G)]
    certificate['target']=[U2,U1]
    certificate['scope']='P length14 waypoint, root improved path from M u2/r; no free basis'
    audit=replay(certificate)
    assert audit['moves']==189 and audit['peak_total_length']==25
    return certificate,audit


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--u1-certificate',required=True)
    parser.add_argument('--u2-certificate',required=True)
    parser.add_argument('--certificate',required=True)
    parser.add_argument('--low-peak-certificate',required=True)
    parser.add_argument('--result',required=True)
    args=parser.parse_args()
    certificate,result=compile_waypoint(args.u1_certificate)
    low_peak,low_audit=compile_low_peak(args.u2_certificate)
    result['preferred_root_improvement_strict_replay']=low_audit
    result['preferred_extra_strict_moves']=10
    Path(args.certificate).write_text(json.dumps(certificate,indent=2)+'\n')
    Path(args.low_peak_certificate).write_text(json.dumps(low_peak,indent=2)+'\n')
    Path(args.result).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
