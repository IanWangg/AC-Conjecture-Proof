// Exact bounded search using the terminal templates of two six-instruction excursions.
#define AC_ROUND08_MAGNUS_NATIVE_LIBRARY
#include "round07_magnus_native.cpp"

namespace two_sixes {
using free_distance::Id;
using State = free_distance::State<2>;
using Set = std::unordered_set<State, free_distance::StateHash<2>>;
using Layers = std::array<std::array<Set, 3>, 4>;

struct Endpoint {
    std::array<std::string, 2> words;
    std::array<unsigned, 2> marks;
    std::array<unsigned, 2> linear;
};

struct Rule {
    std::string equality;
    std::vector<Endpoint> endpoints;
    std::unordered_map<Id, bool> one_row_cache;
};

State pack(Id a, unsigned mark_a, Id b, unsigned mark_b) {
    if ((a | b) & (1U << 31)) throw std::runtime_error("row ID exceeds 31 bits");
    State state{(a << 1) | mark_a, (b << 1) | mark_b};
    std::sort(state.begin(), state.end());
    return state;
}

std::vector<Rule> read_rules(std::istream& stream) {
    std::vector<Rule> rules;
    std::string equality;
    Endpoint end;
    while (stream >> equality >> end.words[0] >> end.words[1] >> end.marks[0] >> end.marks[1]
                  >> end.linear[0] >> end.linear[1]) {
        if (rules.empty() || rules.back().equality != equality) rules.push_back({equality, {}, {}});
        rules.back().endpoints.push_back(end);
    }
    if (!stream.eof() || rules.size() != 15) throw std::runtime_error("invalid template table");
    return rules;
}

std::size_t letter_slot(char letter) {
    return std::string_view("aAbBxXyY").find(letter);
}

template <class Group>
std::array<Id, 8> alphabet(Group& group, Id a, Id b, const std::array<Id, 4>& fixed) {
    return {a, group.inverse(a), b, group.inverse(b), fixed[0], fixed[1], fixed[2], fixed[3]};
}

template <class Group>
Id evaluate(Group& group, const std::array<Id, 8>& words, Id one, std::string_view expression) {
    for (const char letter : expression) one = group.product(one, words[letter_slot(letter)]);
    return one;
}

template <unsigned Degree>
class Search {
    magnus_native::Elements<Degree> group;
    magnus_native::Elements<3> small;
    const Id one = group.intern("");
    const Id small_one = small.intern("");
    const std::array<Id, 4> fixed{group.intern("x"), group.intern("X"), group.intern("y"), group.intern("Y")};
    const std::array<Id, 4> small_fixed{small.intern("x"), small.intern("X"), small.intern("y"), small.intern("Y")};
    std::vector<Id> image;
    std::unordered_map<State, unsigned, free_distance::StateHash<2>> small_guards;
    std::vector<Rule> rules;

    Id lower(Id value) {
        if (value >= image.size()) image.resize(group.size(), free_distance::missing);
        Id& low = image[value];
        if (low == free_distance::missing) low = group.template project<3>(value, small);
        return low;
    }

    unsigned allowed_rules(Id a, Id b) {
        const State key{lower(a), lower(b)};
        auto [found, fresh] = small_guards.try_emplace(key, 0);
        if (fresh) {
            const auto letters = alphabet(small, key[0], key[1], small_fixed);
            for (std::size_t i = 0; i < rules.size(); ++i)
                if (rules[i].equality == "-" || evaluate(small, letters, small_one, rules[i].equality) == small_one)
                    found->second |= 1U << i;
        }
        return found->second;
    }

    bool guard(Rule& rule, const std::array<Id, 8>& letters) {
        if (rule.equality == "-") return true;
        if (rule.equality.find_first_of("bB") != std::string::npos)
            return evaluate(group, letters, one, rule.equality) == one;
        auto [known, fresh] = rule.one_row_cache.try_emplace(letters[0], false);
        if (fresh) known->second = evaluate(group, letters, one, rule.equality) == one;
        return known->second;
    }

    template <class Visit>
    void idle(State state, Visit&& accept) {
        accept(state);  // Pad the number of idle steps to exactly six.
        for (unsigned i = 0; i < 2; ++i) {
            const unsigned j = i ^ 1;
            const Id r = state[i] >> 1, d = state[j] >> 1;
            const unsigned mr = state[i] & 1, md = state[j] & 1;
            accept(pack(group.inverse(r), mr, d, md));
            accept(pack(group.product(r, d), mr ^ md, d, md));
            accept(pack(group.product(r, group.inverse(d)), mr ^ md, d, md));
            for (unsigned letter = 0; letter < 4; ++letter)
                accept(pack(group.conjugate(r, letter), mr, d, md));
        }
    }

    template <class Visit>
    void excursion(State state, Visit&& accept) {
        for (unsigned i = 0; i < 2; ++i) {
            const unsigned j = i ^ 1;
            const Id a = state[i] >> 1, b = state[j] >> 1;
            const unsigned marks = (state[i] & 1) | ((state[j] & 1) << 1);
            const unsigned allowed = allowed_rules(a, b);
            const auto letters = alphabet(group, a, b, fixed);
            for (std::size_t r = 0; r < rules.size(); ++r) {
                if (!(allowed & (1U << r)) || !guard(rules[r], letters)) continue;
                for (const auto& endpoint : rules[r].endpoints) {
                    const Id left = evaluate(group, letters, one, endpoint.words[0]);
                    const Id right = evaluate(group, letters, one, endpoint.words[1]);
                    const unsigned left_mark = endpoint.marks[0] ^ __builtin_parity(marks & endpoint.linear[0]);
                    const unsigned right_mark = endpoint.marks[1] ^ __builtin_parity(marks & endpoint.linear[1]);
                    accept(pack(left, left_mark, right, right_mark));
                }
            }
        }
    }

    Layers layers(State endpoint) {
        Layers result;
        for (unsigned i = 0; i <= 3; ++i) {
            for (unsigned k = 0; k <= 2; ++k) {
                if (i == 3 && k == 2) continue;  // Test this boundary against the smaller opposite set.
                Set& current = result[i][k];
                auto accept = [&](State state) { current.insert(state); };
                if (i == 0 && k == 0) accept(endpoint);
                if (i > 0) for (const State parent : result[i - 1][k]) idle(parent, accept);
                if (k > 0) for (const State parent : result[i][k - 1]) excursion(parent, accept);
            }
        }
        return result;
    }

    static void print_layers(const Layers& layers) {
        std::cout << '[';
        for (unsigned i = 0; i <= 3; ++i) {
            if (i > 0) std::cout << ',';
            std::cout << '[' << layers[i][0].size() << ',' << layers[i][1].size() << ',';
            if (i < 3) std::cout << layers[i][2].size();
            else std::cout << "null";
            std::cout << ']';
        }
        std::cout << ']';
    }

public:
    explicit Search(std::vector<Rule> rule_table) : rules(std::move(rule_table)) {}

    void run() {
        const auto left = layers(pack(group.intern("xxxYYYY"), 0, group.intern("xyxYXY"), 0));
        const auto right = layers(pack(fixed[0], 0, fixed[2], 0));
        std::size_t middle = 0;
        for (const State candidate : left[3][1]) middle += right[3][1].count(candidate);
        std::array<std::size_t, 2> inspected{};
        std::array<Set, 2> outer;
        for (unsigned side = 0; side < 2; ++side) {
            const auto& source = side == 0 ? left : right;
            const auto& target = side == 0 ? right : left;
            auto accept = [&](State state) {
                ++inspected[side];
                if (target[3][0].count(state)) outer[side].insert(state);
            };
            for (const State parent : source[2][2]) idle(parent, accept);
            for (const State parent : source[3][1]) excursion(parent, accept);
        }
        std::cout << "{\"degree\":" << Degree << ",\"left_layers\":";
        print_layers(left);
        std::cout << ",\"right_layers\":";
        print_layers(right);
        std::cout << ",\"meeting_counts\":[" << outer[0].size() << ',' << middle << ',' << outer[1].size()
                  << "],\"boundary_edges_checked\":[" << inspected[0] << ',' << inspected[1]
                  << "],\"magnus_elements\":" << group.size() << "}\n";
    }
};
}

int main(int argc, char** argv) {
    if (argc != 2) throw std::runtime_error("expected one Magnus degree");
    auto rules = two_sixes::read_rules(std::cin);
    switch (std::stoi(argv[1])) {
    case 5: two_sixes::Search<5>(std::move(rules)).run(); break;
    case 6: two_sixes::Search<6>(std::move(rules)).run(); break;
    case 7: two_sixes::Search<7>(std::move(rules)).run(); break;
    case 8: two_sixes::Search<8>(std::move(rules)).run(); break;
    case 9: two_sixes::Search<9>(std::move(rules)).run(); break;
    default: throw std::runtime_error("degree must be 5 through 9");
    }
}
