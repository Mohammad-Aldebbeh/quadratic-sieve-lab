# Local sieves, correlations, and witness counts for shifted squares

Mohammad Aldebbeh — September 2026. A self-contained treatment of local residue counts, finite sieves, correlations, and witness moments for shifted squares, with an exact computational experiment.

## 1. Two different counting questions

Write an even square as $n^2=4m^2$. For a signed odd prime offset $a\in\{q,-q\}$, put

$$G_a(m)=4m^2+a.$$

The companion prime-offset project fixes $n$ and searches over $q$. Here we fix one or more offsets and examine the centers $m$. This makes residue classes and correlations visible.

A prime witness has $G_a(m)$ prime. A squarefree $P_2$ witness has $G_a(m)>1$, no repeated prime factor, and at most two prime factors counted with multiplicity. Thus primes qualify as $P_2$ values, while a prime square does not qualify as squarefree. A roughness requirement $P^-(G_a(m))>n^{1/4}$ excludes small prime factors. These definitions describe finite sets; they assert no theorem about their abundance.

## 2. Local root counts

Let $\rho_a(d)$ count solutions of $G_a(m)\equiv0\pmod d$. At an odd prime $p$,

$$\rho_a(p)=1+\left(\frac{-a}{p}\right),$$

where the Legendre symbol is 0 if $p\mid a$. To see this, multiplication by 2 is a bijection modulo $p$, reducing the congruence to $x^2=-a$. It has one root when the right side is zero, two when it is a nonzero square, and zero otherwise. For odd $a$, $\rho_a(2)=0$.

If $d$ is squarefree, the Chinese remainder theorem gives

$$\rho_a(d)=\prod_{p\mid d}\rho_a(p)\le2^{\omega(d)}.$$

This is the elementary part of the longer manuscript's local-density analysis. It does not need Dirichlet $L$-functions or an infinite product.

## 3. Counting in a finite interval

Let $X$ be a positive integer, and let $A_a(d;X)$ count integers $X<m\le2X$ for which $d\mid G_a(m)$. Each residue class occurs either $\lfloor X/d\rfloor$ or $\lceil X/d\rceil$ times, hence

$$\left|A_a(d;X)-X\frac{\rho_a(d)}d\right|\le\rho_a(d).$$

This bound holds without squarefreeness. For squarefree $d$, the preceding factorization makes the main term explicit. It also exposes a limitation: for large $d$ the error can overwhelm the main term. A precise local formula does not automatically supply a strong global prime-counting theorem.

## 4. An exact finite sieve

Let $\mathcal P$ be a finite set of primes and $P=\prod_{p\in\mathcal P}p$. A center survives this sieve if $\gcd(G_a(m),P)=1$. Inclusion-exclusion gives

$$S_a(X;P)=\sum_{d\mid P}\mu(d)A_a(d;X).$$

Substituting Section 3 and multiplying the finite sums yields the explicit bound

$$\left|S_a(X;P)-X\prod_{p\mid P}\left(1-\frac{\rho_a(p)}p\right)\right|
\le\prod_{p\mid P}(1+\rho_a(p)).$$

For odd $a$ and $k$ odd sieving primes the right side is at most $3^k$. This is a useful rigorous result at modest cutoffs, and a clear reason that simply adding more sieving primes eventually makes this elementary error estimate unhelpful.

Passing the sieve only means having no prime divisor in $\mathcal P$. Composite numbers with larger prime factors survive. Conversely, a prime value equal to a sieving prime is removed. In interpreting survivors as candidates, either work above all sieving primes or handle these small equalities explicitly.

## 5. Shared divisors and correlations

For distinct signed offsets $a,b$, suppose $d\mid G_a(m)$ and $e\mid G_b(m)$. Subtracting the two values gives

$$\gcd(d,e)\mid a-b.$$

Thus equal-sign offsets involve $q-r$, while opposite signs involve $q+r$. This is a necessary condition, not in general a sufficient one.

There is a sharper exact statement. Write $g=\gcd(d,e)$, $d=gu$, $e=gv$, and $k=G_a(m)/d$. Since $\gcd(u,v)=1$,

$$e\mid G_b(m)\quad\Longleftrightarrow\quad g\mid(a-b)
\quad\text{and}\quad uk\equiv(a-b)/g\pmod v.$$

**Proof.** Substitute $G_b(m)=guk-(a-b)$ and divide the divisibility relation by $g$ once $g\mid a-b$. $\square$

An elementary example shows why independence can fail. Modulo 3, both $4m^2+5$ and $4m^2+11$ vanish at $m=1,2$. With a uniformly chosen residue $m\pmod3$, each divisibility event has probability $2/3$, and the joint probability is also $2/3$. Their covariance is

$$\frac23-\left(\frac23\right)^2=\frac29.$$

This is an exact finite probability calculation. It does not assume that the integers themselves are random. It shows that distinct offsets need not give independent local events.

## 6. Witness counts and occupied centers

On any finite set of centers, let $\nu(n)$ be the number of offsets satisfying a chosen witness condition. Define

$$M_1=\sum_n\nu(n),\quad M_2=\sum_n\nu(n)^2,\quad
F_2=\sum_n\nu(n)(\nu(n)-1),\quad S=\#\{n:\nu(n)>0\}.$$

Then $M_2=M_1+F_2$. For $M_2>0$, Cauchy-Schwarz on the occupied centers gives

$$\frac{M_1^2}{M_2}\le S\le M_1.$$

The upper inequality follows because each occupied center contributes at least one witness. Also,

$$0\le M_1-S\le\frac12 F_2.$$

Indeed, for each nonnegative integer $j$, $0\le j-\mathbf1_{j>0}\le j(j-1)/2$. Summing proves the claim. If $M_2=0$, all counts vanish and we interpret the lower bound as zero.

These statements explain what the long manuscript's occupancy deductions are doing. They are rigorous independently of its advanced moment estimates. If one could separately prove $M_1\ge cHK$ and $M_2\le CH(K+K^2)$ for $H$ centers and positive $K$, then they would imply

$$S\ge\frac{c^2}{C}H\frac{K}{1+K}.$$

This last sentence is a conditional implication; this note does not establish those moment hypotheses at arbitrarily large scales.

Separate lower bounds on upper-side and lower-side occupancy do not guarantee a common occupied center unless their sizes force overlap. Always,

$$|A_+\cap A_-|\ge\max(0,|A_+|+|A_-|-H).$$

For example, two disjoint subsets can each occupy 40% of the centers. Directly measuring the intersection is therefore essential when discussing two-sided experiments.

## 7. Exact finite experiment

We checked the 500 even centers $1000<n\le2000$, with odd prime offsets up to $R\in\{7,19,43\}$. Each tested integer was completely factored by trial division. For the second witness class we imposed squarefreeness, at most two prime factors counted with multiplicity, and least prime factor $p$ satisfying $p^4>n$, which is an exact integer test of the roughness condition.

| R | Witness class | Upper occupied | Lower occupied | Both sides occupied |
|---|---|---:|---:|---:|
| 7 | Prime | 216 | 236 | 104 |
| 7 | Rough squarefree P2 | 454 | 461 | 421 |
| 19 | Prime | 329 | 380 | 249 |
| 19 | Rough squarefree P2 | 497 | 498 | 495 |
| 43 | Prime | 439 | 448 | 390 |
| 43 | Rough squarefree P2 | 499 | 500 | 499 |

At $R=7$ for upper prime witnesses, $M_1=246$, $M_2=306$, and $F_2=60$. The moment bound gives $S\ge246^2/306=3362/17$, while the exact occupancy is 216. Here $M_1-S=30=F_2/2$. The script records corresponding statistics for every row and checks all the elementary moment inequalities with exact integer arithmetic.

The difference between the two witness classes is substantial in this finite window. It illustrates why evidence for almost-primes cannot simply be relabeled as evidence for primes. The data establish no asymptotic law or density-one conclusion.

## 8. Scope and further work

The proofs here establish exact residue formulas, a finite sieve estimate, a shared-divisor identity, and general moment inequalities. The experiment illustrates them with fully factored values. A useful next extension is to repeat the experiment on several disjoint windows and study occupancy by residue class, preserving raw data and reporting failures as well as successes.

The original manuscript's Type-II estimates, indefinite quadratic forms, automorphic kernels, singular-series moment theorems, numerical 2.8% assertion, and simultaneous P5/P8 laws are outside this project. The proofs and experiments here depend only on the elementary arguments given in this note.

## Source map

- The root-count setup comes from Section 3 and the signed discussion in Section 14 of the source manuscript.
- The finite moment deductions correspond to the elementary reasoning around Corollary 2.5; they remain valid without accepting the manuscript's asymptotic estimates.
- The shared-divisor identity and covariance example come from Appendix C.5. The explanations and independent finite tests were prepared during this revision.
- The exact unsmoothed count, finite inclusion-exclusion bound, and new experiment were added for this undergraduate version.

The treatment uses standard elementary methods; the source map records the relationship to the earlier manuscript.
