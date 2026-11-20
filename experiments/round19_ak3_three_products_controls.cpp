// Separate literal pairing audit of the five- and six-boundary decisions.
#define AC_ROUND19_THREE_PRODUCTS_LIBRARY
#include "round19_ak3_three_products.cpp"

#include <random>

namespace {
bool planar(const Words& words) {
    string labels;
    std::vector<size_t> rotation, vertex;
    for (size_t v = 0; v < words.size(); ++v) {
        const size_t offset = labels.size(), width = words[v].size();
        labels += words[v];
        for (size_t j = 0; j < width; ++j) {
            rotation.push_back(offset + (j+1)%width);
            vertex.push_back(v);
        }
    }
    const size_t open = labels.size();
    std::vector<size_t> mates(open,open);
    const auto search = [&](auto&& search) -> bool {
        const auto first = std::find(mates.begin(),mates.end(),open) - mates.begin();
        if (size_t(first) == open) {
            std::vector<size_t> components(words.size());
            std::iota(components.begin(),components.end(),0);
            for (size_t i = 0; i < mates.size(); ++i) {
                const auto a = components[vertex[i]], b = components[vertex[mates[i]]];
                for (auto& v : components) if (v == b) v = a;
            }
            std::sort(components.begin(),components.end());
            const auto connected = std::unique(components.begin(),components.end()) - components.begin();
            std::vector<bool> visited(labels.size());
            size_t faces = 0;
            for (size_t i = 0; i < labels.size(); ++i) {
                if (visited[i]) continue;
                ++faces;
                for (auto j = i; !visited[j]; j = rotation[mates[j]]) visited[j] = true;
            }
            return 2*size_t(connected) + labels.size()/2 == words.size() + faces;
        }
        for (size_t j = first+1; j < mates.size(); ++j) {
            if (mates[j] != open || labels[j] != invert(labels[first])) continue;
            mates[first] = j;
            mates[j] = first;
            if (search(search)) return true;
            mates[first] = mates[j] = open;
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
            if (word.empty() || word.back() != invert(c)) word += c;
        }
        if (word.front() != invert(word.back())) return word;
    }
}
} // namespace

#ifndef AC_ROUND19_PAIRING_LIBRARY
int main() {
    std::mt19937 random(1905);
    std::cout << "[";
    for (size_t width : {5,6}) {
        unsigned seen = 0, yes = 0;
        while (seen < 2000) {
            Words words(width);
            int x = 0, y = 0;
            size_t total = 0;
            for (auto& word : words) {
                word = random_cycle(random,1+random()%5);
                const auto [a,b] = vector(word);
                x += a; y += b;
                total += word.size();
            }
            if (x || y || total > 20) continue;
            const bool truth = planar(words);
            Counters counts;
            if (truth != !Equation(counts).solve(words).empty())
                throw std::logic_error("pairing disagreement");
            ++seen;
            yes += truth;
        }
        if (width == 6) std::cout << ',';
        std::cout << "{\"boundaries\":" << width << ",\"positive\":" << yes
                  << ",\"negative\":" << seen-yes << "}";
    }
    std::cout << "]\n";
}
#endif
