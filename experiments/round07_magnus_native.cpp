// Exact rank-two characteristic-two Magnus distances with interned bit vectors.
#define AC_ROUND06_INSTRUCTION_DISTANCE_LIBRARY
#include "round06_free_instruction_distance.cpp"
#include <iomanip>
#include <sstream>

namespace magnus_native {
using free_distance::Id;
using free_distance::missing;

template <unsigned Degree>
class Elements {
    template <unsigned>
    friend class Elements;
    static constexpr std::size_t words = ((std::size_t(1) << (Degree + 1)) + 62) / 64;
    using Polynomial = std::array<uint64_t, words>;
    struct Hash {
        std::size_t operator()(const Polynomial& polynomial) const {
            uint64_t result = 0x517cc1b727220a95ULL;
            for (const auto word : polynomial) {
                result ^= word;
                result *= 0x9e3779b185ebca87ULL;
                result ^= result >> 29;
            }
            return result;
        }
    };
    struct Entry {
        Polynomial value;
        Id inverse = missing;
        std::array<Id, 4> conjugates{missing, missing, missing, missing};
    };
    struct CachedProduct {
        uint64_t key = std::numeric_limits<uint64_t>::max();
        Id value = missing;
    };
    static constexpr std::size_t product_cache_size = std::size_t(1) << 20;
    std::unordered_map<Polynomial, Id, Hash> index;
    std::vector<Entry> entries;
    std::vector<CachedProduct> product_cache{product_cache_size};
    std::array<Id, 4> generators{};
    Id one;

    static constexpr unsigned offset(unsigned degree) { return (1U << degree) - 1; }

    static uint64_t word(const Polynomial& value, unsigned slot) {
        return slot < words ? value[slot] : 0;
    }

    static uint64_t shifted_word(const Polynomial& value, unsigned bit) {
        const auto slot = bit / 64, shift = bit % 64;
        return shift ? (word(value, slot) >> shift) | (word(value, slot + 1) << (64 - shift))
                     : word(value, slot);
    }

    static constexpr unsigned block_words(unsigned degree) {
        return degree < 6 ? 1 : 1U << (degree - 6);
    }

    static uint64_t degree_word(const Polynomial& value, unsigned degree, unsigned chunk) {
        const unsigned width = 1U << degree;
        const auto shift = shifted_word(value, offset(degree) + 64 * chunk);
        return width >= 64 ? shift : shift & ((uint64_t(1) << width) - 1);
    }

    static void xor_word(Polynomial& result, uint64_t value, unsigned bit) {
        if (!value) return;
        const auto slot = bit / 64, shift = bit % 64;
        result[slot] ^= value << shift;
        if (shift && slot + 1 < words) result[slot + 1] ^= value >> (64 - shift);
    }

    static Polynomial multiply(const Polynomial& left, const Polynomial& right) {
        Polynomial result{};
        for (std::size_t i = 0; i < words; ++i) result[i] = left[i] ^ right[i];
        result[0] ^= 1;
        std::array<std::array<uint64_t, block_words(Degree - 1)>, Degree> blocks{};
        for (unsigned j = 1; j < Degree; ++j)
            for (unsigned chunk = 0; chunk < block_words(j); ++chunk)
                blocks[j][chunk] = degree_word(right, j, chunk);
        for (unsigned i = 1; i < Degree; ++i) {
            for (unsigned first = 0; first < block_words(i); ++first) {
                auto terms = degree_word(left, i, first);
                while (terms) {
                    const unsigned index = 64 * first + __builtin_ctzll(terms);
                    for (unsigned j = 1; j <= Degree - i; ++j) {
                        const unsigned at = offset(i + j) + (index << j);
                        for (unsigned second = 0; second < block_words(j); ++second)
                            xor_word(result, blocks[j][second], at + 64 * second);
                    }
                    terms &= terms - 1;
                }
            }
        }
        return result;
    }

    Id identify(const Polynomial& value) {
        if (entries.size() == missing) throw std::runtime_error("Magnus element ID space exhausted");
        auto [it, fresh] = index.try_emplace(value, Id(entries.size()));
        if (fresh) entries.push_back({value});
        return it->second;
    }

public:
    Elements() {
        Polynomial value{};
        value[0] = 1;
        one = identify(value);
        for (unsigned i = 0; i < 2; ++i) {
            value[0] = 1 | (uint64_t(1) << (1 + i));
            generators[2 * i] = identify(value);
            generators[2 * i + 1] = inverse(generators[2 * i]);
        }
    }

    Id intern(std::string source) {
        auto value = entries[one].value;
        for (char letter : source) {
            const auto place = free_distance::letters.find(letter);
            if (place == std::string_view::npos) throw std::runtime_error("unexpected Magnus letter");
            value = multiply(value, entries[generators[place]].value);
        }
        return identify(value);
    }

    std::size_t size() const { return entries.size(); }

    template <unsigned TargetDegree>
    Id project(Id id, Elements<TargetDegree>& target) const {
        static_assert(TargetDegree < Degree);
        constexpr unsigned width = (1U << (TargetDegree + 1)) - 1;
        typename Elements<TargetDegree>::Polynomial projected{};
        std::copy_n(entries[id].value.begin(), projected.size(), projected.begin());
        projected.back() &= (uint64_t(1) << (width % 64)) - 1;
        return target.identify(projected);
    }

    std::string describe(Id id) const {
        std::ostringstream result;
        result << std::hex << std::setfill('0');
        const auto& value = entries[id].value;
        for (auto it = value.rbegin(); it != value.rend(); ++it) result << std::setw(16) << *it;
        return result.str();
    }

    Id inverse(Id id) {
        if (entries[id].inverse != missing) return entries[id].inverse;
        // The first power of two exceeding Degree is a uniform unit exponent.
        auto power = entries[id].value;
        auto result = power;
        for (unsigned exponent = 2; exponent <= Degree; exponent <<= 1) {
            power = multiply(power, power);
            result = multiply(result, power);
        }
        const Id other = identify(result);
        entries[id].inverse = other;
        entries[other].inverse = id;
        return other;
    }

    Id product(Id left, Id right) {
        if (left == one) return right;
        if (right == one) return left;
        const uint64_t key = (uint64_t(left) << 32) | right;
        uint64_t hash = key ^ (key >> 23);
        hash *= 0x9e3779b185ebca87ULL;
        auto& slot = product_cache[(hash ^ (hash >> 31)) & (product_cache_size - 1)];
        if (slot.key == key) return slot.value;
        slot = {key, identify(multiply(entries[left].value, entries[right].value))};
        return slot.value;
    }

    Id conjugate(Id id, std::size_t letter) {
        if (entries[id].conjugates[letter] != missing) return entries[id].conjugates[letter];
        const auto moved = multiply(entries[generators[letter]].value, entries[id].value);
        const Id result = identify(multiply(moved, entries[generators[letter ^ 1]].value));
        entries[id].conjugates[letter] = result;
        entries[result].conjugates[letter ^ 1] = id;
        return result;
    }
};

template <unsigned Degree, std::size_t Rows>
void run(int limit, bool ordered, bool boundary_only) {
    const std::array<std::string, Rows> start{"xxxYYYY", "xyxYXY"}, target{"x", "y"};
    const auto result = free_distance::search<Rows, Elements<Degree>>(start, target, limit, ordered, boundary_only);
    std::cout << "{\"degree\":" << Degree << ",\"spare_rows\":" << Rows - 2
              << ",\"limit\":" << limit << ",\"ordered\":" << (ordered ? "true" : "false")
              << ",\"distance\":" << (result.distance < 0 ? "null" : std::to_string(result.distance))
              << ",\"radii\":[" << result.radii[0] << "," << result.radii[1]
              << "],\"visited\":[" << result.visited[0] << "," << result.visited[1]
              << "],\"distinct_elements\":" << result.words << ",\"midpoint_hex\":[";
    for (std::size_t i = 0; i < result.midpoint.size(); ++i) {
        if (i) std::cout << ',';
        std::cout << '"' << result.midpoint[i] << '"';
    }
    std::cout << ']';
    if (boundary_only) std::cout << ",\"final_boundary_candidates\":" << result.final_boundary_candidates;
    std::cout << "}\n";
}

template <unsigned Degree>
void dispatch(int padding, int limit, bool ordered, bool boundary_only) {
    switch (padding) {
    case 0: run<Degree, 2>(limit, ordered, boundary_only); break;
    case 1: run<Degree, 3>(limit, ordered, boundary_only); break;
    case 2: run<Degree, 4>(limit, ordered, boundary_only); break;
    case 3: run<Degree, 5>(limit, ordered, boundary_only); break;
    case 4: run<Degree, 6>(limit, ordered, boundary_only); break;
    default: throw std::runtime_error("spare row count outside 0–4");
    }
}
}

#ifndef AC_ROUND08_MAGNUS_NATIVE_LIBRARY
int main(int argc, char** argv) {
    try {
        if (argc < 4 || argc > 6)
            throw std::runtime_error("usage: magnus degree spare_rows limit [--ordered] [--boundary-only]");
        const int degree = std::stoi(argv[1]), padding = std::stoi(argv[2]), limit = std::stoi(argv[3]);
        if (limit < 0) throw std::runtime_error("negative search limit");
        bool ordered = false, boundary_only = false;
        for (int i = 4; i < argc; ++i) {
            const std::string_view option(argv[i]);
            if (option == "--ordered" && !ordered) ordered = true;
            else if (option == "--boundary-only" && !boundary_only) boundary_only = true;
            else throw std::runtime_error("unexpected search option");
        }
        switch (degree) {
        case 4: magnus_native::dispatch<4>(padding, limit, ordered, boundary_only); break;
        case 5: magnus_native::dispatch<5>(padding, limit, ordered, boundary_only); break;
        case 6: magnus_native::dispatch<6>(padding, limit, ordered, boundary_only); break;
        case 7: magnus_native::dispatch<7>(padding, limit, ordered, boundary_only); break;
        case 8: magnus_native::dispatch<8>(padding, limit, ordered, boundary_only); break;
        case 9: magnus_native::dispatch<9>(padding, limit, ordered, boundary_only); break;
        case 10: magnus_native::dispatch<10>(padding, limit, ordered, boundary_only); break;
        default: throw std::runtime_error("degree outside 4–10");
        }
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
#endif
