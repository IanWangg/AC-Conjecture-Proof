// Exact one-phase subgroup match between two finite cyclic-pair catalogues.
#define Q_ROTATION_SUBGROUPS_LIBRARY
#include "rotation_subgroups.cpp"

#include <map>
#include <optional>

using Words = std::pair<std::string, std::string>;

struct RotationWitness {
    size_t source;
    Words rotations;
};

std::string cyclic_key(const std::string& word) {
    const auto positive = rotations(word);
    const auto negative = rotations(inv(word));
    return std::min(positive.front(), negative.front());
}

Words pair_key(const Words& words) {
    auto first = cyclic_key(words.first);
    auto second = cyclic_key(words.second);
    if (second < first) std::swap(first, second);
    return {first, second};
}

std::optional<Words> barbell_lobes(const Graph& graph) {
    auto degree = [](const Row& row) {
        return std::count_if(row.begin(), row.end(), [](int target) { return target >= 0; });
    };
    std::vector<int> branches;
    for (size_t vertex = 0; vertex < graph.out.size(); ++vertex)
        if (degree(graph.out[vertex]) == 3) branches.push_back(int(vertex));
    if (branches.size() != 2) return std::nullopt;

    auto extract_loop = [&](int base) {
        for (int label = 0; label < 4; ++label) {
            int next = graph.out[base][label];
            if (next < 0) continue;
            std::string word(1, "xXyY"[label]);
            int reverse = label ^ 1;
            while (degree(graph.out[next]) == 2) {
                int next_label = 0;
                for (; next_label < 4; ++next_label)
                    if (next_label != reverse && graph.out[next][next_label] >= 0) break;
                if (next_label == 4) throw std::logic_error("invalid degree-two vertex");
                word += "xXyY"[next_label];
                next = graph.out[next][next_label];
                reverse = next_label ^ 1;
            }
            if (next == base) return word;
        }
        return std::string{};
    };
    auto first = extract_loop(branches[0]);
    if (first.empty()) return std::nullopt;
    auto second = extract_loop(branches[1]);
    if (second.empty()) throw std::logic_error("barbell has only one lobe");
    return pair_key({first, second});
}

std::vector<Words> read_catalogue(const char* path) {
    std::ifstream input(path);
    if (!input) throw std::runtime_error("unable to open cyclic-pair catalogue");
    std::vector<Words> rows;
    std::string line;
    while (std::getline(input, line)) {
        auto separator = line.find('\t');
        if (separator == std::string::npos) throw std::runtime_error("missing TSV separator");
        Words words{line.substr(0, separator), line.substr(separator + 1)};
        for (const auto& word : {words.first, words.second})
            if (word.empty() || reduce(word) != word || word.front() == inverse(word.back()))
                throw std::runtime_error("catalogue word must be nonempty and cyclically reduced");
        if (pair_key(words) != words) throw std::runtime_error("expected canonical pair");
        rows.push_back(words);
    }
    return rows;
}

using PairIndex = std::map<Words, size_t>;

PairIndex index_pairs(const std::vector<Words>& rows) {
    PairIndex index;
    for (size_t i = 0; i < rows.size(); ++i)
        if (!index.emplace(rows[i], i).second) throw std::runtime_error("duplicate canonical pair");
    return index;
}

template <typename Visitor>
void visit_rotations(const Words& source, Visitor visit) {
    auto first = rotations(source.first);
    auto second = rotations(source.second);
    for (const auto& a : first)
        for (const auto& b : second)
            visit(Words{a, b}, fold(a, b));
}

void write_words(std::ostream& out, const Words& words) {
    out << "[\"" << words.first << "\",\"" << words.second << "\"]";
}

int run_match(const char* forward_path, const char* reverse_path, const char* output_path) {
    auto forward = read_catalogue(forward_path);
    auto reverse = read_catalogue(reverse_path);
    auto forward_pairs = index_pairs(forward);
    auto reverse_pairs = index_pairs(reverse);
    std::ofstream out(output_path);
    if (!out) throw std::runtime_error("unable to open result");
    for (const auto& [words, i] : forward_pairs) {
        auto same = reverse_pairs.find(words);
        if (same != reverse_pairs.end()) {
            out << "{\"status\":\"EQUAL_CYCLIC_PAIR\",\"forward_index\":" << i
                << ",\"reverse_index\":" << same->second << ",\"canonical\":";
            write_words(out, words);
            out << "}\n";
            return 0;
        }
    }

    std::unordered_map<std::string, RotationWitness> forward_graphs;
    uint64_t forward_rotations = 0, reverse_rotations = 0;
    uint64_t forward_barbells = 0, reverse_barbells = 0;
    bool found = false;
    auto write_hit = [&](const char* kind, size_t i, size_t j,
                         const std::optional<Words>& left, const std::optional<Words>& right,
                         const Graph& graph) {
        out << "{\"status\":\"" << kind << "\",\"forward_index\":" << i
            << ",\"reverse_index\":" << j << ",\"forward_rotations\":";
        if (left) write_words(out, *left); else out << "null";
        out << ",\"reverse_rotations\":";
        if (right) write_words(out, *right); else out << "null";
        out << ",\"canonical_unbased_graph\":";
        graph_json(out, unbased_key(graph).second);
        out << "}\n";
        found = true;
    };

    for (size_t i = 0; i < forward.size() && !found; ++i) {
        visit_rotations(forward[i], [&](const Words& actual, const Graph& graph) {
            if (found) return;
            ++forward_rotations;
            const auto lobes = barbell_lobes(graph);
            if (lobes) {
                ++forward_barbells;
                auto hit = reverse_pairs.find(*lobes);
                if (hit != reverse_pairs.end()) {
                    write_hit("FORWARD_INTERSECT_REVERSE_BARBELL", i, hit->second,
                              actual, std::nullopt, graph);
                    return;
                }
            }
            forward_graphs.try_emplace(unbased_key(graph).first, RotationWitness{i, actual});
        });
    }

    for (size_t j = 0; j < reverse.size() && !found; ++j) {
        visit_rotations(reverse[j], [&](const Words& actual, const Graph& graph) {
            if (found) return;
            ++reverse_rotations;
            auto identical = forward_graphs.find(unbased_key(graph).first);
            if (identical != forward_graphs.end()) {
                const auto& witness = identical->second;
                write_hit("BOTH_INTERSECT", witness.source, j, witness.rotations, actual, graph);
                return;
            }
            const auto lobes = barbell_lobes(graph);
            if (lobes) {
                ++reverse_barbells;
                auto hit = forward_pairs.find(*lobes);
                if (hit != forward_pairs.end())
                    write_hit("FORWARD_BARBELL_REVERSE_INTERSECT", hit->second, j,
                              std::nullopt, actual, graph);
            }
        });
    }

    if (!found) {
        out << "{\n  \"status\": \"COMPLETE_NO_ALL_TAIL_SUBGROUP_MATCH\",\n"
            << "  \"forward_cyclic_pairs\": " << forward.size() << ",\n"
            << "  \"reverse_cyclic_pairs\": " << reverse.size() << ",\n"
            << "  \"forward_intersecting_rotation_pairs\": " << forward_rotations << ",\n"
            << "  \"reverse_intersecting_rotation_pairs\": " << reverse_rotations << ",\n"
            << "  \"forward_distinct_rotation_core_keys\": " << forward_graphs.size() << ",\n"
            << "  \"forward_barbell_rotation_cores_counting_repeats\": " << forward_barbells << ",\n"
            << "  \"reverse_barbell_rotation_cores_counting_repeats\": " << reverse_barbells << "\n}\n";
    }
    return 0;
}

int main(int argc, char** argv) {
    if (argc != 4) {
        std::cerr << "usage: round01_ak3_all_tails forward.tsv reverse.tsv output.json\n";
        return 2;
    }
    try {
        return run_match(argv[1], argv[2], argv[3]);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
