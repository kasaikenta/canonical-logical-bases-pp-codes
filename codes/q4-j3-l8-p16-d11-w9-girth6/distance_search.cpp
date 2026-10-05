// Same search and pruning as hardware/quotient_search.cpp.
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
  int n,m,k,orbitsize,lim,blocks,unsat=0,cost=0;
  vector<array<Edge,3>> edges;
  vector<vector<int>> neighbors;
  vector<array<vector<uint64_t>,3>> labels;
  vector<int> assigned,forbidden,syndrome;
  vector<uint64_t> syndrome_bits;
  vector<uint64_t> logical;
  vector<uint64_t> packing_mark;
  uint64_t packing_epoch=0;
  vector<pair<int,int>> support,witness;
  uint64_t nodes=0,closed_stabilizers=0;
  bool found=false,timedout=false;
  chrono::steady_clock::time_point start;
  double seconds;
  void change(int v,int a) {
    for (auto e:edges[v]) {
      int old=syndrome[e.check];
      int next=old^mul4(a,e.coefficient);
      unsat+=(next!=0)-(old!=0);syndrome[e.check]=next;
      if ((old==0)!=(next==0)) syndrome_bits[e.check/64]^=uint64_t(1)<<(e.check%64);
    }
  }
  bool logical_nonzero() {
    for (int j=0;j<blocks;++j) {
      uint64_t x=0;for (auto p:support) x^=labels[p.first][p.second-1][j];
      if(x)return true;
    }return false;
  }
  void dfs() {
    ++nodes;
    if ((nodes&16383)==0 && chrono::duration<double>(chrono::steady_clock::now()-start).count()>seconds) {
      timedout=true;return;
    }
    if (!unsat) {
      if(logical_nonzero()) {found=true;witness=support;}
      else ++closed_stabilizers;
      return;
    }
    int remaining=lim-cost;
    if (remaining<=0 || unsat>3*remaining)return;
    // A set of unsatisfied checks with no available variable touching two
    // members needs at least that many additional symbols (each costs >=1).
    // A greedy packing gives a valid lower bound, not an assumed optimum.
    uint64_t epoch=++packing_epoch;
    // At most 3*lim unsatisfied checks; this variant accepts lim<=27.
    int active[81],active_count=0;
    for(int b=0;b<(int)syndrome_bits.size();++b){
      uint64_t mask=syndrome_bits[b];
      while(mask){int t=__builtin_ctzll(mask);mask&=mask-1;active[active_count++]=64*b+t;}
    }
    int packed=0;
    for(int at=0;at<active_count;++at){int row=active[at];if(packing_mark[row]==epoch)continue;
      if(++packed>remaining)return;
      packing_mark[row]=epoch;
      for(int v:neighbors[row])if(!assigned[v]&&!forbidden[v])
        for(auto e:edges[v])packing_mark[e.check]=epoch;
    }
    int chosen=-1,best=100000;
    for (int at=0;at<active_count;++at) {int row=active[at];
      int cnt=0;
      for (int v:neighbors[row])if(!assigned[v]&&!forbidden[v])++cnt;
      if (!cnt)return;
      if(cnt<best){chosen=row;best=cnt;}
    }
    vector<int> excluded;
    for (int v:neighbors[chosen]) {
      if (assigned[v]||forbidden[v])continue;
      for (int a=1;a<=3;++a) {
        int w=a==3?2:1;
        if (w>remaining)continue;
        assigned[v]=a;cost+=w;support.push_back({v,a});change(v,a);
        dfs();
        change(v,a);support.pop_back();cost-=w;assigned[v]=0;
        if(found||timedout)break;
      }
      forbidden[v]=1;excluded.push_back(v);
      if(found||timedout)break;
    }
    for(int v:excluded)forbidden[v]=0;
  }
  void run(const string& input,const string& output) {
    ifstream in(input);in>>n>>m>>k>>orbitsize;
    blocks=(k+63)/64;edges.resize(n);neighbors.resize(m);labels.resize(n);
    for(int v=0;v<n;++v)for(auto &e:edges[v]){in>>e.check>>e.coefficient;neighbors[e.check].push_back(v);}
    for(int v=0;v<n;++v)for(int a=0;a<3;++a){labels[v][a].resize(blocks);for(auto &x:labels[v][a])in>>x;}
    if(!in){cerr<<"invalid input\n";exit(2);}
    assigned.assign(n,0);forbidden.assign(n,0);syndrome.assign(m,0);logical.assign(blocks,0);packing_mark.assign(m,0);
    syndrome_bits.assign((m+63)/64,0);
    start=chrono::steady_clock::now();int completed=0,total=3*n/orbitsize;
    for(int base=0;base<n/orbitsize && !found && !timedout;++base){
      int root=base*orbitsize;
      for(int v=0;v<root;++v)forbidden[v]=1;
      for(int a=1;a<=3;++a){
        cost=a==3?2:1;assigned[root]=a;support={{root,a}};change(root,a);
        if(cost<=lim)dfs();
        change(root,a);assigned[root]=0;support.clear();cost=0;
        if(found||timedout)break;
        ++completed;
      }
    }
    double elapsed=chrono::duration<double>(chrono::steady_clock::now()-start).count();
    ofstream out(output);
    out<<"{\"bound\":"<<lim<<",\"complete_exclusion\":"<<(!found&&!timedout?"true":"false")
       <<",\"found\":"<<(found?"true":"false")<<",\"timed_out\":"<<(timedout?"true":"false")
       <<",\"completed_roots\":"<<completed<<",\"total_roots\":"<<total
       <<",\"nodes\":"<<nodes<<",\"closed_stabilizer_partials\":"<<closed_stabilizers
       <<",\"elapsed_seconds\":"<<elapsed<<",\"witness\":[";
    for(size_t i=0;i<witness.size();++i){if(i)out<<",";out<<"["<<witness[i].first<<","<<witness[i].second<<"]";}
    out<<"]}\n";out.close();ifstream summary(output);cout<<summary.rdbuf();
  }
};
int main(int argc,char**argv){
  if(argc!=5){cerr<<"input output bound timeout_seconds\n";return 2;}
  Search s;s.lim=stoi(argv[3]);s.seconds=stod(argv[4]);if(s.lim<1||s.lim>27)return 2;s.run(argv[1],argv[2]);
}
