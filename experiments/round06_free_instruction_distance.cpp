// Bidirectional breadth-first search in exact free words, with no length cap.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <string_view>
#include <unordered_map>
#include <unordered_set>
#include <vector>

namespace free_distance {
using Id = uint32_t;
constexpr Id missing = std::numeric_limits<Id>::max();
constexpr std::string_view letters = "xXyY";

char inverse_letter(char letter) {
    return letter >= 'a' && letter <= 'z' ? char(letter - 'a' + 'A') : char(letter - 'A' + 'a');
}

std::string concatenate(std::string_view left, std::string_view right) {
    std::size_t overlap = 0;
    while (overlap < left.size() && overlap < right.size()
           && left[left.size() - 1 - overlap] == inverse_letter(right[overlap])) ++overlap;
    std::string result(left.substr(0, left.size() - overlap));
    result.append(right.substr(overlap));
    return result;
}

class WordTable {
    struct Entry {
        const std::string* word;
        Id inverse = missing;
        std::array<Id, 4> conjugates{missing, missing, missing, missing};
    };
    std::unordered_map<std::string, Id> ids;
    std::vector<Entry> entries;

public:
    Id intern(std::string word) {
        if (entries.size() == missing) throw std::runtime_error("word ID space exhausted");
        auto [position, fresh] = ids.try_emplace(std::move(word), Id(entries.size()));
        if (fresh) entries.push_back({&position->first});
        return position->second;
    }

    const std::string& at(Id id) const { return *entries[id].word; }
    std::string describe(Id id) const { return at(id); }
    std::size_t size() const { return entries.size(); }

    Id inverse(Id id) {
        if (entries[id].inverse != missing) return entries[id].inverse;
        std::string word(at(id).rbegin(), at(id).rend());
        std::transform(word.begin(), word.end(), word.begin(), inverse_letter);
        const Id result = intern(std::move(word));
        entries[id].inverse = result;
        entries[result].inverse = id;
        return result;
    }

    Id product(Id first, Id second) {
        return intern(concatenate(at(first), at(second)));
    }

    Id conjugate(Id id, std::size_t letter) {
        if (entries[id].conjugates[letter] != missing) return entries[id].conjugates[letter];
        const auto head = letters.substr(letter, 1);
        const auto tail = letters.substr(letter ^ 1, 1);
        const Id result = intern(concatenate(concatenate(head, at(id)), tail));
        entries[id].conjugates[letter] = result;
        entries[result].conjugates[letter ^ 1] = id;
        return result;
    }
};

template <std::size_t Rows>
using State = std::array<Id, Rows>;

template <std::size_t Rows>
struct StateHash {
    std::size_t operator()(const State<Rows>& state) const {
        uint64_t result = 0x517cc1b727220a95ULL;
        for (const Id value : state) {
            result ^= value;
            result *= 0x9e3779b185ebca87ULL;
            result ^= result >> 29;
        }
        return result;
    }
};

struct Report {
    int distance = -1;
    std::array<int, 2> radii{};
    std::array<std::size_t, 2> visited{1, 1};
    std::size_t words = 0;
    std::vector<std::string> midpoint;
    uint64_t final_boundary_candidates = 0;
};

template <std::size_t Rows, class Elements = WordTable>
Report search(const std::array<std::string, Rows>& first, const std::array<std::string, Rows>& last,
              int limit, bool ordered, bool boundary_only = false) {
    using Seen = std::unordered_set<State<Rows>, StateHash<Rows>>;
    Elements words;
    auto endpoint = [&](const auto& input) {
        State<Rows> state{};
        for (std::size_t i = 0; i < Rows; ++i) state[i] = words.intern(input[i]);
        if (!ordered) std::sort(state.begin(), state.end());
        return state;
    };
    const auto start = endpoint(first), goal = endpoint(last);
    if (start == goal) return {0, {}, {1, 1}, words.size(), {}, 0};
    std::array<std::vector<State<Rows>>, 2> frontier{{{start}, {goal}}};
    std::array<Seen, 2> seen{{{start}, {goal}}};
    Report result;
    for (int depth = 1; depth <= limit; ++depth) {
        const int side = frontier[0].size() <= frontier[1].size() ? 0 : 1;
        const auto& opposite = seen[1 - side];
        auto& own = seen[side];
        std::vector<State<Rows>> following;
        const bool omit_storage = boundary_only && depth == limit;
        auto admit = [&](State<Rows> next) {
            if (!ordered) std::sort(next.begin(), next.end());
            if (omit_storage) ++result.final_boundary_candidates;
            if (opposite.count(next)) {
                for (const auto id : next) result.midpoint.push_back(words.describe(id));
                return true;
            }
            if (!omit_storage && own.insert(next).second) following.push_back(next);
            return false;
        };
        ++result.radii[side];
        for (const auto& state : frontier[side]) {
            State<Rows> inverses{};
            for (std::size_t i = 0; i < Rows; ++i) inverses[i] = words.inverse(state[i]);
            for (std::size_t i = 0; i < Rows && result.distance < 0; ++i) {
                auto replace = [&](Id value) {
                    if (value == state[i]) return false;
                    auto next = state;
                    next[i] = value;
                    return admit(next);
                };
                bool met = replace(inverses[i]);
                for (std::size_t letter = 0; letter < letters.size() && !met; ++letter)
                    met = replace(words.conjugate(state[i], letter));
                for (std::size_t j = 0; j < Rows && !met; ++j) if (j != i) {
                    met = replace(words.product(state[i], state[j]))
                          || replace(words.product(state[i], inverses[j]));
                }
                if (ordered) for (std::size_t j = i + 1; j < Rows && !met; ++j) {
                    auto next = state;
                    std::swap(next[i], next[j]);
                    met = admit(next);
                }
                if (met) result.distance = depth;
            }
            if (result.distance >= 0) break;
        }
        result.visited[side] = own.size();
        if (result.distance >= 0 || following.empty()) break;
        frontier[side] = std::move(following);
    }
    result.words = words.size();
    return result;
}

template <std::size_t Rows>
void run(int limit, bool ordered, bool boundary_only) {
    const std::array<std::string, Rows> initial{"xxxYYYY", "xyxYXY"}, basis{"x", "y"};
    const Report result = search(initial, basis, limit, ordered, boundary_only);
    const std::string distance = result.distance < 0 ? "null" : std::to_string(result.distance);
    std::cout << "{\"spare_rows\":" << Rows - 2 << ",\"limit\":" << limit
              << ",\"ordered\":" << (ordered ? "true" : "false")
              << ",\"distance\":" << distance << ",\"radii\":[" << result.radii[0]
              << "," << result.radii[1] << "],\"visited\":[" << result.visited[0] << ","
              << result.visited[1] << "],\"distinct_words\":" << result.words;
    if (boundary_only)
        std::cout << ",\"final_boundary_candidates\":" << result.final_boundary_candidates;
    std::cout << "}\n";
}

void selftest() {
    const std::array<std::string, 2> basis{"x", "y"}, changed{"xy", "y"}, swapped{"y", "x"};
    if (search(changed, basis, 1, true).distance != 1 || search(swapped, basis, 1, true).distance != 1
        || search(swapped, basis, 0, false).distance != 0
        || search(std::array<std::string, 2>{"yxY", "Y"}, basis, 1, false).distance >= 0
        || search(std::array<std::string, 2>{"yxY", "Y"}, basis, 2, false).distance != 2)
        throw std::runtime_error("instruction search control failed");
}
}

#ifndef AC_ROUND06_INSTRUCTION_DISTANCE_LIBRARY
int main(int argc, char** argv) {
    try {
        if (argc < 3 || argc > 5)
            throw std::runtime_error("usage: search spare_rows limit [--ordered] [--boundary-only]");
        free_distance::selftest();
        const int spare = std::stoi(argv[1]), limit = std::stoi(argv[2]);
        if (limit < 0) throw std::runtime_error("negative search limit");
        bool ordered = false, boundary_only = false;
        for (int i = 3; i < argc; ++i) {
            const std::string_view option(argv[i]);
            if (option == "--ordered" && !ordered) ordered = true;
            else if (option == "--boundary-only" && !boundary_only) boundary_only = true;
            else throw std::runtime_error("unexpected search option");
        }
        switch (spare) {
        case 0: free_distance::run<2>(limit, ordered, boundary_only); break;
        case 1: free_distance::run<3>(limit, ordered, boundary_only); break;
        case 2: free_distance::run<4>(limit, ordered, boundary_only); break;
        case 3: free_distance::run<5>(limit, ordered, boundary_only); break;
        case 4: free_distance::run<6>(limit, ordered, boundary_only); break;
        default: throw std::runtime_error("spare row count outside 0–4");
        }
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
#endif
