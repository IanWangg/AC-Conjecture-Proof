// Find a literal cap-22 cyclic path back to a certified singleton exit.
#define AC_ROUND04_EXCURSION_LIBRARY
#include "round04_stable_proof_excursions.cpp"

#include <unordered_set>

namespace {

void find_route(int cap, const char* seed_file, const char* route_file,
                size_t limit, const Triple& target) {
    std::ifstream input(seed_file);
    if (!input) throw std::runtime_error("missing first exits");
    std::unordered_set<std::string> seeds;
    Triple rows;
    while (input >> rows[0] >> rows[1] >> rows[2]) seeds.insert(key(rows));

    SignedPermutations symmetries(true);
    std::unordered_set<std::string> visited{key(*symmetries.orbit(target).begin())};
    std::vector<Node> nodes{{target, seed_parent, 0}};
    std::unordered_map<std::string, std::vector<std::string>> variations;
    std::map<int, std::vector<P>> bridge_options;
    size_t chosen = seed_parent;

    for (size_t at = 0; at < nodes.size() && chosen == seed_parent; ++at) {
        const auto current = nodes[at].rows;
        if (seeds.count(key(current))) {
            chosen = at;
            break;
        }
        const int total = int(energy(current));
        for (const auto& w : current)
            if (!variations.count(w)) variations.emplace(w, variants(w));

        for (size_t i = 0; i < 3 && chosen == seed_parent; ++i) {
            for (size_t j = 0; j < 3 && chosen == seed_parent; ++j) {
                if (i == j) continue;
                const int bound = std::max(0, (cap - total - int(current[j].size())) / 2);
                const size_t allowance = cap - total + current[i].size();
                if (!bridge_options.count(bound))
                    bridge_options.emplace(bound, bridges_rank_three(bound));
                for (const auto& a : variations.at(current[i])) {
                    if (chosen != seed_parent) break;
                    for (const auto& b : variations.at(current[j])) {
                        if (chosen != seed_parent) break;
                        for (const auto& [tail, tail_inv] : bridge_options.at(bound)) {
                            auto updated = tail.empty()
                                ? zero_bridge(a, b, allowance)
                                : std::optional<std::string>(canonical(a + tail + b + tail_inv));
                            if (!updated || updated->empty() || updated->size() > allowance) continue;
                            Triple state = current;
                            state[i] = std::move(*updated);
                            std::sort(state.begin(), state.end());
                            if (has_singleton(state)) continue;
                            if (!visited.insert(key(*symmetries.orbit(state).begin())).second) continue;
                            if (nodes.size() >= limit) throw std::runtime_error("orbit limit reached");
                            nodes.push_back({state, at, 0});
                            if (seeds.count(key(state))) {
                                chosen = nodes.size() - 1;
                                break;
                            }
                        }
                    }
                }
            }
        }
    }
    if (chosen == seed_parent) throw std::runtime_error("target component misses all seeds");
    std::ofstream route(route_file);
    if (!route) throw std::runtime_error("could not open route output");
    size_t steps = 0;
    for (size_t at = chosen; at != seed_parent; at = nodes[at].parent) {
        write_tsv(route, nodes[at].rows);
        ++steps;
    }
    std::cout << "Discovered orbits " << nodes.size() << ", route states " << steps << '\n';
}

}

int main(int argc, char** argv) {
    if (argc != 8) {
        std::cerr << "usage: chart_route cap seeds.tsv route.tsv limit row0 row1 row2\n";
        return 1;
    }
    try {
        const Triple target{canonical(argv[5]), canonical(argv[6]), canonical(argv[7])};
        const int cap = std::stoi(argv[1]);
        if (cap < 1 || target[0].empty() || energy(target) > size_t(cap)
            || !std::is_sorted(target.begin(), target.end()) || has_singleton(target))
            throw std::runtime_error("invalid target");
        find_route(cap, argv[2], argv[3], std::stoull(argv[4]), target);
        return 0;
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
