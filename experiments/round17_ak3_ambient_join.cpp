// Exact simultaneous Whitehead minima for two cyclic rows, without packed limits.
#define AC_ROUND05_ORBITS_LIBRARY
#include "round05_ak3_orbits.cpp"

#include <set>

namespace {
using Pair = std::pair<std::string, std::string>;

Pair key(std::string a, std::string b) {
    a = round01::canonical_reduced(a);
    b = round01::canonical_reduced(b);
    return std::minmax(a,b);
}

Pair signed_key(const Pair& source) {
    Pair best = key(source.first, source.second);
    for (const auto& marking : {"xXyY", "XxyY", "xXYy", "XxYy", "yYxX", "YyxX", "yYXx", "YyXx"}) {
        const auto change = [&](std::string word) {
            for (auto& letter : word) letter = marking[orbit_search::digit(letter)];
            return word;
        };
        best = std::min(best, key(change(source.first), change(source.second)));
    }
    return best;
}

size_t energy(const Pair& pair) { return pair.first.size() + pair.second.size(); }

std::set<Pair> shears(const Pair& pair) {
    std::set<Pair> result;
    for (const char generator : {'x','y'}) {
        const char inverse_letter = invchar(generator);
        const char other = generator == 'x' ? 'y' : 'x';
        for (const char side : {other, invchar(other)})
            for (const bool prefix : {false, true}) {
                const std::string positive = prefix ? std::string{side,generator} : std::string{generator,side};
                const auto negative = inverse(positive);
                const auto image = [&](const std::string& word) {
                    std::string changed;
                    for (const auto c : word) {
                        if (c == generator) changed += positive;
                        else if (c == inverse_letter) changed += negative;
                        else changed += c;
                    }
                    return cyclic(changed);
                };
                auto left = image(pair.first), right = image(pair.second);
                if (left.size() + right.size() <= energy(pair))
                    result.insert(signed_key({std::move(left),std::move(right)}));
            }
    }
    return result;
}

class Minima {
    std::map<Pair, Pair> cache;

public:
    Pair reduce(Pair current) {
        std::vector<Pair> path;
        Pair result;
        for (;;) {
            if (const auto it = cache.find(current); it != cache.end()) {
                result = it->second;
                break;
            }
            path.push_back(current);
            const auto successors = shears(current);
            const auto shorter = std::find_if(successors.begin(), successors.end(), [&](const auto& next) {
                return energy(next) < energy(current);
            });
            if (shorter != successors.end()) {
                current = *shorter;
                continue;
            }
            std::set<Pair> plateau{current};
            std::vector<Pair> queue{current};
            for (size_t i = 0; i < queue.size(); ++i)
                for (const auto& next : shears(queue[i])) {
                    if (energy(next) != energy(current))
                        throw std::logic_error("nonminimum Whitehead level");
                    if (plateau.insert(next).second) queue.push_back(next);
                }
            result = *plateau.begin();
            for (const auto& mark : plateau) cache.emplace(mark,result);
            break;
        }
        for (const auto& step : path) cache.emplace(step,result);
        return result;
    }
};

void display(const Pair& pair) {
    std::cout << "[\"" << pair.first << "\",\"" << pair.second << "\"]";
}

int scan(const char* forward_path, const char* archive_path) {
    Minima minima;
    if (minima.reduce(signed_key({"x","y"})) != minima.reduce(signed_key({"x","xy"})))
        throw std::logic_error("positive Whitehead control failed");
    std::ifstream archive(archive_path), forward(forward_path);
    if (!forward || !archive) throw std::runtime_error("cannot open pair collection");
    std::map<Pair,Pair> wanted;
    std::set<Pair> forward_classes;
    size_t archive_rows = 0, forward_rows = 0, matched_rows = 0;
    Pair pair, first_pair, first_archive, first_minimum;
    while (archive >> pair.first >> pair.second) {
        if (cyclic(pair.first) != pair.first || cyclic(pair.second) != pair.second)
            throw std::runtime_error("noncyclic archive pair");
        ++archive_rows;
        wanted.try_emplace(minima.reduce(signed_key(pair)), pair);
    }
    while (forward >> pair.first >> pair.second) {
        if (cyclic(pair.first) != pair.first || cyclic(pair.second) != pair.second)
            throw std::runtime_error("noncyclic forward pair");
        ++forward_rows;
        const auto minimal = minima.reduce(signed_key(pair));
        forward_classes.insert(minimal);
        const auto join = wanted.find(minimal);
        if (join != wanted.end() && matched_rows++ == 0) {
            first_pair = pair;
            first_archive = join->second;
            first_minimum = minimal;
        }
    }
    if (!archive.eof() || !forward.eof() || !archive_rows || !forward_rows)
        throw std::runtime_error("empty or malformed input");
    std::cout << "{\"archive_rows\":" << archive_rows << ",\"archive_classes\":" << wanted.size()
              << ",\"forward_rows\":" << forward_rows << ",\"forward_classes\":" << forward_classes.size()
              << ",\"matching_forward_rows\":" << matched_rows << ",\"first_join\":";
    if (matched_rows) {
        std::cout << "{\"forward\":";
        display(first_pair);
        std::cout << ",\"archive\":";
        display(first_archive);
        std::cout << ",\"canonical_minimum\":";
        display(first_minimum);
        std::cout << '}';
    } else std::cout << "null";
    std::cout << "}\n";
    return 0;
}
}

int main(int argc,char** argv) {
    try {
        if (argc != 3) throw std::runtime_error("usage: ambient-join forward.tsv archive.tsv");
        return scan(argv[1],argv[2]);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
