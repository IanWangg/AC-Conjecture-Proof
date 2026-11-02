"""Agent I: turn d_acsearch output into strict ordinary-AC certificates.

Wraps experiments/d_certify.py (independent re-finding of every cyclic product)
and experiments/f_descent.py (strict ACM descent, for finishing a state that
already has a primitive relator).  Every written certificate is replayed by
experiments/elementary_verify.py before it is saved.

Usage:
  python3 experiments/i_certify.py path RUN.txt TAG S1 S2 T1 T2 OUT.json
      RUN.txt line "PATH TAG len N : [a b] [c d] ..." ; certificate S -> T exactly
  python3 experiments/i_certify.py coll RUN.txt I-J S1 S2 T1 T2 OUT.json
      "COLLISION I-J" block: COLL_A path from source I, COLL_B from source J;
      certificate S (source I) -> T (source J) exactly
  python3 experiments/i_certify.py trivial RUN.txt S1 S2 OUT.json
      first "PATH TRIVIAL" line, then strict descent to (x, y)
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import d_certify  # noqa: E402
import elementary_verify as ev  # noqa: E402


def parse_states(line):
    return [tuple(s.split()) for s in re.findall(r"\[([^\]]*)\]", line)]


def find_line(run, prefix):
    for line in open(run):
        if line.startswith(prefix):
            return line
    raise SystemExit("no line starting with %r" % prefix)


def save(cert, out, desc):
    cert["description"] = desc
    r = ev.replay(cert)
    with open(out, "w") as f:
        json.dump(cert, f, indent=0)
    print(json.dumps({"path": out, **r}))


def main(argv):
    mode = argv[0]
    if mode == "path":
        run, tag, s1, s2, t1, t2, out = argv[1:8]
        states = parse_states(find_line(run, "PATH %s " % tag))
        cert = d_certify.certificate(states, (s1, s2), (t1, t2), "")
        save(cert, out, "engine PATH %s via d_certify" % tag)
    elif mode == "coll":
        run, ij, s1, s2, t1, t2, out = argv[1:8]
        lines = open(run).read().splitlines()
        k = lines.index(next(l for l in lines if l.startswith("COLLISION %s " % ij)))
        a = parse_states(lines[k + 1])
        b = parse_states(lines[k + 2])
        # COLL_A belongs to whichever source was being expanded; orient it
        if d_certify.canon_pair(*a[0]) != d_certify.canon_pair(s1, s2):
            a, b = b, a
        states = a + list(reversed(b))
        cert = d_certify.certificate(states, (s1, s2), (t1, t2), "")
        save(cert, out, "engine collision %s (COLL_A + reversed COLL_B) via d_certify" % ij)
    elif mode == "trivial":
        run, s1, s2, out = argv[1:5]
        states = parse_states(find_line(run, "PATH TRIVIAL"))
        end = states[-1]
        c1 = d_certify.certificate(states, (s1, s2), end, "")
        import f_descent
        import f_thicken as T
        c2 = f_descent.certificate(T.parse(end[0]), T.parse(end[1]), K=3, beam=200)
        if c2 is None:
            raise SystemExit("descent failed from %s" % (end,))
        assert c2["start"] == list(end), (c2["start"], end)
        cert = {"format": "ordinary-ac-elementary-v1", "start": [s1, s2], "target": ["x", "y"],
                "moves": c1["moves"] + c2["moves"]}
        save(cert, out, "engine path to a primitive-relator state (d_certify), then strict descent (f_descent)")
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
