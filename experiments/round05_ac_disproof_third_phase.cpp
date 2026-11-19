// Finite continuation overgroups, followed by all two-copy joins.
#define main round02_two_copies_main
#include "round02_ac_disproof_two_copies.cpp"
#undef main
#include "u_native_primitive.hpp"

namespace {
const std::string alphabet = "xXyY";

Graph bridge_copies(const Graph& core, int a, int b, const std::string& bridge) {
    Graph graph = core;
    const int size = static_cast<int>(core.out.size());
    for (auto row : core.out) {
        for (auto& end : row)
            if (end >= 0) end += size;
        graph.out.push_back(row);
    }
    const int target = size + b;
    for (size_t i = 0; i < bridge.size(); ++i) {
        int end = i + 1 == bridge.size() ? target : add_vertex(graph);
        int label = letter(bridge[i]);
        if (graph.out[a][label] >= 0 || graph.out[end][label ^ 1] >= 0)
            throw std::runtime_error("unfolded connector");
        graph.out[a][label] = end;
        graph.out[end][label ^ 1] = a;
        a = end;
    }
    if (rank(graph) != 2 * rank(core))
        throw std::runtime_error("wrong connected-sum rank");
    return graph;
}

struct PhaseCounts {
    uint64_t roots = 0, clean_roots = 0, middle = 0, clean_middle = 0;
    uint64_t tests = 0, dag = 0, exact = 0, exact_states = 0, positives = 0, incomplete = 0;
};

struct Scanner {
    std::string root_word;
    std::ostream& exceptions;
    std::vector<PhaseCounts> counts;

    bool check(const Graph& graph, int a, int b, const std::string& connector, int i, int j) {
        auto& count = counts[connector.size()];
        ++count.tests;
        if (proves_primitive_absence(graph)) {
            ++count.dag;
            return true;
        }
        const auto result = u_native::decide(graph.out, 1'000'000);
        count.exact_states += result.pair_states;
        if (result.status == u_native::Status::ABSENT) {
            ++count.exact;
            return true;
        }
        const bool positive = result.status == u_native::Status::PRIMITIVE;
        if (positive) ++count.positives;
        else ++count.incomplete;
        exceptions << "{\"root\":" << root_word << ",\"middle\":[" << a << ',' << b
                   << ",\"" << connector << "\"],\"last\":[" << i << ',' << j
                   << "],\"status\":\"" << u_native::status_name(result.status) << '"';
        if (positive)
            exceptions << ",\"primitive\":\"" << result.witness.cyclic_word
                       << "\",\"program\":\"" << result.witness.program
                       << "\",\"alphabet\":\"" << result.witness.alphabet
                       << "\",\"component\":" << result.witness.component
                       << ",\"based_word\":\"" << result.witness.based_word
                       << "\",\"loop_vertex\":" << result.witness.vertex;
        exceptions << ",\"graph\":";
        graph_json(exceptions, graph);
        exceptions << "}\n";
        return false;
    }

    bool finish(const Graph& middle, int a, int b, const std::string& connector) {
        auto& count = counts[connector.size()];
        ++count.middle;
        bool clear = check(middle, a, b, connector, 0, 0);
        const int n = static_cast<int>(middle.out.size());
        for (int i = 0; i < n; ++i)
            for (int j = i + 1; j < n; ++j)
                if (!check(join(middle, i, j), a, b, connector, i, j))
                    clear = false;
        count.clean_middle += clear;
        return clear;
    }

    bool examine_bridge(const Graph& core, const std::string& connector) {
        bool clear = true;
        const int n = static_cast<int>(core.out.size());
        for (int a = 0; a < n; ++a) {
            if (core.out[a][letter(connector.front())] >= 0) continue;
            for (int b = a; b < n; ++b) {
                if (core.out[b][letter(inverse(connector.back()))] >= 0) continue;
                if (a == b && connector > inv(connector)) continue;
                if (!finish(bridge_copies(core, a, b, connector), a, b, connector))
                    clear = false;
            }
        }
        return clear;
    }

    bool bridges(const Graph& core, std::string& connector, int length) {
        if (length == 0) return examine_bridge(core, connector);
        bool clear = true;
        for (char label : alphabet) {
            if (!connector.empty() && label == inverse(connector.back())) continue;
            connector.push_back(label);
            if (!bridges(core, connector, length - 1)) clear = false;
            connector.pop_back();
        }
        return clear;
    }

    void scan(const Graph& core) {
        const int n = static_cast<int>(core.out.size());
        ++counts[0].roots;
        bool clear = finish(core, 0, 0, "");
        for (int a = 0; a < n; ++a)
            for (int b = a + 1; b < n; ++b)
                if (!finish(join(core, a, b), a, b, "")) clear = false;
        counts[0].clean_roots += clear;
        std::string connector;
        for (size_t length = 1; length < counts.size(); ++length) {
            ++counts[length].roots;
            counts[length].clean_roots += bridges(core, connector, static_cast<int>(length));
        }
    }
};

void report(std::ostream& out, const std::vector<PhaseCounts>& counts) {
    out << "{\n  \"by_middle_gap_length\":[\n";
    for (size_t i = 0; i < counts.size(); ++i) {
        const auto& r = counts[i];
        if (i) out << ",\n";
        out << "    {\"length\":" << i << ",\"first_sources\":" << r.roots
            << ",\"certified_first_sources\":" << r.clean_roots
            << ",\"middle_overgroups\":" << r.middle << ",\"certified_middle_overgroups\":" << r.clean_middle
            << ",\"final_graphs\":" << r.tests << ",\"DAG_excluded\":" << r.dag
            << ",\"exact_excluded\":" << r.exact << ",\"exact_pair_states\":" << r.exact_states
            << ",\"primitive_positives\":" << r.positives << ",\"incomplete\":" << r.incomplete << '}';
    }
    out << "\n  ]\n}\n";
}

Graph chain(const std::vector<std::string>& lobes, const std::string& links) {
    Graph core;
    int at = add_vertex(core);
    for (size_t i = 0; i < lobes.size(); ++i) {
        append_path(core, at, lobes[i], true);
        if (i < links.size()) at = append_path(core, at, links.substr(i, 1), false);
    }
    if (rank(core) != static_cast<int>(lobes.size())) throw std::runtime_error("wrong chain rank");
    return core;
}
}  // namespace

int main(int argc, char** argv) {
    try {
        if (argc != 4) throw std::runtime_error("usage: third_phase [rotation|short|four|five|ak2_barbell] middle_gap exceptions.jsonl");
        const std::string mode = argv[1];
        const int cap = std::stoi(argv[2]);
        if (cap < 0) throw std::runtime_error("negative middle gap cap");
        std::ofstream exceptions(argv[3]);
        if (!exceptions) throw std::runtime_error("cannot open exceptions output");
        Scanner scanner{"", exceptions, std::vector<PhaseCounts>(static_cast<size_t>(cap) + 1)};
        if (mode == "rotation" || mode == "short") {
            for (const auto& p : rotations("xxxYYYY")) for (const auto& b : rotations("xyxYXY")) {
                scanner.root_word = "[\"" + p + "\",\"" + b + "\"";
                if (mode == "rotation") {
                    scanner.root_word += "]";
                    scanner.scan(fold(p, b));
                } else {
                    auto label_pair = scanner.root_word;
                    for (char letter : alphabet) {
                        if (letter == p.front() || inverse(letter) == p.back()
                            || inverse(letter) == b.front() || letter == b.back()) continue;
                        std::string connector(1, letter);
                        scanner.root_word = label_pair + ",\"" + connector + "\"]";
                        scanner.scan(source(p, b, connector));
                    }
                }
            }
        } else if (mode == "four") {
            scanner.root_word = "[\"xxxYYYY\",\"XXXyyyy\",\"XXyyyyX\",\"xyxYXY\",\"Xyy\"]";
            scanner.scan(chain({"xxxYYYY", "XXXyyyy", "XXyyyyX", "xyxYXY"}, "Xyy"));
        } else if (mode == "five") {
            scanner.root_word = "[\"xxxYYYY\",\"XXXyyyy\",\"XXyyyyX\",\"xyxYXY\",\"YXYxyx\",\"XyyX\"]";
            scanner.scan(chain({"xxxYYYY", "XXXyyyy", "XXyyyyX", "xyxYXY", "YXYxyx"}, "XyyX"));
        } else if (mode == "ak2_barbell") {
            scanner.root_word = "[\"xYYYx\",\"yxYXYx\",\"y\"]";
            scanner.scan(source("xYYYx", "yxYXYx", "y"));
        } else {
            throw std::runtime_error("unknown source catalogue");
        }
        report(std::cout, scanner.counts);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
