"""Check a separating cut for the rebased join of an actual nested barbell."""

from collections import defaultdict
import json

from elementary_verify import replay
from free_waypoint_search import conj_ops
from primitive_map_pairs import LETTERS, decide, fold, follow, inverse, verify_absence
from round07_automorphism_transport import normalize_pair
from round08_ac_disproof_bridge_language import side_is_folded
from stallings_search import apply


def common_component(graph, first, second):
    reached = {(first, second)}
    queue = [(first, second)]
    for pair in queue:
        for letter in LETTERS:
            target = tuple(follow(graph, vertex, letter) for vertex in pair)
            if min(target) >= 0 and target not in reached:
                reached.add(target)
                queue.append(target)
    return sorted(reached)


def main():
    start = ("xxxYYYY", "xyxYXY")
    left, right, first_bridge = "XXXyyyy", "XYXyxy", "xxY"
    moves = normalize_pair(start, (left, right))
    row = first_bridge + right + inverse(first_bridge)
    moves.extend(conj_ops(1, first_bridge))
    moves.append({"op": "multiply", "i": 1, "j": 0})
    nested = left + row
    rotation = 3
    lobe_a, lobe_b = (word[rotation:] + word[:rotation] for word in (left, nested))
    moves.extend(normalize_pair((left, row + left), (lobe_a, lobe_b)))
    bridge = "Xy"
    moves.extend(conj_ops(1, bridge))
    root_a = (lobe_a, bridge + lobe_b + inverse(bridge))
    root_b = (inverse(bridge) + lobe_a + bridge, lobe_b)
    certificate = {"format": "ordinary-ac-elementary-v1", "start": list(start),
                   "target": list(root_a), "moves": moves}
    checked = replay(certificate)
    moved = tuple(checked["endpoint"])
    for slot in range(2):
        for move in conj_ops(slot, inverse(bridge)):
            moved = apply(moved, move)
    assert moved == root_b
    assert side_is_folded(lobe_a, lobe_b, bridge)
    barbell = fold(root_a)
    right_vertex = follow(barbell, 0, bridge)
    assert right_vertex > 0
    component = common_component(barbell, 0, right_vertex)
    projection = defaultdict(list)
    for a, b in component:
        projection[a].append(b)
    collisions = {a: b for a, b in projection.items() if len(b) > 1}
    assert collisions
    collar = fold((lobe_a, lobe_b))
    cut_directions = (bridge[0], inverse(bridge[-1]))
    assert len(set(cut_directions)) == 2 and all(follow(collar, 0, letter) < 0 for letter in cut_directions)
    local_exclusion = decide(collar, save_certificate=True)
    assert local_exclusion["status"] == "ABSENT"
    joined = fold((*root_a, *root_b))
    exclusion = decide(joined, save_certificate=True)
    assert exclusion["status"] == "ABSENT"
    print(json.dumps({"lobes": [lobe_a, lobe_b], "bridge": bridge, "entry": certificate,
                      "checked_entry": checked, "common_component": component,
                      "noninjective_first_projection": collisions,
                      "available_cut_directions_at_folded_root": cut_directions,
                      "local_collar_graph": collar, "checked_local_collar": verify_absence(local_exclusion),
                      "full_join_graph": joined,
                      "checked_full_join": verify_absence(exclusion)}, indent=2))


if __name__ == "__main__":
    main()
