#!/usr/bin/env python3
"""Deliberately malformed fixtures and output mutations must be rejected.
No claim is made that these tests establish absence of all bugs.
"""
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import argparse,json,subprocess
from audit_python import build,validate_case,ds,permanent,mm,Q,require
from compare_outputs import compare

def fixture_text(c):
    lines=['1',f"{c['id']} {c['n']} {len(c['sizes'])}",
           ' '.join(map(str,c['sizes'])),' '.join(map(str,c['pi'])),
           ' '.join(map(str,c['eta']+c['theta'])),str(len(c['perms']))]
    lines += [' '.join(map(str,[w]+p)) for w,p in zip(c['weights'],c['perms'])]
    return '\n'.join(lines)+'\n'

def tests(fixtures,cpp):
    cases=json.loads(fixtures.read_text());base=deepcopy(next(c for c in cases if c['sizes']==[1,2]))
    mutations=[]
    def add(name,change):
        c=deepcopy(base);change(c);mutations.append((name,c))
    add('bad total dimension',lambda c:c.update(n=4))
    add('nonpositive block size',lambda c:c.update(sizes=[0,3]))
    add('duplicate class image',lambda c:c.update(pi=[0,0]))
    add('unequal block-size interchange',lambda c:c.update(pi=[1,0]))
    add('zero parameter denominator',lambda c:c.update(eta=[1,0]))
    add('negative parameter',lambda c:c.update(theta=[-1,8]))
    add('parameter exceeds one',lambda c:c.update(eta=[9,8]))
    add('negative mixture weight',lambda c:c['weights'].__setitem__(0,-1))
    add('non-bijective point mapping',lambda c:c['perms'][0].__setitem__(0,c['perms'][0][1]))
    outcomes=[]
    with TemporaryDirectory() as td:
        d=Path(td)
        for name,c in mutations:
            py_reject=False
            try:validate_case(c)
            except (AssertionError,ValueError,IndexError,TypeError):py_reject=True
            require(py_reject,'Python accepted '+name)
            (d/'input.txt').write_text(fixture_text(c))
            cp=subprocess.run([str(cpp),str(d/'input.txt'),str(d/'out.tsv')],capture_output=True,text=True,timeout=10)
            require(cp.returncode!=0,'C++ accepted '+name)
            outcomes.append({'test':name,'python':'rejected','cpp':'rejected'})
        (d/'input.txt').write_text('1\n3 4')
        cp=subprocess.run([str(cpp),str(d/'input.txt'),str(d/'out.tsv')],capture_output=True,text=True,timeout=10)
        require(cp.returncode!=0,'C++ accepted truncated fixture')
        outcomes.append({'test':'truncated fixture','cpp':'rejected'})
        good='0\tbasic\t1/2\t0\n1\tpower\t64\t3/4\t2/3\t1\n'
        (d/'good.tsv').write_text(good)
        changed=[('coefficient changed',good.replace('1/2','2/3')),
                 ('label changed',good.replace('basic','power')),
                 ('single extra line',good+'2\tpower\t64\t1\t1\t0\n'),
                 ('single missing line',good.splitlines()[0]+'\n'),
                 ('missing field',good.replace('\t3/4','')),
                 ('zero denominator',good.replace('1/2','1/0'))]
        for name,txt in changed:
            (d/'bad.tsv').write_text(txt)
            for order in [(d/'good.tsv',d/'bad.tsv'),(d/'bad.tsv',d/'good.tsv')]:
                rejected=False
                try:compare(*order)
                except (AssertionError,ValueError,ZeroDivisionError):rejected=True
                require(rejected,'comparator accepted '+name)
            outcomes.append({'test':name,'comparator_both_orders':'rejected'})
        # Control: equivalent unreduced rational encodings must be accepted.
        (d/'equiv.tsv').write_text(good.replace('1/2','2/4').replace('2/3','4/6'))
        compare(d/'good.tsv',d/'equiv.tsv')
    # A row-stochastic-only input is not in the domain; test the domain guard.
    bad=[[Q(1),Q(0)],[Q(1),Q(0)]]
    require(not ds(bad),'row-stochastic-only matrix passed DS guard')
    outcomes.append({'test':'column sums not one','domain_guard':'rejected'})
    return {'mutations_rejected':len(outcomes),'rational_equivalence_control':'accepted',
            'tests':outcomes,
            'audit_correction':'Comparator changed from zip to zip_longest to detect a single extra trailing line.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--fixtures',type=Path,required=True)
    p.add_argument('--cpp',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();r=tests(a.fixtures,a.cpp.resolve());a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'mutations_rejected':r['mutations_rejected']},sort_keys=True))
