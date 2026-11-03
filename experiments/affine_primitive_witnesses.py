"""Explicit primitive loops killed by every character in an affine family.

This is a bounded search for positive witnesses. Absence of a witness in
the menu proves nothing; each returned word is checked independently.
These kernels are coarse overgroups, not actual reachable rank-two pairs.
"""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
for directory in (HERE.parent/'research_v',HERE.parent/'research_r',HERE.parent/'research_m'):sys.path.insert(0,str(directory))
try:
    from v_vertex_identification import spanning,positive_primitive_words,word_voltage
except ImportError:
    from vertex_identification import spanning,positive_primitive_words,word_voltage
from primitive_map_pairs import inverse,reduce,follow
from stallings_search import primitive

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('extensions');p.add_argument('intervals');p.add_argument('--cap',type=int,default=40);p.add_argument('--output',required=True);args=p.parse_args()
    ext=json.loads(Path(args.extensions).read_text());intervals=json.loads(Path(args.intervals).read_text())
    words=sorted(positive_primitive_words(args.cap),key=lambda w:(len(w),w));results=[];found=0
    for row in intervals['records']:
        if row['status']!='STRICT_CYCLE_FAMILY_INFEASIBLE':continue
        index=row['second_identification_index'];source=ext['records'][index];graph=source['graph']
        base=list(map(F,source['rational_particular']));direction=list(map(F,source['rational_directions'][0]))
        routes,_,arc,_=spanning(graph);v0=[F(0)]*len(graph);v1=[F(0)]*len(graph)
        for (a,c,b),(i,s) in arc.items():v0[4*a+c]=s*base[i];v1[4*a+c]=s*direction[i]
        witness=None
        for positive in words:
            for alphabet in ('xy','xY','Xy','XY'):
                word=positive.translate(str.maketrans('xy',alphabet))
                for vertex in range(len(graph)//4):
                    if word_voltage(graph,v0,word,vertex)==word_voltage(graph,v1,word,vertex)==0:
                        based=reduce(routes[vertex]+word+inverse(routes[vertex]))
                        assert follow(graph,0,based)==0 and primitive(based)
                        assert word_voltage(graph,v0,based,0)==word_voltage(graph,v1,based,0)==0
                        witness={'cyclic_word':word,'loop_vertex':vertex,'base_path':routes[vertex],
                                 'based_word':based,'affine_voltage_coefficients':[0,0]};break
                if witness:break
            if witness:break
        found+=bool(witness)
        results.append({'second_identification_index':index,'first_case_index':source['first_case_index'],
                        'second_vertices':source['second_vertices'],'witness':witness})
    result={'status':'COMPLETE_SPECIFIED_POSITIVE_MENU','ordinary_AC_goal_solved':False,
            'primitive_length_menu_cap':args.cap,'positive_source_words':len(words),
            'infeasible_cases':len(results),'cases_with_uniform_affine_primitive':found,
            'cases_without_found_witness':len(results)-found,
            'scope':'Every explicit witness is conclusive for the coarse extension kernels; no absent witness or actual AC claim.',
            'records':results}
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
