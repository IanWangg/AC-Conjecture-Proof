// Search a marked rank-three tail with bounded auxiliary-letter support.
#define AC_ROUND06_SINGLETON_LIBRARY
#include "round06_stable_proof_all_singleton.cpp"

namespace {

Key ordered_pack(Code a, Code b, Code c) {
    const unsigned la = length(a), lb = length(b), lc = length(c);
    const auto a_flag = Code(1) << (3 * la), b_flag = Code(1) << (3 * lb);
    const auto c_flag = Code(1) << (3 * lc);
    Key result = ((Key(1) << 10) | (la << 5) | lb);
    result = (result << (3 * la)) | (a ^ a_flag);
    result = (result << (3 * lb)) | (b ^ b_flag);
    return (result << (3 * lc)) | (c ^ c_flag);
}

Triple ordered_rows(Key key) {
    const auto codes = unpack(key);
    return {decode(codes[0]), decode(codes[1]), decode(codes[2])};
}

void write_ordered(std::ostream& out, Key key) {
    const auto rows = ordered_rows(key);
    out << rows[0] << '\t' << rows[1] << '\t' << rows[2] << '\n';
}

Key marked_key(const Triple& rows) {
    return ordered_pack(encode(rows[0]), encode(rows[1]), encode(rows[2]));
}

bool in_range(const Triple& rows, int floor, int cap) {
    return int(energy(rows)) >= floor && int(energy(rows)) <= cap
        && std::all_of(rows.begin(), rows.end(), [](const auto& word) {
            return !word.empty() && word.size() <= 21;
        });
}

int max_z = 1;

int count_z(const std::string& word) {
    return std::count(word.begin(), word.end(), 'z') + std::count(word.begin(), word.end(), 'Z');
}

struct Scanner {
    std::unordered_map<Code, std::vector<std::string>> rotations;
    std::map<int, std::vector<P>> bridges;
    uint64_t candidates = 0, admitted = 0, nonempty = 0, outside_word_width = 0;

    void neighbors(Key point, int floor, int cap, std::vector<Key>& result) {
        const auto rows = ordered_rows(point);
        const int total = int(energy(rows));
        const int aux_count = count_z(rows[0]) + count_z(rows[1]) + count_z(rows[2]);
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
                if (max_z == 1 && count_z(rows[j])) continue;

                const int bound = std::min(3, std::max(0, (cap - total - int(rows[j].size())) / 2));
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
                            if (!word || aux_count - count_z(rows[i]) + count_z(*word) > max_z) continue;
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
            for (auto word : products) {
                auto replacement = codes;
                replacement[i] = word;
                result.push_back(ordered_pack(replacement[0], replacement[1], replacement[2]));
            }
        }
        std::sort(result.begin(), result.end());
        result.erase(std::unique(result.begin(), result.end()), result.end());
    }
};

template<class Add>
void import(const std::string& path, Add add, int floor, int cap) {
    std::ifstream file(path);
    if (!file) throw std::runtime_error("cannot open input " + path);
    Triple rows;
    while (file >> rows[0] >> rows[1] >> rows[2]) {
        if (!in_range(rows, floor, cap)) continue;
        for (auto& word : rows) word = canonical(word);
        const int auxiliary = count_z(rows[0]) + count_z(rows[1]) + count_z(rows[2]);
        if (auxiliary <= max_z) add(marked_key(rows));
    }
}

int search(int floor, int cap, size_t budget, const std::string& roots, const std::string& targets,
           const std::string& prefix) {
    if (floor < 12 || cap > 40 || floor > cap || !budget)
        throw std::invalid_argument("invalid energy range or search budget");
    Scanner scanner;
    struct Reach {
        std::vector<Key> nodes, neighbors;
        std::unordered_map<Key, size_t, KeyHash> seen;
        std::vector<size_t> layer;
        void add(Key key, size_t parent, std::vector<size_t>& next) {
            if (!seen.try_emplace(key, parent).second) return;
            next.push_back(nodes.size());
            nodes.push_back(key);
        }
    };
    Reach forward, reverse;
    import(roots, [&](Key key) { forward.add(key, seed_parent, forward.layer); }, floor, cap);
    import(targets, [&](Key key) { reverse.add(key, seed_parent, reverse.layer); }, floor, cap);
    if (forward.layer.empty() || reverse.layer.empty()) throw std::runtime_error("empty input");
    size_t expanded = 0;
    std::optional<Key> join;
    while (!join && !forward.layer.empty() && !reverse.layer.empty() && expanded < budget) {
        auto& active = (forward.layer.size() <= reverse.layer.size()) ? forward : reverse;
        auto& other = (&active == &forward) ? reverse : forward;
        std::vector<size_t> next;
        for (auto index : active.layer) {
            if (join || expanded >= budget) break;
            const auto key = active.nodes[index];
            ++expanded;
            if (other.seen.count(key)) {join = key; break;}
            scanner.neighbors(key, floor, cap, active.neighbors);
            for (auto successor : active.neighbors) {
                active.add(successor, index, next);
                if (other.seen.count(successor)) {join=successor; break;}
            }
        }
        active.layer = std::move(next);
    }
    std::ofstream route(prefix + ".route.tsv");
    if (!route) throw std::runtime_error("cannot open output");
    if (join) {
        std::vector<Key> left, right;
        for (Key at = *join;;) {
            left.push_back(at);
            const auto parent = forward.seen.at(at);
            if (parent == seed_parent) break;
            at = forward.nodes[parent];
        }
        for (Key at = *join;;) {
            const auto parent = reverse.seen.at(at);
            if (parent == seed_parent) break;
            at = reverse.nodes[parent];
            right.push_back(at);
        }
        for (auto it = left.rbegin(); it != left.rend(); ++it) write_ordered(route, *it);
        for (auto at : right) write_ordered(route, at);
    }
    std::cout << "{\"expanded\":" << expanded << ",\"forward\":" << forward.nodes.size()
              << ",\"reverse\":" << reverse.nodes.size() << ",\"join\":"
              << (join ? "true" : "false") << "}\n";
    return 0;
}

}

#ifndef AC_ROUND16_PIVOT_LIBRARY
int main(int argc, char** argv) {
    try {
        if (argc != 8) throw std::runtime_error("usage: search floor cap budget roots.tsv targets.tsv prefix max_z");
        max_z = std::stoi(argv[7]);
        if (max_z < 1) throw std::invalid_argument("positive auxiliary-letter bound required");
        return search(std::stoi(argv[1]), std::stoi(argv[2]), std::stoull(argv[3]), argv[4], argv[5], argv[6]);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
#endif
