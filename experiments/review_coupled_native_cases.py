"""Independently refold and decide logged native search exceptions using R."""
import argparse
import base64
import gzip
import hashlib
import json
from pathlib import Path
from primitive_map_pairs import fold, decide, verify_absence


def review(source):
    raw = Path(source).read_bytes()
    if str(source).endswith('.b64'):
        raw = gzip.decompress(base64.b64decode(raw))
    rows = states = 0
    for line in raw.splitlines():
        row = json.loads(line)
        cert = decide(fold(row['pair']), budget=100000, save_certificate=True)
        assert cert['status'] == row['status'] == 'ABSENT'
        checked = verify_absence(cert)['closed_map_pair_states_checked']
        assert checked == row['pair_states']
        states += checked
        rows += 1
    return {'status':'PASS', 'ordinary_AC_goal_solved':False,
            'independent_R_refolds_and_complete_absence_decisions':rows,
            'closed_map_pair_states_independently_verified':states,
            'decoded_log_sha256':hashlib.sha256(raw).hexdigest(),
            'scope':'Logged exceptions from one heuristic search; no global search completeness claimed'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('log')
    parser.add_argument('--output',required=True)
    args = parser.parse_args()
    result = review(args.log)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
