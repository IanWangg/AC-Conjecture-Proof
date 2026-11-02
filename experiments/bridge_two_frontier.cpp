// Target the newly available distance-two bridge edges at cyclic energy23.
// The word helper logic is shared with Q's scanner, not independent.
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>

int letter(char c){auto at=std::string("xXyY").find(c);if(at==std::string::npos)throw std::runtime_error("bad letter");return int(at);}
char inverse(char c){return "xXyY"[letter(c)^1];}
std::string inv(const std::string&w){std::string s;for(auto i=w.rbegin();i!=w.rend();++i)s+=inverse(*i);return s;}
std::string reduce(const std::string&w){std::string s;for(char c:w){letter(c);if(!s.empty()&&s.back()==inverse(c))s.pop_back();else s+=c;}return s;}
std::vector<std::string> rotations(const std::string&w){std::vector<std::string>r;for(size_t i=0;i<w.size();++i)r.push_back(w.substr(i)+w.substr(0,i));std::sort(r.begin(),r.end());r.erase(std::unique(r.begin(),r.end()),r.end());return r;}

std::string cyclic_word(std::string w){w=reduce(w);size_t a=0,b=w.size();while(b-a>1&&w[a]==inverse(w[b-1])){++a;--b;}return w.substr(a,b-a);}
std::string canonical_word(const std::string&w){auto c=cyclic_word(w);if(c.empty())return c;auto r=rotations(c),s=rotations(inv(c));r.insert(r.end(),s.begin(),s.end());return *std::min_element(r.begin(),r.end());}
std::vector<std::string> signed_rotations(const std::string&w){auto r=rotations(w),s=rotations(inv(w));r.insert(r.end(),s.begin(),s.end());std::sort(r.begin(),r.end());r.erase(std::unique(r.begin(),r.end()),r.end());return r;}
std::string quote(const std::string&s){return "\""+s+"\"";}

int main(int argc,char**argv){try{
    if(argc!=5)throw std::runtime_error("usage: bridge_two_frontier source.tsv frontier.tsv provenance.jsonl results.json");
    std::ifstream source(argv[1]);if(!source)throw std::runtime_error("source missing");
    std::map<std::string,std::string> records;
    uint64_t states=0,eligible=0,candidates=0,admitted=0;
    std::vector<std::string>tails;for(char a:std::string("xXyY"))for(char b:std::string("xXyY"))if(a!=inverse(b))tails.push_back(std::string(1,a)+b);
    std::string line;
    while(std::getline(source,line)){auto tab=line.find('\t');if(tab==std::string::npos)throw std::runtime_error("bad TSV");const std::string words[2]={line.substr(0,tab),line.substr(tab+1)};
        for(int i=0;i<2;++i){int j=1-i;int sum=int(words[i].size()+2*words[j].size());if(sum!=19)continue;++eligible;
            for(const auto&a:signed_rotations(words[i]))for(const auto&b:signed_rotations(words[j]))for(const auto&q:tails){++candidates;auto raw=a+q+b+inv(q),p=canonical_word(raw),d=canonical_word(words[j]);if(p.size()+d.size()!=23)continue;++admitted;auto first=p,second=d;if(first>second)std::swap(first,second);std::string key=first+'\t'+second;
                std::string record="{\"state\":["+quote(first)+","+quote(second)+"],\"source_index\":"+std::to_string(states)+",\"source\":["+quote(words[0])+","+quote(words[1])+"],\"recipient\":"+std::to_string(i)+",\"receiver_rotation\":"+quote(a)+",\"donor_rotation\":"+quote(b)+",\"bridge\":"+quote(q)+",\"cyclic_energy\":23}";
                records.emplace(key,record);
            }
        }
        ++states;
    }
    std::ofstream output(argv[2]),provenance(argv[3]);for(const auto&row:records){output<<row.first<<'\n';provenance<<row.second<<'\n';}
    std::ofstream result(argv[4]);result<<"{\n\"status\":\"COMPLETE_STATED_FRONTIER\",\n\"ordinary_AC_goal_solved\":false,\n\"source_pairs\":"<<states<<",\n\"eligible_oriented_sources\":"<<eligible<<",\n\"signed_rotation_bridge_candidates\":"<<candidates<<",\n\"admitted_energy23_candidates\":"<<admitted<<",\n\"distinct_frontier_states\":"<<records.size()<<",\n\"bridge_length\":2,\n\"target_cyclic_energy\":23\n}\n";
    std::cout<<"frontier "<<records.size()<<" states; "<<candidates<<" candidates; "<<eligible<<" eligible source recipients\n";
}catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}}
