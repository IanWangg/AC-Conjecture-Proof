// m_acsearch.cpp -- research M (round 4): a lean, multi-threaded, wide-key
// re-implementation of D's barrier-ordered forward search in the directed
// cyclic-product graph (experiments/d_acsearch.cpp), built for the last
// affordable caps (AK(3) at cap 30, C4/C6 at caps 32-34).
//
// Build:  g++ -O2 -std=c++17 -pthread -o m_acsearch experiments/m_acsearch.cpp
//
// SEMANTICS (identical to d_acsearch, see research-d.md section 2 and the
// coordinator's correction: the graph is DIRECTED, the computed set is the
// FORWARD-REACHABLE set of the source, every reached state is ordinary-AC-
// equivalent to the source):
//   state  = unordered pair of nonempty cyclically reduced words modulo Sigma
//            (rotation / inversion of either relator, swap);
//   move   = replace u by cyc(rot(u) * rot(v)^(+-1));
//   energy = total length; barrier = minimax energy over paths from the
//            source; states are settled level by level (Prop. D4).
// DIFFERENCES to d_acsearch:
//   * no parent pointers: a hit's path is reconstructed afterwards by a
//     verified predecessor search (every chosen predecessor is re-checked by
//     forward expansion, so a printed PATH is a genuine chain of cyclic
//     products); memory is 8W + 1 bytes per state plus a 4-byte slot table;
//   * W = 1 (64-bit keys, cap <= 31, D's exact key encoding, so D's and L's
//     binary dumps are interoperable) or W = 2 (128-bit keys, cap <= 60);
//   * --threads T: lock-free insertion into the slot table, level-synchronous
//     passes; the state set and all barriers are scheduling-independent;
//   * --checkpoint / --resume: a run can be split into phases (each phase
//     completes whole barrier levels);
//   * detection at insertion: primitive relator (Lemma D3), exact Sigma
//     targets, Sigma-contact with a key file (e.g. L's T(20)), and Aut(F2)-
//     orbit contact with an orbit file for states whose Aut-minimal length is
//     <= --orbit-maxlen (Whitehead reduction as in D's aut_canon).
// MODES: search (default), --self-test, --autdump KEYS OUT [--threads T]
//   (Aut-canonicalize a key dump, D-compatible orbit keys), --pred-test.
#include <bits/stdc++.h>
#include <atomic>
#include <thread>
#include <mutex>
using namespace std;
typedef uint64_t u64;
typedef uint32_t u32;
typedef uint8_t u8;
typedef unsigned __int128 u128;

static const int MAXL64 = 31;   // D's limit for 64-bit keys
static const int MAXL128 = 60;  // our limit for 128-bit keys (word buffers 128)
static int W = 1;               // key width in u64 words (1 or 2), set at start
static int CAP = 25;
static inline u8 inv(u8 l) { return l ^ 1; }
static const char LET[4] = {'x', 'X', 'y', 'Y'};
static int letter_of(char c) {
  switch (c) { case 'x': return 0; case 'X': return 1; case 'y': return 2; case 'Y': return 3; }
  return -1;
}

// ---------------- words ----------------
static int reduce_cyc(u8* s, int n) {
  int m = 0;
  for (int i = 0; i < n; i++) { if (m && s[m - 1] == inv(s[i])) m--; else s[m++] = s[i]; }
  int a = 0, b = m;
  while (b - a >= 2 && s[a] == inv(s[b - 1])) { a++; b--; }
  if (a) memmove(s, s + a, b - a);
  return b - a;
}
static bool is_freely_reduced(const u8* s, int n) {
  for (int i = 1; i < n; i++) if (s[i] == inv(s[i - 1])) return false;
  return true;
}
static bool is_cyc_reduced(const u8* s, int n) {
  return is_freely_reduced(s, n) && (n < 2 || s[0] != inv(s[n - 1]));
}
static int minrot(const u8* s, int n) {  // Booth-style least rotation (D's two-pointer)
  u8 d[2 * 128];
  memcpy(d, s, n); memcpy(d + n, s, n);
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
static void canon_word(const u8* s, int n, u8* out) {  // identical to D
  u8 t[128];
  for (int i = 0; i < n; i++) t[i] = inv(s[n - 1 - i]);
  int r1 = minrot(s, n), r2 = minrot(t, n);
  int c = 0;
  for (int i = 0; i < n; i++) { u8 a = s[(r1 + i) % n], b = t[(r2 + i) % n]; if (a != b) { c = a < b ? -1 : 1; break; } }
  if (c <= 0) for (int i = 0; i < n; i++) out[i] = s[(r1 + i) % n];
  else for (int i = 0; i < n; i++) out[i] = t[(r2 + i) % n];
}
static int cmpw(const u8* a, int na, const u8* b, int nb) {
  if (na != nb) return na < nb ? -1 : 1;
  for (int i = 0; i < na; i++) if (a[i] != b[i]) return a[i] < b[i] ? -1 : 1;
  return 0;
}

// ---------------- keys ----------------
struct Key {
  u64 w[2];
  bool operator==(const Key& o) const { return w[0] == o.w[0] && w[1] == o.w[1]; }
  bool operator<(const Key& o) const { return w[0] != o.w[0] ? w[0] < o.w[0] : w[1] < o.w[1]; }
};
// D's 64-bit encoding (exact): (T<<58)|(na<<53)|(a0<<51)|(b0<<49)|base-3 digits
static Key encode_ordered_w(const u8* a, int na, const u8* b, int nb, int width) {
  Key k; k.w[0] = k.w[1] = 0;
  if (width == 1) {
    u64 d = 0;
    auto push = [&](const u8* w, int n) { for (int i = 1; i < n; i++) { u8 c = w[i], f = inv(w[i - 1]); d = d * 3 + (u64)(c - (c > f ? 1 : 0)); } };
    push(a, na); push(b, nb);
    u64 T = na + nb;
    k.w[0] = (T << 58) | ((u64)na << 53) | ((u64)a[0] << 51) | ((u64)b[0] << 49) | d;
  } else {
    // 128-bit: hi word top 16 bits = (T:7)(na:7)(a0:2) ... we use
    // w[0] = (T<<57)|(na<<50)|(a0<<48)|(b0<<46)|(digits>>64 restricted to 46 bits), w[1] = low 64 bits of digits
    u128 d = 0;
    auto push = [&](const u8* w, int n) { for (int i = 1; i < n; i++) { u8 c = w[i], f = inv(w[i - 1]); d = d * 3 + (u128)(c - (c > f ? 1 : 0)); } };
    push(a, na); push(b, nb);
    u64 T = na + nb;
    k.w[1] = (u64)d;
    k.w[0] = (T << 57) | ((u64)na << 50) | ((u64)a[0] << 48) | ((u64)b[0] << 46) | (u64)(d >> 64);
  }
  return k;
}
static Key key_of_canon_w(const u8* a, int na, const u8* b, int nb, int width) {
  if (cmpw(a, na, b, nb) <= 0) return encode_ordered_w(a, na, b, nb, width);
  return encode_ordered_w(b, nb, a, na, width);
}
static Key key_of_canon(const u8* a, int na, const u8* b, int nb) { return key_of_canon_w(a, na, b, nb, W); }
static Key key_of_pair_w(const u8* a, int na, const u8* b, int nb, int width) {
  u8 ca[128], cb[128];
  canon_word(a, na, ca); canon_word(b, nb, cb);
  return key_of_canon_w(ca, na, cb, nb, width);
}
static Key key_of_pair(const u8* a, int na, const u8* b, int nb) { return key_of_pair_w(a, na, b, nb, W); }
static int key_energy_w(const Key& k, int width) { return width == 1 ? (int)((k.w[0] >> 58) & 31) : (int)((k.w[0] >> 57) & 127); }
static int key_energy(const Key& k) { return key_energy_w(k, W); }
static void decode_w(const Key& key, u8* a, int& na, u8* b, int& nb, int width) {
  int T; u128 d;
  if (width == 1) {
    T = (int)(key.w[0] >> 58) & 31; na = (int)(key.w[0] >> 53) & 31;
    a[0] = (key.w[0] >> 51) & 3; b[0] = (key.w[0] >> 49) & 3;
    d = key.w[0] & ((1ULL << 49) - 1);
  } else {
    T = (int)(key.w[0] >> 57) & 127; na = (int)(key.w[0] >> 50) & 127;
    a[0] = (key.w[0] >> 48) & 3; b[0] = (key.w[0] >> 46) & 3;
    d = ((u128)(key.w[0] & ((1ULL << 46) - 1)) << 64) | (u128)key.w[1];
  }
  nb = T - na;
  int digits[128]; int nd = (na - 1) + (nb - 1);
  for (int i = nd - 1; i >= 0; i--) { digits[i] = (int)(d % 3); d /= 3; }
  int p = 0;
  auto pull = [&](u8* w, int n) { for (int i = 1; i < n; i++) { int dg = digits[p++]; u8 f = inv(w[i - 1]); u8 c = (u8)dg; if (c >= f) c++; w[i] = c; } };
  pull(a, na); pull(b, nb);
}
static void decode(const Key& key, u8* a, int& na, u8* b, int& nb) { decode_w(key, a, na, b, nb, W); }
static string wstr(const u8* w, int n) { string s; for (int i = 0; i < n; i++) s += LET[w[i]]; return s; }
static string kstr_w(const Key& key, int width) { u8 a[128], b[128]; int na, nb; decode_w(key, a, na, b, nb, width); return wstr(a, na) + " " + wstr(b, nb); }
static string kstr(const Key& key) { return kstr_w(key, W); }
static inline u64 mix(u64 x) { x += 0x9e3779b97f4a7c15ULL; x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL; x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL; return x ^ (x >> 31); }
static inline u64 khash(const Key& k) { return W == 1 ? mix(k.w[0]) : mix(k.w[0] ^ mix(k.w[1])); }

// ---------------- Whitehead: primitivity and Aut(F2)-orbit canonical form (as in D) ----------------
static int apply_wh(const u8* s, int n, int which, u8* out) {
  u8 g = (which < 2) ? 0 : 2, h = (which < 2) ? 2 : 0, e = (which % 2 == 0) ? h : inv(h);
  int m = 0; u8 tmp[512];
  for (int i = 0; i < n; i++) {
    if (s[i] == g) { tmp[m++] = g; tmp[m++] = e; }
    else if (s[i] == inv(g)) { tmp[m++] = inv(e); tmp[m++] = inv(g); }
    else tmp[m++] = s[i];
  }
  if (m > 250) return -1;
  int L = reduce_cyc(tmp, m);
  memcpy(out, tmp, L);
  return L;
}
static bool is_primitive(const u8* s0, int n0) {
  if (n0 == 1) return true;
  bool has[4] = {false, false, false, false};
  for (int i = 0; i < n0; i++) has[s0[i]] = true;
  if ((has[0] && has[1]) || (has[2] && has[3])) return false;  // classical necessary condition (checked in D's self-test to length 12)
  u8 s[256]; int n = n0; memcpy(s, s0, n);
  while (true) {
    if (n == 1) return true;
    bool improved = false;
    for (int w = 0; w < 4 && !improved; w++) { u8 t[256]; int L = apply_wh(s, n, w, t); if (L >= 0 && L < n) { memcpy(s, t, L); n = L; improved = true; } }
    if (!improved) return false;
  }
}
static u8 d8img(u8 l, int g) { u8 base = l & 2, sgn = l & 1; if (g & 1) base ^= 2; if ((base == 0 && (g & 2)) || (base == 2 && (g & 4))) sgn ^= 1; return (u8)(base | sgn); }
// Whitehead minimization only (cheap part); returns minimal total length and the minimized words
static int wh_minimize(u8* a, int& na, u8* b, int& nb) {
  while (true) {
    bool imp = false;
    for (int m = 0; m < 4 && !imp; m++) {
      u8 ta[256], tb[256]; int la = apply_wh(a, na, m, ta), lb = apply_wh(b, nb, m, tb);
      if (la > 0 && lb > 0 && la + lb < na + nb) { memcpy(a, ta, la); na = la; memcpy(b, tb, lb); nb = lb; imp = true; }
    }
    if (!imp) break;
  }
  return na + nb;
}
// D's aut_canon, verbatim semantics (64-bit D keys; requires minimal length <= 31)
static bool aut_canon64(const u8* a0, int na0, const u8* b0, int nb0, u64& out, int& minlen, size_t limit = 20000) {
  u8 a[256], b[256]; int na = na0, nb = nb0; memcpy(a, a0, na); memcpy(b, b0, nb);
  minlen = wh_minimize(a, na, b, nb);
  if (minlen > MAXL64) return false;
  // D-format (64-bit) keys for the closure, independent of the global width
  auto kp = [&](const u8* x, int nx, const u8* y, int ny) { return key_of_pair_w(x, nx, y, ny, 1).w[0]; };
  auto dec = [&](u64 k, u8* x, int& nx, u8* y, int& ny) { Key kk; kk.w[0] = k; kk.w[1] = 0; decode_w(kk, x, nx, y, ny, 1); };
  vector<u64> stack; unordered_set<u64> seen;
  u64 k0 = kp(a, na, b, nb); stack.push_back(k0); seen.insert(k0);
  bool ok = true;
  while (!stack.empty() && ok) {
    u64 k = stack.back(); stack.pop_back();
    u8 x[128], y[128]; int nx, ny; dec(k, x, nx, y, ny);
    for (int m = 0; m < 4; m++) {
      u8 tx[256], ty[256]; int lx = apply_wh(x, nx, m, tx), ly = apply_wh(y, ny, m, ty);
      if (lx > 0 && ly > 0 && lx + ly == minlen) {
        u64 kk = kp(tx, lx, ty, ly);
        if (seen.insert(kk).second) { stack.push_back(kk); if (seen.size() > limit) { ok = false; break; } }
      } else if (lx > 0 && ly > 0 && lx + ly < minlen) { fprintf(stderr, "internal error: Whitehead minimization not minimal\n"); exit(3); }
    }
  }
  if (!ok) return false;
  u64 best = ~0ULL;
  for (u64 k : seen) {
    u8 x[128], y[128]; int nx, ny; dec(k, x, nx, y, ny);
    for (int g = 0; g < 8; g++) {
      u8 gx[128], gy[128];
      for (int t = 0; t < nx; t++) gx[t] = d8img(x[t], g);
      for (int t = 0; t < ny; t++) gy[t] = d8img(y[t], g);
      best = min(best, kp(gx, nx, gy, ny));
    }
  }
  out = best; return true;
}

// ---------------- forward expansion (identical move generation to d_acsearch) ----------------
// calls f(side, key, energy) for every cyclic product with energy <= cap
template <class F> static void expand_state(const u8* A, int na, const u8* B, int nb, int cap, F f) {
  for (int side = 0; side < 2; side++) {
    const u8* U = side ? B : A; int nu = side ? nb : na;
    const u8* V0 = side ? A : B; int nv = side ? na : nb;
    u8 UU[256]; memcpy(UU, U, nu); memcpy(UU + nu, U, nu);
    for (int sg = 0; sg < 2; sg++) {
      u8 V[128];
      if (sg == 0) memcpy(V, V0, nv); else for (int t = 0; t < nv; t++) V[t] = inv(V0[nv - 1 - t]);
      u8 VV[256]; memcpy(VV, V, nv); memcpy(VV + nv, V, nv);
      for (int k = 0; k < nu; k++) {
        const u8* Ur = UU + k;
        for (int l = 0; l < nv; l++) {
          const u8* Vr = VV + l;
          int c1 = 0, mn = min(nu, nv);
          while (c1 < mn && Ur[nu - 1 - c1] == inv(Vr[c1])) c1++;
          u8 Wd[256]; int L;
          if (c1 < mn) {
            if (Vr[nv - 1] == inv(Ur[0])) continue;  // same cyclic word as a shifted alignment
            L = nu + nv - 2 * c1;
            if (L + nv > cap) continue;
            int m = 0;
            for (int t = 0; t < nu - c1; t++) Wd[m++] = Ur[t];
            for (int t = c1; t < nv; t++) Wd[m++] = Vr[t];
          } else {
            int m = 0;
            for (int t = 0; t < nu; t++) Wd[m++] = Ur[t];
            for (int t = 0; t < nv; t++) Wd[m++] = Vr[t];
            L = reduce_cyc(Wd, m);
            if (L == 0 || L + nv > cap) continue;
          }
          u8 Wc[128]; canon_word(Wd, L, Wc);
          f(side, key_of_canon(Wc, L, V0, nv), L + nv);
        }
      }
    }
  }
}

// ---------------- the state store ----------------
struct Store {
  long long maxstates = 0; int logtable = 0; u64 mask = 0;
  vector<u64> keys;              // stride W
  vector<u8> bar;                // barrier per state (255 = unused)
  vector<atomic<u32>> slot;      // 0 empty, RESV reserved, else index+1
  atomic<long long> n{0};
  atomic<bool> budget{false};
  static const u32 RESV = 0xFFFFFFFFu;
  void init(long long ms, int lt) {
    maxstates = ms; logtable = lt; mask = (1ULL << lt) - 1;
    keys.assign((size_t)(ms + 4096) * W, 0); bar.assign((size_t)(ms + 4096), 255);
    slot = vector<atomic<u32>>(1ULL << lt);
    for (auto& s : slot) s.store(0, memory_order_relaxed);
  }
  inline Key key_at(long long i) const { Key k; k.w[0] = keys[(size_t)i * W]; k.w[1] = W == 2 ? keys[(size_t)i * W + 1] : 0; return k; }
  // lookup only: returns index or -1
  long long find(const Key& k) const {
    u64 p = khash(k) & mask;
    while (true) {
      u32 v = slot[p].load(memory_order_acquire);
      if (v == 0) return -1;
      if (v == RESV) { do { v = slot[p].load(memory_order_acquire); } while (v == RESV); if (v == 0) return -1; }
      if (key_at(v - 1) == k) return v - 1;
      p = (p + 1) & mask;
    }
  }
  // insert if absent; returns index (>=0) if newly inserted, -(idx+2) if present, -1 if budget exceeded
  long long insert(const Key& k, u8 b) {
    u64 p = khash(k) & mask;
    while (true) {
      u32 v = slot[p].load(memory_order_acquire);
      if (v == 0) {
        u32 expect = 0;
        if (slot[p].compare_exchange_strong(expect, RESV, memory_order_acq_rel)) {
          long long idx = n.fetch_add(1, memory_order_acq_rel);
          if (idx >= maxstates) { budget.store(true); slot[p].store(0, memory_order_release); n.fetch_sub(1); return -1; }
          keys[(size_t)idx * W] = k.w[0]; if (W == 2) keys[(size_t)idx * W + 1] = k.w[1];
          bar[idx] = b;
          slot[p].store((u32)(idx + 1), memory_order_release);
          return idx;
        }
        v = expect;  // someone else took it; fall through to examine
      }
      if (v == RESV) { do { v = slot[p].load(memory_order_acquire); } while (v == RESV); if (v == 0) continue; }
      if (key_at(v - 1) == k) return -(long long)(v - 1) - 2;
      p = (p + 1) & mask;
    }
  }
};

// ---------------- targets ----------------
struct Targets {
  vector<pair<Key, u32>> tvec; vector<string> tid; vector<int> tkind;  // exact / aut8
  vector<u64> tkeys64;            // Sigma-key set (D format) -> converted to current width as Keys
  vector<Key> tkeys; vector<u64> bits; u64 bitmask = 0;
  vector<u64> orbits; int orbit_maxlen = 0;
  void load_targets(const string& fn, int kind, int cap) {
    ifstream in(fn); if (!in) { fprintf(stderr, "cannot open %s\n", fn.c_str()); exit(2); }
    string line; long long nread = 0, nused = 0;
    while (getline(in, line)) {
      if (line.empty() || line[0] == '#') continue;
      nread++;
      istringstream ss(line); string id, w1, w2; ss >> id >> w1 >> w2;
      u8 a[256], b[256]; int na = 0, nb = 0; bool ok = true;
      for (char c : w1) { int l = letter_of(c); if (l < 0 || na >= 120) { ok = false; break; } a[na++] = l; }
      for (char c : w2) { int l = letter_of(c); if (l < 0 || nb >= 120) { ok = false; break; } b[nb++] = l; }
      if (!ok) continue;
      na = reduce_cyc(a, na); nb = reduce_cyc(b, nb);
      if (!na || !nb || na + nb > cap) continue;
      int tidx = tid.size(); tid.push_back(id); tkind.push_back(kind); nused++;
      int nimg = kind == 1 ? 8 : 1;
      for (int g = 0; g < nimg; g++) {
        u8 ia[128], ib[128];
        for (int t = 0; t < na; t++) ia[t] = d8img(a[t], g);
        for (int t = 0; t < nb; t++) ib[t] = d8img(b[t], g);
        tvec.push_back({key_of_pair(ia, na, ib, nb), (u32)tidx});
      }
    }
    sort(tvec.begin(), tvec.end(), [](const pair<Key, u32>& x, const pair<Key, u32>& y) { return x.first < y.first || (x.first == y.first && x.second < y.second); });
    tvec.erase(unique(tvec.begin(), tvec.end(), [](const pair<Key, u32>& x, const pair<Key, u32>& y) { return x.first == y.first && x.second == y.second; }), tvec.end());
    fprintf(stderr, "targets %s: read %lld, usable(<=cap) %lld\n", fn.c_str(), nread, nused);
  }
  void load_keys(const string& fn) {  // D-format u64 Sigma keys
    FILE* f = fopen(fn.c_str(), "rb"); if (!f) { fprintf(stderr, "cannot open %s\n", fn.c_str()); exit(2); }
    u64 buf[4096]; size_t got;
    while ((got = fread(buf, 8, 4096, f)) > 0) tkeys64.insert(tkeys64.end(), buf, buf + got);
    fclose(f);
    for (u64 k : tkeys64) {
      Key kk;
      if (W == 1) { kk.w[0] = k; kk.w[1] = 0; }
      else { u8 a[128], b[128]; int na, nb; Key k1; k1.w[0] = k; k1.w[1] = 0; decode_w(k1, a, na, b, nb, 1); kk = key_of_pair(a, na, b, nb); }
      tkeys.push_back(kk);
    }
    sort(tkeys.begin(), tkeys.end()); tkeys.erase(unique(tkeys.begin(), tkeys.end()), tkeys.end());
    int lb = 24; while ((1ULL << lb) < tkeys.size() * 64 && lb < 33) lb++;  // ~64 bits per key
    bitmask = (1ULL << lb) - 1; bits.assign((1ULL << lb) / 64, 0);
    for (auto& k : tkeys) { u64 h = khash(k) & bitmask; bits[h >> 6] |= 1ULL << (h & 63); }
    fprintf(stderr, "target keys %s: %zu (bitset 2^%d bits)\n", fn.c_str(), tkeys.size(), lb);
  }
  inline bool key_hit(const Key& k) const {
    if (tkeys.empty()) return false;
    u64 h = khash(k) & bitmask;
    if (!(bits[h >> 6] >> (h & 63) & 1)) return false;
    return binary_search(tkeys.begin(), tkeys.end(), k);
  }
  void load_orbits(const string& fn, int maxlen) {
    FILE* f = fopen(fn.c_str(), "rb"); if (!f) { fprintf(stderr, "cannot open %s\n", fn.c_str()); exit(2); }
    u64 buf[4096]; size_t got;
    while ((got = fread(buf, 8, 4096, f)) > 0) orbits.insert(orbits.end(), buf, buf + got);
    fclose(f); sort(orbits.begin(), orbits.end()); orbits.erase(unique(orbits.begin(), orbits.end()), orbits.end());
    orbit_maxlen = maxlen;
    fprintf(stderr, "target orbits %s: %zu distinct, tested for states of Aut-minimal length <= %d\n", fn.c_str(), orbits.size(), maxlen);
  }
};

// ---------------- predecessor search (path reconstruction without parent pointers) ----------------
// returns true if child key c is a forward product (energy <= cap) of state (a, b)
static bool is_child_of(const u8* a, int na, const u8* b, int nb, const Key& c) {
  bool found = false;
  expand_state(a, na, b, nb, CAP, [&](int, const Key& k, int) { if (k == c) found = true; });
  return found;
}
// all candidate predecessors of state idx with smaller index; returns the verified one with least index, or -1
static long long find_pred(const Store& S, long long idx) {
  Key ck = S.key_at(idx);
  u8 A[128], B[128]; int na, nb; decode(ck, A, na, B, nb);
  long long best = -1;
  auto consider = [&](const u8* u, int nu, const u8* v, int nv) {
    if (nu <= 0 || nu + nv > CAP || !is_cyc_reduced(u, nu)) return;
    long long j = S.find(key_of_pair(u, nu, v, nv));
    if (j < 0 || j >= idx || S.bar[j] > S.bar[idx]) return;   // the true parent has smaller index and barrier <= child's
    if (best >= 0 && j >= best) return;
    if (is_child_of(u, nu, v, nv, ck)) best = j;
  };
  for (int side = 0; side < 2; side++) {
    const u8* up = side ? B : A; int L = side ? nb : na;   // the relator that was replaced
    const u8* v = side ? A : B; int nv = side ? na : nb;    // the donor (unchanged)
    // (1) parents that are forward products of the child: enumerate cyclic products of up with v
    u8 AA[128], BB[128]; memcpy(AA, up, L); memcpy(BB, v, nv);
    expand_state(AA, L, BB, nv, CAP, [&](int sd, const Key& k, int) {
      if (sd != 0) return;  // only products replacing up
      u8 x[128], y[128]; int nx, ny; decode(k, x, nx, y, ny);
      long long j = S.find(k);
      if (j < 0 || j >= idx || S.bar[j] > S.bar[idx]) return;
      if (best >= 0 && j >= best) return;
      if (is_child_of(x, nx, y, ny, ck)) best = j;
    });
    // (2) donor fully cancelled: U = a . w . a^-1 . Vs^-1 with w a rotation of up or up^-1, |a| = c3
    u8 ws[2][128]; memcpy(ws[0], up, L); for (int t = 0; t < L; t++) ws[1][t] = inv(up[L - 1 - t]);
    for (int wi = 0; wi < 2; wi++) for (int r = 0; r < L; r++) {
      u8 w[128]; for (int t = 0; t < L; t++) w[t] = ws[wi][(r + t) % L];
      for (int sg = 0; sg < 2; sg++) for (int l = 0; l < nv; l++) {
        u8 Vs[128]; for (int t = 0; t < nv; t++) Vs[t] = sg ? inv(v[(l + nv - 1 - t) % nv]) : v[(l + t) % nv];
        u8 Vi[128]; for (int t = 0; t < nv; t++) Vi[t] = inv(Vs[nv - 1 - t]);  // Vs^-1
        int c3max = (CAP - L - 2 * nv) / 2; if (c3max < 0) continue;
        for (int c3 = 0; c3 <= c3max; c3++) {
          long long total = 1; for (int t = 0; t < c3; t++) total *= 4;
          for (long long code = 0; code < total; code++) {
            u8 a[128]; long long cc = code; bool okw = true;
            for (int t = 0; t < c3; t++) { a[t] = cc & 3; cc >>= 2; if (t && a[t] == inv(a[t - 1])) { okw = false; break; } }
            if (!okw) continue;
            u8 U[256]; int m = 0;
            for (int t = 0; t < c3; t++) U[m++] = a[t];
            for (int t = 0; t < L; t++) U[m++] = w[t];
            for (int t = c3 - 1; t >= 0; t--) U[m++] = inv(a[t]);
            for (int t = 0; t < nv; t++) U[m++] = Vi[t];
            if (m + nv > CAP) continue;
            consider(U, m, v, nv);
          }
        }
      }
    }
    // (3) moved relator fully cancelled (nu < nv): U = (Vs[0:nu])^-1
    for (int sg = 0; sg < 2; sg++) for (int l = 0; l < nv; l++) {
      u8 Vs[128]; for (int t = 0; t < nv; t++) Vs[t] = sg ? inv(v[(l + nv - 1 - t) % nv]) : v[(l + t) % nv];
      for (int nu = 1; nu < nv; nu++) { u8 U[128]; for (int t = 0; t < nu; t++) U[t] = inv(Vs[nu - 1 - t]); consider(U, nu, v, nv); }
    }
  }
  return best;
}
static vector<long long> path_to(const Store& S, long long idx) {
  vector<long long> p; p.push_back(idx);
  while (idx > 0) { long long q = find_pred(S, idx); if (q < 0) { fprintf(stderr, "path reconstruction failed at %s\n", kstr(S.key_at(idx)).c_str()); break; } p.push_back(q); idx = q; }
  reverse(p.begin(), p.end()); return p;
}

// ---------------- search driver ----------------
struct Hit { long long idx; int kind; u32 tgt; u64 orbit; };  // kind 0 exact/aut8 target, 1 primitive, 2 key file, 3 orbit file

static int run_search(int argc, char** argv) {
  int cap = 25; long long maxstates = 50000000; int logtable = 0, threads = 1; bool stop_on_trivial = false;
  string src1 = "xxxYYYY", src2 = "xyxYXY";
  vector<pair<string, int>> target_files; string tkeyfile, orbitfile; int orbit_maxlen = 20;
  string dumpkeys, checkpoint, resume; int maxhits_print = 50; int dumpmax = -1; string dumpfile; int stop_level = 999;
  for (int i = 1; i < argc; i++) {
    string a = argv[i];
    auto next = [&]() { if (i + 1 >= argc) { fprintf(stderr, "missing arg for %s\n", a.c_str()); exit(2); } return string(argv[++i]); };
    if (a == "--cap") cap = stoi(next());
    else if (a == "--maxstates") maxstates = stoll(next());
    else if (a == "--logtable") logtable = stoi(next());
    else if (a == "--threads") threads = stoi(next());
    else if (a == "--width") W = stoi(next());
    else if (a == "--source") { string s = next(); size_t c = s.find(','); src1 = s.substr(0, c); src2 = s.substr(c + 1); }
    else if (a == "--exact-targets") target_files.push_back({next(), 0});
    else if (a == "--trivial-targets") target_files.push_back({next(), 1});
    else if (a == "--target-keys") tkeyfile = next();
    else if (a == "--target-orbits") orbitfile = next();
    else if (a == "--orbit-maxlen") orbit_maxlen = stoi(next());
    else if (a == "--dumpkeys") dumpkeys = next();
    else if (a == "--dump") { dumpmax = stoi(next()); dumpfile = next(); }
    else if (a == "--checkpoint") checkpoint = next();
    else if (a == "--resume") resume = next();
    else if (a == "--stop-level") stop_level = stoi(next());   // complete this barrier level, then stop (write checkpoint/dumps)
    else if (a == "--maxhits") maxhits_print = stoi(next());
    else if (a == "--stop-on-trivial") stop_on_trivial = true;
    else if (a == "--no-stop") stop_on_trivial = false;
    else { fprintf(stderr, "unknown option %s\n", a.c_str()); return 2; }
  }
  if (W != 1 && W != 2) { fprintf(stderr, "--width must be 1 or 2\n"); return 2; }
  if (W == 1 && cap > MAXL64) { W = 2; fprintf(stderr, "cap %d > 31: using 128-bit keys\n", cap); }
  if (cap > MAXL128) { fprintf(stderr, "cap must be <= %d\n", MAXL128); return 2; }
  CAP = cap;
  if (!logtable) { logtable = 20; while ((1ULL << logtable) < (u64)(maxstates / 0.7) && logtable < 34) logtable++; }
  fprintf(stderr, "width %d cap %d maxstates %lld logtable %d threads %d; memory ~%.2f GB\n", W, cap, maxstates, logtable, threads,
          ((double)maxstates * (8 * W + 1) + 4.0 * (1ULL << logtable)) / 1e9);
  Store S; S.init(maxstates, logtable);
  Targets T;
  for (auto& tf : target_files) T.load_targets(tf.first, tf.second, cap);
  if (!tkeyfile.empty()) T.load_keys(tkeyfile);
  if (!orbitfile.empty()) T.load_orbits(orbitfile, orbit_maxlen);

  mutex hitmx; vector<Hit> hits; atomic<long long> ntriv{0}, nkeyhit{0}, norbhit{0}, ntgt{0};
  auto detect = [&](long long idx, const Key& k) {
    u8 a[128], b[128]; int na, nb; decode(k, a, na, b, nb);
    if (is_primitive(a, na) || is_primitive(b, nb)) { ntriv++; lock_guard<mutex> g(hitmx); hits.push_back({idx, 1, 0, 0}); if (stop_on_trivial) S.budget.store(true); }
    if (!T.tvec.empty()) {
      auto it = lower_bound(T.tvec.begin(), T.tvec.end(), make_pair(k, (u32)0), [](const pair<Key, u32>& x, const pair<Key, u32>& y) { return x.first < y.first || (x.first == y.first && x.second < y.second); });
      for (; it != T.tvec.end() && it->first == k; ++it) { ntgt++; lock_guard<mutex> g(hitmx); hits.push_back({idx, 0, it->second, 0}); }
    }
    if (T.key_hit(k)) { nkeyhit++; lock_guard<mutex> g(hitmx); hits.push_back({idx, 2, 0, 0}); }
    if (!T.orbits.empty()) {
      u8 ma[256], mb[256]; int mna = na, mnb = nb; memcpy(ma, a, na); memcpy(mb, b, nb);
      int ml = wh_minimize(ma, mna, mb, mnb);
      if (ml <= T.orbit_maxlen) {
        u64 ok; int ml2;
        if (aut_canon64(ma, mna, mb, mnb, ok, ml2) && binary_search(T.orbits.begin(), T.orbits.end(), ok)) { norbhit++; lock_guard<mutex> g(hitmx); hits.push_back({idx, 3, 0, ok}); }
      }
    }
  };

  int start_level = 0; long long resumed = 0;
  if (!resume.empty()) {
    FILE* f = fopen(resume.c_str(), "rb"); if (!f) { fprintf(stderr, "cannot open %s\n", resume.c_str()); return 2; }
    long long hdr[4]; if (fread(hdr, 8, 4, f) != 4) return 2;   // W, cap, nstates, last_complete_barrier
    if (hdr[0] != W || hdr[1] != cap) { fprintf(stderr, "checkpoint width/cap mismatch\n"); return 2; }
    long long n = hdr[2]; start_level = (int)hdr[3] + 1; resumed = n;
    if (n > maxstates) { fprintf(stderr, "checkpoint larger than maxstates\n"); return 2; }
    // barriers are stored after the keys: read them first, then stream the keys (no 8n-byte temporary)
    vector<u8> bb((size_t)n);
    if (fseek(f, 32 + (long long)n * 8 * W, SEEK_SET) != 0 || fread(bb.data(), 1, (size_t)n, f) != (size_t)n) { fprintf(stderr, "checkpoint read error (barriers)\n"); return 2; }
    fseek(f, 32, SEEK_SET);
    const size_t CHK = 1 << 20; vector<u64> kb(CHK * W);
    for (long long i = 0; i < n; ) {
      size_t m = (size_t)min<long long>(CHK, n - i);
      if (fread(kb.data(), 8, m * W, f) != m * W) { fprintf(stderr, "checkpoint read error (keys)\n"); return 2; }
      for (size_t j = 0; j < m; j++) { Key k; k.w[0] = kb[j * W]; k.w[1] = W == 2 ? kb[j * W + 1] : 0; long long r = S.insert(k, bb[i + j]); if (r != i + (long long)j) { fprintf(stderr, "checkpoint reinsertion failed at %lld (%lld)\n", i + (long long)j, r); return 2; } }
      i += m;
    }
    fclose(f);
    fprintf(stderr, "resumed %lld states, continuing from barrier level %d\n", n, start_level);
    // detection on the resumed states is NOT redone here (it was reported by the earlier phase)
  } else {
    u8 a[128], b[128]; int na = 0, nb = 0;
    for (char c : src1) a[na++] = letter_of(c);
    for (char c : src2) b[nb++] = letter_of(c);
    na = reduce_cyc(a, na); nb = reduce_cyc(b, nb);
    Key k = key_of_pair(a, na, b, nb);
    long long r = S.insert(k, (u8)(na + nb));
    detect(r, k);
    fprintf(stderr, "source: %s (energy %d)\n", kstr(k).c_str(), na + nb);
  }

  auto t0 = chrono::steady_clock::now();
  int last_full = start_level - 1; long long expanded_total = 0;
  for (int b = start_level; b <= cap && !S.budget.load(); b++) {
    if (b > stop_level) { fprintf(stderr, "stopping after level %d as requested\n", stop_level); break; }
    long long startidx = 0; long long passes = 0; long long expanded_level = 0;
    while (true) {
      long long endidx = S.n.load();
      if (startidx >= endidx) break;
      atomic<long long> cursor{startidx}; atomic<long long> exp_cnt{0};
      auto worker = [&]() {
        const long long CH = 2048; long long ec = 0;
        while (!S.budget.load()) {
          long long i0 = cursor.fetch_add(CH); if (i0 >= endidx) break;
          long long i1 = min(endidx, i0 + CH);
          for (long long i = i0; i < i1; i++) {
            if (S.bar[i] != (u8)b) continue;
            ec++;
            u8 A[128], B[128]; int na, nb; decode(S.key_at(i), A, na, B, nb);
            expand_state(A, na, B, nb, cap, [&](int, const Key& k, int e) {
              long long r = S.insert(k, (u8)max(b, e));
              if (r >= 0) detect(r, k);
            });
          }
        }
        exp_cnt += ec;
      };
      vector<thread> th; for (int t = 0; t < threads; t++) th.emplace_back(worker); for (auto& t : th) t.join();
      expanded_level += exp_cnt.load(); passes++;
      startidx = endidx;
      if (S.budget.load()) break;
    }
    expanded_total += expanded_level;
    if (!S.budget.load()) last_full = b;
    double el = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
    if (b >= 10 || expanded_level) fprintf(stderr, "barrier %d done=%d: states %lld, expanded %lld (passes %lld), %.1fs\n", b, !S.budget.load(), S.n.load(), expanded_level, passes, el);
  }
  long long N = S.n.load();
  printf("engine m_acsearch width %d cap %d threads %d source %s %s\n", W, cap, threads, src1.c_str(), src2.c_str());
  printf("budget_hit %d last_complete_barrier %d total_states %lld expanded %lld resumed %lld\n", (int)S.budget.load(), last_full, N, expanded_total, resumed);
  vector<long long> cnt(cap + 2, 0), ecnt(cap + 2, 0);
  for (long long i = 0; i < N; i++) { int bb = S.bar[i]; if (bb <= cap) { cnt[bb]++; if (bb <= last_full) ecnt[key_energy(S.key_at(i))]++; } }
  long long cum = 0;
  for (int b = 0; b <= cap; b++) { cum += cnt[b]; if (cnt[b]) printf("src 0 barrier %d new %lld cumulative %lld%s\n", b, cnt[b], cum, b <= last_full ? "" : " (incomplete)"); }
  for (int e = 0; e <= cap; e++) if (ecnt[e]) printf("src 0 energy %d states %lld (within complete barrier<=%d)\n", e, ecnt[e], last_full);
  printf("trivializing_states %lld\ntarget_key_hits %lld\norbit_hits %lld\ntarget_hits %lld\n", ntriv.load(), nkeyhit.load(), norbhit.load(), ntgt.load());
  sort(hits.begin(), hits.end(), [](const Hit& x, const Hit& y) { return x.idx < y.idx; });
  int printed = 0;
  for (auto& h : hits) {
    const char* kindname = h.kind == 0 ? (T.tkind[h.tgt] ? "aut8-trivial" : "exact") : h.kind == 1 ? "PRIMITIVE" : h.kind == 2 ? "KEYFILE" : "ORBIT";
    string tag = h.kind == 0 ? T.tid[h.tgt] : h.kind == 1 ? "TRIVIAL" : h.kind == 2 ? "TKEYHIT" : "ORBITHIT";
    Key k = S.key_at(h.idx);
    printf("HIT target %s kind %s state [%s] barrier %d", tag.c_str(), kindname, kstr(k).c_str(), (int)S.bar[h.idx]);
    if (h.kind == 3) { Key o; o.w[0] = h.orbit; o.w[1] = 0; printf(" orbit [%s]", kstr_w(o, 1).c_str()); }
    printf("\n");
    if (printed < maxhits_print) {
      printed++;
      auto p = path_to(S, h.idx);
      bool ok = (p.size() > 0 && p[0] == 0);
      // verify the chain by forward expansion
      for (size_t i = 0; i + 1 < p.size() && ok; i++) { u8 a[128], bb[128]; int na, nb; decode(S.key_at(p[i]), a, na, bb, nb); if (!is_child_of(a, na, bb, nb, S.key_at(p[i + 1]))) ok = false; }
      printf("PATH %s len %zu verified %d :", tag.c_str(), p.size(), (int)ok);
      for (auto q : p) printf(" [%s]", kstr(S.key_at(q)).c_str());
      printf("\n");
    }
  }
  if (!dumpkeys.empty()) {
    FILE* f = fopen(dumpkeys.c_str(), "wb"); long long nk = 0;
    for (long long i = 0; i < N; i++) if (S.bar[i] <= last_full) { fwrite(&S.keys[(size_t)i * W], 8, W, f); nk++; }
    fclose(f); printf("dumped %lld keys (barrier <= %d, width %d) to %s\n", nk, last_full, W, dumpkeys.c_str());
  }
  if (dumpmax >= 0) {
    FILE* f = fopen(dumpfile.c_str(), "w");
    for (long long i = 0; i < N; i++) { Key k = S.key_at(i); if (key_energy(k) <= dumpmax && S.bar[i] <= last_full) fprintf(f, "%s %d %d 0\n", kstr(k).c_str(), key_energy(k), (int)S.bar[i]); }
    fclose(f);
  }
  if (!checkpoint.empty()) {
    FILE* f = fopen(checkpoint.c_str(), "wb"); long long hdr[4] = {W, cap, N, last_full};
    fwrite(hdr, 8, 4, f); fwrite(S.keys.data(), 8, (size_t)N * W, f); fwrite(S.bar.data(), 1, (size_t)N, f); fclose(f);
    printf("checkpoint %s: %lld states, complete through barrier %d\n", checkpoint.c_str(), N, last_full);
  }
  return 0;
}

// ---------------- --autdump KEYS OUT [--threads T] [--width W] [--maxlen M] ----------------
// Aut-canonicalizes every state of a key dump; with --maxlen M only states whose Whitehead-minimal
// total length is <= M get the (expensive) closure and are written, which suffices for a complete
// orbit comparison against any orbit set whose members all have Aut-minimal length <= M.
static int aut_dump(int argc, char** argv) {
  string keyfile = argv[2], outfile = argv[3]; int threads = 1, maxlen = 255;
  for (int i = 4; i < argc; i++) { string a = argv[i]; if (a == "--threads") threads = stoi(argv[++i]); else if (a == "--width") W = stoi(argv[++i]); else if (a == "--maxlen") maxlen = stoi(argv[++i]); }
  FILE* kf = fopen(keyfile.c_str(), "rb"); if (!kf) { fprintf(stderr, "cannot open %s\n", keyfile.c_str()); return 2; }
  fseek(kf, 0, SEEK_END); long long bytes = ftell(kf); fseek(kf, 0, SEEK_SET);
  long long n = bytes / (8 * W);
  vector<u64> keys((size_t)n * W); if (fread(keys.data(), 8, (size_t)n * W, kf) != (size_t)n * W) return 2; fclose(kf);
  atomic<long long> cursor{0}; atomic<long long> fails{0};
  vector<vector<u64>> outs(threads); vector<vector<long long>> hists(threads, vector<long long>(256, 0));
  auto worker = [&](int tid) {
    const long long CH = 4096;
    while (true) {
      long long i0 = cursor.fetch_add(CH); if (i0 >= n) break;
      long long i1 = min(n, i0 + CH);
      for (long long i = i0; i < i1; i++) {
        Key k; k.w[0] = keys[(size_t)i * W]; k.w[1] = W == 2 ? keys[(size_t)i * W + 1] : 0;
        u8 a[256], b[256]; int na, nb; decode(k, a, na, b, nb);
        int ml = wh_minimize(a, na, b, nb);
        hists[tid][min(ml, 255)]++;
        if (ml > maxlen) continue;
        u64 o; int ml2; bool ok = aut_canon64(a, na, b, nb, o, ml2);
        if (!ok) { fails++; continue; }
        outs[tid].push_back(o);
      }
    }
  };
  vector<thread> th; for (int t = 0; t < threads; t++) th.emplace_back(worker, t); for (auto& t : th) t.join();
  FILE* f = fopen(outfile.c_str(), "wb"); long long written = 0; vector<long long> hist(256, 0); int gmin = 255;
  for (int t = 0; t < threads; t++) { for (u64 o : outs[t]) fwrite(&o, 8, 1, f); written += outs[t].size(); for (int L = 0; L < 256; L++) { hist[L] += hists[t][L]; if (hists[t][L] && L < gmin) gmin = L; } }
  fclose(f);
  printf("autdump states %lld maxlen %d written %lld closure_fail %lld min_aut_length %d file %s\n", n, maxlen, written, fails.load(), gmin, outfile.c_str());
  for (int L = 0; L < 256; L++) if (hist[L]) printf("aut_min_length %d states %lld\n", L, hist[L]);
  return 0;
}

// ---------------- self-test ----------------
static int self_test() {
  mt19937_64 rng(2026);
  auto rand_word = [&](int n, u8* w) { while (true) { for (int i = 0; i < n; i++) { do { w[i] = rng() & 3; } while (i && w[i] == inv(w[i - 1])); } if (n < 2 || w[0] != inv(w[n - 1])) return; } };
  for (int width = 1; width <= 2; width++) {
    W = width;
    int maxlen = width == 1 ? 15 : 29;
    for (int it = 0; it < 200000; it++) {
      int na = 1 + rng() % maxlen, nb = 1 + rng() % maxlen;
      u8 a[128], b[128]; rand_word(na, a); rand_word(nb, b);
      Key k = key_of_pair(a, na, b, nb);
      u8 c[128], d[128]; int nc, nd; decode(k, c, nc, d, nd);
      if (!(key_of_pair(c, nc, d, nd) == k)) { printf("FAIL roundtrip width %d\n", W); return 1; }
      if (key_energy(k) != na + nb) { printf("FAIL energy\n"); return 1; }
      int r = rng() % na; u8 a2[128], b2[128];
      for (int i = 0; i < na; i++) a2[i] = a[(i + r) % na];
      for (int i = 0; i < nb; i++) b2[i] = inv(b[nb - 1 - i]);
      if (!(key_of_pair(b2, nb, a2, na) == k)) { printf("FAIL sigma invariance width %d\n", W); return 1; }
    }
    printf("width %d: 200000 random encode/decode + Sigma-invariance checks passed\n", W);
  }
  // 64-bit encoding must equal D's: compare against hard-coded values computed by D's formula for AK(3)
  W = 1;
  { u8 a[64], b[64]; int na = 0, nb = 0; for (char c : string("xxxYYYY")) a[na++] = letter_of(c); for (char c : string("xyxYXY")) b[nb++] = letter_of(c);
    Key k = key_of_pair(a, na, b, nb);
    // recompute with an independent transcription of D's encoder
    u8 ca[64], cb[64]; canon_word(a, na, ca); canon_word(b, nb, cb);
    const u8 *p = ca, *q = cb; int np = na, nq = nb; if (cmpw(ca, na, cb, nb) > 0) { p = cb; q = ca; np = nb; nq = na; }
    u64 d = 0; for (int i = 1; i < np; i++) { u8 c = p[i], f = inv(p[i - 1]); d = d * 3 + (c - (c > f ? 1 : 0)); } for (int i = 1; i < nq; i++) { u8 c = q[i], f = inv(q[i - 1]); d = d * 3 + (c - (c > f ? 1 : 0)); }
    u64 ref = ((u64)(np + nq) << 58) | ((u64)np << 53) | ((u64)p[0] << 51) | ((u64)q[0] << 49) | d;
    if (k.w[0] != ref) { printf("FAIL D encoding\n"); return 1; }
    printf("D-compatible 64-bit key of AK(3): %016llx [%s]\n", (unsigned long long)k.w[0], kstr(k).c_str()); }
  // primitivity
  auto parse = [](const char* s, u8* w) { int n = 0; for (; *s; s++) w[n++] = letter_of(*s); return n; };
  const char* prim[] = {"x", "Y", "xy", "xxy", "xyxyy", "xxyxxyxy", "YXYYXYYX", "xyxyxyy"};
  const char* nonprim[] = {"xxyy", "xxxyy", "xyXY", "xyxYXY", "xxxYYYY", "xx", "xyyxY"};
  for (auto s : prim) { u8 w[64]; int n = parse(s, w); if (!is_primitive(w, n)) { printf("FAIL primitive %s\n", s); return 1; } }
  for (auto s : nonprim) { u8 w[64]; int n = parse(s, w); if (is_primitive(w, n)) { printf("FAIL nonprimitive %s\n", s); return 1; } }
  // aut_canon64: AK(3) vs its x->xy image; trivial pair
  { u8 a[64], b[64], c[128], d[128]; int na = parse("xxxYYYY", a), nb = parse("xyxYXY", b);
    u64 k1, k2; int m1, m2; aut_canon64(a, na, b, nb, k1, m1);
    int nc = apply_wh(a, na, 0, c), nd = apply_wh(b, nb, 0, d); aut_canon64(c, nc, d, nd, k2, m2);
    if (k1 != k2 || m1 != 13) { printf("FAIL aut_canon AK3\n"); return 1; }
    Key kk; kk.w[0] = k1; kk.w[1] = 0; printf("aut-canonical AK(3): [%s]\n", kstr(kk).c_str()); }
  // small searches, both widths, 1 and 2 threads: AK(3) cap 20 -> 39840 states, T(16) -> 396497 (D/L reference counts)
  struct Ref { const char* s1; const char* s2; int cap; long long states; } refs[] = {{"xxxYYYY", "xyxYXY", 20, 39840}, {"xxxYYYY", "xyxYXY", 22, 257488}, {"x", "y", 16, 396497}};
  for (auto& r : refs) for (int width = 1; width <= 2; width++) for (int th = 1; th <= 2; th++) {
    W = width; CAP = r.cap;
    Store S; S.init(2000000, 22);
    u8 a[64], b[64]; int na = parse(r.s1, a), nb = parse(r.s2, b);
    S.insert(key_of_pair(a, na, b, nb), (u8)(na + nb));
    for (int lev = 0; lev <= r.cap; lev++) {
      long long st = 0;
      while (true) {
        long long en = S.n.load(); if (st >= en) break;
        atomic<long long> cur{st};
        auto worker = [&]() { while (true) { long long i0 = cur.fetch_add(512); if (i0 >= en) break; long long i1 = min(en, i0 + 512);
          for (long long i = i0; i < i1; i++) { if (S.bar[i] != (u8)lev) continue; u8 A[128], B[128]; int xa, xb; decode(S.key_at(i), A, xa, B, xb);
            expand_state(A, xa, B, xb, r.cap, [&](int, const Key& k, int e) { S.insert(k, (u8)max(lev, e)); }); } } };
        vector<thread> ths; for (int t = 0; t < th; t++) ths.emplace_back(worker); for (auto& t : ths) t.join();
        st = en;
      }
    }
    if (S.n.load() != r.states) { printf("FAIL search count (%s,%s) cap %d width %d threads %d: %lld != %lld\n", r.s1, r.s2, r.cap, width, th, S.n.load(), r.states); return 1; }
    // predecessor reconstruction on 30 random states: path must start at the source and every step must be a forward move
    if (th == 1) {
      for (int t = 0; t < 30; t++) {
        long long idx = rng() % S.n.load();
        auto p = path_to(S, idx);
        if (p.empty() || p[0] != 0) { printf("FAIL path reconstruction (no source)\n"); return 1; }
        for (size_t i = 0; i + 1 < p.size(); i++) { u8 A[128], B[128]; int xa, xb; decode(S.key_at(p[i]), A, xa, B, xb); if (!is_child_of(A, xa, B, xb, S.key_at(p[i + 1]))) { printf("FAIL path step\n"); return 1; } if (S.bar[p[i]] > S.bar[p[i + 1]]) { printf("FAIL barrier monotone\n"); return 1; } }
      }
    }
    printf("search (%s,%s) cap %d width %d threads %d: %lld states (reference %lld); 30 reconstructed paths verified\n", r.s1, r.s2, r.cap, width, th, S.n.load(), r.states);
  }
  W = 1;
  printf("self-test passed\n");
  return 0;
}

int main(int argc, char** argv) {
  if (argc == 2 && string(argv[1]) == "--self-test") return self_test();
  if (argc >= 4 && string(argv[1]) == "--autdump") return aut_dump(argc, argv);
  return run_search(argc, argv);
}
