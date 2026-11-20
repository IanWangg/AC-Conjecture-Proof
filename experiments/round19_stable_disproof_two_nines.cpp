// Cut the (9,9) schedule between its two active intervals.
#define AC_ROUND08_MAGNUS_NATIVE_LIBRARY
#include "round07_magnus_native.cpp"

namespace two_nines {
using free_distance::Id;
template <std::size_t Rows> using State = free_distance::State<Rows>;
template <std::size_t Rows> using Set = std::unordered_set<State<Rows>, free_distance::StateHash<Rows>>;
using Pair = State<2>;
using Triple = State<3>;

enum class Instruction { invert, conjugate, product, wait };
struct Move { Instruction kind; unsigned recipient, operand; bool negative; };

bool slides(Move move, unsigned spare, unsigned donor) {
    const unsigned other = 3 - spare - donor;
    return (move.recipient == other && (move.kind != Instruction::product || move.operand != spare)) ||
           (move.recipient == donor && move.kind == Instruction::invert);
}

Id marked(Id value, unsigned coefficient) {
    if (value & (1U << 31)) throw std::runtime_error("row ID exceeds 31 bits");
    return (value << 1) | coefficient;
}

Pair ordered(Id left, Id right) { return left < right ? Pair{left, right} : Pair{right, left}; }

struct Counts { std::size_t depth_seven = 0, penultimate_transitions = 0; };

template <unsigned Degree>
class Search {
    magnus_native::Elements<Degree> group;
    magnus_native::Elements<1> linear;
    const Id one = group.intern("");
    const std::array<Id, 4> letters{group.intern("x"), group.intern("X"), group.intern("y"), group.intern("Y")};
    const std::array<Id, 3> linear_ids{linear.intern("x"), linear.intern("y"), linear.intern("xy")};
    std::vector<unsigned char> old_parities;
    const bool pruned;

    unsigned marked_parity(Id row) {
        const Id value = row >> 1;
        if (value >= old_parities.size()) old_parities.resize(group.size(), 255);
        auto& parity = old_parities[value];
        if (parity == 255) {
            const Id projected = group.template project<1>(value, linear);
            const auto found = std::find(linear_ids.begin(), linear_ids.end(), projected);
            parity = found == linear_ids.end() ? 0 : 1 + (found - linear_ids.begin());
        }
        return parity | ((row & 1) << 2);
    }

    static bool can_return(const std::array<unsigned, 3>& tags) {
        return (tags[0] ^ tags[1]) == 4 || (tags[0] ^ tags[2]) == 4 || (tags[1] ^ tags[2]) == 4;
    }

    template <class Filter, class Visit>
    void edges(Triple state, bool returning, bool wait, Filter&& permitted, Visit&& accept) {
        std::array<unsigned, 3> tags{};
        if (returning) for (unsigned i = 0; i < 3; ++i) tags[i] = marked_parity(state[i]);
        const bool constant_parity = !returning || can_return(tags);
        if constexpr (Degree < 9) if (wait && constant_parity) accept(state, Move{Instruction::wait, 0, 0, false});
        auto apply = [&](Move move) {
            if (!permitted(move)) return;
            const unsigned r = move.recipient;
            const Id a = state[r] >> 1;
            unsigned coefficient = state[r] & 1;
            Id value;
            if (move.kind == Instruction::invert) value = group.inverse(a);
            else if (move.kind == Instruction::conjugate) value = group.conjugate(a, move.operand);
            else {
                const Id b = state[move.operand] >> 1;
                value = group.product(a, move.negative ? group.inverse(b) : b);
                coefficient ^= state[move.operand] & 1;
            }
            if constexpr (Degree == 9) if (value == one || value == a) return;
            Triple child = state;
            child[r] = marked(value, coefficient);
            accept(child, move);
        };
        for (unsigned r = 0; r < 3; ++r) {
            if (constant_parity) {
                apply({Instruction::invert, r, 0, false});
                for (unsigned letter = 0; letter < 4; ++letter) apply({Instruction::conjugate, r, letter, false});
            }
            for (unsigned donor = 0; donor < 3; ++donor) if (r != donor) {
                tags[r] ^= tags[donor];
                const bool possible = !returning || can_return(tags);
                tags[r] ^= tags[donor];
                if (possible) {
                    apply({Instruction::product, r, donor, false});
                    apply({Instruction::product, r, donor, true});
                }
            }
        }
    }

    Set<3> birth_layer(Pair endpoint) {
        Set<3> layer;
        auto admit = [&](Triple child, Move) {
            std::sort(child.begin(), child.end());
            layer.insert(child);
        };
        for (unsigned donor = 0; donor < 2; ++donor) {
            const Id value = endpoint[donor] >> 1;
            for (const Id copy : {value, group.inverse(value)}) {
                Triple birth{endpoint[0], endpoint[1], marked(copy, 1 ^ (endpoint[donor] & 1))};
                if (pruned) edges(birth, false, false, [&](Move move) { return !slides(move, 2, donor); }, admit);
                else admit(birth, Move{});
            }
        }
        return layer;
    }

    Set<2> after_nine(Pair endpoint, Counts& counts) {
        auto layer = birth_layer(endpoint);
        for (unsigned depth = pruned ? 2 : 1; depth < 7; ++depth) {
            Set<3> next;
            for (const Triple& state : layer) edges(state, false, true, [](Move) { return true; }, [&](Triple child, Move) {
                std::sort(child.begin(), child.end());
                next.insert(child);
            });
            layer = std::move(next);
        }
        counts.depth_seven = layer.size();
        std::cerr << "width nine at depth seven " << counts.depth_seven << '\n';
        Set<2> result;
        for (const Triple& state : layer) edges(state, true, !pruned, [](Move) { return true; }, [&](Triple child, Move last) {
            ++counts.penultimate_transitions;
            for (unsigned i = 0; i < 3; ++i) for (unsigned j = i + 1; j < 3; ++j) {
                const Id a = child[i] >> 1, b = child[j] >> 1;
                if (((child[i] ^ child[j]) & 1) == 0 || (a != b && a != group.inverse(b))) continue;
                const Id other = child[3 - i - j];
                if (!pruned || !slides(last, i, j)) result.insert(ordered(child[j], other));
                if (!pruned || !slides(last, j, i)) result.insert(ordered(child[i], other));
            }
        });
        return result;
    }

public:
    explicit Search(bool prune) : pruned(prune) {}

    void run() {
        const Pair start = ordered(marked(group.intern("xxxYYYY"), 0), marked(group.intern("xyxYXY"), 0));
        const Pair basis = ordered(marked(letters[0], 0), marked(letters[2], 0));
        Counts left_counts, right_counts;
        const auto left = after_nine(start, left_counts), right = after_nine(basis, right_counts);
        using MarkedValue = std::pair<std::string, unsigned>;
        std::vector<std::array<MarkedValue, 2>> coordinates;
        for (const Pair& state : left) if (right.count(state)) {
            std::array<MarkedValue, 2> pair{{{group.describe(state[0] >> 1), state[0] & 1},
                                             {group.describe(state[1] >> 1), state[1] & 1}}};
            std::sort(pair.begin(), pair.end());
            coordinates.push_back(std::move(pair));
        }
        std::sort(coordinates.begin(), coordinates.end());
        std::cout << "{\"degree\":" << Degree << ",\"widths\":[9,9],\"commutation_pruned\":" << (pruned ? "true" : "false")
                  << ",\"left\":" << left.size() << ",\"right\":" << right.size() << ",\"depth_seven\":["
                  << left_counts.depth_seven << ',' << right_counts.depth_seven << "],\"edges\":[" << left_counts.penultimate_transitions
                  << ',' << right_counts.penultimate_transitions << "],\"meetings\":" << coordinates.size()
                  << ",\"elements\":" << group.size() << ",\"meeting_coordinates\":[";
        for (std::size_t i = 0; i < coordinates.size(); ++i) {
            if (i > 0) std::cout << ',';
            const auto& pair = coordinates[i];
            std::cout << "[[\"" << pair[0].first << "\"," << pair[0].second << "],[\"" << pair[1].first << "\"," << pair[1].second << "]]";
        }
        std::cout << "]}" << std::endl;
    }
};
}

int main(int argc, char** argv) {
    if (argc != 2 && (argc != 3 || std::string_view(argv[2]) != "--unpruned"))
        throw std::runtime_error("expected one Magnus degree and optional --unpruned");
    const bool prune = argc == 2;
    switch (std::stoi(argv[1])) {
    case 5: two_nines::Search<5>(prune).run(); break;
    case 6: two_nines::Search<6>(prune).run(); break;
    case 7: two_nines::Search<7>(prune).run(); break;
    case 8: two_nines::Search<8>(prune).run(); break;
    case 9: two_nines::Search<9>(prune).run(); break;
    default: throw std::runtime_error("degree must be from five through nine");
    }
}
