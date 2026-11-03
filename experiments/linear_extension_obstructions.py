"""Produce exact short dual certificates for failed character extension."""
import argparse
from fractions import Fraction as F
import json
from math import gcd,lcm
from pathlib import Path

def dual(matrix,rhs):
    rows=[[F(x) for x in row]+[F(b)]+[F(i==j) for j in range(len(matrix))] for i,(row,b) in enumerate(zip(matrix,rhs))]
    width=len(matrix[0]);at=0
    for column in range(width):
        pivot=next((i for i in range(at,len(rows)) if rows[i][column]),None)
        if pivot is None:continue
        rows[pivot],rows[at]=rows[at],rows[pivot]
        scale=rows[at][column];rows[at]=[x/scale for x in rows[at]]
        for i in range(len(rows)):
            if i!=at and rows[i][column]:
                scale=rows[i][column];rows[i]=[x-scale*y for x,y in zip(rows[i],rows[at])]
        at+=1
    row=next(r for r in rows if not any(r[:width]) and r[width])
    values=row[width+1:];den=lcm(*(v.denominator for v in values));values=[int(v*den) for v in values];div=gcd(*values)
    values=[v//div for v in values]
    assert all(sum(v*r[j] for v,r in zip(values,matrix))==0 for j in range(width))
    assert sum(v*b for v,b in zip(values,rhs))!=0
    return values

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('--output',required=True);args=p.parse_args()
    data=json.loads(Path(args.input).read_text());records=[]
    for index,row in enumerate(data['records']):
        if row['status']=='NO_CHARACTER_EXTENSION':
            records.append({'second_identification_index':index,'dual_integer_row':dual(row['coordinate_rows'],row['old_character'])})
    result={'status':'COMPLETE_DUAL_EXTENSION_OBSTRUCTIONS','cases':len(records),'records':records}
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(len(records),'exact dual witnesses')
