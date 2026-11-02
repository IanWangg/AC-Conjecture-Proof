// Heuristic known-trivial-side search, default AK(2), with exact parent edges.
// Q's labelled folding/key routines are shared, not an independent fold.
#define Q_ROTATION_SUBGROUPS_LIBRARY
#if __has_include("rotation_subgroups.cpp")
#include "rotation_subgroups.cpp"
#else
#include "../research_q/rotation_subgroups.cpp"
#endif
#include <cmath>
#include <numeric>
#include <random>
#include <unordered_map>

std::string cyclic_r(std::string w){
    w=reduce(w);std::size_t a=0,b=w.size();
    while(b>a+1 && w[a]==inverse(w[b-1])){++a;--b;}
    return w.substr(a,b-a);
}
std::string minimum_rotation_r(const std::string&w){
    if(w.empty())return w;auto twice=w+w;std::size_t i=0,j=1,k=0,n=w.size();
    while(i<n&&j<n&&k<n){if(twice[i+k]==twice[j+k]){++k;continue;}
        if(twice[i+k]>twice[j+k]){i+=k+1;if(i==j)++i;}
        else{j+=k+1;if(i==j)++j;}k=0;}
    return twice.substr(std::min(i,j),n);
}
std::string canonical_r(std::string w){w=cyclic_r(w);return std::min(minimum_rotation_r(w),minimum_rotation_r(inv(w)));}
std::string pair_key_r(std::string a,std::string b){if(a>b)a.swap(b);return a+":"+b;}
std::string positive_r(unsigned a,unsigned b){
    if(!a)return "y";if(!b)return "x";if(a==b)return "xy";
    auto old=a>b?positive_r(a-b,b):positive_r(a,b-a);std::string out;
    for(char c:old){if((a>b&&c=='y')||(b>a&&c=='x'))out+="xy";else out+=c;}
    return out;
}
bool primitive_r(const std::string&w){
    int a=0,b=0;for(char c:w){if(c=='x')++a;else if(c=='X')--a;else if(c=='y')++b;else --b;}
    if(unsigned(std::abs(a)+std::abs(b))!=w.size()||std::gcd(std::abs(a),std::abs(b))!=1)return false;
    auto model=positive_r(std::abs(a),std::abs(b));
    for(char&c:model)if((c=='x'&&a<0)||(c=='y'&&b<0))c=inverse(c);
    return (model+model).find(w)!=std::string::npos;
}
std::string oriented_r(const std::string&w,unsigned sign,unsigned rotation){auto v=sign?inv(w):w;return v.substr(rotation)+v.substr(0,rotation);}
struct ReverseNode{std::string a,b,q;uint32_t parent=0;uint16_t ra=0,rb=0;uint8_t i=0,sa=0,sb=0;double score=0;};

int main(int argc,char**argv){
    try{
        if(argc!=10&&argc!=12)throw std::runtime_error("usage: reverse_subgroup_walk forward.tsv seed attempts maxnodes cap maxkeys candidate_cap output_prefix saved_path.json [first second]");
        std::ifstream forward(argv[1]);if(!forward)throw std::runtime_error("missing forward catalogue");
        std::unordered_map<std::string,uint32_t> forward_pairs;std::unordered_set<std::string> forward_words;
        std::string line;uint32_t forward_index=0;
        while(std::getline(forward,line)){auto at=line.find('\t');if(at==std::string::npos)throw std::runtime_error("bad forward row");auto a=line.substr(0,at),b=line.substr(at+1);forward_pairs.emplace(pair_key_r(a,b),forward_index++);forward_words.insert(a);forward_words.insert(b);}
        uint64_t seed=std::stoull(argv[2]),attempts=std::stoull(argv[3]),maxnodes=std::stoull(argv[4]),maxkeys=std::stoull(argv[6]);
        unsigned cap=std::stoul(argv[5]),candidate_cap=std::stoul(argv[7]);std::string prefix=argv[8];
        std::mt19937_64 rng(seed);std::uniform_real_distribution<double> uniform(0,1);
        auto score=[&](const ReverseNode&n){
            auto s=n.a.size()+n.b.size(),m=std::min(n.a.size(),n.b.size());
            return .24*s+1.7*std::abs(double(m)-6.0)+9.0*(primitive_r(n.a)+primitive_r(n.b))
                   -1.5*(forward_words.count(n.a)+forward_words.count(n.b));
        };
        std::string first=argc==12?argv[10]:"xxYYY",second=argc==12?argv[11]:"xyxYXY";
        ReverseNode initial;initial.a=canonical_r(first);initial.b=canonical_r(second);initial.score=score(initial);
        if(initial.a.empty()||initial.b.empty())throw std::runtime_error("empty starting coordinate unsupported");
        std::vector<ReverseNode> nodes{initial};std::unordered_map<std::string,uint32_t> seen{{pair_key_r(initial.a,initial.b),0}};
        std::unordered_set<std::string> graph_keys;graph_keys.reserve(maxkeys+1);
        std::vector<uint32_t> elite{0};uint32_t current=0,best=0,found=UINT32_MAX;double bestscore=initial.score;
        std::ofstream candidates(prefix+".pairs.tsv"),provenance(prefix+".pairs.jsonl");
        uint64_t tried=0,accepted=0,discarded=0,rotation_tests=0,candidate_sources=0,dag=0,exceptions=0;unsigned maxsum=initial.a.size()+initial.b.size();
        auto collect=[&](uint32_t node){
            const auto&n=nodes[node];if(n.a.size()+n.b.size()>candidate_cap || std::min(n.a.size(),n.b.size())<4 || primitive_r(n.a)||primitive_r(n.b)||graph_keys.size()>=maxkeys)return;
            ++candidate_sources;auto aa=rotations(n.a),bb=rotations(n.b);
            for(const auto&a:aa)for(const auto&b:bb){
                if(graph_keys.size()>=maxkeys)return;
                ++rotation_tests;auto keyed=unbased_key(fold(a,b));auto vertices=keyed.second.out.size();
                if(vertices<7||vertices>21||!graph_keys.insert(keyed.first).second)continue;
                bool absence=proves_primitive_absence(keyed.second);if(absence)++dag;else ++exceptions;
                auto index=graph_keys.size()-1;candidates<<a<<'\t'<<b<<'\n';
                provenance<<"{\"index\":"<<index<<",\"node\":"<<node<<",\"pair\":[\""<<a<<"\",\""<<b<<"\"],\"source_state\":[\""<<n.a<<"\",\""<<n.b<<"\"],\"vertices\":"<<vertices<<",\"DAG_absence\":"<<(absence?"true":"false")<<"}\n";
            }
        };
        collect(0);const auto started=std::chrono::steady_clock::now();
        for(tried=1;tried<=attempts;++tried){
            if(tried%1000==0){current=uniform(rng)<.75?elite[rng()%elite.size()]:rng()%nodes.size();}
            const auto old=nodes[current];ReverseNode next;next.parent=current;next.i=rng()%2;next.sa=rng()%2;next.sb=rng()%2;
            const auto&r=next.i?old.b:old.a;const auto&d=next.i?old.a:old.b;next.ra=rng()%r.size();next.rb=rng()%d.size();
            auto u=oriented_r(r,next.sa,next.ra),v=oriented_r(d,next.sb,next.rb);
            unsigned tail=uniform(rng)<.68?0:1+rng()%4;
            for(unsigned k=0;k<tail;++k){char c;do{c="xXyY"[rng()%4];}while(!next.q.empty()&&c==inverse(next.q.back()));next.q+=c;}
            auto product=canonical_r(u+next.q+v+inv(next.q));next.a=next.i?old.a:product;next.b=next.i?product:old.b;
            auto sum=next.a.size()+next.b.size();if(product.empty()||sum>cap){++discarded;continue;}
            next.score=score(next);auto key=pair_key_r(next.a,next.b);bool exact=forward_pairs.count(key);
            double temperature=.8+5.0*double((tried/10000)%9)/8,delta=next.score-old.score;
            if(!exact&&delta>0&&uniform(rng)>=std::exp(-delta/temperature))continue;
            ++accepted;auto prior=seen.find(key);
            if(prior!=seen.end())current=prior->second;
            else{
                current=nodes.size();seen.emplace(std::move(key),current);nodes.push_back(next);collect(current);
                maxsum=std::max<unsigned>(maxsum,sum);
                if(next.score<bestscore){bestscore=next.score;best=current;}
                if(std::min(next.a.size(),next.b.size())>=4){elite.push_back(current);if(elite.size()>256){std::sort(elite.begin(),elite.end(),[&](auto a,auto b){return nodes[a].score<nodes[b].score;});elite.resize(128);}}
            }
            if(exact){found=best=current;break;}
            if(nodes.size()>=maxnodes || graph_keys.size()>=maxkeys)break;
        }
        candidates.close();provenance.close();
        std::ofstream journal(prefix+".nodes.jsonl");
        for(std::size_t id=0;id<nodes.size();++id){const auto&n=nodes[id];journal<<"{\"id\":"<<id<<",\"parent\":"<<n.parent<<",\"words\":[\""<<n.a<<"\",\""<<n.b<<"\"],\"i\":"<<unsigned(n.i)<<",\"sa\":"<<unsigned(n.sa)<<",\"sb\":"<<unsigned(n.sb)<<",\"ra\":"<<n.ra<<",\"rb\":"<<n.rb<<",\"q\":\""<<n.q<<"\"}\n";}
        std::vector<uint32_t> path;for(auto at=best;;at=nodes[at].parent){path.push_back(at);if(!at)break;}std::reverse(path.begin(),path.end());
        std::ofstream saved(argv[9]);saved<<"{\"format\":\"cyclic-edge-path-v1\",\"start\":[\""<<first<<"\",\""<<second<<"\"],\"target\":[\""<<nodes[best].a<<"\",\""<<nodes[best].b<<"\"],\"edges\":[";
        for(std::size_t k=1;k<path.size();++k){const auto&n=nodes[path[k]];const auto&p=nodes[n.parent];if(k>1)saved<<',';auto u=oriented_r(n.i?p.b:p.a,n.sa,n.ra),v=oriented_r(n.i?p.a:p.b,n.sb,n.rb);saved<<"{\"i\":"<<unsigned(n.i)<<",\"u\":\""<<u<<"\",\"v\":\""<<v<<"\",\"q\":\""<<n.q<<"\"}";}saved<<"]}\n";
        double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count();std::ofstream result(prefix+".results.json");
        result<<"{\n\"status\":\"HEURISTIC_REVERSE_RUN\",\n\"ordinary_AC_goal_solved\":false,\n\"start\":[\""<<first<<"\",\""<<second<<"\"],\n\"seed\":"<<seed<<",\n\"attempts\":"<<std::min(tried,attempts)<<",\n\"stored_cyclic_states\":"<<nodes.size()<<",\n\"accepted_steps\":"<<accepted<<",\n\"discarded_for_energy\":"<<discarded<<",\n\"maximum_accepted_cyclic_sum\":"<<maxsum<<",\n\"heuristic_energy_cap\":"<<cap<<",\n\"reverse_candidate_energy_cap\":"<<candidate_cap<<",\n\"reverse_candidate_source_states\":"<<candidate_sources<<",\n\"reverse_rotated_pairs_tested\":"<<rotation_tests<<",\n\"distinct_reverse_unbased_core_keys\":"<<graph_keys.size()<<",\n\"direct_DAG_absence_keys\":"<<dag<<",\n\"inconclusive_keys\":"<<exceptions<<",\n\"exact_forward_cyclic_pair_match\":"<<(found==UINT32_MAX?"false":"true")<<",\n\"saved_path_edges\":"<<path.size()-1<<",\n\"seconds\":"<<seconds<<"\n}\n";
        std::cout<<"reverse states "<<nodes.size()<<" graphkeys "<<graph_keys.size()<<" cyclicpairmatch "<<(found!=UINT32_MAX)<<" seconds "<<seconds<<"\n";
        return 0;
    }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}
}
