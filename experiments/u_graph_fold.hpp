#ifndef U_GRAPH_FOLD_HPP
#define U_GRAPH_FOLD_HPP
#include "u_native_primitive.hpp"
#include <map>
#include <numeric>

namespace u_native {
// Repeated single-conflict folding, independent of Q's incremental merger.
inline Graph fold_words(const std::vector<std::string>&words){
    std::vector<std::array<int,3>> arcs;unsigned count=1;
    for(const auto&raw:words){auto w=reduce(raw);unsigned at=0;
        for(size_t i=0;i<w.size();++i){unsigned end=i+1==w.size()?0:count++;int c=letter(w[i]);
            arcs.push_back({int(at),c,int(end)});arcs.push_back({int(end),c^1,int(at)});at=end;}}
    std::vector<unsigned> parent(count);std::iota(parent.begin(),parent.end(),0);
    auto root=[&](unsigned v){while(parent[v]!=v){parent[v]=parent[parent[v]];v=parent[v];}return v;};
    while(true){std::map<std::pair<unsigned,int>,unsigned> outgoing;bool changed=false;
        for(const auto&e:arcs){auto a=root(unsigned(e[0])),b=root(unsigned(e[2]));auto k=std::make_pair(a,e[1]);auto old=outgoing.find(k);
            if(old!=outgoing.end()&&root(old->second)!=b){auto other=root(old->second);parent[std::max(other,b)]=std::min(other,b);changed=true;break;}outgoing[k]=b;}
        if(!changed)break;
    }
    std::vector<std::array<int,4>> quotient(count,{{-1,-1,-1,-1}});
    for(const auto&e:arcs)quotient[root(unsigned(e[0]))][e[1]]=int(root(unsigned(e[2])));
    Graph result;std::vector<int> name(count,-1);std::queue<unsigned> todo;auto base=root(0);name[base]=0;todo.push(base);unsigned next=1;
    while(!todo.empty()){auto v=todo.front();todo.pop();std::array<int,4> row{{-1,-1,-1,-1}};
        for(unsigned c=0;c<4;++c){int end=quotient[v][c];if(end<0)continue;if(name[end]<0){name[end]=int(next++);todo.push(unsigned(end));}row[c]=name[end];}result.push_back(row);}
    validate(result);return result;
}
inline Graph rebase_graph(const Graph&g,unsigned base){
    validate(g);if(base>=g.size())throw std::runtime_error("invalid graph base");
    Graph out;std::vector<int> names(g.size(),-1);std::queue<unsigned> todo;names[base]=0;todo.push(base);unsigned next=1;
    while(!todo.empty()){auto v=todo.front();todo.pop();std::array<int,4> row{{-1,-1,-1,-1}};
        for(unsigned c=0;c<4;++c){int end=g[v][c];if(end<0)continue;if(names[end]<0){names[end]=int(next++);todo.push(unsigned(end));}row[c]=names[end];}out.push_back(row);}
    return out;
}
} // namespace u_native
#endif
