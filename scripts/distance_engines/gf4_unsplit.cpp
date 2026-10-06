// Independent exhaustive GF(4) irreducible-cluster search, binary-weight metric.
#include <algorithm>
#include <array>
#include <chrono>
#include <fstream>
#include <iostream>
#include <vector>
#include <cstdint>
using namespace std;
int mul4[4][4]={{0,0,0,0},{0,1,2,3},{0,2,3,1},{0,3,1,2}};
struct Edge {int c,a;};
int n,m,K,L,root,N; double seconds; vector<array<Edge,3>> E;vector<vector<int>> adjc;
vector<array<vector<uint64_t>,4>> logical_labels;vector<int>s,val;vector<char>ban;vector<uint64_t>label;
uint64_t nodes=0;bool timeoutflag=false,found=false;vector<int>witness;
auto starttime=chrono::steady_clock::now();
void apply(int v,int a){for(auto e:E[v])s[e.c]^=mul4[e.a][a];for(int t=0;t<K;t++)label[t]^=logical_labels[v][a][t];}
void dfs(int cost){
 if(found||timeoutflag)return;
 if((++nodes&16383)==0 && chrono::duration<double>(chrono::steady_clock::now()-starttime).count()>seconds){timeoutflag=true;return;}
 vector<int>active;for(int c=0;c<m;c++)if(s[c])active.push_back(c);
 if(active.empty()){for(auto x:label)if(x){found=true;witness=val;break;}return;}
 int rem=L-cost;if(rem<=0||int(active.size())>3*rem)return;
 int T=0;for(int v=0;v<n;v++)if(!val[v]&&!ban[v]){int t=0;for(auto e:E[v])t+=s[e.c]!=0;if(t==3)T++;}
 if(int(active.size())>2*rem+T)return;
 int best=-1,bsize=100000;vector<char>covered(m,0);int pack=0;
 for(int c:active){int avail=0;for(int v:adjc[c])if(!val[v]&&!ban[v])avail++;if(!avail)return;if(avail<bsize){bsize=avail;best=c;}
 if(!covered[c]){pack++;if(pack>rem)return;for(int v:adjc[c])if(!val[v]&&!ban[v])for(auto e:E[v])covered[e.c]=1;}}
 vector<int>local;
 for(int v:adjc[best])if(!val[v]&&!ban[v]){
  for(int a=1;a<=3;a++){int w=a==3?2:1;if(w>rem)continue;val[v]=a;apply(v,a);dfs(cost+w);apply(v,a);val[v]=0;if(found||timeoutflag)break;}
  ban[v]=1;local.push_back(v);if(found||timeoutflag)break;
 }
 for(int v:local)ban[v]=0;
}
int main(int argc,char**argv){if(argc!=6)return 2;ifstream in(argv[1]);L=stoi(argv[2]);int block=stoi(argv[3]),a=stoi(argv[4]);seconds=stod(argv[5]);in>>n>>m>>K>>N;E.resize(n);adjc.resize(m);logical_labels.resize(n);
 for(int v=0;v<n;v++){for(auto&e:E[v]){in>>e.c>>e.a;adjc[e.c].push_back(v);}for(int a=1;a<4;a++){logical_labels[v][a].resize(K);for(auto&x:logical_labels[v][a])in>>x;}}
 root=block*N;val.assign(n,0);s.assign(m,0);ban.assign(n,0);label.assign(K,0);for(int v=0;v<root;v++)ban[v]=1;
 starttime=chrono::steady_clock::now();val[root]=a;apply(root,a);dfs(a==3?2:1);
 cout<<"{\"block\":"<<block<<",\"a\":"<<a<<",\"limit\":"<<L<<",\"nodes\":"<<nodes<<",\"complete\":"<<(!timeoutflag&&!found?"true":"false")<<",\"found\":"<<(found?"true":"false")<<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-starttime).count()<<",\"witness\":[";bool first=true;if(found)for(int v=0;v<n;v++)if(witness[v]){if(!first)cout<<",";first=false;cout<<"["<<v<<","<<witness[v]<<"]";}cout<<"]}\n";
}
