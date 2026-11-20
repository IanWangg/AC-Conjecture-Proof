// Audit donor-free first exits by stack reduction of each literal product.
#define AC_ROUND11_REVERSE_LIBRARY
#include "round11_stable_proof_reverse.cpp"

namespace {

struct Entry {
    Triple rows;
    bool chart;
    bool reached;
};

std::string stack_product(std::string_view left, std::string_view right) {
    std::string result;
    result.reserve(left.size() + right.size());
    for (auto part : {left, right}) for (char c : part) {
        if (!result.empty() && result.back() == invchar(c)) result.pop_back();
        else result.push_back(c);
    }
    size_t begin = 0, end = result.size();
    while (end - begin > 1 && result[begin] == invchar(result[end - 1])) {
        ++begin;
        --end;
    }
    return result.substr(begin, end - begin);
}

std::vector<std::string> literal_variants(const std::string& word) {
    std::set<std::string> choices;
    for (const auto& oriented : {word, inverse(word)})
        for (size_t i = 0; i < oriented.size(); ++i)
            choices.insert(oriented.substr(i) + oriented.substr(0, i));
    return {choices.begin(), choices.end()};
}

void verify(unsigned cap, const char* roots_path, const char* nodes_path) {
    CompactOrbits orbits;
    const auto short_code = orbits.word(encode("xxyXYY")).best;
    std::unordered_map<Key, Entry, KeyHash> nodes;
    std::vector<Key> pending;
    std::ifstream roots(roots_path), data(nodes_path);
    if (!roots || !data) throw std::runtime_error("cannot open audit catalogue");
    size_t ancestor, pivots;
    Triple rows;
    while (data >> ancestor >> pivots >> rows[0] >> rows[1] >> rows[2]) {
        orbits.limit();
        if (!in_range(rows, 3, cap) || std::any_of(rows.begin(), rows.end(), [&](const auto& word) {
                return orbits.word(encode(word)).best == short_code;
            })) throw std::runtime_error("invalid catalogue row");
        const auto point = signed_key(orbits, rows);
        if (rows_from(point) != rows || !nodes.emplace(point, Entry{rows, pivots != 0, false}).second)
            throw std::runtime_error("repeated or noncanonical catalogue row");
    }
    if (!data.eof() || nodes.empty()) throw std::runtime_error("incomplete catalogue input");
    while (roots >> rows[0] >> rows[1] >> rows[2]) {
        orbits.limit();
        const auto point = signed_key(orbits, rows);
        auto& entry = nodes.at(point);
        if (entry.chart || entry.reached) throw std::runtime_error("invalid root");
        entry.reached = true;
        pending.push_back(point);
    }
    if (!roots.eof() || pending.empty()) throw std::runtime_error("incomplete roots input");
    const auto root_count = pending.size();
    size_t exits = 0;
    uint64_t products = 0;
    for (size_t head = 0; head < pending.size(); ++head) {
        const auto& source = nodes.at(pending[head]).rows;
        const auto total = energy(source);
        std::array<std::vector<std::string>, 3> rotations;
        for (size_t i = 0; i < 3; ++i) rotations[i] = literal_variants(source[i]);
        std::set<Triple> results;
        for (size_t i = 0; i < 3; ++i) for (size_t j = 0; j < 3; ++j) {
            if (i == j) continue;
            const auto allowance = cap - total + source[i].size();
            if (total + source[j].size() + 2 <= cap || allowance > 21)
                throw std::runtime_error("literal audit bound does not cover this menu");
            for (const auto& a : rotations[i]) for (const auto& b : rotations[j]) {
                ++products;
                const auto word = stack_product(a, b);
                if (word.empty()) throw std::runtime_error("zero product in a basis tuple");
                if (word.size() > allowance) continue;
                auto target = source;
                target[i] = canonical(word);
                results.insert(std::move(target));
            }
        }
        for (const auto& target : results) {
            orbits.limit();
            if (std::any_of(target.begin(), target.end(), [&](const auto& word) {
                    return orbits.word(encode(word)).best == short_code;
                })) continue;
            const auto point = signed_key(orbits, target);
            auto& entry = nodes.at(point);
            if (entry.reached) continue;
            entry.reached = true;
            if (entry.chart) ++exits;
            else pending.push_back(point);
        }
    }
    if (pending.size() + exits != nodes.size()) throw std::runtime_error("unreached catalogue row");
    std::cout << "{\"cap\":" << cap << ",\"roots\":" << root_count
              << ",\"closed_chartless\":" << pending.size() << ",\"first_exits\":" << exits
              << ",\"stack_candidates\":" << products << "}\n";
}

}

int main(int argc, char** argv) {
    try {
        if (argc != 4) throw std::runtime_error("usage: stack-audit cap roots.tsv nodes.tsv");
        verify(std::stoul(argv[1]), argv[2], argv[3]);
    } catch (const std::exception& e) {
        std::cerr << e.what() << '\n';
        return 1;
    }
}
