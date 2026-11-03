#define main v_scanner_main
#if __has_include("v_one_phase_bases.cpp")
#include "v_one_phase_bases.cpp"
#else
#include "one_phase_bases.cpp"
#endif
#undef main
int main(int argc,char**argv){
  if(argc!=3)return 2;
  std::ifstream input(argv[1]);std::ofstream output(argv[2]);std::string line;
  while(std::getline(input,line)){
    auto tab=line.find('\t');if(tab==std::string::npos)return 3;
    auto u=line.substr(0,tab),v=line.substr(tab+1);auto graph=extended_fold(u,v);
    output<<"{\"pair\":[\""<<u<<"\",\""<<v<<"\"],\"graph\":";
    graph_json(output,graph);output<<",\"DAG_proves_primitive_absence\":"<<(proves_primitive_absence(graph)?"true":"false")<<"}\n";
  }
}
