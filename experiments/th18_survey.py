#!/usr/bin/env python3
"""TH18 survey: exact BS(n,n+1)-conjugacy classes of the short relators of
Miller-Schupp presentations (repository certificates and, optionally, the
public 1190-presentation benchmark file).

  python3 experiments/th18_survey.py --selftest
  python3 experiments/th18_survey.py --certs            # D/L certificate endpoints
  python3 -I experiments/th18_survey.py --bench FILE    # all_presentations.txt (third-party data)
  python3 -I experiments/th18_survey.py --triage FILE SOLVED_FILE
  python3 -I experiments/th18_survey.py --certify FILE [OUTDIR LINE ...]
"""
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import th18_bs as B  # noqa: E402


def bs_n(r):
    """n if r is a rotation of rel(n)^{+-1}, else None."""
    r = B.red(r)
    for n in range(1, 12):
        R = B.rel(n)
        if len(R) == len(r) and any(R[k:] + R[:k] in (r, B.inv(r)) for k in range(len(R))):
            return n
    return None


def key(w, n):
    """Class of w^{+-1} (normalised to x-exponent +1) and a short name."""
    if B.xexp(w) < 0:
        w = B.inv(w)
    c = B.cls(w, n)
    name = "l=%d" % c[0]
    if c[0] == 3:
        N = n * (n + 1)
        b = B.label3(w, n)[1]
        b = b if 2 * b <= N else b - N
        kind = "divisor" if (n % abs(b) == 0 or (n + 1) % abs(b) == 0) else \
            ("bridge" if abs(b) == (N - 2 * n - 1 if 2 * (2 * n + 1) > N else 2 * n + 1) else "other")
        name += " C_%d (%s)" % (b, kind)
    elif c[0] > 3:
        name += " d=%s a=%s" % ("".join("+" if e > 0 else "-" for e in c[1]), list(c[2]))
    return c, name


def mirror(w):
    return w.translate(str.maketrans("yY", "Yy"))


def survey_certs():
    root = os.path.join(HERE, "..", "certificates")
    for pat, which in (("d_ak3_to_ms*.json", "target"), ("d_ms2a_to_ms*.json", "target"),
                       ("d_ms2b_to_ms*.json", "target"), ("l_ms*_trivialization.json", "start")):
        table = {}
        files = sorted(glob.glob(os.path.join(root, pat)))
        for f in files:
            r, w = json.load(open(f))[which]
            n = bs_n(r)
            if n is None:
                table.setdefault(("non-BS first relator", "-"), []).append(os.path.basename(f))
                continue
            c, name = key(w, n)
            table.setdefault((n, name), []).append(os.path.basename(f)[-21:-5] if which == "target" else w)
        print("%s: %d files" % (pat, len(files)))
        for (n, name), fs in sorted(table.items(), key=str):
            print("   n=%s  %-40s %3d" % (n, name, len(fs)))
    return 0


def survey_bench(path):
    letters = {1: "x", -1: "X", 2: "y", -2: "Y"}
    rows = [json.loads(line) for line in open(path) if line.strip()]
    stats, ex = {}, {}
    for idx, row in enumerate(rows):
        half = len(row) // 2
        r = "".join(letters[v] for v in row[:half] if v)
        w = "".join(letters[v] for v in row[half:] if v)
        n = bs_n(r)
        c, name = key(w, n)
        if c[0] >= 5:
            name = "l=%d" % c[0]
        stats[(n, name)] = stats.get((n, name), 0) + 1
        ex.setdefault((n, name), (idx, w))
    print("%d presentations" % len(rows))
    for k in sorted(stats):
        print("   n=%d  %-28s %4d   first: line %d, w = %s" % (k[0], k[1], stats[k], ex[k][0], ex[k][1]))
    return rows


def triage(bench, solved):
    """Cross-tabulate theory status against a list of presentations reported solved."""
    letters = {1: "x", -1: "X", 2: "y", -2: "Y"}
    dec = lambda row: ("".join(letters[v] for v in row[:len(row) // 2] if v),
                       "".join(letters[v] for v in row[len(row) // 2:] if v))
    done = {dec(json.loads(line)) for line in open(solved) if line.strip()}
    tab, new = {}, []
    for idx, line in enumerate(open(bench)):
        r, w = dec(json.loads(line))
        n = bs_n(r)
        c, name = key(w, n)
        st = "T3 (l=1): AC-trivial" if c[0] == 1 else "T6 (divisor class): AC-trivial" if "divisor" in name \
            else "bridge class: ~ AK(%d) or its mirror" % n if "bridge" in name \
            else "l=3, other class" if c[0] == 3 else "l>=5"
        k = (st, (r, w) in done)
        tab[k] = tab.get(k, 0) + 1
        if "AC-trivial" in st and (r, w) not in done:
            new.append((idx, n, w, name))
    for k in sorted(tab):
        print("   %-40s reported solved: %-5s %4d" % (k[0], k[1], tab[k]))
    return new


def certify(bench, outdir=None, lines=()):
    """Generate and replay (strict verifier) a certificate for EVERY benchmark
    presentation covered by T3 (t-length 1) or T6 (divisor class); store those in `lines`."""
    import elementary_verify as EV
    letters = {1: "x", -1: "X", 2: "y", -2: "Y"}
    cnt, mx = {"T3": 0, "T6": 0}, 0
    for idx, line in enumerate(open(bench)):
        row = json.loads(line)
        r = "".join(letters[v] for v in row[:len(row) // 2] if v)
        w = "".join(letters[v] for v in row[len(row) // 2:] if v)
        n = bs_n(r)
        c, name = key(w, n)
        if r != B.rel(n) or not (c[0] == 1 or "divisor" in name):
            continue
        cert = B.cert_len1(n, w) if c[0] == 1 else B.cert_divisor(n, w)
        res = EV.replay(cert)
        assert cert["start"] == [r, w] and res["endpoint"] == ["x", "y"]
        cnt["T3" if c[0] == 1 else "T6"] += 1
        mx = max(mx, res["moves"])
        if outdir and idx in lines:
            cert["description"] += "; Miller-Schupp benchmark line %d (0-based)" % idx
            with open(os.path.join(outdir, "th18_ms%04d_trivialization.json" % idx), "w") as f:
                json.dump(cert, f, separators=(",", ":"))
    print("certificates generated and replayed: %s; longest has %d moves" % (cnt, mx))


def selftest():
    assert bs_n("YYYYXyyyx") == 3 and bs_n("XyyxYYY") == 2 and bs_n("xyxYXY") is None
    assert key("XYxxY", 3)[1] == "l=3 C_-5 (bridge)" and key("YXXYx", 3)[1] == "l=3 C_5 (bridge)"
    assert key("xxYXy", 3)[1] == "l=3 C_-1 (divisor)" and key("xxyyXy", 3)[1] == "l=3 C_2 (divisor)"
    assert key("XYxxY", 2)[1] == "l=3 C_-1 (divisor)" and key("xy", 5)[1] == "l=1"
    assert key(mirror("XYxxY"), 4)[0] != key("XYxxY", 4)[0]
    print("th18_survey self-test passed")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
    elif sys.argv[1:] == ["--certs"]:
        survey_certs()
    elif len(sys.argv) == 4 and sys.argv[1] == "--triage":
        for row in triage(sys.argv[2], sys.argv[3]):
            print("   not in the solved list, AC-trivial by T3/T6: line %d  n=%d  w=%s  %s" % row)
    elif len(sys.argv) >= 3 and sys.argv[1] == "--certify":
        certify(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None, [int(v) for v in sys.argv[4:]])
    elif len(sys.argv) == 3 and sys.argv[1] == "--bench":
        survey_bench(sys.argv[2])
    else:
        print(__doc__)
