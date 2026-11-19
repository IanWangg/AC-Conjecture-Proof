#ifndef AC_ROUND06_AK3_WIDE_PAIR_HPP
#define AC_ROUND06_AK3_WIDE_PAIR_HPP

#include <algorithm>
#include <array>
#include <cstddef>
#include <cstdint>
#include <utility>

namespace ak3_wide {
using Code = uint64_t;
using Pair = std::pair<Code, Code>;
using Orbit = std::array<Code, 8>;

inline Pair unordered_pair(Code a, Code b) {
    if (a > b) std::swap(a, b);
    return {a, b};
}

inline Pair least_image(const Orbit& a, const Orbit& b) {
    Pair result = unordered_pair(a[0], b[0]);
    for (unsigned i = 1; i < a.size(); ++i)
        result = std::min(result, unordered_pair(a[i], b[i]));
    return result;
}

struct Hash {
    std::size_t operator()(const Pair& pair) const {
        Code mixed = pair.first + 0x9e3779b97f4a7c15ULL;
        mixed = (mixed ^ (mixed >> 30)) * 0xbf58476d1ce4e5b9ULL;
        mixed = (mixed ^ (mixed >> 27)) * 0x94d049bb133111ebULL;
        return (mixed ^ (mixed >> 31)) ^ pair.second;
    }
};
}  // namespace ak3_wide
#endif
