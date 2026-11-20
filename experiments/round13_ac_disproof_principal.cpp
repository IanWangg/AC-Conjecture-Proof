// Independently enumerate all folded images of a based core by congruence propagation.
#include <algorithm>
#include <array>
#include <cstddef>
#include <iostream>
#include <numeric>
#include <set>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using Graph = std::vector<std::array<int, 4>>;

static int representative(std::vector<int>& parents, int at) {
    if (at < 0) {
        return at;
    }
    while (parents[at] != at) {
        parents[at] = parents[parents[at]];
        at = parents[at];
    }
    return at;
}

static Graph quotient(Graph transitions, int first, int second) {
    std::vector<int> parents(transitions.size());
    std::iota(parents.begin(), parents.end(), 0);
    std::vector<std::pair<int, int>> equalities{{first, second}};
    for (std::size_t index = 0; index < equalities.size(); ++index) {
        int a = representative(parents, equalities[index].first);
        int b = representative(parents, equalities[index].second);
        if (a == b) {
            continue;
        }
        parents[b] = a;
        for (int letter = 0; letter < 4; ++letter) {
            int& left = transitions[a][letter];
            const int right = transitions[b][letter];
            if (left < 0) {
                left = right;
            } else if (right >= 0) {
                equalities.emplace_back(left, right);
            }
        }
    }

    std::vector<int> numbers(transitions.size(), -1);
    std::vector<int> order{representative(parents, 0)};
    numbers[order.front()] = 0;
    Graph result;
    for (std::size_t index = 0; index < order.size(); ++index) {
        std::array<int, 4> outgoing{};
        for (int letter = 0; letter < 4; ++letter) {
            const int next = representative(parents, transitions[order[index]][letter]);
            if (next >= 0 && numbers[next] < 0) {
                numbers[next] = static_cast<int>(order.size());
                order.push_back(next);
            }
            outgoing[letter] = next < 0 ? -1 : numbers[next];
        }
        result.push_back(outgoing);
    }
    for (std::size_t at = 0; at < result.size(); ++at) {
        for (int letter = 0; letter < 4; ++letter) {
            const int end = result[at][letter];
            if (end >= 0 && result[end][letter ^ 1] != static_cast<int>(at)) {
                throw std::runtime_error("quotient lost an inverse arc");
            }
        }
    }
    return result;
}

static int rank(const Graph& graph) {
    int arcs = 0;
    for (const auto& outgoing : graph) {
        arcs += std::count_if(outgoing.begin(), outgoing.end(), [](int end) { return end >= 0; });
    }
    return arcs / 2 - static_cast<int>(graph.size()) + 1;
}

int main(int argc, char** argv) {
    const bool rank_increasing = argc == 2 && std::string(argv[1]) == "--rank-increasing";
    if (argc != 1 && !rank_increasing) {
        throw std::runtime_error("usage: principal [--rank-increasing]");
    }
    int vertices;
    if (!(std::cin >> vertices) || vertices <= 0 || vertices > 255) {
        throw std::runtime_error("expected the vertex count before the transition list");
    }
    Graph first(vertices);
    for (auto& outgoing : first) {
        for (auto& end : outgoing) {
            if (!(std::cin >> end) || end < -1 || end >= vertices) {
                throw std::runtime_error("invalid transition");
            }
        }
    }
    if (quotient(first, 0, 0) != first) {
        throw std::runtime_error("expected a canonical connected input core");
    }
    std::set<Graph> images{first};
    std::vector<Graph> pending{first};
    for (std::size_t at = 0; at < pending.size(); ++at) {
        const Graph graph = std::move(pending[at]);
        for (int a = 0; a < static_cast<int>(graph.size()); ++a) {
            for (int b = a + 1; b < static_cast<int>(graph.size()); ++b) {
                auto next = quotient(graph, a, b);
                if ((!rank_increasing || rank(next) == rank(graph) + 1)
                    && images.insert(next).second) {
                    pending.push_back(std::move(next));
                }
            }
        }
    }
    for (const auto& graph : images) {
        bool first_entry = true;
        for (const auto& outgoing : graph) {
            for (const int end : outgoing) {
                if (!first_entry) {
                    std::cout << ' ';
                }
                std::cout << end;
                first_entry = false;
            }
        }
        std::cout << '\n';
    }
}
