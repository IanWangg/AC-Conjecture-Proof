// Literal inverse-letter ribbon pairing audits the rooted contraction search.
#define AC_ROUND19_PAIRING_LIBRARY
#include "round19_ak3_three_products_controls.cpp"

int main() {
    std::mt19937 random(2104);
    std::cout << '[';
    for (size_t width : {7, 8, 9}) {
        unsigned seen = 0, yes = 0;
        while (seen < 3000) {
            Words words(width);
            int x = 0, y = 0;
            size_t total = 0;
            for (auto& word : words) {
                word = random_cycle(random, 1 + random() % 4);
                const auto [a, b] = vector(word);
                x += a;
                y += b;
                total += word.size();
            }
            if (x || y || total > 20) continue;
            const bool truth = planar(words);
            Counters counts;
            if (truth != !Equation(counts, 250000, true).solve(words).empty())
                throw std::logic_error("rooted pairing disagreement");
            ++seen;
            yes += truth;
        }
        // Every conjugate of [x,y] has the same central coordinate in the
        // free class-two quotient, so all of these products are nontrivial.
        Counters central_counts;
        if (!Equation(central_counts, 250000, true).solve(Words(width, "xyXY")).empty())
            throw std::logic_error("nonzero central coordinate accepted");
        if (width != 7) std::cout << ',';
        std::cout << "{\"boundaries\":" << width << ",\"positive\":" << yes
                  << ",\"negative\":" << seen - yes << ",\"central_negative\":true}";
    }
    std::cout << "]\n";
}
