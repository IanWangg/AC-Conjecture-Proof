// Search conjugacy separators with the retained donor killed. The Python
// replayer independently checks every returned marking.
#include <algorithm>
#include <array>
#include <iostream>
#include <map>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>

namespace {
constexpr int max_points = 10;
using Permutation = std::array<int, max_points>;
using Marking = std::array<Permutation, 4>;

int letter(char symbol) {
    switch (symbol) {
        case 'x': return 0;
        case 'X': return 1;
        case 'y': return 2;
        case 'Y': return 3;
        default: throw std::invalid_argument("invalid free letter");
    }
}

std::vector<int> program(const std::string& word) {
    std::vector<int> instructions;
    for (auto at = word.rbegin(); at != word.rend(); ++at) instructions.push_back(letter(*at));
    return instructions;
}

int act(const std::vector<int>& word, const Marking& marking, int point) {
    for (int symbol : word) point = marking[symbol][point];
    return point;
}

bool kills(const std::vector<int>& word, const Marking& marking, int degree) {
    for (int point = 0; point < degree; ++point)
        if (act(word, marking, point) != point) return false;
    return true;
}

unsigned long long cycle_type(const std::vector<int>& word, const Marking& marking, int degree) {
    unsigned seen = 0;
    unsigned long long shape = 0;
    for (int base = 0; base < degree; ++base) {
        if (seen & (1U << base)) continue;
        int point = base, length = 0;
        do {
            seen |= 1U << point;
            point = act(word, marking, point);
            ++length;
        } while (point != base);
        shape += 1ULL << (4 * (length - 1));
    }
    return shape;
}

std::vector<Permutation> cycle_representatives(int degree) {
    std::vector<Permutation> result;
    Permutation current{};
    const auto visit = [&](auto&& visit, int next, int minimum) -> void {
        if (next == degree) {
            result.push_back(current);
            return;
        }
        for (int length = minimum; length <= degree - next; ++length) {
            for (int at = next; at < next + length; ++at)
                current[at] = at == next + length - 1 ? next : at + 1;
            visit(visit, next + length, length);
        }
    };
    visit(visit, 0, 1);
    return result;
}

Permutation inverse(const Permutation& value, int degree) {
    Permutation result{};
    for (int point = 0; point < degree; ++point) result[value[point]] = point;
    return result;
}

void print(const Permutation& value, int degree) {
    for (int point = 0; point < degree; ++point)
        std::cout << (point ? "," : "") << value[point] + 1;
}

void search(const std::string& frozen, const std::string& original, int maximum) {
    const auto donor = program(frozen), source = program(original);
    std::map<std::string, std::vector<int>> pending;
    for (std::string target; std::cin >> target;) pending.emplace(target, program(target));
    for (int degree = 2; degree <= maximum && !pending.empty(); ++degree) {
        Permutation identity{};
        std::iota(identity.begin(), identity.end(), 0);
        for (const auto& x : cycle_representatives(degree)) {
            Marking marking{x, inverse(x, degree), identity, identity};
            do {
                marking[3] = inverse(marking[2], degree);
                if (!kills(donor, marking, degree)) continue;
                const auto want = cycle_type(source, marking, degree);
                for (auto at = pending.begin(); at != pending.end();) {
                    if (cycle_type(at->second, marking, degree) == want) {
                        ++at;
                        continue;
                    }
                    std::cout << at->first << '\t';
                    print(marking[0], degree);
                    std::cout << '\t';
                    print(marking[2], degree);
                    std::cout << '\n';
                    at = pending.erase(at);
                }
                if (pending.empty()) return;
            } while (std::next_permutation(marking[2].begin(), marking[2].begin() + degree));
        }
    }
}
}  // namespace

int main(int argc, char** argv) {
    try {
        if (argc != 4) throw std::invalid_argument("usage: permutation-contacts donor original max-degree");
        const auto degree = std::stoi(argv[3]);
        if (degree < 2 || degree > max_points) throw std::invalid_argument("unsupported degree");
        search(argv[1], argv[2], degree);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
