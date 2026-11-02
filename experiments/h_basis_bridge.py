"""Compile a labelled-core match to an actual ordinary-AC basis bridge.

Both pairs must be bases of their recorded rank-two subgroup core. The
compiler changes the global basepoint, rewrites both pairs in a spanning
tree basis, and uses M's existing strict formal-basis compiler. Formal
conjugations are transported to actual ambient words and fully expanded.
"""
import argparse
from collections import deque
import json
from pathlib import Path
from primitive_map_pairs import LETTERS,follow,inverse,reduce,validate_graph
from complete_primitive import complete
from elementary_verify import replay


def spanning_basis(encoded,base):
    validate_graph(encoded)
    paths = {base:''}
    frontier = deque([base])
    tree = set()

    def edge_key(a,c,b):
        return min((a,c,b),(b,c^1,a))

    while frontier:
        at = frontier.popleft()
        for c,letter in enumerate(LETTERS):
            end = encoded[4*at+c]
            if end >= 0 and end not in paths:
                paths[end] = paths[at]+letter
                tree.add(edge_key(at,c,end))
                frontier.append(end)
    edges = {edge_key(at,c,end) for at in range(len(encoded)//4)
             for c,end in enumerate(encoded[4*at:4*at+4]) if end >= 0}
    extra = sorted(edges-tree)
    assert len(extra) == 2, 'match must be a rank-two core'
    words = []
    arc_labels = {}
    for i,(a,c,b) in enumerate(extra):
        words.append(reduce(paths[a]+LETTERS[c]+inverse(paths[b])))
        arc_labels[a,c,b] = 'xy'[i]
        arc_labels[b,c^1,a] = 'XY'[i]

    def rewrite(word):
        current = base
        result = ''
        for letter in word:
            c = LETTERS.index(letter)
            end = encoded[4*current+c]
            assert end >= 0
            result += arc_labels.get((current,c,end),'')
            current = end
        assert current == base
        return reduce(result)

    def substitute(word):
        values = dict(zip('xy',words))
        values.update(X=inverse(words[0]),Y=inverse(words[1]))
        return reduce(''.join(values[c] for c in word))

    return paths,words,rewrite,substitute


def reverse_ledger(moves):
    result = []
    for move in reversed(moves):
        if move['op'] == 'invert':
            result.append(dict(move))
        elif move['op'] == 'conjugate':
            result.append(dict(move,g=move['g'].swapcase()))
        else:
            j = move['j']
            result += [{'op':'invert','i':j},dict(move),{'op':'invert','i':j}]
    return result


def compile_match(match):
    assert match['status'] == 'MATCH'
    graph = match['canonical_unbased_graph']
    forward = match['forward_rotated_pair']
    backward = match['reverse_pair']
    fb,rb = match['forward_original_base'],match['reverse_original_base']
    paths,z,rewrite,substitute = spanning_basis(graph,fb)
    p = paths[rb]
    conjugated = [reduce(p+w+inverse(p)) for w in backward]
    assert all(follow(graph,fb,w) == fb for w in conjugated+forward)
    r = list(map(rewrite,conjugated))
    f = list(map(rewrite,forward))
    assert list(map(substitute,r)) == conjugated
    assert list(map(substitute,f)) == forward
    ri = complete({'format':'ordinary-ac-elementary-v1','start':r,'target':r,'moves':[]})
    fi = complete({'format':'ordinary-ac-elementary-v1','start':f,'target':f,'moves':[]})
    replay(ri);replay(fi)
    state = list(backward)
    moves = []

    def emit(move):
        i = move['i']
        moves.append(move)
        if move['op'] == 'invert':
            state[i] = inverse(state[i])
        elif move['op'] == 'multiply':
            state[i] = reduce(state[i]+state[move['j']])
        else:
            state[i] = reduce(move['g']+state[i]+inverse(move['g']))

    def conjugate(i,word):
        for letter in word[::-1]:
            emit({'op':'conjugate','i':i,'g':letter})

    def transport(ledger):
        for move in ledger:
            if move['op'] == 'conjugate':
                conjugate(move['i'],substitute(move['g']))
            else:
                emit(dict(move))

    for i in (0,1):
        conjugate(i,p)
    assert state == conjugated
    transport(ri['moves'])
    assert state == z
    transport(reverse_ledger(fi['moves']))
    assert state == forward
    certificate = {'format':'ordinary-ac-elementary-v1','start':backward,
                   'target':forward,'moves':moves,
                   'scope':'Exact basis bridge between matched subgroup pairs; no full AK3 path asserted'}
    strict = replay(certificate)
    result = {'status':'PASS','ordinary_AC_goal_solved':False,
              'base_change_word':p,'spanning_tree_basis_words':z,
              'reverse_formal_basis':r,'forward_formal_basis':f,
              'formal_reverse_to_tree_strict_moves':len(ri['moves']),
              'formal_forward_to_tree_strict_moves':len(fi['moves']),
              'strict_subgroup_basis_bridge':strict,
              'formal_completion_compiler_shared_with_M':True}
    return certificate,result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('match')
    parser.add_argument('--certificate',required=True)
    parser.add_argument('--output',required=True)
    args = parser.parse_args()
    certificate,result = compile_match(json.loads(Path(args.match).read_text()))
    Path(args.certificate).write_text(json.dumps(certificate,indent=2)+'\n')
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
