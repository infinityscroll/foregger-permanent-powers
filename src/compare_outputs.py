#!/usr/bin/env python3
"""Compare independently generated exact outputs after rational normalization."""
import argparse, hashlib, json, sys
from fractions import Fraction
from itertools import zip_longest
from pathlib import Path
if hasattr(sys, 'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
def compare(a:Path,b:Path):
    counts={'lines':0,'rational_fields':0};ha=hashlib.sha256();hb=hashlib.sha256()
    with a.open() as fa,b.open() as fb:
        for i,(sa,sb) in enumerate(zip_longest(fa,fb),1):
            if sa is None or sb is None:raise AssertionError(f'unequal line counts at line {i}')
            aa,bb=sa.strip().split('\t'),sb.strip().split('\t')
            if len(aa)!=len(bb):raise AssertionError(f'field count line {i}')
            ca=[];cb=[]
            for j,(x,y) in enumerate(zip(aa,bb)):
                if j==1:
                    if x!=y:raise AssertionError(f'operation label line {i}')
                    ca.append(x);cb.append(y)
                else:
                    q,r=Fraction(x),Fraction(y)
                    if q!=r:raise AssertionError(f'rational mismatch line {i}, field {j}')
                    counts['rational_fields']+=1;ca.append(str(q));cb.append(str(r))
            ha.update(('\t'.join(ca)+'\n').encode());hb.update(('\t'.join(cb)+'\n').encode());counts['lines']+=1
    counts['canonical_sha256']=ha.hexdigest()
    if ha.digest()!=hb.digest():raise AssertionError('canonical digest')
    return counts
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('a',type=Path);p.add_argument('b',type=Path);p.add_argument('--output',type=Path)
    q=p.parse_args();ans=compare(q.a,q.b);text=json.dumps(ans,indent=2)+'\n'
    if q.output:q.output.write_text(text)
    print(text,end='')
