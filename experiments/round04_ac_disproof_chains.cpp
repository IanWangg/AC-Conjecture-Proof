// Two-copy primitive exclusion for folded chains of four AK(3) lobes.
#define main round02_two_copies_main
#include "round02_ac_disproof_two_copies.cpp"
#undef main
#include "u_native_primitive.hpp"

namespace {
using Lobes = std::array<std::string,4>;

bool legal_outgoing(const std::string& lobe, char edge) {
    return edge != lobe.front() && edge != inverse(lobe.back());
}

Graph chain(const Lobes& lobes, const std::string& bridges) {
    Graph graph;
    int at = add_vertex(graph);
    for (size_t i=0; i<lobes.size(); ++i) {
        append_path(graph,at,lobes[i],true);
        if (i<bridges.size()) at=append_path(graph,at,std::string(1,bridges[i]),false);
    }
    return graph;
}

struct Summary {
    Counts joins;
    uint64_t own_dag=0, own_exact_absent=0, joins_exact_absent=0, exact_states=0;
    uint64_t positive=0, incomplete=0, certified_sources=0;
    std::map<int,uint64_t> source_vertices;
};

bool check(const Lobes& lobes, const std::string& bridges, int a, int b,
           const Graph& graph, Summary& summary, std::ostream& exceptions) {
    auto& count=summary.joins;
    const bool own=a==b;
    if (proves_primitive_absence(graph)) {
        if (own) ++summary.own_dag;
        else ++count.dag_exclusions;
        return true;
    }
    if (!own) ++count.unresolved;
    const auto result=u_native::decide(graph.out,0);
    summary.exact_states+=result.pair_states;
    if (result.status==u_native::Status::ABSENT) {
        if (own) ++summary.own_exact_absent;
        else ++summary.joins_exact_absent;
        return true;
    }
    if (result.status==u_native::Status::PRIMITIVE) ++summary.positive;
    else ++summary.incomplete;
    exceptions<<"{\"lobes\":[";
    for (size_t i=0; i<lobes.size(); ++i) {
        if (i) exceptions<<',';
        exceptions<<'\"'<<lobes[i]<<'\"';
    }
    exceptions<<"],\"bridges\":\""<<bridges<<"\",\"vertices\":["<<a<<','<<b
              <<"],\"status\":\""<<u_native::status_name(result.status)<<"\",\"graph\":";
    graph_json(exceptions,graph);
    if (result.status==u_native::Status::PRIMITIVE)
        exceptions<<",\"primitive\":\""<<result.witness.cyclic_word
                  <<"\",\"based_word\":\""<<result.witness.based_word
                  <<"\",\"vertex\":"<<result.witness.vertex;
    exceptions<<"}\n";
    return false;
}

void check_chain(const Lobes& lobes, const std::string& bridges, Summary& summary,
                 std::ostream& exceptions) {
    const auto core=chain(lobes,bridges);
    if (rank(core)!=4) throw std::runtime_error("expected a rank-four folded chain");
    const auto n=static_cast<int>(core.out.size());
    ++summary.source_vertices[n];
    ++summary.joins.sources;
    bool all=check(lobes,bridges,0,0,core,summary,exceptions);
    for (int a=0; a<n; ++a) for (int b=a+1; b<n; ++b) {
        const auto graph=join(core,a,b);
        const int joined_rank=rank(graph);
        if (joined_rank<4 || joined_rank>8) throw std::runtime_error("unexpected join rank");
        ++summary.joins.tests;
        ++summary.joins.ranks[joined_rank];
        if (!check(lobes,bridges,a,b,graph,summary,exceptions)) all=false;
    }
    summary.certified_sources+=all;
}
}

int main(int argc, char** argv) {
    try {
        if (argc!=2) throw std::runtime_error("usage: four-lobe-chains unresolved.jsonl");
        std::ofstream exceptions(argv[1]);
        if (!exceptions) throw std::runtime_error("cannot open exceptions output");
        const std::string alphabet="xXyY";
        const auto powers=rotations("xxxYYYY");
        const auto braids=rotations("xyxYXY");
        auto inner=powers;
        inner.insert(inner.end(),braids.begin(),braids.end());
        for (std::size_t i=0, n=inner.size(); i<n; ++i) inner.push_back(inv(inner[i]));
        Summary summary;
        for (const auto& p:powers) for (const auto& b:braids)
            for (const auto& r:inner) for (const auto& s:inner)
                for (char c:alphabet) for (char d:alphabet) for (char e:alphabet) {
                    if (!legal_outgoing(p,c) || !legal_outgoing(r,inverse(c))
                        || !legal_outgoing(r,d) || inverse(c)==d
                        || !legal_outgoing(s,inverse(d)) || !legal_outgoing(s,e)
                        || inverse(d)==e || !legal_outgoing(b,inverse(e))) continue;
                    check_chain({p,r,s,b},{c,d,e},summary,exceptions);
                }
        std::cout<<"{\n  \"native_joins\": ";
        write_counts(std::cout,summary.joins);
        std::cout<<",\n  \"certified_sources\": "<<summary.certified_sources
                 <<",\n  \"own_DAG_exclusions\": "<<summary.own_dag
                 <<",\n  \"own_exact_exclusions\": "<<summary.own_exact_absent
                 <<",\n  \"join_exact_exclusions\": "<<summary.joins_exact_absent
                 <<",\n  \"exact_map_states\": "<<summary.exact_states
                 <<",\n  \"primitive_positive\": "<<summary.positive
                 <<",\n  \"incomplete\": "<<summary.incomplete
                 <<",\n  \"source_vertex_counts\": {";
        bool first=true;
        for (const auto& [n,count]:summary.source_vertices) {
            if (!first) std::cout<<", ";
            first=false;
            std::cout<<'\"'<<n<<"\": "<<count;
        }
        std::cout<<"}\n}\n";
        if (!exceptions || !std::cout) throw std::runtime_error("write failed");
    } catch (const std::exception& e) {
        std::cerr<<e.what()<<'\n';
        return 1;
    }
}
