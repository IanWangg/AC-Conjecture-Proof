"""Agent I: which residual components are closed under the Nielsen generators?

For a seed P, if the exact cyclic reductions of swap(P), invx(P) and x_xy(P)
(x<->y, x->x^-1, x->xy) all lie in P's own component of D's cyclic-product
graph (d_acsearch --exact-targets, Sigma-matching), then P ~AC phi(P) for the
three Nielsen generators of Aut(F2), hence for every automorphism (research-d
Lemma D6).  Combined with i_landscape.py's union-find groups, every group that
contains such a seed is a single ordinary AC class (research-i Section 5).
The certificates for each found image are obtainable with i_certify.py path.

Usage:
  python3 experiments/i_autreal_sweep.py COMPONENTS.txt CAP [LANDSCAPE_LOG]
  python3 experiments/i_autreal_sweep.py --selftest
Needs $DACS.
"""
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from i_words import cyc, subst  # noqa: E402
from i_landscape import parse_components  # noqa: E402

GENS = {"swap": {"x": "y", "y": "x"}, "invx": {"x": "X", "y": "y"}, "x_xy": {"x": "xy", "y": "y"}}


def images(a, b):
    return {g: (cyc(subst(a, m)), cyc(subst(b, m))) for g, m in GENS.items()}


def realized(a, b, cap, exe):
    with tempfile.NamedTemporaryFile("w", suffix=".tgt", delete=False) as f:
        for g, (u, v) in images(a, b).items():
            f.write("%s %s %s\n" % (g, u, v))
        tf = f.name
    out = subprocess.run(["timeout", "1200", exe, "--cap", str(max(cap, len(a) + len(b))),
                          "--maxstates", "6000000", "--no-stop", "--maxhits", "0",
                          "--source", "%s,%s" % (a, b), "--exact-targets", tf],
                         capture_output=True, text=True).stdout
    os.unlink(tf)
    found = set()
    for line in out.splitlines():
        if line.startswith("HIT target "):
            found.add(line.split()[2])
    return found


def groups_from_log(path):
    groups = []
    for line in open(path):
        if line.startswith("GROUP"):
            body = line.split("::", 1)[1]
            groups.append([t.split("(")[0] for t in body.split()])
    return groups


def main(comp_file, cap, log=None):
    exe = os.environ.get("DACS", "d_acsearch")
    comps = [c for c in parse_components(comp_file) if not c[3]]
    real = set()
    for name, a, b, _ in comps:
        f = realized(a, b, cap, exe)
        if f == set(GENS):
            real.add(name)
        print("seed %s %s,%s found %s" % (name, a, b, ",".join(sorted(f)) or "-"), flush=True)
    print("aut_realized_seeds %d of %d: %s" % (len(real), len(comps), " ".join(sorted(real))))
    if log:
        gs = groups_from_log(log)
        genuine = [g for g in gs if any(n in real or n in ("AK3", "C3", "P1", "P2") for n in g)]
        print("groups %d genuine_AC_classes %d covering %d components" % (
            len(gs), len(genuine), sum(len(g) for g in genuine)))
        for g in genuine:
            print("GENUINE", " ".join(g))


def selftest():
    im = images("xxxYYYY", "xyxYXY")
    assert im["swap"] == ("yyyXXXX", "yxyXYX"), im["swap"]
    assert im["x_xy"][1] == cyc(subst("xyxYXY", {"x": "xy", "y": "y"}))
    print("i_autreal_sweep self-test passed")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["--selftest"]:
        selftest()
    else:
        main(a[0], int(a[1]), a[2] if len(a) > 2 else None)
