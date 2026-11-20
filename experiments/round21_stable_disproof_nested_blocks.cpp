// Check two four-active blocks within one outer interval of the four-slot retraction.
#define AC_ROUND08_MAGNUS_NATIVE_LIBRARY
#include "round07_magnus_native.cpp"

namespace nested_blocks {
using free_distance::Id;
using State = free_distance::State<4>;
using Set = std::unordered_set<State, free_distance::StateHash<4>>;

enum Stage : unsigned { Idle, Before, First0, First1, First2, First3, Between, Second0, Second1, Second2, Second3, StageCount };
using Layer = std::array<Set, StageCount>;
constexpr std::array<unsigned, StageCount> occupation{2, 3, 4, 4, 4, 4, 3, 4, 4, 4, 4};
constexpr std::array<unsigned, StageCount> needed{12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2};


template <unsigned Degree>
class Cut {
    magnus_native::Elements<Degree> group;
    const Id one = group.intern("");
    std::size_t expanded_states = 0;

    static State order(State state) {
        std::sort(state.begin(), state.end());
        return state;
    }

    template <class Visit>
    void edges(const State& state, unsigned before, unsigned after, Visit&& accept) {
        const unsigned first = 4 - before;
        ++expanded_states;
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

    template <class Visit>
    void transitions(Stage stage, Visit&& accept) {
        if (stage == Idle) {
            accept(Idle);
            accept(Before);
        } else if (stage == Before) {
            accept(Before);
            accept(First0);
        } else if (stage == Between) {
            accept(Between);
            accept(Second0);
        } else if (stage >= First0 && stage <= First3) {
            accept(stage == First3 ? First3 : Stage(stage + 1));
            if (stage == First3) accept(Between);
        } else {
            accept(stage == Second3 ? Second3 : Stage(stage + 1));
        }
    }

    Layer advance(const Layer& prior, unsigned depth, bool completed_first_only = false) {
        Layer result;
        for (unsigned i = 0; i < StageCount; ++i) {
            transitions(Stage(i), [&](Stage after) {
                if (needed[after] > 16 - depth || (completed_first_only && after < Between)) return;
                for (const State& state : prior[i]) {
                    edges(state, occupation[i], occupation[after], [&](State child) { result[after].insert(child); });
                }
            });
        }
        return result;
    }

    void widths(const Layer& layer, unsigned depth, const char* side) {
        std::cerr << side << ' ' << depth;
        for (const auto& states : layer) std::cerr << ' ' << states.size();
        std::cerr << '\n' << std::flush;
    }

    Layer almost(const State& start, const char* side) {
        Layer layer;
        layer[Idle].insert(start);
        for (unsigned depth = 1; depth <= 7; ++depth) {
            layer = advance(layer, depth);
            widths(layer, depth, side);
        }
        return layer;
    }

    // Read the cut edge backwards from the smaller second-block layer.
    std::size_t first_meets_second(const Layer& first_penultimate, const Layer& second_mid) {
        Set matched;
        for (unsigned stage = Second0; stage <= Second1; ++stage) {
            for (const auto& midpoint : second_mid[stage]) {
                edges(midpoint, 4, 4, [&](State predecessor) {
                    if (first_penultimate[First2].count(predecessor) ||
                        first_penultimate[First3].count(predecessor) ||
                        (stage == Second1 && first_penultimate[First1].count(predecessor)))
                        matched.insert(midpoint);
                });
            }
        }
        return matched.size();
    }

    static std::size_t intersection(const Set& left, const Set& right) {
        if (left.size() > right.size()) return intersection(right, left);
        std::size_t hits = 0;
        for (const State& state : left) hits += right.count(state);
        return hits;
    }

public:
    void run() {
        const State ak = order({one, one, group.intern("xxxYYYY"), group.intern("xyxYXY")});
        const State basis = order({one, one, group.intern("x"), group.intern("y")});
        const auto left = almost(ak, "AK"), right = almost(basis, "basis");
        // Only one half needs to be inside its first block at the midpoint.
        const auto left_mid = advance(left, 8, true), right_mid = advance(right, 8, true);
        widths(left_mid, 8, "AK-trimmed");
        widths(right_mid, 8, "basis-trimmed");
        const std::array<std::size_t, 3> hits{
            intersection(left_mid[Between], right_mid[Between]),
            first_meets_second(left, right_mid),
            first_meets_second(right, left_mid),
        };
        std::cout << "{\"degree\":" << Degree << ",\"hits\":[" << hits[0] << ',' << hits[1] << ',' << hits[2]
                  << "],\"expanded_states\":" << expanded_states << ",\"interned_rows\":" << group.size() << "}\n" << std::flush;
    }

};
}

int main(int argc, char** argv) {
    if (argc != 2) throw std::runtime_error("expected one degree");
    const auto degree = std::stoi(argv[1]);
    if (degree == 8) nested_blocks::Cut<8>{}.run();
    else if (degree == 3) nested_blocks::Cut<3>{}.run();
    else throw std::runtime_error("degree must be three or eight");
}
