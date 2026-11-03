"""Explore character extensions after a second vertex identification.

Every successful voltage certificate is unbounded in word length. Failure
of extension or of the sufficient strict-cycle test is not a primitive
witness and is not an AC obstruction.
"""
import argparse
from collections import Counter
from fractions import Fraction
import json
from math import gcd,lcm
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
for directory in (HERE.parent/'research_r',HERE.parent/'research_v'):
    sys.path.insert(0,str(directory))
try:
    from v_vertex_identification import fold_identification,spanning,word_voltage
    from v_voltage_cycle_review import review
except ImportError:
    from vertex_identification import fold_identification,spanning,word_voltage
    from voltage_cycle_review import review
from primitive_map_pairs import inverse,reduce,follow,LETTERS

def affine_solutions(matrix,rhs,columns):
    rows=[[Fraction(x) for x in a]+[Fraction(b)] for a,b in zip(matrix,rhs)]
    pivot_columns=[];row=0
    for column in range(columns):
        pivot=next((i for i in range(row,len(rows)) if rows[i][column]),None)
        if pivot is None:continue
        rows[row],rows[pivot]=rows[pivot],rows[row]
        scale=rows[row][column];rows[row]=[x/scale for x in rows[row]]
        for i in range(len(rows)):
            if i!=row and rows[i][column]:
                scale=rows[i][column];rows[i]=[a-scale*b for a,b in zip(rows[i],rows[row])]
        pivot_columns.append(column);row+=1
    if any(not any(r[:columns]) and r[-1] for r in rows):return None
    free=[i for i in range(columns) if i not in pivot_columns]
    base=[Fraction(0)]*columns
    for i,column in enumerate(pivot_columns):base[column]=rows[i][-1]
    directions=[]
    for column in free:
        v=[Fraction(0)]*columns;v[column]=1
        for i,pivot in enumerate(pivot_columns):v[pivot]=-rows[i][column]
        directions.append(v)
    return base,directions

def literal_basis(graph):
    paths,extra,arc,coords=spanning(graph)
    words=[reduce(paths[a]+LETTERS[c]+inverse(paths[b])) for a,c,b in extra]
    return paths,extra,arc,coords,words

def make_voltage(graph,arc,character):
    denominator=lcm(*(x.denominator for x in character))
    coefficients=[int(x*denominator) for x in character]
    divisor=gcd(*coefficients)
    if divisor:coefficients=[x//divisor for x in coefficients]
    voltage=[0]*len(graph)
    for (a,c,b),(i,sign) in arc.items():voltage[4*a+c]=sign*coefficients[i]
    return voltage,coefficients

def main(data,parameter_cap=5):
    results=[];counts=Counter()
    for first_index,parent in enumerate(data['records']):
        old=tuple(parent['graph']);old_voltage=parent['edge_voltages']
        paths,extra,old_arc,old_coords,basis=literal_basis(old)
        assert len(basis)==3
        old_character=[word_voltage(old,old_voltage,w,0) for w in basis]
        for a in range(len(old)//4):
            for b in range(a+1,len(old)//4):
                graph,projection=fold_identification(old,a,b)
                _,chords,arc,coords,_=literal_basis(graph)
                equations=[coords(w) for w in basis]
                affine=affine_solutions(equations,old_character,len(chords))
                record={'first_case_index':first_index,'first_vertices':parent['identified_vertices'],
                    'second_vertices':[a,b],'graph':list(graph),'rank':len(chords),
                    'vertex_projection':projection,'old_basis_words':basis,
                    'old_character':old_character,'coordinate_rows':equations}
                if affine is None:
                    record['status']='NO_CHARACTER_EXTENSION';counts[record['status']]+=1;results.append(record);continue
                base,directions=affine
                record['extension_free_dimension']=len(directions)
                record['rational_particular']=[str(x) for x in base]
                record['rational_directions']=[[str(x) for x in v] for v in directions]
                if len(directions)>1:
                    record['status']='UNSEARCHED_MULTIPARAMETER';counts[record['status']]+=1;results.append(record);continue
                parameters=[0] if not directions else list(range(-parameter_cap,parameter_cap+1))
                successes=[];tried=[]
                for parameter in parameters:
                    character=[x+(parameter*directions[0][i] if directions else 0) for i,x in enumerate(base)]
                    if not any(character):continue
                    voltage,coefficients=make_voltage(graph,arc,character)
                    pulled=[word_voltage(graph,voltage,w,0) for w in basis]
                    ratios={Fraction(x,y) for x,y in zip(pulled,old_character) if y}
                    assert len(ratios)==1 and next(iter(ratios))!=0
                    scale=next(iter(ratios));assert all(Fraction(x)==scale*y for x,y in zip(pulled,old_character))
                    certificate=review(graph,voltage);tried.append({'parameter':parameter,'status':certificate['status']})
                    if certificate['status']=='PASS':
                        successes.append({'parameter':parameter,'character':coefficients,
                                          'edge_voltages':voltage,'pullback_scale':str(scale),
                                          'cycle_certificate':certificate});break
                record['parameters_tested']=tried
                if successes:
                    record['status']='CERTIFIED_EXTENSION_KERNEL';record['certificate']=successes[0]
                else:record['status']='EXTENSION_TEST_UNRESOLVED'
                counts[record['status']]+=1;results.append(record)
    return {'status':'COMPLETE_SPECIFIED_PARAMETER_TEST','ordinary_AC_goal_solved':False,
            'first_kernel_cases':len(data['records']),'second_identifications':len(results),
            'parameter_cap':parameter_cap,'counts':dict(counts),
            'scope':'Only successful certificates exclude primitive loops unboundedly; all failures unresolved.',
            'records':results}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('input');parser.add_argument('--parameter-cap',type=int,default=5);parser.add_argument('--output',required=True)
    args=parser.parse_args();result=main(json.loads(Path(args.input).read_text()),args.parameter_cap)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
