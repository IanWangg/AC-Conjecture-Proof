// Extend the rank-two signed-orbit basis lookup to longer projected pairs.
#define AC_ROUND06_ORBIT_INDEX_LIBRARY
#include "round06_ak3_orbit_index.cpp"

namespace {
struct ProjectionCatalogue {
    std::unordered_set<ak3_wide::Pair, ak3_wide::Hash> pairs;
    std::unordered_set<basis_index::Key> words;
    int cap = 0, minimum = 32;
    mutable std::unordered_map<basis_index::Key, orbit_index::Images> cache;

    orbit_index::Images images(basis_index::Key key) const {
        if (cache.size() > 65536) cache.clear();
        const auto [entry, inserted] = cache.try_emplace(key);
        if (inserted) entry->second = orbit_index::all_images(key);
        return entry->second;
    }

    explicit ProjectionCatalogue(const char* path) {
        std::ifstream source(path);
        if (!source) throw std::runtime_error("cannot open projected catalogue");
        std::string row;
        while (std::getline(source, row)) {
            const auto tab = row.find('\t');
            if (tab == std::string::npos || !tab || tab > 31 || row.size() - tab - 1 > 31
                || tab + 1 == row.size())
                throw std::runtime_error("projected coordinate exceeds packing width");
            const auto a = basis_index::word_key(row.substr(0, tab));
            const auto b = basis_index::word_key(row.substr(tab + 1));
            const auto ah = images(a), bh = images(b);
            const auto key = ak3_wide::least_image(ah, bh);
            if (key != ak3_wide::unordered_pair(a, b) || !pairs.insert(key).second)
                throw std::runtime_error("noncanonical or repeated projected orbit");
            words.insert(*std::min_element(ah.begin(), ah.end()));
            words.insert(*std::min_element(bh.begin(), bh.end()));
            cap = std::max(cap, int(row.size() - 1));
            minimum = std::min({minimum, int(tab), int(row.size() - tab - 1)});
        }
        if (pairs.empty() || source.bad()) throw std::runtime_error("empty or unreadable projected catalogue");
    }

    bool contains_word(const std::string& word) const {
        if (word.size() > 31) return false;
        const auto orbit = images(basis_index::word_key(word));
        return words.count(*std::min_element(orbit.begin(), orbit.end()));
    }

    bool contains_pair(const std::string& a, const std::string& b) const {
        if (a.size() > 31 || b.size() > 31) return false;
        return pairs.count(ak3_wide::least_image(images(basis_index::word_key(a)),
                                               images(basis_index::word_key(b))));
    }
};
}

int main(int argc, char** argv) {
    try {
        if (argc != 4) throw std::invalid_argument("usage: projection-index forward.tsv reverse.tsv result.json");
        return basis_index::run_scan(ProjectionCatalogue(argv[1]), argv[2], argv[3]);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
