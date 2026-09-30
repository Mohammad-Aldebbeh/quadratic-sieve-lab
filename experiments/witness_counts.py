"""Exact prime and rough squarefree P2 witnesses; run as a module from repo root."""
import argparse
import csv
import json
from math import prod
from pathlib import Path
from src.arithmetic import factorize, is_prime, witness_flags
from src.moments import witness_moments
from src.validation import algebra_checks

ROOT = Path(__file__).resolve().parents[1]


def run(lower=1000, upper=2000, cutoffs=(7, 19, 43)):
    """Return factorizations and statistics; lower < even n <= upper."""
    cutoffs = tuple(sorted(set(cutoffs)))
    if lower < 0 or upper <= lower or not cutoffs or min(cutoffs) < 3:
        raise ValueError("require 0 <= lower < upper and offset cutoffs >= 3")
    centers = list(range(lower + 1 + (lower + 1) % 2, upper + 1, 2))
    if not centers:
        raise ValueError("the interval contains no positive even centers")
    offsets = [q for q in range(3, max(cutoffs) + 1) if is_prime(q)]
    raw = []
    for n in centers:
        for sign in (1, -1):
            for q in offsets:
                value = n * n + sign * q
                factors = factorize(value) if value >= 1 else []
                if value >= 1 and (prod(factors) != value or not all(is_prime(p) for p in factors)):
                    raise ArithmeticError("factorization verification failed")
                raw.append({"n": n, "sign": sign, "q": q, "value": value,
                            "factors": "*".join(map(str, factors)),
                            **witness_flags(value, factors, n)})
    stats = []
    for cutoff in cutoffs:
        for kind in ("prime", "rough_squarefree_P2"):
            occupied = {}
            for sign in (1, -1):
                counts = dict.fromkeys(centers, 0)
                for row in raw:
                    if row["sign"] == sign and row["q"] <= cutoff and row[kind]:
                        counts[row["n"]] += 1
                occupied[sign] = {n for n, j in counts.items() if j}
                stats.append({"R": cutoff, "kind": kind, "sign": sign,
                              "centers": len(centers), **witness_moments(counts.values())})
            both = len(occupied[1] & occupied[-1])
            for row in stats[-2:]:
                row["occupied_both_signs"] = both
    summary = {
        "scope": "Finite exact factorization; no asymptotic or positive-density theorem",
        "range": f"even {lower} < n <= {upper}",
        "sigma": "1/4; tested exactly via least_prime_factor**4 > n",
        "parameters": {"lower_exclusive": lower, "upper_inclusive": upper,
                       "offset_cutoffs": list(cutoffs), "rows": len(raw)},
        "validation": algebra_checks(), "results": stats}
    return raw, summary


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lower", type=int, default=1000)
    parser.add_argument("--upper", type=int, default=2000)
    parser.add_argument("--cutoffs", type=int, nargs="+", default=[7, 19, 43])
    parser.add_argument("--output", type=Path, default=ROOT / "results")
    args = parser.parse_args(argv)
    try:
        raw, summary = run(args.lower, args.upper, args.cutoffs)
    except ValueError as error:
        parser.error(str(error))
    args.output.mkdir(parents=True, exist_ok=True)
    with (args.output / "witnesses.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(raw[0]))
        writer.writeheader()
        writer.writerows(raw)
    (args.output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"Verified {len(raw)} tested values; wrote results to {args.output.resolve()}")


if __name__ == "__main__":
    main()
