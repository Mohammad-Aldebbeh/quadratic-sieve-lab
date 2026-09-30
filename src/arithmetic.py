"""Exact arithmetic for G_a(m) = 4*m*m + a; no probabilistic primality tests."""
from math import isqrt


def is_prime(value):
    """Trial-division primality test, suitable for this project's small inputs."""
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    return all(value % d for d in range(3, isqrt(value) + 1, 2))


def factorize(value):
    """Sorted prime factors with multiplicity; 1 has the empty factorization."""
    if value < 1:
        raise ValueError("factorization requires a positive integer")
    factors = []
    divisor = 2
    while divisor * divisor <= value:
        while value % divisor == 0:
            factors.append(divisor)
            value //= divisor
        divisor += 1 if divisor == 2 else 2
    if value > 1:
        factors.append(value)
    return factors


def roots(offset, modulus):
    """Canonical roots in 0,...,modulus-1, by direct enumeration."""
    if modulus < 1:
        raise ValueError("modulus must be positive")
    return [m for m in range(modulus) if (4 * m * m + offset) % modulus == 0]


def legendre(value, prime):
    """Legendre symbol at an odd prime, including the zero case."""
    if prime == 2 or not is_prime(prime):
        raise ValueError("Legendre symbol requires an odd prime")
    residue = pow(value % prime, (prime - 1) // 2, prime)
    return 0 if residue == 0 else (1 if residue == 1 else -1)


def local_root_count(offset, prime):
    """Number of roots of G_a modulo a prime (also handles even a)."""
    if not is_prime(prime):
        raise ValueError("sieving moduli must be prime")
    if prime == 2:
        return 2 if offset % 2 == 0 else 0
    return 1 + legendre(-offset, prime)


def prime_square_root_count(offset, prime):
    """Number of roots modulo p**2, including p = 2 and singular roots."""
    if not is_prime(prime):
        raise ValueError("sieving moduli must be prime")
    if prime == 2:
        return 4 if offset % 4 == 0 else 0
    if offset % (prime * prime) == 0:
        return prime
    if offset % prime == 0:
        return 0
    return 1 + legendre(-offset, prime)


def prime_square_roots(offset, prime):
    """Canonical roots modulo p**2, using the elementary one-step lift.

    Root construction is separate from the count formula so enumeration
    can check both. Negative and zero offsets are supported.
    """
    if not is_prime(prime):
        raise ValueError("sieving moduli must be prime")
    if prime == 2:
        return list(range(4)) if offset % 4 == 0 else []
    if offset % (prime * prime) == 0:
        return [prime * k for k in range(prime)]
    if offset % prime == 0:
        return []
    lifted = []
    for r in roots(offset, prime):
        quotient = (4 * r * r + offset) // prime
        t = (-quotient * pow(8 * r, -1, prime)) % prime
        lifted.append(r + prime * t)
    return sorted(lifted)


def witness_flags(value, factors, center):
    """Prime and rough squarefree P2 indicators for an exact factorization.

    A P2 value is >1, has at most two prime factors with multiplicity, is
    squarefree, and has least prime factor p with p**4 > center.
    Callers supply a verified complete factorization.
    """
    prime = value > 1 and len(factors) == 1
    almost = (value > 1 and 1 <= len(factors) <= 2
              and len(factors) == len(set(factors)) and factors[0] ** 4 > center)
    return {"prime": int(prime), "rough_squarefree_P2": int(almost)}
