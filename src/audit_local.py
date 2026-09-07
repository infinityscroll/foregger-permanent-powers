#!/usr/bin/env python3
"""Check the explicit local-gap bound using independently matched exact outputs.
This is finite diagnostic coverage, not a proof of the universal theorem.
"""
from fractions import Fraction as Q
from pathlib import Path
from math import factorial
import argparse, hashlib, json, sys
from audit_python import build, norm2, sub, require, partitions
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)

def constants(n,p):
    C=Q(n*n*factorial(n-2),2);r=16*n*n
    rho=min(Q(1,16*n*r),p/(128*C*n))
    require(0<rho<=Q(1,n) and rho<=Q(1,2),'radius domain')
    require(C*rho<=p/4 and 8*C*rho<=p,'Taylor constraints')
    require(n*rho<=Q(1,4) and n*rho<=p/(128*C),'leakage constraints')
    require(16*n*r*r*rho<=r,'mixing remainder constraint')
    require(rho<=1 and rho<=p/(16*C),'late-power error constraint')
    if n>=3:require(Q(n**3*factorial(n-3),6)<=C,'third derivative constant')
    return C,r,rho

def run(fixtures,values):
    cases=json.loads(fixtures.read_text())
    ids=[c['id'] for c in cases]
    require(all(type(id) is int for id in ids) and len(ids)==len(set(ids)),'duplicate or invalid fixture ID')
    selected={c['id']:c for c in cases if c.get('local_radius_case')}
    metadata={};rows=[]
    for id,c in selected.items():
        groups,f,e,g,b,a=build(c);n=c['n'];p=Q(1)
        for m in c['sizes']:p*=Q(factorial(m),m**m)
        C,r,rho=constants(n,p);eps2=norm2(sub(a,f))
        delta=sum(a[i][j] for i in range(n) for j in range(n) if f[i][j]==0)
        require(eps2<=rho*rho,'fixture outside certified local radius')
        bound=4*p*delta+p*eps2/8
        metadata[id]=(c,n,p,r,rho,eps2,delta,bound)
    expected={(id,k) for id,(_,_,_,r,_,_,_,_) in metadata.items() for k in (r,r+1)}
    seen=set()
    with values.open() as inp:
        for line_no,line in enumerate(inp,1):
            fields=line.rstrip('\n').split('\t');id=int(fields[0])
            if id not in metadata or fields[1]!='power':continue
            c,n,p,r,rho,eps2,delta,bound=metadata[id];k=int(fields[2])
            if k<r:continue
            key=(id,k)
            require(key in expected,'unexpected radius-controlled power')
            require(key not in seen,'duplicate radius-controlled power')
            seen.add(key)
            pa,pk,vk=map(Q,fields[3:]);margin=pa-pk-bound
            require(margin>=0,'explicit local permanent gap failed')
            require(vk>=r*delta,'mixing defect lower bound failed')
            require((pa>pk) if eps2>0 else (pa==pk),'local strictness failed')
            digest=hashlib.sha256(str(margin).encode()).hexdigest()
            rows.append({'case':id,'n':n,'mode':c['mode'],'k':k,
                         'source_line':line_no,'p':str(p),'rho':str(rho),
                         'epsilon_squared':str(eps2),'delta':str(delta),
                         'local_lower_bound':str(bound),
                         'nonnegative_margin_sha256':digest,
                         'margin_numerator_bits':margin.numerator.bit_length(),
                         'margin_denominator_bits':margin.denominator.bit_length()})
    require(seen==expected,'missing radius-controlled powers')
    checks=0
    for n in range(2,13):
        for sizes in partitions(n):
            p=Q(1)
            for m in sizes:p*=Q(factorial(m),m**m)
            constants(n,p);checks+=1
    for n in range(13,101):
        for p in [Q(1),Q(factorial(n),n**n)]:constants(n,p);checks+=1
    return {'radius_controlled_fixtures':len(selected),'local_gap_checks':len(rows),
            'constant_checks':checks,'finite_scope_only':True,'records':rows}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--fixtures',type=Path,required=True)
    ap.add_argument('--values',type=Path,required=True);ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args();result=run(a.fixtures,a.values);a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'},sort_keys=True))
