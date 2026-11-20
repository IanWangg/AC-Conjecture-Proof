// Complete bounded paths through successive rank-two Magnus quotients and the free group.
#define AC_ROUND08_MAGNUS_NATIVE_LIBRARY
#include "round07_magnus_native.cpp"
#include <memory>

namespace native_corridor {
using Id = free_distance::Id;

struct Record {
    unsigned degree;
    std::size_t midpoints;
    std::array<std::vector<std::size_t>, 2> widths;
    std::optional<uint64_t> top_mask = std::nullopt;
};

struct Options {
    unsigned final_degree;
    std::array<unsigned, 2> radii;
    unsigned padding = 0;
    bool ordered = false;
    bool free_final = false;
    bool screen = false;
    bool ledger = false;
    bool first_arrivals = false;
    bool partial_degree_six = false;
    bool compact_degree_five = false;
};

struct CompactPairLayer {
    using Pair = free_distance::State<2>;
    std::vector<std::size_t> offsets;
    std::vector<Id> seconds;

    template <class PairSet>
    CompactPairLayer(const PairSet& source, std::size_t element_count) : offsets(element_count + 1), seconds(source.size()) {
        for (const auto& state : source) ++offsets[state[0] + 1];
        for (std::size_t i = 1; i < offsets.size(); ++i) offsets[i] += offsets[i - 1];
        auto position = offsets;
        for (const auto& state : source) seconds[position[state[0]]++] = state[1];
        for (std::size_t i = 0; i < element_count; ++i)
            if (offsets[i + 1] - offsets[i] > 1)
                std::sort(seconds.begin() + offsets[i], seconds.begin() + offsets[i + 1]);
    }

    bool count(const Pair& state) const {
        const std::size_t first = state[0];
        if (first + 1 >= offsets.size()) return false;
        return std::binary_search(seconds.begin() + offsets[first], seconds.begin() + offsets[first + 1], state[1]);
    }
};

struct CompactCounts {
    std::size_t layer_count = 0, pair_count = 0, offset_bytes = 0, second_bytes = 0;
};

enum class Operation { invert, multiply, conjugate, swap };

struct Move {
    Operation op;
    unsigned row;
    unsigned operand = 0;
    int sign = 1;
};

template <std::size_t Rows>
class Corridor {
    using State = free_distance::State<Rows>;
    using StateHash = free_distance::StateHash<Rows>;
    using Set = std::unordered_set<State, StateHash>;
    using Depths = std::unordered_map<State, unsigned, StateHash>;
    using Layers = std::array<std::vector<Set>, 2>;

    const Options options;
    std::vector<Record> records;
    std::vector<std::string> midpoint;
    std::vector<Move> ledger;
    std::optional<CompactCounts> compact_counts;

    static State mark(State tuple, bool ordered) {
        if (!ordered) std::sort(tuple.begin(), tuple.end());
        return tuple;
    }

    template <class Group>
    static std::array<State, 2> endpoints(Group& group, bool ordered) {
        State start, target;
        start.fill(group.intern(""));
        target = start;
        start[0] = group.intern("xxxYYYY");
        start[1] = group.intern("xyxYXY");
        target[0] = group.intern("x");
        target[1] = group.intern("y");
        return {mark(start, ordered), mark(target, ordered)};
    }

    static std::vector<Move> menu(bool ordered) {
        std::vector<Move> moves;
        for (unsigned i = 0; i < Rows; ++i) {
            moves.push_back({Operation::invert, i});
            for (unsigned letter = 0; letter < free_distance::letters.size(); ++letter)
                moves.push_back({Operation::conjugate, i, letter});
            for (unsigned j = 0; j < Rows; ++j) {
                if (i == j) continue;
                moves.push_back({Operation::multiply, i, j, 1});
                moves.push_back({Operation::multiply, i, j, -1});
                if (ordered && i < j) moves.push_back({Operation::swap, i, j});
            }
        }
        return moves;
    }

    template <class Group>
    static State apply(Group& group, State state, Move move) {
        const auto [operation, row, operand, sign] = move;
        switch (operation) {
        case Operation::invert:
            state[row] = group.inverse(state[row]);
            break;
        case Operation::multiply: {
            const Id donor = sign == 1 ? state[operand] : group.inverse(state[operand]);
            state[row] = group.product(state[row], donor);
            break;
        }
        case Operation::conjugate:
            state[row] = group.conjugate(state[row], operand);
            break;
        case Operation::swap:
            std::swap(state[row], state[operand]);
            break;
        }
        return state;
    }

    template <class Expand>
    static Depths ball(const State& start, unsigned radius, Expand&& expand) {
        Depths depths{{start, 0}};
        std::vector<State> frontier{start};
        for (unsigned step = 1; step <= radius; ++step) {
            std::vector<State> next;
            for (const auto& state : frontier)
                expand(state, step, [&](State candidate) {
                    if (depths.try_emplace(candidate, step).second) next.push_back(candidate);
                    return false;
                });
            if (next.empty()) break;
            frontier = std::move(next);
        }
        return depths;
    }

    static Set meeting(const Set& left, const Set& right) {
        const bool left_smaller = left.size() <= right.size();
        const auto& smaller = left_smaller ? left : right;
        const auto& larger = left_smaller ? right : left;
        Set result;
        for (const auto& state : smaller)
            if (larger.count(state)) result.insert(state);
        return result;
    }

    template <class Group, class Available>
    static void restrict_to_meeting(Group& group, std::vector<Set>& layers, const Set& middle,
                                    bool ordered, Available&& available) {
        layers.back() = middle;
        for (std::size_t i = layers.size() - 1; i > 0; --i) {
            Set prior;
            auto keep = [&](State state) {
                state = mark(state, ordered);
                if (available(state, i - 1)) prior.insert(state);
                return false;
            };
            for (const auto& state : layers[i]) {
                keep(state);
                free_distance::visit_neighbors(group, state, ordered, keep);
            }
            layers[i - 1] = std::move(prior);
        }
    }

    template <class Group>
    Layers trim_balls(Group& group, const std::array<Depths, 2>& depths, bool ordered) const {
        const auto radii = options.radii;
        Set middle;
        for (const auto& [state, depth] : depths[0]) {
            (void)depth;
            if (depths[1].count(state)) middle.insert(state);
        }
        Layers result;
        for (unsigned side = 0; side < 2; ++side) {
            result[side].resize(radii[side] + 1);
            restrict_to_meeting(group, result[side], middle, ordered, [&](const State& state, unsigned step) {
                const auto it = depths[side].find(state);
                return it != depths[side].end() && it->second <= step;
            });
        }
        return result;
    }

    template <class Group>
    Layers base_layers(Group& group) const {
        const auto start = endpoints(group, false);
        auto expand = [&](const State& state, unsigned, auto&& admit) {
            free_distance::visit_neighbors(group, state, false, [&](State candidate) {
                return admit(mark(candidate, false));
            });
        };
        const std::array<Depths, 2> depths{
            ball(start[0], options.radii[0], expand), ball(start[1], options.radii[1], expand)};
        return trim_balls(group, depths, false);
    }

    template <class Low, class Allowable, class High, class Projection>
    Layers refine(Low& low, const Allowable& allowed, High& high, bool ordered, Projection&& project) const {
        std::vector<Id> projection;
        auto image = [&](Id id) {
            if (id >= projection.size()) projection.resize(high.size(), free_distance::missing);
            auto& projected = projection[id];
            if (projected == free_distance::missing) projected = project(id);
            return projected;
        };
        auto image_rows = [&](const State& state) {
            State projected;
            std::transform(state.begin(), state.end(), projected.begin(), image);
            return projected;
        };
        const auto moves = menu(ordered);
        const auto start = endpoints(high, ordered);
        auto screen_moves = [&](const State& state, const State& low_state, const auto& permitted, auto&& admit) {
            for (Move move : moves) {
                auto candidate = apply(low, low_state, move);
                if (permitted.count(mark(candidate, false)))
                    admit(mark(apply(high, state, move), ordered));
            }
        };
        if (options.first_arrivals) {
            // An actual path through a successful midpoint survives every lower tier.
            // Replacing its prefix by a shorter high-tier prefix preserves that property,
            // since waits at the midpoint fill any ticks saved by the replacement.
            std::array<Depths, 2> depths;
            for (unsigned side = 0; side < 2; ++side) {
                depths[side] = ball(start[side], options.radii[side], [&](const State& state, unsigned step, auto&& admit) {
                    screen_moves(state, image_rows(state), allowed[side][step], admit);
                });
            }
            return trim_balls(high, depths, ordered);
        }
        Layers result;
        for (unsigned side = 0; side < 2; ++side) {
            auto& levels = result[side];
            levels.resize(allowed[side].size());
            levels[0].insert(start[side]);
            for (std::size_t i = 1; i < levels.size(); ++i) {
                const auto& permitted = allowed[side][i];
                for (const auto& state : levels[i - 1]) {
                    if (options.screen || options.free_final) {
                        const State low_state = image_rows(state);
                        if (permitted.count(mark(low_state, false))) levels[i].insert(state);
                        screen_moves(state, low_state, permitted, [&](State candidate) { levels[i].insert(candidate); });
                    } else {
                        auto admit = [&](State candidate) {
                            if (permitted.count(mark(image_rows(candidate), false)))
                                levels[i].insert(mark(candidate, ordered));
                            return false;
                        };
                        admit(state);
                        free_distance::visit_neighbors(high, state, ordered, admit);
                    }
                }
            }
        }
        const auto middle = meeting(result[0].back(), result[1].back());
        for (unsigned side = 0; side < 2; ++side) {
            restrict_to_meeting(high, result[side], middle, ordered, [&](const State& state, unsigned step) {
                return result[side][step].count(state);
            });
        }
        return result;
    }

    template <class Group>
    static std::vector<State> trace_prefix(Group& group, const std::vector<Set>& layers, State selected,
                                           bool ordered) {
        std::vector<State> path{selected};
        for (std::size_t t = layers.size() - 1; t > 0; --t) {
            if (layers[t - 1].count(selected)) {
                path.push_back(selected);
                continue;
            }
            bool found = free_distance::visit_neighbors(group, selected, ordered, [&](State candidate) {
                candidate = mark(candidate, ordered);
                if (!layers[t - 1].count(candidate)) return false;
                selected = candidate;
                return true;
            });
            if (!found) throw std::runtime_error("corridor trace needs a predecessor");
            path.push_back(selected);
        }
        return {path.rbegin(), path.rend()};
    }

    template <class Group>
    void recover(Group& group, const Layers& layers, bool ordered) {
        if (layers[0].back().empty()) return;
        const auto selected = *std::min_element(layers[0].back().begin(), layers[0].back().end());
        for (Id id : selected) midpoint.push_back(group.describe(id));
        if (!options.ledger) return;
        auto path = trace_prefix(group, layers[0], selected, ordered);
        const auto suffix = trace_prefix(group, layers[1], selected, ordered);
        path.insert(path.end(), suffix.rbegin() + 1, suffix.rend());
        auto start = endpoints(group, true);
        State current = start[0];
        const auto moves = menu(ordered);
        for (const auto& target : path) {
            if (mark(current, ordered) == target) continue;
            bool found = false;
            for (Move move : moves) {
                auto candidate = apply(group, current, move);
                if (mark(candidate, ordered) != target) continue;
                current = candidate;
                ledger.push_back(move);
                found = true;
                break;
            }
            if (!found) throw std::runtime_error("corridor ledger needs a move");
        }
        if (mark(current, ordered) != mark(start[1], ordered))
            throw std::runtime_error("corridor ledger failed to reach a basis");
    }

    void add_record(unsigned degree, const Layers& layers, std::optional<uint64_t> top_mask = std::nullopt) {
        Record record{degree, layers[0].back().size(), {}, top_mask};
        for (unsigned side = 0; side < 2; ++side)
            for (const auto& layer : layers[side]) record.widths[side].push_back(layer.size());
        if (degree) std::cerr << "Degree " << degree;
        else std::cerr << "Free group";
        if (top_mask) std::cerr << " with " << __builtin_popcountll(*top_mask) << " top coordinates";
        std::cerr << " retained " << record.midpoints << " midpoint states.\n";
        records.push_back(std::move(record));
    }

    template <class Next>
    Layers refine_from_five(magnus_native::Elements<5>& degree_five, Layers& layers, Next& next, bool ordered) {
        auto project = [&](Id id) { return next.project(id, degree_five); };
        if constexpr (Rows == 2) if (options.compact_degree_five) {
            std::array<std::vector<CompactPairLayer>, 2> compact;
            CompactCounts counts;
            for (unsigned side = 0; side < 2; ++side) {
                compact[side].reserve(layers[side].size());
                for (auto& layer : layers[side]) {
                    auto& next_layer = compact[side].emplace_back(layer, degree_five.size());
                    ++counts.layer_count;
                    counts.pair_count += next_layer.seconds.size();
                    counts.offset_bytes += next_layer.offsets.size() * sizeof(std::size_t);
                    counts.second_bytes += next_layer.seconds.size() * sizeof(Id);
                    Set{}.swap(layer);
                }
            }
            compact_counts = counts;
            return refine(degree_five, compact, next, ordered, project);
        }
        return refine(degree_five, layers, next, ordered, project);
    }

    void partial_degree_six(std::unique_ptr<magnus_native::Elements<5>> degree_five, Layers layers) {
        using DegreeSix = magnus_native::Elements<6>;
        // The final eleventh coordinate is added by the full degree-six refinement.
        constexpr std::array<unsigned, 10> coordinates{1, 3, 5, 7, 9, 11, 13, 15, 23, 27};
        uint64_t mask = uint64_t(1) << coordinates.front();
        auto current = std::make_unique<DegreeSix>(mask);
        layers = refine_from_five(*degree_five, layers, *current, false);
        degree_five.reset();
        add_record(6, layers, mask);
        for (unsigned i = 1; i < coordinates.size() && !layers[0].back().empty(); ++i) {
            mask |= uint64_t(1) << coordinates[i];
            auto next = std::make_unique<DegreeSix>(mask);
            layers = refine(*current, layers, *next, false, [&](Id id) { return next->project(id, *current); });
            current = std::move(next);
            add_record(6, layers, mask);
        }
        if (layers[0].back().empty()) return;

        auto full = std::make_unique<DegreeSix>();
        const bool ordered = options.ordered && options.final_degree == 6 && !options.free_final;
        layers = refine(*current, layers, *full, ordered, [&](Id id) { return full->project(id, *current); });
        current.reset();
        add_record(6, layers);
        cascade(std::move(full), std::move(layers));
    }

    template <unsigned Degree>
    void cascade(std::unique_ptr<magnus_native::Elements<Degree>> group, Layers layers) {
        if (layers[0].back().empty()) return;
        if (Degree == options.final_degree) {
            if (options.free_final) {
                free_distance::WordTable next;
                auto lifted = refine(*group, layers, next, options.ordered, [&](Id id) {
                    return group->intern(next.at(id));
                });
                add_record(0, lifted);
                recover(next, lifted, options.ordered);
            } else {
                recover(*group, layers, options.ordered);
            }
            return;
        }
        if constexpr (Degree == 5) {
            if (options.partial_degree_six) {
                partial_degree_six(std::move(group), std::move(layers));
                return;
            }
        }
        if constexpr (Degree < 10) {
            auto next = std::make_unique<magnus_native::Elements<Degree + 1>>();
            const bool ordered = options.ordered && Degree + 1 == options.final_degree && !options.free_final;
            Layers lifted;
            if constexpr (Degree == 5) lifted = refine_from_five(*group, layers, *next, ordered);
            else lifted = refine(*group, layers, *next, ordered, [&](Id id) { return next->project(id, *group); });
            group.reset();
            layers = {};
            add_record(Degree + 1, lifted);
            cascade(std::move(next), std::move(lifted));
        }
    }

    static void print_widths(const Record& record) {
        std::cout << "\"midpoints\":" << record.midpoints << ",\"widths\":[";
        for (unsigned side = 0; side < 2; ++side) {
            if (side) std::cout << ',';
            std::cout << '[';
            for (std::size_t j = 0; j < record.widths[side].size(); ++j) {
                if (j) std::cout << ',';
                std::cout << record.widths[side][j];
            }
            std::cout << ']';
        }
        std::cout << ']';
    }

    static void print_ledger_move(Move move) {
        const auto [op, row, operand, sign] = move;
        switch (op) {
        case Operation::invert: std::cout << "[\"invert\"," << row << ']'; break;
        case Operation::multiply: std::cout << "[\"multiply\"," << row << ',' << operand << ',' << sign << ']'; break;
        case Operation::conjugate:
            std::cout << "[\"conjugate\"," << row << ',' << operand / 2 << ',' << ((operand & 1) ? -1 : 1) << ']';
            break;
        case Operation::swap: std::cout << "[\"swap\"," << row << ',' << operand << ']'; break;
        }
    }

    void print() const {
        std::cout << "{\"degree\":" << options.final_degree << ",\"spare_rows\":" << Rows - 2 << ",\"ordered\":"
                  << (options.ordered ? "true" : "false") << ",\"radii\":[" << options.radii[0] << ',' << options.radii[1]
                  << "],\"path_within_budget\":" << (midpoint.empty() ? "false" : "true") << ",\"midpoint_hex\":[";
        if (!options.free_final) print_midpoint();
        std::cout << "],\"tiers\":[";
        for (std::size_t i = 0; i < records.size() && records[i].degree != 0; ++i) {
            if (i) std::cout << ',';
            std::cout << "{\"degree\":" << records[i].degree << ',';
            if (records[i].top_mask) std::cout << "\"top_mask\":" << *records[i].top_mask << ',';
            print_widths(records[i]);
            std::cout << '}';
        }
        std::cout << ']';
        if (options.free_final) {
            std::cout << ",\"midpoint_words\":[";
            print_midpoint();
            std::cout << "],\"free_tier\":";
            if (records.back().degree == 0) {
                std::cout << '{';
                print_widths(records.back());
                std::cout << '}';
            } else {
                std::cout << "null";
            }
        }
        if (options.ledger) {
            std::cout << ",\"moves\":[";
            for (std::size_t i = 0; i < ledger.size(); ++i) {
                if (i) std::cout << ',';
                print_ledger_move(ledger[i]);
            }
            std::cout << ']';
        }
        if (compact_counts) {
            std::cout << ",\"compact_degree_five\":{\"layers\":" << compact_counts->layer_count
                      << ",\"pairs\":" << compact_counts->pair_count << ",\"offset_bytes\":" << compact_counts->offset_bytes
                      << ",\"second_id_bytes\":" << compact_counts->second_bytes << '}';
        }
        std::cout << "}\n";
    }

    void print_midpoint() const {
        for (std::size_t i = 0; i < midpoint.size(); ++i) {
            if (i) std::cout << ',';
            std::cout << '"' << midpoint[i] << '"';
        }
    }

public:
    explicit Corridor(Options parameters) : options(parameters) {}

    template <unsigned BaseDegree>
    void run() {
        auto base = std::make_unique<magnus_native::Elements<BaseDegree>>();
        auto layers = base_layers(*base);
        add_record(BaseDegree, layers);
        cascade(std::move(base), std::move(layers));
        print();
    }
};
}

int main(int argc, char** argv) {
    using namespace native_corridor;
    try {
        if (argc < 4)
            throw std::runtime_error("usage: corridor final_degree left_radius right_radius "
                                     "[--ordered] [--spare-rows N] [--free] [--screen] [--ledger] "
                                     "[--first-arrivals] [--partial-degree-six] [--compact-degree-five]");
        const int degree = std::stoi(argv[1]), left = std::stoi(argv[2]), right = std::stoi(argv[3]);
        if (degree < 5 || degree > 10 || left < 0 || right < 0)
            throw std::runtime_error("degree must be 5–10 and radii nonnegative");
        Options options{unsigned(degree), {unsigned(left), unsigned(right)}};
        for (int i = 4; i < argc; ++i) {
            const std::string_view argument(argv[i]);
            if (argument == "--ordered") options.ordered = true;
            else if (argument == "--free") options.free_final = true;
            else if (argument == "--screen") options.screen = true;
            else if (argument == "--ledger") options.ledger = true;
            else if (argument == "--first-arrivals") options.first_arrivals = true;
            else if (argument == "--partial-degree-six") options.partial_degree_six = true;
            else if (argument == "--compact-degree-five") options.compact_degree_five = true;
            else if (argument == "--spare-rows" && i + 1 < argc) options.padding = std::stoul(argv[++i]);
            else throw std::runtime_error("unexpected corridor option");
        }
        if (options.partial_degree_six && degree < 6) throw std::runtime_error("partial-degree-six needs a final degree of at least six");
        if (options.compact_degree_five && (degree < 6 || options.padding != 0))
            throw std::runtime_error("compact-degree-five requires an unpadded search through at least degree six");
        options.screen = options.screen || options.padding > 0;
        switch (options.padding) {
        case 0: Corridor<2>(options).run<4>(); break;
        case 1: Corridor<3>(options).run<3>(); break;
        case 2: Corridor<4>(options).run<3>(); break;
        case 3: Corridor<5>(options).run<3>(); break;
        default: throw std::runtime_error("spare row count outside 0–3");
        }
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
