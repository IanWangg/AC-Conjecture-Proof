// Two-copy joined cores for all one-letter chains of three AK(3) lobes.
#define main round02_two_copies_main
#include "round02_ac_disproof_two_copies.cpp"
#undef main

#include <set>

namespace {
bool admissible_chain(const std::string& left, const std::string& middle,
                      const std::string& right, char first, char last) {
    return first != left.front() && first != inverse(left.back())
        && inverse(last) != right.front() && last != right.back()
        && std::set<char>{middle.front(), inverse(middle.back()), inverse(first), last}.size() == 4;
}

void check_chain(const std::string& left, const std::string& middle,
                 const std::string& right, char first, char last, Counts& counts) {
    Graph core;
    add_vertex(core);
    append_path(core, 0, left, true);
    const int center = append_path(core, 0, std::string(1, first), false);
    append_path(core, center, middle, true);
    const int end = append_path(core, center, std::string(1, last), false);
    append_path(core, end, right, true);
    if (rank(core) != 3 || !proves_primitive_absence(core))
        throw std::runtime_error("uncertified three-lobe source");
    ++counts.sources;
    const int n = static_cast<int>(core.out.size());
    for (int a = 0; a < n; ++a) {
        for (int b = a + 1; b < n; ++b) {
            const auto graph = join(core, a, b);
            ++counts.tests;
            ++counts.ranks[rank(graph)];
            if (!proves_primitive_absence(graph))
                throw std::runtime_error("uncertified three-lobe join");
            ++counts.dag_exclusions;
        }
    }
}
}

int main() {
    try {
        const auto power = rotations("xxxYYYY");
        const auto braid = rotations("xyxYXY");
        auto centers = power;
        centers.insert(centers.end(), braid.begin(), braid.end());
        for (std::size_t i = 0, unsigned_count = centers.size(); i < unsigned_count; ++i)
            centers.push_back(inv(centers[i]));
        Counts counts;
        for (const auto& left : power)
            for (const auto& right : braid)
                for (const auto& middle : centers)
                    for (char first : std::string("xXyY"))
                        for (char last : std::string("xXyY"))
                            if (admissible_chain(left, middle, right, first, last))
                                check_chain(left, middle, right, first, last, counts);
        write_counts(std::cout, counts);
        std::cout << '\n';
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
    return 0;
}
