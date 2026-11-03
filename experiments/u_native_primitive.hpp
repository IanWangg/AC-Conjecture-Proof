#ifndef U_NATIVE_PRIMITIVE_HPP
#define U_NATIVE_PRIMITIVE_HPP
// Independent integer-map implementation of R's exact primitive-loop theorem.
// Full exhaustion is ABSENT; an explicit state budget is INCOMPLETE.
#include <array>
#include <cstdint>
#include <limits>
#include <queue>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

namespace u_native {
using Graph = std::vector<std::array<int,4>>;
enum class Status { ABSENT, PRIMITIVE, INCOMPLETE };
inline const char* status_name(Status s) {
    return s==Status::ABSENT?"ABSENT":s==Status::PRIMITIVE?"PRIMITIVE":"INCOMPLETE";
}
struct Witness {
    std::string alphabet,program,base_path,cyclic_word,based_word;
    unsigned component=0,vertex=0;
    bool expanded=false;
};
struct AlphabetResult {
    std::string alphabet;
    Status status=Status::INCOMPLETE;
    uint64_t discovered=0,processed=0;
    // Each saved row is A[0..N],B[0..N], including absorbing missing=N.
    std::vector<std::vector<uint16_t>> closed_pairs;
};
struct Result {
    Status status=Status::INCOMPLETE;
    uint64_t pair_states=0;
    std::vector<AlphabetResult> alphabets;
    Witness witness;
};
inline int letter(char c) {
    switch(c){case 'x':return 0;case 'X':return 1;case 'y':return 2;case 'Y':return 3;}
    throw std::runtime_error("invalid free letter");
}
inline char opposite(char c){return "xXyY"[letter(c)^1];}
inline std::string inverse(const std::string&w){
    std::string out;out.reserve(w.size());for(auto i=w.rbegin();i!=w.rend();++i)out+=opposite(*i);return out;
}
inline std::string reduce(const std::string&w){
    std::string out;for(char c:w){letter(c);if(!out.empty()&&out.back()==opposite(c))out.pop_back();else out+=c;}return out;
}
inline void validate(const Graph&g) {
    const size_t n=g.size();
    if(!n||n>=std::numeric_limits<uint16_t>::max())throw std::runtime_error("unsupported graph size");
    for(size_t v=0;v<n;++v)for(unsigned c=0;c<4;++c){int w=g[v][c];
        if(w< -1||w>=int(n))throw std::runtime_error("invalid graph vertex");
        if(w>=0&&g[w][c^1]!=int(v))throw std::runtime_error("inverse arc inconsistency");
    }
    std::vector<bool> seen(n);std::queue<unsigned> todo;seen[0]=true;todo.push(0);size_t count=1;
    while(!todo.empty()){auto v=todo.front();todo.pop();for(int w:g[v])if(w>=0&&!seen[w]){seen[w]=true;todo.push(unsigned(w));++count;}}
    if(count!=n)throw std::runtime_error("disconnected graph");
}
inline int follow(const Graph&g,int v,const std::string&w){
    for(char c:w){if(v<0)return -1;v=g[v][letter(c)];}return v;
}
inline std::string base_path(const Graph&g,unsigned target){
    std::vector<int> parent(g.size(),-1),edge(g.size(),-1);std::queue<unsigned> todo;
    parent[0]=0;todo.push(0);
    while(!todo.empty()&&parent[target]<0){auto v=todo.front();todo.pop();for(unsigned c=0;c<4;++c){int w=g[v][c];
        if(w>=0&&parent[w]<0){parent[w]=int(v);edge[w]=int(c);todo.push(unsigned(w));}}}
    if(parent[target]<0)throw std::runtime_error("unreachable witness vertex");
    std::string reverse_word;for(unsigned v=target;v;v=unsigned(parent[v]))reverse_word+="xXyY"[edge[v]];
    return std::string(reverse_word.rbegin(),reverse_word.rend());
}
namespace detail {
struct Node {std::vector<uint16_t> maps;uint32_t parent;char operation;};
inline std::string key(const std::vector<uint16_t>&maps){
    std::string out;out.reserve(2*maps.size());for(uint16_t x:maps){out+=char(x&255);out+=char(x>>8);}return out;
}
inline int fixed(const std::vector<uint16_t>&maps,size_t offset,size_t n){
    for(size_t v=0;v<n;++v)if(maps[offset+v]==v)return int(v);return -1;
}
inline Witness make_witness(const Graph&g,const std::string&alphabet,
                            const std::vector<Node>&nodes,uint32_t at,
                            unsigned component,unsigned vertex,size_t expansion_limit){
    Witness w;w.alphabet=alphabet;w.component=component;w.vertex=vertex;w.base_path=base_path(g,vertex);
    std::string backwards;for(auto i=at;nodes[i].operation;i=nodes[i].parent)backwards+=nodes[i].operation;
    w.program=std::string(backwards.rbegin(),backwards.rend());
    std::string a(1,alphabet[0]),b(1,alphabet[1]);bool explicit_words=expansion_limit>=1;
    for(char op:w.program){
        if(!explicit_words)break;
        if(a.size()>expansion_limit||b.size()>expansion_limit||a.size()>expansion_limit-b.size()){explicit_words=false;break;}
        if(op=='L')b=a+b;else if(op=='R')a=a+b;else throw std::runtime_error("invalid parent program");
    }
    if(explicit_words){
        w.cyclic_word=component?b:a;
        if(follow(g,int(vertex),w.cyclic_word)!=int(vertex))throw std::runtime_error("witness loop mismatch");
        w.based_word=reduce(w.base_path+w.cyclic_word+inverse(w.base_path));
        if(follow(g,0,w.based_word)!=0)throw std::runtime_error("based witness mismatch");
        w.expanded=true;
    }
    return w;
}
inline AlphabetResult alphabet_decide(const Graph&g,const std::string&alphabet,
                                     uint64_t budget,size_t expansion_limit,
                                     bool save_certificate,Witness&positive){
    const size_t n=g.size(),stride=n+1;
    std::vector<uint16_t> initial(2*stride,uint16_t(n));
    for(unsigned j=0;j<2;++j)for(size_t v=0;v<n;++v){int end=g[v][letter(alphabet[j])];initial[j*stride+v]=uint16_t(end<0?n:end);}
    std::vector<Node> nodes{{initial,0,0}};
    std::unordered_map<std::string,uint32_t> indices;indices.emplace(key(initial),0);
    AlphabetResult result;result.alphabet=alphabet;
    for(size_t at=0;at<nodes.size();++at){
        const auto current=nodes[at].maps;
        for(unsigned component=0;component<2;++component){int v=fixed(current,component*stride,n);
            if(v>=0){
                result.status=Status::PRIMITIVE;result.discovered=nodes.size();result.processed=at;
                positive=make_witness(g,alphabet,nodes,uint32_t(at),component,unsigned(v),expansion_limit);return result;
            }
        }
        std::vector<uint16_t> product(stride);
        for(size_t v=0;v<stride;++v)product[v]=current[stride+current[v]];
        for(char operation:std::string("LR")){
            auto next=current;
            for(size_t v=0;v<stride;++v)next[(operation=='L'?stride:0)+v]=product[v];
            auto encoded=key(next);
            if(indices.find(encoded)!=indices.end())continue;
            if((budget&&nodes.size()>=budget)||nodes.size()>=std::numeric_limits<uint32_t>::max()){
                result.status=Status::INCOMPLETE;result.discovered=nodes.size();result.processed=at;return result;
            }
            indices.emplace(std::move(encoded),uint32_t(nodes.size()));nodes.push_back({std::move(next),uint32_t(at),operation});
        }
    }
    result.status=Status::ABSENT;result.discovered=result.processed=nodes.size();
    if(save_certificate){result.closed_pairs.reserve(nodes.size());for(auto &node:nodes)result.closed_pairs.push_back(std::move(node.maps));}
    return result;
}
} // namespace detail

inline Result decide(const Graph&g,uint64_t budget=100000,size_t expansion_limit=1000000,
                     bool save_certificate=false){
    validate(g);Result result;result.status=Status::ABSENT;
    for(const auto&alphabet:{std::string("xy"),std::string("xY"),std::string("Xy"),std::string("XY")}){
        Witness witness;auto decision=detail::alphabet_decide(g,alphabet,budget,expansion_limit,save_certificate,witness);
        result.pair_states+=decision.discovered;result.alphabets.push_back(std::move(decision));
        auto status=result.alphabets.back().status;
        if(status==Status::PRIMITIVE){result.status=status;result.witness=std::move(witness);return result;}
        if(status==Status::INCOMPLETE)result.status=status;
    }
    return result;
}
} // namespace u_native
#endif
