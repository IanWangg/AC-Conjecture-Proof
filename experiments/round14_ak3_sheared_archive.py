"""Enlarge verified trivial endpoints by one ambient Nielsen shear."""

import argparse
import json
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from hashlib import sha256
from pathlib import Path

from elementary_verify import inverse, reduce, replay
from free_waypoint_search import canonical, conj_ops
from round05_ak3_orbit_audit import MAPS
from round07_automorphism_transport import normalize_pair
from round08_ak3_acm_search import cyclic_peak
from round10_ac_proof_blocks import vectors
from round11_ak3_targeted_acm import BASIS, reverse_suffix
from round12_ac_proof_amalgam_archive import BETA_INV, check, height, substitute
from round12_ac_proof_amalgam_archive import reduce as fiber_reduce
from round12_ak3_reciprocal_charts import (
    chart,
    chart_summary,
    ledger_for_join,
    reverse_index,
)
from round12_ak3_torus_chart import signature

ROOT = Path(__file__).resolve().parents[1]
SHEARS = (("xy", "y"), ("xY", "y"), ("x", "yx"), ("x", "yX"))
SEEDS = (
    ("round11_ak3_cap32_minimum.json", "xxxxxyXXy", "xxyxxyyXYXY"),
    ("round12_ak3_second_energy20.json", "xxxxyXXYY", "xxyyxYYYxxY"),
)


def images(shear, signed_marking):
    x, y = (word.translate(MAPS[signed_marking]) for word in SHEARS[shear])
    return {"x": x, "X": inverse(x), "y": y, "Y": inverse(y)}


def transport(word, mark):
    return reduce("".join(mark[letter] for letter in word))


@lru_cache(maxsize=200000)
def shear_word(word, shear):
    return canonical(transport(word, images(shear, 0)))


@lru_cache(maxsize=400000)
def signed_key(word, marking):
    return canonical(word.translate(MAPS[marking]))


def index(archive, energy):
    """Keep the marked partner pairs absent from the original archive."""
    origins = json.loads(archive.with_suffix(".sources.json").read_text())
    rows = [tuple(row.split()) for row in archive.read_text().splitlines()]
    assert len(origins) == len(rows)
    previous, _ = reverse_index(archive, 56)
    fresh = defaultdict(dict)
    admissible = 0
    for location, pair in zip(origins, rows):
        for shear, _ in enumerate(SHEARS):
            preimage = tuple(shear_word(word, shear) for word in pair)
            if sum(map(len, preimage)) > energy:
                continue
            admissible += 1
            for marking in range(len(MAPS)):
                a, b = (signed_key(word, marking) for word in preimage)
                for donor, receiver in ((a, b), (b, a)):
                    if receiver not in previous.get(donor, {}):
                        fresh[donor].setdefault(
                            receiver, (tuple(location), shear, marking)
                        )
    return fresh, admissible


def exact_candidates(number, reversal, receiver):
    if number == 0:
        expected = signature(receiver)
        for word in sorted(reversal):
            x, y = vectors(word)
            weight = 2 * x - 3 * y
            if (
                abs(weight) == 1
                and signature(word if weight == 1 else inverse(word)) == expected
            ):
                yield word
    else:
        assert height(receiver) == 1
        base = "a"
        for _ in range(3):
            base = substitute(base, BETA_INV)
        coefficient = fiber_reduce(base * 2)
        assert (
            coefficient == "bAbAAbAbAA"
            and check(receiver, coefficient)[0] == "conjugate"
        )
        for target in sorted(reversal):
            status, _ = check(target, coefficient)
            if status == "conjugate":
                yield target


def transformed_suffix(source, archives):
    origin, shear, signed_marking = source
    endpoint, moves = reverse_suffix(("archive", origin, 0), archives)
    mark = images(shear, signed_marking)
    converted = []
    for move in moves:
        if move["op"] == "conjugate":
            converted.extend(conj_ops(move["i"], mark[move["g"]]))
        else:
            converted.append(move)
    changed = shear // 2
    donor = 1 - changed
    sign = shear % 2
    if sign == 0:
        converted.extend(
            (
                {"op": "invert", "i": donor},
                {"op": "multiply", "i": changed, "j": donor},
                {"op": "invert", "i": donor},
            )
        )
    else:
        converted.append({"op": "multiply", "i": changed, "j": donor})
    target = tuple(g.translate(MAPS[signed_marking]) for g in BASIS)
    converted.extend(normalize_pair(target, BASIS))
    endpoint = tuple(transport(word, mark) for word in endpoint)
    receipt = replay(
        {
            "format": "ordinary-ac-elementary-v1",
            "start": list(endpoint),
            "target": list(BASIS),
            "moves": converted,
        }
    )
    assert receipt["endpoint"] == list(BASIS)
    return endpoint, converted


def run(args):
    reversal, admissible = index(args.archive, args.energy)
    trials = []
    print(f"Indexed {len(reversal)} new marked donor keys", file=sys.stderr, flush=True)
    for number, (name, d, r) in enumerate(SEEDS):
        prefix = json.loads((ROOT / "certificates" / name).read_text())
        replay(prefix)
        hits = list(exact_candidates(number, reversal, r))
        checked_forward = (
            chart(args.targeted, (r, d), hits, 4, 1000000) if hits else None
        )
        stages = dict(checked_forward["hits"]) if checked_forward else {}
        contacts = [
            (receiver, donor) for donor in hits for receiver in sorted(reversal[donor])
        ]
        print(
            f"Seed {number}: {len(hits)} exact first block hits, {len(contacts)} contacts",
            file=sys.stderr,
            flush=True,
        )
        records = []
        found = []
        reverse_target = canonical(d)
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            scans = pool.map(
                lambda pair, target=reverse_target: chart(
                    args.targeted, pair, [target], args.depth, args.allocation
                ),
                contacts,
            )
            for (s, e), record in zip(contacts, scans):
                source = reversal[e][s]
                records.append(
                    {"pair": [s, e], "word_checks": 1, "source": source, **record}
                )
                if record["hits"] and e in stages:
                    endpoint, suffix = transformed_suffix(source, args.archives)
                    join = {
                        "forward_pair": (canonical(r), canonical(d)),
                        "reverse_pair": (s, e),
                        "intermediate": (e, canonical(d)),
                        "forward_stage": stages[e],
                        "reverse_stage": record["hits"][0][1],
                    }
                    certificate = ledger_for_join(join, suffix, endpoint, prefix)
                    found.append(
                        {
                            **join,
                            **replay(certificate),
                            "cyclic_peak": cyclic_peak(certificate),
                        }
                    )
                    if args.certificate:
                        args.certificate.write_text(
                            json.dumps(certificate, separators=(",", ":")) + "\n"
                        )
        trials.append(
            {
                "source_fixed_donor": d,
                "source_receiver": r,
                "novel_exact_donors": hits,
                "forward_finite_completion": checked_forward,
                "reverse": chart_summary(records),
                "contacts": records,
                "verified_joins": found,
            }
        )
    return {
        "archive_sha256": sha256(args.archive.read_bytes()).hexdigest(),
        "transformed_energy": args.energy,
        "unmarked_shears_within_energy": admissible,
        "novel_marked_donors": len(reversal),
        "novel_ordered_marked_pairs": sum(map(len, reversal.values())),
        "trials": trials,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("targeted", "archive", "archives"):
        parser.add_argument(name, type=Path)
    parser.add_argument("--energy", default=44, type=int)
    parser.add_argument("--depth", default=3, type=int)
    parser.add_argument("--allocation", default=500000, type=int)
    parser.add_argument("--workers", default=3, type=int)
    parser.add_argument("--certificate", type=Path)
    print(json.dumps(run(parser.parse_args()), indent=2))
