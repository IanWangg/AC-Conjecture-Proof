"""Check twisted conjugacy in finite characteristic-two fibre algebras."""

from functools import lru_cache
import json

from round15_ak3_torus_atlas import apply
from round19_ak3_minimum_class_two import MARKINGS, SOURCE, indexed_word, solve_letter


def bits(word):
    while word:
        lowest = word & -word
        yield lowest.bit_length()-1
        word ^= lowest


class Series:
    def __init__(self, rank, degree):
        self.rank, self.degree = rank, degree
        self.powers = [rank**d for d in range(degree+1)]
        self.offset = [0]
        for size in self.powers:
            self.offset.append(self.offset[-1]+size)
        self.size = self.offset[-1]
        self.terms = [(d,i) for d,size in enumerate(self.powers) for i in range(size)]
        self.symbols = [1 | (1 << (1+i)) for i in range(rank)]

    def multiply(self, left, right):
        output = 0
        for i in bits(left):
            degree, word = self.terms[i]
            for j in bits(right & ((1 << self.offset[self.degree-degree+1])-1)):
                d2, w2 = self.terms[j]
                output ^= 1 << (self.offset[degree+d2] + word*self.powers[d2] + w2)
        return output

    def invert(self, series):
        term, result = 1, 1
        for _ in range(self.degree):
            term = self.multiply(term,series ^ 1)
            result ^= term
        assert self.multiply(series,result) == 1
        return result

    def columns(self, images):
        results = [1]
        for length in range(1,self.degree+1):
            for word in range(self.powers[length]):
                prefix = results[self.offset[length-1]+word//self.rank]
                results.append(self.multiply(prefix, images[word % self.rank] ^ 1))
        return results

    def test_twisted(self, receiver, columns, candidates):
        right = [self.multiply(1 << i, receiver) for i in range(1,self.size)]
        results = []
        for target in candidates:
            pivots = [0] * self.size
            operators = []
            rank = 0
            for image, term in zip(columns[1:],right):
                v = self.multiply(target,image) ^ term
                operators.append(v)
                while v:
                    pivot = v.bit_length()-1
                    if not pivots[pivot]:
                        pivots[pivot] = v
                        rank += 1
                        break
                    v ^= pivots[pivot]
            remaining = receiver ^ target
            while remaining and (pivot := pivots[remaining.bit_length()-1]):
                remaining ^= pivot
            dual = 0
            if remaining:
                index = remaining.bit_length()-1
                for basis in range(index,self.size):
                    image = 1 << basis
                    for column in range(basis,index,-1):
                        if (image >> column) & 1:
                            image ^= pivots[column]
                    dual |= ((image >> index) & 1) << basis
                assert all(bin(row & dual).count("1") % 2 == 0 for row in operators)
                assert bin((receiver ^ target) & dual).count("1") % 2 == 1
            results.append((rank,dual))
        return results


def audit(relator, receiver, degree):
    low = min(i for i,_ in relator)
    high = max(i for i,_ in relator)
    algebra = Series(high-low, degree)
    lower, upper = solve_letter(relator,low), solve_letter(relator,high)

    @lru_cache(None)
    def letter(index):
        if low <= index < high:
            return algebra.symbols[index-low]
        template, delta = (upper,index-high) if index >= high else (lower,index-low)
        return evaluate((i+delta,sign) for i,sign in template)

    def evaluate(word):
        result = 1
        for i, sign in word:
            value = letter(i)
            result = algebra.multiply(result,value if sign == 1 else algebra.invert(value))
        return result

    assert evaluate(relator) == 1 and evaluate((i+1,sign) for i,sign in relator) == 1
    shift = algebra.columns([letter(i+1) for i in range(low,high)])
    back = algebra.columns([letter(i-1) for i in range(low,high)])
    for one,two in ((shift,back),(back,shift)):
        for i in range(1,1+high-low):
            assert xor_images(one,two[i]) == 1 << i
    source, candidate_base = evaluate(receiver), letter(0)
    candidates, current = [], 1
    while True:
        candidates.append(current)
        current = algebra.multiply(current,candidate_base)
        if current == 1:
            break
    report = algebra.test_twisted(source,shift,candidates)
    if algebra.size <= 7:
        actual = set()
        for g in range(1,1 << algebra.size,2):
            inverse = algebra.invert(xor_images(shift,g))
            actual.add(algebra.multiply(algebra.multiply(g,source),inverse))
        assert [not dual for _,dual in report] == [x in actual for x in candidates]
    return {"degree":degree,"unit_algebra_dimension":algebra.size,
            "slope_period":len(candidates),"rank_by_residue":[rank for rank,_ in report],
            "surviving_residues":[i for i,(_,dual) in enumerate(report) if not dual],
            "rejecting_duals_hex":{i:hex(dual) for i,(_,dual) in enumerate(report) if dual}}


def xor_images(columns, series):
    result = 0
    for i in bits(series):
        result ^= columns[i]
    return result


def main():
    result = []
    for i, chart in enumerate(MARKINGS):
        donor, receiver = SOURCE[i],SOURCE[1-i]
        relation, h0 = indexed_word(apply(donor,chart))
        row, h1 = indexed_word(apply(receiver,chart))
        assert (h0,h1) == (0,1)
        caps = (2,4,6) if i == 0 else (2,3,4)
        result.append({"donor":donor,"receiver":receiver,
                       "tests":[audit(relation,row,degree) for degree in caps]})
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
