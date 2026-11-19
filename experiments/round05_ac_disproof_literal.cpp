// Three successive zero-gap join envelopes from the literal AK(3) core.
#define main round02_two_copies_main
#include "round02_ac_disproof_two_copies.cpp"
#undef main
#include "u_native_primitive.hpp"

namespace {
struct Stage {
    uint64_t graph_count = 0, dag = 0, exact = 0, positive = 0, incomplete = 0;
};

void visit(const Graph& graph, std::vector<Stage>& stages, size_t depth,
           std::vector<std::pair<int, int>>& path, std::ostream& exceptions) {
    auto& stage = stages[depth];
    ++stage.graph_count;
    if (proves_primitive_absence(graph)) {
        ++stage.dag;
    } else {
        const auto result = u_native::decide(graph.out, 1'000'000);
        if (result.status == u_native::Status::ABSENT) {
            ++stage.exact;
        } else {
            const bool positive = result.status == u_native::Status::PRIMITIVE;
            if (positive) ++stage.positive;
            else ++stage.incomplete;
            if (stage.positive + stage.incomplete <= 20) {
                exceptions << "{\"path\":[";
                for (size_t i = 0; i < path.size(); ++i) {
                    const auto [a, b] = path[i];
                    if (i) exceptions << ',';
                    exceptions << '[' << a << ',' << b << ']';
                }
                exceptions << "],\"status\":\"" << u_native::status_name(result.status) << '"';
                if (positive)
                    exceptions << ",\"primitive\":\"" << result.witness.cyclic_word
                               << "\",\"based_word\":\"" << result.witness.based_word << '"';
                exceptions << ",\"graph\":";
                graph_json(exceptions, graph);
                exceptions << "}\n";
            }
        }
    }
    if (depth + 1 == stages.size()) return;
    const int vertices = static_cast<int>(graph.out.size());
    for (int a = 0; a < vertices; ++a) {
        for (int b = a; b < vertices; ++b) {
            if (a == b && a) continue;
            path.emplace_back(a, b);
            if (a == b) visit(graph, stages, depth + 1, path, exceptions);
            else visit(join(graph, a, b), stages, depth + 1, path, exceptions);
            path.pop_back();
        }
    }
}
}

int main(int argc, char** argv) {
    try {
        if (argc != 2) throw std::runtime_error("usage: literal_depth_three exceptions.jsonl");
        std::ofstream exceptions(argv[1]);
        if (!exceptions) throw std::runtime_error("cannot open exceptions output");
        const auto graph = fold("xxxYYYY", "xyxYXY");
        std::vector<Stage> stages(4);
        std::vector<std::pair<int, int>> path;
        visit(graph, stages, 0, path, exceptions);
        std::cout << "{\"source_vertices\":" << graph.out.size() << ",\"stages\":[\n";
        for (size_t i = 0; i < stages.size(); ++i) {
            if (i) std::cout << ",\n";
            const auto& s = stages[i];
            std::cout << "{\"conjugation_phases\":" << i << ",\"graphs\":" << s.graph_count
                      << ",\"DAG_excluded\":" << s.dag << ",\"exact_excluded\":" << s.exact
                      << ",\"primitive_positives\":" << s.positive << ",\"incomplete\":" << s.incomplete << '}';
        }
        std::cout << "\n]}\n";
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
