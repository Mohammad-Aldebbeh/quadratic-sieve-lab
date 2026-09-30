"""Independent small enumerations of the arithmetic used in the note."""
from fractions import Fraction
from itertools import combinations, product
from math import gcd, prod
import unittest
from src.arithmetic import factorize, is_prime, local_root_count, roots, witness_flags
from src.moments import witness_moments
from src.sieve import (count_interval, direct_survivors, local_bad_count,
                       survivor_classes, survivor_density)
from src.validation import algebra_checks
from experiments.witness_counts import run
from experiments.local_sieve import run as run_local


class ArithmeticTests(unittest.TestCase):
    def test_factorization_against_independent_divisor_test(self):
        for value in range(1, 1001):
            factors = factorize(value)
            self.assertEqual(prod(factors), value)
            self.assertTrue(all(is_prime(p) for p in factors))
            trial_prime = value > 1 and not any(value % d == 0 for d in range(2, value))
            self.assertEqual(is_prime(value), trial_prime)
        for value in (0, -1):
            with self.assertRaises(ValueError):
                factorize(value)

    def test_prime_roots_and_edge_cases(self):
        for a, p in product(range(-12, 13), (2, 3, 5, 7, 11, 13)):
            self.assertEqual(local_root_count(a, p), len(roots(a, p)))
        for p in (0, 1, 4, 9):
            with self.assertRaises(ValueError):
                local_root_count(3, p)

    def test_pair_union_and_covariance(self):
        for a, b, p in product(range(-7, 8), range(-7, 8), (2, 3, 5, 7)):
            ra, rb = set(roots(a, p)), set(roots(b, p))
            self.assertEqual(local_bad_count((a, b), p), len(ra | rb))
            expected_joint = len(ra) if (a - b) % p == 0 else 0
            self.assertEqual(len(ra & rb), expected_joint)
            covariance = Fraction(expected_joint, p) - Fraction(len(ra) * len(rb), p * p)
            if (a - b) % p:
                self.assertLessEqual(covariance, 0)
        self.assertEqual(local_bad_count((5, 11), 3), 2)
        for q, p in product((3, 5, 7, 11), (2, 3, 5, 7, 11, 13, 19)):
            beta = local_bad_count((q, -q), p)
            self.assertLess(beta, p)
            if p != q and p % 4 == 3:
                self.assertEqual(beta, 2)

    def test_crt_classes_and_interval_counts(self):
        for offsets in ((), (3,), (-5,), (5, -5), (5, 11), (0,), (3, 5, 7)):
            for size in range(4):
                for primes in combinations((2, 3, 5), size):
                    period, classes = survivor_classes(offsets, primes)
                    brute = [m for m in range(period)
                             if all(gcd(4 * m * m + a, period) == 1 for a in offsets)]
                    self.assertEqual(classes, brute)
                    self.assertEqual(Fraction(len(classes), period), survivor_density(offsets, primes))
                    for start, stop in ((-11, 3), (0, 0), (0, period), (17, 94)):
                        actual = len(direct_survivors(offsets, primes, start, stop))
                        self.assertEqual(count_interval(classes, period, start, stop), actual)
        for primes in ((3, 3), (4,), (1,)):
            with self.assertRaises(ValueError):
                survivor_classes((3,), primes)

    def test_finite_inclusion_exclusion(self):
        primes = (2, 3, 5, 7)
        for a in (-11, -5, 3, 5, 11):
            start, stop = 50, 100
            total = 0
            for size in range(len(primes) + 1):
                for subset in combinations(primes, size):
                    d = prod(subset)
                    count = sum((4 * m * m + a) % d == 0 for m in range(start + 1, stop + 1))
                    total += (-1) ** size * count
            self.assertEqual(total, len(direct_survivors((a,), primes, start, stop)))
            bound = prod(1 + local_root_count(a, p) for p in primes)
            self.assertLessEqual(abs(Fraction(total) - (stop - start) * survivor_density((a,), primes)), bound)

    def test_witness_definitions_and_zero_moments(self):
        for value, factors, n, expected in ((1, [], 2, (0, 0)), (-1, [], 2, (0, 0)),
                (49, [7, 7], 1000, (0, 0)), (77, [7, 11], 1000, (0, 1)),
                (15, [3, 5], 1000, (0, 0)), (101, [101], 1000, (1, 1)),
                (6, [2, 3], 16, (0, 0))):
            flags = witness_flags(value, factors, n)
            self.assertEqual((flags["prime"], flags["rough_squarefree_P2"]), expected)
        self.assertEqual(witness_moments([0, 0])["cauchy_lower_bound"], "0")
        for counts in product(range(4), repeat=4):
            witness_moments(counts)

    def test_original_bounded_algebra_checks(self):
        self.assertEqual(algebra_checks(), {"root_and_count_checks": 272,
                                         "quotient_checks": 47670,
                                         "covariance_example": "2/9"})

    def test_small_witness_window_and_unit_value(self):
        raw, summary = run(0, 4, (3, 7))
        self.assertEqual(summary["parameters"]["rows"], 12)
        for row in raw:
            if row["value"] <= 1:
                self.assertEqual((row["prime"], row["rough_squarefree_P2"]), (0, 0))
        with self.assertRaises(ValueError):
            run(2, 3, (3,))

    def test_local_experiment_prime_iterator(self):
        self.assertEqual(run_local(iter((2, 3, 5)), -10, 20),
                         run_local((2, 3, 5), -10, 20))


if __name__ == "__main__":
    unittest.main()
