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

class RowIndex {
    const std::vector<Pair>& catalogue;
    std::unordered_map<Pair, uint32_t, Hash> hashed;
    std::vector<uint32_t> slots;

    static Code mix(Code value) {
        value ^= value >> 33;
        value *= 0xff51afd7ed558ccdULL;
        value ^= value >> 33;
        value *= 0xc4ceb9fe1a85ec53ULL;
        return value ^ (value >> 33);
    }

    size_t position(const Pair& key) const {
        const auto mask = slots.size() - 1;
        size_t at = (mix(key.first) ^ mix(key.second ^ 0x9e3779b97f4a7c15ULL)) & mask;
        while (slots[at] && catalogue[slots[at] - 1] != key) at = (at + 1) & mask;
        return at;
    }

public:
    static constexpr uint32_t missing = std::numeric_limits<uint32_t>::max();

    RowIndex(const std::vector<Pair>& rows, unsigned bits) : catalogue(rows) {
        if (bits > 32) throw std::runtime_error("flat verification index exponent exceeds 32");
        if (bits) slots.resize(size_t(1) << bits);
    }

    bool add(const Pair& key) {
        if (slots.empty()) return hashed.try_emplace(key, catalogue.size()).second;
        if (catalogue.size() >= slots.size() - slots.size() / 16)
            throw std::runtime_error("flat verification index reached its load limit");
        auto& slot = slots[position(key)];
        if (slot) return false;
        slot = uint32_t(catalogue.size()) + 1;
        return true;
    }

    uint32_t find(const Pair& key) const {
        if (!slots.empty()) {
            const auto slot = slots[position(key)];
            return slot ? slot - 1 : missing;
        }
        const auto it = hashed.find(key);
        return it == hashed.end() ? missing : it->second;
    }
};

Pair read_catalogue_row(const std::string& line, int cap, int input_cap) {
    const auto separator = line.find('\t');
    if (separator == std::string::npos || !separator || separator + 1 == line.size()
            || line.size() > size_t(input_cap + 1))
        throw std::runtime_error("invalid orbit catalogue row");
    const auto a = line.substr(0, separator), b = line.substr(separator + 1);
    if (a.size() > 31 || b.size() > 31 || cap - int(std::min(a.size(), b.size())) > 31)
        throw std::runtime_error("an input coordinate or allowed successor exceeds the packed word capacity");
    if (audit::cyclically_reduced(a) != a || audit::cyclically_reduced(b) != b)
        throw std::runtime_error("noncyclic input");
    const Pair key = signed_key(a, b);
    if (key != Pair{orbit_search::word_code(a), orbit_search::word_code(b)})
        throw std::runtime_error("noncanonical or repeated orbit");
    return key;
}

void load_catalogue(int cap, int input_cap, const char* catalogue, std::vector<Pair>& states,
                    RowIndex& ids, unsigned workers) {
    std::ifstream input(catalogue);
    if (!input) throw std::runtime_error("cannot open orbit catalogue");
    const auto before = states.size();
    const auto append = [&](const Pair& key) {
        if (states.size() == std::numeric_limits<uint32_t>::max())
            throw std::runtime_error("state index exhausted");
        if (!ids.add(key)) throw std::runtime_error("noncanonical or repeated orbit");
        states.push_back(key);
    };
    std::string line;
    if (workers == 1) {
        while (std::getline(input, line))
            append(read_catalogue_row(line, cap, input_cap));
    } else {
        constexpr size_t capacity = 1 << 20;
        std::vector<std::string> lines;
        std::vector<Pair> keys;
        lines.reserve(capacity);
        for (;;) {
            lines.clear();
            while (lines.size() < capacity && std::getline(input, line)) lines.push_back(line);
            if (lines.empty()) break;
            keys.resize(lines.size());
            std::vector<std::future<void>> jobs;
            for (unsigned i = 0; i < workers; ++i)
                jobs.push_back(std::async(std::launch::async, [&,i] {
                    for (size_t j = lines.size()*i/workers; j < lines.size()*(i+1)/workers; ++j)
                        keys[j] = read_catalogue_row(lines[j], cap, input_cap);
                }));
            for (auto& job : jobs) job.get();
            for (const auto& key : keys) append(key);
            if ((states.size()-before) % (64*capacity) == 0)
                std::cerr << "loaded " << states.size() << " cumulative catalogue rows\n";
        }
    }
    if (input.bad() || states.size() == before) throw std::runtime_error("empty or unreadable catalogue");
}

uint64_t check_seeds(const RowIndex& ids, int cap, size_t first_new, unsigned workers,
                     const char* manifest_path) {
    std::ifstream manifest(manifest_path);
    std::vector<std::string> paths;
    for (std::string path; std::getline(manifest, path);) {
        if (path.empty()) throw std::runtime_error("empty seed manifest entry");
        paths.push_back(std::move(path));
    }
    if (!manifest.eof() || paths.empty()) throw std::runtime_error("empty or unreadable seed manifest");
    std::atomic<size_t> next_path{0};
    std::vector<std::future<uint64_t>> jobs;
    for (size_t i = 0; i < std::min<size_t>(workers, paths.size()); ++i) {
        jobs.push_back(std::async(std::launch::async, [&] {
            using Record = std::array<Code, 4>;
            std::vector<Record> records(1 << 17);
            uint64_t checked = 0;
            for (size_t file = next_path++; file < paths.size(); file = next_path++) {
                std::ifstream input(paths[file], std::ios::binary);
                if (!input) throw std::runtime_error("cannot open seed shard");
                Pair previous{};
                for (;;) {
                    input.read(reinterpret_cast<char*>(records.data()), records.size() * sizeof(Record));
                    const auto bytes = input.gcount();
                    if (bytes % sizeof(Record)) throw std::runtime_error("truncated seed shard");
                    for (size_t j = 0; j < size_t(bytes) / sizeof(Record); ++j) {
                        const auto& row = records[j];
                        const Pair child{row[0], row[1]};
                        if (!child.first || !child.second || child <= previous
                            || int(orbit_search::length(child.first) + orbit_search::length(child.second)) != cap)
                            throw std::runtime_error("seed shard has unordered or out-of-scope keys");
                        previous = child;
                        const auto recipient = ids.find(child);
                        if (recipient == RowIndex::missing || recipient < first_new)
                            throw std::runtime_error("first-exit seed absent from the new catalogue");
                        const auto parent = ids.find({row[2], row[3]});
                        if (parent == RowIndex::missing || parent >= first_new)
                            throw std::runtime_error("first-exit anchor absent from the old catalogue");
                        ++checked;
                    }
                    if (input.eof()) break;
                    if (!input) throw std::runtime_error("unreadable seed shard");
                }
            }
            return checked;
        }));
    }
    uint64_t total = 0;
    for (auto& job : jobs) total += job.get();
    if (!total) throw std::runtime_error("empty seed index");
    return total;
}

int run(int cap, unsigned workers, const char* catalogue, const char* report,
        const std::string& first, const std::string& second, const char* lower = nullptr,
        unsigned index_bits = 0, const char* seed_manifest = nullptr, bool check_old_boundary = false,
        bool parallel_load = false) {
    if (cap < 13 || cap > 62 || !workers || (lower && cap < 14))
        throw std::runtime_error("need cap 13–62 and positive worker count; extensions begin at cap 14");
    audit::self_test();
    std::vector<Pair> states;
    RowIndex ids(states, index_bits);
    const unsigned loading_workers = parallel_load ? workers : 1;
    if (lower && lower[0] == '@') {
        std::ifstream manifest(lower + 1);
        if (!manifest) throw std::runtime_error("cannot open lower catalogue manifest");
        for (std::string path; std::getline(manifest, path);)
            load_catalogue(cap, cap - 1, path.c_str(), states, ids, loading_workers);
        if (manifest.bad() || states.empty()) throw std::runtime_error("empty or unreadable lower manifest");
    } else if (lower) {
        load_catalogue(cap, cap - 1, lower, states, ids, loading_workers);
    }
    const auto first_scanned = states.size();
    load_catalogue(cap, cap, catalogue, states, ids, loading_workers);
    const auto start_id = ids.find(signed_key(first, second));
    if (start_id == RowIndex::missing) throw std::runtime_error("root orbit absent from catalogue");
    std::cerr << "loaded " << states.size() << " orbits\n";
    const auto seeds_checked = seed_manifest ? check_seeds(ids, cap, first_scanned, workers, seed_manifest) : 0;
    if (seeds_checked) std::cerr << "checked " << seeds_checked << " first-exit seeds and anchors\n";
    compact_verify::Components components(states.size());
    if (lower) {
        if (start_id >= first_scanned) throw std::runtime_error("AK(3) missing from lower catalogue");
        for (uint32_t i = 0; i < first_scanned; ++i) components.join(start_id, i);
    }
    const size_t first_source = check_old_boundary ? 0 : first_scanned;
    std::atomic<std::size_t> cursor(first_source);
    const auto& lookup = ids;
    auto scan = [&]() {
        std::array<compact_verify::Totals, 2> counts{};
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
            if (begin >= states.size()) return counts;
            if ((begin - first_source) % (block * 8192) == 0)
                std::cerr << "checking orbit block starting at " << begin << '\n';
            for (auto i = begin; i < std::min(states.size(), begin + block); ++i) {
                const bool old_source = i < first_scanned;
                auto& totals = counts[old_source ? 0 : 1];
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
                                if (product.empty() || (old_source && int(product.size()) + donor != cap))
                                    continue;
                                ++totals.admitted;
                                const auto next = lookup.find(least_pair(orbit(product), donor_orbit));
                                if (next == RowIndex::missing) throw std::runtime_error("catalogue not closed");
                                neighbors.insert(next);
                            }
                }
                for (const auto neighbor : neighbors) components.join(i, neighbor);
            }
        }
    };
    std::vector<std::future<std::array<compact_verify::Totals, 2>>> jobs;
    for (unsigned i = 0; i < workers; ++i) jobs.push_back(std::async(std::launch::async, scan));
    std::array<compact_verify::Totals, 2> counts{};
    for (auto& job : jobs) {
        const auto batch = job.get();
        for (size_t i = 0; i < counts.size(); ++i) {
            counts[i].candidates += batch[i].candidates;
            counts[i].admitted += batch[i].admitted;
        }
    }
    const auto root = components.root(start_id);
    for (uint32_t i = first_scanned; i < states.size(); ++i)
        if (components.root(i) != root) throw std::runtime_error("catalogue not connected");
    std::ofstream out(report);
    out << "{\n  \"status\":\"" << (lower ? "NEW_ORBITS_CLOSED_AND_ATTACHED" : "CLOSED_AND_CONNECTED")
        << "\",\n  \"cyclic_cap\":" << cap << ",\n  \"signed_permutation_orbits\":" << states.size();
    if (lower) out << ",\n  \"lower_orbits_assumed_connected\":" << first_scanned
                   << ",\n  \"new_orbits_checked\":" << states.size() - first_scanned;
    if (seed_manifest) out << ",\n  \"first_exit_seeds_checked\":" << seeds_checked;
    if (check_old_boundary) out << ",\n  \"old_orbits_boundary_checked\":" << first_scanned
        << ",\n  \"old_rotation_product_candidates\":" << counts[0].candidates
        << ",\n  \"old_first_exit_admitted_products\":" << counts[0].admitted;
    out << ",\n  \"rotation_product_candidates\":" << counts[1].candidates
        << ",\n  \"admitted_neighbors\":" << counts[1].admitted << "\n}\n";
    if (!out) throw std::runtime_error("cannot write independent audit");
    return 0;
}
}

int main(int argc, char** argv) {
    try {
        const auto mode = argc > 1 ? std::string_view(argv[1]) : std::string_view{};
        if ((argc == 8 || argc == 9) &&
            (mode == "--flat-extend" || mode == "--flat-complete" || mode == "--parallel-complete")) {
            const auto bits = std::stoul(argv[7]);
            if (!bits || bits > 32) throw std::runtime_error("index exponent must be in [1,32]");
            return wide_verify::run(std::stoi(argv[2]), std::stoul(argv[3]), argv[5], argv[6],
                                    "xxxYYYY", "xyxYXY", argv[4], bits, argc == 9 ? argv[8] : nullptr,
                                    mode != "--flat-extend", mode == "--parallel-complete");
        }
        if (argc == 7 && std::string_view(argv[1]) == "--extend")
            return wide_verify::run(std::stoi(argv[2]), std::stoul(argv[3]), argv[5], argv[6],
                                    "xxxYYYY", "xyxYXY", argv[4]);
        if (argc != 5 && argc != 7)
            throw std::runtime_error("usage: wide-verify cap workers catalogue.tsv report.json [first second]; "
                                     "wide-verify --extend cap workers lower.tsv outside.tsv report.json; "
                                     "wide-verify --flat-extend|--flat-complete|--parallel-complete cap workers lower.tsv-or-@manifest outside.tsv report.json bits [seed-manifest]");
        return wide_verify::run(std::stoi(argv[1]), std::stoul(argv[2]), argv[3], argv[4],
                                argc == 5 ? "xxxYYYY" : argv[5], argc == 5 ? "xyxYXY" : argv[6]);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
