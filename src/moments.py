"""Witness moments and occupancy, with exact integer verification."""
from fractions import Fraction


def witness_moments(counts):
    counts = tuple(counts)
    if any(not isinstance(j, int) or j < 0 for j in counts):
        raise ValueError("witness counts must be nonnegative integers")
    first = sum(counts)
    second = sum(j * j for j in counts)
    factorial = sum(j * (j - 1) for j in counts)
    occupied = sum(j > 0 for j in counts)
    if not (second == first + factorial and first * first <= occupied * second
            and 0 <= 2 * (first - occupied) <= factorial):
        raise ArithmeticError("moment identity or occupancy inequality failed")
    return {"M1": first, "M2": second, "F2": factorial, "occupied": occupied,
            "cauchy_lower_bound": str(Fraction(first * first, second)) if second else "0"}
