// Enumerate the complete bounded middle product menu in each literal marking.
#define AC_ROUND05_ORBITS_LIBRARY
#include "round05_ak3_orbits.cpp"

#include <set>

int main(int argc, char** argv) {
    using namespace orbit_search;
    try {
        if (argc != 2) throw std::invalid_argument("usage: exact-center cyclic-cap < donor-receiver.tsv");
        const auto cap = std::stoi(argv[1]);
        Worker worker;
        uint64_t charts = 0, outputs = 0, too_long = 0;
        for (std::string fixed, changing; std::cin >> fixed >> changing;) {
            if (int(fixed.size()) + std::abs(int(fixed.size()) - int(changing.size())) > cap) {
                ++charts;
                ++too_long;
                continue;
            }
            if (fixed.empty() || changing.empty() || std::max(fixed.size(), changing.size()) > 31
                || cap < 2 || cap > 31 + int(std::min(fixed.size(), changing.size())))
                throw std::invalid_argument("invalid two-row menu");
            const auto a = word_code(fixed), b = word_code(changing);
            const auto fixed_key = build_orbit(a)[0];
            const auto changing_key = build_orbit(b)[0];
            std::set<Code> solutions;
            worker.scan_pair(a, b, cap, [&](const Orbit& output, const Orbit& donor) {
                if (donor[0] == fixed_key && output[0] != changing_key) solutions.insert(output[0]);
            });
            for (const auto& solution : solutions) std::cout << charts << '\t' << fixed << '\t'
                                                             << word(solution) << '\n';
            outputs += solutions.size();
            ++charts;
        }
        std::cerr << "{\"charts\":" << charts << ",\"candidate_products\":" << worker.candidates
                  << ",\"admitted_products\":" << worker.admitted << ",\"length_excluded_charts\":" << too_long << ",\"marked_outputs\":"
                  << outputs << "}\n";
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
