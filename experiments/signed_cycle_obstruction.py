"""Exact signed-cycle certificate for primitive-free AK(n) subgroups.

The all-n argument is in the accompanying note. Finite computations check
the explicit folded graph and the signed subgraph cycle classifications.
"""
import argparse
from collections import deque
import json
import math
from pathlib import Path
from stallings_search import graph, inverse, reduce, primitive

LETTERS='xXyY'


def canonical(arcs,base=0):
    transitions={}
    for a,c,b in arcs:
        assert (a,c) not in transitions or transitions[a,c]==b
        transitions[a,c]=b
        assert (b,c.swapcase(),a) in arcs
    names={base:0}
    queue=deque([base])
    output=[]
    while queue:
        v=queue.popleft()
        for c in LETTERS:
            w=transitions.get((v,c))
            if w is None:
                output.append(-1)
            else:
                if w not in names:
                    names[w]=len(names)
                    queue.append(w)
                output.append(names[w])
    return tuple(output),names,transitions


def explicit_graph(n):
    length=2*n+1
    edges=[]
    p='x'*n+'Y'*(n+1)
    for i,c in enumerate(p):
        edges.append((i,c,(i+1)%length))
    a,b,c=length,length+1,length+2
    edges.extend(((1,'y',a),(a,'x',b),(b,'Y',c),(c,'X',2*n)))
    return set(edges+[(v,t.swapcase(),u) for u,t,v in edges])


def necklace(word):
    return min(t[k:]+t[:k] for t in (word,inverse(word)) for k in range(len(t)))


def signed_components(arcs,alphabet):
    edges=[e for e in arcs if e[1] in alphabet]
    vertices={a for a,c,b in arcs}|{b for a,c,b in arcs}
    reach={v:{v} for v in vertices}
    for _ in vertices:
        for a,c,b in edges:
            reach[a] |= reach[b]
    components=[]
    while vertices:
        v=min(vertices)
        component={w for w in vertices if w in reach[v] and v in reach[w]}
        vertices-=component
        internal=[e for e in edges if e[0] in component and e[2] in component]
        if len(component)==1 and not any(a==b for a,c,b in internal):
            continue
        assert len(internal)==len(component)
        assert all(sum(a==v for a,c,b in internal)==1 for v in component)
        transition={a:(c,b) for a,c,b in internal}
        start=min(component)
        current=start
        word=''
        while True:
            c,current=transition[current]
            word+=c
            if current==start:
                break
            assert len(word)<=len(component)
        components.append({'vertices':sorted(component),'cycle_word':word})
    return components


def analyze(n):
    assert n>=1
    arcs=explicit_graph(n)
    encoded,names,transitions=canonical(arcs)
    pair=['x'*n+'Y'*(n+1),'xyxYXY']
    actual,size=graph(pair)
    assert actual==encoded
    assert size==len(names)==2*n+4
    assert len(arcs)//2==2*n+5
    for w in pair:
        at=0
        for c in w:
            at=transitions[at,c]
        assert at==0
    components={alphabet:signed_components(arcs,alphabet) for alphabet in ('xy','xY','Xy','XY')}
    assert components['xy']==components['XY']==[]
    assert len(components['xY'])==len(components['Xy'])==1
    p=pair[0]
    for alphabet in ('xY','Xy'):
        assert necklace(components[alphabet][0]['cycle_word'])==necklace(p)
    assert primitive(p)==(n==1)
    return {'n':n,'vertices':size,'unoriented_edges':len(arcs)//2,'rank':2,
            'generator_words':pair,'arcs':sorted(arcs),
            'signed_cyclic_components':components,'power_relator_primitive':n==1,
            'primitive_free_subgroup_conclusion':n>=2}


def positive_primitive(a,b):
    assert a>=0 and b>=0 and math.gcd(a,b)==1
    if a==0:
        return 'y'
    if b==0:
        return 'x'
    if a==b:
        return 'xy'
    if a>b:
        word=positive_primitive(a-b,b)
        return ''.join('xy' if c=='y' else c for c in word)
    word=positive_primitive(a,b-a)
    return ''.join('xy' if c=='x' else c for c in word)


def selftest():
    for a in range(16):
        for b in range(16):
            if math.gcd(a,b)==1:
                word=positive_primitive(a,b)
                assert word.count('x')==a and word.count('y')==b and primitive(word)
    checks=[]
    for n in range(1,51):
        report=analyze(n)
        m='xY'
        w=m*n+'Y'
        images=[m,w]
        def sub(word):
            table={'a':images[0],'A':inverse(images[0]),'b':images[1],'B':inverse(images[1])}
            return reduce(''.join(table[c] for c in word))
        assert sub('aB'+'a'*n)=='x'
        assert sub('B'+'a'*n)=='y'
        checks.append({'n':n,'vertices':report['vertices'],
                       'primitive_free_subgroup_conclusion':report['primitive_free_subgroup_conclusion']})
    return {'status':'PASS','family_graphs_checked':'n=1..50',
            'positive_primitive_vectors_checked':'0<=a,b<=15, gcd(a,b)=1',
            'AK1_positive_control_primitive':'xYY','family_results':checks,
            'AK3_certificate':analyze(3),
            'scope':'Finite checks of the uniform primitive-free initial subgroup theorem; not a global AC obstruction'}


def verify_saved(data):
    expected=analyze(3)
    assert data['AK3_certificate']==json.loads(json.dumps(expected))
    assert data['status']=='PASS'
    return {'status':'PASS','saved_AK3_signed_cycle_certificate_verified':True,
            'vertices':expected['vertices'],'unoriented_edges':expected['unoriented_edges'],
            'all_word_lengths_covered_by_theorem':True,'ordinary_AC_goal_solved':False}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output')
    parser.add_argument('--verify')
    args=parser.parse_args()
    if args.verify:
        result=verify_saved(json.loads(Path(args.verify).read_text()))
    else:
        result=selftest()
        if args.output:
            Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
