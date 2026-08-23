# Experiment Run Digest — Radial Centrifuge Logarithmic Slope Verification

**Run ID:** `centrifuge-slope-verification`
**Experiment ID:** `centrifuge-slope-verification`
**Status:** `COMPLETE`
**Criterion Outcome:** **CRITERION MET**

---

## 1. Mathematical Statement & Criterion

- **Hypothesis:**
  > The discrete radial amplification factor satisfies d/dK [ log |q_rho^K| ] = delta * ln(tau) identically.

- **Primary Criterion (max_abs):** `abs_slope_error <= 1e-45`
- **Observed Metric:** `0.0`
- **Criterion Met:** `True`

*Note: This result applies strictly to the evaluated finite parameter space. It does not constitute proof or refutation of broader conjectures.*

---

## 2. Multi-Metric Summary

| Metric | Classification | Count | Min | Max | Max Abs |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `abs_slope_error` | `criterion_component` | 11 | `0.0` | `0.0` | `0.0` |

---

## 3. Metric Diagnostics & Worst Points

### `abs_slope_error`
- **Classification:** `criterion_component`
- **Description:** Absolute slope error
- **Max Absolute Value:** `0.0`
- **Argmax Parameter Point (id=0):** `val=0.0` | `delta=-0.10000000000000000000000000000000000000000000000000000000000000000000000000000000, K_max=20`
- **Top Worst Parameter Points:**
  - id=0 | `val=0.0` | `delta=-0.10000000000000000000000000000000000000000000000000000000000000000000000000000000, K_max=20`
  - id=1 | `val=0.0` | `delta=-0.080000000000000000000000000000000000000000000000000000000000000000000000000000000, K_max=20`
  - id=2 | `val=0.0` | `delta=-0.060000000000000000000000000000000000000000000000000000000000000000000000000000000, K_max=20`
  - id=3 | `val=0.0` | `delta=-0.040000000000000000000000000000000000000000000000000000000000000000000000000000000, K_max=20`
  - id=4 | `val=0.0` | `delta=-0.020000000000000000000000000000000000000000000000000000000000000000000000000000000, K_max=20`

---

## 4. Execution & Environment Metadata

- **Git Commit:** `b1e4d97d091b3256a16d42e36943d205ad51e367` (Dirty: `False`)
- **Precision:** `80 dps`
- **Tau Value:** `6.2831853071795864769252... (2*pi)`
- **Points Requested:** `11`
- **Points Completed:** `11`
- **Started At:** `2026-08-23T07:59:49.455865+00:00`
- **Completed At:** `2026-08-23T07:59:49.461060+00:00`

---

## 5. Artifact Index

- Manifest: [`manifest.json`](manifest.json)
- Summary: [`summary.json`](summary.json)
- Detailed Points: [`results.jsonl`](results.jsonl)
