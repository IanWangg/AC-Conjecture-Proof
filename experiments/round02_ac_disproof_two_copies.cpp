// Test the finite join of the two rebased source graphs.
#define Q_ROTATION_SUBGROUPS_LIBRARY
#include "rotation_subgroups.cpp"

#include <map>

namespace {
constexpr Row empty_row{-1, -1, -1, -1};

int add_vertex(Graph& graph) {
    graph.out.push_back(empty_row);
    return static_cast<int>(graph.out.size()) - 1;
}

int append_path(Graph& graph, int start, const std::string& word, bool closed) {
    int vertex = start;
    for (size_t i = 0; i < word.size(); ++i) {
        int next = closed && i + 1 == word.size() ? start : add_vertex(graph);
        int label = letter(word[i]);
        if (graph.out[vertex][label] >= 0 || graph.out[next][label ^ 1] >= 0)
            throw std::runtime_error("unfolded source");
        graph.out[vertex][label] = next;
        graph.out[next][label ^ 1] = vertex;
        vertex = next;
    }
    return vertex;
}

Graph source(const std::string& p, const std::string& b, const std::string& bridge) {
    Graph graph;
    add_vertex(graph);
    append_path(graph, 0, p, true);
    const int end = append_path(graph, 0, bridge, false);
    append_path(graph, end, b, true);
    return graph;
}

Graph join(const Graph& graph, int first, int second) {
    const int n = static_cast<int>(graph.out.size());
    std::vector<Row> out = graph.out;
    for (auto row : graph.out) {
        for (int& endpoint : row)
            if (endpoint >= 0) endpoint += n;
        out.push_back(row);
    }
    std::vector<int> parent(2 * n);
    for (int v = 0; v < 2 * n; ++v) parent[v] = v;
    auto root = [&](int v) {
        while (parent[v] != v) {
            parent[v] = parent[parent[v]];
            v = parent[v];
        }
        return v;
    };
    std::vector<std::pair<int, int>> pending{{first, n + second}};
    for (size_t i = 0; i < pending.size(); ++i) {
        auto [a, b] = pending[i];
        a = root(a);
        b = root(b);
        if (a == b) continue;
        parent[b] = a;
        for (int c = 0; c < 4; ++c) {
            if (out[a][c] < 0)
                out[a][c] = out[b][c];
            else if (out[b][c] >= 0)
                pending.emplace_back(out[a][c], out[b][c]);
        }
    }

    Graph result;
    std::vector<int> names(2 * n, -1), queue{root(first)};
    names[queue.front()] = 0;
    for (size_t i = 0; i < queue.size(); ++i) {
        Row row = empty_row;
        for (int c = 0; c < 4; ++c) {
            int at = out[queue[i]][c];
            if (at < 0) continue;
            at = root(at);
            if (names[at] < 0) {
                names[at] = static_cast<int>(queue.size());
                queue.push_back(at);
            }
            row[c] = names[at];
        }
        result.out.push_back(row);
    }
    for (int vertex = 0; vertex < 2 * n; ++vertex) {
        const int image = names[root(vertex)];
        if (image < 0) throw std::runtime_error("source vertex missing from fold");
        for (int c = 0; c < 4; ++c) {
            const int end = graph.out[vertex % n][c];
            if (end < 0) continue;
            const int expected = names[root(end + (vertex >= n ? n : 0))];
            if (expected < 0 || result.out[image][c] != expected)
                throw std::runtime_error("source edge missing from fold");
        }
    }
    return result;
}

int rank(const Graph& graph) {
    int edges = 0;
    for (size_t a = 0; a < graph.out.size(); ++a) {
        for (int c = 0; c < 4; ++c) {
            const int b = graph.out[a][c];
            if (b < 0) continue;
            ++edges;
            if (graph.out[b][c ^ 1] != static_cast<int>(a))
                throw std::runtime_error("broken inverse edge");
        }
    }
    return edges / 2 - static_cast<int>(graph.out.size()) + 1;
}

struct Counts {
    uint64_t sources = 0, tests = 0, dag_exclusions = 0, unresolved = 0;
    std::map<int, uint64_t> ranks;
};

void scan(const std::string& p, const std::string& b, const std::string& bridge,
          Counts& counts, std::ostream& cases) {
    const auto core = source(p, b, bridge);
    if (rank(core) != 2 || !proves_primitive_absence(core))
        throw std::runtime_error("invalid or uncertified single source core");
    ++counts.sources;
    uint64_t previous = counts.unresolved;
    const int n = static_cast<int>(core.out.size());
    for (int a = 0; a < n; ++a) {
        for (int b_vertex = a + 1; b_vertex < n; ++b_vertex) {
            const auto graph = join(core, a, b_vertex);
            const int r = rank(graph);
            if (r < 2 || r > 4) throw std::runtime_error("join rank out of range");
            ++counts.tests;
            ++counts.ranks[r];
            if (proves_primitive_absence(graph)) {
                ++counts.dag_exclusions;
                continue;
            }
            ++counts.unresolved;
            cases << "{\"source\":[\"" << p << "\",\"" << b << "\",\"" << bridge
                  << "\"],\"vertices\":[" << a << "," << b_vertex
                  << "],\"rank\":" << r << ",\"graph\":";
            graph_json(cases, graph);
            cases << "}\n";
        }
    }
    if (counts.unresolved != previous) cases.flush();
}

void enumerate(int remaining, std::string& bridge, const std::vector<std::string>& p_rotations,
               const std::vector<std::string>& b_rotations, Counts& counts, std::ostream& cases) {
    if (remaining == 0) {
        for (const auto& p : p_rotations) {
            if (bridge.front() == p.front() || bridge.front() == inverse(p.back())) continue;
            for (const auto& b : b_rotations) {
                if (inverse(bridge.back()) != b.front() && bridge.back() != b.back())
                    scan(p, b, bridge, counts, cases);
            }
        }
        return;
    }
    for (char next : std::string("xXyY")) {
        if (!bridge.empty() && next == inverse(bridge.back())) continue;
        bridge.push_back(next);
        enumerate(remaining - 1, bridge, p_rotations, b_rotations, counts, cases);
        bridge.pop_back();
    }
}

void write_counts(std::ostream& out, const Counts& counts) {
    out << "{\"sources\":" << counts.sources << ",\"vertex_pairs\":" << counts.tests
        << ",\"DAG_exclusions\":" << counts.dag_exclusions << ",\"DAG_unresolved\":"
        << counts.unresolved << ",\"join_ranks\":{";
    bool first = true;
    for (const auto& [r, count] : counts.ranks) {
        if (!first) out << ",";
        first = false;
        out << "\"" << r << "\":" << count;
    }
    out << "}}";
}
}  // namespace

int main(int argc, char** argv) {
    try {
        if (argc != 6)
            throw std::runtime_error("usage: two_copies n min_bridge max_bridge unresolved.jsonl counts.json");
        const int parameter = std::stoi(argv[1]);
        const int first = std::stoi(argv[2]);
        const int last = std::stoi(argv[3]);
        if (parameter < 2 || first < 1 || last < first)
            throw std::runtime_error("invalid parameter or bridge bounds");
        const auto p = rotations(std::string(parameter, 'x') + std::string(parameter + 1, 'Y'));
        const auto b = rotations("xyxYXY");
        std::ofstream cases(argv[4]), summary(argv[5]);
        if (!cases || !summary) throw std::runtime_error("cannot open outputs");
        summary << "{\n";
        for (int length = first; length <= last; ++length) {
            Counts counts;
            std::string bridge;
            enumerate(length, bridge, p, b, counts, cases);
            if (length != first) summary << ",\n";
            summary << "  \"" << length << "\":";
            write_counts(summary, counts);
            std::cout << "length " << length << ": " << counts.sources << " sources and "
                      << counts.unresolved << " unresolved out of " << counts.tests << std::endl;
        }
        summary << "\n}\n";
        if (!cases || !summary) throw std::runtime_error("output failed");
    } catch (const std::exception& error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
