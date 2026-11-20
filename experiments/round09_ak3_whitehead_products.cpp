// Probe ordinary trajectories by complete product menus at minimal ambient markings.
#define AC_ROUND05_ORBITS_LIBRARY
#include "round05_ak3_orbits.cpp"
#include "round06_ak3_wide_pair.hpp"

#include <set>

namespace whitehead_products {
using namespace orbit_search;
using ak3_wide::Pair;
using ak3_wide::Hash;

unsigned energy(const Pair& pair) { return length(pair.first) + length(pair.second); }
Pair key(const std::string& a, const std::string& b) {
    return ak3_wide::least_image(build_orbit(word_code(a)), build_orbit(word_code(b)));
}

std::string replace(const std::string& row, char generator, const std::string& substitution) {
    std::string result;
    const auto negative = inverse(substitution);
    for (char letter : row) {
        if (letter == generator) result += substitution;
        else if (letter == invchar(generator)) result += negative;
        else result += letter;
    }
    return cyclic(result);
}

std::vector<Pair> transvections(const Pair& pair) {
    const auto left = word(pair.first), right = word(pair.second);
    const auto cap = energy(pair);
    std::vector<Pair> results;
    for (char generator : std::string_view("xy")) {
        const char other = generator == 'x' ? 'y' : 'x';
        for (char sign : {other, invchar(other)})
            for (const std::string& substitution : {std::string{generator, sign}, std::string{sign, generator}}) {
                const auto a = replace(left, generator, substitution), b = replace(right, generator, substitution);
                if (a.size() + b.size() > cap) continue;
                if (a.empty() || b.empty() || a.size() > 31 || b.size() > 31)
                    throw std::runtime_error("Whitehead successor outside packed range");
                results.push_back(key(a, b));
            }
    }
    std::sort(results.begin(), results.end());
    results.erase(std::unique(results.begin(), results.end()), results.end());
    return results;
}

bool ordered(const Pair& a, const Pair& b) {
    return std::make_pair(energy(a), a) < std::make_pair(energy(b), b);
}

class Minima {
    std::unordered_map<Pair, Pair, Hash> reduced;
    std::unordered_map<Pair, std::set<Pair>, Hash> plateau;

public:
    Pair canonical(Pair start) {
        if (const auto found = reduced.find(start); found != reduced.end()) return found->second;
        std::vector<Pair> descent;
        auto current = start;
        Pair result;
        for (;;) {
            if (const auto found = reduced.find(current); found != reduced.end()) {
                result = found->second;
                break;
            }
            descent.push_back(current);
            const auto moves = transvections(current);
            const auto best = std::min_element(moves.begin(), moves.end(), ordered);
            if (best == moves.end() || energy(*best) == energy(current)) {
                std::set<Pair> marks{current};
                std::vector<Pair> queue{current};
                for (size_t at = 0; at < queue.size(); ++at)
                    for (const auto& next : transvections(queue[at])) {
                        if (energy(next) != energy(current)) throw std::logic_error("descent from a minimum");
                        if (marks.insert(next).second) queue.push_back(next);
                    }
                result = *marks.begin();
                for (const auto& mark : marks) reduced.emplace(mark, result);
                plateau.emplace(result, std::move(marks));
                break;
            }
            current = *best;
        }
        for (const auto& pair : descent) reduced.emplace(pair, result);
        return result;
    }

    const auto& marks(const Pair& pair) const { return plateau.at(pair); }
};

void print(std::ostream& out, const Pair& pair) {
    out << word(pair.first) << '\t' << word(pair.second);
}

bool primitive_pair(const Pair& pair) { return primitive(word(pair.first)) || primitive(word(pair.second)); }

struct Witness {
    Pair parent;
    Pair source;
    Pair product;
};

int run(unsigned peak, unsigned threshold, unsigned depth, size_t beam, const char* seeds,
        const char* pairs, const char* parents) {
    if (peak < 13 || peak > 36 || threshold > peak || !depth || !beam)
        throw std::runtime_error("need peak 13–36, threshold at most peak and positive depth and beam");
    std::ifstream roots(seeds);
    std::ofstream all(pairs), edge_log(parents);
    if (!roots || !all || !edge_log) throw std::runtime_error("cannot open seed or output files");
    Minima minima;
    std::vector<Pair> frontier;
    std::unordered_set<Pair, Hash> seen;
    std::string a, b;
    while (roots >> a >> b) {
        if (a.size() > 31 || b.size() > 31 || a.size() + b.size() > peak || cyclic(a) != a || cyclic(b) != b)
            throw std::runtime_error("noncyclic or oversized seed");
        const auto start = minima.canonical(key(a, b));
        if (seen.insert(start).second) {
            frontier.push_back(start);
            print(all, start);
            all << '\n';
        }
    }
    if (frontier.empty() || roots.bad()) throw std::runtime_error("missing seeds");
    std::cout << "{\n  \"cyclic_product_cap\": " << peak << ",\n  \"whitehead_frontier_cap\": " << threshold
              << ",\n  \"beam_width\": " << beam << ",\n  \"seed_classes\": " << frontier.size() << ",\n  \"layers\": [";
    Worker worker;
    size_t primitive_hits = 0;
    for (unsigned layer = 0; layer < depth && !frontier.empty() && !primitive_hits; ++layer) {
        const auto before = worker.candidates, admitted = worker.admitted;
        size_t sources = 0, marked_successors = 0;
        std::map<Pair, Witness> children;
        for (const auto& parent : frontier) {
            if (primitive_pair(parent)) throw std::runtime_error("primitive input has no remaining search");
            // Copy the plateau because other minima may be inserted during the scans.
            const auto marks = minima.marks(parent);
            for (const auto& mark : marks) {
                ++sources;
                if (peak - length(mark.first) > 31) throw std::runtime_error("selected cap exceeds packed range");
                std::set<Pair> products;
                worker.scan_pair(mark.first, mark.second, peak, [&](const auto& receiver, const auto& donor) {
                    products.insert(ak3_wide::least_image(receiver, donor));
                });
                marked_successors += products.size();
                for (const auto& product : products) {
                    const bool hit = primitive_pair(product);
                    if (hit) {
                        ++primitive_hits;
                        print(std::cerr, product);
                        std::cerr << '\n';
                    }
                    const auto child = hit ? product : minima.canonical(product);
                    if ((energy(child) <= threshold || hit) && !seen.count(child))
                        children.try_emplace(child, Witness{parent, mark, product});
                }
            }
        }
        std::vector<Pair> next;
        for (const auto& [child, witness] : children) {
            seen.insert(child);
            next.push_back(child);
            print(all, child);
            all << '\n';
            print(edge_log, child);
            edge_log << '\t';
            print(edge_log, witness.parent);
            edge_log << '\t';
            print(edge_log, witness.source);
            edge_log << '\t';
            print(edge_log, witness.product);
            edge_log << '\n';
        }
        if (layer) std::cout << ',';
        std::cout << "\n    {\"frontier_classes\": " << frontier.size() << ", \"minimal_markings\": " << sources
                  << ", \"product_candidates\": " << worker.candidates - before
                  << ", \"admitted_products\": " << worker.admitted - admitted
                  << ", \"distinct_successors_summed_over_markings\": " << marked_successors
                  << ", \"new_short_classes\": " << next.size() << '}';
        std::sort(next.begin(), next.end(), ordered);
        if (next.size() > beam) next.resize(beam);
        frontier = std::move(next);
    }
    std::cout << "\n  ],\n  \"generated_short_classes\": " << seen.size()
              << ",\n  \"primitive_product_hits\": " << primitive_hits << "\n}\n";
    if (!all || !edge_log) throw std::runtime_error("cannot write generated pairs");
    return 0;
}
}

int main(int argc, char** argv) {
    try {
        if (argc != 8) throw std::runtime_error(
            "usage: whitehead-products peak short-cap depth beam seeds.tsv classes.tsv edges.tsv");
        return whitehead_products::run(std::stoul(argv[1]), std::stoul(argv[2]), std::stoul(argv[3]),
                                       std::stoull(argv[4]), argv[5], argv[6], argv[7]);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
