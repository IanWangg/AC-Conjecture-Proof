// Arbitrary Nielsen-basis matching through common conjugacy classes of rank-two cores.
#define Q_ROTATION_SUBGROUPS_LIBRARY
#include "rotation_subgroups.cpp"
#include "u_native_primitive.hpp"

#include <cstdlib>
#include <numeric>
#include <set>

using Vec = std::array<int, 2>;
using Words = std::array<std::string, 2>;

struct MarkedCore {
    Graph graph;
    std::vector<std::array<char,4>> coordinates;

    explicit MarkedCore(const Words& words) : graph(fold(words[0], words[1])),
        coordinates(graph.out.size(), {0,0,0,0}) {
        std::vector<int> parent(graph.out.size(), -1), letter_to(graph.out.size(), -1);
        std::vector<int> bfs{0};
        parent[0] = 0;
        for (size_t i = 0; i < bfs.size(); ++i) {
            const int v = bfs[i];
            for (int c = 0; c < 4; ++c) {
                const int w = graph.out[v][c];
                if (w < 0 || parent[w] >= 0) continue;
                parent[w] = v;
                letter_to[w] = c;
                bfs.push_back(w);
            }
        }
        int basis_edge = 0;
        for (size_t v = 0; v < graph.out.size(); ++v) {
            for (int c = 0; c < 4; ++c) {
                const int w = graph.out[v][c];
                if (w < 0 || 4 * int(v) + c > 4 * w + (c ^ 1)) continue;
                if ((parent[w] == int(v) && letter_to[w] == c) ||
                    (parent[v] == w && letter_to[v] == (c ^ 1))) continue;
                if (basis_edge == 2) throw std::logic_error("sum of free ranks exceeds two");
                coordinates[v][c] = "xy"[basis_edge];
                coordinates[w][c ^ 1] = "XY"[basis_edge++];
            }
        }
        if (basis_edge != 2) throw std::logic_error("source rank is not two");
    }
};

Vec exponent(const std::string& word) {
    Vec abel{0,0};
    for (const auto c : word) {
        const int a = letter(c);
        abel[a / 2] += (a % 2 ? -1 : 1);
    }
    return abel;
}

int determinant(const Vec& a, const Vec& b) {
    return a[0] * b[1] - a[1] * b[0];
}

std::string cyclic_reduce(const std::string& word) {
    auto reduced = reduce(word);
    size_t a = 0, b = reduced.size();
    while (b > a + 1 && reduced[a] == inverse(reduced[b - 1])) {
        ++a;
        --b;
    }
    return reduced.substr(a, b - a);
}

std::string standard_primitive(int a, int b) {
    if (a == 0) return "y";
    if (b == 0) return "x";
    auto shorter = (a > b) ? standard_primitive(a-b, b) : standard_primitive(a, b-a);
    std::string out;
    for (const auto c : shorter) {
        if ((a > b && c == 'y') || (a <= b && c == 'x')) out += "xy";
        else out += c;
    }
    return out;
}

bool primitive(const std::string& word, const Vec& abel) {
    const int a = std::abs(abel[0]), b = std::abs(abel[1]);
    if (std::gcd(a,b) != 1) return false;
    const auto cyc = cyclic_reduce(word);
    if (cyc.size() != size_t(a + b)) return false;
    auto model = standard_primitive(a,b);
    for (auto& c : model)
        if ((c == 'x' && abel[0] < 0) || (c == 'y' && abel[1] < 0)) c = inverse(c);
    return (model + model).find(cyc) != std::string::npos;
}

struct Loop {
    std::string ambient, left, right;
    Vec a, b;
};

struct Fiber {
    std::vector<int> parent, labels;
    std::vector<Loop> single_loops, double_loops;

    Fiber(const MarkedCore& left, const MarkedCore& right)
        : parent(left.graph.out.size() * right.graph.out.size(), -1), labels(parent.size(), -1) {
        const int width = int(right.graph.out.size());
        auto next = [&](int state, int c) {
            const int a = left.graph.out[state / width][c];
            const int b = right.graph.out[state % width][c];
            return a < 0 || b < 0 ? -1 : a * width + b;
        };
        auto make_loop = [&](int root, int tail, int label, int head) {
            std::string back, word;
            for (int v = tail; v != root; v = parent[v]) back += "xXyY"[labels[v]];
            word.assign(back.rbegin(), back.rend());
            word += "xXyY"[label];
            for (int v = head; v != root; v = parent[v]) word += "xXyY"[labels[v] ^ 1];
            std::string u, v;
            int state = root;
            for (const auto c : word) {
                const auto i = letter(c);
                const auto x = left.coordinates[state / width][i];
                const auto y = right.coordinates[state % width][i];
                if (x) u += x;
                if (y) v += y;
                state = next(state, i);
            }
            if (state != root) throw std::logic_error("expected loop in product graph");
            return Loop{cyclic_reduce(word), u, v, exponent(u), exponent(v)};
        };
        std::vector<int> bfs;
        std::vector<std::array<int,3>> extra;
        for (size_t root = 0; root < parent.size(); ++root) {
            if (parent[root] >= 0) continue;
            parent[root] = int(root);
            bfs.assign(1, int(root));
            extra.clear();
            for (size_t i = 0; i < bfs.size(); ++i) {
                const int v = bfs[i];
                for (int c = 0; c < 4; ++c) {
                    const int w = next(v,c);
                    if (w < 0) continue;
                    if (parent[w] < 0) {
                        parent[w] = v;
                        labels[w] = c;
                        bfs.push_back(w);
                    } else if (4 * v + c < 4 * w + (c ^ 1)
                            && !(parent[w] == v && labels[w] == c)
                            && !(parent[v] == w && labels[v] == (c ^ 1))) {
                        extra.push_back({v,c,w});
                    }
                }
            }
            if (extra.size() > 2 || (extra.size() == 2 && !double_loops.empty()))
                throw std::logic_error("unexpected high-rank product component");
            auto& loops = (extra.size() == 2) ? double_loops : single_loops;
            for (const auto& e : extra) loops.push_back(make_loop(int(root), e[0], e[1], e[2]));
        }
    }
};

bool verified(const Loop& loop) {
    return primitive(loop.left, loop.a) && primitive(loop.right, loop.b);
}

bool compatible(const Loop& a, const Loop& b) {
    return std::abs(determinant(a.a, b.a)) == 1 && std::abs(determinant(a.b, b.b)) == 1;
}

struct Statistics {
    uint64_t compared = 0, rank_two_products = 0, any_cyclic_component = 0;
    uint64_t two_valid_cyclic_components = 0, inconclusive_lattice = 0;
    uint64_t max_cyclic_components = 0, cycles_sum = 0, primitive_projections_sum = 0;
    uint64_t full_ambient_targets = 0, multilift_barbells = 0, rank_filtered_barbells = 0;
    uint64_t unresolved_two_lobes = 0;
};

std::vector<Words> read_pairs(const char* filename) {
    std::ifstream input(filename);
    if (!input) throw std::runtime_error("missing pair catalogue");
    std::vector<Words> result;
    std::string line;
    while (std::getline(input,line)) {
        const auto at = line.find('\t');
        if (at == std::string::npos || line.find('\t', at+1) != std::string::npos)
            throw std::runtime_error("expected two tab-separated relators");
        Words words{line.substr(0,at), line.substr(at+1)};
        for (const auto& word : words)
            if (word.empty() || reduce(word) != word) throw std::runtime_error("unreduced input word");
        result.push_back(words);
    }
    return result;
}

bool lattice_might_work(const Fiber& fiber, const std::vector<size_t>& singles) {
    if (fiber.double_loops.empty()) return false;
    const auto& a = fiber.double_loops[0];
    const auto& b = fiber.double_loops[1];
    if (compatible(a,b)) return true; // Possibility of using two loops from this component.
    for (const size_t id : singles) {
        const auto& c = fiber.single_loops[id];
        // A candidate with coordinates (x,y) must solve each determinant equation with RHS ±1.
        const int u=determinant(a.a,c.a), v=determinant(b.a,c.a);
        const int p=determinant(a.b,c.b), q=determinant(b.b,c.b);
        const int d=u*q-v*p;
        if (d == 0) {
            if (std::abs(u)==std::abs(p) && std::abs(v)==std::abs(q) && std::gcd(u,v)==1)
                return true;
            continue;
        }
        for (const int sign : {-1,1})
            if ((q-v*sign)%d == 0 && (u*sign-p)%d == 0) return true;
    }
    return false;
}

void words_json(std::ostream& out, const Words& words) {
    out << "[\"" << words[0] << "\",\"" << words[1] << "\"]";
}

void loop_json(std::ostream& out, const Loop& loop) {
    out << "{\"ambient\":\"" << loop.ambient << "\",\"left_marked\":\""
        << loop.left << "\",\"right_marked\":\"" << loop.right << "\"}";
}

bool compare(const MarkedCore& left, const MarkedCore& right,
             const Words& a, const Words& b, bool primitive_free,
             Statistics& stats, std::ostream& out) {
    Fiber fiber(left,right);
    ++stats.compared;
    stats.rank_two_products += !fiber.double_loops.empty();
    stats.cycles_sum += fiber.single_loops.size();
    stats.max_cyclic_components = std::max<uint64_t>(stats.max_cyclic_components, fiber.single_loops.size());
    stats.any_cyclic_component += !fiber.single_loops.empty();
    std::vector<size_t> singles;
    for (size_t i=0; i<fiber.single_loops.size(); ++i)
        if (verified(fiber.single_loops[i])) singles.push_back(i);
    stats.primitive_projections_sum += singles.size();
    stats.two_valid_cyclic_components += singles.size()>=2;
    auto report = [&](const Loop& x, const Loop& y) {
        out << "{\"status\":\"MATCH\",\"left\":";
        words_json(out,a);
        out << ",\"right\":";
        words_json(out,b);
        out << ",\"loops\":[";
        loop_json(out,x);
        out << ',';
        loop_json(out,y);
        out << "],\"rank_two_components\":" << !fiber.double_loops.empty() << "}\n";
    };
    for (size_t i=0; i<singles.size(); ++i) {
        const auto& x=fiber.single_loops[singles[i]];
        for (size_t j=i+1; j<singles.size(); ++j) {
            const auto& y=fiber.single_loops[singles[j]];
            if (compatible(x,y)) {
                report(x,y);
                return true;
            }
        }
    }
    const bool ambient = right.graph.out.size() == 1;
    stats.full_ambient_targets += ambient;
    if (!ambient || !primitive_free)
        stats.inconclusive_lattice += lattice_might_work(fiber,singles);
    return false;
}

struct Bridge {
    std::string word;
    std::vector<Vec> lifts;
};

std::vector<Bridge> multilift_bridges(const Graph& g) {
    const int n=int(g.out.size());
    auto next = [&](int state, int c) {
        int i=g.out[state/n][c],j=g.out[state%n][c];
        if (i<0 || j<0) return -1;
        if (i>j) std::swap(i,j);
        return i*n+j;
    };
    std::vector<bool> visited(n*n);
    for (int i=0; i<n; ++i) for (int j=i+1; j<n; ++j) {
        if (visited[i*n+j]) continue;
        std::vector<int> queue{i*n+j};
        visited[queue[0]]=true;
        int darts=0;
        for (size_t k=0; k<queue.size(); ++k)
            for (int c=0; c<4; ++c) {
                int w=next(queue[k],c);
                if (w<0) continue;
                ++darts;
                if (!visited[w]) {
                    visited[w]=true;
                    queue.push_back(w);
                }
            }
        if (darts!=2*int(queue.size()-1))
            throw std::runtime_error("off-diagonal product is not a forest");
    }
    std::set<std::string> labels;
    std::string word;
    auto walk = [&](auto&& self, int state, int forbidden) -> void {
        for (int c=0; c<4; ++c) {
            if (c==forbidden) continue;
            const int w=next(state,c);
            if (w<0) continue;
            word += "xXyY"[c];
            labels.insert(word);
            self(self,w,c^1);
            word.pop_back();
        }
    };
    for (int i=0; i<n; ++i) for (int j=i+1; j<n; ++j) walk(walk,i*n+j,-1);
    std::vector<Bridge> out;
    for (const auto& q : labels) {
        std::vector<Vec> lifts;
        for (int i=0; i<n; ++i) {
            int v=i;
            for (const char c : q) {
                v=g.out[v][letter(c)];
                if (v<0) break;
            }
            if (v>=0) lifts.push_back({i,v});
        }
        if (lifts.size()<2) throw std::logic_error("word does not lift twice");
        out.push_back({q,std::move(lifts)});
    }
    return out;
}

struct Lobe {
    std::vector<int> component;
    int cycles = 0;
    explicit Lobe(const Graph& g, const std::string& word)
        : component(g.out.size()*word.size(),-1) {
        const int n=int(g.out.size()), m=int(word.size());
        std::vector<int> queue;
        for (int root=0; root<n*m; ++root) {
            if (component[root]>=0) continue;
            queue.assign(1,root);
            component[root]=root;
            int darts=0;
            for (size_t k=0; k<queue.size(); ++k) {
                const int v=queue[k]%n, at=queue[k]/n;
                const int prev=(at+m-1)%m, next=(at+1)%m;
                const int a=g.out[v][letter(word[prev])^1];
                const int b=g.out[v][letter(word[at])];
                for (int w : {a<0?-1:prev*n+a,b<0?-1:next*n+b}) {
                    if (w<0) continue;
                    ++darts;
                    if (component[w]<0) {
                        component[w]=root;
                        queue.push_back(w);
                    }
                }
            }
            cycles += darts/2-int(queue.size())+1;
        }
    }
};

bool leaves_lobe(char edge, const std::string& word, size_t at) {
    return edge!=word[at] && edge!=inverse(word[(at+word.size()-1)%word.size()]);
}

std::string rotation(const std::string& word, size_t at) {
    return word.substr(at)+word.substr(0,at);
}

bool compare_barbells(const MarkedCore& left, const Words& a, const Words& b,
                      const std::vector<Bridge>& bridges, bool primitive_free,
                      std::unordered_map<std::string,Lobe>& lobes,
                      Statistics& stats, std::ostream& out) {
    const auto& graph=left.graph;
    const int n=int(graph.out.size());
    const auto& u=lobes.try_emplace(b[0],graph,b[0]).first->second;
    const auto& v=lobes.try_emplace(b[1],graph,b[1]).first->second;
    int cycles=u.cycles+v.cycles;
    if (cycles>=2) ++stats.unresolved_two_lobes;
    std::vector<int> parents(u.component.size()+v.component.size(),-1), touched;
    auto root = [&](int id) {
        if (parents[id]<0) {
            parents[id]=id;
            touched.push_back(id);
        }
        while (parents[id]!=id) id=parents[id];
        return id;
    };
    for (const auto& bridge : bridges) {
        const char first=bridge.word.front(), last=inverse(bridge.word.back());
        for (size_t i=0; i<b[0].size(); ++i) {
            if (!leaves_lobe(first,b[0],i)) continue;
            for (size_t j=0; j<b[1].size(); ++j) {
                if (!leaves_lobe(last,b[1],j)) continue;
                ++stats.multilift_barbells;
                int rank=cycles;
                for (const auto& edge : bridge.lifts) {
                    const int a0=root(u.component[i*n+edge[0]]);
                    const int b0=root(int(u.component.size())+v.component[j*n+edge[1]]);
                    if (a0==b0) ++rank;
                    else parents[b0]=a0;
                }
                for (const int k : touched) parents[k]=-1;
                touched.clear();
                if (rank<2) {
                    ++stats.rank_filtered_barbells;
                    continue;
                }
                const Words target{rotation(b[0],i),
                    bridge.word+rotation(b[1],j)+inv(bridge.word)};
                if (compare(left,MarkedCore(target),a,target,primitive_free,stats,out))
                    return true;
            }
        }
    }
    return false;
}

int main(int argc, char** argv) {
    try {
        if (argc!=5) throw std::runtime_error("usage: fiber_join source.tsv target.tsv literal|rotations|all_tails output.json");
        const auto from=read_pairs(argv[1]), to=read_pairs(argv[2]);
        const std::string mode=argv[3];
        if (mode!="literal" && mode!="rotations" && mode!="all_tails")
            throw std::runtime_error("unknown target mode");
        std::vector<MarkedCore> roots;
        std::vector<std::vector<Bridge>> bridges;
        std::vector<bool> primitive_free, dag_absence;
        std::vector<std::unordered_map<std::string,Lobe>> lobes(from.size());
        for (const auto& a : from) {
            roots.emplace_back(a);
            const auto& graph=roots.back().graph;
            dag_absence.push_back(proves_primitive_absence(graph));
            primitive_free.push_back(dag_absence.back()
                || u_native::decide(graph.out).status==u_native::Status::ABSENT);
            bridges.push_back((mode=="all_tails") ? multilift_bridges(graph) : std::vector<Bridge>{});
        }
        std::vector<Statistics> stats(from.size());
        std::ofstream out(argv[4]);
        if (!out) throw std::runtime_error("cannot create output");
        for (const auto& item : to) {
            if (mode!="literal") for (const auto& w : item)
                if (cyclic_reduce(w)!=w) throw std::runtime_error("rotations require cyclic words");
            const auto first=(mode!="literal" ? rotations(item[0]) : std::vector<std::string>{item[0]});
            const auto second=(mode!="literal" ? rotations(item[1]) : std::vector<std::string>{item[1]});
            for (const auto& u : first) for (const auto& v : second) {
                Words b{u,v};
                MarkedCore target(b);
                for (size_t i=0; i<from.size(); ++i)
                    if (compare(roots[i],target,from[i],b,primitive_free[i],stats[i],out)) return 0;
            }
            if (mode=="all_tails") for (size_t i=0; i<from.size(); ++i)
                if (compare_barbells(roots[i],from[i],item,bridges[i],primitive_free[i],
                                     lobes[i],stats[i],out)) return 0;
        }
        out << "{\"target_rows\":" << to.size() << ",\"target_mode\":\"" << mode << "\",\"sources\":[\n";
        for (size_t i=0; i<from.size(); ++i) {
            const auto& s=stats[i];
            size_t longest=0;
            for (const auto& bridge : bridges[i]) longest=std::max(longest,bridge.word.size());
            if(i) out << ",\n";
            out << "{\"source\":";
            words_json(out,from[i]);
            out << ",\"compared\":" << s.compared << ",\"rank_two_products\":" << s.rank_two_products
                << ",\"any_cyclic_component\":" << s.any_cyclic_component
                << ",\"max_cyclic_components\":" << s.max_cyclic_components
                << ",\"cyclic_components_total\":" << s.cycles_sum
                << ",\"primitive_projections_total\":" << s.primitive_projections_sum
                << ",\"two_valid_cyclic_components\":" << s.two_valid_cyclic_components
                << ",\"inconclusive_lattice\":" << s.inconclusive_lattice
                << ",\"source_has_primitive_absence\":" << primitive_free[i]
                << ",\"source_passes_direct_DAG_test\":" << dag_absence[i]
                << ",\"full_ambient_targets\":" << s.full_ambient_targets
                << ",\"multilift_words\":" << bridges[i].size()
                << ",\"longest_multilift_word\":" << longest
                << ",\"multilift_barbells\":" << s.multilift_barbells
                << ",\"rank_filtered_barbells\":" << s.rank_filtered_barbells
                << ",\"unresolved_two_lobes\":" << s.unresolved_two_lobes << '}';
        }
        out << "]}\n";
        return 0;
    } catch(const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
