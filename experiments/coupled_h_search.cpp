// Heuristic coupled H-level search; Q folding, U exact primitive detection.
#define Q_ROTATION_SUBGROUPS_LIBRARY
#if __has_include("rotation_subgroups.cpp")
#include "rotation_subgroups.cpp"
#include "u_native_primitive.hpp"
#else
#include "../research_q/rotation_subgroups.cpp"
#include "../research_u/u_native_primitive.hpp"
#endif
#include <cmath>
#include <map>
#include <queue>
#include <random>
#include <set>
#include <unordered_map>
using PairH=std::array<std::string,2>;
std::string core_h(std::string w){w=reduce(w);size_t a=0,b=w.size();while(b>a+1&&w[a]==inverse(w[b-1])){++a;--b;}return w.substr(a,b-a);}
std::string canonical_h(std::string w){auto v=core_h(w);auto rr=rotations(v),ss=rotations(inv(v));rr.insert(rr.end(),ss.begin(),ss.end());return *std::min_element(rr.begin(),rr.end());}
std::string tuple_key_h(PairH p){p[0]=canonical_h(p[0]);p[1]=canonical_h(p[1]);if(p[0]>p[1])p[0].swap(p[1]);return p[0]+":"+p[1];}
unsigned energy_h(const PairH&p){return core_h(p[0]).size()+core_h(p[1]).size();}
void nielsen_h(PairH&p,unsigned code){unsigned i=code&1,j=1-i;auto d=(code&4)?inv(p[j]):p[j];p[i]=reduce((code&2)?d+p[i]:p[i]+d);}
using EdgeH=std::array<int,3>;
EdgeH edge_h(int a,int c,int b){return std::min(EdgeH{a,c,b},EdgeH{b,c^1,a});}
PairH tree_basis_h(const Graph&g){
 std::vector<std::string> paths(g.out.size());std::vector<bool> seen(g.out.size());seen[0]=true;std::queue<int> todo;todo.push(0);std::set<EdgeH> tree,edges;
 while(!todo.empty()){int a=todo.front();todo.pop();for(int c=0;c<4;++c){int b=g.out[a][c];if(b>=0&&!seen[b]){seen[b]=true;paths[b]=paths[a]+"xXyY"[c];tree.insert(edge_h(a,c,b));todo.push(b);}}}
 for(size_t a=0;a<g.out.size();++a)for(int c=0;c<4;++c)if(g.out[a][c]>=0)edges.insert(edge_h(a,c,g.out[a][c]));
 PairH basis;unsigned at=0;for(const auto&e:edges)if(!tree.count(e)){if(at>=2)throw std::runtime_error("rank exceeds two");basis[at++]=reduce(paths[e[0]]+"xXyY"[e[1]]+inv(paths[e[2]]));}
 if(at!=2)throw std::runtime_error("rank below two");return basis;
}
void pair_json_h(std::ostream&o,const PairH&p){o<<"[\""<<p[0]<<"\",\""<<p[1]<<"\"]";}
void graph_json_h(std::ostream&o,const Graph&g){o<<'[';bool first=true;for(const auto&r:g.out)for(int x:r){if(!first)o<<',';first=false;o<<x;}o<<']';}
struct NodeH{PairH words,basis;uint32_t parent=0;std::vector<unsigned> prelude;unsigned source_energy=0;double score=0;};
struct ReverseH{PairH words;unsigned corpus=0,index=0;int base=0;};

int main(int argc,char**argv){try{
 if(argc!=10&&argc!=12)throw std::runtime_error("usage: coupled_h_search C22.tsv reverse1.tsv|- reverse2.tsv|- seed attempts maxnodes cap maxprelude prefix [first second]");
 std::unordered_set<std::string> known_pairs;std::ifstream source(argv[1]);if(!source)throw std::runtime_error("missing C22 input");std::string line;
 while(std::getline(source,line)){auto k=line.find('\t');if(k==std::string::npos)throw std::runtime_error("bad C22 row");known_pairs.insert(tuple_key_h({line.substr(0,k),line.substr(k+1)}));}
 std::unordered_map<std::string,ReverseH> reverse;
 for(unsigned corpus=0;corpus<2;++corpus){if(std::string(argv[2+corpus])=="-")continue;std::ifstream input(argv[2+corpus]);if(!input)throw std::runtime_error("missing reverse pairs");unsigned index=0;
  while(std::getline(input,line)){auto k=line.find('\t');if(k==std::string::npos)throw std::runtime_error("bad reverse row");PairH p{line.substr(0,k),line.substr(k+1)};auto keyed=unbased_key(fold(p[0],p[1]));reverse.emplace(keyed.first,ReverseH{p,corpus,index++,keyed.second.original_base});}}
 uint64_t seed=std::stoull(argv[4]),attempts=std::stoull(argv[5]),maxnodes=std::stoull(argv[6]);unsigned cap=std::stoul(argv[7]),prelude_max=std::stoul(argv[8]);std::string prefix=argv[9];
 if(cap>120||!prelude_max)throw std::runtime_error("cap<=120 and positive prelude required");
 std::mt19937_64 rng(seed);std::uniform_real_distribution<double> uniform(0,1);
 PairH initial=argc==12?PairH{argv[10],argv[11]}:PairH{"xxxYYYY","xyxYXY"};
 for(const auto&w:initial)if(w.empty()||core_h(w)!=w)throw std::runtime_error("start must be cyclically reduced");
 const auto pc=canonical_h("xxxYYYY"),bc=canonical_h("xyxYXY"),mc=canonical_h("xY");
 auto score=[&](const PairH&p,unsigned vertices){unsigned frozen=0;for(const auto&w:p){auto c=canonical_h(w);frozen+=c==pc||c==bc||c==mc;}return double(vertices)+.025*energy_h(p)+8*frozen+(known_pairs.count(tuple_key_h(p))?6:0);};
 auto g0=fold(initial[0],initial[1]);NodeH root;root.words=initial;root.basis=tree_basis_h(g0);root.score=score(initial,g0.out.size());
 std::vector<NodeH> nodes{root};std::unordered_map<std::string,uint32_t> accepted_keys{{unbased_key(g0).first,0}};std::unordered_map<std::string,int> tested;
 std::vector<uint32_t> elite{0};uint32_t current=0,best=0;std::string hit_type;
 uint64_t tried=0,discarded=0,admitted=0,dag_absent=0,catalogue_absent=0,native_absent=0,incomplete=0,native_states=0;
 unsigned minvertices=g0.out.size(),maxenergy=energy_h(initial);std::ofstream unresolved(prefix+".incomplete.jsonl"),native_log(prefix+".native.jsonl");auto started=std::chrono::steady_clock::now();
 for(tried=1;tried<=attempts;++tried){
  if(tried%250==0)current=uniform(rng)<.75?elite[rng()%elite.size()]:rng()%nodes.size();
  const auto old=nodes[current];PairH candidate=old.basis;std::vector<unsigned> prelude;bool too_large=false;
  unsigned count=1+rng()%prelude_max;
  for(unsigned k=0;k<count;++k){auto code=rng()%8;nielsen_h(candidate,code);prelude.push_back(code);if(candidate[0].size()+candidate[1].size()>4*cap){too_large=true;break;}}
  if(too_large||candidate[0].empty()||candidate[1].empty()){++discarded;continue;}
  unsigned source_energy=energy_h(candidate);if(source_energy>cap||(source_energy<23&&uniform(rng)<.9)){++discarded;continue;}
  for(auto&w:candidate){w=core_h(w);if(rng()%2)w=inv(w);auto at=rng()%w.size();w=w.substr(at)+w.substr(0,at);}
  auto g=fold(candidate[0],candidate[1]);auto keyed=unbased_key(g);++admitted;
  auto reverse_hit=reverse.find(keyed.first);bool match=reverse_hit!=reverse.end(),positive=false;u_native::Result decision;
  if(!match&&!tested.count(keyed.first)){
   if(known_pairs.count(tuple_key_h(candidate))){tested[keyed.first]=0;++catalogue_absent;}
   else if(proves_primitive_absence(g)){tested[keyed.first]=0;++dag_absent;}
   else{decision=u_native::decide(g.out,100000,1000000,false);native_states+=decision.pair_states;
    native_log<<"{\"parent\":"<<current<<",\"pair\":";pair_json_h(native_log,candidate);
    native_log<<",\"status\":\""<<(decision.status==u_native::Status::PRIMITIVE?"PRIMITIVE":decision.status==u_native::Status::ABSENT?"ABSENT":"INCOMPLETE")<<"\",\"pair_states\":"<<decision.pair_states<<",\"prelude\":[";
    for(size_t k=0;k<prelude.size();++k){if(k)native_log<<',';native_log<<prelude[k];}native_log<<"]}\n";
    if(decision.status==u_native::Status::PRIMITIVE)positive=true;
    else if(decision.status==u_native::Status::ABSENT){tested[keyed.first]=0;++native_absent;}
    else{tested[keyed.first]=1;++incomplete;unresolved<<"{\"parent\":"<<current<<",\"pair\":";pair_json_h(unresolved,candidate);unresolved<<"}\n";}}
  }
  double value=score(candidate,g.out.size()),temperature=2.0+6.0*double((tried/1000)%8)/7;
  if(!match&&!positive&&value>old.score&&uniform(rng)>=std::exp(-(value-old.score)/temperature))continue;
  auto prior=accepted_keys.find(keyed.first);if(prior!=accepted_keys.end()&&!match&&!positive){current=prior->second;continue;}
  NodeH next;next.words=candidate;next.basis=tree_basis_h(g);next.parent=current;next.prelude=prelude;next.source_energy=source_energy;next.score=value;
  current=nodes.size();nodes.push_back(next);accepted_keys[keyed.first]=current;minvertices=std::min<unsigned>(minvertices,g.out.size());maxenergy=std::max(maxenergy,energy_h(candidate));
  if(value<nodes[best].score)best=current;elite.push_back(current);if(elite.size()>256){std::sort(elite.begin(),elite.end(),[&](auto a,auto b){return nodes[a].score<nodes[b].score;});elite.resize(128);}
  if(match||positive){best=current;hit_type=match?"MATCH":"PRIMITIVE";std::ofstream hit(prefix+".hit.json");
   if(match){const auto&r=reverse_hit->second;hit<<"{\"status\":\"MATCH\",\"canonical_unbased_graph\":";graph_json_h(hit,keyed.second);hit<<",\"forward_rotated_pair\":";pair_json_h(hit,candidate);hit<<",\"reverse_pair\":";pair_json_h(hit,r.words);hit<<",\"forward_original_base\":"<<keyed.second.original_base<<",\"reverse_original_base\":"<<r.base<<",\"reverse_corpus\":"<<r.corpus<<",\"reverse_index\":"<<r.index<<"}\n";}
   else{const auto&w=decision.witness;hit<<"{\"status\":\"PRIMITIVE\",\"alphabet\":\""<<w.alphabet<<"\",\"program\":\""<<w.program<<"\",\"component\":"<<w.component<<",\"vertex\":"<<w.vertex<<",\"expanded\":"<<(w.expanded?"true":"false")<<",\"cyclic_word\":\""<<w.cyclic_word<<"\",\"based_word\":\""<<w.based_word<<"\",\"pair\":";pair_json_h(hit,candidate);hit<<",\"encoded_graph\":";graph_json_h(hit,g);hit<<"}\n";}break;}
  if(nodes.size()>=maxnodes)break;
 }
 unresolved.close();native_log.close();std::ofstream journal(prefix+".nodes.jsonl");
 for(size_t id=0;id<nodes.size();++id){const auto&n=nodes[id];journal<<"{\"id\":"<<id<<",\"parent\":"<<n.parent<<",\"words\":";pair_json_h(journal,n.words);journal<<",\"basis\":";pair_json_h(journal,n.basis);journal<<",\"prelude\":[";for(size_t i=0;i<n.prelude.size();++i){if(i)journal<<',';journal<<n.prelude[i];}journal<<"],\"source_energy\":"<<n.source_energy<<"}\n";}
 std::vector<uint32_t> chain;for(auto at=best;;at=nodes[at].parent){chain.push_back(at);if(!at)break;}std::reverse(chain.begin(),chain.end());
 std::ofstream path(prefix+".path.json");path<<"{\"format\":\"coupled-h-phase-path-v1\",\"start\":";pair_json_h(path,initial);path<<",\"target\":";pair_json_h(path,nodes[best].words);path<<",\"stages\":[";
 for(size_t k=1;k<chain.size();++k){const auto&n=nodes[chain[k]];if(k>1)path<<',';path<<"{\"prelude\":[";for(size_t j=0;j<n.prelude.size();++j){if(j)path<<',';path<<n.prelude[j];}path<<"],\"target\":";pair_json_h(path,n.words);path<<"}";}path<<"]}\n";
 double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count();std::ofstream result(prefix+".results.json");
 result<<"{\"status\":\"HEURISTIC_H_SEARCH\",\"ordinary_AC_goal_solved\":false,\"hit\":\""<<hit_type<<"\",\"seed\":"<<seed<<",\"attempts\":"<<std::min(tried,attempts)<<",\"admitted_boundary_graphs\":"<<admitted<<",\"stored_nodes\":"<<nodes.size()<<",\"distinct_classified_graphs\":"<<tested.size()<<",\"known_catalogue_absence\":"<<catalogue_absent<<",\"DAG_absence\":"<<dag_absent<<",\"native_complete_absence\":"<<native_absent<<",\"native_incomplete\":"<<incomplete<<",\"native_pair_states\":"<<native_states<<",\"known_trivial_H_union_keys\":"<<reverse.size()<<",\"min_vertices\":"<<minvertices<<",\"maximum_boundary_cyclic_sum\":"<<maxenergy<<",\"discarded_by_sampling_limits\":"<<discarded<<",\"saved_path_stages\":"<<chain.size()-1<<",\"seconds\":"<<seconds<<"}\n";
 std::cout<<"H nodes "<<nodes.size()<<" classified "<<tested.size()<<" incomplete "<<incomplete<<" hit "<<hit_type<<" seconds "<<seconds<<"\n";return 0;
}catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}}
