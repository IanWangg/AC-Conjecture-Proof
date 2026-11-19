// Explore rank-three excursions between singleton charts of any marked letter.
#define AC_ROUND04_EXCURSION_LIBRARY
#include "round04_stable_proof_excursions.cpp"

#include <atomic>
#include <future>
#include <unordered_set>

namespace {

using Code = uint64_t;
using Key = __uint128_t;
using Images = std::array<Code, 48>;
constexpr std::string_view alphabet = "XYZxyz";

struct KeyHash {
    size_t operator()(Key key) const {
        uint64_t mixed = uint64_t(key) ^ (uint64_t(key >> 64) * 0x9e3779b97f4a7c15ULL);
        mixed = (mixed ^ (mixed >> 30)) * 0xbf58476d1ce4e5b9ULL;
        mixed = (mixed ^ (mixed >> 27)) * 0x94d049bb133111ebULL;
        return mixed ^ (mixed >> 31);
    }
};

Code encode(std::string_view word) {
    Code result = 1;
    for (char c : word) {
        const auto digit = alphabet.find(c);
        if (digit == std::string_view::npos) throw std::logic_error("invalid rank-three letter");
        result = (result << 3) | digit;
    }
    return result;
}

unsigned length(Code word) { return unsigned(63 - __builtin_clzll(word)) / 3; }

std::string decode(Code word) {
    std::string result(length(word), 'X');
    for (auto iter = result.rbegin(); iter != result.rend(); ++iter, word >>= 3)
        *iter = alphabet[word & 7];
    return result;
}

Key pack(Code a, Code b, Code c) {
    if (b < a) std::swap(a, b);
    if (c < b) std::swap(b, c);
    if (b < a) std::swap(a, b);
    const unsigned la = length(a), lb = length(b), lc = length(c);
    const auto a_flag = Code(1) << (3 * la), b_flag = Code(1) << (3 * lb);
    const auto c_flag = Code(1) << (3 * lc);
    Key result = ((Key(1) << 10) | (la << 5) | lb);
    result = (result << (3 * la)) | (a ^ a_flag);
    result = (result << (3 * lb)) | (b ^ b_flag);
    return (result << (3 * lc)) | (c ^ c_flag);
}

std::array<Code, 3> unpack(Key key) {
    const Code high = Code(key >> 64);
    const auto top = high ? 127 - __builtin_clzll(high) : 63 - __builtin_clzll(Code(key));
    const unsigned total = (top - 10) / 3;
    const unsigned meta = unsigned(key >> (3 * total));
    const unsigned la = (meta >> 5) & 31, lb = meta & 31, lc = total - la - lb;
    std::array<Code, 3> result;
    const unsigned lengths[3]{la, lb, lc};
    for (int i = 2; i >= 0; --i) {
        const unsigned bits = 3 * lengths[i];
        const Code flag = Code(1) << bits;
        result[i] = flag | (Code(key) & (flag - 1));
        key >>= bits;
    }
    return result;
}

std::array<std::array<char, 6>, 48> signed_actions() {
    std::array<std::array<char, 6>, 48> actions;
    std::array<char, 3> permutation{'X', 'Y', 'Z'};
    size_t index = 0;
    do {
        for (unsigned signs = 0; signs < 8; ++signs) {
            auto& action = actions[index++];
            for (unsigned i = 0; i < 3; ++i) {
                action[i] = (signs & (1 << i)) ? invchar(permutation[i]) : permutation[i];
                action[i + 3] = invchar(action[i]);
            }
        }
    } while (std::next_permutation(permutation.begin(), permutation.end()));
    return actions;
}

const auto actions = signed_actions();

struct WordOrbit {
    Images images;
    Code best = std::numeric_limits<Code>::max();
    uint64_t best_positions = 0;
};

class CompactOrbits {
    std::unordered_map<Code, WordOrbit> cache;

public:
    void limit() { if (cache.size() > 16384) cache.clear(); }

    const WordOrbit& word(Code key) {
        auto [found, inserted] = cache.try_emplace(key);
        if (inserted) {
            const auto text = decode(key);
            for (size_t action = 0; action < actions.size(); ++action) {
                auto changed = text;
                for (auto& c : changed) c = actions[action][alphabet.find(c)];
                const auto image = encode(canonical(std::move(changed)));
                auto& entry = found->second;
                entry.images[action] = image;
                if (image < entry.best) {
                    entry.best = image;
                    entry.best_positions = 0;
                }
                if (image == entry.best) entry.best_positions |= uint64_t(1) << action;
            }
        }
        return found->second;
    }
};

Key orbit(const Images& a, const Images& b, const Images& c) {
    Key answer = pack(a[0], b[0], c[0]);
    for (size_t i = 1; i < actions.size(); ++i)
        answer = std::min(answer, pack(a[i], b[i], c[i]));
    return answer;
}

Key compact_orbit(const WordOrbit& a, const WordOrbit& b, const WordOrbit& c) {
    // Packing metadata only records lengths. The least first sorted word
    // therefore restricts the ambient actions that can give the least key.
    const auto first = std::min({a.best, b.best, c.best});
    uint64_t positions = (a.best == first ? a.best_positions : 0)
                       | (b.best == first ? b.best_positions : 0)
                       | (c.best == first ? c.best_positions : 0);
    Key answer = ~Key(0);
    while (positions) {
        const auto index = __builtin_ctzll(positions);
        answer = std::min(answer, pack(a.images[index], b.images[index], c.images[index]));
        positions &= positions - 1;
    }
    return answer;
}

Triple rows_from(Key key) {
    const auto codes = unpack(key);
    Triple rows{decode(codes[0]), decode(codes[1]), decode(codes[2])};
    std::sort(rows.begin(), rows.end());
    return rows;
}

P erase_singleton(std::string_view a, std::string_view b, char letter) {
    std::array<char, 6> map{};
    constexpr std::string_view lower = "xyz";
    const auto removed = static_cast<char>(std::tolower(static_cast<unsigned char>(letter)));
    char destination = 'x';
    for (const auto c : lower) {
        if (c == removed) continue;
        map[alphabet.find(c)] = destination;
        map[alphabet.find(invchar(c))] = invchar(destination);
        ++destination;
    }
    const auto project = [&](std::string_view word) {
        std::string image;
        for (char c : word) {
            const char kept = map[alphabet.find(c)];
            if (kept) image += kept;
        }
        return canonical(std::move(image));
    };
    const auto p = project(a), q = project(b);
    if (p.empty() || q.empty()) throw std::logic_error("rank-two projection has a trivial row");
    return canonpair(p, q);
}

struct Worker {
    CompactOrbits orbits;
    std::unordered_map<Code, std::vector<std::string>> rotations;
    std::map<int, std::vector<P>> tails;
    std::unordered_set<Key, KeyHash> fresh;
    std::set<P> returns;
    uint64_t candidates = 0, admitted = 0, nonempty = 0;

    void scan(Key key, int cap) {
        orbits.limit();
        if (rotations.size() > 8192) rotations.clear();
        const auto codes = unpack(key);
        const Triple words{decode(codes[0]), decode(codes[1]), decode(codes[2])};
        if (pack(codes[0], codes[1], codes[2]) != key || length(codes[0]) < 2)
            throw std::logic_error("bad excursion node");
        const int total = int(energy(words));
        for (size_t i = 0; i < 3; ++i)
            if (!rotations.count(codes[i])) rotations.emplace(codes[i], variants(words[i]));
        for (size_t i = 0; i < 3; ++i) {
            std::unordered_set<Code> updates;
            for (size_t j = 0; j < 3; ++j) {
                if (i == j) continue;
                const int bound = std::max(0, (cap - total - int(words[j].size())) / 2);
                const size_t allowance = size_t(cap - total) + words[i].size();
                if (!tails.count(bound)) tails.emplace(bound, bridges_rank_three(bound));
                for (const auto& a : rotations.at(codes[i]))
                    for (const auto& b : rotations.at(codes[j]))
                        for (const auto& [tail, opposite] : tails.at(bound)) {
                            ++candidates;
                            std::optional<std::string> updated;
                            if (tail.empty()) {
                                updated = zero_bridge(a, b, allowance);
                            } else {
                                ++nonempty;
                                auto cyclic_word = cyclic(a + tail + b + opposite);
                                if (cyclic_word.size() <= allowance) updated = canonical(std::move(cyclic_word));
                            }
                            if (!updated) continue;
                            if (updated->empty()) throw std::logic_error("a rank-three row vanished");
                            ++admitted;
                            updates.insert(encode(*updated));
                        }
            }
            const size_t j = (i + 1) % 3, k = (i + 2) % 3;
            const auto& first = orbits.word(codes[j]);
            const auto& second = orbits.word(codes[k]);
            for (const auto word : updates) {
                if (length(word) == 1)
                    returns.insert(erase_singleton(words[j], words[k], decode(word)[0]));
                else
                    fresh.insert(compact_orbit(orbits.word(word), first, second));
            }
        }
    }
};

int explore(int cap, unsigned threads, const std::string& seeds, const std::string& prefix,
            const std::string& invariant) {
    auto allowed_pairs = [&]() {
        std::ifstream file(invariant);
        if (!file) throw std::runtime_error("cannot open rank-two invariant");
        std::set<P> pairs;
        P row;
        while (file >> row.first >> row.second) if (row.first.size() + row.second.size() < size_t(cap))
            pairs.insert(row);
        if (pairs.empty()) throw std::runtime_error("rank-two invariant is empty");
        return pairs;
    }();
    std::unordered_set<Key, KeyHash> seen;
    std::vector<Key> pending;
    CompactOrbits seed_orbits;
    std::ifstream input(seeds);
    if (!input) throw std::runtime_error("cannot open seeds");
    Triple seed;
    size_t literal_seeds = 0;
    while (input >> seed[0] >> seed[1] >> seed[2]) {
        for (const auto& row : seed)
            if (row.size() < 2 || canonical(row) != row) throw std::runtime_error("bad seed word");
        if (energy(seed) > size_t(cap)) throw std::runtime_error("seed exceeds cap");
        seed_orbits.limit();
        const auto key = compact_orbit(seed_orbits.word(encode(seed[0])), seed_orbits.word(encode(seed[1])),
                                       seed_orbits.word(encode(seed[2])));
        if (seen.insert(key).second) pending.push_back(key);
        ++literal_seeds;
    }
    if (pending.empty()) throw std::runtime_error("seed file is empty");
    const auto number_seeds = pending.size();
    constexpr size_t window = 65536, block = 512;
    std::vector<Worker> workers(threads);
    for (size_t at = 0, last = 0; at < pending.size();) {
        const auto end = std::min(at + window, pending.size());
        std::atomic<size_t> cursor(at);
        std::vector<std::future<void>> jobs;
        for (auto& worker : workers) {
            auto* local = &worker;
            jobs.push_back(std::async(std::launch::async, [&pending, local, &cursor, end, cap] {
                for (;;) {
                    const auto from = cursor.fetch_add(block, std::memory_order_relaxed);
                    if (from >= end) break;
                    for (auto i = from; i < std::min(from + block, end); ++i) local->scan(pending[i], cap);
                }
            }));
        }
        for (auto& job : jobs) job.get();
        std::vector<Key> fresh;
        for (auto& worker : workers) {
            for (const auto key : worker.fresh) if (seen.insert(key).second) fresh.push_back(key);
            worker.fresh.clear();
        }
        std::sort(fresh.begin(), fresh.end());
        pending.insert(pending.end(), fresh.begin(), fresh.end());
        at = end;
        if (at - last >= window * 4 || at == pending.size()) {
            std::cerr << "Processed " << at << ", discovered " << pending.size() << '\n';
            last = at;
        }
    }
    uint64_t candidates = 0, admitted = 0, nonempty = 0;
    std::set<P> possible_returns;
    for (const auto& worker : workers) {
        candidates += worker.candidates;
        admitted += worker.admitted;
        nonempty += worker.nonempty;
        possible_returns.insert(worker.returns.begin(), worker.returns.end());
    }
    std::set<P> expanded_returns;
    SignedPermutations rank_two_symmetries(true);
    for (const auto& [a, b] : possible_returns)
        for (const auto& point : rank_two_symmetries.orbit({a, b, "Z"})) {
            Triple copy = point;
            std::sort(copy.begin(), copy.end(), [](const auto& u, const auto& v) {
                return std::pair(u == "Z", u) < std::pair(v == "Z", v);
            });
            expanded_returns.emplace(copy[0], copy[1]);
        }
    std::ofstream returns_file(prefix + ".returns.tsv"), catalogue(prefix + ".states.tsv");
    if (!returns_file || !catalogue) throw std::runtime_error("cannot open scan outputs");
    size_t misses = 0;
    for (const auto& [a, b] : expanded_returns) {
        returns_file << a << '\t' << b << '\n';
        if (!allowed_pairs.count({a, b})) ++misses;
    }
    std::map<size_t, size_t> histogram;
    std::sort(pending.begin(), pending.end());
    size_t min_length = cap;
    for (const auto key : pending) {
        const auto rows = rows_from(key);
        write_tsv(catalogue, rows);
        ++histogram[energy(rows)];
        for (const auto& row : rows) min_length = std::min(min_length, row.size());
    }
    std::cout << "{\n  \"cap\": " << cap << ",\n  \"literal_seeds\": " << literal_seeds
              << ",\n  \"seed_orbits\": " << number_seeds
              << ",\n  \"state_orbits\": " << pending.size()
              << ",\n  \"minimum_row_length\": " << min_length
              << ",\n  \"candidates\": " << candidates
              << ",\n  \"nonempty_bridge_candidates\": " << nonempty
              << ",\n  \"admitted\": " << admitted
              << ",\n  \"reentry_projections\": " << expanded_returns.size()
              << ",\n  \"projections_outside_invariant\": " << misses
              << ",\n  \"orbit_histogram\": {";
    bool first = true;
    for (const auto& [size, count] : histogram) {
        std::cout << (first ? "" : ", ") << '"' << size << "\": " << count;
        first = false;
    }
    std::cout << "}\n}\n";
    return 0;
}

}

#ifndef AC_ROUND06_SINGLETON_LIBRARY
int main(int argc, char** argv) {
    try {
        if (argc != 6) throw std::runtime_error("usage: all_singleton cap threads seeds.tsv invariant.tsv prefix");
        const int cap = std::stoi(argv[1]);
        const unsigned threads = std::stoul(argv[2]);
        if (cap < 20 || cap > 22 || !threads) throw std::runtime_error("need cap 20–22 and a worker");
        return explore(cap, threads, argv[3], argv[5], argv[4]);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
#endif
