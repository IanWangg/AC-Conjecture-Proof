"""Positive, negative and cross-implementation controls for U's native engine."""
import argparse
import copy
import importlib
import json
from math import gcd
from pathlib import Path
import subprocess
import sys
import tempfile
from u_verify_native import follow,reduce,verify_absence,verify_positive


def mechanical(a,b):
    assert gcd(a,b)==1
    n=a+b
    return ''.join('x' if (i+1)*a//n>i*a//n else 'y' for i in range(n))


def inverse(w):return w.swapcase()[::-1]


def tails(cap):
    level=[''];yield ''
    for _ in range(cap):
        level=[w+c for w in level for c in 'xXyY' if not w or w[-1]!=c.swapcase()]
        yield from level


def corpus():
    records=[]
    for a in range(13):
        for b in range(13):
            if gcd(a,b)!=1:continue
            w=mechanical(a,b)
            for alphabet in ('xy','xY','Xy','XY'):
                v=w.translate(str.maketrans({'x':alphabet[0],'y':alphabet[1]}))
                records.append({'kind':'primitive_cycle','words':[v,v],'expected':'PRIMITIVE','rank2':False})
                records.append({'kind':'proper_square_cycle','words':[v+v,v+v],'expected':'ABSENT','rank2':False})
    for q in tails(6):records.append({'kind':'AK3_relative_tail','words':['xxxYYYY',q+'xyxYXY'+inverse(q)],'expected':'ABSENT','rank2':True})
    records +=[
        {'kind':'standard_basis','words':['x','y'],'expected':'PRIMITIVE','rank2':True},
        {'kind':'conjugated_basis','words':['Yxy','y'],'expected':'PRIMITIVE','rank2':True},
        {'kind':'AK2_phase','words':['XXyyy','YXyyXyx'],'expected':'PRIMITIVE','rank2':True},
        {'kind':'branching_negative','words':['XYxYxY','XyyXyyXyyyyyy'],'expected':'ABSENT','rank2':True}]
    return records


def run(binary,reference_directory=None,examples_directory=None):
    records=corpus();reference_fold=reference_decide=old_fold=None
    if reference_directory:
        sys.path.insert(0,str(Path(reference_directory).resolve()))
        reference=importlib.import_module('primitive_map_pairs')
        reference_fold,reference_decide=reference.fold,reference.decide
        old_fold=importlib.import_module('stallings_search').graph
    counts={};total_closed=0;reference_comparisons=old_fold_comparisons=0;examples={}
    with tempfile.TemporaryDirectory(prefix='u-native-controls-') as directory:
        source=Path(directory)/'input.tsv';output=Path(directory)/'output.jsonl'
        source.write_text(''.join(f'{i}\t{row["words"][0]}\t{row["words"][1]}\n' for i,row in enumerate(records)))
        result=subprocess.run([str(Path(binary).resolve()),str(source),str(output),'100000','1','0'],check=True,text=True,capture_output=True)
        native_summary=json.loads(result.stdout)
        seen=set()
        with output.open() as stream:
            for line in stream:
                decision=json.loads(line);i=int(decision['id']);assert i not in seen;seen.add(i)
                row=records[i];assert decision['status']==row['expected']
                assert all(follow(decision['graph'],0,reduce(word))==0 for word in row['words'])
                if decision['status']=='ABSENT':total_closed+=verify_absence(decision)
                else:verify_positive(decision)
                counts[row['kind']]=counts.get(row['kind'],0)+1
                if row['kind'] in ('AK2_phase','branching_negative') or (row['kind']=='AK3_relative_tail' and row['words'][1]=='xyxYXY'):
                    examples[row['kind']]=decision
                if reference_directory:
                    encoded=reference_fold(row['words']);assert tuple(decision['graph'])==encoded
                    prior=reference_decide(encoded,100000)
                    assert prior['status']==decision['status']
                    assert sum(a['pair_states_discovered'] for a in prior['alphabets'])==decision['pair_states']
                    assert [(a['alphabet'],a['status'],a['pair_states_discovered']) for a in prior['alphabets']]==[(a['alphabet'],a['status'],a['discovered']) for a in decision['alphabets']]
                    reference_comparisons+=1
                    if row['rank2']:
                        assert old_fold(tuple(row['words']))[0]==encoded;old_fold_comparisons+=1
        assert seen==set(range(len(records)))
        budget_input=Path(directory)/'budget.tsv';budget_output=Path(directory)/'budget.jsonl'
        budget_input.write_text('0\txx\txx\n')
        subprocess.run([str(Path(binary).resolve()),str(budget_input),str(budget_output),'1','0','0'],check=True,capture_output=True)
        assert json.loads(budget_output.read_text())['status']=='INCOMPLETE'
        # Exercise the integer-map implementation beyond R's byte-map limit.
        wide_input=Path(directory)/'wide.tsv';wide_output=Path(directory)/'wide.jsonl'
        primitive='x'*256+'y';power='x'*300
        wide_input.write_text(f'0\t{primitive}\t{primitive}\n1\t{power}\t{power}\n')
        subprocess.run([str(Path(binary).resolve()),str(wide_input),str(wide_output),'100000','1','0'],check=True,capture_output=True)
        wide=[json.loads(line) for line in wide_output.read_text().splitlines()]
        assert len(wide)==2 and [row['vertices'] for row in wide]==[257,300]
        verify_positive(wide[0]);verify_absence(wide[1])
    bad=copy.deepcopy(examples['AK3_relative_tail']);bad['alphabets'][0]['closed_total_map_pairs'].pop(0)
    try:verify_absence(bad)
    except AssertionError:pass
    else:raise AssertionError('missing initial-pair certificate accepted')
    if examples_directory:
        target=Path(examples_directory);target.mkdir(parents=True,exist_ok=True)
        for kind,decision in examples.items():(target/(kind+'.json')).write_text(json.dumps(decision,indent=2)+'\n')
    assert counts['primitive_cycle']==counts['proper_square_cycle']==372
    assert counts['AK3_relative_tail']==1457
    return {'status':'PASS','ordinary_AC_goal_solved':False,'control_records':len(records),
            'control_kinds':counts,'closed_total_map_pairs_independently_checked':total_closed,
            'R_fold_and_exact_decision_comparisons':reference_comparisons,
            'M_independent_rank2_fold_comparisons':old_fold_comparisons,
            'additional_wide_integer_map_controls':{'primitive_cycle_vertices':257,'proper_power_cycle_vertices':300,'status':'PASS'},
            'budget_stop_correctly_INCOMPLETE':True,'tampered_initial_pair_rejected':True,
            'native_summary':native_summary}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--binary',required=True);parser.add_argument('--references')
    parser.add_argument('--examples-directory');parser.add_argument('--output',required=True)
    args=parser.parse_args();result=run(args.binary,args.references,args.examples_directory)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
