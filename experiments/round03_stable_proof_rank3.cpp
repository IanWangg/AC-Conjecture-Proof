// Complete cyclic peak-bounded search with one fixed isolated pair at the start.
#define main rank_two_binary_main
#include "cyclic_component.cpp"
#undef main

#include <array>
#include <stdexcept>
#include <unordered_set>

namespace rank_three {
using Triple = std::array<std::string, 3>;

std::string key(const Triple& row) {
    return row[0] + ":" + row[1] + ":" + row[2];
}

std::vector<std::pair<std::string, std::string>> bridge_menu(int bound) {
    std::vector<std::pair<std::string, std::string>> words{{"", ""}};
    std::vector<std::string> layer{""};
    for (int length = 0; length < bound; ++length) {
        std::vector<std::string> next;
        for (const auto& prefix : layer) {
            for (char letter : std::string("xXyYzZ")) {
                if (!prefix.empty() && invchar(prefix.back()) == letter) continue;
                next.push_back(prefix + letter);
                words.emplace_back(next.back(), inverse(next.back()));
            }
        }
        layer = std::move(next);
    }
    return words;
}

int search(int parameter, int cap, size_t limit, const char* output) {
    if (parameter < 2 || cap < 2 * parameter + 8 || limit == 0)
        throw std::invalid_argument("parameter, cap, or state limit out of range");
    Triple start{canonical(std::string(parameter, 'x') + std::string(parameter + 1, 'Y')),
                 canonical("xyxYXY"), canonical("z")};
    std::sort(start.begin(), start.end());
    std::vector<Triple> states{start};
    std::unordered_set<std::string> visited{key(start)};
    std::unordered_map<std::string, std::vector<std::string>> orientation_cache;
    std::map<int, std::vector<std::pair<std::string, std::string>>> bridges_cache;
    uint64_t candidates = 0, admitted = 0, positive_bridges = 0;
    bool complete = true;
    size_t offset = 0;
    for (; offset < states.size() && complete; ++offset) {
        const Triple rows = states[offset];
        std::array<int, 3> length{};
        int energy = 0;
        for (size_t i = 0; i < 3; ++i) {
            length[i] = static_cast<int>(rows[i].size());
            energy += length[i];
            if (!orientation_cache.count(rows[i]))
                orientation_cache.emplace(rows[i], variants(rows[i]));
        }
        for (size_t i = 0; i < 3 && complete; ++i) {
            for (size_t j = 0; j < 3 && complete; ++j) {
                if (i == j) continue;
                const int bridge_bound = std::max(0, (cap - energy - length[j]) / 2);
                if (!bridges_cache.count(bridge_bound))
                    bridges_cache.emplace(bridge_bound, bridge_menu(bridge_bound));
                const size_t product_cap = cap - energy + length[i];
                for (const auto& a : orientation_cache.at(rows[i])) {
                    if (!complete) break;
                    for (const auto& b : orientation_cache.at(rows[j])) {
                        if (!complete) break;
                        for (const auto& [tail, inverse_tail] : bridges_cache.at(bridge_bound)) {
                            ++candidates;
                            if (!tail.empty()) ++positive_bridges;
                            auto product = cyclic(a + tail + b + inverse_tail);
                            if (product.size() > product_cap) continue;
                            if (product.empty()) throw std::logic_error("unimodular tuple lost a row");
                            ++admitted;
                            Triple neighbor = rows;
                            neighbor[i] = canonical(product);
                            std::sort(neighbor.begin(), neighbor.end());
                            if (!visited.insert(key(neighbor)).second) continue;
                            if (states.size() == limit) {
                                complete = false;
                                break;
                            }
                            states.push_back(std::move(neighbor));
                        }
                    }
                }
            }
        }
    }
    std::sort(states.begin(), states.end());
    std::ofstream file(output);
    if (!file) throw std::runtime_error("cannot open catalogue");
    for (const auto& row : states) file << row[0] << '\t' << row[1] << '\t' << row[2] << '\n';
    if (!file) throw std::runtime_error("cannot write catalogue");
    std::cout << "{\n"
              << "  \"parameter\": " << parameter << ",\n"
              << "  \"cyclic_cap\": " << cap << ",\n"
              << "  \"complete\": " << (complete ? "true" : "false") << ",\n"
              << "  \"discovered_vertices\": " << states.size() << ",\n"
              << "  \"expanded_vertices\": " << (complete ? offset : offset - 1) << ",\n"
              << "  \"candidate_products\": " << candidates << ",\n"
              << "  \"admitted_products\": " << admitted << ",\n"
              << "  \"nonempty_bridge_candidates\": " << positive_bridges << "\n}\n";
    return complete ? 0 : 2;
}
}

int main(int argc, char** argv) {
    if (argc != 5) {
        std::cerr << "usage: rank3 AK_parameter cyclic_cap state_limit output.tsv\n";
        return 1;
    }
    try {
        return rank_three::search(std::stoi(argv[1]), std::stoi(argv[2]), std::stoull(argv[3]), argv[4]);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
