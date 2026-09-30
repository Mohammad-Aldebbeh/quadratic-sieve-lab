"""Independent enumeration checks after the prime-square proofs."""
from fractions import Fraction
from itertools import combinations, product
import unittest
from src.arithmetic import (legendre, prime_square_root_count,
                            prime_square_roots, roots)
from src.sieve import count_interval
from src.squarefree import (bad_classes, good_classes, local_bad_count,
                            survivor_classes, survivor_density, direct_survivors)


class SquarefreeTests(unittest.TestCase):
    def test_every_offset_residue_at_small_primes(self):
        for p in (2, 3, 5, 7, 11, 13, 17, 19):
            for a in range(-p * p, p * p + 1):
                brute = roots(a, p * p)
                self.assertEqual(prime_square_roots(a, p), brute, (a, p))
                self.assertEqual(prime_square_root_count(a, p), len(brute), (a, p))

    def test_singular_cases_and_two(self):
        for p in (3, 5, 7, 11):
            for a in (p, -p, p * (p + 1), -p * (p + 1)):
                self.assertEqual(prime_square_roots(a, p), [])
            for a in (0, p * p, -2 * p * p):
                self.assertEqual(prime_square_roots(a, p), list(range(0, p * p, p)))
        for a in range(-16, 17):
            self.assertEqual(prime_square_roots(a, 2), list(range(4)) if a % 4 == 0 else [])

    def test_overlap_and_duplicates(self):
        for p in (2, 3, 5, 7):
            for a, b in product(range(p * p), repeat=2):
                ra, rb = set(roots(a, p * p)), set(roots(b, p * p))
                self.assertEqual(ra & rb, ra if a == b else set())
                self.assertEqual(local_bad_count((a, b), p), len(ra | rb))
        for p in (2, 3, 5, 7, 11):
            offsets = (5, 5, 5 + p * p, -5, 0)
            brute = sorted({m for m in range(p * p)
                            if any((4 * m * m + a) % (p * p) == 0 for a in offsets)})
            self.assertEqual(bad_classes(offsets, p), brute)
            self.assertEqual(local_bad_count(offsets, p), len(brute))
            self.assertEqual(good_classes(offsets, p), sorted(set(range(p * p)) - set(brute)))

    def test_opposite_sign_formula(self):
        for q, p in product((3, 5, 7, 11, 13, 17, 19), (2, 3, 5, 7, 11, 13, 17, 19)):
            expected = 0 if p in (2, q) else 2 + legendre(q, p) + legendre(-q, p)
            self.assertEqual(local_bad_count((q, -q), p), expected)
            self.assertEqual(len(bad_classes((q, -q), p)), expected)
            self.assertLess(expected, p * p)

    def test_crt_full_periods_and_signed_intervals(self):
        families = ((), (0,), (4,), (2,), (3,), (-5,), (5, -5),
                    (5, 11), (0, 9), (1, 3, 5), (5, 5, 30))
        for size in range(4):
            for primes in combinations((2, 3, 5), size):
                for offsets in families:
                    period, classes = survivor_classes(offsets, primes)
                    brute = direct_survivors(offsets, primes, -1, period - 1)
                    self.assertEqual(classes, brute, (offsets, primes))
                    self.assertEqual(Fraction(len(classes), period), survivor_density(offsets, primes))
                    for start, stop in ((-37, 12), (0, 0), (17, 94), (100, 100 + 2 * period)):
                        count = count_interval(classes, period, start, stop)
                        self.assertEqual(count, len(direct_survivors(offsets, primes, start, stop)))
                        self.assertLessEqual(abs(Fraction(count) - (stop - start) * survivor_density(offsets, primes)), len(classes))

    def test_empty_sets_generators_and_invalid_moduli(self):
        self.assertEqual(survivor_classes((0,), ()), (1, [0]))
        self.assertEqual(survivor_density((), (2, 3)), 1)
        self.assertEqual(survivor_classes(iter((5, -5)), iter((2, 3))), survivor_classes((5, -5), (2, 3)))
        self.assertEqual(direct_survivors((5,), (), -2, 2), [-1, 0, 1, 2])
        for p in (0, 1, 4, 9, -3):
            for fn in (prime_square_roots, prime_square_root_count):
                with self.assertRaises(ValueError):
                    fn(3, p)
            with self.assertRaises(ValueError):
                bad_classes((), p)
        for primes in ((3, 3), (4,), (1,)):
            with self.assertRaises(ValueError):
                survivor_classes((3,), primes)
        with self.assertRaises(ValueError):
            direct_survivors((3,), (2,), 1, 0)

    def test_signed_prime_family_safe_class(self):
        primes = (2, 3, 5, 7, 11, 13, 17, 19)
        offsets = tuple(sign * q for sign in (-1, 1) for q in primes)
        for family in (offsets, (-30, -15, -10, -6, -1, 1, 6, 10, 15, 30)):
            for p in primes:
                self.assertNotIn(0, bad_classes(family, p))
                self.assertEqual(local_bad_count(family, p), len(bad_classes(family, p)))
            self.assertGreater(survivor_density(family, primes), 0)
            self.assertEqual(direct_survivors(family, primes, -1, 0), [0])


if __name__ == "__main__":
    unittest.main()
