// Continue rank-three search after removing the length-six E17 donor orbit.
#define AC_ROUND11_REVERSE_LIBRARY
#include "round11_stable_proof_reverse.cpp"
#define AC_ROUND09_PRIMITIVE_REUSE
#include "round09_stable_proof_primitive_catalogue.cpp"

#include <queue>

namespace {

using Projection = std::array<std::string, 2>;

Projection signed_projection(const std::string& a, const std::string& b) {
    Projection best{"~", "~"};
    for (const auto& action : actions) {
        if (std::tolower(action[2]) != 'z') continue;
        const auto change = [&](std::string word) {
            for (auto& c : word) c = action[alphabet.find(c)];
            return canonical(std::move(word));
        };
        Projection candidate{change(a), change(b)};
        std::sort(candidate.begin(), candidate.end());
        best = std::min(best, candidate);
    }
    return best;
}

struct ReleaseNode {
    Key key;
    size_t parent;
    unsigned pivots;
};

struct Witness {
    size_t node;
    size_t pivot;
};

class ReleaseSearch {
    Scanner menu;
    std::unordered_set<std::string> excluded_donors;
    std::unordered_map<Code, std::optional<Mark>> charts;
    std::unordered_set<Key,KeyHash> seen;
    std::set<Projection> archive;
    std::vector<ReleaseNode> nodes;
    std::map<Projection,Witness> projections;
    std::map<Projection,Witness> isolated;
    std::priority_queue<std::pair<unsigned,size_t>,std::vector<std::pair<unsigned,size_t>>,
                        std::greater<>> waiting;
    std::optional<Witness> join;
    std::string join_type;
    uint64_t short_donor_edges = 0;
    size_t charted_discovered = 0, charted_expanded = 0;
    int cap;
    bool mixed;
    bool stop_at_chart, allow_short_donor;

    const std::optional<Mark>& chart(const std::string& word) {
        const auto [entry, fresh] = charts.try_emplace(encode(word));
        if (fresh) entry->second = quotient(word);
        return entry->second;
    }

    void admit(Key key, size_t parent) {
        if (seen.count(key)) return;
        const auto rows = rows_from(key);
        if (!allow_short_donor &&
            std::any_of(rows.begin(), rows.end(), [&](const auto& w) {return excluded_donors.count(w);})) {
            ++short_donor_edges;
            return;
        }
        seen.insert(key);
        const size_t index = nodes.size();
        unsigned pivots = 0;
        for (size_t i = 0; i < rows.size(); ++i) {
            const auto& marking = chart(rows[i]);
            if (!marking) continue;
            ++pivots;
            const auto& a = rows[(i + 1) % 3];
            const auto& b = rows[(i + 2) % 3];
            const auto first = canonical(image(a, *marking));
            const auto second = canonical(image(b, *marking));
            if (first.empty() || second.empty()) throw std::logic_error("vanished quotient row");
            const auto pair = signed_projection(first, second);
            const Witness witness{index,i};
            projections.try_emplace(pair, witness);
            if (rows[i].size() == 1) {
                const auto g = rows[i][0];
                if (a.find(g) == a.npos && a.find(invchar(g)) == a.npos &&
                    b.find(g) == b.npos && b.find(invchar(g)) == b.npos)
                    isolated.try_emplace(pair, witness);
            }
            if (!join && (primitive_rank_two(first) || primitive_rank_two(second))) {
                join = witness;
                join_type = "primitive";
            } else if (!join && archive.count(pair)) {
                join = witness;
                join_type = "archive";
            } else if (!join && stop_at_chart) {
                join = witness;
                join_type = "chart";
            }
        }
        nodes.push_back({key, parent, pivots});
        if (pivots) ++charted_discovered;
        if (mixed || !pivots) waiting.emplace(unsigned(energy(rows)), index);
    }

    static void write_projections(const std::string& output,
                                  const std::map<Projection,Witness>& entries,
                                  const std::vector<ReleaseNode>& catalogued) {
        std::ofstream sink(output);
        for (const auto& [pair, trace] : entries) {
            sink << pair[0] << '\t' << pair[1] << '\t' << trace.node << '\t' << trace.pivot << '\t';
            write_tsv(sink, rows_from(catalogued[trace.node].key));
        }
        if (!sink) throw std::runtime_error("cannot write projection catalogue");
    }

public:
    ReleaseSearch(int cap, bool mixed, bool stop_at_chart, bool allow_short_donor)
        : cap(cap), mixed(mixed), stop_at_chart(stop_at_chart), allow_short_donor(allow_short_donor) {
        if (cap < 33 || cap > 39) throw std::invalid_argument("cap out of range");
        for (const auto& action : actions) {
            std::string word = "xxyXYY";
            for (auto& c : word) c = action[alphabet.find(c)];
            excluded_donors.insert(canonical(std::move(word)));
        }
    }

    void run(const std::string& sources, const std::string& archive_path,
             size_t budget, const std::string& output) {
        std::ifstream target(archive_path);
        Projection pair;
        while (target >> pair[0] >> pair[1])
            archive.insert(signed_projection(canonical(pair[0]), canonical(pair[1])));
        if (!target.eof() || archive.empty()) throw std::runtime_error("invalid archive");
        import(sources, [&](Key key) { admit(key, seed_parent); }, 3, cap, menu.orbits);
        const auto root_count = nodes.size();
        if (!root_count || charted_discovered) throw std::runtime_error("expected chartless roots");
        if (!budget) throw std::invalid_argument("positive expansion budget required");
        std::vector<Key> next;
        size_t expanded = 0;
        while (expanded < budget && !waiting.empty() && !join) {
            const auto at = waiting.top().second;
            waiting.pop();
            ++expanded;
            charted_expanded += nodes[at].pivots != 0;
            menu.neighbors(nodes[at].key, 3, cap, next);
            for (const auto point : next) {
                admit(point, at);
                if (join) break;
            }
            if (expanded % 65536 == 0)
                std::cerr << "expanded " << expanded << ", discovered " << nodes.size() << '\n';
        }
        write_projections(output + ".pairs.tsv", projections, nodes);
        write_projections(output + ".isolated.tsv", isolated, nodes);
        std::ofstream genealogy(output + ".nodes.tsv"), route(output + ".route.tsv");
        for (const auto& node : nodes) {
            genealogy << node.parent << '\t' << node.pivots << '\t';
            write_tsv(genealogy, rows_from(node.key));
        }
        if (join) {
            std::vector<Key> path;
            for (size_t i = join->node; i != seed_parent; i = nodes[i].parent)
                path.push_back(nodes[i].key);
            for (auto it = path.rbegin(); it != path.rend(); ++it) write_tsv(route, rows_from(*it));
        }
        if (!genealogy || !route) throw std::runtime_error("cannot write search genealogy");
        std::cout << "{\"cap\":" << cap << ",\"mixed\":" << (mixed ? "true" : "false")
                  << ",\"roots\":" << root_count << ",\"archive_keys\":" << archive.size()
                  << ",\"expanded\":" << expanded << ",\"discovered\":" << nodes.size()
                  << ",\"charted_expanded\":" << charted_expanded
                  << ",\"charted_discovered\":" << charted_discovered
                  << ",\"projection_orbits\":" << projections.size()
                  << ",\"isolated_projection_orbits\":" << isolated.size()
                  << ",\"candidates\":" << menu.candidates << ",\"admitted\":" << menu.admitted
                  << ",\"positive_bridges\":" << menu.nonempty
                  << ",\"word_width_omissions\":" << menu.outside_word_width
                  << ",\"excluded_short_donor_edges\":" << short_donor_edges
                  << ",\"closed\":" << (waiting.empty() && !join ? "true" : "false")
                  << ",\"hit\":";
        if (join) std::cout << "\"" << join_type << "\"";
        else std::cout << "null";
        std::cout << "}\n";
    }
};

}

int main(int argc, char** argv) {
    try {
        if (argc < 6)
            throw std::invalid_argument("usage: release cap budget roots.tsv archive.tsv output [--mixed] [--first-chart] [--allow-short]");
        bool mixed = false, stop_at_chart = false, allow_short_donor = false;
        for (int i = 6; i < argc; ++i) {
            const std::string_view option = argv[i];
            if (option == "--mixed") mixed = true;
            else if (option == "--first-chart") stop_at_chart = true;
            else if (option == "--allow-short") allow_short_donor = true;
            else throw std::invalid_argument("unknown option");
        }
        ReleaseSearch scanner(std::stoi(argv[1]), mixed, stop_at_chart, allow_short_donor);
        scanner.run(argv[3], argv[4], std::stoull(argv[2]), argv[5]);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
