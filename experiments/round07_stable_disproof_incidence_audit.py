"""Independent midpoint audit, using a quotient by unordered columns."""
import json


def midpoint_key(columns, rank):
    return tuple(sorted(columns >> (rank * i) & ((1 << rank) - 1) for i in range(rank)))


def half_schedules(padding, radius, start):
    rank = padding + 2
    stride = sum(1 << (rank * i) for i in range(rank))
    menu = []
    for recipient in range(rank):
        for donor in range(rank):
            if recipient == donor or max(recipient, donor) < 2:
                continue
            weight = 0
            for subset in range(1, 1 << padding):
                inside = subset << 2
                if ((inside >> recipient) ^ (inside >> donor)) & 1:
                    weight |= 1 << (5 * (subset - 1))
            menu.append((recipient, donor, weight))

    def visit(matrix, cuts, depth):
        if depth == radius:
            yield midpoint_key(matrix, rank), cuts
        else:
            for recipient, donor, weight in menu:
                image = matrix ^ (((matrix >> donor) & stride) << recipient)
                yield from visit(image, cuts + weight, depth + 1)

    yield from visit(start, 0, 0)


def check(padding):
    rank = padding + 2
    length = (3 * (padding + 1) + 1) // 2
    left_radius = length // 2
    right_radius = length - left_radius
    unit = sum(1 << (rank * i + i) for i in range(rank))
    # B = I + E_10, so the prefix half starts at B^-1 = B.
    before = {}
    for key, cuts in half_schedules(padding, left_radius, unit ^ 2):
        group = before.setdefault(key, {})
        group[cuts] = group.get(cuts, 0) + 1
    field_count = (1 << padding) - 1
    guards = sum(16 << (5 * i) for i in range(field_count))
    lower = sum(3 << (5 * i) for i in range(field_count))
    parity = accepted = 0
    for key, cuts in half_schedules(padding, right_radius, unit):
        for first, multiplicity in before.get(key, {}).items():
            parity += multiplicity
            # Each field sum is at most eight, and the guard prevents cross-field borrowing.
            if (((first + cuts | guards) - lower) & guards) == guards:
                accepted += multiplicity
    return {
        "padding": padding,
        "left_radius": left_radius,
        "right_radius": right_radius,
        "parity_matches_all_target_orders": parity,
        "all_cuts_at_least_three": accepted,
    }


def main():
    print(json.dumps([check(k) for k in range(1, 5)], indent=2))


if __name__ == "__main__":
    main()
