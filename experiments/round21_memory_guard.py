"""Run a research job in a separate process group and sample its combined RSS."""

import argparse
import os
import signal
import subprocess
import sys
import time


def group_rss_kib(group):
    rows = subprocess.check_output(['ps', '-axo', 'pgid=,rss='], text=True)
    return sum(int(rss) for pgid, rss in map(str.split, rows.splitlines())
               if int(pgid) == group)


def run(cutoff_gib, command):
    child = subprocess.Popen(command, start_new_session=True)
    peak = 0

    def terminate():
        try:
            os.killpg(child.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass

    def interrupted(signum, _frame):
        terminate()
        raise SystemExit(128 + signum)

    signal.signal(signal.SIGTERM, interrupted)
    signal.signal(signal.SIGINT, interrupted)
    try:
        while child.poll() is None:
            peak = max(peak, group_rss_kib(child.pid))
            if peak >= cutoff_gib * 2**20:
                print(f'RSS guard stopped job {child.pid} at {peak} KiB', file=sys.stderr)
                terminate()
                return 125
            time.sleep(0.20)
    finally:
        if child.poll() is None:
            terminate()
        child.wait()
        print(f'Job {child.pid} sampled peak RSS {peak} KiB', file=sys.stderr)
    return child.returncode if child.returncode >= 0 else 128 - child.returncode


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('cutoff_gib', type=float)
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if not 0 < args.cutoff_gib < float('inf') or not args.command:
        parser.error('a finite positive cutoff and one command are required')
    raise SystemExit(run(args.cutoff_gib, args.command))
