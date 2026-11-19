// Bidirectional BFS for an exact minimum in the bounded cyclic macro graph.
#define main cyclic_component_reference_main
#include "cyclic_component.cpp"
#undef main

namespace escape {
constexpr size_t no_parent = size_t(-1);

struct Node {
    P state;
    size_t parent;
};

struct Ball {
    std::vector<Node> nodes;
    std::unordered_map<std::string, size_t> index;
    size_t begin = 0, end = 0, radius = 0;

    explicit Ball(const std::vector<P>& roots) {
        for (const auto& root : roots) {
            if (!index.try_emplace(key(root), nodes.size()).second)
                throw std::runtime_error("duplicate root");
            nodes.push_back({root, no_parent});
        }
        end = nodes.size();
    }

    size_t current_layer_size() const { return end - begin; }

    std::vector<P> to_root(size_t at) const {
        std::vector<P> states;
        while (at != no_parent) {
            states.push_back(nodes.at(at).state);
            at = nodes[at].parent;
        }
        return states;
    }
};

class Menu {
    int cap;
    std::map<std::string, std::vector<std::string>> signed_rotations;
    std::map<int, std::vector<std::pair<std::string,std::string>>> bridge_cache;

public:
    uint64_t products = 0;

    explicit Menu(int maximum) : cap(maximum) {}

    template <typename Visitor>
    bool visit(const P& state, const Visitor& try_state) {
        const std::string words[2]{state.first, state.second};
        for (const auto& word : words) {
            if (!signed_rotations.count(word)) signed_rotations.emplace(word, variants(word));
        }
        for (int receiver = 0; receiver < 2; ++receiver) {
            const auto& a = words[receiver];
            const auto& b = words[1-receiver];
            const int bound = std::max(0, (cap - int(a.size()) - 2 * int(b.size())) / 2);
            if (!bridge_cache.count(bound)) {
                auto& entries = bridge_cache[bound];
                for (const auto& bridge : bridges(bound)) entries.emplace_back(bridge, inverse(bridge));
            }
            for (const auto& u : signed_rotations.at(a))
                for (const auto& v : signed_rotations.at(b))
                    for (const auto& [q, inverse_q] : bridge_cache.at(bound)) {
                        ++products;
                        const auto reduced = cyclic(u + q + v + inverse_q);
                        if (int(reduced.size() + b.size()) > cap) continue;
                        if (try_state(canonpair(canonical(reduced), b))) return true;
                    }
        }
        return false;
    }
};

std::vector<P> read_targets(const char* path, int cap) {
    std::ifstream stream(path);
    if (!stream) throw std::runtime_error("cannot open targets");
    std::vector<P> roots;
    std::string line;
    while (std::getline(stream, line)) {
        const auto tab = line.find('\t');
        if (tab == std::string::npos) throw std::runtime_error("expected target TSV");
        P pair{line.substr(0, tab), line.substr(tab + 1)};
        if (pair.first.empty() || pair.second.empty() || pair.first != canonical(pair.first)
            || pair.second != canonical(pair.second) || pair.first > pair.second
            || int(pair.first.size() + pair.second.size()) > cap)
            throw std::runtime_error("noncanonical or out-of-cap target");
        roots.push_back(std::move(pair));
    }
    if (roots.empty()) throw std::runtime_error("no target rows");
    return roots;
}

int run(int cap, const char* path, const char* output_path) {
    const auto targets = read_targets(path, cap);
    const P start = canonpair(canonical("xxxYYYY"), canonical("xyxYXY"));
    if (std::find(targets.begin(), targets.end(), start) != targets.end())
        throw std::runtime_error("target catalogue contains the start");
    Ball ball[] = {Ball({start}), Ball(targets)};
    Menu menu(cap);
    size_t meeting[2]{no_parent, no_parent};
    for (;;) {
        int which = ball[0].current_layer_size() <= ball[1].current_layer_size() ? 0 : 1;
        auto& here = ball[which];
        auto& there = ball[1-which];
        if (here.current_layer_size() == 0) throw std::runtime_error("no reachable target");
        bool found = false;
        for (size_t at = here.begin; at < here.end && !found; ++at) {
            const auto state = here.nodes[at].state;
            found = menu.visit(state, [&](P next) {
                const auto name = key(next);
                const size_t id = here.nodes.size();
                if (!here.index.try_emplace(name, id).second) return false;
                here.nodes.push_back({std::move(next), at});
                const auto other = there.index.find(name);
                if (other == there.index.end()) return false;
                meeting[which] = id;
                meeting[1-which] = other->second;
                return true;
            });
        }
        if (found) break;
        here.begin = here.end;
        here.end = here.nodes.size();
        ++here.radius;
    }
    auto route = ball[0].to_root(meeting[0]);
    std::reverse(route.begin(), route.end());
    const auto suffix = ball[1].to_root(meeting[1]);
    route.insert(route.end(), suffix.begin()+1, suffix.end());
    const auto distance = route.size()-1;
    if (distance != ball[0].radius + ball[1].radius + 1)
        throw std::logic_error("collision disagrees with exhausted radii");
    std::ofstream out(output_path);
    out << "{\n  \"cyclic_cap\":" << cap << ",\n  \"target_count\":" << targets.size()
        << ",\n  \"minimum_macro_distance\":" << distance
        << ",\n  \"disjoint_ball_radii\":[" << ball[0].radius << ',' << ball[1].radius
        << "],\n  \"states_discovered\":[" << ball[0].nodes.size() << ',' << ball[1].nodes.size()
        << "],\n  \"products_checked\":" << menu.products << ",\n  \"route\":[\n";
    for (size_t i = 0; i < route.size(); ++i) {
        if (i) out << ",\n";
        out << "    [\"" << route[i].first << "\",\"" << route[i].second << "\"]";
    }
    out << "\n  ]\n}\n";
    if (!out) throw std::runtime_error("failed to write output");
    std::cout << "exact macro distance " << distance << " from AK(3) to " << targets.size()
              << " targets\n";
    return 0;
}
}

int main(int argc, char** argv) {
    try {
        if (argc != 4) throw std::runtime_error("usage: escape_path cap targets.tsv result.json");
        return escape::run(std::stoi(argv[1]), argv[2], argv[3]);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
