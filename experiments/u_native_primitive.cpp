#include "u_native_primitive.hpp"
#include "u_graph_fold.hpp"
#include <fstream>
#include <iostream>
#include <sstream>

namespace {
std::vector<std::string> split(const std::string&s,char delimiter){std::vector<std::string>out;std::istringstream input(s);std::string item;while(std::getline(input,item,delimiter))out.push_back(item);return out;}
void quoted(std::ostream&o,const std::string&s){o<<'"';for(char c:s){if(c=='"'||c=='\\')o<<'\\';if(c=='\n')o<<"\\n";else if(c=='\t')o<<"\\t";else o<<c;}o<<'"';}
void write(std::ostream&o,const std::string&id,const u_native::Graph&g,const u_native::Result&r,bool certificate){
    o<<"{\"id\":";quoted(o,id);o<<",\"status\":";quoted(o,u_native::status_name(r.status));
    o<<",\"vertices\":"<<g.size()<<",\"pair_states\":"<<r.pair_states<<",\"alphabets\":[";
    bool first=true;for(const auto&a:r.alphabets){if(!first)o<<',';first=false;o<<"{\"alphabet\":";quoted(o,a.alphabet);o<<",\"status\":";quoted(o,u_native::status_name(a.status));o<<",\"discovered\":"<<a.discovered<<",\"processed\":"<<a.processed;
        if(certificate&&a.status==u_native::Status::ABSENT){o<<",\"closed_total_map_pairs\":[";bool first_pair=true;for(const auto&pair:a.closed_pairs){if(!first_pair)o<<',';first_pair=false;o<<'[';bool f=true;for(auto x:pair){if(!f)o<<',';f=false;o<<x;}o<<']';}o<<']';}o<<'}';}o<<']';
    if(r.status==u_native::Status::PRIMITIVE){const auto&w=r.witness;o<<",\"witness\":{\"alphabet\":";quoted(o,w.alphabet);o<<",\"program\":";quoted(o,w.program);o<<",\"component\":"<<w.component<<",\"vertex\":"<<w.vertex<<",\"base_path\":";quoted(o,w.base_path);o<<",\"expanded\":"<<(w.expanded?"true":"false");
        if(w.expanded){o<<",\"cyclic_word\":";quoted(o,w.cyclic_word);o<<",\"based_word\":";quoted(o,w.based_word);}o<<'}';}
    if(certificate){o<<",\"graph\":[";bool f=true;for(const auto&row:g)for(int v:row){if(!f)o<<',';f=false;o<<v;}o<<']';}
    o<<"}\n";
}
}
int main(int argc,char**argv){
    try{
        if(argc<3){std::cerr<<"usage: u_native_primitive input.tsv output.jsonl [budget] [save_certificates=0|1] [stop_positive=0|1]\n";return 2;}
        uint64_t budget=argc>3?std::stoull(argv[3]):100000;bool certificate=argc>4&&std::string(argv[4])=="1",stop=argc>5&&std::string(argv[5])=="1";
        std::ifstream input(argv[1]);if(!input)throw std::runtime_error("missing TSV input");std::ofstream output(argv[2]);if(!output)throw std::runtime_error("cannot create output");
        std::string line;uint64_t total=0,absent=0,positive=0,incomplete=0,map_states=0,maximum=0;
        while(std::getline(input,line)){if(line.empty())continue;auto fields=split(line,'\t');if(fields.size()!=3&&fields.size()!=5)throw std::runtime_error("TSV row needs id,pair and optional expected graph");
            auto graph=u_native::fold_words({fields[1],fields[2]});
            if(fields.size()==5){auto encoded=split(fields[4],',');if(encoded.empty()||encoded.size()%4)throw std::runtime_error("bad expected graph encoding");u_native::Graph expected(encoded.size()/4);
                for(size_t i=0;i<encoded.size();++i)expected[i/4][i%4]=std::stoi(encoded[i]);expected=u_native::rebase_graph(expected,unsigned(std::stoul(fields[3])));if(expected!=graph)throw std::runtime_error("independent refolding disagrees with input graph");}
            auto result=u_native::decide(graph,budget,1000000,certificate);write(output,fields[0],graph,result,certificate);++total;map_states+=result.pair_states;
            for(const auto&a:result.alphabets)maximum=std::max(maximum,a.discovered);
            if(result.status==u_native::Status::ABSENT)++absent;else if(result.status==u_native::Status::PRIMITIVE)++positive;else ++incomplete;
            if(stop&&positive)break;
        }
        std::cout<<"{\"records\":"<<total<<",\"ABSENT\":"<<absent<<",\"PRIMITIVE\":"<<positive<<",\"INCOMPLETE\":"<<incomplete<<",\"map_pair_states\":"<<map_states<<",\"maximum_one_alphabet\":"<<maximum<<",\"ordinary_AC_goal_solved\":false}\n";
    }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}
}
