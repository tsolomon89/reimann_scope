# Data Provenance Contract

This file governs external mathematical data used by `reimann_scope`.

The core goals are:

- reproducibility;
- independence between discovery and validation;
- explicit distinction between validation data and research-input data;
- support for sparse high-zero blocks;
- preservation of symbolic grade identity alongside finite numerical realization.

---

# 1. Core discovery/validation rule

When validating the baseline zero finder, reference zeros must not seed the discovery algorithm.

Required order:

1. scan the function;
2. identify candidates;
3. refine candidates;
4. verify residuals;
5. compare afterward against the independent reference data.

If the reference table determines the candidate locations, that run is not independent discovery validation.

---

# 2. Two zero-data roles

Every zero block must declare one role.

## 2.1 `validation`

Purpose:

> independently validate the app's zero-discovery/refinement machinery.

Reference coordinates must not seed the discovery being validated.

## 2.2 `research_input`

Purpose:

> provide trusted actual zero coordinates for a structural experiment, especially at very high heights where independent discovery from scratch is not the experimental claim.

This role may directly supply zero coordinates.

A research-input block must never be described as independently discovered by the application.

---

# 3. Source quality

Preference order:

1. primary mathematical computation/database source with documented methods, rigor, and precision;
2. recognized research database maintained by specialists;
3. original published computational dataset with clear provenance.

Do not use:

- unattributed blog lists;
- forum copies;
- random repositories without traceable provenance;
- rounded values when higher-precision originals are available.

The implementation workflow may use internet research to retrieve data.

Runtime should not require internet access.

---

# 4. Block-based zero architecture

Do not model the data as one ever-growing contiguous low-zero file.

Support independent immutable blocks.

Suggested structure:

```text
data/
    zeros/
        low_validation_v1.txt
        medium_research_v1.txt
        high_research_v1.txt
        very_high_sparse_v1.txt
    provenance.json
```

The exact filenames may differ, but block identity must remain explicit.

---

# 5. Required block metadata

Each zero block must include:

```json
{
  "block_id": "very-high-sparse-v1",
  "role": "research_input",
  "source_name": "...",
  "source_author_or_org": "...",
  "source_url": "...",
  "retrieved_at": "...",
  "source_method_notes": "...",
  "zero_index_start": null,
  "zero_index_end": null,
  "ordinate_min": "...",
  "ordinate_max": "...",
  "record_count": 0,
  "stated_source_precision": "...",
  "stored_precision": "...",
  "format": "decimal strings",
  "sha256": "...",
  "preparation_script": "...",
  "preparation_git_commit": "...",
  "notes": "..."
}
```

If the source provides exact zero indices, preserve them.

If it does not, leave them null rather than inventing them.

---

# 6. Required block types for the central campaign

The architecture should support at least:

### Low validation block

Purpose:

- zero-finder regression;
- familiar numerical checks;
- reference matching.

### Medium research block

Purpose:

- cross-height comparison beyond the first low zeros.

### High research block

Purpose:

- test claimed height-independent behavior.

### Very-high sparse research block

Purpose:

- test the programme against genuinely remote actual zeta geometry without requiring a giant contiguous dataset.

### Optional unusual-gap block

Purpose:

- stress-test coherence against atypical local zero spacing.

These are research roles, not a claim that any finite block is representative of the entire spectrum.

---

# 7. Retrieval/preparation scripts

Use reproducible scripts such as:

```text
scripts/fetch_reference_zeros.py
scripts/prepare_zero_blocks.py
```

They should:

1. retrieve the source or consume a documented local source file;
2. preserve decimal precision as text;
3. parse only declared records;
4. validate ordering where appropriate;
5. validate indices where available;
6. write deterministic blocks;
7. compute SHA-256;
8. update provenance metadata;
9. record preparation code version.

Do not require retrieval scripts during ordinary app startup.

---

# 8. Baseline zero-validation report

For a validation block, report:

- searched \(t\)-range;
- discovered count;
- reference count in range;
- matched count;
- maximum
  \[
  |\gamma_{\mathrm{found}}-\gamma_{\mathrm{ref}}|;
  \]
- RMS ordinate difference;
- unmatched discovered roots;
- unmatched reference roots;
- zeta residual statistics;
- precision tier;
- discovery method;
- whether any completeness claim is justified.

A PASS means only agreement with the reference block under the declared method and tolerance.

It is not proof of RH.

---

# 9. High-zero research-input report

When using a research-input block, record:

- exact block ID/checksum;
- selected indices/ordinates;
- source precision;
- local reevaluation precision;
- local zeta residual;
- derivative value/conditioning if derivative normalization is used;
- any source uncertainty;
- whether the point was independently rediscovered or directly supplied.

Do not silently upgrade research-input coordinates into independent discovery results.

---

# 10. Zero simplicity and derivative normalization

The cross-height path

\[
P_n(u)
=
\frac{
\zeta(\frac12+i(\gamma_n+\Delta_nu))
}{
i\Delta_n\zeta'(\rho_n)
}
\]

requires a numerically well-conditioned nonzero derivative.

For every zero used this way, persist:

```json
{
  "zeta_prime_abs": "...",
  "simplicity_check_method": "...",
  "conditioning_warning": false
}
```

Do not claim a general theorem that all zeta zeros are simple.

The experiment only needs the selected zero to satisfy the declared numerical condition.

---

# 11. Prime data

For modest ranges, prefer deterministic local generation by sieve.

Record:

- algorithm;
- maximum \(x\);
- prime count;
- code version;
- checksum if persisted.

The true \(\pi(x)\) comparison baseline must not be generated by the same approximate explicit formula being tested.

If an external prime dataset is used, apply the same provenance standards as zero blocks.

---

# 12. Tau and constants

The symbolic authoritative constant is

\[
\boxed{\tau=2\pi.}
\]

For numerical work, compute it from the active high-precision library.

Do not treat a hand-entered decimal expansion as authoritative.

When a run persists a numerical realization, record:

```json
{
  "symbolic": "2*pi",
  "library": "...",
  "precision_digits": 100,
  "numeric": "..."
}
```

The exact symbolic referent and finite numerical realization are separate metadata.

---

# 13. Grade metadata

For any data derived under a canonical grade, persist the exact grade expression.

Integer example:

```json
{
  "grade_type": "integer",
  "K": "-7",
  "scale_symbolic": "tau^-7",
  "scale_numeric": "..."
}
```

Rational example:

```json
{
  "grade_type": "rational",
  "q": "3/2",
  "scale_symbolic": "tau^(3/2)",
  "scale_numeric": "..."
}
```

Continuous real example:

```json
{
  "grade_type": "continuous",
  "k_input": "0.123456789",
  "scale_symbolic": "tau^k",
  "scale_numeric": "..."
}
```

Do not discard the grade identity after evaluating its decimal value.

---

# 14. Numerical precision

Reference ordinates and authoritative calculated values should be stored as:

- decimal strings;
- exact integers/rationals where applicable;
- symbolic grade metadata.

Do not load reference values through ordinary binary float before high-precision comparison.

All authoritative matching should occur in the same high-precision environment used for the mathematical metric.

---

# 15. Preview versus Audit

### Preview

May use reduced precision and float rendering.

Preview output is never the provenance-authoritative mathematical result.

### Audit

Uses arbitrary/high precision and records:

- requested dps;
- effective library;
- source precision;
- truncation parameters;
- interval/enclosure information where applicable.

Do not claim more precision than the source data support.

---

# 16. Transformed-zero validation

For a declared exact transform:

1. compute the algebraically predicted transformed coordinates;
2. independently discover/refine the transformed function's zeros where the validation claim requires independence;
3. compare afterward.

Do not create a second external transformed-zero dataset merely by transforming the baseline reference list and then call it independent data.

The transformed reference is a prediction, not an external validation source.

---

# 17. Transcendental-continuation worldline data

For a native zero \(\rho\), a worldline point is

\[
s_{\rho,K}=\tau^K\rho.
\]

Persist:

- native zero block ID;
- native zero index/ordinate;
- grade;
- symbolic transformed coordinate expression where practical;
- numerical transformed coordinate;
- critical-surface coordinate;
- normalized radial coordinate;
- residual of the transformed function.

Do not claim that arithmetic lattice noncoincidence proves transformed zero-worldline noncoincidence.

---

# 18. Data for synthetic perturbations

Synthetic off-line zeros are not external data.

Persist them separately under a synthetic descriptor:

```json
{
  "synthetic": true,
  "construction": "reflection_complete_quartet",
  "baseline_zero": "...",
  "delta": "...",
  "gamma": "...",
  "grade": "..."
}
```

Never merge synthetic coordinates into the trusted actual-zero dataset.

---

# 19. Converter provenance

Every authoritative converter run records:

- zero block(s);
- zero count/cutoff;
- branch convention;
- \(x\)-range;
- Möbius truncation rule;
- remainder-series tolerance;
- precision;
- prime baseline generation method/checksum.

The clean and perturbed converter must share all settings except the explicitly declared perturbation.

---

# 20. Provenance changes

Any change to:

- zero source;
- source precision;
- block content;
- block role;
- file normalization;
- prime-generation method;
- tau numeric library;
- branch convention;
- preparation script;
- checksum;
- high-zero selection semantics

must update `data/provenance.json`.

If the change alters the mathematical trust model, add a decision to `DECISIONS.md`.

---

# 21. Recommended provenance schema

```json
{
  "schema_version": "2",
  "zero_blocks": [
    {
      "block_id": "low-validation-v1",
      "role": "validation",
      "source_name": "TBD",
      "source_author_or_org": "TBD",
      "source_url": "TBD",
      "retrieved_at": "TBD",
      "zero_index_start": 1,
      "zero_index_end": 1000,
      "ordinate_min": "TBD",
      "ordinate_max": "TBD",
      "record_count": 1000,
      "stated_source_precision": "TBD",
      "stored_precision": "TBD",
      "format": "decimal strings",
      "sha256": "TBD",
      "preparation_script": "scripts/prepare_zero_blocks.py",
      "preparation_git_commit": "TBD"
    }
  ],
  "primes": {
    "source": "locally generated",
    "algorithm": "TBD",
    "max_x": 0,
    "count": 0,
    "sha256": "TBD"
  },
  "tau": {
    "symbolic": "2*pi",
    "source": "high-precision library",
    "library": "TBD",
    "precision_digits": 0
  }
}
```

---

# 22. Definition of done

The provenance layer is adequate when:

1. validation and research-input zero roles cannot be confused;
2. low and sparse high blocks can coexist;
3. every current research run identifies exact source block checksums;
4. source precision is never overstated;
5. derivative-normalized experiments record conditioning;
6. symbolic grade identity survives into run artifacts;
7. transformed zeros are not falsely described as independent external data;
8. synthetic data remain segregated;
9. the converter is fully reproducible from persisted metadata.
