// Test given marked receivers in every completed fixed-donor chart.
#define AC_ROUND08_ACM_LIBRARY
#include "round08_ak3_acm.cpp"
#include <set>

int main(int argc, char** argv) {
    try {
        using namespace acm08;
        if (argc != 5) throw std::invalid_argument("usage: targeted-acm receiver donor depth allocation_cap < words");
        const auto receiver = std::string(argv[1]);
        const auto donor = std::string(argv[2]);
        const auto depth = std::stoul(argv[3]);
        const auto cap = std::stoul(argv[4]);
        if (receiver.empty() || donor.empty() || cyclic(receiver) != receiver || cyclic(donor) != donor ||
            std::abs(determinant(abel(receiver), abel(donor))) != 1)
            throw std::invalid_argument("expected a cyclic pair with unimodular exponents");
        std::set<std::string> pending;
        for (std::string word; std::cin >> word;) {
            if (word.empty() || cyclic(word) != word || std::abs(determinant(abel(word), abel(donor))) != 1)
                throw std::invalid_argument("invalid target word " + word);
            pending.insert(word);
        }
        Folding folding(cap);
        folding.add_loop(0, receiver);
        const auto donor_rotations = variants(donor);
        std::vector<size_t> sizes;
        std::vector<std::pair<std::string, unsigned>> hits;
        bool allocation_stop = false;
        for (unsigned stage = 0; stage <= depth; ++stage) {
            if (stage) {
                const auto vertices = folding.vertices();
                try {
                    for (int vertex : vertices)
                        for (const auto& rotation : donor_rotations) folding.add_loop(vertex, rotation);
                } catch (const SizeLimit&) {
                    allocation_stop = true;
                    break;
                }
            }
            const auto graph = folding.compact();
            sizes.push_back(graph.size());
            for (auto at = pending.begin(); at != pending.end();) {
                if (present(graph, *at)) {
                    hits.emplace_back(*at, stage);
                    at = pending.erase(at);
                } else {
                    ++at;
                }
            }
            if (pending.empty()) break;
        }
        std::cout << "{\"graph_sizes\":[";
        for (size_t i = 0; i < sizes.size(); ++i) std::cout << (i ? "," : "") << sizes[i];
        std::cout << "],\"allocation_stop\":" << (allocation_stop ? "true" : "false") << ",\"hits\":[";
        for (size_t i = 0; i < hits.size(); ++i)
            std::cout << (i ? "," : "") << "[\"" << hits[i].first << "\"," << hits[i].second << ']';
        std::cout << "]}\n";
    } catch (const acm08::SizeLimit&) {
        std::cerr << "allocation limit does not fit the initial receiver\n";
        return 1;
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
