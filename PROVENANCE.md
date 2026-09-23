# Methods and source

## Mathematical scope

This project develops selected elementary ideas from Mohammad Aldebbeh's exploratory manuscript, *Sharp Transition Laws for Rough Squarefree Almost-Primes at Prime Offsets from Squares*. It is a self-contained treatment of finite residue counts, sieve bounds, correlations, and witness moments.

The tools are modular arithmetic, quadratic residues and Legendre symbols, the Chinese remainder theorem, inclusion-exclusion, the Möbius function on squarefree integers, finite probability, Cauchy-Schwarz, and prime factorization.

## Verification

- Complete proofs of the finite identities and inequalities appear in NOTE.md.
- Local formulas and quotient congruences are checked against direct enumeration.
- Every tested value in the experiment is fully factored; all factors are checked for primality and their product is verified.
- Raw factorizations and summary statistics accompany the code.
- Separate upper, lower, and simultaneous occupancy counts distinguish the different existence questions.

## Relationship to the source manuscript

The root-count setup, elementary moment reasoning, and shared-divisor calculations are developed here independently of the source manuscript's advanced analytic estimates. Those estimates and its numerical certificates are not inputs to the proofs or experiments in this repository. The source map at the end of NOTE.md identifies the relevant sections.

The conclusions concern exact finite identities and the stated experimental window; extension to asymptotic density statements requires additional estimates.
