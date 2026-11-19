// Exhaust parity schedules at the minimum possible number of crossing products.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <unordered_map>
#include <vector>

using Word = std::uint64_t;

struct Product {
    int recipient, donor;
    Word cuts;
};

class Search {
    const int padding, rank, budget, left_radius, right_radius;
    const Word row_mask;
    std::vector<Product> menu;
    std::unordered_multimap<Word, Word> prefixes;
    std::array<int, 6> target{};
    Word target_patterns = 0, target_weight = 0, forward_leaves = 0, backward_leaves = 0;
    Word parity_matches = 0, weighted_matches = 0, valid_cuts = 0;

    Word move(Word state, const Product& product) const {
        return state ^ (((state >> (rank * product.donor)) & row_mask) << (rank * product.recipient));
    }

    void forward(Word state, Word cuts, int depth) {
        if (depth == left_radius) {
            prefixes.emplace(state, cuts);
            ++forward_leaves;
            return;
        }
        for (const auto& product : menu)
            forward(move(state, product), cuts + product.cuts, depth + 1);
    }

    void backward(Word state, Word cuts, int depth) {
        if (depth < right_radius) {
            for (const auto& product : menu)
                backward(move(state, product), cuts + product.cuts, depth + 1);
            return;
        }
        ++backward_leaves;
        const auto [begin, end] = prefixes.equal_range(state);
        for (auto it = begin; it != end; ++it) {
            ++parity_matches;
            weighted_matches += target_weight;
            const Word total = it->second + cuts;
            if (every_cut_has_three_edges(total)) ++valid_cuts;
        }
    }

    bool every_cut_has_three_edges(Word counts) const {
        for (unsigned part = 1; part < (1U << padding); ++part)
            if (((counts >> (4 * (part - 1))) & 15U) < 3) return false;
        return true;
    }

    Word orbit_size_if_representative() const {
        std::array<int, 6> labels{}, conjugate{};
        std::iota(labels.begin(), labels.end(), 0);
        Word scanned = 0, fixed = 0;
        do {
            for (int i = 0; i < rank; ++i) conjugate[labels[i]] = labels[target[i]];
            if (conjugate < target) return 0;
            ++scanned;
            if (conjugate == target) ++fixed;
        } while (std::next_permutation(labels.begin() + 2, labels.begin() + rank));
        return scanned / fixed;
    }

public:
    explicit Search(int k)
        : padding(k), rank(k + 2), budget((3 * (k + 1) + 1) / 2),
          left_radius(budget / 2), right_radius(budget - left_radius),
          row_mask((Word(1) << rank) - 1) {
        for (int i = 0; i < rank; ++i)
            for (int j = 0; j < rank; ++j)
                if (i != j && (i >= 2 || j >= 2)) {
                    Word cuts = 0;
                    for (unsigned part = 1; part < (1U << padding); ++part) {
                        const unsigned block = part << 2;
                        if (((block >> i) ^ (block >> j)) & 1U)
                            cuts |= Word(1) << (4 * (part - 1));
                    }
                    menu.push_back({i, j, cuts});
                }
    }

    void run() {
        Word start = 0;
        for (int i = 0; i < rank; ++i) start |= Word(1) << (rank * i + i);
        std::size_t estimate = 1;
        for (int i = 0; i < left_radius; ++i) estimate *= menu.size();
        prefixes.reserve(estimate);
        forward(start, 0, 0);
        std::iota(target.begin(), target.begin() + rank, 0);
        do {
            target_weight = orbit_size_if_representative();
            if (!target_weight) continue;
            ++target_patterns;
            Word end = 0;
            for (int i = 0; i < rank; ++i) {
                const int label = target[i];
                const Word row = label == 1 ? Word(3) : Word(1) << label;
                end |= row << (rank * i);
            }
            backward(end, 0, 0);
        } while (std::next_permutation(target.begin(), target.begin() + rank));
        std::cout << "{\"padding\":" << padding << ",\"crossing_budget\":" << budget
                  << ",\"target_patterns\":" << target_patterns
                  << ",\"forward_leaves\":" << forward_leaves
                  << ",\"backward_leaves\":" << backward_leaves
                  << ",\"parity_matches\":" << parity_matches
                  << ",\"parity_matches_all_target_orders\":" << weighted_matches
                  << ",\"all_cuts_at_least_three\":" << valid_cuts << "}\n";
    }
};

int main(int argc, char** argv) {
    if (argc != 2) {
        std::cerr << "usage: incidence padding\n";
        return 1;
    }
    try {
        const int k = std::stoi(argv[1]);
        if (k < 1 || k > 4) throw std::runtime_error("padding must be in [1,4]");
        Search(k).run();
    } catch (const std::exception& error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
