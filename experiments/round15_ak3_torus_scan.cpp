// Search stored ordinary first exits for primitive replacements in torus quotients.
#define AC_ROUND07_WIDE_ORBITS_LIBRARY
#include "round07_ak3_wide_orbits.cpp"

#include <sstream>

namespace torus_scan {
using orbit_search::Code;
using orbit_search::word;
using orbit_search::word_code;
using std::string;
using Record = std::array<Code, 4>;

struct Chart {
    unsigned p, q;
    string x, y, plus, minus, period;
};

struct Counts {
    uint64_t marked_rows = 0;
    uint64_t receiver_weight_one = 0;
    uint64_t target_length_matches = 0;
};

string change_marking(const string& w, const Chart& chart) {
    const string X = inverse(chart.x), Y = inverse(chart.y);
    string output;
    for (const char c : w)
        output += c == 'x' ? chart.x : c == 'X' ? X : c == 'y' ? chart.y : Y;
    return output;
}

int weight(const string& w, unsigned p, unsigned q) {
    int wx = 0, wy = 0;
    for (const char c : w) {
        if (c == 'x') ++wx;
        else if (c == 'X') --wx;
        else if (c == 'y') ++wy;
        else if (c == 'Y') --wy;
        else throw std::runtime_error("bad torus chart coordinate");
    }
    return int(q) * wx - int(p) * wy;
}

int axis(int value) { return value > 0 ? 1 : -1; }

int sum_on_axis(int left, int right, unsigned p, unsigned q) {
    if (axis(left) != axis(right)) throw std::runtime_error("different axes in cyclic factor");
    return (left + right) % int(left > 0 ? p : q);
}

std::vector<int> signature(const string& w, unsigned p, unsigned q) {
    std::vector<int> pieces;
    for (const char c : w) {
        const int value = c == 'x' ? 1 : c == 'X' ? int(p) - 1 : c == 'y' ? -1 : 1 - int(q);
        if (pieces.empty() || axis(pieces.back()) != axis(value)) {
            pieces.push_back(value);
        } else {
            const int sum = sum_on_axis(pieces.back(), value, p, q);
            if (sum) pieces.back() = sum;
            else pieces.pop_back();
        }
    }
    size_t begin = 0, end = pieces.size();
    while (begin + 1 < end && axis(pieces[begin]) == axis(pieces[end - 1])) {
        const int sum = sum_on_axis(pieces[begin], pieces[end - 1], p, q);
        --end;
        if (sum) {
            pieces[begin] = sum;
            break;
        }
        ++begin;
    }
    return {pieces.begin() + begin, pieces.begin() + end};
}

bool cyclic_same(const std::vector<int>& a, const std::vector<int>& b) {
    if (a.size() != b.size()) return false;
    auto repeated = a;
    repeated.insert(repeated.end(), a.begin(), a.end());
    return std::search(repeated.begin(), repeated.end(), b.begin(), b.end()) != repeated.end();
}

string target(const string& receiver, const Chart& image, Counts& counts) {
    ++counts.marked_rows;
    auto marked = change_marking(receiver, image);
    const int height = weight(marked, image.p, image.q);
    if (std::abs(height) != 1) throw std::runtime_error("unimodular source lost its torus character");
    ++counts.receiver_weight_one;
    if (height < 0) marked = inverse(marked);
    const auto companion = signature(marked, image.p, image.q);
    const auto slope = signature(image.period, image.p, image.q);
    for (const string* tail : {&image.plus, &image.minus}) {
        const auto start = signature(*tail, image.p, image.q);
        if (companion.size() < start.size() || (companion.size() - start.size()) % slope.size()) continue;
        ++counts.target_length_matches;
        const size_t power = (companion.size() - start.size()) / slope.size();
        auto candidate = *tail;
        for (size_t i = 0; i < power; ++i) candidate += image.period;
        if (tail == &image.minus) candidate = inverse(candidate);
        if (weight(candidate, image.p, image.q) != 1)
            throw std::runtime_error("primitive target has wrong marked character");
        if (cyclic_same(companion, signature(candidate, image.p, image.q)))
            return height < 0 ? inverse(candidate) : candidate;
    }
    return {};
}

int run(const char* chart_tsv, int count, char** files) {
    std::ifstream input(chart_tsv);
    if (!input) throw std::runtime_error("cannot load torus atlas");
    std::unordered_map<Code, Chart> charts;
    std::map<std::pair<unsigned, unsigned>, Counts> counts;
    string name;
    Chart image;
    while (input >> name >> image.p >> image.q >> image.x >> image.y
                 >> image.plus >> image.minus >> image.period) {
        if (name.size() > 31 || image.p < 2 || image.q < 2 ||
            image.period != image.plus + image.minus ||
            weight(image.plus, image.p, image.q) != 1 ||
            weight(image.minus, image.p, image.q) != -1 ||
            signature(image.period, image.p, image.q).empty())
            throw std::runtime_error("invalid torus chart");
        counts.try_emplace({image.p, image.q});
        if (!charts.emplace(word_code(name), image).second) throw std::runtime_error("duplicate atlas key");
    }
    if (!input.eof() || charts.empty()) throw std::runtime_error("incomplete torus atlas");
    std::vector<Record> batch(1 << 19);
    uint64_t checked = 0;
    string hit;
    for (int file = 0; file < count && hit.empty(); ++file) {
        std::ifstream source(files[file], std::ios::binary);
        if (!source) throw std::runtime_error("cannot open boundary shard");
        while (hit.empty()) {
            source.read(reinterpret_cast<char*>(batch.data()), batch.size()*sizeof(Record));
            if (source.gcount()%sizeof(Record)) throw std::runtime_error("truncated boundary shard");
            const auto rows = source.gcount()/sizeof(Record);
            for (size_t index = 0; index < size_t(rows) && hit.empty(); ++index) {
                const auto& record = batch[index];
                ++checked;
                for (unsigned donor = 0; donor < 2; ++donor) {
                    const auto match = charts.find(record[donor]);
                    if (match == charts.end()) continue;
                    const auto& chart = match->second;
                    auto& tally = counts.at({chart.p, chart.q});
                    const auto answer = target(word(record[1-donor]), chart, tally);
                    if (answer.empty()) continue;
                    std::ostringstream receipt;
                    receipt << "{\"child\":[\"" << word(record[0]) << "\",\"" << word(record[1])
                            << "\"],\"anchor\":[\"" << word(record[2]) << "\",\"" << word(record[3])
                            << "\"],\"donor_index\":" << donor << ",\"marking\":[\"" << chart.x
                            << "\",\"" << chart.y << "\"],\"p\":" << chart.p << ",\"q\":" << chart.q
                            << ",\"primitive_in_torus_marking\":\"" << answer << "\"}";
                    hit = receipt.str();
                    break;
                }
            }
            if (source.eof()) break;
            if (!source) throw std::runtime_error("boundary read failed");
        }
        if ((file + 1) % 16 == 0) std::cerr << "checked " << (file+1) << " shards, " << checked << " seeds\n";
    }
    std::cout << "{\n  \"atlas_marked_keys\":" << charts.size() << ",\n  \"seeds_checked\":" << checked
              << ",\n  \"complete\":" << (hit.empty() ? "true" : "false") << ",\n  \"hit\":"
              << (hit.empty() ? "null" : hit) << ",\n  \"torus_counts\":[";
    bool first = true;
    for (const auto& [type, tally] : counts) {
        if (!first) std::cout << ',';
        first = false;
        std::cout << "\n    {\"p\":" << type.first << ",\"q\":" << type.second
                  << ",\"marked_rows\":" << tally.marked_rows << ",\"receiver_weight_one\":"
                  << tally.receiver_weight_one << ",\"target_length_matches\":" << tally.target_length_matches << '}';
    }
    std::cout << "\n  ]\n}\n";
    return 0;
}
} // namespace torus_scan

int main(int argc, char** argv) {
    try {
        if (argc < 3) throw std::runtime_error("usage: torus-scan atlas.tsv shard.bin ...");
        return torus_scan::run(argv[1], argc-2, argv+2);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
