// Exact spherical contractions for three fixed-donor products and an alternating relaxation.
#define AC_ROUND18_TWO_PRODUCTS_LIBRARY
#include "round18_ak3_two_products.cpp"

#include <limits>
#include <set>
#include <unordered_set>

namespace {
using Words = std::vector<string>;

string json_array(const Words& words) {
    string out = "[";
    for (const auto& word : words) {
        if (out.size() > 1) out += ',';
        out += "\"" + word + "\"";
    }
    return out + ']';
}

struct Counters {
    uint64_t top = 0, contractions = 0, memo_hits = 0, terminal = 0;
};

class Equation {
    std::unordered_set<string> rejected;
    std::map<std::pair<string,string>,Menu> cached_menus;
    size_t cached_products = 0;
    Counters& counts;
    const size_t max_rejected;
    const bool rooted_contractions;

    void remember_negative(string key) {
        if (rejected.size() < max_rejected) rejected.emplace(std::move(key));
    }

    const Menu& menu(const string& a, const string& b) {
        auto [it,added] = cached_menus.try_emplace(std::pair{a,b});
        if (added) {
            it->second = zero_bridge(a,b);
            cached_products += it->second.size();
        }
        return it->second;
    }

    string terminal(const Words& words) {
        ++counts.terminal;
        // Clear between terminals so references held by a comparison remain valid.
        if (cached_products > 80000) {
            cached_menus.clear();
            cached_products = 0;
        }
        switch (words.size()) {
            case 0: return "{\"kind\":\"empty\"}";
            case 1: return {};
            case 2:
                return (rooted_contractions ? words[0] : canonical(words[0])) == canonical(inverse(words[1]))
                     ? "{\"kind\":\"pair\"}" : "";
            case 3: {
                const auto target = canonical(inverse(words[2]));
                if (target.size() > words[0].size() + words[1].size()) {
                    if (auto match = positive_bridge(words[0],words[1],target))
                        return "{\"kind\":\"triple\",\"split\":" + triple(*match) + "}";
                } else {
                    const auto& outputs = menu(words[0],words[1]);
                    if (auto it=outputs.find(target); it!=outputs.end())
                        return "{\"kind\":\"triple\",\"split\":" + triple(it->second) + "}";
                }
                return {};
            }
            case 4: {
                const std::array<string,4> list{words[0],words[1],words[2],words[3]};
                const auto match = sphere_with_menus(list, words[1] == words[2],
                    [this](const string& a,const string& b) -> const Menu& { return menu(a,b); });
                if (!match) return {};
                string order = "[";
                for (int index : match->order) {
                    if (order.size() > 1) order += ',';
                    order += char('0'+index);
                }
                return "{\"kind\":\"quadruple\",\"order\":" + order + "],\"left\":"
                     + triple(match->first) + ",\"right\":" + triple(match->second) + "}";
            }
            default: throw std::logic_error("bad terminal sphere width");
        }
    }

    static std::map<string,Split> contact_menu(const string& a, const string& b,
                                               std::optional<size_t> at_a = {},
                                               std::optional<size_t> at_b = {}) {
        std::map<string,Split> out;
        const auto aa = a+a, bb = b+b;
        const size_t a_cut = at_a ? (*at_a+1)%a.size() : 0;
        const size_t b_cut = at_b.value_or(0);
        const size_t a_end = at_a ? a_cut+1 : a.size();
        const size_t b_end = at_b ? b_cut+1 : b.size();
        for (size_t i=a_cut; i<a_end; ++i) {
            const auto left = string_view(aa).substr(i,a.size());
            for (size_t j=b_cut; j<b_end; ++j) {
                const auto right = string_view(bb).substr(j,b.size());
                if (left.back() != invert(right.front())) continue;
                const auto merged = canonical(product(left,right));
                if (!out.count(merged)) out.emplace(merged,Split{string(left),string(right),{}});
            }
        }
        return out;
    }

public:
    explicit Equation(Counters& counts, size_t max_rejected = std::numeric_limits<size_t>::max(),
                      bool rooted_contractions = false)
        : counts(counts), max_rejected(max_rejected), rooted_contractions(rooted_contractions) {}

    string solve(const Words& words) {
        if (!rooted_contractions) return solve_cycles(words);
        auto cycles = words;
        for (auto& word : cycles) word = canonical(word);
        return solve_cycles(cycles);
    }

private:
    string solve_cycles(const Words& words) {
        // A rejected pair costs very little to recompute. Reserve the rooted
        // rejection cache for states whose decision entails contractions.
        if (rooted_contractions && words.size() <= 2) return terminal(words);
        auto sorted = words;
        if (!rooted_contractions) for (auto& word : sorted) word = canonical(word);
        std::sort(sorted.begin(),sorted.end());
        string key;
        for (const auto& word : sorted) key += word + '\t';
        if (rejected.count(key)) { ++counts.memo_hits; return {}; }
        if (words.size() <= 4 && !rooted_contractions) {
            auto result = terminal(words);
            if (result.empty()) remember_negative(std::move(key));
            return result;
        }

        size_t root = std::min_element(words.begin(), words.end(),
            [](const string& a, const string& b) { return a.size() < b.size(); }) - words.begin();
        std::optional<size_t> endpoint;
        if (rooted_contractions) {
            size_t least_partners = std::numeric_limits<size_t>::max();
            constexpr string_view alphabet = "xXyY";
            std::array<size_t,4> counts{};
            for (const auto& word : words) for (const char letter : word) ++counts[alphabet.find(letter)];
            for (size_t index=0; index<words.size(); ++index) {
                const auto& word = words[index];
                for (size_t position=0; position<word.size(); ++position) {
                    const char inverse = invert(word[position]);
                    const size_t total = counts[alphabet.find(inverse)];
                    if (total >= least_partners || word.find(inverse) != string::npos) continue;
                    least_partners = total;
                    root = index;
                    endpoint = position;
                }
            }
            if (!endpoint) {
                // Cutting along a self-arc would give a boundary segment
                // whose exponent vector balances a subset of the other rows.
                std::vector<std::pair<int,int>> vectors;
                for (const auto& word : words) vectors.push_back(vector(word));
                for (size_t index=0; index<words.size(); ++index) {
                    std::vector<std::pair<int,int>> sums{{0,0}};
                    for (size_t other=0; other<words.size(); ++other) if (other != index) {
                        const auto [x,y] = vectors[other];
                        const size_t size = sums.size();
                        for (size_t i=0; i<size; ++i) sums.emplace_back(sums[i].first+x,sums[i].second+y);
                        std::sort(sums.begin(),sums.end());
                        sums.erase(std::unique(sums.begin(),sums.end()),sums.end());
                    }
                    const auto& word = words[index];
                    for (size_t position=0; position<word.size(); ++position) {
                        const char mate = invert(word[position]);
                        const size_t partners = counts[alphabet.find(mate)]
                            - std::count(word.begin(),word.end(),mate);
                        if (partners >= least_partners) continue;
                        int x = 0, y = 0;
                        bool can_pair_on_boundary = false;
                        for (size_t step=1; step<word.size(); ++step) {
                            const char letter = word[(position+step)%word.size()];
                            if (letter == mate && std::binary_search(sums.begin(),sums.end(),std::pair{-x,-y})) {
                                can_pair_on_boundary = true;
                                break;
                            }
                            x += (letter == 'x') - (letter == 'X');
                            y += (letter == 'y') - (letter == 'Y');
                        }
                        if (!can_pair_on_boundary) {
                            least_partners = partners;
                            root = index;
                            endpoint = position;
                        }
                    }
                    if (least_partners == 0) break;
                }
            }
        }
        std::set<std::pair<string,string>> tested_pairs;
        for (size_t i=0; i<words.size(); ++i) for (size_t j=i+1; j<words.size(); ++j) {
            // Self-arcs at one boundary alone would be a noncrossing pairing
            // on a disk, forcing an adjacent inverse pair on that boundary.
            if (rooted_contractions && i != root && j != root) continue;
            const auto first_class = rooted_contractions ? words[i] : canonical(words[i]);
            const auto second_class = rooted_contractions ? words[j] : canonical(words[j]);
            const auto types = std::minmax(first_class,second_class);
            if (!tested_pairs.emplace(types.first,types.second).second) continue;
            auto rest = words;
            rest.erase(rest.begin()+j);
            rest.erase(rest.begin()+i);
            for (const auto& [coefficient,witness] : contact_menu(words[i],words[j],
                    i == root ? endpoint : std::nullopt, j == root ? endpoint : std::nullopt)) {
                ++counts.contractions;
                if (!coefficient.empty()) rest.push_back(coefficient);
                const auto child = solve_cycles(rest);
                if (!child.empty())
                    return "{\"kind\":\"contract\",\"i\":" + std::to_string(i) + ",\"j\":"
                         + std::to_string(j) + ",\"merge\":" + triple(witness) + ",\"coefficient\":\""
                         + coefficient + "\",\"child\":" + child + "}";
                if (!coefficient.empty()) rest.pop_back();
            }
        }
        remember_negative(std::move(key));
        return {};
    }
};

string oriented(const string& word, int sign) {
    return sign < 0 ? inverse(word) : word;
}

string check(const string& a, const string& b, bool alternating, Counters& counts,
             int fixed_count = 3) {
    Equation eq(counts);
    for (const auto& pair : {std::array<string,2>{a,b}, {b,a}}) {
        const auto& r = pair[0];
        const auto& d = pair[1];
        const auto [x,y] = vector(r);
        const auto [u,v] = vector(d);
        if (std::abs(x*v-y*u) != 1) throw std::logic_error("non-unimodular source");
        const auto run = [&](Words factors,int sx,int sy, int first_sign, int sum) -> string {
            const auto goal = primitive(sx,sy);
            factors.push_back(inverse(goal));
            ++counts.top;
            const auto solved = eq.solve(factors);
            if (solved.empty()) return {};
            return "{\"source\":" + json_array({a,b}) + ",\"working_pair\":" + json_array({r,d})
                 + ",\"primitive\":\"" + goal + "\",\"first_sign\":" + std::to_string(first_sign)
                 + ",\"coefficient\":" + std::to_string(sum) + ",\"boundary\":" + json_array(factors)
                 + ",\"equation\":" + solved + "}";
        };
        if (!alternating) {
            for (int sum = -fixed_count; sum <= fixed_count; sum += 2) {
                Words factors{r};
                const int positive_count = (sum+fixed_count)/2;
                for (int i=0; i<fixed_count; ++i) factors.push_back(oriented(d,i<positive_count?1:-1));
                if (auto hit=run(std::move(factors),x+sum*u,y+sum*v,0,sum); !hit.empty())
                    return hit;
            }
        } else {
            // The last two products can keep C=A B^s fixed. Expand its two
            // copies independently, which relaxes their actual shared chart.
            for (int s : {-1,1}) for (int sum : {-2,0,2}) {
                const int first = sum<0 ? -1 : 1, second = sum<=0 ? -1 : 1;
                Words factors{d,oriented(r,first),oriented(d,s*first),
                              oriented(r,second),oriented(d,s*second)};
                if (auto hit=run(std::move(factors),sum*x+(1+sum*s)*u,
                                 sum*y+(1+sum*s)*v,s,sum); !hit.empty())
                    return hit;
            }
        }
    }
    return {};
}
} // namespace

#ifndef AC_ROUND19_THREE_PRODUCTS_LIBRARY
int main(int argc, char** argv) {
    try {
        if (argc != 4) throw std::invalid_argument("usage: three-products fixed|fixed4|alternating pairs.tsv workers");
        const string mode = argv[1];
        if (mode != "fixed" && mode != "fixed4" && mode != "alternating")
            throw std::invalid_argument("mode");
        std::ifstream input(argv[2]);
        const unsigned workers = std::stoul(argv[3]);
        if (!input || !workers) throw std::invalid_argument("invalid input");
        std::vector<std::pair<string,string>> rows;
        for (string a,b; input >> a >> b;) rows.emplace_back(a,b);
        std::atomic<size_t> cursor{0};
        std::vector<Counters> counts(workers);
        std::vector<string> hits(rows.size());
        std::vector<std::future<void>> pool;
        for (unsigned i=0; i<workers; ++i) pool.push_back(std::async(std::launch::async,[&,i] {
            for (size_t j; (j=cursor++) < rows.size();)
                hits[j] = check(rows[j].first,rows[j].second,mode=="alternating",counts[i],
                                mode=="fixed4" ? 4 : 3);
        }));
        for (auto& task : pool) task.get();
        Counters total;
        for (const auto& count : counts) {
            total.top += count.top;
            total.contractions += count.contractions;
            total.memo_hits += count.memo_hits;
            total.terminal += count.terminal;
        }
        std::cout << "{\"mode\":\"" << mode << "\",\"rows_checked\":" << rows.size()
                  << ",\"slopes\":" << total.top << ",\"contractions\":" << total.contractions
                  << ",\"cached_negative\":" << total.memo_hits << ",\"terminal\":" << total.terminal
                  << ",\"hits\":[";
        bool comma=false;
        for (const auto& hit : hits) if (!hit.empty()) {
            if (comma) std::cout << ',';
            comma=true;
            std::cout << hit;
        }
        std::cout << "]}\n";
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
#endif
