// Check the finite cap enclosure using stack reduction and Booth rotation.
#define AC_ROUND06_SINGLETON_LIBRARY
#include "round06_stable_proof_all_singleton.cpp"
#define main rank_two_closure_main
#include "verify_full_cyclic_component.cpp"
#undef main

namespace {

char switch_case(char c) { return c ^ 32; }

std::string backward(const std::string& word) {
    std::string result(word.rbegin(), word.rend());
    for (auto& c : result) c = switch_case(c);
    return result;
}

std::string cyclic_stack(const std::string& a, const std::string& b,
                         const std::string& c, const std::string& d) {
    char stack[80];
    size_t right = 0;
    for (const auto* part : {&a, &b, &c, &d}) {
        for (const char letter : *part) {
            if (right > 0 && stack[right - 1] == switch_case(letter)) --right;
            else stack[right++] = letter;
        }
    }
    size_t left = 0;
    while (left + 1 < right && stack[left] == switch_case(stack[right - 1])) { ++left; --right; }
    return {stack + left, stack + right};
}

std::string class_key(const std::string& cyclically_reduced) {
    return std::min(audit::least_rotation(cyclically_reduced),
                    audit::least_rotation(backward(cyclically_reduced)));
}

std::vector<std::string> all_rotations(const std::string& word) {
    std::set<std::string> distinct;
    const auto opposite = backward(word);
    for (const auto* orientation : {&word, &opposite}) {
        const auto doubled = *orientation + *orientation;
        for (size_t i = 0; i < word.size(); ++i)
            distinct.insert(doubled.substr(i, word.size()));
    }
    return {distinct.begin(), distinct.end()};
}

void append_bridges(int remaining, std::string& prefix, std::vector<P>& result) {
    result.emplace_back(prefix, backward(prefix));
    if (!remaining) return;
    for (const char letter : alphabet) {
        if (!prefix.empty() && prefix.back() == switch_case(letter)) continue;
        prefix.push_back(letter);
        append_bridges(remaining - 1, prefix, result);
        prefix.pop_back();
    }
}

class AlternateKeys {
    std::unordered_map<Code, Images> cache;

public:
    void limit() { if (cache.size() > 16384) cache.clear(); }

    const Images& signed_images(Code code) {
        const auto [it, inserted] = cache.try_emplace(code);
        if (inserted) {
            size_t at = 0;
            for (char a : std::string("XxYyZz"))
                for (char b : std::string("XxYyZz"))
                    for (char c : std::string("XxYyZz")) {
                        if ((a | 32) == (b | 32) || (a | 32) == (c | 32) || (b | 32) == (c | 32)) continue;
                        const std::array<char, 3> relabel{a, b, c};
                        auto text = decode(code);
                        for (auto& letter : text) {
                            const auto image = relabel[(letter | 32) - 'x'];
                            letter = letter >= 'a' ? switch_case(image) : image;
                        }
                        it->second[at++] = encode(class_key(text));
                    }
            if (at != 48) throw std::logic_error("signed basis menu is incomplete");
        }
        return it->second;
    }

    Key state(Code a, Code b, Code c) {
        return orbit(signed_images(a), signed_images(b), signed_images(c));
    }
};

P checked_projection(const std::string& a, const std::string& b, char singleton) {
    const auto project = [&](const std::string& word) {
        std::string image;
        for (const auto c : word) {
            const char lower = c | 32;
            const char deleted = singleton | 32;
            if (lower == deleted) continue;
            const char new_letter = lower - int(lower > deleted);
            image.push_back(c >= 'a' ? new_letter : switch_case(new_letter));
        }
        return class_key(cyclic_stack(image, "", "", ""));
    };
    auto p = project(a), q = project(b);
    if (p.empty() || q.empty()) throw std::logic_error("projection contains an identity");
    if (q < p) std::swap(p, q);
    return {p, q};
}

struct Counts {
    uint64_t candidates = 0, admitted = 0, nonempty = 0;
    std::set<P> returns;
};

int check(int cap, unsigned threads, const std::string& seeds, const std::string& states_path,
          const std::string& returns_path) {
    std::ifstream source(states_path), initial(seeds), returned(returns_path);
    if (!source || !initial || !returned) throw std::runtime_error("missing audit input");
    std::unordered_set<Key, KeyHash> names;
    std::vector<Key> states;
    Triple rows;
    AlternateKeys input_keys;
    while (source >> rows[0] >> rows[1] >> rows[2]) {
        input_keys.limit();
        if (energy(rows) > size_t(cap)) throw std::logic_error("catalogue exceeds cap");
        for (const auto& word : rows)
            if (word.size() < 2 || cyclic_stack(word, "", "", "") != word
                || class_key(word) != word)
                throw std::logic_error("catalogue has a noncanonical word");
        const auto key = input_keys.state(encode(rows[0]), encode(rows[1]), encode(rows[2]));
        if (rows_from(key) != rows || !names.insert(key).second)
            throw std::logic_error("noncanonical or repeated orbit");
        states.push_back(key);
    }
    if (states.empty()) throw std::logic_error("empty catalogue");
    std::set<Key> seed_names;
    size_t seed_count = 0;
    while (initial >> rows[0] >> rows[1] >> rows[2]) {
        input_keys.limit();
        const auto key = input_keys.state(encode(rows[0]), encode(rows[1]), encode(rows[2]));
        if (!names.count(key)) throw std::logic_error("missing seed orbit");
        seed_names.insert(key);
        ++seed_count;
    }
    if (!seed_count) throw std::logic_error("empty seed file");
    std::atomic<size_t> cursor{0};
    const auto& read_only = names;
    const auto worker = [&] {
        AlternateKeys keys;
        std::unordered_map<Code, std::vector<std::string>> rotations;
        std::map<int, std::vector<P>> tails;
        Counts counts;
        constexpr size_t chunk = 512;
        for (;;) {
            const auto begin = cursor.fetch_add(chunk, std::memory_order_relaxed);
            if (begin >= states.size()) break;
            for (size_t at = begin; at < std::min(begin + chunk, states.size()); ++at) {
                keys.limit();
                if (rotations.size() > 8192) rotations.clear();
                const auto ids = unpack(states[at]);
                const Triple current{decode(ids[0]), decode(ids[1]), decode(ids[2])};
                for (size_t i = 0; i < 3; ++i)
                    if (!rotations.count(ids[i])) rotations.emplace(ids[i], all_rotations(current[i]));
                const int total = int(energy(current));
                for (size_t receiver = 0; receiver < 3; ++receiver) {
                    std::unordered_set<Code> updates;
                    for (size_t donor = 0; donor < 3; ++donor) {
                        if (donor == receiver) continue;
                        const int bound = std::max(0, (cap - total - int(current[donor].size())) / 2);
                        const size_t allowance = cap - total + current[receiver].size();
                        if (!tails.count(bound)) {
                            std::string prefix;
                            append_bridges(bound, prefix, tails[bound]);
                        }
                        for (const auto& a : rotations.at(ids[receiver]))
                            for (const auto& b : rotations.at(ids[donor]))
                                for (const auto& [tail, tail_inverse] : tails.at(bound)) {
                                    ++counts.candidates;
                                    counts.nonempty += !tail.empty();
                                    const auto product = cyclic_stack(a, tail, b, tail_inverse);
                                    if (product.empty()) throw std::logic_error("an audited row vanished");
                                    if (product.size() > allowance) continue;
                                    ++counts.admitted;
                                    updates.insert(encode(class_key(product)));
                                }
                    }
                    const size_t other = (receiver + 1) % 3, third = (receiver + 2) % 3;
                    for (auto change : updates) {
                        if (length(change) == 1) {
                            counts.returns.insert(checked_projection(current[other], current[third], decode(change)[0]));
                        } else if (!read_only.count(keys.state(change, ids[other], ids[third]))) {
                            throw std::logic_error("a non-singleton neighbor is absent");
                        }
                    }
                }
            }
            if (begin && begin % (chunk * 1024) == 0)
                std::cerr << "Checked through " << begin << " of " << states.size() << '\n';
        }
        return counts;
    };
    std::vector<std::future<Counts>> jobs;
    for (unsigned i = 0; i < threads; ++i) jobs.push_back(std::async(std::launch::async, worker));
    Counts total;
    for (auto& job : jobs) {
        const auto seen = job.get();
        total.admitted += seen.admitted;
        total.candidates += seen.candidates;
        total.nonempty += seen.nonempty;
        total.returns.insert(seen.returns.begin(), seen.returns.end());
    }
    std::set<P> expanded, expected;
    P pair;
    while (returned >> pair.first >> pair.second) expected.insert(pair);
    for (const auto& [a, b] : total.returns)
        for (const auto order : {std::string("xy"), std::string("yx")})
            for (unsigned signs = 0; signs < 4; ++signs) {
                const auto relabel = [&](std::string word) {
                    for (auto& c : word) {
                        const unsigned position = (c | 32) - 'x';
                        c = ((c < 'a') != bool(signs & (1 << position))) ? switch_case(order[position]) : order[position];
                    }
                    return class_key(word);
                };
                auto p = relabel(a), q = relabel(b);
                if (q < p) std::swap(p, q);
                expanded.emplace(std::move(p), std::move(q));
            }
    if (expanded != expected) throw std::logic_error("reentry projections disagree");
    std::cout << "{\n  \"cap\": " << cap << ",\n  \"literal_seeds\": " << seed_count
              << ",\n  \"seed_orbits\": " << seed_names.size()
              << ",\n  \"state_orbits\": " << states.size()
              << ",\n  \"candidates\": " << total.candidates
              << ",\n  \"nonempty_bridge_candidates\": " << total.nonempty
              << ",\n  \"admitted\": " << total.admitted
              << ",\n  \"reentry_projections\": " << expanded.size() << "\n}\n";
    return 0;
}

}

int main(int argc, char** argv) {
    try {
        if (argc != 6) throw std::runtime_error("usage: audit cap threads seeds.tsv states.tsv returns.tsv");
        const int cap = std::stoi(argv[1]);
        const unsigned threads = std::stoul(argv[2]);
        if (cap < 20 || cap > 22 || !threads) throw std::runtime_error("need cap 20–22 and a worker");
        return check(cap, threads, argv[3], argv[4], argv[5]);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
