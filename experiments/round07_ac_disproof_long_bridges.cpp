// Audit the finite rotation and endpoint hypotheses for unbounded middle bridges.
#define AC_ROUND06_BASIS_PHASES_LIBRARY
#include "round06_ac_disproof_basis_phases.cpp"

namespace long_middle {
using actual_phases::Pair;
const std::string alphabet = "xXyY";

std::string cyclic_class(const std::string& word) {
    return std::min(rotations(word).front(), rotations(inv(word)).front());
}

std::vector<std::string> signed_rotations(const std::string& word) {
    auto labels = rotations(word);
    const auto reversed = rotations(inv(word));
    labels.insert(labels.end(), reversed.begin(), reversed.end());
    return labels;
}

int reads(const Graph& graph, const std::string& label) {
    int count = 0;
    for (int start = 0; start < static_cast<int>(graph.out.size()); ++start) {
        int at = start;
        for (char c : label) {
            at = graph.out[at][letter(c)];
            if (at < 0) break;
        }
        count += at >= 0;
    }
    return count;
}

bool reads_from_attachment(const Graph& graph, const std::string& label) {
    int at = 0;
    for (char c : label) {
        at = graph.out[at][letter(c)];
        if (at < 0) return false;
    }
    return true;
}

Graph with_tail(const std::string& lobe, const std::string& tail) {
    Graph graph;
    add_vertex(graph);
    append_path(graph, 0, lobe, true);
    append_path(graph, 0, tail, false);
    return graph;
}

bool tail_allowed(const std::string& lobe, char c) {
    return c != lobe.front() && c != inverse(lobe.back());
}

bool check_counts(const Graph& graph, const std::vector<std::string>& own,
                  const std::vector<std::string>& other) {
    for (const auto& word : own) if (reads(graph, word) != 1) return false;
    for (const auto& word : other) if (reads(graph, word)) return false;
    return true;
}

bool fits(const std::string& word, char c, char d) {
    return std::all_of(word.begin(), word.end(), [&](char label) {
        return label == c || label == d;
    });
}

std::vector<std::string> forbidden_prefixes(const std::string& lobe,
                                            const std::vector<std::string>& patterns) {
    const auto circle = with_tail(lobe, "");
    std::set<std::string> prefixes;
    for (const auto& pattern : patterns)
        for (size_t cut = 1; cut < pattern.size(); ++cut)
            if (tail_allowed(lobe, pattern[cut]) &&
                reads_from_attachment(circle, inv(pattern.substr(0, cut))))
                prefixes.insert(pattern.substr(cut));
    return {prefixes.begin(), prefixes.end()};
}

unsigned full_alphabet_ends(const std::vector<std::string>& rotations,
                            const std::vector<std::vector<std::string>>& prefixes,
                            char c, char d) {
    unsigned good = 0;
    for (size_t i = 0; i < rotations.size(); ++i) {
        const auto& lobe = rotations[i];
        if (!tail_allowed(lobe, c) && !tail_allowed(lobe, d)) continue;
        if (std::none_of(prefixes[i].begin(), prefixes[i].end(),
                         [&](const std::string& word) { return fits(word, c, d); })) ++good;
    }
    return good;
}

uint64_t unrestricted_alphabets(const Pair& pair, std::vector<std::string> patterns) {
    const auto a = rotations(pair.first), b = rotations(pair.second);
    std::vector<std::vector<std::string>> ap, bp;
    for (const auto& word : a) ap.push_back(forbidden_prefixes(word, patterns));
    for (const auto& word : b) bp.push_back(forbidden_prefixes(word, patterns));
    uint64_t count = 0;
    for (char c : std::string("xX")) for (char d : std::string("yY")) {
        if (std::any_of(patterns.begin(), patterns.end(),
                        [&](const std::string& word) { return fits(word, c, d); })) continue;
        count += full_alphabet_ends(a, ap, c, d) *
                 full_alphabet_ends(b, bp, inverse(c), inverse(d));
    }
    return count;
}

struct CaseCounts {
    uint64_t dag = 0, exact = 0, positive = 0, incomplete = 0;
};

bool pair_excluded(const std::string& a, const std::string& b, CaseCounts& counts) {
    const auto graph = (a == b || a == inv(b)) ? with_tail(a, "") : fold(a, b);
    if (proves_primitive_absence(graph)) {
        ++counts.dag;
        return true;
    }
    const auto verdict = u_native::decide(graph.out, 1'000'000);
    if (verdict.status == u_native::Status::ABSENT) {
        ++counts.exact;
        return true;
    }
    if (verdict.status == u_native::Status::PRIMITIVE) ++counts.positive;
    else ++counts.incomplete;
    return false;
}

bool rotation_check(const Pair& pair, CaseCounts& counts) {
    const auto a = rotations(pair.first), b = rotations(pair.second);
    bool clear = true;
    for (const auto* same : {&a, &b})
        for (size_t i = 0; i < same->size(); ++i)
            for (size_t j = i; j < same->size(); ++j)
                if (!pair_excluded((*same)[i], (*same)[j], counts)) clear = false;
    for (const auto& left : a)
        for (const auto& right : b)
            if (!pair_excluded(left, right, counts)) clear = false;
    return clear;
}

using Endpoints = std::array<std::vector<std::string>, 4>;

Endpoints endpoints(const std::string& lobe, const std::vector<std::string>& own,
                    const std::vector<std::string>& other, size_t length) {
    Endpoints good;
    for (const auto& rotation : rotations(lobe))
        for (size_t i = 0; i < alphabet.size(); ++i) {
            const char c = alphabet[i];
            if (tail_allowed(rotation, c) && check_counts(with_tail(rotation, std::string(length, c)),
                                                         own, other)) good[i].push_back(rotation);
        }
    return good;
}

void write_pair(std::ostream& out, const Pair& pair) {
    out << "[\"" << pair.first << "\",\"" << pair.second << "\"]";
}

void run(int first_mass, int second_mass, int first_gap, const char* catalogue) {
    if (first_mass < 2 || second_mass < 2 || first_gap < 0)
        throw std::runtime_error("invalid phase limits");
    const auto first_menu = actual_phases::slope_pairs(first_mass);
    const auto second_menu = actual_phases::slope_pairs(second_mass);
    const auto connectors = actual_phases::bridge_labels(first_gap);

    std::set<Pair> first;
    actual_phases::placements({"xxxYYYY", "xyxYXY"}, first_menu, connectors,
                             [&](const Pair& pair) { first.insert(pair); });
    std::map<Pair, Pair> lobes;
    for (const auto& placed : first)
        for (const auto& [a, b] : second_menu) {
            Pair words{actual_phases::realize(placed, a), actual_phases::realize(placed, b)};
            Pair key{cyclic_class(words.first), cyclic_class(words.second)};
            if (key.second < key.first) std::swap(key.first, key.second);
            lobes.try_emplace(key, placed);
        }

    std::ofstream rows(catalogue);
    if (!rows) throw std::runtime_error("cannot open lobe catalogue");
    uint64_t intrinsic = 0, clear_rotations = 0, guarded = 0, full_alphabets = 0;
    uint64_t one_letter_families = 0, exponential_families = 0, unpadded_families = 0;
    CaseCounts checks;
    for (const auto& [pair, entry] : lobes) {
        const auto a = signed_rotations(pair.first), b = signed_rotations(pair.second);
        const size_t length = std::max(pair.first.size(), pair.second.size());
        if (!check_counts(with_tail(pair.first, ""), a, b)
            || !check_counts(with_tail(pair.second, ""), b, a)) continue;
        ++intrinsic;
        if (!rotation_check(pair, checks)) continue;
        ++clear_rotations;
        const auto left = endpoints(pair.first, a, b, length);
        const auto right = endpoints(pair.second, b, a, length);
        uint64_t powers = 0, exponential = 0;
        std::string bridge, left_lobe, right_lobe, letters;
        std::vector<std::array<char, 2>> accepted;
        for (size_t i = 0; i < alphabet.size(); ++i) {
            const char c = alphabet[i];
            if (!fits(pair.first, c, c) && !fits(pair.first, inverse(c), inverse(c))
                && !fits(pair.second, c, c) && !fits(pair.second, inverse(c), inverse(c)))
                powers += left[i].size() * right[i ^ 1].size();
            for (size_t j = 0; j < alphabet.size(); ++j) {
                if (i / 2 == j / 2) continue;
                const char d = alphabet[j];
                if (fits(pair.first, c, d) || fits(pair.first, inverse(c), inverse(d))
                    || fits(pair.second, c, d) || fits(pair.second, inverse(c), inverse(d))) continue;
                const auto count = left[i].size() * right[j ^ 1].size();
                if (!count) continue;
                accepted.push_back({c, d});
                exponential += count;
                if (letters.empty()) {
                    letters = std::string{c, d};
                    left_lobe = left[i].front();
                    right_lobe = right[j ^ 1].front();
                    bridge = std::string(length, c) + std::string(length, d);
                }
            }
        }
        one_letter_families += powers;
        exponential_families += exponential;
        auto patterns = a;
        patterns.insert(patterns.end(), b.begin(), b.end());
        const auto unpadded = unrestricted_alphabets(pair, std::move(patterns));
        unpadded_families += unpadded;
        guarded += powers || exponential;
        full_alphabets += exponential != 0;
        rows << "{\"lobes\":";
        write_pair(rows, pair);
        rows << ",\"first_placement\":";
        write_pair(rows, entry);
        rows << ",\"guard_length\":" << length << ",\"constant_families\":" << powers
             << ",\"exponential_families\":" << exponential
             << ",\"unrestricted_alphabet_families\":" << unpadded << ",\"accepted_end_letters\":[";
        for (size_t i = 0; i < accepted.size(); ++i) {
            if (i) rows << ',';
            rows << '"' << accepted[i][0] << accepted[i][1] << '"';
        }
        rows << "],\"example\":[\"" << left_lobe << "\",\"" << bridge << "\",\""
             << right_lobe << "\"],\"example_alphabet\":\"" << letters << "\"}\n";
    }
    std::cout << "{\"first_basis_mass\":" << first_mass << ",\"second_basis_mass\":" << second_mass
              << ",\"first_bridge_cap\":" << first_gap << ",\"first_marked_pairs\":" << first.size()
              << ",\"distinct_second_lobe_pairs\":" << lobes.size() << ",\"bare_lobes_unique\":" << intrinsic
              << ",\"rotation_certified_pairs\":" << clear_rotations << ",\"guarded_pairs\":" << guarded
              << ",\"pairs_with_exponential_families\":" << full_alphabets
              << ",\"rotation_DAG_exclusions\":" << checks.dag << ",\"rotation_exact_exclusions\":" << checks.exact
              << ",\"rotation_positive_checks\":" << checks.positive
              << ",\"rotation_incomplete_checks\":" << checks.incomplete
              << ",\"constant_families\":" << one_letter_families
              << ",\"exponential_families\":" << exponential_families
              << ",\"unrestricted_alphabet_families\":" << unpadded_families << "}\n";
}
}

int main(int argc, char** argv) {
    try {
        if (argc != 5) throw std::runtime_error("usage: long_bridges first_mass second_mass first_gap catalogue.jsonl");
        long_middle::run(std::stoi(argv[1]), std::stoi(argv[2]), std::stoi(argv[3]), argv[4]);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
