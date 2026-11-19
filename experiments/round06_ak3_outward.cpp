// Exhaust finite, short outward routes from the new low-energy cap-29 orbits.
#define AC_ROUND05_ORBITS_LIBRARY
#include "round05_ak3_orbits.cpp"
#include "round06_ak3_wide_pair.hpp"

#include <filesystem>

namespace outward {
using orbit_search::Code;
using orbit_search::length;
using orbit_search::pack;
using orbit_search::word;
using orbit_search::word_code;
using ak3_wide::Pair;
using ak3_wide::Hash;

int energy(const Pair& p) { return length(p.first) + length(p.second); }

Pair read_pair(const std::string& line) {
    const auto tab = line.find('\t');
    if (tab == std::string::npos || !tab || tab + 1 == line.size() || line.size() > 33)
        throw std::runtime_error("invalid orbit TSV row");
    const auto a = word_code(line.substr(0, tab)), b = word_code(line.substr(tab + 1));
    if (a > b) throw std::runtime_error("coordinates out of compact order");
    return {a, b};
}

std::unordered_set<Code> load_known(const char* path) {
    std::ifstream input(path);
    if (!input) throw std::runtime_error("cannot open cap-29 catalogue");
    std::unordered_set<Code> known;
    known.reserve(std::filesystem::file_size(path) / 30);
    std::string line;
    while (std::getline(input, line)) {
        const auto pair = read_pair(line);
        if (energy(pair) > 29 || !known.insert(pack(pair.first, pair.second)).second)
            throw std::runtime_error("non-cap-29 or duplicate input row");
    }
    if (input.bad() || known.empty()) throw std::runtime_error("bad cap-29 input");
    return known;
}

struct Node {
    Pair pair;
    uint32_t parent;
};

struct Local {
    orbit_search::Worker menu;
    std::unordered_map<Pair, uint32_t, Hash> following;
    uint64_t to_known = 0;
};

void pair_json(std::ostream& out, const Pair& p) {
    out << "[\"" << word(p.first) << "\",\"" << word(p.second) << "\"]";
}

void histogram_json(std::ostream& out, const std::map<int, uint64_t>& entries) {
    bool first = true;
    out << '{';
    for (const auto& [key, count] : entries) {
        if (!first) out << ',';
        first = false;
        out << '"' << key << "\":" << count;
    }
    out << '}';
}

int run(int cap, unsigned depth, unsigned workers, const char* seeds_path, const char* known_path,
        const char* tsv_path, const char* result_path) {
    if (cap <= 29 || cap > 32 || !depth || !workers)
        throw std::runtime_error("need cap 30–32, positive depth and worker count");
    round01::check_product();
    const auto known = load_known(known_path);
    auto in_known = [&](const Pair& p) { return energy(p) <= 29 && known.count(pack(p.first, p.second)); };
    std::ifstream seed_tsv(seeds_path);
    std::ofstream tsv(tsv_path), out(result_path);
    if (!seed_tsv || !tsv || !out) throw std::runtime_error("cannot open search input/output");
    std::vector<Node> nodes;
    std::unordered_set<Pair, Hash> seen;
    std::map<int, uint64_t> seed_energy;
    std::string line;
    constexpr uint32_t no_parent = std::numeric_limits<uint32_t>::max();
    while (std::getline(seed_tsv, line)) {
        auto pair = read_pair(line);
        if (!in_known(pair) || !seen.insert(pair).second)
            throw std::runtime_error("seed is repeated or absent from cap 29");
        ++seed_energy[energy(pair)];
        nodes.push_back({pair, no_parent});
    }
    if (seed_tsv.bad() || nodes.empty()) throw std::runtime_error("no valid seeds");
    const uint32_t seed_count = nodes.size();
    uint32_t begin = 0, end = seed_count, smallest = no_parent, primitive_node = no_parent;
    std::vector<Local> locals(workers);
    out << "{\n  \"cap\":" << cap << ",\"requested_depth\":" << depth
        << ",\"known_cap29_orbits\":" << known.size() << ",\"seed_orbits\":" << seed_count
        << ",\"seed_energy\":";
    histogram_json(out, seed_energy);
    out << ",\n  \"layers\":[\n";
    for (unsigned step = 0; step < depth && begin != end && primitive_node == no_parent; ++step) {
        std::atomic<uint32_t> cursor(begin);
        std::vector<std::future<void>> pending;
        for (auto& local : locals) {
            local.following.clear();
            local.to_known = local.menu.candidates = local.menu.admitted = 0;
            pending.push_back(std::async(std::launch::async, [&local, &cursor, &nodes, &seen, &in_known, end, cap] {
                for (;;) {
                    const auto batch = cursor.fetch_add(64);
                    if (batch >= end) return;
                    for (auto id = batch; id < std::min(end, batch + 64); ++id) {
                        const auto& p = nodes[id].pair;
                        local.menu.scan_pair(p.first, p.second, cap, [&](const auto& product, const auto& donor) {
                            const auto candidate = ak3_wide::least_image(product, donor);
                            if (in_known(candidate)) {
                                ++local.to_known;
                            } else if (!seen.count(candidate)) {
                                const auto [record, added] = local.following.try_emplace(candidate, id);
                                if (!added) record->second = std::min(record->second, id);
                            }
                        });
                    }
                }
            }));
        }
        for (auto& job : pending) job.get();
        uint64_t candidates = 0, admitted = 0, back_to_known = 0;
        std::unordered_map<Pair, uint32_t, Hash> all;
        for (const auto& local : locals) {
            candidates += local.menu.candidates;
            admitted += local.menu.admitted;
            back_to_known += local.to_known;
            for (const auto& [pair, id] : local.following) {
                const auto [record, added] = all.try_emplace(pair, id);
                if (!added) record->second = std::min(record->second, id);
            }
        }
        std::vector<std::pair<Pair, uint32_t>> ordered(all.begin(), all.end());
        std::sort(ordered.begin(), ordered.end());
        std::map<int, uint64_t> energies;
        for (const auto& [pair, parent] : ordered) {
            const uint32_t at = nodes.size();
            const auto a = word(pair.first), b = word(pair.second);
            const auto total = energy(pair);
            ++energies[total];
            seen.insert(pair);
            nodes.push_back({pair, parent});
            tsv << a << '\t' << b << '\n';
            if (smallest == no_parent || total < energy(nodes[smallest].pair)) smallest = at;
            if (primitive_node == no_parent && (orbit_search::primitive(a) || orbit_search::primitive(b)))
                primitive_node = at;
        }
        if (step) out << ",\n";
        out << "    {\"step\":" << step + 1 << ",\"input_orbits\":" << end - begin
            << ",\"candidate_products\":" << candidates << ",\"admitted_products\":" << admitted
            << ",\"back_to_cap29\":" << back_to_known << ",\"novel_orbits\":" << ordered.size()
            << ",\"energy\":";
        histogram_json(out, energies);
        out << '}';
        begin = end;
        end = nodes.size();
    }
    auto show_route = [&](uint32_t at) {
        std::vector<Pair> route;
        for (; at != no_parent; at = nodes.at(at).parent) route.push_back(nodes[at].pair);
        out << '[';
        for (auto it = route.rbegin(); it != route.rend(); ++it) {
            if (it != route.rbegin()) out << ',';
            pair_json(out, *it);
        }
        out << ']';
    };
    out << "\n  ],\n  \"minimum_energy_route\":";
    show_route(smallest);
    out << ",\n  \"primitive_route\":";
    show_route(primitive_node);
    out << "\n}\n";
    if (!tsv || !out) throw std::runtime_error("search output failure");
    return 0;
}
}  // namespace outward

int main(int argc, char** argv) {
    try {
        if (argc != 8) throw std::runtime_error("usage: outward cap depth workers seeds.tsv cap29.tsv new.tsv result.json");
        return outward::run(std::stoi(argv[1]), std::stoul(argv[2]), std::stoul(argv[3]),
                            argv[4], argv[5], argv[6], argv[7]);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
