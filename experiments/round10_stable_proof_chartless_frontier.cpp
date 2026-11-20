// Exact rank-three products from the cap-22 chartless sector to energy 23.
#define AC_ROUND06_SINGLETON_LIBRARY
#include "round06_stable_proof_all_singleton.cpp"

namespace {

constexpr int source_cap = 22;
constexpr int target_cap = 23;

unsigned packed_energy(Key key) {
    const Code high = Code(key >> 64);
    const auto top = high ? 127 - __builtin_clzll(high) : 63 - __builtin_clzll(Code(key));
    return unsigned(top - 10) / 3;
}

struct Layer {
    Worker worker;
    std::unordered_map<Key, size_t, KeyHash> targets;
};

int frontier(const char* input_name, const std::string& name, unsigned threads) {
    std::ifstream in(input_name);
    if (!in || !threads) throw std::runtime_error("missing sources or worker count");
    CompactOrbits cache;
    std::vector<Key> sources;
    std::unordered_set<Key, KeyHash> unique;
    Triple words;
    while (in >> words[0] >> words[1] >> words[2]) {
        if (energy(words) > source_cap) throw std::logic_error("source above cap 22");
        const auto key = pack(encode(words[0]), encode(words[1]), encode(words[2]));
        if (rows_from(key) != words || !unique.insert(key).second)
            throw std::logic_error("source rows must be unique and ordered");
        cache.limit();
        if (key != compact_orbit(cache.word(encode(words[0])), cache.word(encode(words[1])),
                                 cache.word(encode(words[2]))))
            throw std::logic_error("source is not the compact signed representative");
        sources.push_back(key);
    }
    if (sources.empty()) throw std::logic_error("empty source catalogue");
    std::atomic<size_t> cursor{0};
    constexpr size_t block = 64;
    std::vector<Layer> workers(threads);
    std::vector<std::future<void>> jobs;
    for (auto& work : workers) {
        auto* local = &work;
        jobs.push_back(std::async(std::launch::async, [local, &sources, &cursor] {
            for (;;) {
                const auto lo = cursor.fetch_add(block, std::memory_order_relaxed);
                if (lo >= sources.size()) return;
                for (size_t i = lo; i < std::min(lo + block, sources.size()); ++i) {
                    local->worker.scan(sources[i], target_cap);
                    for (const auto key : local->worker.fresh) {
                        if (packed_energy(key) != target_cap) continue;
                        const auto [prior, inserted] = local->targets.try_emplace(key, i);
                        if (!inserted) prior->second = std::min(prior->second, i);
                    }
                    local->worker.fresh.clear();
                }
            }
        }));
    }
    std::unordered_map<Key, size_t, KeyHash> destinations;
    uint64_t tested = 0, admitted = 0, bridged = 0;
    for (auto& job : jobs) job.get();
    for (const auto& local : workers) {
        tested += local.worker.candidates;
        admitted += local.worker.admitted;
        bridged += local.worker.nonempty;
        // A singleton reduces total energy below that of the source.
        for (const auto& [key, i] : local.targets) {
            const auto [prior, inserted] = destinations.try_emplace(key, i);
            if (!inserted) prior->second = std::min(prior->second, i);
        }
    }
    std::vector<Key> sorted;
    sorted.reserve(destinations.size());
    for (const auto& [key, ignored] : destinations) sorted.push_back(key);
    std::sort(sorted.begin(), sorted.end());
    std::ofstream triples(name + ".triples.tsv"), parents(name + ".parents.tsv");
    if (!triples || !parents) throw std::runtime_error("cannot write frontier files");
    for (const Key key : sorted) {
        write_tsv(triples, rows_from(key));
        write_tsv(parents, rows_from(sources[destinations.at(key)]));
    }
    if (!triples || !parents) throw std::runtime_error("failed while writing frontier files");
    std::cout << "{\n  \"seed_orbits\": " << sources.size()
              << ",\n  \"target_energy\": " << target_cap
              << ",\n  \"product_candidates\": " << tested
              << ",\n  \"positive_bridge_candidates\": " << bridged
              << ",\n  \"admitted_products_through_cap\": " << admitted
              << ",\n  \"destination_orbits_at_exact_energy\": " << sorted.size() << "\n}\n";
    return 0;
}

}

int main(int argc, char** argv) {
    try {
        if (argc != 4) throw std::runtime_error("usage: chartless-frontier sources.tsv prefix workers");
        return frontier(argv[1], argv[2], std::stoul(argv[3]));
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
