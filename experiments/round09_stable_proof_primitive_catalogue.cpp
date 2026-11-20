// Use one verified primitive chart per row to look for a primitive quotient coordinate.
#ifndef AC_ROUND09_PRIMITIVE_REUSE
#define AC_ROUND06_SINGLETON_LIBRARY
#include "round06_stable_proof_all_singleton.cpp"
#endif

#include <numeric>

namespace {

using Mark = std::array<std::string, 6>;

std::string image(std::string_view word, const Mark& map) {
    std::string result;
    for (const auto c : word) {
        for (const auto a : map[alphabet.find(c)]) {
            if (!result.empty() && result.back() == invchar(a)) result.pop_back();
            else result.push_back(a);
        }
    }
    return result;
}

Mark identity_mark() {
    Mark mark;
    for (unsigned i = 0; i < alphabet.size(); ++i)
        mark[i] = std::string(1, alphabet[i]);
    return mark;
}

unsigned opposite(unsigned i) { return (i + 3) % 6; }

int literal_letter(const std::string& word) {
    for (unsigned letter = 0; letter < 3; ++letter)
        if (std::count(word.begin(), word.end(), alphabet[letter])
            + std::count(word.begin(), word.end(), alphabet[opposite(letter)]) == 1)
            return int(letter);
    return -1;
}

std::optional<Mark> whitehead_reduction(const std::string& word) {
    std::array<std::array<int, 6>, 6> edges{};
    std::array<int, 6> degrees{};
    for (size_t i = 0; i < word.size(); ++i) {
        const unsigned a = opposite(unsigned(alphabet.find(word[i])));
        const unsigned b = unsigned(alphabet.find(word[(i + 1) % word.size()]));
        ++edges[a][b];
        ++degrees[a];
        ++degrees[b];
    }
    int best_delta = 0;
    unsigned multiplier = 0, cut = 0;
    for (unsigned m = 0; m < 6; ++m) {
        for (unsigned side = 1; side < 63; ++side) {
            if (!(side & (1U << m)) || (side & (1U << opposite(m)))) continue;
            int crossing = 0;
            for (unsigned a = 0; a < 6; ++a)
                for (unsigned b = 0; b < 6; ++b)
                    if (((side >> a) ^ (side >> b)) & 1) crossing += edges[a][b];
            if (crossing - degrees[m] < best_delta) {
                best_delta = crossing - degrees[m];
                multiplier = m;
                cut = side;
            }
        }
    }
    if (!cut) return std::nullopt;
    auto map = identity_mark();
    for (unsigned i = 0; i < 6; ++i) {
        if (i == multiplier || i == opposite(multiplier)) continue;
        if (cut & (1U << i)) map[i].insert(map[i].begin(), alphabet[multiplier]);
        if (cut & (1U << opposite(i))) map[i].push_back(alphabet[opposite(multiplier)]);
    }
    if (cyclic(image(word, map)).size() + size_t(-best_delta) != word.size())
        throw std::logic_error("Whitehead cut length disagreement");
    return map;
}

std::optional<Mark> quotient(std::string word) {
    auto marking = identity_mark();
    int selected = literal_letter(word);
    while (selected < 0) {
        const auto reduction = whitehead_reduction(word);
        if (!reduction) return std::nullopt;
        word = cyclic(image(word, *reduction));
        for (auto& value : marking) value = image(value, *reduction);
        selected = literal_letter(word);
    }
    const auto eliminated = unsigned(selected);
    if (word.find(alphabet[opposite(eliminated)]) == std::string::npos)
        word = inverse(word);
    const auto position = word.find(alphabet[opposite(eliminated)]);
    if (position == std::string::npos) throw std::logic_error("literal pivot lost its letter");
    auto solved = identity_mark();
    solved[eliminated] = word.substr(position + 1) + word.substr(0, position);
    solved[opposite(eliminated)] = inverse(solved[eliminated]);
    auto rename = identity_mark();
    char letter = 'x';
    for (unsigned i = 0; i < 3; ++i) {
        if (i == eliminated) continue;
        rename[i] = std::string(1, invchar(letter));
        rename[opposite(i)] = std::string(1, letter++);
    }
    for (auto& value : marking) value = image(image(value, solved), rename);
    return marking;
}

std::string euclidean(int a, int b) {
    if (!a) return "y";
    if (!b) return "x";
    if (a == b) return "xy";
    const auto shorter = a > b ? euclidean(a - b, b) : euclidean(a, b - a);
    std::string result;
    for (const auto c : shorter)
        result += c == (a > b ? 'y' : 'x') ? "xy" : std::string(1, c);
    return result;
}

bool primitive_rank_two(const std::string& word) {
    int a = 0, b = 0;
    for (const auto c : word) {
        switch (c) {
            case 'x': ++a; break;
            case 'X': --a; break;
            case 'y': ++b; break;
            case 'Y': --b; break;
            default: throw std::logic_error("quotient retained its eliminated letter");
        }
    }
    if (size_t(std::abs(a) + std::abs(b)) != word.size() || std::gcd(a, b) != 1) return false;
    auto model = euclidean(std::abs(a), std::abs(b));
    for (auto& c : model)
        if ((c == 'x' && a < 0) || (c == 'y' && b < 0)) c = invchar(c);
    return (model + model).find(word) != std::string::npos;
}

struct CachedPair {
    Key key = 0;
    bool result = false;
};

constexpr std::size_t packed_word_limit = 21;

int dump_chartless(const char* catalogue, unsigned energy_limit, const char* output) {
    std::ifstream source(catalogue);
    std::ofstream destination(output);
    if (!source || !destination) throw std::runtime_error("missing catalogue or output");
    std::unordered_map<Code, bool> primitive_rows;
    uint64_t states = 0, chartless = 0;
    Triple rows;
    while (source >> rows[0] >> rows[1] >> rows[2]) {
        if (energy(rows) > energy_limit) continue;
        ++states;
        if (std::any_of(rows.begin(), rows.end(), [](const auto& word) { return literal_letter(word) >= 0; }))
            continue;
        const auto is_primitive = [&](const auto& word) {
            if (word.size() > packed_word_limit) return quotient(word).has_value();
            const auto [cached, inserted] = primitive_rows.try_emplace(encode(word));
            if (inserted) cached->second = quotient(word).has_value();
            return cached->second;
        };
        if (std::any_of(rows.begin(), rows.end(), is_primitive)) continue;
        ++chartless;
        write_tsv(destination, rows);
    }
    if (!states || !destination) throw std::runtime_error("chartless export failed");
    std::cout << "{\n  \"energy_limit\": " << energy_limit << ",\n  \"states\": " << states
              << ",\n  \"states_without_primitive_row\": " << chartless << "\n}\n";
    return 0;
}

int screen(const char* catalogue, unsigned energy_limit) {
    std::ifstream source(catalogue);
    if (!source) throw std::runtime_error("missing catalogue");
    std::unordered_map<Code, std::optional<Mark>> charts;
    std::unordered_map<std::string, std::optional<Mark>> long_charts;
    auto chart_for = [&](auto& table, const auto& key, const std::string& word) -> const std::optional<Mark>& {
        const auto [chart, inserted] = table.try_emplace(key);
        if (inserted) {
            chart->second = quotient(word);
            if (chart->second && !cyclic(image(word, *chart->second)).empty())
                throw std::logic_error("projecting the pivot did not kill it");
        }
        return chart->second;
    };
    std::vector<CachedPair> tested(1U << 22);
    uint64_t states = 0, no_primitive_row = 0, examined_charts = 0, tested_pairs = 0;
    Triple rows;
    while (source >> rows[0] >> rows[1] >> rows[2]) {
        if (energy(rows) > energy_limit) continue;
        ++states;
        std::array<Code, 3> codes{};
        for (unsigned i = 0; i < rows.size(); ++i)
            if (rows[i].size() <= packed_word_limit) codes[i] = encode(rows[i]);
        bool has_chart = false;
        for (unsigned pivot = 0; pivot < 3; ++pivot) {
            const auto& chart = codes[pivot] ? chart_for(charts, codes[pivot], rows[pivot])
                                             : chart_for(long_charts, rows[pivot], rows[pivot]);
            if (!chart) continue;
            ++examined_charts;
            has_chart = true;
            const auto& marking = *chart;
            for (unsigned other = 0; other < 3; ++other) {
                if (pivot == other) continue;
                auto test = [&]() {
                    ++tested_pairs;
                    return primitive_rank_two(cyclic(image(rows[other], marking)));
                };
                bool primitive;
                if (codes[pivot] && codes[other]) {
                    const Key key = (Key(codes[pivot]) << 64) | codes[other];
                    auto& cell = tested[KeyHash{}(key) & (tested.size() - 1)];
                    if (cell.key != key) cell = {key, test()};
                    primitive = cell.result;
                } else {
                    primitive = test();
                }
                if (primitive) {
                    std::cout << "{\"status\":\"PRIMITIVE\",\"rows\":[\"" << rows[0] << "\",\"" << rows[1]
                              << "\",\"" << rows[2] << "\"],\"pivot_slot\":" << pivot << ",\"witness_slot\":" << other
                              << ",\"primitive_word\":\"" << cyclic(image(rows[other], marking)) << "\"}\n";
                    return 0;
                }
            }
        }
        no_primitive_row += !has_chart;
        if ((states & ((1U << 22) - 1)) == 0)
            std::cerr << "Screened " << states << " states and " << charts.size() + long_charts.size() << " row classes.\n";
    }
    if (!states) throw std::runtime_error("no input states examined");
    std::cout << "{\n  \"status\": \"NO_PRIMITIVE_PROJECTION\","
              << "\n  \"energy_limit\": " << energy_limit << ",\n  \"states\": " << states
              << ",\n  \"states_without_primitive_row\": " << no_primitive_row
              << ",\n  \"charts_examined_one_per_primitive_row\": " << examined_charts
              << ",\n  \"row_classes_classified\": " << charts.size() + long_charts.size()
              << ",\n  \"uncached_projection_checks\": " << tested_pairs << "\n}\n";
    return 0;
}

}

#ifndef AC_ROUND09_PRIMITIVE_REUSE
int main(int argc, char** argv) {
    try {
        if (argc == 4) return dump_chartless(argv[1], std::stoul(argv[2]), argv[3]);
        if (argc != 3)
            throw std::runtime_error("usage: primitive-catalogue states.tsv energy-cap [chartless-output.tsv]");
        return screen(argv[1], std::stoul(argv[2]));
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
#endif
