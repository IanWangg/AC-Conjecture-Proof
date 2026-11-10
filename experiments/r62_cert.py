#!/usr/bin/env python3
"""Agent R6-2: certificate P2 = (XyyxYYY, XXXYxxY) -> (r4, w0) = (XyyyyxYYYYY, xxyyXY):
D's certificate d_ms2b_to_ms0722.json (P2 -> (YYYYYXyyyyx, YYXyXyx)), then rotate the
first relator to r4 by letter conjugations, then one r4-frozen ACM move (YYXyXyx)^{+-1} -> w0
compiled with TH18's exact BS(4,5) conjugacy path (th18_bs.bs_path / compile_path).
    PYTHONDONTWRITEBYTECODE=1 python3 experiments/r62_cert.py certificates
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import th18_bs as B
R4, W0 = 'XyyyyxYYYYY', 'xxyyXY'
def main(outdir):
    d = json.load(open('certificates/d_ms2b_to_ms0722.json'))
    moves = list(d['moves']); state = list(d['target'])
    # rotate first relator YYYYYXyyyyx -> XyyyyxYYYYY by conjugating with single letters
    while state[0] != R4:
        g = B.inv(state[0][0]); moves.append({"op": "conjugate", "i": 0, "g": g})
        state[0] = B.red(g + state[0] + B.inv(g))
        assert len(state[0]) == len(R4)
    for cand, inverted in ((state[1], False), (B.inv(state[1]), True)):
        try:
            path = B.bs_path(cand, W0, 4); break
        except ValueError:
            path = None
    assert path is not None, "not conjugate in BS(4,5)"
    if inverted:
        moves.append({"op": "invert", "i": 1}); state[1] = B.inv(state[1])
    B.compile_path(path, state, 1, moves)
    assert state == [R4, W0], state
    cert = {"format": "ordinary-ac-elementary-v1", "start": d['start'], "target": state, "moves": moves,
            "description": "P2 -> (r4, w0) = (XyyyyxYYYYY, xxyyXY): research-d d_ms2b_to_ms0722.json, rotation, "
                           "one r4-frozen ACM move (TH18 bs_path); w0 = alpha(c), alpha = (x->xy, y->Y). Agent R6-2."}
    p = os.path.join(outdir, 'r62_p2_to_r4_w0.json'); json.dump(cert, open(p, 'w'))
    print(p, len(moves), "moves; inverted:", inverted)
if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else 'certificates')
