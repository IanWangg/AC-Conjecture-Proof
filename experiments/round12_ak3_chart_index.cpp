// Look up many cyclic target words at once in each completed donor chart.
#define AC_ROUND08_ACM_LIBRARY
#include "round08_ak3_acm.cpp"

#include <set>

namespace chart_index {
constexpr size_t prefix_length = 5;
constexpr size_t prefix_count = 2 << (2 * prefix_length);
using Edge = std::pair<int, int>;

struct Index {
    const std::vector<acm08::Row>& graph;
    std::array<std::vector<Edge>, prefix_count> prefixes;

    explicit Index(const std::vector<acm08::Row>& source) : graph(source) {
        for (size_t base = 0; base < graph.size(); ++base)
            visit(int(base), int(base), 1, 0, -1);
    }

    void visit(int base, int at, size_t key, size_t length, int previous) {
        if (length) prefixes[key].emplace_back(base, at);
        if (length == prefix_length) return;
        for (int letter = 0; letter < 4; ++letter) {
            const int target = graph[at][letter];
            if (target >= 0 && (letter ^ 1) != previous)
                visit(base, target, 4 * key + letter, length + 1, letter);
        }
    }

    bool contains(const std::string& word) const {
        const auto length = std::min(word.size(), prefix_length);
        const auto doubled = word + word;
        size_t best_offset = 0, best_key = 0;
        for (size_t offset = 0; offset < word.size(); ++offset) {
            size_t key = 1;
            for (size_t i = offset; i < offset + length; ++i)
                key = 4 * key + acm08::letters.find(doubled[i]);
            if (prefixes[key].empty()) return false;
            if (!best_key || prefixes[key].size() < prefixes[best_key].size()) {
                best_key = key;
                best_offset = offset;
            }
        }
        const auto suffix = std::string_view(doubled).substr(best_offset + length, word.size() - length);
        for (const auto& [start, middle] : prefixes[best_key])
            if (acm08::follow(graph, middle, suffix) == start) return true;
        return false;
    }
};

void run(const std::string& receiver, const std::string& donor, unsigned depth, size_t limit) {
    using namespace acm08;
    if (receiver.empty() || donor.empty() || cyclic(receiver) != receiver || cyclic(donor) != donor ||
        std::abs(determinant(abel(receiver), abel(donor))) != 1)
        throw std::invalid_argument("expected a cyclic pair with unimodular exponents");
    std::set<std::string> pending;
    for (std::string word; std::cin >> word;) {
        if (word.empty() || cyclic(word) != word || std::abs(determinant(abel(word), abel(donor))) != 1)
            throw std::invalid_argument("invalid target word " + word);
        pending.insert(word);
    }
    Folding folding(limit);
    folding.add_loop(0, receiver);
    const auto rotations = variants(donor);
    std::vector<size_t> sizes;
    std::vector<std::pair<std::string, unsigned>> hits;
    bool allocation_stop = false;
    for (unsigned stage = 0; stage <= depth; ++stage) {
        if (stage) {
            const auto vertices = folding.vertices();
            try {
                for (int vertex : vertices)
                    for (const auto& rotation : rotations) folding.add_loop(vertex, rotation);
            } catch (const SizeLimit&) {
                allocation_stop = true;
                break;
            }
        }
        const auto graph = folding.compact();
        const Index index(graph);
        sizes.push_back(graph.size());
        for (auto at = pending.begin(); at != pending.end();) {
            if (index.contains(*at)) {
                hits.emplace_back(*at, stage);
                at = pending.erase(at);
            } else {
                ++at;
            }
        }
        if (pending.empty()) break;
    }
    std::cout << "{\"graph_sizes\":[";
    for (size_t i = 0; i < sizes.size(); ++i)
        std::cout << (i ? "," : "") << sizes[i];
    std::cout << "],\"allocation_stop\":" << (allocation_stop ? "true" : "false") << ",\"hits\":[";
    for (size_t i = 0; i < hits.size(); ++i)
        std::cout << (i ? "," : "") << "[\"" << hits[i].first << "\"," << hits[i].second << ']';
    std::cout << "]}\n";
}
}  // namespace chart_index

int main(int argc, char** argv) {
    try {
        if (argc != 5)
            throw std::invalid_argument("usage: chart-index receiver donor depth allocation_cap < words");
        chart_index::run(argv[1], argv[2], std::stoul(argv[3]), std::stoull(argv[4]));
    } catch (const acm08::SizeLimit&) {
        std::cerr << "allocation limit does not fit the initial receiver\n";
        return 1;
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
