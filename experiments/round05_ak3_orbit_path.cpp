// Find the exact minimum product distance to a target in the signed orbit graph.
#define AC_ROUND05_ORBITS_LIBRARY
#include "round05_ak3_orbits.cpp"

namespace orbit_path {
using namespace orbit_search;
constexpr uint32_t no_parent = std::numeric_limits<uint32_t>::max();

struct Ball {
    std::vector<std::pair<Code, uint32_t>> nodes;
    std::unordered_map<Code, uint32_t> index;
    uint32_t begin = 0, end = 0, radius = 0;

    explicit Ball(Code root) : nodes{{root, no_parent}}, index{{root, 0}}, end(1) {}

    std::vector<Code> to_root(uint32_t at) const {
        std::vector<Code> route;
        for (; at != no_parent; at = nodes.at(at).second) route.push_back(nodes.at(at).first);
        return route;
    }
};

int run(int cap, const std::string& a, const std::string& b, const char* output) {
    if (cap < 13 || cap > 29 || a.empty() || b.empty() || a.size() + b.size() > size_t(cap) || cyclic(a) != a || cyclic(b) != b)
        throw std::runtime_error("expected nonempty cyclic targets within cap 13–29");
    const Code start = orbit_key(build_orbit(word_code("xxxYYYY")), build_orbit(word_code("xyxYXY")));
    const Code target = orbit_key(build_orbit(word_code(a)), build_orbit(word_code(b)));
    if (target == start) throw std::runtime_error("target is already in the start orbit");
    Ball balls[2]{Ball(start), Ball(target)};
    Worker worker;
    uint32_t meeting[2]{no_parent, no_parent};
    while (meeting[0] == no_parent) {
        const unsigned side = (balls[0].end - balls[0].begin > balls[1].end - balls[1].begin);
        auto& from = balls[side];
        auto& to = balls[1 - side];
        if (from.begin == from.end) throw std::runtime_error("target orbit is unreachable");
        for (uint32_t at = from.begin; at < from.end && meeting[0] == no_parent; ++at) {
            worker.next.clear();
            worker.scan(from.nodes[at].first, cap);
            std::vector<Code> ordered(worker.next.begin(), worker.next.end());
            std::sort(ordered.begin(), ordered.end());
            for (const Code next : ordered) {
                const uint32_t id = from.nodes.size();
                if (!from.index.try_emplace(next, id).second) continue;
                from.nodes.emplace_back(next, at);
                const auto match = to.index.find(next);
                if (match == to.index.end()) continue;
                meeting[side] = id;
                meeting[1 - side] = match->second;
                break;
            }
        }
        if (meeting[0] == no_parent) {
            from.begin = from.end;
            from.end = from.nodes.size();
            ++from.radius;
        }
    }
    auto route = balls[0].to_root(meeting[0]);
    std::reverse(route.begin(), route.end());
    const auto suffix = balls[1].to_root(meeting[1]);
    route.insert(route.end(), suffix.begin() + 1, suffix.end());
    const std::size_t distance = route.size() - 1;
    if (distance != 1 + balls[0].radius + balls[1].radius)
        throw std::runtime_error("distance does not match completed radii");
    std::ofstream out(output);
    out << "{\n  \"cyclic_cap\":" << cap << ",\n  \"minimum_macro_distance\":" << distance
        << ",\n  \"disjoint_ball_radii\":[" << balls[0].radius << ',' << balls[1].radius
        << "],\n  \"states_discovered\":[" << balls[0].nodes.size() << ',' << balls[1].nodes.size()
        << "],\n  \"products_checked\":" << worker.candidates << ",\n  \"orbit_route\":[\n";
    for (std::size_t i = 0; i < route.size(); ++i) {
        const auto [u, v] = unpack(route[i]);
        if (i) out << ",\n";
        out << "    [\"" << word(u) << "\",\"" << word(v) << "\"]";
    }
    out << "\n  ]\n}\n";
    if (!out) throw std::runtime_error("cannot write quotient route");
    return 0;
}
}

int main(int argc, char** argv) {
    try {
        if (argc != 5) throw std::runtime_error("usage: orbit-path cap first second route.json");
        return orbit_path::run(std::stoi(argv[1]), argv[2], argv[3], argv[4]);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
