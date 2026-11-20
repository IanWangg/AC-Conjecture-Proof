// Verify rank-two primitive coordinates in a headerless anchored-pair ledger.
#include <array>
#include <cstdint>
#include <fstream>
#include <future>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <unordered_set>
#include <vector>

namespace {
using Code = uint64_t;
using Record = std::array<Code,4>;
using PrimitiveWords = std::unordered_set<Code>;

PrimitiveWords primitive_words() {
    PrimitiveWords words{4,5,6,7};
    for (unsigned a = 1; a < 31; ++a) {
        for (unsigned b = 1; a + b <= 31; ++b) {
            if (std::gcd(a,b) != 1) continue;
            const auto length = a + b;
            const auto sentinel = Code(1) << (2 * length);
            for (unsigned x_sign = 0; x_sign < 2; ++x_sign)
                for (unsigned y_sign = 0; y_sign < 2; ++y_sign) {
                    Code packed = 0;
                    for (unsigned i = 0; i < length; ++i) {
                        const bool y = (i+1)*b/length != i*b/length;
                        packed = (packed << 2) | (y ? 2+y_sign : x_sign);
                    }
                    for (unsigned i = 0; i < length; ++i) {
                        if (!words.insert(sentinel | packed).second)
                            throw std::runtime_error("repeated Christoffel rotation");
                        packed = ((packed << 2) & (sentinel-1)) | (packed >> (2*length-2));
                    }
                }
        }
    }
    return words;
}

bool single_sign(Code key) {
    if (key < 4) throw std::runtime_error("empty or malformed coordinate key");
    unsigned signs = 0;
    while (key > 1) {
        signs |= 1U << (key & 3);
        key >>= 2;
    }
    if (!key) throw std::runtime_error("invalid coordinate sentinel");
    return (signs & 3) != 3 && (signs & 12) != 12;
}

struct Counts {
    uint64_t sign_pure = 0;
    uint64_t hits = 0;
    Code first_hit = 0;
};

int scan(const char* path, unsigned workers) {
    if (!workers) throw std::runtime_error("need positive workers");
    const auto cases = primitive_words();
    std::ifstream input(path,std::ios::binary);
    if (!input) throw std::runtime_error("cannot open orbit ledger");
    std::vector<Record> records(1 << 20);
    uint64_t rows = 0;
    Counts totals;
    while (true) {
        input.read(reinterpret_cast<char*>(records.data()),records.size()*sizeof(Record));
        const auto bytes = input.gcount();
        if (bytes % sizeof(Record)) throw std::runtime_error("truncated orbit ledger");
        const size_t count = bytes / sizeof(Record);
        std::vector<std::future<Counts>> jobs;
        for (unsigned worker = 0; worker < workers && count; ++worker) {
            jobs.push_back(std::async(std::launch::async, [&,worker] {
                Counts local;
                for (size_t i = count*worker/workers; i < count*(worker+1)/workers; ++i) {
                    for (size_t col : {0,1}) {
                        const auto coordinate = records[i][col];
                        if (!single_sign(coordinate)) continue;
                        ++local.sign_pure;
                        if (cases.count(coordinate)) {
                            ++local.hits;
                            if (!local.first_hit) local.first_hit = coordinate;
                        }
                    }
                }
                return local;
            }));
        }
        for (auto& job : jobs) {
            const auto local = job.get();
            totals.sign_pure += local.sign_pure;
            totals.hits += local.hits;
            if (!totals.first_hit) totals.first_hit = local.first_hit;
        }
        rows += count;
        if (input.eof()) break;
        if (!input) throw std::runtime_error("could not read orbit ledger");
    }
    if (!rows) throw std::runtime_error("empty orbit ledger");
    std::cout << "{\"rows\":" << rows << ",\"primitive_word_classes_with_rotations\":" << cases.size()
              << ",\"sign_pure_coordinates\":" << totals.sign_pure
              << ",\"primitive_coordinate_occurrences\":" << totals.hits
              << ",\"first_hit_code\":" << totals.first_hit << "}\n";
    return 0;
}
}

int main(int argc, char** argv) {
    try {
        if (argc != 3) throw std::runtime_error("usage: cyclic-primitives orbit-ledger.bin workers");
        return scan(argv[1],std::stoul(argv[2]));
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
