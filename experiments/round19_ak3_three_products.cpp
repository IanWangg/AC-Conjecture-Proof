// Exact spherical contractions for three fixed-donor products and an alternating relaxation.
#define AC_ROUND18_TWO_PRODUCTS_LIBRARY
#include "round18_ak3_two_products.cpp"

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
                return canonical(words[0]) == canonical(inverse(words[1]))
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

    static std::map<string,Split> contact_menu(const string& a, const string& b) {
        std::map<string,Split> out;
        const auto aa = a+a, bb = b+b;
        for (size_t i=0; i<a.size(); ++i) {
            const auto left = string_view(aa).substr(i,a.size());
            for (size_t j=0; j<b.size(); ++j) {
                const auto right = string_view(bb).substr(j,b.size());
                if (left.back() != invert(right.front())) continue;
                const auto merged = canonical(product(left,right));
                if (!out.count(merged)) out.emplace(merged,Split{string(left),string(right),{}});
            }
        }
        return out;
    }

public:
    explicit Equation(Counters& counts) : counts(counts) {}

    string solve(const Words& words) {
        auto sorted = words;
        for (auto& word : sorted) word = canonical(word);
        std::sort(sorted.begin(),sorted.end());
        string key;
        for (const auto& word : sorted) key += word + '\t';
        if (rejected.count(key)) { ++counts.memo_hits; return {}; }
        if (words.size() <= 4) {
            auto result = terminal(words);
            if (result.empty()) rejected.emplace(std::move(key));
            return result;
        }

        std::set<std::pair<string,string>> tested_pairs;
        for (size_t i=0; i<words.size(); ++i) for (size_t j=i+1; j<words.size(); ++j) {
            const auto first_class = canonical(words[i]), second_class = canonical(words[j]);
            const auto types = std::minmax(first_class,second_class);
            if (!tested_pairs.emplace(types.first,types.second).second) continue;
            auto rest = words;
            rest.erase(rest.begin()+j);
            rest.erase(rest.begin()+i);
            for (const auto& [coefficient,witness] : contact_menu(words[i],words[j])) {
                ++counts.contractions;
                if (!coefficient.empty()) rest.push_back(coefficient);
                const auto child = solve(rest);
                if (!child.empty())
                    return "{\"kind\":\"contract\",\"i\":" + std::to_string(i) + ",\"j\":"
                         + std::to_string(j) + ",\"merge\":" + triple(witness) + ",\"coefficient\":\""
                         + coefficient + "\",\"child\":" + child + "}";
                if (!coefficient.empty()) rest.pop_back();
            }
        }
        rejected.emplace(std::move(key));
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
