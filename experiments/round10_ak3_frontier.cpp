// Extend a complete cyclic AC component by one energy unit, preserving anchors.
#define AC_ROUND07_WIDE_ORBITS_LIBRARY
#include "round07_ak3_wide_orbits.cpp"

#include <filesystem>

namespace frontier {
using ak3_wide::Code;
using ak3_wide::Hash;
using ak3_wide::Pair;
using orbit_search::length;
using orbit_search::word;
using orbit_search::word_code;
using wide_orbits::energy;
constexpr auto no_parent = wide_orbits::no_parent;
constexpr std::size_t window = 1U << 17;
constexpr std::size_t block = 512;

Pair read_pair(const std::string& line, int cap) {
    const auto tab = line.find('\t');
    if (tab == std::string::npos || !tab || tab > 31 || tab + 1 == line.size()
        || line.size() - tab - 1 > 31 || line.size() > std::size_t(cap + 1))
        throw std::runtime_error("bad lower catalogue row");
    const auto a = word_code(line.substr(0, tab)), b = word_code(line.substr(tab + 1));
    if (a > b || length(a) + length(b) > unsigned(cap))
        throw std::runtime_error("lower catalogue row exceeds its scope");
    return {a, b};
}

unsigned common_prefix(Code a, Code b) {
    const auto difference = a ^ b;
    return difference ? unsigned(__builtin_clzll(difference)) / 2 : 32;
}

Code slice(Code left_aligned, unsigned start, unsigned count) {
    return count ? (left_aligned << (2 * start)) >> (64 - 2 * count) : 0;
}

struct Rotation { Code forward, backward; };

std::vector<Rotation> packed_rotations(Code code) {
    const auto size = length(code);
    const unsigned padding = 64 - 2 * size;
    const Code flag = Code(1) << (2 * size);
    const Code mask = flag - 1;
    Code forward = code ^ flag, backward = 0;
    for (unsigned i = 0; i < size; ++i) backward = (backward << 2) | (((forward >> (2 * i)) & 3) ^ 1);
    std::vector<Rotation> result;
    result.reserve(size);
    for (unsigned i = 0; i < size; ++i) {
        result.push_back({forward << padding, backward << padding});
        forward = ((forward << 2) & mask) | (forward >> (2 * size - 2));
        backward = (backward >> 2) | ((backward & 3) << (2 * size - 2));
    }
    return result;
}

// Canonical key of a cyclic product, provided its cyclic length is exact.
Code zero_product(Rotation u, unsigned n, Rotation v, unsigned m, unsigned wanted) {
    const auto first = std::min({n, m, common_prefix(u.backward, v.forward)});
    if (n + m - 2 * first < wanted) return 0;
    const auto second = std::min({n - first, m - first, common_prefix(u.forward, v.backward)});
    const unsigned a = n - first - second, b = m - first - second;
    if (a && b) {
        if (a + b != wanted) return 0;
        const auto bits = (slice(u.forward, second, a) << (2 * b)) | slice(v.forward, first, b);
        return orbit_search::cyclic_key(bits, wanted);
    }
    const Code source = a ? u.forward : v.forward;
    unsigned offset = a ? second : first, count = a + b;
    while (count > wanted && ((slice(source, offset, 1) ^ slice(source, offset + count - 1, 1)) == 1)) {
        ++offset;
        count -= 2;
    }
    if (count != wanted || (count > 1 && ((slice(source, offset, 1) ^ slice(source, offset + count - 1, 1)) == 1)))
        return 0;
    return orbit_search::cyclic_key(slice(source, offset, count), count);
}

struct BoundaryWorker {
    std::unordered_map<Code, std::vector<Rotation>> rotations;
    std::unordered_map<Code, orbit_search::Orbit> orbits;
    std::map<unsigned, std::vector<std::string>> exact_bridges;
    std::unordered_map<Pair, uint32_t, Hash> edges;
    orbit_search::Worker auditor;
    uint64_t zero_checks = 0, bridge_checks = 0, admitted = 0, wrong_parity = 0;

    const std::vector<Rotation>& variants_for(Code value) {
        const auto [entry, fresh] = rotations.try_emplace(value);
        if (fresh) entry->second = packed_rotations(value);
        return entry->second;
    }

    const orbit_search::Orbit& orbit_for(Code value) {
        const auto [entry, fresh] = orbits.try_emplace(value);
        if (fresh) entry->second = orbit_search::build_orbit(value);
        return entry->second;
    }

    void scan(const Pair& state, uint32_t parent, unsigned cap, bool audit) {
        if (rotations.size() > 16384) rotations.clear();
        if (orbits.size() > 65536) orbits.clear();
        std::unordered_set<Pair, Hash> actual;
        const Code rows[2] = {state.first, state.second};
        for (unsigned i = 0; i < 2; ++i) {
            const Code recipient = rows[i], donor = rows[1 - i];
            const unsigned n = length(recipient), m = length(donor);
            if ((n ^ cap) & 1U) {
                ++wrong_parity;
                continue;
            }
            const auto& us = variants_for(recipient);
            const auto& vs = variants_for(donor);
            const auto donor_orbit = orbit_for(donor);
            const unsigned wanted = cap - m;
            auto accept = [&](Code code) {
                ++admitted;
                const auto key = ak3_wide::least_image(orbit_for(code), donor_orbit);
                const auto [entry, added] = edges.try_emplace(key, parent);
                if (!added) entry->second = std::min(entry->second, parent);
                if (audit) actual.insert(key);
            };
            if (n + 2 * m >= cap) {
                zero_checks += 2 * us.size() * vs.size();
                for (auto u : us) for (auto v : vs) {
                    if (const auto p = zero_product(u, n, v, m, wanted)) accept(p);
                    if (const auto p = zero_product(u, n, {v.backward, v.forward}, m, wanted)) accept(p);
                }
                continue;
            }
            const unsigned bridge_size = (cap - n - 2 * m) / 2;
            const auto [entry, fresh] = exact_bridges.try_emplace(bridge_size);
            if (fresh) for (auto bridge : bridges(bridge_size))
                if (bridge.size() == bridge_size) entry->second.push_back(std::move(bridge));
            const auto& tails = entry->second;
            bridge_checks += 2 * us.size() * vs.size() * tails.size();
            for (auto u : us) for (auto v : vs) for (unsigned sign = 0; sign < 2; ++sign) {
                if (sign) std::swap(v.forward, v.backward);
                for (const auto& tail : tails) {
                    const unsigned first = orbit_search::digit(tail.front());
                    const unsigned last = orbit_search::digit(tail.back());
                    if (first == slice(u.backward, 0, 1) || first == slice(u.forward, 0, 1)
                        || last == (slice(v.forward, 0, 1) ^ 1) || last == (slice(v.backward, 0, 1) ^ 1)) continue;
                    const auto uw = word((Code(1) << (2 * n)) | slice(u.forward, 0, n));
                    const auto vw = word((Code(1) << (2 * m)) | slice(v.forward, 0, m));
                    accept(word_code(round01::canonical_reduced(uw + tail + vw + inverse(tail))));
                }
            }
        }
        if (audit) {
            std::unordered_set<Pair, Hash> reference;
            auditor.scan_pair(state.first, state.second, cap, [&](const auto& product, const auto& donor) {
                if (length(product[0]) + length(donor[0]) == cap)
                    reference.insert(ak3_wide::least_image(product, donor));
            });
            if (reference != actual) throw std::runtime_error("boundary disagreement for " + word(state.first) + " " + word(state.second));
        }
    }
};

using Record = std::array<Code, 4>;

void write_edge(std::ostream& stream, const Pair& child, const Pair& parent) {
    const Record record{child.first, child.second, parent.first, parent.second};
    stream.write(reinterpret_cast<const char*>(record.data()), sizeof(record));
}

void write_anchored_route(const std::string& path, unsigned cap, const Pair& anchor,
                          const std::vector<Pair>& outside) {
    std::ofstream out(path);
    out << "{\n  \"cyclic_cap\":" << cap << ",\n  \"lower_anchor\":[\"" << word(anchor.first)
        << "\",\"" << word(anchor.second) << "\"],\n  \"orbit_route\":[";
    auto print = [&](const Pair& pair) { out << "[\"" << word(pair.first) << "\",\"" << word(pair.second) << "\"]"; };
    print(anchor);
    for (const auto& pair : outside) {
        out << ',';
        print(pair);
    }
    out << "]\n}\n";
    if (!out) throw std::runtime_error("could not write anchored route");
}

struct PrimitiveScan {
    std::unordered_map<Code, bool> cache;
    bool test(const Pair& pair) {
        if (cache.size() > 131072) cache.clear();
        auto primitive = [&](Code code) {
            const auto [entry, fresh] = cache.try_emplace(code);
            if (fresh) entry->second = orbit_search::primitive(word(code));
            return entry->second;
        };
        return primitive(pair.first) || primitive(pair.second);
    }
};

int seeds(unsigned cap, unsigned workers, const std::string& source, const std::string& prefix,
          uint64_t limit, uint64_t offset, bool audit) {
    const auto filesize = std::filesystem::file_size(source);
    if (offset > filesize) throw std::runtime_error("offset exceeds input size");
    std::ifstream input(source, std::ios::binary);
    std::ofstream output(prefix + ".boundary.bin", std::ios::binary);
    if (!input || !output) throw std::runtime_error("unable to open seed files");
    if (offset) {
        input.seekg(offset - 1);
        if (input.get() != '\n') throw std::runtime_error("seed offset is not at a line boundary");
    }
    std::vector<BoundaryWorker> locals(workers);
    std::vector<Pair> rows;
    rows.reserve(window);
    uint64_t processed = 0, next_offset = offset, records = 0, primitive_records = 0;
    PrimitiveScan primitiveness;
    for (;;) {
        rows.clear();
        std::string line;
        while (rows.size() < window && (!limit || processed + rows.size() < limit) && std::getline(input, line)) {
            const auto state = read_pair(line, cap - 1);
            if (cap - std::min(length(state.first), length(state.second)) > 31)
                throw std::runtime_error("boundary scan exceeds packed coordinate width");
            rows.push_back(state);
            next_offset += line.size() + 1;
        }
        if (rows.empty()) break;
        std::atomic<std::size_t> cursor(0);
        std::vector<std::future<void>> jobs;
        for (auto& local : locals) {
            jobs.push_back(std::async(std::launch::async, [&local, &cursor, &rows, cap, audit] {
                for (;;) {
                    const auto from = cursor.fetch_add(block, std::memory_order_relaxed);
                    if (from >= rows.size()) return;
                    for (auto i = from; i < std::min(from + block, rows.size()); ++i) local.scan(rows[i], i, cap, audit);
                }
            }));
        }
        for (auto& job : jobs) job.get();
        std::vector<std::pair<Pair, uint32_t>> batch;
        for (auto& local : locals) {
            batch.insert(batch.end(), local.edges.begin(), local.edges.end());
            local.edges.clear();
        }
        std::sort(batch.begin(), batch.end());
        Pair previous{};
        for (const auto& [child, owner] : batch) {
            if (child == previous) continue;
            previous = child;
            write_edge(output, child, rows[owner]);
            ++records;
            if (primitiveness.test(child)) {
                if (!primitive_records++) write_anchored_route(prefix + ".seed-primitive.route.json", cap, rows[owner], {child});
            }
        }
        processed += rows.size();
        output.flush();
        const bool reached_eof = next_offset == filesize;
        uint64_t zero_checks = 0, bridge_checks = 0, admitted = 0, wrong_parity = 0;
        for (const auto& local : locals) {
            zero_checks += local.zero_checks;
            bridge_checks += local.bridge_checks;
            admitted += local.admitted;
            wrong_parity += local.wrong_parity;
        }
        const auto snapshot = prefix + ".boundary.json";
        std::ofstream report(snapshot + ".next");
        report << "{\n  \"cyclic_cap\":" << cap << ",\n  \"source_size\":" << filesize
               << ",\n  \"start_offset\":" << offset << ",\n  \"next_offset\":" << next_offset
               << ",\n  \"source_rows_scanned\":" << processed << ",\n  \"source_reached_eof\":" << (reached_eof ? "true" : "false")
               << ",\n  \"source_boundary_independently_compared\":" << (audit ? "true" : "false")
               << ",\n  \"recipient_parity_skips\":" << wrong_parity << ",\n  \"zero_bridge_rotation_checks\":" << zero_checks
               << ",\n  \"positive_bridge_rotation_checks\":" << bridge_checks << ",\n  \"admitted_candidates\":" << admitted
               << ",\n  \"boundary_records\":" << records << ",\n  \"primitive_boundary_records\":" << primitive_records << "\n}\n";
        report.close();
        if (!output || !report) throw std::runtime_error("unable to checkpoint seed files");
        std::filesystem::rename(snapshot + ".next", snapshot);
        if (!(processed % (window * 8)) || reached_eof || processed == limit)
            std::cerr << "boundary source rows " << processed << ", records " << records << ", next byte " << next_offset << '\n';
        if (primitive_records || reached_eof || (limit && processed == limit)) break;
    }
    if (input.bad() || !processed) throw std::runtime_error("empty or unreadable lower catalogue segment");
    return 0;
}

struct ExpansionWorker {
    orbit_search::Worker menu;
    std::unordered_map<Pair, uint32_t, Hash> discovered;
};

class OrbitMembership {
    std::unordered_set<Pair, Hash> nodes;
    std::vector<Pair> slots;
    size_t used = 0;

    size_t position(const Pair& state) const {
        const size_t mask = slots.size() - 1;
        // The original hash is used with prime-sized tables. Mix the entire key
        // before masking, since adjacent packed words have correlated low bits.
        Code hash = Hash{}(state);
        hash = (hash ^ (hash >> 30)) * 0xbf58476d1ce4e5b9ULL;
        hash = (hash ^ (hash >> 27)) * 0x94d049bb133111ebULL;
        auto index = (hash ^ (hash >> 31)) & mask;
        while (slots[index].first && slots[index] != state) index = (index + 1) & mask;
        return index;
    }

public:
    explicit OrbitMembership(unsigned capacity_bits) {
        if (capacity_bits) slots.resize(size_t(1) << capacity_bits);
    }

    void reserve(size_t count) {
        if (slots.empty()) nodes.reserve(count);
    }

    bool insert(const Pair& state) {
        if (slots.empty()) return nodes.insert(state).second;
        const auto index = position(state);
        if (slots[index].first) return false;
        if (used >= slots.size() * 4 / 5)
            throw std::runtime_error("flat orbit catalogue reached its load limit");
        slots[index] = state;
        ++used;
        return true;
    }

    bool count(const Pair& state) const {
        return slots.empty() ? nodes.count(state) != 0 : slots[position(state)].first != 0;
    }

    size_t size() const { return slots.empty() ? nodes.size() : used; }
};

int expand(unsigned cap, unsigned workers, const std::string& source, const std::string& prefix,
           uint64_t limit, int count, char** files, unsigned known_bits = 0, unsigned outside_bits = 0) {
    std::vector<std::string> sources;
    if (known_bits && !source.empty() && source.front() == '@') {
        std::ifstream manifest(source.substr(1));
        for (std::string path; std::getline(manifest, path);) {
            if (path.empty()) throw std::runtime_error("empty entry in lower catalogue manifest");
            sources.push_back(std::move(path));
        }
        if (manifest.bad() || sources.empty()) throw std::runtime_error("invalid lower catalogue manifest");
    } else {
        sources.push_back(source);
    }
    OrbitMembership known(known_bits);
    if (!known_bits) {
        uint64_t bytes = 0;
        for (const auto& path : sources) bytes += std::filesystem::file_size(path);
        known.reserve(bytes / cap);
    }
    for (const auto& path : sources) {
        std::ifstream input(path);
        if (!input) throw std::runtime_error("unable to open lower catalogue");
        for (std::string line; std::getline(input, line);)
            if (!known.insert(read_pair(line, cap - 1))) throw std::runtime_error("duplicate lower state");
        if (input.bad()) throw std::runtime_error("unreadable lower catalogue");
    }
    if (!known.size()) throw std::runtime_error("empty lower catalogue union");
    if (known_bits) std::cerr << "loaded " << known.size() << " lower orbits\n";
    std::vector<Pair> states, anchors;
    std::vector<uint32_t> parents;
    std::vector<uint64_t> seed_ends;
    OrbitMembership outside(outside_bits);
    if (outside_bits) {
        uint64_t records = 0;
        for (int i = 0; i < count; ++i) {
            const auto bytes = std::filesystem::file_size(files[i]);
            if (bytes % sizeof(Record)) throw std::runtime_error("truncated compact seed file");
            records += bytes / sizeof(Record);
            seed_ends.push_back(records);
        }
        if (records >= no_parent) throw std::runtime_error("compact seed count exceeds the ancestry index");
        const auto reserve = std::min<uint64_t>(no_parent - 1, records + records / 16);
        states.reserve(reserve);
    }
    std::map<unsigned, uint64_t> histogram;
    PrimitiveScan primitiveness;
    uint32_t primitive_node = no_parent;
    auto add = [&](const Pair& state, uint32_t parent) {
        if (!outside.insert(state)) return false;
        if (states.size() == no_parent) throw std::runtime_error("frontier state index exhausted");
        const uint32_t index = states.size();
        states.push_back(state);
        if (parent != no_parent) parents.push_back(parent);
        ++histogram[energy(state)];
        if (primitive_node == no_parent && primitiveness.test(state)) primitive_node = index;
        return true;
    };
    uint64_t total_seed_records = 0;
    for (int i = 0; i < count; ++i) {
        std::ifstream records(files[i], std::ios::binary);
        if (!records) throw std::runtime_error("unable to open boundary records");
        Record raw{};
        while (records.read(reinterpret_cast<char*>(raw.data()), sizeof(raw))) {
            const Pair child{raw[0], raw[1]}, parent{raw[2], raw[3]};
            if (!child.first || !child.second || energy(child) != cap || !known.count(parent))
                throw std::runtime_error("boundary record is outside scope");
            const bool inserted = add(child, no_parent);
            if (outside_bits && !inserted) throw std::runtime_error("flat expansion needs distinct compact seeds");
            if (!outside_bits && inserted) anchors.push_back(parent);
            ++total_seed_records;
        }
        if (!records.eof() || records.gcount()) throw std::runtime_error("truncated boundary file");
    }
    const auto seed_count = states.size();
    if (outside_bits && seed_count != seed_ends.back())
        throw std::runtime_error("compact seed counts disagree");
    if (outside_bits) std::cerr << "loaded " << seed_count << " compact seeds\n";
    std::vector<ExpansionWorker> locals(workers);
    std::size_t at = 0;
    const auto& membership = outside;
    for (; at < states.size() && primitive_node == no_parent && (!limit || at < limit);) {
        const auto end = std::min({at + window, states.size(), limit ? std::size_t(limit) : states.size()});
        std::atomic<std::size_t> cursor(at);
        std::vector<std::future<void>> jobs;
        for (auto& local : locals) {
            jobs.push_back(std::async(std::launch::async, [&local, &cursor, &states, &known, &membership, end, cap] {
                for (;;) {
                    const auto from = cursor.fetch_add(block, std::memory_order_relaxed);
                    if (from >= end) return;
                    for (auto index = from; index < std::min(from + block, end); ++index) {
                        const auto [a, b] = states[index];
                        if (cap - std::min(length(a), length(b)) > 31)
                            throw std::runtime_error("outward product exceeds packed coordinate width");
                        local.menu.scan_pair(a, b, cap, [&](const auto& product, const auto& donor) {
                            const auto candidate = ak3_wide::least_image(product, donor);
                            if ((energy(candidate) < cap && known.count(candidate)) || membership.count(candidate)) return;
                            const auto [entry, fresh] = local.discovered.try_emplace(candidate, index);
                            if (!fresh) entry->second = std::min(entry->second, uint32_t(index));
                        });
                    }
                }
            }));
        }
        for (auto& job : jobs) job.get();
        std::vector<std::pair<Pair, uint32_t>> batch;
        for (auto& local : locals) {
            batch.insert(batch.end(), local.discovered.begin(), local.discovered.end());
            local.discovered.clear();
        }
        std::sort(batch.begin(), batch.end());
        for (const auto& [state, parent] : batch) add(state, parent);
        at = end;
        if (!(at % (window * 8)) || at == states.size() || at == limit)
            std::cerr << "outward rows " << at << ", discovered " << states.size() << '\n';
    }
    auto seed_anchor = [&](uint32_t index) {
        if (!outside_bits) return anchors.at(index);
        const auto file = std::upper_bound(seed_ends.begin(), seed_ends.end(), index) - seed_ends.begin();
        const auto base = file ? seed_ends[file - 1] : 0;
        std::ifstream input(files[file], std::ios::binary);
        input.seekg((index - base) * sizeof(Record));
        Record record{};
        if (!input.read(reinterpret_cast<char*>(record.data()), sizeof(Record))
            || Pair{record[0], record[1]} != states[index])
            throw std::runtime_error("could not retrieve compact seed anchor");
        return Pair{record[2], record[3]};
    };
    auto route = [&](uint32_t index, const std::string& name) {
        std::vector<Pair> steps;
        for (;;) {
            steps.push_back(states[index]);
            if (index < seed_count) break;
            index = parents.at(index - seed_count);
        }
        std::reverse(steps.begin(), steps.end());
        write_anchored_route(prefix + name, cap, seed_anchor(index), steps);
    };
    if (primitive_node != no_parent) route(primitive_node, ".primitive.route.json");
    if (!states.empty()) {
        const auto smallest = std::min_element(states.begin(), states.end(), wide_orbits::catalogue_order);
        route(smallest - states.begin(), ".minimum.route.json");
    }
    std::ofstream ledger(prefix + ".outside.parents.bin", std::ios::binary);
    if (!ledger) throw std::runtime_error("unable to write expansion ledger");
    if (outside_bits) {
        for (int i = 0; i < count; ++i) {
            if (seed_ends[i] == (i ? seed_ends[i - 1] : 0)) continue;
            std::ifstream seeds(files[i], std::ios::binary);
            ledger << seeds.rdbuf();
            if (!seeds || !ledger) throw std::runtime_error("could not copy compact seed anchors");
        }
    } else {
        for (std::size_t index = 0; index < seed_count; ++index)
            write_edge(ledger, states[index], anchors[index]);
    }
    for (std::size_t index = seed_count; index < states.size(); ++index)
        write_edge(ledger, states[index], states[parents.at(index - seed_count)]);
    ledger.close();
    std::sort(states.begin(), states.end(), wide_orbits::catalogue_order);
    std::ofstream output(prefix + ".outside.tsv");
    for (const auto& [a, b] : states) output << word(a) << '\t' << word(b) << '\n';
    output.close();
    uint64_t candidates = 0, admitted = 0;
    for (const auto& local : locals) {
        candidates += local.menu.candidates;
        admitted += local.menu.admitted;
    }
    std::ofstream report(prefix + ".outside.json");
    report << "{\n  \"cyclic_cap\":" << cap << ",\n  \"lower_orbits\":" << known.size()
           << ",\n  \"boundary_records_read\":" << total_seed_records << ",\n  \"unique_seed_orbits\":" << seed_count
           << ",\n  \"expanded_orbits\":" << at << ",\n  \"outside_orbits\":" << states.size()
           << ",\n  \"closure_reached_from_listed_seeds\":" << (at == states.size() ? "true" : "false")
           << ",\n  \"primitive_found\":" << (primitive_node == no_parent ? "false" : "true")
           << ",\n  \"candidate_products\":" << candidates << ",\n  \"admitted_products\":" << admitted
           << ",\n  \"outside_histogram\":{";
    bool first = true;
    for (const auto& [size, population] : histogram) {
        if (!first) report << ',';
        first = false;
        report << '"' << size << "\":" << population;
    }
    report << "}\n}\n";
    if (!ledger || !output || !report) throw std::runtime_error("frontier output failed");
    return 0;
}
}  // namespace frontier

int main(int argc, char** argv) {
    try {
        if (argc < 8)
            throw std::runtime_error("usage: frontier seed cap workers lower.tsv prefix row-limit byte-offset [audit]; frontier expand cap workers lower.tsv prefix row-limit boundary.bin ...; frontier expand-flat cap workers lower.tsv-or-@manifest prefix row-limit lower-bits outside-bits boundary.bin ...");
        const unsigned cap = std::stoul(argv[2]), workers = std::stoul(argv[3]);
        if (cap < 14 || cap > 62 || !workers) throw std::runtime_error("need cap 14–62 and at least one worker");
        const auto limit = std::stoull(argv[6]);
        if (std::string_view(argv[1]) == "seed" && (argc == 8 || (argc == 9 && std::string_view(argv[8]) == "audit")))
            return frontier::seeds(cap, workers, argv[4], argv[5], limit, std::stoull(argv[7]), argc == 9);
        if (cap > 33) throw std::runtime_error("expansion needs cap at most 33");
        if (std::string_view(argv[1]) == "expand" && cap <= 32)
            return frontier::expand(cap, workers, argv[4], argv[5], limit, argc - 7, argv + 7);
        if (std::string_view(argv[1]) == "expand-flat" && argc >= 10) {
            const unsigned known_bits = std::stoul(argv[7]), outside_bits = std::stoul(argv[8]);
            if (!known_bits || !outside_bits || known_bits > 32 || outside_bits > 32)
                throw std::runtime_error("flat catalogue capacity exponents must be 1–32");
            return frontier::expand(cap, workers, argv[4], argv[5], limit, argc - 9, argv + 9,
                                    known_bits, outside_bits);
        }
        throw std::runtime_error("unrecognized frontier command");
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
