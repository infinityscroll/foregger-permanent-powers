// Independent exact diagnostics for the proposed Foregger proof.
// Permanent: Ryser inclusion-exclusion. Power differential: linear recurrence.
// Hessian: direct cofactor sums. Projection: blockwise P X P.
// These are finite checks, not a formal proof of the universal theorem.
#include <boost/multiprecision/cpp_int.hpp>
#include <boost/rational.hpp>
#include <algorithm>
#include <fstream>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <type_traits>
#include <vector>
using Z=boost::multiprecision::cpp_int;
using R=boost::rational<Z>;
template<class T> using Mat=std::vector<std::vector<T>>;
struct Raw {Z n,d;};
void must(bool b,const char* msg){if(!b)throw std::runtime_error(msg);}
Z zgcd(Z a,Z b){if(a<0)a=-a;if(b<0)b=-b;while(b!=0){Z t=a%b;a=b;b=t;}return a;}
Z zpow(Z a,int k){Z x=1;while(k){if(k&1)x*=a;a*=a;k>>=1;}return x;}
template<class T> Mat<T> nul(int n){return Mat<T>(n,std::vector<T>(n,T(0)));}
template<class T> Mat<T> ident(int n){auto a=nul<T>(n);for(int i=0;i<n;++i)a[i][i]=T(1);return a;}
template<class T> Mat<T> mul(const Mat<T>&a,const Mat<T>&b){
 int n=a.size();auto c=nul<T>(n);for(int i=0;i<n;++i)for(int k=0;k<n;++k)if(a[i][k]!=T(0))
 for(int j=0;j<n;++j){c[i][j]+=a[i][k]*b[k][j];}
 return c;
}
template<class T> Mat<T> plusm(const Mat<T>&a,const Mat<T>&b){auto c=a;for(size_t i=0;i<a.size();++i)for(size_t j=0;j<a.size();++j)c[i][j]+=b[i][j];return c;}
template<class T> Mat<T> minusm(const Mat<T>&a,const Mat<T>&b){auto c=a;for(size_t i=0;i<a.size();++i)for(size_t j=0;j<a.size();++j)c[i][j]-=b[i][j];return c;}
template<class T> T per(const Mat<T>&a){
 int n=a.size();T ans(0);for(unsigned s=0;s<(1u<<n);++s){T pr(1);for(int i=0;i<n;++i){T row(0);for(int j=0;j<n;++j)if((s>>j)&1)row+=a[i][j];pr*=row;}
 if((n-__builtin_popcount(s))&1)ans-=pr;else ans+=pr;}return ans;
}
Mat<R> minor(const Mat<R>&a,const std::vector<int>&rr,const std::vector<int>&cc){
 Mat<R>b;for(int i=0;i<(int)a.size();++i){if(std::find(rr.begin(),rr.end(),i)!=rr.end())continue;
 std::vector<R> row;for(int j=0;j<(int)a.size();++j)if(std::find(cc.begin(),cc.end(),j)==cc.end())row.push_back(a[i][j]);b.push_back(row);}return b;
}
R squared(const Mat<R>&a){R s(0);for(auto&r:a)for(auto&x:r)s+=x*x;return s;}
bool zeros(const Mat<R>&a){for(auto&r:a)for(auto&x:r)if(x!=R(0))return false;return true;}
bool ds(const Mat<R>&a){int n=a.size();for(int i=0;i<n;++i){R r(0),c(0);for(int j=0;j<n;++j){if(a[i][j]<R(0))return false;r+=a[i][j];c+=a[j][i];}if(r!=R(1)||c!=R(1))return false;}return true;}
void put(std::ostream&o,const R&x){o<<x.numerator();if(x.denominator()!=1)o<<'/'<<x.denominator();}
void put(std::ostream&o,const Raw&x){o<<x.n;if(x.d!=1)o<<'/'<<x.d;}
template<class T>void put(std::ostream&o,const T&x){o<<x;}
template<class...T>void line(std::ostream&o,const T&...x){bool first=true;auto f=[&](const auto&v){if(!first)o<<'\t';first=false;put(o,v);};(f(x),...);o<<'\n';}
R variance(const Mat<R>&a,const std::vector<std::vector<int>>&groups){R v(a.size());for(auto&rs:groups)for(int j=0;j<(int)a.size();++j){R s(0);for(int i:rs)s+=a[i][j];v-=s*s;}return v;}
Mat<Z> powerm(Mat<Z>a,int k){auto p=ident<Z>(a.size());while(k){if(k&1)p=mul(p,a);a=mul(a,a);k>>=1;}return p;}
Z fact(int n){Z a=1;for(int i=2;i<=n;++i)a*=i;return a;}
R occupancy_rec(const Mat<R>&a,const std::vector<std::vector<int>>&groups,std::vector<int>&used,int col){
 if(col==(int)a.size()){return R(1);}
 R s(0);
 for(int h=0;h<(int)groups.size();++h)if(used[h]<(int)groups[h].size()){
 R prob(0);for(int i:groups[h])prob+=a[i][col];if(prob!=R(0)){++used[h];s+=prob*occupancy_rec(a,groups,used,col+1);--used[h];}}
 return s;
}
int main(int argc,char**argv){try{
 if(argc!=3)throw std::runtime_error("usage: audit_cpp fixtures.txt output.tsv");
 std::ifstream in(argv[1]);std::ofstream out(argv[2]);must(bool(in)&&bool(out),"open input/output");
 int total=0;must(bool(in>>total),"truncated case-count header");must(total>0&&total<10000,"case count");long derivs=0,powers=0;
 for(int t=0;t<total;++t){
 int id=0,n=0,s=0;must(bool(in>>id>>n>>s),"truncated fixture header");must(n>=2&&n<=10&&s>=1&&s<=n,"dimensions");
 std::vector<int>sz(s),pi(s);for(int&v:sz)must(bool(in>>v),"truncated partition");for(int&v:pi)must(bool(in>>v),"truncated class permutation");
 // Validate every index before any indexed class-size access. Bounded positive
 // sizes also make the following integer accumulation safe for malformed input.
 for(int h=0;h<s;++h){must(sz[h]>0&&sz[h]<=n,"partition size");must(pi[h]>=0&&pi[h]<s,"class image out of range");}
 must(std::accumulate(sz.begin(),sz.end(),0)==n,"partition sum");auto sortpi=pi;std::sort(sortpi.begin(),sortpi.end());
 for(int h=0;h<s;++h)must(sortpi[h]==h,"class permutation");
 for(int h=0;h<s;++h)must(sz[h]==sz[pi[h]],"block size preservation");
 Z en,ed,tn,td;must(bool(in>>en>>ed>>tn>>td),"truncated parameters");must(ed>0&&td>0&&en>=0&&en<=ed&&tn>=0&&tn<=td,"parameters");R eta(en,ed),theta(tn,td);
 int l=0;must(bool(in>>l),"truncated mixture length");must(l>0&&l<=1000,"mixture length");std::vector<int>w(l);std::vector<std::vector<int>>pps(l,std::vector<int>(n));int sumw=0;
 for(int h=0;h<l;++h){must(bool(in>>w[h]),"truncated mixture weight");must(w[h]>0&&w[h]<=1000000,"weight");sumw+=w[h];for(int&v:pps[h])must(bool(in>>v),"truncated point permutation");auto q=pps[h];std::sort(q.begin(),q.end());for(int i=0;i<n;++i)must(q[i]==i,"input permutation");}
 must(bool(in),"truncated input");
 std::vector<std::vector<int>>groups(s);int off=0;for(int h=0;h<s;++h)for(int j=0;j<sz[h];++j)groups[h].push_back(off++);
 auto F=nul<R>(n),E=nul<R>(n),G=nul<R>(n),B=nul<R>(n),A=nul<R>(n);
 for(int h=0;h<s;++h){for(int i:groups[h]){for(int j:groups[h])E[i][j]=R(1,sz[h]);for(int j:groups[pi[h]])F[i][j]=R(1,sz[h]);}
 for(int j=0;j<sz[h];++j)G[groups[h][j]][groups[pi[h]][(j+1)%sz[h]]]=R(1);}
 for(int h=0;h<l;++h)for(int i=0;i<n;++i)B[i][pps[h][i]]+=R(w[h],sumw);
 for(int i=0;i<n;++i)for(int j=0;j<n;++j)A[i][j]=(R(1)-eta)*((R(1)-theta)*F[i][j]+theta*G[i][j])+eta*B[i][j];
 must(ds(F)&&ds(E)&&ds(G)&&ds(B)&&ds(A),"not DS");must(mul(E,E)==E&&mul(E,F)==F&&mul(F,E)==F,"projection");
 R p(1);for(int m:sz)p*=R(fact(m),zpow(Z(m),m));must(per(F)==p&&per(E)==p,"base permanent");
 auto X=minusm(B,F),Y=nul<R>(n);R delta(0);
 for(int i=0;i<n;++i)for(int j=0;j<n;++j)if(F[i][j]==R(0))delta+=B[i][j];
 // Project each allowed block by (I-J) X (I-J), independently of Python's means formula.
 for(int h=0;h<s;++h){int m=sz[h];auto P=ident<R>(m),XB=nul<R>(m);for(int i=0;i<m;++i)for(int j=0;j<m;++j){P[i][j]-=R(1,m);XB[i][j]=X[groups[h][i]][groups[pi[h]][j]];}
 auto YY=mul(mul(P,XB),P);for(int i=0;i<m;++i)for(int j=0;j<m;++j)Y[groups[h][i]][groups[pi[h]][j]]=YY[i][j];}
 auto Zm=minusm(X,Y);must(zeros(mul(E,Y))&&zeros(mul(Y,E)),"annihilation");must(squared(X)==squared(Y)+squared(Zm),"orthogonality");R zz(0);for(auto&r:Zm)for(auto&v:r)zz+=(v<R(0)?-v:v);must(zz<=R(4)*delta,"leakage norm");
 R linear(0),quad(0),expected(0);
 for(int i=0;i<n;++i)for(int j=0;j<n;++j)linear+=X[i][j]*per(minor(F,{i},{j}));
 for(int i=0;i<n;++i)for(int k=i+1;k<n;++k)for(int j=0;j<n;++j)for(int h=0;h<n;++h)if(h!=j)quad+=Y[i][j]*Y[k][h]*per(minor(F,{i,k},{j,h}));
 for(int h=0;h<s;++h)if(sz[h]>1){R ss(0);for(int i:groups[h])for(int j:groups[pi[h]])ss+=Y[i][j]*Y[i][j];expected+=p*R(sz[h],2*(sz[h]-1))*ss;}
 must(linear==-p*delta&&quad==expected,"derivative/Hessian");line(out,id,"basic",p,delta,linear,quad,squared(Y),squared(Zm));
 auto FP=ident<R>(n),D=nul<R>(n);std::vector<int>rs={1,2,3,5,16*n*n};size_t next=0;
 for(int r=1;r<=rs.back();++r){D=plusm(mul(D,F),mul(FP,X));FP=mul(FP,F);
 if(r==rs[next]){R dv(0);for(auto&group:groups)for(int j=0;j<n;++j){R x(0),y(0);for(int i:group){x+=FP[i][j];y+=D[i][j];}dv-=R(2)*x*y;}
 must(variance(FP,groups)==R(0)&&dv==R(2*r)*delta,"mixing derivative");line(out,id,"derivative",r,dv);++next;++derivs;}}
 auto M=mul(E,B);R v=variance(M,groups);std::vector<int>used(s,0);must(per(M)/p==occupancy_rec(M,groups,used,0),"categorical identity");must(per(M)<=p*(R(1)-v/R(2*n*n)),"variance bound");line(out,id,"occupancy",per(M),v);
 Z den=1;for(auto&row:A)for(auto&a:row){Z d=a.denominator();den=(den/zgcd(den,d))*d;}auto IA=nul<Z>(n);for(int i=0;i<n;++i)for(int j=0;j<n;++j)IA[i][j]=A[i][j].numerator()*(den/A[i][j].denominator());
 R pa(per(IA),zpow(den,n));Raw lastv{0,1};
 for(int k:std::vector<int>{2,3,8,16*n*n,16*n*n+1}){auto AK=powerm(IA,k);Z dk=zpow(den,k);Raw pk{per(AK),zpow(dk,n)};Z vn=Z(n)*dk*dk;
 for(auto&group:groups)for(int j=0;j<n;++j){Z x=0;for(int i:group)x+=AK[i][j];vn-=x*x;}
 Raw vk{vn,dk*dk};
 must(vk.n*lastv.d>=lastv.n*vk.d,"variance monotone");lastv=vk;
 if(k>=16*n*n){must(pk.n*pa.denominator()<=pa.numerator()*pk.d,"specified power inequality");}
 line(out,id,"power",k,pa,pk,vk);++powers;}
 std::cerr<<"C++ case "<<id<<": n="<<n<<" passed\n";
 }
 std::cerr<<"cases="<<total<<" derivatives="<<derivs<<" powers="<<powers<<"\n";
 return 0;
 }catch(const std::exception&e){std::cerr<<"AUDIT FAILED: "<<e.what()<<'\n';return 1;}}
