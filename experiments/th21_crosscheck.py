"""th21_crosscheck.py -- research TH21: cross-check the C++ BS(1,2)-type test
of experiments/th21_bs12_scan.cpp (mode --words) against TH09's own test
(experiments/th09_killers.py, forward_bs_scan: d_whitehead.aut_canon((w,)) ==
aut_canon((R_BS,)) ) on random words, planted Aut-images of XyxYY and images
of other length-5/6 relators.  Usage:
  python3 experiments/th21_crosscheck.py SCANNER_BINARY [N] [word ...]
With explicit words, only those are tested (used to confirm a hit)."""
import os
import random
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import d_whitehead as W  # noqa: E402
import th09_killers as TH  # noqa: E402

INV = {"x": "X", "X": "x", "y": "Y", "Y": "y"}
MAPS = [{"x": "xy", "X": "YX"}, {"x": "xY", "X": "yX"}, {"y": "yx", "Y": "XY"}, {"y": "yX", "Y": "xY"},
        {"x": "yx", "X": "XY"}, {"x": "Yx", "X": "Xy"}, {"y": "xy", "Y": "YX"}, {"y": "Xy", "Y": "Yx"},
        {"x": "y", "X": "Y", "y": "x", "Y": "X"}, {"x": "X", "X": "x"}, {"y": "Y", "Y": "y"}]


def image(rng, w, steps, maxlen):
    for _ in range(steps):
        m = rng.choice(MAPS)
        v = W.cycred("".join(m.get(c, c) for c in w))
        if 0 < len(v) <= maxlen:
            w = v
    r = rng.randrange(len(w))
    w = w[r:] + w[:r]
    if rng.random() < 0.5:
        w = "".join(INV[c] for c in reversed(w))
    return w


def main():
    binary = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
    rng = random.Random(21)
    words = sys.argv[3:]
    if not words:
        for _ in range(n // 2):  # random cyclically reduced words
            w = W.cycred("".join(rng.choice("xXyY") for _ in range(rng.randint(4, 14))))
            if w:
                words.append(w)
        for base in ("XyxYY", "XyxYY", "xyxYXY", "xxYYY", "XyxYYY", "xxxYYYY", "XyyxYYY"):
            for _ in range(n // 14):
                words.append(image(rng, base, rng.randint(1, 12), 16))
    BS = W.aut_canon((TH.R_BS,))
    out = subprocess.run([binary, "--words"], input="\n".join(words) + "\n", capture_output=True, text=True).stdout.split("\n")
    res = {}
    for line in out:
        if line.strip():
            w, ml, v = line.split()
            res[w] = (int(ml), v == "1")
    agree = pos = 0
    for w in words:
        L, cf = W.aut_canon((w,))
        py = (L, cf) == BS
        ml, cc = res[w]
        if (L, py) == (ml, cc):
            agree += 1
        else:
            print("DISAGREE", w, "python", L, py, "c++", ml, cc)
        pos += py
        if len(sys.argv) > 3:
            print(w, "TH09 test: minimal length", L, "BS(1,2)-type" if py else "not BS(1,2)-type")
    print("crosscheck: %d words, %d agree (minimal length and verdict), %d BS(1,2)-type by TH09's test" % (len(words), agree, pos))


if __name__ == "__main__":
    main()
