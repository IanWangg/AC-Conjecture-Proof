// Constructive quotient-conjugacy search with unweighted coset completion.
#define AC_ROUND05_ORBITS_LIBRARY
#include "round05_ak3_orbits.cpp"

namespace acm08 {

using Row = std::array<int, 4>;
constexpr std::string_view letters = "xXyY";

struct SizeLimit {};

class Folding {
    std::vector<int> parent;
    std::vector<int> size;
    std::vector<Row> arcs;
    size_t cap;

public:
    explicit Folding(size_t limit) : cap(limit) { new_vertex(); }

    int new_vertex() {
        if (parent.size() >= cap) throw SizeLimit{};
        int index = int(parent.size());
        parent.push_back(index);
        size.push_back(1);
        arcs.push_back({-1, -1, -1, -1});
        return index;
    }

    int find(int at) {
        int root = at;
        while (parent[root] != root) root = parent[root];
        while (parent[at] != at) {
            int upper = parent[at];
            parent[at] = root;
            at = upper;
        }
        return root;
    }

    void merge(int first, int second) {
        std::vector<std::pair<int, int>> pending{{first, second}};
        while (!pending.empty()) {
            auto [a, b] = pending.back();
            pending.pop_back();
            a = find(a);
            b = find(b);
            if (a == b) continue;
            if (size[a] < size[b]) std::swap(a, b);
            parent[b] = a;
            size[a] += size[b];
            for (int c = 0; c < 4; ++c) {
                if (arcs[b][c] < 0) continue;
                if (arcs[a][c] < 0) arcs[a][c] = arcs[b][c];
                else pending.emplace_back(arcs[a][c], arcs[b][c]);
            }
        }
    }

    void add_arc(int a, int c, int b) {
        for (int sign = 0; sign < 2; ++sign) {
            const int start = find(sign ? b : a), finish = find(sign ? a : b);
            const int edge = c ^ sign;
            if (arcs[start][edge] < 0) arcs[start][edge] = finish;
            else merge(arcs[start][edge], finish);
        }
    }

    void add_loop(int root, const std::string& word) {
        int at = root;
        for (size_t k = 0; k < word.size(); ++k) {
            const int c = int(letters.find(word[k]));
            const int start = find(at);
            int end = arcs[start][c];
            if (k + 1 == word.size()) {
                add_arc(start, c, root);
                return;
            }
            if (end < 0) {
                end = new_vertex();
                add_arc(start, c, end);
            }
            at = end;
        }
    }

    std::vector<int> vertices() {
        std::vector<int> result{find(0)};
        std::vector<bool> seen(parent.size());
        seen[result[0]] = true;
        for (size_t i = 0; i < result.size(); ++i)
            for (const int target : arcs[result[i]]) {
                if (target < 0) continue;
                const int next = find(target);
                if (!seen[next]) {
                    seen[next] = true;
                    result.push_back(next);
                }
            }
        return result;
    }

    std::vector<Row> compact() {
        const auto active = vertices();
        std::vector<int> index(parent.size(), -1);
        for (size_t i = 0; i < active.size(); ++i) index[active[i]] = int(i);
        std::vector<Row> compact;
        for (int at : active) {
            Row row{};
            for (int c = 0; c < 4; ++c)
                row[c] = arcs[at][c] < 0 ? -1 : index[find(arcs[at][c])];
            compact.push_back(row);
        }
        for (size_t v = 0; v < compact.size(); ++v)
            for (int c = 0; c < 4; ++c)
                if (compact[v][c] >= 0 && compact[compact[v][c]][c ^ 1] != int(v))
                    throw std::logic_error("folded inverse transition inconsistent");
        return compact;
    }
};

using Abel = std::pair<int, int>;

Abel abel(std::string_view word) {
    Abel result{};
    for (char c : word) {
        if (c == 'x') ++result.first;
        else if (c == 'X') --result.first;
        else if (c == 'y') ++result.second;
        else if (c == 'Y') --result.second;
    }
    return result;
}

int determinant(Abel a, Abel b) { return a.first * b.second - a.second * b.first; }

std::string euclidean_word(int x, int y) {
    unsigned a = unsigned(std::abs(x)), b = unsigned(std::abs(y));
    if (std::gcd(a, b) != 1) throw std::logic_error("nonprimitive slope");
    std::vector<bool> replace_y;
    while (a && b && a != b) {
        replace_y.push_back(a > b);
        if (a > b) a -= b;
        else b -= a;
    }
    std::string model = !a ? "y" : !b ? "x" : "xy";
    for (auto it = replace_y.rbegin(); it != replace_y.rend(); ++it) {
        std::string next;
        for (char c : model) {
            if (c == (*it ? 'y' : 'x')) next += "xy";
            else next += c;
        }
        model.swap(next);
    }
    for (auto& c : model)
        if ((c == 'x' && x < 0) || (c == 'y' && y < 0)) c = invchar(c);
    return model;
}

int follow(const std::vector<Row>& graph, int at, std::string_view word) {
    for (char c : word) {
        at = graph[at][letters.find(c)];
        if (at < 0) break;
    }
    return at;
}

bool present(const std::vector<Row>& graph, const std::string& word) {
    for (size_t v = 0; v < graph.size(); ++v)
        if (follow(graph, int(v), word) == int(v)) return true;
    return false;
}

std::pair<std::string, std::string> positive_basis(Abel a, Abel b) {
    if (a.first >= b.first && a.second >= b.second) {
        auto [u, v] = positive_basis({a.first - b.first, a.second - b.second}, b);
        return {u + v, v};
    }
    if (b.first >= a.first && b.second >= a.second) {
        auto [u, v] = positive_basis(a, {b.first - a.first, b.second - a.second});
        return {u, u + v};
    }
    return a.first > b.first ? std::make_pair(std::string("x"), std::string("y"))
                             : std::make_pair(std::string("y"), std::string("x"));
}

struct Tail {
    int start;
    std::string initial, period;
};

Tail make_tail(Abel a, Abel b) {
    const bool flip_x = b.first < 0 || (!b.first && a.first < 0);
    const bool flip_y = b.second < 0 || (!b.second && a.second < 0);
    if (flip_x) { a.first *= -1; b.first *= -1; }
    if (flip_y) { a.second *= -1; b.second *= -1; }
    int start = 0;
    if (a.first < 0) start = std::max(start, (-a.first + b.first - 1) / b.first);
    if (a.second < 0) start = std::max(start, (-a.second + b.second - 1) / b.second);
    auto [initial, period] = positive_basis({a.first + start*b.first, a.second + start*b.second}, b);
    for (auto* word : {&initial, &period})
        for (auto& c : *word)
            if ((c == 'x' && flip_x) || (c == 'y' && flip_y)) c = invchar(c);
    return {start, initial, period};
}

// A word action in a folded inverse graph is a partial injection. Its
// components are paths and cycles, so the power test has a finite exact scan.
std::string tail_witness(const std::vector<Row>& graph, const Tail& tail) {
    const int count = int(graph.size());
    std::vector<int> next(count), previous(count, -1), component(count, -1), position(count);
    for (int at = 0; at < count; ++at) {
        next[at] = follow(graph, at, tail.period);
        if (next[at] >= 0) {
            if (previous[next[at]] != -1) throw std::logic_error("graph action is not injective");
            previous[next[at]] = at;
        }
    }
    std::vector<int> cycle_size;
    auto trace = [&](int first, bool cycle) {
        int at = first, length = 0;
        while (at >= 0 && component[at] < 0) {
            component[at] = int(cycle_size.size());
            position[at] = length++;
            at = next[at];
        }
        cycle_size.push_back(cycle ? length : 0);
    };
    for (int at = 0; at < count; ++at) if (previous[at] < 0) trace(at, false);
    for (int at = 0; at < count; ++at) if (component[at] < 0) trace(at, true);
    int best = count;
    for (int end = 0; end < count; ++end) {
        const int start = follow(graph, end, tail.initial);
        if (start < 0 || component[start] != component[end]) continue;
        int distance = position[end] - position[start];
        if (distance < 0 && cycle_size[component[end]]) distance += cycle_size[component[end]];
        if (distance >= 0) best = std::min(best, distance);
    }
    if (best == count) return {};
    std::string witness = tail.initial;
    for (int i = 0; i < best; ++i) witness += tail.period;
    if (!present(graph, witness)) throw std::logic_error("primitive power witness is not a loop");
    return witness;
}

struct Harvest {
    std::vector<std::string> words;
    std::vector<std::string> primitive_words;
    std::vector<size_t> graph_sizes;
    unsigned stages = 0;
    uint64_t primitive_slopes = 0;
    unsigned primitive_tails = 0;
    uint64_t return_states = 0;
    bool incomplete_graph = false;
};

// Shortest bounded weight-one returns, with an independent queue for each
// first letter. This harvest is a sampling menu, not conjugacy exhaustion.
void short_returns(const std::vector<Row>& graph, const std::array<int, 4>& weight, int limit,
                   size_t bases, Harvest& output) {
    const int max_weight = std::max(std::abs(weight[0]), std::abs(weight[2]));
    const int center = max_weight * limit;
    const int range = 2 * center + 1;
    struct Trace {
        int at, value, previous, depth;
        int letter;
    };
    std::unordered_set<std::string> found;
    const size_t count = std::min(graph.size(), bases);
    for (size_t base_index = 0; base_index < count; ++base_index) {
        const int base = int(base_index * graph.size() / count);
        for (int first = 0; first < 4; ++first) {
            const int start = graph[base][first];
            if (start < 0) continue;
            auto key = [&](int vertex, int value, int last) {
                return (uint64_t(vertex) * range + unsigned(value + center)) * 4 + unsigned(last);
            };
            std::vector<Trace> queue{{start, weight[first], -1, 1, first}};
            std::unordered_set<uint64_t> seen{key(start, weight[first], first)};
            int finish = -1;
            for (size_t i = 0; i < queue.size(); ++i) {
                const auto entry = queue[i];
                if (entry.at == base && entry.value == 1 && (entry.letter ^ 1) != first) {
                    finish = int(i);
                    break;
                }
                if (entry.depth == limit) continue;
                for (int c = 0; c < 4; ++c) {
                    if (c == (entry.letter ^ 1)) continue;
                    const int at = graph[entry.at][c];
                    if (at < 0) continue;
                    const int value = entry.value + weight[c];
                    if (std::abs(1 - value) > (limit - entry.depth - 1) * max_weight) continue;
                    if (!seen.insert(key(at, value, c)).second) continue;
                    queue.push_back({at, value, int(i), entry.depth + 1, c});
                }
            }
            output.return_states += queue.size();
            if (finish < 0) continue;
            std::string word;
            for (int i = finish; i >= 0; i = queue[i].previous) word += letters[queue[i].letter];
            std::reverse(word.begin(), word.end());
            found.insert(round01::canonical_reduced(word));
        }
    }
    output.words.insert(output.words.end(), found.begin(), found.end());
    std::sort(output.words.begin(), output.words.end(), [](const auto& a, const auto& b) {
        return std::make_pair(a.size(), a) < std::make_pair(b.size(), b);
    });
    output.words.erase(std::unique(output.words.begin(), output.words.end()), output.words.end());
}

Harvest scan(const std::string& receiver, const std::string& donor, unsigned depth, size_t cap,
             int primitive_limit, int loop_limit, size_t bases) {
    const Abel r = abel(receiver), d = abel(donor);
    const int det = determinant(r, d);
    if (std::abs(det) != 1) throw std::invalid_argument("rows must have a unimodular exponent matrix");
    const std::array<int, 4> weight{det*d.second, -det*d.second, -det*d.first, det*d.first};
    const int k_limit = (primitive_limit + std::abs(r.first) + std::abs(r.second))
                        / (std::abs(d.first) + std::abs(d.second));
    std::vector<std::string> primitive_candidates;
    for (int k = -k_limit; k <= k_limit; ++k) {
        const Abel slope{r.first + k*d.first, r.second + k*d.second};
        if (std::abs(slope.first) + std::abs(slope.second) <= primitive_limit)
            primitive_candidates.push_back(euclidean_word(slope.first, slope.second));
    }
    Folding folding(cap);
    folding.add_loop(0, receiver);
    std::vector<Row> graph = folding.compact();
    Harvest result;
    result.graph_sizes.push_back(graph.size());
    const auto rotations = variants(donor);
    for (unsigned stage = 1; stage <= depth; ++stage) {
        const auto active = folding.vertices();
        try {
            for (int v : active)
                for (const auto& word : rotations) folding.add_loop(v, word);
        } catch (const SizeLimit&) {
            result.incomplete_graph = true;
            break;
        }
        graph = folding.compact();
        result.graph_sizes.push_back(graph.size());
        result.stages = stage;
    }
    if (primitive_limit == 0) {
        const auto positive = make_tail(r, d);
        const auto negative = make_tail(r, {-d.first, -d.second});
        result.primitive_tails = 2;
        for (int k = 1 - negative.start; k < positive.start; ++k)
            primitive_candidates.push_back(euclidean_word(r.first + k*d.first, r.second + k*d.second));
        for (const auto* tail : {&positive, &negative}) {
            auto witness = tail_witness(graph, *tail);
            if (!witness.empty()) result.primitive_words.push_back(round01::canonical_reduced(witness));
        }
    }
    result.primitive_slopes = primitive_candidates.size();
    for (const auto& candidate : primitive_candidates)
        if (present(graph, candidate)) result.primitive_words.push_back(round01::canonical_reduced(candidate));
    std::sort(result.primitive_words.begin(), result.primitive_words.end());
    result.primitive_words.erase(std::unique(result.primitive_words.begin(), result.primitive_words.end()),
                                 result.primitive_words.end());
    result.words = result.primitive_words;
    if (loop_limit > 0 && bases) short_returns(graph, weight, loop_limit, bases, result);
    return result;
}

void strings(std::ostream& out, const std::vector<std::string>& values) {
    out << '[';
    for (size_t i = 0; i < values.size(); ++i)
        out << (i ? ",\"" : "\"") << values[i] << '"';
    out << ']';
}

void emit(std::ostream& out, const Harvest& result) {
    out << "{\"stages\":" << result.stages << ",\"graph_sizes\":[";
    for (size_t i = 0; i < result.graph_sizes.size(); ++i)
        out << (i ? "," : "") << result.graph_sizes[i];
    out << "],\"primitive_slopes\":" << result.primitive_slopes
        << ",\"primitive_tails\":" << result.primitive_tails
        << ",\"return_states\":" << result.return_states
        << ",\"incomplete_graph\":" << (result.incomplete_graph ? "true" : "false")
        << ",\"words\":";
    strings(out, result.words);
    out << ",\"primitive_words\":";
    strings(out, result.primitive_words);
    out << "}\n";
}

} // namespace acm08

int main(int argc, char** argv) {
    try {
        if (argc != 8) throw std::invalid_argument(
            "usage: acm receiver donor depth allocation_cap primitive_length_or_zero loop_length bases");
        const std::string receiver = cyclic(argv[1]), donor = cyclic(argv[2]);
        if (receiver.empty() || donor.empty()) throw std::invalid_argument("empty input");
        const auto result = acm08::scan(receiver, donor, std::stoul(argv[3]), std::stoull(argv[4]),
                                       std::stoi(argv[5]), std::stoi(argv[6]), std::stoull(argv[7]));
        acm08::emit(std::cout, result);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
