// e_acdist.cpp -- exact AC distances in free-nilpotent quotients F/gamma_{c+1}(F)
// of F = F(x,y), and in F itself, by exhaustive bidirectional breadth-first search.
//
// Standard library only.  Build:  g++ -O2 -std=c++17 -o e_acdist e_acdist.cpp
//
// Quotient model (Magnus 1937): w -> mu(w) in Z<X,Y>/(degree > c), x -> 1+X,
// x^-1 -> 1-X+X^2-..., and similarly for y.  The kernel of this homomorphism is
// exactly gamma_{c+1}(F), so states are compared exactly in N_c = F/gamma_{c+1}(F).
// With --mod m the coefficients are reduced mod m; that is a further (finite)
// quotient of N_c, so its distances are still lower bounds for the free distance.
//
// Move alphabet (identical to research-b.md, 15 symmetric instructions):
//   0: a <- a^-1          1: b <- b^-1          2: swap (a,b) <- (b,a)
//   3: a <- a b           4: a <- a b^-1        5: b <- b a          6: b <- b a^-1
//   7..10:  a <- g^-1 a g,   g = x, X, y, Y
//   11..14: b <- g^-1 b g,   g = x, X, y, Y
// The alphabet is closed under inverses, so the move graph is undirected and
// bidirectional BFS gives exact distances.  If the search stops at completed radii
// (rA, rB) without the two balls meeting, the distance is >= rA + rB + 1 (proved
// in research-e.md); this is the only kind of lower bound this program reports.
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <stdexcept>
using namespace std;
typedef int64_t i64;
typedef int32_t i32;
typedef __int128 i128;

[[maybe_unused]] static const char* MOVE_NAMES[15] = {
    "inv a", "inv b", "swap", "a<-ab", "a<-aB", "b<-ba", "b<-bA",
    "a<-x^-1 a x", "a<-x a x^-1", "a<-y^-1 a y", "a<-y a y^-1",
    "b<-x^-1 b x", "b<-x b x^-1", "b<-y^-1 b y", "b<-y b y^-1"};
static const int MOVE_INVERSE[15] = {0, 1, 2, 4, 3, 6, 5, 8, 7, 10, 9, 12, 11, 14, 13};

// ---------------------------------------------------------------- free words
static string freduce(const string& w) {
    string out;
    out.reserve(w.size());
    for (char ch : w) {
        if (!out.empty() && out.back() == (char)(ch ^ 32)) out.pop_back();
        else out.push_back(ch);
    }
    return out;
}
static string finv(const string& w) {
    string r(w.rbegin(), w.rend());
    for (char& ch : r) ch ^= 32;  // swap case
    return r;
}
static void check_word(const string& w) {
    for (char ch : w)
        if (ch != 'x' && ch != 'X' && ch != 'y' && ch != 'Y')
            throw runtime_error("words must use x,X,y,Y");
}
static const char GEN[4] = {'x', 'X', 'y', 'Y'};

static void free_move(const string& a, const string& b, int m, string& na, string& nb) {
    na = a; nb = b;
    switch (m) {
        case 0: na = finv(a); break;
        case 1: nb = finv(b); break;
        case 2: na = b; nb = a; break;
        case 3: na = freduce(a + b); break;
        case 4: na = freduce(a + finv(b)); break;
        case 5: nb = freduce(b + a); break;
        case 6: nb = freduce(b + finv(a)); break;
        default: {
            int k = (m - 7) % 4;
            string g(1, GEN[k]), gi(1, (char)(GEN[k] ^ 32));
            if (m < 11) na = freduce(gi + a + g);
            else nb = freduce(gi + b + g);
        }
    }
}

// ------------------------------------------------- truncated Magnus algebra
struct Algebra {
    int c = 0, N = 0;  // N = number of monomials of degree <= c = 2^(c+1)-1
    i64 mod = 0;       // 0 => integer coefficients
    vector<vector<i64>> gen;  // images of x, X, y, Y
    i64 maxabs = 0;
    int off(int d) const { return (1 << d) - 1; }
    void init(int cc, i64 m) {
        c = cc; mod = m; N = (1 << (c + 1)) - 1;
        gen.assign(4, vector<i64>(N, 0));
        for (int g = 0; g < 4; g++) {
            int bit = (g < 2) ? 0 : 1;  // X -> bit 0, Y -> bit 1
            bool inv = (g % 2 == 1);
            gen[g][0] = 1;
            for (int d = 1; d <= c; d++) {
                int idx = 0;
                for (int t = 0; t < d; t++) idx = (idx << 1) | bit;
                i64 v = inv ? ((d % 2) ? -1 : 1) : (d == 1 ? 1 : 0);
                gen[g][off(d) + idx] = norm(v);
            }
        }
    }
    i64 norm(i128 v) {
        if (mod) {
            i128 r = v % mod;
            if (r < 0) r += mod;
            return (i64)r;
        }
        if (v > (i128)INT32_MAX || v < (i128)INT32_MIN)
            throw runtime_error("coefficient overflow beyond int32; result would be unsafe");
        i64 a = (i64)v;
        if (a < 0 ? -a > maxabs : a > maxabs) maxabs = a < 0 ? -a : a;
        return a;
    }
    void mul(const i64* a, const i64* b, i64* out) {
        vector<i128> acc(N, 0);
        for (int da = 0; da <= c; da++)
            for (int ia = 0; ia < (1 << da); ia++) {
                i64 ca = a[off(da) + ia];
                if (!ca) continue;
                for (int db = 0; db + da <= c; db++) {
                    int base = off(da + db) + (ia << db);
                    const i64* bp = b + off(db);
                    for (int ib = 0; ib < (1 << db); ib++)
                        if (bp[ib]) acc[base + ib] += (i128)ca * bp[ib];
                }
            }
        for (int i = 0; i < N; i++) out[i] = norm(acc[i]);
    }
    void inverse(const i64* a, i64* out) {
        // a = 1+u;  a^-1 = sum_k (-u)^k, truncated
        vector<i64> negu(N), term(N, 0), tmp(N);
        for (int i = 0; i < N; i++) negu[i] = norm(-(i128)a[i]);
        negu[0] = 0;
        term[0] = 1;
        for (int i = 0; i < N; i++) out[i] = 0;
        out[0] = 1;
        for (int k = 1; k <= c; k++) {
            mul(term.data(), negu.data(), tmp.data());
            term = tmp;
            for (int i = 0; i < N; i++) out[i] = norm((i128)out[i] + term[i]);
        }
    }
    vector<i64> word(const string& w) {
        vector<i64> r(N, 0), t(N);
        r[0] = 1;
        for (char ch : w) {
            int g = ch == 'x' ? 0 : ch == 'X' ? 1 : ch == 'y' ? 2 : 3;
            mul(r.data(), gen[g].data(), t.data());
            r = t;
        }
        return r;
    }
};

// ------------------------------------------------- append-only state set
// Keys are stored densely in insertion order (ids 0,1,2,...); a growable
// open-addressing index maps keys to ids.  Full keys are always compared, so
// membership tests are exact (no fingerprints).
struct Table {
    int K = 0;
    size_t count = 0;
    static const size_t CH = 1 << 16;  // states per storage chunk (no big reallocations)
    vector<vector<i32>> chunks;         // chunk j holds ids j*CH .. j*CH+CH-1
    vector<uint8_t> dist;  // per id
    vector<uint32_t> idx;  // slot -> id+1, 0 = empty
    void init(int k, size_t) { K = k; count = 0; chunks.clear(); dist.clear(); idx.assign(1 << 12, 0); }
    static uint64_t hashk(const i32* k, int K) {
        uint64_t h = 0x9E3779B97F4A7C15ULL;
        for (int i = 0; i < K; i++) {
            h ^= (uint32_t)k[i];
            h *= 0xBF58476D1CE4E5B9ULL;
            h ^= h >> 29;
        }
        return h;
    }
    const i32* key(size_t id) const { return &chunks[id / CH][(id % CH) * K]; }
    // returns id or SIZE_MAX
    size_t find(const i32* k) const {
        size_t m = idx.size() - 1, s = hashk(k, K) & m;
        while (idx[s]) {
            size_t id = idx[s] - 1;
            if (memcmp(key(id), k, K * sizeof(i32)) == 0) return id;
            s = (s + 1) & m;
        }
        return SIZE_MAX;
    }
    void grow() {
        vector<uint32_t> n(idx.size() * 2, 0);
        size_t m = n.size() - 1;
        for (size_t id = 0; id < count; id++) {
            size_t s = hashk(key(id), K) & m;
            while (n[s]) s = (s + 1) & m;
            n[s] = (uint32_t)(id + 1);
        }
        idx.swap(n);
    }
    // insert if absent; returns id and sets inserted
    size_t insert(const i32* k, uint8_t d, bool& inserted) {
        if ((count + 1) * 10 > idx.size() * 7) grow();
        size_t m = idx.size() - 1, s = hashk(k, K) & m;
        while (idx[s]) {
            size_t id = idx[s] - 1;
            if (memcmp(key(id), k, K * sizeof(i32)) == 0) { inserted = false; return id; }
            s = (s + 1) & m;
        }
        if (count >= 0xFFFFFFF0ULL) throw runtime_error("too many states");
        if (count % CH == 0) { chunks.emplace_back(); chunks.back().resize(CH * (size_t)K); }
        memcpy(&chunks[count / CH][(count % CH) * K], k, K * sizeof(i32));
        dist.push_back(d);
        idx[s] = (uint32_t)(count + 1);
        inserted = true;
        return count++;
    }
};

struct NilSearch {
    Algebra A;
    int K;
    vector<i64> sa, sb;  // scratch
    void key_of(const vector<i64>& a, const vector<i64>& b, vector<i32>& k) {
        int M = A.N - 1;
        for (int i = 0; i < M; i++) { k[i] = (i32)a[i + 1]; k[M + i] = (i32)b[i + 1]; }
    }
    void from_key(const i32* k, vector<i64>& a, vector<i64>& b) {
        int M = A.N - 1;
        a[0] = b[0] = 1;
        for (int i = 0; i < M; i++) { a[i + 1] = k[i]; b[i + 1] = k[M + i]; }
    }
    void move(const vector<i64>& a, const vector<i64>& b, const vector<i64>& ai,
              const vector<i64>& bi, int m, vector<i64>& na, vector<i64>& nb) {
        na = a; nb = b;
        vector<i64> t(A.N);
        switch (m) {
            case 0: na = ai; break;
            case 1: nb = bi; break;
            case 2: na = b; nb = a; break;
            case 3: A.mul(a.data(), b.data(), na.data()); break;
            case 4: A.mul(a.data(), bi.data(), na.data()); break;
            case 5: A.mul(b.data(), a.data(), nb.data()); break;
            case 6: A.mul(b.data(), ai.data(), nb.data()); break;
            default: {
                int g = (m - 7) % 4, gi = g ^ 1;
                const vector<i64>& src = (m < 11) ? a : b;
                vector<i64>& dst = (m < 11) ? na : nb;
                A.mul(A.gen[gi].data(), src.data(), t.data());
                A.mul(t.data(), A.gen[g].data(), dst.data());
            }
        }
    }
};

struct Result {
    bool exact = false;
    int distance = -1;      // exact distance if exact
    int lower = -1;         // certified lower bound otherwise
    vector<size_t> layersS, layersT;
    vector<int> path;       // moves from start to target (if exact)
    string note;
};

// Generic bidirectional BFS over an abstract state space given by callbacks.
// To keep the code short and auditable we implement it twice (nil / free).
static Result nil_bfs(int c, i64 mod, const string s0, const string s1, const string t0,
                      const string t1, size_t maxStates, int maxRadius, i64& maxabs) {
    NilSearch S;
    S.A.init(c, mod);
    int M = S.A.N - 1;
    S.K = 2 * M;
    Table T[2];
    T[0].init(S.K, maxStates);
    T[1].init(S.K, maxStates);
    vector<i64> a0 = S.A.word(s0), b0 = S.A.word(s1), a1 = S.A.word(t0), b1 = S.A.word(t1);
    vector<i32> k(S.K);
    vector<vector<size_t>> front(2);
    int radius[2] = {0, 0};
    bool ins;
    Result R;
    R.layersS.push_back(1); R.layersT.push_back(1);
    S.key_of(a0, b0, k);
    front[0].push_back(T[0].insert(k.data(), 0, ins));
    S.key_of(a1, b1, k);
    if (T[0].find(k.data()) != SIZE_MAX) { R.exact = true; R.distance = 0; maxabs = S.A.maxabs; return R; }
    front[1].push_back(T[1].insert(k.data(), 0, ins));
    vector<i64> a(S.A.N), b(S.A.N), ai(S.A.N), bi(S.A.N), na(S.A.N), nb(S.A.N);
    vector<i32> meetKey, cur;
    while (true) {
        if (radius[0] + radius[1] + 1 > maxRadius) {
            R.lower = radius[0] + radius[1] + 1; R.note = "radius cap"; break;
        }
        int side = front[0].size() <= front[1].size() ? 0 : 1;
        int other = 1 - side;
        if (T[0].count + T[1].count + front[side].size() * 14 > maxStates) {
            R.lower = radius[0] + radius[1] + 1; R.note = "state cap"; break;
        }
        vector<size_t> next;
        bool meet = false;
        for (size_t id : front[side]) {
            S.from_key(T[side].key(id), a, b);
            S.A.inverse(a.data(), ai.data());
            S.A.inverse(b.data(), bi.data());
            for (int m = 0; m < 15; m++) {
                S.move(a, b, ai, bi, m, na, nb);
                S.key_of(na, nb, k);
                size_t nid = T[side].insert(k.data(), (uint8_t)(radius[side] + 1), ins);
                if (!ins) continue;
                next.push_back(nid);
                if (!meet && T[other].find(k.data()) != SIZE_MAX) { meet = true; meetKey = k; }
            }
        }
        radius[side]++;
        front[side].swap(next);
        (side == 0 ? R.layersS : R.layersT).push_back(front[side].size());
        if (meet) {
            R.exact = true;
            R.distance = radius[0] + radius[1];
            // Reconstruct a path through meetKey by walking down both distance labels.
            vector<int> left, right;
            for (int sd = 0; sd < 2; sd++) {
                cur = meetKey;
                int d = T[sd].dist[T[sd].find(cur.data())];
                while (d > 0) {
                    S.from_key(cur.data(), a, b);
                    S.A.inverse(a.data(), ai.data());
                    S.A.inverse(b.data(), bi.data());
                    bool stepped = false;
                    for (int m = 0; m < 15 && !stepped; m++) {
                        S.move(a, b, ai, bi, m, na, nb);
                        S.key_of(na, nb, k);
                        size_t s3 = T[sd].find(k.data());
                        if (s3 != SIZE_MAX && T[sd].dist[s3] == d - 1) {
                            // start side: pred = m(cur), so pred -> cur is MOVE_INVERSE[m]
                            if (sd == 0) left.push_back(MOVE_INVERSE[m]);
                            else right.push_back(m);
                            cur = k; d--; stepped = true;
                        }
                    }
                    if (!stepped) throw runtime_error("path reconstruction failed");
                }
            }
            reverse(left.begin(), left.end());
            R.path = left;
            R.path.insert(R.path.end(), right.begin(), right.end());
            if ((int)R.path.size() != R.distance) throw runtime_error("path length mismatch");
            break;
        }
        if (front[side].empty()) { R.note = "component exhausted: distance infinite"; R.lower = -2; break; }
    }
    maxabs = S.A.maxabs;
    return R;
}

static Result free_bfs(const string s0, const string s1, const string t0, const string t1,
                       size_t maxStates, int maxRadius) {
    unordered_map<string, uint8_t> T[2];
    T[0].reserve(maxStates / 2); T[1].reserve(maxStates / 2);
    auto key = [](const string& a, const string& b) { return a + "|" + b; };
    auto split = [](const string& k, string& a, string& b) {
        size_t p = k.find('|'); a = k.substr(0, p); b = k.substr(p + 1);
    };
    vector<vector<const string*>> front(2);  // pointers to keys (node-stable map)
    int radius[2] = {0, 0};
    Result R;
    string ks = key(freduce(s0), freduce(s1)), kt = key(freduce(t0), freduce(t1));
    front[0].push_back(&T[0].emplace(ks, 0).first->first);
    R.layersS.push_back(1); R.layersT.push_back(1);
    if (ks == kt) { R.exact = true; R.distance = 0; return R; }
    front[1].push_back(&T[1].emplace(kt, 0).first->first);
    string a, b, na, nb, meet;
    while (true) {
        if (radius[0] + radius[1] + 1 > maxRadius) {
            R.lower = radius[0] + radius[1] + 1; R.note = "radius cap"; break;
        }
        int side = front[0].size() <= front[1].size() ? 0 : 1, other = 1 - side;
        if (T[0].size() + T[1].size() + front[side].size() * 14 > maxStates) {
            R.lower = radius[0] + radius[1] + 1; R.note = "state cap"; break;
        }
        vector<const string*> next;
        bool met = false;
        for (const string* kp : front[side]) {
            split(*kp, a, b);
            for (int m = 0; m < 15; m++) {
                free_move(a, b, m, na, nb);
                string k2 = key(na, nb);
                auto ins = T[side].emplace(std::move(k2), (uint8_t)(radius[side] + 1));
                if (!ins.second) continue;
                const string* np = &ins.first->first;
                if (!met && T[other].count(*np)) { met = true; meet = *np; }
                next.push_back(np);
            }
        }
        radius[side]++;
        front[side].swap(next);
        (side == 0 ? R.layersS : R.layersT).push_back(front[side].size());
        if (met) {
            R.exact = true;
            R.distance = radius[0] + radius[1];
            vector<int> left, right;
            for (int sd = 0; sd < 2; sd++) {
                string cur = meet;
                int d = T[sd][cur];
                while (d > 0) {
                    split(cur, a, b);
                    bool stepped = false;
                    for (int m = 0; m < 15 && !stepped; m++) {
                        free_move(a, b, m, na, nb);
                        auto it = T[sd].find(key(na, nb));
                        if (it != T[sd].end() && it->second == d - 1) {
                            if (sd == 0) left.push_back(MOVE_INVERSE[m]);
                            else right.push_back(m);
                            cur = key(na, nb); d--; stepped = true;
                        }
                    }
                    if (!stepped) throw runtime_error("path reconstruction failed");
                }
            }
            reverse(left.begin(), left.end());
            R.path = left;
            R.path.insert(R.path.end(), right.begin(), right.end());
            break;
        }
        if (front[side].empty()) { R.note = "component exhausted"; R.lower = -2; break; }
    }
    return R;
}

// Independent replay of a path in the free group (used to validate free paths).
static bool free_replay(string a, string b, const vector<int>& path, const string& t0,
                        const string& t1) {
    a = freduce(a); b = freduce(b);
    string na, nb;
    for (int m : path) { free_move(a, b, m, na, nb); a = na; b = nb; }
    return a == freduce(t0) && b == freduce(t1);
}

static string json_list(const vector<size_t>& v) {
    string s = "[";
    for (size_t i = 0; i < v.size(); i++) s += (i ? "," : "") + to_string(v[i]);
    return s + "]";
}
static string json_path(const vector<int>& p) {
    string s = "[";
    for (size_t i = 0; i < p.size(); i++) s += (i ? "," : "") + to_string(p[i]);
    return s + "]";
}

static long peak_rss_kb() {
    FILE* f = fopen("/proc/self/status", "r");
    if (!f) return -1;
    char line[256];
    long v = -1;
    while (fgets(line, sizeof line, f))
        if (strncmp(line, "VmHWM:", 6) == 0) v = atol(line + 6);
    fclose(f);
    return v;
}

static void print_result(const char* mode, int c, i64 mod, const string& s0, const string& s1,
                         const string& t0, const string& t1, const Result& R, i64 maxabs,
                         const string& label) {
    printf("{\"label\":\"%s\",\"mode\":\"%s\",\"class\":%d,\"mod\":%lld,"
           "\"start\":[\"%s\",\"%s\"],\"target\":[\"%s\",\"%s\"],",
           label.c_str(), mode, c, (long long)mod, s0.c_str(), s1.c_str(), t0.c_str(), t1.c_str());
    if (R.exact) printf("\"result\":\"exact\",\"distance\":%d,\"path\":%s,", R.distance,
                        json_path(R.path).c_str());
    else if (R.lower == -2) printf("\"result\":\"disconnected\",");
    else printf("\"result\":\"lower_bound\",\"distance_at_least\":%d,\"stop\":\"%s\",", R.lower,
                R.note.c_str());
    size_t tot = 0;
    for (size_t x : R.layersS) tot += x;
    for (size_t x : R.layersT) tot += x;
    printf("\"layers_from_start\":%s,\"layers_from_target\":%s,\"states_stored\":%zu,"
           "\"max_abs_coefficient\":%lld,\"peak_rss_kb\":%ld}\n",
           json_list(R.layersS).c_str(), json_list(R.layersT).c_str(), tot, (long long)maxabs,
           peak_rss_kb());
    fflush(stdout);
}

// ------------------------------------------------------------------ self-test
static int selftest() {
    int fails = 0;
    auto expect = [&](bool ok, const char* what) {
        if (!ok) { printf("FAIL: %s\n", what); fails++; }
    };
    // 1. Magnus map is a homomorphism and respects free reduction/inverses.
    srand(12345);
    for (int c = 1; c <= 6; c++) {
        Algebra A; A.init(c, 0);
        for (int trial = 0; trial < 50; trial++) {
            string u, v;
            for (int i = 0; i < 1 + rand() % 9; i++) u += GEN[rand() % 4];
            for (int i = 0; i < 1 + rand() % 9; i++) v += GEN[rand() % 4];
            vector<i64> mu = A.word(u), mv = A.word(v), muv = A.word(u + v), p(A.N),
                        ui(A.N), one(A.N);
            A.mul(mu.data(), mv.data(), p.data());
            expect(p == muv, "homomorphism");
            expect(A.word(freduce(u + v)) == muv, "free reduction invariance");
            A.inverse(mu.data(), ui.data());
            expect(ui == A.word(finv(u)), "inverse");
            A.mul(mu.data(), ui.data(), one.data());
            vector<i64> e(A.N, 0); e[0] = 1;
            expect(one == e, "u u^-1 = 1");
        }
    }
    // 2. Lower central series detection: left-normed commutator of weight k lies in
    //    gamma_k but not gamma_{k+1} (Magnus): image trivial at class k-1, nontrivial at k.
    {
        string w = "x";
        for (int k = 2; k <= 6; k++) {
            string g = (k % 2 == 0) ? "y" : "x";
            w = freduce(finv(w) + finv(g) + w + g);  // [w, g]
            Algebra lo; lo.init(k - 1, 0);
            Algebra hi; hi.init(k, 0);
            vector<i64> e1(lo.N, 0); e1[0] = 1;
            vector<i64> e2(hi.N, 0); e2[0] = 1;
            expect(lo.word(w) == e1, "commutator trivial below its weight");
            expect(hi.word(w) != e2, "commutator nontrivial at its weight");
        }
    }
    // 3. Tiny BFS facts.
    i64 mx;
    Result R = free_bfs("xy", "y", "x", "y", 100000, 20);
    expect(R.exact && R.distance == 1, "free distance (xy,y)->(x,y) is 1");
    R = free_bfs("y", "x", "x", "y", 100000, 20);
    expect(R.exact && R.distance == 1, "free swap distance 1");
    R = free_bfs("x", "y", "x", "y", 100000, 20);
    expect(R.exact && R.distance == 0, "distance 0");
    R = nil_bfs(3, 0, "yxY", "y", "x", "y", 100000, 20, mx);
    expect(R.exact && R.distance == 1, "nil: y x y^-1 -> x via one conjugation");
    // 4. Consistency: for random scrambles, free distance <= scramble length and
    //    nil distance (any class) <= free distance; free paths replay exactly.
    for (int trial = 0; trial < 20; trial++) {
        string a = "x", b = "y", na, nb;
        int L = 1 + rand() % 6;
        for (int i = 0; i < L; i++) { free_move(a, b, rand() % 15, na, nb); a = na; b = nb; }
        Result F = free_bfs(a, b, "x", "y", 2000000, 30);
        expect(F.exact && F.distance <= L, "scramble distance bound");
        expect(free_replay(a, b, F.path, "x", "y"), "free path replays");
        expect((int)F.path.size() == F.distance, "path length = distance");
        for (int c = 1; c <= 4; c++) {
            Result Q = nil_bfs(c, 0, a, b, "x", "y", 2000000, 30, mx);
            expect(Q.exact && Q.distance <= F.distance, "quotient distance <= free distance");
        }
        Result Q8 = nil_bfs(8, 0, a, b, "x", "y", 2000000, 30, mx);
        expect(Q8.exact && Q8.distance == F.distance, "high class matches free on short words");
    }
    // 5. Swapped start must not be treated as identical to target.
    R = nil_bfs(2, 0, "y", "x", "x", "y", 100000, 20, mx);
    expect(R.exact && R.distance == 1, "nil swap distance");
    printf("{\"selftest\":\"%s\",\"failures\":%d}\n", fails ? "FAILED" : "passed", fails);
    return fails ? 1 : 0;
}

int main(int argc, char** argv) {
    string mode = "nil", s0 = "xxxYYYY", s1 = "xyxYXY", t0 = "x", t1 = "y", label = "";
    int c = 2, maxRadius = 60;
    i64 mod = 0;
    size_t maxStates = 2000000;
    for (int i = 1; i < argc; i++) {
        string o = argv[i];
        auto nxt = [&]() { if (i + 1 >= argc) throw runtime_error("missing value"); return string(argv[++i]); };
        if (o == "--selftest") return selftest();
        else if (o == "--mode") mode = nxt();
        else if (o == "--class") c = stoi(nxt());
        else if (o == "--mod") mod = stoll(nxt());
        else if (o == "--start") { s0 = nxt(); s1 = nxt(); }
        else if (o == "--target") { t0 = nxt(); t1 = nxt(); }
        else if (o == "--max-states") maxStates = stoull(nxt());
        else if (o == "--max-radius") maxRadius = stoi(nxt());
        else if (o == "--label") label = nxt();
        else throw runtime_error("unknown option " + o);
    }
    check_word(s0); check_word(s1); check_word(t0); check_word(t1);
    if (mod < 0 || mod > INT32_MAX) throw runtime_error("bad modulus");
    if (mode == "nil") {
        if (c < 1 || c > 7) throw runtime_error("class must be 1..7");
        i64 mx = 0;
        Result R = nil_bfs(c, mod, s0, s1, t0, t1, maxStates, maxRadius, mx);
        print_result("nil", c, mod, s0, s1, t0, t1, R, mx, label);
    } else if (mode == "free") {
        Result R = free_bfs(s0, s1, t0, t1, maxStates, maxRadius);
        if (R.exact && !free_replay(s0, s1, R.path, t0, t1)) throw runtime_error("replay failed");
        print_result("free", 0, 0, s0, s1, t0, t1, R, 0, label);
    } else throw runtime_error("mode must be nil or free");
    return 0;
}
