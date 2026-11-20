// Scan all cyclic products at cap 24 from the observed cap-23 pivot departures.
#define AC_ROUND06_SINGLETON_LIBRARY
#include "round06_stable_proof_all_singleton.cpp"

namespace {

struct Neighbor {
    Triple rows;
    size_t source;
};

int sample(const std::string& input_file, const std::string& output_file, bool follow) {
    std::ifstream input(input_file);
    std::ofstream output(output_file);
    if (!input || !output) throw std::runtime_error("cannot open sample or output");
    Triple rows;
    std::vector<Triple> sources;
    size_t prefix_size = 0;
    CompactOrbits keys;
    std::unordered_set<Key, KeyHash> source_keys;
    while (input >> rows[0] >> rows[1] >> rows[2]) {
        if (follow) {
            Triple parent;
            if (!(input >> parent[0] >> parent[1] >> parent[2]))
                throw std::runtime_error("missing preceding source");
        }
        ++prefix_size;
        if (!follow && has_pivot(rows)) continue;
        if (energy(rows) > size_t(follow ? 24 : 23)) throw std::runtime_error("source exceeds its cap");
        keys.limit();
        const auto key = compact_orbit(keys.word(encode(rows[0])), keys.word(encode(rows[1])), keys.word(encode(rows[2])));
        if (source_keys.insert(key).second) sources.push_back(rows);
    }
    if (sources.empty()) throw std::runtime_error("no source without fixed pivot");
    std::unordered_map<Key, Neighbor, KeyHash> neighbors;
    std::unordered_map<std::string, std::vector<std::string>> rotations;
    std::map<int, std::vector<P>> tails;
    uint64_t checked = 0, admitted = 0, bridged = 0;
    constexpr int cap = 24;
    for (size_t at = 0; at < sources.size(); ++at) {
        const auto& before = sources[at];
        const int total = int(energy(before));
        keys.limit();
        if (rotations.size() > 8192) rotations.clear();
        for (const auto& w : before)
            if (!rotations.count(w)) rotations.emplace(w, variants(w));
        for (size_t i = 0; i < 3; ++i) {
            std::set<std::string> changed;
            for (size_t j = 0; j < 3; ++j) {
                if (i == j) continue;
                const int allowance = cap - total + int(before[i].size());
                const int bound = std::max(0, (cap - total - int(before[j].size())) / 2);
                if (!tails.count(bound)) tails.emplace(bound, bridges_rank_three(bound));
                for (const auto& a : rotations.at(before[i]))
                    for (const auto& b : rotations.at(before[j]))
                        for (const auto& [bridge, back] : tails.at(bound)) {
                            ++checked;
                            bridged += !bridge.empty();
                            std::optional<std::string> result;
                            if (bridge.empty()) result = zero_bridge(a, b, allowance);
                            else {
                                auto value = cyclic(a + bridge + b + back);
                                if (value.size() <= size_t(allowance)) result = canonical(std::move(value));
                            }
                            if (result) {
                                if (result->empty()) throw std::logic_error("a relator vanished");
                                ++admitted;
                                changed.insert(std::move(*result));
                            }
                        }
            }
            const auto& a = keys.word(encode(before[(i + 1) % 3]));
            const auto& b = keys.word(encode(before[(i + 2) % 3]));
            for (const auto& word : changed) {
                const auto key = compact_orbit(keys.word(encode(word)), a, b);
                auto after = before;
                after[i] = word;
                std::sort(after.begin(), after.end());
                neighbors.try_emplace(key, Neighbor{after, at});
            }
        }
    }
    std::vector<Key> names;
    for (const auto& [key, point] : neighbors) names.push_back(key);
    std::sort(names.begin(), names.end());
    size_t singleton = 0;
    std::map<size_t, size_t> energies;
    for (const auto key : names) {
        const auto& result = neighbors.at(key);
        singleton += std::any_of(result.rows.begin(), result.rows.end(), [](const auto& word) {return word.size() == 1;});
        ++energies[energy(result.rows)];
        for (const auto& word : result.rows) output << word << '\t';
        write_tsv(output, sources.at(result.source));
    }
    std::cout << "{\n  \"input_states\": " << prefix_size << ",\n  \"signed_source_orbits\": " << sources.size()
              << ",\n  \"product_candidates\": " << checked
              << ",\n  \"positive_bridge_candidates\": " << bridged
              << ",\n  \"admitted_candidates\": " << admitted
              << ",\n  \"neighbor_orbits\": " << neighbors.size()
              << ",\n  \"neighbors_with_literal_singleton\": " << singleton
              << ",\n  \"histogram\": {";
    bool first = true;
    for (const auto& [size, count] : energies) {
        std::cout << (first ? "" : ",") << '"' << size << "\":" << count;
        first = false;
    }
    std::cout << "}\n}\n";
    return 0;
}

}

int main(int argc, char** argv) {
    try {
        if (argc != 3 && !(argc == 4 && std::string(argv[3]) == "--follow"))
            throw std::runtime_error("usage: one_step source.tsv neighbors-and-parent.tsv [--follow]");
        return sample(argv[1], argv[2], argc == 4);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
