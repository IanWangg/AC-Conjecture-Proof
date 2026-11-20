// Compare the marked boundaries of two length-eight or longer excursions.
#define AC_ROUND08_MAGNUS_NATIVE_LIBRARY
#include "round07_magnus_native.cpp"

namespace wide_cuts {
using free_distance::Id;
template <std::size_t Rows> using State = free_distance::State<Rows>;
template <std::size_t Rows> using Set = std::unordered_set<State<Rows>, free_distance::StateHash<Rows>>;

struct Expression { Id parent; unsigned symbol; };
struct Rule { Id removed, donor, left, right; };

class RuleTable {
    std::unordered_map<std::string, Id> index{{"", 0}};

    Id intern(std::string word) {
        if (const auto found = index.find(word); found != index.end()) return found->second;
        const Id parent = intern(word.substr(0, word.size() - 1));
        const auto symbol = std::string_view("aAbBxXyY").find(word.back());
        if (symbol == std::string_view::npos) throw std::runtime_error("invalid rule symbol");
        const Id id = static_cast<Id>(expressions.size());
        expressions.push_back({parent, static_cast<unsigned>(symbol)});
        index.emplace(std::move(word), id);
        return id;
    }

public:
    std::vector<Expression> expressions{{0, 0}};
    std::vector<Rule> rules;

    void read(std::istream& input) {
        std::string removed, donor, left, right;
        unsigned left_mark, right_mark;
        while (input >> removed >> donor >> left >> right >> left_mark >> right_mark) {
            rules.push_back({intern(removed), intern(donor), (intern(left) << 1) | left_mark,
                             (intern(right) << 1) | right_mark});
        }
        if (!input.eof() || rules.size() != 3592267) throw std::runtime_error("incomplete width-eight rule table");
        index.clear();
        index.rehash(0);
    }
};

Id marked(Id value, unsigned coefficient) {
    if (value & (1U << 31)) throw std::runtime_error("row ID exceeds 31 bits");
    return (value << 1) | coefficient;
}

State<2> order(Id left, Id right) { return left < right ? State<2>{left, right} : State<2>{right, left}; }

struct Options {
    unsigned wider = 8;
    unsigned short_idle = 0;
};

unsigned small_number(std::string_view argument) {
    std::size_t used = 0;
    const auto value = std::stoul(std::string(argument), &used);
    if (used != argument.size() || value > 10) throw std::runtime_error("invalid structured cut argument");
    return static_cast<unsigned>(value);
}

template <unsigned Degree>
class Search {
    magnus_native::Elements<Degree> group;
    RuleTable table;
    const Id one = group.intern("");
    const std::array<Id, 4> letters{group.intern("x"), group.intern("X"), group.intern("y"), group.intern("Y")};
    std::array<Id, 8> alphabet{};
    std::vector<Id> evaluated;
    std::vector<unsigned> stamp;
    unsigned generation = 0;

    Id evaluate(Id expression) {
        if (expression && stamp[expression] != generation) {
            const auto node = table.expressions[expression];
            evaluated[expression] = group.product(evaluate(node.parent), alphabet[node.symbol]);
            stamp[expression] = generation;
        }
        return evaluated[expression];
    }

    void excursion(State<2> boundary, Set<2>& accepted) {
        for (unsigned i = 0; i < 2; ++i) {
            const Id a = boundary[i] >> 1, b = boundary[i ^ 1] >> 1;
            alphabet = {a, group.inverse(a), b, group.inverse(b), letters[0], letters[1], letters[2], letters[3]};
            ++generation;
            for (const Rule& rule : table.rules) {
                if (evaluate(rule.removed) != evaluate(rule.donor)) continue;
                accepted.insert(order(marked(evaluate(rule.left >> 1), rule.left & 1),
                                      marked(evaluate(rule.right >> 1), rule.right & 1)));
            }
        }
    }

    template <std::size_t Rows, class Visit>
    void edges(State<Rows> state, Visit&& accept) {
        if constexpr (Rows == 2 || Degree < 9) accept(state);
        auto change = [&](unsigned recipient, Id value, unsigned coefficient) {
            if constexpr (Rows == 3 && Degree == 9)
                if (value == one || value == (state[recipient] >> 1)) return;
            State<Rows> child = state;
            child[recipient] = marked(value, coefficient);
            std::sort(child.begin(), child.end());
            accept(child);
        };
        for (unsigned i = 0; i < Rows; ++i) {
            const Id a = state[i] >> 1;
            const unsigned mark_a = state[i] & 1;
            change(i, group.inverse(a), mark_a);
            for (unsigned letter = 0; letter < 4; ++letter) change(i, group.conjugate(a, letter), mark_a);
            for (unsigned j = 0; j < Rows; ++j) if (i != j) {
                const Id b = state[j] >> 1;
                const unsigned mark_ab = mark_a ^ (state[j] & 1);
                change(i, group.product(a, b), mark_ab);
                change(i, group.product(a, group.inverse(b)), mark_ab);
            }
        }
    }

    template <std::size_t Rows>
    Set<Rows> advance(const Set<Rows>& layer) {
        Set<Rows> next;
        for (const State<Rows> state : layer) edges(state, [&](State<Rows> child) { next.insert(child); });
        return next;
    }

    std::vector<Set<2>> after_eight(State<2> start, unsigned until) {
        std::vector<Set<2>> result(until + 1);
        Set<2> plain{start};
        for (unsigned step = 0; step <= until; ++step) {
            if (step > 0) {
                plain = advance(plain);
                result[step] = advance(result[step - 1]);
            }
            for (const State<2> state : plain) excursion(state, result[step]);
            std::cerr << "idle " << step << " plain " << plain.size() << " via width eight " << result[step].size() << '\n';
        }
        return result;
    }

    Set<3> active_half(const Set<2>& boundary, unsigned depth) {
        Set<3> layer;
        for (const State<2> state : boundary) for (const Id donor : state) {
            const Id value = donor >> 1;
            const unsigned coefficient = 1 ^ (donor & 1);
            for (const Id copy : {value, group.inverse(value)}) {
                State<3> child{state[0], state[1], marked(copy, coefficient)};
                std::sort(child.begin(), child.end());
                layer.insert(child);
            }
        }
        for (unsigned step = 1; step < depth; ++step) layer = advance(layer);
        return layer;
    }

    static std::size_t intersection_size(const Set<2>& first, const Set<2>& second) {
        if (first.size() > second.size()) return intersection_size(second, first);
        std::size_t result = 0;
        for (const auto& state : first) result += second.count(state);
        return result;
    }

    void between_eights(State<2> start, State<2> basis) {
        const auto left = after_eight(start, 2), right = after_eight(basis, 2);
        std::cout << "{\"degree\":" << Degree << ",\"widths\":[8,8],\"left\":[" << left[0].size()
                  << ',' << left[1].size() << ',' << left[2].size() << "],\"right\":[" << right[0].size()
                  << ',' << right[1].size() << ',' << right[2].size() << "],\"meetings\":["
                  << intersection_size(left[0], right[2]) << ',' << intersection_size(left[1], right[1]) << ','
                  << intersection_size(left[2], right[0]) << "],\"elements\":" << group.size() << "}\n";
    }

    void structured(std::array<State<2>, 2> endpoints, unsigned wide, unsigned short_idle) {
        const unsigned plain_idle = 10 - wide - short_idle;
        const unsigned short_depth = 3 - short_idle, plain_depth = wide - short_depth;
        std::cout << "{\"degree\":" << Degree << ",\"widths\":[8," << wide << "],\"short_idle\":" << short_idle
                  << ",\"active_depths\":[" << short_depth << ',' << plain_depth << "],\"orientations\":[";
        for (unsigned side = 0; side < 2; ++side) {
            const auto short_boundary = after_eight(endpoints[side], short_idle);
            Set<2> plain_boundary{endpoints[side ^ 1]};
            for (unsigned step = 0; step < plain_idle; ++step) plain_boundary = advance(plain_boundary);
            const auto left = active_half(short_boundary.back(), short_depth);
            const auto almost_right = active_half(plain_boundary, plain_depth - 1);
            Set<3> matches;
            std::size_t checked = 0;
            for (const State<3> state : almost_right) edges(state, [&](State<3> child) {
                ++checked;
                if (left.count(child)) matches.insert(child);
            });
            if (side > 0) std::cout << ',';
            std::cout << "{\"short_boundary\":" << short_boundary.back().size() << ",\"plain_boundary\":" << plain_boundary.size()
                      << ",\"active_layer\":" << left.size() << ",\"penultimate_layer\":" << almost_right.size()
                      << ",\"edges\":" << checked << ",\"meetings\":" << matches.size() << '}' << std::flush;
        }
        std::cout << "]}\n";
    }

public:
    explicit Search(RuleTable rules)
        : table(std::move(rules)), evaluated(table.expressions.size(), one), stamp(table.expressions.size()) {}

    void run(Options options) {
        const State<2> start = order(marked(group.intern("xxxYYYY"), 0), marked(group.intern("xyxYXY"), 0));
        const State<2> basis = order(marked(letters[0], 0), marked(letters[2], 0));
        if (options.wider == 8) between_eights(start, basis);
        else structured({start, basis}, options.wider, options.short_idle);
    }
};
}

int main(int argc, char** argv) {
    if (argc < 2) throw std::runtime_error("expected one Magnus degree");
    wide_cuts::Options options;
    if (argc == 4) {
        options.wider = wide_cuts::small_number(argv[2]);
        options.short_idle = wide_cuts::small_number(argv[3]);
        if ((options.wider != 9 && options.wider != 10) || options.short_idle > 10 - options.wider)
            throw std::runtime_error("counts do not fit a structured length-eighteen cut");
    } else if (argc != 2) throw std::runtime_error("expected degree and optional WIDER IDLE");
    wide_cuts::RuleTable table;
    table.read(std::cin);
    switch (std::stoi(argv[1])) {
    case 5: wide_cuts::Search<5>(std::move(table)).run(options); break;
    case 6: wide_cuts::Search<6>(std::move(table)).run(options); break;
    case 7: wide_cuts::Search<7>(std::move(table)).run(options); break;
    case 8: wide_cuts::Search<8>(std::move(table)).run(options); break;
    case 9: wide_cuts::Search<9>(std::move(table)).run(options); break;
    default: throw std::runtime_error("degree must be five through nine");
    }
}
