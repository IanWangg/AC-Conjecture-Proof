#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <string_view>
#include <utility>
#include <vector>

namespace {

using PairCode = __uint128_t;
using Pair = std::pair<std::string, std::string>;
constexpr unsigned row_cache_bits = 22;

char inv(char c) { return c ^ 32; }
unsigned letter(char c) { return (c | 32) - 'x'; }

std::string inverse(std::string_view word) {
    std::string result;
    for (auto at = word.rbegin(); at != word.rend(); ++at) result += inv(*at);
    return result;
}

void push(std::string& stack, char c) {
    if (!stack.empty() && stack.back() == inv(c)) stack.pop_back();
    else stack.push_back(c);
}

std::string_view cyclic_part(std::string_view word) {
    while (word.size() > 1 && word.front() == inv(word.back())) {
        word.remove_prefix(1);
        word.remove_suffix(1);
    }
    return word;
}

std::string canonical(std::string_view word) {
    word = cyclic_part(word);
    if (word.empty()) return "";
    std::string result(word);
    const auto reversed = inverse(word);
    for (const std::string_view oriented : {word, std::string_view(reversed)}) {
        for (size_t start = 0; start < oriented.size(); ++start) {
            std::string rotation(oriented.substr(start));
            rotation += oriented.substr(0, start);
            result = std::min(result, rotation);
        }
    }
    return result;
}

struct Word {
    std::string text;
    std::array<int, 3> exponent{};
    uint64_t code = 1;

    void initialize() {
        exponent = {0, 0, 0};
        code = 1;
        for (const auto c : text) {
            const auto i = letter(c);
            if (i >= exponent.size()) throw std::logic_error("unsupported letter");
            const bool positive = c >= 'x';
            exponent[i] += positive ? 1 : -1;
            code = (code << 3) | (i + (positive ? 3 : 0));
        }
        if (text.size() < 2 || text.size() > 21)
            throw std::logic_error("source contains an invalid row length");
    }
};

int abelian_return_letter(const Word& a, const Word& b, int sign) {
    int selected = -1;
    for (int i = 0; i < 3; ++i) {
        const auto change = a.exponent[i] + sign * b.exponent[i];
        if (!change) continue;
        if (selected >= 0 || std::abs(change) != 1) return -1;
        selected = i;
    }
    return selected;
}

bool singleton_product(std::string_view a, std::string_view b, unsigned allowed, uint64_t& checked) {
    std::string stack;
    for (size_t i = 0; i < a.size(); ++i) {
        for (size_t j = 0; j < b.size(); ++j) {
            ++checked;
            stack.assign(a.substr(i));
            stack += a.substr(0, i);
            for (const auto c : b.substr(j)) push(stack, c);
            for (const auto c : b.substr(0, j)) push(stack, c);
            const auto result = cyclic_part(stack);
            if (result.size() != 1) continue;
            if (letter(result.front()) != allowed) throw std::logic_error("abelian filter mismatch");
            return true;
        }
    }
    return false;
}

std::string erase(std::string_view word, unsigned removed) {
    std::string stack;
    for (const auto c : word) {
        const auto i = letter(c);
        if (i == removed) continue;
        char mapped = 'x' + i - (i > removed);
        if (c < 'x') mapped = inv(mapped);
        push(stack, mapped);
    }
    auto output = canonical(stack);
    if (output.empty()) throw std::logic_error("empty row after a singleton return");
    return output;
}

void record_signed(std::set<Pair>& seen, const std::string& a, const std::string& b) {
    for (unsigned marking = 0; marking < 8; ++marking) {
        const auto apply = [marking](std::string change) {
            for (auto& c : change) {
                const auto p = letter(c);
                const char a = 'x' + (p ^ (marking & 1));
                const bool flip = (c < 'x') != bool(marking & (2U << p));
                c = flip ? inv(a) : a;
            }
            return canonical(change);
        };
        auto p = apply(a);
        auto q = apply(b);
        if (q < p) std::swap(p, q);
        seen.emplace(std::move(p), std::move(q));
    }
}

struct Cache {
    PairCode key = 0;
    unsigned singleton_letters = 0;
};

int audit(const char* source_name, const char* output_name) {
    std::ifstream input(source_name);
    std::ofstream output(output_name);
    if (!input || !output) throw std::runtime_error("cannot open catalogue or reentry output");
    std::array<Word, 3> rows;
    std::vector<Cache> tests(1U << row_cache_bits);
    std::set<Pair> returns;
    uint64_t states = 0, abelian_pair_occurrences = 0, uncached_pairs = 0, rotations = 0;
    uint64_t singleton_pair_occurrences = 0;
    while (input >> rows[0].text >> rows[1].text >> rows[2].text) {
        ++states;
        for (auto& row : rows) row.initialize();
        for (unsigned i = 0; i < 3; ++i) {
            for (unsigned j = i + 1; j < 3; ++j) {
                const Word& a = rows[i], &b = rows[j];
                const auto sum = abelian_return_letter(a, b, 1);
                const auto difference = abelian_return_letter(a, b, -1);
                if (sum < 0 && difference < 0) continue;
                ++abelian_pair_occurrences;
                const auto code = (PairCode(a.code) << 64) | b.code;
                auto hash = uint64_t(code) ^ uint64_t(code >> 64);
                hash = (hash ^ (hash >> 30)) * 0xbf58476d1ce4e5b9ULL;
                hash ^= hash >> 27;
                auto& cache = tests[hash & (tests.size() - 1)];
                if (cache.key != code) {
                    cache = {code, 0};
                    ++uncached_pairs;
                    if (sum >= 0 && singleton_product(a.text, b.text, unsigned(sum), rotations))
                        cache.singleton_letters |= 1U << sum;
                    if (difference >= 0 && singleton_product(a.text, inverse(b.text), unsigned(difference), rotations))
                        cache.singleton_letters |= 1U << difference;
                }
                if (cache.singleton_letters) ++singleton_pair_occurrences;
                for (unsigned k = 0; k < 3; ++k) {
                    if (!(cache.singleton_letters & (1U << k))) continue;
                    const auto other = erase(rows[3 - i - j].text, k);
                    record_signed(returns, erase(a.text, k), other);
                    record_signed(returns, erase(b.text, k), other);
                }
            }
        }
        if ((states & ((1U << 24) - 1)) == 0)
            std::cerr << "Screened " << states << " rows with " << returns.size() << " reentries so far.\n";
    }
    if (!states) throw std::runtime_error("empty catalogue");
    for (const auto& [first, second] : returns) output << first << '\t' << second << '\n';
    if (!output) throw std::runtime_error("could not export reentries");
    std::cout << "{\n  \"states\": " << states << ",\n  \"abelian_pair_occurrences\": " << abelian_pair_occurrences
              << ",\n  \"uncached_pairs\": " << uncached_pairs << ",\n  \"rotation_tests\": " << rotations
              << ",\n  \"singleton_pair_occurrences\": " << singleton_pair_occurrences
              << ",\n  \"distinct_signed_cyclic_reentries\": " << returns.size() << "\n}\n";
    return 0;
}

}

int main(int argc, char** argv) {
    try {
        if (argc != 3) throw std::runtime_error("usage: return-audit states.tsv returns.tsv");
        return audit(argv[1], argv[2]);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
