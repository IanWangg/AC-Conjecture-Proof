// Exhaust the bounded AK(3) component while retaining the two words separately.
#define AC_ROUND05_ORBITS_LIBRARY
#include "round05_ak3_orbits.cpp"
#include "round06_ak3_wide_pair.hpp"

namespace wide_orbits {
using ak3_wide::Pair;
using ak3_wide::Hash;
using orbit_search::length;
using orbit_search::word;
using orbit_search::word_code;
constexpr uint32_t no_parent = std::numeric_limits<uint32_t>::max();

Pair key(const std::string& a, const std::string& b) {
    return ak3_wide::least_image(orbit_search::build_orbit(word_code(a)),
                                 orbit_search::build_orbit(word_code(b)));
}

unsigned energy(const Pair& state) {
    return length(state.first) + length(state.second);
}

bool catalogue_order(const Pair& a, const Pair& b) {
    return std::make_tuple(energy(a), length(a.first), a) <
           std::make_tuple(energy(b), length(b.first), b);
}

void write_route(const std::string& path, int cap, uint32_t at,
                 const std::vector<Pair>& states, const std::vector<uint32_t>& parents) {
    std::vector<Pair> route;
    for (; at != no_parent; at = parents.at(at)) route.push_back(states.at(at));
    std::reverse(route.begin(), route.end());
    std::ofstream out(path);
    out << "{\n  \"cyclic_cap\":" << cap << ",\n  \"macro_distance\":" << route.size() - 1
        << ",\n  \"orbit_route\":[\n";
    bool first = true;
    for (const auto& [a, b] : route) {
        if (!first) out << ",\n";
        first = false;
        out << "    [\"" << word(a) << "\",\"" << word(b) << "\"]";
    }
    out << "\n  ]\n}\n";
    if (!out) throw std::runtime_error("cannot write route");
    std::cerr << "wrote " << path << " after " << route.size() - 1 << " cyclic products\n";
}

struct Local {
    orbit_search::Worker menu;
    std::unordered_map<Pair, uint32_t, Hash> fresh;
};

int run(int cap, unsigned workers, const std::string& prefix) {
    if (cap < 13 || cap > 32 || !workers)
        throw std::runtime_error("need cap 13–32 and positive worker count");
    round01::check_product();
    const Pair start = key("xxxYYYY", "xyxYXY");
    const Pair target = key("XXXYxyxyXYY", "XYXYYXyXYYXy");
    std::vector<Pair> states{start};
    std::vector<uint32_t> parents{no_parent};
    std::unordered_set<Pair, Hash> seen{start};
    std::vector<Local> locals(workers);
    std::unordered_map<ak3_wide::Code, bool> primitive_cache;
    auto primitive = [&](ak3_wide::Code code) {
        if (primitive_cache.size() > 131072) primitive_cache.clear();
        const auto [entry, added] = primitive_cache.try_emplace(code);
        if (added) entry->second = orbit_search::primitive(word(code));
        return entry->second;
    };
    uint64_t primitive_pairs = 0;
    bool target_found = false;
    unsigned minimum = length(start.first);
    std::map<unsigned, uint64_t> histogram{{energy(start), 1}};
    constexpr std::size_t block = 512, window = 65536;
    std::size_t last_progress = 0;
    for (std::size_t at = 0; at < states.size();) {
        const auto end = std::min(at + window, states.size());
        std::atomic<std::size_t> cursor(at);
        const auto& known = seen;
        std::vector<std::future<void>> jobs;
        for (auto& local : locals) {
            jobs.push_back(std::async(std::launch::async, [&local, &states, &known, &cursor, end, cap] {
                for (;;) {
                    const auto from = cursor.fetch_add(block, std::memory_order_relaxed);
                    if (from >= end) return;
                    for (auto index = from; index < std::min(from + block, end); ++index) {
                        const auto& [a, b] = states[index];
                        local.menu.scan_pair(a, b, cap, [&](const auto& recipient, const auto& donor) {
                            const auto next = ak3_wide::least_image(recipient, donor);
                            if (known.count(next)) return;
                            const auto [entry, added] = local.fresh.try_emplace(next, index);
                            if (!added) entry->second = std::min(entry->second, uint32_t(index));
                        });
                    }
                }
            }));
        }
        for (auto& job : jobs) job.get();
        std::vector<std::pair<Pair, uint32_t>> candidates;
        for (auto& local : locals) {
            candidates.insert(candidates.end(), local.fresh.begin(), local.fresh.end());
            local.fresh.clear();
        }
        std::sort(candidates.begin(), candidates.end());
        for (const auto& [next, parent] : candidates) {
            if (!seen.insert(next).second) continue;
            if (states.size() == no_parent) throw std::runtime_error("state index exhausted");
            const uint32_t index = states.size();
            states.push_back(next);
            parents.push_back(parent);
            ++histogram[energy(next)];
            minimum = std::min(minimum, length(next.first));
            if (next == target) {
                target_found = true;
                write_route(prefix + ".waypoint.route.json", cap, index, states, parents);
            }
            if (primitive(next.first) || primitive(next.second)) {
                if (!primitive_pairs)
                    write_route(prefix + ".primitive.route.json", cap, index, states, parents);
                ++primitive_pairs;
            }
        }
        at = end;
        if (at - last_progress >= window * 4 || at == states.size()) {
            std::cerr << "processed " << at << ", discovered " << states.size() << '\n';
            last_progress = at;
        }
    }

    std::vector<uint32_t>().swap(parents);
    std::unordered_set<Pair, Hash>().swap(seen);
    std::sort(states.begin(), states.end(), catalogue_order);
    std::ofstream catalogue(prefix + ".orbit.tsv");
    for (const auto& [a, b] : states) catalogue << word(a) << '\t' << word(b) << '\n';
    catalogue.close();

    uint64_t candidates = 0, admitted = 0;
    for (const auto& local : locals) {
        candidates += local.menu.candidates;
        admitted += local.menu.admitted;
    }
    std::ofstream out(prefix + ".orbit.json");
    out << "{\n  \"status\":\"PASS\",\n  \"cyclic_cap\":" << cap
        << ",\n  \"signed_permutation_orbits\":" << states.size()
        << ",\n  \"primitive_coordinate_orbits\":" << primitive_pairs
        << ",\n  \"w23_found\":" << (target_found ? "true" : "false")
        << ",\n  \"minimum_coordinate\":" << minimum
        << ",\n  \"rotation_product_candidates\":" << candidates
        << ",\n  \"admitted_neighbors\":" << admitted << ",\n  \"orbit_histogram\":{";
    bool first = true;
    for (const auto& [size, count] : histogram) {
        if (!first) out << ',';
        first = false;
        out << '\"' << size << "\":" << count;
    }
    out << "}\n}\n";
    if (!catalogue || !out) throw std::runtime_error("cannot write component");
    return 0;
}
}  // namespace wide_orbits

#ifndef AC_ROUND07_WIDE_ORBITS_LIBRARY
int main(int argc, char** argv) {
    try {
        if (argc != 4) throw std::runtime_error("usage: wide-orbits cap workers output-prefix");
        return wide_orbits::run(std::stoi(argv[1]), std::stoul(argv[2]), argv[3]);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
#endif
