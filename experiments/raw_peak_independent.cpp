// Independent cross-check: the ORIGINAL ordered, oriented raw-word graph.
// No quotient is used in this BFS. Only the final state count is projected.
#include <algorithm>
#include <array>
#include <chrono>
#include <cctype>
#include <iostream>
#include <map>
#include <queue>
#include <string>
#include <unordered_set>

char inverse_letter(char c) { return std::islower(c) ? std::toupper(c) : std::tolower(c); }
std::string inverse_word(const std::string &w) {
    std::string answer;
    for (auto at = w.rbegin(); at != w.rend(); ++at) answer += inverse_letter(*at);
    return answer;
}
std::string freely_reduce(const std::string &w) {
    std::string answer;
    for (char c : w) {
        if (!answer.empty() && answer.back() == inverse_letter(c)) answer.pop_back();
        else answer += c;
    }
    return answer;
}
std::string projection(std::string a, std::string b) {
    a = std::min(a, inverse_word(a));
    b = std::min(b, inverse_word(b));
    if (a > b) std::swap(a, b);
    return a + "|" + b;
}

int main(int argc, char **argv) {
    int cap = argc > 1 ? std::stoi(argv[1]) : 18;
    std::unordered_set<std::string> visited;
    std::queue<std::string> pending;
    std::string start = "xxxYYYY|xyxYXY";
    visited.insert(start);
    pending.push(start);
    int minimum = 13;
    bool target = false;
    while (!pending.empty()) {
        std::string key = pending.front(); pending.pop();
        auto split = key.find('|');
        std::array<std::string,2> r{key.substr(0,split),key.substr(split+1)};
        minimum = std::min(minimum, int(r[0].size()+r[1].size()));
        if (r[0]=="x" && r[1]=="y") target=true;
        for (int i=0; i<2; ++i) {
            int j=1-i;
            std::array<std::string,6> values{
                inverse_word(r[i]), freely_reduce(r[i]+r[j]),
                freely_reduce("x"+r[i]+"X"), freely_reduce("X"+r[i]+"x"),
                freely_reduce("y"+r[i]+"Y"), freely_reduce("Y"+r[i]+"y")};
            for (const auto &v : values) {
                if (v.size()+r[j].size()>static_cast<size_t>(cap)) continue;
                std::string next = i==0 ? v+"|"+r[1] : r[0]+"|"+v;
                if (visited.insert(next).second) pending.push(next);
            }
        }
    }
    std::unordered_set<std::string> projected;
    for (const auto &key : visited) {
        auto split=key.find('|');
        projected.insert(projection(key.substr(0,split),key.substr(split+1)));
    }
    std::map<int,int> energies;
    for (const auto &key : projected) ++energies[int(key.size())-1];
    std::cout << "{\"cap\":" << cap << ",\"raw_ordered_oriented_states\":" << visited.size()
              << ",\"projected_states\":" << projected.size()
              << ",\"minimum_total_length\":" << minimum
              << ",\"target_reached\":" << (target?"true":"false")
              << ",\"energy_counts\":{";
    bool first=true;
    for (const auto &[energy,count] : energies) {
        if (!first) std::cout << ',';
        first=false;
        std::cout << '\"' << energy << "\":" << count;
    }
    std::cout << "}}\n";
}
