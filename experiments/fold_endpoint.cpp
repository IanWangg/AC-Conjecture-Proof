// Exact Stallings folding of two long freely reduced words. No search bound.
#include <array>
#include <fstream>
#include <iostream>
#include <queue>
#include <string>
#include <vector>

struct Graph {
    std::vector<int> parent, size;
    std::vector<std::array<int,4>> adjacency;
    std::queue<std::pair<int,int>> pending;
    int vertex() {
        int v=parent.size(); parent.push_back(v); size.push_back(1);
        adjacency.push_back({-1,-1,-1,-1}); return v;
    }
    int root(int v) {
        while(parent[v]!=v) { parent[v]=parent[parent[v]]; v=parent[v]; }
        return v;
    }
    void arc(int v,int label,int w) {
        if(adjacency[v][label]<0) adjacency[v][label]=w;
        else pending.push({adjacency[v][label],w});
    }
    void edge(int v,int label,int w) { arc(v,label,w); arc(w,label^1,v); }
    void fold() {
        while(!pending.empty()) {
            auto [v,w]=pending.front(); pending.pop(); v=root(v);w=root(w);
            if(v==w)continue;
            if(size[v]<size[w])std::swap(v,w);
            parent[w]=v;size[v]+=size[w];
            for(int label=0;label<4;++label) {
                int destination=adjacency[w][label];
                if(destination<0)continue;
                if(adjacency[v][label]<0)adjacency[v][label]=destination;
                else pending.push({adjacency[v][label],destination});
            }
        }
    }
};

#ifndef AC_FOLD_ENDPOINT_LIBRARY
int main(int argc,char**argv) {
    if(argc!=2){std::cerr<<"usage: fold_endpoint word-pair.txt\n";return 2;}
    std::ifstream input(argv[1]);std::string word;
    Graph graph;graph.vertex();int words=0;
    while(std::getline(input,word)) {
        if(word.empty())continue;
        int v=0;
        for(size_t i=0;i<word.size();++i) {
            int label=word[i]=='x'?0:word[i]=='X'?1:word[i]=='y'?2:word[i]=='Y'?3:-1;
            if(label<0)return 3;
            int w=i+1==word.size()?0:graph.vertex();
            graph.edge(v,label,w);v=w;
        }
        ++words;
    }
    graph.fold();
    int vertices=0,directed=0;
    for(size_t v=0;v<graph.parent.size();++v) {
        if(graph.root(v)!=int(v))continue;
        ++vertices;
        for(int label=0;label<4;++label)if(graph.adjacency[v][label]>=0)++directed;
    }
    int base=graph.root(0);
    bool x=graph.adjacency[base][0]>=0&&graph.root(graph.adjacency[base][0])==base;
    bool y=graph.adjacency[base][2]>=0&&graph.root(graph.adjacency[base][2])==base;
    std::cout<<"{\"words\":"<<words<<",\"vertices\":"<<vertices
             <<",\"unoriented_edges\":"<<directed/2
             <<",\"rank\":"<<directed/2-vertices+1
             <<",\"accepts_x\":"<<(x?"true":"false")
             <<",\"accepts_y\":"<<(y?"true":"false")<<"}\n";
}
#endif
