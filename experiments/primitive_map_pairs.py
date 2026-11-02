"""Exact primitive-loop decision by finite pairs of partial transformations.

Every positive primitive conjugacy class occurs in a positive Nielsen basis
built by (A,B)->(A,AB) and (AB,B). Partial vertex maps of a finite folded
graph form a finite semigroup. Complete pair-state exhaustion therefore
decides whether any primitive cyclic word labels a loop at any vertex.
The proof and limitations are in research-r.md; a budget stop is INCOMPLETE.
"""
import argparse
from collections import deque
import hashlib
import json
from pathlib import Path

LETTERS = 'xXyY'
ALPHABETS = ('xy', 'xY', 'Xy', 'XY')


def inverse(word):
    return word.swapcase()[::-1]


def reduce(word):
    stack = []
    for c in word:
        if c not in LETTERS:
            raise ValueError('invalid free letter')
        if stack and stack[-1] == c.swapcase():
            stack.pop()
        else:
            stack.append(c)
    return ''.join(stack)


def fold(words):
    """Local batch-identification fold; supports any finitely generated H."""
    edges = []
    size = 1
    for word in words:
        word = reduce(word)
        at = 0
        for i, c in enumerate(word):
            end = 0 if i == len(word)-1 else size
            if end:
                size += 1
            edges.append((at,c,end))
            edges.append((end,c.swapcase(),at))
            at = end
    parent = list(range(size))

    def root(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    while True:
        outgoing = {}
        changed = False
        for a,c,b in edges:
            a,b = root(a),root(b)
            if (a,c) in outgoing and root(outgoing[a,c]) != b:
                other = root(outgoing[a,c])
                parent[max(other,b)] = min(other,b)
                changed = True
            else:
                outgoing[a,c] = b
        if not changed:
            break
    arcs = {(root(a),c):root(b) for a,c,b in edges}
    names = {root(0):0}
    frontier = deque([root(0)])
    encoded = []
    while frontier:
        at = frontier.popleft()
        for c in LETTERS:
            end = arcs.get((at,c),-1)
            if end >= 0 and end not in names:
                names[end] = len(names)
                frontier.append(end)
            encoded.append(names[end] if end >= 0 else -1)
    validate_graph(encoded)
    return tuple(encoded)


def validate_graph(encoded):
    if not encoded or len(encoded) % 4:
        raise ValueError('graph must have four transition entries per vertex')
    size = len(encoded)//4
    if size > 255:
        raise ValueError('this byte-map implementation supports at most255 vertices')
    for i,end in enumerate(encoded):
        if not isinstance(end,int) or end < -1 or end >= size:
            raise ValueError('invalid graph vertex')
        if end >= 0:
            start,letter = divmod(i,4)
            if encoded[4*end+(letter^1)] != start:
                raise ValueError('inverse arc missing')
    reached = {0}
    frontier = deque([0])
    while frontier:
        at = frontier.popleft()
        for end in encoded[4*at:4*at+4]:
            if end >= 0 and end not in reached:
                reached.add(end)
                frontier.append(end)
    if len(reached) != size:
        raise ValueError('input graph must be connected to its distinguished vertex')
    return size


def compose(first,second,missing):
    """The map for word AB: follow A first, then B."""
    return bytes(missing if at == missing else second[at] for at in first)


def fixed_vertex(value):
    return next((at for at,end in enumerate(value) if at == end),None)


def follow(encoded,start,word):
    for c in word:
        start = encoded[4*start+LETTERS.index(c)]
        if start < 0:
            return -1
    return start


def base_path(encoded,target):
    frontier = deque([0])
    paths = {0:''}
    while frontier:
        at = frontier.popleft()
        if at == target:
            return paths[at]
        for i,c in enumerate(LETTERS):
            end = encoded[4*at+i]
            if end >= 0 and end not in paths:
                paths[end] = paths[at]+c
                frontier.append(end)
    raise ValueError('primitive loop lies in disconnected input graph')


def recover_program(nodes,index):
    program = []
    while nodes[index][1] is not None:
        program.append(nodes[index][2])
        index = nodes[index][1]
    return ''.join(program[::-1])


def witness(encoded,alphabet,program,component,vertex,max_expand=1000000):
    a,b = alphabet
    la = lb = 1
    explicit = True
    for operation in program:
        if operation == 'L':
            lb += la
            if explicit and lb <= max_expand:
                b = a+b
            else:
                explicit = False
        elif operation == 'R':
            la += lb
            if explicit and la <= max_expand:
                a = a+b
            else:
                explicit = False
        else:
            raise ValueError('invalid basis program')
    result = {'alphabet':alphabet,'positive_basis_program':program,
              'component':component,'loop_vertex':vertex,
              'word_length':(la,lb)[component]}
    path = base_path(encoded,vertex)
    result['base_to_loop_path'] = path
    if explicit:
        word = (a,b)[component]
        assert follow(encoded,vertex,word) == vertex
        based = reduce(path+word+inverse(path))
        assert follow(encoded,0,based) == 0
        result.update(cyclic_primitive_word=word,based_primitive_word=based)
    else:
        result['word_expansion_omitted_above_limit'] = max_expand
    return result


def one_alphabet(encoded,alphabet,budget,save_certificate=False):
    size = len(encoded)//4
    first,second = (bytes(size if encoded[4*v+LETTERS.index(c)] < 0 else
                          encoded[4*v+LETTERS.index(c)] for v in range(size))
                    for c in alphabet)
    nodes = [((first,second),None,None)]
    indices = {(first,second):0}
    position = 0
    while position < len(nodes):
        (a,b),parent,operation = nodes[position]
        for component,value in enumerate((a,b)):
            at = fixed_vertex(value)
            if at is not None:
                return {'status':'PRIMITIVE','alphabet':alphabet,
                        'pair_states_discovered':len(nodes),'pair_states_processed':position,
                        'witness':witness(encoded,alphabet,recover_program(nodes,position),component,at)}
        product = compose(a,b,size)
        for operation,pair in (('L',(a,product)),('R',(product,b))):
            if pair not in indices:
                if budget and len(nodes) >= budget:
                    return {'status':'INCOMPLETE','alphabet':alphabet,
                            'pair_states_discovered':len(nodes),'pair_states_processed':position,
                            'reason':'map_pair_state_budget'}
                indices[pair] = len(nodes)
                nodes.append((pair,position,operation))
        position += 1
    result = {'status':'ABSENT','alphabet':alphabet,
              'pair_states_discovered':len(nodes),'pair_states_processed':position,
              'complete_finite_map_pair_exhaustion':True}
    if save_certificate:
        result['closed_map_pairs'] = [[a.hex(),b.hex()] for ((a,b),_,_) in nodes]
    return result


def decide(encoded,budget=1000000,save_certificate=False):
    encoded = tuple(encoded)
    size = validate_graph(encoded)
    results = []
    for alphabet in ALPHABETS:
        result = one_alphabet(encoded,alphabet,budget,save_certificate)
        results.append(result)
        if result['status'] == 'PRIMITIVE':
            return {'format':'f2-primitive-map-pairs-v1','status':'PRIMITIVE',
                    'vertices':size,'encoded_graph':list(encoded),'alphabets':results,
                    'witness':result['witness']}
    status = 'ABSENT' if all(r['status']=='ABSENT' for r in results) else 'INCOMPLETE'
    return {'format':'f2-primitive-map-pairs-v1','status':status,
            'vertices':size,'encoded_graph':list(encoded),'alphabets':results,
            'ordinary_AC_goal_solved':False}


def compact_absence(certificate):
    """Pool repeated partial maps; retain every closed pair-state exactly."""
    assert certificate['status'] == 'ABSENT'
    size = certificate['vertices']
    maps = []
    names = {}
    alphabets = []
    for row in certificate['alphabets']:
        pairs = []
        for pair in row['closed_map_pairs']:
            indices = []
            for value in pair:
                value = bytes.fromhex(value)
                if value not in names:
                    names[value] = len(maps)
                    maps.append([[i,v] for i,v in enumerate(value) if v != size])
                indices.append(names[value])
            pairs.append(indices)
        alphabets.append({'alphabet':row['alphabet'],'closed_map_pair_indices':pairs})
    return {'format':'f2-primitive-map-pairs-compact-v1','status':'ABSENT',
            'vertices':size,'encoded_graph':certificate['encoded_graph'],
            'partial_maps_as_sparse_pairs':maps,'alphabets':alphabets,
            'ordinary_AC_goal_solved':False}


def expand_compact(certificate):
    assert certificate['format'] == 'f2-primitive-map-pairs-compact-v1'
    size = validate_graph(certificate['encoded_graph'])
    maps = []
    for sparse in certificate['partial_maps_as_sparse_pairs']:
        value = [size]*size
        positions = set()
        for position,end in sparse:
            assert type(position) is type(end) is int
            assert 0 <= position < size and 0 <= end < size
            assert position not in positions
            positions.add(position)
            value[position] = end
        maps.append(bytes(value))
    assert len(set(maps)) == len(maps)
    alphabets = []
    for row in certificate['alphabets']:
        pairs = []
        for indices in row['closed_map_pair_indices']:
            assert len(indices) == 2
            assert all(type(i) is int and 0 <= i < len(maps) for i in indices)
            pairs.append([maps[i].hex() for i in indices])
        alphabets.append({'status':'ABSENT','alphabet':row['alphabet'],
                          'closed_map_pairs':pairs})
    return {'format':'f2-primitive-map-pairs-v1','status':'ABSENT',
            'vertices':size,'encoded_graph':certificate['encoded_graph'],
            'alphabets':alphabets,'ordinary_AC_goal_solved':False}


def verify_absence(certificate):
    if certificate['format'] == 'f2-primitive-map-pairs-compact-v1':
        certificate = expand_compact(certificate)
    assert certificate['format'] == 'f2-primitive-map-pairs-v1'
    assert certificate['status'] == 'ABSENT'
    encoded = certificate['encoded_graph']
    size = validate_graph(encoded)
    assert tuple(row['alphabet'] for row in certificate['alphabets']) == ALPHABETS
    total = 0
    for row in certificate['alphabets']:
        assert row['status'] == 'ABSENT'
        pairs = {tuple(bytes.fromhex(v) for v in pair) for pair in row['closed_map_pairs']}
        assert len(pairs) == len(row['closed_map_pairs'])
        initial = tuple(bytes(size if encoded[4*v+LETTERS.index(c)] < 0 else
                              encoded[4*v+LETTERS.index(c)] for v in range(size))
                        for c in row['alphabet'])
        assert initial in pairs
        for a,b in pairs:
            assert len(a) == len(b) == size
            assert all(v <= size for value in (a,b) for v in value)
            assert fixed_vertex(a) is None and fixed_vertex(b) is None
            product = compose(a,b,size)
            assert (a,product) in pairs and (product,b) in pairs
        total += len(pairs)
    return {'status':'PASS','complete_absence_certificate':True,
            'vertices':size,'closed_map_pair_states_checked':total,
            'ordinary_AC_goal_solved':False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('words',nargs='*')
    parser.add_argument('--graph-json')
    parser.add_argument('--budget',type=int,default=1000000)
    parser.add_argument('--certificate')
    parser.add_argument('--verify')
    parser.add_argument('--output')
    args = parser.parse_args()
    if args.verify:
        result = verify_absence(json.loads(Path(args.verify).read_text()))
    else:
        encoded = json.loads(Path(args.graph_json).read_text()) if args.graph_json else fold(args.words)
        result = decide(encoded,args.budget,bool(args.certificate))
        if args.certificate:
            Path(args.certificate).write_text(json.dumps(result,indent=2)+'\n')
    if args.output:
        Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    display = dict(result)
    if 'alphabets' in display:
        display['alphabets'] = [{k:v for k,v in row.items() if k!='closed_map_pairs'} for row in display['alphabets']]
    print(json.dumps(display,indent=2))
