"""Generate all marked width-seven rules, including zero-defect traces."""

from round15_stable_disproof_two_widths import marked_width_seven


if __name__ == "__main__":
    for rule in marked_width_seven(nonzero_only=False):
        print(7, *rule)
