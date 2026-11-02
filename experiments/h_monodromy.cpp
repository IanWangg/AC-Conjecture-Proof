// h_monodromy.cpp -- AC-monodromy of a finite 2-generated group G (research note H).
//
// Theory (research/research-h.md, Section 3).  Let pi: F(x,y) -> G be onto, G finite, and
// Q_G = G x_{G_ab} Z^2 = F / (ker(pi) cap [F,F]) the abelian fibre product.  The 15 AC
// instructions generate a group  A  acting on G^2; mu: A -> GL2(Z) records the action on
// exponent vectors (conjugations |-> I).  Z = ker(mu).  C = A-orbit of (pi x, pi y).
// Then GL2(Z) acts transitively on C/Z with point stabiliser Lambda_G (monodromy group), and
//     Lambda_G  <=  Gamma := Stab_{GL2(Z)}(image of (x,y) in G_ab^2),
//     [GL2(Z):Lambda_G] = |C/Z|,   [GL2(Z):Gamma] = |O_ab|  (GL2(Z)-orbit in G_ab^2).
// A normally generating pair U of F is AC-equivalent to (x,y) in Q_G iff
//     [pi(U)] == [pi(B_U)] in C/Z,   B_U any basis of F with the exponent matrix of U.
// If |C/Z| == |O_ab| then Lambda_G == Gamma and Q_G obstructs no pair at all.
//
// C/Z is computed as the congruence closure (under the 7 Nielsen instructions) of the relation
// c ~ conj_g^{(i)}(c).  Input (stdin):
//   n                      degree of the permutation representation
//   a_0 ... a_{n-1}        image list of pi(x)   (0-based)
//   b_0 ... b_{n-1}        image list of pi(y)
//   then any number of lines  "name w0 w1"  (words over x,X,y,Y) to test.
// Usage:  h_monodromy [--max-order N] < input      |   h_monodromy --selftest
// Product convention: (p*q)[i] = q[p[i]]  (left-to-right evaluation of words).
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstring>
#include <string>
#include <vector>
#include <unordered_map>
#include <iostream>
#include <sstream>
#include <algorithm>
#include <random>
using namespace std;

struct Group {
    int n = 0, G = 0;
    vector<uint16_t> perms;            // G*n
    vector<int> rgen[4];               // right multiplication by x, X, y, Y
    vector<uint16_t> mul;              // G*G
    vector<int> inv;
    int id = 0, gx = 0, gX = 0, gy = 0, gY = 0;
};

static string key(const uint16_t* p, int n) { return string((const char*)p, 2 * n); }

static bool build(Group& g, const vector<int>& a, const vector<int>& b, int maxorder) {
    int n = g.n;
    vector<uint16_t> A(n), B(n), Ai(n), Bi(n), I(n);
    for (int i = 0; i < n; i++) { A[i] = a[i]; B[i] = b[i]; I[i] = i; }
    for (int i = 0; i < n; i++) { Ai[a[i]] = i; Bi[b[i]] = i; }
    const vector<uint16_t>* gens[4] = {&A, &Ai, &B, &Bi};
    unordered_map<string, int> idx;
    g.perms.assign(I.begin(), I.end());
    idx[key(I.data(), n)] = 0;
    vector<int> parent(1, -1), pgen(1, -1);
    for (int k = 0; k < 4; k++) g.rgen[k].clear();
    vector<uint16_t> tmp(n);
    for (size_t head = 0; head < parent.size(); head++) {
        for (int k = 0; k < 4; k++) {
            const uint16_t* p = &g.perms[head * n];
            for (int i = 0; i < n; i++) tmp[i] = (*gens[k])[p[i]];
            auto it = idx.find(key(tmp.data(), n));
            if (it == idx.end()) {
                int id = (int)parent.size();
                if (id >= maxorder) return false;
                idx[key(tmp.data(), n)] = id;
                g.perms.insert(g.perms.end(), tmp.begin(), tmp.end());
                parent.push_back((int)head); pgen.push_back(k);
            }
        }
    }
    g.G = (int)parent.size();
    int G = g.G;
    for (int k = 0; k < 4; k++) {
        g.rgen[k].assign(G, 0);
        for (int e = 0; e < G; e++) {
            const uint16_t* p = &g.perms[(size_t)e * n];
            for (int i = 0; i < n; i++) tmp[i] = (*gens[k])[p[i]];
            g.rgen[k][e] = idx.at(key(tmp.data(), n));
        }
    }
    g.id = 0; g.gx = g.rgen[0][0]; g.gX = g.rgen[1][0]; g.gy = g.rgen[2][0]; g.gY = g.rgen[3][0];
    // mul[i*G+j] = e_i * e_j, via the BFS tree: e_j = e_parent(j) * gen
    g.mul.assign((size_t)G * G, 0);
    for (int i = 0; i < G; i++) {
        g.mul[(size_t)i * G + 0] = i;
        for (int j = 1; j < G; j++)
            g.mul[(size_t)i * G + j] = g.rgen[pgen[j]][g.mul[(size_t)i * G + parent[j]]];
    }
    g.inv.assign(G, -1);
    for (int i = 0; i < G; i++)
        for (int j = 0; j < G; j++)
            if (g.mul[(size_t)i * G + j] == 0) { g.inv[i] = j; break; }
    return true;
}

static inline int M(const Group& g, int i, int j) { return g.mul[(size_t)i * g.G + j]; }

// the 15 instructions; ids: 0,1 invert; 2 swap; 3,4 u0<-u0 u1^{+-1}; 5,6 u1<-u1 u0^{+-1};
// 7..10 u0 <- h^-1 u0 h, h = x,X,y,Y; 11..14 same on u1.  mu = I for ids >= 7.
static inline void apply(const Group& g, int k, int& u0, int& u1) {
    switch (k) {
        case 0: u0 = g.inv[u0]; break;
        case 1: u1 = g.inv[u1]; break;
        case 2: swap(u0, u1); break;
        case 3: u0 = M(g, u0, u1); break;
        case 4: u0 = M(g, u0, g.inv[u1]); break;
        case 5: u1 = M(g, u1, u0); break;
        case 6: u1 = M(g, u1, g.inv[u0]); break;
        default: {
            int hs[4] = {g.gx, g.gX, g.gy, g.gY};
            int h = hs[(k - 7) % 4];
            int& u = (k < 11) ? u0 : u1;
            u = M(g, M(g, g.inv[h], u), h);
        }
    }
}

static int evalword(const Group& g, const string& w) {
    int e = 0;
    for (char c : w) {
        int k = c == 'x' ? 0 : c == 'X' ? 1 : c == 'y' ? 2 : c == 'Y' ? 3 : -1;
        if (k < 0) { fprintf(stderr, "bad letter %c\n", c); exit(2); }
        e = g.rgen[k][e];
    }
    return e;
}

struct UF {
    vector<int> p;
    explicit UF(int n) : p(n) { for (int i = 0; i < n; i++) p[i] = i; }
    int f(int x) { while (p[x] != x) { p[x] = p[p[x]]; x = p[x]; } return x; }
    bool u(int a, int b) { a = f(a); b = f(b); if (a == b) return false; if (a < b) swap(a, b); p[a] = b; return true; }
};

struct Result {
    long long G, C, classes, Oab, Gab;
    bool ok_image;
};

struct Analysis {
    Group g;
    vector<int> cid;          // pair -> index in C or -1
    vector<uint32_t> Cl;      // C list
    UF* uf = nullptr;
    vector<int> coset;        // element -> coset of [G,G]
    Result r{};
};

static void analyse(Analysis& an) {
    Group& g = an.g;
    long long G = g.G, GG = G * G;
    an.cid.assign(GG, -1);
    int s0 = g.gx, s1 = g.gy;
    uint32_t start = (uint32_t)(s0 * G + s1);
    an.cid[start] = 0; an.Cl.assign(1, start);
    for (size_t h = 0; h < an.Cl.size(); h++) {
        int u0 = an.Cl[h] / G, u1 = an.Cl[h] % G;
        for (int k = 0; k < 15; k++) {
            int v0 = u0, v1 = u1; apply(g, k, v0, v1);
            uint32_t c = (uint32_t)(v0 * G + v1);
            if (an.cid[c] < 0) { an.cid[c] = (int)an.Cl.size(); an.Cl.push_back(c); }
        }
    }
    int Cn = (int)an.Cl.size();
    an.uf = new UF(Cn);
    UF& uf = *an.uf;
    vector<pair<int,int>> q;
    for (int c = 0; c < Cn; c++) {
        int u0 = an.Cl[c] / G, u1 = an.Cl[c] % G;
        for (int k = 7; k < 15; k++) {
            int v0 = u0, v1 = u1; apply(g, k, v0, v1);
            int d = an.cid[(uint32_t)(v0 * G + v1)];
            if (uf.u(c, d)) q.push_back({c, d});
        }
    }
    while (!q.empty()) {
        auto [c, d] = q.back(); q.pop_back();
        int a0 = an.Cl[c] / G, a1 = an.Cl[c] % G, b0 = an.Cl[d] / G, b1 = an.Cl[d] % G;
        for (int k = 0; k < 7; k++) {
            int x0 = a0, x1 = a1, y0 = b0, y1 = b1;
            apply(g, k, x0, x1); apply(g, k, y0, y1);
            int e = an.cid[(uint32_t)(x0 * G + x1)], f = an.cid[(uint32_t)(y0 * G + y1)];
            if (uf.u(e, f)) q.push_back({e, f});
        }
    }
    long long classes = 0;
    for (int c = 0; c < Cn; c++) if (uf.f(c) == c) classes++;
    // derived subgroup D = normal closure of [x,y] = XYxy
    int comm = M(g, M(g, M(g, g.gX, g.gY), g.gx), g.gy);
    vector<char> inD(G, 0), inCl(G, 0);
    vector<int> cls{comm}; inCl[comm] = 1;
    for (size_t h = 0; h < cls.size(); h++)
        for (int hh : {g.gx, g.gX, g.gy, g.gY}) {
            int c = M(g, M(g, g.inv[hh], cls[h]), hh);
            if (!inCl[c]) { inCl[c] = 1; cls.push_back(c); }
        }
    vector<int> D{0}; inD[0] = 1;
    for (size_t h = 0; h < D.size(); h++)
        for (int c : cls) { int e = M(g, D[h], c); if (!inD[e]) { inD[e] = 1; D.push_back(e); } }
    an.coset.assign(G, -1);
    int ncos = 0; vector<int> rep;
    for (int e = 0; e < G; e++) if (an.coset[e] < 0) {
        for (int d : D) an.coset[M(g, e, d)] = ncos;
        rep.push_back(e); ncos++;
    }
    // G_ab multiplication table
    vector<int> amul((size_t)ncos * ncos), ainv(ncos);
    for (int i = 0; i < ncos; i++) for (int j = 0; j < ncos; j++)
        amul[(size_t)i * ncos + j] = an.coset[M(g, rep[i], rep[j])];
    for (int i = 0; i < ncos; i++) ainv[i] = an.coset[g.inv[rep[i]]];
    // O_ab: Nielsen orbit of (x,y) in G_ab^2
    vector<char> seen((size_t)ncos * ncos, 0);
    vector<int> ob{an.coset[s0] * ncos + an.coset[s1]}; seen[ob[0]] = 1;
    for (size_t h = 0; h < ob.size(); h++) {
        int p0 = ob[h] / ncos, p1 = ob[h] % ncos;
        int nx[7][2] = {{ainv[p0], p1}, {p0, ainv[p1]}, {p1, p0},
                        {amul[(size_t)p0 * ncos + p1], p1}, {amul[(size_t)p0 * ncos + ainv[p1]], p1},
                        {p0, amul[(size_t)p1 * ncos + p0]}, {p0, amul[(size_t)p1 * ncos + ainv[p0]]}};
        for (auto& v : nx) { int c = v[0] * ncos + v[1]; if (!seen[c]) { seen[c] = 1; ob.push_back(c); } }
    }
    // image of C in G_ab^2 must equal O_ab
    vector<char> img((size_t)ncos * ncos, 0); long long nimg = 0;
    for (int c = 0; c < Cn; c++) {
        int p = an.coset[an.Cl[c] / G] * ncos + an.coset[an.Cl[c] % G];
        if (!img[p]) { img[p] = 1; nimg++; }
    }
    bool ok = (nimg == (long long)ob.size());
    for (int c : ob) if (!img[c]) ok = false;
    an.r = {G, Cn, classes, (long long)ob.size(), ncos, ok};
}

// exponent sums
static void expo(const string& w, long long& ex, long long& ey) {
    ex = ey = 0;
    for (char c : w) { if (c == 'x') ex++; if (c == 'X') ex--; if (c == 'y') ey++; if (c == 'Y') ey--; }
}

// Row-reduce the exponent matrix [[p,q],[r,s]] (rows = exponent vectors) to I with Nielsen
// operations; returns ops in the 7-instruction numbering (0..6), op list o_1..o_k with
// o_k...o_1 (M) = I.  Returns false if |det| != 1.
static bool reduce_ops(long long p, long long q, long long r, long long s, vector<int>& ops) {
    ops.clear();
    long long m[2][2] = {{p, q}, {r, s}};
    if (llabs(p * s - q * r) != 1) return false;
    auto rowop = [&](int k) {
        switch (k) {
            case 0: m[0][0] = -m[0][0]; m[0][1] = -m[0][1]; break;
            case 1: m[1][0] = -m[1][0]; m[1][1] = -m[1][1]; break;
            case 2: swap(m[0][0], m[1][0]); swap(m[0][1], m[1][1]); break;
            case 3: m[0][0] += m[1][0]; m[0][1] += m[1][1]; break;
            case 4: m[0][0] -= m[1][0]; m[0][1] -= m[1][1]; break;
            case 5: m[1][0] += m[0][0]; m[1][1] += m[0][1]; break;
            case 6: m[1][0] -= m[0][0]; m[1][1] -= m[0][1]; break;
        }
        ops.push_back(k);
    };
    // Euclid on first column
    int guard = 0;
    while (m[1][0] != 0) {
        if (++guard > 100000) return false;
        if (llabs(m[0][0]) < llabs(m[1][0])) { rowop(2); continue; }
        // m0 -= sign * m1 until |m0| < |m1|
        bool same = (m[0][0] > 0) == (m[1][0] > 0);
        rowop(same ? 4 : 3);
    }
    if (m[0][0] < 0) rowop(0);           // now m00 = 1
    if (m[1][1] < 0) rowop(1);           // m11 = 1 (det = +-1, m10 = 0)
    while (m[0][1] != 0) rowop(m[0][1] > 0 ? 4 : 3);
    return m[0][0] == 1 && m[1][1] == 1 && m[0][1] == 0 && m[1][0] == 0;
}

static const int INV7[7] = {0, 1, 2, 4, 3, 6, 5};

// G-image of a basis of F whose exponent matrix equals that of (w0,w1)
static bool basis_image(const Group& g, const string& w0, const string& w1, int& b0, int& b1) {
    long long p, q, r, s; expo(w0, p, q); expo(w1, r, s);
    vector<int> ops;
    if (!reduce_ops(p, q, r, s, ops)) return false;
    b0 = g.gx; b1 = g.gy;
    for (int i = (int)ops.size() - 1; i >= 0; i--) apply(g, INV7[ops[i]], b0, b1);
    return true;
}

// test: 1 = AC-trivial in Q_G, 0 = NOT (obstruction!), -1 = pi(U) not in C, -2 = |det| != 1
static int test_pair(Analysis& an, const string& w0, const string& w1) {
    const Group& g = an.g;
    int u0 = evalword(g, w0), u1 = evalword(g, w1);
    int c = an.cid[(uint32_t)(u0 * g.G + u1)];
    if (c < 0) return -1;
    int b0, b1;
    if (!basis_image(g, w0, w1, b0, b1)) return -2;
    int d = an.cid[(uint32_t)(b0 * g.G + b1)];
    if (d < 0) return -1;
    return an.uf->f(c) == an.uf->f(d) ? 1 : 0;
}

// free-group helpers for the self-test
static string red(const string& w) {
    string o;
    for (char c : w) {
        char ic = (c == 'x') ? 'X' : (c == 'X') ? 'x' : (c == 'y') ? 'Y' : 'y';
        if (!o.empty() && o.back() == ic) o.pop_back(); else o.push_back(c);
    }
    return o;
}
static string finv(const string& w) {
    string o(w.rbegin(), w.rend());
    for (char& c : o) c = (c == 'x') ? 'X' : (c == 'X') ? 'x' : (c == 'y') ? 'Y' : 'y';
    return o;
}
static void fapply(int k, string& u0, string& u1) {
    static const char* H = "xXyY";
    switch (k) {
        case 0: u0 = finv(u0); break;
        case 1: u1 = finv(u1); break;
        case 2: swap(u0, u1); break;
        case 3: u0 = red(u0 + u1); break;
        case 4: u0 = red(u0 + finv(u1)); break;
        case 5: u1 = red(u1 + u0); break;
        case 6: u1 = red(u1 + finv(u0)); break;
        default: {
            string h(1, H[(k - 7) % 4]);
            string& u = (k < 11) ? u0 : u1;
            u = red(finv(h) + u + h);
        }
    }
}

static vector<int> perm_from_cycles(int n, const vector<vector<int>>& cyc) {
    vector<int> p(n); for (int i = 0; i < n; i++) p[i] = i;
    for (auto& c : cyc) for (size_t i = 0; i < c.size(); i++) p[c[i]] = c[(i + 1) % c.size()];
    return p;
}

static int selftest() {
    int fails = 0;
    // (1) reduce_ops / basis_image consistency on random unimodular matrices
    mt19937_64 rng(12345);
    for (int t = 0; t < 2000; t++) {
        string u0 = "x", u1 = "y";
        int len = rng() % 30;
        for (int i = 0; i < len; i++) fapply(rng() % 7, u0, u1);
        long long p, q, r, s; expo(u0, p, q); expo(u1, r, s);
        vector<int> ops;
        if (!reduce_ops(p, q, r, s, ops)) { fails++; continue; }
    }
    // (2) groups: A5 (perfect: expect |C/Z| = 1), S4 (solvable), S5
    struct Case { const char* name; int n; vector<vector<int>> ca, cb; };
    vector<Case> cases = {
        {"A5", 5, {{0, 1, 2}}, {{0, 1, 2, 3, 4}}},
        {"S5", 5, {{0, 1}}, {{0, 1, 2, 3, 4}}},
        {"S4", 4, {{0, 1}}, {{0, 1, 2, 3}}},
        {"C6", 6, {{0, 1, 2, 3, 4, 5}}, {}},
    };
    for (auto& cs : cases) {
        Analysis an; an.g.n = cs.n;
        if (!build(an.g, perm_from_cycles(cs.n, cs.ca), perm_from_cycles(cs.n, cs.cb), 1 << 20)) { fails++; continue; }
        analyse(an);
        printf("selftest %s: |G|=%lld |C|=%lld |C/Z|=%lld |O_ab|=%lld |G_ab|=%lld image_ok=%d\n", cs.name,
               an.r.G, an.r.C, an.r.classes, an.r.Oab, an.r.Gab, (int)an.r.ok_image);
        if (!an.r.ok_image) fails++;
        if (an.r.classes < an.r.Oab) fails++;           // Lambda <= Gamma forces >=
        if (string(cs.name) == "A5" && an.r.classes != 1) fails++;
        // (3) random AC-trivial pairs (instruction sequences from (x,y) in F) must test trivial
        for (int t = 0; t < 300; t++) {
            string u0 = "x", u1 = "y";
            int len = 1 + rng() % 12;
            for (int i = 0; i < len; i++) fapply(rng() % 15, u0, u1);
            if (u0.size() + u1.size() > 400) continue;
            int res = test_pair(an, u0, u1);
            if (res != 1) { fails++; printf("  FAIL trivial pair %s %s -> %d\n", u0.c_str(), u1.c_str(), res); }
        }
        // known AC-trivial presentations
        for (auto pr : vector<pair<string,string>>{{"xYY", "xyxYXY"}, {"xxYYY", "xyxYXY"}}) {
            int res = test_pair(an, pr.first, pr.second);
            if (res != 1) { fails++; printf("  FAIL AK control %s %s -> %d\n", pr.first.c_str(), pr.second.c_str(), res); }
        }
        delete an.uf;
    }
    printf(fails ? "SELFTEST FAILED (%d)\n" : "selftest passed\n", fails);
    return fails ? 1 : 0;
}

int main(int argc, char** argv) {
    int maxorder = 20000;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--selftest")) return selftest();
        if (!strcmp(argv[i], "--max-order") && i + 1 < argc) maxorder = atoi(argv[++i]);
    }
    Analysis an;
    if (!(cin >> an.g.n)) { fprintf(stderr, "no input\n"); return 2; }
    vector<int> a(an.g.n), b(an.g.n);
    for (auto& v : a) cin >> v;
    for (auto& v : b) cin >> v;
    if (!build(an.g, a, b, maxorder)) { printf("{\"error\":\"order exceeds max\"}\n"); return 3; }
    analyse(an);
    printf("{\"order\":%lld,\"C\":%lld,\"classes\":%lld,\"Oab\":%lld,\"Gab\":%lld,\"image_ok\":%d,\"Lambda_eq_Gamma\":%d",
           an.r.G, an.r.C, an.r.classes, an.r.Oab, an.r.Gab, (int)an.r.ok_image, (int)(an.r.classes == an.r.Oab));
    string line, name, w0, w1;
    printf(",\"tests\":{");
    bool first = true;
    getline(cin, line);
    while (getline(cin, line)) {
        istringstream is(line);
        if (!(is >> name >> w0 >> w1)) continue;
        int res = test_pair(an, w0, w1);
        printf("%s\"%s\":%d", first ? "" : ",", name.c_str(), res);
        first = false;
    }
    printf("}}\n");
    delete an.uf;
    return 0;
}
