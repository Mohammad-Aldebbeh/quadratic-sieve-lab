"""Finite exact experiments for an undergraduate sieve and moment study.
Python standard library only. Run: python experiment.py
September 2026 revision.
"""
from fractions import Fraction
from math import gcd, isqrt, prod
from pathlib import Path
import csv
import json


def prime(x):
    return x >= 2 and all(x % d for d in range(2, isqrt(x)+1))


def factors(x):
    out = []
    d = 2
    while d*d <= x:
        while x % d == 0:
            out.append(d)
            x //= d
        d += 1 if d == 2 else 2
    if x > 1:
        out.append(x)
    return out


def roots(a, d):
    return [m for m in range(d) if (4*m*m+a) % d == 0]


def checks():
    count = 0
    primes = [p for p in range(3, 24) if prime(p)]
    for a in [s*q for q in primes for s in (1, -1)]:
        for p in primes:
            legendre = 0 if a % p == 0 else (1 if pow((-a) % p, (p-1)//2, p) == 1 else -1)
            assert len(roots(a, p)) == 1+legendre
            count += 1
        for d in (1, 2, 3, 5, 7, 15, 21, 35, 105):
            r = roots(a, d)
            assert len(r) == prod(len(roots(a,p)) for p in (2,3,5,7) if d % p == 0)
            actual = sum((4*m*m+a) % d == 0 for m in range(101, 201))
            assert abs(Fraction(actual)-Fraction(100*len(r),d)) <= len(r)
            count += 1
    # Quotient identity, including shared factors and both signs.
    signed = [s*q for q in (3,5,7,11) for s in (1,-1)]
    quotient_checks = 0
    for m in range(1,31):
        for a in signed:
            for b in signed:
                if a == b:
                    continue
                for d in range(1,16):
                    if (4*m*m+a) % d:
                        continue
                    for e in range(1,16):
                        g = gcd(d,e)
                        u,v = d//g,e//g
                        k = (4*m*m+a)//d
                        rhs = (a-b) % g == 0 and (u*k-(a-b)//g) % v == 0
                        assert ((4*m*m+b) % e == 0) == rhs
                        quotient_checks += 1
    # Exact local covariance: offsets 5,11 share roots mod 3.
    r1,r2 = set(roots(5,3)),set(roots(11,3))
    covariance = Fraction(len(r1&r2),3)-Fraction(len(r1)*len(r2),9)
    assert covariance == Fraction(2,9)
    assert factors(1) == [] and factors(49) == [7,7] and factors(77) == [7,11]
    return {'root_and_count_checks':count,'quotient_checks':quotient_checks,
            'covariance_example':str(covariance)}


def main():
    validation = checks()
    offsets = [q for q in range(3,44) if prime(q)]
    centers = list(range(1002,2001,2))
    raw = []
    for n in centers:
        for sign in (1,-1):
            for q in offsets:
                value = n*n+sign*q
                fac = factors(value)
                assert prod(fac) == value and all(prime(p) for p in fac)
                raw.append({'n':n,'sign':sign,'q':q,'value':value,
                            'factors':'*'.join(map(str,fac)),
                            'prime':int(len(fac)==1),
                            'rough_squarefree_P2':int(len(fac)<=2 and len(fac)==len(set(fac)) and fac[0]**4>n)})
    stats = []
    for R in (7,19,43):
        for kind in ('prime','rough_squarefree_P2'):
            occupied = {}
            for sign in (1,-1):
                nu = {n:0 for n in centers}
                for r in raw:
                    if r['sign']==sign and r['q']<=R and r[kind]:
                        nu[r['n']] += 1
                M1 = sum(nu.values())
                M2 = sum(v*v for v in nu.values())
                F2 = sum(v*(v-1) for v in nu.values())
                S = sum(v>0 for v in nu.values())
                assert M2 == M1+F2
                assert M1*M1 <= S*M2 and 0 <= 2*(M1-S) <= F2
                occupied[sign] = {n for n,v in nu.items() if v}
                stats.append({'R':R,'kind':kind,'sign':sign,'centers':len(centers),
                              'M1':M1,'M2':M2,'F2':F2,'occupied':S,
                              'cauchy_lower_bound':str(Fraction(M1*M1,M2)) if M2 else '0'})
            both = len(occupied[1]&occupied[-1])
            for row in stats[-2:]:
                row['occupied_both_signs'] = both
    dest = Path(__file__).resolve().parent
    dest.mkdir(exist_ok=True)
    with (dest/'witnesses.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(raw[0]));w.writeheader();w.writerows(raw)
    summary = {'scope':'Finite exact factorization; no asymptotic or positive-density theorem',
               'range':'even 1000 < n <= 2000','sigma':'1/4; tested exactly via least_prime_factor**4 > n',
               'validation':validation,'results':stats}
    (dest/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2))


if __name__ == '__main__':
    main()
