"""Finite prime-square sieves; survival tests only the selected squares."""
from fractions import Fraction
from math import prod
from .arithmetic import is_prime, prime_square_root_count, prime_square_roots
from .sieve import validate_primes


def bad_classes(offsets, prime):
    """Union of the root sets modulo p**2 for the supplied offsets."""
    if not is_prime(prime):
        raise ValueError("modulus must be prime")
    return sorted({r for a in offsets for r in prime_square_roots(a, prime)})


def good_classes(offsets, prime):
    """Complement of bad_classes in the canonical period p**2."""
    bad = set(bad_classes(offsets, prime))
    return [r for r in range(prime * prime) if r not in bad]


def local_bad_count(offsets, prime):
    """Formula for beta^(2): count each distinct offset residue once."""
    if not is_prime(prime):
        raise ValueError("modulus must be prime")
    modulus = prime * prime
    return sum(prime_square_root_count(a, prime)
               for a in {a % modulus for a in offsets})


def survivor_density(offsets, primes):
    """Exact rational density for a finite set of prime squares."""
    offsets = tuple(offsets)
    primes = validate_primes(primes)
    return prod((Fraction(p * p - local_bad_count(offsets, p), p * p)
                 for p in primes), start=Fraction(1))


def survivor_classes(offsets, primes):
    """Return (product of p**2, sorted CRT survivor classes)."""
    offsets = tuple(offsets)
    primes = validate_primes(primes)
    period, classes = 1, [0]
    for p in primes:
        modulus = p * p
        good = good_classes(offsets, p)
        inverse = pow(period, -1, modulus)
        classes = sorted(r + period * (((s - r) * inverse) % modulus)
                         for r in classes for s in good)
        period *= modulus
    return period, classes


def direct_survivors(offsets, primes, start, stop):
    """Independent direct divisibility checks on start < m <= stop.

    gcd(G_a, product(p**2)) = 1 would test prime divisibility instead
    and is deliberately not used here.
    """
    offsets = tuple(offsets)
    squares = tuple(p * p for p in validate_primes(primes))
    if stop < start:
        raise ValueError("start must not exceed stop")
    return [m for m in range(start + 1, stop + 1)
            if all((4 * m * m + a) % square != 0
                   for a in offsets for square in squares)]
