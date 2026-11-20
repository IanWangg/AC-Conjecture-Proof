// Complete bounded paths through successive exact rank-two Magnus quotients.
#define AC_ROUND08_MAGNUS_NATIVE_LIBRARY
#include "round07_magnus_native.cpp"

namespace native_corridor {
using State = free_distance::State<2>;
using StateHash = free_distance::StateHash<2>;
using Id = free_distance::Id;
using Set = std::unordered_set<State, StateHash>;
using Depths = std::unordered_map<State, unsigned, StateHash>;
using Layers = std::array<std::vector<Set>, 2>;

struct Record {
    unsigned degree;
    std::size_t midpoints;
    std::array<std::vector<std::size_t>, 2> widths;
};

State mark(State tuple, bool ordered) {
    if (!ordered && tuple[0] > tuple[1]) std::swap(tuple[0], tuple[1]);
    return tuple;
}

template <unsigned Degree>
std::array<State, 2> endpoints(magnus_native::Elements<Degree>& group, bool ordered) {
    return {mark({group.intern("xxxYYYY"), group.intern("xyxYXY")}, ordered),
            mark({group.intern("x"), group.intern("y")}, ordered)};
}

template <unsigned Degree>
Depths ball(magnus_native::Elements<Degree>& group, const State& start, unsigned radius) {
    Depths depths{{start, 0}};
    std::vector<State> frontier{start};
    for (unsigned step = 1; step <= radius; ++step) {
        std::vector<State> next;
        for (const auto& state : frontier)
            free_distance::visit_neighbors(group, state, false, [&](State candidate) {
                candidate = mark(candidate, false);
                if (depths.try_emplace(candidate, step).second) next.push_back(candidate);
                return false;
            });
        frontier = std::move(next);
    }
    return depths;
}

Set meeting(const Set& left, const Set& right) {
    const bool left_smaller = left.size() <= right.size();
    const auto& smaller = left_smaller ? left : right;
    const auto& larger = left_smaller ? right : left;
    Set result;
    for (const auto& state : smaller)
        if (larger.count(state)) result.insert(state);
    return result;
}

template <unsigned Degree, class Available>
void restrict_to_meeting(magnus_native::Elements<Degree>& group, std::vector<Set>& layers,
                         const Set& middle, bool ordered, Available&& available) {
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

Layers base_layers(magnus_native::Elements<4>& group, const std::array<unsigned, 2>& radii) {
    const auto start = endpoints(group, false);
    const std::array<Depths, 2> depths{ball(group, start[0], radii[0]), ball(group, start[1], radii[1])};
    Set middle;
    for (const auto& [state, depth] : depths[0]) {
        (void)depth;
        if (depths[1].count(state)) middle.insert(state);
    }
    Layers result;
    for (unsigned side = 0; side < 2; ++side) {
        result[side].resize(radii[side] + 1);
        restrict_to_meeting(group, result[side], middle, false, [&](const State& state, unsigned step) {
            const auto it = depths[side].find(state);
            return it != depths[side].end() && it->second <= step;
        });
    }
    return result;
}

template <unsigned Low, unsigned High>
Layers refine(magnus_native::Elements<Low>& low, const Layers& allowed,
              magnus_native::Elements<High>& high, bool ordered) {
    std::vector<Id> projection;
    auto image = [&](Id id) {
        if (id >= projection.size()) projection.resize(high.size(), free_distance::missing);
        auto& projected = projection[id];
        if (projected == free_distance::missing) projected = high.project(id, low);
        return projected;
    };
    const auto start = endpoints(high, ordered);
    Layers result;
    for (unsigned side = 0; side < 2; ++side) {
        auto& levels = result[side];
        levels.resize(allowed[side].size());
        levels[0].insert(start[side]);
        for (std::size_t i = 1; i < levels.size(); ++i) {
            auto admit = [&](State state) {
                if (allowed[side][i].count(mark({image(state[0]), image(state[1])}, false)))
                    levels[i].insert(mark(state, ordered));
                return false;
            };
            for (const auto& state : levels[i - 1]) {
                admit(state);
                free_distance::visit_neighbors(high, state, ordered, admit);
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

void add_record(std::vector<Record>& records, unsigned degree, const Layers& result) {
    Record record{degree, result[0].back().size(), {}};
    for (unsigned side = 0; side < 2; ++side)
        for (const auto& layer : result[side]) record.widths[side].push_back(layer.size());
    std::cerr << "Degree " << degree << " retained " << record.midpoints << " midpoint states.\n";
    records.push_back(std::move(record));
}

template <unsigned Degree>
void cascade(magnus_native::Elements<Degree>& group, Layers& layers, unsigned goal_degree,
             bool ordered, std::vector<Record>& records, std::vector<std::string>& midpoint) {
    if (layers[0].back().empty()) return;
    if (Degree == goal_degree) {
        const auto selected = *std::min_element(layers[0].back().begin(), layers[0].back().end());
        for (Id id : selected) midpoint.push_back(group.describe(id));
        return;
    }
    if constexpr (Degree < 10) {
        magnus_native::Elements<Degree + 1> next_group;
        auto next_layers = refine(group, layers, next_group, ordered && Degree + 1 == goal_degree);
        layers = {};
        add_record(records, Degree + 1, next_layers);
        cascade(next_group, next_layers, goal_degree, ordered, records, midpoint);
    }
}

void run(unsigned final_degree, const std::array<unsigned, 2>& radii, bool ordered) {
    magnus_native::Elements<4> base;
    auto allowed = base_layers(base, radii);
    std::vector<Record> records;
    std::vector<std::string> midpoint;
    add_record(records, 4, allowed);
    cascade(base, allowed, final_degree, ordered, records, midpoint);
    std::cout << "{\"degree\":" << final_degree << ",\"spare_rows\":0,\"ordered\":"
              << (ordered ? "true" : "false") << ",\"radii\":[" << radii[0] << "," << radii[1]
              << "],\"path_within_budget\":" << (midpoint.empty() ? "false" : "true") << ",\"midpoint_hex\":[";
    for (std::size_t index = 0; index < midpoint.size(); ++index) {
        if (index) std::cout << ',';
        std::cout << '"' << midpoint[index] << '"';
    }
    std::cout << "],\"tiers\":[";
    for (std::size_t i = 0; i < records.size(); ++i) {
        if (i) std::cout << ',';
        const auto& record = records[i];
        std::cout << "{\"degree\":" << record.degree << ",\"midpoints\":" << record.midpoints
                  << ",\"widths\":[";
        for (unsigned side = 0; side < 2; ++side) {
            if (side) std::cout << ',';
            std::cout << '[';
            for (std::size_t j = 0; j < record.widths[side].size(); ++j) {
                if (j) std::cout << ',';
                std::cout << record.widths[side][j];
            }
            std::cout << ']';
        }
        std::cout << "]}";
    }
    std::cout << "]}\n";
}
}

int main(int argc, char** argv) {
    try {
        if (argc != 4 && (argc != 5 || std::string_view(argv[4]) != "--ordered"))
            throw std::runtime_error("usage: corridor final_degree left_radius right_radius [--ordered]");
        const int degree = std::stoi(argv[1]), left = std::stoi(argv[2]), right = std::stoi(argv[3]);
        if (degree < 5 || degree > 10 || left < 0 || right < 0)
            throw std::runtime_error("degree must be 5–10 and radii nonnegative");
        native_corridor::run(degree, {unsigned(left), unsigned(right)}, argc == 5);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
