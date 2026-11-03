// Independent native paired-rotation enumeration for a cyclic word tuple.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
int letter(char c){auto at=string("xXyY").find(c);if(at==string::npos)throw runtime_error("bad letter");return at;}
struct Link {
 vector<int> sheet,vertex; array<vector<int>,4> darts; int edges=0,vertices=0,components=0;
 Link(const vector<string>&words){
  for(const auto&w:words){
   if(w.empty())throw runtime_error("empty word");int n=w.size(),offset=edges;
   sheet.resize(2*(edges+n));vertex.resize(2*(edges+n));
   for(int i=0;i<n;++i){int a=letter(w[i]),b=letter(w[(i+1)%n]);if((a^1)==b)throw runtime_error("not cyclically reduced");
    int d=2*(offset+i);vertex[d]=a^1;vertex[d+1]=b;darts[a^1].push_back(d);darts[b].push_back(d+1);
    int before=2*(offset+(i+n-1)%n)+1;sheet[before]=d;sheet[d]=before;
   }edges+=n;
  }
  array<int,4> roots{0,1,2,3};auto root=[&](int v){while(roots[v]!=v)v=roots[v];return v;};
  for(int e=0;e<edges;++e)roots[root(vertex[2*e])]=root(vertex[2*e+1]);
  vector<int> used;for(int v=0;v<4;++v)if(!darts[v].empty()){++vertices;used.push_back(root(v));}
  sort(used.begin(),used.end());used.erase(unique(used.begin(),used.end()),used.end());components=used.size();
 }
};
struct Result{uint64_t checked=0;map<int,uint64_t>hist;int best=100000;bool complete=true;array<vector<int>,4>orders;};
Result enumerate(const Link&g,uint64_t budget){
 Result result;auto x=g.darts[0],y=g.darts[2];vector<int>sigma(2*g.edges);vector<uint64_t>seen(2*g.edges);uint64_t stamp=0;
 auto permutation_next=[](vector<int>&a){return a.size()>1&&next_permutation(a.begin()+1,a.end());};
 do{do{
  if(budget&&result.checked==budget){result.complete=false;return result;}
  array<vector<int>,4>orders;orders[0]=x;orders[2]=y;
  for(int v:{0,2})for(auto at=orders[v].rbegin();at!=orders[v].rend();++at)orders[v^1].push_back(g.sheet[*at]);
  for(const auto&o:orders)for(size_t j=0;j<o.size();++j)sigma[o[j]]=o[(j+1)%o.size()];
  ++stamp;int faces=0;for(int d=0;d<2*g.edges;++d)if(seen[d]!=stamp){++faces;int a=d;do{seen[a]=stamp;a=sigma[a^1];}while(a!=d);}
  int twice=2*g.components-g.vertices+g.edges-faces;if(twice<0||twice%2)throw runtime_error("bad surface Euler characteristic");
  int genus=twice/2;++result.checked;++result.hist[genus];if(genus<result.best){result.best=genus;result.orders=orders;}
  if(genus==0)return result;
 }while(permutation_next(y));sort(y.begin(),y.end());}while(permutation_next(x));return result;
}
void write_result(ostream&o,const vector<string>&words,const Result&r){
 o<<"{\"status\":\""<<(r.best==0?"PLANAR_COMPATIBLE":r.complete?"NO_PLANAR_COMPATIBLE":"INCOMPLETE")<<"\",\"words\":[";
 for(size_t i=0;i<words.size();++i){if(i)o<<',';o<<'"'<<words[i]<<'"';}o<<"],\"checked\":"<<r.checked<<",\"minimum_observed_genus\":"<<r.best<<",\"genus_histogram\":{";
 bool first=true;for(auto[g,n]:r.hist){if(!first)o<<',';first=false;o<<'"'<<g<<"\":"<<n;}o<<"},\"best_orders\":[";
 for(int v=0;v<4;++v){if(v)o<<',';o<<'[';for(size_t i=0;i<r.orders[v].size();++i){if(i)o<<',';o<<r.orders[v][i];}o<<']';}o<<"]}";
}
int main(int argc,char**argv){try{
 if(argc==5&&string(argv[1])=="--batch"){
  ifstream input(argv[2]);ofstream out(argv[3]);if(!input||!out)throw runtime_error("missing batch stream");string row;uint64_t budget=stoull(argv[4]),index=0,positive=0,incomplete=0;
  while(getline(input,row)){auto at=row.find('\t');if(at==string::npos)throw runtime_error("batch needs two TSV words");vector<string>words{row.substr(0,at),row.substr(at+1)};auto result=enumerate(Link(words),budget);write_result(out,words,result);out<<'\n';++index;positive+=result.best==0;incomplete+=!result.complete;if(index%1000==0)cerr<<"rows "<<index<<" positive "<<positive<<" incomplete "<<incomplete<<'\n';}
  cout<<"rows "<<index<<" positive "<<positive<<" incomplete "<<incomplete<<'\n';return 0;
 }
 if(argc<4)throw runtime_error("usage: thickening_rotations output.json budget word...");vector<string>words;for(int i=3;i<argc;++i)words.push_back(argv[i]);
 Link graph(words);auto result=enumerate(graph,stoull(argv[2]));ofstream out(argv[1]);write_result(out,words,result);out<<'\n';
 cout<<"rotations "<<result.checked<<" minimum observed genus "<<result.best<<" complete "<<result.complete<<'\n';return 0;
 }catch(const exception&e){cerr<<e.what()<<'\n';return 1;}}
