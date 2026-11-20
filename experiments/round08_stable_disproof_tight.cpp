// Exact parity reachability for each tight crossing graph.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <utility>
#include <vector>

using Matrix = unsigned __int128;
using Edge = std::pair<unsigned, unsigned>;
using Moves = std::vector<Edge>;
constexpr unsigned rank = 9;
constexpr unsigned column_mask = (1U << rank) - 1;

constexpr Matrix diagonal(unsigned step) {
    Matrix result = 0;
    for (unsigned i = 0; i < rank; ++i) result |= Matrix(1) << (step * i);
    return result;
}

constexpr Matrix identity = diagonal(rank + 1);
constexpr Matrix stripes = diagonal(rank);

Matrix row_add(Matrix matrix, Edge move) {
    const auto [receiver, donor] = move;
    return matrix ^ (((matrix >> donor) & stripes) << receiver);
}

Matrix canonical_columns(Matrix matrix) {
    std::array<unsigned, rank> columns{};
    for (unsigned i = 0; i < columns.size(); ++i)
        columns[i] = (matrix >> (rank * i)) & column_mask;
    std::sort(columns.begin(), columns.end());
    Matrix canonical = 0;
    for (unsigned column : columns)
        canonical = (canonical << rank) | column;
    return canonical;
}

Moves edge_menu(Edge edge) {
    const auto [u, v] = edge;
    Moves moves;
    for (unsigned a = u == 0 ? 0 : u + 1; a <= u + 1; ++a) {
        for (unsigned b = v == 0 ? 0 : v + 1; b <= v + 1; ++b) {
            moves.emplace_back(a, b);
            moves.emplace_back(b, a);
        }
    }
    return moves;
}

using Layers = std::vector<std::vector<Matrix>>;

std::vector<Matrix> layer(const Layers& lower, const std::vector<Moves>& menus, unsigned mask) {
    std::vector<Matrix> result;
    std::size_t candidates = 0;
    for (unsigned remaining = mask; remaining; remaining &= remaining - 1) {
        const unsigned edge = __builtin_ctz(remaining);
        candidates += lower[mask ^ (1U << edge)].size() * menus[edge].size();
    }
    result.reserve(candidates);
    for (unsigned remaining = mask; remaining; remaining &= remaining - 1) {
        const unsigned edge = __builtin_ctz(remaining);
        for (Matrix previous : lower[mask ^ (1U << edge)]) {
            for (Edge move : menus[edge])
                result.push_back(row_add(previous, move));
        }
    }
    std::sort(result.begin(), result.end());
    result.erase(std::unique(result.begin(), result.end()), result.end());
    return result;
}

Moves trace(const Layers& lower, const std::vector<Moves>& menus, unsigned mask, Matrix matrix) {
    Moves reverse;
    while (mask) {
        bool found = false;
        for (unsigned remaining = mask; remaining && !found; remaining &= remaining - 1) {
            const unsigned edge = __builtin_ctz(remaining), next_mask = mask ^ (1U << edge);
            const auto& predecessors = lower[next_mask];
            for (Edge move : menus[edge]) {
                const Matrix previous = row_add(matrix, move);
                if (!std::binary_search(predecessors.begin(), predecessors.end(), previous))
                    continue;
                reverse.push_back(move);
                matrix = previous;
                mask = next_mask;
                found = true;
                break;
            }
        }
        if (!found) throw std::runtime_error("trace needs a predecessor");
    }
    std::reverse(reverse.begin(), reverse.end());
    return reverse;
}

void print_moves(const Moves& moves) {
    std::cout << '[';
    for (unsigned index = 0; index < moves.size(); ++index) {
        if (index) std::cout << ',';
        const auto [receiver, donor] = moves[index];
        std::cout << '[' << receiver << ',' << donor << ']';
    }
    std::cout << ']';
}

void check(const std::vector<Edge>& edges) {
    const unsigned all = (1U << edges.size()) - 1;
    const unsigned left_radius = edges.size() / 2, right_radius = edges.size() - left_radius;
    std::vector<Moves> menus;
    for (auto edge : edges) menus.push_back(edge_menu(edge));
    Layers lower(all + 1);
    lower[0] = {identity};
    for (unsigned mask = 1; mask <= all; ++mask)
        if (__builtin_popcount(mask) <= left_radius)
            lower[mask] = layer(lower, menus, mask);

    std::uint64_t prefix_count = 0, inverse_suffix_count = 0, matches = 0;
    Moves witness;
    for (unsigned mask = 1; mask <= all; ++mask) {
        if (__builtin_popcount(mask) != left_radius) continue;
        const auto& prefixes = lower[mask];
        const unsigned right = all ^ mask;
        const auto inverse_suffixes = right_radius > left_radius ? layer(lower, menus, right) : lower[right];
        prefix_count += prefixes.size();
        inverse_suffix_count += inverse_suffixes.size();

        // Right multiplication by I+E_10 adds column 1 into column 0.
        std::vector<std::pair<Matrix, Matrix>> keys;
        keys.reserve(prefixes.size());
        for (Matrix matrix : prefixes)
            keys.emplace_back(canonical_columns(matrix ^ ((matrix >> rank) & column_mask)), matrix);
        std::sort(keys.begin(), keys.end());
        for (Matrix matrix : inverse_suffixes) {
            const Matrix target = canonical_columns(matrix);
            auto candidate = std::lower_bound(keys.begin(), keys.end(), std::pair{target, Matrix(0)});
            for (; candidate != keys.end() && candidate->first == target; ++candidate) {
                ++matches;
                if (witness.empty()) {
                    witness = trace(lower, menus, mask, candidate->second);
                    const auto suffix = trace(lower, menus, right, matrix);
                    witness.insert(witness.end(), suffix.rbegin(), suffix.rend());
                }
            }
        }
    }
    std::cout << "{\"edges\":";
    print_moves(edges);
    std::cout << ",\"prefix_matrices\":" << prefix_count << ",\"inverse_suffix_matrices\":" << inverse_suffix_count
              << ",\"matching_matrix_pairs\":" << matches << ",\"witness\":";
    print_moves(witness);
    std::cout << "}\n" << std::flush;
}

int main(int argc, char** argv) {
    try {
        if (argc != 2) throw std::runtime_error("usage: tight input_graphs");
        std::ifstream input(argv[1]);
        if (!input) throw std::runtime_error("cannot open graph list");
        unsigned count;
        while (input >> count) {
            if (count != 9 && count != 11 && count != 12)
                throw std::runtime_error("only tight 5-, 6- or 7-padding graphs supported");
            std::vector<Edge> edges(count);
            for (auto& [u, v] : edges)
                if (!(input >> u >> v) || u >= v || v >= rank - 1)
                    throw std::runtime_error("invalid edge");
            check(edges);
        }
        if (!input.eof()) throw std::runtime_error("invalid graph list");
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
