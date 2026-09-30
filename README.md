# Local sieves for shifted even squares

A number-theory project by Mohammad Aldebbeh, studying

$$G_a(m)=4m^2+a,$$

especially the opposite-sign shifts $a=\pm q$ for an odd prime $q$. The project asks which centers survive finite divisibility restrictions, how several shifts interact, and how witness counts relate to occupied centers.

Read the **[mathematical note (PDF)](math/note.pdf)** or its **[LaTeX source](math/note.tex)**. The historical repository name `quadratic-sieve-lab` does not describe an implementation of the classical quadratic-sieve factoring algorithm.

## Mathematics

The project combines quadratic residues, the Chinese remainder theorem, finite inclusion-exclusion, and Cauchy-Schwarz for several shifted squares. The prime-square extension is proved by elementary lifting and implemented with exact arithmetic.

For an odd prime, the bad-class count is

$$\rho_a(p)=1+\left(\frac{-a}{p}\right).$$

For a prime square, it is

$$\rho_a(p^2)=\begin{cases}
1+\left(\frac{-a}{p}\right),&p\nmid a,\\
0,&p\mid a,\quad p^2\nmid a,\\
p,&p^2\mid a.
\end{cases}$$

At modulus $2$, there are no bad classes for odd offsets and both classes are bad for even offsets. At modulus $4$, all four classes are bad if $4\mid a$, and none otherwise. The note proves the nondegenerate lifting step directly and treats the repeated-root cases separately.

For a finite offset family $A$, root sets at any modulus are identical for congruent offsets and disjoint for distinct offset residues. In particular,

$$\beta_A^{(2)}(p)=\sum_{c\in A\bmod p^2}\rho_c(p^2),$$

using each distinct residue once. For a finite prime set $\mathcal P$ and $M=\prod_{p\in\mathcal P}p^2$, CRT gives

$$N_A^{(2)}(M)=\prod_{p\in\mathcal P}(p^2-\beta_A^{(2)}(p)),\qquad
\delta_A^{(2)}(M)=\prod_{p\in\mathcal P}\left(1-\frac{\beta_A^{(2)}(p)}{p^2}\right).$$

For the prime sieve, with $P=\prod_{p\in\mathcal P}p$ and $\beta_A(p)=\sum_{c\in A\bmod p}\rho_c(p)$, the corresponding density is $\delta_A(P)=\prod_{p\in\mathcal P}(1-\beta_A(p)/p)$. The note also proves finite inclusion-exclusion and interval bounds, local covariance, a divisor-compatibility identity, and witness-moment inequalities.

**Opposite-sign result.** For $A=\{q,-q\}$ with $q$ an odd prime, the prime-square bad count is zero at $p=2$ and $p=q$. At other odd primes it is

$$2+\left(\frac{q}{p}\right)+\left(\frac{-q}{p}\right),$$

equal to $2$ when $p\equiv3\pmod4$, and $0$ or $4$ when $p\equiv1\pmod4$. Every finite prime-square-sieve density is positive. The prime-sieve density is positive too, with one bad class at $p=q$. More generally, a finite family of nonzero squarefree integer offsets has no prime-square obstruction: the local class $m=0$ is always safe. This includes signed prime offsets.

## Exact computations

- [Prime sieve](results/local_sieve.md): seven families, period $210$, prime set $\{2,3,5,7\}$.
- [Prime-square sieve](results/squarefree_sieve.md): thirteen families, period $44{,}100$, the same prime set. This includes singular roots, repeated offsets, zero/even offsets, and an empty family.
- [Witness experiment](results/summary.json): all 13,000 values for 500 even centers $1000<n\le2000$ and 13 odd prime offsets through 43, on both signs. [Complete factorizations](results/witnesses.csv), including failures, are retained.

Both sieve experiments compare complete CRT periods and the interval $500<m\le1000$ with direct enumeration. For $A=\{5,-5\}$, prime-square density is $47/63$, giving 32,900 classes per period and 372 survivors in that interval.

The witness experiment distinguishes primes from **rough squarefree $P_2$** values: values greater than 1, no repeated prime factor, at most two prime factors with multiplicity, and least factor $p$ satisfying $p^4>n$. At offset cutoff 43, both signs are occupied at 390 centers for primes and 499 for rough squarefree $P_2$. **The two signs can use different successful offsets.**

## Scope

Surviving selected prime squares means avoiding those squares only. It does not certify global squarefreeness, primality, roughness, or the $P_2$ condition. The local densities are exact finite-period proportions; positive densities for every finite prime set do not establish a global simultaneous-squarefreeness or prime theorem. The witness tables give exact observations in the stated finite window. The note explains the small-prime equality exception and the unproved hypotheses behind any asymptotic moment deduction.

## Reproduce

Use **Python 3.10 or later, standard library only**, from the repository root:

```sh
python -m unittest discover -s tests -v
python -m experiments.witness_counts
python -m experiments.local_sieve
python -m experiments.squarefree_sieve
```

The experiments regenerate the checked-in files in `results/`. For an alternative prime-square run saved separately:

```sh
python -m experiments.squarefree_sieve --primes 2 3 5 --start -100 --stop 100 --output results/squarefree-small
```

Each module accepts `--help` and `--output`. The old `python experiment.py` command remains supported. Trial division and explicit CRT class storage are suitable for modest inputs; period sizes grow quickly. Arithmetic tests check formulas against independent enumeration after the mathematical proofs.

To rebuild the standalone PDF using an existing Tectonic installation:

```sh
tectonic math/note.tex
```

Or run an existing LaTeX installation twice:

```sh
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=math math/note.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=math math/note.tex
```

No external bibliography or figures are required.

## Repository

```text
math/                       Standalone note source and compiled PDF
src/                        Exact arithmetic, prime/square sieves, moments
experiments/                Reproducible parameterized experiments
tests/                      Arithmetic and independent enumeration checks
results/                    Selected exact outputs and all witness rows
```

The original project remains available in Git history. The top-level `experiment.py` is a compatibility entry point for the witness experiment.

## Further questions

1. Count roots modulo $p^k$ for $k\ge3$, including repeated-root cases, and study finite power-free sieves.
2. Classify minimal signed-prime families obstructing the prime sieve modulo 3 and 5, despite their prime-square admissibility.
3. Determine sharp count-discrepancy bounds as a fixed window is translated through a CRT period.
