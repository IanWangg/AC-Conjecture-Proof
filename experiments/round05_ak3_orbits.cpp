// Exact bounded cyclic AC search modulo signed ambient basis permutations.
#define AC_ROUND01_COMPONENT_LIBRARY
#include "round01_ak3_cyclic_component.cpp"

#include <array>
#include <atomic>
#include <cstdint>
#include <future>
#include <limits>
#include <numeric>

namespace orbit_search {
using Code = uint64_t;
using Orbit = std::array<Code, 8>;
constexpr std::string_view alphabet = "xXyY";

unsigned digit(char c) {
    const auto found = alphabet.find(c);
    if (found == std::string::npos) throw std::runtime_error("invalid generator");
    return unsigned(found);
}

Code word_code(const std::string& word) {
    Code code = 1;
    for (char c : word) code = (code << 2) | digit(c);
    return code;
}

unsigned length(Code code) { return (63 - __builtin_clzll(code)) / 2; }

std::string word(Code code) {
    std::string out(length(code), 'x');
    for (auto it = out.rbegin(); it != out.rend(); ++it, code >>= 2) *it = alphabet[code & 3];
    return out;
}

unsigned transformed(unsigned c, unsigned symmetry) {
    const unsigned new_generator = (c >> 1) ^ (symmetry >> 2);
    return 2 * new_generator + ((c ^ (symmetry >> (c >> 1))) & 1);
}

// The leading sentinel and first-coordinate length make pair keys injective.
// Numerical word ordering is by length then digit order, which is sufficient.
Code pack(Code a, Code b) {
    if (a > b) std::swap(a, b);
    const auto sa = length(a), sb = length(b);
    return ((((Code(32 + sa) << (2 * sa)) | (a ^ (Code(1) << (2 * sa)))) << (2 * sb))
            | (b ^ (Code(1) << (2 * sb))));
}

std::pair<Code, Code> unpack(Code key) {
    const unsigned sum = (63 - __builtin_clzll(key) - 5) / 2;
    const unsigned sa = (key >> (2 * sum)) & 31;
    const unsigned sb = sum - sa;
    const Code first_flag = Code(1) << (2 * sa), second_flag = Code(1) << (2 * sb);
    return {first_flag | ((key >> (2 * sb)) & (first_flag - 1)),
            second_flag | (key & (second_flag - 1))};
}

Code cyclic_key(Code letters, unsigned size) {
    const unsigned shift = 2 * (size - 1);
    const Code mask = (Code(1) << (2 * size)) - 1;
    Code other = 0, best = letters;
    for (unsigned i = 0; i < size; ++i) other = (other << 2) | (((letters >> (2 * i)) & 3) ^ 1);
    for (unsigned i = 0; i < size; ++i) {
        best = std::min({best, letters, other});
        letters = ((letters << 2) & mask) | (letters >> shift);
        other = ((other << 2) & mask) | (other >> shift);
    }
    return best | (mask + 1);
}

Orbit build_orbit(Code code) {
    const auto size = length(code);
    Orbit result{};
    for (unsigned i = 0; i < size; ++i) {
        const auto c = unsigned((code >> (2 * i)) & 3);
        for (unsigned symmetry = 0; symmetry < result.size(); ++symmetry)
            result[symmetry] |= Code(transformed(c, symmetry)) << (2 * i);
    }
    for (auto& value : result) value = cyclic_key(value, size);
    return result;
}

Code orbit_key(const Orbit& a, const Orbit& b) {
    Code key = std::numeric_limits<Code>::max();
    for (unsigned i = 0; i < a.size(); ++i) key = std::min(key, pack(a[i], b[i]));
    return key;
}

bool primitive(const std::string& cyclic) {
    int a = 0, b = 0;
    for (char c : cyclic) {
        if (c == 'x') ++a; else if (c == 'X') --a; else if (c == 'y') ++b; else --b;
    }
    return size_t(std::abs(a) + std::abs(b)) == cyclic.size() && std::gcd(std::abs(a), std::abs(b)) == 1
        && [&] {
            // Standard positive Euclidean primitive in the prescribed slope.
            std::vector<bool> replace_y;
            int p = std::abs(a), q = std::abs(b);
            while (p && q && p != q) {
                replace_y.push_back(p > q);
                if (p > q) p -= q; else q -= p;
            }
            std::string model = !p ? "y" : !q ? "x" : "xy";
            for (auto op = replace_y.rbegin(); op != replace_y.rend(); ++op) {
                std::string next;
                for (char c : model) {
                    if (c == (*op ? 'y' : 'x')) next += "xy"; else next += c;
                }
                model = std::move(next);
            }
            for (auto& c : model) if ((c == 'x' && a < 0) || (c == 'y' && b < 0)) c = invchar(c);
            return (model + model).find(cyclic) != std::string::npos;
        }();
}

struct Worker {
    uint64_t candidates = 0, admitted = 0;
    std::unordered_map<Code, Orbit> orbit_cache;
    std::unordered_map<Code, std::vector<std::string>> rotation_cache;
    std::map<int, std::vector<std::pair<std::string, std::string>>> tails;
    std::unordered_set<Code> next;

    const Orbit& orbit(Code code) {
        const auto [it, created] = orbit_cache.try_emplace(code);
        if (created) it->second = build_orbit(code);
        return it->second;
    }

    void scan(Code key, int cap) {
        if (orbit_cache.size() > 32768) orbit_cache.clear();
        if (rotation_cache.size() > 8192) rotation_cache.clear();
        const auto unpacked = unpack(key);
        const Code codes[2]{unpacked.first, unpacked.second};
        const std::string coordinates[2]{word(codes[0]), word(codes[1])};
        for (unsigned i = 0; i < 2; ++i)
            if (!rotation_cache.count(codes[i])) rotation_cache.emplace(codes[i], variants(coordinates[i]));
        for (unsigned i = 0; i < 2; ++i) {
            const auto& a = coordinates[i];
            const auto& b = coordinates[1 - i];
            const auto donor_orbit = orbit(codes[1 - i]);
            const int bound = std::max(0, (cap - int(a.size()) - 2 * int(b.size())) / 2);
            if (!tails.count(bound)) {
                auto& entries = tails[bound];
                for (const auto& tail : bridges(bound)) entries.emplace_back(tail, inverse(tail));
            }
            const size_t limit = cap - b.size();
            for (const auto& u : rotation_cache.at(codes[i]))
                for (const auto& v : rotation_cache.at(codes[1 - i]))
                    for (const auto& tail : tails.at(bound)) {
                        ++candidates;
                        auto product = tail.first.empty() ? round01::cyclic_product(u, v, limit)
                            : std::optional<std::string>(canonical(u + tail.first + v + tail.second));
                        if (!product || product->size() > limit) continue;
                        if (product->empty()) throw std::runtime_error("empty AC descendant coordinate");
                        ++admitted;
                        next.insert(orbit_key(orbit(word_code(*product)), donor_orbit));
                    }
        }
    }
};

int run(int cap, unsigned threads, const char* catalogue_path, const char* report_path) {
    if (cap < 13 || cap > 29 || !threads) throw std::runtime_error("need cap 13–29 and at least one worker");
    round01::check_product();
    const Code start = orbit_key(build_orbit(word_code("xxxYYYY")), build_orbit(word_code("xyxYXY")));
    std::vector<Code> states{start};
    std::unordered_set<Code> seen{start};
    std::vector<Worker> workers(threads);
    constexpr std::size_t block = 1024, window = 65536;
    std::size_t last_progress = 0;
    for (std::size_t at = 0; at < states.size();) {
        const auto end = std::min(at + window, states.size());
        std::atomic<std::size_t> cursor(at);
        std::vector<std::future<void>> jobs;
        for (auto& worker : workers) {
            jobs.push_back(std::async(std::launch::async, [&states, &worker, &cursor, end, cap] {
                for (;;) {
                    const auto from = cursor.fetch_add(block, std::memory_order_relaxed);
                    if (from >= end) return;
                    for (auto id = from; id < std::min(end, from + block); ++id) worker.scan(states.at(id), cap);
                }
            }));
        }
        for (auto& job : jobs) job.get();
        std::vector<Code> fresh;
        for (auto& worker : workers) {
            for (Code candidate : worker.next) if (seen.insert(candidate).second) fresh.push_back(candidate);
            worker.next.clear();
        }
        std::sort(fresh.begin(), fresh.end());
        states.insert(states.end(), fresh.begin(), fresh.end());
        at = end;
        if (at - last_progress >= window * 4 || at == states.size()) {
            std::cerr << "processed " << at << ", discovered " << states.size() << '\n';
            last_progress = at;
        }
    }
    std::sort(states.begin(), states.end());
    std::map<unsigned, uint64_t> histogram;
    uint64_t candidates = 0, admitted = 0, primitive_states = 0;
    for (const auto& worker : workers) { candidates += worker.candidates; admitted += worker.admitted; }
    std::ofstream catalogue(catalogue_path);
    unsigned minimum = cap;
    for (Code state : states) {
        const auto [a, b] = unpack(state);
        const auto x = word(a), y = word(b);
        if (pack(a, b) != state || orbit_key(build_orbit(a), build_orbit(b)) != state)
            throw std::runtime_error("invalid orbit representative");
        minimum = std::min(minimum, length(a));
        ++histogram[length(a) + length(b)];
        if (primitive(x) || primitive(y)) ++primitive_states;
        catalogue << x << '\t' << y << '\n';
    }
    catalogue.close();
    std::ofstream out(report_path);
    out << "{\n  \"status\":\"PASS\",\n  \"cyclic_cap\":" << cap
        << ",\n  \"signed_permutation_orbits\":" << states.size() << ",\n  \"primitive_coordinate_orbits\":"
        << primitive_states << ",\n  \"minimum_coordinate\":" << minimum
        << ",\n  \"rotation_product_candidates\":" << candidates << ",\n  \"admitted_neighbors\":" << admitted
        << ",\n  \"orbit_histogram\":{";
    bool first = true;
    for (const auto& [energy, count] : histogram) {
        if (!first) out << ',';
        first = false;
        out << '\"' << energy << "\":" << count;
    }
    out << "}\n}\n";
    if (!catalogue || !out) throw std::runtime_error("cannot write component or report");
    return 0;
}

int expand(const char* input_path, const char* output_path) {
    std::ifstream input(input_path);
    std::ofstream output(output_path);
    if (!input || !output) throw std::runtime_error("cannot open signed-orbit expansion files");
    std::unordered_map<Code, Orbit> orbit_cache;
    std::unordered_map<Code, std::string> literal_cache;
    auto images = [&](Code code) -> Orbit {
        const auto [it, fresh] = orbit_cache.try_emplace(code);
        if (fresh) it->second = build_orbit(code);
        return it->second;
    };
    auto literal = [&](Code code) -> const std::string& {
        const auto [it, fresh] = literal_cache.try_emplace(code);
        if (fresh) it->second = round01::canonical_reduced(word(code));
        return it->second;
    };
    std::map<unsigned, uint64_t> histogram;
    uint64_t rows = 0, distinct = 0;
    std::string row;
    while (std::getline(input, row)) {
        if (orbit_cache.size() > 65536) orbit_cache.clear();
        if (literal_cache.size() > 65536) literal_cache.clear();
        const auto mid = row.find('\t');
        if (mid == std::string::npos || !mid || mid + 1 == row.size() || row.size() > 30)
            throw std::runtime_error("invalid orbit row");
        const auto a = images(word_code(row.substr(0, mid))), b = images(word_code(row.substr(mid + 1)));
        std::array<Code, 8> keys{};
        for (unsigned i = 0; i < keys.size(); ++i) keys[i] = pack(a[i], b[i]);
        std::sort(keys.begin(), keys.end());
        const auto end = std::unique(keys.begin(), keys.end());
        ++histogram[unsigned(end - keys.begin())];
        for (auto it = keys.begin(); it != end; ++it) {
            const auto [first, second] = unpack(*it);
            const auto& p = literal(first);
            const auto& q = literal(second);
            output << std::min(p, q) << '\t' << std::max(p, q) << '\n';
            ++distinct;
        }
        ++rows;
    }
    if (input.bad() || !output || !rows) throw std::runtime_error("signed-orbit expansion I/O failed");
    std::cout << "{\n  \"input_orbits\":" << rows << ",\n  \"expanded_rows\":" << distinct << ",\n  \"multiplicities\":{";
    bool first = true;
    for (const auto& [size, count] : histogram) {
        if (!first) std::cout << ',';
        first = false;
        std::cout << '\"' << size << "\":" << count;
    }
    std::cout << "}\n}\n";
    return 0;
}
}

#ifndef AC_ROUND05_ORBITS_LIBRARY
int main(int argc, char** argv) {
    try {
        if (argc == 4 && std::string(argv[1]) == "expand") return orbit_search::expand(argv[2], argv[3]);
        if (argc != 5) throw std::runtime_error("usage: orbits cap threads catalogue.tsv report.json");
        return orbit_search::run(std::stoi(argv[1]), std::stoul(argv[2]), argv[3], argv[4]);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
#endif
