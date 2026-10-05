// Complete search with stabilizer-coset minimality and binary-check packing.
// A packing consists of unsatisfied physical binary checks with disjoint
// available binary-bit neighborhoods. Each packed check needs a distinct
// additional bit, hence the packing size is a safe binary-weight lower bound.
// A minimum logical word overlaps each stabilizer row in at most half its weight.
// Enumerate only nonzero syndrome checks; defer logical labels until closure.
// Complete bounded search for a nonzero GF(4) syndrome-kernel quotient.
// Symbol coefficients have binary costs 1,1,2. No heuristic pruning.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <utility>
#include <vector>
using namespace std;
struct Edge { int check, coefficient; };
int mul4(int a,int b) {
  return ((a&1)*(b&1)^((a>>1)*(b>>1))) |
    ((((a&1)*(b>>1))^((a>>1)*(b&1))^((a>>1)*(b>>1)))<<1);
}
struct Search {
  int maxdegree=0;
  int ns,m,k,P,lim,n,unsat=0,active_symbols=0,cost=0,nonminimal=0;
  int root_first=0,root_last=-1;
  vector<array<Edge,3>> edges;
  vector<vector<int>> neighbors,incidence,stabilizer_incidence;
  vector<array<vector<uint64_t>,3>> labels;
  vector<int> assigned,forbidden,syndrome,stabilizer_overlap,stabilizer_half;
  vector<uint64_t> syndrome_bits,mark;
  uint64_t epoch=0,nodes=0,closed_stabilizers=0;
  vector<int> support,witness;
  string stabilizer_input;
  bool found=false,timedout=false;
  chrono::steady_clock::time_point start;
  double seconds;
  void change(int v){
    for(int r:incidence[v]){
      int old_symbol=syndrome[2*(r/2)]||syndrome[2*(r/2)+1];
      unsat+=syndrome[r]?-1:1;syndrome[r]^=1;
      int next_symbol=syndrome[2*(r/2)]||syndrome[2*(r/2)+1];
      active_symbols+=next_symbol-old_symbol;
      syndrome_bits[r/64]^=uint64_t(1)<<(r%64);
    }
  }
  void coset_change(int v,int delta){
    for(int r:stabilizer_incidence[v]){
      int old=stabilizer_overlap[r],next=old+delta;
      nonminimal+=(next>stabilizer_half[r])-(old>stabilizer_half[r]);stabilizer_overlap[r]=next;
    }
  }
  bool logical_nonzero(){
    for(int j=0;j<(k+63)/64;++j){uint64_t w=0;
      for(int v:support)w^=labels[v/2][v%2][j];
      if(w)return true;
    }return false;
  }
  void dfs(){
    ++nodes;if(nonminimal)return;
    if((nodes&16383)==0&&chrono::duration<double>(chrono::steady_clock::now()-start).count()>seconds){timedout=true;return;}
    if(!unsat){if(logical_nonzero()){found=true;witness=support;}else ++closed_stabilizers;return;}
    int remaining=lim-cost;
    if(remaining<=0||unsat>maxdegree*remaining||active_symbols>3*remaining)return;
    int active[162],na=0;
    for(int b=0;b<(int)syndrome_bits.size();++b){uint64_t x=syndrome_bits[b];while(x){int t=__builtin_ctzll(x);x&=x-1;active[na++]=64*b+t;}}
    uint64_t stamp=++epoch;int packed=0;
    for(int j=0;j<na;++j){int r=active[j];if(mark[r]==stamp)continue;
      if(++packed>remaining)return;mark[r]=stamp;
      for(int v:neighbors[r])if(!assigned[v]&&!forbidden[v])for(int t:incidence[v])mark[t]=stamp;
    }
    int chosen=-1,best=100000;
    for(int j=0;j<na;++j){int r=active[j],cnt=0;
      for(int v:neighbors[r])if(!assigned[v]&&!forbidden[v])++cnt;
      if(!cnt)return;if(cnt<best){chosen=r;best=cnt;}
    }
    vector<int> excluded;
    for(int v:neighbors[chosen]){
      if(assigned[v]||forbidden[v])continue;
      assigned[v]=1;++cost;support.push_back(v);change(v);coset_change(v,1);
      dfs();coset_change(v,-1);change(v);support.pop_back();--cost;assigned[v]=0;
      forbidden[v]=1;excluded.push_back(v);if(found||timedout)break;
    }
    for(int v:excluded)forbidden[v]=0;
  }
  void run(const string& input,const string& output){
    ifstream in(input);in>>ns>>m>>k>>P;n=2*ns;
    edges.resize(ns);labels.resize(ns);neighbors.resize(2*m);incidence.resize(n);
    for(int v=0;v<ns;++v)for(auto &e:edges[v]){
      in>>e.check>>e.coefficient;
      for(int b=0;b<2;++b){int val=mul4(1<<b,e.coefficient);for(int t=0;t<2;++t)if(val&(1<<t)){
        neighbors[2*e.check+t].push_back(2*v+b);incidence[2*v+b].push_back(2*e.check+t);
      }}
    }
    for(auto &x:incidence)maxdegree=max(maxdegree,(int)x.size());
    for(int v=0;v<ns;++v)for(int a=0;a<3;++a){labels[v][a].resize((k+63)/64);for(auto &w:labels[v][a])in>>w;}
    if(!in){cerr<<"invalid input\n";exit(2);}
    ifstream st(stabilizer_input);int nr,nb;st>>nr>>nb;if(nb!=n||nr<1)exit(2);
    stabilizer_incidence.resize(n);stabilizer_overlap.assign(nr,0);stabilizer_half.resize(nr);
    for(int r=0;r<nr;++r){int wt;st>>wt;stabilizer_half[r]=wt/2;for(int j=0;j<wt;++j){int bit;st>>bit;if(bit<0||bit>=n)exit(2);stabilizer_incidence[bit].push_back(r);}}
    if(!st)exit(2);
    assigned.assign(n,0);forbidden.assign(n,0);syndrome.assign(2*m,0);mark.assign(2*m,0);syndrome_bits.assign((2*m+63)/64,0);
    int full=2*ns/P;if(root_last<0)root_last=full;if(root_first<0||root_first>=root_last||root_last>full)exit(2);
    start=chrono::steady_clock::now();int completed=0;
    for(int base=0;base<ns/P&&!found&&!timedout;++base){int root=2*base*P;
      for(int v=0;v<root;++v)forbidden[v]=1;
      for(int b=0;b<2;++b){int r=2*base+b;
        if(b==1)forbidden[root]=1;
        if(r<root_first||r>=root_last)continue;
        int v=root+b;assigned[v]=1;cost=1;support={v};change(v);coset_change(v,1);
        dfs();coset_change(v,-1);change(v);assigned[v]=0;cost=0;support.clear();
        if(found||timedout)break;++completed;
      }
      forbidden[root]=0;
    }
    double elapsed=chrono::duration<double>(chrono::steady_clock::now()-start).count();
    ofstream out(output);out<<"{\"engine\":\"physical_binary_bit_branching_v1\",\"bound\":"<<lim<<",\"complete_exclusion\":"<<(!found&&!timedout?"true":"false")
      <<",\"found\":"<<(found?"true":"false")<<",\"timed_out\":"<<(timedout?"true":"false")<<",\"completed_roots\":"<<completed
      <<",\"total_roots\":"<<root_last-root_first<<",\"root_first\":"<<root_first<<",\"root_last\":"<<root_last<<",\"full_total_roots\":"<<full
      <<",\"root_scope\":\"two physical-bit roots per base column; checked QC shift invariance required\",\"nodes\":"<<nodes
      <<",\"closed_stabilizer_partials\":"<<closed_stabilizers<<",\"elapsed_seconds\":"<<elapsed<<",\"witness\":[";
    vector<int> val(ns,0);for(int v:witness)val[v/2]^=1<<(v%2);bool comma=false;
    for(int v=0;v<ns;++v)if(val[v]){if(comma)out<<",";out<<"["<<v<<","<<val[v]<<"]";comma=true;}out<<"]}\n";out.close();
    ifstream result(output);cout<<result.rdbuf();
  }
};
int main(int argc,char**argv){if(argc!=6&&argc!=8)return 2;Search s;s.lim=stoi(argv[3]);s.seconds=stod(argv[4]);s.stabilizer_input=argv[5];
 if(argc==8){s.root_first=stoi(argv[6]);s.root_last=stoi(argv[7]);}if(s.lim<1||s.lim>27)return 2;s.run(argv[1],argv[2]);}
