// Bounded bidirectional reduction of a literal pivot's tail.
#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

namespace {

char opposite(char c) {
    constexpr char case_bit = 'a' ^ 'A';
    return c ^ case_bit;
}

std::string inverse(std::string word) {
    std::reverse(word.begin(), word.end());
    for (auto& c : word) c = opposite(c);
    return word;
}

std::string reduce(const std::string& word) {
    std::string out;
    out.reserve(word.size());
    for (const auto c : word) {
        if (!out.empty() && out.back() == opposite(c)) out.pop_back();
        else out.push_back(c);
    }
    return out;
}

struct Factor {
    unsigned row = 0;
    int sign = 1;
    std::string tail;
};

struct Rule {
    std::string replacement;
    Factor factor;
};

using Rules = std::unordered_map<std::string, std::vector<Rule>>;

Rules rewrites(const std::array<std::string, 2>& donors) {
    Rules result;
    for (unsigned row = 0; row < donors.size(); ++row) {
        for (const int sign : {1, -1}) {
            const auto word = sign == 1 ? donors[row] : inverse(donors[row]);
            for (size_t rotation = 0; rotation < word.size(); ++rotation) {
                const auto relator = word.substr(rotation) + word.substr(0, rotation);
                const auto conjugator = inverse(word.substr(0, rotation));
                for (size_t cut = 0; cut <= relator.size(); ++cut)
                    result[relator.substr(0, cut)].push_back(
                         Rule{inverse(relator.substr(cut)), Factor{row, -sign, conjugator}});
            }
        }
    }
    return result;
}

constexpr auto seed = std::numeric_limits<size_t>::max();

struct Node {
    std::string word;
    size_t parent;
    Factor factor;
};

struct Search {
    std::vector<Node> nodes;
    std::vector<size_t> layer;
    std::unordered_map<std::string, size_t> indices;
    size_t expanded = 0;

    size_t add(std::string word, size_t parent, Factor factor) {
        const auto index = nodes.size();
        if (!indices.emplace(word, index).second) return seed;
        nodes.push_back({std::move(word), parent, std::move(factor)});
        return index;
    }

    explicit Search(const std::string& word) { layer.push_back(add(word, seed, {})); }

    std::vector<Factor> factors(size_t at) const {
        std::vector<Factor> result;
        for (; nodes[at].parent != seed; at = nodes[at].parent)
            result.push_back(nodes[at].factor);
        std::reverse(result.begin(), result.end());
        return result;
    }
};

void run(const std::array<std::string, 2>& donors, const std::string& word,
         size_t cap, size_t budget, std::ostream& output) {
    if (word.size() > cap) throw std::invalid_argument("initial tail exceeds cap");
    const auto rules = rewrites(donors);
    Search forward(word), backward("");
    std::array<size_t, 2> join{seed, seed};
    if (word.empty()) join = {0, 0};
    while (join[0] == seed && !forward.layer.empty() && !backward.layer.empty()
           && forward.expanded + backward.expanded < budget) {
        const bool reversed = backward.layer.size() < forward.layer.size();
        auto& active = reversed ? backward : forward;
        const auto& opposite_search = reversed ? forward : backward;
        std::vector<size_t> next;
        for (const auto parent : active.layer) {
            if (forward.expanded + backward.expanded >= budget || join[0] != seed) break;
            ++active.expanded;
            const auto w = active.nodes[parent].word;
            for (size_t i = 0; i <= w.size() && join[0] == seed; ++i) {
                const auto before = w.substr(0, i);
                for (size_t j = i; j <= w.size() && join[0] == seed; ++j) {
                    const auto it = rules.find(w.substr(i, j - i));
                    if (it == rules.end()) continue;
                    const auto suffix = w.substr(j);
                    const auto back = inverse(suffix);
                    for (const auto& rule : it->second) {
                        auto candidate = reduce(before + rule.replacement + suffix);
                        if (candidate.size() > cap) continue;
                        auto factor = rule.factor;
                        factor.tail = reduce(back + factor.tail);
                        const auto index = active.add(std::move(candidate), parent, std::move(factor));
                        if (index == seed) continue;
                        next.push_back(index);
                        const auto other = opposite_search.indices.find(active.nodes[index].word);
                        if (other != opposite_search.indices.end()) {
                            join[reversed] = index;
                            join[!reversed] = other->second;
                            break;
                        }
                    }
                }
            }
        }
        active.layer = std::move(next);
    }
    if (join[0] != seed) {
        auto proof = forward.factors(join[0]);
        const auto tail = backward.factors(join[1]);
        for (auto it = tail.rbegin(); it != tail.rend(); ++it)
            proof.push_back({it->row, -it->sign, it->tail});
        auto checking_word = word;
        for (const auto& factor : proof) {
            const auto relator = factor.sign == 1 ? donors[factor.row] : inverse(donors[factor.row]);
            checking_word = reduce(checking_word + factor.tail + relator + inverse(factor.tail));
            if (checking_word.size() > cap) throw std::logic_error("factor proof exceeded cap");
            output << factor.row << '\t' << factor.sign << '\t' << factor.tail << '\n';
        }
        if (!checking_word.empty()) throw std::logic_error("factor proof did not close");
    }
    std::cout << "{\"word_cap\":" << cap << ",\"forward\":" << forward.expanded
              << ",\"backward\":" << backward.expanded << ",\"hit\":"
              << (join[0] == seed ? "false" : "true") << "}\n";
}

} // namespace

int main(int argc, char** argv) {
    try {
        if (argc != 7) throw std::invalid_argument("usage: tail r1 r2 word cap budget proof.tsv");
        std::ofstream output(argv[6]);
        if (!output) throw std::runtime_error("cannot open proof output");
        run({argv[1], argv[2]}, argv[3], std::stoull(argv[4]), std::stoull(argv[5]), output);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
