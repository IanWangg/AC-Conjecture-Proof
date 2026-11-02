"""Agent I: which published residual classes does a component meet up to Aut(F2)?

Uses D's engine (experiments/d_acsearch.cpp compiled to $DACS):
  --autmatch KEYS TARGETS  prints at most 50 AUTHIT lines, so we iterate,
  deleting every residual label already seen, until all hits are listed.

Targets: nahomar residual_classes16.txt converted to lines
  "R<line>_<len>_<label> w1 w2"  (label = the published component name).

Usage:
  python3 experiments/i_residual_merge.py KEYS.bin RESID.tgt [NAME]
  python3 experiments/i_residual_merge.py --convert residual_classes16.txt OUT.tgt
  python3 experiments/i_residual_merge.py --selftest
Output: one line "NAME labels L1:count L2:count ..." (counts = matching states,
complete only for the final iteration's labels).
"""
import os
import re
import subprocess
import sys
import tempfile


def labels_of(out):
    labs = {}
    for line in out.splitlines():
        m = re.match(r"AUTHIT state \[.*\] target (\S+)", line)
        if m:
            lab = m.group(1).split("_", 2)[2]
            labs[lab] = labs.get(lab, 0) + 1
    tot = 0
    for line in out.splitlines():
        if line.startswith("autmatch states"):
            tot = int(line.split(" hits ")[1].split()[0])
    return labs, tot


def merge(keys, tgt, name=""):
    exe = os.environ.get("DACS", "d_acsearch")
    lines = [l for l in open(tgt) if l.strip()]
    found = {}
    for _ in range(40):
        with tempfile.NamedTemporaryFile("w", suffix=".tgt", delete=False) as f:
            f.writelines(lines)
            tf = f.name
        out = subprocess.run(["timeout", "1500", exe, "--autmatch", keys, tf],
                             capture_output=True, text=True).stdout
        os.unlink(tf)
        labs, tot = labels_of(out)
        for k, v in labs.items():
            found[k] = found.get(k, 0) + v
        if tot <= 50 or not labs:
            break
        lines = [l for l in lines if l.split()[0].split("_", 2)[2] not in labs]
    print(name, "labels", " ".join("%s:%d" % kv for kv in sorted(found.items())), flush=True)
    return found


def convert(src, out):
    with open(out, "w") as f:
        for i, line in enumerate(open(src), 1):
            p = line.split()
            if len(p) >= 4:
                f.write("R%d_%s_%s %s %s\n" % (i, p[0], p[3], p[1], p[2]))


def selftest():
    sample = ("AUTHIT state [xy xY] target R3_14_C3\nAUTHIT state [xy xY] target R9_15_R74\n"
              "autmatch states 10 closure_fail 0 targets 2 target_fail 0 hits 2 min_aut_length 14\n")
    labs, tot = labels_of(sample)
    assert labs == {"C3": 1, "R74": 1} and tot == 2, (labs, tot)
    print("i_residual_merge self-test passed")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["--selftest"]:
        selftest()
    elif a[:1] == ["--convert"]:
        convert(a[1], a[2])
    else:
        merge(a[0], a[1], a[2] if len(a) > 2 else "")
