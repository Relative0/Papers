// Exact bounded integer residual counting. CUDD performs BDD compilation/sifting;
// this kernel performs all online traversal, memoization, updates and repeated counts.
#include <cstdint>
#include <vector>
#include <cstring>
#include <stdexcept>
#include <algorithm>
using std::vector; using u64=uint64_t; using i64=int64_t;
struct Node {uint32_t level; i64 lo,hi;};
template<class T> T take(const uint8_t*&p,const uint8_t*end){if(size_t(end-p)<sizeof(T))throw std::runtime_error("short");T v;memcpy(&v,p,sizeof(T));p+=sizeof(T);return v;}
template<class T> void put(vector<uint8_t>&b,T v){auto p=(uint8_t*)&v;b.insert(b.end(),p,p+sizeof(T));}
struct Engine {
 int kind;vector<uint32_t> order;vector<int8_t> fixed;vector<Node> nodes;vector<u64> words,memo;vector<uint8_t> valid;vector<unsigned> free_suffix;i64 root=1;bool cached=false;u64 answer=0,visits=0;
 int level(i64 e){return std::abs(e)==1?int(order.size()):nodes.at(std::abs(e)-2).level;}
 u64 edge(i64 e){
  int l=level(e);u64 all=u64(1)<<free_suffix[l];
  if(e==1)return 1;if(e==-1)return 0;
  size_t j=std::abs(e)-2;
  if(!valid[j]){visits++;Node t=nodes[j];int l=t.level;
   auto branch=[&](i64 c){return edge(c)<<(free_suffix[l+1]-free_suffix[level(c)]);};
   memo[j]=fixed[l]<0?branch(t.lo)+branch(t.hi):branch(fixed[l]?t.hi:t.lo);valid[j]=1;
  }
  return e<0?all-memo[j]:memo[j];
 }
 u64 count(){if(cached)return answer;visits=0;
  if(kind==0){answer=0;for(u64 x:words)answer+=__builtin_popcountll(x);}
  else {free_suffix.assign(order.size()+1,0);for(int i=int(order.size())-1;i>=0;--i)free_suffix[i]=free_suffix[i+1]+(fixed[i]<0);valid.assign(nodes.size(),0);memo.resize(nodes.size());answer=edge(root)<<(free_suffix[0]-free_suffix[level(root)]);}
  cached=true;return answer;
 }
 void update(uint32_t z,int b){
  auto it=std::find(order.begin(),order.end(),z);if(it==order.end()||(b!=0&&b!=1))throw std::runtime_error("coordinate");size_t pos=it-order.begin();
  if(kind){if(fixed[pos]>=0)throw std::runtime_error("reassigned");fixed[pos]=b;}
  else {unsigned shift=order.size()-1-pos;u64 size=u64(1)<<(order.size()-1);vector<u64> next((size+63)/64,0);
   for(u64 a=0;a<size;++a){u64 src=((a>>shift)<<(shift+1))|(u64(b)<<shift)|(a&((u64(1)<<shift)-1));if((words[src/64]>>(src%64))&1)next[a/64]|=u64(1)<<(a%64);}
   words.swap(next);order.erase(it);
  }cached=false;
 }
 vector<uint8_t> dump(){vector<uint8_t>b;put<uint32_t>(b,kind?0x31444243:0x3142504e);put<uint32_t>(b,order.size());
  for(auto x:order)put<uint32_t>(b,x);
  if(kind){put<uint32_t>(b,nodes.size());put<i64>(b,root);for(auto x:fixed)put<int8_t>(b,x);for(auto t:nodes){put<uint32_t>(b,t.level);put<i64>(b,t.lo);put<i64>(b,t.hi);}}
  else {size_t bytes=((u64(1)<<order.size())+7)/8;auto p=(uint8_t*)words.data();b.insert(b.end(),p,p+bytes);}return b;
 }
};
extern "C" {
u64 nc_raw(const u64*U,size_t nu,const u64*W,size_t nw){u64 total=0;for(size_t i=0;i<nu;i++)for(size_t j=0;j<nw;j++)total+=__builtin_parityll(U[i]&W[j]);return total;}
void* nc_load(const uint8_t*data,size_t len){Engine*e=nullptr;try{auto p=data,end=data+len;uint32_t magic=take<uint32_t>(p,end);e=new Engine;e->kind=magic==0x31444243?1:0;if(!e->kind&&magic!=0x3142504e)throw std::runtime_error("magic");auto n=take<uint32_t>(p,end);if(n>62)throw std::runtime_error("width");for(unsigned i=0;i<n;i++)e->order.push_back(take<uint32_t>(p,end));
 if(e->kind){auto m=take<uint32_t>(p,end);e->root=take<i64>(p,end);for(unsigned i=0;i<n;i++)e->fixed.push_back(take<int8_t>(p,end));for(unsigned j=0;j<m;j++){Node t{take<uint32_t>(p,end),take<i64>(p,end),take<i64>(p,end)};if(t.level>=n||std::abs(t.lo)>j+1||std::abs(t.hi)>j+1||!t.lo||!t.hi)throw std::runtime_error("dag");e->nodes.push_back(t);}if(std::abs(e->root)>m+1||!e->root)throw std::runtime_error("root");}
 else {if(n>24)throw std::runtime_error("packed width");size_t bits=u64(1)<<n,bytes=(bits+7)/8;if(size_t(end-p)!=bytes)throw std::runtime_error("packed length");e->words.assign((bits+63)/64,0);memcpy(e->words.data(),p,bytes);p+=bytes;}
 if(p!=end)throw std::runtime_error("trailing");return e;
 }catch(...){delete e;return nullptr;}}
void* nc_packed(unsigned p,unsigned q,const uint32_t*names,const u64*U,const u64*W){try{if(p+q>24)return nullptr;auto e=new Engine;e->kind=0;e->order.assign(names,names+p+q);u64 total=u64(1)<<(p+q);e->words.assign((total+63)/64,0);for(u64 x=0;x<(u64(1)<<p);x++)for(u64 y=0;y<(u64(1)<<q);y++){u64 i=(x<<q)|y;if(__builtin_parityll(U[x]&W[y]))e->words[i/64]|=u64(1)<<(i%64);}return e;}catch(...){return nullptr;}}
int nc_update(void*p,unsigned z,int b){try{((Engine*)p)->update(z,b);return 0;}catch(...){return -1;}}
u64 nc_count(void*p){return ((Engine*)p)->count();}
u64 nc_visits(void*p){return ((Engine*)p)->visits;}
size_t nc_dump(void*p,uint8_t*out){auto b=((Engine*)p)->dump();if(out)memcpy(out,b.data(),b.size());return b.size();}
void nc_free(void*p){delete (Engine*)p;}
}
