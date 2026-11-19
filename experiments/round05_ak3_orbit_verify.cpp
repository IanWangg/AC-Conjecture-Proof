// Independently check closure and connectivity of a packed cyclic orbit catalogue.
#define AC_ROUND05_ORBITS_LIBRARY
#include "round05_ak3_orbits.cpp"
#define main ordinary_full_verifier_main
#include "verify_full_cyclic_component.cpp"
#undef main

namespace compact_verify {
using orbit_search::Code;
using orbit_search::Orbit;
using orbit_search::orbit_key;
using orbit_search::word;
using orbit_search::word_code;

Code numeric_word(const std::string& digits) {
    Code code = 1;
    for (unsigned char digit : digits) code = 4 * code + digit;
    return code;
}

std::string min_signed(const std::string& digits) {
    auto opposite = digits;
    std::reverse(opposite.begin(), opposite.end());
    for (auto& digit : opposite) digit ^= 1;
    return std::min(audit::least_rotation(digits), audit::least_rotation(opposite));
}

Orbit explicit_images(const std::string& digits) {
    constexpr unsigned relabel[][4]{{0,1,2,3}, {1,0,2,3}, {0,1,3,2}, {1,0,3,2},
                                    {2,3,0,1}, {3,2,0,1}, {2,3,1,0}, {3,2,1,0}};
    Orbit result;
    for (unsigned s = 0; s < result.size(); ++s) {
        std::string image = digits;
        for (auto& digit : image) digit = char(relabel[s][unsigned(digit)]);
        result[s] = numeric_word(min_signed(image));
    }
    return result;
}

std::string digits(const std::string& word) {
    auto out = word;
    for (char& c : out) c = char(orbit_search::digit(c));
    return out;
}

struct Components {
    std::vector<std::atomic<uint32_t>> parents;

    explicit Components(std::size_t size) : parents(size) {
        for (uint32_t i = 0; i < size; ++i) parents[i].store(i, std::memory_order_relaxed);
    }

    uint32_t root(uint32_t x) {
        for (;;) {
            auto parent = parents[x].load(std::memory_order_relaxed);
            if (parent == x) return x;
            const auto grandparent = parents[parent].load(std::memory_order_relaxed);
            if (parent != grandparent)
                parents[x].compare_exchange_weak(parent, grandparent, std::memory_order_relaxed);
            x = grandparent;
        }
    }

    void join(uint32_t x, uint32_t y) {
        for (;;) {
            auto a = root(x), b = root(y);
            if (a == b) return;
            if (a < b) std::swap(a, b);
            if (parents[a].compare_exchange_weak(a, b, std::memory_order_relaxed)) return;
        }
    }
};

std::string stack_product(const std::string& u, const std::string& q, const std::string& v,
                          const std::string& inverse_q, int limit) {
    char stack[64];
    int right = 0;
    for (const auto* part : {&u, &q, &v, &inverse_q}) for (char c : *part) {
        if (right && stack[right - 1] == (c ^ 1)) --right;
        else stack[right++] = c;
    }
    int left = 0;
    while (right - left > 1 && stack[left] == (stack[right - 1] ^ 1)) { ++left; --right; }
    if (left == right) throw std::runtime_error("empty descendant");
    return right - left <= limit ? std::string(stack + left, stack + right) : std::string{};
}

struct Totals {
    uint64_t candidates = 0, admitted = 0;
};

int run(int cap, unsigned workers, const char* tsv, const char* report) {
    if (cap < 13 || cap > 29 || !workers) throw std::runtime_error("need cap 13–29 and at least one worker");
    audit::self_test();
    std::ifstream input(tsv);
    if (!input) throw std::runtime_error("cannot open orbit catalogue");
    std::vector<Code> states;
    std::unordered_map<Code, uint32_t> ids;
    std::string line;
    while (std::getline(input, line)) {
        const auto separator = line.find('\t');
        if (separator == std::string::npos || !separator || separator + 1 == line.size() || line.size() > size_t(cap + 1))
            throw std::runtime_error("invalid orbit catalogue row");
        const auto a = line.substr(0, separator), b = line.substr(separator + 1);
        if (audit::cyclically_reduced(a) != a || audit::cyclically_reduced(b) != b)
            throw std::runtime_error("noncyclic input");
        const Code key = orbit_key(explicit_images(digits(a)), explicit_images(digits(b)));
        if (key != orbit_search::pack(word_code(a), word_code(b)) || !ids.try_emplace(key, states.size()).second)
            throw std::runtime_error("noncanonical or repeated orbit key");
        states.push_back(key);
    }
    if (input.bad() || states.empty()) throw std::runtime_error("empty or unreadable orbit catalogue");
    const Code start = orbit_key(explicit_images(digits("xxxYYYY")), explicit_images(digits("xyxYXY")));
    const auto start_id = ids.at(start);
    Components components(states.size());
    std::atomic<std::size_t> cursor(0);
    const auto& lookup = ids;
    auto scan = [&]() {
        Totals totals;
        std::unordered_map<Code, Orbit> images;
        std::unordered_map<Code, std::vector<std::string>> rotations;
        std::map<int, std::vector<std::pair<std::string, std::string>>> tails;
        auto orbit = [&](const std::string& cyclic_digits) -> const Orbit& {
            const auto canonical = min_signed(cyclic_digits);
            const auto [it, inserted] = images.try_emplace(numeric_word(canonical));
            if (inserted) it->second = explicit_images(canonical);
            return it->second;
        };
        for (;;) {
            const auto from = cursor.fetch_add(1024, std::memory_order_relaxed);
            if (from >= states.size()) return totals;
            for (auto at = from; at < std::min(states.size(), from + 1024); ++at) {
                if (images.size() > 32768) images.clear();
                if (rotations.size() > 8192) rotations.clear();
                const auto [a, b] = orbit_search::unpack(states[at]);
                const Code codes[2]{a, b};
                const std::string words[2]{word(a), word(b)};
                for (int i = 0; i < 2; ++i) if (!rotations.count(codes[i])) {
                    auto variants = audit::signed_rotations(words[i]);
                    for (auto& value : variants) value = digits(value);
                    rotations.emplace(codes[i], std::move(variants));
                }
                std::unordered_set<uint32_t> neighbors;
                for (int i = 0; i < 2; ++i) {
                    const int receiver = int(words[i].size()), donor = int(words[1 - i].size());
                    const int bound = std::max(0, (cap - receiver - 2 * donor) / 2);
                    if (!tails.count(bound)) {
                        std::string prefix;
                        std::vector<std::string> reduced;
                        audit::append_tails(bound, prefix, reduced);
                        for (const auto& q : reduced) tails[bound].emplace_back(digits(q), digits(audit::reversed_inverse(q)));
                    }
                    const auto donor_orbit = orbit(digits(words[1 - i]));
                    for (const auto& u : rotations.at(codes[i]))
                        for (const auto& v : rotations.at(codes[1 - i]))
                            for (const auto& [q, inverse_q] : tails.at(bound)) {
                                ++totals.candidates;
                                const auto product = stack_product(u, q, v, inverse_q, cap - donor);
                                if (product.empty()) continue;
                                ++totals.admitted;
                                const auto next = lookup.find(orbit_key(orbit(product), donor_orbit));
                                if (next == lookup.end()) throw std::runtime_error("orbit catalogue not closed");
                                neighbors.insert(next->second);
                            }
                }
                for (const auto neighbor : neighbors) components.join(at, neighbor);
            }
        }
    };
    std::vector<std::future<Totals>> jobs;
    for (unsigned i = 0; i < workers; ++i) jobs.push_back(std::async(std::launch::async, scan));
    Totals totals;
    for (auto& job : jobs) {
        const auto count = job.get();
        totals.candidates += count.candidates;
        totals.admitted += count.admitted;
    }
    const auto root = components.root(start_id);
    for (uint32_t i = 0; i < states.size(); ++i)
        if (components.root(i) != root) throw std::runtime_error("orbit catalogue not connected");
    std::ofstream out(report);
    out << "{\n  \"status\":\"CLOSED_AND_CONNECTED\",\n  \"cyclic_cap\":" << cap << ",\n  \"signed_permutation_orbits\":"
        << states.size() << ",\n  \"rotation_product_candidates\":" << totals.candidates
        << ",\n  \"admitted_neighbors\":" << totals.admitted << "\n}\n";
    if (!out) throw std::runtime_error("cannot write independent audit");
    return 0;
}
}

int main(int argc, char** argv) {
    try {
        if (argc != 5) throw std::runtime_error("usage: verify cap workers catalogue.tsv output.json");
        return compact_verify::run(std::stoi(argv[1]), std::stoul(argv[2]), argv[3], argv[4]);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
