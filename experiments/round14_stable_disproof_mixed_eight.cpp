// Generate the width-eight terminal templates surviving the isolated quadratic marking.
#define AC_ROUND06_INSTRUCTION_DISTANCE_LIBRARY
#include "round06_free_instruction_distance.cpp"

namespace mixed_eight {
using free_distance::Id;
using free_distance::WordTable;
using Rows = std::array<unsigned, 3>;
using State = std::array<Id, 4>;
using Set = std::unordered_set<State, free_distance::StateHash<4>>;
constexpr unsigned code_count = 1U << 18;
constexpr unsigned row_mask = 63;

enum class Kind { invert, multiply, conjugate };
struct Move { Kind kind; unsigned recipient, operand; bool negative; };

std::vector<Move> instructions() {
    std::vector<Move> moves;
    for (unsigned i = 0; i < 3; ++i) {
        moves.push_back({Kind::invert, i, 0, false});
        for (unsigned j = 0; j < 3; ++j) if (i != j) {
            moves.push_back({Kind::multiply, i, j, false});
            moves.push_back({Kind::multiply, i, j, true});
        }
        for (unsigned letter = 0; letter < 4; ++letter) moves.push_back({Kind::conjugate, i, letter, false});
    }
    return moves;
}

unsigned encode(Rows rows) { return rows[0] | (rows[1] << 6) | (rows[2] << 12); }
unsigned product(unsigned a, unsigned b) {
    return a ^ b ^ ((a & 4) ? (b & 3) << 3 : 0) ^ ((a & b & 4) ? 32 : 0);
}
unsigned inverse(unsigned row) { return row ^ ((row & 4) ? ((row & 3) << 3) | 32 : 0); }

unsigned mixed_step(unsigned code, Move move) {
    const unsigned offset = 6 * move.recipient;
    const unsigned row = (code >> offset) & row_mask;
    unsigned output = row;
    switch (move.kind) {
    case Kind::invert: output = inverse(row); break;
    case Kind::multiply: {
        const unsigned donor = (code >> (6 * move.operand)) & row_mask;
        output = product(row, move.negative ? inverse(donor) : donor);
        break;
    }
    case Kind::conjugate:
        if (row & 4) output ^= 8U << (move.operand / 2);
        break;
    }
    return code ^ ((row ^ output) << offset);
}

Id formal_step(WordTable& words, State state, Move move) {
    const Id row = state[move.recipient];
    switch (move.kind) {
    case Kind::invert: return words.inverse(row);
    case Kind::multiply:
        return words.product(row, move.negative ? words.inverse(state[move.operand]) : state[move.operand]);
    case Kind::conjugate: return words.conjugate(row, move.operand);
    }
    throw std::runtime_error("invalid formal move");
}

struct Comparison {
    WordTable words;
    const Id one = words.intern("");
    const Id a = words.intern("a"), b = words.intern("b"), A = words.inverse(a);
    const std::vector<Move> moves = instructions();
    std::vector<std::array<unsigned, 27>> mixed_edges{code_count};
    std::vector<unsigned char> distance = std::vector<unsigned char>(code_count, 99);
    std::vector<std::array<unsigned, 7>> allowed{code_count};
    std::vector<unsigned char> parity;

    void initialize() {
        std::vector<unsigned> frontier;
        for (unsigned alpha = 1; alpha <= 3; ++alpha)
            for (unsigned beta = alpha + 1; beta <= 3; ++beta) {
                Rows rows{alpha, beta, 4};
                do {
                    const unsigned state = encode(rows);
                    distance[state] = 0;
                    frontier.push_back(state);
                } while (std::next_permutation(rows.begin(), rows.end()));
            }
        std::cout << "R " << frontier.size();
        for (unsigned code = 0; code < code_count; ++code)
            for (unsigned k = 0; k < moves.size(); ++k) mixed_edges[code][k] = mixed_step(code, moves[k]);
        for (unsigned radius = 1; radius <= 7; ++radius) {
            std::vector<unsigned> next;
            for (const unsigned code : frontier)
                for (const unsigned child : mixed_edges[code]) if (distance[child] == 99) {
                    distance[child] = radius;
                    next.push_back(child);
                }
            frontier = std::move(next);
            std::cout << ' ' << frontier.size();
        }
        std::cout << '\n';
        for (unsigned code = 0; code < code_count; ++code)
            for (unsigned remaining = 0; remaining <= 6; ++remaining)
                for (unsigned k = 0; k < moves.size(); ++k)
                    if (distance[mixed_edges[code][k]] <= remaining) allowed[code][remaining] |= 1U << k;
    }

    unsigned old_linear(Id word) {
        if (word >= parity.size()) parity.resize(words.size(), 255);
        auto& value = parity[word];
        if (value != 255) return value;
        value = 0;
        for (const char letter : words.at(word)) {
            if (letter == 'a' || letter == 'A') value ^= 1;
            if (letter == 'b' || letter == 'B') value ^= 2;
        }
        return value;
    }

    template<class Visit>
    void active_moves(State source, unsigned remaining, Visit&& accept) {
        const unsigned mixed = source[3];
        for (unsigned mask = allowed[mixed][remaining]; mask; mask &= mask - 1) {
            const unsigned k = __builtin_ctz(mask);
            const auto move = moves[k];
            const Id image = formal_step(words, source, move);
            if (image == one || image == source[move.recipient]) continue;
            State child = source;
            child[move.recipient] = image;
            child[3] = mixed_edges[mixed][k];
            accept(child, k);
        }
    }

    template<class Visit>
    void terminal(State state, Visit&& accept) {
        const unsigned mixed = state[3];
        unsigned z_rows = 0;
        for (unsigned i = 0; i < 3; ++i) if ((mixed >> (6 * i)) & 4) z_rows |= 1U << i;
        if (z_rows == 0 || z_rows & (z_rows - 1)) return;
        const unsigned i = __builtin_ctz(z_rows);
        Id left = state[(i + 1) % 3], right = state[(i + 2) % 3];
        if (left > right) std::swap(left, right);
        for (unsigned mask = allowed[mixed][0]; mask; mask &= mask - 1) {
            const unsigned k = __builtin_ctz(mask);
            const Move move = moves[k];
            if (move.kind != Kind::multiply || move.recipient != i ||
                old_linear(state[move.operand]) != old_linear(state[i])) continue;
            const Id donor = move.negative ? state[move.operand] : words.inverse(state[move.operand]);
            accept(State{state[i], donor, left, right}, k);
        }
    }

    std::array<Set, 6> prefixes(unsigned alpha, unsigned beta) {
        const unsigned after_birth = encode({alpha, beta, product(4, alpha)});
        std::array<Set, 6> layers;
        layers[0] = {{a, b, a, after_birth}, {a, b, A, after_birth}};
        for (unsigned depth = 1; depth <= 5; ++depth) {
            for (const State state : layers[depth - 1])
                active_moves(state, 7 - depth, [&](State child, unsigned) { layers[depth].insert(child); });
        }
        return layers;
    }

    void compare(unsigned alpha, unsigned beta, Set& cases) {
        const auto layers = prefixes(alpha, beta);
        std::cout << "L " << alpha << ' ' << beta;
        for (const auto& layer : layers) std::cout << ' ' << layer.size();
        std::size_t final_edges = 0;
        for (const State state : layers.back()) active_moves(state, 1, [&](State child, unsigned) {
            ++final_edges;
            terminal(child, [&](State pattern, unsigned) { cases.insert(pattern); });
        });
        std::cout << ' ' << final_edges << ' ' << cases.size() << '\n' << std::flush;
    }

    void trace(unsigned alpha, unsigned beta, const Set& wanted) {
        const auto broad = prefixes(alpha, beta);
        std::array<Set, 7> viable;
        std::unordered_map<State, unsigned, free_distance::StateHash<4>> final_moves;
        for (const State state : broad[5]) active_moves(state, 1, [&](State child, unsigned) {
            terminal(child, [&](State pattern, unsigned move) {
                if (wanted.count(pattern)) {
                    viable[5].insert(state);
                    viable[6].insert(child);
                    final_moves[child] |= 1U << move;
                }
            });
        });
        for (int depth = 4; depth >= 0; --depth) for (const State state : broad[depth])
            active_moves(state, 6 - depth, [&](State child, unsigned) {
                if (viable[depth + 1].count(child)) viable[depth].insert(state);
            });

        std::vector<std::array<unsigned, 8>> traces;
        std::array<unsigned, 8> instructions{};
        auto visit = [&](auto& self, State state, unsigned depth) -> void {
            if (depth == 6) {
                for (unsigned mask = final_moves.at(state); mask; mask &= mask - 1) {
                    instructions[7] = __builtin_ctz(mask);
                    traces.push_back(instructions);
                }
                return;
            }
            active_moves(state, 6 - depth, [&](State child, unsigned k) {
                if (viable[depth + 1].count(child)) {
                    instructions[depth + 1] = k;
                    self(self, child, depth + 1);
                }
            });
        };
        for (const State state : viable[0]) {
            instructions[0] = state[2] == A;
            visit(visit, state, 0);
        }
        std::sort(traces.begin(), traces.end());
        std::cout << "V " << alpha << ' ' << beta << ' ' << traces.size();
        for (const auto& layer : viable) std::cout << ' ' << layer.size();
        std::cout << '\n';
        for (const auto& path : traces) {
            std::cout << "W " << alpha << ' ' << beta;
            for (const unsigned instruction : path) std::cout << ' ' << instruction;
            std::cout << '\n';
        }
    }

    void run() {
        initialize();
        Set cases;
        // Swapping x and y recovers the other three independent markings.
        for (const Rows marking : {Rows{1, 2, 0}, Rows{1, 3, 0}, Rows{3, 1, 0}})
            compare(marking[0], marking[1], cases);
        std::vector<std::array<std::string, 4>> output;
        output.reserve(cases.size());
        for (const State state : cases) {
            std::array<std::string, 4> row{words.at(state[0]), words.at(state[1]), words.at(state[2]), words.at(state[3])};
            if (row[2] > row[3]) std::swap(row[2], row[3]);
            output.push_back(std::move(row));
        }
        std::sort(output.begin(), output.end());
        for (const auto& row : output) std::cout << "T " << row[0] << ' ' << row[1] << ' ' << row[2] << ' ' << row[3] << '\n';
    }

    void run_traces() {
        Set wanted;
        std::array<std::string, 4> pattern;
        while (std::cin >> pattern[0] >> pattern[1] >> pattern[2] >> pattern[3]) {
            State key{words.intern(pattern[0]), words.intern(pattern[1]), words.intern(pattern[2]), words.intern(pattern[3])};
            if (key[2] > key[3]) std::swap(key[2], key[3]);
            wanted.insert(key);
        }
        if (!std::cin.eof() || wanted.empty()) throw std::runtime_error("invalid residual template list");
        initialize();
        for (const Rows marking : {Rows{1, 2, 0}, Rows{1, 3, 0}, Rows{3, 1, 0}}) trace(marking[0], marking[1], wanted);
    }
};

struct StrictComparison {
    using Pair = free_distance::State<2>;
    using Pairs = std::unordered_set<Pair, free_distance::StateHash<2>>;
    WordTable words;
    Pairs reached;
    std::vector<unsigned char> exponents;

    static Pair pair(Id a, Id b) { return a <= b ? Pair{a, b} : Pair{b, a}; }

    void radius_seven() {
        const Pair start = pair(words.intern("a"), words.intern("b"));
        reached.insert(start);
        std::vector<Pair> frontier{start};
        for (unsigned depth = 1; depth <= 7; ++depth) {
            std::vector<Pair> following;
            auto add = [&](Id a, Id b) {
                const Pair child = pair(a, b);
                if (reached.insert(child).second) following.push_back(child);
            };
            for (Pair state : frontier) for (unsigned i = 0; i < 2; ++i) {
                const Id a = state[i], b = state[i ^ 1];
                add(words.inverse(a), b);
                add(words.product(a, b), b);
                add(words.product(a, words.inverse(b)), b);
                for (unsigned letter = 0; letter < 4; ++letter) add(words.conjugate(a, letter), b);
            }
            frontier = std::move(following);
        }
    }

    unsigned exponent_coordinates(Id word) {
        if (word >= exponents.size()) exponents.resize(words.size(), 255);
        auto& value = exponents[word];
        if (value != 255) return value;
        unsigned a = 0, b = 0;
        for (const char letter : words.at(word)) {
            a += letter == 'a';
            a -= letter == 'A';
            b += letter == 'b';
            b -= letter == 'B';
        }
        return value = (a & 15) | ((b & 15) << 4);
    }

    void run() {
        radius_seven();
        std::array<std::size_t, 4> counts{};
        std::string line;
        while (std::getline(std::cin, line)) {
            if (line.empty() || line[0] != 'T') {
                std::cout << line << '\n';
                continue;
            }
            std::array<std::string_view, 4> tokens;
            std::string_view remaining(line);
            remaining.remove_prefix(2);
            for (std::string_view& token : tokens) {
                const auto space = remaining.find(' ');
                token = remaining.substr(0, space);
                remaining.remove_prefix(space == std::string_view::npos ? remaining.size() : space + 1);
            }
            const Id a = words.intern(std::string(tokens[2])), b = words.intern(std::string(tokens[3]));
            if (reached.count(pair(a, b))) {
                ++counts[0];
                continue;
            }
            const Id removed = words.intern(std::string(tokens[0])), donor = words.intern(std::string(tokens[1]));
            const bool direct = donor == a || donor == b;
            const Id replaced = direct ? donor : words.inverse(donor);
            if (replaced != a && replaced != b) throw std::runtime_error("signed donor missing from terminal pair");
            const Id substitute = direct ? removed : words.inverse(removed);
            if (reached.count(pair(substitute, replaced == a ? b : a))) ++counts[1];
            else if (exponent_coordinates(removed) != exponent_coordinates(donor)) ++counts[2];
            else {
                ++counts[3];
                std::cout << line << '\n';
            }
        }
        std::cout << "C " << reached.size();
        for (const std::size_t count : counts) std::cout << ' ' << count;
        std::cout << '\n';
    }
};
}

int main(int argc, char** argv) {
    if (argc == 1) mixed_eight::Comparison{}.run();
    else if (argc == 2 && std::string_view(argv[1]) == "--strict") mixed_eight::StrictComparison{}.run();
    else if (argc == 2 && std::string_view(argv[1]) == "--traces") mixed_eight::Comparison{}.run_traces();
    else throw std::runtime_error("expected no arguments, --strict or --traces");
}
