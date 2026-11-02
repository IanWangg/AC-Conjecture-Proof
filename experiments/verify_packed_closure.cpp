// Independent finite-set certificate audit using STRING word operations.
// Does not rerun BFS, trust parent pointers, or use packed-word multiplication.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <vector>

char inverse_letter(char c) {
    switch(c) {case 'x':return 'X';case 'X':return 'x';case 'y':return 'Y';case 'Y':return 'y';}
    throw std::runtime_error("invalid letter");
}
std::string inverse(const std::string &s) {
    std::string t;
    for(auto it=s.rbegin();it!=s.rend();++it) t+=inverse_letter(*it);
    return t;
}
std::string reduce(const std::string &s) {
    std::string t;
    for(char c:s) {if(!t.empty()&&t.back()==inverse_letter(c)) t.pop_back();else t+=c;}
    return t;
}
uint64_t bits(const std::string &s) {
    uint64_t v=0;unsigned shift=0;
    for(char c:s) {auto d=std::string("xXyY").find(c);if(d==std::string::npos)throw std::runtime_error("invalid word");v|=uint64_t(d)<<shift;shift+=2;}
    return v;
}
uint64_t canonical(std::string a,std::string b) {
    uint64_t va=std::min(bits(a),bits(inverse(a))),vb=std::min(bits(b),bits(inverse(b)));
    unsigned la=a.size(),lb=b.size();
    if(la>lb || (la==lb&&va>vb)) {std::swap(la,lb);std::swap(va,vb);}
    return va | (vb<<(2*la)) | (uint64_t(la)<<54) | (uint64_t(lb)<<59);
}
std::array<std::string,2> decode(uint64_t key) {
    unsigned lengths[2]={unsigned((key>>54)&31),unsigned(key>>59)};
    if(lengths[0]+lengths[1]>27) throw std::runtime_error("packing length invalid");
    std::array<std::string,2> answer;
    unsigned offset=0;
    for(unsigned j=0;j<2;++j) for(unsigned k=0;k<lengths[j];++k) {answer[j]+="xXyY"[(key>>offset)&3];offset+=2;}
    return answer;
}
template<class T> void read(std::ifstream &f,T &x){f.read(reinterpret_cast<char*>(&x),sizeof(x));}
int main(int argc,char **argv) {
    try {
        if(argc!=2) throw std::runtime_error("usage: verify_packed_closure CHECKPOINT");
        std::ifstream f(argv[1],std::ios::binary);
        uint64_t magic,processed,count;unsigned n,cap;
        read(f,magic);read(f,n);read(f,cap);read(f,processed);read(f,count);
        if(!f||magic!=0x41435041434b3031ULL||n<1||cap>25||processed!=count||count>100000000) throw std::runtime_error("invalid or incomplete checkpoint");
        std::vector<uint64_t> states(count);
        f.read(reinterpret_cast<char*>(states.data()),count*sizeof(uint64_t));
        if(!f) throw std::runtime_error("truncated checkpoint");
        std::unordered_set<uint64_t> members;
        members.reserve(count*5/4);
        for(auto key:states) if(!members.insert(key).second) throw std::runtime_error("duplicate member");
        uint64_t start=canonical(std::string(n,'x')+std::string(n+1,'Y'),"xyxYXY");
        if(!members.count(start)) throw std::runtime_error("starting tuple absent");
        unsigned minimum=100;
        std::map<unsigned,uint64_t> energies;
        uint64_t checked=0,edges=0;
        for(uint64_t key:states) {
            auto r=decode(key);
            unsigned energy=r[0].size()+r[1].size();
            if(energy>cap || reduce(r[0])!=r[0] || reduce(r[1])!=r[1] || canonical(r[0],r[1])!=key) throw std::runtime_error("malformed/noncanonical state");
            minimum=std::min(minimum,energy);++energies[energy];
            // Determinant is redundant for closure, but checks the packed
            // representation against the normal-generation necessary invariant.
            int ex[2][2]={{0,0},{0,0}};
            for(unsigned j=0;j<2;++j) for(char c:r[j]) ex[j][c=='x'||c=='X'?0:1]+=(c=='x'||c=='y'?1:-1);
            int det=ex[0][0]*ex[1][1]-ex[0][1]*ex[1][0];
            if(det!=1&&det!=-1) throw std::runtime_error("nonunimodular state");
            auto test=[&](const std::string &a,const std::string &b) {
                if(a.size()+b.size()<=cap) {
                    ++edges;
                    if(!members.count(canonical(a,b))) throw std::runtime_error("set is not closed under an allowed neighbor");
                }
            };
            for(unsigned i=0;i<2;++i) {
                unsigned j=1-i;
                std::array<std::string,2> recipient={r[i],inverse(r[i])},donor={r[j],inverse(r[j])};
                for(const auto &a:recipient) for(const auto &b:donor) test(reduce(a+b),r[j]);
                for(char g:std::string("xXyY")) test(reduce(std::string(1,g)+r[i]+inverse_letter(g)),r[j]);
            }
            if(++checked%1000000==0) std::cerr<<"closure states checked="<<checked<<'\n';
        }
        std::cout<<"{\"closed\":true,\"start_present\":true,\"n\":"<<n<<",\"cap\":"<<cap
                 <<",\"states_checked\":"<<checked<<",\"allowed_neighbor_checks\":"<<edges
                 <<",\"minimum_total_length\":"<<minimum<<",\"energy_counts\":{";
        bool first=true;
        for(auto [e,c]:energies){if(!first)std::cout<<',';first=false;std::cout<<'"'<<e<<"\":"<<c;}
        std::cout<<"}}\n";
    } catch(const std::exception &e) {std::cerr<<e.what()<<'\n';return 1;}
}
