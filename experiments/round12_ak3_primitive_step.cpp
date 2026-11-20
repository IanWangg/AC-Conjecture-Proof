// Detect an ordinary one-product primitive at any resulting cyclic length.
#define AC_ROUND05_ORBITS_LIBRARY
#include "round05_ak3_orbits.cpp"

#include <numeric>
#include <optional>
#include <sstream>

namespace primitive_step {
using orbit_search::primitive;
using std::string;
using std::string_view;

char invert(char letter) {
    return letter >= 'a' ? letter - ('a' - 'A') : letter + ('a' - 'A');
}

string inverse(string_view word) {
    string output;
    output.reserve(word.size());
    for (auto it = word.rbegin(); it != word.rend(); ++it) output.push_back(invert(*it));
    return output;
}

string trim_cycle(string_view word) {
    while (word.size() > 1 && word.front() == invert(word.back())) {
        word.remove_prefix(1);
        word.remove_suffix(1);
    }
    return string(word);
}

struct Word {
    string text;
    string doubled;
    int x = 0, y = 0;
    explicit Word(string text) : text(std::move(text)), doubled(this->text + this->text) {
        if (this->text.empty()) throw std::runtime_error("empty source coordinate");
        for (size_t i = 0; i < this->text.size(); ++i) {
            const auto next = this->text[i];
            if (next == invert(this->text[(i + 1) % this->text.size()]))
                throw std::runtime_error("source coordinate is not cyclically reduced");
            switch (next) {
                case 'x': ++x; break;
                case 'X': --x; break;
                case 'y': ++y; break;
                case 'Y': --y; break;
                default: throw std::runtime_error("source coordinate outside rank two");
            }
        }
    }
    size_t size() const { return text.size(); }
    string_view arc(size_t first, size_t count) const {
        return string_view(doubled).substr(first, count);
    }
};

struct Hit {
    string receiver_rotation;
    string donor_rotation;
    string primitive_word;
};

bool allowed(string_view letters, char x, char y) {
    return std::all_of(letters.begin(), letters.end(), [=](char c) { return c == x || c == y; });
}

std::optional<Hit> from_orientation(const Word& a, const Word& b) {
    const int x = a.x + b.x, y = a.y + b.y;
    if (std::gcd(x, y) != 1) return {};
    const size_t required = std::abs(x) + std::abs(y);
    const size_t removed = (a.size() + b.size() - required) / 2;
    const char sign_x = x > 0 ? 'x' : x < 0 ? 'X' : '\0';
    const char sign_y = y > 0 ? 'y' : y < 0 ? 'Y' : '\0';
    if (removed >= std::min(a.size(), b.size())) {
        const bool swap = a.size() > b.size();
        const Word& short_word = swap ? b : a;
        const Word& long_word = swap ? a : b;
        for (size_t first = 0; first < short_word.size(); ++first) {
            const auto rotation = short_word.arc(first, short_word.size());
            const string block = inverse(rotation);
            for (size_t at = long_word.doubled.find(block); at < long_word.size();
                 at = long_word.doubled.find(block, at + 1)) {
                const auto tail = long_word.arc(at + block.size(), long_word.size() - block.size());
                const auto reduced = trim_cycle(tail);
                if (reduced.size() != required || !primitive(reduced)) continue;
                const auto other = long_word.arc(at, long_word.size());
                return swap ? Hit{string(other), string(rotation), reduced}
                            : Hit{string(rotation), string(other), reduced};
            }
        }
        return {};
    }
    for (size_t first = 0; first < a.size(); ++first) {
        const string_view tail_a = a.arc(first + removed, a.size() - removed);
        if (!allowed(tail_a, sign_x, sign_y)) continue;
        const string block = inverse(a.arc(first, removed));
        for (size_t at = b.doubled.find(block); at < b.size(); at = b.doubled.find(block, at + 1)) {
            const string_view tail_b = b.arc(at + removed, b.size() - removed);
            if (!allowed(tail_b, sign_x, sign_y)) continue;
            string candidate(tail_a);
            candidate += tail_b;
            if (primitive(candidate))
                return Hit{string(a.arc((first + removed) % a.size(), a.size())),
                           string(b.arc(at, b.size())), candidate};
        }
    }
    return {};
}

bool scan(const string& row, std::ostream& output) {
    const auto split = row.find('\t');
    if (split == string::npos || row.find('\t', split + 1) != string::npos)
        throw std::runtime_error("expected two tab-separated coordinates");
    const Word words[2]{Word(row.substr(0, split)), Word(row.substr(split + 1))};
    const Word negative[2]{Word(inverse(words[0].text)), Word(inverse(words[1].text))};
    for (unsigned receiver = 0; receiver < 2; ++receiver) {
        const unsigned donor = 1 - receiver;
        for (const Word* orientation : {&words[donor], &negative[donor]}) {
            const auto hit = from_orientation(words[receiver], *orientation);
            if (!hit) continue;
            output << "{\"source\":[\"" << words[0].text << "\",\"" << words[1].text
                   << "\"],\"receiver_index\":" << receiver
                   << ",\"receiver_rotation\":\"" << hit->receiver_rotation
                   << "\",\"donor_rotation\":\"" << hit->donor_rotation
                   << "\",\"primitive\":\"" << hit->primitive_word << "\"}";
            return true;
        }
    }
    return false;
}

using Record = std::array<orbit_search::Code, 4>;

bool scan_record(const Record& record, std::ostream& output) {
    const auto& [a, b, p, q] = record;
    if (!a || !b || !p || !q) throw std::runtime_error("invalid boundary record");
    using orbit_search::word;
    std::ostringstream hit;
    if (!scan(word(a) + '\t' + word(b), hit)) return false;
    output << "{\"anchor\":[\"" << word(p) << "\",\"" << word(q)
           << "\"],\"last_edge\":" << hit.str() << '}';
    return true;
}

int run(const char* path, unsigned workers, bool boundary) {
    if (!workers) throw std::runtime_error("need a positive worker count");
    std::ifstream input(path, std::ios::binary);
    if (!input) throw std::runtime_error("cannot open the signed orbit catalogue");
    constexpr size_t batch_size = 262144;
    std::vector<string> batch(batch_size);
    std::vector<Record> records(boundary ? batch_size : 0);
    uint64_t rows_checked = 0;
    string hit;
    for (;;) {
        size_t count = 0;
        if (boundary) {
            input.read(reinterpret_cast<char*>(records.data()), records.size() * sizeof(Record));
            if (input.gcount() % sizeof(Record)) throw std::runtime_error("truncated boundary record");
            count = input.gcount() / sizeof(Record);
        } else {
            while (count < batch.size() && std::getline(input, batch[count])) ++count;
        }
        if (!count) break;
        std::vector<std::future<std::pair<size_t, string>>> tasks;
        std::atomic<size_t> cursor(0);
        constexpr size_t chunk = 1024;
        for (unsigned worker = 0; worker < workers; ++worker) {
            tasks.push_back(std::async(std::launch::async, [&] {
                size_t checked = 0;
                std::ostringstream result;
                for (;;) {
                    const size_t start = cursor.fetch_add(chunk, std::memory_order_relaxed);
                    if (start >= count) break;
                    for (size_t index = start; index < std::min(start + chunk, count); ++index) {
                        ++checked;
                        if (boundary ? scan_record(records[index], result) : scan(batch[index], result))
                            return std::make_pair(checked, result.str());
                    }
                }
                return std::make_pair(checked, string{});
            }));
        }
        for (auto& task : tasks) {
            const auto [checked, candidate] = task.get();
            rows_checked += checked;
            if (!candidate.empty() && (hit.empty() || candidate < hit)) hit = candidate;
        }
        if (!(rows_checked % (batch_size * 32)))
            std::cerr << "checked " << rows_checked << " source rows\n";
        if (!hit.empty()) break;
    }
    if (input.bad() || !rows_checked) throw std::runtime_error("empty or unreadable catalogue");
    std::cout << "{\n  \"rows_checked\":" << rows_checked
              << ",\n  \"complete\":" << (hit.empty() ? "true" : "false")
              << ",\n  \"hit\":" << (hit.empty() ? "null" : hit) << "\n}\n";
    return 0;
}
}  // namespace primitive_step

int main(int argc, char** argv) {
    try {
        const bool boundary = argc == 4 && std::string_view(argv[3]) == "--boundary";
        if (argc != 3 && !boundary)
            throw std::runtime_error("usage: primitive-step source workers [--boundary]");
        return primitive_step::run(argv[1], std::stoul(argv[2]), boundary);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
