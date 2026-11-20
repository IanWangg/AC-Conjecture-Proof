// Bounded search through the one- and two-auxiliary-occurrence rank-three graph.
#define AC_ROUND16_PIVOT_LIBRARY
#include "round16_stable_proof_pivot.cpp"

namespace {

Key unmarked_rows(const Triple& rows) {
    return pack(encode(canonical(rows[0])), encode(canonical(rows[1])), encode(canonical(rows[2])));
}

struct AuxiliaryMarkings {
    using RowImages = std::array<Code, 16>;
    std::vector<std::array<char,6>> markings;
    std::unordered_map<Code, RowImages> cache;

    AuxiliaryMarkings() {
        for (const auto& map : actions)
            if (map[2] == 'Z' || map[2] == 'z') markings.push_back(map);
        if (markings.size() != 16) throw std::logic_error("wrong auxiliary marking count");
    }

    const RowImages& images(Code key) {
        auto [it, inserted] = cache.try_emplace(key);
        if (inserted) {
            const auto word = decode(key);
            for (size_t i = 0; i < markings.size(); ++i) {
                auto changed = word;
                for (auto& c : changed) c = markings[i][alphabet.find(c)];
                it->second[i] = encode(canonical(std::move(changed)));
            }
        }
        return it->second;
    }

    Key key(Key plain) {
        if (cache.size() > 300000) cache.clear();
        const auto words = unpack(plain);
        const auto& a = images(words[0]);
        const auto& b = images(words[1]);
        const auto& c = images(words[2]);
        Key least = ~Key(0);
        for (size_t i = 0; i < markings.size(); ++i)
            least = std::min(least, pack(a[i], b[i], c[i]));
        return least;
    }
};

std::string positive_tail(std::string word) {
    if (count_z(word) != 1) throw std::logic_error("expected one auxiliary occurrence");
    if (word.find('z') == std::string::npos) word = inverse(std::move(word));
    const auto at = word.find('z');
    return word.substr(at + 1) + word.substr(0, at);
}

struct TwoTailMenu {
    std::unordered_map<Code, std::vector<std::string>> rotations;
    std::map<int, std::vector<P>> tails;
    uint64_t product_candidates = 0;
    uint64_t difference_edges = 0;
    uint64_t width_omissions = 0;

    void scan(Key state, int cap, std::vector<Key>& result) {
        const auto rows = rows_from(state);
        // rows_from orders the text lexically, unlike the length-first packing.
        const std::array<Code,3> words{encode(rows[0]), encode(rows[1]), encode(rows[2])};
        const std::array<int,3> charges{count_z(rows[0]), count_z(rows[1]), count_z(rows[2])};
        const int support = charges[0] + charges[1] + charges[2];
        if (support < 1 || support > 2 || *std::max_element(charges.begin(), charges.end()) != 1)
            throw std::logic_error("invalid auxiliary support");
        const int total = int(energy(rows));
        if (rotations.size() > 16384) rotations.clear();
        for (size_t i = 0; i < rows.size(); ++i)
            if (!rotations.count(words[i])) rotations.emplace(words[i], variants(rows[i]));

        result.clear();
        const auto add = [&](size_t slot, const std::string& word) {
            if (word.empty()) throw std::logic_error("vanished relator");
            if (word.size() > 21) {
                ++width_omissions;
                return;
            }
            auto destination = words;
            destination[slot] = encode(word);
            result.push_back(pack(destination[0], destination[1], destination[2]));
        };
        for (size_t i = 0; i < rows.size(); ++i) {
            if (support == 2 && !charges[i]) continue;
            const size_t allowance = cap - total + rows[i].size();
            for (size_t j = 0; j < rows.size(); ++j) {
                if (i == j) continue;
                if (support == 2 && charges[j]) {
                    const auto difference = canonical(positive_tail(rows[i]) + inverse(positive_tail(rows[j])));
                    ++difference_edges;
                    if (difference.size() <= allowance) add(i, difference);
                    continue;
                }

                const int bound = std::max(0, (cap - total - int(rows[j].size())) / 2);
                auto [available, fresh] = tails.try_emplace(bound);
                if (fresh) {
                    for (const auto& bridge : bridges(bound))
                        available->second.emplace_back(bridge, inverse(bridge));
                }
                std::unordered_set<Code> admitted;
                for (const auto& a : rotations.at(words[i]))
                    for (const auto& b : rotations.at(words[j]))
                        for (const auto& [g, back] : available->second) {
                            ++product_candidates;
                            auto word = g.empty() ? zero_bridge(a, b, allowance)
                                                  : std::optional<std::string>(canonical(a + g + b + back));
                            if (!word || word->size() > allowance) continue;
                            if (word->empty()) throw std::logic_error("vanished relator");
                            if (word->size() > 21) {
                                ++width_omissions;
                                continue;
                            }
                            admitted.insert(encode(*word));
                        }
                for (const auto word : admitted) {
                    auto destination = words;
                    destination[i] = word;
                    result.push_back(pack(destination[0], destination[1], destination[2]));
                }
            }
        }
        std::sort(result.begin(), result.end());
        result.erase(std::unique(result.begin(), result.end()), result.end());
    }
};

// Independent stack reduction and all rank-three bridge labels for replay.
struct StackAudit {
    uint64_t product_candidates = 0, difference_edges = 0, width_omissions = 0;
    std::map<int, std::vector<P>> conjugators;

    void scan(Key state, int cap, std::vector<Key>& result) {
        const auto rows = rows_from(state);
        const int total = int(energy(rows));
        const int support = count_z(rows[0]) + count_z(rows[1]) + count_z(rows[2]);
        const std::array<std::vector<std::string>,3> signs{
            variants(rows[0]), variants(rows[1]), variants(rows[2])};
        result.clear();
        for (size_t i = 0; i < rows.size(); ++i) {
            for (size_t j = 0; j < rows.size(); ++j) {
                if (i == j) continue;
                const int bound = std::max(0, (cap - total - int(rows[j].size())) / 2);
                auto [available, fresh] = conjugators.try_emplace(bound);
                if (fresh) available->second = bridges_rank_three(bound);
                const size_t limit = cap - total + rows[i].size();
                std::unordered_set<std::string> admitted;
                for (const auto& a : signs[i])
                    for (const auto& b : signs[j])
                        for (const auto& [g, back] : available->second) {
                            ++product_candidates;
                            auto product = cyclic(a + g + b + back);
                            if (product.empty()) throw std::logic_error("vanished audit row");
                            if (product.size() > limit) continue;
                            const auto occurrences = count_z(product);
                            if (occurrences > 1 || support - count_z(rows[i]) + occurrences > 2)
                                continue;
                            if (product.size() > 21) {
                                ++width_omissions;
                                continue;
                            }
                            admitted.insert(canonical(std::move(product)));
                        }
                for (const auto& word : admitted) {
                    auto next = rows;
                    next[i] = word;
                    result.push_back(unmarked_rows(next));
                }
            }
        }
        std::sort(result.begin(), result.end());
        result.erase(std::unique(result.begin(), result.end()), result.end());
    }
};

template<class Menu>
int search_reverse(int cap, size_t budget, const std::string& forward, const std::string& roots,
                   const std::string& output, bool signed_markings) {
    if (cap < 3 || cap > 33 || !budget) throw std::invalid_argument("invalid search cap or budget");
    AuxiliaryMarkings orbit;
    const auto normalize = [&](Key plain) {
        return signed_markings ? orbit.key(plain) : plain;
    };
    std::unordered_map<Key,size_t,KeyHash> target;
    {
        std::ifstream in(forward);
        Triple rows;
        size_t parent, index = 0;
        while (in >> parent >> rows[0] >> rows[1] >> rows[2]) {
            if (!in_range(rows, 3, cap)) throw std::runtime_error("forward node outside width or energy");
            target.try_emplace(normalize(unmarked_rows(rows)), index++);
        }
        if (!in.eof() || target.empty()) throw std::runtime_error("invalid forward catalogue");
    }
    std::vector<Key> nodes, neighbors;
    std::vector<size_t> parents;
    std::unordered_set<Key,KeyHash> seen;
    auto add = [&](Key key, size_t parent) {
        if (!seen.insert(key).second) return;
        nodes.push_back(key);
        parents.push_back(parent);
    };
    max_z = 2;
    import(roots, [&](Key key) { add(normalize(unmarked_rows(ordered_rows(key))), seed_parent); }, 3, cap);
    const auto root_count = nodes.size();
    if (!root_count) throw std::runtime_error("no reverse roots");
    Menu menu;
    size_t expanded = 0, join = seed_parent;
    while (expanded < nodes.size() && expanded < budget && join == seed_parent) {
        if (target.count(nodes[expanded])) {
            join = expanded;
            break;
        }
        menu.scan(nodes[expanded], cap, neighbors);
        for (const auto raw : neighbors) {
            const auto point = normalize(raw);
            add(point, expanded);
            if (target.count(point)) {
                join = nodes.size() - 1;
                if (nodes[join] != point) throw std::logic_error("repeated unregistered join");
                break;
            }
        }
        ++expanded;
        if (expanded % 65536 == 0)
            std::cerr << "expanded " << expanded << ", discovered " << nodes.size() << '\n';
    }
    std::ofstream route(output);
    if (!route) throw std::runtime_error("cannot write the reverse route");
    for (size_t at = join; at != seed_parent; at = parents[at])
        write_tsv(route, rows_from(nodes[at]));
    if (expanded == nodes.size() && join == seed_parent) {
        auto sorted = nodes;
        std::sort(sorted.begin(), sorted.end());
        std::ofstream catalogue(output + ".states.tsv");
        for (const auto key : sorted) write_tsv(catalogue, rows_from(key));
        if (!catalogue) throw std::runtime_error("cannot write closed graph catalogue");
    }
    std::cout << "{\"roots\":" << root_count << ",\"forward_keys\":" << target.size()
              << ",\"expanded\":" << expanded << ",\"discovered\":" << nodes.size()
              << ",\"product_candidates\":" << menu.product_candidates
              << ",\"difference_edges\":" << menu.difference_edges
              << ",\"width_omissions\":" << menu.width_omissions << ",\"forward_anchor\":";
    if (join == seed_parent) std::cout << "null";
    else std::cout << target.at(nodes[join]);
    std::cout << ",\"closed\":" << (expanded == nodes.size() && join == seed_parent ? "true" : "false") << "}\n";
    return 0;
}

}

int main(int argc, char** argv) {
    try {
        bool signed_markings = false, audit = false;
        for (int i = 6; i < argc; ++i) {
            if (std::string_view(argv[i]) == "--signed") signed_markings = true;
            else if (std::string_view(argv[i]) == "--stack-audit") audit = true;
            else throw std::invalid_argument("unknown option");
        }
        if (argc < 6)
            throw std::invalid_argument("usage: two-tails cap budget forward.tsv roots.tsv route.tsv [--signed] [--stack-audit]");
        const auto cap = std::stoi(argv[1]);
        const auto budget = std::stoull(argv[2]);
        if (audit) return search_reverse<StackAudit>(cap, budget, argv[3], argv[4], argv[5], signed_markings);
        return search_reverse<TwoTailMenu>(cap, budget, argv[3], argv[4], argv[5], signed_markings);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
