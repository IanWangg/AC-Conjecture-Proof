// Bounded cyclic product search starting at an unanchored chart projection.
#define AC_ROUND05_ORBITS_LIBRARY
#include "round05_ak3_orbits.cpp"
#include "round06_ak3_wide_pair.hpp"

#include <set>

namespace {
using namespace orbit_search;

struct Node { ak3_wide::Pair state; size_t parent; };
constexpr size_t root = std::numeric_limits<size_t>::max();

bool has_primitive(const ak3_wide::Pair& state) {
    const auto [first, second] = state;
    return primitive(word(first)) || primitive(word(second));
}

int search(int cap, size_t limit, const std::string& first, const std::string& second,
           const std::string& prefix, const char* target_file) {
    if (cap < 2 || cap > 62 || !limit || first.empty() || second.empty()
        || first.size() > 31 || second.size() > 31
        || first.size() + second.size() > size_t(cap))
        throw std::runtime_error("invalid start, cap or budget");
    const auto start = ak3_wide::least_image(build_orbit(word_code(first)), build_orbit(word_code(second)));
    std::unordered_set<ak3_wide::Pair, ak3_wide::Hash> targets;
    if (target_file) {
        std::ifstream input(target_file);
        if (!input) throw std::runtime_error("cannot open target catalogue");
        std::string a, b;
        while (input >> a >> b) {
            if (a.empty() || b.empty() || a.size() > 31 || b.size() > 31 || a.size() + b.size() > size_t(cap))
                throw std::runtime_error("invalid target pair");
            targets.insert(ak3_wide::least_image(build_orbit(word_code(a)), build_orbit(word_code(b))));
        }
        if (targets.empty()) throw std::runtime_error("empty target catalogue");
    }
    std::vector<Node> states{{start, root}};
    std::unordered_set<ak3_wide::Pair, ak3_wide::Hash> seen{start};
    Worker worker;
    size_t at = 0, winner = has_primitive(start) || targets.count(start) ? 0 : root;
    for (; at < states.size() && at < limit && winner == root; ++at) {
        std::set<ak3_wide::Pair> fresh;
        const auto [a,b] = states[at].state;
        if (cap - std::min(int(length(a)), int(length(b))) > 31)
            throw std::runtime_error("a successor could exceed the packed word capacity");
        worker.scan_pair(a, b, cap, [&](const Orbit& product, const Orbit& donor) {
            fresh.insert(ak3_wide::least_image(product, donor));
        });
        for (const auto& key : fresh) {
            if (!seen.insert(key).second) continue;
            states.push_back({key, at});
            if (winner == root && (has_primitive(key) || targets.count(key))) winner = states.size() - 1;
        }
        if ((at + 1) % 100000 == 0)
            std::cerr << "Checked " << at + 1 << ", discovered " << states.size() << '\n';
    }
    std::ofstream out(prefix + ".tsv"), route(prefix + ".route.tsv");
    if (!out || !route) throw std::runtime_error("cannot open search outputs");
    const bool primitive_found = winner != root && has_primitive(states[winner].state);
    const bool target_found = winner != root && targets.count(states[winner].state);
    if (winner != root) {
        std::vector<ak3_wide::Pair> path;
        for (size_t next = winner; next != root; next = states[next].parent)
            path.push_back(states[next].state);
        for (auto it = path.rbegin(); it != path.rend(); ++it) {
            const auto [a, b] = *it;
            route << word(a) << '\t' << word(b) << '\n';
        }
    }
    unsigned min_energy = cap, min_word = cap;
    std::map<unsigned, size_t> energies;
    std::sort(states.begin(), states.end(), [](const Node& a, const Node& b) { return a.state < b.state; });
    for (const auto& node : states) {
        const auto [a, b] = node.state;
        ++energies[length(a) + length(b)];
        min_word = std::min(min_word, length(a));
        min_energy = std::min(min_energy, length(a) + length(b));
        out << word(a) << '\t' << word(b) << '\n';
    }
    std::cout << "{\n  \"cyclic_cap\": " << cap << ",\n  \"expanded_orbits\": " << at
              << ",\n  \"discovered_orbits\": " << states.size()
              << ",\n  \"product_candidates\": " << worker.candidates
              << ",\n  \"admitted_product_candidates\": " << worker.admitted
              << ",\n  \"minimum_cyclic_energy\": " << min_energy
              << ",\n  \"minimum_cyclic_coordinate\": " << min_word
              << ",\n  \"primitive_found\": " << (primitive_found ? "true" : "false")
              << ",\n  \"target_found\": " << (target_found ? "true" : "false")
              << ",\n  \"closed\": " << ((winner == root && at == states.size()) ? "true" : "false")
              << ",\n  \"orbit_histogram\": {";
    bool initial = true;
    for (const auto& [energy, n] : energies) {
        std::cout << (initial ? "" : ", ") << '"' << energy << "\": " << n;
        initial = false;
    }
    std::cout << "}\n}\n";
    return 0;
}
}

int main(int argc, char** argv) {
    try {
        if (argc != 6 && argc != 7)
            throw std::runtime_error("usage: waypoint_search cap budget row1 row2 output_prefix [targets.tsv]");
        return search(std::stoi(argv[1]), std::stoull(argv[2]), argv[3], argv[4], argv[5], argc == 7 ? argv[6] : nullptr);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
