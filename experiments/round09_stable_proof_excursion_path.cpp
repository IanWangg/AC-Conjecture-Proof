// Recover one bounded signed-orbit excursion path back to a first-exit seed.
#define AC_ROUND06_SINGLETON_LIBRARY
#include "round06_stable_proof_all_singleton.cpp"

namespace {

Key key_of(CompactOrbits& cache, const Triple& words) {
    cache.limit();
    return compact_orbit(cache.word(encode(words[0])), cache.word(encode(words[1])),
                         cache.word(encode(words[2])));
}

struct Side {
    std::vector<Key> frontier;
    std::unordered_map<Key, Key, KeyHash> parents;
};

std::vector<Key> ancestors(const Side& side, Key point) {
    std::vector<Key> path{point};
    while (side.parents.at(point) != point) {
        point = side.parents.at(point);
        path.push_back(point);
    }
    return path;
}

int recover(int cap, size_t limit, const std::string& seed_file, const Triple& target) {
    std::ifstream seeds_file(seed_file);
    if (!seeds_file) throw std::runtime_error("missing seed catalogue");
    CompactOrbits cache;
    std::unordered_map<Key, Triple, KeyHash> seeds;
    Triple words;
    while (seeds_file >> words[0] >> words[1] >> words[2])
        seeds.try_emplace(key_of(cache, words), words);
    if (seeds.empty()) throw std::runtime_error("empty seed catalogue");
    const auto root = key_of(cache, target);
    if (energy(target) > size_t(cap)) throw std::runtime_error("target above cap");
    Side inward{{root}, {{root, root}}}, outward;
    for (const auto& [key, unused] : seeds) {
        outward.frontier.push_back(key);
        outward.parents.emplace(key, key);
    }
    std::sort(outward.frontier.begin(), outward.frontier.end());
    const auto emit = [&](Key meeting) {
        const auto start = ancestors(outward, meeting);
        write_tsv(std::cout, seeds.at(start.back()));
        for (auto at = start.rbegin() + 1; at != start.rend(); ++at)
            write_tsv(std::cout, rows_from(*at));
        const auto end = ancestors(inward, meeting);
        for (auto at = end.begin() + 1; at != end.end(); ++at)
            write_tsv(std::cout, rows_from(*at));
    };
    if (seeds.count(root)) {
        emit(root);
        return 0;
    }
    Worker worker;
    size_t expanded = 0;
    while (!inward.frontier.empty() && !outward.frontier.empty() && expanded < limit) {
        const auto reverse = inward.frontier.size() < outward.frontier.size();
        auto& active = reverse ? inward : outward;
        const auto& other = reverse ? outward : inward;
        std::vector<Key> next;
        for (const auto key : active.frontier) {
            if (expanded == limit) break;
            ++expanded;
            worker.scan(key, cap);
            std::vector<Key> fresh(worker.fresh.begin(), worker.fresh.end());
            worker.fresh.clear();
            std::sort(fresh.begin(), fresh.end());
            for (const auto neighbor : fresh) {
                if (!active.parents.try_emplace(neighbor, key).second) continue;
                if (other.parents.count(neighbor)) {
                    emit(neighbor);
                    std::cerr << "Frontiers meet after " << expanded << " expansions.\n";
                    return 0;
                }
                next.push_back(neighbor);
            }
        }
        active.frontier = std::move(next);
        std::cerr << "Expanded " << expanded << ", frontiers " << inward.frontier.size()
                  << " and " << outward.frontier.size() << '\n';
    }
    std::cerr << "No seed recovered within the " << limit << " expansion limit.\n";
    return 2;
}

}

int main(int argc, char** argv) {
    try {
        if (argc != 7) throw std::runtime_error("usage: excursion-path cap limit seeds.tsv row1 row2 row3");
        return recover(std::stoi(argv[1]), std::stoull(argv[2]), argv[3], {argv[4], argv[5], argv[6]});
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
