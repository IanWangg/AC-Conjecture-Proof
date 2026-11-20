// Bound a degree-nine retraction with one width-six and one width-seven interval.
#define AC_ROUND08_MAGNUS_NATIVE_LIBRARY
#include "round07_magnus_native.cpp"

namespace mixed_widths {
using free_distance::Id;
using State = free_distance::State<2>;
using Hash = free_distance::StateHash<2>;
using Set = std::unordered_set<State, Hash>;
using Layers = std::vector<std::array<Set, 4>>;

struct Expression {
    unsigned parent;
    unsigned symbol;
};

class Words {
    std::unordered_map<std::string, unsigned> catalogue{{"", 0}};

public:
    std::vector<Expression> expressions{{0, 0}};

    unsigned add(std::string word) {
        const unsigned parent = word.empty() ? 0 : add(word.substr(0, word.size() - 1));
        auto [found, fresh] = catalogue.try_emplace(word, expressions.size());
        if (fresh) {
            const auto slot = std::string_view("aAbBxXyY").find(word.back());
            if (slot == std::string_view::npos) throw std::runtime_error("invalid template letter");
            expressions.push_back({parent, static_cast<unsigned>(slot)});
        }
        return found->second;
    }
};

struct Endpoint {
    std::array<unsigned, 2> words, marks, linear;
};

struct Rule {
    unsigned equality;
    bool only_a;
    std::vector<Endpoint> endpoints;
    std::unordered_map<Id, bool> unary_equality;
};

struct Tables {
    Words words;
    std::array<std::vector<Rule>, 2> rules;
};

struct StructuredCut {
    unsigned short_rule;
    unsigned active_width;
    unsigned short_idle;
};

unsigned small_number(std::string_view argument) {
    std::size_t used = 0;
    const auto value = std::stoul(std::string(argument), &used);
    if (used != argument.size() || value > 18) throw std::runtime_error("invalid structured cut argument");
    return static_cast<unsigned>(value);
}

Tables read(std::istream& stream, bool two_sevens) {
    Tables input;
    unsigned span;
    std::string relation, left, right;
    Endpoint endpoint;
    std::array<std::size_t, 2> counts{};
    while (stream >> span >> relation >> left >> right >> endpoint.marks[0] >> endpoint.marks[1]
                  >> endpoint.linear[0] >> endpoint.linear[1]) {
        if (span != 6 && span != 7) throw std::runtime_error("unsupported interval width");
        const unsigned width = span - 6;
        auto& rules = input.rules[width];
        const unsigned equality = relation == "-" ? 0 : input.words.add(relation);
        if (rules.empty() || rules.back().equality != equality)
            rules.push_back({equality, relation.find_first_of("bB") == std::string::npos, {}, {}});
        endpoint.words = {input.words.add(left), input.words.add(right)};
        rules.back().endpoints.push_back(endpoint);
        ++counts[width];
    }
    const std::array<std::size_t, 2> expected = two_sevens ? std::array<std::size_t, 2>{0, 7047}
                                                         : std::array<std::size_t, 2>{136, 5769};
    if (!stream.eof() || counts != expected)
        throw std::runtime_error("incomplete marked transition table");
    return input;
}

State pack(Id a, unsigned mark_a, Id b, unsigned mark_b) {
    if ((a | b) & (1U << 31)) throw std::runtime_error("row ID exceeds 31 bits");
    const Id left = (a << 1) | mark_a, right = (b << 1) | mark_b;
    return left < right ? State{left, right} : State{right, left};
}

template <class Group>
class Evaluation {
    Group& group;
    const std::vector<Expression>& expressions;
    std::array<Id, 8> alphabet{};
    std::vector<Id> values;
    std::vector<unsigned> stamps;
    unsigned generation = 0;

public:
    Evaluation(Group& group, const std::vector<Expression>& words)
        : group(group), expressions(words), values(words.size(), group.intern("")), stamps(words.size()) {}

    void mark(Id a, Id b, const std::array<Id, 4>& fixed) {
        alphabet = {a, group.inverse(a), b, group.inverse(b), fixed[0], fixed[1], fixed[2], fixed[3]};
        if (++generation == 0) {
            std::fill(stamps.begin(), stamps.end(), 0);
            ++generation;
        }
    }

    Id evaluate(unsigned expression) {
        if (expression != 0 && stamps[expression] != generation) {
            const auto& node = expressions[expression];
            values[expression] = group.product(evaluate(node.parent), alphabet[node.symbol]);
            stamps[expression] = generation;
        }
        return values[expression];
    }
};

template <unsigned Degree>
class Search {
    using Active = free_distance::State<3>;
    using ActiveSet = std::unordered_set<Active, free_distance::StateHash<3>>;

    magnus_native::Elements<Degree> high;
    magnus_native::Elements<3> low;
    Tables tables;
    const bool two_sevens;
    Evaluation<magnus_native::Elements<Degree>> marked{high, tables.words.expressions};
    Evaluation<magnus_native::Elements<3>> coarse{low, tables.words.expressions};
    const std::array<Id, 4> high_letters{high.intern("x"), high.intern("X"), high.intern("y"), high.intern("Y")};
    const std::array<Id, 4> low_letters{low.intern("x"), low.intern("X"), low.intern("y"), low.intern("Y")};
    const Id high_one = high.intern(""), low_one = low.intern("");
    std::vector<Id> projections;
    std::array<std::unordered_map<State, std::vector<unsigned>, Hash>, 2> permitted;

    Id project(Id value) {
        if (value >= projections.size()) projections.resize(high.size(), free_distance::missing);
        Id& image = projections[value];
        if (image == free_distance::missing) image = high.template project<3>(value, low);
        return image;
    }

    const std::vector<unsigned>& allowed(Id a, Id b, unsigned width) {
        const State key{project(a), project(b)};
        auto [found, fresh] = permitted[width].try_emplace(key);
        if (fresh) {
            coarse.mark(key[0], key[1], low_letters);
            const auto& rules = tables.rules[width];
            for (unsigned r = 0; r < rules.size(); ++r)
                if (coarse.evaluate(rules[r].equality) == low_one) found->second.push_back(r);
        }
        return found->second;
    }

    bool guard(Rule& rule, Id a) {
        if (rule.equality == 0) return true;
        if (!rule.only_a) return marked.evaluate(rule.equality) == high_one;
        auto [found, fresh] = rule.unary_equality.try_emplace(a, false);
        if (fresh) found->second = marked.evaluate(rule.equality) == high_one;
        return found->second;
    }

    template <class Visit>
    void idle(State state, Visit&& accept) {
        accept(state);
        for (unsigned i = 0; i < 2; ++i) {
            const unsigned j = i ^ 1;
            const Id a = state[i] >> 1, b = state[j] >> 1;
            const unsigned ma = state[i] & 1, mb = state[j] & 1;
            accept(pack(high.inverse(a), ma, b, mb));
            accept(pack(high.product(a, b), ma ^ mb, b, mb));
            accept(pack(high.product(a, high.inverse(b)), ma ^ mb, b, mb));
            for (unsigned letter = 0; letter < 4; ++letter)
                accept(pack(high.conjugate(a, letter), ma, b, mb));
        }
    }

    template <class Visit>
    void excursion(State state, unsigned width, bool restore, Visit&& accept) {
        for (unsigned i = 0; i < 2; ++i) {
            const unsigned j = i ^ 1;
            const Id a = state[i] >> 1, b = state[j] >> 1;
            const unsigned input = (state[i] & 1) | ((state[j] & 1) << 1);
            const auto& coarse_rules = allowed(a, b, width);
            marked.mark(a, b, high_letters);
            for (const unsigned index : coarse_rules) {
                auto& rule = tables.rules[width][index];
                if (!guard(rule, a)) continue;
                for (const auto& endpoint : rule.endpoints) {
                    const unsigned left = endpoint.marks[0] ^ __builtin_parity(input & endpoint.linear[0]);
                    const unsigned right = endpoint.marks[1] ^ __builtin_parity(input & endpoint.linear[1]);
                    if (restore && (left | right)) continue;
                    accept(pack(marked.evaluate(endpoint.words[0]), left, marked.evaluate(endpoint.words[1]), right));
                }
            }
        }
    }

    template <class Visit>
    void last_excursions(const std::array<Set, 4>& layer, unsigned used, Visit&& accept) {
        if (two_sevens) {
            if (used != 0)
                for (const State parent : layer[used == 3 ? 1 : 0]) excursion(parent, 1, used == 3, accept);
        } else {
            for (unsigned width = 0; width < 2; ++width)
                if (used & (1U << width))
                    for (const State parent : layer[used ^ (1U << width)]) excursion(parent, width, used == 3, accept);
        }
    }

    Layers layers(State start, unsigned idle_steps) {
        Layers result(idle_steps + 1);
        for (unsigned i = 0; i <= idle_steps; ++i) {
            for (unsigned used = 0; used < 4; ++used) {
                if ((two_sevens && used == 2) || (i == idle_steps && used == 3)) continue;
                auto accept = [&](State state) { result[i][used].insert(state); };
                if (i == 0 && used == 0) accept(start);
                if (i > 0)
                    for (const State previous : result[i - 1][used]) idle(previous, accept);
                last_excursions(result[i], used, accept);
            }
        }
        return result;
    }

    static void print(const Layers& layers) {
        std::cout << '[';
        for (unsigned i = 0; i < layers.size(); ++i) {
            if (i > 0) std::cout << ',';
            std::cout << '[';
            for (unsigned used = 0; used < 4; ++used) {
                if (used > 0) std::cout << ',';
                std::cout << layers[i][used].size();
            }
            std::cout << ']';
        }
        std::cout << ']';
    }

    struct IdleBoundaries {
        std::vector<Set> plain, via_short;
    };

    IdleBoundaries boundaries(State endpoint, unsigned maximum_idle, StructuredCut cut) {
        IdleBoundaries result{std::vector<Set>(maximum_idle + 1), std::vector<Set>(cut.short_idle + 1)};
        result.plain[0].insert(endpoint);
        for (unsigned i = 1; i <= maximum_idle; ++i)
            for (const State state : result.plain[i - 1]) idle(state, [&](State child) { result.plain[i].insert(child); });
        for (unsigned i = 0; i <= cut.short_idle; ++i) {
            auto accept = [&](State child) { result.via_short[i].insert(child); };
            if (i > 0) for (const State state : result.via_short[i - 1]) idle(state, accept);
            for (const State state : result.plain[i]) excursion(state, cut.short_rule, false, accept);
        }
        return result;
    }

    template <class Visit>
    void active_edges(Active state, Visit&& accept) {
        if constexpr (Degree < 9) accept(state);
        auto change = [&](unsigned row, Id value, unsigned mark) {
            if constexpr (Degree == 9)
                if (value == high_one || value == (state[row] >> 1)) return;
            if (value & (1U << 31)) throw std::runtime_error("row ID exceeds 31 bits");
            Active child = state;
            child[row] = (value << 1) | mark;
            std::sort(child.begin(), child.end());
            accept(child);
        };
        for (unsigned i = 0; i < 3; ++i) {
            const Id a = state[i] >> 1;
            const unsigned mark_a = state[i] & 1;
            change(i, high.inverse(a), mark_a);
            for (unsigned letter = 0; letter < 4; ++letter) change(i, high.conjugate(a, letter), mark_a);
            for (unsigned j = 0; j < 3; ++j) if (i != j) {
                const Id b = state[j] >> 1;
                const unsigned mark = mark_a ^ (state[j] & 1);
                change(i, high.product(a, b), mark);
                change(i, high.product(a, high.inverse(b)), mark);
            }
        }
    }

    ActiveSet active_layer(const Set& boundary, unsigned depth) {
        ActiveSet layer;
        for (const State pair : boundary) for (unsigned donor = 0; donor < 2; ++donor) {
            const Id copy = pair[donor] >> 1;
            const unsigned mark = (pair[donor] & 1) ^ 1;
            for (const Id value : {copy, high.inverse(copy)}) {
                if (value & (1U << 31)) throw std::runtime_error("row ID exceeds 31 bits");
                Active child{pair[0], pair[1], (value << 1) | mark};
                std::sort(child.begin(), child.end());
                layer.insert(child);
            }
        }
        for (unsigned i = 1; i < depth; ++i) {
            ActiveSet next;
            for (const Active state : layer) active_edges(state, [&](Active child) { next.insert(child); });
            layer = std::move(next);
        }
        return layer;
    }

public:
    Search(Tables input, bool repeated_width) : tables(std::move(input)), two_sevens(repeated_width) {}

    void run() {
        const State start = pack(high.intern("xxxYYYY"), 0, high.intern("xyxYXY"), 0);
        const State goal = pack(high_letters[0], 0, high_letters[2], 0);
        const std::array<Layers, 2> walks{layers(start, 2), layers(goal, two_sevens ? 2 : 3)};
        std::array<std::size_t, 2> edges{};
        std::array<std::size_t, 4> meetings{};
        if (two_sevens) {
            for (const State state : walks[0].back()[1]) meetings[1] += walks[1].back()[1].count(state);
        } else {
            for (unsigned used : {1, 2})
                for (const State state : walks[0].back()[used]) meetings[used] += walks[1].back()[used ^ 3].count(state);
        }
        for (unsigned side = 0; side < 2; ++side) {
            const auto& walk = walks[side];
            const Set& opposite = walks[side ^ 1].back()[0];
            Set matched;
            auto accept = [&](State state) {
                ++edges[side];
                if (opposite.count(state)) matched.insert(state);
            };
            for (const State previous : walk[walk.size() - 2][3]) idle(previous, accept);
            last_excursions(walk.back(), 3, accept);
            meetings[side == 0 ? 3 : 0] = matched.size();
        }
        std::cout << "{\"degree\":" << Degree << ",\"left_layers\":";
        print(walks[0]);
        std::cout << ",\"right_layers\":";
        print(walks[1]);
        std::cout << ",\"meetings\":[" << meetings[0] << ',' << meetings[1] << ',';
        if (!two_sevens) std::cout << meetings[2] << ',';
        std::cout << meetings[3] << "],\"edges\":[" << edges[0] << ',' << edges[1]
                  << "],\"elements\":" << high.size() << "}\n";
    }

    void run_structured(StructuredCut cut) {
        const unsigned idle_budget = 18 - (6 + cut.short_rule) - cut.active_width;
        if (cut.short_idle > idle_budget) throw std::runtime_error("invalid split of the remaining idle instructions");
        const unsigned plain_idle = idle_budget - cut.short_idle;
        const unsigned short_depth = 5 - cut.short_rule - cut.short_idle, plain_depth = cut.active_width - short_depth;
        const State start = pack(high.intern("xxxYYYY"), 0, high.intern("xyxYXY"), 0);
        const State goal = pack(high_letters[0], 0, high_letters[2], 0);
        const unsigned maximum_idle = std::max(cut.short_idle, plain_idle);
        const std::array<IdleBoundaries, 2> endpoints{boundaries(start, maximum_idle, cut), boundaries(goal, maximum_idle, cut)};
        std::cout << "{\"degree\":" << Degree << ",\"short_idle\":" << cut.short_idle << ",\"active_depths\":[" << short_depth
                  << ',' << plain_depth << "],\"orientations\":[";
        for (unsigned side = 0; side < 2; ++side) {
            const Set& short_boundary = endpoints[side].via_short[cut.short_idle];
            const Set& plain_boundary = endpoints[side ^ 1].plain[plain_idle];
            const auto left = active_layer(short_boundary, short_depth);
            const auto almost_right = active_layer(plain_boundary, plain_depth - 1);
            ActiveSet matched;
            std::size_t edges = 0;
            for (const Active state : almost_right) active_edges(state, [&](Active child) {
                ++edges;
                if (left.count(child)) matched.insert(child);
            });
            if (side > 0) std::cout << ',';
            std::cout << "{\"short_boundary\":" << short_boundary.size() << ",\"plain_boundary\":" << plain_boundary.size()
                      << ",\"active_layer\":" << left.size() << ",\"penultimate_layer\":" << almost_right.size()
                      << ",\"edges\":" << edges << ",\"meetings\":" << matched.size() << '}' << std::flush;
        }
        std::cout << "]}\n";
    }
};

template <unsigned Degree>
void run(Tables tables, bool two_sevens, std::optional<StructuredCut> cut) {
    Search<Degree> search(std::move(tables), two_sevens);
    if (cut) search.run_structured(*cut);
    else search.run();
}
}

int main(int argc, char** argv) {
    const std::string_view mode = argc > 2 ? argv[2] : "";
    const bool two_sevens = argc == 3 && mode == "--two-sevens";
    std::optional<mixed_widths::StructuredCut> cut;
    if (argc == 4 && mode == "--six-eight") {
        cut = mixed_widths::StructuredCut{0, 8, mixed_widths::small_number(argv[3])};
    } else if (argc == 6 && mode == "--structured") {
        const unsigned shorter = mixed_widths::small_number(argv[3]), wider = mixed_widths::small_number(argv[4]);
        if ((shorter != 6 && shorter != 7) || wider < 8 || shorter + wider > 18)
            throw std::runtime_error("structured cut requires a short width of six or seven and a wider interval within budget");
        cut = mixed_widths::StructuredCut{shorter - 6, wider, mixed_widths::small_number(argv[5])};
    }
    if (argc != 2 && !two_sevens && !cut)
        throw std::runtime_error("expected degree with optional --two-sevens, --six-eight IDLE or --structured SHORT WIDE IDLE");
    auto tables = mixed_widths::read(std::cin, two_sevens || (cut && cut->short_rule == 1));
    switch (std::stoi(argv[1])) {
    case 5: mixed_widths::run<5>(std::move(tables), two_sevens, cut); break;
    case 6: mixed_widths::run<6>(std::move(tables), two_sevens, cut); break;
    case 7: mixed_widths::run<7>(std::move(tables), two_sevens, cut); break;
    case 8: mixed_widths::run<8>(std::move(tables), two_sevens, cut); break;
    case 9: mixed_widths::run<9>(std::move(tables), two_sevens, cut); break;
    default: throw std::runtime_error("degree must be between five and nine");
    }
}
