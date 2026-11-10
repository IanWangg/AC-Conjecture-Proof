// r61_scan128.cpp -- research R6-1: experiments/th21_bs12_scan.cpp (TH21) with
// the key reader switched to agent M's 128-bit keys (experiments/m_acsearch.cpp,
// width W = 2, --dumpkeys output: 16 bytes per key, w[0] then w[1]; cap <= 60).
// Changes vs TH21: decode2/key2_of_pair (M's width-2 coder, copied in logic),
// a relator cache keyed by the full word (TH21's 64-bit wkey only holds words
// of length <= 29), probe keys (--probe W1 W2: exact-key occurrence count, to
// check encoding compatibility on a known source state), extra selftest part 0
// (width-2 round trip; width-2 vs width-1 decoding agree for T <= 28).
// Classification code (Whitehead reduction, orbit S, selftest 2-5) unchanged.
// Original TH21 description:
// stream a file of D-encoded 64-bit
// canonical state keys (experiments/d_acsearch.cpp / m_acsearch.cpp, width 1)
// and test both relators of every state for BS(1,2) type, i.e. for being (up
// to conjugacy and inversion) an Aut(F2)-image of XyxYY = x^-1 y x y^-2
// (TH09 Theorem 1: such a relator in a balanced presentation of the trivial
// group makes the presentation AC-trivial).
// Exact test: Whitehead-reduce the cyclic word with x->xy, x->xY, y->yx, y->yX
// (all rank-2 Whitehead automorphisms up to inner ones and signed
// permutations) while the cyclic length strictly drops; accept iff the minimal
// length is 5 and the minimal word lies in S = all length-5 cyclic words
// Aut-equivalent to XyxYY (closure of XyxYY under signed permutations,
// rotation, inversion and length-preserving Whitehead moves; Whitehead's
// theorem makes both steps exact).
// Build: g++ -O2 -std=c++17 -pthread -o r61_scan128 experiments/r61_scan128.cpp
// Usage: r61_scan128 --selftest | --words (stdin: one word per line)
//        r61_scan128 KEYFILE128 CAP [--threads T] [--start I] [--end J] [--maxhits H] [--probe W1 W2] [--nocache 1]
#include <bits/stdc++.h>
#include <fcntl.h>
#include <unistd.h>
using namespace std;
typedef uint64_t u64; typedef uint8_t u8;
static inline u8 inv(u8 l) { return l ^ 1; }
static const char LET[4] = {'x', 'X', 'y', 'Y'};
static const int B = 512;
// ---- D's word utilities and key encoding (copied verbatim in logic) ----
static int reduce_cyc(u8* s, int n) {
  int m = 0;
  for (int i = 0; i < n; i++) { if (m && s[m - 1] == inv(s[i])) m--; else s[m++] = s[i]; }
  int a = 0, b = m;
  while (b - a >= 2 && s[a] == inv(s[b - 1])) { a++; b--; }
  if (a) memmove(s, s + a, b - a);
  return b - a;
}
static int minrot(const u8* s, int n) {
  u8 d[2 * B]; memcpy(d, s, n); memcpy(d + n, s, n);
  int i = 0, j = 1, k = 0;
  while (i < n && j < n && k < n) {
    u8 a = d[i + k], b = d[j + k];
    if (a == b) { k++; continue; }
    if (a > b) i += k + 1; else j += k + 1;
    if (i == j) j++;
    k = 0;
  }
  return min(i, j);
}
static void canon_word(const u8* s, int n, u8* out) {
  u8 t[B];
  for (int i = 0; i < n; i++) t[i] = inv(s[n - 1 - i]);
  int r1 = minrot(s, n), r2 = minrot(t, n), c = 0;
  for (int i = 0; i < n; i++) { u8 a = s[(r1 + i) % n], b = t[(r2 + i) % n]; if (a != b) { c = a < b ? -1 : 1; break; } }
  if (c <= 0) for (int i = 0; i < n; i++) out[i] = s[(r1 + i) % n];
  else for (int i = 0; i < n; i++) out[i] = t[(r2 + i) % n];
}
static int cmpw(const u8* a, int na, const u8* b, int nb) {
  if (na != nb) return na < nb ? -1 : 1;
  for (int i = 0; i < na; i++) if (a[i] != b[i]) return a[i] < b[i] ? -1 : 1;
  return 0;
}
static u64 encode_ordered(const u8* a, int na, const u8* b, int nb) {
  u64 d = 0;
  auto push = [&](const u8* w, int n) { for (int i = 1; i < n; i++) { u8 c = w[i], f = inv(w[i - 1]); d = d * 3 + (u64)(c - (c > f ? 1 : 0)); } };
  push(a, na); push(b, nb);
  u64 T = na + nb;
  return (T << 58) | ((u64)na << 53) | ((u64)a[0] << 51) | ((u64)b[0] << 49) | d;
}
static u64 key_of_pair(const u8* a, int na, const u8* b, int nb) {
  u8 ca[B], cb[B]; canon_word(a, na, ca); canon_word(b, nb, cb);
  if (cmpw(ca, na, cb, nb) <= 0) return encode_ordered(ca, na, cb, nb);
  return encode_ordered(cb, nb, ca, na);
}
static bool decode(u64 key, u8* a, int& na, u8* b, int& nb) {
  int T = (int)(key >> 58) & 31; na = (int)(key >> 53) & 31; nb = T - na;
  if (na < 1 || nb < 1) return false;
  a[0] = (key >> 51) & 3; b[0] = (key >> 49) & 3;
  u64 d = key & ((1ULL << 49) - 1);
  int digits[64]; int nd = (na - 1) + (nb - 1);
  for (int i = nd - 1; i >= 0; i--) { digits[i] = (int)(d % 3); d /= 3; }
  if (d != 0) return false;
  int p = 0;
  auto pull = [&](u8* w, int n) { for (int i = 1; i < n; i++) { int dg = digits[p++]; u8 f = inv(w[i - 1]); u8 c = (u8)dg; if (c >= f) c++; w[i] = c; } };
  pull(a, na); pull(b, nb);
  return true;
}
// ---- agent M's 128-bit keys (m_acsearch.cpp encode_ordered_w / decode_w, width 2) ----
typedef unsigned __int128 u128;
struct K2 { u64 w0, w1; bool operator==(const K2& o) const { return w0 == o.w0 && w1 == o.w1; } };
static K2 encode_ordered2(const u8* a, int na, const u8* b, int nb) {
  u128 d = 0;
  auto push = [&](const u8* w, int n) { for (int i = 1; i < n; i++) { u8 c = w[i], f = inv(w[i - 1]); d = d * 3 + (u128)(c - (c > f ? 1 : 0)); } };
  push(a, na); push(b, nb);
  u64 T = na + nb; K2 k;
  k.w1 = (u64)d;
  k.w0 = (T << 57) | ((u64)na << 50) | ((u64)a[0] << 48) | ((u64)b[0] << 46) | (u64)(d >> 64);
  return k;
}
static K2 key2_of_pair(const u8* a, int na, const u8* b, int nb) {
  u8 ca[B], cb[B]; canon_word(a, na, ca); canon_word(b, nb, cb);
  if (cmpw(ca, na, cb, nb) <= 0) return encode_ordered2(ca, na, cb, nb);
  return encode_ordered2(cb, nb, ca, na);
}
static bool decode2(const K2& key, u8* a, int& na, u8* b, int& nb) {
  int T = (int)(key.w0 >> 57) & 127; na = (int)(key.w0 >> 50) & 127; nb = T - na;
  if (na < 1 || nb < 1 || T > 60) return false;
  a[0] = (key.w0 >> 48) & 3; b[0] = (key.w0 >> 46) & 3;
  u128 d = ((u128)(key.w0 & ((1ULL << 46) - 1)) << 64) | (u128)key.w1;
  int digits[128]; int nd = (na - 1) + (nb - 1);
  for (int i = nd - 1; i >= 0; i--) { digits[i] = (int)(d % 3); d /= 3; }
  if (d != 0) return false;
  int p = 0;
  auto pull = [&](u8* w, int n) { for (int i = 1; i < n; i++) { int dg = digits[p++]; u8 f = inv(w[i - 1]); u8 c = (u8)dg; if (c >= f) c++; w[i] = c; } };
  pull(a, na); pull(b, nb);
  return true;
}
static string wstr(const u8* w, int n) { string s; for (int i = 0; i < n; i++) s += LET[w[i]]; return s; }
static int parse(const string& s, u8* w) { int n = 0; for (char c : s) { int l = c == 'x' ? 0 : c == 'X' ? 1 : c == 'y' ? 2 : c == 'Y' ? 3 : -1; if (l >= 0) w[n++] = (u8)l; } return n; }
// ---- automorphisms ----
// which 0..3: x->xy, x->xY, y->yx, y->yX ; 4..7: x->yx, x->Yx, y->xy, y->Xy
static int apply_map(const u8* s, int n, int which, u8* out) {
  u8 g = (which % 4 < 2) ? 0 : 2, h = 2 - g, e = (which % 2 == 0) ? h : inv(h);
  bool left = which >= 4; int m = 0; u8 tmp[2 * B];
  if (2 * n > 2 * B) return -1;
  for (int i = 0; i < n; i++) {
    if (s[i] == g) { if (left) { tmp[m++] = e; tmp[m++] = g; } else { tmp[m++] = g; tmp[m++] = e; } }
    else if (s[i] == inv(g)) { if (left) { tmp[m++] = inv(g); tmp[m++] = inv(e); } else { tmp[m++] = inv(e); tmp[m++] = inv(g); } }
    else tmp[m++] = s[i];
  }
  int L = reduce_cyc(tmp, m); if (L > B) return -1;
  memcpy(out, tmp, L); return L;
}
static void signed_perm(const u8* s, int n, int p, u8* out) {  // p bit0 swap, bit1 flip x, bit2 flip y
  for (int i = 0; i < n; i++) { int g = s[i] >> 1, sg = s[i] & 1; sg ^= (g == 0 ? (p >> 1) & 1 : (p >> 2) & 1); if (p & 1) g = 1 - g; out[i] = (u8)(2 * g + sg); }
}
static int wh_min(u8* s, int n, int nmaps = 4) {
  while (n > 1) {
    bool imp = false;
    for (int w = 0; w < nmaps && !imp; w++) { u8 t[B]; int L = apply_map(s, n, w, t); if (L >= 0 && L < n) { memcpy(s, t, L); n = L; imp = true; } }
    if (!imp) break;
  }
  return n;
}
static u64 wkey(const u8* s, int n) { u64 k = (u64)n << 58; for (int i = 0; i < n; i++) k |= (u64)s[i] << (2 * i); return k; }
static vector<u64> Svec, Tvec; static vector<string> Sstr;
// closure at length 5 of base: all length-5 canonical cyclic words in its Aut-orbit
static void build_S(const char* base, vector<u64>& Svec, vector<string>& Sstr) {
  u8 w[B], c[B]; int n = parse(base, w); canon_word(w, n, c);
  set<u64> seen; vector<vector<u8>> st; seen.insert(wkey(c, 5)); st.push_back(vector<u8>(c, c + 5));
  while (!st.empty()) {
    vector<u8> cur = st.back(); st.pop_back();
    for (int m = 0; m < 16; m++) {
      u8 t[B]; int L;
      if (m < 8) L = apply_map(cur.data(), 5, m, t); else { signed_perm(cur.data(), 5, m - 8, t); L = 5; }
      if (L < 5) { fprintf(stderr, "%s not Whitehead-minimal?!\n", base); exit(3); }
      if (L != 5) continue;
      canon_word(t, 5, c); u64 k = wkey(c, 5);
      if (seen.insert(k).second) st.push_back(vector<u8>(c, c + 5));
    }
  }
  for (u64 k : seen) { Svec.push_back(k); u8 t[5]; for (int i = 0; i < 5; i++) t[i] = (k >> (2 * i)) & 3; Sstr.push_back(wstr(t, 5)); }
}
static thread_local int last_cls = 0;  // for minimal length 5: 1 BS(1,2) orbit, 2 trefoil (xxYYY) orbit, 3 other; else 0
static bool classify(const u8* s0, int n0, int& ml, int nmaps = 4) {
  u8 s[B]; memcpy(s, s0, n0); int n = reduce_cyc(s, n0);
  n = wh_min(s, n, nmaps); ml = n;
  last_cls = 0; if (n != 5) return false;
  u8 c[8]; canon_word(s, 5, c); u64 k = wkey(c, 5);
  bool bs = binary_search(Svec.begin(), Svec.end(), k);
  last_cls = bs ? 1 : binary_search(Tvec.begin(), Tvec.end(), k) ? 2 : 3;
  return bs;
}
// ---- self-test ----
static int fails = 0;
#define CHECK(c, msg) do { if (!(c)) { fails++; if (fails < 20) printf("FAIL %s\n", msg); } } while (0)
static int random_aut_image(mt19937_64& R, const string& w0, int steps, int maxlen, u8* out) {
  u8 s[B]; int n = parse(w0, s);
  for (int k = 0; k < steps; k++) {
    u8 t[B]; int L; int m = R() % 12;
    if (m < 8) L = apply_map(s, n, m, t); else { signed_perm(s, n, R() % 8, t); L = n; }
    if (L < 0 || L > maxlen) continue;
    memcpy(s, t, L); n = L;
  }
  int r = R() % n; for (int i = 0; i < n; i++) out[i] = s[(i + r) % n];
  if (R() & 1) { u8 t[B]; for (int i = 0; i < n; i++) t[i] = inv(out[n - 1 - i]); memcpy(out, t, n); }
  return n;
}
static int selftest() {
  mt19937_64 R(2121);
  printf("S (%zu length-5 canonical cyclic words Aut-equivalent to XyxYY):", Svec.size());
  for (auto& s : Sstr) printf(" %s", s.c_str()); printf("\n");
  // 0. width-2 (M) coder: round trip up to T = 60; agrees with width-1 decoding for T <= 28
  int n0 = 0, n0small = 0;
  for (int it = 0; it < 300000; it++) {
    u8 a[B], b[B]; int na = 1 + R() % 40, nb = 1 + R() % (61 - na);
    for (int i = 0; i < na; i++) a[i] = R() % 4; for (int i = 0; i < nb; i++) b[i] = R() % 4;
    na = reduce_cyc(a, na); nb = reduce_cyc(b, nb); if (!na || !nb) continue;
    K2 k = key2_of_pair(a, na, b, nb); u8 c[B], d[B]; int nc, nd; n0++;
    CHECK(decode2(k, c, nc, d, nd) && key2_of_pair(c, nc, d, nd) == k && nc + nd == na + nb, "roundtrip2");
    CHECK(key2_of_pair(b, nb, a, na) == k, "swap invariance2");
    if (na + nb <= 28) { u64 k1 = key_of_pair(a, na, b, nb); u8 e[B], f[B]; int ne, nf; n0small++;
      CHECK(decode(k1, e, ne, f, nf) && ne == nc && nf == nd && !memcmp(e, c, nc) && !memcmp(f, d, nd), "w1 vs w2"); }
  }
  printf("width-2 coder: %d random pairs round-tripped (T<=60), %d compared with width-1 decoding (T<=28)\n", n0, n0small);
  // 1. key encoding round trip on random pairs
  for (int it = 0; it < 200000; it++) {
    u8 a[B], b[B]; int na = 1 + R() % 20, nb = 1 + R() % (30 - na);
    for (int i = 0; i < na; i++) a[i] = R() % 4; for (int i = 0; i < nb; i++) b[i] = R() % 4;
    na = reduce_cyc(a, na); nb = reduce_cyc(b, nb); if (!na || !nb) continue;
    u64 k = key_of_pair(a, na, b, nb); u8 c[B], d[B]; int nc, nd;
    CHECK(decode(k, c, nc, d, nd) && key_of_pair(c, nc, d, nd) == k && nc + nd == na + nb, "roundtrip");
    CHECK(key_of_pair(b, nb, a, na) == k, "swap invariance");
  }
  // 2. planted positives: random Aut-images of XyxYY (and of XYxyy), rotated, maybe inverted
  int npos = 0; map<int, int> lens;
  for (int it = 0; it < 30000; it++) {
    u8 w[B]; int n = random_aut_image(R, it % 2 ? "XyxYY" : "XYxyy", 1 + R() % 40, it % 3 ? 28 : 120, w);
    int ml, ml8; bool v = classify(w, n, ml), v8 = classify(w, n, ml8, 8);
    CHECK(v && ml == 5 && v8 && ml8 == 5, ("planted positive " + wstr(w, n)).c_str()); npos++; lens[n]++;
  }
  printf("planted positives: %d tested (lengths %d..%d)\n", npos, lens.begin()->first, lens.rbegin()->first);
  // 3. negatives
  const char* neg[] = {"x", "xy", "xxy", "xyxyY", "xyxYXY", "xxxYYYY", "xxYYY", "XyyyxYYYY", "XyxYYY", "XyyxYYY", "xyXY", "xxyyXXYY", "XyxY", "XYxyyy", "xyyxYY"};
  for (auto w0 : neg) {
    u8 w[B]; int n = parse(w0, w); int ml; bool v = classify(w, n, ml);
    printf("  negative %-10s minlen %d bs %d\n", w0, ml, (int)v); CHECK(!v, w0);
    for (int it = 0; it < 3000; it++) { u8 u[B]; int m = random_aut_image(R, w0, 1 + R() % 30, 40, u); int ml2; bool v2 = classify(u, m, ml2); CHECK(!v2 && ml2 == ml, ("neg image of " + string(w0) + " " + wstr(u, m)).c_str()); }
  }
  // 4. 4 maps suffice: reduction with the 4 maps is never improved by the 8 maps
  for (int it = 0; it < 100000; it++) {
    u8 w[B]; int n = 1 + R() % 28; for (int i = 0; i < n; i++) w[i] = R() % 4; n = reduce_cyc(w, n); if (!n) continue;
    int m4, m8; bool v4 = classify(w, n, m4), v8 = classify(w, n, m8, 8); CHECK(m4 == m8 && v4 == v8, "4 vs 8 maps");
  }
  // 5. AK(3) relators
  { u8 a[B], b[B]; int na = parse("xxxYYYY", a), nb = parse("xyxYXY", b), m1, m2; bool v1 = classify(a, na, m1), v2 = classify(b, nb, m2);
    printf("AK(3): xxxYYYY minlen %d bs %d ; xyxYXY minlen %d bs %d\n", m1, (int)v1, m2, (int)v2); CHECK(!v1 && !v2, "AK3"); 
    CHECK(last_cls == 2, "xyxYXY in trefoil orbit"); u8 t[B]; int nt = parse("xxYYY", t); classify(t, nt, m1); CHECK(last_cls == 2, "xxYYY trefoil");
    printf("trefoil (xxYYY) orbit at length 5: %zu canonical words\n", Tvec.size()); }
  printf(fails ? "SELFTEST FAILED (%d failures)\n" : "SELFTEST PASSED\n", fails);
  return fails ? 1 : 0;
}
// ---- scan ----
struct Res { long long states = 0, rels = 0, hits = 0, badlen = 0, badrt = 0, baddec = 0, ak3 = 0, ak3exact = 0, probe = 0, probeexact = 0, cachehit = 0; long long hist[64] = {0}, c5[4] = {0}; };
static mutex pm; static atomic<long long> done_states(0), total_hits(0);
static vector<K2> ak3keys; static int maxhits = 20; static bool nocache = false;  // --nocache 1: classify every relator afresh (cache cross-check)  // ak3keys[0..7]: AK(3) D8 images; [8..15]: --probe pair images
static void worker(int fd, long long lo, long long hi, int cap, Res* Rp, int tid, const char* fname) {
  // relator cache keyed by the full word: k0 = letters 0..31, k1 = (n << 58) | letters 32..60 (n <= 61)
  Res& R = *Rp; const int LOG = 23; vector<u64> ck0(1u << LOG, 0), ck1(1u << LOG, 0); vector<uint16_t> cv(1u << LOG, 0);
  const long long BLK = 1 << 20; vector<u64> buf(2 * BLK); auto t0 = chrono::steady_clock::now();
  for (long long p = lo; p < hi && total_hits < maxhits; p += BLK) {
    long long cnt = min(BLK, hi - p); size_t want = cnt * 16, got = 0;
    while (got < want) { ssize_t r = pread(fd, (char*)buf.data() + got, want - got, p * 16 + got); if (r <= 0) { fprintf(stderr, "read error\n"); exit(2); } got += r; }
    for (long long i = 0; i < cnt; i++) {
      K2 key; key.w0 = buf[2 * i]; key.w1 = buf[2 * i + 1]; u8 w[2][B]; int n[2];
      R.states++;
      if (!decode2(key, w[0], n[0], w[1], n[1])) { R.baddec++; continue; }
      if (n[0] + n[1] > cap) R.badlen++;
      if (!(key2_of_pair(w[0], n[0], w[1], n[1]) == key)) R.badrt++;
      for (size_t q = 0; q < ak3keys.size(); q++) if (ak3keys[q] == key) { if (q < 8) { R.ak3++; if (q == 0) R.ak3exact++; } else { R.probe++; if (q == 8) R.probeexact++; } }
      for (int j = 0; j < 2; j++) {
        R.rels++; int nn = n[j]; u64 k0 = 0, k1 = (u64)nn << 58;
        for (int t = 0; t < nn && t < 61; t++) { if (t < 32) k0 |= (u64)w[j][t] << (2 * t); else k1 |= (u64)w[j][t] << (2 * (t - 32)); }
        bool cacheable = nn <= 61 && !nocache; u64 h = ((k0 ^ (k1 * 0xC2B2AE3D27D4EB4FULL)) * 0x9E3779B97F4A7C15ULL) >> (64 - LOG);
        int ml, cls; bool bs;
        if (cacheable && ck0[h] == k0 && ck1[h] == k1) { R.cachehit++; ml = cv[h] & 255; cls = cv[h] >> 8; bs = cls == 1; }
        else { bs = classify(w[j], nn, ml); cls = last_cls; if (cacheable) { ck0[h] = k0; ck1[h] = k1; cv[h] = (uint16_t)(ml | (cls << 8)); } }
        R.hist[ml]++; R.c5[cls]++;
        if (bs) { R.hits++; total_hits++; lock_guard<mutex> g(pm);
          printf("HIT file %s index %lld relator %d state [%s %s] bs-relator %s\n", fname, p + i, j, wstr(w[0], n[0]).c_str(), wstr(w[1], n[1]).c_str(), wstr(w[j], n[j]).c_str()); fflush(stdout); }
      }
    }
    long long d = (done_states += cnt);
    if (tid == 0) { double el = chrono::duration<double>(chrono::steady_clock::now() - t0).count(); fprintf(stderr, "progress: %lld states done (thread0 at index %lld), %.1fs\n", d, p + cnt, el); }
  }
}
int main(int argc, char** argv) {
  build_S("XyxYY", Svec, Sstr); { vector<string> t; build_S("xxYYY", Tvec, t); }
  if (argc >= 2 && string(argv[1]) == "--selftest") return selftest();
  if (argc >= 2 && string(argv[1]) == "--words") {
    string line; while (getline(cin, line)) { u8 w[B]; int n = parse(line, w); if (!n) continue; int ml; bool v = classify(w, n, ml); printf("%s %d %d\n", line.c_str(), ml, (int)v); }
    return 0;
  }
  if (argc < 3) { fprintf(stderr, "usage: see header\n"); return 2; }
  const char* fname = argv[1]; int cap = atoi(argv[2]); int T = 2; long long st = 0, en = -1;
  string pr1, pr2;
  for (int i = 3; i + 1 < argc; i += 2) { string a = argv[i]; if (a == "--threads") T = atoi(argv[i + 1]); else if (a == "--start") st = atoll(argv[i + 1]); else if (a == "--end") en = atoll(argv[i + 1]); else if (a == "--maxhits") maxhits = atoi(argv[i + 1]); else if (a == "--nocache") nocache = atoi(argv[i + 1]) != 0; else if (a == "--probe" && i + 2 < argc) { pr1 = argv[i + 1]; pr2 = argv[i + 2]; i++; } }
  int fd = open(fname, O_RDONLY); if (fd < 0) { fprintf(stderr, "cannot open %s\n", fname); return 2; }
  long long sz = lseek(fd, 0, SEEK_END), N = sz / 16;
  printf("file %s bytes %lld keys128 %lld (bytes%%16=%lld) cap %d threads %d\n", fname, sz, N, sz % 16, cap, T);
  if (en < 0 || en > N) en = N;
  auto add_images = [&](const char* s1, const char* s2) { u8 a[B], b[B], ga[B], gb[B]; int na = parse(s1, a), nb = parse(s2, b);
    for (int p = 0; p < 8; p++) { signed_perm(a, na, p, ga); signed_perm(b, nb, p, gb); ak3keys.push_back(key2_of_pair(ga, na, gb, nb)); } };
  add_images("xxxYYYY", "xyxYXY");
  printf("AK(3) key128 %016llx %016llx\n", (unsigned long long)ak3keys[0].w0, (unsigned long long)ak3keys[0].w1);
  if (!pr1.empty()) { add_images(pr1.c_str(), pr2.c_str()); printf("probe [%s %s] key128 %016llx %016llx\n", pr1.c_str(), pr2.c_str(), (unsigned long long)ak3keys[8].w0, (unsigned long long)ak3keys[8].w1); }
  printf("scanning index range [%lld, %lld)\n", st, en); fflush(stdout);
  vector<Res> RR(T); vector<thread> th; long long per = (en - st + T - 1) / T;
  for (int t = 0; t < T; t++) { long long lo = st + t * per, hi = min(en, lo + per); th.emplace_back(worker, fd, lo, max(lo, hi), cap, &RR[t], t, fname); }
  for (auto& x : th) x.join();
  Res S; for (auto& r : RR) { S.states += r.states; S.rels += r.rels; S.hits += r.hits; S.badlen += r.badlen; S.badrt += r.badrt; S.baddec += r.baddec; S.ak3 += r.ak3; S.ak3exact += r.ak3exact; S.probe += r.probe; S.probeexact += r.probeexact; for (int i = 0; i < 4; i++) S.c5[i] += r.c5[i]; S.cachehit += r.cachehit; for (int i = 0; i < 64; i++) S.hist[i] += r.hist[i]; }
  printf("states_scanned %lld relators_tested %lld bs12_hits %lld\n", S.states, S.rels, S.hits);
  printf("decode_failures %lld total_length_over_cap %lld roundtrip_failures %lld ak3_D8_image_occurrences %lld ak3_exact_key_occurrences %lld cache_hits %lld\n", S.baddec, S.badlen, S.badrt, S.ak3, S.ak3exact, S.cachehit);
  if (!pr1.empty()) printf("probe_D8_image_occurrences %lld probe_exact_key_occurrences %lld\n", S.probe, S.probeexact);
  printf("minimal_length_5 split: BS(1,2)-orbit %lld trefoil(xxYYY)-orbit %lld other %lld\n", S.c5[1], S.c5[2], S.c5[3]);
  printf("whitehead_minimal_length_histogram (relator occurrences):"); for (int i = 0; i < 64; i++) if (S.hist[i]) printf(" %d:%lld", i, S.hist[i]); printf("\n");
  printf(S.states == en - st ? "COMPLETE range [%lld, %lld)\n" : "INCOMPLETE (stopped early) range [%lld, %lld)\n", st, en);
  return 0;
}
