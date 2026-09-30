# Exact experiment outputs

- `witnesses.csv`: all original 13,000 complete factorizations, including failures; unchanged byte-for-byte.
- `summary.json`: original twelve moment/occupancy records and validation fields, plus parameters.
- `local_sieve.json`, `local_sieve.md`: seven fixed-offset prime-sieve cases, exact rational densities and interval errors.
- `squarefree_sieve.json`, `squarefree_sieve.md`: thirteen finite prime-square-sieve cases, including singular roots and empty/repeated offsets.

The default README commands regenerate these files. Alternative output directories keep custom runs separate. The sieve tables concern fixed offsets; the witness table varies offsets at each center. Prime-square survival excludes only the selected squares. No table is an asymptotic assertion.
