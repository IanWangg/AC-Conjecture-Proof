// Search backwards from the cap-23 stable waypoint for an ordinary cap-29 entry.
#define AC_ROUND07_WIDE_ORBITS_LIBRARY
#include "round07_ak3_wide_orbits.cpp"

#include <filesystem>

namespace waypoint_bridge {
using wide_orbits::Pair;
using wide_orbits::Hash;
using wide_orbits::energy;
using wide_orbits::word;
using wide_orbits::no_parent;
using orbit_search::Code;

std::unordered_set<Code> load_cap29(const char* path) {
    std::ifstream input(path);
    if (!input) throw std::runtime_error("cannot open cap-29 catalogue");
    std::unordered_set<Code> known;
    known.reserve(std::filesystem::file_size(path) / 30);
    std::string row;
    while (std::getline(input, row)) {
        const auto split = row.find('\t');
        if (split == std::string::npos || !split || split + 1 == row.size() || row.size() > 30)
            throw std::runtime_error("invalid cap-29 row");
        const auto a = row.substr(0, split), b = row.substr(split + 1);
        if (!known.insert(orbit_search::pack(orbit_search::word_code(a), orbit_search::word_code(b))).second)
            throw std::runtime_error("duplicate cap-29 row");
    }
    if (input.bad() || known.empty()) throw std::runtime_error("empty or unreadable cap-29 catalogue");
    return known;
}

int run(int cap, uint32_t state_limit, const char* known_path, const std::string& prefix) {
    if (cap < 29 || cap > 32 || !state_limit)
        throw std::runtime_error("need cap 29–32 and positive state limit");
    round01::check_product();
    const auto known = load_cap29(known_path);
    const Pair target = wide_orbits::key("XXXYxyxyXYY", "XYXYYXyXYYXy");
    std::vector<Pair> states{target};
    std::vector<uint32_t> parents{no_parent};
    std::unordered_set<Pair, Hash> visited{target};
    auto is_known = [&](const Pair& state) {
        return energy(state) <= 29 && known.count(orbit_search::pack(state.first, state.second));
    };
    if (is_known(target)) throw std::runtime_error("waypoint already in cap-29 catalogue");
    orbit_search::Worker worker;
    std::unordered_set<Pair, Hash> next;
    std::unordered_map<Code, bool> primitive_cache;
    auto primitive = [&](Code code) {
        if (primitive_cache.size() > 131072) primitive_cache.clear();
        const auto [it, inserted] = primitive_cache.try_emplace(code);
        if (inserted) it->second = orbit_search::primitive(word(code));
        return it->second;
    };
    uint32_t bridge = no_parent, primitive_index = no_parent;
    uint32_t lowest = 0;
    uint32_t begin = 0, end = 1, completed_radius = 0, expanded = 0;
    while (begin != end && bridge == no_parent && primitive_index == no_parent && states.size() < state_limit) {
        for (uint32_t i = begin; i < end && bridge == no_parent && primitive_index == no_parent
                                       && states.size() < state_limit; ++i) {
            const auto [a, b] = states[i];
            next.clear();
            worker.scan_pair(a, b, cap, [&](const auto& recipient, const auto& donor) {
                next.insert(ak3_wide::least_image(recipient, donor));
            });
            std::vector<Pair> ordered(next.begin(), next.end());
            std::sort(ordered.begin(), ordered.end());
            ++expanded;
            for (const auto& state : ordered) {
                if (!visited.insert(state).second) continue;
                if (states.size() == no_parent) throw std::runtime_error("state index exhausted");
                const uint32_t index = states.size();
                states.push_back(state);
                parents.push_back(i);
                if (wide_orbits::catalogue_order(state, states[lowest])) lowest = index;
                if (is_known(state)) bridge = index;
                if (primitive(state.first) || primitive(state.second)) primitive_index = index;
                if (bridge != no_parent || primitive_index != no_parent || states.size() >= state_limit) break;
            }
        }
        if (expanded == end && bridge == no_parent && primitive_index == no_parent && states.size() < state_limit) {
            begin = end;
            end = states.size();
            ++completed_radius;
            std::cerr << "cap " << cap << " completed radius " << completed_radius
                      << ", discovered " << states.size() << '\n';
        }
    }
    if (bridge != no_parent) {
        // The lift compiler can concatenate this route with a cap-29 prefix.
        std::vector<Pair> route;
        for (auto at = bridge; at != no_parent; at = parents[at]) route.push_back(states[at]);
        std::ofstream out(prefix + ".bridge.route.json");
        out << "{\n  \"cyclic_cap\":" << cap << ",\n  \"macro_distance\":" << route.size() - 1
            << ",\n  \"orbit_route\":[\n";
        bool first = true;
        for (const auto& [a, b] : route) {
            if (!first) out << ",\n";
            first = false;
            out << "    [\"" << word(a) << "\",\"" << word(b) << "\"]";
        }
        out << "\n  ]\n}\n";
        if (!out) throw std::runtime_error("cannot write bridge");
    }
    if (primitive_index != no_parent)
        wide_orbits::write_route(prefix + ".primitive.route.json", cap, primitive_index, states, parents);
    wide_orbits::write_route(prefix + ".lowest.route.json", cap, lowest, states, parents);
    auto catalogue = states;
    std::sort(catalogue.begin(), catalogue.end(), wide_orbits::catalogue_order);
    std::ofstream tsv(prefix + ".orbit.tsv");
    for (const auto& [a, b] : catalogue) tsv << word(a) << '\t' << word(b) << '\n';
    tsv.close();
    std::ofstream out(prefix + ".json");
    out << "{\n  \"cyclic_cap\":" << cap << ",\n  \"known_orbits\":" << known.size()
        << ",\n  \"state_limit\":" << state_limit << ",\n  \"states_discovered\":" << states.size()
        << ",\n  \"states_expanded\":" << expanded << ",\n  \"completed_radius\":" << completed_radius
        << ",\n  \"minimum_discovered_energy\":" << energy(states[lowest])
        << ",\n  \"product_candidates\":" << worker.candidates << ",\n  \"admitted_products\":" << worker.admitted
        << ",\n  \"hit_cap29\":" << (bridge != no_parent ? "true" : "false")
        << ",\n  \"hit_primitive\":" << (primitive_index != no_parent ? "true" : "false")
        << ",\n  \"closed_component\":" << (begin == end ? "true" : "false") << "\n}\n";
    if (!tsv || !out) throw std::runtime_error("cannot write search report");
    return 0;
}
}

int main(int argc, char** argv) {
    try {
        if (argc != 5) throw std::runtime_error("usage: waypoint-bridge cap state-limit cap29.tsv output-prefix");
        return waypoint_bridge::run(std::stoi(argv[1]), std::stoul(argv[2]), argv[3], argv[4]);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
