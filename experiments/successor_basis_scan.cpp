// X actual-successor scan; Farey/scanner implementation credited to V.
// Higher Nielsen bases of the original AK subgroup, then all rotations.
// Raw basis words are retained until the final independent-conjugacy phase.
#define Q_ROTATION_SUBGROUPS_LIBRARY
#if __has_include("rotation_subgroups.cpp")
#include "rotation_subgroups.cpp"
#else
#include "../research_q/rotation_subgroups.cpp"
#endif
#include <map>
#include <set>
#include <unordered_map>

std::string cyclic_word(std::string w){
    w=reduce(w);size_t a=0,b=w.size();
    while(b>a+1&&w[a]==inverse(w[b-1])){++a;--b;}
    return w.substr(a,b-a);
}
std::string class_word(const std::string&w){
    auto c=cyclic_word(w);std::string answer;
    for(const auto&v:{c,inv(c)})for(size_t i=0;i<v.size();++i){auto r=v.substr(i)+v.substr(0,i);if(answer.empty()||r<answer)answer=r;}
    return answer;
}
std::string pair_key(std::string a,std::string b){if(a>b)a.swap(b);return a+":"+b;}
int theta_length(int a,int b,int n){return std::abs(a+b)+5*std::abs(a)+6*std::abs(b);}
struct Basis{std::string u,v,program;int s0=1,s1=1,a=1,b=0,c=0,d=1;};
struct ReverseRecord{std::string u,v;uint64_t row=0;int corpus=0,base=0;};

// Q's exact vertex-identification fold, with the graph-size safety guard
// relaxed from120 to255. The shared full adjacency key remains injective.
Graph extended_fold(const std::string&u,const std::string&v){
    std::vector<std::array<int,3>> arcs;int n=1;
    for(const auto&w:{u,v}){int at=0;for(size_t i=0;i<w.size();++i){int next=i+1==w.size()?0:n++;int c=letter(w[i]);arcs.push_back({at,c,next});arcs.push_back({next,c^1,at});at=next;}}
    if(n>255)throw std::runtime_error("graph exceeds byte-key capacity");
    std::vector<int>parent(n);std::vector<Row> out(n,Row{-1,-1,-1,-1});for(int i=0;i<n;++i)parent[i]=i;
    auto root=[&](int at){while(parent[at]!=at){parent[at]=parent[parent[at]];at=parent[at];}return at;};
    auto unite=[&](int first,int second){std::vector<std::pair<int,int>>queue{{first,second}};
        for(size_t k=0;k<queue.size();++k){int a=root(queue[k].first),b=root(queue[k].second);if(a==b)continue;if(a>b)std::swap(a,b);parent[b]=a;
            for(int c=0;c<4;++c){int x=out[a][c],y=out[b][c];if(x<0)out[a][c]=y;else if(y>=0)queue.emplace_back(x,y);}}};
    for(const auto&e:arcs){int a=root(e[0]),b=root(e[2]);if(out[a][e[1]]<0)out[a][e[1]]=b;else unite(out[a][e[1]],b);}
    std::vector<int>names(n,-1),queue{root(0)};names[queue[0]]=0;Graph result;
    for(size_t k=0;k<queue.size();++k){Row row{-1,-1,-1,-1};int a=root(queue[k]);
        for(int c=0;c<4;++c)if(out[a][c]>=0){int b=root(out[a][c]);if(names[b]<0){names[b]=int(queue.size());queue.push_back(b);}row[c]=names[b];}result.out.push_back(row);}
    int oriented=0;for(size_t a=0;a<result.out.size();++a){int degree=0;for(int c=0;c<4;++c){int b=result.out[a][c];if(b>=0){++oriented;++degree;if(result.out[b][c^1]!=int(a))throw std::runtime_error("inverse arc inconsistency");}}if(degree<2)throw std::runtime_error("noncore source");}
    if(oriented/2-int(result.out.size())+1!=2)throw std::runtime_error("rank not two");return result;
}

int main(int argc,char**argv){
  try{
    if(argc<5)throw std::runtime_error("usage: one_phase_bases cap sources.jsonl candidates.jsonl results.json [max_graphs [n [reverse.tsv ...]]]");
    int n=argc>6?std::stoi(argv[6]):3;
    int cap=std::stoi(argv[1]);if(n<2||cap<2*n+7||cap>250)throw std::runtime_error("require n>=2,2n+7<=cap<=250 for byte graph keys");
    uint64_t graph_limit=argc>5?std::stoull(argv[5]):UINT64_MAX;
    std::ofstream sources(argv[2]),candidates(argv[3]);
    if(!sources||!candidates)throw std::runtime_error("cannot open output");
    std::unordered_map<std::string,ReverseRecord> reverse_keys;uint64_t reverse_rows=0;
    for(int arg=7;arg<argc;++arg){
      std::ifstream file(argv[arg]);if(!file)throw std::runtime_error("reverse file missing");std::string line;uint64_t row=0;
      while(std::getline(file,line)){auto tab=line.find('\t');if(tab==std::string::npos)throw std::runtime_error("bad reverse TSV");auto a=line.substr(0,tab),b=line.substr(tab+1);auto core=unbased_key(extended_fold(a,b));reverse_keys.emplace(core.first,ReverseRecord{a,b,row,arg-7,core.second.original_base});++row;++reverse_rows;}
    }
    std::vector<Basis> pending;std::string p="yXYXyx",braid="yyyyXXX";
    for(int s0:{1,-1})for(int s1:{1,-1})pending.push_back({s0>0?p:inv(p),s1>0?braid:inv(braid),"",s0,s1,s0,0,0,s1});
    std::set<std::string> source_seen;std::unordered_set<std::string> graph_seen;
    graph_seen.reserve(1000000);
    uint64_t basis_nodes=0,source_count=0,rotation_pairs=0,graphs=0,dag=0,exceptions=0;
    int maximum_graph_vertices=0,maximum_raw_basis_sum=0;
    bool complete=true,matched=false;auto started=std::chrono::steady_clock::now();
    std::map<int,uint64_t> source_histogram;
    while(!pending.empty()){
      Basis basis=std::move(pending.back());pending.pop_back();
      std::string cu=cyclic_word(basis.u),cv=cyclic_word(basis.v);
      int energy=cu.size()+cv.size();
      if(int(cu.size())!=theta_length(basis.a,basis.b,n)||int(cv.size())!=theta_length(basis.c,basis.d,n))throw std::runtime_error("theta length formula mismatch");
      if(energy>cap)continue;
      ++basis_nodes;maximum_raw_basis_sum=std::max<int>(maximum_raw_basis_sum,basis.u.size()+basis.v.size());
      // Children are generated even when this final conjugacy family was seen.
      auto uv=reduce(basis.u+basis.v);
      pending.push_back({basis.u,uv,basis.program+"L",basis.s0,basis.s1,basis.a,basis.b,basis.a+basis.c,basis.b+basis.d});
      pending.push_back({uv,basis.v,basis.program+"R",basis.s0,basis.s1,basis.a+basis.c,basis.b+basis.d,basis.c,basis.d});
      auto first=class_word(cu),second=class_word(cv);
      if(!source_seen.insert(pair_key(first,second)).second)continue;
      uint64_t index=source_count++;++source_histogram[energy];
      sources<<"{\"source_index\":"<<index<<",\"signs\":["<<basis.s0<<","<<basis.s1<<"],\"basis_program\":\""<<basis.program<<"\",\"matrix_columns\":[["<<basis.a<<","<<basis.b<<"],["<<basis.c<<","<<basis.d<<"]],\"raw_basis\":[\""<<basis.u<<"\",\""<<basis.v<<"\"],\"cyclic_basis\":[\""<<cu<<"\",\""<<cv<<"\"],\"cyclic_energy\":"<<energy<<"}\n";
      auto uu=rotations(cu),vv=rotations(cv);
      for(const auto&u:uu){for(const auto&v:vv){
        ++rotation_pairs;auto unbased=unbased_key(extended_fold(u,v));
        if(!graph_seen.insert(unbased.first).second)continue;
        ++graphs;maximum_graph_vertices=std::max<int>(maximum_graph_vertices,unbased.second.out.size());
        auto match=reverse_keys.find(unbased.first);
        if(match!=reverse_keys.end()){
          const auto &back=match->second;std::ofstream hit(std::string(argv[4])+".match.json");
          hit<<"{\"status\":\"MATCH\",\"ordinary_AC_goal_solved\":false,\"forward_source_index\":"<<index<<",\"forward_source_pair\":[\""<<cu<<"\",\""<<cv<<"\"],\"forward_rotated_pair\":[\""<<u<<"\",\""<<v<<"\"],\"forward_original_base\":"<<unbased.second.original_base<<",\"initial_domain_signs\":["<<basis.s0<<","<<basis.s1<<"],\"initial_Nielsen_program\":\""<<basis.program<<"\",\"raw_basis_before_rotations\":[\""<<basis.u<<"\",\""<<basis.v<<"\"],\"reverse_corpus\":"<<back.corpus<<",\"reverse_index\":"<<back.row<<",\"reverse_pair\":[\""<<back.u<<"\",\""<<back.v<<"\"],\"reverse_original_base\":"<<back.base<<",\"canonical_unbased_graph\":";graph_json(hit,unbased.second);hit<<"}\n";
          matched=true;complete=false;break;
        }
        if(proves_primitive_absence(unbased.second)){++dag;}
        else{
          ++exceptions;
          candidates<<"{\"source_index\":"<<index<<",\"signs\":["<<basis.s0<<","<<basis.s1<<"],\"basis_program\":\""<<basis.program<<"\",\"raw_basis\":[\""<<basis.u<<"\",\""<<basis.v<<"\"],\"source\":[\""<<cu<<"\",\""<<cv<<"\"],\"pair\":[\""<<u<<"\",\""<<v<<"\"],\"original_base\":"<<unbased.second.original_base<<",\"graph\":";
          graph_json(candidates,unbased.second);candidates<<"}\n";
        }
        if(graphs>=graph_limit){complete=false;break;}
      }if(!complete)break;}
      if(!complete)break;
      if(source_count%100==0)std::cout<<"sources "<<source_count<<" graphs "<<graphs<<" exceptions "<<exceptions<<std::endl;
    }
    sources.close();candidates.close();
    auto seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count();
    std::ofstream result(argv[4]);result<<"{\n\"status\":\""<<(matched?"MATCH":complete?"COMPLETE":"INCOMPLETE")<<"\",\"ordinary_AC_goal_solved\":false,\n\"AK_parameter\":"<<n<<",\"prelude_cyclic_energy_cap\":"<<cap<<",\"signed_Farey_nodes\":"<<basis_nodes<<",\"distinct_final_cyclic_pair_families\":"<<source_count<<",\"rotation_pairs\":"<<rotation_pairs<<",\"distinct_unbased_core_graphs\":"<<graphs<<",\"direct_DAG_absence_graphs\":"<<dag<<",\"exception_graphs\":"<<exceptions<<",\"reverse_input_rows\":"<<reverse_rows<<",\"distinct_reverse_keys\":"<<reverse_keys.size()<<",\"reverse_subgroup_match\":"<<(matched?"true":"false")<<",\"maximum_graph_vertices\":"<<maximum_graph_vertices<<",\"maximum_raw_Nielsen_basis_sum\":"<<maximum_raw_basis_sum<<",\"seconds\":"<<seconds<<",\"source_energy_histogram\":{";
    bool first=true;for(const auto&entry:source_histogram){if(!first)result<<",";first=false;result<<"\""<<entry.first<<"\":"<<entry.second;}result<<"}}\n";
    std::cout<<"finished cap "<<cap<<" sources "<<source_count<<" rotations "<<rotation_pairs<<" graphs "<<graphs<<" exceptions "<<exceptions<<" seconds "<<seconds<<std::endl;
    return 0;
  }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}
}
