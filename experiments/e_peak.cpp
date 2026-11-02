// e_peak.cpp -- exhaustive connected components of a balanced pair in the finite
// graph G_L whose vertices are ordered pairs (u,v) of freely reduced words in
// F(x,y) with |u|+|v| <= L, and whose edges are the 15 instructions of
// research-b.md / e_acdist.cpp (inversions, swap, a<-ab^{+-1}, b<-ba^{+-1},
// conjugation of either coordinate by x^{+-1}, y^{+-1}), restricted to G_L.
//
// The instruction set is closed under inverses and the length constraint is on
// vertices, so G_L is an undirected graph and BFS enumerates the whole component.
// If (x,y) is not in the component of U, every AC path from U to (x,y) built from
// these instructions -- in particular every ordinary-ac-elementary-v1 certificate,
// whose primitives are among them -- visits a pair of total length >= L+1.
//
// Standard library only.  Build: g++ -O2 -std=c++17 -o e_peak e_peak.cpp
// Encoding (exact, injective): bit 63 occupancy flag, |u| in bits 58..62, |v| in
// bits 53..57, letters x,X,y,Y -> 0,1,2,3 two bits each in the low bits.  L <= 26.
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>
#include <stdexcept>
#include <algorithm>
using namespace std;
typedef uint64_t u64;

static const char LET[4] = {'x', 'X', 'y', 'Y'};
static int code(char c) { return c == 'x' ? 0 : c == 'X' ? 1 : c == 'y' ? 2 : 3; }

// Store |u| (5 bits) and |v| (5 bits) explicitly: bits 63 flag, 58..62 |u|,
// 53..57 |v|, letters in low 2(|u|+|v|) <= 52 bits.  So L <= 26.
static u64 encodeT(const string& a, const string& b) {
    if (a.size() > 26 || b.size() > 26 || a.size() + b.size() > 26)
        throw runtime_error("too long to encode (L <= 26)");
    u64 k = (1ULL << 63) | ((u64)a.size() << 58) | ((u64)b.size() << 53);
    u64 bits = 0;
    for (char c : a) bits = (bits << 2) | code(c);
    for (char c : b) bits = (bits << 2) | code(c);
    return k | bits;
}
static void decodeT(u64 k, string& a, string& b) {
    int la = (int)((k >> 58) & 31), lb = (int)((k >> 53) & 31);
    u64 bits = k & ((1ULL << 53) - 1);
    a.assign(la, '?');
    b.assign(lb, '?');
    for (int i = lb - 1; i >= 0; i--) { b[i] = LET[bits & 3]; bits >>= 2; }
    for (int i = la - 1; i >= 0; i--) { a[i] = LET[bits & 3]; bits >>= 2; }
}

static string freduce(const string& w) {
    string out;
    for (char ch : w) {
        if (!out.empty() && out.back() == (char)(ch ^ 32)) out.pop_back();
        else out.push_back(ch);
    }
    return out;
}
static string finv(const string& w) {
    string r(w.rbegin(), w.rend());
    for (char& ch : r) ch ^= 32;
    return r;
}
static void move(const string& a, const string& b, int m, string& na, string& nb) {
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
            string g(1, LET[k]), gi(1, (char)(LET[k] ^ 32));
            if (m < 11) na = freduce(gi + a + g);
            else nb = freduce(gi + b + g);
        }
    }
}

struct Set64 {
    vector<u64> t;
    size_t n = 0;
    void init() { t.assign(1 << 16, 0); n = 0; }
    static u64 h(u64 k) { k ^= k >> 33; k *= 0xff51afd7ed558ccdULL; k ^= k >> 33; k *= 0xc4ceb9fe1a85ec53ULL; k ^= k >> 33; return k; }
    void grow() {
        vector<u64> o(t.size() * 2, 0);
        size_t m = o.size() - 1;
        for (u64 k : t) if (k) { size_t s = h(k) & m; while (o[s]) s = (s + 1) & m; o[s] = k; }
        t.swap(o);
    }
    bool insert(u64 k) {  // true if new
        if ((n + 1) * 2 > t.size()) grow();
        size_t m = t.size() - 1, s = h(k) & m;
        while (t[s]) { if (t[s] == k) return false; s = (s + 1) & m; }
        t[s] = k; n++;
        return true;
    }
    bool contains(u64 k) const {
        size_t m = t.size() - 1, s = h(k) & m;
        while (t[s]) { if (t[s] == k) return true; s = (s + 1) & m; }
        return false;
    }
};

static long peak_rss_kb() {
    FILE* f = fopen("/proc/self/status", "r");
    if (!f) return -1;
    char line[256]; long v = -1;
    while (fgets(line, sizeof line, f)) if (strncmp(line, "VmHWM:", 6) == 0) v = atol(line + 6);
    fclose(f);
    return v;
}

static const int MOVE_INVERSE[15] = {0, 1, 2, 4, 3, 6, 5, 8, 7, 10, 9, 12, 11, 14, 13};

struct Comp {
    vector<int> path;  // shortest instruction path inside G_L (only with --path)
    bool reached = false, complete = false;
    size_t size = 0;
    int reachDepth = -1;
    vector<size_t> layers;
    size_t byLen[27] = {0};
    size_t minTotal = 1000;
};

// BFS of the component of (s0,s1) in G_L; stops early only at the state cap.
static FILE* g_dump = nullptr;
static int g_dumpT = -1;
// --canon T: collect complex classes of component states of total length <= T.
// Class = cyclic reduction of both relators, then the minimum over the 8 signed
// permutations of {x,y}, cyclic rotations and inversion of each relator, and
// relator order (same normalization as e_thicken_check.py's canon()).
#include <set>
static int g_canonT = -1;
static std::set<string>* g_classes = nullptr;
static string cyc_reduce(string w) {
    w = freduce(w);
    size_t i = 0, j = w.size();
    while (j - i >= 2 && w[i] == (char)(w[j - 1] ^ 32)) { i++; j--; }
    return w.substr(i, j - i);
}
static string min_rot(const string& w) {
    string best = w, iw = finv(w);
    for (const string& v : {w, iw})
        for (size_t k = 0; k < v.size(); k++) {
            string r = v.substr(k) + v.substr(0, k);
            if (r.size() < best.size() || (r.size() == best.size() && r < best)) best = r;
        }
    return best;
}
static string canon_class(const string& a0, const string& b0) {
    string a = cyc_reduce(a0), b = cyc_reduce(b0), best;
    for (int sw = 0; sw < 2; sw++)
        for (int sx = 0; sx < 2; sx++)
            for (int sy = 0; sy < 2; sy++) {
                auto img = [&](const string& w) {
                    string o = w;
                    for (char& c : o) {
                        bool isx = (c == 'x' || c == 'X'), pos = (c == 'x' || c == 'y');
                        if (isx ? sx : sy) pos = !pos;
                        if (sw) isx = !isx;
                        c = isx ? (pos ? 'x' : 'X') : (pos ? 'y' : 'Y');
                    }
                    return min_rot(o);
                };
                string u = img(a), v = img(b);
                auto lt = [](const string& p, const string& q) { return p.size() < q.size() || (p.size() == q.size() && p < q); };
                if (lt(v, u)) swap(u, v);
                string key = u + " " + v;
                if (best.empty() || lt(key, best)) best = key;
            }
    return best;
}
static Comp component(const string& s0, const string& s1, int L, size_t cap,
                      const string& t0, const string& t1, bool wantPath = false) {
    vector<vector<u64>> layers;  // kept only when wantPath
    Comp C;
    Set64 S; S.init();
    u64 target = encodeT(freduce(t0), freduce(t1));
    vector<u64> cur, nxt;
    u64 k0 = encodeT(freduce(s0), freduce(s1));
    if ((int)(s0.size() + s1.size()) > L) throw runtime_error("start longer than L");
    S.insert(k0); cur.push_back(k0);
    C.layers.push_back(1);
    if (wantPath) layers.push_back(cur);
    string a, b, na, nb;
    int depth = 0;
    auto note = [&](u64 k) {
        int t = (int)(((k >> 58) & 31) + ((k >> 53) & 31));
        if (g_dump && t <= g_dumpT) { string da, db; decodeT(k, da, db); fprintf(g_dump, "%s %s\n", da.c_str(), db.c_str()); }
        if (g_classes && t <= g_canonT) { string da, db; decodeT(k, da, db); g_classes->insert(canon_class(da, db)); }
        C.byLen[t]++;
        if ((size_t)t < C.minTotal) C.minTotal = t;
    };
    note(k0);
    if (k0 == target) { C.reached = true; C.reachDepth = 0; }
    while (!cur.empty()) {
        nxt.clear();
        for (u64 k : cur) {
            decodeT(k, a, b);
            for (int m = 0; m < 15; m++) {
                move(a, b, m, na, nb);
                if ((int)(na.size() + nb.size()) > L) continue;
                u64 k2 = encodeT(na, nb);
                if (S.insert(k2)) {
                    nxt.push_back(k2);
                    note(k2);
                    if (k2 == target && !C.reached) { C.reached = true; C.reachDepth = depth + 1; }
                }
            }
            if (S.n > cap) { C.size = S.n; return C; }
        }
        depth++;
        cur.swap(nxt);
        if (!cur.empty()) C.layers.push_back(cur.size());
        if (wantPath) {
            layers.push_back(cur);
            if (C.reached) {  // reconstruct a shortest path start -> target inside G_L
                for (auto& lay : layers) sort(lay.begin(), lay.end());
                u64 at = target;
                for (int d = C.reachDepth - 1; d >= 0; d--) {
                    decodeT(at, a, b);
                    bool stepped = false;
                    for (int m = 0; m < 15 && !stepped; m++) {
                        move(a, b, m, na, nb);
                        if ((int)(na.size() + nb.size()) > L) continue;
                        u64 kk = encodeT(na, nb);
                        if (binary_search(layers[d].begin(), layers[d].end(), kk)) {
                            C.path.insert(C.path.begin(), MOVE_INVERSE[m]);
                            at = kk; stepped = true;
                        }
                    }
                    if (!stepped) throw runtime_error("path reconstruction failed");
                }
                C.size = S.n;
                return C;  // component not completed in path mode
            }
        }
    }
    C.complete = true;
    C.size = S.n;
    return C;
}

static void report(const string& label, const string& s0, const string& s1, int L, const Comp& C) {
    printf("{\"label\":\"%s\",\"start\":[\"%s\",\"%s\"],\"L\":%d,\"component_complete\":%s,"
           "\"component_size\":%zu,\"contains_xy\":%s,\"bfs_depth_to_xy\":%d,\"min_total_length\":%zu,"
           "\"bfs_radius\":%zu,\"count_by_total_length\":{",
           label.c_str(), s0.c_str(), s1.c_str(), L, C.complete ? "true" : "false", C.size,
           C.reached ? "true" : "false", C.reachDepth, C.minTotal, C.layers.size() - 1);
    bool first = true;
    for (int t = 0; t <= 26; t++)
        if (C.byLen[t]) { printf("%s\"%d\":%zu", first ? "" : ",", t, C.byLen[t]); first = false; }
    printf("},\"path\":[");
    for (size_t i = 0; i < C.path.size(); i++) printf("%s%d", i ? "," : "", C.path[i]);
    printf("],\"peak_rss_kb\":%ld}\n", peak_rss_kb());
    fflush(stdout);
}

static int selftest() {
    int fails = 0;
    auto expect = [&](bool ok, const char* w) { if (!ok) { printf("FAIL %s\n", w); fails++; } };
    // encoding round trip
    const char* ws[] = {"", "x", "XyYx", "xxxYYYY", "yXyXyXyXyXyX"};
    for (const char* u : ws) for (const char* v : ws) {
        string a, b; decodeT(encodeT(u, v), a, b);
        expect(a == u && b == v, "encode/decode");
    }
    // (xy,y) reaches (x,y) inside L=3; component of (x,y) at L=2 is the 8 signed
    // generator pairs (x^{+-1},y^{+-1}) and their swaps: 8 states? (x,y),(X,y),(x,Y),(X,Y),
    // (y,x),(Y,x),(y,X),(Y,X); conjugations by generators keep length 2 only when
    // conjugating a letter by itself or its inverse (no change) -> 8 states.
    Comp C = component("x", "y", 2, 1000000, "x", "y");
    expect(C.complete && C.size == 8 && C.reached, "L=2 component of (x,y) has 8 states");
    C = component("xy", "y", 3, 1000000, "x", "y");
    expect(C.complete && C.reached, "(xy,y) reaches (x,y) within L=3");
    // A presentation of a nontrivial group (Z/2 x Z): (xx, xyXY) never reaches (x,y).
    C = component("xx", "xyXY", 12, 50000000, "x", "y");
    expect(C.complete && !C.reached, "(x^2,[x,y]) does not reach (x,y) at L=12 (control)");
    // AK(3) at L=13: research-a.md bounds the nonincreasing component by
    // 2 * (|Orb(p_3)|+|Orb(q_3)|) * |Orb(b)| = 2*28*12 = 672 ordered pairs; with ordinary
    // letter conjugations only the Orb(p_3) half is reachable: 2*14*12 = 336.
    C = component("xxxYYYY", "xyxYXY", 13, 1000000, "x", "y");
    expect(C.complete && C.size == 336 && !C.reached, "AK(3) L=13 component = 2*14*12 = 336");
    printf("{\"selftest\":\"%s\",\"failures\":%d}\n", fails ? "FAILED" : "passed", fails);
    return fails ? 1 : 0;
}

int main(int argc, char** argv) {
    string s0 = "xxxYYYY", s1 = "xyxYXY", label = "";
    int L = 14;
    size_t cap = 100000000;
    bool wantPath = false;
    int dumpT = -1;  // with --dump T: print every component state of total length <= T
    for (int i = 1; i < argc; i++) {
        string o = argv[i];
        auto nx = [&]() { if (i + 1 >= argc) throw runtime_error("missing value"); return string(argv[++i]); };
        if (o == "--selftest") return selftest();
        else if (o == "--start") { s0 = nx(); s1 = nx(); }
        else if (o == "--L") L = stoi(nx());
        else if (o == "--cap") cap = stoull(nx());
        else if (o == "--label") label = nx();
        else if (o == "--path") wantPath = true;
        else if (o == "--dump") dumpT = stoi(nx());
        else if (o == "--canon") g_canonT = stoi(nx());
        else throw runtime_error("unknown option " + o);
    }
    if (L > 26) throw runtime_error("L must be <= 26");
    if (dumpT >= 0) { g_dump = stderr; g_dumpT = dumpT; }
    std::set<string> classes;
    if (g_canonT >= 0) g_classes = &classes;
    Comp C = component(s0, s1, L, cap, "x", "y", wantPath);
    if (g_classes) for (const string& c : classes) fprintf(stderr, "%s\n", c.c_str());
    report(label, s0, s1, L, C);
    return 0;
}
