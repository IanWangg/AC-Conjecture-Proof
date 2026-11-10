"""TH14: generate rank-3 certificates for Theorem A of research-th14.md (STABLE, one stabilization).

  python3 experiments/th14_cert.py invy R1 R2 OUT.json   # (R1,R2,z) -> (R1(x,y^-1), R2(x,y^-1), z)
  python3 experiments/th14_cert.py --selftest

Construction (Theorem A): eps_y = sigma_y eps_z sigma_y with sigma_y = (y z).  The standard sequence S_y(U):
(U,z) -> (U[y:=z], y) needs an explicit expression y^-1 = prod g_k r_{j_k}^{e_k} g_k^-1, found here by a
deterministic best-first search (a proof that y = 1 in the group).  The certificate is checked by
experiments/th14_verify3.py; nothing here is trusted.
"""
import heapq
import json
import sys

INV = {c: c.swapcase() for c in 'xXyYzZ'}


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


def derive(start, rels, cap=28, maxnodes=1200000):
    """Best-first search over w -> red(w[:i] + R + w[i:]), R a cyclic rotation of r_j^{+-1} cancelling at
    least one letter.  Returns [(j, eps, g)] with start * prod_k g_k r_{j_k}^{eps_k} g_k^-1 = 1, or None."""
    rots = []
    for j, r in enumerate(rels):
        for eps, s in ((1, r), (-1, inv(r))):
            for k in range(len(s)):
                rots.append((s[k:] + s[:k], j, eps, s[:k]))
    seen, pq, cnt = {start: None}, [(len(start), 0, start)], 0
    while pq:
        _, _, w = heapq.heappop(pq)
        if w == '':
            path, cur = [], w
            while seen[cur] is not None:
                cur, mv = seen[cur]
                path.append(mv)
            return path[::-1]
        if cnt > maxnodes:
            return None
        for i in range(len(w) + 1):
            for R, j, eps, pre in rots:
                left = i > 0 and R[0] == INV[w[i - 1]]
                right = i < len(w) and R[-1] == INV[w[i]]
                if not (left or right):
                    continue
                v = red(w[:i] + R + w[i:])
                if len(v) > cap or v in seen:
                    continue
                seen[v] = (w, (j, eps, red(inv(w[i:]) + inv(pre))))
                cnt += 1
                heapq.heappush(pq, (len(v), cnt, v))
    return None


def S_y(U, path):
    """Macro sequence (U[0], U[1], z) -> (U[0][y:=z], U[1][y:=z], y);  path: y * prod = 1 over U."""
    sw = str.maketrans('yYzZ', 'zZyY')
    seq = [('M', 2, j, eps, g) for (j, eps, g) in path]                    # z -> z y^-1
    for k in (0, 1):
        r = U[k]
        for pos, c in enumerate(r):
            v = r[pos + 1:]                                                # untouched suffix
            if c == 'y':
                seq.append(('M', k, 2, 1, red(inv(v) + 'Y')))              # u y v -> u z v
            elif c == 'Y':
                seq.append(('M', k, 2, -1, inv(v)))                        # u Y v -> u Z v
    seq.append(('C', 2, 'Z'))                                              # z Y -> Y z
    seq += [('M', 2, j, eps, g.translate(sw)) for (j, eps, g) in path]     # Y z -> Y
    seq.append(('I', 2))
    return seq


def transport(seq, m):
    """Apply a signed letter permutation m (dict on x,y,z) to a macro sequence."""
    full = dict(m)
    full.update({INV[a]: INV[b] for a, b in m.items()})
    f = lambda w: ''.join(full[c] for c in w)
    return [(t[0], t[1], f(t[2])) if t[0] == 'C' else t if t[0] == 'I' else t[:4] + (f(t[4]),) for t in seq]


def expand(seq):
    out = []
    for t in seq:
        if t[0] == 'I':
            out.append({'op': 'invert', 'i': t[1]})
        elif t[0] == 'C':
            out.append({'op': 'conjugate', 'i': t[1], 'g': t[2]})
        else:
            _, i, j, eps, g = t
            out += [{'op': 'conjugate', 'i': j, 'g': c} for c in reversed(g)]
            if eps < 0:
                out.append({'op': 'invert', 'i': j})
            out.append({'op': 'multiply', 'i': i, 'j': j})
            if eps < 0:
                out.append({'op': 'invert', 'i': j})
            out += [{'op': 'conjugate', 'i': j, 'g': INV[c]} for c in g]
    return out


def cert_invy(r1, r2, cap=28, maxnodes=1200000):
    U = (red(r1), red(r2))
    path = derive('y', U, cap, maxnodes)
    if path is None:
        raise SystemExit('no derivation of y found within the bounds')
    s = S_y(U, path)
    seq = s + [('I', 2)] + transport(s, {'x': 'x', 'y': 'z', 'z': 'Y'})    # psi = sigma_y eps_z
    fl = str.maketrans('yY', 'Yy')
    return {'format': 'stable1-ac-elementary-rank3-v1', 'start': [U[0], U[1], 'z'],
            'target': [U[0].translate(fl), U[1].translate(fl), 'z'], 'moves': expand(seq),
            'macro_moves': sum(t[0] == 'M' for t in seq), 'area_y_used': len(path),
            'description': 'STABLE (one stabilization, rank 3): (r1,r2,z) -> (r1(x,y^-1), r2(x,y^-1), z) by '
                           'Theorem A of research-th14.md (eps_y = sigma_y eps_z sigma_y). Not an ordinary '
                           'rank-2 AC equivalence.'}


def selftest():
    from th14_verify3 import replay
    c = cert_invy('xxYYY', 'xyxYXY', cap=20, maxnodes=200000)             # AK(2)
    r = replay(c)
    assert r['stable1'] and r['endpoint'] == ['xxyyy', 'xYxyXy', 'z'], r
    c = cert_invy('xy', 'y')                                               # a basis
    assert replay(c)['endpoint'] == ['xY', 'Y', 'z']
    print('th14_cert self-test passed (AK(2): %d moves)' % r['moves'])


if __name__ == '__main__':
    if sys.argv[1:] == ['--selftest']:
        selftest()
    elif len(sys.argv) == 5 and sys.argv[1] == 'invy':
        c = cert_invy(sys.argv[2], sys.argv[3])
        json.dump(c, open(sys.argv[4], 'w'))
        print('written', sys.argv[4], 'moves', len(c['moves']), 'macro', c['macro_moves'], 'area_y', c['area_y_used'])
