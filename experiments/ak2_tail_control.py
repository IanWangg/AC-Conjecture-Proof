"""Exact positive control discovered by the Nielsen-prelude/tail method."""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'research_m'))
from stallings_search import apply,inverse,primitive
from complete_primitive import complete
from nielsen_tail_probe import cyclic,orbit_min


def make():
    start=('xxYYY','xyxYXY')
    state=start
    moves=[]

    def emit(op):
        nonlocal state
        state=apply(state,op)
        moves.append(op)

    def canonicalize(index):
        target=orbit_min(state[index])
        for flip in (False,True):
            word=inverse(state[index]) if flip else state[index]
            core=cyclic(word)
            options=[k for k in range(len(core)) if core[k:]+core[:k]==target]
            if options:
                if flip:emit({'op':'invert','i':index})
                while state[index]!=cyclic(state[index]):
                    emit({'op':'conjugate','i':index,'g':state[index][0].swapcase()})
                prefix=state[index][:options[0]]
                for letter in prefix:
                    emit({'op':'conjugate','i':index,'g':letter.swapcase()})
                assert state[index]==target
                return
        raise AssertionError('missing canonical rotation')

    # One genuine initial Nielsen operation, donor orientation restored.
    emit({'op':'invert','i':0})
    emit({'op':'multiply','i':1,'j':0})
    emit({'op':'invert','i':0})
    canonicalize(0)
    canonicalize(1)
    assert state==('XXyyy','XYxYYxy')
    # The signed-cycle criterion left this subgroup, and the following
    # Nielsen operation exposes an actual ambient primitive coordinate.
    emit({'op':'invert','i':1})
    emit({'op':'multiply','i':0,'j':1})
    emit({'op':'invert','i':1})
    assert state==('XXyyXyyXyx','XYxYYxy')
    assert primitive(state[0])
    waypoint={'format':'ordinary-ac-elementary-v1','start':list(start),
              'target':list(state),'moves':moves,
              'scope':'AK(2) positive control, not an AK(3) solution'}
    return waypoint,complete(waypoint)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--directory',default='.')
    args=parser.parse_args()
    waypoint,full=make()
    directory=Path(args.directory)
    directory.mkdir(parents=True,exist_ok=True)
    for name,data in (('o_ak2_tail_waypoint.json',waypoint),('o_ak2_tail_full.json',full)):
        directory.joinpath(name).write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'primitive_waypoint':waypoint['target'],
                      'waypoint_strict_moves':len(waypoint['moves']),
                      'full_strict_moves':len(full['moves'])},indent=2))
