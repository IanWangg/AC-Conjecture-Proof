// Run the signed cycle tests on one long folded endpoint.
#define AC_FOLD_ENDPOINT_LIBRARY
#include "fold_endpoint.cpp"

bool acyclic(Graph& graph,int first,int second,int blocked) {
    const int signs[]={first,second};
    std::vector<int> indegree(2*graph.parent.size(),-1);
    std::vector<int> active;
    for(int v=0;v<int(graph.parent.size());++v) if(graph.root(v)==v)
        for(int i=0;i<2;++i) if(graph.adjacency[v][signs[i]]>=0) {
            active.push_back(2*v+i);
            indegree[2*v+i]=0;
        }
    auto visit=[&](int state,auto advance) {
        const int i=state%2;
        const auto next=graph.root(graph.adjacency[state/2][signs[i]]);
        for(int j=0;j<2;++j)
            if((i!=blocked || j!=blocked) && indegree[2*next+j]>=0)
                advance(2*next+j);
    };
    for(int state:active) visit(state,[&](int next) {++indegree[next];});
    std::vector<int> queue;
    for(int state:active) if(!indegree[state]) queue.push_back(state);
    for(std::size_t at=0;at<queue.size();++at)
        visit(queue[at],[&](int next) {if(--indegree[next]==0) queue.push_back(next);});
    return queue.size()==active.size();
}
int main() {
    Graph graph;
    graph.vertex();
    std::string word;
    for(int row=0;row<2;++row) {
        if (!(std::cin>>word) || word.empty()) return 2;
        int cur=0;
        for(size_t i=0;i<word.size();++i) {
            auto sign=std::string("xXyY").find(word[i]);
            if(sign==std::string::npos) return 1;
            auto next=i+1==word.size()?0:graph.vertex();
            graph.edge(cur,sign,next);
            cur=next;
        }
    }
    graph.fold();
    int vertices=0;
    for(int i=0;i<int(graph.parent.size());++i) vertices+=graph.root(i)==i;
    std::cout<<"{\n  \"folded_vertices\": "<<vertices<<",\n  \"acyclic_signed_transitions\": [";
    int pass=0;
    for(int x:{0,1})for(int y:{2,3})for(int b:{0,1}) {
        const auto okay=acyclic(graph,x,y,b);
        if (x!=0 || y!=2 || b!=0) std::cout<<", ";
        std::cout<<std::boolalpha<<okay;
        pass+=okay;
    }
    std::cout<<"],\n  \"literal_subgroup_primitive_absence\": "
             <<std::boolalpha<<(pass==8)<<"\n}\n";
    return pass==8?0:1;
}
