// Generate all unrestricted marked width-eight templates not excluded by the first strict tests.
#define AC_MIXED_EIGHT_LIBRARY
#include "round14_stable_disproof_mixed_eight.cpp"

namespace unrestricted_eight {
using mixed_eight::Id;
using mixed_eight::Kind;
using mixed_eight::State;
using mixed_eight::Set;
using mixed_eight::StrictComparison;

class Search {
    StrictComparison comparison;
    free_distance::WordTable& words = comparison.words;
    const Id one = words.intern("");
    const std::vector<mixed_eight::Move> menu = mixed_eight::instructions();
    std::array<uint64_t, 4> counts{};
    Set residual;

    template <class Visit>
    void active_steps(State current, Visit&& accept) {
        for (const auto move : menu) {
            const Id value = mixed_eight::formal_step(words, current, move);
            if (value == one || value == current[move.recipient]) continue;
            State next = current;
            next[move.recipient] = value;
            if (move.kind == Kind::multiply)
                next[3] ^= ((current[3] >> move.operand) & 1) << move.recipient;
            accept(next);
        }
    }

    void check_terminals(State state) {
        for (unsigned recipient = 0; recipient < 3; ++recipient) {
            const Id removed = state[recipient];
            const auto pair = StrictComparison::pair(state[(recipient + 1) % 3], state[(recipient + 2) % 3]);
            const unsigned exponent = comparison.exponent_coordinates(removed);
            for (unsigned donor = 0; donor < 3; ++donor) {
                if (donor == recipient) continue;
                if ((exponent ^ comparison.exponent_coordinates(state[donor])) & 0x11) continue;
                if (!(((state[3] >> recipient) ^ (state[3] >> donor)) & 1))
                    throw std::runtime_error("equal marked linear rows");
                if (comparison.reached.count(pair)) {
                    counts[0] += 2;
                    continue;
                }
                const unsigned other = 3 - recipient - donor;
                for (const bool negative : {false, true}) {
                    const Id signed_donor = negative ? words.inverse(state[donor]) : state[donor];
                    const Id substituted = negative ? words.inverse(removed) : removed;
                    if (comparison.reached.count(StrictComparison::pair(substituted, state[other]))) {
                        ++counts[1];
                        continue;
                    }
                    if (exponent != comparison.exponent_coordinates(signed_donor)) {
                        ++counts[2];
                        continue;
                    }
                    const Id retained_donor = (state[donor] << 1) | ((state[3] >> donor) & 1);
                    const Id retained_other = (state[other] << 1) | ((state[3] >> other) & 1);
                    const auto retained = StrictComparison::pair(retained_donor, retained_other);
                    residual.insert({removed, signed_donor, retained[0], retained[1]});
                    ++counts[3];
                }
            }
        }
    }

public:
    void run() {
        comparison.radius_seven();
        std::cerr << "pair radius7 " << comparison.reached.size() << '\n';
        const Id a = words.intern("a"), b = words.intern("b");
        Set layer{{a, b, a, 4}, {a, b, words.inverse(a), 4}};
        for (unsigned step = 1; step <= 5; ++step) {
            Set next;
            for (const State state : layer) active_steps(state, [&](State child) { next.insert(child); });
            layer = std::move(next);
            std::cerr << "prefix " << step << ' ' << layer.size() << '\n';
        }
        for (const State state : layer) active_steps(state, [&](State child) { check_terminals(child); });
        std::cerr << "covered";
        for (const uint64_t count : counts) std::cerr << ' ' << count;
        std::cerr << " residual " << residual.size() << '\n';
        for (const State state : residual) {
            const bool ordered = words.at(state[2] >> 1) <= words.at(state[3] >> 1);
            const Id left = ordered ? state[2] : state[3], right = ordered ? state[3] : state[2];
            std::cout << words.at(state[0]) << ' ' << words.at(state[1]) << ' ' << words.at(left >> 1) << ' '
                      << words.at(right >> 1) << ' ' << (left & 1) << ' ' << (right & 1) << '\n';
        }
    }
};
}

int main() { unrestricted_eight::Search{}.run(); }
