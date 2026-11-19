// Fast generation of the full cyclic AC component with the positive bridge menu.
#define main reference_cyclic_component_main
#include "cyclic_component.cpp"
#undef main

#include <optional>
#include <stdexcept>
#include <string_view>
#include <unordered_set>

namespace round01 {

size_t least_rotation(std::string_view word) {
    const size_t size = word.size();
    const std::string doubled = std::string(word) + std::string(word);
    size_t first = 0, second = 1, offset = 0;
    while (first < size && second < size && offset < size) {
        const char a = doubled[first + offset], b = doubled[second + offset];
        if (a == b) {
            ++offset;
            continue;
        }
        if (a > b) {
            first += offset + 1;
            if (first == second) ++first;
        } else {
            second += offset + 1;
            if (first == second) ++second;
        }
        offset = 0;
    }
    return std::min(first, second);
}

std::string canonical_reduced(const std::string& word) {
    if (word.empty()) return word;
    const auto opposite = inverse(word);
    const auto first = least_rotation(word);
    const auto second = least_rotation(opposite);
    return std::min(word.substr(first) + word.substr(0, first),
                    opposite.substr(second) + opposite.substr(0, second));
}

// Both inputs are already cyclically reduced. Before considering rotations,
// delete exactly the cancellations at the two seams or the surviving fragment.
std::optional<std::string> cyclic_product(std::string_view a, std::string_view b,
                                          size_t length_limit) {
    while (!a.empty() && !b.empty() && a.back() == invchar(b.front())) {
        a.remove_suffix(1);
        b.remove_prefix(1);
    }
    while (!a.empty() && !b.empty() && a.front() == invchar(b.back())) {
        a.remove_prefix(1);
        b.remove_suffix(1);
    }
    auto trim_survivor = [](std::string_view& word) {
        while (word.size() > 1 && word.front() == invchar(word.back())) {
            word.remove_prefix(1);
            word.remove_suffix(1);
        }
    };
    if (a.empty()) trim_survivor(b);
    if (b.empty()) trim_survivor(a);
    if (a.size() + b.size() > length_limit) return std::nullopt;
    return canonical_reduced(std::string(a) + std::string(b));
}

void check_product() {
    const auto reduced = bridges(5);
    for (const auto& a : reduced) {
        if (cyclic(a) != a) continue;
        for (const auto& b : reduced) {
            if (cyclic(b) != b) continue;
            const auto reference = canonical(a + b);
            if (cyclic_product(a, b, 10) != reference ||
                (!reference.empty() && cyclic_product(a, b, reference.size() - 1)))
                throw std::logic_error("seam reduction control failed");
        }
    }
}

int run(int cap, const char* catalogue_path, const char* result_path) {
    if (cap < 13) throw std::runtime_error("cap must include AK(3)");
    check_product();
    const P initial = canonpair(canonical("xxxYYYY"), canonical("xyxYXY"));
    std::vector<P> states{initial};
    std::unordered_set<std::string> seen{key(initial)};
    std::unordered_map<std::string, std::vector<std::string>> rotation_cache;
    std::map<int, std::vector<std::pair<std::string, std::string>>> bridge_cache;
    uint64_t candidates = 0, admitted = 0;
    for (size_t at = 0; at < states.size(); ++at) {
        const auto state = states[at];
        const std::string coordinates[2] = {state.first, state.second};
        for (const auto& word : coordinates)
            if (!rotation_cache.count(word)) rotation_cache.emplace(word, variants(word));
        for (size_t receiver = 0; receiver < 2; ++receiver) {
            const auto& a = coordinates[receiver];
            const auto& b = coordinates[1 - receiver];
            const int max_bridge = std::max(0, (cap - int(a.size()) - 2 * int(b.size())) / 2);
            if (!bridge_cache.count(max_bridge)) {
                auto& tails = bridge_cache[max_bridge];
                for (const auto& tail : bridges(max_bridge))
                    tails.emplace_back(tail, inverse(tail));
            }
            const size_t max_product = cap - b.size();
            for (const auto& u : rotation_cache.at(a))
                for (const auto& v : rotation_cache.at(b))
                    for (const auto& [tail, inverse_tail] : bridge_cache.at(max_bridge)) {
                        ++candidates;
                        auto product = tail.empty() ? cyclic_product(u, v, max_product)
                            : std::optional<std::string>(canonical(u + tail + v + inverse_tail));
                        if (!product || product->size() > max_product) continue;
                        ++admitted;
                        auto next = canonpair(std::move(*product), b);
                        if (seen.insert(key(next)).second) states.push_back(std::move(next));
                    }
        }
    }
    std::sort(states.begin(), states.end());
    std::map<size_t, size_t> histogram;
    size_t min_sum = cap, min_word = cap, min_bridge = 3 * cap + 2;
    std::ofstream catalogue(catalogue_path);
    if (!catalogue) throw std::runtime_error("cannot create catalogue");
    catalogue << '[';
    for (size_t i = 0; i < states.size(); ++i) {
        const auto& [a, b] = states[i];
        const auto energy = a.size() + b.size(), small = std::min(a.size(), b.size());
        ++histogram[energy];
        min_sum = std::min(min_sum, energy);
        min_word = std::min(min_word, small);
        min_bridge = std::min(min_bridge, energy + small + 2);
        if (i) catalogue << ',';
        catalogue << "[\"" << a << "\",\"" << b << "\"]";
    }
    catalogue << "]\n";
    catalogue.close();
    if (!catalogue) throw std::runtime_error("cannot finish catalogue");
    std::ofstream result(result_path);
    if (!result) throw std::runtime_error("cannot create run summary");
    result << "{\n  \"status\": \"PASS\",\n  \"cyclic_cap\": " << cap
           << ",\n  \"full_bridge_menu\": true,\n  \"states\": " << states.size()
           << ",\n  \"rotation_product_candidates\": " << candidates
           << ",\n  \"admitted_neighbors\": " << admitted
           << ",\n  \"minimum_cyclic_sum\": " << min_sum
           << ",\n  \"minimum_cyclic_coordinate\": " << min_word
           << ",\n  \"minimum_disjoint_axes_neighbor_sum\": " << min_bridge
           << ",\n  \"histogram\": {";
    bool first = true;
    for (const auto& [energy, count] : histogram) {
        if (!first) result << ", ";
        first = false;
        result << '"' << energy << "\": " << count;
    }
    result << "}\n}\n";
    if (!result) throw std::runtime_error("cannot finish run summary");
    std::cout << "generated " << states.size() << " states from " << candidates
              << " candidate products\n";
    return 0;
}

}  // namespace round01

int main(int argc, char** argv) {
    if (argc != 4) {
        std::cerr << "usage: round01_ak3_cyclic_component cap catalogue.json result.json\n";
        return 2;
    }
    try {
        return round01::run(std::stoi(argv[1]), argv[2], argv[3]);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
