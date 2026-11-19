// Unbounded geodesic bridge rank filter using finitely many partial maps.
#define main round02_fiber_join_main
#include "round02_ak3_fiber_join.cpp"
#undef main

namespace bridge_maps {

bool nonmalnormal(const Graph& graph) {
    const int n = int(graph.out.size());
    std::vector<bool> seen(n*n);
    for (int a = 0; a < n; ++a) for (int b = a+1; b < n; ++b) {
        const int root = a*n+b;
        if (seen[root]) continue;
        seen[root] = true;
        std::vector<int> queue{root};
        size_t edges_times_two = 0;
        for (size_t i = 0; i < queue.size(); ++i) {
            const auto state = queue[i];
            for (int c = 0; c < 4; ++c) {
                int u = graph.out[state/n][c], v = graph.out[state%n][c];
                if (u < 0 || v < 0) continue;
                if (u > v) std::swap(u,v);
                ++edges_times_two;
                const int next = u*n+v;
                if (!seen[next]) { seen[next] = true; queue.push_back(next); }
            }
        }
        if (edges_times_two != 2*(queue.size()-1)) return true;
    }
    return false;
}

struct MapState {
    std::string word;
    std::vector<Vec> lifts;
};

std::vector<MapState> complete_maps(const Graph& graph) {
    const size_t n = graph.out.size();
    const char missing = char(255);
    if (n >= 255) throw std::runtime_error("partial-map state expects fewer than 255 vertices");
    struct Node { std::string map, word; };
    std::vector<Node> nodes;
    std::unordered_set<std::string> seen;
    auto add = [&](std::string map, std::string word) {
        if (size_t(std::count(map.begin(),map.end(),missing))+2 > n) return;
        const auto key = word.front() + (word.back() + map);
        if (seen.insert(key).second) nodes.push_back({std::move(map),std::move(word)});
    };
    auto extend = [&](const std::string& map, int c) {
        std::string next(n, missing);
        for (size_t i = 0; i < n; ++i) if (map[i] != missing) {
            const int at = graph.out[static_cast<unsigned char>(map[i])][c];
            if (at >= 0) next[i]=char(at);
        }
        return next;
    };
    std::string identity(n, missing);
    for (size_t i = 0; i < n; ++i) identity[i]=char(i);
    for (int c = 0; c < 4; ++c) add(extend(identity,c), std::string(1,"xXyY"[c]));
    for (size_t i = 0; i < nodes.size(); ++i) {
        const auto [map,word] = nodes[i];
        for (int c = 0; c < 4; ++c)
            if (c != (letter(word.back())^1)) add(extend(map,c), word+"xXyY"[c]);
    }
    std::vector<MapState> out;
    for (const auto& [map,word] : nodes) {
        MapState bridge{word,{}};
        for (size_t v = 0; v < n; ++v)
            if (map[v] != missing) bridge.lifts.push_back({int(v),static_cast<unsigned char>(map[v])});
        out.push_back(std::move(bridge));
    }
    return out;
}

struct MapStats {
    uint64_t placements = 0, rank_two_or_more = 0, intrinsic_exceptions = 0;
    size_t longest = 0;
    std::unordered_map<std::string,Lobe> cache;
};

void scan(const Graph& graph, const Words& lobe_words, const std::vector<MapState>& maps,
          MapStats& stats) {
    const size_t n = graph.out.size();
    const auto& a = stats.cache.try_emplace(lobe_words[0],graph,lobe_words[0]).first->second;
    const auto& b = stats.cache.try_emplace(lobe_words[1],graph,lobe_words[1]).first->second;
    const int intrinsic = a.cycles+b.cycles;
    if (intrinsic >= 2) ++stats.intrinsic_exceptions;
    std::vector<int> parents(a.component.size()+b.component.size(),-1), touched;
    auto root = [&](int id) {
        if (parents[id] < 0) { parents[id]=id; touched.push_back(id); }
        while (parents[id] != id) id=parents[id];
        return id;
    };
    for (const auto& map : maps) {
        const char first=map.word.front(), last=inverse(map.word.back());
        for (size_t i = 0; i < lobe_words[0].size(); ++i) {
            if (!leaves_lobe(first,lobe_words[0],i)) continue;
            for (size_t j = 0; j < lobe_words[1].size(); ++j) {
                if (!leaves_lobe(last,lobe_words[1],j)) continue;
                ++stats.placements;
                int rank = intrinsic;
                for (const auto& lift : map.lifts) {
                    const int x=root(a.component[i*n+lift[0]]);
                    const int y=root(int(a.component.size())+b.component[j*n+lift[1]]);
                    if (x==y) ++rank;
                    else parents[y]=x;
                }
                for (int id : touched) parents[id]=-1;
                touched.clear();
                if (rank>=2) ++stats.rank_two_or_more;
            }
        }
    }
}

int audit(const char* catalogue, const char* output) {
    const auto tuples=read_pairs(catalogue);
    std::ofstream out(output);
    if (!out) throw std::runtime_error("cannot write malnormality audit");
    uint64_t exceptions=0;
    for (const auto& words : tuples) {
        const auto graph=fold(words[0],words[1]);
        if (nonmalnormal(graph)) ++exceptions;
    }
    out << "{\n  \"displayed_cores\":" << tuples.size()
        << ",\n  \"nonmalnormal_cores\":" << exceptions << "\n}\n";
    return 0;
}

int compare_catalogues(const char* from, const char* to, const char* output) {
    const auto targets=read_pairs(to);
    std::ofstream out(output);
    if (!out) throw std::runtime_error("cannot write bridge-map result");
    out << "{\n  \"targets\": " << targets.size() << ",\n  \"sources\":[\n";
    bool first=true;
    for (const auto& words : read_pairs(from)) {
        const auto graph=fold(words[0],words[1]);
        const auto maps=complete_maps(graph);
        MapStats stats;
        for (const auto& bridge : maps) stats.longest=std::max(stats.longest,bridge.word.size());
        for (const auto& target : targets) scan(graph,target,maps,stats);
        if (!first) out << ",\n";
        first=false;
        out << "    {\"source\":";
        words_json(out,words);
        out << ",\"nonmalnormal\":" << (nonmalnormal(graph) ? "true":"false")
            << ",\"multilift_map_states\":" << maps.size() << ",\"longest_representative\":" << stats.longest
            << ",\"map_placements\":" << stats.placements
            << ",\"rank_at_least_two\":" << stats.rank_two_or_more
            << ",\"intrinsic_lobe_exceptions\":" << stats.intrinsic_exceptions << '}';
    }
    out << "\n  ]\n}\n";
    return 0;
}

}

int main(int argc,char** argv) {
    try {
        if (argc==4 && std::string(argv[1])=="audit") return bridge_maps::audit(argv[2],argv[3]);
        if (argc==5 && std::string(argv[1])=="scan") return bridge_maps::compare_catalogues(argv[2],argv[3],argv[4]);
        throw std::runtime_error("usage: bridge_maps audit catalogue.tsv output.json | scan from.tsv to.tsv output.json");
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
