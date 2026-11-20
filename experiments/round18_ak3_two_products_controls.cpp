// Independent small sphere audit by literal pairings of boundary letters.
#define AC_ROUND18_TWO_PRODUCTS_LIBRARY
#include "round18_ak3_two_products.cpp"

#include <random>

namespace {
string reference_reduce(string_view word) {
    string stack;
    for (const char c : word) {
        if (!stack.empty() && stack.back() == invert(c)) stack.pop_back();
        else stack.push_back(c);
    }
    size_t first = 0, last = stack.size();
    while (first+1 < last && stack[first] == invert(stack[last-1])) { ++first; --last; }
    return stack.substr(first,last-first);
}

string reference_rotate(const string& word) {
    string least = word;
    for (size_t i = 1; i < word.size(); ++i)
        least = std::min(least, word.substr(i)+word.substr(0,i));
    return least;
}

bool planar(const std::array<string,4>& words) {
    string labels;
    std::vector<int> around, vertex;
    for (int v = 0; v < int(words.size()); ++v) {
        const int offset = labels.size(), width = words[v].size();
        labels += words[v];
        for (int j = 0; j < width; ++j) {
            around.push_back(offset+(j+1)%width);
            vertex.push_back(v);
        }
    }
    std::vector<int> paired(labels.size(),-1);
    const auto search = [&](auto&& search) -> bool {
        const auto found = std::find(paired.begin(),paired.end(),-1);
        if (found == paired.end()) {
            std::array<int,4> components{0,1,2,3};
            for (size_t i = 0; i < paired.size(); ++i) {
                const int a = components[vertex[i]], b = components[vertex[paired[i]]];
                for (auto& v : components) if (v == b) v = a;
            }
            std::sort(components.begin(),components.end());
            const auto conn = std::unique(components.begin(),components.end()) - components.begin();
            std::vector<bool> seen(labels.size());
            int faces = 0;
            for (size_t i = 0; i < seen.size(); ++i) {
                if (seen[i]) continue;
                ++faces;
                for (auto j = i; !seen[j]; j = around[paired[j]]) seen[j] = true;
            }
            const int edges = labels.size()/2;
            return 2*conn == 4 - edges + faces;
        }
        const auto i = found-paired.begin();
        for (auto j = i+1; j < int(paired.size()); ++j) {
            if (paired[j] >= 0 || labels[j] != invert(labels[i])) continue;
            paired[i] = j;
            paired[j] = i;
            if (search(search)) return true;
            paired[i] = paired[j] = -1;
        }
        return false;
    };
    return search(search);
}

string random_cycle(std::mt19937& random, unsigned width) {
    for (;;) {
        string word;
        while (word.size() < width) {
            const char c = "xXyY"[random()%4];
            if (!word.empty() && word.back() == invert(c)) continue;
            word += c;
        }
        if (word.front() != invert(word.back())) return word;
    }
}
} // namespace

int main() {
    std::mt19937 random(1804);
    for (int i = 0; i < 20000; ++i) {
        const auto a = random_cycle(random,1+random()%74);
        const auto b = random_cycle(random,1+random()%74);
        if (canonical(a) != reference_rotate(a) || product(a,b) != reference_reduce(a+b))
            throw std::logic_error("rotation or cancellation controls disagree");
    }
    int positive = 0, cases = 0;
    while (cases < 4000) {
        std::array<string,4> words;
        int x = 0, y = 0;
        for (auto& w : words) {
            w = random_cycle(random,1+random()%4);
            const auto [a,b] = vector(w);
            x += a; y += b;
        }
        if (x || y) continue;
        ++cases;
        const bool value = planar(words);
        if (value != sphere(words,false).has_value())
            throw std::logic_error("sphere pairings disagree: "+words[0]+" "+words[1]+" "+words[2]+" "+words[3]);
        positive += value;
    }
    std::cout << "{\"rotations_reductions\":20000,\"sphere_cases\":" << cases
              << ",\"positive\":" << positive << ",\"negative\":" << cases-positive << "}\n";
}
