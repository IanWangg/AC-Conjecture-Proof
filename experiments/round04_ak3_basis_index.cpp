// Join a large cyclic catalogue to short intrinsic bases of reverse cores.
#define main round02_fiber_join_main
#include "round02_ak3_fiber_join.cpp"
#undef main
#include <map>

namespace basis_index {

using Key = uint64_t;

std::string cyclic_key(const std::string& cyclic) {
    auto forwards = rotations(cyclic);
    auto backwards = rotations(inv(cyclic));
    return std::min(forwards.front(), backwards.front());
}

Key word_key(const std::string& word) {
    Key code = 1;
    for (char c : word) code = (code << 2) | letter(c);
    return code;
}

Key pair_key(const std::string& a, const std::string& b) {
    const auto& low = std::min(a, b);
    const auto& high = std::max(a, b);
    Key code = 32 + low.size();
    for (const auto* word : {&low, &high})
        for (char c : *word) code = (code << 2) | letter(c);
    return code;
}

struct Catalogue {
    std::unordered_set<Key> pairs, words;
    int cap = 0, minimum = 28;

    explicit Catalogue(const char* path) {
        std::ifstream file(path);
        if (!file) throw std::runtime_error("cannot open forward catalogue");
        std::string row;
        while (std::getline(file, row)) {
            const auto tab = row.find('\t');
            if (tab == std::string::npos || tab == 0 || tab + 1 == row.size() || row.size() > 29)
                throw std::runtime_error("expected nonempty forward words of total length at most 28");
            const auto a = row.substr(0, tab), b = row.substr(tab + 1);
            cap = std::max(cap, int(a.size() + b.size()));
            minimum = std::min({minimum, int(a.size()), int(b.size())});
            if (!pairs.insert(pair_key(a, b)).second)
                throw std::runtime_error("duplicate forward pair");
            words.insert(word_key(a));
            words.insert(word_key(b));
        }
        if (pairs.empty() || file.bad()) throw std::runtime_error("empty or unreadable forward catalogue");
    }
};

int degree(const Graph& graph, int vertex) {
    return int(std::count_if(graph.out[vertex].begin(), graph.out[vertex].end(),
                             [](int endpoint) { return endpoint >= 0; }));
}

struct Segment {
    std::string word;
    int end;
};

Segment segment(const Graph& graph, int start, int c) {
    Segment path{std::string(1, "xXyY"[c]), graph.out[start][c]};
    int backward = c ^ 1;
    while (degree(graph, path.end) == 2) {
        int next = 0;
        while (next == backward || graph.out[path.end][next] < 0) ++next;
        path.word += "xXyY"[next];
        path.end = graph.out[path.end][next];
        backward = next ^ 1;
    }
    return path;
}

struct Shape {
    std::string first, second;
    int first_chord, second_chord;
    int shared = 0, bridge = 0;
    std::string kind;

    int length_lower_bound(int a, int b) const {
        return std::abs(a) * first_chord + std::abs(b) * second_chord
             + std::abs(a + b) * shared + ((a && b) ? 2 * bridge : 0);
    }
};

Shape barbell(const std::string& left, const std::string& right, const std::string& bridge) {
    return Shape{left, bridge + right + inv(bridge), int(left.size()), int(right.size()),
                 0, int(bridge.size()), "barbell"};
}

Shape describe(const Graph& graph) {
    std::vector<int> branches;
    for (int i = 0; i < int(graph.out.size()); ++i)
        if (degree(graph, i) > 2) branches.push_back(i);
    if (branches.size() != 1 && branches.size() != 2)
        throw std::runtime_error("unexpected rank-two topology");

    auto paths = [&](int start) {
        std::vector<Segment> out;
        for (int c = 0; c < 4; ++c)
            if (graph.out[start][c] >= 0) out.push_back(segment(graph, start, c));
        return out;
    };
    const auto from_first = paths(branches[0]);
    if (branches.size() == 1) {
        std::vector<std::string> loops;
        for (const auto& path : from_first)
            if (path.word < inv(path.word)) loops.push_back(path.word);
        if (loops.size() != 2) throw std::runtime_error("bad figure-eight");
        return Shape{loops[0], loops[1], int(loops[0].size()), int(loops[1].size()), 0, 0, "rose"};
    }
    std::vector<std::string> crossing;
    std::string first_loop;
    for (const auto& path : from_first)
        if (path.end == branches[1]) crossing.push_back(path.word);
        else first_loop = path.word;
    if (crossing.size() == 3) {
        const auto& p = crossing[0];
        const auto& q = crossing[1];
        const auto& r = crossing[2];
        return Shape{p + inv(q), p + inv(r), int(q.size()), int(r.size()), int(p.size()), 0, "theta"};
    }
    if (crossing.size() != 1 || first_loop.empty()) throw std::runtime_error("bad barbell");
    for (const auto& path : paths(branches[1]))
        if (path.end == branches[1]) return barbell(first_loop, path.word, crossing.front());
    throw std::runtime_error("missing second barbell lobe");
}

std::string basis_word(const Shape& shape, int a, int b) {
    const auto primitive = standard_primitive(std::abs(a), std::abs(b));
    const auto first = a < 0 ? inv(shape.first) : shape.first;
    const auto second = b < 0 ? inv(shape.second) : shape.second;
    std::string expanded;
    for (char c : primitive) expanded += c == 'x' ? first : second;
    return cyclic_key(cyclic_reduce(expanded));
}

struct Totals {
    uint64_t rotation_pairs = 0, rotation_cores = 0, bridges = 0, slopes = 0;
    uint64_t possible_coordinates = 0, basis_pairs_checked = 0, endpoint_pairs = 0;
    std::map<std::string, uint64_t> topology;
};

struct Candidate {
    Vec slope;
    std::string word;
};

bool scan(const Catalogue& catalogue, const Shape& shape, const Words& reverse,
          const Words& representatives, const std::string& bridge,
          Totals& stats, std::ostream& out) {
    ++stats.topology[shape.kind];
    std::vector<Candidate> accepted;
    const int limit = catalogue.cap - catalogue.minimum;
    for (int a = 0; a * shape.first_chord <= limit; ++a) {
        const int bound = (limit - a * shape.first_chord) / shape.second_chord;
        for (int b = -bound; b <= bound; ++b) {
            if ((a == 0 && b != 1) || std::gcd(a, std::abs(b)) != 1) continue;
            const int lower = shape.length_lower_bound(a, b);
            if (lower > limit) continue;
            ++stats.slopes;
            auto word = basis_word(shape, a, b);
            if (int(word.size()) < lower) throw std::runtime_error("homology length bound failed");
            if (int(word.size()) > limit || !catalogue.words.count(word_key(word))) continue;
            ++stats.possible_coordinates;
            for (const auto& previous : accepted) {
                if (previous.word.size() + word.size() > size_t(catalogue.cap) ||
                    std::abs(determinant(previous.slope, {a, b})) != 1) continue;
                ++stats.basis_pairs_checked;
                if (!catalogue.pairs.count(pair_key(previous.word, word))) continue;
                out << "{\"status\":\"JOIN\",\"topology\":\"" << shape.kind
                    << "\",\"reverse_pair\":";
                words_json(out, reverse);
                out << ",\"reverse_lobe_representatives\":";
                words_json(out, representatives);
                out << ",\"bridge\":\"" << bridge << "\",\"core_basis\":";
                words_json(out, Words{shape.first, shape.second});
                out << ",\"slopes\":[[" << previous.slope[0] << ',' << previous.slope[1]
                    << "],[" << a << ',' << b << "]],\"forward_pair\":";
                words_json(out, Words{std::min(previous.word, word), std::max(previous.word, word)});
                out << "}\n";
                return true;
            }
            accepted.push_back({{a, b}, std::move(word)});
        }
    }
    return false;
}

bool reverse_bridges(int remaining, std::string& path, const Words& words,
                     const std::vector<std::string>& first, const std::vector<std::string>& second,
                     const Catalogue& catalogue, Totals& stats, std::ostream& out) {
    if (remaining == 0) {
        for (const auto& p : first) {
            if (path.front() == p.front() || path.front() == inverse(p.back())) continue;
            for (const auto& q : second) {
                if (inverse(path.back()) == q.front() || path.back() == q.back()) continue;
                ++stats.bridges;
                if (scan(catalogue, barbell(p, q, path), words, Words{p, q}, path, stats, out))
                    return true;
            }
        }
        return false;
    }
    for (char c : std::string("xXyY")) {
        if (!path.empty() && c == inverse(path.back())) continue;
        path.push_back(c);
        if (reverse_bridges(remaining - 1, path, words, first, second, catalogue, stats, out))
            return true;
        path.pop_back();
    }
    return false;
}

int run(const char* forward, const char* reverse, const char* output) {
    const Catalogue catalogue(forward);
    const auto targets = read_pairs(reverse);
    std::ofstream out(output);
    if (!out) throw std::runtime_error("cannot open basis-index report");
    Totals stats;
    std::unordered_set<std::string> seen;
    for (const auto& item : targets) {
        for (const auto& w : item)
            if (w.empty() || cyclic_reduce(w) != w || cyclic_key(w) != w)
                throw std::runtime_error("reverse pair must use canonical cyclic coordinates");
        if (item[0].size() + item[1].size() <= size_t(catalogue.cap)
            && catalogue.pairs.count(pair_key(item[0], item[1]))) {
            out << "{\"status\":\"EQUAL_CYCLIC_PAIR\",\"pair\":";
            words_json(out, item);
            out << "}\n";
            return 0;
        }

        const auto first = rotations(item[0]), second = rotations(item[1]);
        for (const auto& a : first) for (const auto& b : second) {
            ++stats.rotation_pairs;
            const auto [key, core] = unbased_key(fold(a, b));
            if (!seen.insert(key).second) continue;
            ++stats.rotation_cores;
            if (scan(catalogue, describe(core), item, Words{a, b}, "", stats, out)) return 0;
        }

        const int lobe_energy = int(item[0].size() + item[1].size());
        int pure = 1000;
        for (const auto& w : item)
            if (w.size() < 28 && catalogue.words.count(word_key(w))) pure = std::min(pure, int(w.size()));
        const int bound = std::max((catalogue.cap - lobe_energy - pure) / 2,
                                   (catalogue.cap - 2 * lobe_energy) / 4);
        for (int length = 1; length <= bound; ++length) {
            std::string path;
            if (reverse_bridges(length, path, item, first, second, catalogue, stats, out))
                return 0;
        }
        if (++stats.endpoint_pairs % 1000 == 0)
            std::cerr << stats.endpoint_pairs << " reverse pairs, " << stats.rotation_cores
                      << " distinct rotation cores, " << stats.bridges << " bridges\n";
    }
    out << "{\n  \"status\":\"NO_SUBGROUP_JOIN\",\n  \"forward_pairs\":" << catalogue.pairs.size()
        << ",\n  \"forward_distinct_words\":" << catalogue.words.size()
        << ",\n  \"forward_cap\":" << catalogue.cap
        << ",\n  \"forward_minimum_coordinate\":" << catalogue.minimum
        << ",\n  \"reverse_pairs\":" << stats.endpoint_pairs
        << ",\n  \"reverse_rotation_pairs\":" << stats.rotation_pairs
        << ",\n  \"reverse_distinct_rotated_cores\":" << stats.rotation_cores
        << ",\n  \"reverse_geodesic_bridges\":" << stats.bridges
        << ",\n  \"primitive_slopes_constructed\":" << stats.slopes
        << ",\n  \"coordinates_found_in_forward_catalogue\":" << stats.possible_coordinates
        << ",\n  \"basis_pair_lookups\":" << stats.basis_pairs_checked << ",\n  \"core_topologies\":{";
    bool first = true;
    for (const auto& [kind, count] : stats.topology) {
        if (!first) out << ',';
        first = false;
        out << '"' << kind << "\":" << count;
    }
    out << "}\n}\n";
    if (!out) throw std::runtime_error("basis-index report write failed");
    return 0;
}
}  // namespace basis_index

int main(int argc, char** argv) {
    try {
        if (argc != 4) throw std::runtime_error("usage: basis_index forward.tsv reverse.tsv result.json");
        return basis_index::run(argv[1], argv[2], argv[3]);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
