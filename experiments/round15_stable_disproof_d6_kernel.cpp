// Certify the central kernel from degree six to degree five by a Schreier census.
#define AC_ROUND08_MAGNUS_NATIVE_LIBRARY
#include "round07_magnus_native.cpp"

int main() {
    using free_distance::Id;
    magnus_native::Elements<6> high;
    magnus_native::Elements<5> low;
    const Id x = high.intern("x"), y = high.intern("y"), one = high.intern("");
    std::vector<Id> representatives(low.size(), free_distance::missing);
    for (const char* word : {"", "x", "X", "y", "Y"}) {
        const Id lift = high.intern(word);
        representatives[high.project(lift, low)] = lift;
    }
    std::array<uint64_t, 64> leading{};
    std::size_t schreier_edges = 0, nonidentity = 0;
    for (Id position = 0; position < low.size(); ++position) {
        for (const Id letter : {x, y}) {
            ++schreier_edges;
            const Id moved = high.product(representatives[position], letter);
            const Id image = high.project(moved, low);
            if (image == representatives.size()) {
                representatives.push_back(moved);
                continue;
            }
            if (image > representatives.size()) throw std::runtime_error("missing lower representative");
            const Id kernel_element = high.product(moved, high.inverse(representatives[image]));
            if (kernel_element == one) continue;
            ++nonidentity;
            // Degree six occupies the 64 bits starting at index 63.
            const auto hex = high.describe(kernel_element);
            uint64_t coefficients = (std::stoull(hex.substr(0, 16), nullptr, 16) << 1) |
                                    (std::stoull(hex.substr(16), nullptr, 16) >> 63);
            if (high.project(kernel_element, low) != low.intern("") || coefficients == 0)
                throw std::runtime_error("invalid central element");
            while (coefficients != 0) {
                const unsigned pivot = __builtin_ctzll(coefficients);
                if (leading[pivot] == 0) {
                    leading[pivot] = coefficients;
                    break;
                }
                coefficients ^= leading[pivot];
            }
        }
    }

    const auto dimension = std::count_if(leading.begin(), leading.end(), [](uint64_t row) { return row != 0; });
    if (low.size() != 524288 || schreier_edges != 1048576 || nonidentity != 507220 || dimension != 11)
        throw std::runtime_error("unexpected central kernel census");
    std::cout << "{\"lower_degree\":5,\"upper_degree\":6,\"lower_elements\":" << low.size()
              << ",\"positive_schreier_edges\":" << schreier_edges << ",\"nonidentity_schreier_images\":" << nonidentity
              << ",\"central_kernel_dimension\":" << dimension << ",\"central_basis\":[";
    bool first = true;
    for (unsigned pivot = 0; pivot < leading.size(); ++pivot) if (leading[pivot] != 0) {
        if (!first) std::cout << ',';
        first = false;
        std::cout << "{\"degree_six_coordinate\":" << pivot << ",\"coefficients_hex\":\"" << std::hex << leading[pivot]
                  << std::dec << "\"}";
    }
    std::cout << "]}\n";
}
