// Joint Whitehead descent between cyclic rank-three products.
#define AC_ROUND11_REVERSE_LIBRARY
#include "round11_stable_proof_reverse.cpp"
#define AC_ROUND09_PRIMITIVE_REUSE
#include "round09_stable_proof_primitive_catalogue.cpp"

namespace {
struct Cut {
    unsigned multiplier;
    unsigned side;
    Mark mark;
};

std::vector<Cut> all_cuts() {
    std::vector<Cut> cuts;
    for (unsigned m = 0; m < alphabet.size(); ++m)
        for (unsigned side = 1; side < 63; ++side) {
            if (!(side & (1U << m)) || (side & (1U << opposite(m)))) continue;
            auto map = identity_mark();
            for (unsigned i = 0; i < alphabet.size(); ++i) {
                if (i == m || i == opposite(m)) continue;
                if (side & (1U << i)) map[i].insert(map[i].begin(), alphabet[m]);
                if (side & (1U << opposite(i))) map[i].push_back(alphabet[opposite(m)]);
            }
            cuts.push_back({m, side, std::move(map)});
        }
    return cuts;
}

class JointDescent {
    CompactOrbits& cache;
    const std::vector<Cut> cuts = all_cuts();
    std::unordered_map<Key, Key, KeyHash> reduced;
public:
    explicit JointDescent(CompactOrbits& cache) : cache(cache) {}

    Key minimize(Key input) {
        std::vector<Key> path;
        auto current = input;
        for (;;) {
            if (const auto it = reduced.find(current); it != reduced.end()) {
                current = it->second;
                break;
            }
            path.push_back(current);
            const auto rows = rows_from(current);
            std::array<std::array<int, 6>, 6> edges{};
            std::array<int, 6> degrees{};
            for (const auto& word : rows)
                for (size_t i = 0; i < word.size(); ++i) {
                    const auto a = opposite(unsigned(alphabet.find(word[i])));
                    const auto b = unsigned(alphabet.find(word[(i + 1) % word.size()]));
                    ++edges[std::min(a, b)][std::max(a, b)];
                    ++degrees[a];
                    ++degrees[b];
                }
            int least = 0;
            const Cut* best = nullptr;
            for (const auto& cut : cuts) {
                int delta = -degrees[cut.multiplier];
                for (unsigned a = 0; a < alphabet.size(); ++a)
                    for (unsigned b = a + 1; b < alphabet.size(); ++b)
                        if (((cut.side >> a) ^ (cut.side >> b)) & 1) delta += edges[a][b];
                if (delta < least) {
                    least = delta;
                    best = &cut;
                }
            }
            if (!best) break;
            Triple child;
            for (unsigned i = 0; i < 3; ++i) child[i] = canonical(image(rows[i], best->mark));
            if (int(energy(child)) != int(energy(rows)) + least)
                throw std::logic_error("joint Whitehead cut length disagreement");
            if (!in_range(child, 3, int(energy(rows))))
                return input; // Skip a descent incompatible with the packed coordinate width.
            cache.limit();
            current = signed_key(cache, child);
        }
        for (auto key : path) reduced.emplace(key, current);
        return current;
    }
};

using Projection = std::array<std::string, 2>;

std::optional<Projection> primitive_projection(
    const Triple& rows, std::unordered_map<Code, std::optional<Mark>>& charts,
    std::set<Projection>& projected, std::ofstream& out, const std::array<Key, 2>& ancestry) {
    for (size_t pivot = 0; pivot < 3; ++pivot) {
        const auto [it, fresh] = charts.try_emplace(encode(rows[pivot]));
        if (fresh) it->second = quotient(rows[pivot]);
        if (!it->second) continue;
        const auto& mark = *it->second;
        Projection p{canonical(image(rows[(pivot + 1) % 3], mark)),
                     canonical(image(rows[(pivot + 2) % 3], mark))};
        if (p[0].empty() || p[1].empty()) throw std::logic_error("trivial projected row");
        std::sort(p.begin(), p.end());
        if (projected.insert(p).second) {
            out << p[0] << '\t' << p[1] << '\t';
            for (auto key : ancestry)
                for (const auto& row : rows_from(key)) out << row << '\t';
            out << pivot << '\n';
        }
        if (primitive_rank_two(p[0]) || primitive_rank_two(p[1])) return p;
    }
    return std::nullopt;
}

void emit(std::ostream& out, Key key) {
    const auto rows = rows_from(key);
    out << rows[0] << '\t' << rows[1] << '\t' << rows[2];
}

int run(int product_cap, int beam_cap, unsigned levels, size_t width, const Triple& start,
        const std::string& prefix) {
    if (!in_range(start, 3, product_cap) || product_cap > 36 || beam_cap > product_cap || !width || !levels)
        throw std::invalid_argument("invalid search bounds or root");
    Scanner scanner;
    JointDescent descent(scanner.orbits);
    std::unordered_map<Code, std::optional<Mark>> charts;
    std::unordered_map<Key, size_t, KeyHash> visited;
    std::unordered_set<Key, KeyHash> checked_products;
    std::set<Projection> distinct_projections;
    std::ofstream projection_file(prefix + ".pairs.tsv"), edge_file(prefix + ".edges.tsv");
    if (!projection_file || !edge_file) throw std::runtime_error("cannot write results");

    const Key raw_root = signed_key(scanner.orbits, start), root = descent.minimize(raw_root);
    visited.emplace(root, energy(rows_from(root)));
    emit(edge_file, root);
    edge_file << '\t';
    emit(edge_file, raw_root);
    edge_file << '\n';
    std::vector<Key> frontier{root}, successors;
    std::optional<std::array<Key, 2>> winner;
    std::vector<std::array<size_t, 4>> layer_stats;
    for (unsigned depth = 1; depth <= levels && !frontier.empty() && !winner; ++depth) {
        std::vector<Key> next;
        const auto checked_before = checked_products.size(), projected_before = distinct_projections.size();
        const auto expansions = frontier.size();
        for (auto parent : frontier) {
            const auto local_cap = std::min(product_cap, int(visited.at(parent)) + 5);
            scanner.neighbors(parent, 3, local_cap, successors);
            for (auto raw : successors) {
                if (checked_products.insert(raw).second) {
                    if (primitive_projection(rows_from(raw), charts, distinct_projections,
                                             projection_file, {parent, raw})) {
                        winner = {parent, raw};
                        break;
                    }
                }
                const auto reduced = descent.minimize(raw);
                const auto length = energy(rows_from(reduced));
                if (int(length) > beam_cap ||
                    !visited.try_emplace(reduced, length).second) continue;
                next.push_back(reduced);
                emit(edge_file, reduced);
                edge_file << '\t';
                emit(edge_file, parent);
                edge_file << '\t';
                emit(edge_file, raw);
                edge_file << '\n';
            }
            if (winner) break;
        }
        layer_stats.push_back({expansions, checked_products.size() - checked_before,
                               distinct_projections.size() - projected_before, next.size()});
        std::sort(next.begin(), next.end(), [&](Key a, Key b) {
            return std::make_pair(visited.at(a), a) < std::make_pair(visited.at(b), b);
        });
        if (next.size() > width) next.resize(width);
        frontier = std::move(next);
        std::cerr << "layer " << depth << " examined " << checked_products.size() << " product orbits\n";
    }
    if (winner) {
        std::ofstream hit(prefix + ".hit.tsv");
        for (auto key : *winner) write_tsv(hit, rows_from(key));
    }
    std::cout << "{\n  \"product_cap\":" << product_cap << ",\n  \"beam_cap\":" << beam_cap
              << ",\n  \"product_energy_slack\":5"
              << ",\n  \"beam_width\":" << width << ",\n  \"root_energy\":" << energy(rows_from(root))
              << ",\n  \"layer_stats_expansions_products_projections_new\":[";
    for (size_t i = 0; i < layer_stats.size(); ++i) {
        if (i) std::cout << ',';
        const auto [a,b,c,d] = layer_stats[i];
        std::cout << '[' << a << ',' << b << ',' << c << ',' << d << ']';
    }
    std::cout << "],\n  \"product_candidates\":" << scanner.candidates
              << ",\n  \"width_omissions\":" << scanner.outside_word_width
              << ",\n  \"visited_representatives\":" << visited.size()
              << ",\n  \"exact_distinct_products\":" << checked_products.size()
              << ",\n  \"exact_distinct_marked_projections\":" << distinct_projections.size()
              << ",\n  \"primitive_projection_hit\":" << (winner ? "true" : "false") << "\n}\n";
    return 0;
}
}

int main(int argc, char** argv) {
    try {
        if (argc != 9) throw std::runtime_error("usage: whitehead product-cap beam-cap levels width r1 r2 r3 prefix");
        return run(std::stoi(argv[1]), std::stoi(argv[2]), std::stoul(argv[3]), std::stoull(argv[4]),
                   {canonical(argv[5]),canonical(argv[6]),canonical(argv[7])},argv[8]);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
