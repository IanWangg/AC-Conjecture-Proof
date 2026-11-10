"""TH14: Stallings-graph tools for the stable exits of research-th14.md (standard library only).

Words over x,y with X,Y the inverses.  A subgroup K = <w1,...,wk> of F(x,y) is represented by its
based folded Stallings graph.  Used for
  corank1(K)      : is there t with <K,t> = F2 ?  (iff identifying two vertices of the graph folds to the rose;
                    proof in research-th14.md, Lemma E1)
  overgroups(K)   : all folded quotients of the graph (= all subgroups H >= K that are "principal quotients");
                    every rank-2 subgroup H >= K (K noncyclic, K != H) occurs among them (Takahasi).
  factor(K-words) : for each proper rank-2 quotient H: a basis (p,q) of H and the rewriting W of the words.
Self-test: python3 experiments/th14_stallings.py --selftest
"""
import sys
from itertools import product

INV = {'x': 'X', 'X': 'x', 'y': 'Y', 'Y': 'y'}


def red(w):
    out = []
    for c in w:
        if out and out[-1] == INV[c]:
            out.pop()
        else:
            out.append(c)
    return ''.join(out)


def inv(w):
    return ''.join(INV[c] for c in reversed(w))


def cyc(w):
    w = red(w)
    while len(w) >= 2 and w[0] == INV[w[-1]]:
        w = w[1:-1]
    return w


def fold(n, edges, merges=()):
    """n vertices, edges = iterable of (u, 'x'|'y', v); merges = pairs to identify.  Returns the folded
    based graph in canonical BFS labelling from vertex 0: tuple of (u, letter, v), plus vertex count."""
    par = list(range(n))

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    for a, b in merges:
        par[find(a)] = find(b)
    edges = list(edges)
    while True:
        fw, bw, merged = {}, {}, False
        for u, l, v in edges:
            u, v = find(u), find(v)
            for d, key, val in ((fw, (u, l), v), (bw, (v, l), u)):
                o = d.get(key)
                if o is None:
                    d[key] = val
                elif find(o) != find(val):
                    par[find(o)] = find(val)
                    merged = True
        if not merged:
            break
    # canonical relabel by BFS from find(0), letters in order x, X, y, Y
    root = find(0)
    lab, order, i = {root: 0}, [root], 0
    out = set()
    while i < len(order):
        u = order[i]
        i += 1
        for l in 'xy':
            for d, sign in ((fw, 1), (bw, -1)):
                v = d.get((u, l))
                if v is None:
                    continue
                v = find(v)
                if v not in lab:
                    lab[v] = len(order)
                    order.append(v)
                out.add((lab[u], l, lab[v]) if sign == 1 else (lab[v], l, lab[u]))
    return tuple(sorted(out)), len(order)


def stallings(words):
    edges, n = [], 1
    for w in words:
        w = red(w)
        cur = 0
        for k, c in enumerate(w):
            nxt = 0 if k == len(w) - 1 else n
            if nxt:
                n += 1
            edges.append((cur, c, nxt) if c in 'xy' else (nxt, INV[c], cur))
            cur = nxt
    return fold(n, edges)


def rank(g):
    return len(g[0]) - g[1] + 1


def is_rose(g):
    return g[1] == 1 and len(g[0]) == 2


def corank1(g):
    """Return a pair (u,v) whose identification folds to the rose, or None."""
    E, n = g
    for u in range(n):
        for v in range(u + 1, n):
            if is_rose(fold(n, E, [(u, v)])):
                return (u, v)
    return None


def quotients(g, limit=200000):
    """All folded quotients of g (closure under single identifications)."""
    seen, todo = {g}, [g]
    while todo:
        E, n = todo.pop()
        for u in range(n):
            for v in range(u + 1, n):
                h = fold(n, E, [(u, v)])
                if h not in seen:
                    seen.add(h)
                    todo.append(h)
                    if len(seen) > limit:
                        raise RuntimeError('quotient limit')
    return seen


def basis_and_rewriter(g):
    """Spanning tree by BFS; returns (basis words, function rewriting a word of the subgroup in that basis
    using letters x,y,(z..) for the non-tree edges)."""
    E, n = g
    nb = {u: [] for u in range(n)}
    for (u, l, v) in E:
        nb[u].append((l, v, (u, l, v)))
        nb[v].append((INV[l], u, (u, l, v)))
    path, tree, order = {0: ''}, set(), [0]
    for u in order:
        for l, v, e in sorted(nb[u]):
            if v not in path:
                path[v] = path[u] + l
                tree.add(e)
                order.append(v)
    nontree = sorted(e for e in E if e not in tree)
    names = 'xyzuvw'
    basis = [red(path[u] + l + inv(path[v])) for (u, l, v) in nontree]
    step = {}
    for (u, l, v) in E:
        step[(u, l)] = (v, (u, l, v), 1)
        step[(v, INV[l])] = (u, (u, l, v), -1)

    def rewrite(w):
        cur, out = 0, []
        for c in red(w):
            if (cur, c) not in step:
                return None
            cur, e, s = step[(cur, c)]
            if e in nontree:
                a = names[nontree.index(e)]
                out.append(a if s == 1 else a.upper())
        if cur != 0:
            return None
        return ''.join(out)
    return basis, rewrite


def subst(w, p, q):
    m = {'x': p, 'y': q, 'X': inv(p), 'Y': inv(q)}
    return red(''.join(m[c] for c in w))


def words_upto(L):
    out = ['']
    for n in range(1, L + 1):
        for t in product('xXyY', repeat=n):
            w = ''.join(t)
            if red(w) == w:
                out.append(w)
    return out


def selftest():
    assert is_rose(stallings(['x', 'y'])) and is_rose(stallings(['xy', 'y']))
    g = stallings(['xx', 'y'])
    assert g[1] == 2 and rank(g) == 2 and corank1(g) is not None        # <x^2,y,x> = F
    g = stallings(['xx', 'yy'])
    assert rank(g) == 2 and corank1(g) is None                          # needs two more generators
    g = stallings(['XXYx', 'y'])                                        # (x^-2 y^-1 x, y): corank 1 via t = x
    assert not is_rose(g) and corank1(g) is not None
    # rewriting: K = <x^2 y^-1 x^-2... > inside H = <x^2, y>
    h = stallings(['xx', 'y'])
    basis, rw = basis_and_rewriter(h)
    w = 'xxyXXY'
    r = rw(w)
    assert r is not None and subst(r, basis[0], basis[1]) == red(w), (basis, r)
    assert rw('x') is None
    # quotients of the graph of <x^2,y^2> include the rose and <x,y^2>, <x^2,y>
    qs = quotients(stallings(['xx', 'yy']))
    assert stallings(['x', 'y']) in qs and stallings(['x', 'yy']) in qs and stallings(['xx', 'y']) in qs
    # AK(2) relators: no claim, just exercise
    g = stallings(['xxYYY', 'xyxYXY'])
    assert rank(g) == 2
    print('th14_stallings self-test passed')


if __name__ == '__main__':
    if sys.argv[1:] == ['--selftest']:
        selftest()
