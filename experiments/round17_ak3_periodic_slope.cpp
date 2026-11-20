// Find permutation certificates against every primitive of an affine slope.
#define main ac_round14_contacts_cli
#include "round14_ak3_permutation_contacts.cpp"
#undef main

#include <bitset>

namespace {
constexpr int period_bound = 2520; // Every permutation order on up to 10 points divides this.

Permutation evaluate(const std::vector<int>& word, const Marking& marking, int degree) {
    Permutation value{};
    for (int point = 0; point < degree; ++point) value[point] = act(word, marking, point);
    return value;
}

unsigned long long shape(const Permutation& value, int degree) {
    unsigned seen = 0;
    unsigned long long answer = 0;
    for (int start = 0; start < degree; ++start) {
        if (seen & (1U << start)) continue;
        int point = start, length = 0;
        do {
            seen |= 1U << point;
            point = value[point];
            ++length;
        } while (point != start);
        answer += 1ULL << (4 * (length - 1));
    }
    return answer;
}

void slope(const char* fixed, const char* source, const char* a, const char* b, int maximum) {
    const auto donor = program(fixed), receiver = program(source);
    const auto transverse = program(a), axial = program(b);
    std::bitset<period_bound> possible;
    possible.set();
    for (int degree = 2; degree <= maximum; ++degree) {
        Permutation identity{};
        std::iota(identity.begin(), identity.begin() + degree, 0);
        for (const auto& x : cycle_representatives(degree)) {
            Marking marking{x, inverse(x, degree), identity, identity};
            do {
                marking[3] = inverse(marking[2], degree);
                if (!kills(donor, marking, degree)) continue;
                const auto want = cycle_type(receiver, marking, degree);
                const auto initial = evaluate(transverse, marking, degree);
                const auto increment = evaluate(axial, marking, degree);
                auto power = identity;
                std::vector<bool> mask;
                do {
                    Permutation target{}, next{};
                    for (int point = 0; point < degree; ++point) {
                        target[point] = initial[power[point]];
                        next[point] = increment[power[point]];
                    }
                    mask.push_back(shape(target, degree) == want);
                    power = next;
                } while (power != identity);
                if (period_bound % mask.size()) throw std::logic_error("permutation period does not divide bound");
                if (std::all_of(mask.begin(), mask.end(), [](bool allowed) { return allowed; })) continue;
                const auto old = possible;
                for (int i = 0; i < period_bound; ++i)
                    if (!mask[i % mask.size()]) possible.reset(i);
                if (possible != old) {
                    print(marking[0], degree);
                    std::cout << '\t';
                    print(marking[2], degree);
                    std::cout << '\t' << possible.count() << '\n';
                }
                if (possible.none()) return;
            } while (std::next_permutation(marking[2].begin(), marking[2].begin() + degree));
        }
    }
}
}

int main(int argc, char** argv) {
    try {
        if (argc != 6) throw std::invalid_argument("usage: periodic-slope donor receiver transverse axial degree");
        const int degree = std::stoi(argv[5]);
        if (degree < 2 || degree > max_points) throw std::invalid_argument("unsupported degree");
        slope(argv[1], argv[2], argv[3], argv[4], degree);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
    return 0;
}
