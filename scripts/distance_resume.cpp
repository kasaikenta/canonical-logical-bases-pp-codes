// Independent exhaustive GF(4) irreducible-cluster search, binary-weight metric.
#include <algorithm>
#include <array>
#include <chrono>
#include <fstream>
#include <iostream>
#include <vector>
#include <cstdint>
#include <csignal>
#include <cstdio>
#include <sstream>
using namespace std;
int mul4[4][4]={{0,0,0,0},{0,1,2,3},{0,2,3,1},{0,3,1,2}};
struct Edge {int c,a;};
int n,m,K,L,root,N; double seconds; vector<array<Edge,3>> E;vector<vector<int>> adjc;
vector<array<vector<uint64_t>,4>> logical_labels;vector<int>s,val;vector<char>ban;vector<uint64_t>label;
struct State{int cost;vector<int> vals;vector<char> bans;};
vector<State> frontier;int split_depth=0;volatile sig_atomic_t stopped=0;
void on_signal(int){stopped=1;}
void save_state(int cost){frontier.push_back({cost,val,ban});}
uint64_t nodes=0;bool timeoutflag=false,found=false;vector<int>witness;
auto starttime=chrono::steady_clock::now();
void apply(int v,int a){for(auto e:E[v])s[e.c]^=mul4[e.a][a];for(int t=0;t<K;t++)label[t]^=logical_labels[v][a][t];}
void dfs(int cost){
 if(found)return;
 if(timeoutflag||stopped){timeoutflag=true;save_state(cost);return;}
 if(split_depth){int selected=0;for(int a:val)selected+=a!=0;if(selected>=split_depth){save_state(cost);return;}}
 if((++nodes&16383)==0 && chrono::duration<double>(chrono::steady_clock::now()-starttime).count()>seconds){timeoutflag=true;save_state(cost);return;}
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
  for(int a=1;a<=3;a++){int w=a==3?2:1;if(w>rem)continue;val[v]=a;apply(v,a);dfs(cost+w);apply(v,a);val[v]=0;if(found)break;}
  ban[v]=1;local.push_back(v);if(found)break;
 }
 for(int v:local)ban[v]=0;
}

void write_states(string filename,vector<State> const&states){
 string tmp=filename+".tmp";ofstream out(tmp);out<<n<<" "<<states.size()<<"\n";
 for(auto const&st:states){out<<st.cost<<" ";int c=0;for(int a:st.vals)c+=a!=0;out<<c;for(int v=0;v<n;v++)if(st.vals[v])out<<" "<<v<<" "<<st.vals[v];c=0;for(char b:st.bans)c+=b!=0;out<<" "<<c;for(int v=0;v<n;v++)if(st.bans[v])out<<" "<<v;out<<"\n";}
 out.flush();if(!out)throw runtime_error("checkpoint write failed");out.close();if(rename(tmp.c_str(),filename.c_str()))throw runtime_error("rename checkpoint");
}
vector<State> read_states(string filename){
 ifstream in(filename);int nn,count;in>>nn>>count;if(!in||nn!=n)throw runtime_error("invalid checkpoint header");vector<State> rs;
 for(int k=0;k<count;k++){State st;st.vals.assign(n,0);st.bans.assign(n,0);int countv;in>>st.cost>>countv;for(int j=0;j<countv;j++){int v,a;in>>v>>a;st.vals[v]=a;}in>>countv;for(int j=0;j<countv;j++){int v;in>>v;st.bans[v]=1;}if(!in)throw runtime_error("invalid checkpoint state");rs.push_back(st);}return rs;
}
int main(int argc,char**argv){
 // split INPUT LIMIT ROOT VALUE DEPTH OUT; run INPUT LIMIT FRONTIER SECONDS OUT
 if(argc!=8&&argc!=7)return 2;string mode=argv[1];ifstream in(argv[2]);L=stoi(argv[3]);
 in>>n>>m>>K>>N;if(!in)return 3;E.resize(n);adjc.resize(m);logical_labels.resize(n);
 for(int v=0;v<n;v++){for(auto&e:E[v]){in>>e.c>>e.a;adjc[e.c].push_back(v);}for(int a=1;a<4;a++){logical_labels[v][a].resize(K);for(auto&x:logical_labels[v][a])in>>x;}}
 vector<State> work;string output;
 if(mode=="split"){
  int block=stoi(argv[4]),a=stoi(argv[5]);split_depth=stoi(argv[6]);output=argv[7];seconds=3600;
  State st;st.cost=a==3?2:1;st.vals.assign(n,0);st.bans.assign(n,0);root=block*N;st.vals[root]=a;for(int v=0;v<root;v++)st.bans[v]=1;work.push_back(st);
 }else if(mode=="expand"){work=read_states(argv[4]);split_depth=stoi(argv[5]);seconds=3600;output=argv[6];}else{work=read_states(argv[4]);seconds=stod(argv[5]);output=argv[6];}
 signal(SIGTERM,on_signal);signal(SIGUSR1,on_signal);starttime=chrono::steady_clock::now();
 for(size_t j=0;j<work.size();j++){
  if(found)break;
  if(timeoutflag||stopped){frontier.insert(frontier.end(),work.begin()+j,work.end());timeoutflag=true;break;}
  val=work[j].vals;ban=work[j].bans;s.assign(m,0);label.assign(K,0);for(int v=0;v<n;v++)if(val[v])apply(v,val[v]);dfs(work[j].cost);
 }
 if(found)frontier.clear();write_states(output,frontier);
 cout<<"{\"limit\":"<<L<<",\"nodes\":"<<nodes<<",\"complete\":"<<(mode=="run"&&!timeoutflag&&!found?"true":"false")<<",\"found\":"<<(found?"true":"false")<<",\"frontier_size\":"<<frontier.size()<<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-starttime).count()<<",\"witness\":[";bool first=true;if(found)for(int v=0;v<n;v++)if(witness[v]){if(!first)cout<<",";first=false;cout<<"["<<v<<","<<witness[v]<<"]";}cout<<"]}\n";
}
