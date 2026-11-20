// Compare the two outer active intervals in the four-slot degree-eight retraction.
#define AC_ROUND08_MAGNUS_NATIVE_LIBRARY
#include "round07_magnus_native.cpp"

namespace two_outer {
using free_distance::Id;
using State = free_distance::State<4>;
using Set = std::unordered_set<State, free_distance::StateHash<4>>;

struct Shape {
    unsigned left, right, idle;
};

template <unsigned Degree>
class Cut {
    magnus_native::Elements<Degree> group;
    const Id one = group.intern("");
    std::size_t moves = 0;

    static State order(State state) {
        std::sort(state.begin(), state.end());
        return state;
    }

    template <class Visit>
    void edges(const State& state, unsigned before, unsigned after, Visit&& accept) {
        const unsigned first = 4 - before;
        ++moves;
        if (after > before) {
            for (unsigned i = first; i < 4; ++i) {
                for (const Id value : {state[i], group.inverse(state[i])}) {
                    State next = state;
                    next[0] = value;
                    accept(order(next));
                }
            }
        } else if (after < before) {
            for (unsigned i = first; i < 4; ++i) {
                const Id inverted = group.inverse(state[i]);
                for (unsigned j = first; j < 4; ++j) {
                    if (i != j && (state[j] == state[i] || state[j] == inverted)) {
                        State next = state;
                        next[i] = one;
                        accept(order(next));
                        break;
                    }
                }
            }
        } else {
            for (unsigned i = first; i < 4; ++i) {
                auto change = [&](Id value) {
                    if (value == one || value == state[i]) return;
                    State next = state;
                    next[i] = value;
                    accept(order(next));
                };
                change(group.inverse(state[i]));
                for (unsigned letter = 0; letter < 4; ++letter) change(group.conjugate(state[i], letter));
                for (unsigned j = first; j < 4; ++j) if (i != j) {
                    change(group.product(state[i], state[j]));
                    change(group.product(state[i], group.inverse(state[j])));
                }
            }
        }
    }

    Set next(const Set& layer, unsigned before, unsigned after) {
        Set result;
        for (const State& state : layer) edges(state, before, after, [&](State child) { result.insert(child); });
        return result;
    }

    Set four_active_windows(const Set& start, unsigned span) {
        Set answers;
        Set first = next(start, 2, 3);
        for (unsigned leading = 0; leading + 7 <= span; ++leading) {
            Set four = next(first, 3, 4);
            for (unsigned step = 0; step < 3; ++step) four = next(four, 4, 4);
            for (unsigned inside = 3; inside + leading + 4 <= span; ++inside) {
                Set last = next(four, 4, 3);
                for (unsigned trail = span - (inside + leading + 4); trail; --trail) last = next(last, 3, 3);
                for (const State& state : last) edges(state, 3, 2, [&](State child) { answers.insert(child); });
                if (inside + leading + 4 < span) four = next(four, 4, 4);
            }
            if (leading + 7 < span) first = next(first, 3, 3);
        }
        return answers;
    }

    std::size_t three_active_cut(Set start, Set finish, unsigned span) {
        // Read the last crossing backwards as another birth. Expand the smaller
        // current layer at each of the span-2 same-occupancy instructions.
        start = next(start, 2, 3);
        finish = next(finish, 2, 3);
        for (unsigned step = 0; step < span - 2; ++step) {
            if (start.size() > finish.size()) std::swap(start, finish);
            start = next(start, 3, 3);
        }
        return intersection(start, finish);
    }

    static std::size_t intersection(const Set& left, const Set& right) {
        if (left.size() > right.size()) return intersection(right, left);
        std::size_t hits = 0;
        for (const State& state : left) hits += right.count(state);
        return hits;
    }

    void run(Shape shape, unsigned before, unsigned gap, unsigned after, bool reverse) {
        std::array<State, 2> endpoints{
            order({one, one, group.intern("xxxYYYY"), group.intern("xyxYXY")}),
            order({one, one, group.intern("x"), group.intern("y")}),
        };
        if (reverse) std::swap(endpoints[0], endpoints[1]);
        Set left{endpoints[0]}, right{endpoints[1]};
        for (unsigned step = 0; step < before; ++step) left = next(left, 2, 2);
        for (unsigned step = 0; step < after; ++step) right = next(right, 2, 2);
        const auto seeds = std::array{left.size(), right.size()};
        auto left_windows = four_active_windows(left, shape.left);
        auto right_windows = four_active_windows(right, shape.right);
        const auto widths = std::array{left_windows.size(), right_windows.size()};
        auto left_middle = left_windows;
        auto right_middle = right_windows;
        for (unsigned step = 0; step < gap; ++step) {
            left_middle = next(left_middle, 2, 2);
            right_middle = next(right_middle, 2, 2);
        }
        const std::array<std::size_t, 3> hits{three_active_cut(left, right_middle, shape.left),
                                             three_active_cut(right, left_middle, shape.right),
                                             intersection(left_middle, right_windows)};
        std::cout << "{\"degree\":" << Degree << ",\"widths\":[" << shape.left << ',' << shape.right
                  << "],\"idle\":[" << before << ',' << gap << ',' << after << "],\"ak_on_right\":"
                  << (reverse ? "true" : "false") << ",\"seeds\":[" << seeds[0] << ',' << seeds[1]
                  << "],\"four_active_boundaries\":[" << widths[0] << ',' << widths[1]
                  << "],\"middle_boundaries\":[" << left_middle.size() << ',' << right_middle.size() << "],\"hits\":["
                  << hits[0] << ',' << hits[1] << ',' << hits[2] << "],\"expanded_states\":" << moves
                  << ",\"interned_rows\":" << group.size() << "}\n" << std::flush;
    }

public:
    void run(unsigned a, unsigned b, int pad = -1, int orientation = -1) {
        const Shape shape{a, b, 16 - a - b};
        if (a < 7 || b < a || a + b > 16 || b > 9) throw std::runtime_error("invalid widths");
        const unsigned orientations = a == b ? 1 : 2;
        for (unsigned reverse = 0; reverse < orientations; ++reverse) {
            if (orientation >= 0 && reverse != unsigned(orientation)) continue;
            for (unsigned before = 0; before <= shape.idle; ++before)
                for (unsigned after = 0; after + before <= shape.idle; ++after) {
                    const unsigned gap = shape.idle - before - after;
                    if (pad >= 0 && (before * 100 + gap * 10 + after) != unsigned(pad)) continue;
                    run(shape, before, gap, after, reverse != 0);
                }
        }
    }
};
}

int main(int argc, char** argv) {
    if (argc < 4 || argc > 6) throw std::runtime_error("expected degree, widths, optional idle placement and orientation");
    const int degree = std::stoi(argv[1]);
    const unsigned a = std::stoul(argv[2]), b = std::stoul(argv[3]);
    const int pad = argc >= 5 ? std::stoi(argv[4]) : -1;
    const int orientation = argc >= 6 ? std::stoi(argv[5]) : -1;
    if (degree == 8) two_outer::Cut<8>{}.run(a, b, pad, orientation);
    else if (degree == 3) two_outer::Cut<3>{}.run(a, b, pad, orientation);
    else throw std::runtime_error("degree must be three or eight");
}
