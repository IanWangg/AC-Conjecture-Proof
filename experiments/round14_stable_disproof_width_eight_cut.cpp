// Exclude an isolated width-eight interval using cubic guards at the idle cut.
#define AC_ROUND08_MAGNUS_NATIVE_LIBRARY
#include "round07_magnus_native.cpp"
#include <map>

namespace width_eight_cut {
using free_distance::Id;
using State = free_distance::State<2>;
using Set = std::unordered_set<State, free_distance::StateHash<2>>;
using Pair = std::array<std::string, 2>;
using Layers = std::array<std::array<Set, 2>, 6>;

struct Rule {
    std::string equality;
    std::vector<Pair> endpoints;
};

using Rules = std::unordered_map<unsigned, std::vector<Rule>>;

State ordered(Id a, Id b) { return a < b ? State{a, b} : State{b, a}; }
unsigned input_key(unsigned a, unsigned b) { return (a << 15) | b; }

Rules read_rules(std::istream& input) {
    std::unordered_map<unsigned, std::map<std::string, std::vector<Pair>>> grouped;
    std::string equality, left, right;
    unsigned a, b;
    std::size_t count = 0;
    while (input >> a >> b >> equality >> left >> right) {
        if (a >= (1U << 15) || b >= (1U << 15)) throw std::runtime_error("invalid cubic input");
        grouped[input_key(a, b)][equality].push_back({left, right});
        ++count;
    }
    if (!input.eof() || count != 9504) throw std::runtime_error("incomplete cubic rule table");
    Rules result;
    for (auto& [key, relations] : grouped)
        for (auto& [equality, endpoints] : relations) result[key].push_back({equality, std::move(endpoints)});
    return result;
}

template <unsigned Degree>
class Search {
    magnus_native::Elements<Degree> group;
    magnus_native::Elements<3> cubic;
    const Id one = group.intern("");
    const std::array<Id, 4> generators{group.intern("x"), group.intern("X"), group.intern("y"), group.intern("Y")};
    static constexpr uint16_t unknown = std::numeric_limits<uint16_t>::max();
    std::vector<uint16_t> cubic_values;
    std::vector<uint16_t> images;
    Rules rules;

    unsigned project(Id value) {
        if (value >= images.size()) images.resize(group.size(), unknown);
        auto& result = images[value];
        if (result == unknown) {
            const Id image = group.template project<3>(value, cubic);
            if (image >= cubic_values.size()) cubic_values.resize(cubic.size(), unknown);
            auto& bits = cubic_values[image];
            if (bits == unknown) bits = std::stoul(cubic.describe(image), nullptr, 16);
            result = bits;
        }
        return result;
    }

    Id evaluate(std::string_view word, const std::array<Id, 8>& alphabet) {
        Id value = one;
        for (const char letter : word)
            value = group.product(value, alphabet[std::string_view("aAbBxXyY").find(letter)]);
        return value;
    }

    template <class Visit>
    void idle(State state, Visit&& accept) {
        accept(state);
        for (unsigned i = 0; i < 2; ++i) {
            const Id a = state[i], b = state[i ^ 1];
            accept(ordered(group.inverse(a), b));
            accept(ordered(group.product(a, b), b));
            accept(ordered(group.product(a, group.inverse(b)), b));
            for (unsigned letter = 0; letter < 4; ++letter)
                accept(ordered(group.conjugate(a, letter), b));
        }
    }

    template <class Visit>
    void excursion(State state, Visit&& accept) {
        for (unsigned i = 0; i < 2; ++i) {
            const Id a = state[i], b = state[i ^ 1];
            const unsigned old_a = project(a), old_b = project(b);
            const auto found = rules.find(input_key(old_a, old_b));
            if (found == rules.end()) continue;
            const std::array<Id, 8> alphabet{a, group.inverse(a), b, group.inverse(b), generators[0], generators[1],
                                             generators[2], generators[3]};
            for (const Rule& rule : found->second) {
                if (rule.equality != "-" && evaluate(rule.equality, alphabet) != one) continue;
                for (const auto& endpoint : rule.endpoints)
                    accept(ordered(evaluate(endpoint[0], alphabet), evaluate(endpoint[1], alphabet)));
            }
        }
    }

    Layers layers(State start) {
        Layers result;
        result[0][0].insert(start);
        for (unsigned i = 0; i <= 5; ++i) {
            if (i > 0)
                for (const State parent : result[i - 1][0])
                    idle(parent, [&](State state) { result[i][0].insert(state); });
            if (i == 5) break;
            auto accept = [&](State state) { result[i][1].insert(state); };
            if (i > 0) for (const State parent : result[i - 1][1]) idle(parent, accept);
            for (const State parent : result[i][0]) excursion(parent, accept);
        }
        return result;
    }

    static void print_layers(const std::array<Layers, 2>& walks) {
        for (unsigned side = 0; side < 2; ++side) {
            if (side > 0) std::cout << ',';
            std::cout << '[';
            for (unsigned i = 0; i <= 5; ++i) {
                if (i > 0) std::cout << ',';
                std::cout << '[' << walks[side][i][0].size() << ',' << walks[side][i][1].size() << ']';
            }
            std::cout << ']';
        }
    }

public:
    explicit Search(Rules input) : rules(std::move(input)) {}

    void run() {
        const State start = ordered(group.intern("xxxYYYY"), group.intern("xyxYXY"));
        const State basis = ordered(generators[0], generators[2]);
        const std::array<Layers, 2> walks{layers(start), layers(basis)};
        std::array<Set, 2> hits;
        std::array<std::size_t, 2> edge_counts{};
        for (unsigned side = 0; side < 2; ++side) {
            const Set& other = walks[side ^ 1][5][0];
            auto accept = [&](State state) {
                ++edge_counts[side];
                if (other.count(state)) hits[side].insert(state);
            };
            for (const State parent : walks[side][4][1]) idle(parent, accept);
            for (const State parent : walks[side][5][0]) excursion(parent, accept);
        }
        std::cout << "{\"degree\":" << Degree << ",\"widths\":[";
        print_layers(walks);
        std::cout << "],\"midpoints\":[" << hits[0].size() << ',' << hits[1].size() << "],\"edges\":[" << edge_counts[0]
                  << ',' << edge_counts[1] << "],\"elements\":" << group.size() << "}\n";
    }
};
}

int main(int argc, char** argv) {
    if (argc != 2) throw std::runtime_error("expected one Magnus degree");
    auto rules = width_eight_cut::read_rules(std::cin);
    switch (std::stoi(argv[1])) {
    case 6: width_eight_cut::Search<6>(std::move(rules)).run(); break;
    case 7: width_eight_cut::Search<7>(std::move(rules)).run(); break;
    case 8: width_eight_cut::Search<8>(std::move(rules)).run(); break;
    case 9: width_eight_cut::Search<9>(std::move(rules)).run(); break;
    default: throw std::runtime_error("degree must be between six and nine");
    }
}
