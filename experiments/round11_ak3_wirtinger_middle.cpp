// Enumerate common middle relators from two finite chart completions.
#define AC_ROUND08_ACM_LIBRARY
#include "round08_ak3_acm.cpp"

#include <set>

namespace wirtinger_middle {
using acm08::Row;

struct Chart {
    std::vector<Row> graph;
    std::vector<size_t> sizes;
    bool allocation_stop = false;
};

Chart completed_chart(const std::string& receiver, const std::string& donor, unsigned depth, size_t cap) {
    acm08::Folding folding(cap);
    folding.add_loop(0, receiver);
    Chart chart{folding.compact(), {}};
    chart.sizes.push_back(chart.graph.size());
    const auto rotations = variants(donor);
    for (unsigned stage = 0; stage < depth; ++stage) {
        const auto vertices = folding.vertices();
        try {
            for (int vertex : vertices)
                for (const auto& rotation : rotations) folding.add_loop(vertex, rotation);
        } catch (const acm08::SizeLimit&) {
            chart.allocation_stop = true;
            break;
        }
        chart.graph = folding.compact();
        chart.sizes.push_back(chart.graph.size());
    }
    return chart;
}

class Product {
    const std::vector<Row>& left;
    const std::vector<Row>& right;
    size_t width;

public:
    static constexpr uint32_t missing = UINT32_MAX;
    std::vector<unsigned char> degree;

    Product(const std::vector<Row>& a, const std::vector<Row>& b) : left(a), right(b), width(b.size()) {
        if (a.size() > missing / width) throw std::length_error("product exceeds 32-bit vertex indices");
        degree.resize(a.size() * b.size());
    }

    uint32_t next(uint32_t vertex, int letter) const {
        const auto a = left[vertex / width][letter], b = right[vertex % width][letter];
        return a < 0 || b < 0 ? missing : uint32_t(a * width + b);
    }

    size_t cyclic_core() {
        std::vector<uint32_t> peel;
        for (uint32_t at = 0; at < degree.size(); ++at) {
            for (int letter = 0; letter < 4; ++letter)
                degree[at] += next(at, letter) != missing;
            if (degree[at] == 1) peel.push_back(at);
        }
        for (size_t index = 0; index < peel.size(); ++index) {
            const auto at = peel[index];
            if (!degree[at]) continue;
            degree[at] = 0;
            for (int letter = 0; letter < 4; ++letter) {
                const auto end = next(at, letter);
                if (end != missing && degree[end] && --degree[end] == 1) peel.push_back(end);
            }
        }
        return std::count_if(degree.begin(), degree.end(), [](unsigned char value) { return value != 0; });
    }
};

struct Search {
    const Product& graph;
    std::array<int, 4> weight;
    size_t limit;
    uint64_t budget;
    std::string word;
    uint64_t visited = 0;
    std::set<std::string> words;

    void cycle(uint32_t base, uint32_t at, int last, int exponent) {
        if (visited == budget) return;
        ++visited;
        if (!word.empty() && base == at && std::abs(exponent) == 1 &&
            word.front() != invchar(word.back())) words.insert(round01::canonical_reduced(word));
        if (word.size() == limit) return;
        for (int letter = 0; letter < 4; ++letter) {
            if (last >= 0 && letter == (last ^ 1)) continue;
            const auto end = graph.next(at, letter);
            if (end == Product::missing || end < base || !graph.degree[end]) continue;
            word.push_back(acm08::letters[letter]);
            cycle(base, end, letter, exponent + weight[letter]);
            word.pop_back();
        }
    }
};

void print_chart(const char* name, const Chart& chart) {
    std::cout << '"' << name << "\":{\"graph_sizes\":[";
    for (size_t i = 0; i < chart.sizes.size(); ++i) std::cout << (i ? "," : "") << chart.sizes[i];
    std::cout << "],\"allocation_stop\":" << (chart.allocation_stop ? "true" : "false") << '}';
}
}  // namespace wirtinger_middle

int main(int argc, char** argv) {
    try {
        using namespace wirtinger_middle;
        if (argc != 8) throw std::invalid_argument(
            "usage: middle common wrong corrected depth allocation_cap maximum_length visit_budget");
        const std::string common = argv[1], wrong = argv[2], corrected = argv[3];
        for (const auto* row : {&common, &wrong, &corrected})
            if (row->empty() || cyclic(*row) != *row) throw std::invalid_argument("noncyclic relator");
        const auto abel = acm08::abel(wrong);
        if (abel != acm08::abel(corrected) || std::abs(acm08::determinant(acm08::abel(common), abel)) != 1)
            throw std::invalid_argument("donor exponents must agree and give unimodular input pairs");
        const auto depth = std::stoul(argv[4]), cap = std::stoul(argv[5]);
        const auto maximum = std::stoul(argv[6]);
        const auto budget = std::stoull(argv[7]);
        const auto first = completed_chart(common, wrong, depth, cap);
        const auto second = completed_chart(common, corrected, depth, cap);
        Product graph(first.graph, second.graph);
        const auto core = graph.cyclic_core();
        Search search{graph, {abel.second, -abel.second, -abel.first, abel.first}, maximum, budget, ""};
        for (uint32_t at = 0; at < graph.degree.size() && search.visited < budget; ++at)
            if (graph.degree[at]) search.cycle(at, at, -1, 0);
        std::cout << '{';
        print_chart("before", first);
        std::cout << ',';
        print_chart("after", second);
        std::cout << ",\"product_vertices\":" << graph.degree.size() << ",\"cyclic_core_vertices\":" << core
                  << ",\"word_length_limit\":" << maximum << ",\"visited_prefixes\":" << search.visited
                  << ",\"complete\":" << (search.visited < budget ? "true" : "false") << ",\"common_middles\":";
        acm08::strings(std::cout, {search.words.begin(), search.words.end()});
        std::cout << "}\n";
    } catch (const acm08::SizeLimit&) {
        std::cerr << "allocation limit does not fit the initial receiver\n";
        return 1;
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
