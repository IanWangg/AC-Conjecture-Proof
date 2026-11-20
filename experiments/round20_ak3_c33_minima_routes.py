"""Recover and strictly replay the ordinary cap-33 routes to its nine minima."""

import argparse
from functools import lru_cache
import json
from mmap import ACCESS_READ, mmap
from pathlib import Path
from struct import Struct
import subprocess
from tempfile import TemporaryDirectory

from round17_ak3_e22_ordinary import compile_path

ALPHABET = "xXyY"
RECORD = Struct("=4Q")
PAIR = Struct("=2Q")
MASK = (1 << 64)-1


def code(word):
    packed = 1
    for c in word:
        packed = (packed << 2) | ALPHABET.index(c)
    return packed


def word(key):
    chars = []
    while key > 1:
        chars.append(ALPHABET[key & 3])
        key >>= 2
    assert key == 1 and chars
    return "".join(reversed(chars))


def shard_number(pair):
    a,b = pair
    mixed = (a + 0x9e3779b97f4a7c15) & MASK
    mixed = ((mixed ^ (mixed >> 30)) * 0xbf58476d1ce4e5b9) & MASK
    mixed = ((mixed ^ (mixed >> 27)) * 0x94d049bb133111eb) & MASK
    return ((mixed ^ (mixed >> 31)) ^ b) & 127


def seed_parent(shards, pair):
    with (shards/f"unique.{shard_number(pair)}.bin").open("rb") as source:
        with mmap(source.fileno(),0,access=ACCESS_READ) as rows:
            low,high=0,len(rows)//RECORD.size
            while low < high:
                middle=(low+high)//2
                first,second,a,b=RECORD.unpack_from(rows,middle*RECORD.size)
                if pair==(first,second):
                    return a,b
                if pair < (first,second):
                    high=middle
                else:
                    low=middle+1
    return None


def trace(catalogue, ledger_tail, shards):
    with ledger_tail.open("rb") as source, mmap(source.fileno(),0,access=ACCESS_READ) as rows:
        @lru_cache(None)
        def parent(pair):
            wanted=PAIR.pack(*pair)
            at=rows.find(wanted)
            while at != -1:
                if at % RECORD.size == 0:
                    return PAIR.unpack_from(rows,at+PAIR.size)
                at=rows.find(wanted,at+1)
            return seed_parent(shards,pair)

        for first,second in catalogue:
            current=(code(first),code(second))
            path=[current]
            while (previous := parent(current)) is not None:
                if previous in path:
                    raise ValueError("orbit parent cycle")
                path.append(previous)
                current=previous
            route=[[word(a),word(b)] for a,b in reversed(path)]
            assert len(route)>1 and sum(map(len,route[0]))<=32
            yield {"cyclic_cap":33,"lower_anchor":route[0],"orbit_route":route}


def transport(catalogue, ledger_tail, shards, search, cap29, cap22, literal):
    minima = [line.split() for line in catalogue.read_text().splitlines()
              if sum(map(len,line.split())) == 17]
    assert len(minima)==9
    reports = []
    for anchored in trace(minima,ledger_tail,shards):
        with TemporaryDirectory() as scratch:
            work=Path(scratch)
            outer=work/"outer.json"
            outer.write_text(json.dumps(anchored)+"\n")
            paths = []
            start = anchored["lower_anchor"]
            for cap, targets in ((32,cap29),(29,cap22)):
                branch = work/f"back{cap}"
                summary = json.loads(subprocess.check_output(
                    [search, str(cap), "3000000", *start, branch, targets], stderr=subprocess.PIPE))
                if not summary["target_found"]:
                    raise RuntimeError(f"no cap-{cap} bridge from {start}")
                route = Path(str(branch)+".route.tsv")
                paths.append(route)
                start = route.read_text().splitlines()[-1].split()
            certificate, receipt = compile_path(outer,*paths,literal)
            reports.append({"native_ancestry":anchored,
                            "old_routes":[path.read_text().splitlines() for path in paths],
                            "strict_replay":receipt["final"],"certificate":certificate})
    return reports


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ("catalogue","ledger_tail","shards","search","cap29","cap22","literal"):
        parser.add_argument(name,type=Path)
    args=parser.parse_args()
    print(json.dumps(transport(**vars(args)),separators=(",",":")))
