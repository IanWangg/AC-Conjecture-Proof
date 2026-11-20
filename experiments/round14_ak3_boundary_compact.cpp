// Deduplicate native boundary records while preserving one old anchor per seed.
#define AC_ROUND07_WIDE_ORBITS_LIBRARY
#include "round07_ak3_wide_orbits.cpp"

#include <filesystem>

namespace boundary_compact {
using Code = orbit_search::Code;
using Record = std::array<Code, 4>;
using wide_orbits::energy;
using wide_orbits::Hash;
using wide_orbits::Pair;

constexpr size_t read_batch = 1 << 20;
constexpr size_t write_batch = 1 << 13;

std::string shard_file(const std::filesystem::path& work, const char* kind, size_t shard) {
    return (work / (std::string(kind) + "." + std::to_string(shard) + ".bin")).string();
}

template <typename Container>
void write_records(std::ostream& output, const Container& records) {
    output.write(reinterpret_cast<const char*>(records.data()), records.size() * sizeof(Record));
    if (!output) throw std::runtime_error("cannot write boundary shard");
}

uint64_t partition(unsigned cap, const std::filesystem::path& work, size_t shards,
                   int inputs, char** paths) {
    std::vector<std::ofstream> outputs(shards);
    std::vector<std::vector<Record>> buckets(shards);
    for (size_t i = 0; i < shards; ++i) {
        outputs[i].open(shard_file(work, "raw", i), std::ios::binary);
        if (!outputs[i]) throw std::runtime_error("cannot open boundary shard");
        buckets[i].reserve(write_batch);
    }
    std::vector<Record> input_batch(read_batch);
    uint64_t done = 0;
    for (int i = 0; i < inputs; ++i) {
        std::ifstream source(paths[i], std::ios::binary);
        if (!source) throw std::runtime_error("cannot read boundary input");
        for (;;) {
            source.read(reinterpret_cast<char*>(input_batch.data()),
                        input_batch.size() * sizeof(Record));
            const auto bytes = source.gcount();
            if (bytes % sizeof(Record)) throw std::runtime_error("truncated boundary record");
            const auto count = bytes / sizeof(Record);
            for (size_t at = 0; at < size_t(count); ++at) {
                const auto& row = input_batch[at];
                const Pair child{row[0], row[1]}, parent{row[2], row[3]};
                if (!child.first || !child.second || !parent.first || !parent.second
                    || child.first > child.second || parent.first > parent.second
                    || energy(child) != cap || energy(parent) >= cap)
                    throw std::runtime_error("record exceeds boundary scope");
                const auto shard = Hash{}(child) & (shards - 1);
                auto& bucket = buckets[shard];
                bucket.push_back(row);
                if (bucket.size() == write_batch) {
                    write_records(outputs[shard], bucket);
                    bucket.clear();
                }
            }
            done += count;
            if (!(done % (read_batch * 128)))
                std::cerr << "partitioned " << done << " records\n";
            if (source.eof()) break;
            if (!source) throw std::runtime_error("boundary read failed");
        }
    }
    if (!done) throw std::runtime_error("empty boundary inputs");
    for (size_t i = 0; i < shards; ++i) {
        write_records(outputs[i], buckets[i]);
        outputs[i].close();
        if (!outputs[i]) throw std::runtime_error("cannot close boundary shard");
    }
    return done;
}

struct Counts { uint64_t records, seeds; };

Counts compact_shard(const std::filesystem::path& work, size_t shard) {
    const auto raw = shard_file(work, "raw", shard);
    std::ifstream source(raw, std::ios::binary | std::ios::ate);
    const auto bytes = source.tellg();
    if (!source || bytes < 0 || bytes % sizeof(Record))
        throw std::runtime_error("invalid boundary shard");
    const size_t rows = bytes / sizeof(Record);
    std::vector<Record> records(rows);
    source.seekg(0);
    if (rows) source.read(reinterpret_cast<char*>(records.data()), bytes);
    if (!source) throw std::runtime_error("could not read whole shard");
    source.close();
    std::sort(records.begin(), records.end());
    records.erase(std::unique(records.begin(), records.end(), [](const auto& a, const auto& b) {
        return a[0] == b[0] && a[1] == b[1];
    }), records.end());
    const auto output_path = shard_file(work, "unique", shard);
    std::ofstream output(output_path, std::ios::binary);
    if (!output) throw std::runtime_error("cannot open compact shard");
    write_records(output, records);
    output.close();
    if (!output) throw std::runtime_error("cannot close compact shard");
    std::filesystem::remove(raw);
    return {rows, records.size()};
}

int run(unsigned cap, unsigned workers, const std::filesystem::path& work, size_t shards,
        int inputs, char** paths) {
    if (cap < 14 || cap > 62 || !workers || !inputs || !shards || (shards & (shards - 1)) || shards > 256)
        throw std::runtime_error("need valid cap, workers, and at most 256 power-of-two shards");
    if (!std::filesystem::create_directory(work)) throw std::runtime_error("need a new work directory");
    const auto input_records = partition(cap, work, shards, inputs, paths);
    std::cerr << "full input partitioned, " << input_records << " records\n";
    std::vector<Counts> counts(shards);
    std::vector<std::future<void>> jobs;
    std::atomic<size_t> next_shard(0), done(0);
    for (unsigned worker = 0; worker < std::min<size_t>(workers, shards); ++worker) {
        jobs.push_back(std::async(std::launch::async, [&] {
            for (;;) {
                const auto shard = next_shard++;
                if (shard >= shards) break;
                counts[shard] = compact_shard(work, shard);
                const auto finished = ++done;
                if (!(finished % 16)) std::cerr << "compacted " << finished << " shards\n";
            }
        }));
    }
    for (auto& job : jobs) job.get();
    uint64_t all_records = 0, all_seeds = 0;
    for (const auto& count : counts) {
        all_records += count.records;
        all_seeds += count.seeds;
    }
    if (input_records != all_records) throw std::runtime_error("input record census disagrees");
    std::cout << "{\n  \"cyclic_cap\":" << cap << ",\n  \"input_records\":" << all_records
              << ",\n  \"distinct_seeds\":" << all_seeds
              << ",\n  \"duplicate_records\":" << all_records - all_seeds << ",\n  \"shards\":[";
    for (size_t i = 0; i < shards; ++i) {
        if (i) std::cout << ',';
        std::cout << "\n    {\"index\":" << i << ",\"input_records\":" << counts[i].records
                  << ",\"seeds\":" << counts[i].seeds << '}';
    }
    std::cout << "\n  ]\n}\n";
    return 0;
}
}  // namespace boundary_compact

int main(int argc, char** argv) {
    try {
        if (argc < 6)
            throw std::runtime_error("usage: boundary-compact cap workers output-dir shards boundary.bin ...");
        return boundary_compact::run(std::stoul(argv[1]), std::stoul(argv[2]), argv[3],
                                     std::stoul(argv[4]), argc - 5, argv + 5);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
