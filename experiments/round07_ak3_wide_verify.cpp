// Independently verify a full signed orbit component with separate word codes.
#define AC_ROUND05_ORBIT_VERIFY_LIBRARY
#include "round05_ak3_orbit_verify.cpp"
#include "round06_ak3_wide_pair.hpp"

namespace wide_verify {
using ak3_wide::Pair;
using ak3_wide::Hash;
using compact_verify::Code;
using compact_verify::Orbit;

Pair least_pair(const Orbit& a, const Orbit& b) {
    Pair least{std::numeric_limits<Code>::max(), 0};
    for (unsigned i = 0; i != a.size(); ++i) {
        auto ends = std::minmax(a[i], b[i]);
        least = std::min(least, Pair{ends.first, ends.second});
    }
    return least;
}

Pair signed_key(const std::string& a, const std::string& b) {
    return least_pair(compact_verify::explicit_images(compact_verify::digits(a)),
                      compact_verify::explicit_images(compact_verify::digits(b)));
}

int run(int cap, unsigned workers, const char* catalogue, const char* report,
        const std::string& first, const std::string& second) {
    if (cap < 13 || cap > 32 || !workers)
        throw std::runtime_error("need cap 13–32 and positive worker count");
    audit::self_test();
    std::ifstream input(catalogue);
    if (!input) throw std::runtime_error("cannot open orbit catalogue");
    std::vector<Pair> states;
    std::unordered_map<Pair, uint32_t, Hash> ids;
    std::string line;
    while (std::getline(input, line)) {
        const auto separator = line.find('\t');
        if (separator == std::string::npos || !separator || separator + 1 == line.size()
                || line.size() > size_t(cap + 1))
            throw std::runtime_error("invalid orbit catalogue row");
        if (states.size() == std::numeric_limits<uint32_t>::max())
            throw std::runtime_error("state index exhausted");
        const auto a = line.substr(0, separator), b = line.substr(separator + 1);
        if (audit::cyclically_reduced(a) != a || audit::cyclically_reduced(b) != b)
            throw std::runtime_error("noncyclic input");
        const Pair key = signed_key(a, b);
        if (key != Pair{orbit_search::word_code(a), orbit_search::word_code(b)}
                || !ids.try_emplace(key, states.size()).second)
            throw std::runtime_error("noncanonical or repeated orbit");
        states.push_back(key);
    }
    if (input.bad() || states.empty()) throw std::runtime_error("empty or unreadable catalogue");
    const auto start_id = ids.at(signed_key(first, second));
    std::cerr << "loaded " << states.size() << " orbits\n";
    compact_verify::Components components(states.size());
    std::atomic<std::size_t> cursor(0);
    const auto& lookup = ids;
    auto scan = [&]() {
        compact_verify::Totals totals;
        std::unordered_map<Code, Orbit> images;
        std::unordered_map<Code, std::vector<std::string>> rotations;
        std::map<int, std::vector<std::pair<std::string, std::string>>> tails;
        auto orbit = [&](std::string digits) -> const Orbit& {
            const auto canonical = compact_verify::min_signed(digits);
            const auto [it, inserted] = images.try_emplace(compact_verify::numeric_word(canonical));
            if (inserted) it->second = compact_verify::explicit_images(canonical);
            return it->second;
        };
        constexpr std::size_t block = 512;
        for (;;) {
            const auto begin = cursor.fetch_add(block, std::memory_order_relaxed);
            if (begin >= states.size()) return totals;
            if (begin % (block * 8192) == 0)
                std::cerr << "checking orbit block starting at " << begin << '\n';
            for (auto i = begin; i < std::min(states.size(), begin + block); ++i) {
                if (images.size() > 32768) images.clear();
                if (rotations.size() > 8192) rotations.clear();
                const auto [a, b] = states[i];
                const Code codes[2]{a, b};
                const std::string words[2]{orbit_search::word(a), orbit_search::word(b)};
                for (int j = 0; j < 2; ++j) if (!rotations.count(codes[j])) {
                    auto variants = audit::signed_rotations(words[j]);
                    for (auto& value : variants) value = compact_verify::digits(value);
                    rotations.emplace(codes[j], std::move(variants));
                }
                std::unordered_set<uint32_t> neighbors;
                for (int j = 0; j < 2; ++j) {
                    const int receiver = int(words[j].size()), donor = int(words[1 - j].size());
                    const int bound = std::max(0, (cap - receiver - 2 * donor) / 2);
                    if (!tails.count(bound)) {
                        std::string prefix;
                        std::vector<std::string> reduced;
                        audit::append_tails(bound, prefix, reduced);
                        for (const auto& tail : reduced)
                            tails[bound].emplace_back(compact_verify::digits(tail),
                                                    compact_verify::digits(audit::reversed_inverse(tail)));
                    }
                    const auto donor_orbit = orbit(compact_verify::digits(words[1 - j]));
                    for (const auto& u : rotations.at(codes[j]))
                        for (const auto& v : rotations.at(codes[1 - j]))
                            for (const auto& [q, inverse_q] : tails.at(bound)) {
                                ++totals.candidates;
                                const auto product = compact_verify::stack_product(u, q, v, inverse_q, cap - donor);
                                if (product.empty()) continue;
                                ++totals.admitted;
                                const auto next = lookup.find(least_pair(orbit(product), donor_orbit));
                                if (next == lookup.end()) throw std::runtime_error("catalogue not closed");
                                neighbors.insert(next->second);
                            }
                }
                for (const auto neighbor : neighbors) components.join(i, neighbor);
            }
        }
    };
    std::vector<std::future<compact_verify::Totals>> jobs;
    for (unsigned i = 0; i < workers; ++i) jobs.push_back(std::async(std::launch::async, scan));
    compact_verify::Totals totals;
    for (auto& job : jobs) {
        const auto count = job.get();
        totals.candidates += count.candidates;
        totals.admitted += count.admitted;
    }
    const auto root = components.root(start_id);
    for (uint32_t i = 0; i < states.size(); ++i)
        if (components.root(i) != root) throw std::runtime_error("catalogue not connected");
    std::ofstream out(report);
    out << "{\n  \"status\":\"CLOSED_AND_CONNECTED\",\n  \"cyclic_cap\":" << cap
        << ",\n  \"signed_permutation_orbits\":" << states.size()
        << ",\n  \"rotation_product_candidates\":" << totals.candidates
        << ",\n  \"admitted_neighbors\":" << totals.admitted << "\n}\n";
    if (!out) throw std::runtime_error("cannot write independent audit");
    return 0;
}
}

int main(int argc, char** argv) {
    try {
        if (argc != 5 && argc != 7)
            throw std::runtime_error("usage: wide-verify cap workers catalogue.tsv report.json [first second]");
        return wide_verify::run(std::stoi(argv[1]), std::stoul(argv[2]), argv[3], argv[4],
                                argc == 5 ? "xxxYYYY" : argv[5], argc == 5 ? "xyxYXY" : argv[6]);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
