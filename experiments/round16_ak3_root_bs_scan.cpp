// Classify height-one words in Z *_{x^k=t} BS(n,n+1).
#define AC_ROUND07_WIDE_ORBITS_LIBRARY
#include "round07_ak3_wide_orbits.cpp"

#include <optional>
#include <variant>

namespace root_bs {
using orbit_search::Code;
using orbit_search::word;
using orbit_search::word_code;
using Power = int64_t;
using Record = std::array<Code, 4>;

Power plus(Power left, Power right) {
    Power result;
    if (__builtin_add_overflow(left, right, &result))
        throw std::overflow_error("exponent addition overflow");
    return result;
}

Power times(Power coefficient, Power exponent) {
    Power result;
    if (__builtin_mul_overflow(coefficient, exponent, &result))
        throw std::overflow_error("exponent multiplication overflow");
    return result;
}

struct Chart {
    int k, n;
    std::string x, y;
};

struct Step {
    int sign;
    Power base;
};

struct Hnn {
    Power first = 0;
    std::vector<Step> steps;

    Power& tail() { return steps.empty() ? first : steps.back().base; }
    void base(Power p) { tail() = plus(tail(), p); }

    void stable(int sign, int n) {
        if (!steps.empty() && sign == -steps.back().sign) {
            const int initial = sign < 0 ? n : n + 1;
            const int final = sign < 0 ? n + 1 : n;
            if (tail() % initial == 0) {
                const auto exponent = times(tail() / initial, final);
                steps.pop_back();
                base(exponent);
                return;
            }
        }
        steps.push_back({sign, 0});
    }

    void stable_power(Power p, int n) {
        const int sign = p < 0 ? -1 : 1;
        while (p != 0) {
            stable(sign, n);
            p -= sign;
        }
    }

    void append(const Hnn& rhs, int n) {
        base(rhs.first);
        for (const auto step : rhs.steps) {
            stable(step.sign, n);
            base(step.base);
        }
    }

    Power height() const {
        Power height = 0;
        for (const auto step : steps) height += step.sign;
        return height;
    }

    std::optional<Power> edge_power(int n) const {
        const auto p = height();
        if (uint64_t(std::abs(p)) != steps.size()) return {};
        auto normalized = *this;
        normalized.stable_power(-p, n);
        if (normalized.steps.empty() && normalized.first == 0) return p;
        return {};
    }
};

using Factor = std::variant<Power, Hnn>;

void combine(Factor& left, const Factor& right, int n) {
    if (auto* outer = std::get_if<Power>(&left))
        *outer = plus(*outer, std::get<Power>(right));
    else
        std::get<Hnn>(left).append(std::get<Hnn>(right), n);
}

bool identity(const Factor& factor) {
    if (const auto* outer = std::get_if<Power>(&factor)) return *outer == 0;
    const auto& inner = std::get<Hnn>(factor);
    return inner.steps.empty() && inner.first == 0;
}

std::optional<Factor> cross_edge(const Factor& factor, int k, int n) {
    if (const auto* outer = std::get_if<Power>(&factor)) {
        if (*outer % k == 0) {
            Hnn inner;
            inner.stable_power(*outer / k, n);
            return inner;
        }
    } else if (const auto edge = std::get<Hnn>(factor).edge_power(n)) {
        return times(*edge, k);
    }
    return {};
}

void reduce(std::vector<Factor>& factors, int k, int n) {
    for (size_t i = 0; i < factors.size();) {
        if (identity(factors[i])) {
            factors.erase(factors.begin() + i);
            if (i) --i;
        } else if (i + 1 < factors.size() && factors[i].index() == factors[i + 1].index()) {
            combine(factors[i], factors[i + 1], n);
            factors.erase(factors.begin() + i + 1);
        } else if (factors.size() == 1) {
            break;
        } else if (auto edge = cross_edge(factors[i], k, n)) {
            if (i > 0) {
                combine(factors[i - 1], *edge, n);
                factors.erase(factors.begin() + i);
                --i;
            } else {
                combine(*edge, factors[1], n);
                factors[1] = std::move(*edge);
                factors.erase(factors.begin());
            }
        } else {
            ++i;
        }
    }
}

std::string mark(const std::string& receiver, const Chart& chart) {
    const auto X = inverse(chart.x), Y = inverse(chart.y);
    std::string result;
    for (const auto c : receiver)
        result += c == 'x' ? chart.x : c == 'X' ? X : c == 'y' ? chart.y : Y;
    return result;
}

std::optional<Power> primitive_power(std::string marked, int k, int n) {
    const auto height = std::count(marked.begin(), marked.end(), 'x')
                      - std::count(marked.begin(), marked.end(), 'X');
    if (std::abs(height) != 1) throw std::runtime_error("receiver has wrong height");
    if (height < 0) marked = inverse(marked);
    std::vector<Factor> factors;
    for (const auto c : marked) {
        if (c == 'x' || c == 'X') factors.emplace_back(Power(c == 'x' ? 1 : -1));
        else factors.emplace_back(Hnn{Power(c == 'y' ? 1 : -1), {}});
    }
    reduce(factors, k, n);
    while (factors.size() > 1 && factors.front().index() == factors.back().index()) {
        std::rotate(factors.begin(), factors.begin() + 1, factors.end());
        reduce(factors, k, n);
    }
    if (factors.size() == 1 && std::holds_alternative<Power>(factors[0])) {
        if (std::get<Power>(factors[0]) != 1) throw std::logic_error("changed receiver height");
        return 0;
    }
    if (factors.size() != 2) return {};
    if (std::holds_alternative<Hnn>(factors.front())) std::swap(factors.front(), factors.back());
    auto inner = std::move(std::get<Hnn>(factors[1]));
    const auto h = inner.height();
    if (plus(std::get<Power>(factors[0]), times(k, h)) != 1)
        throw std::logic_error("changed receiver height");
    Hnn adjusted;
    adjusted.stable_power(-h, n);
    adjusted.append(inner, n);
    if (adjusted.steps.empty()) return adjusted.first;
    if (adjusted.steps.size() % 2) throw std::logic_error("odd stable length at height zero");
    const auto half = Power(adjusted.steps.size() / 2);
    for (const auto p : {half, -half}) {
        Hnn trial;
        trial.stable_power(-p, n);
        trial.append(adjusted, n);
        trial.stable_power(p, n);
        if (trial.steps.empty()) return trial.first;
    }
    return {};
}

using ChartMap = std::unordered_map<Code, Chart>;
using Occurrences = std::map<std::pair<int, int>, uint64_t>;

std::string inspect(const Record& seed, const ChartMap& charts, Occurrences& occurrences) {
    for (int slot = 0; slot < 2; ++slot) {
        const auto it = charts.find(seed[slot]);
        if (it == charts.end()) continue;
        const auto& chart = it->second;
        ++occurrences.at({chart.k, chart.n});
        const auto exponent = primitive_power(mark(word(seed[1-slot]), chart), chart.k, chart.n);
        if (!exponent) continue;
        return "{\"child\":[\"" + word(seed[0]) + "\",\"" + word(seed[1])
            + "\"],\"anchor\":[\"" + word(seed[2]) + "\",\"" + word(seed[3])
            + "\"],\"fixed_slot\":" + std::to_string(slot)
            + ",\"k\":" + std::to_string(chart.k) + ",\"n\":" + std::to_string(chart.n)
            + ",\"marking\":[\"" + chart.x + "\",\"" + chart.y
            + "\"],\"target_y_exponent\":" + std::to_string(*exponent) + "}";
    }
    return {};
}

int scan(const char* atlas, int count, char** files) {
    std::ifstream input(atlas);
    if (!input) throw std::runtime_error("cannot open root BS atlas");
    ChartMap charts;
    Occurrences occurrences;
    Chart chart;
    for (std::string relator; input >> relator >> chart.k >> chart.n >> chart.x >> chart.y;) {
        if (relator.size() > 31 || chart.k < 2 || chart.n < 1 ||
            !charts.emplace(word_code(relator), chart).second)
            throw std::runtime_error("invalid root BS chart");
        occurrences.try_emplace({chart.k, chart.n}, 0);
    }
    if (!input.eof() || charts.empty()) throw std::runtime_error("empty root BS atlas");
    std::vector<Record> batch(1 << 19);
    uint64_t scanned = 0;
    std::string hit;
    for (int file = 0; file < count && hit.empty(); ++file) {
        std::ifstream stream(files[file], std::ios::binary);
        if (!stream) throw std::runtime_error("cannot open boundary shard");
        while (hit.empty()) {
            stream.read(reinterpret_cast<char*>(batch.data()), batch.size() * sizeof(Record));
            const auto bytes = stream.gcount();
            if (bytes % sizeof(Record)) throw std::runtime_error("truncated boundary shard");
            for (size_t i = 0; i < size_t(bytes) / sizeof(Record) && hit.empty(); ++i) {
                ++scanned;
                hit = inspect(batch[i], charts, occurrences);
            }
            if (stream.eof()) break;
            if (!stream) throw std::runtime_error("boundary read error");
        }
        if ((file+1) % 16 == 0) std::cerr << "checked " << file+1 << " shards, " << scanned << " seeds\n";
    }
    std::cout << "{\n  \"atlas_marked_keys\":" << charts.size() << ",\n  \"seeds_checked\":" << scanned
              << ",\n  \"complete\":" << (hit.empty() ? "true" : "false") << ",\n  \"hit\":"
              << (hit.empty() ? "null" : hit) << ",\n  \"occurrences\":[";
    bool first = true;
    for (const auto& [type, number] : occurrences) {
        if (!first) std::cout << ',';
        first = false;
        std::cout << "\n    [" << type.first << ',' << type.second << ',' << number << ']';
    }
    std::cout << "\n  ]\n}\n";
    return 0;
}
} // namespace root_bs

#ifndef AC_ROUND16_ROOT_BS_LIBRARY
int main(int argc, char** argv) {
    try {
        if (argc < 3) throw std::runtime_error("usage: root-bs atlas.tsv shard.bin ...");
        return root_bs::scan(argv[1], argc-2, argv+2);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
#endif
