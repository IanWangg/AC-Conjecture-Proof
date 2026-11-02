#!/usr/bin/env python3
"""Convert ACSolverX datasets (Fagan et al., "The Two-Hump Problem",
arXiv:2606.21611; https://github.com/Math-AI-Caltech/ACSolverX) into target
files for experiments/d_acsearch.cpp.  Standard library only.

Each dataset line is a Python literal: a flat list of 2*m integers
(1=x, 2=y, -1=x^-1, -2=y^-1, 0=padding), two zero-padded relators.
Output lines: "<id> <word1> <word2>" over x,X,y,Y.

Usage: python3 -I experiments/d_prepare_targets.py DATA_DIR OUT_DIR
Run with -I because the inputs are third-party files.
"""
import ast
import gzip
import os
import sys

LET = {1: "x", -1: "X", 2: "y", -2: "Y"}


def parse(line):
    v = ast.literal_eval(line.strip())
    m = len(v) // 2
    if len(v) != 2 * m:
        raise ValueError("odd length")
    out = []
    for block in (v[:m], v[m:]):
        word = [a for a in block if a != 0]
        if any(a not in LET for a in word):
            raise ValueError("bad letter")
        out.append("".join(LET[a] for a in word))
    return out


def convert(src, dst, tag):
    opener = gzip.open if src.endswith(".gz") else open
    n = bad = 0
    with opener(src, "rt") as f, open(dst, "w") as g:
        for i, line in enumerate(f):
            if not line.strip():
                continue
            try:
                w1, w2 = parse(line)
            except (ValueError, SyntaxError):
                bad += 1
                continue
            if not w1 or not w2:
                bad += 1
                continue
            g.write(f"{tag}:{i} {w1} {w2}\n")
            n += 1
    print(f"{src} -> {dst}: {n} presentations, {bad} skipped")


def selftest():
    assert parse("[-2, -2, -1, 2, 1, 0, 0, -2, 1, 0]") == ["YYXyx", "Yx"]
    print("self-test passed")


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        selftest()
        sys.exit(0)
    data, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    for name, tag in (("1190MS.txt", "MS"), ("AC19.txt", "AC19"),
                      ("AC19_extended.txt", "AC19X"), ("AC1M.txt.gz", "AC1M")):
        convert(os.path.join(data, name), os.path.join(out, tag + ".tgt"), tag)
