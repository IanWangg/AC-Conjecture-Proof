// Exact spherical four-boundary test for an uncapped two-product primitive.
#include <algorithm>
#include <array>
#include <atomic>
#include <fstream>
#include <future>
#include <iostream>
#include <map>
#include <numeric>
#include <optional>
#include <stdexcept>
#include <string>
#include <string_view>
#include <unordered_map>
#include <vector>

namespace {
using std::string;
using std::string_view;

char invert(char c) { return c >= 'a' ? c - 'a' + 'A' : c - 'A' + 'a'; }

string inverse(string_view word) {
    string out;
    out.reserve(word.size());
    for (auto c = word.rbegin(); c != word.rend(); ++c) out += invert(*c);
    return out;
}

string rotate(string_view word, size_t cut) {
    return string(word.substr(cut)) + string(word.substr(0, cut));
}

string canonical(string_view word) {
    if (word.empty()) return {};
    size_t least = 0;
    for (size_t i = 1, j = 0; i < word.size();) {
        const char a = word[(least+j) % word.size()], b = word[(i+j) % word.size()];
        if (a == b && j+1 < word.size()) { ++j; continue; }
        if (a <= b) i += j+1;
        else { least = i; ++i; }
        j = 0;
    }
    return rotate(word, least);
}

string product(string_view a, string_view b) {
    while (!a.empty() && !b.empty() && a.back() == invert(b.front())) {
        a.remove_suffix(1);
        b.remove_prefix(1);
    }
    while (!a.empty() && !b.empty() && a.front() == invert(b.back())) {
        a.remove_prefix(1);
        b.remove_suffix(1);
    }
    if (a.empty()) while (b.size() > 1 && b.front() == invert(b.back())) {
        b.remove_prefix(1); b.remove_suffix(1);
    }
    if (b.empty()) while (a.size() > 1 && a.front() == invert(a.back())) {
        a.remove_prefix(1); a.remove_suffix(1);
    }
    return string(a) + string(b);
}

struct Split {
    string a, b, bridge;
};

using Menu = std::unordered_map<string, Split>;

Menu zero_bridge(const string& a, const string& b) {
    Menu outputs;
    const string aa = a+a, bb = b+b;
    for (size_t i = 0; i < a.size(); ++i) {
        const auto left = string_view(aa).substr(i, a.size());
        for (size_t j = 0; j < b.size(); ++j) {
            const auto right = string_view(bb).substr(j,b.size());
            const auto image = canonical(product(left, right));
            if (!outputs.count(image)) outputs.emplace(image, Split{string(left), string(right), {}});
        }
    }
    return outputs;
}

bool is_rotation(string_view word, const string& doubled, size_t size) {
    return word.size() == size && doubled.find(word) < size;
}

std::optional<Split> positive_bridge(const string& a, const string& b, const string& target) {
    if (target.size() <= a.size()+b.size() || (target.size()-a.size()-b.size()) % 2)
        return {};
    const size_t gap = (target.size()-a.size()-b.size()) / 2;
    const string aa = a+a, bb = b+b, tt = target+target;
    for (size_t i = 0; i < target.size(); ++i) {
        const auto left = string_view(tt).substr(i,a.size());
        if (!is_rotation(left, aa, a.size())) continue;
        const auto right = string_view(tt).substr(i+a.size()+gap,b.size());
        if (!is_rotation(right, bb, b.size())) continue;
        const auto bridge = string_view(tt).substr(i+a.size(),gap);
        const auto back = string_view(tt).substr(i+a.size()+gap+b.size(),gap);
        if (back == inverse(bridge)) return Split{string(left),string(right),string(bridge)};
    }
    return {};
}

struct Meeting {
    std::array<int, 4> order;
    Split first, second;
};

template<class BuildMenu>
std::optional<Meeting> sphere_with_menus(const std::array<string,4>& rows, bool coincident,
                                       BuildMenu build_menu) {
    for (const auto order : {std::array<int,4>{0,1,2,3}, {0,2,1,3}, {0,3,1,2}}) {
        const auto [i,j,k,l] = order;
        if (coincident && j == 2) continue;
        const auto& left = build_menu(rows[i], rows[j]);
        // Index the right product by its inverse, to compare both sides literally.
        const auto& right = build_menu(inverse(rows[l]), inverse(rows[k]));
        for (const auto& [needed, witness] : left) {
            if (const auto entry = right.find(needed); entry != right.end())
                return Meeting{order,witness,{inverse(entry->second.b),inverse(entry->second.a),{}}};
            if (auto bridge = positive_bridge(rows[k],rows[l],inverse(needed)))
                return Meeting{order,witness,std::move(*bridge)};
        }
        for (const auto& [needed, witness] : right)
            if (auto bridge = positive_bridge(rows[i],rows[j],needed))
                return Meeting{order,std::move(*bridge),{inverse(witness.b),inverse(witness.a),{}}};
    }
    return {};
}

std::optional<Meeting> sphere(const std::array<string,4>& rows, bool coincident) {
    return sphere_with_menus(rows,coincident,zero_bridge);
}

std::pair<int,int> vector(const string& word) {
    int x = 0, y = 0;
    for (char c : word) {
        if (c == 'x') ++x;
        else if (c == 'X') --x;
        else if (c == 'y') ++y;
        else if (c == 'Y') --y;
        else throw std::invalid_argument("invalid free letter");
    }
    return {x,y};
}

string positive(int x, int y) {
    if (!x) return "y";
    if (!y) return "x";
    if (x == y) return "xy";
    const auto before = x > y ? positive(x-y,y) : positive(x,y-x);
    string after;
    for (char c : before) {
        if (c == (x > y ? 'y' : 'x')) after += "xy";
        else after += c;
    }
    return after;
}

string primitive(int x, int y) {
    if (std::gcd(x,y) != 1) throw std::logic_error("non-unimodular source");
    auto word = positive(std::abs(x),std::abs(y));
    for (char& c : word) if ((c == 'x' && x < 0) || (c == 'y' && y < 0)) c = invert(c);
    return word;
}

string triple(const Split& split) {
    return "[\"" + split.a + "\",\"" + split.b + "\",\"" + split.bridge + "\"]";
}

string scan(const string& a, const string& b) {
    const std::array<string,2> pair{a,b};
    for (int donor = 0; donor < 2; ++donor) {
        const auto& fixed = pair[donor];
        const auto& other = pair[1-donor];
        const auto [x,y] = vector(other);
        const auto [u,v] = vector(fixed);
        if (std::abs(x*v-y*u) != 1) throw std::logic_error("bad source determinant");
        for (const int sum : {0,2,-2}) {
            const auto p = primitive(x+sum*u,y+sum*v);
            const auto f = sum < 0 ? inverse(fixed) : fixed;
            const auto g = sum <= 0 ? inverse(fixed) : fixed;
            if (const auto meeting = sphere({other,f,g,inverse(p)},sum != 0)) {
                string order = "[";
                for (const int i : meeting->order) {
                    if (order.size() > 1) order += ',';
                    order += char('0'+i);
                }
                return "{\"source\":[\"" + a + "\",\"" + b + "\"],\"donor_index\":"
                     + std::to_string(donor) + ",\"axial_coefficient\":" + std::to_string(sum)
                     + ",\"primitive\":\"" + p + "\",\"order\":" + order + "],\"left\":"
                     + triple(meeting->first) + ",\"right\":" + triple(meeting->second) + "}";
            }
        }
    }
    return {};
}
} // namespace

#ifndef AC_ROUND18_TWO_PRODUCTS_LIBRARY
int main(int argc, char** argv) {
    try {
        if (argc != 3) throw std::invalid_argument("usage: two-products pairs.tsv workers");
        std::ifstream input(argv[1]);
        const unsigned workers = std::stoul(argv[2]);
        if (!input || !workers) throw std::invalid_argument("invalid inputs");
        size_t checked = 0;
        string hit;
        while (hit.empty()) {
            std::vector<std::pair<string,string>> batch;
            for (string a,b; batch.size() < 1024 && input >> a >> b;)
                batch.emplace_back(std::move(a),std::move(b));
            if (batch.empty()) break;
            std::atomic<size_t> cursor{0};
            std::vector<std::future<std::pair<size_t,string>>> pool;
            for (unsigned i=0; i<workers; ++i) pool.push_back(std::async(std::launch::async,[&] {
                size_t local = 0;
                string witness;
                for (size_t j; (j=cursor++) < batch.size() && witness.empty();) {
                    witness=scan(batch[j].first,batch[j].second);
                    ++local;
                }
                return std::pair{local,witness};
            }));
            for (auto& task : pool) {
                auto [local,witness]=task.get();
                checked+=local;
                if (hit.empty()) hit=std::move(witness);
            }
            if (checked % 4096 == 0) std::cerr << "checked " << checked << '\n';
        }
        if (input.bad()) throw std::runtime_error("input read error");
        std::cout << "{\"rows_checked\":" << checked << ",\"complete\":" << (hit.empty() ? "true" : "false")
                  << ",\"hit\":" << (hit.empty()?"null":hit) << "}\n";
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
#endif
