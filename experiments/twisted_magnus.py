"""Exact finite characteristic-quotient tests of one twisted conjugacy problem.

Fiber generators a,b; alpha(a)=b, alpha(b)=aB. The finite quotient is the
image in units of F2<<a,b>> truncated above the specified degree, modulo 2.
No conclusion here concerns all Andrews-Curtis paths.
"""
from collections import deque
import argparse
import hashlib
import json
from pathlib import Path


def inverse_word(word):
    return word.swapcase()[::-1]


class Magnus2:
    def __init__(self, degree):
        self.degree = degree
        self.size = 2**(degree+1)-1
        self.length = [(i+1).bit_length()-1 for i in range(self.size)]
        self.value = [i-(2**l-1) for i,l in enumerate(self.length)]
        self.a = 1 | (1 << 1)
        self.b = 1 | (1 << 2)
        self.A = self.inverse(self.a)
        self.B = self.inverse(self.b)
        self.letters = dict(zip('abAB',(self.a,self.b,self.A,self.B)))

    def product(self, a, b):
        result = 0
        while a:
            bit = a & -a
            i = bit.bit_length()-1
            a ^= bit
            li,vi = self.length[i],self.value[i]
            rest = b
            while rest:
                bit = rest & -rest
                j = bit.bit_length()-1
                rest ^= bit
                lj = self.length[j]
                if li+lj <= self.degree:
                    k = 2**(li+lj)-1+(vi<<lj)+self.value[j]
                    result ^= 1 << k
        return result

    def inverse(self, a):
        v = a ^ 1
        ans,power = 1,1
        for _ in range(self.degree):
            power = self.product(power,v)
            ans ^= power
        assert self.product(a,ans) == 1
        return ans

    def evaluate(self, word):
        ans = 1
        for c in word:
            ans = self.product(ans,self.letters[c])
        return ans

    def columns(self, left, right):
        return [self.product(self.product(left,1<<i),right) for i in range(self.size)]

    @staticmethod
    def apply(columns, value):
        ans = 0
        while value:
            bit = value & -value
            ans ^= columns[bit.bit_length()-1]
            value ^= bit
        return ans


def experiment(degree,budget=1000000,group_order=False):
    ring = Magnus2(degree)
    images = {'a':'b','b':'aB','A':'B','B':'bA'}
    inverse_images = {'a':'ba','b':'a','A':'AB','B':'A'}
    # Verify both substitutions are inverse in the finite algebra.
    for c in 'abAB':
        for first,second in ((images,inverse_images),(inverse_images,images)):
            assert ring.evaluate(''.join(second[d] for d in first[c])) == ring.letters[c]
    # Substitution on augmentation monomials, proving a finite-order
    # automorphism of the generated finite group rather than only a map
    # on a bounded list of ordinary words.
    substitution=[]
    for i in range(ring.size):
        value=1
        for shift in reversed(range(ring.length[i])):
            letter='ab'[(ring.value[i]>>shift)&1]
            value=ring.product(value,ring.evaluate(images[letter])^1)
        substitution.append(value)
    alpha_order,aa,bb=0,ring.a,ring.b
    while True:
        aa=ring.apply(substitution,aa)
        bb=ring.apply(substitution,bb)
        alpha_order+=1
        if (aa,bb)==(ring.a,ring.b):
            break
        assert alpha_order<100000
    def alpha(value,exponent):
        for _ in range(exponent%alpha_order):
            value=ring.apply(substitution,value)
        return value
    def semiproduct(u,v):
        return (ring.product(u[0],alpha(v[0],u[1])),(u[1]+v[1])%alpha_order)
    def semi_inverse(u):
        return (alpha(ring.inverse(u[0]),-u[1]),(-u[1])%alpha_order)
    sx,sy=(1,1),(ring.evaluate('aB'),1)
    original_letters={'x':sx,'y':sy,'X':semi_inverse(sx),'Y':semi_inverse(sy)}
    def original_word(word):
        result=(1,0)
        for c in word:
            result=semiproduct(result,original_letters[c])
        return result
    assert original_word('XXyxYxxY')==(1,0)
    assert original_word('XXyx')==(ring.a,0)
    assert original_word('Xy')==(ring.b,0)
    assert original_word('yyyyXXX')==(ring.evaluate('abbAbA'),1)
    assert original_word('xY')==(ring.evaluate('bA'),0)
    columns = []
    for c in 'abAB':
        left = ring.letters[c]
        right = ring.inverse(ring.evaluate(images[c]))
        columns.append(ring.columns(left,right))
    start = ring.evaluate('abbAbA')
    candidate = ring.evaluate('bA')
    order, current = 1,candidate
    while current != 1:
        current = ring.product(current,candidate)
        order += 1
        assert order <= 2**degree
    powers,current = [],1
    for _ in range(order):
        powers.append(current)
        current = ring.product(current,candidate)
    seen = {start}
    queue = deque([start])
    processed = 0
    while queue:
        current = queue.popleft()
        processed += 1
        for transform in columns:
            nxt = ring.apply(transform,current)
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
        if len(seen)>budget:
            break
    complete = not queue
    hits = [k for k,power in enumerate(powers) if power in seen]
    width = (ring.size+7)//8
    digest = hashlib.sha256(b''.join(x.to_bytes(width,'little') for x in sorted(seen))).hexdigest()
    result={'degree':degree,'coefficient_field':2,'magnus_vector_size':ring.size,
            'complete_twisted_orbit':complete,'orbit_states':len(seen),
            'states_processed':processed,'candidate_order':order,
            'alpha_order_on_fiber_image':alpha_order,
            'original_word_checks':'bprime=1; a=X^2 yx; b=Xy; p^-1=W*t; xY=C',
            'candidate_k_residues_seen':hits,'orbit_sha256':digest,
            'scope':'One primitive-replacement twisted conjugacy test; not an AC obstruction'}
    if group_order:
        right_columns=[ring.columns(1,ring.letters[c]) for c in 'abAB']
        elements={1}
        pending=deque([1])
        while pending:
            element=pending.popleft()
            for transform in right_columns:
                nxt=ring.apply(transform,element)
                if nxt not in elements:
                    elements.add(nxt)
                    pending.append(nxt)
            assert len(elements)<=2000000
        result['finite_fiber_group_order']=len(elements)
        result['finite_semidirect_quotient_order']=len(elements)*alpha_order
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--degree',type=int,default=5)
    p.add_argument('--budget',type=int,default=1000000)
    p.add_argument('--output')
    p.add_argument('--group-order',action='store_true')
    args = p.parse_args()
    result = experiment(args.degree,args.budget,args.group_order)
    if args.output:
        Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
