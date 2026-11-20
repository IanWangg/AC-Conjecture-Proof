// Enumerate every degree-five Magnus element and measure the degree-four fibers.
#define AC_ROUND08_MAGNUS_NATIVE_LIBRARY
#include "round07_magnus_native.cpp"
#include <map>

int main() {
    using free_distance::Id;
    magnus_native::Elements<5> high;
    magnus_native::Elements<4> low;
    magnus_native::Elements<1> linear;
    const Id x = high.intern("x"), y = high.intern("y");
    // Right multiplication by the two positive generators suffices in this finite group.
    for (Id current = 0; current < high.size(); ++current) {
        high.product(current, x);
        high.product(current, y);
    }
    std::vector<unsigned> fiber_size;
    for (Id current = 0; current < high.size(); ++current) {
        const Id image = high.project(current, low);
        if (image >= fiber_size.size()) fiber_size.resize(low.size());
        ++fiber_size[image];
    }
    std::map<unsigned, std::size_t> histogram;
    std::array<std::size_t, 4> parity_sizes{};
    for (Id image = 0; image < low.size(); ++image) {
        ++histogram[fiber_size[image]];
        ++parity_sizes.at(low.project(image, linear));
    }
    const Id zero = linear.intern("");
    std::size_t independent_pairs = 0;
    for (Id a = 0; a < linear.size(); ++a)
        for (Id b = a + 1; b < linear.size(); ++b)
            if (a != zero && b != zero) independent_pairs += parity_sizes[a] * parity_sizes[b];

    if (high.size() != 524288 || low.size() != 8192 || histogram.size() != 1 || histogram.count(64) != 1 ||
        independent_pairs != 12582912)
        throw std::runtime_error("unexpected group or fiber census");
    const auto marked_pairs = independent_pairs * 64 * 64;
    std::cout << "{\"degree_five_elements\":" << high.size() << ",\"degree_four_elements\":" << low.size()
              << ",\"fiber_size\":64,\"degree_four_independent_unordered_pairs\":" << independent_pairs
              << ",\"degree_five_aligned_pairs\":" << marked_pairs << ",\"one_bit_chart_bytes\":" << marked_pairs / 8
              << ",\"first_arrival_nibble_bytes_per_side\":" << marked_pairs / 2 << "}\n";
}
