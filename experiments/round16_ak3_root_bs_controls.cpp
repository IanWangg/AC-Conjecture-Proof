#define AC_ROUND16_ROOT_BS_LIBRARY
#include "round16_ak3_root_bs_scan.cpp"

#include <random>

namespace {
using root_bs::primitive_power;

struct Control {
    std::string word;
    bool exists;
};

void check(const Control& control, const std::string& word, int k, int n) {
    if (primitive_power(word, k, n).has_value() != control.exists)
        throw std::runtime_error("failed root-adjoined control: " + word);
}

std::string random_word(std::mt19937& engine) {
    std::string word;
    for (unsigned i = 0, length = engine() % 24; i < length; ++i)
        word += "xXyY"[engine() % 4];
    return word;
}
}

int main() {
    constexpr unsigned repeats = 128;
    std::mt19937 engine(1603);
    unsigned comparisons = 0;
    for (int k = 2; k <= 5; ++k) {
        const std::string t(k, 'x'), T(k, 'X');
        for (int n = 1; n <= 5; ++n) {
            const auto relator = t + std::string(n, 'y') + T + std::string(n + 1, 'Y');
            std::vector<Control> controls{
                {"x", true},
                {"xyyy", true},
                {"x" + t + "y" + T, true},
                {"x" + T + "Y" + t, true},
                {"xyxyXy", false},
            };
            if (n > 1) controls.push_back({"xy" + t + "y" + T + "Y", false});
            for (const auto& control : controls) {
                check(control, control.word, k, n);
                ++comparisons;
                for (unsigned i = 0; i < repeats; ++i) {
                    const auto c = random_word(engine);
                    auto word = c + control.word + inverse(c);
                    for (unsigned j = 0; j < 3; ++j) {
                        const auto insertion = random_word(engine);
                        const auto piece = j % 2 ? inverse(relator) : relator;
                        word.insert(engine() % (word.size() + 1), insertion + piece + inverse(insertion));
                    }
                    check(control, word, k, n);
                    check(control, inverse(word), k, n);
                    comparisons += 2;
                }
            }
        }
    }
    std::cout << "{\"fixed_seed\":1603,\"comparisons\":" << comparisons << "}\n";
}
