// Screen reachable cyclic pairs and their independently rotated representatives.
#define main round02_two_copies_main
#include "round02_ac_disproof_two_copies.cpp"
#undef main
#include "u_graph_fold.hpp"
#include <numeric>

namespace frontier {
using Words = std::pair<std::string, std::string>;

struct Counts {
    uint64_t source_pairs = 0, rotations = 0, cores = 0, own_tests = 0, joins = 0;
    uint64_t dag = 0, exact_absent = 0, exact_states = 0, positive = 0, incomplete = 0;
};

Words read_pair(const std::string& row) {
    const auto separator = row.find('\t');
    if (separator == std::string::npos) throw std::runtime_error("expected two TSV columns");
    Words pair{row.substr(0, separator), row.substr(separator + 1)};
    for (const auto* word : {&pair.first, &pair.second})
        if (word->empty() || reduce(*word) != *word || word->front() == inverse(word->back()))
            throw std::runtime_error("expected nonempty cyclically reduced words");
    return pair;
}

Graph source_core(const Words& words) {
    if (words.first.size() + words.second.size() <= 120) return fold(words.first, words.second);
    Graph graph{u_native::fold_words({words.first, words.second})};
    if (rank(graph) != 2 || graph.out.size() >= 255)
        throw std::runtime_error("unsupported rank or unbased core size");
    return graph;
}

bool check(const Words& input, const Words& rotated, const Graph& source_core,
           int a, int b, const Graph& graph, Counts& counts, std::ostream& hits) {
    if (proves_primitive_absence(graph)) { ++counts.dag; return true; }
    const auto result = u_native::decide(graph.out, 0);
    counts.exact_states += result.pair_states;
    if (result.status == u_native::Status::ABSENT) { ++counts.exact_absent; return true; }
    if (result.status == u_native::Status::PRIMITIVE) ++counts.positive;
    else ++counts.incomplete;
    hits << "{\"source\":[\"" << input.first << "\",\"" << input.second
         << "\"],\"rotated\":[\"" << rotated.first << "\",\"" << rotated.second
         << "\"],\"vertices\":[" << a << ',' << b << "],\"source_core\":";
    graph_json(hits, source_core);
    hits << ",\"graph\":";
    graph_json(hits, graph);
    hits << ",\"status\":\"" << u_native::status_name(result.status) << '"';
    if (result.status == u_native::Status::PRIMITIVE) {
        const auto& witness = result.witness;
        hits << ",\"primitive\":\"" << witness.cyclic_word << "\",\"based_word\":\""
             << witness.based_word << "\",\"loop_vertex\":" << witness.vertex
             << ",\"alphabet\":\"" << witness.alphabet << "\",\"program\":\""
             << witness.program << "\",\"component\":" << witness.component;
    }
    hits << "}\n";
    hits.flush();
    return false;
}

int run(std::istream& input, std::ostream& hits, std::ostream& output, bool rotate) {
    Counts counts;
    std::unordered_set<std::string> seen;
    std::string row;
    while (std::getline(input, row)) {
        const auto words = read_pair(row);
        ++counts.source_pairs;
        const auto first = rotate ? rotations(words.first) : std::vector<std::string>{words.first};
        const auto second = rotate ? rotations(words.second) : std::vector<std::string>{words.second};
        for (const auto& u : first) for (const auto& v : second) {
            ++counts.rotations;
            const auto [key, graph] = unbased_key(source_core({u, v}));
            if (!seen.insert(key).second) continue;
            ++counts.cores;
            ++counts.own_tests;
            if (!check(words, {u, v}, graph, 0, 0, graph, counts, hits)) continue;
            for (size_t a = 0; a < graph.out.size(); ++a) {
                for (size_t b = a + 1; b < graph.out.size(); ++b) {
                    ++counts.joins;
                    check(words, {u, v}, graph, static_cast<int>(a), static_cast<int>(b),
                          join(graph, static_cast<int>(a), static_cast<int>(b)), counts, hits);
                }
            }
        }
        if (counts.source_pairs % 1000 == 0)
            std::cerr << counts.source_pairs << " source rows, " << counts.cores << " cores, "
                      << counts.joins << " joins and " << counts.positive << " positives\n";
    }
    output << "{\n  \"rotations_enabled\": " << (rotate ? "true" : "false")
           << ",\n  \"source_pairs\": " << counts.source_pairs
           << ",\n  \"rotation_pairs\": " << counts.rotations
           << ",\n  \"unbased_cores\": " << counts.cores
           << ",\n  \"own_tests\": " << counts.own_tests
           << ",\n  \"distinct_vertex_joins\": " << counts.joins
           << ",\n  \"DAG_absent\": " << counts.dag
           << ",\n  \"exact_absent\": " << counts.exact_absent
           << ",\n  \"exact_map_pair_states\": " << counts.exact_states
           << ",\n  \"positive\": " << counts.positive
           << ",\n  \"incomplete\": " << counts.incomplete << "\n}\n";
    if (!hits || !output) throw std::runtime_error("output write failed");
    return 0;
}
}

int main(int argc, char** argv) {
    try {
        if (argc != 5 || (std::string(argv[2]) != "literal" && std::string(argv[2]) != "rotations"))
            throw std::runtime_error("usage: frontier source.tsv literal|rotations hits.jsonl result.json");
        std::ifstream input(argv[1]);
        std::ofstream hits(argv[3]), output(argv[4]);
        if (!input || !hits || !output) throw std::runtime_error("file open failed");
        return frontier::run(input, hits, output, std::string(argv[2]) == "rotations");
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
