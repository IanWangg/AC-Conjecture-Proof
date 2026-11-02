"""Agent I: landscape of shared-vertex torus-knot pairs T(a;p,q).

T(a;p,q) = (x^p y^q, x^a y x^-1 y).  With z = x^-1 y the pair is
(x^p (x z)^q, x^(a+1) z^2): torus-knot relators in the bases (x, xz) and (x, z),
which share the primitive element x.

Usage:
  python3 experiments/i_family.py --list A LMAX      # members, det, group triviality
  python3 experiments/i_family.py --run A LMAX CAP   # D's engine per member (needs $DACS)
  python3 experiments/i_family.py --selftest
The engine binary is experiments/d_acsearch.cpp compiled to $DACS.
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i_words import red, cyc, pw, inv  # noqa: E402


def T(a, p, q):
    return (cyc(pw("x", p) + pw("y", q)), cyc(pw("x", a) + "yX" + "y"))


def det(r1, r2):
    def es(w):
        return (w.count("x") - w.count("X"), w.count("y") - w.count("Y"))
    a, b = es(r1), es(r2)
    return a[0] * b[1] - a[1] * b[0]


def toint(w):
    return [{"x": 1, "X": -1, "y": 2, "Y": -2}[c] for c in w]


def group_trivial(r1, r2):
    import f_descent
    return f_descent.is_trivial_group(toint(r1), toint(r2), limit=300000)


def members(a, lmax):
    out = []
    for p in range(1, lmax):
        for q in range(-lmax, lmax + 1):
            if q == 0:
                continue
            r1, r2 = T(a, p, q)
            if len(r1) + len(r2) > lmax or not r1 or not r2:
                continue
            if abs(det(r1, r2)) != 1:
                continue
            out.append((p, q, r1, r2))
    return out


def run_engine(r1, r2, cap, maxstates=20000000, extra=()):
    exe = os.environ.get("DACS", "d_acsearch")
    cmd = ["timeout", "1500", exe, "--cap", str(cap), "--maxstates", str(maxstates),
           "--source", "%s,%s" % (r1, r2)] + list(extra)
    res = subprocess.run(cmd, capture_output=True, text=True)
    out = res.stdout
    info = {"cap": cap}
    for line in out.splitlines():
        if line.startswith("budget_hit"):
            f = line.split()
            info["budget_hit"] = int(f[1])
            info["last_complete"] = int(f[3])
            info["states"] = int(f[5])
        elif line.startswith("trivializing_states"):
            info["trivial"] = int(line.split()[1])
        elif line.startswith("PATH TRIVIAL") and "path" not in info:
            info["path"] = line
    return info


def selftest():
    r1, r2 = T(2, 4, 7)
    assert (r1, r2) == ("xxxxyyyyyyy", "xxyXy"), (r1, r2)
    # basis check: x^a y x^-1 y = x^(a+1) z^2 with y = x z
    for a in (2, 4, -4):
        z_img = {"x": "x", "y": "xz"}
        w = red(pw("x", a) + "xz" + "X" + "xz")
        assert w == red(pw("x", a + 1) + "zz"), w
    assert abs(det(*T(2, 4, 7))) == 1
    print("i_family self-test passed")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
    elif sys.argv[1] == "--list":
        a, lmax = int(sys.argv[2]), int(sys.argv[3])
        for p, q, r1, r2 in members(a, lmax):
            print(a, p, q, r1, r2, len(r1) + len(r2), "trivial_group=%s" % group_trivial(r1, r2))
    elif sys.argv[1] == "--run":
        a, lmax, cap = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
        for p, q, r1, r2 in members(a, lmax):
            g = group_trivial(r1, r2)
            info = run_engine(r1, r2, max(cap, len(r1) + len(r2)))
            print(a, p, q, r1, r2, len(r1) + len(r2), "grp=%s" % g,
                  "cap=%d states=%s complete=%s trivial=%s" % (
                      info["cap"], info.get("states"), info.get("last_complete"), info.get("trivial")),
                  flush=True)
