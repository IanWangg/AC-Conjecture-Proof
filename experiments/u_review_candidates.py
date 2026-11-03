"""Refold and independently certify every native decision on a Q/V corpus.

Optional comparison with R's already published compact closed-map certificate
checks equality of the entire reachable pair sets, not merely their sizes.
No R detector or folding implementation is imported.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from u_candidate_adapter import adapt
from u_verify_native import verify_absence,verify_positive


def compare_compact(native,prior):
    cert=prior['certificate'];assert cert['status']==native['status']=='ABSENT'
    assert cert['encoded_graph']==native['graph']
    n=native['vertices'];maps=[]
    for sparse in cert['partial_maps_as_sparse_pairs']:
        values=[n]*(n+1)
        for start,end in sparse:values[start]=end
        maps.append(tuple(values))
    assert len(cert['alphabets'])==len(native['alphabets'])==4
    for a,b in zip(cert['alphabets'],native['alphabets']):
        assert a['alphabet']==b['alphabet']
        previous={maps[i]+maps[j] for i,j in a['closed_map_pair_indices']}
        assert previous=={tuple(pair) for pair in b['closed_total_map_pairs']}


def run(source,binary,r_certificates=None):
    counts={'ABSENT':0,'PRIMITIVE':0,'INCOMPLETE':0};closed=0;compared=0;maximum=0
    with tempfile.TemporaryDirectory(prefix='u-native-candidate-review-') as directory:
        tsv=Path(directory)/'input.tsv';out=Path(directory)/'output.jsonl'
        provenance=adapt(source,tsv)
        batch=subprocess.run([str(Path(binary).resolve()),str(tsv),str(out),'100000','1','0'],check=True,text=True,capture_output=True)
        summary=json.loads(batch.stdout)
        reference=Path(r_certificates).open() if r_certificates else None
        try:
            with out.open() as stream:
                for index,line in enumerate(stream):
                    native=json.loads(line);assert native['id']==str(index)
                    counts[native['status']]+=1
                    maximum=max(maximum,*(a['discovered'] for a in native['alphabets']))
                    if native['status']=='ABSENT':closed+=verify_absence(native)
                    elif native['status']=='PRIMITIVE':verify_positive(native)
                    if reference:
                        prior=json.loads(next(reference));assert prior['candidate_index']==index
                        compare_compact(native,prior);compared+=1
            if reference:assert next(reference,None) is None
        finally:
            if reference:reference.close()
        assert sum(counts.values())==provenance['records']==summary['records']
        assert all(counts[k]==summary[k] for k in counts)
        return {'status':'PASS','ordinary_AC_goal_solved':False,**provenance,
                'complete_decision_counts':counts,
                'independent_input_refolding_matches_expected_graph':True,
                'closed_total_map_pairs_independently_checked':closed,
                'entire_closed_pair_sets_equal_R_compact_certificates':compared,
                'maximum_one_alphabet':maximum,'native_summary':summary}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('source');parser.add_argument('--binary',required=True)
    parser.add_argument('--R-certificates');parser.add_argument('--output',required=True)
    args=parser.parse_args();result=run(args.source,args.binary,args.R_certificates)
    content=json.dumps(result,indent=2)+'\n';Path(args.output).write_text(content);print(content,end='')
