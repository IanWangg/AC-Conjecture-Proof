"""Exact Fox derivatives of the braid-quotient certificate's lifting errors.

Elements of B3 are keyed by (exponent sum, C2*C3 normal form). Equality of
these data is exact, using B3=<s,t|s^2=t^3> and its central kernel.
"""
import argparse
from collections import defaultdict
import json
import time

IDENTITY = (0, ())
NORMAL_IMAGES = {'x': ((1,2),(0,1)), 'X': ((0,1),(1,1)),
                 'y': ((0,1),(1,2)), 'Y': ((1,1),(0,1))}


def syllables(word):
    out=[]
    for factor, exponent in word:
        if out and out[-1][0] == factor:
            exponent += out.pop()[1]
        exponent %= (2,3)[factor]
        if exponent:
            out.append((factor,exponent))
    return tuple(out)


def product(a,b):
    return a[0]+b[0], syllables(a[1]+b[1])


def inverse(a):
    return -a[0], syllables((f,-e) for f,e in reversed(a[1]))


LETTERS={c:(1 if c.islower() else -1,NORMAL_IMAGES[c]) for c in 'xXyY'}


def evaluate(word):
    ans=IDENTITY
    for c in word:
        ans=product(ans,LETTERS[c])
    return ans


def clean(poly):
    return {g:c for g,c in poly.items() if c}


def add(a,b,scale=1):
    result=defaultdict(int,a)
    for g,c in b.items():
        result[g]+=scale*c
    return clean(result)


def ring_product(a,b):
    out=defaultdict(int)
    for g,c in a.items():
        for h,d in b.items():
            out[product(g,h)]+=c*d
    return clean(out)


def fox(word):
    derivatives=[defaultdict(int),defaultdict(int)]
    prefix=IDENTITY
    for c in word:
        i='xy'.index(c.lower())
        if c.islower():
            derivatives[i][prefix]+=1
            prefix=product(prefix,LETTERS[c])
        else:
            prefix=product(prefix,LETTERS[c])
            derivatives[i][prefix]-=1
    return tuple(clean(d) for d in derivatives)


def module_coefficient(word):
    """Find K with d(word)=K*d(b), and verify both coordinates exactly.

    Highest exponent grade of d_x(b)=1+xy-y is uniquely its xy term.
    Hence the highest grade of K is recovered by right division by xy.
    The loop terminates for the concrete errors checked here. No blanket
    termination claim for arbitrary words is made by this implementation.
    """
    if evaluate(word) != IDENTITY:
        raise ValueError('word is not in the braid-relator kernel')
    dx,dy=fox(word)
    dbx,dby=fox('xyxYXY')
    expected=add(add({IDENTITY:1},{evaluate('xy'):1}),{evaluate('y'):1},-1)
    assert dbx==expected
    remaining=dict(dx)
    answer={}
    xy_inverse=evaluate('YX')
    loops=0
    while remaining:
        loops+=1
        if loops>1000:
            raise RuntimeError('finite-support division did not terminate in 1000 grade steps')
        grade=max(g[0] for g in remaining)
        top={product(g,xy_inverse):c for g,c in remaining.items() if g[0]==grade}
        answer=add(answer,top)
        remaining=add(remaining,ring_product(top,dbx),-1)
        assert not remaining or max(g[0] for g in remaining)<grade
    assert ring_product(answer,dbx)==dx
    assert ring_product(answer,dby)==dy
    return answer


def represent(poly):
    words=representatives(set(poly))
    return [{'coefficient':c,'word':words.get(g),'exponent_sum':g[0],
             'modular_syllables':g[1]} for g,c in sorted(poly.items())]


def representatives(targets,depth=12):
    words={IDENTITY:''}
    frontier=[IDENTITY]
    for _ in range(depth):
        if targets<=words.keys():
            break
        nxt=[]
        for g in frontier:
            for c in 'xXyY':
                h=product(g,LETTERS[c])
                if h not in words:
                    words[h]=words[g]+c
                    nxt.append(h)
        frontier=nxt
    return {g:words[g] for g in targets if g in words}


def augment(poly):
    return sum(poly.values())


def l1(poly):
    return sum(abs(c) for c in poly.values())


def free_inverse(word):
    return word.swapcase()[::-1]


def free_reduce(word):
    stack=[]
    for c in word:
        if stack and stack[-1] == c.swapcase():
            stack.pop()
        else:
            stack.append(c)
    return ''.join(stack)


def shell_diagram(word, limit=200000):
    """Look for an area-minimal disk shelling, using the module lower bound.

    Every rewrite removes precisely one unit of the known module norm.
    This search is finite but incomplete for diagrams that cannot be shelled
    under these rules. A returned path is checked as exact free-word rewrites.
    """
    relator='xyxYXY'
    patterns=[]
    for base,sign in ((relator,1),(free_inverse(relator),-1)):
        for rotation in range(6):
            r=base[rotation:]+base[:rotation]
            conjugator=inverse(evaluate(base[:rotation]))
            for cut in range(7):
                patterns.append((r[:cut],free_inverse(r[cut:]),sign,conjugator,
                                 free_inverse(base[:rotation])))
    initial_coefficient=module_coefficient(word)
    failed=set()
    visits=0
    budget_hit=False
    started=time.monotonic()

    def dfs(current, coefficient):
        nonlocal visits,budget_hit
        visits+=1
        if visits>limit:
            budget_hit=True
            return None
        if current=='':
            assert coefficient=={}
            return []
        if not coefficient or current in failed:
            return None
        prefixes=[IDENTITY]
        for c in current:
            prefixes.append(product(prefixes[-1],LETTERS[c]))
        candidates={}
        for position,prefix in enumerate(prefixes):
            for pattern,replacement,sign,offset,offset_word in patterns:
                if not current.startswith(pattern,position):
                    continue
                cell=product(prefix,offset)
                if coefficient.get(cell,0)*sign <= 0:
                    continue
                changed=free_reduce(current[:position]+replacement+current[position+len(pattern):])
                if changed==current:
                    continue
                next_coefficient=add(coefficient,{cell:sign},-1)
                move={'position':position,'pattern':pattern,'replacement':replacement,
                      'result':changed,'cell_sign':sign,
                      'conjugator':free_reduce(current[:position]+offset_word),
                      'cell_exponent_sum':cell[0],'cell_modular_syllables':cell[1]}
                candidates.setdefault(changed,(next_coefficient,move))
        for changed,(next_coefficient,move) in sorted(candidates.items(),key=lambda item:len(item[0])):
            rest=dfs(changed,next_coefficient)
            if rest is not None:
                return [move]+rest
            if budget_hit:
                return None
        failed.add(current)
        return None

    path=dfs(word,initial_coefficient)
    if path is not None:
        assert len(path)==l1(initial_coefficient)
        current=word
        reconstructed=''
        for move in path:
            p=move['position']
            assert current[p:p+len(move['pattern'])]==move['pattern']
            assert free_reduce(move['pattern']+free_inverse(move['replacement'])) in {
                base[k:]+base[:k] for base in (relator,free_inverse(relator)) for k in range(6)}
            current=free_reduce(current[:p]+move['replacement']+current[p+len(move['pattern']):])
            assert current==move['result']
            g=move['conjugator']
            assert evaluate(g)==(move['cell_exponent_sum'],tuple(move['cell_modular_syllables']))
            cell=relator if move['cell_sign'] == 1 else free_inverse(relator)
            reconstructed=free_reduce(reconstructed+g+cell+free_inverse(g))
        assert current==''
        assert reconstructed==word
    return {'path':path,'area_lower_bound':l1(initial_coefficient),
            'area_upper_bound':len(path) if path is not None else None,
            'search_visits':visits,'budget_hit':budget_hit,
            'seconds':round(time.monotonic()-started,4)}


def stallings(words):
    """Fold a based bouquet of word loops, keeping inverse labeled arcs."""
    edges=[]
    size=1
    for word in words:
        source=0
        for index,c in enumerate(word):
            target=0 if index==len(word)-1 else size
            if target:
                size+=1
            edges.append((source,c,target))
            edges.append((target,c.swapcase(),source))
            source=target
    parent=list(range(size))
    def root(v):
        while parent[v]!=v:
            parent[v]=parent[parent[v]]
            v=parent[v]
        return v
    merges=0
    while True:
        outgoing={}
        changed=False
        for source,c,target in edges:
            source,target=root(source),root(target)
            key=(source,c)
            if key in outgoing and root(outgoing[key])!=target:
                a,b=root(outgoing[key]),target
                parent[max(a,b)]=min(a,b)
                merges+=1
                changed=True
                break
            outgoing[key]=target
        if not changed:
            break
    final={(root(source),c,root(target)) for source,c,target in edges}
    vertices={source for source,c,target in final}|{target for source,c,target in final}
    base=root(0)
    # All initial edges lie on loops. For completeness trim non-base leaves.
    while True:
        leaves={v for v in vertices if v!=base and sum(a==v for a,c,b in final)==1}
        if not leaves:
            break
        final={e for e in final if e[0] not in leaves and e[2] not in leaves}
        vertices-=leaves
    ids={v:i for i,v in enumerate(sorted(vertices))}
    arcs=sorted((ids[a],c,ids[b]) for a,c,b in final)
    transitions={(a,c):b for a,c,b in arcs}
    start=ids[base]
    def accepts(word):
        current=start
        for c in word:
            if (current,c) not in transitions:
                return False
            current=transitions[current,c]
        return current==start
    assert all(accepts(w) for w in words)
    return {'vertices':len(vertices),'unoriented_edges':len(arcs)//2,
            'rank':len(arcs)//2-len(vertices)+1,'basepoint':start,
            'accepts_x':accepts('x'),'accepts_y':accepts('y'),
            'arcs':arcs,'vertex_merges':merges}


def selftest():
    b='xyxYXY'
    assert module_coefficient(b)=={IDENTITY:1}
    assert module_coefficient(b.swapcase()[::-1])=={IDENTITY:-1}
    assert module_coefficient('x'+b+'X')=={evaluate('x'):1}
    # The commutator of two kernel elements is invisible to this module.
    # It remains a nonempty freely reduced word in the free group.
    commutator=b+'x'+b+'X'+b.swapcase()[::-1]+'x'+b.swapcase()[::-1]+'X'
    assert module_coefficient(commutator)=={}
    assert free_reduce(commutator)!=''
    for word in ('x','xy','xyxyxy','xxYXy'):
        a=evaluate(word)
        assert product(a,inverse(a))==IDENTITY
    assert evaluate('xyxyxy')!=(0,())
    assert evaluate('xyxYXY')==IDENTITY
    assert stallings(['xy','y'])['vertices']==1
    assert stallings(['xx','y'])['vertices']==2
    assert not stallings(['xx','y'])['accepts_x']


def inspect(certificate, diagrams=False):
    with open(certificate) as stream:
        cert=json.load(stream)
    words=cert['free_basis_residuals']
    s={evaluate('X'*i):1 for i in range(4)}
    expected0=add({evaluate('YYYY'):1},s,-1)
    expected1=add({evaluate('XY'):1},{evaluate('YYY'):1},-1)
    expected1=add(expected1,ring_product(add({evaluate('y'):1},{evaluate('Xyyy'):1},-1),s))
    expected1=add(expected1,ring_product({evaluate('X'):1},{evaluate('y'*i):1 for i in range(3)}),-1)
    assert [module_coefficient(w) for w in words]==[expected0,expected1]
    result=[]
    for word in words:
        coefficient=module_coefficient(word)
        result.append({'word':word,'free_length':len(word),
                       'module_coefficient':represent(coefficient),
                       'support_size':len(coefficient),
                       'augmentation':augment(coefficient),'l1_norm':l1(coefficient),
                       'fox_pair_verified':True})
        if diagrams:
            result[-1]['diagram']=shell_diagram(word)
    return {'source':'braid quotient lift certificate',
            'scope':'relation-module lifting errors; no free-group trivialization',
            'compact_coefficients':['Y^4-(1+X+X^2+X^3)',
                                    'XY-Y^3+(y-X*y^3)*(1+X+X^2+X^3)-X*(1+y+y^2)'],
            'residuals':result,
            'endpoint_words':cert['target'],
            'endpoint_subgroup':stallings(cert['target'])}


def verify_saved(result):
    """Replay stored polynomial and diagram evidence without any search."""
    relator='xyxYXY'
    dbx,dby=fox(relator)
    orbit={base[k:]+base[:k] for base in (relator,free_inverse(relator)) for k in range(6)}
    for residual in result['residuals']:
        word=residual['word']
        recorded={}
        for term in residual['module_coefficient']:
            g=(term['exponent_sum'],tuple(tuple(s) for s in term['modular_syllables']))
            assert evaluate(term['word'])==g
            assert g not in recorded
            recorded[g]=term['coefficient']
        assert fox(word)==(ring_product(recorded,dbx),ring_product(recorded,dby))
        assert l1(recorded)==residual['l1_norm']
        assert augment(recorded)==residual['augmentation']
        assert len(recorded)==residual['support_size']
        if residual.get('diagram',{}).get('path') is not None:
            path=residual['diagram']['path']
            current=word
            reconstructed=''
            for move in path:
                p=move['position']
                assert current[p:p+len(move['pattern'])]==move['pattern']
                assert free_reduce(move['pattern']+free_inverse(move['replacement'])) in orbit
                current=free_reduce(current[:p]+move['replacement']+current[p+len(move['pattern']):])
                assert current==move['result']
                g=move['conjugator']
                cell=relator if move['cell_sign']==1 else free_inverse(relator)
                reconstructed=free_reduce(reconstructed+g+cell+free_inverse(g))
            assert current=='' and reconstructed==word
            assert len(path)==l1(recorded)==residual['diagram']['area_lower_bound']==residual['diagram']['area_upper_bound']
    assert json.loads(json.dumps(stallings(result['endpoint_words'])))==json.loads(json.dumps(result['endpoint_subgroup']))
    return {'status':'PASS','minimal_braid_areas':[r['l1_norm'] for r in result['residuals']],
            'endpoint_subgroup_vertices':result['endpoint_subgroup']['vertices'],
            'endpoint_subgroup_rank':result['endpoint_subgroup']['rank'],
            'free_group_goal_solved':False}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('certificate',nargs='?',default='certificates/psl2z_quotient_lift.json')
    parser.add_argument('--output')
    parser.add_argument('--diagrams',action='store_true')
    parser.add_argument('--verify')
    parser.add_argument('--summary',action='store_true')
    args=parser.parse_args()
    selftest()
    if args.verify:
        with open(args.verify) as stream:
            result=json.load(stream)
        print(json.dumps(verify_saved(result),indent=2))
        raise SystemExit(0)
    result=inspect(args.certificate,args.diagrams)
    verify_saved(result)
    if args.output:
        with open(args.output,'w') as stream:
            json.dump(result,stream,indent=2)
            stream.write('\n')
    print(json.dumps(verify_saved(result) if args.summary else result,indent=2))
