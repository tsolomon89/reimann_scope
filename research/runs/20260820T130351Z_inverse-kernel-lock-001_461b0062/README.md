# Experiment Run Digest — Exact Dirichlet kernel pairing preservation under inverse scale lock AB=1

**Run ID:** `20260820T130351Z_inverse-kernel-lock-001_461b0062`  
**Experiment ID:** `inverse-kernel-lock-001`  
**Status:** `COMPLETE`  
**Criterion Outcome:** **CRITERION MET**

---

## 1. Mathematical Statement & Criterion

- **Hypothesis:**  
  > When Inverse Scale Lock is active (AB=1) with shifts C=D=0, the analytically continued kernel transformation Z_{A,0,1/A,0}(s) is identically equal to zeta(s), achieving maximum absolute difference <= 1e-30 across sample domain points at 80 dps.

- **Primary Criterion:** `abs_diff <= 1e-30`
- **Observed Metric:** `0.0`
- **Criterion Met:** `True`

*Note: This result applies strictly to the evaluated finite parameter space. It does not constitute proof or refutation of broader conjectures.*

---

## 2. Multi-Metric Summary

| Metric | Classification | Count | Min | Max | Max Abs |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `abs_diff` | `primary_criterion` | 100 | `0.0` | `0.0` | `0.0` |

---

## 3. Metric Diagnostics & Worst Points

### `abs_diff`
- **Classification:** `primary_criterion`
- **Description:** Primary criterion metric: abs_diff
- **Max Absolute Value:** `0.0`
- **Argmax Parameter Point (id=0):** `A=0.25, inverse_scale_lock=true, C=0.0, D=0.0, s_re=0.5, s_im=10.000000000000000000000000000000000000000000000000000000000000000000000000000000`
- **Top Worst Parameter Points:**
  - id=0 | `val=0.0` | `A=0.25, inverse_scale_lock=true, C=0.0, D=0.0, s_re=0.5, s_im=10.000000000000000000000000000000000000000000000000000000000000000000000000000000`
  - id=1 | `val=0.0` | `A=0.25, inverse_scale_lock=true, C=0.0, D=0.0, s_re=0.5, s_im=15.000000000000000000000000000000000000000000000000000000000000000000000000000000`
  - id=2 | `val=0.0` | `A=0.25, inverse_scale_lock=true, C=0.0, D=0.0, s_re=0.5, s_im=20.000000000000000000000000000000000000000000000000000000000000000000000000000000`
  - id=3 | `val=0.0` | `A=0.25, inverse_scale_lock=true, C=0.0, D=0.0, s_re=0.5, s_im=25.000000000000000000000000000000000000000000000000000000000000000000000000000000`
  - id=4 | `val=0.0` | `A=0.25, inverse_scale_lock=true, C=0.0, D=0.0, s_re=0.5, s_im=30.000000000000000000000000000000000000000000000000000000000000000000000000000000`

---

## 4. Execution & Environment Metadata

- **Git Commit:** `10be6b46af780f66dab638540ec67e0dfaaf9d2e` (Dirty: `False`)
- **Precision:** `80 dps`
- **Tau Value:** `6.2831853071795864769252...`
- **Points Requested:** `100`
- **Points Completed:** `100`
- **Started At:** `2026-08-20T13:03:51.632296+00:00`
- **Completed At:** `2026-08-20T13:03:52.546155+00:00`

---

## 5. Artifact Index

- Manifest: [`manifest.json`](manifest.json)
- Summary: [`summary.json`](summary.json)
- Detailed Points: [`results.jsonl`](results.jsonl)
