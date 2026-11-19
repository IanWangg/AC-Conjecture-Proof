// Exact reverse-basis lookup against a forward catalogue of signed ambient orbits.
#define AC_ROUND04_AK3_BASIS_INDEX_LIBRARY
#include "round04_ak3_basis_index.cpp"
#include "round06_ak3_wide_pair.hpp"

#include <filesystem>

namespace orbit_index {
using basis_index::Key;
using Images = ak3_wide::Orbit;

unsigned word_length(Key word) {
    return (63 - __builtin_clzll(word)) / 2;
}

constexpr unsigned marking[8][4]{
    {0, 1, 2, 3}, {1, 0, 2, 3}, {0, 1, 3, 2}, {1, 0, 3, 2},
    {2, 3, 0, 1}, {3, 2, 0, 1}, {2, 3, 1, 0}, {3, 2, 1, 0},
};

Images all_images(Key word) {
    const unsigned length = word_length(word);
    const unsigned high_shift = 2 * length - 2;
    const Key sentinel = Key(1) << (2 * length);
    const Key mask = sentinel - 1;
    Images images{};
    for (unsigned symmetry = 0; symmetry < images.size(); ++symmetry) {
        Key forward = 0, backward = 0;
        for (unsigned at = 0; at < length; ++at) {
            const unsigned code = (word >> (2 * at)) & 3;
            const Key image = marking[symmetry][code];
            forward |= image << (2 * at);
            backward = (backward << 2) | (image ^ 1);
        }
        Key least = mask;
        for (unsigned at = 0; at < length; ++at) {
            least = std::min({least, forward, backward});
            forward = ((forward << 2) & mask) | (forward >> high_shift);
            backward = ((backward << 2) & mask) | (backward >> high_shift);
        }
        images[symmetry] = sentinel | least;
    }
    return images;
}

struct Catalogue {
    std::unordered_set<ak3_wide::Pair, ak3_wide::Hash> pairs;
    std::unordered_set<Key> words;
    int cap = 0, minimum = 32;
    mutable std::unordered_map<Key, Images> cache;

    Images images(Key code) const {
        if (cache.size() > 65536) cache.clear();
        const auto [position, added] = cache.try_emplace(code);
        if (added) position->second = all_images(code);
        return position->second;
    }

    Key word_orbit(Key code) const {
        const auto orbit = images(code);
        return *std::min_element(orbit.begin(), orbit.end());
    }

    explicit Catalogue(const char* path) {
        std::ifstream input(path);
        if (!input) throw std::runtime_error("cannot open orbit catalogue");
        const auto expected = std::filesystem::file_size(path) / 29;
        pairs.reserve(expected);
        words.reserve(expected);
        std::string row;
        while (std::getline(input, row)) {
            auto separator = row.find('\t');
            if (separator == std::string::npos || !separator || separator + 1 == row.size() || row.size() > 33)
                throw std::runtime_error("expected two nonempty coordinates of total length at most 32");
            const std::string a = row.substr(0, separator), b = row.substr(separator + 1);
            const Key first = basis_index::word_key(a), second = basis_index::word_key(b);
            const auto first_images = images(first), second_images = images(second);
            const auto pair = ak3_wide::unordered_pair(first, second);
            if (pair != ak3_wide::least_image(first_images, second_images) || !pairs.insert(pair).second)
                throw std::runtime_error("noncanonical or repeated orbit row");
            words.insert(*std::min_element(first_images.begin(), first_images.end()));
            words.insert(*std::min_element(second_images.begin(), second_images.end()));
            cap = std::max(cap, int(a.size() + b.size()));
            minimum = std::min({minimum, int(a.size()), int(b.size())});
        }
        if (input.bad() || pairs.empty()) throw std::runtime_error("empty or unreadable orbit catalogue");
    }

    bool contains_word(const std::string& word) const {
        if (word.size() > 31) return false;
        return words.count(word_orbit(basis_index::word_key(word)));
    }

    bool contains_pair(const std::string& a, const std::string& b) const {
        return pairs.count(ak3_wide::least_image(images(basis_index::word_key(a)),
                                                images(basis_index::word_key(b))));
    }
};
}

int main(int argc, char** argv) {
    try {
        if (argc != 4) throw std::runtime_error("usage: orbit-index forward.orbit.tsv reverse.tsv result.json");
        return basis_index::run_scan(orbit_index::Catalogue(argv[1]), argv[2], argv[3]);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
