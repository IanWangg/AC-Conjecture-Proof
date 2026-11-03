"""Independent bounded Nielsen-basis class enumeration for the initial AK H_n.

Enumerates primitive exponent vectors and unimodular pairs directly, rather
than traversing V's positive Farey tree. Chosen primitive representatives
need not jointly be a literal basis: only their independent conjugacy
classes are used, and unimodularity guarantees a basis with those classes.
"""
import argparse
import base64
import gzip
from itertools import combinations
import hashlib
import json
from math import gcd
from pathlib import Path


def inverse(w):return w.swapcase()[::-1]


def reduce(w):
    out=[]
    for c in w:
        if out and out[-1]==c.swapcase():out.pop()
        else:out.append(c)
    return ''.join(out)


def cyclic(w):
    w=reduce(w)
    while len(w)>1 and w[0]==w[-1].swapcase():w=w[1:-1]
    return w


def canonical(w):
    w=cyclic(w)
    return min(v[i:]+v[:i] for v in (w,inverse(w)) for i in range(len(v))) if w else ''


def positive(a,b):
    assert a>=0 and b>=0 and gcd(a,b)==1
    if not a:return 'b'
    if not b:return 'a'
    if a==b:return 'ab'
    if a>b:return positive(a-b,b).replace('b','ab')
    return positive(a,b-a).replace('a','ab')


def representative(a,b):
    return positive(abs(a),abs(b)).translate(str.maketrans({'a':'A' if a<0 else 'a',
                                                          'b':'B' if b<0 else 'b'}))


def substitute(w,n):
    a='x'*n+'Y'*(n+1);b='xyxYXY'
    table={'a':a,'A':inverse(a),'b':b,'B':inverse(b)}
    return reduce(''.join(table[c] for c in w))


def length(n,a,b):return 2*abs(a+b)+(2*n-1)*abs(a)+4*abs(b)


def read_payload(path):
    """Read plain UTF-8, gzip, or base64-wrapped gzip corpus bytes."""
    raw=Path(path).read_bytes()
    if str(path).endswith('.b64'):raw=base64.b64decode(raw,validate=False)
    if raw.startswith(b'\x1f\x8b'):raw=gzip.decompress(raw)
    return raw


def enumerate_classes(n,cap):
    assert n>=2
    shortest=min(2*n+1,6)
    bound_a=(cap-shortest)//(2*n-1)
    bound_b=(cap-shortest)//4
    vectors=[]
    images={}
    for a in range(max(0,bound_a)+1):
        for b in range(-max(0,bound_b),max(0,bound_b)+1):
            if gcd(a,b)!=1 or (not a and b<0):continue
            value=length(n,a,b)
            if value+shortest>cap:continue
            word=substitute(representative(a,b),n)
            assert len(cyclic(word))==value
            vectors.append((a,b))
            images[a,b]=canonical(word)
    families={}
    matrix_pairs=0
    for u,v in combinations(vectors,2):
        determinant=u[0]*v[1]-u[1]*v[0]
        if abs(determinant)!=1 or length(n,*u)+length(n,*v)>cap:continue
        matrix_pairs+=1
        key=tuple(sorted((images[u],images[v])))
        families.setdefault(key,[]).append({'columns':[list(u),list(v)],
                                           'determinant':determinant,
                                           'formal_representatives':[representative(*u),representative(*v)]})
    return families,{'status':'COMPLETE_BOUNDED_BASIS_CLASSES',
                     'ordinary_AC_goal_solved':False,'n':n,'cyclic_endpoint_cap':cap,
                     'shortest_primitive_H_coordinate':shortest,
                     'absolute_vector_coordinate_bounds':[bound_a,bound_b],
                     'projective_primitive_vectors_tested':len(vectors),
                     'unimodular_projective_pairs':matrix_pairs,
                     'distinct_cyclic_basis_pair_classes':len(families),
                     'all_vector_length_formulas_checked_by_literal_substitution':True,
                     'scope':'All initial-H Nielsen basis cyclic classes with stated endpoint energy; no primitive absence conclusion'}


def compare(families,path):
    raw=read_payload(path)
    text=raw.decode()
    if text.lstrip().startswith('['):
        data=json.loads(text)
        rows=[r.get('pair',r.get('cyclic_basis')) if isinstance(r,dict) else r for r in data]
    elif text.lstrip().startswith('{'):
        rows=[r.get('pair',r.get('cyclic_basis')) for r in
              (json.loads(line) for line in text.splitlines() if line.strip())]
    else:
        rows=[line.split('\t') for line in text.splitlines() if line.strip()]
    actual={tuple(sorted(map(canonical,row))) for row in rows}
    expected=set(families)
    missing=sorted(expected-actual);extra=sorted(actual-expected)
    assert not missing and not extra,{'missing':missing[:5],'extra':extra[:5]}
    return {'status':'PASS','compared_source_sha256':hashlib.sha256(raw).hexdigest(),
            'exact_cyclic_family_sets_equal':True,'compared_distinct_classes':len(actual)}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--n',type=int,default=3)
    parser.add_argument('--cap',type=int,default=40);parser.add_argument('--families',required=True)
    parser.add_argument('--provenance');parser.add_argument('--compare');parser.add_argument('--output',required=True)
    args=parser.parse_args();families,result=enumerate_classes(args.n,args.cap)
    ordered=sorted(families)
    Path(args.families).write_text(''.join(a+'\t'+b+'\n' for a,b in ordered))
    if args.provenance:Path(args.provenance).write_text(json.dumps([{'pair':key,'matrix_sources':families[key]} for key in ordered],indent=2)+'\n')
    if args.compare:result['independent_Farey_comparison']=compare(families,args.compare)
    result['family_tsv_sha256']=hashlib.sha256(Path(args.families).read_bytes()).hexdigest()
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
