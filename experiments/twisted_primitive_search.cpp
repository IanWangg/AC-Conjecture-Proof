// Direct free-kernel conjugator search in Q=<x,y|XXyxYxxY>.
// Q=F(a,b) semidirect_alpha Z, alpha(a)=b, alpha(b)=aB.
// A positive hit would be a primitive ACM waypoint; failure is bounded only.
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

unsigned Rank=2;
char inv(char c) {switch(c){case 'a':return 'A';case 'A':return 'a';case 'b':return 'B';case 'B':return 'b';case 'c':return 'C';case 'C':return 'c';}throw std::runtime_error("bad letter");}
std::string inverse(const std::string &s) {std::string t;for(auto at=s.rbegin();at!=s.rend();++at)t+=inv(*at);return t;}
std::string reduce(const std::string &s) {
    std::string t;
    for(char c:s){if(!t.empty()&&t.back()==inv(c))t.pop_back();else t+=c;}
    return t;
}
std::string image(char c,bool backwards=false) {
    if(Rank==3){
        if(!backwards){switch(c){case 'a':return "b";case 'A':return "B";case 'b':return "c";case 'B':return "C";case 'c':return "aB";case 'C':return "bA";}}
        else{switch(c){case 'a':return "ca";case 'A':return "AC";case 'b':return "a";case 'B':return "A";case 'c':return "b";case 'C':return "B";}}
    }
    if(!backwards){switch(c){case 'a':return "b";case 'A':return "B";case 'b':return "aB";case 'B':return "bA";}}
    else{switch(c){case 'a':return "ba";case 'A':return "AB";case 'b':return "a";case 'B':return "A";}}
    throw std::runtime_error("invalid kernel letter");
}
std::string alpha(const std::string &s,bool backwards=false) {
    std::string t;for(char c:s)t+=image(c,backwards);return reduce(t);
}
std::string power(std::string base,int exponent) {
    if(exponent<0){base=inverse(base);exponent=-exponent;}
    std::string out;while(exponent--)out+=base;return reduce(out);
}
int main(int argc,char **argv) {
    try {
        unsigned maximum=argc>1?std::stoul(argv[1]):14;
        Rank=argc>2?std::stoul(argv[2]):2;
        if(Rank!=2&&Rank!=3)throw std::runtime_error("rank must be 2 or3");
        std::string fixed=argc>3?argv[3]:"";
        std::string source_override=argc>4?argv[4]:"";
        if(!fixed.empty()&&Rank!=2)throw std::runtime_error("fixed target mode currently requires rank2");
        int fixed_a=0,fixed_b=0;
        for(char c:fixed){fixed_a+=(c=='a')-(c=='A');fixed_b+=(c=='b')-(c=='B');}
        if(maximum>22)throw std::runtime_error("explicit maximum length must be <=22");
        std::string alphabet=Rank==2?"aAbB":"aAbBcC";
        for(char c:alphabet)if(alpha(alpha(std::string(1,c)),true)!=std::string(1,c)||alpha(alpha(std::string(1,c),true))!=std::string(1,c))throw std::runtime_error("inverse automorphism control failed");
        std::string product,v="a";
        for(int k=0;k<=5;++k){if(k>=2)product=reduce(product+v);v=alpha(v);}
        const std::string W=source_override.empty()?(Rank==2?"abbAbA":"bCB"):source_override;
        if(source_override.empty()&&Rank==2&&product!=W)throw std::runtime_error("power-relator kernel identity failed");
        int wa=0,wb=0;for(char c:W){wa+=(c=='a')-(c=='A');wb+=(c=='b')-(c=='B');}
        int da=fixed_a-wa,db=fixed_b-wb;
        int required_a=2*da+db,required_b=da+db;
        if(Rank==3&&alpha(alpha(alpha("a")))!="aB")throw std::runtime_error("rank3 defining relation failed");
        std::vector<uint64_t> nodes(maximum+1,0),tested(maximum+1,0);
        struct Hit {std::string q;int k;};std::vector<Hit> hits;
        std::string q;
        auto visit=[&](auto &&self,const std::string &aq,int aexp,int bexp,int cexp)->void {
            unsigned depth=q.size();++nodes[depth];
            if((Rank==2&&((fixed.empty()&&bexp==-2)||(!fixed.empty()&&aexp==required_a&&bexp==required_b)))||(Rank==3&&aexp==2*bexp+1&&cexp==bexp+1)) {
                ++tested[depth];int k=Rank==2?-aexp-1:bexp;
                if(reduce(q+W+inverse(aq))==(fixed.empty()?power(Rank==2?"bA":"a",k):fixed))hits.push_back({q,k});
            }
            if(depth==maximum)return;
            int minimum=std::abs(bexp+2);
            if(!fixed.empty())minimum=std::abs(aexp-required_a)+std::abs(bexp-required_b);
            if(Rank==3){
                minimum=1000000;int half=(aexp-1)/2;
                for(int k:{half-1,half,half+1,bexp,cexp-1})minimum=std::min(minimum,std::abs(2*k+1-aexp)+std::abs(k-bexp)+std::abs(k+1-cexp));
            }
            if(minimum>int(maximum-depth))return;
            for(char c:alphabet) {
                if(!q.empty()&&q.back()==inv(c))continue;
                q+=c;
                self(self,reduce(aq+image(c)),aexp+(c=='a')-(c=='A'),bexp+(c=='b')-(c=='B'),cexp+(c=='c')-(c=='C'));
                q.pop_back();
            }
        };
        visit(visit,"",0,0,0);
        std::cout<<"{\"fiber_rank\":"<<Rank<<",\"maximum_conjugator_length\":"<<maximum<<",\"source_kernel\":\""<<W<<"\",\"fixed_kernel_target\":\""<<fixed<<"\",\"fixed_required_exponents\":";
        if(fixed.empty())std::cout<<"null";else std::cout<<'['<<required_a<<','<<required_b<<']';
        std::cout<<",\"nodes_by_length\":[";
        bool first=true;for(auto n:nodes){if(!first)std::cout<<',';first=false;std::cout<<n;}
        std::cout<<"],\"candidate_tests_by_length\":[";
        first=true;for(auto n:tested){if(!first)std::cout<<',';first=false;std::cout<<n;}
        std::cout<<"],\"hits\":[";
        first=true;for(auto hit:hits){if(!first)std::cout<<',';first=false;std::cout<<"{\"q\":\""<<hit.q<<'"';if(fixed.empty())std::cout<<",\"k\":"<<hit.k;std::cout<<'}';}
        std::cout<<"],\"scope\":\"bounded exact conjugator search, not a global obstruction\"}\n";
    }catch(const std::exception &e){std::cerr<<e.what()<<'\n';return 1;}
}
