// e_thicken.cpp -- exact test of whether the presentation 2-complex of a one-vertex
// presentation <x,y | r_1,...,r_k> embeds in some 3-manifold ("thickenable").
//
// Criterion (research-e.md, Section 6; classical, cf. Osborne-Stevens / Neuwirth):
// K thickens iff there are (a) a cyclic order pi_g of the occurrences of g^{+-1} for
// each generator g, giving the rotation at the link vertex g+, (b) a handle type
// t_g in {orientable, non-orientable}, with rotation at g- equal to pi_g^{-1}
// (orientable 1-handle) or pi_g (non-orientable 1-handle), such that
//   (1) the link graph with this rotation system is planar (every component genus 0),
//   (2) every relator passes an even number of times through non-orientable handles
//       (so its attaching curve has an annular neighbourhood).
// The program enumerates all (a),(b) exhaustively; (d_g - 1)! orders per generator.
//
// Input (stdin): one presentation per line, relators separated by spaces, letters
// x,X,y,Y.  Output: one JSON line per presentation.
// Build: g++ -O2 -std=c++17 -o e_thicken e_thicken.cpp ;  ./e_thicken --selftest
#include <cstdio>
#include <cstdint>
#include <string>
#include <vector>
#include <sstream>
#include <iostream>
#include <algorithm>
#include <numeric>
#include <stdexcept>
#include <array>
#include <functional>
using namespace std;

struct Pres {
    vector<string> rel;
};

struct Result {
    bool thick = false;
    long long tried = 0;
    vector<vector<int>> order;  // witness cyclic orders (occurrence ids)
    int types = -1;             // bit g set = non-orientable handle for generator g
};

static Result test(const Pres& P) {
    // occurrences
    vector<int> gen, sgn, relOf;
    vector<vector<int>> relOcc(P.rel.size());
    for (size_t i = 0; i < P.rel.size(); i++)
        for (char c : P.rel[i]) {
            int g = (c == 'x' || c == 'X') ? 0 : (c == 'y' || c == 'Y') ? 1 : -1;
            if (g < 0) throw runtime_error("bad letter");
            relOcc[i].push_back((int)gen.size());
            gen.push_back(g);
            sgn.push_back((c == 'x' || c == 'y') ? 1 : -1);
            relOf.push_back((int)i);
        }
    int n = (int)gen.size();
    if (n == 0) { Result R; R.thick = true; return R; }
    // half-edge 2k = occurrence k at g+, 2k+1 = occurrence k at g-
    vector<int> alpha(2 * n, -1);
    for (auto& occ : relOcc) {
        int m = (int)occ.size();
        for (int j = 0; j < m; j++) {
            int k = occ[j], k2 = occ[(j + 1) % m];
            int hf = 2 * k + (sgn[k] > 0 ? 0 : 1);    // finish end of k
            int hs = 2 * k2 + (sgn[k2] > 0 ? 1 : 0);  // start end of k2
            if (alpha[hf] != -1 || alpha[hs] != -1) throw runtime_error("half-edge reused");
            alpha[hf] = hs; alpha[hs] = hf;
        }
    }
    for (int h = 0; h < 2 * n; h++) if (alpha[h] < 0) throw runtime_error("unused half-edge");
    vector<vector<int>> occOf(2);
    for (int k = 0; k < n; k++) occOf[gen[k]].push_back(k);
    // link vertices present
    vector<int> vertexOf(2 * n);
    for (int k = 0; k < n; k++) { vertexOf[2 * k] = 2 * gen[k]; vertexOf[2 * k + 1] = 2 * gen[k] + 1; }
    // relator parity of occurrences per generator
    vector<array<int, 2>> occCount(P.rel.size(), {0, 0});
    for (int k = 0; k < n; k++) occCount[relOf[k]][gen[k]]++;
    // components of the link graph (independent of rotations)
    vector<int> comp(4, -1);
    {
        vector<int> par(4); iota(par.begin(), par.end(), 0);
        function<int(int)> f = [&](int a) { return par[a] == a ? a : par[a] = f(par[a]); };
        for (int h = 0; h < 2 * n; h++) par[f(vertexOf[h])] = f(vertexOf[alpha[h]]);
        for (int v = 0; v < 4; v++) comp[v] = f(v);
    }
    int V = 0, C = 0;
    {
        vector<int> present(4, 0), seenRoot(4, 0);
        for (int h = 0; h < 2 * n; h++) present[vertexOf[h]] = 1;
        for (int v = 0; v < 4; v++) if (present[v]) { V++; if (!seenRoot[comp[v]]) { seenRoot[comp[v]] = 1; C++; } }
    }
    int E = n;  // corners
    int needF = E - V + 2 * C;
    Result R;
    vector<int> sigma(2 * n), visited(2 * n);
    vector<int> p0 = occOf[0], p1 = occOf[1];
    // enumerate cyclic orders: fix first element, permute the rest
    auto firstPerm = [](vector<int>& p) { if (p.size() > 1) sort(p.begin() + 1, p.end()); };
    auto nextPerm = [](vector<int>& p) { return p.size() > 1 && next_permutation(p.begin() + 1, p.end()); };
    firstPerm(p0);
    do {
        firstPerm(p1);
        do {
            for (int t = 0; t < 4; t++) {
                // parity condition
                bool ok = true;
                for (auto& cnt : occCount) {
                    int s = ((t & 1) ? cnt[0] : 0) + ((t & 2) ? cnt[1] : 0);
                    if (s % 2) { ok = false; break; }
                }
                if (!ok) continue;
                R.tried++;
                for (int g = 0; g < 2; g++) {
                    const vector<int>& p = g ? p1 : p0;
                    int d = (int)p.size();
                    bool nonor = t & (1 << g);
                    for (int i = 0; i < d; i++) {
                        int k = p[i], kn = p[(i + 1) % d], kp = p[(i + d - 1) % d];
                        sigma[2 * k] = 2 * kn;                    // rotation at g+
                        sigma[2 * k + 1] = 2 * (nonor ? kn : kp) + 1;  // at g-: equal or reversed
                    }
                }
                fill(visited.begin(), visited.end(), 0);
                int F = 0;
                for (int h = 0; h < 2 * n; h++) {
                    if (visited[h]) continue;
                    F++;
                    int c = h;
                    while (!visited[c]) { visited[c] = 1; c = sigma[alpha[c]]; }
                }
                if (F == needF) {
                    R.thick = true; R.order = {p0, p1}; R.types = t;
                    return R;
                }
                if (F > needF) throw runtime_error("Euler bound violated: bug");
            }
        } while (nextPerm(p1));
    } while (nextPerm(p0));
    return R;
}

static void print(const Pres& P, const Result& R) {
    printf("{\"relators\":[");
    for (size_t i = 0; i < P.rel.size(); i++) printf("%s\"%s\"", i ? "," : "", P.rel[i].c_str());
    printf("],\"thickenable\":%s,\"rotation_systems_tried\":%lld", R.thick ? "true" : "false", R.tried);
    if (R.thick) {
        printf(",\"witness_nonorientable_handles\":[%s,%s],\"witness_orders\":[",
               (R.types & 1) ? "true" : "false", (R.types & 2) ? "true" : "false");
        for (int g = 0; g < 2; g++) {
            printf("%s[", g ? "," : "");
            for (size_t i = 0; i < R.order[g].size(); i++) printf("%s%d", i ? "," : "", R.order[g][i]);
            printf("]");
        }
        printf("]");
    }
    printf("}\n");
}

static int selftest() {
    int fails = 0;
    auto expect = [&](const vector<string>& r, bool want, const char* what) {
        Pres P; P.rel = r;
        Result R = test(P);
        if (R.thick != want) { printf("FAIL %s\n", what); fails++; }
    };
    expect({"x", "y"}, true, "standard pair (wedge of two discs)");
    expect({"xyXY"}, true, "torus");
    expect({"xyxY"}, true, "Klein bottle (needs a non-orientable handle)");
    expect({"xx"}, true, "RP^2 (embeds in RP^2 x I)");
    expect({"xxx"}, true, "pseudo-projective plane of order 3 (spine of punctured L(3,1))");
    expect({"xxxxx"}, true, "order-5 pseudo-projective plane (punctured L(5,1))");
    expect({"xy", "y"}, true, "(xy,y)");
    expect({"xyXY", "x"}, true, "torus with a disc on x");
    printf("{\"selftest\":\"%s\",\"failures\":%d}\n", fails ? "FAILED" : "passed", fails);
    return fails ? 1 : 0;
}

int main(int argc, char** argv) {
    if (argc > 1 && string(argv[1]) == "--selftest") return selftest();
    string line;
    while (getline(cin, line)) {
        istringstream is(line);
        Pres P; string w;
        while (is >> w) P.rel.push_back(w);
        if (P.rel.empty()) continue;
        print(P, test(P));
        fflush(stdout);
    }
    return 0;
}
