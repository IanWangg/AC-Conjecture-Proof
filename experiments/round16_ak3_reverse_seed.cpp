// Meet the complete cap-33 first-exit index from a marked rank-two waypoint.
#define AC_ROUND07_WIDE_ORBITS_LIBRARY
#include "round07_ak3_wide_orbits.cpp"

#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>

namespace {
using wide_orbits::Hash;
using wide_orbits::Pair;
using wide_orbits::energy;
using wide_orbits::no_parent;
using orbit_search::Code;
using orbit_search::word;
using Record = std::array<Code, 4>;

struct Shard {
    const Record* records = nullptr;
    size_t size = 0;
    ~Shard() { if (records) munmap(const_cast<Record*>(records), size * sizeof(Record)); }
    Shard() = default;
    Shard(Shard&&) = delete;
    Shard(const Shard&) = delete;

    void load(const std::string& path) {
        std::ifstream input(path, std::ios::binary | std::ios::ate);
        const auto bytes = input.tellg();
        if (!input || bytes <= 0 || bytes % sizeof(Record))
            throw std::runtime_error("bad seed shard");
        size = bytes / sizeof(Record);
        const int fd = open(path.c_str(), O_RDONLY);
        if (fd < 0) throw std::runtime_error("cannot open seed shard");
        auto* mapping = mmap(nullptr, bytes, PROT_READ, MAP_PRIVATE, fd, 0);
        close(fd);
        if (mapping == MAP_FAILED) throw std::runtime_error("cannot map seed shard");
        records = static_cast<const Record*>(mapping);
    }

    const Record* find(const Pair& p) const {
        const auto row = std::lower_bound(records, records + size, p,
            [](const Record& record, const Pair& id) { return Pair{record[0], record[1]} < id; });
        if (row == records + size || Pair{(*row)[0], (*row)[1]} != p) return nullptr;
        return row;
    }
};

constexpr unsigned seed_energy = 33;
constexpr size_t shard_count = 128;

struct Worker {
    orbit_search::Worker menu;
    std::vector<std::pair<Pair, uint32_t>> out;
    std::unordered_set<Pair, Hash> local;
};

void write_pair(const Pair& p) {
    std::cout << "[\"" << word(p.first) << "\",\"" << word(p.second) << "\"]";
}

int search(const Pair& root, const std::string& shards, uint32_t budget, unsigned workers,
           const char* catalogue, unsigned cap) {
    if (cap < seed_energy || cap > 62 || energy(root) > cap || !workers || !budget)
        throw std::runtime_error("invalid reverse search parameters");
    std::array<Shard, shard_count> index;
    uint64_t indexed = 0;
    for (size_t i = 0; i < index.size(); ++i) {
        index[i].load(shards + "/unique." + std::to_string(i) + ".bin");
        indexed += index[i].size;
    }
    std::vector<Pair> nodes{root};
    std::vector<uint32_t> parents{no_parent};
    std::unordered_set<Pair, Hash> visited{root};
    std::vector<Worker> pool(workers);
    const auto ak3 = wide_orbits::key("xxxYYYY", "xyxYXY");
    const Record* hit = nullptr;
    bool ak3_met = false;
    uint32_t found = no_parent, primitive = no_parent, expanded = 0;
    const auto classify = [&](const Pair& key, uint32_t at) {
        if (key == ak3 && at != 0) {
            found = at;
            ak3_met = true;
        }
        if (energy(key) == seed_energy) {
            hit = index[Hash{}(key) & (index.size()-1)].find(key);
            if (hit) found = at;
        }
        if (orbit_search::primitive(word(key.first)) || orbit_search::primitive(word(key.second)))
            primitive = at;
    };
    classify(root, 0);
    while (expanded < nodes.size() && expanded < budget && found == no_parent && primitive == no_parent) {
        const uint32_t end = std::min<uint64_t>({expanded + uint64_t(768), nodes.size(), budget});
        std::atomic<uint32_t> cursor{expanded};
        std::vector<std::future<void>> tasks;
        for (auto& worker : pool) {
            worker.out.clear();
            tasks.push_back(std::async(std::launch::async, [&worker, &nodes, &visited, &cursor, end, cap] {
                for (;;) {
                    const auto at = cursor++;
                    if (at >= end) break;
                    worker.local.clear();
                    const auto [a,b] = nodes[at];
                    if (cap - std::min(orbit_search::length(a), orbit_search::length(b)) > 31)
                        throw std::runtime_error("reverse product exceeds packed coordinate width");
                    worker.menu.scan_pair(a, b, cap, [&](const auto& r, const auto& d) {
                        const auto key = ak3_wide::least_image(r,d);
                        if (!visited.count(key) && worker.local.insert(key).second)
                            worker.out.emplace_back(key, at);
                    });
                }
            }));
        }
        for (auto& task : tasks) task.get();
        std::vector<std::pair<Pair, uint32_t>> fresh;
        for (const auto& worker : pool) fresh.insert(fresh.end(), worker.out.begin(), worker.out.end());
        std::sort(fresh.begin(), fresh.end());
        for (const auto& [key, parent] : fresh) {
            if (!visited.insert(key).second) continue;
            if (nodes.size() >= no_parent) throw std::runtime_error("reverse index exhausted");
            const uint32_t at = nodes.size();
            nodes.push_back(key);
            parents.push_back(parent);
            classify(key, at);
            if (found != no_parent || primitive != no_parent) break;
        }
        if (expanded / 16384 != end / 16384)
            std::cerr << "expanded " << end << ", discovered " << nodes.size() << '\n';
        expanded = end;
    }
    uint64_t candidates = 0, admitted = 0;
    for (const auto& worker : pool) {
        candidates += worker.menu.candidates;
        admitted += worker.menu.admitted;
    }
    if (catalogue) {
        auto ordered = nodes;
        std::sort(ordered.begin(), ordered.end(), wide_orbits::catalogue_order);
        std::ofstream tsv(catalogue);
        for (const auto& [a, b] : ordered) tsv << word(a) << '\t' << word(b) << '\n';
        if (!tsv) throw std::runtime_error("cannot write reverse catalogue");
    }
    std::cout << "{\"cap\":" << cap << ",\"indexed_seeds\":" << indexed
              << ",\"expanded\":" << expanded << ",\"discovered\":" << nodes.size()
              << ",\"candidates\":" << candidates << ",\"admitted\":" << admitted
              << ",\"closed\":" << (expanded == nodes.size() && found == no_parent && primitive == no_parent ? "true" : "false")
              << ",\"seed_anchor\":";
    if (hit) write_pair(Pair{(*hit)[2], (*hit)[3]});
    else std::cout << "null";
    if (cap != seed_energy) std::cout << ",\"ak3_orbit_met\":" << (ak3_met ? "true" : "false");
    std::cout << ",\"primitive\":" << (primitive != no_parent ? "true" : "false") << ",\"route\":[";
    std::vector<Pair> route;
    for (auto at = found != no_parent ? found : primitive; at != no_parent; at = parents[at])
        route.push_back(nodes[at]);
    for (auto it = route.rbegin(); it != route.rend(); ++it) {
        if (it != route.rbegin()) std::cout << ',';
        write_pair(*it);
    }
    std::cout << "]}\n";
    return 0;
}
}

int main(int argc, char** argv) {
    try {
        if (argc < 6 || argc > 8)
            throw std::runtime_error("usage: reverse-seed row0 row1 shard-dir expansion-budget workers [catalogue.tsv [cap]]");
        for (int i : {1, 2}) {
            const std::string row(argv[i]);
            if (row.empty() || row.size() > 31 || cyclic(row) != row)
                throw std::runtime_error("need nonempty cyclically reduced coordinates of width at most 31");
        }
        round01::check_product();
        return search(wide_orbits::key(argv[1], argv[2]), argv[3],
                      std::stoul(argv[4]), std::stoul(argv[5]), argc >= 7 ? argv[6] : nullptr,
                      argc == 8 ? std::stoul(argv[7]) : seed_energy);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
