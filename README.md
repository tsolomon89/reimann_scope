# Riemann Microscope / Macroscope

Minimal interactive research instrument for visualizing the Riemann zeta function, its zeros, scale transformations, and the explicit-formula relationship between zeros and primes.

## Authority

- `SPEC.md` is authoritative for mathematical and product behavior.
- `MATH_CONTRACT.md` is authoritative for exact identities, invariants, and implementation-level mathematical tests.
- `DATA_PROVENANCE.md` is authoritative for trusted external datasets and validation rules.
- `DECISIONS.md` is append-only and records consequential implementation decisions.

If code behavior conflicts with these documents, treat the conflict as a bug until resolved.

## Scope

The app should let a user:

- plot the complex trace of \(\zeta(s)\);
- see the corresponding sampling path in the \(s\)-plane;
- discover zeros computationally;
- validate baseline zeros against an independent reference dataset;
- apply explicit camera, coordinate, argument, and kernel transformations;
- see where the critical line and zeros move under those transforms;
- reconstruct the prime staircase from zeta zeros;
- perturb an individual zero and see the converter response;
- inspect the exact tau-grade radial amplification
  \[
  q_\rho^K=\tau^{K(\rho-\frac12)}.
  \]

It is not a proof engine or theorem-scoring system.

## Preferred stack

- Python 3.12+
- Plotly Dash
- `python-flint` / Arb for high-precision zeta and root refinement where practical
- `mpmath` as secondary/fallback
- NumPy for arrays and caching
- Pytest for tests

Do not introduce a separate frontend unless a concrete limitation requires it.

## Expected repository

```text
riemann-microscope/
    app.py
    math_core.py
    transforms.py
    zero_finder.py
    converter.py
    cache.py
    reference_data.py
    data/
        zeros_reference.*
        primes.*
        provenance.json
    tests/
        test_zeta_values.py
        test_zero_finder.py
        test_transforms.py
        test_kernel_lab.py
        test_converter.py
        test_perturbation.py
    SPEC.md
    MATH_CONTRACT.md
    DATA_PROVENANCE.md
    DECISIONS.md
    README.md
```

## Install

Use a virtual environment.

```bash
python -m venv .venv
```

Activate it, then install the project dependencies.

The coding agent should create a pinned `requirements.txt` or `pyproject.toml` once the implementation stack is confirmed.

## Run

Expected local command:

```bash
python app.py
```

The app should start locally and print the address to open in a browser.

## Test

```bash
pytest -q
```

Mathematical trust tests must pass before UI polish or exploratory use.

## Compute tiers

### Preview

Used while dragging controls.

Target:

- 30–40 decimal digits
- ~200–500 path samples
- cached/reduced zero work
- interactive latency under ~200 ms where practical

### Audit

Used on slider release or explicit high-precision action.

Target:

- 80+ decimal digits
- ~1,000–5,000 path samples
- full selected zero count
- independent recomputation

The UI must always show which tier is active.

## Baseline startup behavior

At default \(k=0\):

1. evaluate the critical-line zeta trace;
2. discover zeros without using the external reference table as seeds;
3. refine discovered roots;
4. verify residuals against \(\zeta\);
5. compare afterward against the vendored reference-zero snapshot;
6. show validation statistics.

## Definition of done

The MVP is complete when a user can:

- recognize the critical-line zeta trace;
- see where it is sampled in the \(s\)-plane;
- see the program independently discover and validate known zeros;
- move \(k,A,B,\delta,\gamma\) and always know what mathematical object changed;
- see the transformed critical line move or remain fixed according to the selected transform;
- compare baseline and transformed traces;
- change the zero count in the converter and watch the prime reconstruction respond;
- move one zero off the line and see the clean/perturbed difference immediately;
- inspect the exact \(\tau^{K\delta}\) amplification independently of aggregate reconstruction noise.

When this works, stop. Do not add a proof-program layer.
