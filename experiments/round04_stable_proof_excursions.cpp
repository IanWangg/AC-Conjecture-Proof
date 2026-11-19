// Exhaust cyclic rank-three excursions while the isolated z row is absent.
#define main rank_two_reference_main
#include "cyclic_component.cpp"
#undef main

#include <array>
#include <cstdint>
#include <limits>
#include <optional>
#include <set>
#include <stdexcept>
#include <string_view>

namespace {
using Triple = std::array<std::string, 3>;
constexpr size_t seed_parent = std::numeric_limits<size_t>::max();

struct Node {
    Triple rows;
    size_t parent;
    size_t orbit_size;
};

class SignedPermutations {
    std::vector<std::array<char, 3>> images;
    std::unordered_map<std::string, std::vector<std::string>> cache;

public:
    explicit SignedPermutations(bool all) {
        for (int swap = 0; swap <= int(all); ++swap)
            for (int inv_x = 0; inv_x <= int(all); ++inv_x)
                for (int inv_y = 0; inv_y <= int(all); ++inv_y)
                    for (int inv_z = 0; inv_z <= int(all); ++inv_z) {
                        const char x = swap ? 'y' : 'x', y = swap ? 'x' : 'y';
                        images.push_back({inv_x ? invchar(x) : x, inv_y ? invchar(y) : y,
                                          inv_z ? 'Z' : 'z'});
                    }
    }

    const std::vector<std::string>& transformed(const std::string& word) {
        auto [iter, inserted] = cache.try_emplace(word);
        if (inserted) {
            for (const auto& basis : images) {
                auto image = word;
                for (auto& c : image)
                    c = c >= 'a' ? basis[c - 'x'] : invchar(basis[c - 'X']);
                iter->second.push_back(canonical(image));
            }
        }
        return iter->second;
    }

    std::set<Triple> orbit(const Triple& rows) {
        const auto& a = transformed(rows[0]);
        const auto& b = transformed(rows[1]);
        const auto& c = transformed(rows[2]);
        std::set<Triple> orbit;
        for (size_t index = 0; index < images.size(); ++index) {
            Triple point{a[index], b[index], c[index]};
            std::sort(point.begin(), point.end());
            orbit.insert(std::move(point));
        }
        return orbit;
    }
};

bool has_singleton(const Triple& rows) {
    return std::find(rows.begin(), rows.end(), "Z") != rows.end();
}

bool has_pivot(const Triple& rows) {
    return std::any_of(rows.begin(), rows.end(), [](const auto& w) {
        return std::count(w.begin(), w.end(), 'z') + std::count(w.begin(), w.end(), 'Z') == 1;
    });
}

std::string erase_auxiliary(std::string w) {
    w.erase(std::remove_if(w.begin(), w.end(), [](char c) {return c == 'z' || c == 'Z';}), w.end());
    return canonical(std::move(w));
}

size_t energy(const Triple& rows) {
    return rows[0].size() + rows[1].size() + rows[2].size();
}

std::string key(const Triple& rows) {
    return rows[0] + ":" + rows[1] + ":" + rows[2];
}

std::vector<P> bridges_rank_three(int bound) {
    std::vector<P> out{{"", ""}};
    std::vector<std::string> level{""};
    for (int length = 0; length < bound; ++length) {
        std::vector<std::string> next;
        for (const auto& w : level) {
            for (char c : std::string("xXyYzZ")) {
                if (w.empty() || invchar(w.back()) != c) {
                    next.push_back(w + c);
                    out.emplace_back(next.back(), inverse(next.back()));
                }
            }
        }
        level = std::move(next);
    }
    return out;
}

// A zero-bridge product can cancel only at the two seams or in the
// surviving factor after the other factor disappears.
std::optional<std::string> zero_bridge(std::string_view a, std::string_view b, size_t cap) {
    while (!a.empty() && !b.empty() && a.back() == invchar(b.front())) {
        a.remove_suffix(1);
        b.remove_prefix(1);
    }
    while (!a.empty() && !b.empty() && a.front() == invchar(b.back())) {
        a.remove_prefix(1);
        b.remove_suffix(1);
    }
    auto trim = [](std::string_view& w) {
        while (w.size() > 1 && w.front() == invchar(w.back())) {
            w.remove_prefix(1);
            w.remove_suffix(1);
        }
    };
    if (a.empty()) trim(b);
    if (b.empty()) trim(a);
    if (a.size() + b.size() > cap) return std::nullopt;
    return canonical(std::string(a) + std::string(b));
}

void write_tsv(std::ostream& out, const Triple& rows) {
    out << rows[0] << '\t' << rows[1] << '\t' << rows[2] << '\n';
}

int scan(int cap, const std::string& seeds_path, const std::string& output_prefix, size_t limit,
         bool signed_symmetries) {
    std::ifstream seeds(seeds_path);
    if (!seeds) throw std::runtime_error("Opening seed file failed");
    std::ofstream states_out(output_prefix + ".states.tsv"), returns_out(output_prefix + ".returns.tsv");
    std::ofstream route_out(output_prefix + ".route.tsv");
    if (!states_out || !returns_out || !route_out) throw std::runtime_error("Opening output failed");
    std::vector<Node> nodes;
    std::unordered_map<std::string, size_t> seen;
    SignedPermutations symmetries(signed_symmetries);
    auto insert_orbit = [&](const Triple& rows, size_t parent) {
        if (seen.count(key(rows))) return;
        auto orbit = symmetries.orbit(rows);
        for (const auto& member : orbit)
            if (!seen.emplace(key(member), nodes.size()).second)
                throw std::logic_error("Orbit classes overlapped");
        nodes.push_back({rows, parent, orbit.size()});
    };
    Triple rows;
    while (seeds >> rows[0] >> rows[1] >> rows[2]) {
        if (has_singleton(rows) || energy(rows) > static_cast<size_t>(cap)
                || !std::is_sorted(rows.begin(), rows.end()))
            throw std::runtime_error("Malformed seed");
        insert_orbit(rows, seed_parent);
    }
    const size_t initial = nodes.size();
    const size_t initial_expanded = seen.size();
    if (initial > limit) throw std::runtime_error("Seed count exceeds state limit");

    size_t first_no_pivot = seed_parent, no_pivot = 0, min_length = cap + 1;
    uint64_t candidates = 0, admitted = 0, nonempty_bridges = 0;
    std::set<P> returns;
    std::map<size_t, size_t> histogram;
    std::unordered_map<std::string, std::vector<std::string>> variants_cache;
    std::map<int, std::vector<P>> tail_cache;
    bool complete = true;
    for (size_t at = 0; at < nodes.size(); ++at) {
        const auto current = nodes[at].rows;
        write_tsv(states_out, current);
        histogram[energy(current)] += nodes[at].orbit_size;
        for (const auto& w : current) {
            if (!variants_cache.count(w)) variants_cache.emplace(w, variants(w));
            min_length = std::min(min_length, w.size());
        }
        if (!has_pivot(current)) {
            no_pivot += nodes[at].orbit_size;
            if (first_no_pivot == seed_parent) first_no_pivot = at;
        }
        if (!complete) continue;
        for (size_t i = 0; i < 3 && complete; ++i)
            for (size_t j = 0; j < 3 && complete; ++j) {
                if (i == j) continue;
                const int bound = std::max(0, (cap - int(energy(current)) - int(current[j].size())) / 2);
                const size_t allowance = size_t(cap) - energy(current) + current[i].size();
                if (!tail_cache.count(bound)) tail_cache.emplace(bound, bridges_rank_three(bound));
                for (const auto& a : variants_cache.at(current[i])) {
                    if (!complete) break;
                    for (const auto& b : variants_cache.at(current[j])) {
                        if (!complete) break;
                        for (const auto& [tail, tail_inv] : tail_cache.at(bound)) {
                            ++candidates;
                            std::optional<std::string> candidate;
                            if (tail.empty()) {
                                candidate = zero_bridge(a, b, allowance);
                            } else {
                                ++nonempty_bridges;
                                const auto word = cyclic(a + tail + b + tail_inv);
                                if (word.size() <= allowance) candidate = canonical(word);
                            }
                            if (!candidate) continue;
                            if (candidate->empty()) throw std::logic_error("A row vanished");
                            ++admitted;
                            auto next = current;
                            next[i] = std::move(*candidate);
                            std::sort(next.begin(), next.end());
                            if (has_singleton(next)) {
                                P projected;
                                bool first = true;
                                for (auto w : next) if (w != "Z") {
                                    if (first) projected.first = erase_auxiliary(w);
                                    else projected.second = erase_auxiliary(w);
                                    first = false;
                                }
                                returns.insert(canonpair(projected.first, projected.second));
                                continue;
                            }
                            if (seen.count(key(next))) continue;
                            if (nodes.size() == limit) {
                                complete = false;
                                break;
                            }
                            insert_orbit(next, at);
                        }
                    }
                }
            }
    }
    std::set<P> expanded_returns;
    for (const auto& [first, second] : returns)
        for (const auto& member : symmetries.orbit({first, second, "Z"})) {
            P projected;
            bool first_slot = true;
            for (const auto& w : member) if (w != "Z") {
                (first_slot ? projected.first : projected.second) = w;
                first_slot = false;
            }
            expanded_returns.insert(std::move(projected));
        }
    for (const auto& [first, second] : expanded_returns)
        returns_out << first << '\t' << second << '\n';
    if (first_no_pivot != seed_parent) {
        std::vector<size_t> path;
        for (size_t at = first_no_pivot; at != seed_parent; at = nodes[at].parent)
            path.push_back(at);
        for (auto it = path.rbegin(); it != path.rend(); ++it) write_tsv(route_out, nodes[*it].rows);
    }
    std::cout << "{\n  \"cap\": " << cap
              << ",\n  \"complete\": " << (complete ? "true" : "false")
              << ",\n  \"signed_symmetries\": " << (signed_symmetries ? "true" : "false")
              << ",\n  \"seed_orbits\": " << initial
              << ",\n  \"seeds\": " << initial_expanded
              << ",\n  \"state_orbits\": " << nodes.size()
              << ",\n  \"states\": " << seen.size()
              << ",\n  \"minimum_row_length\": " << min_length
              << ",\n  \"pivotless\": " << no_pivot
              << ",\n  \"candidates\": " << candidates
              << ",\n  \"nonempty_bridge_candidates\": " << nonempty_bridges
              << ",\n  \"admitted\": " << admitted
              << ",\n  \"reentry_projections\": " << expanded_returns.size()
              << ",\n  \"histogram\": {";
    bool first = true;
    for (const auto& [n, count] : histogram) {
        if (!first) std::cout << ", ";
        first = false;
        std::cout << "\"" << n << "\": " << count;
    }
    std::cout << "}\n}\n";
    return complete ? 0 : 2;
}
}

#ifndef AC_ROUND04_EXCURSION_LIBRARY
int main(int argc, char** argv) {
    if (argc != 5 && !(argc == 6 && std::string(argv[5]) == "--signed-symmetries")) {
        std::cerr << "usage: excursions cyclic_cap seeds.tsv output_prefix limit [--signed-symmetries]\n";
        return 1;
    }
    try {
        return scan(std::stoi(argv[1]), argv[2], argv[3], std::stoull(argv[4]), argc == 6);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
#endif
