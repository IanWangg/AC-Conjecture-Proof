// Heuristic actual ordinary-AC search. No negative run proves an obstruction.
// Each accepted state has a parent and exact signed-rotation/tail-product edge.
#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <random>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

char inverse_letter(char c){return c=='x'?'X':c=='X'?'x':c=='y'?'Y':'y';}
std::string inverse(std::string w){std::reverse(w.begin(),w.end());for(char &c:w)c=inverse_letter(c);return w;}
std::string cyclic(std::string w){
    std::string stack;for(char c:w){if(!stack.empty()&&stack.back()==inverse_letter(c))stack.pop_back();else stack+=c;}
    size_t a=0,b=stack.size();while(b>a+1&&stack[a]==inverse_letter(stack[b-1])){++a;--b;}return stack.substr(a,b-a);
}
std::string least_rotation(const std::string &w){
    if(w.empty())return w;std::string twice=w+w;size_t i=0,j=1,k=0,n=w.size();
    while(i<n&&j<n&&k<n){if(twice[i+k]==twice[j+k]){++k;continue;}
        if(twice[i+k]>twice[j+k]){i+=k+1;if(i==j)++i;}else{j+=k+1;if(i==j)++j;}k=0;}
    return twice.substr(std::min(i,j),n);
}
std::string canonical(std::string w){w=cyclic(w);return std::min(least_rotation(w),least_rotation(inverse(w)));}
std::string key(std::string a,std::string b){if(a>b)a.swap(b);return a+":"+b;}
std::string positive(unsigned a,unsigned b){
    if(!a)return "y";if(!b)return "x";if(a==b)return "xy";
    std::string old= a>b?positive(a-b,b):positive(a,b-a),out;
    for(char c:old){if((a>b&&c=='y')||(b>a&&c=='x'))out+="xy";else out+=c;}return out;
}
bool primitive(const std::string &w){
    if(w.empty())return false;int a=0,b=0;
    for(char c:w){if(c=='x')++a;else if(c=='X')--a;else if(c=='y')++b;else --b;}
    if(unsigned(std::abs(a)+std::abs(b))!=w.size()||std::gcd(std::abs(a),std::abs(b))!=1)return false;
    std::string model=positive(std::abs(a),std::abs(b));
    for(char &c:model)if((c=='x'&&a<0)||(c=='y'&&b<0))c=inverse_letter(c);
    return (model+model).find(w)!=std::string::npos;
}
struct Node{std::string a,b,q;uint32_t parent;uint16_t ra=0,rb=0;uint8_t i=0,sa=0,sb=0;};
std::string orient(const std::string&w,unsigned sign,unsigned rotation){auto v=sign?inverse(w):w;return v.substr(rotation)+v.substr(0,rotation);}
std::string word_json(const std::string&w){return "\""+w+"\"";}

int main(int argc,char **argv){
    if(argc==2&&std::string(argv[1])=="--primitive-selftest"){
        const unsigned expected[]={0,4,8,24,32,80,48,168,128,216};std::vector<std::string> level{""};
        for(unsigned length=1;length<=9;++length){std::vector<std::string> next;unsigned count=0;
            for(const auto&w:level)for(char c:std::string("xXyY")){if(!w.empty()&&w.back()==inverse_letter(c))continue;auto v=w+c;next.push_back(v);if(v.front()!=inverse_letter(v.back())&&primitive(v))++count;}
            if(count!=expected[length]){std::cerr<<"primitive census failed "<<length<<" "<<count<<"\n";return 1;}level.swap(next);
        }std::cout<<"primitive census lengths1..9 PASS\n";return 0;
    }
    if(argc!=8&&argc!=10&&argc!=11){std::cerr<<"usage: random_cyclic_escape catalogue.json seed attempts maxnodes cap result.json path.json [first second [saved_node]]\n";return 2;}
    std::ifstream source(argv[1]);if(!source){std::cerr<<"missing source\n";return 2;}
    std::unordered_set<std::string> known,known_words;std::string text((std::istreambuf_iterator<char>(source)),{});std::vector<std::string> words;
    for(size_t at=0;(at=text.find('"',at))!=std::string::npos;){auto end=text.find('"',at+1);if(end==std::string::npos)return 2;words.push_back(text.substr(at+1,end-at-1));at=end+1;}
    if(words.size()%2)return 2;for(size_t i=0;i<words.size();i+=2){known.insert(key(words[i],words[i+1]));known_words.insert(words[i]);known_words.insert(words[i+1]);}
    auto seed=std::stoull(argv[2]), attempts=std::stoull(argv[3]),maxnodes=std::stoull(argv[4]);unsigned cap=std::stoul(argv[5]);
    std::mt19937_64 rng(seed);std::uniform_real_distribution<double> uniform(0,1);
    std::string first=argc>=10?argv[8]:"xxxYYYY",second=argc>=10?argv[9]:"xyxYXY";
    if(!known.count(key(canonical(first),canonical(second)))){std::cerr<<"start outside verified component\n";return 2;}
    std::vector<Node> nodes{{canonical(first),canonical(second),"",0}};
    std::unordered_map<std::string,uint32_t> seen{{key(nodes[0].a,nodes[0].b),0}};
    std::vector<uint32_t> elite{0};uint32_t current=0,best=0,found=UINT32_MAX;uint64_t tested=0,accepted=0,discarded=0,outside=0;
    unsigned minword=std::min(first.size(),second.size()),minsum=first.size()+second.size(),maxsum=minsum;double bestscore=1e100;auto started=std::chrono::steady_clock::now();
    auto score=[&](const Node&n){auto s=n.a.size()+n.b.size(),m=std::min(n.a.size(),n.b.size());return 1.7*m+0.35*s+(known.count(key(n.a,n.b))?18.0:0.0)+6.0*(known_words.count(n.a)+known_words.count(n.b));};
    for(tested=1;tested<=attempts;++tested){
        if(tested%2000==0){if(uniform(rng)<0.7)current=elite[rng()%elite.size()];else current=rng()%nodes.size();}
        const Node old=nodes[current];Node next;next.parent=current;next.i=rng()%2;next.sa=rng()%2;next.sb=rng()%2;
        auto &recipient=next.i?old.b:old.a;auto &donor=next.i?old.a:old.b;
        next.ra=rng()%recipient.size();next.rb=rng()%donor.size();
        auto u=orient(recipient,next.sa,next.ra),v=orient(donor,next.sb,next.rb);
        unsigned tail=uniform(rng)<0.7?0:1+rng()%3;
        for(unsigned i=0;i<tail;++i){char c;do{c="xXyY"[rng()%4];}while(!next.q.empty()&&c==inverse_letter(next.q.back()));next.q+=c;}
        auto product=canonical(u+next.q+v+inverse(next.q));
        next.a=next.i?old.a:product;next.b=next.i?product:old.b;
        unsigned sum=next.a.size()+next.b.size();if(sum>cap||product.empty()){++discarded;continue;}
        bool hit=primitive(product);double delta=score(next)-score(old),temperature=0.8+4.0*double((tested/10000)%7)/6;
        if(!hit&&delta>0&&uniform(rng)>=std::exp(-delta/temperature))continue;
        ++accepted;auto k=key(next.a,next.b);auto existing=seen.find(k);
        if(existing!=seen.end())current=existing->second;
        else{
            current=nodes.size();seen.emplace(std::move(k),current);nodes.push_back(next);
            if(!known.count(key(next.a,next.b)))++outside;
            if(score(next)<bestscore){bestscore=score(next);best=current;}
            if(!known.count(key(next.a,next.b))){elite.push_back(current);if(elite.size()>256){std::sort(elite.begin(),elite.end(),[&](auto a,auto b){return score(nodes[a])<score(nodes[b]);});elite.resize(128);}}
            minword=std::min<unsigned>(minword,std::min(next.a.size(),next.b.size()));minsum=std::min(minsum,sum);maxsum=std::max(maxsum,sum);
        }
        if(hit){found=current;best=current;break;}
        if(nodes.size()>=maxnodes)break;
    }
    if(argc==11){auto requested=std::stoul(argv[10]);if(requested>=nodes.size()){std::cerr<<"saved node unavailable\n";return 2;}best=requested;}
    std::ofstream candidates(std::string(argv[6])+".elite.json");candidates<<"[";bool first_candidate=true;
    for(auto id:elite){if(!first_candidate)candidates<<",";first_candidate=false;candidates<<"{\"node\":"<<id<<",\"words\":["<<word_json(nodes[id].a)<<","<<word_json(nodes[id].b)<<"]}";}candidates<<"]\n";
    std::vector<uint32_t> path;for(auto at=best;;at=nodes[at].parent){path.push_back(at);if(!at)break;}std::reverse(path.begin(),path.end());
    std::ofstream ledger(argv[7]);ledger<<"{\n\"format\":\"cyclic-edge-path-v1\",\"start\":["<<word_json(first)<<","<<word_json(second)<<"],\"target\":["<<word_json(nodes[best].a)<<","<<word_json(nodes[best].b)<<"],\"edges\":[\n";
    for(size_t k=1;k<path.size();++k){auto n=nodes[path[k]],p=nodes[n.parent];auto u=orient(n.i?p.b:p.a,n.sa,n.ra),v=orient(n.i?p.a:p.b,n.sb,n.rb);if(k>1)ledger<<",\n";
        ledger<<"{\"i\":"<<unsigned(n.i)<<",\"u\":"<<word_json(u)<<",\"v\":"<<word_json(v)<<",\"q\":"<<word_json(n.q)<<"}";}
    ledger<<"]}\n";
    double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count();std::ofstream result(argv[6]);
    result<<"{\n\"status\":\"HEURISTIC_RUN\",\"ordinary_AC_goal_solved\":false,\"primitive_coordinate_found\":"<<(found==UINT32_MAX?"false":"true")<<",\"seed\":"<<seed<<",\"attempts\":"<<std::min(tested,attempts)<<",\"accepted_steps\":"<<accepted<<",\"stored_states\":"<<nodes.size()<<",\"outside_known_cap22_states\":"<<outside<<",\"discarded_for_length\":"<<discarded<<",\"minimum_coordinate_length\":"<<minword<<",\"minimum_cyclic_sum\":"<<minsum<<",\"maximum_accepted_cyclic_sum\":"<<maxsum<<",\"heuristic_length_cap\":"<<cap<<",\"saved_path_edges\":"<<path.size()-1<<",\"saved_endpoint\":["<<word_json(nodes[best].a)<<","<<word_json(nodes[best].b)<<"],\"seconds\":"<<seconds<<"}\n";
    std::cout<<"stored="<<nodes.size()<<" outside="<<outside<<" primitive="<<(found!=UINT32_MAX)<<" minimumcoordinate="<<minword<<" seconds="<<seconds<<"\n";
}
