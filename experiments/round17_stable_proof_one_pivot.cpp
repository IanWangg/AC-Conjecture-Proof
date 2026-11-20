// Close the one-auxiliary-occurrence tail of the strict Round 16 chart.
#define AC_ROUND16_PIVOT_LIBRARY
#include "round16_stable_proof_pivot.cpp"

int main(int argc, char** argv) {
    try {
        if (argc != 2 && argc != 3)
            throw std::runtime_error("usage: one-pivot32 roots.tsv [nodes.tsv]");
        constexpr int floor = 12;
        constexpr int cap = 32;
        Scanner scanner;
        std::vector<Key> nodes, neighbors;
        std::vector<size_t> parents;
        std::unordered_set<Key, KeyHash> seen;
        const auto append = [&](Key key, size_t parent) {
            if (!seen.insert(key).second) return;
            nodes.push_back(key);
            parents.push_back(parent);
        };
        import(argv[1], [&](Key key) { append(key, seed_parent); }, floor, cap);
        if (nodes.size() != 1) throw std::runtime_error("expected one starting chart");
        size_t releases = 0;
        for (size_t parent = 0; parent < nodes.size(); ++parent) {
            auto rows = ordered_rows(nodes[parent]);
            if (rows[0].size() == 1) {
                ++releases;
                continue;
            }
            if (count_z(rows[0]) != 1 || count_z(rows[1]) || count_z(rows[2])
                || rows[1].size() < 9 || rows[2].size() < 9
                || rows[1].size() + rows[2].size() < 20)
                throw std::logic_error("one-pivot support or width invariant failed");
            scanner.neighbors(nodes[parent], floor, cap, neighbors);
            for (const auto key : neighbors) append(key, parent);
        }
        if (argc == 3) {
            std::ofstream out(argv[2]);
            for (size_t i = 0; i < nodes.size(); ++i) {
                out << parents[i] << '\t';
                write_ordered(out, nodes[i]);
            }
            if (!out) throw std::runtime_error("failed to write catalogue");
        }
        std::cout << "{\"expanded\":" << nodes.size() - releases
                  << ",\"discovered\":" << nodes.size()
                  << ",\"returns\":" << releases << ",\"closed\":true}\n";
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
