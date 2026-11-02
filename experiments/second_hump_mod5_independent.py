"""Independent string-polynomial/class3-normal-form check for W=BAbb.

No imports from either finite Magnus filter. All computations overF5.
"""
from itertools import product,combinations
import argparse
import json
from pathlib import Path
P=5;D=4


def add(a,b,scale=1):
    out=dict(a)
    for w,v in b.items():
        out[w]=(out.get(w,0)+scale*v)%P
        if not out[w]:del out[w]
    return out
def mul(a,b):
    out={}
    for u,v in a.items():
        for w,z in b.items():
            if len(u+w)<=D:out[u+w]=(out.get(u+w,0)+v*z)%P
    return {w:v for w,v in out.items() if v}
def inv(a):
    out,power,v={'':1},{'':1},add(a,{'':1},-1)
    for k in range(1,D+1):power=mul(power,v);out=add(out,power,-1 if k%2 else 1)
    assert mul(a,out)=={'':1}
    return out
LETTERS={c:{'':1,c:1} for c in 'ab'}
LETTERS.update({c.upper():inv(v) for c,v in list(LETTERS.items())})
ALPHA=dict(zip('abAB',('b','aB','B','bA')))
def word(w):
    out={'':1}
    for c in w:out=mul(out,LETTERS[c])
    return out
def inverse_word(w):return w.swapcase()[::-1]
def alpha_word(w):return ''.join(ALPHA[c] for c in w)
def low(a):return {w:v for w,v in a.items() if len(w)<=3}
def comm(u,v):return inverse_word(u)+inverse_word(v)+u+v


def experiment():
    monomials=[''.join(w) for w in product('ab',repeat=4)]
    cols=[]
    for w in monomials:
        image={'':1}
        for c in w:image=mul(image,add(word(ALPHA[c]),{'':1},-1))
        diff=add({w:1},image,-1);cols.append([diff.get(m,0) for m in monomials])
    rows=[r[:] for r in cols];pivots=[];at=0
    for col in range(len(monomials)):
        choice=next((j for j in range(at,len(rows)) if rows[j][col]),None)
        if choice is None:continue
        rows[at],rows[choice]=rows[choice],rows[at]
        factor=pow(rows[at][col],-1,P);rows[at]=[v*factor%P for v in rows[at]]
        for j in range(len(rows)):
            if j!=at and rows[j][col]:
                factor=rows[j][col];rows[j]=[(u-factor*v)%P for u,v in zip(rows[j],rows[at])]
        pivots.append(col);at+=1
    free=[j for j in range(16) if j not in pivots];functionals=[]
    for j in free:
        f=[0]*16;f[j]=1
        for row,pivot in zip(rows,pivots):f[pivot]=-row[j]%P
        assert all(sum(a*b for a,b in zip(f,c))%P==0 for c in cols)
        functionals.append(f)
    c2=comm('a','b');c3a=comm('a',c2);c3b=comm('b',c2)
    checks=[]
    for k in range(P):
        s,t=(2*k+1)%P,k%P;matches=[]
        for u,v,w in product(range(P),repeat=3):
            q='a'*s+'b'*t+c2*u+c3a*v+c3b*w
            image=word(q+'BAbb'+inverse_word(alpha_word(q)));target=word('a'*k)
            if low(image)==low(target):
                defect=add(image,target,-1);assert all(len(m)==4 for m in defect)
                vector=[defect.get(m,0) for m in monomials]
                values=[sum(a*b for a,b in zip(f,vector))%P for f in functionals]
                matches.append({'conjugator_word':q,'normal_coordinates':[u,v,w],
                                'defect':defect,'quotient_functionals':values})
        assert len(matches)==1;checks.append({'k':k,**matches[0]})
    separating=None
    for support in range(1,len(functionals)+1):
        for ids in combinations(range(len(functionals)),support):
            for coefficients in product(range(1,P),repeat=support):
                values=[sum(c*row['quotient_functionals'][i] for i,c in zip(ids,coefficients))%P for row in checks]
                if all(values):
                    f=[sum(c*functionals[i][j] for i,c in zip(ids,coefficients))%P for j in range(16)];separating=f,values;break
            if separating:break
        if separating:break
    assert separating;f,values=separating
    assert all(sum(a*b for a,b in zip(f,c))%P==0 for c in cols)
    for row,value in zip(checks,values):row['separating_functional_value']=value
    return {'status':'PASS','method':'independent string polynomials + class3 basic-commutator forms',
            'coefficient_field':P,'central_I_minus_alpha_rank':len(pivots),'candidate_order':5,
            'normal_forms_checked':625,'checks':checks,
            'separating_functional':{m:v for m,v in zip(monomials,f) if v},
            'all_parameters_excluded':True,'free_group_AC_goal_solved':False}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output');args=p.parse_args();result=experiment()
    if args.output:Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
