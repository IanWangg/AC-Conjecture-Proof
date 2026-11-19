// Enumerate actual simultaneous intrinsic bases in two conjugation phases.
#define main round02_two_copies_main
#include "round02_ac_disproof_two_copies.cpp"
#undef main
#include "u_native_primitive.hpp"

#include <numeric>
#include <set>
#include <string_view>

namespace actual_phases {
using Pair = std::pair<std::string, std::string>;
using Slope = std::array<int, 2>;
using SlopePair = std::pair<Slope, Slope>;

std::string cyclic_reduce(const std::string& word) {
    const auto reduced = reduce(word);
    size_t start = 0, end = reduced.size();
    while (end > start + 1 && reduced[start] == inverse(reduced[end - 1])) {
        ++start;
        --end;
    }
    return reduced.substr(start, end - start);
}

std::string euclidean_primitive(int a, int b) {
    if (a == 0) return "y";
    if (b == 0) return "x";
    if (a == b) return "xy";
    const bool more_x = a > b;
    const auto shorter = more_x ? euclidean_primitive(a - b, b)
                                : euclidean_primitive(a, b - a);
    std::string result;
    for (const char c : shorter) {
        if (c == (more_x ? 'y' : 'x')) result += "xy";
        else result += c;
    }
    return result;
}

int norm(const Slope& slope) { return std::abs(slope[0]) + std::abs(slope[1]); }

std::vector<SlopePair> slope_pairs(int bound) {
    std::vector<Slope> slopes;
    for (int a = 0; a < bound; ++a) for (int b = 1 - bound; b < bound; ++b)
        if ((a || b > 0) && std::gcd(a, b) == 1 && a + std::abs(b) < bound)
            slopes.push_back({a, b});
    std::vector<SlopePair> out;
    for (size_t i = 0; i < slopes.size(); ++i) for (size_t j = i + 1; j < slopes.size(); ++j) {
        const auto& a = slopes[i];
        const auto& b = slopes[j];
        if (norm(a) + norm(b) <= bound && std::abs(a[0] * b[1] - a[1] * b[0]) == 1)
            out.emplace_back(a, b);
    }
    return out;
}

std::string realize(const Pair& marking, const Slope& slope) {
    const auto pattern = euclidean_primitive(std::abs(slope[0]), std::abs(slope[1]));
    const auto first = slope[0] < 0 ? inv(marking.first) : marking.first;
    const auto second = slope[1] < 0 ? inv(marking.second) : marking.second;
    std::string word;
    for (char c : pattern) word += c == 'x' ? first : second;
    return cyclic_reduce(word);
}

void bridges(int remaining, std::string& bridge, std::vector<std::string>& labels) {
    if (remaining == 0) return;
    for (char c : std::string_view("xXyY")) {
        if (!bridge.empty() && c == inverse(bridge.back())) continue;
        bridge += c;
        labels.push_back(bridge);
        bridges(remaining - 1, bridge, labels);
        bridge.pop_back();
    }
}

std::vector<std::string> bridge_labels(int cap) {
    std::vector<std::string> result;
    std::string prefix;
    bridges(cap, prefix, result);
    return result;
}

Pair sorted_pair(Pair pair) {
    pair.first = std::min(pair.first, inv(pair.first));
    pair.second = std::min(pair.second, inv(pair.second));
    if (pair.second < pair.first) std::swap(pair.first, pair.second);
    return pair;
}

template<class Visit>
void placements(const Pair& marking, const std::vector<SlopePair>& menu,
                const std::vector<std::string>& connectors, Visit visit) {
    std::map<Slope, std::vector<std::string>> cache;
    auto get = [&](const Slope& slope) -> const std::vector<std::string>& {
        const auto [where, fresh] = cache.try_emplace(slope);
        if (fresh) where->second = rotations(realize(marking, slope));
        return where->second;
    };
    for (const auto& [a, b] : menu) {
        for (const auto& p : get(a)) for (const auto& q : get(b)) {
            visit(sorted_pair({p, q}));
            for (const auto& bridge : connectors) {
                if (bridge.front() == p.front() || bridge.front() == inverse(p.back())
                    || inverse(bridge.back()) == q.front() || bridge.back() == q.back()) continue;
                visit(sorted_pair({p, bridge + q + inv(bridge)}));
            }
        }
    }
}

struct Counts { uint64_t dag = 0, exact = 0, positive = 0, incomplete = 0; };

std::vector<std::pair<int, int>> join_representatives(const Graph& core, bool compress) {
    const int n = int(core.out.size());
    std::vector<bool> seen(n * n);
    std::vector<std::pair<int, int>> representatives{{0, 0}}, component;
    for (int a = 0; a < n; ++a) for (int b = a + 1; b < n; ++b) {
        if (seen[a * n + b]) continue;
        representatives.emplace_back(a, b);
        if (!compress) continue;
        component.assign(1, {a, b});
        seen[a * n + b] = true;
        for (size_t i = 0; i < component.size(); ++i) {
            const auto [v, w] = component[i];
            for (int c = 0; c < 4; ++c) {
                auto x = core.out[v][c], y = core.out[w][c];
                if (x < 0 || y < 0) continue;
                if (x == y) throw std::runtime_error("nonimmersed core in two-copy screen");
                if (x > y) std::swap(x, y);
                if (seen[x * n + y]) continue;
                seen[x * n + y] = true;
                component.emplace_back(x, y);
            }
        }
    }
    return representatives;
}

void screen(const Graph& core, const Pair& entry, const Pair& words, Counts& counts, std::ostream& cases,
            bool compress) {
    for (const auto& [a, b] : join_representatives(core, compress)) {
        const auto graph = a == b ? core : join(core, a, b);
        if (proves_primitive_absence(graph)) {
            ++counts.dag;
            continue;
        }
        const auto result = u_native::decide(graph.out, 1'000'000);
        if (result.status == u_native::Status::ABSENT) {
            ++counts.exact;
            continue;
        }
        if (result.status == u_native::Status::PRIMITIVE) ++counts.positive;
        else ++counts.incomplete;
        cases << "{\"first\":[\"" << entry.first << "\",\"" << entry.second
              << "\"],\"second\":[\"" << words.first << "\",\"" << words.second
              << "\"],\"vertices\":[" << a << ',' << b << "],\"status\":\""
              << u_native::status_name(result.status) << '"';
        if (result.status == u_native::Status::PRIMITIVE)
            cases << ",\"primitive\":\"" << result.witness.cyclic_word << "\"";
        cases << ",\"graph\":";
        graph_json(cases, graph);
        cases << "}\n";
        cases.flush();
    }
}

void run(int first_bound, int second_bound, int first_gap, int second_gap, const char* output, bool compress) {
    if (first_bound < 2 || second_bound < 2 || first_gap < 0 || second_gap < 0)
        throw std::runtime_error("basis bounds must be at least two and gaps nonnegative");
    const auto first_menu = slope_pairs(first_bound), second_menu = slope_pairs(second_bound);
    const auto first_bridges = bridge_labels(first_gap), second_bridges = bridge_labels(second_gap);
    std::ofstream exceptions(output);
    if (!exceptions) throw std::runtime_error("cannot write exceptions");
    std::set<Pair> first;
    placements({"xxxYYYY", "xyxYXY"}, first_menu, first_bridges,
               [&](const Pair& pair) { first.insert(pair); });
    uint64_t second_placements = 0, pairs_covered = 0;
    Counts counts;
    std::unordered_set<std::string> cores, based_pairs;
    for (const auto& marking : first) {
        placements(marking, second_menu, second_bridges, [&](const Pair& pair) {
            ++second_placements;
            if (!based_pairs.insert(pair.first + ' ' + pair.second).second) return;
            const auto [key, core] = unbased_key(fold(pair.first, pair.second));
            if (cores.insert(key).second) {
                const auto n = core.out.size();
                pairs_covered += 1 + n * (n - 1) / 2;
                screen(core, marking, pair, counts, exceptions, compress);
            }
        });
    }
    std::cout << "{\"first_basis_bound\":" << first_bound << ",\"second_basis_bound\":" << second_bound
              << ",\"first_geodesic_gap\":" << first_gap << ",\"second_geodesic_gap\":" << second_gap
              << ",\"first_slope_pairs\":" << first_menu.size() << ",\"second_slope_pairs\":" << second_menu.size()
              << ",\"first_marked_pairs\":" << first.size() << ",\"second_placements\":" << second_placements
              << ",\"distinct_second_marked_pairs\":" << based_pairs.size()
              << ",\"distinct_second_cores\":" << cores.size() << ",\"vertex_pairs_covered\":" << pairs_covered
              << ",\"DAG_excluded\":" << counts.dag
              << ",\"exact_excluded\":" << counts.exact << ",\"primitive_positives\":" << counts.positive
              << ",\"incomplete\":" << counts.incomplete << "}\n";
}
}

int main(int argc, char** argv) {
    try {
        if (argc != 6 && (argc != 7 || std::string_view(argv[6]) != "--all-final-vertices"))
            throw std::runtime_error("usage: scan first_bound second_bound first_gap second_gap exceptions.jsonl [--all-final-vertices]");
        actual_phases::run(std::stoi(argv[1]), std::stoi(argv[2]), std::stoi(argv[3]), std::stoi(argv[4]),
                           argv[5], argc == 6);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
