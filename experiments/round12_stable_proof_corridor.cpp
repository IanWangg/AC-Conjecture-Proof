// Explore excursions that pass through rank-three tuples without any primitive row.
#define AC_ROUND11_REVERSE_LIBRARY
#include "round11_stable_proof_reverse.cpp"
#define AC_ROUND09_PRIMITIVE_REUSE
#include "round09_stable_proof_primitive_catalogue.cpp"

#include <queue>

namespace {
struct Point {
    Key key;
    size_t parent;
    unsigned primitive_rows;
};

using Projection = std::array<std::string, 2>;
constexpr auto initial_parent = std::numeric_limits<size_t>::max();

Projection signed_projection(const std::string& a, const std::string& b) {
    Projection best{"~", "~"};
    for (const auto& action : actions) {
        if (std::tolower(action[2]) != 'z') continue;
        auto translate = [&](std::string word) {
            for (auto& c : word) c = action[alphabet.find(c)];
            return canonical(std::move(word));
        };
        Projection marked{translate(a), translate(b)};
        std::sort(marked.begin(), marked.end());
        best = std::min(best, marked);
    }
    return best;
}

struct Candidate {
    size_t parent;
    Key key;
};

class Corridor {
    Scanner menu;
    std::unordered_map<Code, std::optional<Mark>> cached_charts;
    std::unordered_map<Key, size_t, KeyHash> seen;
    std::unordered_set<Key, KeyHash> exits;
    std::map<Projection, Candidate> projections;
    std::vector<Point> reached;
    std::priority_queue<std::pair<unsigned, size_t>, std::vector<std::pair<unsigned, size_t>>,
                        std::greater<>> queue;
    std::vector<Key> neighbors;
    int floor, cap;
    size_t expanded = 0, chartless_seed_count = 0, first_layer = 0;
    std::optional<Candidate> primitive_join;

    const std::optional<Mark>& chart(std::string const& word) {
        const auto [entry, fresh] = cached_charts.try_emplace(encode(word));
        if (fresh) entry->second = quotient(word);
        return entry->second;
    }

    unsigned pivot_count(const Triple& rows) {
        unsigned total = 0;
        for (const auto& row : rows) total += chart(row).has_value();
        return total;
    }

    size_t append(Key key, size_t parent, unsigned count, unsigned length) {
        const size_t index = reached.size();
        const auto [entry, fresh] = seen.try_emplace(key, index);
        if (!fresh) return entry->second;
        reached.push_back({key, parent, count});
        if (!count) queue.emplace(length, index);
        return index;
    }

    void record_exit(Key key, size_t parent, const Triple& rows) {
        if (!exits.insert(key).second) return;
        for (size_t i = 0; i < 3; ++i) {
            const auto& projection = chart(rows[i]);
            if (!projection) continue;
            auto a = canonical(image(rows[(i + 1) % 3], *projection));
            auto b = canonical(image(rows[(i + 2) % 3], *projection));
            if (a.empty() || b.empty()) throw std::logic_error("vanishing quotient coordinate");
            const auto pair = signed_projection(a, b);
            projections.try_emplace(pair, Candidate{parent, key});
            if (!primitive_join && (primitive_rank_two(a) || primitive_rank_two(b)))
                primitive_join = Candidate{parent, key};
        }
    }

    void export_route(std::ostream& stream, size_t last) const {
        std::vector<Key> route;
        for (size_t index = last; index != initial_parent; index = reached[index].parent)
            route.push_back(reached[index].key);
        for (auto it = route.rbegin(); it != route.rend(); ++it)
            write_tsv(stream, rows_from(*it));
    }

public:
    Corridor(int floor, int cap) : floor(floor), cap(cap) {
        if (floor < 3 || floor > cap || cap > 38) throw std::invalid_argument("invalid energy interval");
    }

    void run(const Triple& source, size_t budget, const std::string& output) {
        if (!in_range(source, floor, cap)) throw std::invalid_argument("source outside energy interval");
        const auto root = signed_key(menu.orbits, source);
        const auto root_pivots = pivot_count(rows_from(root));
        append(root, initial_parent, root_pivots, energy(source));
        if (root_pivots > 2) throw std::invalid_argument("three primitive rows cannot vanish in two products");

        if (root_pivots == 2) {
            menu.neighbors(root, floor, cap, neighbors);
            for (auto key : neighbors) {
                const auto next = rows_from(key);
                const auto count = pivot_count(next);
                if (!count) throw std::logic_error("one product changed two primitive rows");
                if (count == 1) append(key, 0, count, energy(next));
            }
            first_layer = reached.size() - 1;
        }
        if (root_pivots) {
            const auto end = reached.size();
            for (size_t parent = root_pivots == 2 ? 1 : 0; parent < end; ++parent) {
                menu.neighbors(reached[parent].key, floor, cap, neighbors);
                for (auto key : neighbors) {
                    const auto next = rows_from(key);
                    if (!pivot_count(next)) append(key, parent, 0, energy(next));
                }
            }
            chartless_seed_count = reached.size() - end;
        } else {
            chartless_seed_count = 1;
        }

        while (expanded < budget && !queue.empty() && !primitive_join) {
            const size_t parent = queue.top().second;
            queue.pop();
            ++expanded;
            menu.neighbors(reached[parent].key, floor, cap, neighbors);
            for (auto key : neighbors) {
                const auto next = rows_from(key);
                if (pivot_count(next)) record_exit(key, parent, next);
                else append(key, parent, 0, energy(next));
            }
        }

        std::ofstream nodes(output + ".nodes.tsv"), pairs(output + ".pairs.tsv"), route(output + ".route.tsv");
        if (!nodes || !pairs || !route) throw std::runtime_error("cannot write corridor outputs");
        for (const auto& point : reached) {
            nodes << point.parent << '\t' << point.primitive_rows << '\t';
            write_tsv(nodes, rows_from(point.key));
        }
        for (const auto& [pair, witness] : projections) {
            pairs << pair[0] << '\t' << pair[1] << '\t' << witness.parent << '\t';
            write_tsv(pairs, rows_from(witness.key));
        }
        if (primitive_join) {
            export_route(route, primitive_join->parent);
            write_tsv(route, rows_from(primitive_join->key));
        }
        const auto best = std::min_element(reached.begin(), reached.end(), [](auto a, auto b) {
            const auto ea = energy(rows_from(a.key)), eb = energy(rows_from(b.key));
            return std::make_tuple(a.primitive_rows != 0, ea, a.key)
                 < std::make_tuple(b.primitive_rows != 0, eb, b.key);
        });
        std::ofstream nearest(output + ".chartless.tsv");
        if (best != reached.end() && !best->primitive_rows)
            export_route(nearest, size_t(best - reached.begin()));
        std::cout << "{\n  \"floor\":" << floor << ", \"cap\":" << cap
                  << ", \"root_pivots\":" << root_pivots
                  << ",\n  \"one_product_one_pivot\":" << first_layer
                  << ", \"chartless_seeds\":" << chartless_seed_count
                  << ",\n  \"chartless_expanded\":" << expanded
                  << ", \"chartless_discovered\":" << reached.size() - first_layer - (root_pivots != 0)
                  << ",\n  \"exit_orbits\":" << exits.size()
                  << ", \"signed_projections\":" << projections.size()
                  << ",\n  \"candidates\":" << menu.candidates
                  << ", \"positive_bridge_candidates\":" << menu.nonempty
                  << ", \"admitted_products\":" << menu.admitted
                  << ", \"products_above_word_width\":" << menu.outside_word_width
                  << ",\n  \"closed\":" << (queue.empty() ? "true" : "false")
                  << ", \"primitive_projection_hit\":" << (primitive_join ? "true" : "false") << "\n}\n";
    }
};
}

int main(int argc, char** argv) {
    try {
        if (argc != 8) throw std::runtime_error("usage: corridor floor cap budget r1 r2 r3 prefix");
        Corridor scanner(std::stoi(argv[1]), std::stoi(argv[2]));
        Triple source{canonical(argv[4]), canonical(argv[5]), canonical(argv[6])};
        scanner.run(source, std::stoull(argv[3]), argv[7]);
        return 0;
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
