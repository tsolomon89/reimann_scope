# Experiment Run Digest — Transcendental Continuation Zero Worldline and Radial Invariant Sweep

**Run ID:** `20260821T143617Z_transcendental-worldlines-001_6c9c685a`  
**Experiment ID:** `transcendental-worldlines-001`  
**Status:** `COMPLETE`  
**Criterion Outcome:** **INCOMPLETE / INVALID**

---

## 1. Mathematical Statement & Criterion

- **Hypothesis:**  
  > For any zero rho = 1/2 + delta + i*gamma, the transformed zero s_rho(k) = tau^k * rho is an exact zero of Z_tau(s, k), and its normalized radial coordinate R_tau(s_rho(k), k) = delta identically.

- **Primary Criterion (max_abs):** `max_residual <= 1e-45`
- **Observed Metric:** `N/A`
- **Criterion Met:** `None`

*Note: This result applies strictly to the evaluated finite parameter space. It does not constitute proof or refutation of broader conjectures.*

---

## 2. Multi-Metric Summary

| Metric | Classification | Count | Min | Max | Max Abs |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `max_residual` | `criterion_component` | 0 | `N/A` | `N/A` | `N/A` |
| `zeta_residual` | `criterion_component` | 0 | `N/A` | `N/A` | `N/A` |
| `radial_residual` | `criterion_component` | 0 | `N/A` | `N/A` | `N/A` |

---

## 3. Metric Diagnostics & Worst Points

### `max_residual`
- **Classification:** `criterion_component`
- **Description:** Combined maximum residual
- **Max Absolute Value:** `N/A`

### `zeta_residual`
- **Classification:** `criterion_component`
- **Description:** Residual of Z_tau at transformed zero point
- **Max Absolute Value:** `N/A`

### `radial_residual`
- **Classification:** `criterion_component`
- **Description:** Radial coordinate error |R_tau(s, k) - delta|
- **Max Absolute Value:** `N/A`

---

## 4. Execution & Environment Metadata

- **Git Commit:** `624ce7b4bbfd93a547871022b9d884533fa5c207` (Dirty: `True`)
- **Precision:** `80 dps`
- **Tau Value:** `6.2831853071795864769252...`
- **Points Requested:** `99`
- **Points Completed:** `99`
- **Started At:** `2026-08-21T14:36:17.328518+00:00`
- **Completed At:** `2026-08-21T14:36:17.862889+00:00`

---

## 5. Artifact Index

- Manifest: [`manifest.json`](manifest.json)
- Summary: [`summary.json`](summary.json)
- Detailed Points: [`results.jsonl`](results.jsonl)
