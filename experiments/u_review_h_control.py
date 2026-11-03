"""Independent elementary replay and native refold of a coupled-H control.

The pure-word replay below imports no root/T/M/R elementary-move code.
It accepts only the repository's three strict ordinary AC primitives.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from u_verify_native import inverse,reduce,verify_positive


def strict_replay(record):
    assert record['format']=='ordinary-ac-elementary-v1'
    assert isinstance(record['start'],list) and len(record['start'])==2
    assert isinstance(record['target'],list) and len(record['target'])==2
    state=[reduce(w) for w in record['start']]
    peak=sum(map(len,state));counts={'invert':0,'multiply':0,'conjugate':0}
    for move in record['moves']:
        i=move['i'];assert type(i)==int and i in (0,1)
        op=move['op'];counts[op]+=1
        if op=='invert':
            assert set(move)=={'op','i'}
            state[i]=inverse(state[i])
        elif op=='multiply':
            assert set(move)=={'op','i','j'}
            j=move['j'];assert type(j)==int and j in (0,1) and j!=i
            state[i]=reduce(state[i]+state[j])
        elif op=='conjugate':
            assert set(move)=={'op','i','g'}
            g=move['g'];assert isinstance(g,str) and len(g)==1 and g in 'xXyY'
            state[i]=reduce(g+state[i]+inverse(g))
        else:raise AssertionError('unknown elementary move')
        peak=max(peak,sum(map(len,state)))
    assert state==[reduce(w) for w in record['target']]
    return {'moves':len(record['moves']),'peak_total_length':peak,'endpoint':state,'move_counts':counts}


def checked_file(path):
    raw=Path(path).read_bytes()
    return {'filename':Path(path).name,'sha256':hashlib.sha256(raw).hexdigest()}


def run(prefix,binary,engine,repository_root=None):
    if repository_root:
        root=Path(repository_root);certificate_root=root/'certificates'
        paths=[certificate_root/('coupled_ak2_'+name+'.json') for name in ('strict','exposed','full')]
        hit_path=certificate_root/'coupled_ak2_primitive_hit.json'
        path_path=certificate_root/'coupled_ak2_phase_path.json'
        results_path=root/'results'/'coupled_ak2_control_results.json'
        engine=engine or root/'experiments'/'coupled_h_search.cpp'
    else:
        assert prefix and engine
        paths=[Path(str(prefix)+suffix) for suffix in ('_strict.json','_exposed.json','_full.json')]
        hit_path=Path(str(prefix)+'.hit.json');path_path=Path(str(prefix)+'.path.json')
        results_path=Path(str(prefix)+'.results.json')
    certificates=[json.loads(path.read_text()) for path in paths]
    replayed=[strict_replay(row) for row in certificates]
    for row in certificates:assert row['start']==['xxYYY','xyxYXY']
    for left,right in zip(certificates,certificates[1:]):
        assert right['moves'][:len(left['moves'])]==left['moves']
    assert replayed[-1]['endpoint']==['x','y']
    hit=json.loads(hit_path.read_text());phase=json.loads(path_path.read_text())
    assert hit['status']=='PRIMITIVE' and phase['start']==certificates[0]['start']
    assert phase['target']==hit['pair']==replayed[0]['endpoint']
    with tempfile.TemporaryDirectory(prefix='u-native-h-control-') as directory:
        source=Path(directory)/'input.tsv';target=Path(directory)/'output.jsonl'
        source.write_text('0\t'+'\t'.join(hit['pair'])+'\t0\t'+','.join(map(str,hit['encoded_graph']))+'\n')
        native=subprocess.run([str(Path(binary).resolve()),str(source),str(target),'100000','1','0'],check=True,text=True,capture_output=True)
        record=json.loads(target.read_text());verify_positive(record)
        for key in ('alphabet','program','component','vertex','expanded','cyclic_word','based_word'):
            assert record['witness'][key]==hit[key]
        assert record['witness']['based_word'] in replayed[1]['endpoint']
    data=json.loads(results_path.read_text());search=data.get('heuristic_engine',data)
    assert search['hit']=='PRIMITIVE' and search['saved_path_stages']==len(phase['stages'])
    return {'status':'PASS','ordinary_AC_goal_solved':False,'literal_start':certificates[0]['start'],
            'AK_parameter':2,'phase_count':len(phase['stages']),'search_attempts':search['attempts'],
            'search_incomplete_graphs':search['native_incomplete'],
            'independent_strict_phase_path':replayed[0],
            'independent_strict_exposed_path':replayed[1],
            'independent_strict_complete_path':replayed[2],
            'independent_refolding_matches_recorded_hit_graph':True,
            'independently_verified_native_witness':record['witness'],
            'native_summary':json.loads(native.stdout),
            'source_files':[checked_file(p) for p in paths+[hit_path,path_path,results_path,Path(engine)]],
            'scope':'A complete AK(2) positive calibration; no AK(3) or unrestricted AC conclusion'}


if __name__=='__main__':
    parser=argparse.ArgumentParser();group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--prefix');group.add_argument('--repository-root')
    parser.add_argument('--binary',required=True);parser.add_argument('--engine');parser.add_argument('--output',required=True)
    args=parser.parse_args()
    if args.prefix and not args.engine:parser.error('--engine is required with --prefix')
    result=run(args.prefix,args.binary,args.engine,args.repository_root)
    content=json.dumps(result,indent=2)+'\n';Path(args.output).write_text(content);print(content,end='')
