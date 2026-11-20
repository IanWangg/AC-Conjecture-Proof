// Expand shared donors into independently conjugated spherical boundary words.
#define AC_ROUND19_THREE_PRODUCTS_LIBRARY
#include "round19_ak3_three_products.cpp"

#include <mutex>

namespace {
using Expansion = std::vector<int>;

void append(Expansion& result, const Expansion& factors, int sign) {
    if (sign > 0) result.insert(result.end(), factors.begin(), factors.end());
    else for (auto it = factors.rbegin(); it != factors.rend(); ++it) result.push_back(-*it);
}

struct Case {
    int receiver;
    std::array<int, 4> signs;
    std::array<int, 4> multiplicities;
    std::pair<int, int> slope;
    Words boundary;
};

std::vector<Case> cases(const std::array<string, 2>& source, const string& mode,
                        uint64_t& sign_histories) {
    std::vector<Case> output;
    for (int first_receiver : {0, 1}) {
        const int first_donor = 1 - first_receiver;
        std::set<std::pair<std::array<int, 4>, std::pair<int, int>>> seen;
        for (unsigned mask = 0; mask < 16; ++mask) {
            std::array<int, 4> signs;
            for (size_t i = 0; i < signs.size(); ++i) signs[i] = (mask & (1u << i)) ? 1 : -1;
            const std::array<int, 4> receiver{
                first_receiver,
                mode[1] == 'A' ? first_receiver : first_donor,
                mode[2] == 'A' ? first_receiver : first_donor,
                mode[2] == 'A' ? first_receiver : first_donor};
            std::array<Expansion, 2> rows{{{1}, {2}}};
            for (size_t i = 0; i < signs.size(); ++i) {
                append(rows[receiver[i]], rows[1 - receiver[i]], signs[i]);
            }
            ++sign_histories;

            const auto& factors = rows[receiver.back()];
            std::pair<int, int> slope{0, 0};
            std::array<int, 4> multiplicities{};
            Words words;
            for (int factor : factors) {
                const int index = std::abs(factor) - 1;
                const auto [x, y] = vector(source[index]);
                const int sign = factor > 0 ? 1 : -1;
                ++multiplicities[2 * index + (factor < 0)];
                slope.first += sign * x;
                slope.second += sign * y;
                words.push_back(oriented(source[index], sign));
            }
            if (!seen.emplace(multiplicities, slope).second) continue;
            words.push_back(inverse(primitive(slope.first, slope.second)));
            output.push_back({first_receiver, signs, multiplicities, slope, std::move(words)});
        }
    }
    return output;
}

template <class Values>
void integer_array(const Values& values) {
    std::cout << '[';
    for (size_t i = 0; i < values.size(); ++i) {
        if (i) std::cout << ',';
        std::cout << values[i];
    }
    std::cout << ']';
}

struct Scan {
    uint64_t sign_histories = 0;
    size_t completed = 0, witnesses = 0;
    std::vector<Case> menu;
    std::vector<std::pair<Counters, string>> results;
};
} // namespace

int main(int argc, char** argv) {
    try {
        if (argc != 4 && argc != 5)
            throw std::invalid_argument("usage: four-products AAB|ABA|ABB rows.tsv workers [memo-limit]");
        const string mode = argv[1];
        if (mode != "AAB" && mode != "ABA" && mode != "ABB") throw std::invalid_argument("mode");
        std::ifstream input(argv[2]);
        unsigned workers = std::stoul(argv[3]);
        const size_t memo_limit = argc == 5 ? std::stoull(argv[4]) : 250000;
        if (!input || !workers) throw std::invalid_argument("invalid input");
        std::vector<std::array<string, 2>> rows;
        for (string a, b; input >> a;) {
            if (!(input >> b)) throw std::invalid_argument("incomplete source pair");
            rows.push_back({std::move(a), std::move(b)});
        }
        if (input.bad() || rows.empty()) throw std::invalid_argument("missing source catalogue");
        std::vector<Scan> scans(rows.size());
        std::vector<std::pair<size_t, size_t>> tasks;
        for (size_t i = 0; i < rows.size(); ++i) {
            const auto [x, y] = vector(rows[i][0]);
            const auto [u, v] = vector(rows[i][1]);
            if (std::abs(x * v - y * u) != 1) throw std::invalid_argument("non-unimodular input");
            auto& scan = scans[i];
            scan.menu = cases(rows[i], mode, scan.sign_histories);
            scan.results.resize(scan.menu.size());
            for (size_t j = 0; j < scan.menu.size(); ++j) tasks.emplace_back(i, j);
        }
        std::atomic<size_t> cursor{0};
        std::mutex progress_mutex;
        std::vector<std::future<void>> pool;
        for (unsigned i = 0; i < workers; ++i) pool.push_back(std::async(std::launch::async, [&] {
            for (size_t task; (task = cursor++) < tasks.size();) {
                const auto [row, index] = tasks[task];
                auto& scan = scans[row];
                auto& [count, hit] = scan.results[index];
                // Bound memo lifetime to one equation without limiting depth or words.
                Equation equation(count, memo_limit, true);
                hit = equation.solve(scan.menu[index].boundary);
                std::lock_guard<std::mutex> lock(progress_mutex);
                if (!hit.empty()) ++scan.witnesses;
                if (++scan.completed == scan.menu.size())
                    std::cerr << mode << " row " << row + 1 << " complete, "
                              << scan.completed << " cases, " << scan.witnesses << " hits\n";
            }
        }));
        for (auto& task : pool) task.get();

        std::cout << "{\"mode\":\"" << mode << "\",\"rows\":[\n";
        for (size_t i = 0; i < scans.size(); ++i) {
            if (i) std::cout << ",\n";
            const auto& scan = scans[i];
            Counters count;
            for (const auto& result : scan.results) {
                count.contractions += result.first.contractions;
                count.memo_hits += result.first.memo_hits;
                count.terminal += result.first.terminal;
            }
            std::cout << "{\"source\":" << json_array({rows[i][0], rows[i][1]})
                      << ",\"sign_histories\":" << scan.sign_histories
                      << ",\"equations\":" << scan.menu.size() << ",\"contractions\":" << count.contractions
                      << ",\"cached_negative\":" << count.memo_hits << ",\"terminal\":" << count.terminal
                      << ",\"hits\":[";
            size_t emitted = 0;
            for (size_t k = 0; k < scan.results.size(); ++k) {
                const auto& hit = scan.results[k].second;
                if (hit.empty()) continue;
                if (emitted++) std::cout << ',';
                const auto& candidate = scan.menu[k];
                std::cout << "{\"first_receiver\":" << candidate.receiver << ",\"signs\":";
                integer_array(candidate.signs);
                std::cout << ",\"multiplicities\":";
                integer_array(candidate.multiplicities);
                std::cout << ",\"slope\":[" << candidate.slope.first << ',' << candidate.slope.second
                          << "],\"boundary\":" << json_array(candidate.boundary)
                          << ",\"equation\":" << hit << '}';
            }
            std::cout << "]}";
        }
        std::cout << "\n]}\n";
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
