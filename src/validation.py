"""Original bounded algebra checks; finite verification, not general proofs."""
from fractions import Fraction
from math import gcd, prod
from .arithmetic import factorize, is_prime, legendre, roots


def algebra_checks():
    count = 0
    primes = [p for p in range(3, 24) if is_prime(p)]
    for a in [s * q for q in primes for s in (1, -1)]:
        for p in primes:
            if len(roots(a, p)) != 1 + legendre(-a, p):
                raise ArithmeticError("local root formula failed")
            count += 1
        for d in (1, 2, 3, 5, 7, 15, 21, 35, 105):
            r = roots(a, d)
            expected = prod(len(roots(a, p)) for p in (2, 3, 5, 7) if d % p == 0)
            actual = sum((4 * m * m + a) % d == 0 for m in range(101, 201))
            if len(r) != expected or abs(Fraction(actual) - Fraction(100 * len(r), d)) > len(r):
                raise ArithmeticError("CRT or interval count failed")
            count += 1
    signed = [s * q for q in (3, 5, 7, 11) for s in (1, -1)]
    quotient_checks = 0
    for m in range(1, 31):
        for a in signed:
            for b in signed:
                if a == b:
                    continue
                for d in range(1, 16):
                    if (4 * m * m + a) % d:
                        continue
                    for e in range(1, 16):
                        g = gcd(d, e)
                        u, v = d // g, e // g
                        k = (4 * m * m + a) // d
                        rhs = (a - b) % g == 0 and (u * k - (a - b) // g) % v == 0
                        if ((4 * m * m + b) % e == 0) != rhs:
                            raise ArithmeticError("quotient identity failed")
                        quotient_checks += 1
    r1, r2 = set(roots(5, 3)), set(roots(11, 3))
    covariance = Fraction(len(r1 & r2), 3) - Fraction(len(r1) * len(r2), 9)
    if covariance != Fraction(2, 9):
        raise ArithmeticError("covariance example failed")
    if not (factorize(1) == [] and factorize(49) == [7, 7] and factorize(77) == [7, 11]):
        raise ArithmeticError("factorization examples failed")
    return {"root_and_count_checks": count, "quotient_checks": quotient_checks,
            "covariance_example": str(covariance)}
