"""Expand a saved ordinary word-operation ledger into strict AC moves."""
import argparse
import json
from pathlib import Path
import first_order_correction as f


def expand(cert):
    moves=[]
    for move in cert['moves']:
        i=move['i']
        if move['op']=='conjugate':
            g=move.get('word',move.get('g'))
            moves.extend({'op':'conjugate','i':i,'g':c} for c in reversed(g))
        elif move['op']=='multiply' and move.get('sign',1)<0:
            moves.extend([{'op':'invert','i':move['j']},
                          {'op':'multiply','i':i,'j':move['j']},
                          {'op':'invert','i':move['j']}])
        else:moves.append({k:v for k,v in move.items() if k!='sign'})
    return {'format':'ordinary-ac-elementary-v1',
            'scope':'Actual free-word expansion; target is exactly the saved free target',
            'start':cert['start'],'target':cert['target'],'moves':moves}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('certificate')
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    output=expand(f.load(args.certificate))
    Path(args.output).write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'strict_moves':len(output['moves']),'target_lengths':list(map(len,output['target']))}))
