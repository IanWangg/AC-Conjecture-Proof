"""Agent I: the published residual landscape modulo Aut(F2).

For every component of nahomar's residual_components16_c28.txt flagged
trivial=0 (plus optional extra seeds), compute its component in D's full
cyclic-product graph to total length CAP (`d_acsearch --dumpkeys`), reduce every
state to its Whitehead-canonical Aut(F2)-orbit (`--autmatch --autdump`), and
union components that share an orbit.  Two components share an orbit iff some
state of one is an automorphic image of a state of the other, so (research-d
Lemma D2) they are simultaneously AC-trivial or not; if a union-find group
contains a class on which Aut(F2) is AC-realized (AK3: research-d Lemma D6;
C3, P1, P2: research-i Section 5), then every member of the group is
ordinary-AC-equivalent to it (transport each link by the accumulated
automorphism).  A component reaching a primitive relator is AC-trivial.

Usage:
  python3 experiments/i_landscape.py COMPONENTS.txt CAP WORKDIR [name:w1,w2 ...]
  python3 experiments/i_landscape.py --selftest
Needs $DACS (compiled experiments/d_acsearch.cpp) and numpy.
"""
import os
import subprocess
import sys

AUT_REALIZED = {"AK3", "C3", "P1", "P2"}


def parse_components(path):
    out = []
    for line in open(path):
        if not line.startswith("component"):
            continue
        f = line.split()
        d = dict(t.split("=", 1) for t in f if "=" in t)
        name = d["name"]
        i = f.index("seed=" + d["seed"])
        w1, w2 = f[i + 1], f[i + 2]
        out.append((name, w1, w2, d.get("trivial") == "1"))
    return out


class UF:
    def __init__(self, n):
        self.p = list(range(n))

    def find(self, a):
        while self.p[a] != a:
            self.p[a] = self.p[self.p[a]]
            a = self.p[a]
        return a

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a != b:
            self.p[max(a, b)] = min(a, b)


def groups_from_orbits(orbit_sets):
    """orbit_sets: list of numpy uint64 arrays (unique).  Returns UF."""
    import numpy as np
    uf = UF(len(orbit_sets))
    if not orbit_sets:
        return uf
    keys = np.concatenate(orbit_sets)
    owner = np.concatenate([np.full(len(s), i, dtype=np.int32) for i, s in enumerate(orbit_sets)])
    order = np.argsort(keys, kind="stable")
    keys, owner = keys[order], owner[order]
    same = np.nonzero(keys[1:] == keys[:-1])[0]
    for j in same:
        uf.union(int(owner[j]), int(owner[j + 1]))
    return uf


def run(comps, cap, work, extra):
    import numpy as np
    exe = os.environ.get("DACS", "d_acsearch")
    os.makedirs(work, exist_ok=True)
    items = [(n, a, b) for n, a, b, triv in comps if not triv] + extra
    orbit_sets, info = [], []
    for k, (name, a, b) in enumerate(items):
        kf = os.path.join(work, "k_%d.bin" % k)
        af = os.path.join(work, "a_%d.bin" % k)
        out = subprocess.run(["timeout", "1200", exe, "--cap", str(max(cap, len(a) + len(b))),
                              "--maxstates", "6000000", "--source", "%s,%s" % (a, b),
                              "--dumpkeys", "0", kf], capture_output=True, text=True).stdout
        triv = states = 0
        for line in out.splitlines():
            if line.startswith("trivializing_states"):
                triv = int(line.split()[1])
            if line.startswith("budget_hit"):
                states = int(line.split()[5])
        subprocess.run(["timeout", "1200", exe, "--autmatch", kf, "--autdump", af],
                       capture_output=True, text=True)
        s = np.unique(np.fromfile(af, dtype=np.uint64)) if os.path.exists(af) else np.zeros(0, np.uint64)
        orbit_sets.append(s)
        info.append((name, a, b, states, len(s), triv))
        for f in (kf, af):
            if os.path.exists(f):
                os.unlink(f)
        print("comp %d %s %s,%s states %d orbits %d trivial %d" % (k, name, a, b, states, len(s), triv), flush=True)
    uf = groups_from_orbits(orbit_sets)
    groups = {}
    for i in range(len(items)):
        groups.setdefault(uf.find(i), []).append(i)
    multi = [g for g in groups.values() if len(g) > 1]
    print("components %d groups %d merged_groups %d" % (len(items), len(groups), len(multi)))
    for g in sorted(multi, key=lambda g: -len(g)):
        names = [info[i][0] for i in g]
        genuine = any(n in AUT_REALIZED for n in names)
        print("GROUP size %d %s :: %s" % (len(g), "AC-class(Aut-realized)" if genuine else "same-status",
                                          " ".join("%s(%s,%s)" % (info[i][0], info[i][1], info[i][2]) for i in g)))
    for i, t in enumerate(info):
        if t[5]:
            print("TRIVIALIZED %s %s %s" % (t[0], t[1], t[2]))


def selftest():
    import numpy as np
    s = [np.array([1, 5, 9], np.uint64), np.array([2, 5], np.uint64), np.array([7], np.uint64),
         np.array([7, 11], np.uint64)]
    uf = groups_from_orbits(s)
    assert uf.find(0) == uf.find(1) and uf.find(2) == uf.find(3) and uf.find(0) != uf.find(2)
    print("i_landscape self-test passed")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["--selftest"]:
        selftest()
    else:
        extra = []
        for t in a[3:]:
            n, w = t.split(":")
            w1, w2 = w.split(",")
            extra.append((n, w1, w2))
        run(parse_components(a[0]), int(a[1]), a[2], extra)
