import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

from elementary_verify import replay
from round07_automorphism_transport import normalize_pair
from round07_stable_proof_compile_join import compile_local_caps, lift_from
from round08_ak3_acm_search import cyclic_peak


def compile_route(backward_route, literal_path, destination):
    orbits = [tuple(line.split()) for line in backward_route.read_text().splitlines()]
    target = orbits[0]
    lifted = lift_from(target, orbits, 32)
    with TemporaryDirectory() as scratch:
        work = Path(scratch)
        target_tsv = work / 'target.tsv'
        route_json = work / 'route.json'
        target_tsv.write_text('\t'.join(lifted[-1]) + '\n')
        subprocess.run([str(literal_path.resolve()), '22', str(target_tsv), str(route_json)],
                       check=True, capture_output=True)
        prefix = [tuple(row) for row in json.loads(route_json.read_text())['route']]
    assert prefix[-1] == lifted[-1]
    route = prefix + lifted[-2::-1]
    certificate, _ = compile_local_caps(route, 32)
    certificate['moves'].extend(normalize_pair(tuple(certificate['target']), target))
    certificate['target'] = list(target)
    checked = replay(certificate)
    peak = cyclic_peak(certificate)
    assert peak == 32
    destination.write_text(json.dumps(certificate, separators=(',', ':')) + '\n')
    return {'backward_orbit_route': orbits, 'marked_cyclic_route': route,
            'strict_replay': {**checked, 'cyclic_peak': peak}}


if __name__ == '__main__':
    print(json.dumps(compile_route(*map(Path, sys.argv[1:])), indent=2))
