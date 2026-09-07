#!/usr/bin/env python3
"""Exact diagnostic tests, not a machine proof of the universal theorem.
Python route: fractions, subset-DP permanent, dual-number binary powering.
"""
from fractions import Fraction as Q
from math import factorial, lcm
from pathlib import Path
import argparse, json, random, sys
if hasattr(sys, 'set_int_max_str_digits'): sys.set_int_max_str_digits(0)
def require(v,msg):
    if not v: raise AssertionError(msg)
def zero(n): return [[Q(0) for _ in range(n)] for _ in range(n)]
def eye(n): return [[Q(i==j) for j in range(n)] for i in range(n)]
def add(a,b): return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def sub(a,b): return [[x-y for x,y in zip(r,s)] for r,s in zip(a,b)]
def scale(a,c): return [[c*x for x in r] for r in a]
def mm(a,b):
    n=len(a); c=zero(n)
    for i in range(n):
        for k in range(n):
            if a[i][k]:
                for j in range(n): c[i][j]+=a[i][k]*b[k][j]
    return c
def norm2(a): return sum(x*x for r in a for x in r)
def eq0(a): return all(x==0 for r in a for x in r)
def ds(a):
    n=len(a)
    return (all(x>=0 for r in a for x in r) and all(sum(r)==1 for r in a)
      and all(sum(a[i][j] for i in range(n))==1 for j in range(n)))
def permanent(a):
    n=len(a); d=[0]*(1<<n); d[0]=1
    for mask in range(1<<n):
        i=mask.bit_count()
        if i==n: continue
        for j in range(n):
            if not (mask>>j)&1: d[mask|(1<<j)]+=d[mask]*a[i][j]
    return d[-1]
def permanent_polynomial2(a,y):
    n=len(a); d=[[Q(0)]*3 for _ in range(1<<n)]; d[0][0]=Q(1)
    for mask in range(1<<n):
        i=mask.bit_count()
        if i==n: continue
        for j in range(n):
            if not(mask>>j)&1:
                dst=d[mask|(1<<j)]; src=d[mask]
                for k in range(3):
                    dst[k]+=src[k]*a[i][j]
                    if k: dst[k]+=src[k-1]*y[i][j]
    return d[-1]
def dual_power(f,x,k):
    n=len(f); ap,ad=f,x; rp,rd=eye(n),zero(n)
    while k:
        if k&1: rp,rd=mm(rp,ap),add(mm(rd,ap),mm(rp,ad))
        ap,ad=mm(ap,ap),add(mm(ad,ap),mm(ap,ad)); k//=2
    return rp,rd
def integer_form(a):
    den=lcm(*(x.denominator for r in a for x in r))
    return [[int(x*den) for x in r] for r in a],den
def imul(a,b):
    n=len(a)
    return [[sum(a[i][k]*b[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
def ipower(a,k):
    n=len(a);r=[[int(i==j) for j in range(n)] for i in range(n)]
    while k:
        if k&1:r=imul(r,a)
        a=imul(a,a);k//=2
    return r
def partitions(n,lo=1):
    if n==0: yield []
    for x in range(lo,n+1):
        for rest in partitions(n-x,x):yield [x]+rest

def generate_fixtures(path):
    rng=random.Random(20260907);cases=[]
    for n in range(2,8):
        for sizes in partitions(n):
            ident=list(range(len(sizes)));rot=ident.copy()
            for m in sorted(set(sizes)):
                ids=[i for i,v in enumerate(sizes) if v==m]
                for j,i in enumerate(ids):rot[i]=ids[(j+1)%len(ids)]
            for pi in ([ident] if rot==ident else [ident,rot]):
                pp=[]
                for _ in range(4):
                    p=list(range(n));rng.shuffle(p);pp.append(p)
                c={'id':len(cases),'n':n,'sizes':sizes,'pi':pi,'weights':[1,2,4,8],
                   'perms':pp,'eta':[1,1024],'theta':[1,32]}
                if len(cases)%9==0:c['eta']=[0,1]
                if len(cases)%11==0:c['theta']=[0,1]
                cases.append(c)
    # Radius-controlled fixtures additionally test the explicit local theorem.
    patterns=[([2],[0]),([1,1],[1,0]),([1,2],[0,1]),
              ([2,2],[1,0]),([1,2,2],[0,2,1]),
              ([2,2,2],[1,2,0]),([1,2,2,2],[0,2,3,1])]
    for sizes,pi in patterns:
        n=sum(sizes);p=Q(1)
        for m in sizes:p*=Q(factorial(m),m**m)
        C=Q(n*n*factorial(n-2),2);r=16*n*n
        rho=min(Q(1,16*n*r),p/(128*C*n));small=rho/(16*n)
        pp=[]
        for _ in range(4):
            perm=list(range(n));rng.shuffle(perm);pp.append(perm)
        for mode in ['tangent','leakage','coupled']:
            eta=Q(0) if mode=='tangent' else small
            theta=Q(0) if mode=='leakage' else small
            cases.append({'id':len(cases),'n':n,'sizes':sizes,'pi':pi,
                          'weights':[1,2,4,8],'perms':pp,
                          'eta':[eta.numerator,eta.denominator],
                          'theta':[theta.numerator,theta.denominator],
                          'local_radius_case':True,'mode':mode})
    path.write_text(json.dumps(cases,indent=2)+'\n')
    with path.with_suffix('.txt').open('w') as out:
        out.write(str(len(cases))+'\n')
        for c in cases:
            out.write(f"{c['id']} {c['n']} {len(c['sizes'])}\n")
            out.write(' '.join(map(str,c['sizes']))+'\n')
            out.write(' '.join(map(str,c['pi']))+'\n')
            out.write(' '.join(map(str,c['eta']+c['theta']))+'\n')
            out.write(str(len(c['perms']))+'\n')
            for w,p in zip(c['weights'],c['perms']):out.write(' '.join(map(str,[w]+p))+'\n')
    return cases

def validate_case(c):
    n=c['n'];sizes=c['sizes'];pi=c['pi']
    require(isinstance(n,int) and 2<=n<=10,'invalid dimension')
    require(all(isinstance(m,int) and m>0 for m in sizes) and sum(sizes)==n,'invalid partition')
    require(sorted(pi)==list(range(len(sizes))),'invalid class permutation')
    require(all(sizes[i]==sizes[pi[i]] for i in range(len(sizes))),'class sizes not preserved')
    require(0<len(c['weights'])==len(c['perms'])<=1000,'invalid mixture length')
    require(all(isinstance(w,int) and 0<w<=1000000 for w in c['weights']),'invalid mixture weights')
    require(all(sorted(p)==list(range(n)) for p in c['perms']),'invalid point permutation')
    for name in ['eta','theta']:
        num,den=c[name]
        require(isinstance(num,int) and isinstance(den,int) and den>0 and 0<=num<=den,'invalid parameter')

def build(c):
    validate_case(c)
    n=c['n'];groups=[];t=0
    for m in c['sizes']:groups.append(list(range(t,t+m)));t+=m
    f,e,g,b=zero(n),zero(n),zero(n),zero(n);pi=c['pi']
    for h,rs in enumerate(groups):
        for i in rs:
            for j in rs:e[i][j]=Q(1,len(rs))
            for j in groups[pi[h]]:f[i][j]=Q(1,len(rs))
        for q,i in enumerate(rs):g[i][groups[pi[h]][(q+1)%len(rs)]]=Q(1)
    total=sum(c['weights'])
    for w,p in zip(c['weights'],c['perms']):
        for i,j in enumerate(p):b[i][j]+=Q(w,total)
    eta,theta=Q(*c['eta']),Q(*c['theta'])
    a=add(scale(add(scale(f,1-theta),scale(g,theta)),1-eta),scale(b,eta))
    return groups,f,e,g,b,a

def project(x,groups,pi):
    y=zero(len(x))
    for h,rs in enumerate(groups):
        cs=groups[pi[h]];m=len(rs)
        rr={i:sum(x[i][j] for j in cs)/m for i in rs}
        cc={j:sum(x[i][j] for i in rs)/m for j in cs}
        mu=sum(x[i][j] for i in rs for j in cs)/(m*m)
        for i in rs:
            for j in cs:y[i][j]=x[i][j]-rr[i]-cc[j]+mu
    return y,sub(x,y)
def variance(a,groups):
    return Q(len(a))-sum(sum(a[i][j] for i in rs)**2 for rs in groups for j in range(len(a)))
def occupancy_probability(m,groups):
    caps=tuple(len(g) for g in groups);states={(0,)*len(groups):Q(1)}
    for j in range(len(m)):
        nd={}
        for counts,p in states.items():
            for h,rs in enumerate(groups):
                if counts[h]<caps[h]:
                    new=list(counts);new[h]+=1;new=tuple(new)
                    nd[new]=nd.get(new,Q(0))+p*sum(m[i][j] for i in rs)
        states=nd
    return states.get(caps,Q(0))
def line(out,*v):out.write('\t'.join(map(str,v))+'\n')

def audit(cases,path):
    counts={'cases':0,'derivatives':0,'hessians':0,'power_tests':0,'occupancy_tests':0}
    with path.open('w') as out:
        for c in cases:
            n=c['n'];groups,f,e,g,b,a=build(c);pi=c['pi']
            require(all(ds(h) for h in [f,e,g,b,a]),'not DS')
            require(mm(e,e)==e and mm(e,f)==f and mm(f,e)==f,'projection')
            p=Q(1)
            for rs in groups:p*=Q(factorial(len(rs)),len(rs)**len(rs))
            require(permanent(f)==p and permanent(e)==p,'exceptional permanent')
            x=sub(b,f);y,z=project(x,groups,pi)
            delta=sum(b[i][j] for i in range(n) for j in range(n) if f[i][j]==0)
            require(eq0(mm(e,y)) and eq0(mm(y,e)),'tangent annihilation')
            require(norm2(x)==norm2(y)+norm2(z),'orthogonal split')
            require(sum(abs(t) for row in z for t in row)<=4*delta,'leakage control')
            pp=permanent_polynomial2(f,x)
            require(pp[0]==p and pp[1]==-p*delta,'first derivative')
            py=permanent_polynomial2(f,y);expected=Q(0)
            for h,rs in enumerate(groups):
                m=len(rs)
                if m>1:expected+=p*Q(m,2*(m-1))*sum(y[i][j]**2 for i in rs for j in groups[pi[h]])
            require(py==[p,Q(0),expected],'Hessian coefficient')
            line(out,c['id'],'basic',p,delta,pp[1],py[2],norm2(y),norm2(z));counts['hessians']+=1
            for r in [1,2,3,5,16*n*n]:
                fp,der=dual_power(f,x,r)
                val=-2*sum(sum(fp[i][j] for i in rs)*sum(der[i][j] for i in rs) for rs in groups for j in range(n))
                require(variance(fp,groups)==0,'exceptional variance')
                require(val==2*r*delta,'mixing derivative')
                line(out,c['id'],'derivative',r,val);counts['derivatives']+=1
            mi=mm(e,b);v=variance(mi,groups)
            require(permanent(mi)/p==occupancy_probability(mi,groups),'occupancy identity')
            require(permanent(mi)<=p*(1-v/(2*n*n)),'variance bound')
            line(out,c['id'],'occupancy',permanent(mi),v);counts['occupancy_tests']+=1
            za,den=integer_form(a);pa=Q(permanent(za),den**n);lastv=Q(0)
            for k in [2,3,8,16*n*n,16*n*n+1]:
                ak=ipower(za,k);dk=den**k;pk=Q(permanent(ak),dk**n)
                vk=Q(n*dk*dk-sum(sum(ak[i][j] for i in rs)**2 for rs in groups for j in range(n)),dk*dk)
                require(vk>=lastv,'variance monotonicity');lastv=vk
                if k>=16*n*n:require(pk<=pa,'specified local-power test failed')
                line(out,c['id'],'power',k,pa,pk,vk);counts['power_tests']+=1
            counts['cases']+=1
            print(f"Python case {c['id']}: n={n}, sizes={c['sizes']}, pi={pi}",flush=True)
    return counts

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--fixtures',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True);ap.add_argument('--generate',action='store_true')
    q=ap.parse_args();q.output.parent.mkdir(parents=True,exist_ok=True)
    cases=generate_fixtures(q.fixtures) if q.generate else json.loads(q.fixtures.read_text())
    stats=audit(cases,q.output);q.output.with_suffix('.summary.json').write_text(json.dumps(stats,indent=2)+'\n')
    print(json.dumps(stats,sort_keys=True))
if __name__=='__main__':main()
