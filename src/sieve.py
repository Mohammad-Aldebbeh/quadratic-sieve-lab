"""CRT survivor classes and exact interval counts, for finite prime sets."""
from fractions import Fraction
from math import gcd, prod
from .arithmetic import is_prime, local_root_count, roots


def validate_primes(primes):
    primes = tuple(primes)
    if len(set(primes)) != len(primes) or any(not is_prime(p) for p in primes):
        raise ValueError("provide distinct prime moduli")
    return primes


def local_bad_count(offsets, prime):
    """Union of bad classes, grouping offsets equal modulo the prime.

    For distinct offset residues the root sets are disjoint. This implements
    the joint-survival proposition without enumerating the roots.
    """
    if not is_prime(prime):
        raise ValueError("modulus must be prime")
    return sum(local_root_count(a, prime) for a in {a % prime for a in offsets})


def survivor_density(offsets, primes):
    """Exact density over a full period; this is a finite rational product."""
    offsets = tuple(offsets)
    primes = validate_primes(primes)
    return prod((Fraction(p - local_bad_count(offsets, p), p) for p in primes),
                start=Fraction(1))


def survivor_classes(offsets, primes):
    """Return (period, sorted survivors) using iterative CRT lifting.

    Memory grows with the number of survivor classes. This is intended for
    small products; direct interval sieving can be cheaper for larger ones.
    """
    offsets = tuple(offsets)
    primes = validate_primes(primes)
    period, classes = 1, [0]
    for p in primes:
        bad = set().union(*(set(roots(a, p)) for a in offsets))
        good = set(range(p)) - bad
        inverse = pow(period, -1, p)
        classes = sorted(r + period * (((s - r) * inverse) % p)
                         for r in classes for s in good)
        period *= p
    return period, classes


def count_interval(classes, period, start, stop):
    """Exact number of survivors in start < m <= stop (also for negative m)."""
    if period < 1 or stop < start:
        raise ValueError("positive period and start <= stop required")
    return sum((stop - r) // period - (start - r) // period for r in classes)


def direct_survivors(offsets, primes, start, stop):
    """Independent bounded enumeration for checking the CRT implementation."""
    offsets = tuple(offsets)
    period = prod(validate_primes(primes))
    if stop < start:
        raise ValueError("start must not exceed stop")
    return [m for m in range(start + 1, stop + 1)
            if all(gcd(4 * m * m + a, period) == 1 for a in offsets)]
