// Independent check: monomial STRINGS and direct polynomial products.
// It does not use the Python implementation's index-concatenation formula
// or its precomputed affine transformation columns.
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

struct Ring {
    unsigned degree,size;
    std::vector<std::string> monomials;
    std::unordered_map<std::string,unsigned> indices;
    std::vector<std::vector<int>> table;
    std::array<uint64_t,4> letters;
    Ring(unsigned d):degree(d) {
        if(d<1||d>5)throw std::runtime_error("supported degree1..5");
        monomials.push_back("");
        for(unsigned len=1;len<=degree;++len) {
            size_t begin=(size_t(1)<<(len-1))-1,end=(size_t(1)<<len)-1;
            for(size_t k=begin;k<end;++k)for(char c:std::string("ab"))monomials.push_back(monomials[k]+c);
        }
        size=monomials.size();
        for(unsigned i=0;i<size;++i)indices[monomials[i]]=i;
        table.resize(size,std::vector<int>(size,-1));
        for(unsigned i=0;i<size;++i)for(unsigned j=0;j<size;++j) {
            std::string joined=monomials[i]+monomials[j];
            if(joined.size()<=degree)table[i][j]=indices.at(joined);
        }
        letters[0]=1|(uint64_t(1)<<indices.at("a"));
        letters[1]=1|(uint64_t(1)<<indices.at("b"));
        letters[2]=inverse(letters[0]);letters[3]=inverse(letters[1]);
    }
    uint64_t multiply(uint64_t a,uint64_t b) const {
        uint64_t ans=0;
        while(a) {
            unsigned i=__builtin_ctzll(a);a&=a-1;
            uint64_t rest=b;
            while(rest) {
                unsigned j=__builtin_ctzll(rest);rest&=rest-1;
                int k=table[i][j];
                if(k>=0)ans^=uint64_t(1)<<k;
            }
        }
        return ans;
    }
    uint64_t inverse(uint64_t a) const {
        uint64_t v=a^1,power=1,answer=1;
        for(unsigned k=0;k<degree;++k){power=multiply(power,v);answer^=power;}
        if(multiply(a,answer)!=1)throw std::runtime_error("inverse control");
        return answer;
    }
    uint64_t evaluate(const std::string &word) const {
        uint64_t ans=1;
        for(char c:word)ans=multiply(ans,letters.at(std::string("abAB").find(c)));
        return ans;
    }
};

int main(int argc,char **argv) {
    try {
        unsigned degree=argc>1?std::stoul(argv[1]):5;
        Ring r(degree);
        std::array<uint64_t,4> right={r.evaluate("B"),r.evaluate("bA"),r.evaluate("b"),r.evaluate("aB")};
        std::vector<uint64_t> queue={r.evaluate("abbAbA")};
        std::unordered_set<uint64_t> seen={queue[0]};
        for(size_t at=0;at<queue.size();++at) {
            uint64_t w=queue[at];
            for(unsigned i=0;i<4;++i) {
                uint64_t nxt=r.multiply(r.multiply(r.letters[i],w),right[i]);
                if(seen.insert(nxt).second)queue.push_back(nxt);
            }
            if(seen.size()>1000000)throw std::runtime_error("state budget reached; no conclusion");
        }
        uint64_t c=r.evaluate("bA"),power=1;
        unsigned order=0;
        std::vector<unsigned> hits;
        do {
            if(seen.count(power))hits.push_back(order);
            power=r.multiply(power,c);++order;
            if(order>256)throw std::runtime_error("unexpected candidate order");
        } while(power!=1);
        std::cout<<"{\"degree\":"<<degree<<",\"complete_twisted_orbit\":true,\"orbit_states\":"<<seen.size()
                 <<",\"candidate_order\":"<<order<<",\"candidate_k_residues_seen\":[";
        bool first=true;for(unsigned k:hits){if(!first)std::cout<<',';first=false;std::cout<<k;}
        std::cout<<"],\"method\":\"independent monomial-string convolution\"}\n";
    }catch(const std::exception &e){std::cerr<<e.what()<<'\n';return 1;}
}
