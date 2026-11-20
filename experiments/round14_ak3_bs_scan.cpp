#define AC_ROUND07_WIDE_ORBITS_LIBRARY
#include "round07_ak3_wide_orbits.cpp"

using orbit_search::Code;
using Record = std::array<Code,4>;

int run(const char* atlas, int count, char** files) {
    std::ifstream words(atlas);
    if (!words) throw std::runtime_error("could not read the Baumslag-Solitar atlas");
    std::unordered_set<Code> keys;
    uint64_t classes = 0, checked = 0;
    for (std::string w; words >> w;) {
        if (w.empty() || w.size() > 31) throw std::runtime_error("atlas word exceeds encoding");
        const auto images = orbit_search::build_orbit(orbit_search::word_code(w));
        keys.insert(images.begin(),images.end());
        ++classes;
    }
    if (keys.empty()) throw std::runtime_error("empty Baumslag-Solitar atlas");

    std::vector<Record> chunk(1 << 19);
    const char* file = nullptr;
    Record hit{};
    for (int i = 0; i < count && !file; ++i) {
        std::ifstream input(files[i],std::ios::binary);
        if (!input) throw std::runtime_error("could not read seed shard");
        while (!file) {
            input.read(reinterpret_cast<char*>(chunk.data()),chunk.size()*sizeof(Record));
            if (input.gcount()%sizeof(Record)) throw std::runtime_error("truncated seed record");
            const auto records = input.gcount()/sizeof(Record);
            for (size_t j=0; j<size_t(records); ++j) {
                ++checked;
                const auto& r=chunk[j];
                if (!keys.count(r[0]) && !keys.count(r[1])) continue;
                hit=r;
                file=files[i];
                break;
            }
            if (input.eof()) break;
            if (!input) throw std::runtime_error("cannot read whole seed shard");
        }
        if ((i+1)%16==0) std::cerr<<"checked "<<i+1<<" shards, "<<checked<<" seeds\n";
    }
    std::cout<<"{\n  \"atlas_classes\":"<<classes<<",\n  \"atlas_marked_keys\":"<<keys.size()
             <<",\n  \"seed_records_checked\":"<<checked<<",\n  \"complete\":"<<(file?"false":"true")
             <<",\n  \"hit\":";
    if (file) {
        using orbit_search::word;
        std::cout<<"{\"child\":[\""<<word(hit[0])<<"\",\""<<word(hit[1])
                 <<"\"],\"anchor\":[\""<<word(hit[2])<<"\",\""<<word(hit[3])<<"\"]}";
    } else {
        std::cout<<"null";
    }
    std::cout<<"\n}\n";
    return 0;
}

int main(int argc,char** argv) {
    try {
        if (argc<3) throw std::runtime_error("usage: bs-scan atlas.tsv seed-shard.bin ...");
        return run(argv[1],argc-2,argv+2);
    } catch (const std::exception& error) {
        std::cerr<<error.what()<<'\n';
        return 1;
    }
}
