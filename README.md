# Local sieves and witness counts for shifted squares

A mathematical and computational project by Mohammad Aldebbeh studying small-prime divisibility of $4m^2\pm q$ and the relationship between witness counts and the number of even squares with a successful offset.

## Results

The mathematical note derives exact quadratic-residue counts, a finite inclusion-exclusion sieve bound, a shared-divisor identity, an explicit covariance example, and inequalities relating witness moments to occupancy. The arguments use modular arithmetic, the Chinese remainder theorem, inclusion-exclusion, and Cauchy-Schwarz.

An exact experiment compares prime witnesses with rough squarefree numbers having at most two prime factors, for 500 even inputs $1000<n\le2000$ and odd prime offsets up to 43. At offset cutoff 43, both signs have prime witnesses at 390 of the 500 centers; both have qualifying almost-prime witnesses at 499 centers. The full results retain separate upper, lower, and simultaneous counts.

These results consist of elementary identities and finite computations. The universal prime-offset questions and asymptotic occupancy laws remain open in this project.

## Contents

- [Mathematical note](NOTE.md): proofs, experiment, and results.
- [Methods and source](PROVENANCE.md): mathematical scope and verification.
- [Experiment](experiment.py), [complete factorizations](witnesses.csv), and [summary](summary.json).

## Reproduce

```sh
python experiment.py
```

Python's standard library is sufficient. The script factors every tested value exactly and compares prime witnesses with squarefree numbers having at most two prime factors and least prime factor greater than $n^{1/4}$. It verifies every factor's primality and multiplies factors back to recover the input. Algebra checks cover 272 local-root/count cases and 47,670 quotient-congruence cases; moment inequalities are checked with exact integer arithmetic.
