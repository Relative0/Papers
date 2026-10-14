#include <bits/stdc++.h>
using namespace std;

struct Poset { vector<pair<int,int>> edges; vector<array<int,3>> tris; };

static bool transitive(int n, uint32_t mask, const vector<pair<int,int>>& pairs){
    bool r[8][8]{};
    for(int i=0;i<(int)pairs.size();++i) if(mask>>i&1u) r[pairs[i].first][pairs[i].second]=1;
    for(int a=0;a<n;a++)for(int b=a+1;b<n;b++) if(r[a][b])
      for(int c=b+1;c<n;c++) if(r[b][c] && !r[a][c]) return false;
    return true;
}
static int height(int n, uint32_t mask, const vector<pair<int,int>>& pairs){
    bool r[8][8]{}; for(int i=0;i<(int)pairs.size();++i) if(mask>>i&1u) r[pairs[i].first][pairs[i].second]=1;
    int h[8]{}; int mx=0;
    for(int v=0;v<n;v++){ for(int u=0;u<v;u++) if(r[u][v]) h[v]=max(h[v],h[u]+1); mx=max(mx,h[v]); }
    return mx;
}
static int rank_f2(vector<uint32_t> rows, int m){
    int row=0; for(int col=0;col<m && row<(int)rows.size();col++){
        int p=-1; for(int r=row;r<(int)rows.size();r++) if((rows[r]>>col)&1u){p=r;break;}
        if(p<0) continue; swap(rows[row],rows[p]);
        for(int r=row+1;r<(int)rows.size();r++) if((rows[r]>>col)&1u) rows[r]^=rows[row];
        row++;
    } return row;
}
static bool augment(int u, const vector<uint32_t>& adj, vector<int>& mt, vector<int>& seen){
    uint32_t bits=adj[u];
    while(bits){ int v=__builtin_ctz(bits); bits&=bits-1; if(seen[v]) continue; seen[v]=1; if(mt[v]<0 || augment(mt[v],adj,mt,seen)){mt[v]=u;return true;} }
    return false;
}
static bool unique_perfect(const vector<uint32_t>& adj, int m){
    vector<int> mt(m,-1); // triangle/right -> edge/left
    for(int u=0;u<m;u++){ vector<int> seen(m); if(!augment(u,adj,mt,seen)) return false; }
    vector<int> matchL(m,-1); for(int v=0;v<m;v++) matchL[mt[v]]=v;
    // orient contracted graph: for each unmatched edge u-v, arc matched-pair(u) -> matched-pair(mt[v])? Any directed cycle iff alternating cycle.
    vector<vector<int>> dg(m);
    for(int u=0;u<m;u++){
      uint32_t bits=adj[u];
      while(bits){int v=__builtin_ctz(bits);bits&=bits-1; if(v==matchL[u]) continue; int u2=mt[v]; dg[u].push_back(u2);}
    }
    vector<int> col(m,0);
    function<bool(int)> dfs=[&](int u){col[u]=1; for(int v:dg[u]){if(col[v]==1)return true;if(col[v]==0&&dfs(v))return true;} col[u]=2;return false;};
    for(int u=0;u<m;u++)if(col[u]==0&&dfs(u))return false;
    return true;
}

int main(int argc,char**argv){
    int n=6; if(argc>1)n=atoi(argv[1]);
    vector<pair<int,int>> pairs; for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)pairs.push_back({i,j});
    vector<Poset> ps;
    uint32_t total=1u<<pairs.size();
    for(uint32_t mask=0;mask<total;mask++){
      if(!transitive(n,mask,pairs) || height(n,mask,pairs)>2) continue;
      bool r[8][8]{}; Poset p;
      for(int i=0;i<(int)pairs.size();i++)if(mask>>i&1u){auto e=pairs[i];r[e.first][e.second]=1;p.edges.push_back(e);}
      for(int a=0;a<n;a++)for(int b=a+1;b<n;b++)for(int c=b+1;c<n;c++) if(r[a][b]&&r[b][c])p.tris.push_back({a,b,c});
      ps.push_back(move(p));
    }
    cerr<<"posets "<<ps.size()<<"\n";
    long long profiles=0, square=0, neutral=0, nonunique=0; int maxm=0;
    vector<int> lab(n);
    for(size_t pi=0;pi<ps.size();pi++){
      auto &p=ps[pi]; int Ltot=1<<(2*n); // base4 labels encoded 2 bits each
      for(int code=0;code<Ltot;code++){
        int t=code; for(int i=0;i<n;i++){lab[i]=t&3;t>>=2;} profiles++;
        vector<pair<int,int>> de; de.reserve(p.edges.size());
        int eidx[8][8]; memset(eidx,-1,sizeof(eidx));
        for(auto [a,b]:p.edges) if(lab[a]&~lab[b]){eidx[a][b]=de.size();de.push_back({a,b});}
        vector<array<int,3>> dt; dt.reserve(p.tris.size());
        for(auto tr:p.tris){int a=tr[0],b=tr[1],c=tr[2]; if((lab[a]&~lab[b])||(lab[a]&~lab[c])||(lab[b]&~lab[c])) dt.push_back(tr);}
        int m=de.size(); if(m!=(int)dt.size())continue; square++; maxm=max(maxm,m);
        if(m==0){neutral++;continue;}
        vector<uint32_t> rows(m,0), adj(m,0); // rows edges x cols tris; adj left=edge -> tris
        for(int j=0;j<m;j++){
          int a=dt[j][0],b=dt[j][1],c=dt[j][2];
          int ee[3]={eidx[b][c],eidx[a][c],eidx[a][b]};
          for(int z=0;z<3;z++) if(ee[z]>=0){rows[ee[z]] |= (1u<<j); adj[ee[z]]|=(1u<<j);} 
        }
        if(rank_f2(rows,m)!=m)continue;
        neutral++;
        if(!unique_perfect(adj,m)){
          nonunique++;
          cout<<"COUNTEREXAMPLE n="<<n<<" poset_index="<<pi<<" code="<<code<<" m="<<m<<"\nP edges:";
          for(auto e:p.edges)cout<<" ("<<e.first<<","<<e.second<<")";
          cout<<"\nlabels:";for(int x:lab)cout<<" "<<x;cout<<"\ndeleted edges:";for(auto e:de)cout<<" ("<<e.first<<","<<e.second<<")";
          cout<<"\ndeleted triangles:";for(auto x:dt)cout<<" ("<<x[0]<<","<<x[1]<<","<<x[2]<<")";cout<<"\n";
          return 2;
        }
      }
      if((pi+1)%500==0) cerr<<"done "<<(pi+1)<<" neutral "<<neutral<<"\n";
    }
    cout<<"NO_COUNTEREXAMPLE n="<<n<<" posets="<<ps.size()<<" profiles="<<profiles<<" square="<<square<<" F2_neutral="<<neutral<<" maxm="<<maxm<<"\n";
    return 0;
}
