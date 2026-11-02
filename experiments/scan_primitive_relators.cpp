// Inspect every distinct relator in a packed-search checkpoint.
// Exact rank-two cyclic Whitehead minimization; no length cutoff on descent.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>

char inv(char c) {return c=='x'?'X':c=='X'?'x':c=='y'?'Y':'y';}
std::string inverse(const std::string &s) {std::string t;for(auto at=s.rbegin();at!=s.rend();++at)t+=inv(*at);return t;}
std::string reduce(const std::string &s) {
    std::string t;
    for(char c:s){if(!t.empty()&&t.back()==inv(c))t.pop_back();else t+=c;}
    return t;
}
std::string cyclic(std::string s) {
    s=reduce(s);size_t a=0,b=s.size();
    while(b>a+1&&s[a]==inv(s[b-1])){++a;--b;}
    return s.substr(a,b-a);
}
std::string necklace(std::string s) {
    s=cyclic(s);std::string best=s;
    for(auto t:{s,inverse(s)})for(size_t k=0;k<t.size();++k)best=std::min(best,t.substr(k)+t.substr(0,k));
    return best;
}
std::string substitute(const std::string &s,char target,char donor,bool left) {
    std::string image=left?std::string(1,donor)+target:std::string(1,target)+donor;
    std::string negative=inverse(image),t;
    for(char c:s){if(c==target)t+=image;else if(c==inv(target))t+=negative;else t+=c;}
    return cyclic(t);
}
bool primitive(std::string s) {
    s=cyclic(s);
    while(s.size()>1) {
        std::string best=s;
        for(char target:std::string("xy")) {
            char other=target=='x'?'y':'x';
            for(char donor:{other,inv(other)})for(bool left:{false,true}) {
                std::string t=substitute(s,target,donor,left);
                if(t.size()<best.size())best=t;
            }
        }
        if(best.size()==s.size())return false;
        s=best;
    }
    return s.size()==1;
}
template<class T>void read(std::ifstream &f,T &v){f.read(reinterpret_cast<char*>(&v),sizeof(v));}
void selftest() {
    for(unsigned length=1;length<=9;++length) {
        uint64_t count=0;std::string word;
        std::function<void()> visit=[&]() {
            if(word.size()==length) {
                if(word.front()!=inv(word.back())&&primitive(word))++count;
                return;
            }
            for(char c:std::string("xXyY")) {
                if(!word.empty()&&word.back()==inv(c))continue;
                word+=c;visit();word.pop_back();
            }
        };
        visit();unsigned phi=0;
        for(unsigned a=1;a<=length;++a)if(std::gcd(a,length)==1)++phi;
        uint64_t expected=length==1?4:4*length*phi;
        if(count!=expected)throw std::runtime_error("cyclic primitive census control failed");
    }
    std::cout<<"{\"primitive_census_selftest\":\"PASS\",\"lengths\":\"1..9\",\"formula\":\"4 at length1; 4 L phi(L) otherwise\"}\n";
}
int main(int argc,char **argv) {
    try {
        if(argc==2&&std::string(argv[1])=="--selftest"){selftest();return 0;}
        if(argc!=2)throw std::runtime_error("usage: scan_primitive_relators CHECKPOINT");
        if(!primitive("x")||!primitive("xyx")||!primitive("xyxyxyx")||primitive("xyXY")||primitive("xx")||primitive("xxxYYYY")||primitive("xyxYXY"))throw std::runtime_error("primitive controls failed");
        std::ifstream f(argv[1],std::ios::binary);
        uint64_t magic,processed,count;unsigned n,cap;
        read(f,magic);read(f,n);read(f,cap);read(f,processed);read(f,count);
        if(!f||magic!=0x41435041434b3031ULL||cap>25||count>100000000)throw std::runtime_error("invalid checkpoint");
        std::unordered_set<uint64_t> words;
        unsigned minimum=100;
        for(uint64_t k=0;k<count;++k) {
            uint64_t key;read(f,key);if(!f)throw std::runtime_error("truncated checkpoint");
            unsigned lengths[2]={unsigned((key>>54)&31),unsigned(key>>59)},offset=0;
            for(unsigned len:lengths) {
                uint64_t mask=len?(uint64_t(1)<<(2*len))-1:0;
                uint64_t word=(key>>offset)&mask;
                words.insert(word|(uint64_t(len)<<58));
                minimum=std::min(minimum,len);offset+=2*len;
            }
        }
        std::unordered_map<std::string,bool> cache;
        uint64_t primitive_count=0,checked=0;
        std::string example;
        for(auto key:words) {
            unsigned len=key>>58;std::string s;
            for(unsigned k=0;k<len;++k)s+="xXyY"[(key>>(2*k))&3];
            std::string rep=necklace(s);
            auto at=cache.find(rep);
            bool yes;
            if(at==cache.end()){yes=primitive(rep);cache.emplace(rep,yes);}else yes=at->second;
            if(yes){++primitive_count;if(example.empty())example=s;}
            if(++checked%1000000==0)std::cerr<<"distinct relators checked="<<checked<<'\n';
        }
        std::cout<<"{\"n\":"<<n<<",\"cap\":"<<cap<<",\"checkpoint_states\":"<<count
                 <<",\"unique_oriented_raw_relators\":"<<words.size()<<",\"unique_cyclic_inverse_orbits\":"<<cache.size()
                 <<",\"minimum_individual_relator_length\":"<<minimum<<",\"primitive_raw_relators\":"<<primitive_count
                 <<",\"primitive_example\":\""<<example<<"\"}\n";
    }catch(const std::exception &e){std::cerr<<e.what()<<'\n';return 1;}
}
