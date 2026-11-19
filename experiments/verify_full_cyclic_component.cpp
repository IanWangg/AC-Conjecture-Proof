// Independent closed-set and connectedness audit for a cyclic AC component.
// Does not import or compile the component generator.  The report proves
// completeness of this finite menu for arbitrary conjugating tails.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <future>
#include <iostream>
#include <limits>
#include <map>
#include <queue>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

namespace audit {
using Words = std::pair<std::string,std::string>;

char opposite(char c) {
    switch(c) {
        case 'x': return 'X'; case 'X': return 'x';
        case 'y': return 'Y'; case 'Y': return 'y';
        default: throw std::runtime_error("letter outside x,X,y,Y");
    }
}

std::string reversed_inverse(const std::string& word) {
    std::string result;
    result.reserve(word.size());
    for(auto at=word.rbegin();at!=word.rend();++at) result.push_back(opposite(*at));
    return result;
}

std::string cyclically_reduced(const std::string& input) {
    std::string stack;
    stack.reserve(input.size());
    for(char c:input) {
        opposite(c); // Validate independently of whether a cancellation occurs.
        if(!stack.empty() && stack.back()==opposite(c)) stack.pop_back();
        else stack.push_back(c);
    }
    std::size_t left=0,right=stack.size();
    while(right-left>1 && stack[left]==opposite(stack[right-1])) {++left;--right;}
    return stack.substr(left,right-left);
}

// Booth's minimum cyclic rotation algorithm; independent of the generator's
// enumeration/minimum of all copied rotations.
std::string least_rotation(const std::string& word) {
    if(word.empty()) return word;
    const std::size_t n=word.size();
    const std::string twice=word+word;
    std::size_t i=0,j=1,k=0;
    while(i<n && j<n && k<n) {
        char a=twice[i+k],b=twice[j+k];
        if(a==b) {++k;continue;}
        if(a>b) {i+=k+1;if(i==j)++i;}
        else {j+=k+1;if(i==j)++j;}
        k=0;
    }
    return twice.substr(std::min(i,j),n);
}

std::string class_word(const std::string& word) {
    auto c=cyclically_reduced(word);
    return std::min(least_rotation(c),least_rotation(reversed_inverse(c)));
}

std::string pair_key(std::string a,std::string b) {
    if(a>b) a.swap(b);
    return a+":"+b;
}

std::vector<std::string> signed_rotations(const std::string& word) {
    if(word.empty()) return {""};
    std::vector<std::string> values;
    const auto opposite_word=reversed_inverse(word);
    for(const auto* w : {&word,&opposite_word}) {
        const auto twice=*w+*w;
        for(std::size_t i=0;i<w->size();++i) values.push_back(twice.substr(i,w->size()));
    }
    std::sort(values.begin(),values.end());
    values.erase(std::unique(values.begin(),values.end()),values.end());
    return values;
}

void append_tails(int remaining,std::string& prefix,std::vector<std::string>& out) {
    out.push_back(prefix);
    if(!remaining) return;
    for(char c : std::string("XYxy")) {
        if(!prefix.empty() && prefix.back()==opposite(c)) continue;
        prefix.push_back(c);
        append_tails(remaining-1,prefix,out);
        prefix.pop_back();
    }
}

void self_test() {
    if(class_word("xYyX")!="" || class_word("xyXY")!="XYxy")
        throw std::runtime_error("free/cyclic reduction control failed");
    // Independently compare Booth to exhaustive rotations for every reduced
    // test word through length seven, including periodic words.
    std::string prefix;
    std::vector<std::string> controls;
    append_tails(7,prefix,controls);
    for(const auto& w:controls) {
        auto reduced=cyclically_reduced(w);
        auto rotations=signed_rotations(reduced);
        if(class_word(w)!=rotations.front()) throw std::runtime_error("rotation control failed");
    }
}

int run(const std::string& input,int cap,const std::string& output,int workers) {
    if(workers<1) throw std::runtime_error("workers must be positive");
    self_test();
    const auto started=std::chrono::steady_clock::now();
    std::ifstream source(input);
    if(!source) throw std::runtime_error("cannot open catalogue TSV");
    std::vector<Words> states;
    std::unordered_map<std::string,uint32_t> index;
    std::map<int,uint64_t> histogram;
    int min_sum=std::numeric_limits<int>::max(),min_word=min_sum,min_bridge=min_sum;
    std::string line;
    while(std::getline(source,line)) {
        auto tab=line.find('\t');
        if(tab==std::string::npos || line.find('\t',tab+1)!=std::string::npos)
            throw std::runtime_error("invalid TSV row");
        auto a=line.substr(0,tab),b=line.substr(tab+1);
        if(a.empty() || b.empty() || a>b || class_word(a)!=a || class_word(b)!=b)
            throw std::runtime_error("noncanonical or empty source coordinate");
        int sum=static_cast<int>(a.size()+b.size()),small=static_cast<int>(std::min(a.size(),b.size()));
        if(sum>cap) throw std::runtime_error("state exceeds supplied cyclic cap");
        auto id=static_cast<uint32_t>(states.size());
        if(!index.emplace(pair_key(a,b),id).second) throw std::runtime_error("duplicate source state");
        states.emplace_back(a,b);
        ++histogram[sum];
        min_sum=std::min(min_sum,sum);min_word=std::min(min_word,small);
        min_bridge=std::min(min_bridge,sum+small+2);
    }
    const auto start_key=pair_key(class_word("xxxYYYY"),class_word("xyxYXY"));
    if(!index.count(start_key)) throw std::runtime_error("original AK(3) class missing");
    if(index.count(pair_key(class_word("x"),class_word("y"))))
        throw std::runtime_error("standard basis unexpectedly present");

    std::vector<std::vector<uint32_t>> adjacent(states.size());
    struct Counts {
        uint64_t candidates=0,accepted=0,positive_tail_candidates=0,positive_tail_accepted=0;
        int maximum_tail=0;
    };
    const auto& lookup=index;
    // Workers share the catalogue and write disjoint rows of the adjacency table.
    auto scan=[&](std::size_t begin,std::size_t end) {
        std::unordered_map<std::string,std::vector<std::string>> orientations;
        std::map<int,std::vector<std::pair<std::string,std::string>>> tails;
        Counts counts;
        for(std::size_t state=begin;state<end;++state) {
            const std::string words[2]={states[state].first,states[state].second};
            for(const auto& w:words)
                if(!orientations.count(w)) orientations.emplace(w,signed_rotations(w));
            for(int recipient=0;recipient<2;++recipient) {
                const int donor=1-recipient;
                const int numerator=cap-static_cast<int>(words[recipient].size())
                                       -2*static_cast<int>(words[donor].size());
                const int bound=numerator<0 ? 0 : numerator/2;
                counts.maximum_tail=std::max(counts.maximum_tail,bound);
                if(!tails.count(bound)) {
                    std::vector<std::string> raw;
                    std::string prefix;
                    append_tails(bound,prefix,raw);
                    for(const auto& q:raw) tails[bound].emplace_back(q,reversed_inverse(q));
                }
                for(const auto& a:orientations.at(words[recipient]))
                    for(const auto& b:orientations.at(words[donor]))
                        for(const auto& q:tails.at(bound)) {
                            ++counts.candidates;
                            if(!q.first.empty()) ++counts.positive_tail_candidates;
                            const auto reduced=cyclically_reduced(a+q.first+b+q.second);
                            if(reduced.size()+words[donor].size()>static_cast<std::size_t>(cap)) continue;
                            const auto product=std::min(least_rotation(reduced),
                                                        least_rotation(reversed_inverse(reduced)));
                            ++counts.accepted;
                            if(!q.first.empty()) ++counts.positive_tail_accepted;
                            auto next=lookup.find(pair_key(product,words[donor]));
                            if(next==lookup.end()) {
                                std::cerr<<"missing neighbor from "<<words[0]<<" / "<<words[1]
                                         <<"; recipient="<<recipient<<" tail="<<q.first
                                         <<" product="<<product<<"\n";
                                throw std::runtime_error("catalogue not closed under full finite menu");
                            }
                            adjacent[state].push_back(next->second);
                        }
            }
            auto& neighbors=adjacent[state];
            std::sort(neighbors.begin(),neighbors.end());
            neighbors.erase(std::unique(neighbors.begin(),neighbors.end()),neighbors.end());
        }
        return counts;
    };
    const auto partitions=std::min(static_cast<std::size_t>(workers),states.size());
    const auto policy=partitions==1 ? std::launch::deferred : std::launch::async;
    std::vector<std::future<Counts>> scans;
    for(std::size_t part=0;part<partitions;++part)
        scans.push_back(std::async(policy,scan,states.size()*part/partitions,
                                   states.size()*(part+1)/partitions));
    Counts counts;
    for(auto& scan_result:scans) {
        const auto part=scan_result.get();
        counts.candidates+=part.candidates;
        counts.accepted+=part.accepted;
        counts.positive_tail_candidates+=part.positive_tail_candidates;
        counts.positive_tail_accepted+=part.positive_tail_accepted;
        counts.maximum_tail=std::max(counts.maximum_tail,part.maximum_tail);
    }
    std::vector<bool> reached(states.size(),false);
    std::queue<uint32_t> frontier;
    const auto initial=index.at(start_key);
    reached[initial]=true;frontier.push(initial);
    std::size_t reachable=1;
    while(!frontier.empty()) {
        auto at=frontier.front();frontier.pop();
        for(auto next:adjacent[at]) if(!reached[next]) {
            reached[next]=true;frontier.push(next);++reachable;
        }
    }
    if(reachable!=states.size()) throw std::runtime_error("source contains disconnected states");
    auto elapsed=std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count();
    std::ofstream result(output);
    result<<"{\n  \"status\": \"PASS\",\n  \"ordinary_AC_goal_solved\": false,\n"
          <<"  \"cyclic_cap\": "<<cap<<",\n  \"canonical_states\": "<<states.size()<<",\n"
          <<"  \"minimum_cyclic_sum\": "<<min_sum<<",\n  \"minimum_cyclic_coordinate\": "<<min_word<<",\n"
          <<"  \"minimum_disjoint_axes_neighbor_sum\": "<<min_bridge<<",\n"
          <<"  \"all_menu_candidates_checked\": "<<counts.candidates<<",\n"
          <<"  \"admitted_neighbor_checks\": "<<counts.accepted<<",\n"
          <<"  \"positive_tail_candidates_checked\": "<<counts.positive_tail_candidates<<",\n"
          <<"  \"positive_tail_admitted_checks\": "<<counts.positive_tail_accepted<<",\n"
          <<"  \"maximum_geodesic_bridge_length_needed\": "<<counts.maximum_tail<<",\n"
          <<"  \"all_states_reachable_from_original_AK3\": true,\n"
          <<"  \"closed_under_full_geometric_neighbor_menu\": true,\n"
          <<"  \"independent_free_reduction_and_Booth_canonicalizer\": true,\n"
          <<"  \"minimum_required_cyclic_peak\": "<<cap+1<<",\n"
          <<"  \"seconds\": "<<elapsed<<",\n  \"state_histogram\": {";
    bool first=true;
    for(auto entry:histogram) {if(!first)result<<", ";first=false;result<<"\""<<entry.first<<"\": "<<entry.second;}
    result<<"}\n}\n";
    std::cout<<"PASS "<<states.size()<<" states; "<<counts.candidates<<" menu checks; "
             <<counts.positive_tail_candidates<<" positive-tail checks; "<<elapsed<<" seconds\n";
    return 0;
}
} // namespace audit

int main(int argc,char** argv) {
    try {
        if(argc!=4 && argc!=5)
            throw std::runtime_error("usage: verify_full_cyclic_component catalogue.tsv cap result.json [workers]");
        return audit::run(argv[1],std::stoi(argv[2]),argv[3],argc==5 ? std::stoi(argv[4]) : 1);
    } catch(const std::exception& e) {std::cerr<<"FAIL: "<<e.what()<<"\n";return 1;}
}
