// Search a stated bounded rank-three cyclic graph from certified reverse roots.
#define AC_ROUND06_SINGLETON_LIBRARY
#include "round06_stable_proof_all_singleton.cpp"

namespace {

Key signed_key(CompactOrbits& orbits, const Triple& rows) {
    return compact_orbit(orbits.word(encode(rows[0])), orbits.word(encode(rows[1])),
                         orbits.word(encode(rows[2])));
}

bool in_range(const Triple& rows, int floor, int cap) {
    return int(energy(rows)) >= floor && int(energy(rows)) <= cap
        && std::all_of(rows.begin(), rows.end(), [](const auto& word) {
            return !word.empty() && word.size() <= 21;
        });
}

struct Seen {
    size_t parent;
    unsigned distance;
};

struct Scanner {
    CompactOrbits orbits;
    std::unordered_map<Code, std::vector<std::string>> rotations;
    std::map<int, std::vector<P>> bridges;
    uint64_t candidates = 0, admitted = 0, nonempty = 0, outside_word_width = 0;

    void neighbors(Key point, int floor, int cap, std::vector<Key>& result) {
        const auto rows = rows_from(point);
        const int total = int(energy(rows));
        orbits.limit();
        if (rotations.size() > 8192) rotations.clear();
        const std::array<Code, 3> codes{encode(rows[0]), encode(rows[1]), encode(rows[2])};
        for (size_t i = 0; i < 3; ++i)
            if (!rotations.count(codes[i])) rotations.emplace(codes[i], variants(rows[i]));
        result.clear();
        for (size_t i = 0; i < 3; ++i) {
            const size_t allowance = cap - total + rows[i].size();
            std::unordered_set<Code> products;
            for (size_t j = 0; j < 3; ++j) {
                if (i == j) continue;
                const int bound = std::max(0, (cap - total - int(rows[j].size())) / 2);
                if (!bridges.count(bound)) bridges.emplace(bound, bridges_rank_three(bound));
                for (const auto& a : rotations.at(codes[i]))
                    for (const auto& b : rotations.at(codes[j]))
                        for (const auto& [tail, back] : bridges.at(bound)) {
                            ++candidates;
                            std::optional<std::string> word;
                            if (tail.empty()) word = zero_bridge(a, b, allowance);
                            else {
                                ++nonempty;
                                auto rotated = cyclic(a + tail + b + back);
                                if (rotated.size() <= allowance) word = canonical(std::move(rotated));
                            }
                            if (!word) continue;
                            if (word->empty()) throw std::runtime_error("vanished row on a unimodular path");
                            if (int(word->size() + total - rows[i].size()) < floor) continue;
                            if (word->size() > 21) {
                                ++outside_word_width;
                                continue;
                            }
                            ++admitted;
                            products.insert(encode(*word));
                        }
            }
            const auto& a = orbits.word(codes[(i + 1) % 3]);
            const auto& b = orbits.word(codes[(i + 2) % 3]);
            for (auto word : products) result.push_back(compact_orbit(a, b, orbits.word(word)));
        }
        std::sort(result.begin(), result.end());
        result.erase(std::unique(result.begin(), result.end()), result.end());
    }
};

template<class Add>
size_t import(const std::string& path, Add add, int floor, int cap, CompactOrbits& cache) {
    std::ifstream file(path);
    if (!file) throw std::runtime_error("cannot open input " + path);
    size_t count = 0;
    Triple rows;
    while (file >> rows[0] >> rows[1] >> rows[2]) {
        if (!in_range(rows, floor, cap)) continue;
        for (auto& word : rows) word = canonical(word);
        cache.limit();
        add(signed_key(cache, rows));
        ++count;
    }
    return count;
}

int search(int floor, int cap, size_t budget, const std::string& roots, const std::string& targets,
           const std::string& prefix) {
    if (floor < 12 || cap > 34 || floor > cap || !budget)
        throw std::invalid_argument("invalid energy range or search budget");
    Scanner scanner;
    std::unordered_set<Key, KeyHash> wanted;
    const size_t eligible_targets = import(targets, [&](Key key) { wanted.insert(key); }, floor, cap, scanner.orbits);
    std::unordered_map<Key, Seen, KeyHash> visited;
    std::vector<Key> nodes, neighbors;
    std::optional<size_t> join;
    const auto add = [&](Key key, size_t parent, unsigned distance) {
        if (!visited.try_emplace(key, Seen{parent, distance}).second) return;
        if (!join && wanted.count(key)) join = nodes.size();
        nodes.push_back(key);
    };
    import(roots, [&](Key key) { add(key, seed_parent, 0); }, floor, cap, scanner.orbits);
    const size_t root_count = nodes.size();
    if (!root_count || wanted.empty()) throw std::runtime_error("empty roots or targets after filtering");
    size_t expanded = 0;
    while (!join && expanded < nodes.size() && expanded < budget) {
        const unsigned depth = visited.at(nodes[expanded]).distance;
        scanner.neighbors(nodes[expanded], floor, cap, neighbors);
        for (auto key : neighbors) add(key, expanded, depth + 1);
        ++expanded;
    }

    std::ofstream states(prefix + ".tsv"), route(prefix + ".route.tsv");
    if (!states || !route) throw std::runtime_error("cannot write output");
    std::map<unsigned, size_t> reached_by_depth, expanded_by_depth;
    size_t singleton_free = 0;
    for (size_t index = 0; index < nodes.size(); ++index) {
        const auto point = rows_from(nodes[index]);
        write_tsv(states, point);
        const unsigned distance = visited.at(nodes[index]).distance;
        ++reached_by_depth[distance];
        if (index < expanded) ++expanded_by_depth[distance];
        singleton_free += std::none_of(point.begin(), point.end(), [](const auto& word) { return word.size() == 1; });
    }
    if (join) {
        std::vector<size_t> path;
        for (size_t index = *join; index != seed_parent; index = visited.at(nodes[index]).parent)
            path.push_back(index);
        for (auto index = path.rbegin(); index != path.rend(); ++index) write_tsv(route, rows_from(nodes[*index]));
    }
    const auto counts = [](const auto& histogram) {
        std::cout << '[';
        for (const auto& [depth, count] : histogram) std::cout << (depth ? ", " : "") << count;
        std::cout << ']';
    };
    std::cout << "{\n  \"floor\":" << floor << ",\n  \"cap\":" << cap << ",\n  \"word_width_cap\":21,"
              << "\n  \"roots\":" << root_count << ",\n  \"eligible_target_rows\":" << eligible_targets
              << ",\n  \"target_orbits\":" << wanted.size()
              << ",\n  \"expanded\":" << expanded << ",\n  \"discovered\":" << nodes.size()
              << ",\n  \"without_singleton\":" << singleton_free
              << ",\n  \"candidates\":" << scanner.candidates << ",\n  \"positive_bridge_candidates\":" << scanner.nonempty
              << ",\n  \"admitted\":" << scanner.admitted << ",\n  \"products_above_word_width\":" << scanner.outside_word_width
              << ",\n  \"closed\":" << (!join && expanded == nodes.size() ? "true" : "false")
              << ",\n  \"join\":" << (join ? "true" : "false") << ",\n  \"reached_by_depth\":";
    counts(reached_by_depth);
    std::cout << ",\n  \"expanded_by_depth\":";
    counts(expanded_by_depth);
    std::cout << "\n}\n";
    return 0;
}

}

int main(int argc, char** argv) {
    try {
        if (argc != 7) throw std::runtime_error("usage: reverse floor cap budget roots.tsv targets.tsv prefix");
        return search(std::stoi(argv[1]), std::stoi(argv[2]), std::stoull(argv[3]), argv[4], argv[5], argv[6]);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
