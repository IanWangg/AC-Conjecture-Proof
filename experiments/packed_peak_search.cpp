// Exact raw-word quotient graph. State packing only; no cyclic normalization.
// Quotient by relator inversion/permutation; all recipient/donor signs emitted.
// Alphabet x,X,y,Y maps to 0,1,2,3; inverse letter toggles bit zero.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <filesystem>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

struct Word { uint64_t bits=0; unsigned len=0; };
bool operator==(Word a, Word b) { return a.bits==b.bits && a.len==b.len; }
void push(Word &w, unsigned c) {
    if (w.len && ((w.bits >> (2*(w.len-1))) & 3)==(c^1)) {
        --w.len;
        w.bits &= w.len ? ((uint64_t(1) << (2*w.len))-1) : 0;
    } else {
        if (w.len>=30) throw std::runtime_error("word packing overflow");
        w.bits |= uint64_t(c) << (2*w.len++);
    }
}
Word inverse(Word w) {
    Word out;
    for (unsigned i=w.len; i; --i) push(out, ((w.bits >> (2*(i-1)))&3)^1);
    return out;
}
Word multiply(Word a, Word b) {
    for (unsigned i=0; i<b.len; ++i) push(a, (b.bits>>(2*i))&3);
    return a;
}
Word conjugate(Word a, unsigned g) {
    Word out;
    push(out,g);
    out=multiply(out,a);
    push(out,g^1);
    return out;
}
Word parse(const std::string &s) {
    Word out;
    for (char c:s) { auto at=std::string("xXyY").find(c); if(at==std::string::npos) throw std::runtime_error("bad word"); push(out,unsigned(at)); }
    return out;
}
std::string text(Word w) {
    std::string s;
    for(unsigned i=0;i<w.len;++i) s += "xXyY"[(w.bits>>(2*i))&3];
    return s;
}
uint64_t mask(unsigned n) { return n ? (uint64_t(1)<<(2*n))-1 : 0; }
uint64_t canonical(Word a, Word b) {
    a.bits=std::min(a.bits,inverse(a).bits);
    b.bits=std::min(b.bits,inverse(b).bits);
    if(a.len>b.len || (a.len==b.len && a.bits>b.bits)) std::swap(a,b);
    if(a.len+b.len>27) throw std::runtime_error("state packing overflow");
    return a.bits | (b.bits<<(2*a.len)) | (uint64_t(a.len)<<54) | (uint64_t(b.len)<<59);
}
std::array<Word,2> unpack(uint64_t key) {
    unsigned a=(key>>54)&31, b=(key>>59)&31;
    return {Word{key&mask(a),a},Word{(key>>(2*a))&mask(b),b}};
}
uint64_t mix(uint64_t z) {
    z+=0x9e3779b97f4a7c15ULL;
    z=(z^(z>>30))*0xbf58476d1ce4e5b9ULL;
    z=(z^(z>>27))*0x94d049bb133111ebULL;
    return z^(z>>31);
}
struct FlatSet {
    std::vector<uint64_t> table;
    size_t count=0;
    FlatSet():table(size_t(1)<<18,0){}
    void place(uint64_t key) {
        size_t at=mix(key)&(table.size()-1);
        while(table[at]) at=(at+1)&(table.size()-1);
        table[at]=key;
    }
    bool insert(uint64_t key) {
        if(!key) throw std::runtime_error("empty tuple unsupported");
        if((count+1)*10>table.size()*7) {
            std::vector<uint64_t> old;
            old.swap(table);
            table.resize(old.size()*2,0);
            for(uint64_t item:old) if(item) place(item);
        }
        size_t at=mix(key)&(table.size()-1);
        while(table[at]) { if(table[at]==key) return false; at=(at+1)&(table.size()-1); }
        table[at]=key; ++count; return true;
    }
};
template<class T> void write(std::ofstream &f,const T &v){ f.write(reinterpret_cast<const char*>(&v),sizeof(v)); }
template<class T> void read(std::ifstream &f,T &v){ f.read(reinterpret_cast<char*>(&v),sizeof(v)); }

int main(int argc,char **argv) {
    try {
        unsigned n=argc>1?std::stoul(argv[1]):3;
        unsigned cap=argc>2?std::stoul(argv[2]):19;
        uint64_t budget=argc>3?std::stoull(argv[3]):10000000;
        std::string checkpoint=argc>4?argv[4]:"";
        bool resume=argc>5 && std::string(argv[5])=="resume";
        if(n<1 || cap<2*n+7 || cap>25) throw std::runtime_error("require n>=1 and 2n+7<=cap<=25");
        FlatSet seen;
        std::vector<uint64_t> queue;
        std::vector<uint32_t> parents;
        std::vector<uint8_t> edges;
        uint64_t processed=0;
        if(resume) {
            std::ifstream f(checkpoint,std::ios::binary);
            uint64_t magic,count; unsigned oldn,oldcap;
            read(f,magic); read(f,oldn); read(f,oldcap); read(f,processed); read(f,count);
            if(!f || magic!=0x41435041434b3031ULL || oldn!=n || oldcap!=cap || count>100000000 || processed>count) throw std::runtime_error("invalid/incompatible checkpoint");
            queue.resize(count); parents.resize(count); edges.resize(count);
            f.read(reinterpret_cast<char*>(queue.data()),count*sizeof(uint64_t));
            f.read(reinterpret_cast<char*>(parents.data()),count*sizeof(uint32_t));
            f.read(reinterpret_cast<char*>(edges.data()),count);
            if(!f) throw std::runtime_error("truncated checkpoint");
            for(auto key:queue) if(!seen.insert(key)) throw std::runtime_error("duplicate checkpoint state");
        } else {
            uint64_t start=canonical(parse(std::string(n,'x')+std::string(n+1,'Y')),parse("xyxYXY"));
            seen.insert(start); queue.push_back(start); parents.push_back(0); edges.push_back(255);
        }
        if(budget<=queue.size() && processed<queue.size()) throw std::runtime_error("resume budget must exceed saved discovery count");
        auto emit=[&](Word a,Word b,unsigned edge) {
            if(a.len+b.len>cap) return;
            uint64_t key=canonical(a,b);
            if(seen.insert(key)) {
                if(processed>UINT32_MAX) throw std::runtime_error("parent index overflow");
                queue.push_back(key); parents.push_back(uint32_t(processed)); edges.push_back(uint8_t(edge));
            }
        };
        unsigned minimum=2*n+7;
        size_t best=0;
        for(size_t k=0;k<queue.size();++k){ auto r=unpack(queue[k]); if(r[0].len+r[1].len<minimum){minimum=r[0].len+r[1].len;best=k;} }
        uint64_t next_report=((queue.size()/1000000)+1)*1000000;
        bool target=false;
        while(processed<queue.size()) {
            auto pair=unpack(queue[processed]);
            unsigned energy=pair[0].len+pair[1].len;
            if(energy<minimum){minimum=energy;best=processed;}
            if(pair[0].len==1 && pair[1].len==1 && ((pair[0].bits^pair[1].bits)&2)) { target=true; best=processed; break; }
            for(unsigned i=0;i<2;++i) {
                unsigned j=1-i;
                for(unsigned sa=0;sa<2;++sa) for(unsigned sb=0;sb<2;++sb) {
                    Word a=sa?inverse(pair[i]):pair[i], b=sb?inverse(pair[j]):pair[j];
                    Word product=multiply(a,b);
                    if(i==0) emit(product,pair[j],i*4+sa*2+sb);
                    else emit(pair[j],product,i*4+sa*2+sb);
                }
                for(unsigned g=0;g<4;++g) {
                    Word c=conjugate(pair[i],g);
                    if(i==0) emit(c,pair[j],8+i*4+g);
                    else emit(pair[j],c,8+i*4+g);
                }
            }
            ++processed;
            if(queue.size()>=next_report) {std::cerr<<"discovered="<<queue.size()<<" processed="<<processed<<"\n"; next_report+=1000000;}
            if(queue.size()>=budget) break;
        }
        std::array<uint64_t,28> energies{};
        for(auto key:queue) { auto r=unpack(key); ++energies[r[0].len+r[1].len]; }
        if(!checkpoint.empty()) {
            const std::string temporary=checkpoint+".tmp";
            std::ofstream f(temporary,std::ios::binary|std::ios::trunc);
            uint64_t magic=0x41435041434b3031ULL,count=queue.size();
            write(f,magic);write(f,n);write(f,cap);write(f,processed);write(f,count);
            f.write(reinterpret_cast<const char*>(queue.data()),count*sizeof(uint64_t));
            f.write(reinterpret_cast<const char*>(parents.data()),count*sizeof(uint32_t));
            f.write(reinterpret_cast<const char*>(edges.data()),count);
            f.flush();
            if(!f) throw std::runtime_error("checkpoint write failed");
            f.close();
            std::filesystem::rename(temporary,checkpoint);
        }
        std::cout<<"{\"n\":"<<n<<",\"cap\":"<<cap<<",\"complete\":"<<(!target&&processed==queue.size()?"true":"false")
                 <<",\"target_reached\":"<<(target?"true":"false")<<",\"states_discovered\":"<<queue.size()<<",\"states_processed\":"<<processed
                 <<",\"minimum_processed_length\":"<<minimum<<",\"energy_counts\":{";
        bool first=true;
        for(unsigned k=0;k<energies.size();++k) if(energies[k]) {if(!first)std::cout<<',';first=false;std::cout<<'"'<<k<<"\":"<<energies[k];}
        std::cout<<"},\"best_path\":[";
        std::vector<size_t> path;
        for(size_t k=best;;k=parents[k]) {path.push_back(k);if(k==0)break;}
        std::reverse(path.begin(),path.end());
        first=true;
        for(auto k:path) {if(!first)std::cout<<',';first=false;auto r=unpack(queue[k]);std::cout<<"{\"words\":[\""<<text(r[0])<<"\",\""<<text(r[1])<<"\"],\"edge\":"<<unsigned(edges[k])<<'}';}
        std::cout<<"]}\n";
    } catch(const std::exception &e) {std::cerr<<e.what()<<'\n';return 1;}
}
