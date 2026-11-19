// Screen exact two-copy joins after bounded, geodesic first bridges.
#define main round02_two_copies_main
#include "round02_ac_disproof_two_copies.cpp"
#undef main
#include "u_graph_fold.hpp"

namespace disjoint {

struct Census {
    uint64_t sources = 0, cores = 0, joins = 0, dag_absent = 0, exact_absent = 0;
    uint64_t map_states = 0, positive = 0, incomplete = 0;
    std::unordered_set<std::string> seen;
};

bool test(const Graph& graph, const std::string& p, const std::string& b,
          const std::string& bridge, int first, int second,
          Census& counts, std::ostream& witnesses) {
    if (proves_primitive_absence(graph)) {
        ++counts.dag_absent;
        return true;
    }
    const auto verdict = u_native::decide(graph.out, 0);
    counts.map_states += verdict.pair_states;
    if (verdict.status == u_native::Status::ABSENT) {
        ++counts.exact_absent;
        return true;
    }
    if (verdict.status == u_native::Status::PRIMITIVE) ++counts.positive;
    else ++counts.incomplete;
    witnesses << "{\"source\":[\"" << p << "\",\"" << b << "\",\"" << bridge
              << "\"],\"vertices\":[" << first << ',' << second
              << "],\"status\":\"" << u_native::status_name(verdict.status)
              << "\",\"graph\":";
    graph_json(witnesses, graph);
    if (verdict.status == u_native::Status::PRIMITIVE)
        witnesses << ",\"primitive\":\"" << verdict.witness.cyclic_word
                  << "\",\"based_word\":\"" << verdict.witness.based_word
                  << "\",\"loop_vertex\":" << verdict.witness.vertex;
    witnesses << "}\n";
    return false;
}

void scan(const std::string& bridge, const std::vector<std::string>& left,
          const std::vector<std::string>& right, Census& counts, std::ostream& witnesses) {
    for (const auto& p : left) {
        if (bridge.front() == p.front() || bridge.front() == inverse(p.back())) continue;
        for (const auto& b : right) {
            if (inverse(bridge.back()) == b.front() || bridge.back() == b.back()) continue;
            ++counts.sources;
            const auto core = source(p, b, bridge);
            if (rank(core) != 2) throw std::runtime_error("barbell is not rank two");
            const auto key = unbased_key(core).first;
            if (!counts.seen.insert(key).second) continue;
            ++counts.cores;
            if (!test(core, p, b, bridge, 0, 0, counts, witnesses)) continue;
            const auto n = static_cast<int>(core.out.size());
            for (int i = 0; i < n; ++i) for (int j = i + 1; j < n; ++j) {
                ++counts.joins;
                test(join(core, i, j), p, b, bridge, i, j, counts, witnesses);
            }
        }
    }
}

void enumerate(int remaining, std::string& bridge, const std::vector<std::string>& left,
               const std::vector<std::string>& right, Census& counts, std::ostream& witnesses) {
    if (remaining == 0) {
        scan(bridge, left, right, counts, witnesses);
        return;
    }
    for (char letter : std::string("xXyY")) {
        if (!bridge.empty() && letter == inverse(bridge.back())) continue;
        bridge.push_back(letter);
        enumerate(remaining - 1, bridge, left, right, counts, witnesses);
        bridge.pop_back();
    }
}

bool cyclic(const std::string& word) {
    return !word.empty() && reduce(word) == word && word.front() != inverse(word.back());
}
}  // namespace disjoint

int main(int argc, char** argv) {
    try {
        if (argc != 7)
            throw std::runtime_error("usage: disjoint left right min max witnesses.jsonl counts.json");
        const std::string p = argv[1], b = argv[2];
        const int first = std::stoi(argv[3]), last = std::stoi(argv[4]);
        if (!disjoint::cyclic(p) || !disjoint::cyclic(b) || first < 1 || last < first)
            throw std::runtime_error("bad cyclic input or bridge bounds");
        std::ofstream witnesses(argv[5]), output(argv[6]);
        if (!witnesses || !output) throw std::runtime_error("cannot open outputs");
        const auto left = rotations(p), right = rotations(b);
        output << "{\n  \"left\":\"" << p << "\",\"right\":\"" << b << "\",\n  \"lengths\":{\n";
        for (int length = first; length <= last; ++length) {
            disjoint::Census counts;
            std::string bridge;
            disjoint::enumerate(length, bridge, left, right, counts, witnesses);
            if (length != first) output << ",\n";
            output << "    \"" << length << "\":{\"admissible\":" << counts.sources
                   << ",\"distinct_cores\":" << counts.cores
                   << ",\"joins\":" << counts.joins << ",\"dag_absent\":" << counts.dag_absent
                   << ",\"exact_absent\":" << counts.exact_absent
                   << ",\"map_states\":" << counts.map_states << ",\"positive\":" << counts.positive
                   << ",\"incomplete\":" << counts.incomplete << '}';
            output.flush();
            std::cerr << "length " << length << ": " << counts.sources << " sources, "
                      << counts.joins << " joins, " << counts.positive << " positive\n";
        }
        output << "\n  }\n}\n";
        if (!witnesses || !output) throw std::runtime_error("output failed");
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
    return 0;
}
