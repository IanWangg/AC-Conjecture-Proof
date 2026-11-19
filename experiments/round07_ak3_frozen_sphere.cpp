// Test for a primitive replacement while retaining one energy-18 donor.
#define AC_ROUND05_ORBITS_LIBRARY
#include "round05_ak3_orbits.cpp"

namespace frozen {
using namespace orbit_search;

Code literal(const std::string& word) { return build_orbit(word_code(word))[0]; }

void scan(const std::string& first, const std::string& second, int cap, unsigned radius) {
    const auto root = literal(first), fixed = literal(second);
    if (root == fixed || length(root) + length(fixed) > unsigned(cap) || cap - int(length(fixed)) > 31
            || primitive(word(root)) || primitive(word(fixed)))
        throw std::runtime_error("expected two distinct nonprimitive rows at a representable cyclic cap");
    std::unordered_set<Code> seen{root};
    std::vector<Code> frontier{root};
    Worker worker;
    uint64_t primitive_coordinates = 0;
    std::cout << "{\"recipient\":\"" << first << "\",\"frozen_donor\":\"" << second
              << "\",\"cyclic_cap\":" << cap << ",\"radius\":" << radius << ",\"layers\":[";
    for (unsigned i = 0; i < radius; ++i) {
        std::vector<Code> next;
        uint64_t before = worker.candidates;
        for (const auto current : frontier)
            worker.scan_pair(current, fixed, cap, [&](const auto& changed, const auto& donor) {
                if (donor[0] != fixed || !seen.insert(changed[0]).second) return;
                next.push_back(changed[0]);
                if (primitive(word(changed[0]))) {
                    std::cerr << "primitive receiver " << word(changed[0]) << " from " << word(current)
                              << " in layer " << i + 1 << '\n';
                    ++primitive_coordinates;
                }
            });
        if (i) std::cout << ',';
        std::cout << "{\"new_words\":" << next.size() << ",\"menu_candidates\":"
                  << worker.candidates - before << "}" << std::flush;
        frontier.swap(next);
    }
    std::cout << "],\"distinct_recipients\":" << seen.size()
              << ",\"primitive_recipients\":" << primitive_coordinates << "}";
}
}

int main(int argc, char** argv) {
    try {
        if (argc != 3) throw std::runtime_error("usage: frozen-sphere cap radius");
        const int cap = std::stoi(argv[1]);
        const unsigned radius = std::stoul(argv[2]);
        const std::string a = "xxxyxyXXy", b = "xxyXyXYxy";
        std::cout << "[\n  ";
        frozen::scan(a, b, cap, radius);
        std::cout << ",\n  ";
        frozen::scan(b, a, cap, radius);
        std::cout << "\n]\n";
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
