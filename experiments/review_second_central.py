"""Independent tensor/Magnus check of L's next-central classes.

Shares the previously verified exact B3/Fox arithmetic from I, but does not
import L's audit code. Uses a different Schreier transversal and computes
degree-two tensors before mapping the antisymmetric tensor to coinvariants.
"""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import first_order_correction as f

m=f.m


def transversal(targets):
    # Different shortlex order from L, hence generally a different free basis.
    representatives={m.IDENTITY:''}
    layer=[m.IDENTITY]
    depth=0
    while not targets <= representatives.keys():
        fresh=[]
        for g in layer:
            for letter in 'yYxX':
                h=m.product(g,m.LETTERS[letter])
                if h not in representatives:
                    representatives[h]=representatives[g]+letter
                    fresh.append(h)
        layer=fresh
        depth+=1
        if depth>20 or len(representatives)>1000000:
            raise RuntimeError('independent transversal budget reached')
    # Every representative is a literal tree path and every prefix is retained.
    for word in representatives.values():
        for k in range(len(word)):
            prefix=word[:k]
            assert representatives[m.evaluate(prefix)]==prefix
    return representatives,depth


def rank_mod101(vectors):
    pivots={}
    for vector in vectors:
        row={g:c%101 for g,c in vector.items() if c%101}
        while row:
            key=min(row)
            coefficient=row[key]
            if key not in pivots:
                scale=pow(coefficient,-1,101)
                pivots[key]={g:c*scale%101 for g,c in row.items()}
                break
            for g,c in pivots[key].items():
                value=(row.get(g,0)-coefficient*c)%101
                if value:row[g]=value
                else:row.pop(g,None)
    return len(pivots)


def class_from_tensor(form, basis):
    # Degree-two Magnus expansion in the genuine Schreier free generators.
    abelian=defaultdict(int)
    tensor=defaultdict(int)
    for i,sign in form:
        for j,count in list(abelian.items()):
            tensor[j,i]+=count*sign
        if sign==-1:
            tensor[i,i]+=1
        abelian[i]+=sign
        if not abelian[i]:del abelian[i]
    assert not abelian
    tensor={key:value for key,value in tensor.items() if value}
    indices=set(i for i,j in tensor)|set(j for i,j in tensor)
    for i in indices:
        assert tensor.get((i,i),0)==0
        for j in indices:
            assert tensor.get((i,j),0)==-tensor.get((j,i),0)
    output=defaultdict(int)
    for (i,j),coefficient in tensor.items():
        if i>=j:
            continue
        for g,c in basis[i].items():
            for h,e in basis[j].items():
                relative=m.product(m.inverse(g),h)
                if relative==m.IDENTITY:
                    continue
                reverse=m.inverse(relative)
                assert reverse!=relative
                key,sign=(relative,1) if relative<reverse else (reverse,-1)
                output[key]+=coefficient*c*e*sign
    return m.clean(output),len(tensor)


def review(certificate,expected_path,strict_path=None):
    cert=f.load(certificate)
    if strict_path:
        from elementary_verify import replay
        strict=json.loads(Path(strict_path).read_text())
        strict_summary=replay(strict)
        assert strict['target']==cert['target']
    else:
        strict_summary=None
    errors=[m.free_reduce(w+t.swapcase()) for w,t in zip(cert['target'],'xy')]
    paths=[]
    needed={m.IDENTITY}
    for word in errors:
        current=m.IDENTITY
        edges=[]
        for letter in word:
            end=m.product(current,m.LETTERS[letter])
            edges.append((current,letter,end))
            needed.add(end)
            current=end
        assert current==m.IDENTITY
        paths.append(edges)
    reps,depth=transversal(needed)
    basis_edges={}
    coefficients=[]
    basis_words=[]
    forms=[]
    for path,word in zip(paths,errors):
        form=[]
        for g,c,h in path:
            edge=(g,c) if c.islower() else (h,c.lower())
            if edge not in basis_edges:
                vertex,letter=edge
                end=m.product(vertex,m.LETTERS[letter])
                loop=m.free_reduce(reps[vertex]+letter+m.free_inverse(reps[end]))
                if not loop:
                    basis_edges[edge]=None
                else:
                    index=len(coefficients)
                    basis_edges[edge]=index
                    basis_words.append(loop)
                    coefficient=m.module_coefficient(loop)
                    assert coefficient
                    coefficients.append(coefficient)
            index=basis_edges[edge]
            if index is not None:
                sign=1 if c.islower() else -1
                if form and form[-1]==(index,-sign):
                    form.pop()
                else:
                    form.append((index,sign))
        reconstructed=m.free_reduce(''.join(basis_words[i] if sign==1 else m.free_inverse(basis_words[i]) for i,sign in form))
        assert reconstructed==word
        forms.append(form)
    assert rank_mod101(coefficients)==len(coefficients)
    expected=json.loads(Path(expected_path).read_text())
    rows=[]
    for form,wanted in zip(forms,expected['residuals']):
        result,tensor_support=class_from_tensor(form,coefficients)
        saved={(row['B3_exponent'],tuple(tuple(x) for x in row['C2C3_syllables'])):row['coefficient'] for row in wanted['next_central_class']}
        assert result==saved
        rows.append({'Schreier_word_length_alternate_tree':len(form),
                     'degree_two_tensor_support':tensor_support,
                     'all_coefficients_match_L':True,'next_central_support':len(result),
                     'next_central_l1':sum(map(abs,result.values()))})
    # Independent positive orientation control: [s0,s1] has tensor coefficient +1.
    identity={m.IDENTITY:1}
    x={m.evaluate('x'):1}
    control,_=class_from_tensor([(0,1),(1,1),(0,-1),(1,-1)],[identity,x])
    relative=m.evaluate('x')
    rev=m.inverse(relative)
    assert control==({relative:1} if relative<rev else {rev:-1})
    return {'status':'PASS','independent_algorithm':'degree-two Magnus tensors in alternate Schreier basis',
            'shared_arithmetic':'I exact B3 group and Fox coefficient functions; no L audit code imported',
            'transversal_order':'yYxX','transversal_depth':depth,'transversal_vertices':len(reps),
            'needed_prefix_vertices':len(needed),'free_basis_generators_used':len(coefficients),
            'free_basis_module_rank_mod101':rank_mod101(coefficients),
            'prefix_closed_tree_checked':True,'exact_free_reconstruction_checked':True,
            'strict_free_ledger':None if strict_summary is None else {
                'moves':strict_summary['moves'],'peak_total_length':strict_summary['peak_total_length'],
                'endpoint_lengths':list(map(len,strict_summary['endpoint']))},
            'residuals':rows,'ordinary_AC_goal_solved':False,
            'source_sha256':{str(path):hashlib.sha256(Path(path).read_bytes()).hexdigest() for path in (certificate,expected_path)}}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('certificate')
    parser.add_argument('expected_classes')
    parser.add_argument('--strict')
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    result=review(args.certificate,args.expected_classes,args.strict)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
