// All independent rotations of a supplied cyclic catalogue, with exact
// folding and unbased labelled-core deduplication.  Candidate means only
// failure of a sufficient primitive-absence criterion, not a primitive.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>

using Row=std::array<int,4>;
struct Graph {std::vector<Row> out; int original_base=0;};
int letter(char c){auto at=std::string("xXyY").find(c);if(at==std::string::npos)throw std::runtime_error("bad letter");return int(at);}
char inverse(char c){return "xXyY"[letter(c)^1];}
std::string inv(const std::string&w){std::string s;for(auto i=w.rbegin();i!=w.rend();++i)s+=inverse(*i);return s;}
std::string reduce(const std::string&w){std::string s;for(char c:w){letter(c);if(!s.empty()&&s.back()==inverse(c))s.pop_back();else s+=c;}return s;}
std::vector<std::string> rotations(const std::string&w){std::vector<std::string>r;for(size_t i=0;i<w.size();++i)r.push_back(w.substr(i)+w.substr(0,i));std::sort(r.begin(),r.end());r.erase(std::unique(r.begin(),r.end()),r.end());return r;}

Graph fold(const std::string&u,const std::string&v){
    std::vector<std::array<int,3>> arcs;
    int n=1;
    for(const auto&w:{u,v}){
        int at=0;
        for(size_t i=0;i<w.size();++i){int next=i+1==w.size()?0:n++;int c=letter(w[i]);arcs.push_back({at,c,next});arcs.push_back({next,c^1,at});at=next;}
    }
    if(n>120)throw std::runtime_error("unexpected graph size");
    std::vector<int>parent(n);std::vector<Row> out(n,Row{-1,-1,-1,-1});
    for(int i=0;i<n;++i)parent[i]=i;
    auto root=[&](int at){while(parent[at]!=at){parent[at]=parent[parent[at]];at=parent[at];}return at;};
    auto unite=[&](int first,int second){
        std::vector<std::pair<int,int>> queue{{first,second}};
        for(size_t k=0;k<queue.size();++k){int a=root(queue[k].first),b=root(queue[k].second);if(a==b)continue;if(a>b)std::swap(a,b);parent[b]=a;
            for(int c=0;c<4;++c){int x=out[a][c],y=out[b][c];if(x<0)out[a][c]=y;else if(y>=0)queue.emplace_back(x,y);}
        }
    };
    for(const auto&e:arcs){int a=root(e[0]),b=root(e[2]);if(out[a][e[1]]<0)out[a][e[1]]=b;else unite(out[a][e[1]],b);}
    std::vector<int>names(n,-1),queue{root(0)};names[queue[0]]=0;Graph result;
    for(size_t k=0;k<queue.size();++k){Row row{-1,-1,-1,-1};int a=root(queue[k]);
        for(int c=0;c<4;++c)if(out[a][c]>=0){int b=root(out[a][c]);if(names[b]<0){names[b]=int(queue.size());queue.push_back(b);}row[c]=names[b];}
        result.out.push_back(row);
    }
    int oriented=0;
    for(size_t a=0;a<result.out.size();++a){int degree=0;for(int c=0;c<4;++c){int b=result.out[a][c];if(b>=0){++oriented;++degree;if(result.out[b][c^1]!=int(a))throw std::runtime_error("inverse arc inconsistency");}}if(degree<2)throw std::runtime_error("noncore source");}
    if(oriented/2-int(result.out.size())+1!=2)throw std::runtime_error("rank not two");
    return result;
}

std::pair<std::string,Graph> unbased_key(const Graph&g){
    std::vector<int>branches;
    for(size_t i=0;i<g.out.size();++i){int degree=0;for(int c:g.out[i])if(c>=0)++degree;if(degree>=3)branches.push_back(int(i));}
    if(branches.empty()||branches.size()>2)throw std::runtime_error("bad rank-two core topology");
    std::string best;Graph answer;bool first=true;
    for(int base:branches){
        std::vector<int>names(g.out.size(),-1),queue{base};names[base]=0;Graph h;std::string code;
        for(size_t k=0;k<queue.size();++k){Row row{-1,-1,-1,-1};
            for(int c=0;c<4;++c){int end=g.out[queue[k]][c];if(end>=0){if(names[end]<0){names[end]=int(queue.size());queue.push_back(end);}row[c]=names[end];}code.push_back(char(row[c]+1));}
            h.out.push_back(row);
        }
        h.original_base=names[g.original_base];
        if(first||code<best){first=false;best=code;answer=h;}
    }
    return {best,answer};
}

bool double_free_cycle(const Graph&g,int a,int b,int blocked){
    std::vector<int>color(2*g.out.size(),0);
    auto visit=[&](auto&&self,int state)->bool{
        if(color[state]==1)return true;if(color[state]==2)return false;color[state]=1;
        int at=state/2,previous=state%2,edge=previous?b:a,end=g.out[at][edge];
        if(end<0)throw std::runtime_error("inactive state traversed");
        for(int next=0;next<2;++next){if(previous==blocked&&next==blocked)continue;if(g.out[end][next?b:a]>=0&&self(self,2*end+next))return true;}
        color[state]=2;return false;
    };
    for(size_t v=0;v<g.out.size();++v)for(int i=0;i<2;++i)if(g.out[v][i?b:a]>=0&&visit(visit,2*int(v)+i))return true;
    return false;
}
bool proves_primitive_absence(const Graph&g){
    for(int a:{0,1})for(int b:{2,3})for(int blocked=0;blocked<2;++blocked)if(double_free_cycle(g,a,b,blocked))return false;
    return true;
}
void graph_json(std::ostream&out,const Graph&g){out<<'[';bool first=true;for(const auto&row:g.out)for(int end:row){if(!first)out<<',';first=false;out<<end;}out<<']';}

int main(int argc,char**argv){
    try{
        if(argc==4&&std::string(argv[1])=="--folds"){
            std::ifstream input(argv[2]);std::ofstream output(argv[3]);std::string line;
            while(std::getline(input,line)){auto tab=line.find('\t');if(tab==std::string::npos)throw std::runtime_error("bad row");auto g=unbased_key(fold(line.substr(0,tab),line.substr(tab+1))).second;output<<"{\"original_base\":"<<g.original_base<<",\"DAG_proves_primitive_absence\":"<<(proves_primitive_absence(g)?"true":"false")<<",\"graph\":";graph_json(output,g);output<<"}\n";}
            return 0;
        }
        if(argc<4)throw std::runtime_error("usage: rotation_subgroups catalogue.tsv candidates.jsonl result.json [max_pairs]");
        uint64_t limit=argc>4?std::stoull(argv[4]):UINT64_MAX;
        std::ifstream input(argv[1]);if(!input)throw std::runtime_error("input missing");std::ofstream candidate(argv[2]);
        std::unordered_set<std::string>seen;seen.reserve(1000000);
        uint64_t pairs=0,rotations_tested=0,graphs=0,dag=0,inconclusive=0;
        const auto start=std::chrono::steady_clock::now();std::string line;bool complete=true;
        while(std::getline(input,line)){
            if(pairs>=limit){complete=false;break;}
            auto tab=line.find('\t');if(tab==std::string::npos)throw std::runtime_error("bad row");std::string u=line.substr(0,tab),v=line.substr(tab+1);
            for(const auto&w:{u,v})if(w.empty()||reduce(w)!=w||w.front()==inverse(w.back()))throw std::runtime_error("source not cyclically reduced");
            auto uu=rotations(u),vv=rotations(v);
            for(const auto&a:uu)for(const auto&b:vv){++rotations_tested;auto labelled=unbased_key(fold(a,b));if(!seen.insert(labelled.first).second)continue;++graphs;
                if(proves_primitive_absence(labelled.second)){++dag;continue;}
                ++inconclusive;candidate<<"{\"source_index\":"<<pairs<<",\"source\":[\""<<u<<"\",\""<<v<<"\"],\"pair\":[\""<<a<<"\",\""<<b<<"\"],\"original_base\":"<<labelled.second.original_base<<",\"graph\":";graph_json(candidate,labelled.second);candidate<<"}\n";
                if(inconclusive<=20||inconclusive%100==0)candidate.flush();
            }
            ++pairs;
            if(pairs%10000==0)std::cout<<"pairs "<<pairs<<" rotation_pairs "<<rotations_tested<<" unique_unbased_graphs "<<graphs<<" candidates "<<inconclusive<<std::endl;
        }
        candidate.close();double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
        std::ofstream result(argv[3]);result<<"{\n\"status\":\""<<(complete?"COMPLETE":"INCOMPLETE")<<"\",\n\"ordinary_AC_goal_solved\":false,\n\"literal_source_pairs\":"<<pairs<<",\n\"independent_rotation_pairs\":"<<rotations_tested<<",\n\"distinct_unbased_labelled_core_graphs\":"<<graphs<<",\n\"direct_DAG_primitive_absence_graphs\":"<<dag<<",\n\"inconclusive_graphs\":"<<inconclusive<<",\n\"seconds\":"<<seconds<<"\n}\n";
        std::cout<<"finished "<<pairs<<" pairs "<<graphs<<" graphs "<<inconclusive<<" candidates "<<seconds<<" seconds\n";
    }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}
}
