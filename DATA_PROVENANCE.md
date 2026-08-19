# Data Provenance Contract

This file governs external mathematical data used by the Riemann Microscope / Macroscope.

The purpose is reproducibility and independence between **discovery** and **validation**.

## 1. Core rule

Reference zeros validate the zero finder. They must **never** seed the baseline zero-discovery algorithm.

Required order:

1. scan the function;
2. discover candidate zeros;
3. refine them;
4. verify the zeta residual;
5. compare afterward against reference data.

If the zero finder uses the reference table to choose candidate locations, the validation is invalid.

## 2. Reference zeta zeros

The implementation agent must select a reputable public source of rigorously computed nontrivial Riemann-zeta zeros.

Preference order:

1. primary mathematical computation/database source with documented rigor and precision;
2. recognized research database maintained by mathematicians;
3. original published/computed dataset with clear provenance.

Do not use an unattributed list copied from a blog, forum, or random repository.

The implementation step may browse the web to choose and retrieve the source. Runtime must not require internet access.

## 3. Vendored zero snapshot

For MVP, vendor a deterministic subset of approximately

\[
10^3\text{ to }10^4
\]

positive ordinates.

Suggested location:

```text
data/zeros_reference.*
```

Accompany it with:

```text
data/provenance.json
```

Metadata must contain at least:

- dataset name;
- source organization / author;
- source URL;
- retrieval date;
- original stated precision;
- number of records vendored;
- first ordinate;
- last ordinate;
- file format;
- SHA-256 checksum;
- preparation-script version or git commit;
- notes on transformation from the original source.

## 4. Retrieval/preparation script

Create a small reproducible script such as:

```text
scripts/fetch_reference_zeros.py
```

It should:

1. retrieve the chosen source;
2. parse only the required subset;
3. preserve precision as decimal strings;
4. validate monotonic ordering;
5. write the vendored snapshot;
6. compute SHA-256;
7. write/update provenance metadata.

Do not require this script during ordinary app startup.

## 5. Zero-validation report

At baseline \(k=0\), compare independently discovered zeros with the vendored reference list.

Report:

- t-range searched;
- discovered-zero count;
- reference-zero count in range;
- matched count;
- maximum
  \[
  |\gamma_{\mathrm{found}}-\gamma_{\mathrm{ref}}|;
  \]
- RMS difference;
- unmatched discovered roots;
- unmatched reference roots;
- zeta residual statistics;
- precision tier used.

A validation PASS means only that the baseline finder agrees with the reference source within the declared range and tolerance. It does not prove RH.

## 6. Prime data

For a modest MVP range, prefer generating the prime table locally with a deterministic sieve rather than downloading a large external asset.

Record:

- generation algorithm;
- maximum \(x\);
- generated prime count;
- SHA-256 checksum if persisted.

If a larger external prime dataset is later used, apply the same provenance requirements as the zero table.

The true \(\pi(x)\) baseline must not be produced by the same approximate explicit-formula reconstruction being tested.

## 7. Constants

Compute

\[
\tau=2\pi
\]

from the high-precision numeric library rather than treating a hand-entered decimal as authoritative.

If cached, record library, precision, and checksum.

## 8. Numerical precision

Store reference ordinates as strings or exact decimal text.

Do not load them through ordinary binary float before comparison.

Reference matching must occur in the same high-precision numeric environment used for zero refinement.

## 9. Transform validation

For \(k\neq0\) or other transformed functions:

- do not create a second external zero dataset;
- independently discover transformed zeros;
- calculate predicted mapped zeros from the exact transform;
- compare discovered vs predicted.

The original external zero table is only the independent baseline anchor.

## 10. Provenance changes

Any change to zero source, source precision, vendored count, file normalization, prime-generation method, or checksum must update `data/provenance.json`.

Append a note to `DECISIONS.md` if the change alters the mathematical trust model.

## 11. Initial provenance template

```json
{
  "zeta_zeros": {
    "source_name": "TBD",
    "source_author_or_org": "TBD",
    "source_url": "TBD",
    "retrieved_at": "TBD",
    "stated_precision": "TBD",
    "vendored_count": 0,
    "first_ordinate": "TBD",
    "last_ordinate": "TBD",
    "format": "decimal strings",
    "sha256": "TBD",
    "preparation_script": "scripts/fetch_reference_zeros.py"
  },
  "primes": {
    "source": "locally generated",
    "algorithm": "TBD",
    "max_x": 0,
    "sha256": "TBD"
  },
  "tau": {
    "source": "high-precision library",
    "library": "TBD",
    "precision_digits": 0
  }
}
```
