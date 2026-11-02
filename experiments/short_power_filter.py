"""Filter ALL cyclic free words length<=7 with the fixed first-hump braid.

The finite quotient is Research K's exact mod2 degree5 Magnus semidirect
group. Rejection proves nonconjugacy in the deletion group; a survivor
still needs an actual conjugator or another exact argument.
"""
from collections import Counter,deque
import argparse
import json
from pathlib import Path
from twisted_magnus import Magnus2,inverse_word


def orbit_word(word):
    result=set()
    for w in (word,inverse_word(word)):
        result.update(w[k:]+w[:k] for k in range(len(w)))
    return result


def free_reduce(word):
    out=[]
    for c in word:
        if out and out[-1]==c.swapcase():out.pop()
        else:out.append(c)
    return ''.join(out)


def exact_coefficient(word):
    forward={'a':'b','b':'aB','A':'B','B':'bA'}
    backward={'a':'ba','b':'a','A':'AB','B':'A'}
    def power(word,n):
        mapping=forward if n>=0 else backward
        for _ in range(abs(n)):word=free_reduce(''.join(mapping[c] for c in word))
        return word
    coeff,exponent='',0
    for c in word:
        fiber={'x':'','X':'','y':'aB','Y':'B'}[c]
        coeff=free_reduce(coeff+power(fiber,exponent))
        exponent+=1 if c.islower() else -1
    return coeff,exponent


def cyclic_words(maximum):
    frontier=['']
    for _ in range(maximum):
        nxt=[]
        for w in frontier:
            for c in 'xXyY':
                if not w or w[-1]!=c.swapcase():
                    v=w+c;nxt.append(v)
                    if v[0]!=v[-1].swapcase():yield v
        frontier=nxt


def experiment(maximum=7):
    ring=Magnus2(5)
    images={'a':'b','b':'aB','A':'B','B':'bA'}
    substitution=[]
    for i in range(ring.size):
        image=1
        for shift in reversed(range(ring.length[i])):
            c='ab'[(ring.value[i]>>shift)&1]
            image=ring.product(image,ring.evaluate(images[c])^1)
        substitution.append(image)
    a,b,alpha_order=ring.a,ring.b,0
    while True:
        a,b=ring.apply(substitution,a),ring.apply(substitution,b);alpha_order+=1
        if (a,b)==(ring.a,ring.b):break
        assert alpha_order<100000
    assert alpha_order==24
    def alpha(value,n):
        for _ in range(n%alpha_order):value=ring.apply(substitution,value)
        return value
    transformations=[]
    for c in 'abAB':
        transformations.append(ring.columns(ring.letters[c],ring.inverse(ring.evaluate(images[c]))))
    start=ring.evaluate('abbAbA')
    seen={start};queue=deque([start])
    while queue:
        value=queue.popleft()
        for transform in transformations:
            nxt=ring.apply(transform,value)
            if nxt not in seen:seen.add(nxt);queue.append(nxt)
    assert len(seen)==65536
    # x=t, y=(aB)t, X=t^-1, Y=B t^-1 in the exact model.
    fiber={'x':1,'X':1,'y':ring.evaluate('aB'),'Y':ring.evaluate('B')}
    span=max(maximum,7)
    twists={(n,c):alpha(v,n) for n in range(-span,span+1) for c,v in fiber.items()}
    def evaluate(word):
        coefficient,exponent=1,0
        for c in word:
            coefficient=ring.product(coefficient,twists[(exponent,c)])
            exponent+=1 if c.islower() else -1
        return coefficient,exponent
    assert evaluate('yyyyXXX')==(start,1)
    passed=[];tested=Counter();eligible=Counter()
    for word in cyclic_words(maximum):
        tested[len(word)]+=1
        exponent=sum(1 if c.islower() else -1 for c in word)
        if abs(exponent)!=1:continue
        eligible[len(word)]+=1
        normalized=word if exponent==1 else inverse_word(word)
        coefficient,actual_exponent=evaluate(normalized)
        assert actual_exponent==1
        if coefficient in seen:passed.append(word)
    classes={min(orbit_word(w)) for w in passed}
    for w in passed:assert orbit_word(w)<=set(passed)
    exact_candidates=[]
    for word in sorted(classes):
        exponent=sum(1 if c.islower() else -1 for c in word)
        normalized=word if exponent==1 else inverse_word(word)
        coeff,e=exact_coefficient(normalized)
        assert e==1 and ring.evaluate(coeff)==evaluate(normalized)[0]
        exact_candidates.append({'representative':word,'normalized_chi_one_word':normalized,
                                 'exact_fiber_coefficient':coeff,'stable_exponent':e})
    p,q='xxxYYYY','yyyXXXX'
    return {'maximum_cyclic_length':maximum,'tested_by_length':dict(sorted(tested.items())),
            'eligible_exponent_abs_one_by_length':dict(sorted(eligible.items())),
            'finite_twisted_orbit_states':len(seen),'surviving_words':sorted(passed),
            'surviving_cyclic_inverse_orbit_representatives':sorted(classes),
            'exact_twisted_candidates':exact_candidates,
            'only_original_power_orbit':set(passed)==orbit_word(p),
            'only_original_and_swapped_power_orbits':set(passed)==orbit_word(p)|orbit_word(q),
            'scope':'Necessary finite quotient filter; survivors are not asserted conjugate in G'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--maximum',type=int,default=7);p.add_argument('--output');args=p.parse_args()
    result=experiment(args.maximum)
    if args.output:Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
