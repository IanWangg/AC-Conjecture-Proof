#define AC_ROUND07_WIDE_ORBITS_LIBRARY
#include "round07_ak3_wide_orbits.cpp"

namespace bs_normal {
using orbit_search::Code;
using orbit_search::word;
using orbit_search::word_code;
using Record = std::array<Code,4>;

struct Chart { int n; std::string x,y; };
struct Syllable { int sign; int64_t exponent; };

std::string mark(const std::string& w, const Chart& chart) {
    const auto X = inverse(chart.x), Y = inverse(chart.y);
    std::string result;
    for (const auto c : w) result += c=='x' ? chart.x : c=='X' ? X : c=='y' ? chart.y : Y;
    return result;
}

size_t cyclic_hnn_length(const std::string& word, int n) {
    const auto cut = word.find_first_of("yY");
    if (cut==std::string::npos) throw std::runtime_error("receiver is outside the height-one branch");
    const auto rotated = word.substr(cut)+word.substr(0,cut);
    std::vector<Syllable> ring;
    int height = 0;
    for (const auto c : rotated) {
        if (c=='y' || c=='Y') {
            const int sign = c=='y' ? 1 : -1;
            height += sign;
            ring.push_back({sign,0});
        } else {
            ring.back().exponent += c=='x' ? 1 : -1;
        }
    }
    if (std::abs(height)!=1) throw std::runtime_error("receiver has wrong marked height");
    while (ring.size()>1) {
        bool reduced = false;
        for (size_t i=0; i<ring.size(); ++i) {
            const auto j = (i+1)%ring.size();
            if (ring[i].sign==ring[j].sign) continue;
            const int initial = ring[i].sign>0 ? n : n+1;
            const int final = ring[i].sign>0 ? n+1 : n;
            if (ring[i].exponent%initial) continue;
            const auto before = (i+ring.size()-1)%ring.size();
            int64_t merged, scaled;
            if (__builtin_mul_overflow(ring[i].exponent / initial,int64_t(final),&scaled) ||
                __builtin_add_overflow(ring[before].exponent,scaled,&merged) ||
                __builtin_add_overflow(merged,ring[j].exponent,&merged))
                throw std::overflow_error("cyclic HNN exponent overflow");
            ring[before].exponent = merged;
            ring.erase(ring.begin()+std::max(i,j));
            ring.erase(ring.begin()+std::min(i,j));
            reduced=true;
            break;
        }
        if (!reduced) break;
    }
    return ring.size();
}

int run(const char* atlas,int count,char** files) {
    std::ifstream input(atlas);
    if (!input) throw std::runtime_error("cannot read the BS atlas");
    std::unordered_map<Code,Chart> marks;
    std::map<int,uint64_t> candidates;
    Chart chart;
    for (std::string row; input>>row>>chart.n>>chart.x>>chart.y;) {
        if (row.size()>31 || chart.n<2 || !marks.emplace(word_code(row),chart).second)
            throw std::runtime_error("invalid BS chart");
        candidates.try_emplace(chart.n,0);
    }
    if (!input.eof() || marks.empty()) throw std::runtime_error("empty BS atlas");
    std::vector<Record> batch(1<<19);
    uint64_t scanned=0;
    std::string hit;
    for (int file=0; file<count && hit.empty(); ++file) {
        std::ifstream stream(files[file],std::ios::binary);
        if (!stream) throw std::runtime_error("cannot open boundary shard");
        for (;;) {
            stream.read(reinterpret_cast<char*>(batch.data()),batch.size()*sizeof(Record));
            const auto bytes=stream.gcount();
            if (bytes%sizeof(Record)) throw std::runtime_error("truncated boundary shard");
            for (size_t i=0; i<size_t(bytes)/sizeof(Record) && hit.empty(); ++i) {
                const auto& record=batch[i];
                ++scanned;
                for (unsigned r=0; r<2; ++r) {
                    const auto found=marks.find(record[r]);
                    if (found==marks.end()) continue;
                    const auto& basis=found->second;
                    ++candidates.at(basis.n);
                    if (cyclic_hnn_length(mark(word(record[1-r]),basis),basis.n)!=1) continue;
                    hit="{\"child\":[\""+word(record[0])+"\",\""+word(record[1])
                        +"\"],\"anchor\":[\""+word(record[2])+"\",\""+word(record[3])
                        +"\"],\"fixed_slot\":"+std::to_string(r)+",\"n\":"+std::to_string(basis.n)+"}";
                    break;
                }
            }
            if (!hit.empty() || stream.eof()) break;
            if (!stream) throw std::runtime_error("boundary input error");
        }
        if ((file+1)%16==0) std::cerr<<"checked "<<file+1<<" shards, "<<scanned<<" seeds\n";
    }
    std::cout<<"{\n  \"atlas_marked_keys\":"<<marks.size()<<",\n  \"seeds_checked\":"<<scanned
             <<",\n  \"complete\":"<<(hit.empty()?"true":"false")<<",\n  \"hit\":"
             <<(hit.empty()?"null":hit)<<",\n  \"candidates\":{";
    bool first=true;
    for (const auto& [n,c] : candidates) {
        if (!first) std::cout<<',';
        first=false;
        std::cout<<"\n    \""<<n<<"\":"<<c;
    }
    std::cout<<"\n  }\n}\n";
    return 0;
}
} // namespace bs_normal

int main(int argc,char** argv) {
    try {
        if (argc<3) throw std::runtime_error("usage: bs-normal atlas.tsv shard.bin ...");
        return bs_normal::run(argv[1],argc-2,argv+2);
    } catch (const std::exception& error) {
        std::cerr<<error.what()<<'\n';
        return 1;
    }
}
