// Independent stack-reduction replay of the strict stable JSONL ledger.
#include <algorithm>
#include <fstream>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

char opposite(char letter) { return letter ^ 32; }

std::string inverse(std::string word) {
    std::reverse(word.begin(), word.end());
    for (auto& letter : word) letter = opposite(letter);
    return word;
}

std::string reduced(const std::string& word) {
    std::string stack;
    stack.reserve(word.size());
    for (char letter : word) {
        if (!stack.empty() && stack.back() == opposite(letter)) stack.pop_back();
        else stack.push_back(letter);
    }
    return stack;
}

size_t cyclic_size(const std::string& word) {
    size_t a = 0, b = word.size();
    while (b > a + 1 && word[a] == opposite(word[b - 1])) { ++a; --b; }
    return b - a;
}

std::string conjugated(const std::string& word, char letter) {
    if (word.empty()) return word;
    size_t begin = 0, end = word.size();
    if (word.front() == opposite(letter)) ++begin;
    if (end > begin && word[end - 1] == letter) --end;
    std::string result;
    result.reserve(end - begin + 2);
    if (begin == 0) result += letter;
    result.append(word, begin, end - begin);
    if (end == word.size()) result += opposite(letter);
    return result;
}

std::string field(const std::string& object, const std::string& name) {
    const std::string pattern = "\"" + name + "\":";
    const size_t at = object.find(pattern);
    if (at == std::string::npos) throw std::runtime_error("missing field " + name);
    const size_t begin = at + pattern.size();
    if (object.at(begin) == '"') {
        const size_t end = object.find('"', begin + 1);
        if (end == std::string::npos) throw std::runtime_error("unterminated string");
        return object.substr(begin + 1, end - begin - 1);
    }
    const size_t end = object.find_first_of(",}", begin);
    if (end == std::string::npos) throw std::runtime_error("unterminated value");
    return object.substr(begin, end - begin);
}

std::vector<std::string> pair(const std::string& object, const std::string& label) {
    const std::string prefix = "{\"" + label + "\":[\"";
    if (object.rfind(prefix, 0) != 0) throw std::runtime_error("invalid pair line");
    const auto delimiter = object.find("\",\"", prefix.size());
    if (delimiter == std::string::npos || object.size() < delimiter + 6
        || object.substr(object.size() - 3) != "\"]}")
        throw std::runtime_error("invalid pair array");
    return {object.substr(prefix.size(), delimiter - prefix.size()),
            object.substr(delimiter + 3, object.size() - delimiter - 6)};
}

size_t row_slot(const std::string& operation, const std::string& key, size_t rows) {
    const auto text = field(operation, key);
    if (text.size() != 1 || text[0] < '0' || size_t(text[0] - '0') >= rows)
        throw std::runtime_error("invalid row slot");
    return size_t(text[0] - '0');
}

void replay(const char* path) {
    std::ifstream file(path);
    std::string line;
    if (!file || !std::getline(file, line)) throw std::runtime_error("missing ledger");
    std::vector<std::string> rows = pair(line, "start");
    if (rows != std::vector<std::string>{"xxxYYYY", "xyxYXY"}) throw std::runtime_error("wrong starting tuple");
    std::vector<size_t> cyclic_lengths{7, 6};
    std::set<char> mark{'x', 'y'};
    size_t moves = 0, rank_peak = 2, raw_peak = 13, cyclic_peak = 13;
    bool done = false;
    while (std::getline(file, line)) {
        if (line.rfind("{\"target\":", 0) == 0) {
            if (rows != pair(line, "target")) throw std::runtime_error("target words do not match");
            done = true;
            break;
        }
        const auto op = field(line, "op");
        if (op == "stabilize") {
            const auto g = field(line, "generator");
            if (g.size() != 1 || g[0] < 'a' || g[0] > 'z' || !mark.insert(g[0]).second)
                throw std::runtime_error("invalid stabilization");
            rows.push_back(g);
            cyclic_lengths.push_back(1);
        } else {
            const auto i = row_slot(line, "i", rows.size());
            if (op == "destabilize") {
                const auto g = field(line, "generator");
                if (g.size() != 1 || rows[i] != g || !mark.erase(g[0]))
                    throw std::runtime_error("missing singleton at deletion");
                for (size_t j = 0; j < rows.size(); ++j)
                    if (i != j && rows[j].find_first_of(g + opposite(g[0])) != std::string::npos)
                        throw std::runtime_error("deleted generator is not isolated");
                rows.erase(rows.begin() + i);
                cyclic_lengths.erase(cyclic_lengths.begin() + i);
            } else if (op == "invert") {
                rows[i] = inverse(rows[i]);
            } else if (op == "multiply") {
                const auto j = row_slot(line, "j", rows.size());
                if (i == j) throw std::runtime_error("self product");
                rows[i] = reduced(rows[i] + rows[j]);
                cyclic_lengths[i] = cyclic_size(rows[i]);
            } else if (op == "conjugate") {
                const auto g = field(line, "g");
                if (g.size() != 1 || !mark.count(g[0] | 32)) throw std::runtime_error("invalid conjugator");
                rows[i] = conjugated(rows[i], g[0]);
            } else throw std::runtime_error("invalid instruction");
        }
        if (rows.size() != mark.size()) throw std::runtime_error("rank does not match row count");
        ++moves;
        rank_peak = std::max(rank_peak, rows.size());
        size_t raw = 0, cyclic = 0;
        for (size_t i = 0; i < rows.size(); ++i) {
            raw += rows[i].size();
            cyclic += cyclic_lengths[i];
        }
        raw_peak = std::max(raw_peak, raw);
        cyclic_peak = std::max(cyclic_peak, cyclic);
    }
    if (!done || std::getline(file, line)) throw std::runtime_error("ledger has missing or extra trailer");
    std::cout << "{\n  \"moves\": " << moves << ",\n  \"rank_peak\": " << rank_peak
              << ",\n  \"raw_peak\": " << raw_peak << ",\n  \"cyclic_peak\": " << cyclic_peak
              << ",\n  \"final_words\": [\"" << rows[0] << "\", \"" << rows[1] << "\"]\n}\n";
}

}

int main(int argc, char** argv) {
    try {
        if (argc != 2) throw std::runtime_error("usage: strict_verify ledger.jsonl");
        replay(argv[1]);
        return 0;
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
