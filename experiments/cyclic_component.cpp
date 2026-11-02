// Exact cyclic AC component generator with optional full bridge menu.
// The separate axes proof establishes completeness of that finite menu.
#include <algorithm>
#include <chrono>
#include <fstream>
#include <iostream>
#include <map>
#include <queue>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;
using P=pair<string,string>;
char invchar(char c){return c>='a'&&c<='z'?c-'a'+'A':c-'A'+'a';}
string inverse(string s){reverse(s.begin(),s.end());for(char &c:s)c=invchar(c);return s;}
string reduce(string s){string t;for(char c:s){if(!t.empty()&&t.back()==invchar(c))t.pop_back();else t+=c;}return t;}
string cyclic(string s){s=reduce(s);size_t a=0,b=s.size();while(b>a+1&&s[a]==invchar(s[b-1])){a++;b--;}return s.substr(a,b-a);}
vector<string> variants(string s){s=cyclic(s);vector<string> v;for(string t:{s,inverse(s)})for(size_t k=0;k<t.size();k++)v.push_back(t.substr(k)+t.substr(0,k));sort(v.begin(),v.end());v.erase(unique(v.begin(),v.end()),v.end());return v;}
string canonical(string s){s=cyclic(s);if(s.empty())return s;string best=s;for(string t:{s,inverse(s)})for(size_t k=0;k<t.size();k++)best=min(best,t.substr(k)+t.substr(0,k));return best;}
P canonpair(string a,string b){if(b<a)swap(a,b);return {a,b};}
string key(P p){return p.first+":"+p.second;}
vector<string> bridges(int length){vector<string> all{""},level{""};for(int j=0;j<length;j++){vector<string> next;for(auto p:level)for(char c:string("xXyY"))if(p.empty()||p.back()!=invchar(c))next.push_back(p+c);all.insert(all.end(),next.begin(),next.end());level=std::move(next);}return all;}
int main(int argc,char**argv){
 if(argc<4){cerr<<"cap catalogue.json results.json [maxstates=5000000] [fullbridge=0]\n";return 2;}
 int cap=stoi(argv[1]);size_t maxstates=argc>4?stoull(argv[4]):5000000;
 bool fullbridge=argc>5&&stoi(argv[5]);
 auto begun=chrono::steady_clock::now();
 P initial=canonpair(canonical("xxxYYYY"),canonical("xyxYXY"));
 vector<P> nodes{initial};unordered_map<string,size_t> seen{{key(initial),0}};
 unordered_map<string,vector<string>> vc;
 unsigned long long checks=0,admitted=0;size_t at=0;bool stop=false;
 int minsum=13,minword=6,minbridge=21;map<int,size_t> hist;
 for(;at<nodes.size()&&!stop;at++){
  P p=nodes[at];string w[2]={p.first,p.second};
  for(auto s:w)if(!vc.count(s))vc[s]=variants(s);
  const auto vv0=vc[w[0]],vv1=vc[w[1]];vector<string> vv[2]={vv0,vv1};
  for(int i=0;i<2&&!stop;i++){
   int d=fullbridge?(cap-(int)w[i].size()-2*(int)w[1-i].size())/2:0;
   if(d<0)d=0;
   auto tails=bridges(d);
   for(auto a:vv[i])for(auto b:vv[1-i])for(auto tail:tails){
   if(stop)break;
   checks++;string r=canonical(a+tail+b+inverse(tail));
   if(r.size()+w[1-i].size()>(size_t)cap)continue;
   admitted++;P q=canonpair(r,w[1-i]);string k=key(q);
   if(seen.count(k))continue;
   seen[k]=nodes.size();nodes.push_back(q);
   if(min(q.first.size(),q.second.size())<5)cerr<<"short coordinate "<<q.first<<" "<<q.second<<"\n";
   if(nodes.size()>=maxstates){stop=true;break;}
  }}
  if(at%100000==0)cerr<<"processed "<<at<<" states "<<nodes.size()<<" checks "<<checks<<"\n";
 }
 sort(nodes.begin(),nodes.end());
 ofstream out(argv[2]);out<<"[";bool first=true;
 for(auto p:nodes){
  if(!first)out<<",";first=false;out<<"[\""<<p.first<<"\",\""<<p.second<<"\"]";
  int s=p.first.size()+p.second.size(),m=min(p.first.size(),p.second.size());
  minsum=min(minsum,s);minword=min(minword,m);minbridge=min(minbridge,s+m+2);hist[s]++;
 }
 out<<"]\n";out.close();
 double sec=chrono::duration<double>(chrono::steady_clock::now()-begun).count();
 ofstream result(argv[3]);
 result<<"{\n\"status\":\""<<(stop?"INCOMPLETE":"PASS")<<"\",\n\"ordinary_AC_goal_solved\":false,\n";
 result<<"\"cyclic_cap\":"<<cap<<",\n\"full_bridge_menu\":"<<(fullbridge?"true":"false")<<",\n\"states\":"<<nodes.size()<<",\n\"rotation_product_candidates\":"<<checks<<",\n\"admitted_neighbors\":"<<admitted<<",\n";
 result<<"\"minimum_cyclic_sum\":"<<minsum<<",\n\"minimum_cyclic_coordinate\":"<<minword<<",\n\"minimum_disjoint_axes_neighbor_sum\":"<<minbridge<<",\n\"seconds\":"<<sec<<",\n\"histogram\":{";
 first=true;for(auto z:hist){if(!first)result<<",";first=false;result<<"\""<<z.first<<"\":"<<z.second;}result<<"}\n}\n";
 cout<<"states="<<nodes.size()<<" minsum="<<minsum<<" minword="<<minword<<" minbridge="<<minbridge<<" complete="<<(!stop)<<" seconds="<<sec<<"\n";
}
